# EXP-13 evidence directory

This directory holds EXP-13 low-cost evaluation evidence.

## What lives here now

- `PILOT_BATCH1_PRE_REGISTRATION.json` — frozen pre-registration of Pilot
  Batch 1: 6 tasks (T-001, T-004, T-006, T-008, T-010, T-012) × routes
  A / B / premium = 18 planned runs. It records the *plan only*; `usage_ref` is
  `null` for every entry and no execution evidence is fabricated before merge.

Pilot execution is partially complete. `EXP13-T-008-{A,B,premium}.json` are the
three legal pre-execution stops; each records `HUMAN_REVIEW_REQUIRED` without a
model call. The Router and Codex-rollout adapters provide fail-closed telemetry
paths for A/B and premium respectively. The remaining 15 model runs are blocked
until a versioned execution/scoring protocol freezes prompts, output artifacts,
artifact checks and defect/retry/tool-call attribution. No synthetic usage or
post-hoc scoring rules should be added to unblock the batch.

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
