# EXP-20 Phase 0 + CP-01 — Upstream audit: Dify and OpenHands

Status: COMPLETE
Run date: 2026-10-09 (UTC)
Method: read-only source audit. Nothing was installed, deployed, vendored, or executed
from either upstream. No new repository, service, database, queue, sandbox, or runtime.

## 1. Pins

| Upstream | Pin | Commit date | Nearest release | License | Read from |
|---|---|---|---|---|---|
| Dify | `langgenius/dify@b2ce9ac10000cbf3d6bd37e5a11234762e0b6d95` (`main`) | 2026-10-09T03:33:39Z | `1.17.1` (2026-09-10) | **Dify Open Source License** — modified Apache 2.0 + 2 extra conditions; GitHub reports `NOASSERTION` | `api/**` sparse checkout |
| OpenHands (source named in `README.md`) | `OpenHands/OpenHands@937d0d6aa201d8ac31cac514e0dc64ce5c434004` (`main`) | 2026-10-09T02:40:30Z | `v1.26.0` (2026-10-08), npm `@openhands/agent-canvas` 1.26.0 | MIT | full tree |
| OpenHands agent SDK (secondary pin, required — see §2) | `OpenHands/software-agent-sdk@33044182505244749928644a4643368a9e998ee7` (`main`) | 2026-10-09T02:35:02Z | — | MIT | `openhands-sdk/**`, `openhands-tools/**`, `openhands-agent-server/**` |
| Dify workflow engine (dependency, not vendored) | `graphon==0.7.0` (`api/pyproject.toml:48`), upstream `langgenius/graphon`, PyPI latest `0.8.0` | — | — | **no license classifier on PyPI** → unverified | PyPI metadata only |

Murat hosts inspected in the same session (read-only):

| Host | Pin | Accessible | Used for |
|---|---|---|---|
| `Murkin1980/murat-project-engineer` | `21ad8ba2` (this branch base) | yes | primary host; all production functions used as the control arm |
| `Murkin1980/mebelflow-ai` | `4e16d8dd2e7f83e444ffa85b5743b9a1462d10b3` (2026-09-22) | yes (public) | existing AI gateway surface (`packages/ai-gateway/src/index.ts`, 338 lines) |
| `Murkin1980/minibase-cloudflare` | `9ab38d83…` as pinned by EXP-25 `MINIBASE_FIT.md` | yes (public) | MiniBase facts reused from the EXP-25 audit; not re-cloned |
| `Murkin1980/Murat-AI-Orchestrator` | — | **no** — `403 Resource not accessible by integration` | no architecture claim is made about it in this experiment |
| `Murkin1980/business-discovery` | — | **no** — `403 Resource not accessible by integration` | no architecture claim is made about it in this experiment |

## 2. Structural finding that changes the audit

Both upstreams moved since the EXP-20 `README.md` was written (2026-10-02). Auditing the
names in that file without this correction would have produced a fictional map:

1. **`OpenHands/OpenHands` is no longer the Python coding agent.** At the pin it is *Agent
   Canvas*: a TypeScript/React-Router + Electron "self-hosted developer control center"
   (`package.json` name `@openhands/agent-canvas`, 1094 `.ts` + 1059 `.tsx` files, 10
   incidental `.py` files). The agent loop, sandbox/workspace boundary, event store,
   confirmation policy and failure classification live in the separate
   `OpenHands/software-agent-sdk` repository (`openhands-sdk`, `openhands-tools`,
   `openhands-agent-server`). The "sandbox/executor boundary and resumable execution"
   item in the EXP-20 task therefore had to be audited in the SDK pin, and the Canvas pin
   was audited for what it actually contributes: a *backend registry* and control-plane
   services (`src/api/backend-registry/*`, `src/api/runtime-service/`,
   `src/api/conversation-service/`, `src/api/event-service/`, `src/api/workspaces-service/`,
   `src/api/tool-catalog-service/`, `src/api/cloud/sandbox-service.api.ts`).
2. **Dify's workflow engine is no longer in `api/core/workflow`.** The graph engine,
   variable pool, and the generic node set (`llm`, `code`, `tool`, `if_else`, `iteration`,
   `answer`, …) were extracted into the external package `graphon` (`api/pyproject.toml:48`;
   imports such as `from graphon.graph_engine import GraphEngine, GraphEngineConfig` and
   `from graphon.runtime import VariablePool` in `api/tests/unit_tests/core/workflow/*`).
   `api/core/workflow` at the pin keeps only Dify-specific nodes (`agent`, `agent_v2`,
   `human_input`, `knowledge_*`, `trigger_*`) plus the entry/adapter layer
   (`workflow_entry.py`, `node_factory.py`, `human_input_policy.py`). The "workflow
   representation" item in the EXP-20 task is therefore an audit of a **third-party generic
   DAG dependency**, not of code inside Dify.

