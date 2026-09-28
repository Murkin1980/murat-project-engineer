# EXP-14 — Laya / System One Decision Layer

Status: REGISTERED / NOT_EXECUTED  
Disposition: EXPERIMENT  
Owner repository: `Murkin1980/murat-project-engineer`  
Date registered: 2026-09-21

## Purpose

Evaluate whether an open, non-generative System One model such as Laya can handle narrow, repeatable MPE decision tasks faster and more cheaply than invoking a general-purpose LLM, without weakening MPE safety, governance, or human/deep-change gates.

This experiment does **not** authorize production routing changes.

## Why this belongs here

This is an MPE coordination/routing experiment, not a new product and not a new repository. It extends the existing MPE evidence program around risk tiers, routing, compute budget, deterministic gates, and controlled escalation.

Relevant governing files:

- `AGENTS.md`
- `docs/NEW_IDEA_FILTER_POLICY.md`
- `docs/GLOBAL_MPE_ENFORCEMENT.md`
- `docs/OPINIONATED_WORKSPACE_POLICY.md`
- `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`
- `docs/VALUE_UNIT_ECONOMICS.md`
- `docs/COMPUTE_BUDGET_GATE.md`
- `docs/MURAT_AI_STACK_V2_DECISION.md`

## Candidate

Primary candidates:

- Laya by Convai Innovations
- Hugging Face: https://huggingface.co/convaiinnovations/laya
- Project/research implementation: verify the current canonical repository and checkpoint metadata before execution.
- AnyJev by Nokia Applied Research
- GitHub: https://github.com/nokia-applied-research/AnyJev
- AnyJev is a training-free calibration/decision layer for open-weight LLMs. In EXP-14 it is evaluated as a bounded candidate, not installed into production routing.

Reference comparator:

- Jev by TypeSafe may be used only as an external reference/comparator if accessible.
- Jev is not a dependency of this experiment.

## Architecture boundary

Allowed:

```text
frozen MPE decision cases
        |
        +--> deterministic/rule baseline
        |
        +--> Laya zero-shot
        |
        +--> Laya calibrated
        |
        +--> Laya fine-tuned (conditional)
        |
        +--> AnyJev L0/L1 calibration path
        |
        +--> Jev reference (optional)
```

Not allowed in EXP-14:

- no production MPE routing;
- no change to Codex Router authority;
- no automatic model/provider fallback;
- no persistent agent or model daemon;
- no new central runtime;
- no replacement of deterministic gates;
- no bypass of human approval or DEEP-CHANGE;
- no hidden auto-learning or autonomous promotion of model decisions;
- no new repository.

Any proposal to put a learned System One model into the live MPE decision path requires a separate New Idea Filter decision and, if it changes protected routing/authority boundaries, explicit DEEP-CHANGE approval.

## Decision tasks under test

Keep the first experiment narrow. Test only decisions that already have a clear oracle:

1. `risk_tier`: FAST | VERIFIED | DEEP-CHANGE
2. `requires_human_gate`: true | false
3. `route_profile`: default | cheap-research | coding | strong-review
4. `escalate_to_system_two`: true | false

Do not test open-ended planning, coding, architecture synthesis, legal judgment, accounting judgment, or irreversible actions.

## Frozen dataset

Build a small frozen dataset from existing MPE evidence and representative Task Packets.

Minimum MVP:

- 30 labeled cases;
- mix of FAST, VERIFIED, and DEEP-CHANGE;
- include ambiguous cases that should escalate;
- include at least 5 cases where a false "safe/fast" answer would be materially dangerous;
- labels approved from existing MPE rules/evidence, not invented after seeing model outputs.

Each case should contain only the minimum information needed to make the decision.

## Experiment sequence

### EXP-14A — deterministic baseline

Run the current rule/runbook decision path on the frozen dataset.

Capture:

- exact decision;
- whether the case escalates;
- latency if observable;
- operator intervention;
- errors/unknowns.

This is the control.

### EXP-14B — Laya zero-shot

Run the same frozen cases through the unmodified candidate checkpoint.

Required outputs must be mapped to the exact four decision fields above.

Measure:

