# SUPERSEDED — former EXP-34 Self-Improving Harness intake

**Owner decision: MERGE (2026-10-30).** EXP-34 is **CANCELLED / NOT RESERVED / DO NOT REGISTER**. This file is historical intake only. Do not execute its former experiment plan.

**Canonical consolidation target:** [Harness² Self-Improvement Lab PR #113](https://github.com/Murkin1980/murat-project-engineer/pull/113), branch `experiment/harness2-self-improvement-lab`, authoritative plan `experiments/harness2-self-improvement/EXPERIMENT_PLAN.md`. Preserve E0, E1–E5, and CP-SI-01…07; do not renumber EXP-30…33.

**Priority dependency:** PR #115 stabilization/recovery must be accepted and validated first, before Harness² experiment execution.

## CP-00 collision-resolution handoff for Arena

1. Read mandatory MPE governance and the current PR #113 plan; re-read this superseded intake and current registry/PR state.
2. Record comparison of goals, mechanics, checkpoints, metrics, safety gates, and genuinely unique requirements. Eliminate duplicate design.
3. Suggest only minimal missing requirements for PR #113; no parallel registry entry or experiment implementation.
4. Check reuse of EXP-27 orchestration/budget/approval, EXP-28 retrospective, and EXP-29 Git-derived bootstrap.
5. Keep CP-SI-01…07 unchanged. Record CP-00 disposition and prepare existing CP-SI-01 as documentation/audit only; no independent execution before upstream PR #115 readiness.
6. Verify PR branch/work permissions before any edit. Do **not** automatically change PR #113, merge, deploy, run a self-modifying agent, or weaken governance. On deep-change, report `DEEP_CHANGE_REQUIRED` and stop.
7. Final report: PASS / PARTIAL / BLOCKED; overlap/unique requirements matrix; minimal proposed diffs; PR/SHA; next authorized checkpoint.

## Initial comparison (design review; verify in Arena)

| Topic | PR #113 | Superseded intake | Recommendation |
| --- | --- | --- | --- |
| Objective | Recursive Propose-Probe-Compose; safe generalization | Three sequential harness improvements | OVERLAP; keep #113 |
| Runs | E1 baseline; E2 k=1/3/5; E3 held-out transfer | A baseline + B/C/D three iterations | OVERLAP; optional predeclared three-step sequential arm within E2, only if marginal evidence |
| Metrics | Held-out success, cost/correct task, tokens, time, retries, violations | Also context bytes/tool calls explicitly | Candidate tiny addition: measure context bytes and tool calls when instrumentable |
| Safety | E0 isolation, E4 adversarial suite, fail-closed | Allowlisted scratch diff, rollback, immutable governance | OVERLAP; retain #113; make rollback checks explicit if currently untested |
| Reuse | EXP-29 and existing MPE | EXP-27/28/29 explicitly | Candidate tiny addition: explicitly document EXP-27 lease/budget/approval and EXP-28 retrospective reuse |
| Evidence | Hashes, settings, costs, frozen rubrics, logs | Four-arm table, candidate diff, outcome | OVERLAP; no duplicate evidence format |
| Scope | CP-SI-01 design only, STOP | Full execution in one session | Conflict: #113 wins; do not jump to execution |

Historical EXP-34 instructions are superseded by this file.