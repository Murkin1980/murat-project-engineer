# CP-01 — Technical/business document fixture — results

**Status: READY** (with documented environmental deviations; no deep-change requirement found)
Date: 2026-10-10 (UTC) · Executor: Arena Agent Mode (fresh session, bootstrap-verified)

## 1. Exact source and version

| Item | Value |
|---|---|
| Document | `docs/governance/SCOPE-CHANGE-CONTROL.md` (MPE Scope & Change Control) |
| Document version | 2026-09-24 (file header), canonical in this repo, 12,561 B, 24 sections |
| Fixture PDF | `work/books/scope-control/book.pdf` — 10 pages, no bookmarks, text layer, rendered deterministically by `work/tools/make_fixture_pdf.py` from the canonical .md (dev-only helper, not part of the book) |
| Upstream Papermorph | commit `093418e1d23026f93fe2b12a7ea203dde5361455`, MIT (c) 2026 TedKaczynski — see `evidence/upstream.md` |
| Book slug | `scope-control` · pilot = ch01 (source §1–§3) of 5 planned chapters |

## 2. Model / agent used

- Pipeline executor: Arena Agent Mode session (this session). The stock skill is
  agent-facing instructions ("Opus 5.5 only" refers to the upstream Claude Code
  path); the same pipeline steps were executed here.
- Narration: stock voice spec `en-US-AndrewMultilingualNeural, rate -4%` was NOT
  usable (Edge TTS endpoint blocked in sandbox — verified). Fallback: Arena-native
  TTS, registered voice `voice-00` (masculine, user-selected from 2 candidates,
  auditioned on real ch01 narration).
- Audio engineering: 10 real clips synthesized (11 narration beats; `ladder` and
  `boundary` each from 2 clips joined at a sentence boundary). 3 beats
  (`wrap`, `final1`, `finish`) are **silent deterministic CBR placeholders** with
  captions carrying the text — the TTS per-turn synthesis limit (10) was hit;
  they are one regeneration away from real voice. All MP3s normalized to uniform
  64 kbps CBR (the TTS output's first 56 kbps frame was dropped; see §6).

## 3. Generated structure and storyboard

- Page map `work/books/scope-control/sections.json` (stock no-bookmarks path:
  `outline.py` → "No bookmarks" → `split_pages.py --pages` preview → hand map →
  `--text-only` extraction). 10 pages, 5 sections, no gaps/overlaps (script-verified).
- Book map `work/books/scope-control/chapters.md`: 5 chapters / 3 units (only ch01
  ready; per the template, unready chapters are not listed on the cover).
- Storyboard `work/books/scope-control/chapters/ch01.md`: 11 beats
  (intro, principle, q1, ladder, conflict, q2, boundary, q3, wrap, final1, finish)
  with per-beat eye/watch/why/marks/keep-or-fade, quiz design, and fact verification.
- `work/books/scope-control/BOOK.md`: intake decisions, conventions, visual models.

## 4. Generated narration

- `work/content/scope-control/ch01/narration.en.json` — stock format, 11 beats,
  23 speech marks (`[[mark]]` before the triggering word).
- ~340 words, 143.9 s total audio. Mark cross-check: every `m('…')` in the chapter
  resolves to a mark in the narration; 5 narration marks are intentionally
  unanchored (question beats).
- `work/content/scope-control/ch01/splits.json` documents the two sentence-boundary
  splits; `work/tools/build_timings.py` derives the stock-schema `timings.js`
  `{beat: {dur, marks, cues}}` (measured MP3 durations; marks exact at clip joins,
  linear within a clip — vs. stock Edge-TTS word boundaries, the documented
  precision difference).

## 5. Generated animation / interactive artifact

- `work/site/scope-control/` — 17 files, 1.5 MB, self-contained: cover + contents
  (book.html-based, unit sketch in `unit-art.js`), engine byte-copies of the pinned
  commit, ch01 lesson with 11 beats: condensing "new work" box, 6-rung priority
  ladder, crossed-out forbidden action, tap-to-rank quiz (pickEls), 6-chip rule
  list with STOP pulse, 5 quizzes (3 quick checks + 2 full-screen practice),
  finish scorecard.
- Live preview: `python3 -m http.server 8765 -d site` (running; entry
  `/scope-control/`). All routes verified 200 incl. 1.1 MB of audio.
- Delivery pass (no browser/Playwright in sandbox — stock `shot.py`/`check_blank.py`
  not runnable): node `--check` on every script; headless execution of **all 11
  beats + all 5 quiz builders against the engine API with the real TIMINGS**
  (`work/tools/smoke_beats.js`) — 0 failures; static geometry review (all elements
  within the 1600×900 stage, quiz tokens clear of the BAND card y≥686); every beat
  opens within 0.8 s (engine lead-in invariant satisfied by design).
- Engine fallback verified by code read: if an MP3 fails, the player degrades to a
  wall-clock with a visible sound note (beats stay timed by TIMINGS durations).

## 6. Factual errors / unsupported claims — manual fact-check

Checked every narrated/on-screen claim against `pages/ch01/text.md` (→ canonical .md):

- Verbatim facts used: "smallest sufficient correct change"; the six minimized
  categories (code, dependencies, infrastructure, configuration, abstractions,
  unrelated edits); "Simplicity first."; the 6-rung priority order and wording;
  the §3 six bullets; "new checkpoint begins only after an owner instruction or
  committed owner-approved spec authorizes it." — **0 factual errors, 0 unsupported
  claims.**
- Two deliberate shortenings (flagged in the storyboard): rung 3 drops "and project
  instructions"; rung 4 renders "/" as "&". No meaning change; no counts altered.
- Question items (q1/q2/q3/final1) all trace to §1–§3 statements; every wrong
  option is wrong *for a reason tied to the source* (explanations cite the rule).

## 7. Manual correction count

Corrections to **generated artifact** (what the metric targets): **2**
1. `unit-art.js` — typo in the `P()` helper (duplicated style attr) — fixed pre-serving.
2. Audio concatenation — byte-joining the split clips left a first-frame
   bitrate mismatch (56 kbps frame 0) that truncated player duration inference;
   fixed by dropping each clip's first frame and rebuilding the CBR stream.

Corrections to **dev tooling** (not the artifact; counted separately): 4
(make_fixture_pdf.py string-iteration + font name; build_timings.py outdir +
time_at; unit-art typo above double-counted? no — tooling: make_fixture ×2,
build_timings ×2).
Re-runs forced by tooling: 2 (PDF re-render, timings rebuild ×2).

## 8. Generation and edit effort

- Wall time ≈ 1.5 h agent work across the session's turns (bootstrap preflight
  included separately in `evidence/bootstrap/`).
