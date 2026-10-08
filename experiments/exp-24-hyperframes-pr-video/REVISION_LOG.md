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

---

## REV-004 — Owner approval of the corrected voice clips (issue #55)

**Type:** owner decision (approval)
**Request:** "Owner has approved both corrected voice clips" → mark `scene6-brand-fixed.mp3` and
`scene9-brand-fixed.mp3` as `OWNER_APPROVED`, replace only the corresponding scene audio in the mix, update
`VOICE_MANIFEST.json`, verify hashes and timing, preserve all other approved clips.
**Changed:** `VOICE_MANIFEST.json` — `owner_review` (decision, date, approved hashes and durations, statement),
`approval` block per clip group, and per-clip `approval` / `artifact_present` fields.
**Preserved:** script, storyboard, composition, provider choice (`voice-00`), every other clip's hash record.
**Result:** approval registered; **mix rebuild could not be executed** — see REV-005.

## REV-005 — Approved audio artifacts lost in a sandbox reset (BLOCKED_RESTORE)

**Type:** environment loss / blocker
**Detected:** 2026-10-08, at the start of the media-integration task.
**What happened:** the execution sandbox restarted and reset the working tree to the branch base
(`95f7eb4`). Audio and render artifacts are deliberately **not** committed to git (owner rule: no binary
audio in the repository), so all 11 audio files and the preview MP4 were lost. The text artifacts survived
and the commits were restored from `origin` (`773c675`).
**Evidence:**

| Artifact | Expected hash (recorded) | State now |
| --- | --- | --- |
| `scene6-brand-fixed.mp3` | `70e20d0e645f23e9760bfebf67c48cb08c819b2875246c249c66fbe427e1c743` | MISSING |
| `scene9-brand-fixed.mp3` | `9a622b991b2a0a3a64e8172625652a324fff783b924aecaea4d38bb7b6136e80` | MISSING |
| `scene1..5,7,8.mp3` | `bb1c226b…`, `64837c13…`, `b877ebce…`, `96f4ca4f…`, `053a1a7a…`, `61a2b3d8…`, `b56603cf…` | MISSING |
| `narration-ru-salamat-mebel.mp3` | `98ce2c638fdbb5666c6c6495…` (pre-correction mix) | MISSING |
| `preview-salamat-mebel-v1.mp4` | `50f4bece0d4a09285a53cc34a4e254e7…` | MISSING |

**Recoverable from git:** no — the corrected clips were created after the last audio-bearing commit and were
never committed; the tracked copies in `f10f092` were the superseded pre-correction files.
**Action taken:** approval recorded, artifact state recorded in `VOICE_MANIFEST.json`
(`artifact_state`, `mix_state`), nothing regenerated, no substitute inserted, no mix rebuilt.
**Why regeneration was not performed:** the owner's approval applies to specific audited bytes; regenerating
would silently replace approved audio with material the owner has not heard, and the other seven clips were
explicitly ordered not to be regenerated. The narrower action is the blocker.
**Restore options:** (A) owner attaches the two approved MP3 files to the chat — exact bytes return;
(B) owner authorises regeneration with `voice-00` and the same Cyrillic text — new hashes and a further
listening check.
**Blocked until restored:** mix rebuild · manifest duration/hash refresh for scenes 6 and 9 · timeline re-run ·
preview regeneration. CP-10…CP-12 remain not started either way.

## REV-006 — Owner Instagram portfolio becomes the first media source (issue: media integration)

