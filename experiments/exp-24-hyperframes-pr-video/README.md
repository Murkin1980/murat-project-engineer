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


---

# Owner-authorized Phase 2 — Agentic text → film pipeline

Authorized: 2026-10-08  
New Idea Filter disposition: **MERGE**  
Reference case: https://alexeykrol.com/blog/2026/10/07/video1/

## Why EXP-24 is being extended

The Phase 1 HyperFrames run remains valid historical evidence: **PARTIAL / ADOPT_WITH_CHANGES**. It proved the PR-evidence → storyboard → composition path, but rendering was blocked by the Arena runtime.

The owner has now supplied a stronger production reference: an agent receives source text and manages the production chain from semantic breakdown and storyboard through stock-footage search, voice, music, subtitles, programmatic editing, mobile-readability revisions, final render and publication.

Therefore EXP-24 is no longer centered on HyperFrames. HyperFrames becomes one optional renderer/component candidate.

The experiment's new question is:

> Can MPE/Arena turn an existing text or structured source into a reviewable, agent-managed film through a stable storyboard contract, pluggable media/voice/render adapters, deterministic assembly, mobile QA, and natural-language revision—without creating a parallel video platform?

## Updated target architecture

```text
source text / article / script / PR evidence
  -> semantic/editorial breakdown
  -> EDITORIAL_STORYBOARD.json
  -> visual intent + footage queries
  -> media adapter
       -> stock footage
       -> generated footage
       -> local/project assets
  -> voice adapter
  -> music/audio mix
  -> Remotion-first assembly adapter
       -> HyperFrames optional
  -> subtitles + titles + graphics
  -> mobile QA / acceptance
  -> preview
  -> natural-language revision loop
  -> final render
  -> optional publish adapter
```

## Reuse rule

Reuse the Phase 1 fixture/storyboard/evidence where useful. Do not create another video repository, database, queue, control plane or media platform.

Provider-specific code must sit behind narrow adapters. Storyblocks and ElevenLabs are useful reference providers, not mandatory dependencies.

## Two intended modes

### REAL_FOOTAGE
For articles, business explanations, educational material, case studies, Murat House and marketing/reporting content. Prefer licensed stock or existing project assets when realism is more valuable than generated imagery.

### GENERATIVE
For AI-serial and other synthetic visual work. The storyboard, narration, subtitle, assembly, QA and revision layers remain shared; only the visual-source adapter changes.

## Phase 2 checkpoints

### CP-06 — Source → Editorial JSON
Convert one bounded source into structured scenes containing:
- scene id/order;
- narration;
- editorial purpose;
- visual intent;
- footage search queries;
- titles/graphics;
- estimated duration;
- source grounding.

PASS requires a human-reviewable storyboard before any expensive media/render step.

### CP-07 — Media acquisition adapter
Resolve scene media through a provider-neutral contract.

Start with local/free/test assets if credentials or licensing are unavailable. Record provider, asset id/source, license/usage note and scene mapping.

Storyblocks may be tested when the owner's connected account is available, but it is not architecture authority.

### CP-08 — Voice adapter
Create narration through a narrow `VoiceProvider` contract.

ElevenLabs is the preferred reference provider when credentials/credits are available. Preserve voice/model/settings metadata sufficient to reproduce the run. A local/test voice is acceptable for pipeline validation.

### CP-09 — Programmatic assembly
Use **Remotion as the preferred baseline compositor** for Phase 2 because it gives the agent direct control over timing, footage, titles, graphics, subtitles, music and repeatable code changes.

HyperFrames remains an optional alternative/component; do not force it into the critical path.

PASS requires one preview generated from the frozen storyboard and media manifest.

### CP-10 — Mobile QA
Treat mobile readability as an acceptance test, not a subjective afterthought.

At minimum verify at an effective 360 px player width:
- titles and key labels remain readable;
- subtitles are broken into short phrases with no more than two lines;
- no critical text is outside safe areas;
- no obvious overflow/clipping;
- no tiny service/debug text;
- visual hierarchy survives downscaling.

Automate what can be checked deterministically; preserve screenshots/frames where useful.

### CP-11 — Natural-language revision loop
Test at least three plain-language edits such as:
- “text is too small on a phone”;
- “this footage repeats”;
- “make the voice older/slower”;
- “replace scene 7 but keep narration”.

The agent must translate the request into bounded project changes, preserve unaffected approved assets where appropriate, and emit a new preview.

### CP-12 — Final render and publish boundary
Produce a final render only after CP-06…CP-11 are accepted.

Publishing (for example YouTube upload) is a separate adapter and remains approval-gated. Do not auto-publish during the experiment unless the owner explicitly authorizes that exact action.

## Phase 2 acceptance

### PASS
One source is converted end-to-end into a useful film with:
- reviewable editorial storyboard;
- traceable media;
- narration/audio;
- programmatic composition;
- mobile acceptance checks;
- at least one successful natural-language revision;
- final render;
- no parallel platform/infrastructure.

### PARTIAL
The core contracts and preview/revision path work, but one external provider/render/publish dependency blocks final completion.

### FAIL
The agentic approach requires disproportionate manual production work, cannot keep source/media provenance, or becomes materially less controllable than a normal lightweight editing workflow.

## Deep-change stop conditions for Phase 2

Stop and request explicit owner approval before:
- creating a new repository or persistent video service;
- introducing a database/queue/control plane;
- making a paid provider mandatory across projects;
- changing MPE/Arena authority boundaries;
- changing AI-serial canon automatically;
- publishing publicly without explicit authorization;
- storing third-party licensed media outside permitted terms.

## Phase 2 priority

The smallest useful proof is **one source → storyboard → media/voice → Remotion preview → mobile QA → natural-language revision → final render**.

Do not optimize for a five-minute film first. Prove control and repeatability on the smallest source that exercises the pipeline.
