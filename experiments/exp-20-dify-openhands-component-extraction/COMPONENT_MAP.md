# EXP-20 CP-01 — Component map: Dify / OpenHands components → existing Murat equivalents

Status: COMPLETE
Donor pins: see [`UPSTREAM_AUDIT.md`](UPSTREAM_AUDIT.md) §1.
Contract per row: `component → existing Murat equivalent → gap → disposition`.

Allowed dispositions (and nothing else): **`KEEP_EXISTING`** (Murat already has it — the
default when the function exists), **`BORROW`** (reuse the pattern/mechanism inside an
existing Murat component), **`ADAPT`** (reproduce the behaviour with Murat-specific
changes), **`REJECT`** (duplicate, no consumer, or requires a parallel platform).

Rows marked `DEEP_CHANGE_REQUIRED` are `REJECT` **and** stopped by the EXP-20 stop rules;
they are not implemented, not scheduled, and not proposed.

## 1. Summary table

### Dify (`langgenius/dify@b2ce9ac1`)

| # | Category | Dify component | Existing Murat equivalent | Gap | Disposition |
|---|---|---|---|---|---|
| D1 | tool execution | `ToolEngine.agent_invoke/_invoke` + `ToolInvokeMeta(time_cost, error, tool_config)` | `scripts/execution_runner.run_task` (single enforcement point) + `gates/registry.yaml` | no per-invocation structured record: every executor failure becomes one `execution_status="ERROR"` string | **ADAPT** (classification proven in CP-03 P2; the timing/meta half is not proven and is not proposed for production) |
| D2 | typed tool/provider abstraction | `ToolParameter` with closed `ToolParameterType` + `ToolParameterForm(schema/form/llm)` + `init_frontend_parameter`; `ToolProviderType` (7 provider kinds) | `contracts/*.schema.json`, `scripts/triage_engine.validate_task` (typed task contract), `skills/murat-project-engineer/references/route-profiles.md`; MebelFlow `packages/ai-gateway` uses zod `json_schema` structured output | MPE has **no tool registry and no tool callers**; there is no second concrete consumer, so a parameter-declaration layer would be an abstraction without a consumer (SCOPE-CHANGE-CONTROL §10) | **REJECT** for MPE (reference-only for a future gateway tool surface) |
| D3 | retries / error recovery | `api/core/tools/errors.py` — 10 typed failure classes | gate `failure_state` + `retry_policy` exist per gate, but nothing classifies a failure | a failure has no kind, no retryability, no bounded retry decision | **BORROW** (proven in CP-03 P2) |
| D4 | retries / error recovery | `output_failure_orchestrator.py` — state-free decision, retry budget, `_STRATEGY_TERMINAL_RANK` precedence | `scripts/dispatch_autonomy.py` already composes ceilings with `min(...)` (most restrictive wins) | composition already exists; only the *state-free* shape (caller owns the attempt counter) was missing | **KEEP_EXISTING** for composition; **BORROW** the state-free decision shape (used by P2 `decide()`) |
| D5 | retries / error recovery | per-node `retry_config` / `error_strategy` (in `graphon`) | `gates/registry.yaml.retry_policy` prose; playbook `max_rework_cycles` | the prose budget is not machine-readable | **ADAPT** (P2 derives a bounded budget from the registry's own text with an explicit auditable rule table; the registry is not edited) |
| D6 | human approval | `human_input_policy.py`, `nodes/human_input/{pause_reason,session_binding,boundary,callback}.py`, `agent_v2/ask_human_{hitl,resume}.py`, `repositories/human_input_repository.py` | `HUMAN_REQUIRED` / `BLOCKED` / `WAITING` in `runtime_coordination.STATES`; `task_acceptance.accept_task`; graceful-handoff `BLOCKER` + `NEXT ACTION`; EXP-27 CP-04 proved resume from the persisted handoff | none that is measurable: MPE already pauses, records the blocker, and resumes without rediscovery. Dify's typed pause reason is the same idea as P2's closed kind vocabulary and is covered there | **KEEP_EXISTING** |
| D7 | sandbox / executor isolation | `core/helper/code_executor/code_executor.py` → external sandbox service (`CODE_EXECUTION_ENDPOINT`) + `ssrf_proxy.py` | Codex/host is the execution authority (`STATUS.md`); MPE executes nothing | adopting it means an external execution service and a new security boundary | **REJECT — `DEEP_CHANGE_REQUIRED`** (new infrastructure platform; materially changes security boundaries) |
| D8 | task/session state | `core/repositories/{sqlalchemy,celery}_workflow_execution_repository.py` | Git + `evidence/**` + `contracts/RUN_REPORT.*`; `.mpe-runtime/` ephemeral JSONL | none worth paying for: a shared workflow DB would become a second source of truth | **REJECT — `DEEP_CHANGE_REQUIRED`** (shared workflow DB + queue) |
| D9 | workflow representation | external `graphon==0.7.0` graph engine (`GraphEngine`, `VariablePool`, node set, `error_strategy`) | playbooks (`playbooks/*.md`) + `gates/registry.yaml` + typed handoffs; MPE explicitly has no DAG runtime | none that MPE is allowed to fill | **REJECT — `DEEP_CHANGE_REQUIRED`** (generic DAG engine; plus unverified `graphon` license) |
| D10 | plugin/tool registry | plugin daemon client (`core/plugin/impl/*`, 13 modules) + `ToolManager` | `experts/`, `teams/`, `playbooks/`, `skills/` are the bounded capability model | none; a plugin daemon is an out-of-process platform | **REJECT — `DEEP_CHANGE_REQUIRED`** (new infrastructure platform / parallel control plane) |
| D11 | model/provider abstraction | `ModelInstance` / `QuotaManagedModelInstance`, `provider_manager.py`, `hosting_configuration.py` | **Codex Router is the inference/protocol/credential gateway** (`STATUS.md`); `route-profiles.md` names the explicit slugs | none; replacing or wrapping the Router is an authority change | **KEEP_EXISTING** (any change = Router authority stop rule) |
| D12 | context packaging | variable pool / system-environment-conversation variable prefixes | `context/CONTEXT_MAP.md` progressive disclosure; EXP-27 CP-02 ancestry packet (measured 2,164.5 B vs 46,542.5 B in EXP-28) | none measured; a variable pool presumes a DAG runtime | **KEEP_EXISTING** |
| D13 | observability | trace-provider registry (`core/ops/unified_trace/*`), OTel extensions, 84 provider-trace files, external backends | `evidence/**`, Run Report `deterministic_gate_results`, `USAGE_RECORD`, dashboard; EXP-002 evidence-trust boundary in `validate_package.py` | none that justifies an external tracing SaaS; MPE's model is *trusted evidence refs*, not spans | **REJECT** (duplicate evidence model + external service) |
| D14 | RAG / knowledge ingestion | `core/rag/**` (104 files), `services/knowledge/**`, `api/providers/vdb` (173 files) | none in MPE; MiniBase is the portfolio data plane (EXP-25); `business-discovery` not readable from this session | no current measurable need inside MPE and no consumer identified in this session | **REJECT** (no consumer; would duplicate a MiniBase-backed retrieval if one is ever needed) |

### OpenHands (`OpenHands/OpenHands@937d0d6a` + `software-agent-sdk@33044182`)

| # | Category | OpenHands component | Existing Murat equivalent | Gap | Disposition |
|---|---|---|---|---|---|
| O1 | sandbox / executor isolation | `BaseWorkspace` (`execute_command`, `file_upload/download`, `git_changes/diff`, `pause/resume`) with local + remote(httpx) implementations | none — Codex/host executes; MPE `enforce_execution` gates an *injected callable*, it does not run commands | real, but filling it means owning an executor | **REJECT — `DEEP_CHANGE_REQUIRED`** (persistent agent runtime; new security boundary) |
| O2 | sandbox / executor isolation | `agent_server/docker_runtime/*` (per-conversation containers, owner label, encrypted credential manifest), `runtime_router.py` | none | same as O1 plus Docker provisioning and secret storage | **REJECT — `DEEP_CHANGE_REQUIRED`** |
| O3 | task/session state (durability) | `EventLog`: one file per event `event-{idx:05d}-{event_id}.json`, `.eventlog-len-{n}.marker` advanced delete-first, `flock` + 30 s timeout, duplicate-id `ValueError`, `_scan_and_build_index` refusing a non-contiguous index, stale-index rebuild | `scripts/runtime_coordination.append_event/read_events/summarize_events` — one JSONL, explicit single-writer claim, fsync, strict validation | **measured**: a torn tail makes the production reader raise and loses *all* events (0/5 recovered, `invalid JSONL line 5`); duplicate `event_id`s are appended silently (4 records for 3 ids) | **BORROW** (crash-tolerant recovery + idempotent append, proven in CP-03 P1). The length marker is **BORROW-secondary**: measured value is small under MPE's existing single-writer claim (0 parses vs 4 for a 4-event log) and it never proves integrity — see `DUPLICATE_FILTER.md` §4 |
| O4 | task/session state (resume) | `ConversationState`/`base_state.json`, create-or-resume, tool-spec and client-tool recovery, `render_resume_transcript` | graceful-handoff contract (`AGENTS.md`), `contracts/HANDOFF.md`, `contracts/AGENT_RUNTIME_STATE.schema.json`, `RUNTIME_EVENT.schema.json` + `summarize_events`; EXP-27 CP-04 already proved fresh-process resume with 0 rediscovery steps and 21/21 handoff fields | none on the contract; only the durability gap in O3 | **KEEP_EXISTING** (contract) + the narrow **BORROW** in O3; transcript re-rendering **REJECT** (needs LLM context management → Router/cost) |
| O5 | human approval | `SecurityRisk` + `ConfirmationPolicyBase` (`AlwaysConfirm`/`NeverConfirm`/`ConfirmRisky(confirm_unknown=True)`), `SecurityAnalyzer`/LLM analyzer/ToolShield, `agent.py:1165` | `triage_engine` → `earned_autonomy` (evidence-trust-gated ceiling, L4 owner-only) → `dispatch_autonomy` (most-restrictive, hard blocks) → `task_acceptance.accept_task` + single `enforce_execution`, fail-closed; `deep_change_check` gate | none — MPE's version is stricter and already fail-closed on unknown; donor default is `NeverConfirm()` | **KEEP_EXISTING** (donor mechanism **REJECT**: it would move approval authority out of MPE) |
| O6 | human approval | `hooks/*` — PreToolUse/PostToolUse/SessionStart/Stop external scripts returning allow/deny | `gates/registry.yaml` deterministic gates + `enforce_execution` single enforcement point | none; external hook scripts would put arbitrary code around the gate | **KEEP_EXISTING**; hook mechanism **REJECT** (security-boundary change) |
| O7 | retries / error recovery | `StuckDetector` — 5 non-progress patterns, 20-event window, thresholds, scans only after the last user message | gate `retry_policy` prose; EXP-27 CP-05 already prototyped bounded-stop guards (retries / tool calls / wall time / budget) and recommended `ADOPT_IN_MPE` in a future authorized checkpoint | partially covered by the EXP-27 recommendation; MPE has no agent loop to detect monologue/alternating patterns in | **REJECT** for this checkpoint (overlap with the EXP-27 P4 bounded-stop guard; no second consumer; would be a parallel non-progress authority). Recorded as reference-only |
| O8 | retries / error recovery | `event/error_classification.py` — closed `FailureKind`, `retryable`, `user_action`, frozen `extra="forbid"`, authoritative-class-first ordering, **detail never copied into evidence** | nothing: `run_task` returns `execution_status="ERROR"` + raw exception text; MebelFlow `ai-gateway` throws 7 string sentinels (`GATEWAY_BUSY`, `SESSION_CALL_LIMIT`, `TENANT_BUDGET_EXCEEDED`, …) as generic `Error` and has **0** occurrences of "retry" | **measured**: 14 distinct real failures → 1 undifferentiated production status; the planted token inside one exception message is copied into the production `execution_result` | **BORROW** (proven in CP-03 P2; second concrete consumer identified in MebelFlow AI) |
| O9 | context packaging | `RollingCondenser` / `LLMSummarizingCondenser` (`max_size=240`, `keep_first=2`, validated invariant), pipeline condenser | `context/CONTEXT_MAP.md`, EXP-27 CP-02 ancestry packet (measured in EXP-28) | none measured; condensation spends model calls | **KEEP_EXISTING** (condenser **REJECT**: LLM-in-MPE = Router authority + cost) |
| O10 | task/session state | event tree with `parent_id`, branching, `path_to_root`, `View` | linear append-only JSONL + `summarize_events` | none wanted: `RUNTIME_COORDINATION_PATTERNS.md` puts event-sourcing architecture explicitly out of scope | **REJECT** |
| O11 | model/provider abstraction | `sdk/llm/**` (litellm), profiles, `switch_llm` / `classify_and_switch_llm` tools | Codex Router | none | **KEEP_EXISTING** |
| O12 | plugin/tool registry | `tool/registry.py` — resolver registry, sealed catalog, `ToolCatalogEntry(usable, user_selectable, in_default_set)`, JSON-Schema action/observation, per-action `security_risk` | `experts/` `capability_profile` + `preferred_route_profile`, `teams/`, `playbooks/`, `skills/`; no tool runtime | none inside MPE; the plausible host (`murat-ai-orchestrator`) is **not readable from this session**, so no gap can be evidenced | **REJECT** for MPE (no consumer); reference-only for the orchestrator if its owner ever asks |
| O13 | workflow representation | Canvas `backend-registry/*` (health, active backend, url selection) + `automation-service` (schedule/webhook) | `route-profiles.md`, Router, `STATUS.md` boundaries (no daemon/scheduler) | none allowed | **REJECT — `DEEP_CHANGE_REQUIRED`** (separate scheduler/queue; parallel control plane) |
| O14 | observability | token/cost/`LLMCompletionLogEvent` as events in the same durable log; `observability/laminar`; agent-server telemetry | `contracts/USAGE_RECORD.*`, `scripts/usage_from_router_log.py`, `scripts/usage_from_codex_rollout.py` (fail-closed), `usage_instrumentation.py`, compute-budget gates | none: MPE already fails closed rather than synthesize telemetry | **KEEP_EXISTING** |
| O15 | retries / error recovery (concurrency) | `fifo_lock.py`, `resource_lock_manager.py`, `cancellation.py`, `parallel_executor.py` | `runtime_coordination._claim_event_writer` (`O_CREAT|O_EXCL`), `find_worktree_collisions`, lifecycle `validate_transition`; EXP-27 CP-03 lease (recommended `ADOPT_IN_ORCHESTRATOR`) | none beyond the EXP-27 lease recommendation | **KEEP_EXISTING** |
| O16 | secret handling | `conversation/secret_registry.py` + cipher for persisted secrets; per-container credential manifest | `secrets_scan` gate; MPE evidence stores no secrets (EXP-25 audits a 16-hex digest, never a raw key) | none — MPE persists no secrets to protect | **KEEP_EXISTING** |
| O17 | sandbox resume control | Canvas `cloud-sandbox-resume-suppression.ts` (suppress one auto-resume per conversation id) | n/a — no cloud sandbox | none | **REJECT** |

## 2. Special-interest verdicts (the two the task asked to prioritize)

### 2.1 OpenHands sandbox/executor boundary and resumable execution

* **Sandbox/executor boundary → `REJECT` / `DEEP_CHANGE_REQUIRED`.** The boundary is real and
  well built (one abstract workspace, local + remote implementations, Docker provisioning
  with an owner label). MPE has no executor at all: `STATUS.md` keeps Codex as the execution
  authority, and `enforce_execution` only gates an injected callable. Hosting a workspace
  boundary would require a persistent runtime and a new security boundary — two explicit stop
  rules. It was **not forced**, per the task instruction.
* **Resumable execution → `KEEP_EXISTING` + one narrow `BORROW`.** MPE already has the resume
  contract (graceful handoff, `AGENT_RUNTIME_STATE`, `RUNTIME_EVENT`, EXP-27 CP-04 fresh-process
  resume with 0 rediscovery steps). The only measurable gap is *durability granularity*: MPE's
  strict reader is all-or-nothing, so one torn line destroys the whole run's evidence, and a
  duplicate `event_id` is appended silently. That narrow slice is P1.

### 2.2 Dify typed tool/provider abstraction or workflow representation

* **Workflow representation → `REJECT` / `DEEP_CHANGE_REQUIRED`.** It is no longer Dify code:
  the graph engine, variable pool and node set are the external `graphon==0.7.0` package
  (`api/pyproject.toml:48`), whose PyPI metadata carries **no license classifier**. Adopting it
  would mean a generic DAG engine + a new dependency with unverified terms — three stop rules at
  once.
* **Typed tool/provider abstraction → `REJECT` for MPE.** `ToolParameter` with
  `form = schema | form | llm` is a genuinely good idea, and MPE has nothing like a tool
  registry to hang it on; the provider half belongs to the Codex Router, whose authority may not
  change. No second concrete consumer exists inside MPE, so building it would violate
  SCOPE-CHANGE-CONTROL §10. It stays reference-only for a future gateway tool surface.
* **What Dify actually contributes → `BORROW` (D3/D4/D5).** Its typed failure classes, its
  state-free decision orchestrator and its most-restrictive precedence converge with OpenHands'
  `error_classification.py` on the same mechanism. Two independent upstreams agreeing on one
  pattern that MPE demonstrably lacks is the strongest signal in this audit, and it is what P2
  proves.

## 3. Where a borrowed component would land (no landing was performed)

| Component | Landing target | Change size if ever authorized |
|---|---|---|
| P1 crash-tolerant recovery + idempotent append | `scripts/runtime_coordination.py` (additive functions beside `read_events`/`append_event`; the strict reader stays the default) | ~60 lines, stdlib only, no contract/schema change; the `event_log_valid` gate keeps its declared `failure_state` |
| P2 failure classification → gate `failure_state` | `scripts/execution_runner.py` (annotation on the returned outcome) reading `gates/registry.yaml` | ~120 lines, stdlib only, no new gate, no new status vocabulary, no authority change |
| P2 (portfolio reuse) | MebelFlow AI `packages/ai-gateway/src/index.ts` — classify its 7 existing string sentinels instead of throwing generic `Error` | not performed here; another repository, another owner decision |

No production file was modified by this experiment (`evidence/proof_run.json →
production_files_changed: []`, 11 digests compared before/after).
