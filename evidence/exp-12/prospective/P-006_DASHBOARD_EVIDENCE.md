# EXP-12 P-006 — Dashboard target evidence (salamat-projects-dashboard)

Case: `EXP12-P-006` · Parent instruction: `docs/experiments/EXP-12_P006_DASHBOARD_EXPERIMENT_SYNC.md`
Recorded: 2026-10-10 (UTC)

## Source revisions

- MPE canonical source revision used: `65873ff61aedefc98a9c9f1fe39447a87e075215` (`origin/main` at start and end of target work; also the frozen pre-registration commit).
- `experiments/EXPERIMENT_REGISTRY.json` content read by the sync: blob `sha 08c3857ad310dee0a9bf8701e31a20630df21ae1`, `updated_at 2026-10-10`, 30 experiments (GitHub Contents API, `ref=main`).
- Dashboard baseline: `aa150e8b792f60f0fc2fe0704542818c6781abae` — equal to current `origin/main` at execution, so no rebase was needed and the frozen baseline remained authoritative.

## Reconciliation finding

The mirrored snapshot `config/experiments.github.json` was stale against current MPE evidence (mirror 2026-09-24/17 entries vs canonical 2026-10-10/30 entries):

| Experiment | Mirror (stale) | Canonical now |
| --- | --- | --- |
| EXP-09 | READY_TO_TEST | HOLD (source-of-truth missing; closed non-reproducible) |
| EXP-14 | PLANNED | FAIL (closed; no Laya authority) |
| EXP-15 | PLANNED | PASS |
| EXP-S2C-01 | PLANNED | PASS |
| EXP-16 | PLANNED | RETIRED |
| EXP-QOOPIA-MEMORY | PLANNED | RETIRED |
| EXP-UX-UI-SKILLS | READY_TO_TEST | RETIRED |
| EXP-12 | PASS (2026-09-21, "pre-register until ten") | PASS (2026-10-10, P-006 next action) |
| EXP-13 | READY_TO_TEST (Pilot Batch 1 wording) | READY_TO_TEST (Cloudflare relay preflight wording) |
| EXP-17…EXP-29 | absent | present (incl. EXP-26 `PARTIAL`) |

The canonical `PARTIAL` status is not accepted by the dashboard's read-only contract enum, so a contract-acceptance change is unavoidable for a current mirror — the same situation as `RETIRED`, previously fixed by one-line enum extension `48cb906` ("fix: accept canonical MPE retired experiment status").

## Changes made (verified; publication blocked — see below)

Dashboard branch `arena/ddd6961d-exp12-p006-experiments-sync`, commit `fc4ff90` (on `aa150e8`), 3 files, +307/−21 lines (all but 2 lines in the mechanically generated snapshot):

1. `config/experiments.github.json` — regenerated **by the existing read-only mechanism** `npm run sync:experiments` (`scripts/sync-mpe-experiments.ts`, unmodified) from MPE `main`; now 30 entries, snapshot `updated_at 2026-10-10`. No manual edits, no new source of truth.
2. `src/contract/experiment-registry.ts` — `ExperimentStatusSchema` enum gains `PARTIAL` (contract accepts current canonical vocabulary).
3. `src/components/DashboardApp.tsx` — `experimentFilterLabels` gains `PARTIAL: 'Partial'` (required by the exhaustive `Record<ExperimentStatus|'ALL',…>` type; same treatment `RETIRED` received). No UI redesign; no new filter tab (consistent with `RETIRED`).

Explicit non-changes: no write-back path, no execution/session controls, no API/Worker/backend/database, no Cloudflare or deploy config change, no second registry, no PROJECT_STATUS/CHECKPOINTS/ROADMAP churn (this is not a dashboard checkpoint; mirror precedent `48cb906` recorded no status churn either).

## Stale open experiment-mirror PRs (identified, deliberately NOT merged)

All four hand-edit `config/experiments.github.json` against the 2026-09-24 baseline and conflict with current canonical evidence:

- **#16** "Sync EXP-14 AnyJev candidate" — renames EXP-14 to "Laya / AnyJev …" and keeps it `PLANNED`; canonical is `FAIL`, closed.
- **#17** "experiments: show AI Search / Entity Readiness" — full manual rewrite/reformat of the snapshot (own `updated_at 2026-09-26`); does not match current canonical entries (e.g. canonical EXP-17 is `HOLD`, manifest-capture only).
- **#18** "Experiments: mirror EXP-07 Strix retry" — sets EXP-07 `READY_TO_TEST` "run one bounded Strix quick scan"; canonical decision is `PASS` + "Keep Strix on hold". Directly contradicts the owner's current disposition.
- **#19** "Experiments: mirror Harness Router / Zerg Router" — adds a routing-candidates entry that does not exist in the canonical MPE registry at all (would create facts outside the source of truth).

Recommendation for the owner: supersede and close #16–#19 rather than merging any of them; this change (or a re-run of `npm run sync:experiments` after the P-006 evidence lands) makes them redundant by construction.

## Validation (target repository)

- `npm ci` — PASS (Node v22.22.3, npm 10.9.8).
- `npm test` (`tsx --test tests/**/*.test.ts`) — **267 pass / 0 fail**; includes `tests/experiment-registry.test.ts` validating the regenerated snapshot through `parseExperimentRegistry` (fails closed on any unknown status).
- `npm run verify:snapshot` — PASS (portfolio snapshot untouched: schemaVersion 1.2.0, version 6, 15 projects, no credentials).
- `npm run build` (`tsc -b && vite build`) — PASS (pre-existing 500 kB chunk warning only, unrelated, recorded in `docs/UI_SKILLS_EXPERIMENT.md` R7).
- `git diff --check` — clean.
- Sandbox note: Node fetch required `NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` for the sync's HTTPS call (environment-only workaround; no code/config change).

## Deployment / write-back statement

No production deployment occurred. No Cloudflare or Pages configuration was touched. No write-back to MPE or any project repository was performed or added; the dashboard remains a read-only monitoring UI.

## Publication blocker and next action

The change is committed and fully validated on the local branch, but the Arena sandbox's GitHub connection is read-only for `Murkin1980/salamat-projects-dashboard`: `git push` returns 403 ("Permission to Murkin1980/salamat-projects-dashboard.git denied to Murkin1980") and REST ref creation returns 403 "Resource not accessible by integration". No PR could therefore be opened from the sandbox.

Applicable artifact: `P-006_DASHBOARD_PATCH.patch` (same directory) — `git checkout -b arena/ddd6961d-exp12-p006-experiments-sync aa150e8 && git am P-006_DASHBOARD_PATCH.patch` (or `git apply`), push, open a bounded PR against `main`, CI `validate` job, owner merge decision.
