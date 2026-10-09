# Arena Task — EXP-28 Agent Workflow Skills / `/retro`

Decision: **EXPERIMENT**
Repository: `Murkin1980/murat-project-engineer`

## Objective

Evaluate whether a deterministic, post-run retrospective can turn evidence from completed engineering runs into specific improvements to MPE navigation, instructions, or checks without expanding global governance.

## Fixed sample

Use only these three completed run records:

- EXP-24 HyperFrames, **Phase 1 only — PARTIAL**;
- EXP-25 Atomic CRM — **PASS**;
- EXP-27 Paperclip — **PASS**.

Do not treat the owner-authorized EXP-24 Phase 2 as a completed run. Read the records and linked evidence already present under each experiment directory. Do not reconstruct missing chat events or invent timestamps.

## Governing sources

Read and follow the applicable current MPE source-of-truth before drawing recommendations, including:

- `AGENTS.md`;
- `docs/governance/SCOPE-CHANGE-CONTROL.md`;
- `docs/OPERATING_MODEL.md` and `STATUS.md`;
- `docs/NEW_IDEA_FILTER_POLICY.md`, `docs/GLOBAL_MPE_ENFORCEMENT.md`, and `docs/OPINIONATED_WORKSPACE_POLICY.md`;
- `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md` and `docs/VALUE_UNIT_ECONOMICS.md`;
- `context/CONTEXT_MAP.md` and the relevant experiment records.

The explicit experiment scope outranks historical convention, but it does not weaken MPE's deep-change boundary or source-of-truth rules.

## Required reconstruction

For each run, record:

`task → actions taken → delays/errors → evidenced root cause (or unknown) → what could have prevented recurrence`

Explicitly assess all five classes:

1. Long search for a file or context.
2. Wrong or unnecessary execution path.
3. Error that a deterministic check could catch.
4. Instructions that were insufficient or excessive.
5. Repeated environment/tooling friction.

A missing event log means **unknown**, not permission to infer what happened.

## Recommendation gate

Every proposed change must contain:

- concrete evidence from a named run/artifact;
- root cause;
- minimal change and its existing MPE landing point;
- expected effect;
- risk of a false improvement or new overhead;
- a test that can disprove the recommendation.

Prefer `NO_CHANGE` for one-off, low-cost issues. Reject generic advice, additions made only because a rule "might be useful," and any duplicate governance or parallel source of truth.

## Reference extraction

Extract mechanisms from `/retro`, `/pr`, and instruction-review materials as `KEEP / BORROW / ADAPT / REJECT`. Do not copy or install the upstream skill. Do not create a prototype unless it is necessary to test the hypothesis; existing run evidence is preferred.

## Acceptance

PASS only if:

- all three runs are handled;
- findings point to real issues already present in evidence;
- recommendations are concrete and falsifiable;
- the experiment does not create a duplicate governance layer;
- at least one change is immediately usable in MPE;
- at least one unnecessary or harmful candidate is rejected with evidence;
- a measurable comparison against a manual/no-packet baseline is shown, with its limitations stated.

No automatic `/retro` hook, recurring process, new service, agent, runtime, database, or production integration is authorized. Stop if completing the experiment would require crossing the deep-change boundary; report `DEEP_CHANGE_REQUIRED` rather than weakening that boundary.
