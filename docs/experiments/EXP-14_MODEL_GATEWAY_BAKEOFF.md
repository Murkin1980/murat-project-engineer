# EXP-14 — Model Gateway Bake-off

Date: 2026-08-21  
Status: SPEC READY / EXECUTION DEFERRED UNTIL ACTIVE EXP-13 IS SAFELY CHECKPOINTED  
New Idea Filter disposition: `EXTEND_EXISTING`  
Execution tier: `VERIFIED`  
Deep change: `NO` for the bounded experiment described here

## Purpose

Evaluate whether Murat Project Engineer can delegate low-level provider execution, fallback and authoritative usage telemetry to a mature model gateway while retaining all semantic routing, governance, risk and deep-change authority inside MPE.

This experiment does **not** authorize production migration, Router replacement, credential-boundary changes, a new central runtime, or a new repository.

## Mandatory architectural boundary

```text
MPE semantic/governance decision
            ↓
execution policy / capability class
            ↓
compute-budget preflight
            ↓
execution gateway interface
            ↓
provider/model execution
```

MPE owns:

- `FAST / VERIFIED / DEEP-CHANGE`;
- New Idea Filter and project priority;
- risk classification and human approval gates;
- Expert / Team selection;
- deterministic and semantic review policy;
- capability class (`CHEAP / BALANCED / PREMIUM`);
- maximum allowed compute and escalation policy;
- business-value and experiment-governance decisions.

A gateway may own only low-level execution concerns such as provider API normalization, endpoint/model selection inside an MPE-approved envelope, retries, fallback, timeout, rate limits, health handling and usage telemetry.

The gateway MUST NOT become the authority for risk classification, task policy, deep-change decisions or automatic downgrade of an MPE-approved capability class.

## Current repository checkpoint

```text
CURRENT_REPO_STATE:
- repository: Murkin1980/murat-project-engineer
- default branch: main
- current architecture: MPE plugin/runbooks above an unchanged Codex Router boundary
- no model-gateway runtime exists in this repository

CURRENT_ACTIVE_EXPERIMENT:
- EXP-13 — Low-cost evaluation harness + pre-execution rework
- status: ACTIVE
- Pilot Batch 1 pre-registered, not yet executed

NEXT_FREE_EXPERIMENT_ID:
- EXP-14

CURRENT_ROUTER_BOUNDARY:
- MPE/Codex coordinator owns task classification, role selection, cost policy and reviewer escalation
- route profiles resolve to explicit model routes
- Codex Router remains the inference/protocol/credential gateway
- no Router authority transfer is authorized

CURRENT_COMPUTE_BUDGET_STATE:
- Compute Budget Gate is experimental
- scripts/compute_budget.py remains the preflight/reforecast source of truth
- contracts/USAGE_RECORD.md remains the canonical usage telemetry contract
- scripts/usage_instrumentation.py is the sole projection path into RUN_REPORT and COMPUTE_BUDGET usage blocks
- measurement provenance remains observed | estimated | unobserved

FILES_TO_CHANGE:
- docs/MURAT_AI_STACK_V2_IMPLEMENTATION_PLAN.md

FILES_TO_ADD:
- docs/experiments/EXP-14_MODEL_GATEWAY_BAKEOFF.md

DEEP_CHANGE:
- NO for specification and isolated bounded harness work
```

If implementation later requires Router authority transfer, production traffic migration, credential ownership changes, security-boundary changes or a new central runtime, then:

`DEEP_CHANGE = YES`

Stop and request explicit user approval before proceeding.

## Hypotheses

Primary hypothesis:

> MPE can delegate low-level multi-provider execution, fallback and usage telemetry to a mature gateway without delegating semantic routing, governance or risk authority, reducing duplicated infrastructure while improving real cost observability.

Secondary hypothesis:

> Gateway/provider observed usage can materially improve calibration of the existing MPE Compute Budget estimator.

Null hypothesis:

> A gateway adds operational complexity, latency or architectural ambiguity without sufficient reliability, cost or telemetry benefit.

## Candidates

Minimum comparison:

1. current MPE / Router path — control;
2. LiteLLM — primary gateway candidate.

Where practical and cheap:

3. Cloudflare AI Gateway — managed-infrastructure comparison candidate.

Candidate versions and exact provider/model slugs must be verified from current official documentation at execution time and recorded in evidence. No model names are frozen by this specification.

