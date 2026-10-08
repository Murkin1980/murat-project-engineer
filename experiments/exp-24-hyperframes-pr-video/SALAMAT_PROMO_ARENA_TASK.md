# Arena Task — EXP-24 Salamat Mebel Promo

Decision: **MERGE into EXP-24**  
Branch: `exp-24-salamat-mebel-promo`  
Repository: `Murkin1980/murat-project-engineer`  
Experiment: `experiments/exp-24-hyperframes-pr-video/`  
Fixture: **Salamat Mebel 2-minute promo**



## HARD SCOPE CONTRACT — AUTHORITATIVE

This section overrides any ambiguous wording elsewhere in this task.

### Interpretation rule

**If an action is not explicitly allowed by this task, do not perform it.**

Do not infer permission from:
- a desired final result;
- tool availability;
- convenience;
- quota availability;
- prior habits;
- a generated plan;
- a model suggestion;
- an available API;
- the existence of an image/video generation tool.

When uncertain, choose the narrower action and preserve a blocker/handoff instead of expanding scope.

### Ordered checkpoint gate

Execution order is mandatory:

```text
CP-06 storyboard
THEN owner-reviewable artifact exists
THEN CP-07 stock/media search
THEN media manifest exists
THEN CP-08 voice/music
THEN CP-09 assembly
THEN CP-10 mobile QA
THEN CP-11 revisions
THEN CP-12 final render
```

Do not execute a later checkpoint before the required artifacts of the previous checkpoint exist in the repository.

### Media-source authority

For all ordinary visual scenes, the source priority is mandatory:

1. **REAL LICENSED VIDEO FOOTAGE — Storyblocks first**
2. other explicitly approved licensed real footage
3. existing owner/project media
4. bounded placeholder for pipeline testing
5. generative media only where explicitly allowed below

Do not reorder this priority.

### Generative media — explicit allowlist only

Generative media is allowed only for:
- logo reveal;
- abstract branded transition;
- simple diagram/graphic;
- branded end card;
- visual bridge that cannot reasonably be sourced as real footage.

Generative media is **not allowed** for:
- furniture production;
- CNC/cutting/edgebanding;
- workers or craftspeople;
- client consultation;
- installation;
- kitchens;
- wardrobes;
- finished furniture;
- interiors;
- hands touching furniture/materials;
- countertop tactile shot;
- hardware/detail footage;
- any scene for which suitable real stock footage can reasonably exist.

Do not generate an image/video for a disallowed category even if Storyblocks access is blocked.

### No generative fallback for stock failure

If Storyblocks search/auth/download is blocked:

- complete the storyboard;
- complete Storyblocks search queries;
- complete the media manifest with unresolved assets;
- record the exact blocker;
- use neutral local/test placeholders only when necessary to prove assembly;
- mark the checkpoint PARTIAL if required.

**Do not convert blocked stock scenes into generated images or generated video.**

### No quota-driven production

Never generate media merely because:
- a previous plan mentioned N assets;
- a quota remains;
- a batch has already started;
- the tool can generate more;
- a scene count exists.

Asset count is not a target.

Generate only an explicitly permitted asset that is required by the approved storyboard.

### Maximum generative budget before owner review

Before the owner reviews the first assembled preview:
- maximum **3 generated visual assets total**;
- each must map to an allowed generative category;
- each must be listed in `MEDIA_MANIFEST.json` with reason for generation.

Do not generate asset #4 without explicit owner authorization.

### Real-video rule

The core promo must remain motion-video-first.

Static generated images must not become the main visual language and must not be used as substitutes for stock video across consecutive ordinary scenes.

### Minimal-diff correction rule

If this hard scope is added after work has already begun:
- do not restart automatically;
- classify already produced assets as KEEP / REVIEW / UNUSED;
- preserve only assets compliant with this contract;
- continue from the earliest incomplete mandatory checkpoint.

### Mandatory self-check before every media action

Before acquiring or generating any visual asset, answer internally:

1. Which scene requires this asset?
2. Is this scene allowed to use generative media?
3. Has Storyblocks-first search already been completed for this scene?
4. Is this asset recorded/planned in MEDIA_MANIFEST?
5. Does this action keep generated visual assets within the allowed budget?

If any answer is NO, do not perform the media action.

### Scope violation handling

If any prior step violated this contract:
- stop the violating activity;
- do not continue the batch;
- record the deviation in `REVISION_LOG.md` or handoff evidence;
- preserve useful compliant outputs;
- resume from the correct checkpoint.

Do not hide or silently normalize the deviation.


## Objective

Create the first production-like Phase 2 fixture for EXP-24:

