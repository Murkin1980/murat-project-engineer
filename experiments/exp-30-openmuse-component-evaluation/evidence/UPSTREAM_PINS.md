# EXP-30 / CP-01 — Upstream pins and verification

Run date: 2026-10-16 UTC (session started 2026-10-15 UTC)
Method: read-only source audit. Nothing was installed, built, run, deployed or imported
from OpenMuse. No upstream write was attempted.

## 1. Canonical pin

| Fact | Value | Verified by |
| --- | --- | --- |
| Repository | `CopilotKit/OpenMuse` (GitHub API `full_name`: `CopilotKit/openmuse`) | `gh api repos/CopilotKit/OpenMuse` |
| Audited commit (pin) | `1ac68f3909f2478ab6280883f1ab5ea65eb5719d` | local `git rev-parse HEAD`; `gh api repos/CopilotKit/OpenMuse/branches/main`; `git ls-remote` for `HEAD` and `refs/heads/main` (all three identical) |
| Commit subject / author date | `perf(server): scope refreshIdeas status queries (#109)` / 2026-10-06T22:39:29Z | `gh api .../commits/main` |
| Default branch | `main` | API |
| Tags | none | `git tag` (empty) + `gh api repos/CopilotKit/OpenMuse/tags` (empty) |
| GitHub releases | none | `gh api repos/CopilotKit/OpenMuse/releases` (empty) |
| Declared version | `0.1.0`, `"private": true` | `OpenMuse@1ac68f3:package.json:3-4` |
| Changelog | single entry `0.1.0-alpha — 2026-09-15` | `OpenMuse@1ac68f3:CHANGELOG.md:3` |

Consequence: **there is no released version to depend on; the commit SHA is the only
reproducible pin.** "Nearest release" does not exist for this upstream.

## 2. Maintenance / activity (read from the GitHub API on 2026-10-15/16 UTC)

| Fact | Value |
| --- | --- |
| Created | 2026-09-15T16:05:44Z |
| Last push (any branch) | 2026-10-14T17:03:51Z |
| Last `main` commit | 2026-10-06T22:39:29Z (9 days before the audit) |
| Commits on `main` | 125 (`?per_page=1` → `rel="last" page=125`) |
| Contributors (non-anon) | 27 (`?per_page=1` → `rel="last" page=27`); top: `jerelvelarde` 39, `kvnloo` 15, `asasemahmed` 11 |
| Branches | 30 |
| Open issues / open PRs | 11 / 41 (`search/issues` totals) |
| Stars / forks | 5,075 / 704 |
| Archived | false |
| CI workflow | one file, 5 jobs: `quality` (`ci.yml:13`), `platform` (`:30`), `browser` (`:50`), `browser-container` (`:64`), `computer-container` (`:75`) |
| Last `main` CI result | `CI / push / success` created 2026-10-06T22:39:33Z |
| Recent non-`main` CI | two renovate branches `failure` (2026-10-12, 2026-10-14) — dependency-update churn is red in PRs, main is green |

Interpretation (inference, not a claim by upstream): an active but very young
single-vendor alpha (one month old), versionless, with dependency churn that currently
fails its own CI on update branches.

## 3. Languages, size, package managers

| Fact | Value | Source |
| --- | --- | --- |
| Language bytes | TypeScript 1,380,481; Python 4,799; JavaScript 3,089; Dockerfile 834 | `gh api .../languages` |
| Non-test TS/TSX | 99 files / 22,807 lines under `apps/` + `packages/` | local `wc -l` over the shallow clone |
| Test TS/TSX | 60 files / 14,465 lines | same |
| Test declarations | 413 top-level `test(` in `tests/*.test.ts`; 32 `apps/mobile/test`; 4 `apps/worker/tests`; 2 `apps/computer` | `grep -c '^test('` |
| `docs/VERIFICATION.md` claim | "**154 tests pass**" (document dated Sept 16 2026) | `OpenMuse@1ac68f3:docs/VERIFICATION.md:7` |
| Declared package manager | `pnpm@11.19.0` | `package.json:7` |
| Node engines | `>=22` in `package.json:9`, while `README.md:66` and CI require **Node 24 LTS** (`.github/workflows/ci.yml` `node-version: 24`) | both files |
| Second package manager | `apps/worker` carries its own `package.json` + `package-lock.json` (npm, single dependency `playwright@1.62.1`) and its image builds with `npm ci` | `apps/worker/package.json:1-18`, `apps/worker/Dockerfile:3-4` |
| Workspace | `apps/mobile`, `apps/worker` only; `pnpm.overrides` pins `image-size@2.0.4`; `patchedDependencies` patches `metro@0.83.3` | `pnpm-workspace.yaml:1-21` |
| Lockfile size | `pnpm-lock.yaml` 14,137 lines | local `wc -l` |
| Dependency-update bot | `renovate.json` present | repo root |

The `154 tests` documentation figure and the 413 test declarations found at the pin do
not agree. Recorded as a doc/code drift observation; not resolved (out of CP-01 scope).

## 4. Application / platform targets (verified)

