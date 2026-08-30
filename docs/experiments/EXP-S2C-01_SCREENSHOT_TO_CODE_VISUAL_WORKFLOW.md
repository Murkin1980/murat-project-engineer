# EXP-S2C-01 — Screenshot-to-Code Visual Workflow

Status: `PLANNED`
Primary disposition: `EXPERIMENT`
Date registered: 2026-08-28
Upstream reference: `abi/screenshot-to-code`
Pinned source tree: `d026163f586dfa8c5c10d28c36edd59a9d3b0e88`
Deep-change: `false` for this bounded experiment
New repository: `forbidden`

## Hypothesis

A bounded screenshot-to-code workflow that uses browser-render feedback, asset extraction, and targeted edits can reduce human UI reconstruction/rework effort for an existing Murat project by at least 30% without degrading mobile fidelity or creating a new persistent runtime dependency.

## Why this is an experiment, not implementation

The upstream project overlaps existing Codex visual-development capabilities and existing Murat projects. Its full stack would duplicate frontend editor, AI-provider, runtime, image-processing, and service infrastructure.

The experiment therefore validates only the reusable workflow patterns before any adoption decision.

## First target

Preferred existing project target: `Interactive KP / Qulpinay Style`.

Reason:

- bounded visual artifact;
- real business use;
- low architecture risk;
- straightforward reference-vs-output comparison;
- easy rollback;
- no need to touch Business Discovery core architecture.

## Baseline

Current Codex visual workflow on the same reference screenshot and same requested output scope.

## Candidate path

`reference screenshot -> bounded screenshot-to-code workflow -> asset extraction when useful -> create artifact -> browser render desktop/mobile -> visual inspection -> targeted edits -> Codex production adaptation`

The full upstream hosted/product UI is not required.

## Scope lock

Allowed:

- static screenshot input;
- one bounded real UI fixture;
- temporary/local or branch-only execution;
- HTML/Tailwind or the closest low-friction prototype target;
- browser screenshot verification;
- asset extraction;
- targeted edits;
- evidence capture;
- comparison against baseline.

Not allowed in EXP-S2C-01:

- new repository;
- production integration;
- persistent agent/service/runtime;
- workflow engine;
- scheduler/daemon;
- provider-routing replacement;
- Business Discovery architecture changes;
- multi-screen video workflow;
- automatic deployment to production;
- copying the full upstream React/Vite + FastAPI product.

## Fixture

Use one real visual reference relevant to an existing furniture-facing artifact.

Preferred fixture:

- one Interactive KP / Qulpinay-style page or one comparable furniture landing screen.

The exact reference must be recorded before execution.

## Required evidence

Record both baseline and candidate:

1. source/reference image identifier;
2. start/end timestamps or observable effort duration;
3. first usable prototype artifact;
4. final candidate artifact;
5. desktop screenshot;
6. mobile screenshot;
7. count of manual correction instructions;
8. count of generation/edit cycles;
9. list of extracted/generated/reused assets;
10. production migration notes;
11. observed API/AI cost where available;
12. final independent visual review.

## Metrics

Primary:

- human reconstruction/rework time;
- manual correction count;
- visual fidelity;
- mobile fidelity;
- production migration effort.

Secondary:

- generation/edit cycles;
- asset accuracy;
- AI cost;
- regression count.

Optional:

- perceptual image similarity metric if it can be added without expanding experiment scope.

## PASS criteria

Outcome is `PASS` only if:

- human reconstruction/rework effort is reduced by >=30%, OR effort is roughly equal but visual fidelity is materially better;
- mobile output is not worse than baseline;
- no screenshot-as-layout cheating is used;
- migration into the target production repository is not materially harder than baseline;
- no new persistent runtime/service is needed;
- result can be reproduced from the recorded fixture and instructions.

## REWORK criteria

Use `REWORK` when the core loop is valuable but one bounded issue prevents PASS, such as:

- weak asset extraction;
- unstable targeted editing;
- lack of independent visual scoring;
- excessive model/provider cost;
- cleanup required before production handoff.

## HOLD/FAIL criteria

Use `HOLD` when:

- cleanup/migration consumes the saved generation time;
- visual quality is not better than the current Codex workflow;
- the candidate needs a standalone service/runtime to become useful;
- external provider requirements outweigh the measured benefit.

## Deep-change gate

The experiment itself is not deep-change.

STOP and request explicit approval before any proposal to introduce:

- a persistent shared screenshot-to-code runtime;
- autonomous visual coding agents running as infrastructure;
- new workflow/orchestration authority;
- a new repository/product boundary;
- provider-routing authority changes;
- shared persistent generation state.

## Expected post-experiment dispositions

If PASS: likely `REUSE_COMPONENT` for selected patterns only.

Candidate reusable patterns:

- mandatory browser-render verification;
- desktop + mobile preview feedback;
- controlled create/edit file semantics;
- asset-first reconstruction;
- run evidence/cost capture.

If REWORK: repeat only after the blocking condition is precisely scoped.

If HOLD: preserve the architecture report as reference; do not integrate.

## Research reference

Full architectural analysis:

`docs/evaluations/SCREENSHOT_TO_CODE_DEEP_ANALYSIS_2026-08-28.md`

## Continuation instruction

Before execution, select the exact existing-project fixture and freeze the baseline/candidate instructions. Run both paths against the same scope. Do not modify production code during the experiment. Produce an experiment report using `docs/experiments/EXPERIMENT_REPORT_TEMPLATE.md` and then run the New Idea Filter again before any adoption work.
