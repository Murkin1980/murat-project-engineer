# Compute Budget — usage instrumentation policy (forward validation)

Status: EXPERIMENTAL
Disposition: EXTEND_EXISTING

## Why this exists

The controlled validation of the Compute Budget Estimator (see `COMPUTE_BUDGET_VALIDATION_REPORT.md`) found zero historical runs with observed usage telemetry. Every prior MPE run recorded `approximate_cost: null` or a qualitative note ("Exact Router cost not observable."). The estimator cannot be validated retroactively, so validation must move forward.

This policy defines the minimum fields every new substantial MPE run MUST capture so the estimator can be validated on the next 5-10 runs.

## Mandatory fields per run

```text
provider
model
input_tokens
cached_input_tokens
output_tokens
observed_cost
model_calls
tool_calls
retries
start_time
end_time
progress checkpoints
measurement_source
```

These map directly onto the canonical `contracts/COMPUTE_BUDGET.schema.json`:

| Policy field | Contract field | Type |
|---|---|---|
| provider / model | `routing.actual_provider_mix` | string -> {slug: fraction} |
| input_tokens | `usage.input_tokens` | integer (null if missing) |
| cached_input_tokens | `usage.cached_input_tokens` | integer (null if missing) |
| output_tokens | `usage.output_tokens` | integer (null if missing) |
| observed_cost | `usage.estimated_cost` | number (null if missing) |
| model_calls | run report `commands_tools_used` / evidence | integer |
| tool_calls | run report `commands_tools_used` / evidence | integer |
| retries | run report `rework_count` / evidence | integer |
| start_time | run report `start_timestamp` | ISO-8601 datetime |
| end_time | run report `end_timestamp` | ISO-8601 datetime |
| progress checkpoints | efficiency / validation dataset | [{progress_percent, cost_at_checkpoint}] |
| measurement_source | `usage.measurement` | observed \| estimated \| unobserved |

## Measurement quality rules

1. `observed` ONLY when the value comes from a provider/router bill, an authoritative usage API response, or a log line that is committed as evidence. Operator memory is not `observed`.
2. `estimated` when a defensible reconstruction exists (known calls x known pricing, with the pricing snapshot dated and committed). A reconstructed value MUST be labelled `estimated` and must never be promoted to `observed`.
3. `unobserved` otherwise. Record `null`, never a fabricated zero.

## Progress checkpoints

Capture at least two checkpoints per run (target ~20% and ~50% project progress):

```json
{"progress_percent": 20, "cost_usd": 0.42, "measurement_source": "router-usage-api"}
```

The ~20% checkpoint is what makes the burn-rate reforecast (naive and adjusted projected totals) testable against the final cost.

## Dated pricing snapshot

Provider pricing MUST be captured with its date (see `PRICING_SNAPSHOT_DATE` in `scripts/compute_budget.py`). When vendor prices change, a new snapshot is added; historical runs keep the snapshot they were priced under, so the estimator stays reproducible.

## Forward validation trigger

Once 5-10 runs carry observed usage (>= 5 observed preferred), re-run:

```bash
python scripts/compute_budget_retrospective.py
```

and evaluate against the experimental targets (preflight min-max hit rate >= 80%; reforecast error <= +/-25% after ~20% progress) in `docs/COMPUTE_BUDGET_GATE.md`.

## Explicitly out of scope

No separate telemetry backend, no billing service, no analytics service, no new authority store. The fields above live in the existing Run Report, Experiment Record, and compute-budget snapshot. Business Discovery and shared research architecture are unchanged.
