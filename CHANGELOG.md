# Changelog

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
