# REVISION_LOG — Salamat Mebel promo (EXP-24 Phase 2)

Owner-directed revisions and scope corrections, in order. Every entry records the
request, the interpreted change set, what changed, what was intentionally
preserved, and the resulting artifact.

---

## REV-000 — Scope correction: generated stills produced before HARD SCOPE CONTRACT

**Type:** scope correction (owner-added hard contract, 2026-10-08)
**Trigger:** `SALAMAT_PROMO_ARENA_TASK.md` § HARD SCOPE CONTRACT — "Media-source authority",
"Generative media — explicit allowlist only", "No generative fallback for stock failure",
"Maximum generative budget before owner review".
**Detected:** 2026-10-08, during CP-07 (before any preview was assembled or rendered).

### Deviation

Before the hard contract existed on the branch, the media-fallback path generated **10 still
stills** to stand in for Storyblocks footage (`tools/media_assets.py`, provider
`arena-generate-image`). This violates the contract in three ways:

1. it converts blocked stock scenes into generated images (§ No generative fallback for stock failure);
2. 9 of the 10 assets are in **explicitly disallowed categories** (kitchens, interiors, CNC,
   production/workshop, workers/assembly, client consultation, hardware/details, hands on
   materials, measuring);
3. it exceeds the pre-review budget of **3 generated visual assets**.

### Action taken (minimal-diff correction, no restart)

- The generation batch was stopped. No further image or video generation is performed.
- All 10 assets are classified **UNUSED** — none is compliant with the allowlist, so none is preserved
  in the composition, the manifests or the repository working tree.
- Assets were moved out of the tracked tree to
  `.artifacts/exp-24-salamat-promo/unused-generative/` (git-ignored), each with a recorded SHA-256 so
  the deviation stays auditable without shipping non-compliant media:

| # | Asset | SHA-256 (first 16) | Classification | Disallowed category |
| --- | --- | --- | --- | --- |
| 1 | `01-hook-kitchen.png` | `804314954ef40e57` | UNUSED | kitchens / interiors |
| 2 | `02-hook-wide-interior.png` | `d3db5ba76fed9e0a` | UNUSED | interiors |
| 3 | `03-process-measure.png` | `68b3965d764eb9e8` | UNUSED | hands touching furniture/materials (measurement) |
| 4 | `04-measure-consult.png` | `43a3a007c98e967a` | UNUSED | client consultation |
| 5 | `05-materials-samples.png` | `00cb8a9cbf30c4f8` | UNUSED | hardware/detail + hands on materials |
| 6 | `06-craft-panels.png` | `ca956c5bd93a75ee` | UNUSED | furniture production |
| 7 | `07-craft-cnc.png` | `c318b5feeab604e2` | UNUSED | CNC/cutting |
| 8 | `08-craft-edge.png` | `f34f7a01bf9cf1fb` | UNUSED | edgebanding/detail footage |
| 9 | `09-craft-hardware.png` | `64130458c0509566` | UNUSED | hardware/detail footage |
| 10 | `10-craft-assembly.png` | `c11f83c2e91477e6` | UNUSED | workers / assembly |

- `public/assets/img/` (the 1080p JPEG masters derived from those stills) was deleted from the tracked tree.
- No asset was silently normalised: the deviation is recorded here and in `SALAMAT_PROMO_RESULTS.md`.

### Corrected media policy now in force

| Priority | Source | Status in this environment |
| --- | --- | --- |
| 1 | REAL LICENSED VIDEO — **Storyblocks first** | `BLOCKED_PROVIDER` (no credentials, provider host unreachable) — queries + search URLs recorded per scene |
| 2 | other explicitly approved licensed real footage | not available |
| 3 | existing owner/project media | none supplied for this fixture |
| 4 | bounded neutral placeholder, **for pipeline testing only** | in use: per-scene "search slate" cards rendered by Remotion (no imagery, no fake footage) |
| 5 | generative media (allowlist only) | used for **3** branded motion graphics, all in-house Remotion code |

### Generative budget accounting (before owner review)

