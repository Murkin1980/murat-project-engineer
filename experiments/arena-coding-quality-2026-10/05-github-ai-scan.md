# EXP-CODE-2026-05 — GitHub AI Scan

Status: PLANNED / NOT EXECUTED
Primary series decision: EXPERIMENT
Individual New Idea Filter disposition: HOLD
Repository: Murkin1980/murat-project-engineer
Owner gate: no implementation, production changes, new repositories, paid services or deep changes without separate approval.

## Scope and checkpoints

### CP-01
Objective: Check eligibility, repository plan, pricing, data/security terms and existing CodeQL/review overlap without enabling paid services.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-02
Objective: Prepare small historical PR sample with known security findings and nonissues; define precision, recall and reviewer-time baseline.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-03
Objective: If eligible at no unapproved cost, run read-only trial; otherwise record BLOCKED and cost/permission gate.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-04
Objective: Compare incremental confirmed findings, false positives and expense; recommend HOLD/ADOPT_WITH_CHANGES/REJECT.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

## Common gates
Read AGENTS.md, docs/governance/SCOPE-CHANGE-CONTROL.md, docs/NEW_IDEA_FILTER_POLICY.md, docs/GLOBAL_MPE_ENFORCEMENT.md and relevant project source-of-truth before any work. Check current overlapping experiments/PRs first, including EXP-29 Arena bootstrap. Use existing Execution Report and Browser Evidence formats. No secrets, no production writes, no automatic merge/deploy. If provider feature is unavailable, return BLOCKED rather than fabricate evidence. Compare baseline vs trial with actual measured data. Final outcome: ADOPT_WITH_CHANGES, HOLD or REJECT with explicit human approval for any follow-up.
