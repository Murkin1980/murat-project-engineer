# EXP-13 — OpenCode Go Connectivity Preflight

Status: OWNER-AUTHORIZED PREFLIGHT  
Primary disposition: **EXTEND_EXISTING**  
Experiment: `EXP-13 — Low-cost evaluation harness`  
Repository: `Murkin1980/murat-project-engineer`

## Purpose

Before spending money or starting EXP-13 Pilot Batch 1, verify that the Arena environment can actually:

1. access the frozen OpenCode Go routes;
2. make a real call to each required model;
3. obtain honest token/usage telemetry;
4. convert that telemetry through the existing MPE usage adapter without fabrication.

This is a connectivity/evidence preflight only.

**Do not start Pilot Batch 1.**

## Frozen routes under test

From EXP-13:

- Route A: `opencode-go/deepseek-v4-flash`
- Route B: `opencode-go/kimi-k2.7-code`

Do not substitute other providers or models in this preflight.

## Startup

Read first:

- `AGENTS.md`
- `docs/governance/SCOPE-CHANGE-CONTROL.md`
- `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`
- `scripts/usage_from_router_log.py`

Use EXP-29 bootstrap if required by `AGENTS.md`.

## Step 1 — credential/config presence

Check whether the Arena runtime has usable OpenCode/OpenCode Go provider configuration or credentials.

Allowed:
- inspect environment variable names/config presence;
- inspect provider/router configuration paths;
- inspect non-secret metadata needed to identify the provider.

Forbidden:
- print API keys/tokens/secrets;
- commit credentials;
- copy credentials into evidence.

Report only:
- `PRESENT` / `ABSENT`;
- configuration source/type;
- provider name;
- whether the config appears scoped to Arena/Router/local runtime.

## Step 2 — minimal live calls

Only if credentials/config are present:

Make exactly **one minimal live call** to Route A and exactly **one minimal live call** to Route B.

Prompt:

`Reply with exactly OK`

No EXP-13 dataset task may be used here.

Do not retry repeatedly. One bounded retry is allowed only for an obvious transient transport error and must be reported.

For each route record:

- requested model;
- actual model/provider returned, if observable;
- success/failure;
- response content;
- latency;
- input tokens;
- output tokens;
- total tokens if supplied;
- request/run/event id if supplied;
- observed cost if supplied by the provider;
- source location of the usage evidence.

Do not estimate missing token counts.

Do not fabricate cost.

## Step 3 — usage evidence compatibility

For each successful route call, test whether the real telemetry can be consumed by:

`scripts/usage_from_router_log.py`

Use the actual event window / model / expected call count.

The adapter must fail closed if the evidence is incomplete or mixed.

A valid result must demonstrate that a real EXP-13 `USAGE_RECORD` could be produced from this telemetry without invented fields.

Preserve generated preflight usage records only if they are clearly labelled `PREFLIGHT_ONLY` and cannot be mistaken for Pilot Batch 1 evidence.

## Step 4 — classify exactly one result

Return exactly one primary result:

### READY_FOR_EXP13

Use only when all are true:
- Route A callable;
- Route B callable;
- real token usage exists for both;
- telemetry is attributable to the isolated calls;
- `usage_from_router_log.py` can produce valid records for both without fabrication.

### CALLABLE_BUT_USAGE_BLOCKED

Use when:
- Route A and/or B responds successfully;
- but required token/usage evidence is missing, mixed, opaque, or incompatible with the adapter.

### CREDENTIALS_MISSING

Use when:
- required OpenCode Go/provider credentials or configuration are absent from the Arena environment.

### PROVIDER_BLOCKED

Use when:
- credentials/config appear present;
- but the provider/model calls fail for permissions, model availability, billing, endpoint, or provider-access reasons.

Do not invent a fifth status.

## Evidence

Create:

`evidence/exp-13/opencode-go-preflight/`

Minimum files:

- `README.md`
- `RESULT.json`
- `ROUTE_A.md`
- `ROUTE_B.md`

Optional:
- sanitized adapter output / usage records;
- sanitized command transcript.

Never store secrets.

`RESULT.json` must include:

- result;
- route A callable;
- route B callable;
- token usage available A/B;
- adapter valid A/B;
- cost observed/unobserved;
- blocker;
- next action.

## Spending boundary

This preflight is intentionally tiny.

Maximum intended paid work:
- one minimal Route A call;
- one minimal Route B call;
- at most one bounded transient retry per route.

Do not run the 18-run Pilot Batch.

Do not perform benchmark tasks.

Do not top up or purchase anything automatically.

## Repository boundary

Allowed changes:
- preflight evidence under `evidence/exp-13/opencode-go-preflight/`;
- a short factual append to EXP-13 documentation if needed.

Forbidden:
- changing frozen EXP-13 routes;
- changing thresholds;
- changing dataset;
- changing pricing snapshot;
- changing Pilot Batch pre-registration;
- changing Router authority;
- production deployment;
- new service/runtime/database/queue;
- storing credentials.

## Interpretation

If result is `READY_FOR_EXP13`:
- EXP-13 remains `READY_TO_TEST`;
- next action is owner approval to start the frozen Pilot Batch 1.

If result is `CREDENTIALS_MISSING`:
- stop;
- report which configuration class is missing;
- do not propose synthetic usage.

If result is `CALLABLE_BUT_USAGE_BLOCKED`:
- stop;
- the provider is not yet suitable for the current frozen EXP-13 evidence contract.

If result is `PROVIDER_BLOCKED`:
- stop;
- distinguish billing/permission/model/endpoint failure when observable.

## Terminal report

```text
RESULT: READY_FOR_EXP13 / CALLABLE_BUT_USAGE_BLOCKED / CREDENTIALS_MISSING / PROVIDER_BLOCKED
ROUTE A CALLABLE: YES/NO
ROUTE B CALLABLE: YES/NO
ROUTE A TOKENS: OBSERVED/UNAVAILABLE
ROUTE B TOKENS: OBSERVED/UNAVAILABLE
ROUTE A ADAPTER: PASS/FAIL/NOT_RUN
ROUTE B ADAPTER: PASS/FAIL/NOT_RUN
OBSERVED COST: <value or UNOBSERVED>
SECRETS STORED: NO
PILOT BATCH STARTED: NO
REPOSITORY CHANGES:
BLOCKER:
NEXT ACTION:
```

## Merge boundary

Open one bounded PR against `murat-project-engineer/main`.

Do not merge automatically.

Stop after the preflight result and evidence are recorded.