**Type:** owner-directed media-source change (EXTEND_EXISTING)
**Request:** the profile `https://www.instagram.com/salamat_mebelkz/` is the designated Salamat Mebel
portfolio source; for finished furniture and portfolio scenes the priority becomes owner originals →
owner Instagram media → licensed stock → neutral placeholders, while workshop/CNC beats stay Storyblocks-first.
**Changed:** `OWNER_MEDIA_SHORTLIST.json` (new — requests, scene mapping, submission paths, rights notes),
`INSTAGRAM_MEDIA_AUDIT.md` (new — access audit), `MEDIA_MANIFEST.json` (each asset now carries
`source_priority` and `owner_source` with provider `OWNER_INSTAGRAM`, profile URL, category, availability and
review status), `tools/resolve_media.py` (reads the shortlist; ~15 lines).
**Preserved:** script, storyboard beats, scene structure, brand meaning, Storyblocks requests for the seven
workshop/process beats, the two branded motion graphics, the 3-asset generative budget.
**Result:** 12 of 17 stock-request beats now prefer owner material (10 explicitly need owner upload);
0 owner assets resolved because access is blocked.
**Blocker:** `BLOCKED_OWNER_MEDIA_ACCESS` — Instagram is unreachable from this runtime (HTTP 000 on four
hosts while DNS resolves), no credentials exist, and Arena provides no Instagram connector. Nothing was
scraped, no authentication was bypassed, and no candidate was invented.
**Next:** owner review of the shortlist — attach originals (preferred) or point the pipeline at a reachable
copy (e.g. a GitHub release asset).

## REV-007 — Render verification of the compressed composition + two defects recorded for CP-10

**Type:** verification (no behaviour change intended) + defect record
**Why:** the LOC compression of `src/Promo.tsx` (REV-006, style hoisting only) had to be proven
layout-neutral before it was trusted.
**How verified:** reinstalled the toolchain after the sandbox reset (npm install; Chromium re-extracted to
`/tmp/chromium` with `LD_LIBRARY_PATH=/tmp/al2023/lib`), bundled the TSX with esbuild (clean), then rendered
one frame: `npx remotion still src/index.ts SalamatPromo out/verify-frame.png --frame=1800`.
**Result:** the composition renders; the style hoisting is visually neutral.

**Two defects found in that frame — NOT fixed here, recorded for CP-10:**

1. **Captions re-wrap in the browser → more than two visual lines.** `tools/build_timeline.py` wraps captions
   at 44 characters per line, but a 112 px caption inside `maxWidth: 1560` fits only ~26–28 characters. The
   browser therefore re-wraps each prepared line, so the beat at 60.0 s (`tactile-hero`) renders four visual
   lines instead of two. Requirement affected: "subtitles ≤ 2 lines".
2. **Slate content and captions collide.** On placeholder beats the slate text is vertically centred while the
   caption block is bottom-anchored and grows upward; with extra wrapped lines the two overlap and both become
   hard to read (visible in the same frame).

**Correction of an earlier claim:** `SALAMAT_PROMO_RESULTS.md` previously recorded "captions 1–2 lines
(measured)" — that measurement was taken from `timeline.json` data and did not account for browser
re-wrap. The data claim was true; the rendered claim was not. It is corrected there.
**Not fixed now because:** the fix belongs to CP-10 (mobile acceptance), and CP-10 may not run while the media
blockers are open. Suggested fix, for when it is authorised: set the caption budget to ~28 characters at
112 px (or reduce caption font / widen the box) and reserve a caption band that slate layouts keep clear.

## REV-008 — Partial audio restore: 7 of 9 approved clips recovered byte-for-byte

**Type:** recovery (evidence, not a change)
**What was done:** after REV-005 recorded the loss, the git history was re-checked for audio blobs. The
nine narration clips (pre-correction set) are still present in commit `6edcf9f`. Exported with
`git show 6edcf9f:…/public/audio/sceneN.mp3 > public/audio/sceneN.mp3` (export to file — deliberately not
`git checkout`, which would re-stage binaries that are forbidden in the repository).
**Verification:** every restored file was hashed and compared with the approved-hash list:

| Clip | Bytes | sha256 (first 8) | Expected | Result |
| --- | --- | --- | --- | --- |
| scene1.mp3 | 43,276 | `bb1c226b` | `bb1c226b` | MATCH |
| scene2.mp3 | 63,129 | `64837c13` | `64837c13` | MATCH |
| scene3.mp3 | 81,102 | `b877ebce` | `b877ebce` | MATCH |
| scene4.mp3 | 67,727 | `96f4ca4f` | `96f4ca4f` | MATCH |
| scene5.mp3 | 56,233 | `053a1a7a` | `053a1a7a` | MATCH |
| scene7.mp3 | 84,236 | `61a2b3d8` | `61a2b3d8` | MATCH |
| scene8.mp3 | 48,501 | `b56603cf` | `b56603cf` | MATCH |

**Remaining gap:** only the two corrected clips are still missing — `scene6-brand-fixed.mp3`
(`70e20d0e…`, 10.501 s) and `scene9-brand-fixed.mp3` (`9a622b99…`, 3.788 s). They were created after the
last audio-bearing commit and were never committed.
**Scope check:** seven files rewritten on disk, zero files added to git (audio is git-ignored by owner
rule), no audio regenerated, no mix rebuilt, no manifests changed beyond recording the recovery.
**Impact if only these two are restored:** the mix can be rebuilt immediately — expected 69.616 s
(69.642 − 10.606 + 10.501 − 3.709 + 3.788).

## REV-009 — Owner decision after the LOC audit: R5 applied, pilot scoped to three projects

**Type:** owner decision (EXTEND_EXISTING) + governance action
**Owner verdict on the audit:** accepted — handwritten LOC = 1,183, budget respected.

**Decisions and how they were executed:**

| # | Owner decision | Action taken |
| --- | --- | --- |
| 1 | Do not perform R1–R4; keep existing tools and artifacts | no deletion, no rewrite, no merge — nothing removed |
| 2 | R5 allowed: minimal `.gitattributes` for generated JSON and the vendor lockfile; do not change file contents | added repo-root `.gitattributes` (12 lines, config only); verified with `git check-attr`: the three generated JSONs and `package-lock.json` resolve `linguist-generated=true` / `linguist-vendored`; `Promo.tsx`, tools, `VOICE_MANIFEST.json` stay unmarked and remain counted as code |
| 3 | Keep `loc_report.py` as the mandatory budget gate | tool kept unchanged; run again this turn (see the report) |
| 4 | Future reports must show handwritten / generated / vendor / total diff separately | adopted; this report uses the four-way breakdown |
| 5 | Return to CP-08 recovery: restore the two approved MP3s with SHA-256 verification, no regeneration | **partially blocked:** the two files are not attached yet; the seven other approved clips are restored and re-verified; **no regeneration performed** (explicitly forbidden) |
| 6 | Continue the CP-07 owner-media pilot, max three real Salamat Mebel projects | pilot block added to `OWNER_MEDIA_SHORTLIST.json` v2 (3 project slots with the beats each covers, per-project ask, scenes outside the pilot); audit §6a records the scope; intake 0 of 3 |
| 7 | Do not expand the architecture, do not create new services | no new source files, no new dependencies, no new services; the only new file is the `.gitattributes` config |

**CP-08 recovery status (facts):** `scene1/2/3/4/5/7/8.mp3` present and re-hashed this turn —
`bb1c226b`, `64837c13`, `b877ebce`, `96f4ca4f`, `053a1a7a`, `61a2b3d8`, `b56603cf` (7/7 MATCH).
`scene6-brand-fixed.mp3` (`70e20d0e…`) and `scene9-brand-fixed.mp3` (`9a622b99…`) are still absent; they can only
return as the owner's own attachment. The mix rebuild stays deferred until they arrive.

**Instagram availability re-checked 2026-10-08:** still blocked — TLS handshake reset by the egress policy on
`www.instagram.com`, `instagram.com`, `i.instagram.com`, `graph.instagram.com` (HTTP 000) while DNS resolves to
`2a03:2880:f36c:22:face:b00c:0:4420`. No scraping, no bypass, nothing inspected.

**Still gated:** final render and publication (owner STOP GATE), CP-10…CP-12, any further architecture work.
