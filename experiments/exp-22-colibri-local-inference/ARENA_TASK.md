# Arena task — EXP-22 Colibri

You are executing a bounded MPE experiment. Read `README.md` first.

## Mission

Determine whether Colibri provides measurable value as an **optional local inference component** for existing MPE systems, especially constrained classification/routing.

Do not build a new platform.

## Required order

1. Inspect this repository for existing inference/provider/router abstractions that could accept a Colibri adapter.
2. Inspect current Colibri documentation/upstream only as needed to reproduce a minimal local test.
3. Choose the smallest supported model/hardware path sufficient for the experiment.
4. Run CP-01: READY/WARNING/BLOCKED constrained classification on a frozen fixture set.
5. Run CP-02: routing among a fixed list of existing agents/services.
6. Run CP-03 only if CP-01 or CP-02 shows useful signal: verify provider/API compatibility from an isolated harness.
7. Record evidence and produce `FINDINGS.md`.

## Before changing code

Report:
- existing component to extend/reuse;
- why this does not duplicate current infrastructure;
- exact files you intend to add/change;
- whether any deep-change trigger exists.

If a deep-change is required, STOP and report it. Do not implement it.

## Evaluation

For every CP record:
- model + revision
- hardware
- commands/config needed to reproduce
- latency
- memory/storage footprint
- expected output
- actual output
- pass/fail
- notable failure modes

For CP-01 and CP-02 use deterministic/frozen fixtures committed under this directory when possible.

## Boundaries

Allowed:
- files under `experiments/exp-22-colibri-local-inference/`;
- minimal isolated test harness;
- read-only inspection of existing project code;
- a tiny adapter proof only if it is isolated and does not change production behavior.

Not allowed:
- new repository;
- production deployment;
- production configuration changes;
- default-provider changes;
- secrets;
- new control plane/router;
- refactor of unrelated MPE code;
- merging any production integration as part of this experiment.

## Deliverable

End `FINDINGS.md` with:

```
RESULT: PASS | PARTIAL | FAIL
RECOMMENDATION: REUSE_COMPONENT | HOLD | REJECT
BEST_USE_CASE: <one sentence>
MEASURED_VALUE: <numbers, not adjectives>
NEXT_STEP: <one bounded action or NONE>
DEEP_CHANGE: YES | NO
```

If RESULT is PASS, propose the smallest follow-up patch for `murat-ai-orchestrator` or the relevant existing component. Do not implement that follow-up without a separate authorization.
