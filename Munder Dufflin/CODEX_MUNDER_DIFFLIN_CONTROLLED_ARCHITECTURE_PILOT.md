# CODEX INSTRUCTION — MUNDER DIFFLIN CONTROLLED ARCHITECTURE PILOT
## Murat Project Engineer — Multi-Agent Runtime / Coordination Evaluation

**Date:** 2026-08-15  
**Primary governing repository:** `Murkin1980/murat-project-engineer`  
**Decision:** `EXPERIMENT`  
**Suggested run:** `RUN-10`  
**New repository:** `NO`  
**Deep change:** `NOT AUTHORIZED`

---

# 0. EXECUTIVE DIRECTIVE

Evaluate **Munder Difflin** as an external local-first multi-agent harness and as a source of reusable runtime/coordination patterns.

The goal is NOT to replace Murat Project Engineer.

The goal is NOT to adopt Munder Difflin as a second orchestrator by default.

The goal is to answer:

> Which specific runtime mechanisms implemented by Munder Difflin provide measurable value beyond the current Murat Project Engineer + Codex workflow, and can any of them be reused without creating overlapping authority or deep architectural duplication?

Munder Difflin currently presents capabilities including:

- real CLI worker processes;
- worktree isolation;
- GOD/orchestrator agent;
- agent mailboxes;
- shared memory / semantic recall;
- task ledger / blackboard;
- schedules / triggers;
- approval gates;
- per-agent budgets;
- circuit breaker;
- observability / command center;
- local-first execution;
- Codex and other CLI agents as workers.

Treat every capability as **untrusted until measured**.

---

# 1. MURAT PROJECT ENGINEER NEW IDEA FILTER

Record:

```text
MURAT_PROJECT_ENGINEER_NEW_IDEA_FILTER

Idea:
Evaluate Munder Difflin as a reusable multi-agent runtime/reference architecture.

Decision:
EXPERIMENT

Why:
- It overlaps materially with existing MPE coordination concepts.
- It may contain reusable implementations of worktree isolation, mailbox transport,
  lifecycle control, budgets, approvals, observability, and runtime supervision.
- A controlled pilot can determine value without changing production architecture.
- A new repository is unnecessary.
- Direct adoption would risk two competing orchestrators.
```

Do not begin adoption before the experiment ends.

---

# 2. CURRENT ARCHITECTURE — MUST REMAIN AUTHORITATIVE

Preserve these boundaries:

```text
Murat Project Engineer
= policy + bounded coordination + project rules + gates + evidence

Codex
= primary execution/orchestration environment

Codex Router
= inference / protocol / credential gateway only

Git / project files
= source of truth

Experts
= bounded roles

Expert Teams
= temporary per-run compositions

Playbooks
= versioned procedures

Review Gates
= deterministic / semantic / human checks

Run Reports
= durable evidence
```

Do not silently reassign these responsibilities to Munder Difflin.

---

# 3. CRITICAL OVERLAP RISK

Munder Difflin has its own orchestrator/supervisor.

Therefore the following architecture is prohibited in this pilot:

```text
Murat Project Engineer
        ↓
Munder GOD orchestrator
        ↓
Codex
        ↓
Codex Router
```

if both MPE and Munder are allowed to independently:

- decompose work;
- choose roles;
- assign tasks;
- change scope;
- promote memory;
- schedule missions;
- approve actions;
- decide terminal outcomes.

Two policy authorities are not allowed.

---

# 4. ALLOWED EXPERIMENT MODES

Only these modes are allowed:

## MODE A — Harness benchmark

Munder runs independently on one isolated benchmark task.

MPE remains external evaluator.

```text
MPE
 └─ defines benchmark + acceptance criteria
      ↓
Munder
 └─ executes isolated benchmark
      ↓
MPE
 └─ evaluates evidence
```

## MODE B — Component/reference analysis

Codex reads Munder source/docs and identifies reusable patterns.

