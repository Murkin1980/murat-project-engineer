# MPE Compute Budget Gate

Status: EXPERIMENTAL / required for substantial execution preflight
Disposition: EXTEND_EXISTING

## Purpose

The Compute Budget Gate adds an explicit AI compute-economics check to Murat Project Engineer before substantial execution. It is not a billing system and must not invent precision when usage telemetry is unavailable.

Canonical name: `AI Compute Budget`. The top-level metric is the whole AI compute budget, never an OpenAI-only cost.

## Mandatory execution sequence

New Idea Filter -> Scope Gate -> Compute Budget Preflight -> Budget Approval -> Execution -> Usage Capture -> Burn-rate Reforecast -> Completion Review

The gate applies to new repositories and to substantial stages of existing projects, including deep-change work, large refactors, migrations, multi-stage experiments, and large code-generation tasks.

## Canonical data contract

See `contracts/COMPUTE_BUDGET.schema.json`, `contracts/COMPUTE_BUDGET.md`, and `contracts/COMPUTE_BUDGET.example.json`. The snapshot has six blocks — `compute_budget`, `preflight`, `usage`, `forecast`, `routing`, `efficiency` — plus a derived `status` block.

## Deterministic engine

`scripts/compute_budget.py` is the single source of truth for the gate logic. It provides:

- `estimate_preflight(...)` — deterministic preflight estimate.
- `budget_health(...)` — GREEN / YELLOW / ORANGE / RED / UNOBSERVED.
- `burn_rate_metrics(...)` — budget_consumed_percent, cost_per_progress_percent, burn_rate_ratio.
- `burn_rate_status(...)` — OK / BURN_RATE_ANOMALY / UNOBSERVED.
- `reforecast(...)` — evidence-based burn-rate reforecast (naive + adjusted projected totals, remaining cost, confidence).
- `compute_snapshot(...)` — assemble the canonical snapshot and derive forecast + efficiency + statuses.
- `run_report_budget_summary(...)` — project the snapshot into the Run Report budget block.
- `migrate_approximate_usage_cost(...)` — backward-compatible migration of the legacy `approximate_usage_cost` field.
- `render_dashboard_budget(...)` — dashboard budget block with explicit UNOBSERVED rendering.

## Provider scenarios

Two scenarios are priced from a dated, overridable snapshot (`PRICING_SNAPSHOT`):

1. `economy` — DeepSeek / Kimi / Qwen / MiniMax low-cost stack.
2. `premium` — OpenAI / Anthropic benchmark.

OpenAI cost is a benchmark, not the top-level metric.

## Forecast semantics

All numeric usage values carry a measurement status:

- `observed` — reported by a provider/router or derived from authoritative billing telemetry.
- `estimated` — calculated from known calls/context/pricing but not directly metered.
- `unobserved` — telemetry is missing and a precise claim is not defensible.

Never report an estimated or unobserved value as observed.

## Budget health states

Computed against projected total cost / hard limit:

- GREEN: <= 70%
- YELLOW: > 70% and <= 90%
- ORANGE: > 90% and <= 110%
- RED: > 110%
- UNOBSERVED: hard limit or usable forecast telemetry is unavailable

## Burn-rate anomaly

- project progress: 25%
- budget consumed: 70%
- burn-rate ratio: 70 / 25 = 2.8x

A burn-rate ratio >= 1.5 raises `BURN_RATE_ANOMALY` even if the hard budget has not been exceeded.

## Reforecast rule

After observed usage and progress exist, MPE prefers the evidence-based burn-rate reforecast over the initial preflight point estimate. The original preflight estimate remains stored for calibration. The reforecast is purely progress + observed-cost driven and never folds the initial estimate into its projection.

## Run Report integration

The existing `RUN_REPORT` gains an optional `compute_budget` summary block (planned budget, hard limit, spend, projected total, projected remaining, budget status, burn-rate status, measurement quality, forecast confidence, provider/model mix). The legacy `approximate_usage_cost` field is preserved; when numeric it is migrated as an *estimated* (never observed) spend.

## Dashboard representation

Each project card shows two separate bars — PROJECT PROGRESS and AI BUDGET — plus a budget summary block. When usage is not observed, the dashboard renders `UNOBSERVED` rather than fake zeros.

## MVP acceptance criteria

Evaluate the gate on 5-10 MPE runs.

Success target:

- actual final cost falls inside the preflight min-max band for >= 80% of runs;
- after approximately 20% progress, expected total-cost forecast is within roughly +/-25% of final cost for the majority of runs;
- economy routing does not reduce required PASS-rate or deterministic-check quality.

If these criteria fail, improve the estimator before expanding dashboard complexity.
