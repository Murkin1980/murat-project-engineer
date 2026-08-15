# CODEX INSTRUCTION — MPE RUNTIME PATTERNS EXTENSION
## Reuse three validated Munder Difflin patterns without adopting Munder runtime

**Date:** 2026-08-15
**Primary repository:** `Murkin1980/murat-project-engineer`
**Decision:** `EXTEND_EXISTING`
**Source experiment:** `RUN-10`
**Suggested next run:** `RUN-11`
**New repository:** `NO`
**Deep change:** `NOT AUTHORIZED`

# 0. EXECUTIVE DIRECTIVE

Extend the existing Murat Project Engineer architecture with exactly three small runtime/evidence patterns identified in RUN-10:

1. Typed atomic mailbox transport
2. Compact append-only runtime event vocabulary
3. Ephemeral agent lifecycle/worktree metadata

Do NOT adopt Munder Difflin runtime.

Do NOT introduce:
- GOD orchestrator
- persistent agents
- semantic shared memory
- scheduler
- heartbeats
- mission engine
- background daemon
- autonomous approval bypass
- workflow engine
- new datastore
- event-sourcing architecture
- new repository

MPE remains the policy layer.
Codex remains the execution environment.
Git/project files remain the source of truth.

# 1. BINDING INPUT FROM RUN-10

Use these conclusions from RUN-10 as design input:

```text
MUNDER_OVERALL_DECISION = REUSE_PATTERN
```

Reuse patterns only:

```text
1. Typed, atomic filesystem mailbox envelopes mapped to existing HANDOFF fields.
2. Minimal append-only event vocabulary: spawn / handoff / gate / terminal.
3. Explicit ephemeral lifecycle/worktree metadata owned by Codex.
```

Rejected scope:

```text
GOD orchestrator
autonomous bypass mode
semantic shared memory
scheduled missions
heartbeats
persistent agents
workflow-engine state
direct Munder dependency
```

Do not reopen rejected scope in this task.

# 2. NEW IDEA FILTER

Record:

```text
MURAT_PROJECT_ENGINEER_NEW_IDEA_FILTER

Idea:
Add three small runtime/evidence patterns derived from RUN-10.

Decision:
EXTEND_EXISTING

Why:
- They fill concrete observability/handoff gaps in existing MPE.
- They do not require a new repository.
- They preserve Codex as execution authority.
- They compile into current Run Reports instead of creating a second source of truth.
- They can be implemented as contracts/helpers, not a runtime platform.
```

# 3. REPOSITORY AUDIT FIRST

Before editing, inspect current canonical files for:

```text
HANDOFF contract
Run Report schema
Experiment Record schema
gate registry
terminal state vocabulary
expert/team definitions
stage2 experiment files
existing event/status helpers
worktree conventions
```

Search for:

```text
HANDOFF
handoff
run_report
experiment_record
gate
terminal
worktree
lifecycle
event
agent
expert
team
```

Build a short reuse map:

```yaml
existing_artifact:
  purpose:
  reuse_as_is:
  extension_needed:
  conflict:
```

Prefer minimal edits to canonical contracts.

# 4. PATTERN 1 — TYPED ATOMIC MAILBOX TRANSPORT

Goal:

```text
HANDOFF contract = semantic truth
Mailbox envelope = transport wrapper
```

Do NOT create free-form agent chat as the source of truth.

Suggested logical envelope:

```json
{
  "schema_version": "1.0",
  "message_id": "msg-...",
  "run_id": "RUN-...",
  "task_id": "task-...",
  "sender_role": "Researcher",
  "recipient_role": "Implementer",
  "handoff_ref": "path-or-id",
  "created_at": "...",
  "status": "READY"
}
```

Allowed statuses:

```text
READY
CLAIMED
DELIVERED
FAILED
SUPERSEDED
```

Keep payload small.
The detailed handoff content remains in the existing typed HANDOFF artifact or fields.

# 5. ATOMIC DELIVERY

If filesystem transport is implemented:

```text
write temp file
→ close/fsync if applicable
→ atomic rename into inbox
```

Do not rely on partially written JSON.

Do not add:
- socket server
- daemon
- broker
- queue service

A bounded filesystem helper is enough.

# 6. MAILBOX TRACEABILITY

Every delivery must be traceable to:

```text
run_id
task_id
sender
recipient
handoff_ref
message_id
```

No anonymous messages.
No hidden context transfer.

