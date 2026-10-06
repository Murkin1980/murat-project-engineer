# EXP-27 CP-01 — Component map: donor patterns vs. existing MPE / Orchestrator mechanisms

Status: COMPLETE
Donor pin: `paperclipai/paperclip@d9f600043f13cf19172da1373d1336a0db31664b` (MIT) — see `UPSTREAM_AUDIT.md`.

Legend: **KEEP** = MPE already solves it, keep current mechanism; **BORROW** = pattern worth reproducing
inside an existing MPE component; **ADAPT** = reproduce with MPE-specific changes; **REJECT** = duplicate,
out of scope, or requires a parallel control plane.

Each row answers the CP-01 contract:
`Paperclip pattern → problem solved → existing MPE/orchestrator equivalent → overlap → incremental value →
required dependency/runtime → adoption risk → verdict`.

## Priority patterns

### P1 — Goal ancestry / context ownership — **BORROW**

| Field | Assessment |
|---|---|
| Problem solved | An executor must know *why* a task exists, and a resumed session must know which exact source text produced its brief. |
| Donor mechanism | `goals.parent_id`/`level` + `issues.goal_id`/`parent_id`; `paperclipTurnContext.assignment/events` with per-source `owner` + `revision = sha256(trimmed source)`; `objectiveSource` on compact continuation (`doc/plans/2026-09-21-task-context-ownership.md`). |
| Existing MPE equivalent | `context/CONTEXT_MAP.md` progressive disclosure; `AGENTS.md` required reading order; `experiments/EXPERIMENT_REGISTRY.json` (`why`, `experiment_path`, `next_action`); per-experiment `ARENA_TASK.md` / `README.md` checkpoint chain; typed Handoff (`contracts/HANDOFF.md`); Run Report `project`/`task`/`risk_tier`. |
| Overlap | High on intent (MPE already declares project → experiment → checkpoint → task in documents); zero on machine-readable compaction and on source-revision evidence. |
| Incremental value | (a) one compact packet an executor can be handed instead of scanning documents; (b) a digest per ancestry source, so the packet can state *which revision* of the goal text it used; (c) measured rediscovery drop (CP-02: 3 file reads / ≈44 KB → 1 file / ≈2.2 KB packet, 0 rediscovery steps). |
| Required dependency/runtime | None beyond Python stdlib and existing repository files. No store, no service. |
| Adoption risk | Low. Main risk is duplication: a packet must stay a *derived view* of the registry + experiment docs, never a second source of truth. |
| Verdict | **BORROW** → reproduce inside MPE experiment/task tooling; MPE keeps Git documents as source of truth. |

### P2 — Atomic task checkout / lease — **ADAPT**

| Field | Assessment |
|---|---|
| Problem solved | Two executors must never work the same task; a crashed owner must not deadlock the task forever; the winning/terminal state must be inspectable. |
| Donor mechanism | Durable exclusivity row keyed by a unique constraint (`execution_workspace_runtime_leases`, `owner_key`, `claimed_at`, `renewed_at`, `expires_at`), task `checkout_run_id`, `409 Conflict` on duplicate checkout, explicit *"never retry a 409"* rule, stale-owner adoption event `issue.checkout_lock_adopted`, and status-version guards. |
| Existing MPE equivalent | `scripts/runtime_coordination.py`: atomic mailbox delivery via `os.open(O_CREAT\|O_EXCL)` + `os.replace`, single-writer event-log claim (`_claim_event_writer`), lifecycle state machine (`CREATED…CANCELLED`) with `validate_transition`, `find_worktree_collisions`. |
| Overlap | Partially high: MPE already has the exclusive-create primitive, single-writer ownership, and terminal-state vocabulary, but **no task-level lease** with expiry/reclaim/release records. |
| Incremental value | A task-scoped lease that (a) reports the conflicting owner without retry, (b) bounds recovery by explicit expiry rather than "hope nobody else picks it up", and (c) keeps the released/terminal record visible instead of deleting it. CP-03 measured exactly one winner and zero duplicate executions across 3 × 8 concurrent processes. |
| Required dependency/runtime | File-backed proof uses stdlib only (one lock file + one record file). The donor version requires a Postgres unique constraint, which MPE will not add for this pattern. |
| Adoption risk | Medium-low: stale-lease handling and clock handling are easy to get wrong; a wrong reclaim window can hand a task to two owners. Must stay bounded, explicit, and single-host (MPE has no shared filesystem guarantee across executors today). |
| Verdict | **ADAPT** → if adopted, extend `scripts/runtime_coordination.py` in a separately authorized checkpoint with a single-host, file-backed lease; do not import a DB-backed checkout model. |

