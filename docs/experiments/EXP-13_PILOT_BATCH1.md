# EXP-13 — Pilot Batch 1 plan

Date: 2026-08-21
Status: PARTIALLY EXECUTED — 3 pre-execution escalation runs recorded; 15 model runs blocked pending a frozen execution/scoring protocol
Parent: `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`

## Pre-registration

Frozen manifest: `evidence/exp-13/PILOT_BATCH1_PRE_REGISTRATION.json`.

6 tasks × 3 routes = **18 planned runs**:

- Tasks: `T-001`, `T-004`, `T-006`, `T-008`, `T-010`, `T-012`
- Routes: `A` (cheap-research), `B` (coding), `premium` (strong-review)

| Task | Class | Expected on every route |
|---|---|---|
| T-001 | FAST documentation sync | proceeds; PASS if clean |
| T-004 | VERIFIED invoice feature | proceeds |
| T-006 | VERIFIED validator gate | proceeds |
| T-008 | VERIFIED production deploy | `HUMAN_REVIEW_REQUIRED` (legal) |
| T-010 | VERIFIED case export | proceeds |
| T-012 | VERIFIED mailbox refactor | proceeds |

## Per-run record

Every run produces an `EXP13_EXECUTION_RECORD` containing:

- `exp13_checks` result (all 9 checks)
- `USAGE_RECORD` (embedded)
- retries / model_calls / tool_calls
- escalation
- defects
- cost_usd + cost_measurement

## Frozen acceptance criteria

1. Exactly 18 runs; the harness enforces STOP after `max_runs` (18).
2. `T-008` → escalation `HUMAN_REVIEW_REQUIRED`, outcome `HUMAN_REQUIRED`, on
   **all three routes**. This is the one legal escalation.
3. The other 15 runs proceed and record real `USAGE_RECORD` evidence.
4. No execution evidence is created for A/B/premium before merge.

## STOP rule

After the 18 runs, STOP and analyse. Do not auto-continue into further batches
or into A/B/premium execution-evidence work in the same task.

## Execution checkpoint — 2026-08-25

The three T-008 routes were executed through the deterministic pre-execution
gate. All stopped before any model call with `HUMAN_REVIEW_REQUIRED` /
`HUMAN_REQUIRED`, null cost and unobserved usage, as pre-registered.

The remaining 15 runs have not started. The frozen assets define task summaries,
routes and telemetry, but do not define the model prompt, required output
artifact, artifact-level acceptance checks, or an observable procedure for
assigning defects/retries/tool calls. Inventing those rules after seeing the
registered batch would make route comparisons non-reproducible. A versioned,
pre-registered execution/scoring protocol is required before model calls.
