# AI Compute Budget — canonical contract v1

Canonical name: `AI Compute Budget`. The top-level metric is the whole AI compute budget, never an OpenAI-only cost. `observed` / `estimated` / `unobserved` usage are distinct and must not be conflated.

```yaml
compute_budget:
  currency: USD
  planned_budget:
  hard_limit:

preflight:
  input_tokens_min:
  input_tokens_expected:
  input_tokens_max:
  output_tokens_min:
  output_tokens_expected:
  output_tokens_max:
  estimated_cost_min:
  estimated_cost_expected:
  estimated_cost_max:
  confidence:

usage:
  input_tokens:
  cached_input_tokens:
  output_tokens:
  estimated_cost:
  measurement: observed | estimated | unobserved

forecast:
  estimated_total_cost_min:
  estimated_total_cost_expected:
  estimated_total_cost_max:
  remaining_cost_expected:
  confidence:

routing:
  recommended_stack:
  actual_provider_mix:

efficiency:
  project_progress_percent:
  budget_consumed_percent:
  cost_per_progress_percent:

status:
  budget_status: GREEN | YELLOW | ORANGE | RED | UNOBSERVED
  burn_rate_status: OK | BURN_RATE_ANOMALY | UNOBSERVED
  burn_rate_ratio:
```

## Field reference (flat)

- compute_budget_currency: fixed USD
- compute_budget_planned_budget:
- compute_budget_hard_limit:
- preflight_input_tokens_min:
- preflight_input_tokens_expected:
- preflight_input_tokens_max:
- preflight_output_tokens_min:
- preflight_output_tokens_expected:
- preflight_output_tokens_max:
- preflight_estimated_cost_min:
- preflight_estimated_cost_expected:
- preflight_estimated_cost_max:
- preflight_confidence: low | medium | high
- usage_input_tokens:
- usage_cached_input_tokens:
- usage_output_tokens:
- usage_estimated_cost:
- usage_measurement: observed | estimated | unobserved
- forecast_estimated_total_cost_min:
- forecast_estimated_total_cost_expected:
- forecast_estimated_total_cost_max:
- forecast_remaining_cost_expected:
- forecast_confidence: low | medium | high
- routing_recommended_stack:
- routing_actual_provider_mix:
- efficiency_project_progress_percent:
- efficiency_budget_consumed_percent:
- efficiency_cost_per_progress_percent:
- status_budget_status: GREEN | YELLOW | ORANGE | RED | UNOBSERVED
- status_burn_rate_status: OK | BURN_RATE_ANOMALY | UNOBSERVED
- status_burn_rate_ratio:

## Rules

- Never report an estimated or unobserved value as observed.
- `burn_rate_ratio = budget_consumed_percent / project_progress_percent`; raise `BURN_RATE_ANOMALY` on a clear progress/budget divergence.
- The preflight (initial estimate) and the burn-rate reforecast are separate blocks and must not be conflated.
- Provider scenarios: `economy` (DeepSeek / MiniMax / Qwen / Kimi low-cost stack) and `premium` (OpenAI / Anthropic benchmark). OpenAI is a benchmark, not the headline metric.
