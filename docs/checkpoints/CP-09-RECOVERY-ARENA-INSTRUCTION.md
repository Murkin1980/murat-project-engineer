# CP-09 — Recovery execution instruction (Arena)

**Repository:** `Murkin1980/murat-project-engineer`
**Decision:** `EXTEND_EXISTING`
**Status:** OWNER HANDOFF / implementation authorized only within CP-09; no merge authority.
**Baseline:** `94eeed98962e5de7f54498390782cca72d67c774`; evidence merged via PR #112, merge commit `3969b88ff2ad6220fcb1a8c5b3d8d8854e230bec`.
**Scope:** recovery of existing 27 failing tests, EXP-23 lifecycle/disposition conflict, registry/dashboard/Reladraw generated views. No feature delivery, new infra, repository, deployment or architectural redesign.

## 0. Governance first

Read, in order:
1. `docs/governance/SCOPE-CHANGE-CONTROL.md`
2. `AGENTS.md`
3. `docs/NEW_IDEA_FILTER_POLICY.md`, `docs/GLOBAL_MPE_ENFORCEMENT.md`, `docs/OPINIONATED_WORKSPACE_POLICY.md` where relevant
4. `evidence/cp09/RESULTS.md` and `evidence/cp09/baseline-unittest-94eeed9.log`
5. `experiments/exp-29-arena-bootstrap-harness/README.md`, `RESULTS.md`, builder and tests
6. The precise registry contract, dashboard/Reladraw generators, tests, and EXP-23 canonical artifacts affected.

Use Arena's active session branch if session policy prevents naming a new one; explicitly report that. Start from current `origin/main`, including PR #112 evidence, not the earlier baseline SHA. Search for overlapping active PRs before making edits.

## 1. Bootstrap safety

This is a context-heavy resumptive task. Use the existing EXP-29 `harness/bootstrap_builder.py` to generate a task-specific derived packet using canonical current Git sources. Read builder CLI/help and follow the documented invocation; do not guess arguments. Verify `FRESH` and matching CP-09 identity and base/current Git provenance BEFORE consuming packet. A `STALE` or `REJECTED` packet must not be treated as authority. If a CP-09 packet cannot be generated under existing schema, record this blocker and proceed directly from canonical Git only if doing so does not violate its validation/governance contract; do not change bootstrap semantics to make the task start.

## 2. Fresh baseline

Run exact documented `python -m unittest discover -s tests -v` on clean current main and verify whether 440/412/27/0/1 remains valid; save any new raw log separately with commit SHA. Run `python -m unittest tests.test_exp29_bootstrap -v` and `python scripts/validate_package.py .`. Before counting status or changing files, establish reproducible failures. Distinguish baseline test counts from current result.

## 3. Root-cause repair, ordered

### 3a. Registry status contract
Locate authoritative status definitions and meaning of `RETIRED` and `PARTIAL`. Determine whether data or test expectations are wrong using normative Git evidence. Make only the smallest supported fix and preserve valid status distinctions. No blanket expansion of enums to satisfy tests.

### 3b. EXP-23 disposition
Canonical final result is `PASS / REUSE_COMPONENT` per registry, FINDINGS and final README conclusion; initial filter route was `EXPERIMENT`. Treat them as potentially distinct lifecycle concepts. Locate the existing authoritative semantic contract and validator. If it already distinguishes initial and final decisions, make minimal representation/parser correction with positive + negative regression tests; preserve fail-closed behavior for true conflicting *final* dispositions. If semantics require changing the public/bootstrap contract or source-of-truth hierarchy, STOP just this portion with `BLOCKED_DEEP_CHANGE` and request explicit owner approval; never silently mutate initial history or canonical final disposition.

### 3c. Dashboard registry views
Locate source data, renderer/generation command, expected coverage, and generated-view acceptance rules. Determine whether missing/truncated status assets and next-step text stem from stale generated views or defective renderer. Fix actual root cause. Regenerate only established derived artifacts with inspectable diff. Preserve mobile completeness, names, statuses, next actions; don't weaken tests or replace them with shallow existence checks.

### 3d. Reladraw
Identify canonical producer and deterministic output rules (dates, stable ordering and source digests). Compare current output to committed diagrams/mobile views. Refresh only those artifacts whose contract and source justify refresh. Avoid wholesale churn and test snapshot updating without evidence.

These sections may be handled in one bounded CP-09 branch, but separate commits by root cause where practical. If one section is blocked, continue safe independent sections and clearly report it.

## 4. Gates and boundaries

No new architecture, dependencies, data migrations, infra, new repo, expansion of EXP-29 bootstrap public contract, or new feature. Never delete tests, hide failing cases, suppress verification, or rewrite governance to force green. Evidence must support changes. If deep-change is required, stop that portion and ask owner while continuing independently safe fixes.

Run targeted tests after each category, then all 440+ current full-suite tests and the 42 EXP-29 regression tests, package validation, and `git diff --check`. Report exact totals, exit statuses, filenames, causes, and meaningful change size. If baseline total evolves legitimately, explain it. Verify no secrets, sandbox paths, or unnecessary generated churn in diff.

## 5. Delivery

Commit implementation only when coherent; push current permitted Arena branch and open a scoped PR into `main` with:
- before/after failures and commands;
- traceable root-cause-to-change matrix;
- EXP-23 lifecycle semantics and evidence (or BLOCKED reason);
- list of generated artifacts and exact producer commands;
- security/scope/deep-change statement;
- regression results and remaining blockers.

**DO NOT MERGE**, deploy, or claim PASS unless full suite has 0 failures and 0 errors, EXP-29 tests pass, EXP-23 is resolved on documented semantics, and all acceptance requirements are verified. If blocked, produce evidence-backed PARTIAL/BLOCKED PR only if it does not weaken main and mark it HOLD.

Final handoff: RESULT, STATE, EVIDENCE, CHANGES, BLOCKER, NEXT ACTION, HANDOFF, branch, HEAD SHA and PR URL. No unsupported PASS claims.