No Munder runtime authority enters MPE.

## MODE C — Narrow runtime reuse proposal

After evidence, propose one bounded runtime component such as:

```text
worktree isolation
mailbox transport
agent lifecycle tracking
budget enforcement
circuit breaker
event/telemetry model
```

Do not implement unless it is clearly non-deep-change.

---

# 5. OFFICIAL SOURCES TO VERIFY

Before install or execution, verify current documentation.

Primary references:

- `https://munderdiffl.in/`
- `https://munderdiffl.in/privacy.html`
- `https://munderdiffl.in/blog/`
- `https://github.com/chaitanyagiri/munder-difflin`

Verify:

```text
latest release
supported OS
supported agent CLIs
Windows behavior
license
install procedure
worktree behavior
mailbox behavior
memory behavior
approval gates
budgets
circuit breaker
scheduling/triggers
telemetry
data storage
```

Do not rely on stale command syntax.

---

# 6. PRIVACY / LOCAL-FIRST GATE

Current public documentation describes Munder Difflin as local-first.

Nevertheless verify before use:

```yaml
privacy_gate:
  local_app:
  account_required:
  sync_service:
  code_uploaded_by_munder:
  memory_uploaded_by_munder:
  telemetry_enabled:
  telemetry_fields:
  telemetry_disable_supported:
  worker_provider_data_policy:
  status:
```

Important distinction:

```text
Munder local-first
≠
worker model provider local
```

Codex / Claude / OpenCode / other workers retain their own provider/data rules.

Do not store secrets in experiment reports.

---

# 7. INSTALLATION POSITION

Install Munder Difflin as a **separate desktop/local evaluation tool**.

Do NOT add it as a dependency to:

- `murat-project-engineer`;
- `business-discovery`;
- `mebeldocs-ai`;
- Kitchen Configurator;
- any production repository.

Do not modify project runtime configuration to support it.

Prefer official desktop release.

If building from source is required, use a clean isolated directory outside product repositories.

Record:

```yaml
installation:
  version:
  source:
  install_method:
  os:
  runtime_requirements:
  config_path:
  data_path:
  telemetry_setting:
  uninstall_path:
```

---

# 8. PRE-FLIGHT — CURRENT MPE CAPABILITY MAP

Before touching Munder runtime, inspect current MPE.

Build:

```text
CURRENT_MPE_CAPABILITY_MAP
```

Required rows:

```text
task decomposition
expert selection
temporary teams
typed handoffs
worktree isolation
agent lifecycle
mailbox/messaging
shared memory
project source-of-truth
run state
review gates
human approval
budget/cost tracking
circuit breaker
scheduling
resume/interruption
observability
task board
rollback
evidence persistence
```

For each:

```yaml
capability:
  exists_in_mpe:
  implementation_state:
  canonical_files:
  used_in_real_runs:
  known_gap:
```

Do not compare against assumptions.

---

# 9. MUNDER COMPONENT MAP

Inspect Munder source/docs and create:

```text
MUNDER_COMPONENT_MAP
```

At minimum:

```text
GOD orchestrator
worker process launcher
PTY/session management
worktree manager
mailbox router
agent inbox/outbox
task ledger
blackboard
shared memory
semantic memory index
approval system
budgets
circuit breaker
schedules/triggers
Slack/webhook triggers
GitHub/CI integration
command center
terminal UI
diff/review UI
telemetry
event model
resume/recovery
```

For every component record:

```yaml
component:
  source_path_or_doc:
  responsibility:
  state_owned:
  persistence:
  inputs:
  outputs:
  dependencies:
  security_boundary:
```

---

# 10. REQUIRED OVERLAP MATRIX

Create:

```text
MPE vs MUNDER OVERLAP MATRIX
```

For every Munder component classify:

```text
DUPLICATE
MUNDER_BETTER
MPE_BETTER
MISSING_IN_MPE
COMPLEMENTARY
NOT_NEEDED
DEEP_CHANGE
```

