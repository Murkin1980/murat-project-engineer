# EXP-13 — Low-cost evaluation harness + pre-execution rework

Status: ACTIVE — harness published; Pilot Batch 1 pre-registered, not yet executed
Date: 2026-08-21
New Idea Filter disposition: `EXPERIMENT` (extends the EXP-12 triage line)
Execution tier: `VERIFIED`

## Reconstruction note (read first)

This revision is a **controlled reconstruction** of a previously built but
unpublished EXP-13 harness whose original patch was not preserved. It is not a
byte-for-byte restoration. The frozen semantics below were re-established from
the approved experiment requirements and are the authoritative contract going
forward. Any future change to the dataset, thresholds, pricing snapshot,
routes, or acceptance criteria requires a new versioned asset plus a documented
decision — never a silent edit.

Known difference from the lost implementation: this reconstruction ships more
regression coverage, so the full suite runs **180 tests OK (1 skip)** rather
than the lost implementation's reported 159. No frozen semantics depend on that
count; it is recorded here only for traceability.

## Hypothesis

A low-cost, deterministic pre-execution check stage can decide whether a task
may proceed on a chosen route (A / B / premium) *before* real budget is spent,
and can correctly escalate to human review or a stronger route when the triage
says the task must not execute autonomously — at a fraction of the cost of
discovering that after execution.

## What this is

- `contracts/EXP13_EXECUTION_RECORD.schema.json` — the canonical record of one
  harness run: pre-execution checks, full checks, escalation, outcome, defects,
  and cost (never fabricated).
- `scripts/exp13_checks.py` — deterministic check pipeline (see frozen
  semantics below).
- `scripts/exp13_harness.py` — wraps checks into an immutable record; enforces
  the batch STOP rule (`max_runs`).
- `experiments/exp-13/` — frozen dataset v2 (12 tasks), routes, thresholds and
  pricing snapshot.
- `tests/test_exp13_checks.py`, `tests/test_exp13_harness.py` — unit tests.
- `evidence/exp-13/PILOT_BATCH1_PRE_REGISTRATION.json` — frozen batch plan.

## Frozen semantics

### Dataset v2 (`experiments/exp-13/tasks_v2.json`)

12 tasks `T-001`…`T-012`. Each task is a deterministic triage input (the
`scripts/triage_engine.py` contract) plus a pre-registered expected label
(`risk_tier` + `human_approval_required`). The expected labels are frozen
acceptance criteria; the harness's `triage_expected_match` check fails if the
triage engine drifts from them.

### Routes (`experiments/exp-13/routes.json`)

| Route | Profile | Model slug |
|---|---|---|
| `A` | `cheap-research` | `opencode-go/deepseek-v4-flash` |
| `B` | `coding` | `opencode-go/kimi-k2.7-code` |
| `premium` | `strong-review` | `gpt-5.6-sol` |

### Pricing snapshot (`experiments/exp-13/pricing_snapshot.json`)

Dated `2026-08-21`, USD per 1,000,000 tokens, consistent with the Compute
Budget `PRICING_SNAPSHOT`. Observed cost stays observed; reconstructed cost is
labelled `estimated`; missing spend is `null` / `unobserved`.

### Thresholds (`experiments/exp-13/thresholds.json`)

- `max_retries` = 2
- `max_defects` = 0
- `max_escalations_per_run` = 1
- `cost_budget_ratio_soft` = 0.7, `cost_budget_ratio_hard` = 1.0

### Checks (9, in order)

Pre-execution (cheap; run before any execution):
`route_resolves`, `triage_expected_match`, `acceptance_present`,
`human_review_due`.

Execution (run only when the run proceeds):
`usage_valid`, `usage_consistent`, `retries_within_limit`,
`defects_within_limit`, `cost_within_limit`.

### Escalation (derived, never hand-set)

Precedence: human > premium > none.

- `HUMAN_REVIEW_REQUIRED` — triage mandates human approval (any approval or
  deep-change signal). The run stops before execution.
- `PREMIUM_REQUIRED` — the triage tier is `DEEP-CHANGE` and the route is not
  `premium`. Note: the current triage engine always marks `DEEP-CHANGE`
  human-approval-required, so end-to-end the human escalation wins first; the
  premium rule is a distinct, separately tested escalation class
  (`escalation_for`). A deep change is never auto-executed on any route.
- `NONE` — the run may proceed.

### Outcome (derived, never hand-set)

- `HUMAN_REQUIRED` — human-review escalation.
- `REWORK` — premium escalation, or a non-fatal check failure
  (usage_consistent / retries / defects / cost).
- `BLOCKED` — the usage evidence is invalid.
- `PASS` — every applicable check passes.

### Cost (never fabricated)

- Escalated (not executed) run → `cost_usd: null`, `unobserved`.
- Executed run → observed cost if present, else reconstructed `estimated`,
  else `null` / `unobserved`.

## PASS / FAIL criteria

PASS for this stage requires:

1. Frozen assets present and versioned (dataset v2, routes, thresholds, pricing).
2. Deterministic record generation (same inputs → same record).
3. T-008 (production change) legally escalates to `HUMAN_REVIEW_REQUIRED` on
   every route.
4. All 12 frozen expected labels are reproduced by the triage engine.
5. Package validation passes; no prohibited architecture element is introduced.
6. The batch harness enforces STOP after `max_runs`.

## Metrics (recorded per run)

- check results (all 9)
- escalation + outcome
- retries / model_calls / tool_calls
- defects
- cost_usd + cost_measurement

## Non-scope

- No real execution of Pilot Batch 1 here (post-merge, separate task).
- No dataset v2 / thresholds / pricing / routes / acceptance changes.
- No autonomous execution, approval, routing authority, service, or scheduler.
- No fabricated usage telemetry.

## How to run (local)

```powershell
python scripts/exp13_harness.py --task T-008 --route A --output /tmp/exp13.json
python scripts/exp13_harness.py --batch evidence/exp-13/PILOT_BATCH1_PRE_REGISTRATION.json --base-dir evidence/exp-13
python -m unittest discover -s tests
python scripts/validate_package.py .
```

The single-run CLI needs a real `USAGE_RECORD` (`--usage`) for any task that
proceeds to execution; a task that escalates before execution needs none.

## Continuation instructions

1. After merge, run Pilot Batch 1 (6 tasks × 3 routes = 18 runs) with real
   `USAGE_RECORD` evidence; the harness enforces STOP after 18.
2. Record, per run, the `exp13_checks` result + usage + retries/calls/
   escalation/defects/cost.
3. T-008 must produce `HUMAN_REVIEW_REQUIRED`; anything else is a defect.
4. After 18 runs, STOP and analyse. Do not auto-continue.
5. Change thresholds / pricing / routes / dataset only in a new versioned asset
   with a documented decision.
