# MURAT AI STACK v2 — NEXT IMPLEMENTATION INSTRUCTION
Date: 2026-08-10
Status: APPROVED NEXT STEP / SOFT-COMPATIBLE IMPLEMENTATION
Base package: MURAT_AI_STACK_V2_RESEARCH_PACKAGE_2026-08-10.zip
Architecture decision: Option A+ — Disciplined Current Stack

## 0. Mission

Continue Murat AI Stack v2 from research into the first bounded implementation.

Do NOT redesign the architecture.
Do NOT install Prime Agent.
Do NOT convert Codex Router into an orchestrator.
Do NOT build a generic workflow engine.
Do NOT create persistent runtime agents.
Do NOT modify MASTER, security boundaries, credentials, or Router authority.

The goal of this stage is to implement the smallest useful operational layer that combines the strongest findings from:

- Murat AI Stack v2 research package;
- Prime Agent / Prime Multi-Agent patterns;
- OmniWork patterns:
  - Expert;
  - Expert Team;
  - Playbook;
  - Review Gate;
  - Shared Memory;
  - goal-to-delivery orchestration.

These OmniWork concepts are vocabulary and lightweight contracts only. They must NOT become a new platform or daemon.

---

# 1. Architectural invariant

Preserve:

User
  -> Codex Orchestrator
  -> Murat Project Engineer
  -> Expert / Expert Team selected by risk and task
  -> Plugin / Skill
  -> explicit model route
  -> Codex Router
  -> provider/model
  -> tools / MCP / repository
  -> deterministic gates
  -> optional independent Judge
  -> optional human gate
  -> run report

Strict boundaries:

- Codex = execution/orchestration environment.
- Codex Router = inference/provider/protocol/credential gateway only.
- Plugin/Skill = professional capability.
- Expert = bounded role definition, not a model and not a permanent process.
- Expert Team = temporary set of role instances for one task/run.
- Playbook = versioned human-readable execution procedure.
- Review Gate = mandatory verification or approval point.
- Shared Memory = reviewed project knowledge referenced from source-of-truth files.
- Model = replaceable reasoning resource.
- Tool/MCP = external capability.

Never bind an Expert permanently to one model.

---

# 2. Implement Murat Project Engineer v1.0

Create a real minimal plugin/skill package named:

murat-project-engineer

It is the coordinator capability for software/project work.

Minimum responsibilities:

1. classify the task;
2. determine risk tier;
3. select one Expert or a temporary Expert Team;
4. select the appropriate Playbook;
5. resolve explicit model route/profile;
6. run mandatory deterministic gates;
7. call an independent Judge only when required;
8. enforce deep-change-gate;
9. produce the compact run report;
10. stop at PASS / REWORK / BLOCKED / HUMAN_REQUIRED.

It must NOT:
- own provider credentials;
- bypass Codex permissions;
- edit Router routing policy autonomously;
- install new executable skills autonomously;
- promote temporary observations to durable memory automatically;
- create persistent agents;
- change MASTER.

---

# 3. Add lightweight Expert definitions

Create:

murat-project-engineer/experts/

Start with exactly four Expert definitions:

1. architect.md
2. coder.md
3. reviewer.md
4. researcher.md

Each Expert definition must contain only:

- expert_id
- role
- responsibility
- invoke_when
- do_not_invoke_when
- allowed_inputs
- expected_outputs
- required_skills
- capability_profile
- preferred_route_profile
- max_rework_cycles
- forbidden_actions
- handoff_contract

Do NOT add lifecycle daemons, queues, databases, agent identities, heartbeats, schedules, retained state, or autonomous loops.

Expert is a role contract, not an application process.

---

# 4. Add temporary Expert Team composition

Create:

murat-project-engineer/teams/

Only define reusable team compositions, not running teams.

Initial teams:

## software-standard
- architect
- coder

## software-verified
- architect
- coder
- reviewer

## research-verified
- researcher
- reviewer

Team creation at runtime must be temporary and scoped to one run.

Rules:

- single Expert is preferred when sufficient;
- do not use a Team merely because multiple agents are available;
- reviewer must be independent from the producer invocation for IMPORTANT or higher risk;
- multi-solver remains evidence-gated and is not part of the default team.

---

# 5. Convert current runbooks into Playbooks

Create:

murat-project-engineer/playbooks/

Required initial Playbooks:

1. fast.md
2. verified.md
3. deep-change.md
4. software-feature.md

Playbook is markdown/YAML-frontmatter if useful, but NOT a generic DSL.

Each Playbook must declare:

- playbook_id
- version
- supported_task_classes
- risk_tier
- roles
- sequence
- required_inputs
- deterministic_gates
- optional_semantic_review
- human_gate_conditions
- max_rework_cycles
- terminal_states
- run_report_fields