Then choose one proposal status:

```text
REUSE_COMPONENT
REUSE_PATTERN
HOLD
REJECT
```

No integration is allowed solely because something exists in Munder.

---

# 11. PRIMARY BENCHMARK TASK

Use ONE bounded real repository task.

Preferred repository:

```text
Murkin1980/murat-project-engineer
```

or another low-risk public/internal code repo if current MPE worktree is unsuitable.

Do not benchmark on:

- production customer data;
- MebelDocs sensitive data;
- live financial flows;
- authentication systems;
- deployment infrastructure.

Suggested benchmark:

> Inspect one bounded subsystem, identify one real small issue or missing validation, implement a minimal fix, add/update a test, run deterministic checks, independently review the diff, and return PASS / REWORK.

---

# 12. BENCHMARK TEAM

Use exactly three functional roles:

```text
Researcher
Implementer
Reviewer
```

Do not create a large hive.

Expected handoff:

```text
Researcher
  ↓
findings / target files / risks
  ↓
Implementer
  ↓
minimal patch + tests
  ↓
Reviewer
  ↓
PASS / REWORK
```

If Munder requires a supervisor, the supervisor may route messages only within the benchmark.

It may NOT change benchmark acceptance criteria.

---

# 13. BENCHMARK CONSTRAINTS

Record before execution:

```yaml
benchmark:
  repository:
  baseline_commit:
  branch:
  goal:
  acceptance_criteria:
  allowed_files:
  forbidden_files:
  max_files_changed:
  tests_required:
  build_required:
  deep_change_allowed: false
  max_rework:
  max_human_interventions:
```

Use isolated worktrees if supported.

No agent may modify the same working tree concurrently.

---

# 14. CONTROL RUN

Compare Munder with the current MPE/Codex workflow.

Use equivalent starting state.

Preferred structure:

```text
RUN A
MPE + Codex

RUN B
Munder Difflin
```

or reuse a sufficiently comparable recent MPE run if it has:

- same risk tier;
- similar scope;
- complete evidence;
- clear rework/human-intervention metrics.

Do not fabricate symmetry where tasks differ materially.

---

# 15. COMPARISON METRICS

Record for both:

```yaml
comparison:
  task_decomposition_quality:
  correct_file_discovery:
  scope_violations:
  files_changed:
  unexpected_files_changed:
  agent_collisions:
  handoff_quality:
  context_loss:
  human_interventions:
  rework_count:
  tests_passed:
  tests_failed:
  acceptance_criteria_passed:
  review_quality:
  rollback_clarity:
  interruption_recovery:
  traceability:
  runtime:
  observable_cost:
```

Qualitative scores:

```text
POOR
ADEQUATE
GOOD
EXCELLENT
```

---

# 16. WORKTREE EVALUATION

This is a priority capability.

Evaluate:

```text
creation
naming
base commit correctness
isolation
parallel safety
cleanup
diff visibility
merge/review flow
failure cleanup
```

Decision:

```text
WORKTREE_CAPABILITY:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT
```

---

# 17. MAILBOX / HANDOFF EVALUATION

Evaluate whether Munder mailbox materially improves MPE typed handoffs.

Check:

```text
sender identity
recipient identity
task correlation
message ordering
delivery state
acknowledgement
artifact references
failure state
retries
durability
human visibility
```

Compare to current MPE handoff model.

Do not adopt free-form agent chat as a replacement for typed handoffs.

Preferred reuse outcome:

```text
typed handoff contract
+
mailbox transport
```

if compatible.

---

# 18. AGENT LIFECYCLE EVALUATION

Evaluate:

```text
spawn
ready
working
blocked
waiting
reviewing
done
failed
cancelled
```

Identify whether Munder has a coherent runtime state machine.

Ask:

