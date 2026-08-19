# Run Usage Record — canonical contract v1

Machine-readable per-run usage telemetry captured by `scripts/usage_instrumentation.py`. This is the forward-validation companion to the `AI Compute Budget` contract: it records the fields a new run must write so the Compute Budget Estimator can later be validated on OBSERVED data.

```yaml
schema_version: 1.0
run_id:
provider:
model:
input_tokens:
cached_input_tokens:
output_tokens:
observed_cost:
model_calls:
tool_calls:
retries:
start_time:
end_time:
progress_checkpoints: []
measurement_source: provider_api | router_billing | usage_api | execution_log | price_reconstruction | operator_estimate | none
measurement: observed | estimated | unobserved
```

## Field reference (flat)

- usage_provider: primary provider (e.g. OpenCode Zen, OpenAI, Anthropic) or null
- usage_model: resolved model slug (e.g. opencode-go/deepseek-v4-flash) or null
- usage_input_tokens: total prompt/input tokens or null
- usage_cached_input_tokens: cached input tokens or null
- usage_output_tokens: total completion/output tokens or null
- usage_observed_cost: cost figure in USD or null
- usage_model_calls: number of model calls or null
- usage_tool_calls: number of tool calls or null
- usage_retries: number of retries or null
- usage_start_time: ISO-8601 datetime or null
- usage_end_time: ISO-8601 datetime or null
- usage_progress_checkpoints: [{progress_percent, cost_usd, measurement_source}]
- usage_measurement_source: where the telemetry came from
- usage_measurement: observed | estimated | unobserved (derived from measurement_source)

## Source of truth

`USAGE_RECORD` is the canonical source of truth for usage telemetry. `RUN_REPORT.usage` and `COMPUTE_BUDGET.usage` are projections of `USAGE_RECORD` only and must not be written independently. The only projection paths are `usage_to_run_report` and `usage_to_compute_budget` in `scripts/usage_instrumentation.py`.

Note on `estimated_cost`: in the `COMPUTE_BUDGET.usage` block, `estimated_cost` is a generic destination field name, not a quality claim. The quality of the value is carried by `measurement`; when the source is `observed`, the value remains observed by provenance even though it lands in a field named `estimated_cost`. Do not rename `estimated_cost` — it is part of the canonical Compute Budget contract and changing it would break backward compatibility.

## Measurement rules

`measurement` is derived from `measurement_source` and never promoted:

- `observed` <- provider_api, router_billing, usage_api (authoritative telemetry).
- `estimated` <- execution_log, price_reconstruction, operator_estimate.
- `unobserved` <- none (or missing source).

An estimated or unobserved value is never reported as observed. When `measurement` is `unobserved`, `observed_cost` must be null. Missing counts stay null, never a fabricated zero.
