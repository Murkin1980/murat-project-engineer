# PROMO_BRIEF — Salamat Mebel 2-minute promo (EXP-24 Phase 2 fixture)

Checkpoint: **CP-06** (source → editorial JSON)
Date: 2026-10-08
Experiment: `experiments/exp-24-hyperframes-pr-video/`
Fixture: **Salamat Mebel promo**
Task source: `SALAMAT_PROMO_ARENA_TASK.md` (branch `exp-24-salamat-mebel-promo`, merged into this session branch)
Disposition: **MERGE into EXP-24** — no new repository, service, database, queue or control plane.

---

## 1. Bounded source

The bounded source for this fixture is the owner-supplied promo task itself (`SALAMAT_PROMO_ARENA_TASK.md`,
objective, production rule, business context, editorial structure, duration and claims policy) plus the
existing Salamat Mebel project context already recorded in this repository:

| Source ref | Used for |
| --- | --- |
| `experiments/exp-24-hyperframes-pr-video/SALAMAT_PROMO_ARENA_TASK.md` | objective, mix rule, blocks A–F, claims policy, publishing boundary |
| `docs/evaluations/PERSONALIZED_ASSESSMENT_ENGINE_V0.md` | confirms `salamat-mebel-kz` / `salamat-kitchen-configurator` are existing Salamat Mebel project tracks in this repository's evidence |
| `docs/GLOBAL_MPE_ENFORCEMENT.md` (§ Salamat Projects Dashboard) | confirms the Salamat portfolio observer is read-only; not a data source for public claims |

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
- Tone: premium, contemporary, trustworthy, calm. Not "generic AI ad", not a hard-sell radio spot.
- Narration: mature, unhurried, confident; no announcer exaggeration; no young-startup voice; Russian.
- Music: low-profile premium corporate / architectural mood; narration stays clearly dominant.

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

## 6. Production mix rule (design intent)

| Share | Source | Used for |
| --- | --- | --- |
| 75–80 % | `REAL_FOOTAGE` — Storyblocks (primary) via a provider adapter | manufacturing, CNC/cutting/edgebanding/painting, assembly, installers, kitchens/wardrobes/interiors, consultation/design review, hardware details |
| 20–25 % | `GENERATIVE` / branded motion | logo reveal, brand transitions, text/graphic cards, bridge shots, branded final frame |

People, factory shots, installations and finished furniture must **not** be generated while suitable real
footage is available. If the provider is unavailable, the media plan is still completed and a bounded
fallback is used; the actual delivered mix is reported honestly in `SALAMAT_PROMO_RESULTS.md`.

## 7. Provider plan (adapters, not dependencies)

| Layer | Primary provider | Adapter contract | Fallback |
| --- | --- | --- | --- |
| Footage | Storyblocks | `MEDIA_MANIFEST.json` scene → asset mapping with query, licence note, provenance | local/branded/generated placeholders, `asset_status: BLOCKED_PROVIDER` |
| Voice | ElevenLabs (reference) | `VOICE_MANIFEST.json` provider/model/voice/settings + measured durations | environment `VoiceProvider` (Arena speech), recorded as a distinct provider |
| Music | licensed stock | `MUSIC_MANIFEST.json` track/id/licence/gain | locally synthesized, licence-free bed (`tools/make_music.py`), hash-recorded |
| Render | Remotion | storyboard + manifests → timeline → composition | none required (Remotion is baseline for Phase 2) |

No provider is hard-wired into the storyboard contract: a scene declares *intent* (`visual_source_preference`,
`footage_queries`) and the manifest resolves it.

## 8. Editorial structure (owner-supplied, kept as intent)

| Block | Time | Purpose |
| --- | --- | --- |
| A — Hook | 0–11 s | premium visual impact, brand, one positioning phrase |
| B — What we do | 11–36 s | custom furniture; idea/measurement → finished installation; interiors tailored to the room |
| C — Production & craftsmanship | 36–71 s | materials, cutting/CNC, edge processing, finishing, hardware, assembly (real footage wherever possible) |
| D — Product range | 71–101 s | kitchens; wardrobes/storage; children's/bathroom/TV; commercial — representative shots, no catalogue overload |
| E — Quality + installation | 101–115 s | detail quality, installation, fit/finish, result in the interior |
| F — Brand close / CTA | 115–120 s | logo, concise neutral CTA, no invented contact data |

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
