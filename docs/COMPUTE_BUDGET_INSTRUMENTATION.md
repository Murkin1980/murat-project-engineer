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

## Implementation (now wired in)

The policy above is implemented as code, not just prose:

- `contracts/USAGE_RECORD.schema.json` / `.md` / `.example.json` — the canonical usage record contract.
- `scripts/usage_instrumentation.py` — deterministic recorder:
  - `UsageRecorder` accumulates model calls, tool calls, retries, cost, and progress checkpoints and emits a validated record;
  - `classify_measurement(source)` derives observed/estimated/unobserved and never promotes;
  - `usage_to_compute_budget(record)` projects the record onto the compute-budget `usage` block;
  - `usage_to_run_report(record)` projects it onto the Run Report `usage` block;
  - CLI: `python scripts/usage_instrumentation.py --template RUN-XX` (empty UNOBSERVED record) or `python scripts/usage_instrumentation.py <record.json>` (validate).
- `contracts/RUN_REPORT.schema.json` gains an optional `usage` block (same shape as USAGE_RECORD, minus `schema_version`/`run_id`), so every new run writes its usage inline and old reports stay valid.

Example of recording a run in code:

```python
from scripts.usage_instrumentation import UsageRecorder

record = (
    UsageRecorder(run_id="RUN-XX")
    .start(provider="OpenCode Zen", model="opencode-go/deepseek-v4-flash")
    .record_model_call(1200, 240, cost=0.01)   # per model call
    .record_tool_call(3)
    .record_retry(1)
    .record_checkpoint(20, 0.11, "router_billing")
    .to_record("router_billing")
)
```

If no telemetry is available, emit `empty_record(run_id)` — explicit UNOBSERVED, never fake zeros.

## Explicitly out of scope

No separate telemetry backend, no billing service, no analytics service, no new authority store. The fields above live in the existing Run Report, Experiment Record, and compute-budget snapshot. Business Discovery and shared research architecture are unchanged.

The Compute Budget Gate itself stays EXPERIMENTAL: instrumentation records telemetry only and never enforces a budget, blocks a run, or promotes the gate to a mandatory ritual.
