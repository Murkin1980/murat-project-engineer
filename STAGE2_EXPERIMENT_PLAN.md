# Murat Project Engineer — Stage 2 Experiment Plan

Date: 2026-08-11  
Updated: 2026-08-18  
Status: ACTIVE  
Purpose: validate whether Murat Project Engineer v1.0 improves real project execution enough to justify keeping or expanding the architecture.

## Decision boundary

Stage 2 is an evidence-gathering phase, not an architecture expansion.

Do **not** add a daemon, scheduler, generic workflow engine, persistent runtime agents, autonomous memory promotion, Router task orchestration, or Prime Agent runtime integration during this stage.

A move toward Option B (Pattern Hybrid) requires evidence from the experiment and a separate deep-change RFC/approval.

## Primary question

Does the v1.0 disciplined coordinator improve correctness, review quality, interruption recovery, and execution clarity at acceptable overhead compared with the simpler baseline Codex workflow?

## Experiment size

Run 20 representative tasks across real Murat AI Stack projects.

Target split:

- 6 FAST runs
- 10 VERIFIED runs
- 4 DEEP-CHANGE classification exercises or approved deep-change runs

Include at least 5 baseline runs using the prior simpler Codex approach on comparable task classes.

## Representative project mix

Use real work where practical:

1. Murat Project Engineer
2. MebelDocs KZ / mebeldocs-ai
3. MebelLegal KZ
4. Furniture Layout / Configurator
5. Furniture Production or related operational tooling
6. Furniture Sales / customer-facing workflow
7. Codex Router maintenance tasks that do not change Router authority

Do not force equal representation. Prefer actual work that would have been done anyway.

## Task classes to cover

At minimum, include examples of:

- small documentation/configuration change
- isolated bug fix
- feature implementation
- refactor with regression risk
- repository/release readiness review
- external research feeding an engineering decision
- UI or interaction change
- data/schema-sensitive change
- security/permissions-sensitive change
- interrupted task resumed from handoff/context artifacts

## Run procedure

For every Murat Project Engineer run:

1. Read source-of-truth files for the target project.
2. Classify risk as FAST, VERIFIED, or DEEP-CHANGE.
3. Select the smallest sufficient Expert or temporary Team.
4. Select the matching Playbook.
5. Record route profile/model resolution when observable.
6. Execute the task.
7. Run mandatory deterministic gates before semantic review.
8. Use an independent Reviewer/Judge only where the playbook/risk requires it.
9. Record rework and human intervention.
10. Emit one terminal state: PASS, REWORK, BLOCKED, or HUMAN_REQUIRED.
11. Complete one Experiment Record and one compact Run Report.

For baseline runs, record the same measurable fields where possible, but do not retroactively simulate Expert/Team behavior.

## Required evidence per run

Each run should preserve observable evidence, not hidden reasoning:

- task and acceptance criteria
- source-of-truth references
- risk classification
- selected playbook
- Expert/Team used
- model/route resolution if observable
- files changed
- deterministic gate results
- reviewer findings
- rework count
- human intervention
- interruption/recovery issue, if any
- escaped defect discovered after PASS, if any
- rollback information
- approximate usage/cost if observable

## Success metrics

Track these across the 20 runs:

### Quality

- deterministic gate failure rate before final PASS
- defects escaped after PASS
- reviewer findings that caused useful rework
- reviewer false positives
- acceptance criteria missed before final review

### Efficiency

- rework count
- human interventions
- obvious redundant expert/reviewer calls
- approximate token/cost overhead when observable
- whether the selected risk tier was judged excessive or insufficient afterward

### Recoverability

- can a run be resumed from source-of-truth + handoff + Run Report without reconstructing hidden context?
- did interruption cause duplicated work or contradictory decisions?

### Architecture pressure

Explicitly mark whether a run showed a real need for:

- fan-out/fan-in coordination
- durable runtime state beyond versioned files
- machine-readable workflow state
- generic workflow execution
- persistent agents

A single preference for convenience is not sufficient evidence for architecture expansion.

## Stage 2 exit criteria

After 20 runs, produce `STAGE2_EXPERIMENT_REVIEW.md` containing:

1. run matrix and task distribution
2. baseline vs coordinator comparison
3. quality findings
4. overhead findings
5. interruption/recovery findings
6. reviewer value and false-positive rate
7. repeated fan-out/fan-in evidence
8. architecture-pressure evidence
9. recommendation: KEEP A+ | ADJUST A+ | RFC OPTION B | STOP

## Option B trigger

Recommend an RFC for Option B only if repeated evidence shows that human-readable runbooks and versioned handoffs are insufficient, for example:

- gates are repeatedly skipped or inconsistently applied despite correct use
- multiple real tasks require recurring fan-out/fan-in that becomes error-prone
- interruption recovery repeatedly fails because state cannot be reconstructed
- orchestration bookkeeping becomes a material source of defects or excessive overhead

Any Option B proposal remains subject to the deep-change-gate.

## First five suggested runs

Use these as the starting queue unless real work provides better candidates:

1. Murat Project Engineer — documentation/status hygiene (FAST)
2. Furniture Configurator — small bounded UI/interaction change (VERIFIED)
3. MebelDocs KZ — isolated document-generation or validation bug (VERIFIED)
4. MebelLegal KZ — research-backed legal workflow change with deterministic checks (VERIFIED)
5. Murat Project Engineer — interrupted/resumed maintenance task to test recoverability (VERIFIED)

## Guardrails

- No architecture expansion during measurement.
- No automatic memory promotion.
- No secrets in reports or handoffs.
- No hidden chain-of-thought in artifacts.
- No permanent model binding to Expert roles.
- Router remains inference/protocol/credential gateway only.
- Project source-of-truth files override stale session notes.

## EXP-12 triage sub-experiment

Run 12 introduced a deterministic, stateless triage scorecard as an `EXPERIMENT` within Option A+. The first retrospective backtest validates mechanics only. Prospective tasks must be recorded before execution and compared with final human/observed tiers. Automatic execution, approval, adaptive scoring and Router authority remain out of scope. The living record is `docs/experiments/EXP-12_CLEARS_TRIAGE.md`.

---

# Roadmap alignment update — 2026-08-18

## MPE New Idea Filter decision

**EXTEND_EXISTING**

The recommendations in `mpe_recommendations.md` strengthen the existing MPE direction and do not justify a parallel product, repository, runtime or workflow engine. MPE remains the governance/policy layer; execution remains external and replaceable.

## Architectural position to preserve

MPE should mature toward an enforceable governance core that owns:

- task/risk classification;
- smallest-sufficient Expert/Team selection;
- typed contracts and handoffs;
- deterministic and semantic gates;
- evidence-backed completion;
- terminal states;
- controlled human escalation;
- auditability and run-level observability.

MPE should **not** own during Stage 2:

- scheduling;
- persistent runtime agents;
- generic workflow execution;
- autonomous memory services;
- credentials/protocol routing;
- a custom tracing backend;
- a custom multi-agent runtime.

This keeps the product differentiated as a governance and engineering-control layer rather than another orchestration framework.

## Updated priority for Runs 13–20

The remaining Stage 2 runs should continue to be real evidence-gathering runs, but their selection should deliberately exercise the governance capabilities that the recommendations identify as highest-value.

### RUN-13 — Goal + Run Contract

Purpose: merge the planned goal-contract experiment with the stronger machine-readable governance direction.

Validate a minimal versioned `Run`/goal contract containing at least:

- goal / acceptance criteria;
- risk tier;
- source-of-truth references;
- selected Expert/Team and playbook;
- required gates;
- terminal state;
- evidence references.

No runtime integration. The experiment succeeds only if the contract reduces ambiguity and can be deterministically validated.

### RUN-14 — Typed Handoff / Gate / Evidence / Terminal State

Formalize and test the smallest useful schemas for:

- `Handoff`;
- `GateResult`;
- `EvidenceRecord`;
- `TerminalState`.

Add explicit contract versioning and stable identifiers. Validate referential integrity between `run_id`, handoffs, gate reports, evidence and terminal state.

This absorbs the useful part of the earlier context-layer plan into a stronger typed-delivery foundation instead of creating a second context subsystem.

### RUN-15 — Validator Hardening + Negative Tests

Promote the validator from a package checker toward the enforcement boundary for MPE artifacts.

Test failure cases such as:

- missing evidence;
- broken references;
- invalid state transitions;
- incompatible contract versions;
- a green gate without required evidence;
- contradictory terminal state;
- incomplete handoff.

This becomes a P0 experiment because enforceability is more valuable than adding more orchestration behavior.

### RUN-16 — Context Provenance, Not Autonomous Memory

Continue the existing context-layer idea only as a provenance experiment:

- what context was read;
- from which source of truth;
- freshness/version identity;
- what evidence was derived from it;
- whether a resumed run can reconstruct required context.

Do not build a memory service or autonomous memory promotion. The earlier “living memory” idea remains deferred until Stage 2 proves versioned artifacts are insufficient.

### RUN-17 — Review / Approval Contract

Exercise human review as a governance contract without adding a persistent runtime.

Add/validate states and artifacts such as:

- `awaiting_review`;
- `awaiting_approval`;
- `rejected`;
- `returned_for_rework`;
- approval/rejection record with actor, reason, timestamp and evidence references.

