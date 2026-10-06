# EXP-24 — HyperFrames PR → Video

Status: PLANNED  
Decision: EXPERIMENT  
Owner: Murat Project Engineer  
Repository: `Murkin1980/murat-project-engineer`  
External reference: `heygen-com/hyperframes`

## Purpose

Test whether the open-source HyperFrames project can be reused as a bounded video-rendering component for Murat Project Engineer.

The experiment must answer one question:

> Can MPE turn a completed engineering task / GitHub pull request into a short, understandable, deterministic 30–60 second video report without creating a separate video platform?

This experiment is not authorization to build a video SaaS, new repository, persistent rendering service, new control plane, or production publishing pipeline.

## New Idea Filter

Primary disposition: **EXPERIMENT**

### Existing-project fit

The capability belongs to Murat Project Engineer because its value is explaining and reviewing work already performed by MPE/Arena/Codex.

### Reuse

Prefer HyperFrames as an external reusable rendering component. Do not reproduce its rendering engine unless a small compatibility shim is required.

### Duplication check

Do not duplicate:
- MPE task/PR evidence extraction;
- existing GitHub integration;
- existing artifact/evidence formats;
- deployment infrastructure;
- media storage infrastructure;
- orchestration/routing.

### Measurable value hypothesis

A successful result should reduce the human work required to understand a completed PR by producing a concise visual summary that is:
- grounded in the actual PR;
- reproducible;
- easier to review from a phone than reading a long engineering report;
- cheap enough to run as an optional artifact.

No VRU is claimed until a real or production-like PR is rendered and the resulting report is verified useful.

## Scope

Minimum experiment:

```text
existing completed GitHub PR
  -> evidence extraction
  -> concise changelog / narration
  -> structured storyboard
  -> HyperFrames composition
  -> preview
  -> deterministic MP4 render
  -> evidence + evaluation
```

Target duration: approximately 30–60 seconds.

Use one real completed PR from an existing Murat repository as the primary fixture. Prefer a PR with:
- a clear before/after;
- bounded scope;
- meaningful tests/evidence;
- no sensitive data.

If repository policy prevents consuming a live remote PR directly, freeze a minimal local fixture derived from the PR and record its source SHA/URL.

## Non-goals

Do not:
- create a new repository;
- create a general-purpose video editor;
- create a hosted rendering service;
- create a database;
- create auth;
- create a queue/worker platform;
- add automatic social publishing;
- add autonomous background rendering;
- change MPE Router authority;
- replace canonical engineering reports with video;
- make video the source of truth.

The video is a derived presentation artifact only.

## Mandatory startup

Before implementation Arena must read:
1. `AGENTS.md`
2. `docs/governance/SCOPE-CHANGE-CONTROL.md`
3. `docs/NEW_IDEA_FILTER_POLICY.md`
4. `docs/GLOBAL_MPE_ENFORCEMENT.md`
5. `docs/OPINIONATED_WORKSPACE_POLICY.md`
6. `docs/VALUE_UNIT_ECONOMICS.md`
7. this file
8. `ARENA_TASK.md`

Then inspect only the MPE paths required for experiment placement, evidence conventions, GitHub/PR data access, and tests.

## Phase 0 — Baseline / component audit

Read HyperFrames upstream sufficiently to determine:
- license;
- runtime requirements;
- composition model;
- rendering entrypoint;
- deterministic-render constraints;
- headless/browser/media dependencies;
- audio/narration support if any;
- whether MP4 can be produced locally in Arena;
- which pieces can be reused without importing the whole project.

Record:
- upstream commit/tag used;
- required dependency/runtime assumptions;
- any network or binary constraints;
- whether vendoring/copying is necessary.

Do not copy large parts of upstream code during reconnaissance.

## Phase 1 — Freeze one PR fixture

Choose one completed PR from an existing Murat project.

Extract only the minimum facts needed for a viewer to understand:
- project/repository;
- PR title/number;
- problem;
- meaningful changed areas;
- important before/after behavior;
- verification/tests;
- final result;
- remaining limitation if any.

