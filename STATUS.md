# Murat Project Engineer — Status

Updated: 2026-08-29

## Current version

- Release: v1.1
- Stage 1: COMPLETE
- Stage 2: ACTIVE — 20-run evidence experiment
- Stage 2A: FIRST-FIVE EVIDENCE CAPTURED
- Runs 07–12: EVIDENCE CAPTURED — four PASS, one REWORK, one BLOCKED
- Portfolio dashboard: LIVE at https://murat-project-engineer.muriktl.workers.dev

## Current architecture

Murat Project Engineer remains a bounded coordinator and policy layer for Murat AI Stack Option A+.

Implemented and available:

- coordinator skill
- bounded Expert roles: Architect, Coder, Reviewer, Researcher
- temporary Expert Teams
- FAST, VERIFIED, DEEP-CHANGE and Software Feature playbooks
- deterministic Review Gates
- typed handoffs
- compact Markdown Run Reports
- machine-readable Run Report schema/example
- Markdown Experiment Record template
- machine-readable Experiment Record schema/example
- progressive context map
- context-provider architecture documentation
- mandatory New Idea Filter Policy
- operating-model documentation connecting portfolio filtering to risk-tiered execution
- unified evidence-first workflow: Value / Scope / Deep-change gates → Task Packet → Skillization Gate → bounded delegation → technical checks → Browser Evidence → verification-state check → final Git-diff checkpoint
- Task Packet and Browser Evidence contracts
- deterministic verification-state helper that invalidates scoped evidence after post-verification changes
- safe delegation rules: narrowed authority, explicit stop conditions, and one writer per worktree by default
- package validator and tests
- isolated software-feature PoC
- Stage 2 evidence for Runs 01–11
- bounded runtime-coordination contracts and stateless helpers from Run 11
- EXP-12 deterministic triage prototype, contracts and first retrospective backtest
- EXP-13 low-cost evaluation harness + pre-execution rework (frozen dataset v2, routes A/B/premium, thresholds, pricing snapshot, checks, and Pilot Batch 1 pre-registration)
- portfolio dashboard (read-only static asset, Workers Static Assets, auto-deploy on configured main push)

## Stage 2 run status

- Run 01 — Murat Project Engineer documentation/status hygiene — FAST baseline — PASS
- Run 02 — Furniture Configurator parametric/UI/pricing feature — VERIFIED baseline — PASS
- Run 03 — MebelDocs AI order→invoice→PDF vertical slice — VERIFIED baseline — PASS
- Run 04 — MebelLegal unified order workflow/domain-boundary change — DEEP-CHANGE baseline — PASS
- Run 05 — Murat Project Engineer Stage 2A resume/evidence readiness — VERIFIED coordinator — BLOCKED
- Run 06 — Murat Project Engineer operating-model/status synchronization — FAST coordinator — PASS
- Run 07 — Strix/FreeBuff controlled evaluation — VERIFIED coordinator — PASS (evaluation completed; Strix NOT_EXECUTED/HOLD)
- Run 08 — BrowserAct public-web acquisition evaluation — VERIFIED coordinator — PASS
- Run 09 — Personalized Assessment Engine v0 — VERIFIED coordinator — REWORK
- Run 10 — Munder Difflin controlled pilot — VERIFIED coordinator — BLOCKED
- Run 11 — bounded runtime-coordination patterns — VERIFIED coordinator — PASS
- Run 12 — CLEARS deterministic triage/executability backtest — VERIFIED coordinator — PASS (retrospective mechanics only)

Run 05 remains historically BLOCKED because repository-local package validator and unit tests were not executable through the GitHub connector execution surface during that run. No PASS is retroactively claimed.

Run 06 is a separate FAST documentation/policy synchronization run. It does not replace or rewrite Run 05.

Run 07 PASS applies only to completion of the controlled evaluation. Strix execution is NOT_EXECUTED and its decision remains HOLD. FreeBuff execution is REJECT; selected Codebuff patterns are REUSE_COMPONENT.

Run 09 remains REWORK until its unresolved production-rule, external-LLM, Git-boundary, and source-of-truth findings are addressed. Run 10 remains historically BLOCKED. Run 11 remains inside Option A+ only while its mailbox, JSONL, and lifecycle elements stay bounded, stateless, conditional helpers rather than runtime authority.

