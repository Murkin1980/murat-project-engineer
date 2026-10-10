# EXP-12 P-005 — Murat House MPE Laboratory editorial refinement

Status: OWNER-AUTHORIZED PROSPECTIVE CASE  
Parent: `docs/experiments/EXP-12_CLEARS_TRIAGE.md`  
Target: `Murkin1980/Murat-house` PR #27  
Pre-registration: `evidence/exp-12/prospective/P-005_PRE_REGISTRATION.json`

## Objective

Use the existing real Murat House editorial task as prospective case P-005.

The human label is already frozen in the pre-registration **before** engine execution.

Do not change that label after seeing the engine output.

## Sequence

1. Sync `Murkin1980/murat-project-engineer` main.
2. Read EXP-12 and P-005 pre-registration.
3. Run the deterministic triage engine against exactly the frozen P-005 triage input and record the engine output.
4. Do not rewrite the human label.
5. Then work in `Murkin1980/Murat-house` on the existing PR #27 only.
6. Read Murat House `AGENTS.md`, publication/content rules, and PR #27.
7. Refine only the existing MPE Laboratory editorial package:
   - series structure;
   - cross-references;
   - editorial/style consistency;
   - evidence links already available;
   - unresolved editorial questions.
8. Keep everything private/draft/non-public.
9. Run the repository's required validation.
10. Record the observed final classification after the task is complete.
11. Return to MPE and create P-005 execution/evaluation evidence without modifying the pre-registration.

## Hard boundaries

Do not:
- publish anything;
- change visibility to public;
- add routes/schemas/dependencies/runtime services;
- deploy;
- create a new repository;
- change canonical MPE experiment evidence;
- touch unrelated Murat House content.

If completing PR #27 would require any of those, stop and classify the task according to the observed requirement instead of crossing the boundary.

## Evidence

In MPE create:
- `evidence/exp-12/prospective/P-005_EXECUTION.json`
- `evidence/exp-12/prospective/P-005_EVALUATION.json`

In Murat House, keep the task bounded to PR #27 and add only the smallest evidence/review note required by local governance.

## Terminal report

```text
CASE: EXP12-P-005
HUMAN LABEL: FAST / approval NO
ENGINE LABEL:
OBSERVED FINAL LABEL:
HUMAN↔ENGINE:
ENGINE↔OBSERVED:
HUMAN↔OBSERVED:
TARGET PR: Murat-house #27
PUBLICATION: NO
PRODUCTION CHANGES: NONE
VALIDATION:
RESULT: PASS / REWORK / BLOCKED / HUMAN_REQUIRED
NEXT ACTION:
```

Do not merge Murat House PR #27 automatically.
Do not merge the MPE evidence PR automatically.