The extraction must remain attributable to actual PR/evidence data.

Do not invent impact claims.

Create a deterministic local fixture when necessary so the experiment remains reproducible.

## Phase 2 — Storyboard contract

Define the smallest stable structured representation between PR evidence and rendering.

Prefer a narrow structure such as:
- title;
- 3–6 scenes;
- scene duration;
- scene headline;
- 1–3 evidence-backed facts;
- optional metric;
- optional code/file label;
- narration text;
- source references.

Avoid designing a generic media DSL.

The storyboard must be inspectable and testable without rendering video.

## Phase 3 — HyperFrames composition

Build only enough composition logic to render the fixture.

Target:
- 16:9;
- 1080p if supported without disproportionate cost;
- 30–60 seconds;
- readable on a phone;
- restrained motion;
- no decorative complexity that obscures the engineering facts.

Prefer existing MPE visual assets/tokens if readily reusable. Do not introduce a new design system.

If voice generation requires an external paid API, do not add it for this experiment. Use text-only or a local/free deterministic alternative.

## Phase 4 — Deterministic render

Attempt:
1. preview;
2. MP4 render;
3. second render from the identical frozen fixture.

Record:
- render command;
- duration;
- output size;
- hashes for deterministic inputs;
- output hashes.

If identical MP4 byte hashes are not realistic because of container metadata, compare the strongest stable representation available (for example frame sequence hashes, normalized metadata, or equivalent) and explain the boundary precisely.

A render blocked solely by Arena sandbox/browser/binary limitations may be PARTIAL rather than FAIL if the component path is otherwise validated.

## Phase 5 — Evaluation

Evaluate against these criteria:

### Grounding
Every material statement in the video is traceable to the selected PR/evidence.

### Comprehension
The viewer can answer:
- what changed;
- why;
- whether verification passed;
- what remains.

### Mobile usefulness
The video/report is practical to review from a smartphone.

### Repeatability
The same frozen input produces materially equivalent output.

### Cost / complexity
The solution does not require new persistent infrastructure.

### Reuse
The PR-evidence → storyboard contract can be reused for other MPE projects without project-specific forks.

## Acceptance

### PASS
A real completed PR is converted into a usable 30–60 second video artifact, grounding is verified, repeatability is demonstrated, and no parallel infrastructure is introduced.

### PARTIAL
The extraction/storyboard/composition path is validated but final video rendering is blocked by an external/sandbox dependency, or one significant acceptance criterion remains unverified.

### FAIL
HyperFrames cannot be reused economically/reliably for this purpose, requires disproportionate infrastructure, or produces a result that is materially less useful than the existing engineering evidence.

## Final adoption decision

Return one:
- ADOPT
- ADOPT_WITH_CHANGES
- DO_NOT_ADOPT

Adoption means only that HyperFrames (or the smallest proven reusable portion) may become an optional MPE reporting component.

It does not authorize production integration.

## Evidence to preserve

Keep experiment-only evidence under this experiment directory unless repository conventions require another existing evidence location.

Minimum:
- upstream version/commit;
- selected PR fixture source;
- frozen extracted evidence;
- storyboard;
- composition/render command;
- preview/render artifact reference if repository-safe;
- verification results;
- limitations;
- final PASS/PARTIAL/FAIL;
- ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT;
- STATE / EVIDENCE / CHANGES / RESULT / BLOCKER / NEXT ACTION / HANDOFF if interrupted.

Do not commit large binaries if repository conventions discourage them; record a reproducible artifact location/hash instead.

## Deep-change stop conditions

Stop and ask the owner before:
- introducing a persistent rendering service;
- adding recurring paid APIs;
- changing production deployment architecture;
- adding a new repository;
- creating new storage/auth/queue infrastructure;
- changing canonical MPE evidence/source-of-truth;
- automatically publishing generated video.

## Completion boundary

This experiment ends after one real PR fixture has been rendered/evaluated and the adoption recommendation is recorded.

Do not continue into productionization without a new owner-authorized checkpoint.