| Target | Evidence |
| --- | --- |
| Always-on Node HTTP API | `OpenMuse@1ac68f3:apps/server/src/index.ts:1-20` (`@hono/node-server` `serve`, `SIGINT/SIGTERM` drain) |
| In-process or separate task worker | `apps/server/src/index.ts:11` (`if (config.taskWorkerEnabled) agent.start()`), `apps/server/src/worker-entry.ts:7-10` (separate worker **requires** `DATABASE_URL`; PGlite cannot be shared across processes) |
| Persistent browser sidecar (Node + Playwright + Chromium) | `apps/worker/src/index.ts:3-13`, `apps/worker/Dockerfile:1` (`mcr.microsoft.com/playwright:v1.62.1-noble`) |
| Optional Docker Linux computer, or E2B desktop VM | `apps/computer/Dockerfile:1-18`, `apps/server/src/computer.ts`, `apps/server/src/computer-e2b-desktop.ts`, `docs/COMPUTER.md` |
| Expo / React Native iOS + Android + web client | `apps/mobile/package.json` (`expo ~54`, `react-native 0.81.5`), root `package.json:23-25` |
| Deployment: Render Blueprint (3 services) + docker compose | `render.yaml`, `infra/compose.yaml` |
| Storage: embedded PGlite **or** PostgreSQL via `pg` | `apps/server/src/db.ts:160-180` |
| Cloudflare Workers / D1 / R2 / Pages | **none.** No `wrangler.*`, no `workerd`, no D1/R2 binding anywhere outside the dependency lockfile. Verified by 0-match greps (case-insensitive, `--include=*.ts,*.tsx,*.md,*.json,*.yaml,yml --include=Dockerfile`, `pnpm-lock.yaml` excluded) for each of: `cloudflare`, `wrangler`, `\bD1\b`, `durable object`, `workers.dev`, `\bR2\b`. An unanchored `d1` search matches only `thread1` test-fixture identifiers, not a D1 reference |

## 5. Licensing facts (read, not assumed)

* Root `LICENSE` is the standard **MIT** text, `Copyright (c) 2026 OpenMuse contributors`
  (`OpenMuse@1ac68f3:LICENSE:1-3`). sha256 `399a9cccf1b228c9e8ad348ef66a0a5802d438d46735d0d068390925aee5ee36` (21 lines).
* Only one `LICENSE` file exists in the whole tree and there is **no `NOTICE` file**
  (`find . -name "LICENSE*" -o -iname "NOTICE*"` → root `LICENSE` only). Sub-packages
  (`apps/mobile`, `apps/worker`) declare no `license` field, so the root MIT governs the tree.
* MIT obligation that would apply to any copied code: the copyright + permission notice
  must be included in all copies or substantial portions (`LICENSE:5-7` text). No patent grant.
* Contributions are accepted under MIT; **no CLA/DCO** is required (`CONTRIBUTING.md:54`).
* Explicitly outside the license: CopilotKit **Intelligence** is a separate service —
  "Intelligence is a separate service and is not included in this repository's MIT license"
  (`README.md:194`), repeated at `docs/RICH-THREADS.md:30`.
* Artwork: the capybara icon is original work bundled under the same MIT
  (`apps/mobile/assets/README.md:1-5`).
* Direct-dependency licenses spot-verified on the exact pinned versions through the npm
  registry: `@ag-ui/core@0.0.59` MIT, `@ag-ui/client@0.0.59` MIT,
  `@copilotkit/runtime@1.70.1` MIT, `@copilotkit/react-native@1.70.1` MIT,
  `@copilotkit/aimock@1.42.0` MIT, `@electric-sql/pglite@0.3.14` Apache-2.0,
  `playwright@1.62.1` Apache-2.0, `hono@4.11.4` MIT, `zod@4.1.0` MIT,
  `@hono/node-server@1.19.0` MIT, `pg@8.16.3` MIT, `pdf-lib@1.17.1` MIT,
  `parse5@7.3.0` MIT, `rxjs@7.8.1` Apache-2.0, `@tanstack/ai@0.59.0` MIT,
  `@tanstack/ai-anthropic@0.18.13` MIT, `@tanstack/ai-gemini@0.32.1` MIT,
  `@tanstack/ai-openai@0.23.2` MIT, `@modelcontextprotocol/sdk@1.30.0` MIT,
  `@e2b/desktop@2.4.0` MIT, `@typesafe-ai/sdk@0.6.0` MIT, `typescript@5.9.2` Apache-2.0,
  `tsx@4.20.0` MIT, `@biomejs/biome@2.4.0` `MIT OR Apache-2.0`,
  `@google/genai` (transitive, `latest`) Apache-2.0.
  → No copyleft in the audited set; MIT/Apache-2.0 only. Transitive closure beyond the
  audited set was **not** walked (dependency import is prohibited in CP-01).

## 6. Cost / credential surface of the upstream itself (relevant to later decisions)

| Constraint | Evidence |
| --- | --- |
| The API refuses to start without a CopilotKit **Intelligence** project key — in *every* mode, including local sample mode | `apps/server/src/config.ts:152` (`required("CPK_INTELLIGENCE_API_KEY", …)`) + `apps/server/src/app.ts:35` (`assertApiDeploymentConfig`) + `SECURITY.md:35` (CI uses synthetic keys) and `docs/RICH-THREADS.md:28` ("The API fails at startup with a missing-key error when the key is unset") |
| Model provider key required for open-ended delegated tasks | `apps/server/src/engine/model.ts:22-27` (returns `waiting_input` when `MODEL` is unset) |
| Web search is on by default and sends queries/context to a third party (Parallel, keyless) | `README.md:154` |
| SDK telemetry defaults to **full capture** into the shared CopilotKit PostHog sink | `apps/server/src/config.ts:26-28` (`COPILOTKIT_TELEMETRY_SAMPLE_RATE ??= "1"`), `README.md:198`; tests opt out in `tests/setup.ts:1-4` |
| Smallest hosting plan that survives is 1 GB (512 MB OOM-kills before the port binds, because PGlite loads embedded Postgres) | `render.yaml:5-6` comment |