## 3. Phase 0 — what was read in this repository before any change

| Source | What it constrained |
|---|---|
| `AGENTS.md` | mandatory reading order, human-value rules, graceful-handoff contract (STATE/EVIDENCE/CHANGES/RESULT/BLOCKER/NEXT ACTION/HANDOFF), chat-handoff format |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | smallest sufficient change; reuse before building (§7); no abstraction without a real consumer (§10); no parallel systems (§19); deep-change gate (§6); change-size thresholds (§21) |
| `STATUS.md` | "Boundaries still in force": no daemon/scheduler, no generic workflow engine/DAG runtime, no persistent runtime agents, no Router orchestration; Codex stays the execution authority, Codex Router stays the inference/protocol/credential gateway |
| `docs/NEW_IDEA_FILTER_POLICY.md` | disposition vocabulary; `NEW_REPOSITORY` is the exception; duplication is a rejection reason |
| `experiments/exp-20-…/README.md` | EXP-20 disposition `REUSE_COMPONENT`, candidate list, acceptance criteria (incl. license check), constraints |
| `docs/architecture/RUNTIME_COORDINATION_PATTERNS.md` + `Munder Dufflin/CODEX_MPE_RUNTIME_PATTERNS_EXTENSION_RUN11.md` | the Run-11 bounded runtime patterns: mailbox transport, 7-event JSONL vocabulary, single-writer claim, ephemeral lifecycle metadata, and the explicit "out of scope" list |
| `contracts/RUNTIME_EVENT.schema.json`, `contracts/AGENT_RUNTIME_STATE.schema.json`, `contracts/HANDOFF.md`, `contracts/RUN_REPORT.md`, `contracts/COMPUTE_BUDGET.md` | existing typed evidence contracts the proofs must not replace |
| `gates/registry.yaml` | 20 deterministic gates with declared `failure_state` + `retry_policy` (the authoritative vocabulary used by proof P2) |
| `scripts/runtime_coordination.py`, `scripts/execution_runner.py`, `scripts/task_acceptance.py`, `scripts/dispatch_autonomy.py`, `scripts/earned_autonomy.py`, `scripts/triage_engine.py`, `scripts/validate_package.py` | the existing production surface used as the control arm |
| EXP-25 (`COMPONENT_MAP.md`, `MINIBASE_FIT.md`, `RESULTS.md`) | MiniBase facts, the donor-audit method, and the "one object → one identity" rule |
| EXP-27 (`UPSTREAM_AUDIT.md`, `COMPONENT_MAP.md`, `RESULTS.md`, `evidence/*`) | Paperclip-derived patterns already adopted/recommended: goal-ancestry packet, single-host lease, resumable handoff evidence, bounded-stop budget guard, rejection of donor approval authority |
| EXP-28 (`RESULTS.md`) | the measured value of the EXP-27 ancestry packet (2,164.5 B vs 46,542.5 B) — used in CP-02 to reject duplicate context-packaging work |

**EXP-11 does not exist.** The registry has no `EXP-11` entry and there is no
`experiments/exp-11*` directory. The material the task refers to is Stage-2 **Run 11**
(bounded runtime-coordination patterns), which produced
`docs/architecture/RUNTIME_COORDINATION_PATTERNS.md`, the three runtime contracts
(`MAILBOX_ENVELOPE`, `RUNTIME_EVENT`, `AGENT_RUNTIME_STATE`) and
`scripts/runtime_coordination.py`. That is what was audited. The discrepancy is recorded
rather than silently repaired.

## 4. Dify — audited mechanisms (pin `b2ce9ac1`)

