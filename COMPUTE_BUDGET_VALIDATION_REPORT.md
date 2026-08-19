# Compute Budget Estimator — Controlled Validation Report

Date: 2026-08-20
Disposition: EXTEND_EXISTING
Estimator version under test: 1.0 (unchanged)

---

## RESULT

**`INSUFFICIENT_HISTORICAL_TELEMETRY`**

The repository contains no historical MPE run with observed usage telemetry. Every prior run recorded `approximate_cost: null` or a qualitative note ("Exact Router cost not observable.", "No external runtime/API cost observed."). There are no token counts, no provider billing figures, no model/tool call counts that could defensibly reconstruct a cost. The estimator therefore cannot be validated retroactively — and this report does not fabricate a validation.

## Candidates found (inventory, unchanged)

Coordinator runs with structured evidence:

| Run | Task class | Tier | Type | Route profile | Outcome |
|---|---|---|---|---|---|
| RUN-06 | narrow-document hygiene | FAST | documentation | — | PASS |
| RUN-07 | external capability security/eval (STRIX/FreeBuff/CodeBuff) | VERIFIED | research | cheap-research=deepseek-v4-flash; strong-review=gpt-5.6-sol | PASS |
| RUN-08 | BrowserAct public-web evidence acquisition | VERIFIED | browser/tool | deepseek-v4-flash | PASS |
| RUN-09 | Personalized Assessment Engine v0 | VERIFIED | coding/eval | deepseek-v4-pro | REWORK |
| RUN-10 | Munder Difflin architecture pilot | VERIFIED | architecture | gpt-5-codex | BLOCKED |
| RUN-11 | runtime coordination contracts | VERIFIED | implementation | deepseek-v4-pro | PASS |
| RUN-12 | Clears triage backtest (EXP-12) | VERIFIED | evaluation | deepseek-v4-pro | PASS |

Historical baselines (stage2a run-01..05, incl. one DEEP-CHANGE) have minimal/no role-level data and were not eligible. The current Compute Budget Gate MVP run (RUN-CBG-001) is the estimator's own output and was correctly excluded from "actual".

## Selected runs (5)

Chosen to cover the required type spread, one per slot, all coordinator runs with the richest structured evidence:

1. **RUN-07** — research-heavy (STRIX/FreeBuff/CodeBuff security & execution evaluation).
2. **RUN-08** — browser/tool-heavy (BrowserAct public-web acquisition; only run with operator-observed retries=2 and tool_calls=29).
3. **RUN-10** — architecture/design (Munder Difflin controlled pilot; fan-out/fan-in, 3 human interventions).
4. **RUN-11** — coding/implementation (bounded runtime coordination contracts; rework=3; has committed JSONL event evidence).
5. **RUN-12** — evaluation/testing (Clears triage 20/20 backtest).

Not selected (same-type duplicates or weaker data): RUN-06 (docs-only, no route), RUN-09 (same coding/eval type as RUN-12, outcome REWORK with fewer structured metrics), stage2a baselines.

## Measurement quality

| Run | measurement | Why |
|---|---|---|
| RUN-07 | UNOBSERVED | `approximate_cost: null` |
| RUN-08 | UNOBSERVED | "0 observed for local Chrome; external service cost UNKNOWN" |
| RUN-10 | UNOBSERVED | "No external product/API cost observed." |
| RUN-11 | UNOBSERVED | "Exact Router cost not observable." |
| RUN-12 | UNOBSERVED | "Exact Router cost not observable." |

Observed: 0 · Estimated: 0 · Unobserved: 5 (of 5 selected; 12 of 12 in full inventory).

No run qualifies as ESTIMATED: there are no token counts, call counts, or provider pricing facts from which a cost could be defensibly reconstructed, and reconstructing tokens from file sizes is explicitly forbidden.

## Blind retrospective preflight

The estimator v1.0 ran unchanged against the pre-execution inputs authored in `experiments/compute-budget/validation_runs.json` (scope, task class, complexity, expected stages, expected calls, expected context, routing policy). Output:

| Run | scenario | input tok expected | output tok expected | cost min | cost expected | cost max | confidence |
|---|---|---|---|---|---|---|---|
| RUN-07 | economy | 1,200,000 | 54,000 | $0.95 | $1.37 | $1.83 | medium |
| RUN-08 | economy | 1,400,000 | 63,000 | $0.77 | $1.10 | $1.46 | medium |
| RUN-10 | premium | 1,500,000 | 67,500 | $10.05 | $14.41 | $19.34 | medium |
| RUN-11 | economy | 1,800,000 | 81,000 | $1.43 | $2.06 | $2.76 | medium |
| RUN-12 | economy | 800,000 | 36,000 | $0.65 | $0.94 | $1.25 | medium |

Structural check passed: every run produced ordered token/cost ranges and a routing recommendation. Premium (RUN-10) prices ~14x the economy runs, consistent with the dated pricing snapshot — this is a scenario difference, not a validation of accuracy.

## Range hit / miss, error %

Not computable. Zero runs carry `actual.cost_usd`, so there are no `range_hit`, `expected_error_percent`, or `actual_vs_expected_ratio` values. No accuracy is reported for UNOBSERVED runs.

## Burn-rate reforecast

Not computable. No run records a progress checkpoint with an observed spend, so no `spent_at_checkpoint`, `naive_projected_total`, `adjusted_projected_total`, or `forecast_error_percent` can be produced. No checkpoint was invented.

## Aggregate accuracy

- Observed runs count: **0**
- Preflight range hit rate: **n/a** (target >= 80%)
- Mean/median/worst expected error %: **n/a**
- Mean reforecast error %: **n/a**

## Known limitations

1. All historical evidence predates usage capture; `approximate_cost` was deliberately null (a correct, honest choice that the gate now preserves).
2. The estimator's pricing snapshot is illustrative and dated, not tied to any committed provider bill.
3. No committed evidence contains provider usage-API responses or router billing logs.

## Estimator weaknesses observed (from structure, not accuracy)

- The preflight is a deterministic spread estimator; its min-max band is a fixed ±35% of the expected token volume, so its real accuracy against actual spend is entirely untested.
- The reforecast adjustment factor is uncalibrated against any real checkpoint data.
- `medium` confidence is over-assigned (the estimator cannot yet distinguish "well-anchored" from "speculative" scope).

## Recommendation

**INSUFFICIENT_HISTORICAL_TELEMETRY.** Keep the estimator as experimental; do NOT promote Compute Budget Gate to a mandatory ritual yet. Enable the minimum instrumentation defined in `docs/COMPUTE_BUDGET_INSTRUMENTATION.md`, accumulate 5-10 new runs with observed usage (>= 5 observed preferred), then re-run `scripts/compute_budget_retrospective.py` and re-evaluate against the experimental targets (>= 80% range hit; <= +/-25% reforecast error after ~20% progress).

## Files added / changed

- `experiments/compute-budget/validation_runs.json` (new — canonical dataset)
- `scripts/compute_budget_retrospective.py` (new — blind retrospective runner)
- `evidence/validation/COMPUTE_BUDGET_RETROSPECTIVE_RESULTS.json` (new — machine-readable result)
- `docs/COMPUTE_BUDGET_INSTRUMENTATION.md` (new — forward instrumentation policy)
- `tests/test_compute_budget_retrospective.py` (new — deterministic tests)
- `CHANGELOG.md` (updated)
- `COMPUTE_BUDGET_VALIDATION_REPORT.md` (new — this report)

No estimator parameters were changed; no historical evidence was rewritten; no new repository, billing service, or telemetry backend was created.
