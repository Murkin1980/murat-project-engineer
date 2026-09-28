# Changelog

## Unreleased — EXP-07 Strix retry: review findings fixed, target/baseline frozen, run BLOCKED (2026-09-28)

- Fixed all three Codex review findings on PR #27 inside the existing `EXP-07` identity (no new experiment, repository or parallel security workflow).
- `docs/security/STRIX_PILOT.md` now carries a mandatory **Evidence handling and raw-output boundary** (`RAW_STRIX_OUTPUT_NEVER_COMMITTED`): raw Strix reports/logs, `strix_runs/**`, exploit payloads, exploitable endpoints, source excerpts, secrets and sensitive vulnerability details must never be committed; raw evidence stays in access-controlled temporary/local storage, and only a sanitized artifact may enter Git (summary, vulnerability class, affected component/path without exploit details, severity, reproduction status, prior detection by tests/linters/security checks/issues/ordinary review, remediation state, safe evidence hash). The MVP-scope bullet that told executors to store the raw report as evidence was replaced. `.gitignore` now blocks `strix_runs/`, `.strix/`, `raw-pentest/`, `*.har`, `*.pcap`.
- Added the mandatory **Target and baseline freeze** gate (`BASELINE_FREEZE_REQUIRED_BEFORE_SCAN`, `STRIX_RUN_BEFORE_BASELINE_FREEZE = FORBIDDEN`): one MPE-owned target, with repository, branch, exact commit SHA, scan scope, excluded paths, current test result, build/typecheck, existing static/security checks, known security issues and the ordinary code-review baseline recorded before Strix starts; no suitable bounded target means `BLOCKED`. Also added `STRIX_WRITABLE_MOUNT_FORBIDDEN` because the documented Strix CLI mounts a local target directory writable — scans must use a clean clone of the frozen SHA, explicit `--scope-mode`, `--max-turns`/`--max-budget`, and no autofix.
- Froze the retry target `Murkin1980/mebeldocs-ai@2d6d60b240f8f4e2546cf451433c8f1ff0aad65a` (`main`) and executed its baseline in a clean temporary clone: `npm ci` exit 0, `npm test` 202/202 pass, `tsc --noEmit` PASS, `next build` PASS (21 API routes), plus recorded existing checks (tests + typecheck only; no CI, SAST/DAST, dependency or secrets scanning), known issues (pilot-static auth context; internal error messages returned by some routes) and the ordinary code-review baseline. The 2026-08-14 baseline (`fad30491`, 197/2) is explicitly non-reusable for novelty comparison.
- Added the mandatory **Canonical status mapping** (`EXECUTION_OUTCOME_IS_NOT_REGISTRY_STATUS`): `PASS`→`PASS`, `WARNING`→`HOLD`, `BLOCKED`→`HOLD`, `FAIL`→`FAIL`, using only the existing `contracts/EXPERIMENT_REGISTRY.schema.json` enum — no new registry status and no schema change. `result_summary` must carry the literal `execution_outcome:` token. Acceptance criteria were clarified (a successful Strix start is not a `PASS`) and `FAIL` was defined.
- Recorded the 2026-09-28 retry execution as `BLOCKED` / registry `HOLD` with the observed missing prerequisites: no Docker (no `docker`/`podman`/`nerdctl`/`containerd`/`runc`, no `/var/run/docker.sock`, `CapEff 0000000000000000`), no Strix CLI (`strix-agent` 1.6.2 requires Python ≥3.12 versus 3.11.2 available; `pip install --dry-run` found no distribution), and no LLM credential (`STRIX_LLM` + `LLM_API_KEY` / ChatGPT sign-in). Strix Cloud was rejected as an unauthorized new external service that uploads owner code. No scan was simulated and no finding was synthesized: every count is `0 = NOT_RUN`.
- Added the sanitized artifact `evidence/exp-07/STRIX_RETRY_2026-09-28.json` plus `evidence/exp-07/README.md`, and updated the `EXP-07` registry entry (`HOLD`, PR #27 link, evidence link, next action naming the single bounded scan).
- Added `tests/test_exp07_strix_retry.py` (15 deterministic guards) so the sanitization boundary, the frozen target/baseline, the no-simulation rule and the outcome→status mapping cannot drift silently. Suite: 333 tests OK (1 skipped); `scripts/validate_package.py` PASSED; registry validates against its JSON Schema with 0 errors; `git diff --check` clean; sensitive-pattern scan over changed files 0 hits.
- No production integration, CI security gate, autonomous remediation, recurring scan, new security service, new repository, MPE architecture change or Strix execution authority was added. PR #27 was not merged.

## Unreleased — MPE navigation-test stabilization and status synchronization (2026-09-10)

- Fixed the failing `tests/test_dashboard_navigation.py` regression guard. The test was written against the 2026-09-02 snapshot (nav `class="jump-nav"`, filter section `id="decisions"`); the intentional 2026-09-07 weekly refresh (7962d91b09) regenerated the page with `class="nav"` and section `id="ideas"`. The parser now follows the page's `<nav>` element and expects `{brief, p0, support, hold, ideas}`. The original invariant is preserved: section-navigation links must target exactly the existing section set. No dashboard HTML change.
- Synchronized `STATUS.md` with origin/main 95d9e4ba, merged PRs, CI runs and the live dashboard: status verification date recorded; EXP-002 state split (external models' understanding of the frozen IR is SUPPORTED; confirmed cross-executor execution is INCONCLUSIVE, self-reported execution claims stay UNVERIFIED); EXP-13 telemetry state split (fail-closed usage adapters exist in main for all routes; Pilot Batch 1 has zero executed runs); stale deployed dashboard recorded (live site shows the 12.08.2026 snapshot while main carries 07.09.2026, and CI deploy steps are skipped until repository Cloudflare credentials are configured); one nearest action named (choose one small real task from an active project and run it through the existing MPE, recording the outcome, time, rework, and available telemetry; EXP-13 Pilot Batch 1 stays unrun for now).
- Corrected the confirmed stale telemetry status lines in `docs/experiments/EXP-13_PILOT_BATCH1.md` and `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md` (premium route has had a fail-closed Codex-rollout usage adapter since 893517b; "BLOCKED pending token telemetry" no longer accurate). Frozen acceptance criteria unchanged.
- Recorded the stabilization as RUN-13 (`evidence/stage2/RUN-13_REPORT.json`, `evidence/stage2/RUN-13_EXPERIMENT_RECORD.json`) and extended the existing canonical experiment-record field guard in `tests/test_contracts.py` to cover RUN-13.
- No production code, contracts, frozen assets, workflows, or architecture changed.

## Unreleased — EXP-13 low-cost evaluation harness + pre-execution rework (2026-08-21)

- Added `contracts/EXP13_EXECUTION_RECORD.schema.json` — canonical record of one EXP-13 low-cost evaluation run: pre-execution checks, full checks, escalation, outcome, defects, and cost (cost is never fabricated).
- Added `scripts/exp13_checks.py` — deterministic check pipeline: 4 cheap pre-execution checks (`route_resolves`, `triage_expected_match`, `acceptance_present`, `human_review_due`) and 5 execution checks (`usage_valid`, `usage_consistent`, `retries_within_limit`, `defects_within_limit`, `cost_within_limit`). Escalation (`HUMAN_REVIEW_REQUIRED` > `PREMIUM_REQUIRED` > `NONE`) and outcome (`HUMAN_REQUIRED` / `REWORK` / `BLOCKED` / `PASS`) are derived, never hand-set.
- Added `scripts/exp13_harness.py` — wraps checks into immutable records, enforces the batch STOP rule (`max_runs`), and summarizes batches. It never invents telemetry: a run that proceeds requires a real `USAGE_RECORD`; an escalated run stores an empty, unobserved record.
- Added frozen EXP-13 assets in `experiments/exp-13/`: dataset v2 (`tasks_v2.json`, 12 tasks T-001…T-012), routes (`routes.json`, A/B/premium), thresholds (`thresholds.json`), and a dated pricing snapshot (`pricing_snapshot.json`).
- Pre-registered Pilot Batch 1 (`evidence/exp-13/PILOT_BATCH1_PRE_REGISTRATION.json`): 6 tasks (T-001, T-004, T-006, T-008, T-010, T-012) × routes A/B/premium = 18 planned runs. T-008 legally escalates to `HUMAN_REVIEW_REQUIRED`; the harness enforces STOP after 18 runs.
- Documented the experiment in `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`, `docs/experiments/EXP-13_PILOT_BATCH1.md`, and `docs/experiments/EXP13_PRE_EXECUTION_REWORK.md`.
- Added `tests/test_exp13_checks.py` and `tests/test_exp13_harness.py`.

Reconstruction note: this EXP-13 revision is a controlled reconstruction of a previously built but unpublished harness whose patch was not preserved. It is not a byte-for-byte restoration. The frozen semantics (dataset v2, thresholds, pricing snapshot, routes, acceptance criteria) are authoritative from this revision forward. The suite runs 180 tests OK (1 skip) — more than the lost implementation's reported 159 — because the reconstruction ships additional determinism/regression coverage.

## Unreleased — Run Usage Instrumentation (2026-08-20)

- Added the canonical `USAGE_RECORD` contract (`contracts/USAGE_RECORD.schema.json` / `.md` / `.example.json`) for per-run usage telemetry: provider, model, input/cached/output tokens, observed cost, model/tool calls, retries, start/end timestamps, progress checkpoints, and measurement_source.
- Added `scripts/usage_instrumentation.py` — a deterministic recorder plus `classify_measurement` (observed/estimated/unobserved derived from measurement_source, never promoted), `usage_to_compute_budget`, `usage_to_run_report`, and a CLI.
- Extended `contracts/RUN_REPORT.schema.json` / `.md` / `.example.json` with an optional `usage` block so every new run writes its usage inline while historical reports stay valid.
- Compute Budget Gate remains EXPERIMENTAL: instrumentation records telemetry only and does not enforce a budget or hard-stop a run.

## Unreleased — Compute Budget Controlled Validation (2026-08-20)

- Ran a blind retrospective validation of the Compute Budget Estimator v1.0 against five selected historical MPE runs (research / browser / architecture / implementation / evaluation).
- Result: `INSUFFICIENT_HISTORICAL_TELEMETRY` — all 12 inventoried runs carry `approximate_cost: null` or qualitative "not observable" notes; zero observed usage. No accuracy is reported and no telemetry is fabricated.
- Added `experiments/compute-budget/validation_runs.json` (canonical dataset), `scripts/compute_budget_retrospective.py` (blind preflight runner), and `evidence/validation/COMPUTE_BUDGET_RETROSPECTIVE_RESULTS.json`.
- Added `docs/COMPUTE_BUDGET_INSTRUMENTATION.md` defining the mandatory per-run usage fields (provider, model, tokens, observed_cost, calls, retries, timestamps, progress checkpoints, measurement_source) for forward validation on the next 5-10 runs.
- Added `COMPUTE_BUDGET_VALIDATION_REPORT.md`. Estimator parameters unchanged; no historical evidence rewritten.

## Unreleased — Compute Budget Gate MVP (2026-08-19)

- Added the `AI Compute Budget` canonical contract (`contracts/COMPUTE_BUDGET.*`) with six blocks plus a derived status block.
- Added `scripts/compute_budget.py` — a deterministic, dependency-free gate engine: preflight estimate, GREEN/YELLOW/ORANGE/RED/UNOBSERVED health, burn-rate metrics and `BURN_RATE_ANOMALY`, evidence-based reforecast, provider scenarios (economy vs premium), Run Report summary and dashboard rendering.
- Extended `contracts/RUN_REPORT.*` with an optional `compute_budget` summary block while keeping `approximate_usage_cost` backward compatible (migrated as *estimated*, never *observed*).
- Added three deterministic gates (`compute_budget_preflight`, `compute_budget_health`, `compute_budget_burn_rate`) to `gates/registry.yaml`.
- Added the PROJECT PROGRESS / AI BUDGET split to the Portfolio Dashboard, rendering `UNOBSERVED` instead of fake zeros when usage is missing.
- Recorded a controlled validation across 12 historical MPE runs: all report UNOBSERVED spend (no historical cost telemetry); the min-max accuracy criterion is deferred until usage capture is wired into new runs.
- No billing backend, payment automation, persistent agents, scheduler, workflow engine, authority store or new repository were introduced.

## Unreleased — Stage 2 (2026-08-13)

- Added EXP-12 CLEARS deterministic triage contracts, stateless prototype, 20-case retrospective dataset, tests and evidence.
- Recorded 20/20 retrospective fixture agreement with zero DEEP-CHANGE false negatives; prospective accuracy remains NOT_OBSERVABLE pending pre-registered validation.
- Applied Router-review safety rework: maximum architectural impact cannot fall below DEEP-CHANGE/human approval, and runtime input validation enforces the triage contract.
- Added immutable prospective registration/evaluation contracts and evaluator; completed P-001 with three-way label agreement and one direct-CLI rework. Prospective progress is 1/10.
- Completed P-002: added deterministic EXECUTED evidence generation and changed evaluation to consume the frozen execution artifact with hashes. Prospective progress is 2/10.

- Activated `docs/NEW_IDEA_FILTER_POLICY.md` as a mandatory portfolio gate for new products, features, services, agents, plugins, integrations, automations, repositories and substantial technical ideas.
- Added `docs/OPERATING_MODEL.md` to connect portfolio dispositions (`EXTEND_EXISTING`, `REUSE_COMPONENT`, `MERGE`, `EXPERIMENT`, `HOLD`, `NEW_REPOSITORY`, `REJECT`) with the existing FAST / VERIFIED / DEEP-CHANGE execution model.
- Recorded Run 06 as a FAST coordinator run for status/operating-model synchronization.
- Preserved Run 05 as historically BLOCKED pending real repository-local package validator and unit-test execution; no retroactive PASS was claimed.
- Continued Option A+ without introducing a daemon, scheduler, generic workflow engine, persistent runtime agents, adaptive routing, autonomous memory promotion, Router authority changes, Prime runtime, mandatory external context providers or Workspace UI.

## Unreleased — Stage 2A (2026-08-11)

- Added `contracts/RUN_REPORT.schema.json` and `contracts/RUN_REPORT.example.json` without replacing the Markdown Run Report contract.
- Added machine-readable Experiment Record schema/example beside the existing Markdown template.
- Added explicit nullability for historically unobservable baseline metrics so `unknown` is not encoded as a false zero.
- Added `context/CONTEXT_MAP.md` for progressive source-of-truth disclosure by task class and Expert role.
- Added `docs/CONTEXT_PROVIDERS.md` with replaceable Project, Repository, Documentation, Live Web and User context-provider categories.
- Kept Docsalot and Context.dev optional/documented only; no runtime dependency was introduced.
- Captured real-work evidence for Stage 2A Runs 01–05 using four historical baselines and one resumed coordinator run.
- Added `STAGE2A_FIRST5_REVIEW.md` with risk distribution, baseline/coordinator observations, recovery findings, evidence-format findings and `CONTINUE_20_RUNS` recommendation.
- Preserved Option A+ boundaries: no daemon, scheduler, workflow engine, persistent agents, adaptive routing, autonomous memory promotion, Router authority change, Prime runtime or Workspace UI.
- Current Run 05 remains BLOCKED pending repository-local package validator and unit-test execution in a local/Codex environment; no unverified PASS was recorded.

## 1.0.0 — 2026-08-10

- Added the coordinator skill, four Expert contracts and three temporary Team definitions.
- Added FAST, VERIFIED, DEEP-CHANGE and Software Feature Playbooks.
- Added 12 Review Gates, context manifest, typed handoff and Run Report.
- Added deterministic validation and an isolated sample run.
- Preserved Codex, Router, MASTER, credentials and persistent-agent boundaries.
