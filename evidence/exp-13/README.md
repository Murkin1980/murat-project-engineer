# EXP-13 evidence directory

This directory holds EXP-13 low-cost evaluation evidence.

## What lives here now

- `PILOT_BATCH1_PRE_REGISTRATION.json` — frozen pre-registration of Pilot
  Batch 1: 6 tasks (T-001, T-004, T-006, T-008, T-010, T-012) × routes
  A / B / premium = 18 planned runs. It records the *plan only*; `usage_ref` is
  `null` for every entry and no execution evidence is fabricated before merge.

Pilot execution is partially unblocked. `scripts/usage_from_router_log.py` can
produce honest estimated USAGE_RECORDs for isolated, metered A/B Router event
windows. Premium remains blocked because current native `gpt-5.6-sol` events
contain no token counts. The three T-008 entries stop before execution and
therefore legally retain `usage_ref: null`. No synthetic usage files should be
added to unblock the batch.

## Attempt 2026-09-30 — BLOCKED at the usage-evidence gate

`PILOT_BATCH1_ATTEMPT_2026-09-30/` records the registered batch attempt
(runner: `experiments/exp-13/harness/exp13_pilot_attempt.py`, base commit
`66dc1c5`): 18/18 cases attempted through the harness with the registered
`usage_ref: null`; the three T-008 routes completed via pre-execution
escalation (`HUMAN_REVIEW_REQUIRED` / `HUMAN_REQUIRED`, unobserved usage,
`cost_usd: null`); the 15 proceeding routes were refused by the fail-closed
evidence gate (`ContractError: usage record is required when the run proceeds
to execution`); the registered batch CLI aborted with zero files written; all
decisions deterministic across repetitions; observed/estimated/unobserved =
0/0/18; no synthetic telemetry substituted. See
`experiments/exp-13/FINDINGS.md` for the analysis. The per-run
`EXP13-<task>-<route>.json` batch outputs below still belong to the future
unblocked run; the attempt directory intentionally does not create them for
proceeding routes.

## What lands here after merge

Per-run `EXP13_EXECUTION_RECORD` files named `EXP13-<task>-<route>.json`, each
produced by `scripts/exp13_harness.py` from a real `USAGE_RECORD`:

```
python scripts/exp13_harness.py --batch evidence/exp-13/PILOT_BATCH1_PRE_REGISTRATION.json --base-dir evidence/exp-13
```

Plus `EXP13-PILOT-BATCH1_SUMMARY.json` (the harness's `summarize` output).

## Pilot Batch 1 rules (frozen)

- 6 tasks × 3 routes = 18 real runs.
- Every executed run records `exp13_checks` result + `USAGE_RECORD` +
  retries / calls / escalation / defects / cost.
- T-008 legally produces `HUMAN_REVIEW_REQUIRED` (production change signal).
- After 18 runs: STOP and analyse. No automatic transition to further work.