> Could MPE preserve policy authority while reusing only lifecycle state/transport?

---

# 19. BUDGET EVALUATION

Inspect:

```text
per-agent token budget
spend limit
runtime limit
velocity limit
budget breach behavior
human approval
auditability
```

Compare against MPE Run Report cost fields.

Important:

Tracking cost after a run is not the same as enforcing a runtime budget.

Determine whether Munder provides a missing capability.

---

# 20. CIRCUIT BREAKER EVALUATION

Evaluate the advertised control ladder conceptually:

```text
STEER
→ CONSTRAIN
→ STOP
```

Test only using safe artificial conditions.

Examples:

```text
repeated failed test
scope drift attempt
rework threshold exceeded
worker stuck
```

Do not create destructive failure scenarios.

---

# 21. HUMAN APPROVAL EVALUATION

Check how Munder handles:

```text
scope expansion
destructive operation
spend/budget threshold
sensitive operation
blocked agent
```

Compare with MPE:

```text
FAST
VERIFIED
DEEP_CHANGE
```

MPE deep-change gate remains authoritative.

If Munder approval semantics conflict with MPE:

```text
MPE_WINS
```

---

# 22. SHARED MEMORY EVALUATION

This capability is HIGH RISK for architectural duplication.

MPE currently treats Git/project files as source of truth.

Therefore do NOT adopt Munder memory wholesale.

Inspect:

```text
markdown memory
semantic recall/index
personal memory
shared/org memory
automatic writes
promotion rules
deletion
staleness
source attribution
conflict resolution
```

Answer:

> Can any memory technique be reused without creating a second source of truth?

Allowed outcomes:

```text
REUSE_PATTERN
HOLD
REJECT
```

Default preference:

```text
HOLD
```

unless strong evidence shows a bounded safe reuse.

No autonomous memory promotion is authorized.

---

# 23. SCHEDULING / LONG-RUNNING MISSIONS

Do NOT enable autonomous recurring missions in this pilot.

Inspect only.

Scheduling, Slack triggers, webhooks, unattended missions, or overnight autonomy represent architecture pressure.

Record:

```text
SCHEDULING_CAPABILITY:
REFERENCE_ONLY
```

If adoption would require scheduler/runtime authority:

```text
DEEP_CHANGE_REQUIRES_USER_APPROVAL
```

---

# 24. OBSERVABILITY EVALUATION

Evaluate whether Munder improves visibility of:

```text
active agents
current task
current state
worktree
budget
messages
blocked state
reviews
diffs
completed work
failure reason
```

Assess Command Center / UI as:

```text
UX_ONLY
OPERATIONALLY_USEFUL
ARCHITECTURALLY_USEFUL
```

Do not copy pixel-office UI or branding.

Focus on state model and operator visibility.

---

# 25. EVENT / TELEMETRY MODEL

Inspect internal event handling.

Identify whether there is a useful generic event vocabulary:

```text
agent_spawned
task_assigned
message_sent
work_started
work_blocked
approval_requested
approval_granted
budget_warning
review_started
review_completed
agent_stopped
```

Compare with MPE Run Report fields.

Potential reuse:

```text
runtime event stream
→ compact Run Report
```

Do not introduce event sourcing infrastructure in this pilot.

---

# 26. RESUME / INTERRUPTION TEST

Run one safe interruption test using supported controls.

Check whether:

- task state survives;
- worktree survives;
- handoff survives;
- context is restored correctly;
- duplicate execution occurs;
- human intervention is required.

Do not terminate processes in a way that risks repository corruption.

---

# 27. SECURITY REVIEW

Inspect especially:

```text
shell execution
PTY spawning
working-directory boundaries
environment inheritance
API keys
CLI credentials
mailbox inputs
webhook inputs
Slack inputs
file access
memory poisoning
command injection surfaces
```

Do not run adversarial security testing beyond safe source review in this pilot.

---