| Generative asset | Allowlist category | Reason | Kind |
| --- | --- | --- | --- |
| `brand-logo-reveal` | logo reveal | brand opening beat of block A; cannot be stock footage | in-house Remotion motion graphic |
| `brand-transition` | abstract branded transition | single brand wipe between block C and block D; serves as the film's one designed transition | in-house Remotion motion graphic |
| `brand-end-card` | branded end card | closing CTA frame required by block F | in-house Remotion motion graphic |

**Generated imagery count: 0 / 3 budget used. Generated video count: 0.**
No asset #4 will be created without explicit owner authorization.

### Preserved compliant work

- CP-06 storyboard structure, claims policy, block structure, per-scene Storyblocks queries and
  fallback queries, source grounding.
- Contract validator, timeline builder, media/provider adapter scaffolding, Remotion project.
- All of it is provider-neutral: resolving Storyblocks later changes the media manifest only.

### Resume point

Earliest incomplete mandatory checkpoint = **CP-07 (media manifest)**, then CP-08. No later checkpoint
was executed; no preview/render artifact was produced before the manifest existed.

---

## REV-001 — Voice selection (CP-08)

**Type:** owner decision
**Request:** "вариант A — Arena Speech Provider через существующий тонкий адаптер", two Russian male
candidates, mature/calm/confident, no announcer pathos; final voice-over not to be asserted before the choice.
**Interpreted change set:** register one `VoiceProvider` adapter (no new voice service), audition two
candidates, keep the storyboard untouched (narration is the approved script verbatim).
**Changed:** `VOICE_MANIFEST.json` (provider metadata, selected voice, measured durations, hashes);
9 narration clips + one mix under `promo-remotion/public/audio/` (git-ignored, hashed).
**Preserved:** `EDITORIAL_STORYBOARD.json`, `MEDIA_MANIFEST.json`, every scene and query.
**Result:** owner selected **audition Sample 2 → `voice-00`**. Narration total 69.6 s, fits inside every
scene's script timing; the film becomes 122.23 s. Draft status — the owner has not approved a final voice-over.

## REV-002 — No music substitute

**Type:** scope compliance
**Request:** storyboard/voice/preview only; nothing may be fabricated for missing licensed media.
**Interpreted change set:** record the music bed as a provider blocker instead of synthesising one.
**Changed:** `MUSIC_MANIFEST.json`.
**Preserved:** nothing removed — the mix simply has no bed, and `musicGainDb` stays reserved at −21 dB.
**Result:** preview contains narration only (silent after 1:10); the final film requires a licensed track.

---

## REV-003 — Brand-name pronunciation fix (issue #55, CP-08 targeted)

**Type:** owner-reported defect repair (HIGH priority, EXTEND_EXISTING)
**Request:** the selected voice `voice-00` pronounced the brand name with a foreign accent. The name must
sound like ordinary Russian **«Саламат Мебель»**, in context, in the two affected scenes.
**Root cause:** storyboard and script carry the brand as Latin `Salamat Mebel`
(`SALAMAT_PROMO_SCRIPT.md` scenes 6 and 9), and that Latin string was passed straight to TTS, so the
provider read it with English phonetics.

**Interpreted change set (strict minimal diff):**

| Kept unchanged | Changed |
| --- | --- |
| `SALAMAT_PROMO_SCRIPT.md` (narrative source of truth — **not** rewritten to Cyrillic) | TTS input only: `Salamat Mebel` → `Саламат Мебель` |
| visual brand name `SALAMAT MEBEL` and every storyboard overlay | two narration clips: `scene6-brand-fixed.mp3`, `scene9-brand-fixed.mp3` |
| `voice-00` (Sample 2) — no substitute voice | — |
| clips 1–5 and 7–8 (byte-identical, hashes below) | — |
| Remotion composition, timeline, mix, preview — **not rebuilt, awaiting owner approval** | — |

### Files and hashes