```text
Salamat Mebel promo brief
→ editorial script/storyboard
→ Storyblocks-first media plan
→ voice/music plan
→ Remotion assembly
→ mobile QA
→ natural-language revision loop
→ final 2-minute promo render
```

The purpose is not to build a video platform. The purpose is to prove that an agent can manage most of a real promo-video production workflow while the owner reviews meaning, brand fit and quality.

## Production rule

Target mix:

- **75–80% REAL_FOOTAGE**
  - Storyblocks or equivalent licensed stock footage
  - furniture manufacturing
  - CNC/cutting/edgebanding/painting/assembly
  - installers
  - kitchens/wardrobes/interiors
  - client consultation / design review
  - hardware/detail shots
- **20–25% GENERATIVE / MOTION**
  - Salamat Mebel logo reveal
  - brand transitions
  - simple diagrams / text graphics
  - tasteful visual bridge shots where stock footage does not fit
  - optional branded final frame

Do **not** generate people, factory shots, installations or finished furniture if suitable real footage is available.

## Business context to reflect

Salamat Mebel:
- custom case furniture;
- kitchens;
- wardrobes / built-in storage;
- hallways;
- children’s furniture;
- TV units;
- bathroom cabinetry;
- reception / office / medical / commercial furniture;
- quality materials and hardware;
- project-to-installation workflow;
- premium positioning;
- Almaty / Almaty region focus.

Do not invent certifications, production volumes, warranty terms, delivery times, addresses, phone numbers, awards or client counts unless they are already verified in repository/project evidence.

## Target audience

Primary:
- homeowner / apartment owner;
- customer considering custom kitchen or built-in furniture.

Secondary:
- small business / retail / office customer.

The film must feel premium, contemporary and trustworthy, not like a generic AI-generated ad.

## Duration

Target: **110–125 seconds**.

Do not exceed 130 seconds unless required to preserve approved narration.

## Editorial structure

Use this as a starting structure, not as immutable wording:

### Scene block A — Hook (0–10 sec)
Purpose:
- immediate premium visual impact;
- Salamat Mebel name/logo;
- one concise positioning phrase.

### Scene block B — What we do (10–35 sec)
Purpose:
- custom furniture;
- from idea and measurements to finished installation;
- interiors tailored to the actual room and customer task.

### Scene block C — Production and craftsmanship (35–70 sec)
Purpose:
- material selection;
- cutting/CNC;
- edge processing;
- painting/finishing where relevant;
- hardware/details;
- assembly.

Use real footage wherever possible.

### Scene block D — Product range (70–100 sec)
Purpose:
- kitchens;
- wardrobes/storage;
- children’s / bathroom / TV units;
- commercial furniture.

Avoid rapid catalog-style overload. Show categories through strong representative shots.

### Scene block E — Quality + installation (100–115 sec)
Purpose:
- detail quality;
- installation;
- fit/finish;
- result in the interior.

### Scene block F — Brand close / CTA (115–120 sec)
Purpose:
- logo;
- concise call to action;
- no invented contact data.

If verified contact information is unavailable, use a neutral CTA such as:
“Salamat Mebel — мебель, созданная под ваше пространство.”

## CP-06 — Promo brief + editorial storyboard

Create:

- `PROMO_BRIEF.md`
- `EDITORIAL_STORYBOARD.json`

Storyboard requirements per scene:
- id;
- order;
- target duration;
- narration;
- editorial purpose;
- visual intent;
- real-footage vs generative preference;
- Storyblocks search queries;
- fallback queries;
- title/overlay text;
- source/business grounding;
- approval notes.

Target 12–18 scenes.

Do not acquire media before the storyboard is readable and internally coherent.

## CP-07 — Media plan / acquisition

Create:

- `MEDIA_MANIFEST.json`

For each scene record:
- asset source/provider;
- asset URL/id if available;
- license/usage note;
- search query that found it;
- scene mapping;
- selected in/out intent;
- whether it is REAL_FOOTAGE or GENERATIVE;
- fallback asset/query.

Preferred source: **Storyblocks**.

If Storyblocks authentication is unavailable:
- complete the media plan and queries;
- use local/test placeholders only as a bounded fallback;
- record the exact auth blocker;
- do not switch the architecture to a different provider just to finish quickly.

Avoid repeated stock clips and obvious visual duplication.

## CP-08 — Voice and music

Voice:
- Russian by default unless the owner explicitly selects another language;
- mature, calm, confident;
- no “radio announcer” exaggeration;
- no overly young startup voice;
- natural pacing.

Use a provider adapter. ElevenLabs is preferred if available.

Create:
- voice metadata;
- provider/model/voice id;
- pacing/speed/settings;
- narration asset path/reference.

