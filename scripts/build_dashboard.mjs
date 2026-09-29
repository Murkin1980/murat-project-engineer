#!/usr/bin/env node
/**
 * Production build for the MPE portfolio dashboard (Cloudflare static hosting).
 *
 * The dashboard is a committed static snapshot: `dashboard/public/` is the only
 * source of truth (HTML + the generated Reladraw SVG views). This build does not
 * transform, bundle or fetch anything — it assembles the deployable output
 * directory declared in `wrangler.jsonc` (`assets.directory`) and then verifies
 * that the deployable artifact is complete before Cloudflare can ship it.
 *
 * Fail-closed rules:
 *   - the output directory is synced from the source (no stale files survive);
 *   - every asset referenced by `index.html` must exist and stay byte-identical;
 *   - the desktop Reladraw view and every mobile status view must be present;
 *   - mobile views must keep the 390px readable-size contract;
 *   - on any failure the output directory is removed, so a broken artifact can
 *     never be uploaded.
 *
 * The sync only rewrites files whose bytes changed. A running `wrangler dev`
 * therefore keeps serving valid assets while a rebuild happens.
 *
 * Zero dependencies, Node >= 20. Usage: node scripts/build_dashboard.mjs
 */

import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, "..");
const SOURCE_DIR = path.join(ROOT, "dashboard", "public");
const WRANGLER_CONFIG = path.join(ROOT, "wrangler.jsonc");
const MOBILE_MAX_WIDTH_PX = 390;
const MOBILE_FONT_SIZE = "14px";

/** Minimal JSONC reader: strip // and /* *\/ comments, then JSON.parse. */
function readWranglerConfig(file) {
  const text = fs.readFileSync(file, "utf8");
  const stripped = text
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/^\s*\/\/.*$/gm, "");
  return JSON.parse(stripped);
}

function resolveOutputDir(config) {
  const declared = config?.assets?.directory;
  if (!declared) {
    throw new Error("wrangler.jsonc must declare assets.directory");
  }
  const outputDir = path.resolve(ROOT, declared);
  if (!outputDir.startsWith(ROOT + path.sep)) {
    throw new Error(`assets.directory must stay inside the repository: ${declared}`);
  }
  if (outputDir === ROOT) {
    throw new Error("assets.directory must not be the repository root");
  }
  if (outputDir === SOURCE_DIR || outputDir.startsWith(SOURCE_DIR + path.sep)) {
    throw new Error("assets.directory must not point at the committed source directory");
  }
  return outputDir;
}

function listFiles(dir, base = dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...listFiles(full, base));
    } else if (entry.isFile()) {
      out.push(path.relative(base, full).split(path.sep).join("/"));
    }
  }
  return out;
}

/** Absolute asset references (`src` / `href`) used by the dashboard page. */
function referencedAssets(html) {
  const refs = new Set();
  const pattern = /(?:src|href)="(\/[^"#]*)"/g;
  let match;
  while ((match = pattern.exec(html)) !== null) {
    refs.add(match[1]);
  }
  return [...refs].sort();
}

function sha256(file) {
  return createHash("sha256").update(fs.readFileSync(file)).digest("hex").slice(0, 12);
}

function readSvgHead(file, bytes = 600) {
  const fd = fs.openSync(file, "r");
  const buffer = Buffer.alloc(bytes);
  const read = fs.readSync(fd, buffer, 0, bytes, 0);
  fs.closeSync(fd);
  return buffer.subarray(0, read).toString("utf8");
}

function checkMobileView(relPath, file, failures) {
  const head = readSvgHead(file);
  const width = /width="(\d+)"/.exec(head);
  const fontSize = /font-size="([^"]+)"/.exec(head);
  if (!width) {
    failures.push(`${relPath}: no explicit width attribute`);
    return;
  }
  if (Number(width[1]) > MOBILE_MAX_WIDTH_PX) {
    failures.push(`${relPath}: width ${width[1]}px exceeds the ${MOBILE_MAX_WIDTH_PX}px mobile budget`);
  }
  if (!fontSize || fontSize[1] !== MOBILE_FONT_SIZE) {
    failures.push(`${relPath}: font-size must stay ${MOBILE_FONT_SIZE}, found ${fontSize ? fontSize[1] : "none"}`);
  }
}

/**
 * Sync `src` into `dest`: write only files whose bytes changed, then remove
 * anything in `dest` that no longer exists in `src` (including empty folders).
 * Returns the number of written files.
 */
