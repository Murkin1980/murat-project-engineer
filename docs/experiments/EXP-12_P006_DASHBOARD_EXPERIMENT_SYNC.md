# EXP-12 P-006 — Salamat Projects Dashboard experiment reconciliation

Status: OWNER-AUTHORIZED PROSPECTIVE CASE  
Parent: `docs/experiments/EXP-12_CLEARS_TRIAGE.md`  
Target: `Murkin1980/salamat-projects-dashboard`  
Pre-registration: `evidence/exp-12/prospective/P-006_PRE_REGISTRATION.json`

## Objective

Use a real current dashboard-maintenance task as prospective case P-006.

The human label is frozen before engine execution:

`VERIFIED / approval not required`

Do not alter it after seeing the engine output.

## Execution sequence

1. Sync current MPE `main`.
2. Read EXP-12 and the frozen P-006 pre-registration.
3. Run the deterministic triage engine against exactly the frozen P-006 input and record the output.
4. Then sync `Murkin1980/salamat-projects-dashboard` current `main`.
5. Read its `AGENTS.md` and required source-of-truth documents.
6. Inspect the current experiment view/data path and the open stale experiment-mirror PRs before changing anything.
7. Reconcile the dashboard's mirrored experiment information against current MPE `experiments/EXPERIMENT_REGISTRY.json` and referenced evidence.
8. Reuse the existing read-only source/snapshot architecture. Prefer removing/superseding stale duplicated facts over adding another layer.
9. Change only the smallest necessary dashboard data/source adapter, fixture/test, or evidence/docs files.
10. Run repository-required validation/tests/build.
11. Do not deploy.
12. Record the observed final classification after implementation.
13. Add P-006 execution/evaluation evidence back to MPE.

## Hard boundaries

Do not:
- add dashboard write-back;
- add task/Arena/Codex execution controls;
- create an API, Worker, backend, database, service, or second experiment registry;
- deploy or change Cloudflare config;
- redesign unrelated dashboard UI;
- change MPE canonical experiment statuses from the dashboard;
- blindly merge stale experiment mirror PRs.

If current dashboard architecture already derives the experiment view correctly and no code/data change is necessary, record a verified NO_CHANGE result rather than manufacturing a patch.

## Required evidence

In MPE:
- `P-006_EXECUTION.json`
- `P-006_EVALUATION.json`

In the dashboard PR/evidence:
- exact MPE source revision used;
- stale/conflicting mirror PRs identified;
- files changed or explicit NO_CHANGE;
- tests/build results;
- statement that deployment/write-back did not occur.

## Terminal report

```text
CASE: EXP12-P-006
HUMAN LABEL: VERIFIED / approval NO
ENGINE LABEL:
OBSERVED FINAL LABEL:
HUMAN↔ENGINE:
ENGINE↔OBSERVED:
HUMAN↔OBSERVED:
TARGET: salamat-projects-dashboard
MPE SOURCE SHA:
STALE MIRROR PRS:
FILES CHANGED:
DEPLOYMENT: NO
WRITE-BACK: NO
VALIDATION:
RESULT: PASS / REWORK / BLOCKED / HUMAN_REQUIRED / NO_CHANGE
NEXT ACTION:
```

Open bounded PRs only where changes are actually required.
Do not merge automatically.
