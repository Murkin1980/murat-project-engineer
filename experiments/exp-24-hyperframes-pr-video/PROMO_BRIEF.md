# PROMO_BRIEF — Salamat Mebel 2-minute promo (EXP-24 Phase 2 fixture)

Checkpoint: **CP-06** (source → editorial JSON)
Date: 2026-10-08
Experiment: `experiments/exp-24-hyperframes-pr-video/`
Fixture: **Salamat Mebel promo**
Task source: `SALAMAT_PROMO_ARENA_TASK.md` (branch `exp-24-salamat-mebel-promo`, merged into this session branch)
Disposition: **MERGE into EXP-24** — no new repository, service, database, queue or control plane.

---

## 1. Bounded source

**Narrative source-of-truth: `SALAMAT_PROMO_SCRIPT.md`** (owner-approved baseline script, 9 scenes,
0:00–2:00). CP-06 transforms that script into a shot-level storyboard; it does not create a new concept.

| Source ref | Used for |
| --- | --- |
| `SALAMAT_PROMO_SCRIPT.md` | **narrative source of truth** — scene intent, narration wording, on-screen text, timecodes, mandatory tactile countertop shot |
| `SALAMAT_PROMO_ARENA_TASK.md` | HARD SCOPE CONTRACT (checkpoint order, media-source authority, generative allowlist and budget), business context, claims policy, publishing boundary |
| `SALAMAT_PROMO_OWNER_NOTES.md` | mandatory tactile countertop shot and its narration meaning |
| `docs/evaluations/PERSONALIZED_ASSESSMENT_ENGINE_V0.md` | confirms `salamat-mebel-kz` / `salamat-kitchen-configurator` are existing Salamat Mebel project tracks in this repository's evidence |
| `docs/GLOBAL_MPE_ENFORCEMENT.md` (§ Salamat Projects Dashboard) | confirms the Salamat portfolio observer is read-only; not a data source for public claims |

Narration wording may be adapted **only** for voice timing, subtitle readability, natural speech or scene
timing — meaning and scene intent are preserved. `promo-remotion/tools/build_storyboard_from_script.py`
enforces this mechanically: the shot narration parts must reproduce the script narration verbatim, shot
durations must sum to the script's own timecodes, and no overlay may contain text that is not in the
script's approved on-screen text. A mismatch aborts the build.

No live Salamat Mebel website, catalogue, price list, contact data or client data was read for this fixture.
Everything in the film is limited to the business context explicitly authorized in the task.

## 2. Film identity

| Field | Value |
| --- | --- |
| Working title | `Salamat Mebel — мебель, созданная под ваше пространство` |
| Language | Russian (narration + on-screen text) |
| Format | 16:9, 1920×1080, 30 fps |
| Target duration | 120 s (accepted range 110–125 s, hard cap 130 s) |
| Mode | `REAL_FOOTAGE` first (stock/branded), with a bounded generative fallback |
| Review surface | phone first (360 px effective width), then desktop |

## 3. Audience and tone

- Primary: homeowner / apartment owner considering a custom kitchen or built-in furniture.
- Secondary: small business / retail / office customer (reception, office, medical, commercial furniture).
- Tone: premium, contemporary, tactile, trustworthy, calm — explicitly **not** a generic AI advertisement.
- Narration: mature, unhurried, confident; no announcer exaggeration; no young-startup voice; Russian.
- Music: low-profile premium corporate / architectural mood; narration stays clearly dominant.
- Central brand idea (script): *Мы проектируем мебель не вокруг каталога, а вокруг вашего пространства.*

## 4. Business context the film may reflect

Custom case furniture (корпусная мебель на заказ):
kitchens · wardrobes / built-in storage · hallways · children's furniture · TV units · bathroom cabinetry ·
reception / office / medical / commercial furniture · project-to-installation workflow ·
quality materials and hardware · premium positioning · Almaty / Almaty region focus.

## 5. Claims policy (hard constraint)

