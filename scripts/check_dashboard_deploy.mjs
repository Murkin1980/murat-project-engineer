#!/usr/bin/env node
/**
 * Deploy readiness check for the MPE dashboard on Cloudflare static hosting.
 *
 * Local mode (default, `npm run check`):
 *   1. runs the production build (`scripts/build_dashboard.mjs`);
 *   2. serves the output directory with Cloudflare-compatible routing;
 *   3. requests every dashboard route and every referenced asset.
 *
 * Remote/workerd mode (`--base-url`): runs the same route, asset, view and
 * 390px checks against an already-served site — `wrangler dev`, or the deployed
 * Workers URL after a manual deploy.
 *
 * Both modes verify that served bytes stay identical to the committed source in
 * `dashboard/public/`, that the desktop and mobile Reladraw views survive, and
 * that the mobile views keep the 390px readable-size contract.
 *
 * Exits non-zero on any failure, so it is safe as a pre-deploy gate.
 * Zero dependencies, Node >= 20.
 */

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import { startPreview } from "./preview_dashboard.mjs";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, "..");
const SOURCE_DIR = path.join(ROOT, "dashboard", "public");
const MOBILE_MAX_WIDTH_PX = 390;
const MOBILE_FONT_SIZE = "14px";

const checks = [];
function record(category, target, ok, detail) {
  checks.push({ category, target, ok: Boolean(ok), detail });
}

function readJsonc(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/\/\*[\s\S]*?\*\//g, "").replace(/^\s*\/\/.*$/gm, ""));
}

function referencedAssets(html) {
  const refs = new Set();
  const pattern = /(?:src|href)="(\/[^"#]*)"/g;
  let match;
  while ((match = pattern.exec(html)) !== null) refs.add(match[1]);
  return [...refs].sort();
}

function parseArgs(argv) {
  const options = { baseUrl: null };
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (flag === "--base-url") options.baseUrl = argv[++index];
    else if (flag === "--help" || flag === "-h") options.help = true;
    else throw new Error(`unknown argument: ${flag}`);
  }
  if (options.baseUrl) options.baseUrl = options.baseUrl.replace(/\/$/, "");
  return options;
}