### P3 — Persistent resumable evidence — **KEEP + BORROW (verification only)**

| Field | Assessment |
|---|---|
| Problem solved | A different executor or process must resume without the original chat/session and without redoing finished work. |
| Donor mechanism | `heartbeat_runs` / `heartbeat_run_events` (event history), SHA-256 + `byteSize` + `idempotencyKey` artifact registration (`doc/AGENT-ARTIFACTS.md`), continuation re-render that preserves the current objective. |
| Existing MPE equivalent | Mandatory graceful-handoff fields (STATE, EVIDENCE, CHANGES, RESULT, BLOCKER, NEXT ACTION, HANDOFF) in `AGENTS.md` / `docs/GLOBAL_MPE_ENFORCEMENT.md`; typed Handoff contract `contracts/HANDOFF.md`; `contracts/RUN_REPORT.md`; `contracts/RUNTIME_EVENT.schema.json` event log + `summarize_events`; `evidence/**`. |
| Overlap | Very high on contract; the donor adds content digests and idempotency keys per artifact, and a run event stream that is used by watchdogs. |
| Incremental value | The MPE contract already carries the fields; what was missing is a *checked* completeness + no-re-execution assertion. CP-04 measured 21/21 handoff fields present, resume in a fresh isolated interpreter with 0 rediscovery steps and 0 re-executed steps, and a valid 6-event JSONL log. |
| Required dependency/runtime | None. |
| Adoption risk | Low, provided artifacts stay repository/evidence-linked and the digest never becomes an authorization signal (same rule the donor states for its `revision`). |
| Verdict | **KEEP** the existing handoff contract; **BORROW** only the habit of recording a digest + idempotency key per produced artifact and asserting evidence completeness at handoff time. |

### P4 — Budget / runaway guard — **ADAPT**

| Field | Assessment |
|---|---|
| Problem solved | Unbounded retries, tool calls, wall time, or spend must stop work with an explicit state instead of silently continuing. |
| Donor mechanism | `BudgetPolicy.warnPercent` warning → `hard_stop` at 100%; `budget_incidents` with `approvalId`; scope pause (agent/project/company); documented rule that a retry must not bypass an unresolved budget hold. |
| Existing MPE equivalent | `contracts/COMPUTE_BUDGET.md` (`hard_limit`, `budget_status: GREEN…RED`, `burn_rate_status`), `scripts/compute_budget.budget_health`, run-report budget summary, `gates/registry.yaml` `retry_policy` / failure states, playbook `max_rework_cycles`, EXP-13 pre-registered route checks. |
| Overlap | High on the *status vocabulary* (warn/hard/RED) and on cost accounting; low on an *enforced runtime boundary* — MPE defines statuses and retry policies but had no small deterministic guard that raises on the last permitted retry/tool call/wall time. |
| Incremental value | CP-05 measured four hard boundaries (max retries, max tool calls, max wall time, projected cost vs. `hard_limit`) each producing an explicit STOP/BLOCKED with counters, and the cost dimension mapped onto the existing canonical `budget_health` status (`RED` at/over `hard_limit`) instead of a new status vocabulary. |
| Required dependency/runtime | None (stdlib clock/counters; no new daemon, no token accounting service). Token/cost limits stay `estimated`/`unobserved` unless existing usage evidence exists. |
| Adoption risk | Low-medium: an enforced guard is only useful if the executor path actually routes through it; a guard that can be bypassed is worse than none because it creates false confidence. |
| Verdict | **ADAPT** → keep the MPE status vocabulary; add an enforced bounded-stop primitive only where a real executor path exists (no production change in this experiment). |