Run 12 PASS validates deterministic execution and retrospective fixture consistency. Prospective P-001–P-003 are complete; P-003 is the first real product case (`mebeldocs-ai@987c13e`). All labels matched `VERIFIED / approval=false`. Progress is 3/10, still insufficient for operational reliance.

## New Idea Filter

`docs/NEW_IDEA_FILTER_POLICY.md` is ACTIVE and MANDATORY.

Every new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea must be evaluated through Murat Project Engineer before implementation starts.

The primary disposition must be one of:

- `EXTEND_EXISTING`
- `REUSE_COMPONENT`
- `MERGE`
- `EXPERIMENT`
- `HOLD`
- `NEW_REPOSITORY`
- `REJECT`

`NEW_REPOSITORY` is the exception, not the default.

See `docs/OPERATING_MODEL.md` for how portfolio filtering connects to the existing FAST / VERIFIED / DEEP-CHANGE execution model.

## Unified execution workflow

`docs/UNIFIED_EXECUTION_WORKFLOW.md` is ACTIVE and MANDATORY for bounded implementation and delegation. It turns the existing gates into one evidence chain rather than independent rules. `PASS` is valid only for the captured Git-complete snapshot and current verification state; the required check returns `UNVERIFIED` after any change-set, status, content, `HEAD`, or base movement and enforces the Task Packet changed-path scope.

## Boundaries still in force

Not part of the current implementation:

- daemon or scheduler
- generic workflow engine / DAG runtime
- persistent runtime agents
- independent memory service
- automatic memory promotion
- adaptive routing
- Router task/workflow orchestration
- Prime Agent runtime integration
- mandatory Docsalot dependency
- mandatory Context.dev dependency
- Workspace UI implementation

Codex remains the execution/orchestration environment. Codex Router remains the inference/protocol/credential gateway.

## Current objective

Continue the Stage 2 experiment defined in `STAGE2_EXPERIMENT_PLAN.md` toward 20 representative runs.

The experiment must measure quality, rework, reviewer value, interruption recovery, overhead, and genuine architecture pressure before any expansion is proposed.

## Next actions

1. Preserve the historical Run 05 and Run 10 BLOCKED outcomes; do not retroactively promote them.
2. Keep Run 09 in REWORK until the recorded findings are resolved or explicitly scoped out.
3. Continue Runs 13–20 with fresh real work; pre-register the next EXP-12 case only when its real task is selected and reach 10 cases before operational reliance.
4. Ensure the 20-run set contains at least five baseline runs total; Runs 01–04 currently provide four historical baselines.
5. Use independent Reviewer on enough VERIFIED runs to measure reviewer usefulness and false positives.
6. Keep Run 11 helpers conditional and bounded. A poller, daemon, retry worker, router, scheduler, shared state, database, or generic messaging/runtime layer requires a new filter and DEEP-CHANGE review.
7. Add selected deterministic gates to GitHub CI only through a separate bounded change.
8. Maintain the portfolio dashboard snapshot as part of the weekly status ritual.
9. EXP-13 Pilot Batch 1 has recorded its three legal T-008 pre-execution stops (`HUMAN_REVIEW_REQUIRED` / `HUMAN_REQUIRED`, no model usage). The 15 proceeding model runs remain `BLOCKED`: telemetry paths now exist, but the frozen experiment lacks a model prompt, required artifact, artifact-level acceptance checks, and observable defect/retry/tool-call attribution. Create and pre-register a versioned execution/scoring protocol before spending model budget; do not invent post-hoc rules. After all 18 records exist, STOP and analyse.

## Evidence-format finding

Stage 2A showed that retrospective baselines need a distinction between zero and unknown. Machine-readable experiment metrics therefore keep required fields but permit `null` where a historical value is not observable.

This is evidence portability only; no database or workflow runtime was added.

## Deep-change rule

Any proposal to add a workflow runtime, persistence layer for orchestration state, persistent agents, autonomous memory promotion, Router authority changes, adaptive routing, Prime runtime integration, or core architecture redesign is a deep change and requires explicit approval before implementation.
