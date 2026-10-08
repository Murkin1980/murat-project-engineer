# SALAMAT_PROMO_RESULTS — EXP-24 Phase 2, Salamat Mebel promo

Status at this checkpoint: **CP-06 … CP-09 complete; CP-10 … CP-12 not started (not authorised).**
Phase 1 terminal record in `RESULTS.md` is untouched.

```text
RESULT (interim, owner-defined next checkpoint): PARTIAL — contracts, voice adapter and assembly preview
        work end-to-end, but no licensed footage exists and no music bed exists, so the film cannot pass
        CP-10 acceptance or reach CP-12.
ADOPTION: ADOPT_WITH_CHANGES (unchanged for the pipeline; final decision reserved until a licensed run)
NARRATIVE SOURCE: SALAMAT_PROMO_SCRIPT.md (owner-approved; 9 scenes, 0:00–2:00)
PROVIDERS: Storyblocks — BLOCKED_PROVIDER (no credentials, host unreachable)
           ElevenLabs — BLOCKED_PROVIDER (no credentials) → VoiceProvider adapter on Arena speech
           Music — NOT_PROVIDED (no licensed track; nothing substituted)
MEDIA: 17 stock requests, 0 resolved · generated imagery 0 · branded generative graphics 2 / budget 3
VOICE: owner-selected voice (audition Sample 2 → voice-00), 9 clips, 69.6 s narration, RU script text verbatim
RENDER: promo-remotion/out/preview-salamat-mebel-v1.mp4 — 122.23 s, 1920×1080, 30 fps, H.264+AAC, 9.28 MB
        SHA-256 50f4bece0d4a09285a53cc34a4e254e7…
CODE: 1,195 added implementation lines (preferred budget ≤ 1,200); 6 code files
PUBLISHING: not executed anywhere; no upload, no public link
```

## Checkpoint ledger

| CP | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| CP-06 | source → editorial storyboard | **DONE** | `EDITORIAL_STORYBOARD.json` (18 beats, 120.0 s, 9 script scenes). `tools/build_storyboard.py` aborts unless narration rejoins verbatim, beat durations sum to the script timecodes and every overlay string comes from the script's "On-screen text". Re-run: storyboard byte-identical. |
| CP-07 | media manifest + provenance | **DONE (PARTIAL media)** | `MEDIA_MANIFEST.json` — 17 Storyblocks requests with query, search URL, licence note, in/out intent, fallback queries, blocker + required action; `MEDIA_PROVIDER_LOG.md` logs every probe. Nothing licensed, nothing substituted. |
| CP-08 | narration via VoiceProvider adapter | **DONE (draft voice)** | `VOICE_MANIFEST.json` — owner-selected voice (Sample 2), measured durations, per-beat apportioned shares, hashes, provenance commands, limitations. `MUSIC_MANIFEST.json` — no licensed track, `NOT_PROVIDED`. |
| CP-09 | smallest Remotion composition + preview | **DONE (technical)** | `preview-salamat-mebel-v1.mp4`; review page `REVIEW_CP09.html`; audio verified present (speech 0–70 s, RMS ≈ 0.08, peak 0.58). |
| CP-10 | mobile acceptance at 360 px | NOT STARTED | representative frames captured for the owner's own review only; no acceptance claimed |
| CP-11 | natural-language revisions | NOT STARTED | `REVISION_LOG.md` currently records only the scope correction REV-000 |
| CP-12 | final render | NOT STARTED | blocked: unlicensed footage, no music, draft voice |

## Owner-directed decisions honoured

- **Variant A** — Arena speech provider behind the existing thin `VoiceProvider` adapter; no new voice service.
- **Two Russian male candidates** auditioned; owner chose **Sample 2**; final voice-over not asserted before that choice.
- **CP-09 preview authorised** on neutral slates using the current Remotion composition.
- **No generative substitute** for the missing stock footage: 0 generated images, 0 generated video.
- **Storyblocks blocker preserved** as a recorded blocker with a required action.
- **Publication refused** — nothing was uploaded anywhere.

## Verification performed in this checkpoint (facts, not self-report)

| Check | Result |
| --- | --- |
| `git rev-parse HEAD` | `6edcf9f` (preview built from this commit's contracts) |
| Code lines added vs `main` (`.py/.ts/.tsx`) | 1,175 in 8 files; `loc_report.py` prints 1,195 including `package.json` |
| Generated binaries tracked | 0 after the audit fix |
| Storyboard re-run | byte-identical SHA-256 `6e627a0b4b899e87…` |
| Manifest / timeline re-run | differ only in `created`/`generatedAt` timestamps — not claimed byte-identical |
| Timeline total after voice | 122.23 s (two beats extended by narration + 0.8 s breath pad) |
| Captions per beat | 1–2 lines, never more (measured from `timeline.json`) |
| Audio in the MP4 | AAC stereo present; per-10 s RMS 0.08 for the first 70 s, 0.0000 afterwards |
| Storyblocks probe | `BLOCKED_PROVIDER` — 17 unresolved, 0 resolved |

## Blockers (preserved, not worked around)

1. **Storyblocks** — no API credentials in this environment and the provider host is unreachable from the
   sandbox. Required action: authenticate a licensed provider, run the recorded queries, license matching
   clips, re-run `tools/resolve_media.py`. No storyboard change will be needed.
2. **Music** — no licensed track available; a bed may not be fabricated. The preview therefore has 52 s of
   silence after the narration ends.
3. **ElevenLabs** — no credentials. The Arena speech adapter satisfies CP-08 for a draft, but it exposes no
   speed/pitch control, so an owner request such as "older/slower" cannot be executed through it.
4. **Duration** — the script's 120 s yields 122.23 s once narration plus breath is respected on two beats
   (within the accepted 110–125 s window, under the 130 s cap).

## Next action

Await the owner's review of the two voice samples and this preview, then either
(a) supply Storyblocks access so CP-07 can resolve and CP-10…CP-12 can proceed, or
(b) record CP-10…CP-12 as blocked and keep the fixture at its current PARTIAL state.
