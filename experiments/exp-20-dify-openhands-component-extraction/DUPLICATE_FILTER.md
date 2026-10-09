# EXP-20 CP-02 — Duplicate filter

Status: COMPLETE
Rule applied: **a component is not transferred because the upstream implemented it more
elegantly.** It is transferred only when it fills a gap that is *measurable against the
existing Murat implementation* — a number produced by running MPE's own production code as
the control arm. Everything else is `KEEP_EXISTING` or `REJECT`.

Every measurement quoted below comes from `evidence/cp03_p1_durable_event_evidence.json`,
`evidence/cp03_p2_failure_classification.json` and `evidence/proof_run.json`, produced by
`harness/exp20_proof.py`.

## 1. Duplicate register

| Upstream component | Duplicates which Murat mechanism | Why it is a duplicate | Decision |
|---|---|---|---|
| Dify `ModelInstance` / `provider_manager` / hosting configuration; OpenHands `sdk/llm` (litellm) + profiles + `switch_llm` | **Router** — Codex Router is the inference/protocol/credential gateway (`STATUS.md`, `route-profiles.md` with explicit slugs `gpt-5.6-sol`, `opencode-go/deepseek-v4-flash`, `opencode-go/kimi-k2.7-code`) | Both donors offer a provider abstraction whose whole job is choosing/credentialing a model. MPE already delegates that, and `STATUS.md` lists "Router authority change" and "adaptive routing" as boundaries in force | `KEEP_EXISTING` (adopting either = Router authority stop rule) |
| OpenHands `ConfirmationPolicyBase` / `SecurityRisk` / `SecurityAnalyzer` / LLM analyzer / ToolShield; Dify `human_input` HITL pause + resume | **MPE governance + existing approval/evidence model** — `triage_engine` → `earned_autonomy` (evidence-trust-gated ceiling, L4 owner-only) → `dispatch_autonomy` (most-restrictive, hard blocks) → `task_acceptance.accept_task` + the single `enforce_execution` point, fail-closed; `deep_change_check` gate ("detection cannot be overridden") | Same function, weaker or equal strictness: OpenHands' default state is `NeverConfirm()` (`state.py:123`) and its `ASK` hook decision is commented out as future work; Dify's HITL is authority *inside its own workflow engine*. MPE's path already blocks an integration-sensitive task at `HUMAN_REQUIRED` and never executes a hard-blocked task even with an approval flag (EXP-27 CP-05) | `KEEP_EXISTING`; donor mechanisms `REJECT` (moving approval authority out of MPE is forbidden) |
| Dify `output_failure_orchestrator` precedence table; OpenHands `fifo_lock` / `resource_lock_manager` / lease-like ownership | **MPE governance** — `dispatch_autonomy` composes ceilings with `min(...)`; `runtime_coordination._claim_event_writer` (`O_CREAT|O_EXCL`) + `find_worktree_collisions`; **Paperclip-derived** EXP-27 CP-03 single-host lease (already `ADAPT` / `ADOPT_IN_ORCHESTRATOR`) | The composition rule and the exclusivity primitive already exist and are already the subject of a closed recommendation | `KEEP_EXISTING` (only the *state-free decision shape* is borrowed, which is 8 lines inside P2) |
| OpenHands `StuckDetector` (5 non-progress patterns, 20-event window) | **Paperclip-derived** EXP-27 CP-05 bounded-stop guard (`max_retries`, `max_tool_calls`, `max_wall_seconds`, `compute_budget.hard_limit` → `budget_health`), already recommended `ADOPT_IN_MPE`; plus gate `retry_policy` and playbook `max_rework_cycles` | Overlapping function (stop a run that is not making progress) with a different trigger. MPE has no agent loop, no user/agent message alternation and no observation stream, so three of the five donor patterns have no host signal at all | `REJECT` for this checkpoint — recorded as reference-only so the EXP-27 guard, not a second detector, remains the single non-progress authority |
| OpenHands `RollingCondenser` / `LLMSummarizingCondenser`; Dify variable pool + system variables | **MPE governance + Paperclip-derived** — `context/CONTEXT_MAP.md` progressive disclosure, and the EXP-27 CP-02 ancestry packet whose value EXP-28 already measured (2,164.5 B packet vs 46,542.5 B no-packet scan, 95.35 % fewer bytes) | Context packaging is already a closed, measured recommendation. A condenser additionally spends model calls, which in MPE means Router + budget authority | `KEEP_EXISTING` / `REJECT` |
| OpenHands `EventLog` `parent_id` tree, branching, `View`, `path_to_root` | **MPE governance** — `docs/architecture/RUNTIME_COORDINATION_PATTERNS.md` puts "event-sourcing architecture" and "workflow engine" explicitly out of scope; `summarize_events` maps a *linear* log into existing Run Report concepts | Branching history is an event-sourcing feature MPE has deliberately not adopted | `REJECT` |
| Dify `core/repositories/{sqlalchemy,celery}_*`; OpenHands agent-server + Canvas backend registry/automations | **murat-ai-orchestrator** (the portfolio's orchestration host) + **MPE governance** (`STATUS.md`: no daemon, no scheduler, no persistent runtime agents, no orchestration state persistence) | A workflow DB, a Celery queue, a backend registry and schedule/webhook automations are exactly the parallel control plane the orchestrator exists to be — and `Murkin1980/Murat-AI-Orchestrator` is not readable from this session, so no gap in it can even be evidenced | `REJECT — DEEP_CHANGE_REQUIRED` |
| Dify plugin daemon + `ToolManager`; OpenHands `tool/registry.py` sealed catalog | **MPE governance** — `experts/` `capability_profile` + `preferred_route_profile`, `teams/`, `playbooks/`, `skills/` are the bounded capability model; **murat-ai-orchestrator** would be the only plausible tool-registry host | MPE invokes Experts and gates, not tools. A registry without a caller is an abstraction with no consumer (SCOPE-CHANGE-CONTROL §10) | `REJECT` for MPE (reference-only for the orchestrator) |
| Dify `core/rag/**` + `api/providers/vdb` (173 files); Dify `core/ops` trace providers + OTel | **MiniBase** (`minibase-cloudflare` is the portfolio data plane — EXP-25 `MINIBASE_FIT.md`: one project D1, logical collections, keyset pagination, `records:upsert-many` with `Idempotency-Key`) and the **existing approval/evidence model** (`evidence/**`, Run Report `deterministic_gate_results` + `evidence_ref` trust boundary in `validate_package.py`, `USAGE_RECORD`, dashboard) | A vector store / knowledge pipeline would be a second data plane beside MiniBase; an external tracing backend would be a second evidence model beside the trusted-`evidence_ref` rule that EXP-002 promoted into the validator | `REJECT` |
| Dify external code sandbox (`CODE_EXECUTION_ENDPOINT`) + SSRF proxy; OpenHands `BaseWorkspace` + `docker_runtime` | **MPE governance** — Codex/host is the execution authority; `enforce_execution` gates an injected callable and MPE runs no commands | Filling this "gap" means owning an executor: a persistent runtime plus a new security boundary | `REJECT — DEEP_CHANGE_REQUIRED` |
| OpenHands `secret_registry` + cipher, per-container credential manifest | **existing approval/evidence model** — `secrets_scan` gate; EXP-25 audits a 16-hex digest and never a raw key; this experiment redacts its own planted token instead of storing it | MPE persists no secrets, so there is nothing to encrypt | `KEEP_EXISTING` |
| OpenHands token/cost events, `LLMCompletionLogEvent`, laminar observability | **MPE governance** — `contracts/USAGE_RECORD.*`, `scripts/usage_from_router_log.py`, `scripts/usage_from_codex_rollout.py` (fail-closed when a rollout lacks a per-call breakdown), `usage_instrumentation.py`, three compute-budget gates | MPE already refuses to synthesize telemetry ("do not substitute synthetic telemetry", `STATUS.md` item 9); donor-style always-on token events would invite exactly that | `KEEP_EXISTING` |

## 2. What survived the filter, and the measured value

Only two components survived. Both were measured against MPE's own production functions run
in the same process, on the same fixtures.

### P1 — crash-tolerant, idempotent event evidence (OpenHands `EventLog` subset) → `BORROW`

| Measured against | Control arm (existing MPE production code) | Borrowed arm | Delta |
|---|---|---|---|
| Torn tail on a 5-event log (34 bytes cut mid-line) | `runtime_coordination.read_events` raises `ContractError: invalid JSONL line 5`; **0 of 5 events recoverable**; `summarize_events` impossible → 100 % evidence loss | 4 of 5 recovered, 1 explicit damage record (`torn_tail`, line 5, 214 bytes, `terminated: false`), `summarize_events` (production, unchanged) still returns a summary | **100 % → 20 % evidence loss**; the run stays resumable |
| Real committed MPE log (`exp-27/evidence/run-EXP27-CP04.events.jsonl`, 6 events) | 6 events, summary S | 6 events, summary **identical to S**, 0 damage | no behavioural change on a healthy log (no regression) |
| Duplicate `event_id` replay | `append_event` accepts it silently: 4 records for 3 unique ids, 1 duplicate record | identical replay → `DUPLICATE_REPLAYED`, 0 bytes written, log digest unchanged; different payload under the same id → `DuplicateEventConflict`, log digest unchanged | **1 → 0** duplicate evidence records |
| Fresh-process resume with only the damaged log | not possible (the reader raises before any summary exists) | isolated interpreter, `read_from_chat: false`, 0 rediscovery steps, correct `run_id`/`task_id`/lifecycle, `resumable: true`, packet identical to the in-process one | resume after a crash becomes possible at all |
| Overhead | median append 0.00094 s | median append 0.00106 s (ratio **1.124**), +1 empty sidecar file per log, +2 syscalls per append, 0 new dependencies | ~12 % on a micro-benchmark of a 25-append loop; 0 bytes of extra payload |

Not claimed: the length marker is **not** an integrity proof. It answers "did the log
advance?" with 0 parses instead of 4 for a 4-event log (measured), and a stale or absent marker yields
`MARKER_UNVERIFIED` / `MARKER_ABSENT`, never a silent `COMPLETE`. Under MPE's existing
single-writer claim its value is marginal, and it is recorded as borrow-secondary rather
than being sold as a win.

### P2 — deterministic failure classification onto the existing gate vocabulary (OpenHands + Dify) → `BORROW`

| Measured against | Control arm (existing MPE production code) | Borrowed arm | Delta |
|---|---|---|---|
| 14 real failure cases (real MPE exception classes, real `gate_id`s from `gates/registry.yaml`, real `run_task` path with the `tests/test_execution_runner.py` L4 + 5-verified-PASS fixture) | `execution_status` = `ERROR` for **all 14** — 1 distinct value; executor invoked exactly once per case; no kind, no retryability, no gate mapping | 8 distinct kinds → 4 distinct decisions (`RETRY`, `REWORK`, `BLOCKED`, `HUMAN_REQUIRED`), each anchored to the gate's own declared `failure_state` | **1 → 8** distinguishable outcomes; 8 cases get a bounded retry inside the gate's own policy instead of an undifferentiated error |
| Authority | — | `allowed_action`, `acceptance_state`, `executor_invoked`, `execution_allowed`, `human_gate_required`, `blocking_reasons`, `execution_status` identical in **14/14** cases; 0 cases downgraded below the declared gate state; 2 escalated (fail-closed `auth`, `internal`) | annotation only — measured, not asserted |
| Independent convergence with the registry | — | `compute_budget_health` (quota) and `deep_change_check` (unknown) land on `HUMAN_REQUIRED`, the state the registry already declares; 4/14 cases match the declared state exactly | the donor vocabulary reproduces MPE's own decisions where MPE already had them |
| Deep-change authority | `run_task(deep_change_task, executor, history=5 verified PASS, current_level="L4", stop_condition=True)` → `allowed_action=OBSERVE`, `acceptance_state=BLOCKED`, executor calls **0** | classifier adds `kind=unknown`, `decision=HUMAN_REQUIRED`, `retry_budget=0`, `classifier_granted_execution=false` | 0 executions granted by the new layer |
| Evidence hygiene | the production arm copies raw exception text into `execution_result`; the planted token `PLANTED-PROOF-TOKEN-not-a-real-credential-9f3c` appears in **1** case's production output | the classification carries `kind`/`retryable`/`executor_action` only: planted-token occurrences **0**, cases copying raw text **0** | a credential-looking string stops travelling with the evidence |
| Determinism / cost | — | 3 identical passes, order-independent, median classify 4.2 µs, 0 new dependencies, `gates/registry.yaml` parsed with 20/20 gates by a 25-line dependency-free reader | deterministic and free |

Second concrete consumer (why this is not a one-off abstraction): MebelFlow AI
`packages/ai-gateway/src/index.ts` (`4e16d8dd`) throws 7 string sentinels as generic
`Error` (`GATEWAY_BUSY:275`, `SESSION_REQUEST_IN_PROGRESS:277`, `SESSION_CALL_LIMIT:289,310`,
`TENANT_BUDGET_EXCEEDED:296`, `BUDGET_RESERVATION_MISSING:233`) and collapses a provider
HTTP failure into prose (`:121-122`), with **0** occurrences of the word "retry" in the
file. It has the same gap MPE's runner has, and the same closed-vocabulary fix applies
without touching its limits or its authority. No change was made to that repository.

## 3. Stop rules applied (`DEEP_CHANGE_REQUIRED`)

Each of these was **stopped, not implemented**, per the EXP-20 stop rules:

| Stop rule | Upstream components that hit it |
|---|---|
| new persistent runtime | OpenHands `BaseWorkspace` + agent-server + Canvas backend registry (O1, O2, O13) |
| shared workflow DB | Dify `sqlalchemy_workflow_execution_repository` / node execution repositories (D8) |
| Router authority change | Dify `ModelInstance`/`provider_manager`; OpenHands `sdk/llm` + profiles + `switch_llm` (D11, O11) |
| separate scheduler/queue | Dify Celery repositories; Canvas `automation-service` schedule/webhook (D8, O13) |
| new canonical source of truth | Dify workflow DB state; OpenHands `base_state.json` as the agent's truth; any external tracing/knowledge store (D8, D13, D14, O4) |
| generic DAG engine | `graphon==0.7.0` graph engine + variable pool + node set (D9) |

Additional independent rejection ground for D9: `graphon` publishes **no license
classifier** on PyPI, so its terms could not be verified in this session.

## 4. Full-platform adoption is not needed — the proof

* Two components, ~580 lines of experiment-scoped Python (`harness/durable_event_evidence.py`
  301, `harness/failure_classification.py` 280 — plus the 675-line runner and 40-line worker
  that only measure), **0** new dependencies, **0** services, **0** databases, **0** queues,
  **0** daemons, **0** sandboxes.
* Both proofs call the existing production functions (`read_events`, `summarize_events`,
  `append_event`, `validate_event`, `run_task`) instead of replacing them; the strict reader
  and the single enforcement point remain the defaults.
* `evidence/proof_run.json` records `production_files_changed: []` across 11 digested
  production/governance files, `persistent_runtime_created: false`,
  `database_or_queue_created: false`, `sandbox_or_executor_service_created: false`,
  `workflow_engine_created: false`.
* Rollback is deleting `experiments/exp-20-dify-openhands-component-extraction/harness` and
  `evidence`; nothing else in the repository references them.
