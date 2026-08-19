# MPE Compute Budget Gate

Status: EXPERIMENTAL / required for substantial execution preflight
Disposition: EXTEND_EXISTING

## Purpose

The Compute Budget Gate adds an explicit AI compute-economics check to Murat Project Engineer before substantial execution. It is not a billing system and must not invent precision when usage telemetry is unavailable.

## Mandatory execution sequence

New Idea Filter -> Scope Gate -> Compute Budget Preflight -> Budget Approval -> Execution -> Usage Capture -> Burn-rate Reforecast -> Completion Review

The gate applies to new repositories and to substantial stages of existing projects, including deep-change work, large refactors, migrations, multi-stage experiments, and large code-generation tasks.

## Canonical data contract

```yaml
compute_budget:
  currency: USD
  planned_budget: null
  hard_limit: null

preflight:
  input_tokens_min: null
  input_tokens_expected: null
  input_tokens_max: null
  output_tokens_min: null
  output_tokens_expected: null
  output_tokens_max: null
  estimated_cost_min: null
  estimated_cost_expected: null
  estimated_cost_max: null
  confidence: low|medium|high

usage:
  input_tokens: null
  cached_input_tokens: null
  output_tokens: null
  observed_cost: null
  measurement: observed|estimated|unobserved

forecast:
  projected_total_cost_min: null
  projected_total_cost_expected: null
  projected_total_cost_max: null
  projected_remaining_cost_expected: null
  confidence: low|medium|high
  burn_rate_per_progress_point: null

routing:
  recommended_stack: []
  actual_provider_mix: {}

efficiency:
  project_progress_percent: null
  budget_consumed_percent: null
  cost_per_progress_percent: null
  burn_rate_ratio: null
```

## Provider comparison

Preflight SHOULD compare at least:

1. economy routing: OpenCode Zen / Chinese or other low-cost stack;
2. premium benchmark: OpenAI and/or Anthropic when pricing data is available;
3. BYOK/other routing where relevant.

OpenAI cost is a benchmark, not the top-level metric. The top-level field is AI Compute Budget.

## Forecast semantics

All numeric usage values must carry a measurement status:

- observed: reported by a provider/router or derived from authoritative billing telemetry;
- estimated: calculated from known calls/context/pricing but not directly metered;
- unobserved: telemetry is missing and a precise claim is not defensible.

Never report an estimated or unobserved value as observed.

## Budget health states

Health is computed against projected total cost / hard limit:

- GREEN: <= 70%
- YELLOW: > 70% and <= 90%
- ORANGE: > 90% and <= 110%
- RED: > 110%
- UNOBSERVED: hard limit or usable forecast telemetry is unavailable

## Burn-rate anomaly

The dashboard and run reports SHOULD compare budget consumption against project progress.

Example:

- project progress: 25%
- budget consumed: 70%
- burn-rate ratio: 70 / 25 = 2.8x

This should raise a burn-rate anomaly even if the hard budget has not yet been exceeded.

## Reforecast rule

After sufficient execution evidence exists (normally 10-20% project progress or enough completed comparable tasks), MPE SHOULD prefer an evidence-based burn-rate reforecast over the initial preflight point estimate. The original estimate remains stored for calibration.

## MVP acceptance criteria

Evaluate the gate on 5-10 MPE runs.

Success target:

- actual final cost falls inside the preflight min-max band for >= 80% of runs;
- after approximately 20% progress, expected total-cost forecast is within roughly +/-25% of final cost for the majority of runs;
- economy routing does not reduce required PASS-rate or deterministic-check quality.

If these criteria fail, improve the estimator before expanding dashboard complexity.

## Dashboard representation

Each project card SHOULD show two separate bars:

- PROJECT PROGRESS
- AI BUDGET

Recommended supporting values:

- spent / planned budget;
- projected total cost range;
- expected remaining cost;
- cost per progress point;
- forecast confidence;
- budget health;
- burn-rate anomaly when present.

The dashboard should render a canonical MPE snapshot rather than become the source of truth for estimation logic.