## Provider/model matrix

Start with the smallest useful matrix:

```text
ECONOMY
- Qwen or equivalent
- DeepSeek or equivalent

ALTERNATIVE
- Kimi or comparable provider if accessible

CONTROL
- one OpenAI, Anthropic or Gemini model
```

Use only 2–3 provider/model paths for the first bounded run. Do not purchase large credits.

## Experiment questions

The experiment must answer:

1. Can MPE use one stable execution interface across multiple providers?
2. Can provider/model changes occur without changing MPE semantic task policy?
3. Can controlled fallback work reliably?
4. Can MPE preserve control over `CHEAP / BALANCED / PREMIUM` classes?
5. Can actual token usage be captured accurately?
6. Can actual cost be captured authoritatively or reconstructed reliably?
7. Can retries and fallback events be observed?
8. Does gateway use materially increase latency?
9. Does it simplify or complicate credential management?
10. Does it create another source of truth?
11. Does it duplicate the existing Router?
12. Can current `USAGE_RECORD` ingest useful telemetry without a second schema?
13. Does real telemetry improve Compute Budget forecasting?
14. Can gateway failure occur without corrupting MPE state?
15. Can the gateway be restarted/replaced easily?
16. Does it create unacceptable vendor lock-in?

## Minimal implementation scope

Do not build a production gateway.

```text
MPE test harness
      ↓
minimal gateway adapter
      ↓
LiteLLM
      ↓
2–3 providers/models
```

Any adapter must remain isolated to experiment scope and must not become a parallel application architecture.

Before writing custom gateway-related code, check whether the selected gateway already provides the capability. Do not reimplement generic provider adapters, retry engines, basic fallback, generic load balancing, basic token counting, rate limiting, virtual keys or generic spend ledgers unless evidence proves the gateway capability is insufficient for an MPE-specific requirement.

## Workload

Use a bounded deterministic corpus of 10–20 representative calls. Include:

- simple classification;
- coding;
- structured generation;
- review;
- reasoning;
- summarization;
- tool-oriented prompt where supported.

At least some cases must have deterministic or independently verifiable outputs. Subjective answer quality alone is insufficient.

## Required tests

### Test A — Basic compatibility

Send the same bounded request through the current control path and the gateway path. Capture output, quality result and telemetry.

### Test B — Provider switch

Change provider/model via gateway configuration without modifying MPE semantic task logic.

PASS if MPE logic remains unchanged.

### Test C — Fallback

Force or simulate primary-provider failure. Record first provider, failure, fallback provider, retries, latency, token usage and cost.

### Test D — Budget telemetry

Capture input tokens, cached input tokens where available, output tokens, provider/model, model calls, retries, cost and measurement source. Map them into existing MPE telemetry.

### Test E — Estimate versus actual

Run normal MPE Compute Budget preflight before execution and compare:

```text
estimated min / expected / max
vs
observed final cost
```

### Test F — Gateway outage

Make the gateway unavailable and verify:

- failure is explicit;
- MPE state remains valid;
- no false PASS occurs;
- retry is safe.

### Test G — Restart/recovery

Restart the gateway and verify recovery. Lifecycle recovery is mandatory evidence, not optional operability polish.

## Telemetry mapping rule

`contracts/USAGE_RECORD.md` remains the canonical usage source of truth.

Do not create a second billing schema, telemetry platform or cost source of truth.

For each call, collect gateway-specific raw evidence as experiment evidence, then map only contract-supported values through the existing `UsageRecorder` path.

Current canonical fields include:

```text
run_id
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
progress_checkpoints
measurement_source
measurement
```

The desired experiment dimensions below are evaluation metadata, not automatic additions to `USAGE_RECORD`:

```text
experiment_case_id
task_class
risk_tier
capability_class
gateway
fallbacks
latency_ms
time_to_first_token
success
error_type
fallback_success
quality_result
deterministic_gate_result
```

Add any canonical field only after proving a real contract gap. Prefer experiment evidence/report fields first.

### Measurement provenance

Preserve existing semantics:

- `observed` only from authoritative sources already allowed by instrumentation policy (`provider_api`, `router_billing`, `usage_api`);
- `estimated` for execution logs, price reconstruction or operator estimates;
- `unobserved` when authoritative telemetry is absent.

A gateway estimate MUST NOT be promoted to observed merely because the gateway reports it.

