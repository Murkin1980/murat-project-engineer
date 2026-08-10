# Murat Project Engineer — Status

Updated: 2026-08-11

## Current version

- Release: v1.0
- Stage 1: COMPLETE
- Stage 2: ACTIVE — 20-run evidence experiment
- Stage 2A: FIRST-FIVE EVIDENCE CAPTURED; current coordinator run BLOCKED on local validator/unit-test execution

## Current architecture

Murat Project Engineer remains a bounded coordinator layer for Murat AI Stack Option A+.

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
- package validator and tests
- isolated software-feature PoC
- Stage 2A evidence for Runs 01–05

## Stage 2A first-five status

- Run 01 — Murat Project Engineer documentation/status hygiene — FAST baseline — PASS
- Run 02 — Furniture Configurator parametric/UI/pricing feature — VERIFIED baseline — PASS
- Run 03 — MebelDocs AI order→invoice→PDF vertical slice — VERIFIED baseline — PASS
- Run 04 — MebelLegal unified order workflow/domain-boundary change — DEEP-CHANGE baseline — PASS
- Run 05 — Murat Project Engineer Stage 2A resume/evidence readiness — VERIFIED coordinator — BLOCKED

Run 05 is blocked only because the repository-local package validator and unit tests are not executable through the current GitHub connector surface. No PASS is claimed without those deterministic checks.

Interruption recovery itself succeeded: the task resumed from `STATUS.md`, `STAGE2_EXPERIMENT_PLAN.md`, current Git history and the Stage 2A continuation instruction without hidden chain-of-thought or durable runtime state.

See `STAGE2A_FIRST5_REVIEW.md` and `evidence/stage2a/`.

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

## Next action

1. In a local/Codex execution environment, resume Run 05 and execute:
   - `python scripts/validate_package.py .`
   - `python -m unittest discover -s tests -v`
2. If the checks pass, record the resumed validation as a subsequent evidence update without rewriting history.
3. Continue Runs 06–20 with fresh real work, prioritizing coordinator runs with observable deterministic gates and at least one more baseline run.
4. Use independent Reviewer on enough VERIFIED runs to measure reviewer value and false positives.

## Evidence-format finding

Stage 2A showed that retrospective baselines need a distinction between zero and unknown. Machine-readable experiment metrics therefore keep required fields but permit `null` where a historical value is not observable.

This is evidence portability only; no database or workflow runtime was added.

## Deep-change rule

Any proposal to add a workflow runtime, persistence layer for orchestration state, persistent agents, autonomous memory promotion, Router authority changes, adaptive routing, Prime runtime integration, or core architecture redesign is a deep change and requires explicit approval before implementation.
