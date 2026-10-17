# EXP-CODE-2026-02 — Cloudflare persistent browser

Status: PLANNED / NOT EXECUTED
Primary series decision: EXPERIMENT
Individual New Idea Filter disposition: EXPERIMENT
Repository: Murkin1980/murat-project-engineer
Owner gate: no implementation, production changes, new repositories, paid services or deep changes without separate approval.

## Scope and checkpoints

### CP-01
Objective: Verify current Cloudflare Agents SDK browserTool availability/version, permissions, billing, data residency and browser isolation; compare existing Browser Evidence/TinyFish.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-02
Objective: Design one synthetic, credential-free multi-step web scenario; define session lifetime, secret redaction, teardown and evidence schema.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-03
Objective: Run same scenario using current approach and browserTool only if safe/available; capture success, reauth count, duration, costs and screenshots.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-04
Objective: Document comparison, security/deep-change risks and explicit approval gate for any authenticated session or infrastructure change.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

## Common gates
Read AGENTS.md, docs/governance/SCOPE-CHANGE-CONTROL.md, docs/NEW_IDEA_FILTER_POLICY.md, docs/GLOBAL_MPE_ENFORCEMENT.md and relevant project source-of-truth before any work. Check current overlapping experiments/PRs first, including EXP-29 Arena bootstrap. Use existing Execution Report and Browser Evidence formats. No secrets, no production writes, no automatic merge/deploy. If provider feature is unavailable, return BLOCKED rather than fabricate evidence. Compare baseline vs trial with actual measured data. Final outcome: ADOPT_WITH_CHANGES, HOLD or REJECT with explicit human approval for any follow-up.
