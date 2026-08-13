# Murat Project Engineer — Status

Updated: 2026-08-13

## Current version

- Release: v1.0
- Stage 1: COMPLETE
- Stage 2: ACTIVE — 20-run evidence experiment
- Stage 2A: FIRST-FIVE EVIDENCE CAPTURED
- Run 06: COMPLETE — operating-model/status synchronization
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
- package validator and tests
- isolated software-feature PoC
- Stage 2 evidence for Runs 01–06
- portfolio dashboard (read-only static asset, Workers Static Assets, auto-deploy on configured main push)

## Stage 2 run status

- Run 01 — Murat Project Engineer documentation/status hygiene — FAST baseline — PASS
- Run 02 — Furniture Configurator parametric/UI/pricing feature — VERIFIED baseline — PASS
- Run 03 — MebelDocs AI order→invoice→PDF vertical slice — VERIFIED baseline — PASS
- Run 04 — MebelLegal unified order workflow/domain-boundary change — DEEP-CHANGE baseline — PASS
- Run 05 — Murat Project Engineer Stage 2A resume/evidence readiness — VERIFIED coordinator — BLOCKED
- Run 06 — Murat Project Engineer operating-model/status synchronization — FAST coordinator — PASS

Run 05 remains historically BLOCKED because repository-local package validator and unit tests were not executable through the GitHub connector execution surface during that run. No PASS is retroactively claimed.

Run 06 is a separate FAST documentation/policy synchronization run. It does not replace or rewrite Run 05.

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

1. In a local/Codex execution environment, complete the pending Run 05 deterministic validation:
   - `python scripts/validate_package.py .`
   - `python -m unittest discover -s tests -v`
2. Preserve Run 05 history and record any resumed validation as a later evidence update.
3. Continue Runs 07–20 with fresh real work.
4. Ensure the 20-run set contains at least five baseline runs total; currently Runs 01–04 provide four historical baselines.
5. Use independent Reviewer on enough VERIFIED runs to measure reviewer usefulness and false positives.
6. Apply the New Idea Filter before beginning any substantial new project/repository/feature idea.
7. Maintain portfolio dashboard snapshot as part of the weekly status ritual.

## Evidence-format finding

Stage 2A showed that retrospective baselines need a distinction between zero and unknown. Machine-readable experiment metrics therefore keep required fields but permit `null` where a historical value is not observable.

This is evidence portability only; no database or workflow runtime was added.

## Deep-change rule

Any proposal to add a workflow runtime, persistence layer for orchestration state, persistent agents, autonomous memory promotion, Router authority changes, adaptive routing, Prime runtime integration, or core architecture redesign is a deep change and requires explicit approval before implementation.