Transient mailbox files should not be committed by default.

# 7. PATTERN 2 — COMPACT APPEND-ONLY EVENT VOCABULARY

Required core events:

```text
spawn
handoff
gate
terminal
```

Optional only if needed:

```text
claim
block
resume
```

Do not create dozens of event types.

Suggested record:

```json
{
  "schema_version": "1.0",
  "event_id": "evt-...",
  "run_id": "RUN-...",
  "timestamp": "...",
  "type": "handoff",
  "actor": "Researcher",
  "target": "Implementer",
  "task_id": "task-...",
  "ref": "handoff-or-gate-ref",
  "status": "DELIVERED"
}
```

Events must be factual.

Do not include:
- model chain-of-thought
- large transcripts
- secrets
- raw prompt logs

# 8. EVENT STORAGE

Use a simple append-only artifact if needed, for example:

```text
evidence/runtime/RUN-XX.events.jsonl
```

or the closest current canonical equivalent.

Do not introduce:
- SQLite
- Postgres
- event broker
- streaming service
- event-sourcing framework

Event files are supporting evidence only.
Run Report remains canonical.

# 9. EVENT → RUN REPORT SUMMARY

Add a deterministic helper that can summarize compatible runtime events into current Run Report fields.

Examples:

```text
handoff events → handoff count
gate events → gate summary
terminal events → terminal outcome
spawn events → invoked roles
```

Do not rewrite Run Report semantics to fit events.

# 10. PATTERN 3 — EPHEMERAL AGENT LIFECYCLE METADATA

Allowed states:

```text
CREATED
READY
WORKING
BLOCKED
WAITING
REVIEWING
DONE
FAILED
CANCELLED
```

Use fewer if equivalent vocabulary already exists.

Suggested record:

```json
{
  "run_id": "RUN-...",
  "role": "Implementer",
  "task_id": "task-...",
  "state": "WORKING",
  "started_at": "...",
  "updated_at": "...",
  "worktree": null,
  "pid": null
}
```

Do not persist provider conversation history.

# 11. WORKTREE METADATA

Track only descriptive ownership metadata if Codex creates isolated worktrees:

```text
worktree_path
branch
base_commit
owner_role
task_id
created_at
cleanup_status
```

MPE must not become a worktree-manager service.
Codex/host Git remain responsible for creation and cleanup.

# 12. COLLISION PREVENTION RULE

Add a deterministic rule:

```text
Two concurrently active writer roles must not own the same mutable worktree.
```

If two roles may write:

```text
separate worktrees
```

or execute sequentially.

Record collision as a gate failure.

# 13. MINIMAL GATES

Evaluate current gate registry for:

```text
mailbox_schema_valid
handoff_traceable
event_log_valid
worktree_collision_check
terminal_state_valid
```

Add only gates with measurable safety value.

# 14. CONTRACT VALIDATION

If the repo consistently uses schemas, possible additions:

```text
MAILBOX_ENVELOPE.schema.json
RUNTIME_EVENT.schema.json
AGENT_RUNTIME_STATE.schema.json
```

Otherwise follow existing TypeScript/Python validation conventions.

Do not force a new schema subsystem.

# 15. REQUIRED TESTS

Mailbox:

```text
valid envelope accepted
missing sender rejected
missing recipient rejected
invalid status rejected
partial JSON not accepted
duplicate message_id handled deterministically
```

Events:

```text
valid core event accepted
unknown event type rejected
append order preserved
event summary deterministic
```

Lifecycle/worktree:

```text
valid state transition accepted
invalid state rejected
two writers same worktree detected
different worktrees allowed
terminal role cannot return to WORKING without explicit new invocation
```

# 16. STATE TRANSITIONS

If transition validation is added, keep it small:

```text
CREATED → READY
READY → WORKING
WORKING → BLOCKED | WAITING | REVIEWING | DONE | FAILED | CANCELLED
BLOCKED → WORKING | CANCELLED | FAILED
WAITING → WORKING | CANCELLED
REVIEWING → DONE | WORKING | FAILED
```

Do not overengineer.

# 17. NO PERSISTENT AGENT IDENTITY

Runtime identity must be run/task scoped.

Prefer:

```text
RUN-11 / Researcher / task-1
```

Not:

```text
researcher-agent-forever
```

Experts remain reusable role definitions, not persistent agents.

# 18. EXPLICITLY OUT OF SCOPE

Do not add:

```text
semantic memory
vector DB
agent memories
auto-promoted lessons
shared hidden context
cron
missions
heartbeat
background polling
recurring workers
GodAgent
SupervisorService
MissionController
HiveManager
AgentOffice
```

Durable lessons belong in Git/project docs/contracts/playbooks/decision records.

# 19. PILOT AFTER IMPLEMENTATION

Run one bounded three-role simulation:

```text
Researcher
→ mailbox handoff
Implementer
→ worktree metadata
→ mailbox handoff
Reviewer
→ gate
→ terminal event
```

Use a safe synthetic or bounded task.

The goal is runtime-contract validation, not model-intelligence benchmarking.

# 20. REQUIRED METRICS

Capture:

```text
handoff_count
handoff_schema_failures
duplicate_message_count
event_count
invalid_event_count
worktree_collisions
lifecycle_transition_failures
human_interventions
rework_count
```

Also compare qualitatively:

```text
handoff ambiguity: BEFORE / AFTER
runtime observability: BEFORE / AFTER
collision visibility: BEFORE / AFTER
```

# 21. SUCCESS CRITERIA

Pass only if all are true:

```text
1. Existing HANDOFF semantics remain authoritative.
2. Mailbox transport is typed and atomic.
3. Runtime events are compact and append-only.
4. Events compile into existing evidence instead of replacing it.
5. Lifecycle metadata is ephemeral.
6. Worktree ownership is observable.
7. Same-worktree concurrent writer collision is detectable.
8. No daemon/scheduler/database/orchestrator is added.
9. No new repository is created.
10. Existing tests remain passing.
11. New deterministic tests pass.
12. Run Report remains canonical.
```

# 22. STOP CONDITIONS

Return `HOLD` if implementation requires:

- large refactor
- new persistent service
- new database
- broad Run Report schema rewrite
- changes to Codex Router authority
- persistent runtime manager
- deep changes to expert/team model

Return:

```text
DEEP_CHANGE_REQUIRES_USER_APPROVAL
```

if any deep-change boundary is crossed.

# 23. DOCUMENTATION

Create or update a concise architecture note, suggested:

```text
docs/architecture/RUNTIME_COORDINATION_PATTERNS.md
```

Document:

```text
purpose
boundaries
mailbox transport
event vocabulary
lifecycle metadata
worktree ownership
canonical evidence
explicit out-of-scope items
```

# 24. RUN EVIDENCE

Use current canonical schemas.

Suggested run:

```text
RUN-11
```

Suggested task:

```text
Implement and validate lightweight runtime coordination patterns:
typed mailbox transport, compact append-only events,
and ephemeral lifecycle/worktree metadata.
```

# 25. TERMINAL DECISION

Choose exactly one:

```text
RUNTIME_PATTERNS_DECISION:

REUSE_COMPONENT
HOLD
REJECT
```

Interpretation:

```text
REUSE_COMPONENT
= patterns are now small, tested, bounded MPE capabilities.

HOLD
= useful but current contracts or implementation cost are not ready.

REJECT
= no measurable coordination value.
```

# 26. REQUIRED FINAL RESPONSE TO MURAT

Return exactly:

```text
MPE RUNTIME PATTERNS EXTENSION

Overall:
PASS / CONDITIONAL / FAIL

Repository:
murat-project-engineer

Decision:
REUSE_COMPONENT / HOLD / REJECT

Mailbox transport:
PASS / FAIL

Atomic delivery:
PASS / FAIL

Event vocabulary:
PASS / FAIL

Event → Run Report summary:
PASS / PARTIAL / FAIL

Lifecycle metadata:
PASS / FAIL

Worktree metadata:
PASS / FAIL

Collision detection:
PASS / FAIL

Existing HANDOFF preserved:
YES / NO

Run Report remains source of truth:
YES / NO

Persistent agents added:
NO

Scheduler added:
NO

Shared memory added:
NO

New orchestrator added:
NO

New database added:
NO

New repository:
NO

Deep change required:
YES / NO

New tests:
N

Test result:
PASS / FAIL

Handoff ambiguity:
IMPROVED / SAME / WORSE

Runtime observability:
IMPROVED / SAME / WORSE

Collision visibility:
IMPROVED / SAME / WORSE

Recommended next action:
...
```

# 27. FINAL RULE

Implement only enough runtime structure to make bounded multi-agent work:

```text
clearer
safer
more traceable
less collision-prone
```

Do not turn MPE into a persistent agent operating system.
