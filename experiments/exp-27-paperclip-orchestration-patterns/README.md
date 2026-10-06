# EXP-27 — Paperclip orchestration patterns

Status: PLANNED  
Decision: REUSE_COMPONENT  
Owner: Murat Project Engineer  
Repository: `Murkin1980/murat-project-engineer`

## Purpose

Evaluate Paperclip strictly as a donor/reference for orchestration and control-plane patterns that may strengthen existing MPE and `murat-ai-orchestrator` components.

Do not adopt Paperclip as a product, deploy a persistent Paperclip service, replace MPE governance, or move repository/project source-of-truth into Paperclip.

Primary question:

> Which Paperclip orchestration patterns measurably improve one bounded MPE engineering workflow without introducing a parallel control plane?

## Primary disposition

**REUSE_COMPONENT**

Paperclip is a donor. Any useful mechanism must map into an existing Murat project/component before adoption.

## Sources to audit

- `https://github.com/paperclipai/paperclip`
- Habr overview previously captured for this experiment

Arena must verify current upstream commit/tag and license during CP-01 rather than rely on this file for freshness.

## Existing-system priority

Primary landing target for reusable mechanics:

1. `murat-ai-orchestrator`
2. MPE task/run/evidence contracts
3. read-only surfacing in the dashboard where useful

Do not create a separate Paperclip runtime or source of truth.

## Candidate patterns

Prioritize these five:

1. **Goal context / ancestry**
   - project → goal → experiment/checkpoint → task
   - executor receives compact parent context
   - parent goal remains visible through completion

2. **Atomic task checkout / lease**
   - one active owner per task
   - duplicate executor receives explicit already-owned / lease-conflict result
   - lease expiry/recovery behavior must be bounded and inspectable

3. **Persistent task/run evidence**
   - plan, state, blocker, outputs, terminal result
   - resumable by a fresh executor without reconstructing full chat history
   - align with existing MPE graceful-handoff contract

4. **Budget / runaway guard**
   - bounded retries
   - bounded tool calls
   - bounded wall time where measurable
   - optional token/cost boundary only if observable without new infrastructure
   - hard limit must stop/block rather than silently continue

5. **Approval / governance gate**
   - preserve MPE READY/WARNING/BLOCKED semantics
   - merge/deploy/deep-change stays under existing MPE authority
   - no Paperclip-level override

Secondary/reference-only:
- heartbeat/routine concepts
- agent role boundaries
- audit/activity events
- runtime adapter ideas

## Non-goals

Do NOT:
- deploy Paperclip;
- create a new repository;
- create a permanent control-plane service;
- add a new database;
- add a queue/scheduler/daemon solely for this experiment;
- replace the Router;
- replace MPE governance;
- move canonical project state out of Git/repositories;
- enable unbounded autonomous execution;
- create 24/7 agent fleets;
- add recurring paid infrastructure;
- start production integration.

## Mandatory startup

Read in this order:
1. `AGENTS.md`
2. `docs/governance/SCOPE-CHANGE-CONTROL.md`
3. mandatory New Idea / Global / Workspace governance
4. this file
5. `ARENA_TASK.md`

Then inspect only existing task/run/evidence/orchestration components required for the bounded proof.

## CP-01 — Upstream audit + component map

Audit current Paperclip:
- license;
- pinned commit/tag;
- task ownership/locking model;
- goal/context model;
- run history/evidence;
- budget/runaway controls;
- approvals/governance;
- heartbeat/routine mechanics;
- agent/runtime adapter boundaries.

For each candidate record:

```text
Paperclip pattern
→ problem solved
→ existing MPE/orchestrator equivalent
→ overlap
→ incremental value
→ required dependency/runtime
→ adoption risk
→ KEEP / BORROW / ADAPT / REJECT
```

PASS only if at least one pattern offers incremental value without requiring a parallel control plane.

## CP-02 — Goal context

Use one existing bounded MPE engineering workflow/task.

Provide a compact ancestry chain:

```text
project
→ parent goal
→ experiment/checkpoint
→ task
```

Verify:
- executor can state the parent goal;
- task completion preserves the goal;
- no extra canonical source is created.

Measure context overhead and rediscovery steps.

## CP-03 — Atomic task lease

Create the smallest deterministic local proof that one task cannot be owned by two executors simultaneously.

Required behaviors:
- first checkout succeeds;
- second checkout fails explicitly;
- release/terminal state is visible;
- stale/recovery behavior, if tested, is bounded and deterministic;
- no persistent daemon required.

Prefer file-backed or existing MPE/orchestrator primitives.

## CP-04 — Persistent evidence + resume

Persist enough state for a fresh executor to resume without original chat context.

Minimum evidence:
- task identity;
- parent goal;
- current state;
- completed steps;
- blocker;
- outputs/evidence refs;
- next action;
- terminal/lease status.

Test a fresh-process or equivalent restart/resume.

PASS only if resume succeeds without rediscovery of already captured facts.

## CP-05 — Budget/runaway + approval gate

Demonstrate at least one hard execution boundary:
- retry limit;
- tool-call limit;
- wall-time limit;
- or another deterministic bounded resource.

Crossing it must produce explicit STOP/BLOCKED behavior.

Then demonstrate an integration-sensitive boundary returning existing MPE READY/WARNING/BLOCKED and requiring the existing approval path.

Do not perform merge/deploy/deep-change as part of the proof.

## Required measurements

Where applicable:
- duplicate task executions;
- lease conflicts;
- rediscovery steps;
- resume success;
- evidence completeness;
- retries/tool calls/wall time;
- human approval points;
- incremental implementation complexity;
- files/dependencies/services added;
- compatibility with current READY/WARNING/BLOCKED governance.

Do not claim a VRU unless a real or production-like user workflow receives verified relief.

## Acceptance

### PASS
At least one Paperclip-inspired mechanism improves bounded MPE orchestration behavior, with deterministic evidence, no parallel control plane, and no governance/source-of-truth change.

### PARTIAL
Useful signal exists, but one important behavior remains unverified or the executor environment blocks direct validation.

### FAIL
No meaningful incremental value, excessive complexity, duplication of existing mechanisms, or dependence on persistent parallel infrastructure.

## Final adoption result

Return:
- ADOPT_WITH_CHANGES
- DO_NOT_ADOPT

Also classify each tested pattern as:
- ADOPT_IN_ORCHESTRATOR
- ADOPT_IN_MPE
- REUSE_PATTERN_ONLY
- REJECT

Do not return “install Paperclip”.

## Evidence

Keep experiment artifacts under:

`experiments/exp-27-paperclip-orchestration-patterns/`

Minimum:
- `UPSTREAM_AUDIT.md`
- `COMPONENT_MAP.md`
- bounded proof harness/fixtures if created
- `RESULTS.md`

## Stop conditions

Stop and report before:
- new repo;
- persistent Paperclip service;
- new DB/queue/daemon;
- Router authority change;
- governance replacement;
- Git/source-of-truth change;
- autonomous merge/deploy;
- recurring paid infrastructure;
- production integration.

## Completion boundary

Stop after CP-01…CP-05 and the component-level recommendation.

No productionization is authorized by this experiment.
