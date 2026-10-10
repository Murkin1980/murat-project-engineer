# Upstream — Papermorph (EXP-23 CP-01)

## Pin

- Repository: https://github.com/DozenTwelve/Papermorph
- Pinned commit: `093418e1d23026f93fe2b12a7ea203dde5361455` ("feat: merge math chapters 21-22")
- Cloned: 2026-10-10 (UTC), read-only; working clone kept outside the MPE repo
  (`/home/user/papermorph-upstream`), never committed here.
- License: **MIT** (Copyright (c) 2026 TedKaczynski). Copy retained at
  `papermorph-upstream/LICENSE`. Per-file attribution: the MIT license requires the
  copyright notice in copies/substantial portions — the engine copy in this book
  (`site/scope-control/lib/engine.js|css`) is a substantial portion, so the upstream
  LICENSE must ship with any future reuse of `lib/`. Recorded for CP-03.

## What it is

A Claude Code **Skill** (`.claude/skills/papermorph/`) that turns PDFs into animated,
narrated, interactive **web books**. Stock pipeline (README):

```
PDF -> Book plan -> Storyboards -> Narration -> Animation & quizzes -> Web book
```

- Output is static: HTML + JS + CSS + MP3, no build step, no backend, no accounts
  (progress in `localStorage`). Served with `python3 -m http.server 8765 -d site`.
- One chapter = one 1600×900 SVG stage; **beats** pair narration clips with timed
  actions via `[[marks]]` → `m('name', offset)`; question types: choice, blanks,
  grid, tap/tapEls/pickEls, pickPoint, sorter; finish card with first-try scoring.
- Engine (`assets/engine/engine.js`, 90 KB, unmodified in this run) provides stage,
  tweens, player (space/←→/Home/C/F/?, `?beat=N&t=S` frozen frame), guide mascot.
- Stock tooling: `uv` + `pymupdf` (outline/split), `edge-tts` + `ffprobe` (narration
  and word-boundary timings), Playwright Chromium (delivery screenshots, e2e).
- README states "Today: Opus 5.5 only" for the Claude Code path; the skill is
  agent-facing instructions, so any competent agent (this run: Arena Agent Mode) can
  execute the same pipeline. No image models, no BGM, English-first.

## Stock fidelity — what ran stock vs. deviations (CP-01)

| Stage | Stock? | Notes |
|---|---|---|
| Intake (BOOK.md, decisions) | yes | template + up-front decisions recorded in BOOK.md |
| Split (`outline.py`, `split_pages.py`, sections.json) | yes | run verbatim (venv `pymupdf 1.28.2` instead of `uv run --with pymupdf` — same library, different launcher; `uv` not installable in sandbox). No-bookmarks PDF → documented preview+map path. |
| Book map (chapters.md) | yes | 5 chapters in 3 units, pilot = ch01 |
| Initialize (engine/template copies) | yes | verbatim copy block from site.md; no template edits beyond the documented content fields |
| Pilot (storyboard → narration → beats) | yes | stock chapter loop 1–5; beat shape, marks, quiz types per authoring.md/engine.md |
| Narration synthesis | **deviation (environmental)** | stock `tts.py` uses Edge TTS; sandbox blocks `speech.platform.bing.com` (verified `ClientConnectorError`). Fallback: Arena-native TTS per beat (male voice matching stock `en-US-AndrewMultilingualNeural` intent); long beats (ladder, boundary) split at a sentence boundary and concatenated so mark times stay exact at the join. |
| timings.js | **deviation (tooling)** | stock derives word-boundary marks from Edge TTS events. Fallback `tools/build_timings.py` (deterministic) derives the stock schema `{dur, marks, cues}` from measured MP3 durations with linear-within-clip mark interpolation. |
| Delivery pass | **partial (environmental)** | stock = Playwright screenshots (`shot.py`, `check_blank.py`) — no browser installable in sandbox. Substituted: node syntax check of every script, headless execution of all 11 beats against the engine API with real TIMINGS (tools/smoke_beats.js), static geometry review, live HTTP preview for human playthrough. |
| Engine | unmodified | `lib/engine.js|css` are byte copies of the pinned commit |

## Sandbox constraints (measured, not assumed)

- Outbound network limited to github.com / codeload.github.com / api.github.com /
  registry.npmjs.org / pypi.org / files.pythonhosted.org. Edge TTS, Playwright CDN: blocked.
- No `uv`, no `ffmpeg`/`ffprobe`, no system browser; python3.11 + pip (PEP 668 → venv)
  + node 22 available.