function runBuild() {
  const result = spawnSync(process.execPath, [path.join(SCRIPT_DIR, "build_dashboard.mjs")], {
    cwd: ROOT,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
  process.stdout.write(result.stdout ?? "");
  process.stderr.write(result.stderr ?? "");
  record("build", "npm run build", result.status === 0, `exit ${result.status}`);
  return result.status === 0;
}

function checkConfig() {
  const config = readJsonc(path.join(ROOT, "wrangler.jsonc"));
  const packageJson = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8"));
  const dist = path.resolve(ROOT, config.assets.directory);
  record("config", "worker name", config.name === "murat-project-engineer", String(config.name));
  record("config", "output directory", path.relative(ROOT, dist) === "dist", path.relative(ROOT, dist));
  record("config", "build command", config.build?.command === "node scripts/build_dashboard.mjs", String(config.build?.command));
  record("config", "npm build command", packageJson.scripts?.build === config.build?.command, String(packageJson.scripts?.build));
  record(
    "config",
    "assets routing",
    config.assets?.html_handling === "auto-trailing-slash" &&
      config.assets?.not_found_handling === "single-page-application",
    `${config.assets?.html_handling} / ${config.assets?.not_found_handling}`,
  );
  return dist;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    console.log("Usage: node scripts/check_dashboard_deploy.mjs [--base-url http://127.0.0.1:8787]");
    return 0;
  }

  checkConfig();
  const remote = Boolean(options.baseUrl);
  if (!remote && !runBuild()) return report();

  let base = options.baseUrl;
  let preview = null;
  if (!remote) {
    try {
      preview = await startPreview({ dir: path.resolve(ROOT, "dist") });
      base = preview.url.replace(/\/$/, "");
    } catch (error) {
      record("preview", "start local server", false, error.message);
      return report();
    }
  }
  record("preview", remote ? `target ${base}` : "local static server", Boolean(base), remote ? "external" : preview.url);

  try {
    const indexResponse = await fetch(base + "/");
    const html = await indexResponse.text();
    if (indexResponse.status !== 200 || !html.includes("<!doctype html>")) {
      record("route", "/", false, `${indexResponse.status} — no dashboard HTML served`);
      return report();
    }
    record("route", "/", true, `200 ${indexResponse.headers.get("content-type")}`);

    const assets = referencedAssets(html);

    // --- routes -------------------------------------------------------------
    const routes = [
      { path: "/index.html", expect: { status: 307, location: "/" } },
      { path: "/registry/", expect: { status: 200, type: "text/html", body: html } },
      { path: "/brief", expect: { status: 200, type: "text/html", body: html } },
      { path: "/unknown/deep/route", expect: { status: 200, type: "text/html", body: html } },
    ];
    for (const route of routes) {
      const response = await fetch(base + route.path, { redirect: "manual" });
      const type = response.headers.get("content-type") ?? "";
      const body = response.status === 200 ? await response.text() : "";
      const ok =
        response.status === route.expect.status &&
        (!route.expect.type || type.startsWith(route.expect.type)) &&
        (!route.expect.body || body === route.expect.body) &&
        (!route.expect.location || response.headers.get("location") === route.expect.location);
      record("route", route.path, ok,
        `${response.status} ${type || "-"}` + (route.expect.location ? ` -> ${response.headers.get("location")}` : ""));
    }

    // --- assets served + byte-identical to the committed source --------------
    for (const asset of assets) {
      const response = await fetch(base + asset);
      const served = Buffer.from(await response.arrayBuffer());
      const type = response.headers.get("content-type") ?? "";
      record("asset", asset, response.status === 200 && type.startsWith("image/svg+xml") && served.length > 0,
        `${response.status} ${type} ${served.length}B`);
      const source = fs.readFileSync(path.join(SOURCE_DIR, asset.slice(1)));
      record("parity", asset, served.equals(source), `served ${served.length}B vs committed ${source.length}B`);
    }

    // --- Reladraw views: desktop + mobile preserved -------------------------
    const desktopViews = assets.filter((asset) => asset.startsWith("/registry/") && !asset.includes("/mobile/"));
    const mobileViews = assets.filter((asset) => asset.startsWith("/registry/mobile/"));
    record("views", "desktop portfolio view",
      desktopViews.length === 1 && desktopViews[0] === "/registry/portfolio.svg", desktopViews.join(", ") || "none");
    record("views", "mobile status views", mobileViews.length >= 4, `${mobileViews.length} views`);
    for (const marker of ['class="registry-views registry-desktop"', 'class="registry-views registry-mobile"']) {
      const label = /class="([^"]+)"/.exec(marker)[1];
      record("views", label, html.includes(marker), html.includes(marker) ? "served" : "missing");
    }
    const responsiveRules = [
      ["desktop view at native size", ".registry-desktop .registry-image-frame img{max-width:none}"],
      ["mobile view hidden on desktop", ".registry-mobile{display:none}"],
      ["mobile switch at <=649px", "@media(max-width:649px){.registry-desktop{display:none}.registry-mobile{display:block}"],
    ];
    for (const [label, rule] of responsiveRules) {
      record("views", label, html.includes(rule), html.includes(rule) ? "css served" : "css missing");
    }

    // --- mobile 390px contract on the served bytes --------------------------
    for (const view of mobileViews) {
      const served = await (await fetch(base + view)).text();
      const head = served.slice(0, 600);
      const width = Number(/width="(\d+)"/.exec(head)?.[1] ?? "0");
      const fontSize = /font-size="([^"]+)"/.exec(head)?.[1] ?? "";
      record("mobile-390", view, width > 0 && width <= MOBILE_MAX_WIDTH_PX && fontSize === MOBILE_FONT_SIZE,
        `width ${width}px, font-size ${fontSize || "unset"}`);
    }
    record("mobile-390", "viewport meta",
      html.includes('<meta name="viewport" content="width=device-width,initial-scale=1">'), "served index.html");
    record("mobile-390", "390px layout invariants",
      html.includes("width:min(calc(100vw - 28px),1649px)") && html.includes("margin:10px -14px"), "served index.html");

    // --- dashboard content sanity -------------------------------------------
    for (const marker of ["<title>", 'id="registry"', 'id="brief"', 'id="p0"', 'id="support"', 'id="hold"', 'id="ideas"', "EXPERIMENT_REGISTRY.json"]) {
      record("content", marker, html.includes(marker), html.includes(marker) ? "served" : "missing");
    }
  } finally {
    if (preview) await preview.close();
  }

  return report();
}

function report() {
  const byCategory = new Map();
  for (const check of checks) {
    const list = byCategory.get(check.category) ?? [];
    list.push(check);
    byCategory.set(check.category, list);
  }
  console.log("\nDASHBOARD DEPLOY CHECKS");
  let failed = 0;
  for (const [category, list] of byCategory) {
    const bad = list.filter((check) => !check.ok);
    failed += bad.length;
    console.log(`${bad.length === 0 ? "PASS" : "FAIL"}  ${category} (${list.length - bad.length}/${list.length})`);
    for (const check of list) {
      if (!check.ok || process.env.VERBOSE === "1") {
        console.log(`      ${check.ok ? "ok  " : "FAIL"} ${check.target} — ${check.detail}`);
      }
    }
  }
  const total = checks.length;
  console.log(`\n${failed === 0 ? "ALL CHECKS PASSED" : "CHECKS FAILED"}: ${total - failed}/${total}`);
  return failed === 0 ? 0 : 1;
}

main().then(
  (code) => process.exit(code),
  (error) => {
    console.error(`CHECKS FAILED\n- ${error.stack ?? error.message}`);
    process.exit(1);
  },
);