# 28. MUNDER ORCHESTRATOR EVALUATION

The GOD orchestrator itself must receive a separate decision.

Evaluate:

```text
goal decomposition
role selection
task routing
scope preservation
escalation
adjudication
terminal decision
```

Compare against MPE.

Allowed final statuses:

```text
MUNDER_ORCHESTRATOR:
REJECT
HOLD
REUSE_PATTERN
```

Do NOT return `REUSE_COMPONENT` for the orchestrator unless Murat explicitly authorizes a later deep-change evaluation.

---

# 29. NO AUTOMATIC MEMORY / SCHEDULE / AUTONOMY ADOPTION

The following are blocked from implementation:

```text
shared semantic memory as new source of truth
persistent orchestrator runtime
scheduled missions
Slack-triggered autonomous work
webhook-triggered autonomous work
cross-device node network
24/7 unattended agent office
automatic task ingestion
automatic PR shipping
```

These require separate explicit approval.

---

# 30. COMPONENT-LEVEL TERMINAL DECISIONS

Return independent decisions for:

```text
WORKTREE_MANAGER
MAILBOX_TRANSPORT
AGENT_LIFECYCLE
BUDGET_GATES
CIRCUIT_BREAKER
APPROVAL_MODEL
OBSERVABILITY_MODEL
EVENT_MODEL
SHARED_MEMORY
SCHEDULER
GOD_ORCHESTRATOR
DESKTOP_RUNTIME
```

Each:

```text
REUSE_COMPONENT
REUSE_PATTERN
HOLD
REJECT
```

---

# 31. OVERALL MUNDER DECISION

Choose exactly one:

```text
MUNDER_OVERALL_DECISION:

REUSE_COMPONENT
REUSE_PATTERN
HOLD
REJECT
```

Interpretation:

## REUSE_COMPONENT
A narrow existing Munder runtime component can be reused without transferring policy authority.

## REUSE_PATTERN
Source/design patterns are useful, but direct runtime integration is not justified.

## HOLD
Promising but evidence insufficient or integration cost too high.

## REJECT
No meaningful incremental value beyond current MPE/Codex.

---

# 32. DEEP-CHANGE TRIGGERS

Immediately stop implementation if proposal requires:

- Munder GOD becoming primary orchestrator;
- replacing MPE coordinator;
- replacing Codex execution authority;
- changing Codex Router authority;
- persistent agent runtime;
- shared autonomous memory;
- new scheduler;
- background daemon;
- 24/7 missions;
- Slack/webhook task ingress;
- cross-device hive;
- new state database;
- new repository;
- automatic PR merge/deployment;
- production secrets changes.

Return:

```text
DEEP_CHANGE_REQUIRES_USER_APPROVAL
```

---

# 33. REQUIRED ARTIFACTS

Inside `murat-project-engineer`, reuse canonical paths where possible.

Suggested:

```text
docs/evaluations/MUNDER_DIFFLIN_EVALUATION.md
docs/evaluations/MUNDER_MPE_COMPONENT_MATRIX.md
docs/evaluations/MUNDER_REUSE_DECISION.md
evidence/stage2/RUN-10_REPORT.json
evidence/stage2/RUN-10_EXPERIMENT_RECORD.json
```

Optional compact benchmark evidence:

```text
evidence/stage2/run-10/
  benchmark-summary.json
  component-decisions.json
```

Do not commit:

- Munder runtime data;
- personal memory;
- credentials;
- terminal history with secrets;
- large logs;
- node identifiers;
- unrelated agent conversations.

---

# 34. RUN REPORT

Use current MPE schema.

Suggested task:

```text
Controlled Munder Difflin architecture and runtime evaluation against the current MPE/Codex multi-agent workflow.
```

Suggested risk tier:

```text
VERIFIED
```

Suggested experts:

```text
Researcher
Architect
Reviewer
```

Use the smallest sufficient team.

---

# 35. ACCEPTANCE CRITERIA