No expression language.
No arbitrary Python.
No scheduler.
No daemon.
No generic DAG executor.

---

# 6. Review Gates

Create:

murat-project-engineer/gates/

Implement a registry of named gates.

Initial cross-project gates:

- clean_diff_scope
- secrets_scan
- build
- typecheck
- lint
- unit_tests
- integration_tests
- acceptance_tests
- artifact_exists
- artifact_hash
- rollback_available
- deep_change_check

Gate contract:

gate_id
type: deterministic | semantic | human
hard: true | false
applicable_when
evidence_required
failure_state
retry_policy

Rules:

1. deterministic checks always precede semantic Judge;
2. a hard deterministic failure can never be overruled by an LLM;
3. malformed Judge output = INCONCLUSIVE;
4. budget exhaustion != PASS;
5. deep change = HUMAN_REQUIRED until explicit user approval;
6. external irreversible effects require their own human/policy gate.

---

# 7. Shared Memory — use existing source-of-truth, do not build memory service

Adopt OmniWork's useful concept of shared cross-agent context, but implement it with current project files.

Do NOT create:
- vector DB;
- memory daemon;
- autonomous memory writer;
- global memory service;
- self-modifying prompt store.

Create a simple context manifest:

murat-project-engineer/context/project-context.md

It should reference, not duplicate:

- MASTER;
- AGENTS.md;
- FOUNDATION.md;
- DESIGN.md;
- STATUS.md;
- SESSION_NOTES.md;
- approved project decisions;
- relevant plugin/skill docs.

Memory classes for this stage:

A. Session observations
- temporary;
- never automatically promoted.

B. Project facts/decisions
- must live in reviewed source-of-truth files;
- must include provenance when material.

C. Lessons candidates
- stored only as proposals in LESSONS_CANDIDATE.md;
- no automatic promotion.

D. Core rules
- immutable from this implementation;
- deep-change-gate required.

---

# 8. Typed handoff without building a workflow engine

Create a small handoff template:

murat-project-engineer/contracts/HANDOFF.md

Required fields:

- run_id
- task_id
- producer_role
- consumer_role
- task_summary
- input_refs
- changed_files
- artifact_refs
- assumptions
- unresolved_risks
- checks_already_run
- required_next_checks
- acceptance_criteria
- do_not_change

Architect -> Coder and Coder -> Reviewer must use this contract in verified flows.

Do not pass hidden chain-of-thought.
Pass only observable decisions, evidence, artifacts and unresolved risks.

---

# 9. Compact Run Report v1

Create:

murat-project-engineer/contracts/RUN_REPORT.md

Required fields:

- run_id
- project
- task
- start/end timestamp
- risk_tier
- playbook
- experts_invoked
- route_profiles
- files_changed
- commands/tools_used
- deterministic_gate_results
- judge_verdict if used
- approvals
- rework_count
- outcome: PASS | REWORK | BLOCKED | HUMAN_REQUIRED
- unresolved_risks
- rollback
- approximate usage/cost when observable

Do NOT create JSONL observability infrastructure yet.

This report is the measurement source for the first 20 runs.

---

# 10. Risk classification

Use these tiers:

## FAST
Low-risk, reversible, narrow.
Flow:
single Expert -> self-check/deterministic checks -> report

## VERIFIED
Meaningful code/content change.
Flow:
Architect -> Coder -> deterministic gates -> optional/required Reviewer -> report

## DEEP-CHANGE
Touches:
- MASTER;
- core architecture;
- Router authority;
- security/credentials;
- persistent agents;
- fundamental plugin boundaries;
- memory governance;
- central runtime.

Flow:
analysis -> soft-compatible alternative check -> STOP -> HUMAN_REQUIRED

The exact user approval marker remains:

DEEP_CHANGE_REQUIRES_USER_APPROVAL

No implementation continues past that marker without explicit approval.

---

# 11. SoftwareFeature Playbook v1

Implement the first real PoC:

Task
  -> classify
  -> risk
  -> Architect
  -> typed handoff
  -> Coder
  -> deterministic gates
  -> Reviewer only if risk/criteria require
  -> max one normal rework cycle
  -> final gates
  -> Run Report
  -> terminal state

Architect output:
- objective;
- affected components;
- constraints;
- acceptance criteria;
- likely files;
- tests required;
- rollback;
- deep-change assessment.

Coder output:
- implementation;
- changed files;
- tests;
- deviations;
- unresolved issues.

Reviewer input:
- original task;
- Architect contract;
- candidate diff/artifacts;
- deterministic results;
- acceptance criteria.

Reviewer output must be structured:

decision: PASS | REWORK | INCONCLUSIVE | HUMAN_REQUIRED
critical_findings:
noncritical_findings:
evidence:
confidence:

Reviewer must not edit the candidate in the same invocation.

---

# 12. Route Profiles

Do not modify Router internals.

Maintain simple coordinator-side profiles:

- default
- cheap-research
- coding
- strong-review

Each profile resolves to an explicit currently configured Router model slug.

If a route is unavailable:
- report it;
- use an explicitly allowed fallback;
- record fallback in Run Report.

Do not implement adaptive learning/routing yet.

---

# 13. Baseline and experiment

Before evaluating the new method, select 20 representative real or isolated tasks.

For every task record:

- task class;
- risk tier;
- whether one Expert or Team was used;
- run duration;
- model/profile;
- tool calls where observable;
- deterministic gate failures;
- reviewer findings;
- false positive reviewer findings;
- rework count;
- human intervention;
- defect escaped after PASS;
- interruption/recovery issue;
- estimated token/cost overhead;
- whether fan-out/fan-in was actually needed.

At least some runs must be executed with the previous simpler Codex approach as baseline.

The objective is not to prove the architecture correct.
The objective is to discover where the architecture is unnecessary or insufficient.

---

# 14. Stop / expansion criteria

Do NOT progress automatically to a Workflow Engine.

Workflow/Env Lite RFC is allowed only when evidence shows one of:

- >= 5 repeated workflows with stable structure;
- >= 3 material gate/recovery failures caused by runbook limitations;
- repeated fan-out/fan-in need;
- repeated resume/recovery pain;
- measurable defect/effort advantage from a formal executor.

Do NOT progress automatically to persistent agents.

Persistent-agent RFC requires:
- >= 3 expensive repeated context rebuilds;
- stable state ownership;
- measurable expected benefit;
- TTL/stale detection/migration/rollback design.

Do NOT integrate Prime runtime unless current Codex path repeatedly fails specifically because of long-running detached execution, persistent kernel state, recursive programmatic subagents or crash recovery.

---

# 15. OmniWork-derived UX concepts to retain

Adopt these names in documentation where helpful:

Expert
Expert Team
Playbook
Review Gate
Shared Memory
Goal -> Delivery

But keep Murat-specific execution semantics.

Important:
OmniWork is an architecture/UX inspiration, not a dependency.

Do not copy its product assumptions about creative workflows into Murat's vertical domains.

Future domain teams may include:

Furniture Project Team
- Sales Expert
- Layout Expert
- Engineering Expert
- Production Expert
- Document Expert
- Legal Expert

But DO NOT implement these domain teams in this stage.
First validate the software workflow PoC.

---

# 16. Deliverables for this Codex iteration

Codex must produce:

1. repository/path audit showing where this package should live;
2. murat-project-engineer plugin/skill skeleton;
3. experts/ with four role contracts;
4. teams/ with three temporary team definitions;
5. playbooks/ with four runbooks/playbooks;
6. gates/ registry;
7. context/project-context.md;
8. contracts/HANDOFF.md;
9. contracts/RUN_REPORT.md;
10. SoftwareFeature PoC wiring using existing Codex capabilities;
11. tests/validation for contracts and required fields;
12. README.md explaining execution;
13. CHANGELOG.md;
14. one sample run in an isolated repository/worktree;
15. sample completed RUN_REPORT.md;
16. implementation review identifying anything that accidentally became a second orchestration platform.

---

# 17. Mandatory final self-review

Before declaring completion, answer:

1. Did we change MASTER?
2. Did we change Router authority?
3. Did we introduce a daemon?
4. Did we introduce a generic workflow engine?
5. Did we introduce persistent runtime agents?
6. Did we create automatic memory promotion?
7. Did we give an LLM power to override deterministic hard gates?
8. Did we bind roles permanently to models?
9. Did we bypass deep-change-gate?
10. Can the whole Stage 1 implementation be disabled/reverted without breaking existing projects?

If any answer to 1–9 is YES:
STOP and mark:
DEEP_CHANGE_REQUIRES_USER_APPROVAL

Question 10 must be YES.

---

# 18. Completion definition

This iteration is complete only when:

- one isolated SoftwareFeature workflow has run end-to-end;
- each handoff is explicit;
- deterministic gates are evidenced;
- Reviewer independence is preserved when used;
- final state is typed;
- Run Report exists;
- rollback is documented;
- no central architecture authority changed;
- the implementation can be removed without breaking Codex Router or existing projects.

Do not continue into Stage 2/3/Prime/Persistence automatically.

Return:
- implementation summary;
- created/changed files;
- sample run result;
- deviations from this instruction;
- metrics captured;
- unresolved risks;
- recommendation: CONTINUE / NARROW / STOP / RFC_REQUIRED.
