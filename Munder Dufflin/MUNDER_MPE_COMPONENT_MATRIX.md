# Munder ↔ MPE component matrix

| Component | Munder evidence | MPE evidence | Overlap | Decision |
|---|---|---|---|---|
| Task decomposition | GOD, task board, dependencies | playbooks and temporary teams | Partial | HOLD |
| Expert roles | hired persistent agent records | bounded `experts/*.md` roles | Partial | KEEP_MPE |
| Team composition | runtime fleet | smallest sufficient temporary team | Partial | KEEP_MPE |
| Typed handoffs | mailbox envelopes/queue | `contracts/HANDOFF.md` | Strong semantic overlap | REUSE_PATTERN |
| Source of truth | hive + registry + memory + DB | Git/project files | Conflict | KEEP_MPE |
| Run state | registry/task board/events | Run Report/Experiment Record | Partial | REUSE_PATTERN |
| Review gates | hooks/control layer | deterministic gate registry | Partial | KEEP_MPE |
| Human approval | hook/HITL controls; autonomy bypass option | explicit deep-change gate | Conflict | REJECT |
| Evidence capture | events, transcripts, cost ledger | typed evidence artifacts | Partial | REUSE_PATTERN |
| Worktree isolation | optional per-agent worktrees | host/Codex isolation, no MPE runtime | Gap in MPE runtime | HOLD |
| Mailbox transport | atomic filesystem mailbox + local socket hook | artifact handoff contract only | Complementary | REUSE_PATTERN |
| Agent lifecycle | spawn/archive/restore registry | bounded invocation, no persistent lifecycle | Complementary | REUSE_PATTERN |
| Budget enforcement | token/cost caps and breaker | no runtime budget enforcer | Complementary | HOLD |
| Circuit breaker | steer → constrain → stop | terminal states and human gate | Partial | HOLD |
| Scheduling/resume | missions, heartbeat, restore | explicitly out of scope | Conflict | REJECT |
| Observability | Command Center, event log, fleet view | compact reports/evidence | Complementary | REUSE_PATTERN |
| Task board | Kanban/dependencies | no durable board runtime | Complementary | HOLD |
| Event model | append-only runtime events | typed terminal evidence | Complementary | REUSE_PATTERN |
| Shared memory | semantic/markdown memory | Git source-of-truth context | Conflict | REJECT |
| GOD orchestrator | persistent central authority | Codex remains orchestrator | Direct conflict | REJECT |

## Component terminal decisions

- Worktree manager: **HOLD** — source-backed, not runtime-verified in this pilot.
- Mailbox transport: **REUSE_PATTERN** — useful atomic delivery pattern; retain MPE's typed artifact contract.
- Agent lifecycle: **REUSE_PATTERN** — explicit lifecycle/events are useful, but natural exit classification needs scrutiny.
- Budget gates: **HOLD** — not exercised.
- Circuit breaker: **HOLD** — not exercised end-to-end.
- Approval model: **REJECT** — bypass-capable autonomy conflicts with MPE's approval boundary.
- Observability model: **REUSE_PATTERN** — compact state/events can complement reports.
- Event model: **REUSE_PATTERN** — map a small vocabulary into existing evidence, without a new authority store.
- Shared memory: **REJECT** — duplicates Git/project source of truth.
- Scheduler: **REJECT** — outside Option A+ boundaries and enabled unexpectedly during onboarding.
- GOD orchestrator: **REJECT** — duplicates Codex authority.
- Desktop runtime: **HOLD** — useful UI, but unsigned and not operational with Codex in this test.