| Clip | Duration | SHA-256 | Status |
| --- | --- | --- | --- |
| `scene6.mp3` (old) | 10.606 s | `94955cd80bd7ec12a7d09bf3f5076ea6eba775bd66447734ed2137b422e1bd2b` | **preserved on disk, not replaced** |
| `scene6-brand-fixed.mp3` (new) | 10.501 s | `70e20d0e645f23e9760bfebf67c48cb08c819b2875246c249c66fbe427e1c743` | awaiting owner audio review |
| `scene9.mp3` (old) | 3.709 s | `1066e00385fac48c1300170bb6231b563aa616693bb09941a45cb0267c0da477` | **preserved on disk, not replaced** |
| `scene9-brand-fixed.mp3` (new) | 3.788 s | `9a622b991b2a0a3a64e8172625652a324fff783b924aecaea4d38bb7b6136e80` | awaiting owner audio review |

Unaffected clips re-verified byte-identical (`scene1` `bb1c226b…`, `scene2` `64837c13…`, `scene3`
`b877ebce…`, `scene4` `96f4ca4f…`, `scene5` `053a1a7a…`, `scene7` `61a2b3d8…`, `scene8` `b56603cf…`).

### Pronunciation timestamps (clip-relative, measured by energy-envelope phrase segmentation, 120 ms gaps)

| Clip | Brand-name utterance | Phrase map |
| --- | --- | --- |
| `scene6-brand-fixed.mp3` | **0.06–1.35 s** "Саламат Мебель" (then a pause before «делает кухни…») | 0.06–1.35 · 1.51–1.61 · 1.73–5.27 · 5.39–6.05 · 6.24–7.85 · 8.02–8.42 · 8.56–10.20 |
| `scene9-brand-fixed.mp3` | **0.05–1.02 s** "Саламат Мебель" | 0.05–1.02 · 1.22–3.44 |
| `scene6.mp3` (old) | 0.06–3.42 s — the name ran on without a phrase break | 0.06–3.42 · 3.58–5.38 · 5.50–5.73 · 6.23–7.82 · 8.00–10.22 |
| `scene9.mp3` (old) | 0.04–0.99 s | 0.04–0.99 · 1.20–3.41 |

Acoustic comparison of the first 1.7 s (evidence that the name was re-synthesised, not merely re-encoded):
scene 6 envelope correlation 0.711, first energy peak moved 1.54 s → 0.75 s; scene 9 correlation 0.823.

### Technical verification

| Check | scene 6 (new) | scene 9 (new) |
| --- | --- | --- |
| File exists / decodes | yes, MP3 44.1 kHz mono | yes, MP3 44.1 kHz mono |
| Lead-in silence | 0.061 s | 0.056 s |
| Lead-out silence | 0.278 s | 0.310 s |
| Peak / RMS | 0.811 / 0.1162 | 0.748 / 0.1098 |
| No clipped word at start/end | PASS (non-zero lead-in and lead-out) | PASS |
| Level comparable to the original | 0.1162 vs 0.1138 | 0.1098 vs 0.1114 |
| Full text spoken | duration within 0.1 s of the original clip that carried the same sentence → consistent | 3.79 s vs 3.71 s |

**Not verified by the agent:** audible pronunciation quality. The agent cannot listen to the audio, so
`PRONUNCIATION CHECK = NEEDS OWNER REVIEW`; the acoustic evidence above only proves the name was
re-synthesised as a distinct, bounded utterance.

### Blocker found and fixed while doing this (unrelated to the audio itself)

The tracked branch commit `f10f092` contained **23 generated files** (10 audio clips + 13 render
artifacts) because the `.gitignore` patterns `promo-remotion/…` are anchored to the repository root and
never matched the experiment subdirectory. Fixed in `602b8a5`: patterns re-anchored as
`**/promo-remotion/{out,node_modules,public/audio}/`, the 23 files untracked (still on disk), verified
0 media files tracked inside EXP-24. This also restores compliance with "no binary audio in Git".

### Deferred until the owner approves the pronunciation

1. rebuild the narration mix (`narration-ru-salamat-mebel.mp3`) with the two fixed clips;
2. update `VOICE_MANIFEST.json` durations/hashes for scenes 6 and 9;
3. re-run `tools/build_timeline.py` (scene 6 shortens by 0.105 s, scene 9 lengthens by 0.079 s);
4. regenerate the technical preview.

Not executed: CP-10…CP-12, full video render, any publishing.