Pilot passes only if:

```text
1. Munder installs/runs without product repository integration.
2. One bounded multi-agent benchmark completes.
3. Worktree isolation is verified or accurately classified.
4. Handoff/mailbox behavior is observed.
5. Reviewer remains independent.
6. No deep-change boundary is crossed.
7. No new repository is created.
8. MPE retains policy authority.
9. At least one Munder capability is shown to be measurably better,
   missing in MPE, or explicitly unnecessary.
10. Component-by-component decisions are evidence-backed.
```

---

# 36. SUCCESS DEFINITION

Success is NOT:

```text
Munder looks impressive
```

Success is NOT:

```text
three agents ran at once
```

Success is:

```text
clear evidence of which runtime capabilities:
- solve a real MPE gap,
- duplicate existing MPE,
- add unacceptable complexity,
- or can be reused safely.
```

---

# 37. IMPLEMENTATION ORDER

Execute exactly:

```text
STEP 1
Read MPE source of truth + recent Run Reports.

STEP 2
Record New Idea Filter = EXPERIMENT.

STEP 3
Build CURRENT_MPE_CAPABILITY_MAP.

STEP 4
Research current official Munder docs/repo/release.

STEP 5
Build MUNDER_COMPONENT_MAP.

STEP 6
Build MPE vs MUNDER OVERLAP MATRIX.

STEP 7
Verify privacy/local-first/telemetry behavior.

STEP 8
Install Munder outside product repos.

STEP 9
Configure only the minimum workers required for benchmark.

STEP 10
Define bounded benchmark task and acceptance criteria.

STEP 11
Run control/current-MPE comparison if needed.

STEP 12
Run Munder three-role benchmark.

STEP 13
Evaluate worktrees, mailbox, lifecycle, approvals, budgets, circuit breaker, observability.

STEP 14
Run one safe interruption/resume check.

STEP 15
Review security boundaries.

STEP 16
Produce per-component REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT.

STEP 17
Produce MUNDER_OVERALL_DECISION.

STEP 18
Update MPE evaluation + RUN-10 evidence.

STEP 19
Return compact result to Murat.

STEP 20
STOP.
No production integration.
```

---

# 38. REQUIRED FINAL RESPONSE TO MURAT

Return exactly:

```text
MUNDER DIFFLIN CONTROLLED PILOT

Overall:
PASS / CONDITIONAL / FAIL

Munder version:
...

Benchmark repository:
...

Benchmark result:
PASS / REWORK / FAIL

Acceptance criteria:
PASS / FAIL

Compared with current MPE/Codex:
BETTER / MIXED / EQUIVALENT / WORSE

Worktree manager:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Mailbox transport:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Agent lifecycle:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Budget gates:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Circuit breaker:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Approval model:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Observability model:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Event model:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Shared memory:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Scheduler:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

GOD orchestrator:
REUSE_PATTERN / HOLD / REJECT

Desktop runtime:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Human interventions:
N

Rework:
N

Agent collisions:
N

Interruption recovery:
PASS / PARTIAL / FAIL

Privacy/local-first gate:
PASS / BLOCKED

New repository:
NO

Deep change required:
YES / NO

Overall decision:
REUSE_COMPONENT / REUSE_PATTERN / HOLD / REJECT

Top 3 reusable ideas/components:
1. ...
2. ...
3. ...

What should NOT be adopted:
...

Recommended next action:
...
```

Then point Murat to the full reports.

---

# 39. FINAL ARCHITECTURE RULE

Do not optimize for:

```text
more autonomous agents
```

Optimize for:

```text
less coordination cost
+
fewer collisions
+
better handoffs
+
better runtime safety
+
better evidence
+
no duplicated authority
```

Munder Difflin earns a place only if it improves those outcomes measurably.

Murat Project Engineer remains the governing policy layer unless Murat explicitly approves a future deep-change.
