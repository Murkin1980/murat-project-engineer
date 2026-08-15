# Runtime Coordination Patterns

Status: bounded MPE capability
Decision: `EXTEND_EXISTING`
Source experiment: RUN-10

## Purpose and reuse map

| Existing artifact | Purpose | Reuse as-is | Extension needed | Conflict |
|---|---|---|---|---|
| `contracts/HANDOFF.md` | Semantic handoff truth | Yes | Envelope carries only its reference | None |
| `contracts/RUN_REPORT.schema.json` | Canonical run evidence | Yes | Event helper summarizes into existing fields | None |
| `gates/registry.yaml` | Deterministic safety policy | Yes | Five measurable coordination gates | None |
| Expert/team definitions | Bounded roles | Yes | Run-scoped lifecycle metadata only | Persistent identity prohibited |
| Codex/host Git worktrees | Isolation and cleanup | Yes | Descriptive ownership metadata | MPE must not manage worktrees |

## Boundaries

MPE supplies contracts and a stateless helper. Codex remains the execution authority; Git/project files and the Run Report remain canonical. Runtime inboxes, JSONL events, and lifecycle records are ephemeral supporting evidence and are not committed by default.

## Mailbox transport

`MAILBOX_ENVELOPE.schema.json` wraps a reference to the authoritative typed HANDOFF. `message_id` is restricted to 1–128 ASCII letters, digits, underscores, or hyphens so it cannot become a path. `deliver_atomic` rejects mailbox paths crossing a symlink or Windows junction/reparse point, acquires a message-scoped exclusive lock, writes and fsyncs a temporary file, and atomically renames it into the inbox. Duplicate or concurrently active message IDs fail deterministically, including between processes. Transient inboxes belong under `.mpe-runtime/mailboxes/`. There is no broker, socket, poller, retry worker, or daemon.

## Event vocabulary

Core factual events are `spawn`, `handoff`, `gate`, and `terminal`; optional bounded events are `claim`, `block`, and `resume`. JSONL is append-only supporting evidence owned by exactly one named writer, normally the run coordinator. The helper records that owner beside the log and rejects a different writer; it does not provide multi-writer locking or a broker. The run owner must retain the log only for the evidence period required by the project, then archive a redacted artifact or delete it. Events exclude prompts, transcripts, secrets, and chain-of-thought. `summarize_events` maps them into existing Run Report concepts without modifying Run Report semantics.

## Lifecycle and worktree ownership

Lifecycle identities are scoped to run, role, and task. State transitions are validated against a small finite vocabulary. Worktree metadata is descriptive; Codex/host Git creates and cleans worktrees. Two concurrently active writer roles owning the same resolved worktree path is a gate failure.

## Explicitly out of scope

No persistent agents, scheduler, heartbeat, mission engine, background service, shared/semantic memory, database, workflow engine, event-sourcing architecture, new orchestrator, autonomous approval bypass, provider history, or new repository.
