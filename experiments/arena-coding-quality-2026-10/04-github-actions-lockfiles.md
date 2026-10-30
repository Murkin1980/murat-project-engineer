# EXP-CODE-2026-04 — GitHub Actions lockfiles

Status: PLANNED / NOT EXECUTED
Primary series decision: EXPERIMENT
Individual New Idea Filter disposition: EXTEND_EXISTING
Repository: Murkin1980/murat-project-engineer
Owner gate: no implementation, production changes, new repositories, paid services or deep changes without separate approval.

## Scope and checkpoints

### CP-01
Objective: Inventory Actions usage in two representative repositories, existing SHA pinning, Dependabot and permissions; verify gh actions-lock preview.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-02
Objective: Prototype lockfile on isolated branch with no secrets, compare transitive action resolution and workflow compatibility.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-03
Objective: Test reproducibility and update behavior in CI or dry-run; capture failures, maintenance overhead and rollback.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-04
Objective: Document suitability and version constraints; request approval before changing production CI policies.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

## Common gates
Read AGENTS.md, docs/governance/SCOPE-CHANGE-CONTROL.md, docs/NEW_IDEA_FILTER_POLICY.md, docs/GLOBAL_MPE_ENFORCEMENT.md and relevant project source-of-truth before any work. Check current overlapping experiments/PRs first, including EXP-29 Arena bootstrap. Use existing Execution Report and Browser Evidence formats. No secrets, no production writes, no automatic merge/deploy. If provider feature is unavailable, return BLOCKED rather than fabricate evidence. Compare baseline vs trial with actual measured data. Final outcome: ADOPT_WITH_CHANGES, HOLD or REJECT with explicit human approval for any follow-up.