| Category | Where it lives | What it actually does |
|---|---|---|
| Tool execution | `api/core/tools/__base/tool.py`, `api/core/tools/tool_engine.py` | `ToolEngine.agent_invoke/_invoke` wraps one tool call, times it, and returns `(response, files, ToolInvokeMeta)`; `ToolInvokeMeta` carries `time_cost`, `error`, `tool_config` (`entities/tool_entities.py:492`) so a failed call still produces a structured record instead of a bare exception |
| Typed tool/provider abstraction | `api/core/tools/entities/tool_entities.py` | `ToolProviderType` (`:65`) = plugin / builtin / workflow / api / app / dataset-retrieval / mcp; `ToolParameter` (`:294`) with a closed `ToolParameterType`, `multiple`, `options`, `input_schema`, and a **`ToolParameterForm` of `schema` / `form` / `llm`** (`:330`) — i.e. the declaration states *who supplies the value*; `init_frontend_parameter` normalizes/validates a value against that declaration |
| Tool error taxonomy | `api/core/tools/errors.py` | 10 typed classes: provider-not-found, tool-not-found, parameter-validation, provider-credential-validation, not-supported, invoke, api-schema, SSRF, credential-policy-violation, plus `ToolEngineInvokeError(meta)` |
| Retries / error recovery | `api/core/workflow/nodes/agent_v2/output_failure_orchestrator.py` | explicitly **state-free** decision engine: `OutputFailureDecision` = retry / use_default / fail_node / take_fail_branch; retry budget is the max across failed outputs (`:108`); competing strategies merge through `_STRATEGY_TERMINAL_RANK` (`:77`) — most restrictive wins. Node-level `error_strategy` / `retry_config` live in `graphon` |
| Human approval (HITL) | `api/core/workflow/human_input_policy.py`, `nodes/human_input/{boundary,callback,entities,enums,pause_reason,session_binding}.py`, `nodes/agent_v2/{ask_human_hitl,ask_human_resume}.py`, `api/core/repositories/human_input_repository.py` | a run **pauses** with a typed reason (`pause_reason.py`: `HumanInputRequired` carrying `form_id`, `inputs`, `actions`, `node_id`, resolved defaults, unioned with `SchedulingPause`), binds the pause to a session, persists a form, and resumes through a separate resume path. A workflow containing human-input nodes cannot be published as a workflow tool (`errors.py: WorkflowToolHumanInputNotSupportedError`) |
| Sandbox / executor isolation | `api/core/helper/code_executor/code_executor.py`, `api/core/helper/ssrf_proxy.py` | code nodes are **not** executed in-process: they are POSTed to an external sandbox service (`dify_config.CODE_EXECUTION_ENDPOINT`) over a pooled `httpx` client, with an SSRF proxy for outbound fetches |
| Task/session state | `api/core/repositories/{sqlalchemy,celery}_workflow_execution_repository.py`, `…_node_execution_repository.py` | workflow/node execution state is persisted through SQLAlchemy repositories and Celery task queues |
| Context packaging | `api/core/workflow/{system_variables,variable_pool_initializer,variable_prefixes}.py`, `api/core/model_context.py` | variable pool + system/environment/conversation variable prefixes (implementation in `graphon.runtime.VariablePool`) |
| Observability | `api/core/ops/{ops_trace_manager,base_trace_instance}.py`, `api/core/ops/unified_trace/{registry,provider,hierarchy,parent_context,trace_builder}.py`, `api/extensions/otel/**`, `api/providers/trace/**` (84 files) | a trace-provider registry with external backends (Langfuse/LangSmith-style) plus OpenTelemetry extensions; per-tool `time_cost`/`error` meta |
| Model/provider abstraction | `api/core/model_manager.py`, `api/core/provider_manager.py`, `api/core/hosting_configuration.py`, `api/core/plugin/impl/model_runtime*.py` | `ModelInstance` / `QuotaManagedModelInstance`; provider credentials and model runtime calls are delegated to the plugin daemon |
| Workflow representation | external `graphon==0.7.0` (`api/pyproject.toml:48`); `api/core/workflow/{workflow_entry,node_factory,graph_topology}.py` | graph engine, node types, edges, variable pool and error strategy are a **separate generic graph-execution library**; Dify keeps a node factory and adapters |
| Plugin/tool registry | `api/core/plugin/{plugin_service,provider_identity}.py`, `api/core/plugin/impl/*` (13 modules), `api/core/tools/tool_manager.py` | plugins (tools, models, agent strategies, datasources, endpoints, triggers) are resolved through an out-of-process **plugin daemon** client; `ToolManager` is the in-process registry over builtin/api/workflow/mcp/plugin providers |

## 5. OpenHands — audited mechanisms

### 5.1 Agent Canvas (`OpenHands/OpenHands@937d0d6a`)

