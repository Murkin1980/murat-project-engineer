# EXP-CODE-2026-01 — Poteto Mode / agent verification

Status: PLANNED / NOT EXECUTED
Primary series decision: EXPERIMENT
Individual New Idea Filter disposition: EXTEND_EXISTING
Repository: Murkin1980/murat-project-engineer
Owner gate: no implementation, production changes, new repositories, paid services or deep changes without separate approval.

## Scope and checkpoints

### CP-01
Objective: Inventory existing AGENTS, Execution Report, Browser Evidence, EXP-29 bootstrap and identify missing verification behavior; baseline 5 historical tasks.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-02
Objective: Design minimal verify-before-claim checklist with reproduction, tests, runtime/browser evidence, negative cases and explicit UNVERIFIED status; no new agent.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-03
Objective: Run 5 bounded retrospective cases with unchanged baseline vs checklist; record false PASS, human interventions, token/time costs.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

### CP-04
Objective: Review measured results and decide ADOPT_WITH_CHANGES/HOLD/REJECT; propose instruction-only minimal diff, no automatic rollout.
Deliverables: source/version verification, minimal reproducible evidence, risks, metrics, exact changed files (if any), cost, verdict READY/WARNING/BLOCKED and next action.
Acceptance: factual claims linked to primary source; hypothesis marked separately; no unapproved scope expansion.
STOP: checkpoint boundary; await explicit owner authorization for the next checkpoint.

## Common gates
Read AGENTS.md, docs/governance/SCOPE-CHANGE-CONTROL.md, docs/NEW_IDEA_FILTER_POLICY.md, docs/GLOBAL_MPE_ENFORCEMENT.md and relevant project source-of-truth before any work. Check current overlapping experiments/PRs first, including EXP-29 Arena bootstrap. Use existing Execution Report and Browser Evidence formats. No secrets, no production writes, no automatic merge/deploy. If provider feature is unavailable, return BLOCKED rather than fabricate evidence. Compare baseline vs trial with actual measured data. Final outcome: ADOPT_WITH_CHANGES, HOLD or REJECT with explicit human approval for any follow-up.
