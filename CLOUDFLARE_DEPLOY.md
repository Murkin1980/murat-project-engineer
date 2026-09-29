# Cloudflare deploy — MPE portfolio dashboard

Short, exact manual procedure. Scope: the existing static dashboard inside
`murat-project-engineer`. No new repository, service, worker, database or
registry-schema change is involved.

| Item | Value |
| --- | --- |
| Repository | `Murkin1980/murat-project-engineer` (root = deploy root) |
| Product | Cloudflare Workers Static Assets (existing worker `murat-project-engineer`) |
| Build command | `npm run build` → `node scripts/build_dashboard.mjs` |
| Output directory | `dist` (generated, gitignored) |
| Deploy source of truth | `dashboard/public/` (committed HTML + Reladraw SVGs) |
| Config | `wrangler.jsonc` (`build.command`, `assets.directory`, `auto-trailing-slash`, `single-page-application`) |
| Production URL | https://murat-project-engineer.muriktl.workers.dev |
| Requirements | Node.js >= 20 (22 recommended), Cloudflare API token with **Account → Workers Scripts → Edit** |

## 1. Verify locally (no credentials needed)

```bash
npm run build          # assembles ./dist from dashboard/public, fails closed on a missing asset
npm run check          # 43 checks: build, config, routes, assets, byte parity, Reladraw views, mobile 390px
npm run dev            # real Cloudflare runtime (workerd) on http://127.0.0.1:8787
npm run deploy:dry-run # wrangler config + asset upload dry run, no API token required
python -m unittest discover -s tests
python scripts/validate_package.py .
```

`npm run preview` is a dependency-free static server with the same routing rules
(`--dir dist --host 0.0.0.0 --port 8787`); use it when `wrangler dev` cannot run.

Pin note: wrangler `4.143.0` is pinned in `.github/workflows/deploy-dashboard.yml`
and in `package.json`. Wrangler `4.110.0` (previous pin) deploys fine but its
bundled workerd rejects `compatibility_date: 2026-08-13`, so local `wrangler dev`
fails on that version.

## 2. Authenticate (choose one)

```bash
# A) API token — recommended for CI and for a one-off manual deploy
export CLOUDFLARE_API_TOKEN="<token: Account / Workers Scripts / Edit>"
export CLOUDFLARE_ACCOUNT_ID="<account id>"

# B) Interactive OAuth (browser); no env vars needed afterwards
npx --yes wrangler@4.143.0 login
```

Never commit, paste into chat, or write tokens into `wrangler.jsonc`,
`package.json`, the workflow file, or any file under `dashboard/`.

## 3. Deploy

```bash
cd <repo root>            # murat-project-engineer
git status                # must be clean or contain only intended dashboard changes
npm run deploy:dry-run    # confirm: "Read N files from the assets directory .../dist"
npx --yes wrangler@4.143.0 deploy
```

`wrangler deploy` runs `build.command` itself, so `./dist` is always rebuilt from
`dashboard/public/` immediately before upload. Expected output ends with the
worker URL and a deployment version id — record both.

## 4. Verify the deployed site

```bash
node scripts/check_dashboard_deploy.mjs --base-url https://murat-project-engineer.muriktl.workers.dev
```

This runs the same route/asset/parity/Reladraw/390px checks against production.
Manual spot checks:

- `/` → 200, dashboard snapshot title and date;
- `/index.html` → 307 → `/`;
- any unknown path (e.g. `/brief`) → 200 with `index.html` (SPA fallback);
- `/registry/portfolio.svg` → 200 `image/svg+xml` (desktop Reladraw view);
- `/registry/mobile/status-pass.svg`, `-ready_to_test.svg`, `-planned.svg`, `-hold.svg` → 200 `image/svg+xml`;
- phone or devtools at **390 px width**: mobile status cards readable without zoom (SVG width 346–355 px, font-size 14 px), desktop view hidden below 650 px.

## 5. Auto-deploy from GitHub (existing workflow)

`.github/workflows/deploy-dashboard.yml` deploys on every push to `main` and on
`workflow_dispatch`. It skips silently while credentials are missing, so a green
run is **not** proof of a deploy. To enable it, in the repository settings add:

- Secret `CLOUDFLARE_API_TOKEN` (Account → Workers Scripts → Edit);
- Variable `CLOUDFLARE_ACCOUNT_ID`.

Then re-run the workflow (or push to `main`) and confirm the run log contains
`Deployed murat-project-engineer` plus the version id.

## 6. Rollback

```bash
npx --yes wrangler@4.143.0 deployments list          # inspect versions
npx --yes wrangler@4.143.0 rollback                  # roll back to the previous version
# or redeploy a known-good snapshot:
git checkout <good-sha> -- dashboard/public && npm run build && npx --yes wrangler@4.143.0 deploy
```

## 7. Cloudflare Pages (only if the owner explicitly chooses it)

The dashboard is already deployed as a Worker; creating a Pages project would be
a second hosting surface and is out of scope here. If it is ever approved, the
Pages settings are: root directory `/` (repository root), build command
`npm run build`, output directory `dist`, `NODE_VERSION=22`, no environment
secrets. CLI equivalent against an existing Pages project:
`npx --yes wrangler@4.143.0 pages deploy dist`.

## 8. Boundaries preserved by this deploy path

- Only `murat-project-engineer` is used; no new repository, worker, service or database.
- `experiments/EXPERIMENT_REGISTRY.json` schema and content are untouched; the
  dashboard serves only the generated Reladraw renders.
- Desktop (`/registry/portfolio.svg`) and mobile (`/registry/mobile/status-*.svg`)
  Reladraw views are copied byte-identically by the build and verified per deploy.
- `dist/` is generated output (gitignored); `dashboard/public/` stays the source of truth.
