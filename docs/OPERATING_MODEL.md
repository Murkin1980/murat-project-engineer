# Murat Project Engineer — Operating Model

Status: ACTIVE
Updated: 2026-08-19
Architecture: Option A+ boundaries unchanged

## Purpose

This document connects the portfolio-level New Idea Filter with the existing per-task Murat Project Engineer execution model. It is policy/documentation only and does not create a runtime, queue, scheduler, persistent agent, memory service, or workflow engine.

## Lifecycle

### 1. Idea intake

Any new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea first passes `docs/NEW_IDEA_FILTER_POLICY.md`.

The filter returns one primary disposition:

- `EXTEND_EXISTING`
- `REUSE_COMPONENT`
- `MERGE`
- `EXPERIMENT`
- `HOLD`
- `NEW_REPOSITORY`
- `REJECT`

No implementation starts before this disposition is recorded.

### 2. Project placement

If the disposition permits work, identify the target project's source-of-truth files and confirm that the idea fits the project's foundation, architecture, scope, priorities, and deep-change-gate.

`NEW_REPOSITORY` is exceptional and requires the evidence defined in the New Idea Filter Policy.

### 3. Execution classification

A concrete implementation task is classified using the existing MPE risk tiers:

- `FAST`
- `VERIFIED`
- `DEEP-CHANGE`

Portfolio disposition and execution risk are separate decisions. For example, an `EXTEND_EXISTING` idea can still be a `DEEP-CHANGE` task.

### 4. Bounded execution

For coordinator runs:

1. select the smallest sufficient Expert or temporary Expert Team;
2. use the applicable existing Playbook;
3. preserve observable handoffs where needed;
4. run deterministic gates before optional semantic review;
5. require explicit user approval for DEEP-CHANGE when applicable;
6. emit one terminal state: `PASS`, `REWORK`, `BLOCKED`, or `HUMAN_REQUIRED`.

### 4.1 Unified execution invariant

Every implementation and delegation follows `docs/UNIFIED_EXECUTION_WORKFLOW.md`: New Idea Filter (when needed) → Value / Scope / Deep-change gates → Task Packet → Skillization Gate → bounded execution or delegation → technical checks → Browser Evidence (when browser-observable) → verification-state check → final Git-diff checkpoint → terminal state.

The Task Packet is the pre-execution authority boundary. Delegates receive a narrowed packet or typed handoff; one writer owns a worktree unless isolated worktrees and a merge owner are explicit. The required Git-complete verification check returns `UNVERIFIED` after any change-set, status, content, `HEAD`, or base movement, so `PASS` cannot survive a moving diff.

### 4.2 Cost-aware execution invariant

Token and model cost are product-quality constraints, not an afterthought. A platform that consumes disproportionate model budget for routine tests is considered operationally defective even when its outputs are correct.

MPE therefore applies these constitutional rules:

1. **Cheapest sufficient model first.** Every task, test, evaluator, synthetic persona, reviewer and helper must use the cheapest model tier that is demonstrably adequate for the required quality and risk level.
2. **Deterministic before generative.** Use schemas, validators, unit tests, static checks, fixtures, cached/versioned evidence and other deterministic mechanisms before spending tokens on semantic evaluation.
3. **Selective escalation.** Expensive/high-capability models are reserved for ambiguous cases, failed gates, high-risk reasoning, final adjudication, or tasks whose measured quality cannot be maintained by cheaper tiers.
4. **No premium-model default for bulk evaluation.** Repeated regression runs, synthetic-persona populations, large experiment batches and broad candidate screening must not fan out directly to premium models by default.
5. **Router/provider portability.** MPE must support configurable inference routers/provider adapters so different tests can use different low-cost models without coupling governance contracts to one vendor or model family.
6. **Router authority stays bounded.** Routers select or reach inference providers/models; they do not gain project authority, approval authority, workflow ownership or autonomous execution authority.
7. **Budget guardrails are first-class.** Runs should support explicit limits such as maximum model calls, turns, context size, token/cost budget and premium-model escalations where observable and technically available.
8. **Fail closed on budget exhaustion.** A run that reaches its configured budget limit should stop, degrade to deterministic evidence, or request escalation rather than silently continue consuming premium capacity.
9. **Measure cost per useful outcome.** Experiments should record observable usage/cost and compare it against defects found, useful rework, evidence gained and business value. More model calls are never a success metric by themselves.
10. **Model names are configuration, not constitution.** Specific low-cost and premium models may change over time. The invariant is tiered, evidence-based routing, not permanent binding to one model.

Default routing intent:

- `FAST` / GREEN: deterministic tooling plus low-cost model when semantic work is needed;
- `VERIFIED` / YELLOW: low-cost worker/evaluator first, with escalation only after failed/ambiguous gates or explicit quality need;
- `DEEP-CHANGE` / RED: human gate first where required, then the capability tier justified by the risk;
- final judge/reviewer: use the strongest necessary model only on the smallest evidence package that can support the decision.

This policy explicitly permits installing/configuring multiple inference routers or provider adapters for economical testing, provided they remain replaceable infrastructure and respect MPE contracts, evidence requirements, security rules and deep-change boundaries.

### 5. Evidence

Measured Stage 2 work records:

- Run Report;
- Experiment Record;
- source/artifact references;
- rollback information;
- gate results;
- reviewer findings when used;
- architecture-pressure signals;
- observable model/router selection and cost/usage where available;
- budget-limit or escalation events where applicable.

Do not store hidden chain-of-thought, secrets, agent lifecycle state, queue state, or invented metrics.

## Authority boundaries

- Codex remains the execution/orchestration environment.
- Murat Project Engineer remains a bounded coordinator and policy layer.
- Codex Router or any additional inference router remains an inference/protocol/credential gateway only.
- Multiple routers/providers may coexist for cost and capability routing, but no router owns project decisions, approvals or workflow state.
- Experts remain bounded roles, not persistent processes.
- Git/project files remain the source of truth.
- The deep-change-gate remains mandatory.

## Current Stage 2 rule

Continue validating this operating model through the 20-run evidence experiment before proposing architectural expansion.

Cost-aware routing may be evaluated as a bounded experiment inside the existing architecture because it changes model/provider selection rather than project authority. Installing a new router that changes credentials, security boundaries, runtime ownership, persistent state, or autonomous execution remains subject to the appropriate security/deep-change review.

A need for better ergonomics, batching, dashboards, or UI is not by itself evidence for a workflow engine, persistent agents, adaptive routing, or durable orchestration state.