Use a DEEP-CHANGE classification exercise or an already-approved real task. This validates the policy model before choosing any interrupt-capable runtime.

### RUN-18 — Trace ↔ run_id Observability Contract

Define a runtime-neutral trace correlation interface:

- stable `run_id`;
- external trace/provider ID when available;
- event/gate/handoff correlation;
- evidence links;
- failure reason codes.

Do **not** build a tracing backend. The purpose is to prove that MPE can consume external traces while remaining runtime-independent.

### RUN-19 — Run-Level Audit Dashboard

Extend the dashboard using static/versioned MPE artifacts only.

The run view should expose:

- route / selected team;
- handoffs;
- gates;
- approvals;
- evidence;
- terminal state;
- reason codes and failed-gate drill-down where data exists.

This replaces “status-only dashboard” thinking with an audit interface while staying inside Option A+.

### RUN-20 — Stage 2 Governed Delivery Capstone

Run one representative end-to-end task through the mature Stage 2 governance path:

`New Idea Filter → FAST/VERIFIED/DEEP-CHANGE → Run Contract → Expert/Team → typed handoffs → deterministic gates → review/approval where required → evidence → terminal state → audit view`.

RUN-20 is not a new runtime implementation. It is the final integrated validation of the governance model before the Stage 2 exit review.

## Reordered backlog after Stage 2

The previous long-range experiment list remains useful, but recommendations change its order and merge several items to avoid duplicate infrastructure.

### Tier A — core governance first

Covered or initiated by RUN-13…RUN-20:

1. goal/run contracts;
2. typed handoff/gate/evidence/terminal-state contracts;
3. validator and negative tests;
4. provenance/context integrity;
5. review/approval policy contracts;
6. trace correlation contract;
7. run-level audit dashboard.

These are now ahead of runtime expansion, living memory and generic multi-agent execution.

### Tier B — first external execution adapter, conditional after Stage 2

Only after `STAGE2_EXPERIMENT_REVIEW.md` recommends KEEP A+, ADJUST A+, or an explicitly approved RFC path:

**OpenAI Agents SDK controlled adapter experiment**

Candidate scope:

- `adapters/openai-agents/`;
- map MPE Expert definitions to external agent definitions;
- map playbook instructions/routes;
- translate MPE gates into pre/post validations or guardrails where appropriate;
- correlate external traces to MPE `run_id`;
- preserve MPE as policy authority and the SDK as replaceable execution layer.

This is an experiment, not a commitment to make OpenAI Agents SDK the permanent runtime.

### Tier C — human-in-the-loop runtime experiment, deep-change gated

If Stage 2 and the first adapter show a real need for controlled pause/resume, evaluate an interrupt-capable runtime such as LangGraph behind the same MPE governance contracts.

This requires a separate deep-change decision before implementation because it changes execution architecture.

### Tier D — retained experiments, lower priority

Keep, but do not promote ahead of the governance core:

- bounded routing / multi-agent execution patterns;
- persistent task identity where versioned `run_id` proves insufficient;
- workspace/worktree isolation patterns;
- security policy packs;
- budget controls;
- circuit breakers;
- maturity scoring;
- learning-loop evaluation.

Patterns already learned from BrowserAct, Munder Difflin and bounded fan-out/fan-in should be reused here rather than reimplemented as separate subsystems.

### Deferred / evidence-required

Do not build unless repeated Stage 2 evidence demonstrates the need:

- living autonomous memory;
- scheduler;
- daemon;
- persistent workers/agents;
- generic workflow engine;
- custom tracing backend;
- custom multi-agent runtime;
- Router orchestration authority.

## Product maturity sequence after alignment

The roadmap now follows this order:

1. **Measure disciplined coordination** — Stage 2 baseline and real runs.
2. **Make governance machine-enforceable** — contracts + validator + negative tests.
3. **Make decisions auditable** — evidence + trace correlation + run-level dashboard.
4. **Prove human control semantics** — review/approval contracts.
5. **Finish Stage 2 and decide architecture** — KEEP A+ | ADJUST A+ | RFC OPTION B | STOP.
6. **Only then test one external runtime adapter** — OpenAI Agents SDK first candidate.
7. **Only with evidence and approval add interrupt/resume runtime capability**.
8. **Apply mature MPE to Business Discovery and other projects as consumers**, not as competing governance systems.

## Business-value hypothesis

The measurable value of these changes is not “more agents.” It is whether MPE can demonstrate:

- fewer skipped gates;
- fewer acceptance criteria missed before review;
- fewer escaped defects;
- lower ambiguity during handoff/resume;
- lower reviewer false-positive/rework overhead;
- faster audit of why a run passed, failed or required human intervention;
- runtime portability without losing governance.

Any experiment that does not improve one of these measurable outcomes should be deprioritized.