**Allowed** (given by the owner in the task's business context):
- custom case furniture, kitchens, wardrobes/built-in storage, hallways, children's furniture, TV units,
  bathroom cabinetry, commercial/reception/medical furniture;
- quality materials and hardware; project → installation workflow; premium positioning;
- Almaty / Almaty region focus;
- process statements (measurement, design, production, assembly, delivery, installation) stated as *process*, not as guarantees.

**Forbidden** (do not invent): certifications, production volumes/capacity, warranty terms, delivery times,
addresses, phone numbers, e-mail, awards, client counts, years on the market, price levels, "the best/#1"
superlatives, named partners or suppliers, medical/office compliance claims.

**CTA**: no verified contact data is available to this experiment, therefore the neutral CTA
«Salamat Mebel — мебель, созданная под ваше пространство.» is used and no contact block is rendered.

Every narration line and overlay in `EDITORIAL_STORYBOARD.json` carries a `source_grounding` list.
A validator (`promo-remotion/tools/validate_contracts.py`) fails the build if a scene is missing grounding.

## 6. Media policy (HARD SCOPE CONTRACT)

**Media-source authority — mandatory, do not reorder:**

1. **REAL LICENSED VIDEO FOOTAGE — Storyblocks first** (every ordinary scene);
2. other explicitly approved licensed real footage;
3. existing owner/project media;
4. bounded neutral placeholder — pipeline testing only;
5. generative media — **allowlist only**.

Generative media is allowed for: logo reveal · abstract branded transition · simple diagram/graphic ·
branded end card · a visual bridge with no reasonable real source. It is **not** allowed for furniture
production, CNC/cutting/edgebanding, workers or craftspeople, client consultation, installation,
kitchens, wardrobes, finished furniture, interiors, hands touching furniture or materials, the
countertop tactile shot, hardware/detail footage, or any scene for which real stock can reasonably exist.

**If Storyblocks is blocked:** complete the storyboard, complete the search queries, complete the media
manifest with unresolved assets, record the exact blocker, and use neutral test placeholders only where
needed to prove assembly — mark the checkpoint PARTIAL. **Never convert a blocked stock scene into
generated imagery.** Generated visual assets before owner review: **maximum 3**.

**Real-video rule:** the promo stays motion-first. Static imagery must not become the main visual
language or stand in for stock video across consecutive ordinary scenes.

## 7. Provider plan (adapters, not dependencies)

| Layer | Primary provider | Adapter contract | Fallback |
| --- | --- | --- | --- |
| Footage | Storyblocks | `MEDIA_MANIFEST.json` scene → asset mapping with query, licence note, provenance | local/branded/generated placeholders, `asset_status: BLOCKED_PROVIDER` |
| Voice | ElevenLabs (reference) | `VOICE_MANIFEST.json` provider/model/voice/settings + measured durations | environment `VoiceProvider` (Arena speech), recorded as a distinct provider |
| Music | licensed stock | `MUSIC_MANIFEST.json` track/id/licence/gain | locally synthesized, licence-free bed (`tools/make_music.py`), hash-recorded |
| Render | Remotion | storyboard + manifests → timeline → composition | none required (Remotion is baseline for Phase 2) |

No provider is hard-wired into the storyboard contract: a scene declares *intent* (`visual_source_preference`,
`footage_queries`) and the manifest resolves it.

## 8. Editorial structure (from the owner script)

The shot-level storyboard is generated from `SALAMAT_PROMO_SCRIPT.md`; the script's own timecodes are
authoritative and the film is **120 s**:

| Script scene | Timecode | Shots | Notes |
| --- | --- | --- | --- |
| 1 Opening | 0:00–0:08 | 2 | interior first, wordmark second |
| 2 Not ready-made furniture, but a solution | 0:08–0:22 | 2 | measurement + client discussion |
| 3 Project | 0:22–0:36 | 2 | drawings + material selection |
| 4 Production | 0:36–0:55 | 3 | cutting → processing → assembly |
| 5 Materials and tactile quality | 0:55–1:08 | 2 | **mandatory tactile hero shot**, real footage only |
| 6 What we make | 1:08–1:27 | 3 | kitchen/storage · home rooms · commercial |
| 7 Installation | 1:27–1:42 | 2 | fitting + adjustment |
| 8 Result | 1:42–1:53 | 1 | no overlay copy |
| 9 Brand close | 1:53–2:00 | 1 | branded end card, neutral CTA |

## 9. Acceptance gates carried into this fixture

1. reviewable storyboard before any expensive media/render step (CP-06);
2. traceable media provenance per scene (CP-07);
3. narration through a `VoiceProvider` adapter with reproducibility metadata (CP-08);
4. Remotion preview from the frozen contracts (CP-09);
5. mobile QA at 360 px effective width, machine-readable + representative frames (CP-10);
6. ≥ 3 natural-language revisions with minimal-diff behaviour (CP-11);
7. final 1080p render, publish **not** executed (CP-12).

## 10. Approval notes / open questions for the owner

- **Owner review requested (CP-06):** Russian narration wording, brand CTA line, and whether the film may
  imply "собственное производство" — this brief keeps production as a *process the customer sees*
  (раскрой, ЧПУ, кромка, сборка) without claiming plant size, capacity or ownership.
- **Provider authorization:** no Storyblocks or ElevenLabs credentials are present in this execution
  environment; the media plan is therefore delivered as a Storyblocks-ready manifest with a bounded fallback.
  Supplying credentials later re-resolves the same manifest without storyboard changes.
- **Publishing:** explicitly out of scope. No upload, no link sharing outside the review surface.