| Category | Where it lives | What it actually does |
|---|---|---|
| Executor/backend selection | `src/api/backend-registry/{storage,active-store,health-store,health-storage,url-selection,auth,default-backend,types}.ts` | a registry of agent backends (local, remote, cloud) with persisted health and an active-backend selection; switching backends does not lose the conversation |
| Runtime/session control | `src/api/runtime-service/agent-server-runtime-service.ts`, `src/api/conversation-service/*`, `src/api/event-service/*`, `src/api/workspaces-service/*` | runtime + conversation + event + workspace services in front of an agent server |
| Sandbox | `src/api/cloud/sandbox-service.api.ts`, `src/api/cloud/sandbox-service.types.ts`, `src/api/cloud/cloud-sandbox-resume-suppression.ts` | cloud sandbox lifecycle; auto-resume can be explicitly suppressed per conversation id (an in-memory set, consumed once) |
| Tool catalog | `src/api/tool-catalog-service/*`, `src/api/mcp-service/*`, `src/api/mcp-health/*` | a catalog of tools offered to clients, plus MCP server health |
| Automations | `src/api/automation-service/*`, `docs/ACP_AGENTS.md` | scheduled/webhook automations that drive ACP-compatible agents (OpenHands, Claude Code, Codex, Gemini) |

### 5.2 Agent SDK (`software-agent-sdk@33044182`)

| Category | Where it lives | What it actually does |
|---|---|---|
| Sandbox / executor boundary | `openhands/sdk/workspace/base.py` (`BaseWorkspace`), `workspace/local.py`, `workspace/remote/base.py` (999 lines), `workspace/repo.py`, `workspace/models.py` | one abstract executor boundary — `execute_command`, `file_upload`, `file_download`, `git_changes`, `git_diff`, plus `pause()` / `resume()` (`base.py:262-273`) — with a local implementation (shared shell utility, `timeout: float = 30.0`, `CommandResult.timeout_occurred`) and a remote implementation over `httpx` with explicit connect/read/write/pool timeouts. Tools are written against the boundary, not against a machine |
| Sandbox provisioning | `openhands-agent-server/openhands/agent_server/docker_runtime/{provisioning,registry,proxy,storage,mediation,routers}.py`, `runtime_router.py` | per-conversation **Docker** containers, an owner label (`ai.openhands.runtime-owner`), an encrypted credential manifest per container, and a runtime router |
| Task/session state | `openhands/sdk/conversation/state.py` (776 lines), `conversation/base.py`, `conversation/persistence_const.py` | `ConversationState` persists `base_state.json`: agent, workspace, `max_iterations`, `stuck_detection`, `execution_status` (`ConversationExecutionStatus.is_terminal()`), `confirmation_policy`, `security_analyzer`, `blocked_actions` / `blocked_messages`, `last_user_message_id`, `leaf_event_id`, `stats`, `secret_registry`, `tags`, `agent_state`, `hook_config` |
| Durable event log | `openhands/sdk/conversation/event_store.py` (374 lines), `openhands/sdk/io/local.py` | one JSON file per event named `event-{idx:05d}-{event_id}.json` (index readable without parsing the payload); `flock`-based lock with a 30 s timeout and a documented NFS caveat; a length-marker sidecar `.eventlog-len-{length}.marker` advanced **delete-first** so an interrupted update leaves no marker and forces a recount; duplicate event id → `ValueError`; `_scan_and_build_index` resume that refuses a non-contiguous index; stale in-memory index → rebuild from disk and retry once; `parent_id` event tree with legacy linear fallback and cycle detection |
| Resumable execution | `openhands/sdk/event/resume_transcript.py`, `conversation/impl/local_conversation.py:329-410` | create-or-resume from `base_state.json`; on resume the agent, its tool specs and client tools are recovered from persisted state; `render_resume_transcript` re-renders the durable events into a bounded transcript (head/tail truncation helpers) for the next session |
| Human approval | `openhands/sdk/security/{risk,confirmation_policy,analyzer,llm_analyzer,toolshield_*}.py`, `agent/agent.py:1165` | `SecurityRisk` LOW/MEDIUM/HIGH/UNKNOWN with `is_riskier`; policies `AlwaysConfirm` / `NeverConfirm` / `ConfirmRisky(threshold, confirm_unknown=True)`; the agent asks for confirmation when **any** action risk in the step satisfies the policy; default state is `NeverConfirm()` (`state.py:123`) |
| Hook gate | `openhands/sdk/hooks/{types,config,manager,executor,conversation_hooks}.py` | `HookEventType` PreToolUse / PostToolUse / UserPromptSubmit / SessionStart / SessionEnd / Stop; `HookDecision` allow / deny (`ASK` is commented out as future work); hooks run as external scripts receiving JSON on stdin |
| Retries / error recovery | `openhands/sdk/conversation/stuck_detector.py` (370 lines), `event/error_classification.py` | `StuckDetector` finds five non-progress patterns (repeating action-observation, repeating action-error, monologue, alternating pattern, context-window errors) inside a **20-event window** with configurable thresholds, scanning only events after the last user message; `classify_error` maps a failure to a closed vocabulary |
| Failure classification | `openhands/sdk/event/error_classification.py` | `FailureKind` = auth / quota / rate_limit / config / transient / agent_action / internal / unknown; `ErrorClassification` is frozen, `extra="forbid"`, and carries only `kind`, `retryable`, `user_action` (none/retry/settings), `error_id`. Documented donor rules: authoritative class names are matched **before** message heuristics; generic wrappers are matched **after**; and `detail` is inspected locally only — it is *never* copied into the classification or sent to telemetry |
| Context packaging | `openhands/sdk/context/{agent_context,memory,view,prompts}`, `context/condenser/{base,llm_summarizing_condenser,pipeline_condenser,no_op_condenser}.py` | `RollingCondenser` / `LLMSummarizingCondenser` with `max_size=240`, `keep_first=2` and a validated `keep_first < max_size // 2` invariant; condensation emits `Condensation` / `CondensationRequest` / `CondensationSummaryEvent` events into the same log |
| Observability | `openhands/sdk/observability/laminar/*`, `sdk/event/{token,llm_completion_log,hook_execution}.py`, `agent-server/openhands/agent_server/telemetry/models.py` | token/cost events and completion logs as first-class events in the same durable log; optional external observability backend |
| Model/provider abstraction | `openhands/sdk/llm/**` (litellm-based), `sdk/profiles/*`, `sdk/settings/model.py`, `tool/builtins/{switch_llm,classify_and_switch_llm}.py` | one LLM abstraction over litellm with profiles and in-run model switching tools |
| Tool registry | `openhands/sdk/tool/{registry,spec,schema,tool,client_tool,defaults}.py`, `tool/builtins/*`, `openhands-tools/**` (18 tool families) | a process-global resolver registry with a **sealed catalog** (`_SEALED_CATALOG`), `ToolCatalogEntry(name, user_selectable, usable, description, in_default_set)`, JSON-Schema-validated action/observation types, per-action `security_risk`, and `ToolExecutor[ActionT, ObservationT]` |
| Concurrency | `openhands/sdk/conversation/{fifo_lock,resource_lock_manager,cancellation}.py`, `agent/parallel_executor.py`, `utils/async_executor.py` | FIFO lock, resource-lock manager, cooperative cancellation, parallel tool execution with an internal-failure classification |

