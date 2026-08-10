# Murat AI Stack v2 — Implementation Plan

Дата: 2026-08-10  
Статус: plan only; no architectural migration authorized

## Principles

1. Preserve MASTER, Codex, Codex Router, Agent Plugins and existing projects.
2. Build only against measured problems.
3. Use one agent when one agent is sufficient.
4. Deterministic verification precedes model judgment.
5. Temporary state cannot become permanent authority automatically.
6. Every stage is independently reversible.
7. Any deep change requires explicit user approval.

## Stage 0 — Research Complete

Status: complete.

Outputs:

- 14 specialized research reports;
- current-state audit;
- official Prime Agent and Prime Multi-Agent code analysis;
- integration comparison A–D;
- independent skeptic review;
- decision and this implementation plan.

Exit criteria:

- facts separated from inference;
- conflicts recorded;
- safe/deep changes separated;
- no runtime, Router, credentials, MASTER or production changes made.

## Stage 1 — Minimal Workflow PoC

Goal: validate orchestration discipline without a workflow engine.

Deliverables:

1. `Murat Project Engineer v1.0` plugin skeleton and selected skills.
2. Three risk-tier runbooks:
   - `fast`;
   - `verified`;
   - `deep-change`.
3. `SoftwareFeatureWorkflow` runbook.
4. Project gate registry as a simple reviewed table/config.
5. Compact `RUN_REPORT.md` or `run.json` template.
6. Baseline comparison protocol.

PoC flow:

```text
Task -> Architect -> Coder -> Tests/Build/Lint -> optional Judge
     -> PASS | REWORK | BLOCKED -> Run report
```

Constraints:

- isolated non-production repository/worktree;
- current Router untouched;
- MASTER untouched;
- no Prime installation;
- no persistent agents;
- no generic YAML DSL;
- one bounded rework cycle unless explicitly approved;
- no paid mass testing.

Metrics collected for 20 representative runs:

- risk tier;
- number of roles/agents;
- mandatory gate misses;
- defects before/after review;
- interruption recovery time;
- elapsed time and token overhead;
- human interventions;
- Judge findings and false positives;
- fan-out/fan-in frequency.

Acceptance:

- runbook is repeatable;
- mandatory checks are evidenced;
- no regression in current projects;
- overhead is understood;
- rollback works by disabling the runbook.

## Stage 2 — Solver / Judge

Goal: add independent verification only where it improves outcomes.

Implementation order:

1. Deterministic checks for each selected project.
2. Evidence bundle format: task, artifact, checks, unresolved risks.
3. Independent reviewer for semantic/high-impact tasks.
4. Verdicts: `PASS`, `REWORK`, `INCONCLUSIVE`, `HUMAN_REQUIRED`.
5. Rework budget and exit conditions.

Domain priorities:

- Engineering: tests/build/lint first.
- MebelDocs: totals, numbering, accounting logic and export fixtures.
- MebelLegal: source/citation validation plus human legal gate.
- Configurator: geometry and module constraints before visual/semantic review.

Kill or narrow LLM Judge if deterministic gates catch over 80% of defects, false-positive/INCONCLUSIVE exceeds 10%, or review adds over 25% cost/latency without material defect reduction.

## Stage 3 — Minimal Agent Trace

Goal: improve auditability without building an observability platform.

Start with one compact report per run containing:

- IDs/timestamps;
- risk tier and roles;
- model routes;
- tools/commands and outcomes;
- artifacts/changed files;
- verification and approvals;
- usage/cost summary if available;
- errors and unresolved risks.

Do not store private chain-of-thought.

Expansion gate for JSONL + SQLite:

- at least two real incidents cannot be diagnosed from report, Git and Codex transcript;
- or replay/resume is required repeatedly;
- or an audit/compliance requirement exists.

Only then evaluate append-only JSONL, content-addressed artifacts and rebuildable SQLite index.

## Stage 4 — Router Integration

Default action: no Router code change.

Use manually maintained route profiles above Router:

- `default`;
- `cheap-research`;
- `coding`;
- `strong-review`.

Coordinator resolves the role/task policy to an explicit model slug. Router continues provider/model mapping, protocol translation, credential isolation, compaction and usage handling.

Do not implement adaptive routing until there is a task-specific eval corpus and stable cost/quality/latency telemetry. Any change to Router authority is `DEEP_CHANGE_REQUIRES_USER_APPROVAL`.

## Stage 5 — Persistent Agents

Default action: do not create persistent runtime agents.

First use:

- project source-of-truth files;
- `STATUS.md`/handoff;
- versioned plugin/skill;
- temporary agent reconstructed from reviewed context.

Persistence RFC trigger:

- at least three repeated expensive context rebuilds;
- stable state ownership;
- measurable acceptance-rate or time improvement expected;
- TTL, cleanup, stale detection, migration and rollback owner identified.

If approved, start with one project-scoped case steward. Global specialists remain exceptional and require approval.

## Stage 6 — Controlled Continual Harness

Default mechanism: normal Git proposal/review.

Allowed flow:

```text
Observed pattern
  -> evidence
  -> proposed patch / LESSONS_CANDIDATE
  -> tests
  -> human or maintainer review
  -> merge/reject
  -> version/revert available
```

No autonomous Memory/Prompt/Agent CRUD service. Level 5 MASTER/core changes always pass `deep-change-gate` and explicit approval.

Reconsider a formal continual harness only after at least ten recurring improvement proposals demonstrate that ordinary Git review is the bottleneck.

## Stage 7 — Prime Agent Integration Only If Justified

Prime is not on the default implementation path.

Trigger an RFC only if the current Codex path fails at least three times for a reason directly tied to:

- detached long-running sessions;
- persistent kernel state;
- recursive programmatic subagents;
- crash recovery across long autonomous work;
- RLM workflow not reasonably reproducible in Codex.

RFC must include:

- isolated sandbox boundary;
- allowlisted tools and filesystem scope;
- secret isolation;
- cost, depth, child and wall-time caps;
- Trace adapter;
- external-effect idempotency;
- comparative benchmark against Codex;
- complete uninstall/rollback.

Prime main-path or central runtime integration is `DEEP_CHANGE_REQUIRES_USER_APPROVAL`.

## Conditional Stage — Workflow / Env Lite

This stage is evidence-gated and may occur after Stage 1–3.

Trigger only when:

- five or more workflows repeat with stable structure;
- or three or more material gate/recovery failures occur;
- or fan-out/fan-in is regularly required;
- and runbooks cannot solve the issue without unacceptable overhead.

Minimal scope:

- versioned definition;
- typed step inputs/outputs;
- dependencies and bounded parallelism;
- verification and human gates;
- retry/rework limits;
- explicit terminal states;
- compact run state.

Explicitly exclude expression languages, general scheduler, daemon, arbitrary Python and automatic self-modification from v1.

## User Simulation Track

1. Establish 10–20 golden deterministic fixtures per selected workflow.
2. Stabilize domain oracle.
3. Add read-only multi-turn scenarios only for observed conversational defect classes.
4. Use deterministic-first scoring and semantic Judge for residual criteria.
5. Add mutation tests to verify that the evaluator catches planted defects.

Do not treat simulated users as ground truth or persistent agents.

## Multi-Solver Escalation Rule

- `SIMPLE`: one agent.
- `STANDARD`: one Solver + deterministic checks.
- `IMPORTANT`: one Solver + independent Judge.
- `COMPLEX`: proposer + two diverse Solvers + Judge.
- `HIGH-RISK`: multiple checks/agents + human gate.

Use three solvers only when expected failure cost materially exceeds roughly three times the inference/review cost, or the user explicitly requests independent alternatives.

## Rollback by Stage

- Stage 1: disable runbook; retain inert reports.
- Stage 2: remove optional Judge; deterministic checks remain useful.
- Stage 3: stop emitting reports/index; no runtime state dependency.
- Stage 4: revert profile instructions; Router unchanged.
- Stage 5: expire project lease, export reviewed state to project files, recreate temporary agent.
- Stage 6: Git revert skill/policy patches.
- Stage 7: stop isolated Prime runtime, revoke its capability access, archive/export non-secret artifacts, remove adapter.

## Approval Boundaries

No approval is implied by this plan. Explicit user approval is required before:

- changing MASTER/core rules;
- changing Router authority/security/credentials;
- adding a central runtime/daemon;
- installing Prime into the main path;
- creating persistent production/global agents;
- enabling autonomous skill/memory promotion;
- expanding permissions or schedules;
- production migrations.

Marker: `DEEP_CHANGE_REQUIRES_USER_APPROVAL`.

## Recommended Next Development Task

Design `Murat Project Engineer v1.0` and the Stage 1 `SoftwareFeatureWorkflow` runbook in an isolated project, including risk tiers, deterministic gate registry and compact run report. Do not yet build Workflow DSL, persistent agents, Prime integration or Router v2.

