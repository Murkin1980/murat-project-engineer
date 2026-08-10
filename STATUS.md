# Murat Project Engineer — Status

Updated: 2026-08-11

## Current version

- Release: v1.0
- Stage 1: COMPLETE
- Stage 2: ACTIVE — 20-run evidence experiment

## Current architecture

Murat Project Engineer remains a bounded coordinator layer for Murat AI Stack Option A+.

Implemented and available:

- coordinator skill
- bounded Expert roles: Architect, Coder, Reviewer, Researcher
- temporary Expert Teams
- FAST, VERIFIED, DEEP-CHANGE and Software Feature playbooks
- deterministic Review Gates
- typed handoffs
- compact Run Reports
- experiment record template
- package validator and tests
- isolated software-feature PoC

## Boundaries still in force

Not part of the current implementation:

- daemon or scheduler
- generic workflow engine / DAG runtime
- persistent runtime agents
- independent memory service
- automatic memory promotion
- Router task/workflow orchestration
- Prime Agent runtime integration

Codex remains the execution/orchestration environment. Codex Router remains the inference/protocol/credential gateway.

## Current objective

Execute the Stage 2 experiment defined in `STAGE2_EXPERIMENT_PLAN.md` and collect 20 representative runs across real Murat AI Stack work, including comparable baseline runs.

The experiment must measure quality, rework, reviewer value, interruption recovery, overhead, and genuine architecture pressure before any expansion is proposed.

## Next action

Start Run 01 on the next suitable real task. Complete the existing Experiment Record and Run Report artifacts for that task.

## Deep-change rule

Any proposal to add a workflow runtime, persistence layer, persistent agents, autonomous memory promotion, Router authority changes, or Prime runtime integration is a deep change and requires explicit approval before implementation.
