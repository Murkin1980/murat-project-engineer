# EXP-CODE-2026-03 — Cloudflare MCP Issues / Events

Status: PLANNED / NOT EXECUTED
Primary series decision: EXPERIMENT
Individual New Idea Filter disposition: REUSE_COMPONENT
Repository: Murkin1980/murat-project-engineer
Owner gate: no implementation, production changes, new repositories, paid services or deep changes without separate approval.

## Scope and checkpoints

### CP-01
Objective: Inventory current Workers Issues/Logs/Traces and Execution Report event sources; verify MCP Events feature and access.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-02
Objective: Specify read-only mapping issue ID, Worker, timestamp, fingerprint, trace, severity, evidence URI to existing report; no second store.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-03
Objective: Test with synthetic/staging issue and duplicate/retry events; check idempotency, redaction, event loss, cost and time-to-diagnosis.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-04
Objective: Evaluate evidence and draft optional integration checkpoint only if current pipeline has a measured gap; no autonomous production fix.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

## Common gates
Read AGENTS.md, docs/governance/SCOPE-CHANGE-CONTROL.md, docs/NEW_IDEA_FILTER_POLICY.md, docs/GLOBAL_MPE_ENFORCEMENT.md and relevant project source-of-truth before any work. Check current overlapping experiments/PRs first, including EXP-29 Arena bootstrap. Use existing Execution Report and Browser Evidence formats. No secrets, no production writes, no automatic merge/deploy. If provider feature is unavailable, return BLOCKED rather than fabricate evidence. Compare baseline vs trial with actual measured data. Final outcome: ADOPT_WITH_CHANGES, HOLD or REJECT with explicit human approval for any follow-up.
