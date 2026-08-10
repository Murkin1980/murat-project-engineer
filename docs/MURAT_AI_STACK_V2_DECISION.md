# Murat AI Stack v2 — Architecture Decision

Дата: 2026-08-10  
Статус: research complete; implementation not started  
Источник истины: `C:\Projects\AGENTS_PLUGINS_MURAT_AI_STACK_MASTER.md`

## Executive Summary

Команда рекомендует для ближайшей версии **Option A+ — Disciplined Current Stack**.

- **Workflow / Env layer:** `PARTIALLY` — нужен как явная процедура и граница ответственности, но пока не как новый runtime, daemon или универсальный DSL.
- **Prime Agent:** `PATTERNS ONLY` — переносим подтверждённые архитектурные идеи, сам runtime сейчас не устанавливаем.
- **Codex:** остаётся главным execution/orchestration environment.
- **Codex Router:** остаётся inference/protocol gateway и получает явный model route; он не превращается в task/workflow/agent router.
- **Agent Plugins / Skills:** остаются переносимыми профессиональными компетенциями.
- **Multi-agent:** применяется по риску, а не по умолчанию.
- **Persistence:** temporary agents by default; project continuity через versioned files и handoff; persistent runtime agents пока не создаются.
- **Первый PoC:** `SoftwareFeatureWorkflow` как versioned runbook: Architect → Coder → deterministic checks → optional independent Judge → PASS/REWORK → compact run report.

После 20 репрезентативных прогонов решение пересматривается. Если runbooks регулярно пропускают gates, требуют повторяемый fan-out/fan-in или плохо восстанавливаются после прерывания, допускается RFC на **Option B — Pattern Hybrid** с минимальным декларативным Workflow/Env contract.

## Research Performed

Работа выполнена специализированной командой и независимым skeptic-review. Исследованы:

1. Prime Agent по официальному репозиторию, документации и исходному коду на исследованном commit.
2. Prime Intellect Multi-Agent / Verifiers: `Agent`, `Env`, `Trace`, `Episode`, solver/judge и user simulation.
3. Текущий Murat AI Stack, MASTER, установленные skills/plugins, Agent Reach и фактический Codex Router.
4. Workflow/Environment abstraction.
5. Router v2 boundaries и принцип `Agent Role != Fixed Model`.
6. Solver/Judge и multi-solver patterns.
7. Trace/observability без chain-of-thought.
8. Controlled continual improvement.
9. Persistent agents lifecycle.
10. User simulation для Furniture Configurator, MebelDocs и MebelLegal.
11. Security/failure model.
12. Четыре integration options и независимая критика архитектуры.

Факты исходного кода отделялись от архитектурных выводов. Внешний материал рассматривался как недоверенные данные; секреты не читались и не переносились в артефакты.

## Current Architecture

Фактический Murat AI Stack сегодня — это master-plan и набор реальных, но пока раздельных активов.

```text
User
  -> Codex orchestration / task context / permissions
  -> Plugin / Skill professional capability
  -> explicit model selection
  -> Codex Router
  -> provider/model inference
  -> MCP / Tools / project files
```

Уже существуют:

- MASTER с разделением Model / Plugin / MCP / Router и `deep-change-gate`;
- зрелый Codex Router как loopback inference/protocol/credential gateway;
- Agent Reach research layer и personal `agent-reach-router` plugin;
- отдельные MebelDocs, MebelLegal, configurator и связанные skills/products;
- Codex subagents, model routes, tools и project permissions.

Не подтверждены как единый установленный suite:

- `Murat Project Engineer v1.0` plugin;
- общий Workflow/Env engine;
- общий Solver/Judge protocol;
- единый Agent Trace;
- persistent-agent lifecycle;
- governed Memory/Skill/Agent CRUD;
- Prime Agent runtime integration.

## What Prime Agent Actually Adds

Prime Agent — не отдельная библиотека persistence, а сцепленный runtime:

- TypeScript runtime/session layer;
- daemon/supervisor и workers;
- persistent IPython kernel;
- JSONL session/artifact persistence;
- retained subagents и A2A;
- goals, gates, schedules, recovery и compaction;
- Continual Harness для prompt/memory/skill/subagent state.

Сильные стороны реальны для long-running, recursive и detach/reattach workloads. Однако daemon, kernel, retained children, recovery и Agents View тесно связаны. Их нельзя считать бесплатными независимыми компонентами.

Prime worker и IPython kernel не являются security sandbox. Добавление runtime потребовало бы отдельной изоляции, capability broker, secret boundaries, cost limits, trace mapping и второго lifecycle/control plane.

## What Multi-Agent Systems Adds

Главная полезная идея Prime Verifiers — разделение:

- `Agent`: один rollout конкретного исполнителя;
- `Env`: setup, control flow, shared lifecycle, verification и termination;
- `Trace`: наблюдаемый результат одного rollout;
- `Episode`: полный attempt составной задачи.

