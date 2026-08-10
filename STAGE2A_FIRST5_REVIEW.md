# Murat Project Engineer — Stage 2A First Five Review

Date: 2026-08-11  
Scope: first five real-work evidence runs  
Recommendation: `CONTINUE_20_RUNS`

## Run matrix

| Run | Project | Task | Mode | Risk | Outcome |
|---|---|---|---|---|---|
| 01 | Murat Project Engineer | Stage 2 experiment plan + durable status continuation point | baseline | FAST | PASS |
| 02 | Furniture Configurator | Parametric wardrobe, product switch, pricing/options/URL behavior | baseline | VERIFIED | PASS |
| 03 | MebelDocs AI | First order → invoice → PDF vertical slice | baseline | VERIFIED | PASS |
| 04 | MebelLegal KZ | Unified order document workflow and domain-boundary change | baseline | DEEP-CHANGE | PASS |
| 05 | Murat Project Engineer | Resume Stage 2A and add portable evidence/context documentation | coordinator | VERIFIED | BLOCKED |

Run 05 is blocked only on repository-local validator/unit-test execution not available through the current GitHub connector execution surface. The changes and evidence are preserved and rollbackable; no PASS is claimed without those checks.

## Risk distribution

- FAST: 1
- VERIFIED: 3
- DEEP-CHANGE: 1

Run 04 differs from the preferred Stage 2A queue classification. The inspected historical change modified `FOUNDATION.md` and domain ownership and therefore is correctly recorded as DEEP-CHANGE. Its ADR is marked accepted by the owner for the working prototype.

## Baseline vs coordinator

- baseline: 4
- Murat Project Engineer coordinator: 1

Historical baseline runs use only observable Git/project evidence. No Expert, Team, route, reviewer, rework, cost, or intervention behavior is retroactively simulated. Unobservable values are stored as `null` or `NOT_OBSERVABLE`.

The overall 20-run experiment still needs at least one additional comparable baseline to reach the planned minimum of five baseline runs.

## Reviewer value

No independent reviewer finding is observable in Runs 01–04. Run 05 did not invoke an independent semantic reviewer because the Verified playbook makes it optional and the blocking issue is deterministic validation availability, not semantic uncertainty.

- useful reviewer findings: 0 observable
- reviewer false positives: 0 observable

This sample is insufficient to estimate reviewer value or false-positive rate. Later VERIFIED runs should deliberately include independent review where semantic risk justifies it.

## Rework

Baseline rework counts were not observable and remain null.

Run 05 had one evidence-format rework cycle: the first Experiment Record schema required integer/boolean metrics even when baseline observability was absent. The schema was adjusted so the field remains required while `null` explicitly represents an unobservable value. This prevents false zeros from contaminating experiment metrics.

## Interruption and recovery

Run 05 successfully resumed after a prior session from versioned source-of-truth artifacts:

- `STATUS.md`
- `STAGE2_EXPERIMENT_PLAN.md`
- current repository commits
- the Stage 2A instruction supplied for this continuation

The task objective and architecture boundaries were recoverable without reconstructing hidden chain-of-thought. No durable runtime state, queue, persistent agent, or memory service was needed for recovery.

The run itself remains BLOCKED only because package validator/unit tests cannot be executed through the current GitHub connector surface.

## Overhead

Observable overhead in this sample is mostly evidence capture:

- additional JSON evidence files;
- source/artifact provenance references;
- explicit `NOT_OBSERVABLE` handling for retrospective baselines;
- several small Git commits because the connector writes individual files.

Token/cost and precise execution duration are not observable for the historical baselines and are not estimated.

No current evidence shows that this overhead requires a workflow runtime. Batch-oriented repository writes may improve ergonomics later without changing architecture.

## Architecture pressure

Across the five runs, no repeated evidence requires:

- fan-out/fan-in orchestration;
- durable workflow state beyond project files;
- a generic workflow engine;
- persistent runtime agents;
- adaptive routing;
- Router task/workflow authority;
- Prime Agent runtime.

Run 04 is especially useful: a large approved domain-boundary change was handled with ADR, versioned foundation/architecture documents, additive migration discipline, tests and rollback evidence. Its complexity did not itself create workflow-engine pressure.

Run 05's validation limitation is an execution-surface/tooling limitation, not evidence for a new orchestration architecture.

## JSON evidence format and future Workspace readiness

The JSON companions are sufficient for a future Workspace UI to list, filter and summarize:

- run identity;
- project/task;
- risk/playbook;
- experts/routes when observable;
- files/tools;
- gate outcomes with evidence references;
- terminal outcome;
- rollback;
- baseline/coordinator mode;
- interruption/recovery;
- architecture-pressure flags.

One correction was required during the first-five exercise: baseline metrics need explicit nullability when they were not historically observable. Required fields remain present, so consumers can distinguish `0` from `unknown`.

No workflow runtime state, queue state, agent lifecycle state or hidden reasoning is needed for this UI-readiness level.

## Recurring missing fields

No recurring missing field is proven after the nullability correction.

Potential future needs should be observed before changing the schema. In particular, do not add workflow-state fields merely for UI convenience.

## Deviations from Stage 2A instruction

1. Runs 01–04 are real historical baseline work rather than four newly executed tasks. This follows the Stage 2 rule not to retroactively simulate Expert/Team behavior and avoids artificial work.
2. Run 04 is classified DEEP-CHANGE rather than VERIFIED because its observable change modified foundational domain boundaries; owner acceptance is present in ADR 002.
3. Package validator and repository unit tests for current Run 05 could not be executed through the available GitHub connector. Run 05 therefore ends BLOCKED rather than claiming PASS.
4. Docsalot and Context.dev remain optional/documented only. No external private project context was published.

## Decision

`CONTINUE_20_RUNS`

Reason:

- interruption recovery from versioned files worked;
- baseline portability works after explicit nullability for unknown metrics;
- no repeated gate-skipping, fan-out bookkeeping failure, durable orchestration-state requirement, or persistent-agent pressure is observed;
- one connector execution limitation is not architectural evidence.

For Runs 06–20, prioritize fresh coordinator runs with locally executable deterministic gates and at least one additional baseline. Include independent Reviewer use on enough VERIFIED tasks to measure useful findings and false positives.