Music:
- low-profile premium corporate / architectural / craftsmanship mood;
- narration remains clearly dominant;
- no aggressive trailer music.

Record:
- provider/source;
- track id;
- license note;
- gain/mix setting.

## CP-09 — Remotion assembly

Use Remotion as the preferred compositor.

Required:
- 16:9;
- 1920×1080 target;
- clean branded typography;
- restrained transitions;
- no template-like over-animation;
- titles large enough for mobile;
- subtitles supported from the start;
- audio levels normalized;
- scene timing derived from storyboard/voice, not arbitrary hardcoding.

HyperFrames is optional and must not block execution.

Create a preview before final render.

## CP-10 — Mobile QA

Test at effective 360 px player width.

Mandatory checks:
- subtitle lines <= 2;
- readable title size;
- no clipped text;
- no text outside safe areas;
- no tiny debug/service text;
- key brand statements remain readable;
- subtitles do not cover important furniture details/faces/hands where avoidable;
- CTA readable in final frame.

Preserve representative screenshots/frames and a machine-readable QA result.

## CP-11 — Natural-language revision proof

Apply at least these three owner-style revisions:

1. “На телефоне текст мелкий — сделай крупнее.”
2. “Кадры не должны повторяться — замени повторы.”
3. “Сделай голос взрослее/спокойнее, остальные одобренные части не трогай.”

For each revision record:
- input request;
- interpreted change set;
- files/scenes changed;
- files/scenes intentionally preserved;
- new preview result.

Goal: prove minimal-diff behavior.

## CP-12 — Final render

Final artifact target:
- 1080p MP4;
- 110–125 sec;
- approved narration;
- licensed/traceable assets;
- mobile-readable text;
- no unresolved placeholder media;
- no unapproved public upload.

Record:
- render command;
- duration;
- file size;
- hash;
- provider costs/credits if visible;
- final QA result.

## Publishing boundary

Do **not** upload to YouTube, Instagram, TikTok, Facebook or any public channel unless the owner explicitly authorizes that exact upload after reviewing the final render.

You may prepare a publish manifest/template, but do not execute publishing.

## Required outputs

Under:
`experiments/exp-24-hyperframes-pr-video/`

Create/update:

- `PROMO_BRIEF.md`
- `EDITORIAL_STORYBOARD.json`
- `MEDIA_MANIFEST.json`
- `VOICE_MANIFEST.json` (or equivalent)
- `MUSIC_MANIFEST.json` (or equivalent)
- `MOBILE_QA.md`
- `REVISION_LOG.md`
- Remotion composition source
- `SALAMAT_PROMO_RESULTS.md`

Do not overwrite the Phase 1 terminal result in `RESULTS.md`.

## Terminal result

`SALAMAT_PROMO_RESULTS.md` must report:

- RESULT: PASS / PARTIAL / FAIL
- ADOPTION: ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT
- duration
- footage mix actual %
- Storyblocks usage
- generated media usage
- voice provider
- music provider
- Remotion render status
- mobile QA
- natural-language revision results
- cost/credits if known
- blockers
- changed files
- artifact/hash
- next action

## PASS

PASS only when:
- a real 2-minute promo is rendered;
- most footage is real/licensed stock;
- generated content is used selectively;
- storyboard/media provenance is preserved;
- mobile QA passes;
- at least one revision round succeeds with minimal-diff behavior;
- no parallel video infrastructure is introduced.

## PARTIAL

PARTIAL when:
- storyboard/media/voice/Remotion path is validated;
- but a provider auth/credit/runtime blocker prevents a finished render;
- or one major acceptance gate remains unverified.

## FAIL

FAIL when:
- the workflow still requires substantial manual timeline editing;
- stock selection cannot be made reliably enough;
- provenance cannot be maintained;
- natural-language revisions cause broad uncontrolled changes;
- or the result is materially worse than a simple manual editor workflow.

## Stop / deep-change gates

Stop and ask the owner before:
- new repository;
- persistent video service;
- database/queue/control plane;
- mandatory paid-provider dependency;
- automatic publishing;
- use of unlicensed third-party assets;
- production changes outside EXP-24;
- changing Salamat Mebel public claims beyond verified evidence.

## Execution discipline

1. Read existing EXP-24 README/ARENA_TASK/RESULTS first.
2. Preserve Phase 1 evidence.
3. Work only on branch `exp-24-salamat-mebel-promo`.
4. Start at CP-06.
5. Persist outputs after every checkpoint.
6. Do not wait for perfect provider access before producing the reviewable storyboard/media plan.
7. Prefer the smallest reproducible working pipeline over infrastructure work.
8. Stop after the terminal result is recorded.