## Primary metrics

### Cost

- cost per successful task;
- total experiment cost;
- preflight estimate error;
- premium-model usage rate.

### Quality

- deterministic PASS rate;
- required semantic criteria;
- regression against current control.

### Reliability

- success rate;
- fallback success;
- retry rate;
- outage/restart recovery.

### Performance

- total latency;
- gateway overhead;
- time to first token where available.

### Operability

- setup/config complexity;
- logs and debugging burden;
- restart/recovery;
- credentials handling.

### Architectural fit

- provider independence;
- MPE policy independence;
- schema reuse;
- Router overlap;
- local/self-hosted future compatibility;
- vendor lock-in.

## Preliminary acceptance criteria

A gateway candidate may advance only if:

1. deterministic quality is not materially degraded;
2. MPE semantic routing remains outside the gateway;
3. provider changes require no semantic-policy code changes;
4. controlled fallback works;
5. useful usage telemetry maps through existing MPE contracts;
6. no second billing/telemetry source of truth is created;
7. operational complexity is acceptable;
8. rollback is trivial;
9. no credentials are committed;
10. cost/usage observability improves materially.

Preferred additional target: Compute Budget can be calibrated against several genuinely observed runs.

## Kill criteria

Stop or reject if:

- gateway requires replacing MPE governance;
- useful value cannot be measured without major Router modification;
- telemetry is less reliable than the control path;
- abstraction causes unacceptable feature loss;
- latency overhead is material without compensating benefit;
- operational complexity exceeds measurable value;
- credentials/security become worse;
- quality decreases materially;
- gateway becomes a new central state authority;
- dependency is not reversibly replaceable;
- basic testing requires production migration.

Do not rationalize around a failed kill criterion; record the failure.

## Security

Never commit provider API keys, gateway master keys, Cloudflare secrets, OpenAI/Anthropic/Gemini/DeepSeek/Qwen/Kimi/Moonshot/OpenRouter keys or other credentials.

Committed configuration may contain placeholders only. Use environment variables or an already approved secret mechanism.

## Rollback

Specification rollback: revert this document and the Stage 4 roadmap update.

Experimental harness rollback, if later implemented: delete/disable the isolated experiment adapter/harness and return to the current MPE/Router control path. No production migration is part of EXP-14, so rollback must not require data migration or Router reconfiguration.

## Relationship to existing experiments

- EXP-12 remains a triage/governance experiment and its historical evidence must not be rewritten.
- EXP-13 remains the active low-cost evaluation harness. Do not modify its frozen dataset, routes, thresholds, pricing or evidence for this experiment.
- EXP-14 may reuse risk-tier metadata, deterministic evaluation infrastructure, run reports and compute-budget telemetry, but evidence must remain distinguishable.

### Priority / sequencing rule

EXP-14 has elevated priority because it affects multi-provider cost, observed telemetry and future routing economics, but it must **not** interrupt the currently active controlled EXP-13. Execute EXP-14 only after EXP-13 is completed or safely checkpointed under its own rules.

## Required final report

When the experiment is actually executed, report:

### RESULT

One of:

```text
PASS
PARTIAL
FAIL
BLOCKED
```

### Evidence

- exact gateway version;
- exact provider/model slugs;
- test matrix;
- token usage and measurement source;
- cost;
- latency;
- fallbacks/retries;
- failures;
- deterministic quality;
- configuration complexity.

### Comparison

```text
Current control
vs
LiteLLM
vs
Cloudflare AI Gateway if tested
```

### Compute Budget calibration

```text
preflight estimate
actual observed cost
absolute error
percentage error
```

### Architecture finding

Explicitly state whether MPE/gateway responsibility separation remained intact.

### Recommendation

Recommend exactly one next direction. Do not automatically integrate the winner.

## Completion definition

EXP-14 specification is complete when:

- Stage 4 roadmap reflects the gateway evaluation;
- this specification exists;
- MPE/Router authority boundaries remain unchanged;
- workload, tests, metrics, acceptance and kill criteria are explicit;
- telemetry reuses existing MPE contracts;
- rollback is explicit;
- no production migration occurred;
- no new repository was created;
- no secret was committed.

The objective is not to install LiteLLM. The objective is to determine with evidence whether a model gateway should become an execution layer beneath MPE while MPE remains the governance and semantic-routing authority.