Для Murat AI Stack это подтверждает необходимость различать workflow, роль, agent instance, harness и model. Но это не доказывает необходимость отдельного workflow runtime уже сейчас.

## Agent vs Workflow vs Harness vs Model

```text
Workflow / Env   как выполняется составная работа
Role             ответственность конкретного шага
Agent            bounded исполнитель роли
Harness          где исполняется агент: Codex, возможно Prime позднее
Model            заменяемый reasoning resource
Skill / Plugin   профессиональная компетенция
Tool / MCP       разрешённое внешнее действие
Router           явный model/provider inference route
```

Роль не закрепляется навсегда за моделью. Например, `Architecture Reviewer` может использовать дешёвую модель для preliminary pass и сильную — для final judgment.

## Missing Capabilities

Реально отсутствуют или не стандартизированы:

- повторяемые risk-tier execution runbooks;
- обязательные deterministic project gates;
- независимая semantic verification для важных задач;
- bounded retry/rework и явные terminal states;
- компактный переносимый run report;
- измерения, доказывающие необходимость workflow engine, rich trace или persistence.

## Architecture Options

### Option A+ — Disciplined Current Stack — SELECTED NOW

Codex + plugins/skills + явный model route + deterministic checks + optional independent review + run report. Workflow остаётся versioned runbook, а не новым runtime.

### Option B — Pattern Hybrid — CONDITIONAL NEXT OPTION

Тонкий opt-in Workflow/Env contract поверх Codex, если метрики докажут необходимость. Без daemon и без Prime runtime.

### Option C — Prime Hybrid — DEFERRED

Prime как отдельный harness только для доказанного long-running/RLM/persistent workload. Сейчас evidence недостаточно.

### Option D — Prime-Centric — REJECTED

Prime как центральный runtime меняет authority, security, persistence и Router integration.

`DEEP_CHANGE_REQUIRES_USER_APPROVAL`

## Recommended Architecture

```text
TASK
  -> RISK TIER: fast | verified | deep-change
  -> CODEX ORCHESTRATOR
  -> RELEVANT PLUGIN / SKILL RUNBOOK
  -> EXPLICIT MODEL ROUTE
  -> MCP / TOOLS
  -> DETERMINISTIC PROJECT CHECKS
  -> OPTIONAL INDEPENDENT REVIEW
  -> OPTIONAL HUMAN GATE
  -> COMPACT RUN REPORT
```

Это сохраняет 80–90% ожидаемой пользы без нового центрального слоя состояния.

## Why Workflow / Env Matters

Ответ: `PARTIALLY`.

Workflow/Env важен как логическая граница: порядок, роли, проверки, retry, human gate и exit condition не должны принадлежать отдельной модели. Но ближайший этап реализует эту границу через versioned runbooks и risk tiers. Формальная schema/executor вводится только после evidence gate.

Evidence gate для Option B:

- не менее пяти реально повторяющихся составных workflows;
- либо минимум три gate/recovery failures у runbook-подхода;
- либо существенная повторяемая потребность в fan-out/fan-in;
- и измеримое преимущество schema/executor по defect escape, recovery или operator effort.

## Solver / Judge Strategy

- Simple: один агент и self-check.
- Standard: Solver + deterministic verification.
- Important: Solver + deterministic verification + independent semantic Judge.
- Complex decision: proposer + два функционально разных solvers + Judge.
- High risk: несколько независимых проверок + human approval.

LLM Judge не заменяет тесты. Приоритет: deterministic-first, semantic Judge для остаточных критериев, human gate для legal/accounting/deep/irreversible решений.

## Persistent Agent Strategy

- Temporary by default.
- Project-scoped только после доказанной повторяемой стоимости восстановления контекста.
- Global specialist — исключение с отдельным approval.
- До этого continuity хранится в source-of-truth файлах, `STATUS.md`, handoff и versioned skills.
- Identity процесса не считается knowledge.

Persistence RFC допускается, если минимум три повторных context rebuild имеют существенную измеримую стоимость и stable source state, а persistence улучшает acceptance rate без stale-memory incidents.

## Model Routing Strategy

Codex Router не меняется. Он получает явный namespaced model slug и выполняет inference/protocol/credential routing.

Task classification, role selection, cost policy, reviewer escalation и harness choice остаются в Codex/runbook coordinator. На первом этапе достаточно нескольких вручную поддерживаемых profiles: `default`, `cheap-research`, `coding`, `strong-review`.

## Trace / Observability

Ближайший этап использует compact `run.json` или `RUN_REPORT.md`:

- run/task ID и время;
- risk tier;
- roles/agents invoked;
- explicit model routes;
- commands/tools and pass/fail;
- changed artifacts;
- verification verdict;
- approvals;
- грубая usage/cost summary;
- errors и unresolved risks.