function syncDirectory(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const expected = new Set();
  let written = 0;
  for (const rel of listFiles(src)) {
    expected.add(rel);
    const bytes = fs.readFileSync(path.join(src, rel));
    const target = path.join(dest, rel);
    if (fs.existsSync(target) && fs.readFileSync(target).equals(bytes)) continue;
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, bytes);
    written += 1;
  }
  for (const rel of listFiles(dest)) {
    if (!expected.has(rel)) fs.rmSync(path.join(dest, rel), { force: true });
  }
  removeEmptyDirs(dest);
  return written;
}

function removeEmptyDirs(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) removeEmptyDirs(path.join(dir, entry.name));
  }
  if (fs.readdirSync(dir).length === 0 && dir !== ROOT) fs.rmdirSync(dir);
}

function build() {
  const failures = [];
  const config = readWranglerConfig(WRANGLER_CONFIG);
  const outputDir = resolveOutputDir(config);

  if (!fs.existsSync(path.join(SOURCE_DIR, "index.html"))) {
    throw new Error(`dashboard source is missing index.html: ${SOURCE_DIR}`);
  }

  const written = syncDirectory(SOURCE_DIR, outputDir);

  const html = fs.readFileSync(path.join(outputDir, "index.html"), "utf8");
  const built = new Set(listFiles(outputDir));

  // 1. Every route/asset the page references must be deployable.
  for (const ref of referencedAssets(html)) {
    const rel = ref.replace(/^\//, "");
    if (!built.has(rel)) {
      failures.push(`missing referenced asset: ${ref}`);
      continue;
    }
    const source = path.join(SOURCE_DIR, rel);
    const target = path.join(outputDir, rel);
    if (!fs.readFileSync(source).equals(fs.readFileSync(target))) {
      failures.push(`asset changed during build (must stay byte-identical): ${ref}`);
    }
  }

  // 2. The Reladraw views survive the build: desktop portfolio + every mobile status.
  const desktopView = "registry/portfolio.svg";
  if (!built.has(desktopView)) {
    failures.push(`missing desktop Reladraw view: /${desktopView}`);
  }
  const mobileViews = [...built].filter((file) => file.startsWith("registry/mobile/status-") && file.endsWith(".svg"));
  if (mobileViews.length === 0) {
    failures.push("missing mobile Reladraw status views: registry/mobile/status-*.svg");
  }

  // 3. Mobile 390px contract (same invariant guarded by tests/test_dashboard_registry_views.py).
  for (const view of mobileViews) {
    checkMobileView(view, path.join(outputDir, view), failures);
  }
  for (const invariant of [
    '<meta name="viewport" content="width=device-width,initial-scale=1">',
    "width:min(calc(100vw - 28px),1649px)",
    "margin:10px -14px",
  ]) {
    if (!html.includes(invariant)) {
      failures.push(`index.html lost a responsive invariant: ${invariant}`);
    }
  }

  // 4. No repository internals may leak into the deployable output.
  for (const forbidden of [".git", ".env", "node_modules", "wrangler.jsonc", "package.json"]) {
    if (built.has(forbidden) || [...built].some((file) => file.startsWith(`${forbidden}/`))) {
      failures.push(`deploy output must not contain: ${forbidden}`);
    }
  }

  if (failures.length > 0) {
    fs.rmSync(outputDir, { recursive: true, force: true });
    console.error("DASHBOARD BUILD FAILED");
    for (const failure of failures) {
      console.error(`- ${failure}`);
    }
    return 1;
  }

  const totalBytes = [...built].reduce((sum, file) => sum + fs.statSync(path.join(outputDir, file)).size, 0);
  console.log("DASHBOARD BUILD PASSED");
  console.log(`source:      ${path.relative(ROOT, SOURCE_DIR) || "."}`);
  console.log(`output dir:  ${path.relative(ROOT, outputDir)}`);
  console.log(`assets:      ${built.size} files, ${totalBytes} bytes (${written} written, ${built.size - written} unchanged)`);
  console.log(`views:       desktop /${desktopView}; mobile ${mobileViews.length} status views (<= ${MOBILE_MAX_WIDTH_PX}px, ${MOBILE_FONT_SIZE})`);
  for (const file of [...built].sort()) {
    const size = fs.statSync(path.join(outputDir, file)).size;
    console.log(`  ${sha256(path.join(outputDir, file))}  ${String(size).padStart(6)} B  /${file}`);
  }
  return 0;
}

try {
  process.exit(build());
} catch (error) {
  console.error(`DASHBOARD BUILD FAILED\n- ${error.message}`);
  process.exit(1);
}