### P5 — Approval / governance gate — **REJECT (as a donor mechanism); existing MPE gate is reused**

| Field | Assessment |
|---|---|
| Problem solved | Governed or irreversible actions must require a recorded human approval before execution. |
| Donor mechanism | Approval objects for hires/strategy/spend/security + `request_confirmation` cards bound to a plan revision with idempotency keys + wake-on-resolution. |
| Existing MPE equivalent | `scripts/triage_engine.py` (risk tiers, `human_approval_required`, approval signals) → `scripts/earned_autonomy.py` (evidence-trust-gated levels, L4 owner-only) → `scripts/dispatch_autonomy.py` (most-restrictive ceiling, hard blocks) → `scripts/task_acceptance.py` (`accept_task`, single `enforce_execution` point, fail-closed); `gates/registry.yaml`; `docs/governance/SCOPE-CHANGE-CONTROL.md` §6 deep-change gate; evidence-trust boundary in `scripts/validate_package.py`. |
| Overlap | Complete for the MPE use case. Paperclip's gate is authority *inside its own control plane*; adopting it would move approval authority out of MPE, which the experiment forbids. |
| Incremental value | None that MPE does not already have — and MPE's version is stricter (fail-closed, earned-autonomy ceiling, deep-change owner gate, trusted-evidence requirement). |
| Required dependency/runtime | Would require the Paperclip server/DB (parallel control plane) to be the approval authority. |
| Adoption risk | High: replacing or duplicating the existing approval path would break the MPE source of truth and the deep-change boundary. |
| Verdict | **REJECT** the donor mechanism; keep and reuse the existing MPE approval path. CP-05 confirms it blocks an integration-sensitive task at `HUMAN_REQUIRED` without a recorded approval, never executes a hard-blocked task even with approval, and cannot be overridden by a satisfied budget guard. |

## Secondary / reference-only (not adopted, not scheduled)

| Donor mechanic | MPE position |
|---|---|
| Heartbeat + watchdog runs | Not adopted. MPE explicitly does not add 24/7 agent fleets or persistent runtime agents. |
| Routines / schedules | Not adopted; no scheduler or daemon is authorized. |
| Org chart / hired roles / permissions model | Reference only for future permission discussions; MPE has bounded Expert roles and teams. |
| Runtime adapter plugin model | Reference only; MPE runs executors inside approved checkpoints, not as a managed fleet. |
| Durable continuation scheduler | Reference only; MPE's graceful handoff covers the documented need. |

## Overlap that must stay rejected

- A Paperclip-shaped **orchestration service** (server + Postgres + UI) would be a parallel control plane and a
  second source of truth → **REJECT** (`docs/NEW_IDEA_FILTER_POLICY.md`, `docs/GLOBAL_MPE_ENFORCEMENT.md`).
- Migrating task/run/evidence state out of Git and `evidence/**` into any external store → **REJECT**.
- Importing Paperclip's budget, approval, or checkout authority into the MPE Router/orchestrator → **REJECT**.

## Landing targets (if a future owner authorizes adoption work)

1. `scripts/runtime_coordination.py` — the only plausible landing zone for the lease primitive (single-host, file-backed).
2. MPE contracts (`contracts/HANDOFF.md`, `contracts/COMPUTE_BUDGET.md`, `contracts/RUN_REPORT.md`) — pattern-level
   fields only (digest/idempotency key, explicit STOP outcome); no schema replacement.
3. `murat-ai-orchestrator` — only if that project independently needs budget/lease semantics; no cross-repo change
   is made or proposed by this experiment.