- Heaviest costs: engine API verification (grep of 90 KB engine for exact
  signatures — the skill's "read the function before first use" guidance), and the
  MP3 concatenation defect (§7.2), which required frame-level analysis.
- Reproducible? Yes for structure; audio depends on the Arena TTS voice (stable
  `voice-00`), timings are deterministic from the MP3s (`build_timings.py`),
  PDF render is deterministic (`make_fixture_pdf.py`), smoke test is one command.
  All commands + tools are recorded in this file and in the tools directory.

## 9. Reproducibility notes / environment

- Sandbox: no `uv`, no `ffmpeg`, no browser; python3.11 + venv (`pymupdf 1.28.2`,
  `mutagen`) + node 22. Network: PyPI/GitHub/npm hosts only (Edge TTS blocked).
- Every stock stage has a recorded stock-or-deviation status in
  `evidence/upstream.md` §"Stock fidelity".
- No production project touched; no new repository; no canon changes; all
  artifacts under this experiment directory (book workspace in `work/`).

## 10. Verdict inputs for the final recommendation

- Fixture fidelity: **pass** (0 factual errors, verbatim-checked).
- Manual correction: **low** (2 artifact corrections, both caught by local checks
  before human review; no "impressive one-shot requiring heavy repair").
- Editability/regeneration: **pass** — scene/beat-level: any beat is an isolated
  `BEATS` entry + narration line + audio file; regenerate one beat without
  touching others; `?beat=N&t=S` frozen-frame review; quiz ids/positions are data.
- Reusable components visible: outline→storyboard→marks→beats structure,
  timings schema, quiz data model (detailed in CP-03).