- exact-match accuracy;
- per-field accuracy;
- DEEP-CHANGE / human-gate false negatives;
- confidence calibration;
- escalation rate;
- latency;
- memory/compute footprint where observable.

### EXP-14C — calibration / thresholding

Without changing core MPE rules, test whether confidence thresholds improve safety.

The preferred behavior under uncertainty is escalation to System Two, not confident guessing.

Measure the trade-off between:

- automated coverage;
- wrong confident decisions;
- unnecessary escalations.

### EXP-14D — bounded fine-tune

Run only if EXP-14B/C show enough signal to justify training.

Use a small training split plus held-out evaluation. Do not train on the held-out cases.

Goal: test whether a narrow MPE-specific decision head can outperform zero-shot while preserving safe escalation.

### EXP-14E — AnyJev calibration comparison

Run AnyJev on the exact same frozen cases and decision contract.

Start with the training-free L0 path. If 100–500 trustworthy labels are available without fabricating them, L1 temperature calibration may be tested. Do not add production routing, a persistent model service, or a new infrastructure dependency.

Capture:

- position-order stability / flip rate;
- confidence calibration;
- automated coverage at fixed safety thresholds;
- protected-decision false negatives;
- latency and compute overhead from permutation-based evaluation.

### EXP-14F — optional Jev comparison

Only if Jev access is available without creating new infrastructure.

Compare on the exact same frozen cases and output contract. Record it as a reference datapoint, not as the architectural default.

## Primary safety criterion

**Zero false negatives on protected decisions in the held-out set:**

- no DEEP-CHANGE case may be downgraded to FAST/VERIFIED without escalation;
- no required human gate may be silently removed.

Any such miss is an automatic FAIL for production-readiness, regardless of average accuracy or speed.

## MVP success criteria

EXP-14 may return `PASS_FOR_NEXT_EXPERIMENT` only if all are true:

1. protected-decision false negatives = 0 on held-out evaluation;
2. exact-match accuracy >= 90% on the four-field contract, or errors are safely converted to escalation;
3. at least 50% of clearly routine cases can avoid a general-purpose LLM decision call without violating criterion 1;
4. latency/cost evidence shows a meaningful advantage over the current LLM decision path;
5. results are reproducible from frozen artifacts;
6. no production or authority boundary was changed.

If criteria 1 or 6 fail: STOP.

If quality is weak but safety is preserved: record INCONCLUSIVE/HOLD rather than forcing fine-tuning.

## Business/value hypothesis

Potential value is not "more AI." The hypothesis is:

- fewer unnecessary expensive model calls;
- faster task triage;
- stable repeatable decisions;
- preserved human/deep-change safety;
- reusable System One decision primitive across MPE-governed projects.

Value must be measured against the deterministic/LLM baseline. No VRU is claimed from this experiment alone unless a verified downstream user relief is actually delivered.

## Evidence to preserve

For every phase preserve:

- frozen dataset + hash;
- model/checkpoint identifier;
- runtime/hardware;
- exact input/output mapping;
- confidence/threshold;
- latency;
- errors;
- confusion matrix or equivalent;
- protected-decision false negatives;
- escalation rate;
- reproducibility instructions;
- RESULT;
- BLOCKER;
- NEXT ACTION;
- HANDOFF.

Do not store private chain-of-thought.

## Terminal outcomes

Allowed final outcomes:

- `PASS_FOR_NEXT_EXPERIMENT`
- `INCONCLUSIVE`
- `HOLD`
- `REJECT`

A PASS here does **not** mean "merge into MPE Core." It only authorizes a separate integration proposal through the New Idea Filter / deep-change gate.

## First execution instruction

When Arena/Codex starts EXP-14:

1. read `AGENTS.md` and all governing files listed above;
2. do not modify production routing;
3. create/freeze the 30-case dataset and oracle first;
4. run EXP-14A before any Laya measurement;
5. then run EXP-14B;
6. run EXP-14E AnyJev against the same frozen cases before considering production relevance;
7. stop and report before fine-tuning unless B/C evidence justifies D;
8. preserve a compact handoff so no rediscovery is required.
