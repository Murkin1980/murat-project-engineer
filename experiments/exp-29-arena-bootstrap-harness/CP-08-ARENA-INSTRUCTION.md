# EXP-29 / CP-08 — Arena instruction: Bootstrap State Consistency Recovery

Status: OWNER-AUTHORIZED TASK INSTRUCTION (documentation only). Implementation and merge remain separate actions.
Repository: `Murkin1980/murat-project-engineer`
Primary New Idea Filter decision for this corrective checkpoint: `EXTEND_EXISTING`.
Preserve original EXP-29 disposition: `REUSE_COMPONENT`.
Deep-change: not authorized. Delivery: session branch → PR → owner review; no merge or deployment.

## Goal
Repair the EXP-29 Bootstrap state-drift root cause in the existing harness: freshness by file digest must not be mistaken for correct current task, checkpoint, disposition, or authorized resume action. Do not add a parallel memory service, database, agent, or infrastructure.

## Phase 0 — read and reproduce
1. Read `docs/governance/SCOPE-CHANGE-CONTROL.md` **first**, then `AGENTS.md`, `docs/NEW_IDEA_FILTER_POLICY.md` if relevant, `experiments/exp-29-arena-bootstrap-harness/README.md`, `ARENA_TASK.md`, `RESULTS.md`, `harness/bootstrap_builder.py`, `tests/test_exp29_bootstrap.py`, experiment registry, and the existing CP-06/CP-07 evidence.
2. Compare current `main` and session branch, inspect merged PRs #70/#74 before claiming status. Do not treat the derived packet as source of truth.
3. Record baseline: `python3 -m unittest tests.test_exp29_bootstrap` and the documented full test suite. Prior preflight reported 34 tests/2 failures, 432 tests/27 failures/1 skipped; these numbers must be reproduced or explained, not assumed.
4. Verify actual branch write by authorized git workflow, not merely HTTP receive-pack availability.

## Phase 1 — reconcile canonical state
- Confirm actual CP-06/CP-07 state from Git evidence and reconcile experiment registry/README/results only as warranted.
- Preserve historical checkpoint evidence and the EXP-29 `REUSE_COMPONENT` decision; no retroactive invented successes.
- Replace active CP-05-era `status`/`nearest_action`/resume instructions with evidence-supported state. Explicitly distinguish current task CP-08 from historical checkpoints.
- Resolve conflicting canonical sources according to governance, or STOP for owner decision.

## Phase 2 — minimal builder repair
- Reuse the existing deterministic builder and provenance, with minimal change.
- Ensure EXP-29 disposition survives extraction, and missing/ambiguous disposition does not silently disappear.
- Ensure `resume.next_authorized_action` is complete (not sentence-truncated) and current; active task and checkpoint/status fields agree.
- Fail closed for missing, contradictory, unsupported or obsolete authorization-critical state. Avoid heuristic fabrication.
- Regenerate committed `ARENA_CONTEXT.json` and `ARENA_CONTEXT.md` from canonical Git as derived artifacts; verify FRESH and rebuild-identical.

## Phase 3 — verification
Add focused regression coverage for disposition preservation, status/checkpoint consistency, full resume action, contradictory/stale active instructions, deterministic provenance, and fail-closed negative controls. Run focused tests and the documented full suite; report baseline versus final. No new regressions. Classify unrelated failures but do not expand scope to fix them.

## Phase 4 — delivery and boundaries
- Commit only CP-08 files on the Arena platform-authorized `arena/…` session branch; push and open a PR against `main`.
- Do not push directly to `main`, bypass branch binding, change permissions/rulesets/governance, merge/close PR, or deploy.
- If push fails, preserve evidence and report exact error. If a fundamental architectural or source-of-truth change is required, STOP and request explicit deep-change authorization.
- Do not confuse this documentation-only PR branch (`docs/exp29-cp08-arena-instruction`) with Arena's writable session branch.

## Acceptance / final report
PASS only if: EXP-29 source state is evidence-aligned; `REUSE_COMPONENT` preserved; packet FRESH/rebuild-identical; resume complete/current/authorized; focused tests pass; no newly failing full-suite tests; changes delivered via session branch PR. Otherwise PARTIAL/BLOCKED.

Report: RESULT; branch, SHA, PR; files and root cause; freshness + semantic consistency; focused and full tests before/after; remaining baseline failures; governance/deep-change; next authorized action. STOP after PR delivery, await owner review.
