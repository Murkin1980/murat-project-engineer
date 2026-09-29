#!/usr/bin/env node
/**
 * Local production preview of the built dashboard.
 *
 * Serves the deploy output directory (`dist/` by default) with the same request
 * semantics Cloudflare Workers Static Assets applies, so a local check means the
 * same thing as the deployed site:
 *
 *   html_handling: "auto-trailing-slash"
 *     /                 -> /index.html
 *     /index.html       -> 307 /
 *     /section          -> 307 /section/  (when section/index.html exists)
 *     /section/         -> section/index.html
 *     /page.html        -> 307 /page
 *   not_found_handling: "single-page-application"
 *     unknown path      -> 200 /index.html
 *
 * Zero dependencies, Node >= 20.
 * CLI:      node scripts/preview_dashboard.mjs [--dir dist] [--host 0.0.0.0] [--port 8787]
 * Program:  import { startPreview } from "./preview_dashboard.mjs"
 */

import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(SCRIPT_DIR, "..");

const CONTENT_TYPES = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".map": "application/json; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".webmanifest": "application/manifest+json; charset=utf-8",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
};

function contentTypeFor(file) {
  return CONTENT_TYPES[path.extname(file).toLowerCase()] ?? "application/octet-stream";
}

/** Resolve a URL pathname to a file inside rootDir, or null when outside/missing. */
function resolveAsset(rootDir, pathname) {
  const decoded = decodeURIComponent(pathname);
  const relative = path.normalize(decoded).replace(/^(\.\.[/\\])+/, "").replace(/^[/\\]+/, "");
  const candidate = path.join(rootDir, relative);
  if (candidate !== rootDir && !candidate.startsWith(rootDir + path.sep)) {
    return null; // path traversal guard
  }
  let stat;
  try {
    stat = fs.statSync(candidate);
  } catch {
    return null;
  }
  if (stat.isDirectory()) {
    const index = path.join(candidate, "index.html");
    return fs.existsSync(index) ? index : null;
  }
  return stat.isFile() ? candidate : null;
}

function sendFile(res, file, status = 200) {
  const body = fs.readFileSync(file);
  res.writeHead(status, {
    "content-type": contentTypeFor(file),
    "content-length": String(body.length),
    "cache-control": status === 200 ? "public, max-age=0, must-revalidate" : "no-store",
  });
  res.end(body);
}

function redirect(res, location) {
  res.writeHead(307, { location, "cache-control": "no-store" });
  res.end();
}

/** Workers Static Assets "auto-trailing-slash" html handling. */
function applyHtmlHandling(rootDir, pathname) {
  if (pathname.endsWith(".html") && pathname !== "/index.html") {
    return { redirect: pathname.slice(0, -".html".length) };
  }
  if (pathname === "/index.html") {
    return { redirect: "/" };
  }
  if (!pathname.endsWith("/")) {
    const asDirectory = resolveAsset(rootDir, pathname + "/");
    if (asDirectory) {
      return { redirect: pathname + "/" };
    }
    const withHtml = resolveAsset(rootDir, pathname + ".html");
    if (withHtml) {
      return { redirect: pathname + "/" };
    }
  }
  return {};
}

export function createRequestHandler(rootDir, options = {}) {
  const log = options.log ?? null;
  return function handleRequest(req, res) {
    const url = new URL(req.url, "http://localhost");
    const pathname = url.pathname;
    const handled = applyHtmlHandling(rootDir, pathname);
    if (handled.redirect) {
      log?.(`${req.method} ${pathname} -> 307 ${handled.redirect}`);
      redirect(res, handled.redirect);
      return;
    }
    const file = resolveAsset(rootDir, pathname);
    if (file) {
      log?.(`${req.method} ${pathname} -> 200 /${path.relative(rootDir, file).split(path.sep).join("/")}`);
      sendFile(res, file);
      return;
    }
    // not_found_handling: "single-page-application"
    const fallback = path.join(rootDir, "index.html");
    if (fs.existsSync(fallback)) {
      log?.(`${req.method} ${pathname} -> 200 /index.html (spa fallback)`);
      sendFile(res, fallback);
      return;
    }
    log?.(`${req.method} ${pathname} -> 404`);
    res.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    res.end("404 Not Found");
  };
}

/** Start the preview server; resolves with { server, host, port, close() }. */
export function startPreview(options = {}) {
  const rootDir = path.resolve(options.dir ?? path.join(ROOT, "dist"));
  if (!fs.existsSync(path.join(rootDir, "index.html"))) {
    return Promise.reject(new Error(`no built dashboard at ${rootDir} — run "npm run build" first`));
  }
  const host = options.host ?? "0.0.0.0";
  const server = http.createServer(createRequestHandler(rootDir, { log: options.log ?? null }));
  return new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(options.port ?? 0, host, () => {
      const address = server.address();
      resolve({
        server,
        rootDir,
        host: address.address,
        port: address.port,
        url: `http://${address.address === "0.0.0.0" ? "127.0.0.1" : address.address}:${address.port}/`,
        close: () => new Promise((done) => server.close(done)),
      });
    });
  });
}

function parseArgs(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const flag = argv[index];
    if (flag === "--dir") options.dir = argv[++index];
    else if (flag === "--host") options.host = argv[++index];
    else if (flag === "--port") options.port = Number(argv[++index]);
    else if (flag === "--help" || flag === "-h") options.help = true;
    else throw new Error(`unknown argument: ${flag}`);
  }
  return options;
}

const isMain = process.argv[1] && import.meta.url === new URL(`file://${path.resolve(process.argv[1])}`).href;
if (isMain) {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    process.exit(2);
  }
  if (options.help) {
    console.log("Usage: node scripts/preview_dashboard.mjs [--dir dist] [--host 0.0.0.0] [--port 8787]");
    process.exit(0);
  }
  options.port = options.port ?? Number(process.env.PORT ?? 8787);
  options.log = (line) => console.log(line);
  startPreview(options)
    .then((preview) => {
      console.log(`Serving ${path.relative(ROOT, preview.rootDir)} on http://${preview.host}:${preview.port}/`);
      console.log("Cloudflare-compatible routing: auto-trailing-slash + single-page-application fallback. Ctrl+C to stop.");
    })
    .catch((error) => {
      console.error(`PREVIEW FAILED\n- ${error.message}`);
      process.exit(1);
    });
}