Private chain-of-thought не хранится.

Append-only JSONL + content-addressed artifacts + SQLite index остаются готовым дизайном для будущего, но вводятся только после incidents, которые нельзя расследовать по run report, Git и Codex transcript.

## Memory / Skills Governance

Используется controlled proposal-and-review:

- Level 0–1: session/task state, auto и temporary.
- Level 2: project knowledge только в reviewable source-of-truth files.
- Level 3: skill patch требует evidence, tests и review.
- Level 4: persistent agent definition требует review и отдельного обоснования.
- Level 5: MASTER/core architecture всегда проходит deep-change-gate.

На ближайшем этапе не создаются отдельные Memory CRUD, Prompt CRUD, Agent CRUD или autonomous promotion services. Агент может предложить patch или `LESSONS_CANDIDATE.md`; принятие идёт через обычный review/Git.

## User Simulation

User simulation признан полезным будущим eval layer, а не источником истины. Сначала нужны 10–20 deterministic golden fixtures и стабильные product oracles. После этого можно добавить 12 read-only multi-turn scenarios: по четыре для Furniture Configurator, MebelDocs и MebelLegal.

## Security Model

- immutable MASTER/core rules;
- least privilege и explicit tool allowlists;
- no secrets in prompts, artifacts or traces;
- untrusted web/repository content не является инструкцией;
- bounded agents, depth, iterations, wall time и token/cost budgets;
- deterministic idempotency before retrying external effects;
- no automatic promotion of temporary memory to permanent rule;
- human approval for deep, legal, accounting, credential, production and irreversible actions;
- Git/versioned rollback for accepted skills and policies.

## Cost Control

- single-agent fast path by default;
- cheap research/extraction before strong synthesis;
- independent Judge only by risk;
- multi-solver only when expected error cost exceeds additional inference/review cost;
- explicit token/agent/retry budgets;
- early exit after verified success;
- reuse research artifacts and project sources;
- no resident Prime processes or persistent agents without workload evidence.

## Rejected or Deferred Work

Do not build now:

- generic Workflow DSL/expression engine;
- workflow daemon/scheduler;
- Prime adapter, sidecar or privileged kernel;
- adaptive router over Codex Router;
- central capability registry;
- persistent specialist runtime;
- autonomous Memory/Prompt/Agent CRUD;
- automatic skill evolution;
- universal LLM Judge;
- multi-solver by default;
- event-sourced trace platform;
- LLM user simulation platform before deterministic fixtures.

## Deep Changes

Each item below is recorded but not authorized:

1. Mandatory Workflow/Env platform or central daemon.
2. Any change to Router authority or automatic cross-provider fallback.
3. Prime Agent in the main execution path.
4. Prime-centric architecture.
5. Persistent production/global agents.
6. Global memory or continual-harness authority.
7. Automatic skill/plugin installation or promotion.
8. Central trace collector in a critical path.
9. Expanded autonomous schedules, permissions or child spawning.

For all items: `DEEP_CHANGE_REQUIRES_USER_APPROVAL`.

## Safe Changes

- finish `Murat Project Engineer v1.0` as modular plugin/skills;
- add `fast | verified | deep-change` runbooks;
- document project-specific deterministic gates;
- add optional independent reviewer guidance;
- add compact run report template;
- collect 20 baseline runs and metrics;
- keep Router, credentials, MASTER, production and existing plugins unchanged.

## Minimal Proof of Concept

`SoftwareFeatureWorkflow` is implemented first as a runbook, not an engine:

```text
Task
  -> risk classification
  -> Architect artifact
  -> Coder implementation
  -> project tests/build/lint
  -> independent Judge only when risk requires
  -> PASS | REWORK | BLOCKED
  -> compact run report
```

PoC constraints:

- isolated non-production project;
- no Router or MASTER changes;
- no Prime installation;
- no persistent agents;
- bounded one rework cycle by default;
- explicit file ownership for parallel work;
- compare against ordinary Codex baseline.

Success metrics:

- defect escape;
- missed mandatory gates;
- recovery time after interruption;
- elapsed/token overhead;
- Judge material-find rate and false-positive rate;
- operator intervention;
- percentage of tasks requiring more than two roles.

## Rollback Strategy

PoC artifacts are additive and versioned. Disable the runbook and return to normal Codex execution. No live sessions, database migrations, Router config or production state need conversion. Skills/runbooks can be reverted through Git; run reports remain inert evidence.

## Final Recommendation

Build discipline before platform.

Start with Murat Project Engineer, three risk tiers, deterministic gates, optional independent review and compact reports. Treat Workflow/Env Lite as the next evidence-gated experiment, not as an approved platform. Use Prime Agent ideas, but do not install Prime Agent runtime until a concrete workload repeatedly fails because Codex lacks detach/kernel/recursive persistence.