## 6. License compatibility (checked before any copying)

* **No upstream source was copied into this repository.** Both proofs are independent
  implementations of the *pattern*, written against MPE's existing contracts.
* **OpenHands (MIT, both pins)** would permit verbatim reuse with attribution; it was still
  not reused verbatim because MPE has no Python agent runtime to host it and SCOPE-CHANGE-
  CONTROL §11 forbids a dependency the existing stack does not need.
* **Dify** is *not* plain Apache-2.0. Its license adds (a) a commercial-license requirement
  for operating a multi-tenant environment and (b) a logo/copyright restriction on the
  frontend, and it reserves the producer's right to change the terms. Copying Dify source
  into portfolio projects that may become multi-tenant (MebelFlow AI, Business Discovery)
  is therefore treated as **not permitted by default** in this experiment: Dify contributes
  patterns only, with an independent implementation.
* **`graphon`** has no license classifier on PyPI and no license file reachable through the
  package metadata; its terms are unverified. Any MPE dependency on it is rejected on that
  ground alone, independently of the generic-DAG stop rule.

## 7. Audit limitations

* Neither upstream was executed. All behaviour statements are read from source, docstrings
  and the upstreams' own tests; nothing here is a measured property of Dify or OpenHands.
* `graphon` was not read (not vendored in Dify, no license); the workflow-engine statements
  come from Dify's imports, its pinned version and its own tests.
* `Murkin1980/Murat-AI-Orchestrator` and `Murkin1980/business-discovery` are not readable
  from this session (`403`). Rows in `COMPONENT_MAP.md` that name them say so explicitly and
  make no architecture claim.
* Dify's `api/core/model_runtime` path no longer exists at the pin (provider/model runtime
  now goes through `api/core/plugin/impl/model_runtime*.py` + `graphon.model_runtime`); the
  EXP-20 `README.md` candidate list predates that move.
