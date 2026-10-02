# EXP-21 — Paperclip Agent Organization / Control Plane

Status: PLANNED

## Decision

Primary MPE disposition: EXPERIMENT.

Paperclip should be evaluated as an external reference and bounded experimental control-plane candidate, not adopted wholesale and not given authority over MPE governance.

## Source

- Paperclip: https://github.com/paperclipai/paperclip
- Habr overview: https://habr.com/ru/articles/1012490/

Paperclip describes itself as an open-source orchestration/control plane for teams of AI agents. Its current repository includes goal alignment, org charts, task assignment, heartbeats, budgets/cost controls, governance/approvals, persistent work context, routines, plugins, and multiple agent runtimes. It supports agents such as Codex, Claude Code, OpenClaw, Cursor, Gemini CLI and others.

## Why this matters

The interesting layer is not another coding agent. It is the management/control plane around multiple existing agents:

mission → goals → projects → tasks → agent assignment → execution → review → cost/governance → evidence.

This overlaps strongly with MPE and with the Dify/OpenHands component-extraction experiment, so duplication must be tested explicitly.

## Candidate capabilities to inspect

- goal ancestry / goal-aware task context
- atomic task checkout and execution locks
- persistent task/run history
- heartbeat-based execution
- budget thresholds and hard stops
- human approval/review gates
- agent roles, permissions and responsibility boundaries
- workspace/runtime resolution
- routines/schedules
- accountable connection permissions
- plugin/adapter model
- portable agent/team configuration
- durable activity/audit events

## Existing-system mapping

Compare against:

- Murat Project Engineer governance and New Idea Filter
- existing MPE experiment registry and evidence model
- existing agent/orchestration components
- OpenHands execution-layer candidates
- Dify workflow-layer candidates
- existing AI gateway and project repositories
- existing automation/scheduling capabilities

Classify each candidate:

- KEEP — already sufficiently solved internally.
- BORROW — useful architectural pattern.
- ADAPT — reproduce the capability inside an existing system.
- EXPERIMENT — requires a bounded proof.
- IGNORE — no demonstrated current need.

## Critical invariant

Paperclip must not become the source of truth for project decisions.

MPE remains the governance/decision layer. Repository/project artifacts remain their own source of truth. Any future execution layer must operate inside explicit task, permission, budget, and approval boundaries.

## Bounded proof

Use one existing MPE engineering workflow with a small number of agents/runs.

Measure:

- coordination overhead;
- duplicate task execution;
- context rediscovery;
- cost visibility;
- ability to pause/stop runaway work;
- human review burden;
- evidence/resumability quality;
- reuse value versus existing MPE mechanisms.

Do not create a permanent autonomous company or 24/7 agent fleet for the experiment.

## Acceptance criteria

1. No new repository.
2. No production architecture change.
3. No replacement of MPE governance.
4. No unbounded autonomous execution.
5. Budget/cost hard-stop behavior is explicitly tested if available.
6. Task locking/concurrency behavior is explicitly tested if available.
7. Human approval and rollback boundaries are preserved.
8. Useful capabilities are mapped to existing components before any new implementation is proposed.
9. Source-code reuse is considered only after license/dependency review.

## Next action

Perform a comparative audit of Paperclip against MPE, OpenHands, Dify, and the current agent/automation stack. Select the smallest non-duplicative capability for a bounded proof.
