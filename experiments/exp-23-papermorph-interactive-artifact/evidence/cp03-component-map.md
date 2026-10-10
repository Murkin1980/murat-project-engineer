# CP-03 — Component extraction review — results

**Status: READY (analysis; no code copied or integrated — not authorized by this task)**
Date: 2026-10-10 (UTC)

Upstream: Papermorph @ `093418e`, MIT (c) 2026 TedKaczynski. MIT permits
reuse with license notice retained in copied/substantial portions (the engine
copied into the pilot book must therefore ship with the upstream LICENSE on any
future adoption).

Reuse targets (from README): MPE (book/document → skill workflows), Murat House
(interactive explanatory content), AI-serial (script → storyboard/visual scene
prototype — blocked fixture, see CP-02), 1C Tutor KZ (interactive trainer with
check questions, feedback, points, step sequencing — README verified 2026-10-10).

## Candidate components

### 1. Source → structured outline — REUSE (extend EXP-24 editorial JSON)

- **What**: PDF/text → page map + section text + chapter map
  (`outline.py`/`split_pages.py`/`sections.json`/`chapters.md`). Deterministic,
  LLM-free, ~10 KB of scripts, PyMuPDF only.
- **Extends**: EXP-24 CP-06 "Source → Editorial JSON" (scene id/order,
  narration, editorial purpose, visual intent, duration, source grounding) and
  EXP-002 machine-protocol task representation for structured inputs.
- **Duplication risk**: low if folded into EXP-24's existing scene JSON as an
  extraction stage; medium if re-implemented per project.
- **Coupling to Papermorph**: none (plain scripts + JSON).
- **Licensing**: MIT, small portion (notice trivially satisfied).
- **Minimum adapter surface**: point `outline.py`/`split_pages.py` at the
  project's source format; emit the project's scene schema instead of
  `sections.json`.
- **Measurable benefit**: removes manual page/section mapping; CP-01 measured
  this stage at ~10 min of agent time for a 10-page document with 0 errors,
  fully reproducible.

### 2. Outline → storyboard with speech-marked narration — REUSE (the core contract)

- **What**: beat list + `narration.<lang>.json` with `[[mark]]` tags placed
  before the word an on-screen action waits for; `timings.js`
  `{beat: {dur, marks, cues}}` as the sync artifact. The mark is the entire
  narration↔visual contract: one line of narration text drives both audio and
  animation timing.
- **Extends**: EXP-24's shared storyboard + narration layers (its GENERATIVE
  mode for AI-serial is exactly the consumer this contract is missing); MPE
  "document → skill workflow" artifacts that need timed reveals.
- **Duplication risk**: low — it is a *schema + convention*, not a runtime.
  Adopting it in two places (EXP-24, Murat House) is sharing, not duplication.
- **Coupling to Papermorph**: zero for the schema; the engine's `m('mark',
  offset)` consumer is the only coupling point.
- **Licensing**: MIT; the schema is documentation-level (notice in docs).
- **Minimum adapter surface**: keep the JSON shapes; any player that reads
  `marks` + `dur` consumes it.
- **Measurable benefit**: CP-01 produced 23 marks / 11 beats / 5 quizzes with
  0 sync defects found on static review; beat-level regeneration is possible
  (change one narration line → one audio file → timings recompute
  deterministically). This is the component that most directly answers the
  EXP-23 hypothesis ("script → storyboard with low manual correction cost").

### 3. Storyboard → narration (TTS) — HOLD

- **What**: per-beat narration synthesis + word-boundary timing (`tts.py`,
  Edge TTS).
- **Finding**: sandbox-blocked for Edge TTS (measured); word-boundary quality is
  provider-dependent. The *schema* (candidate 2) is provider-neutral; the
  *synthesis tooling* is not worth reusing (EXP-24 already treats providers as
  narrow adapters; ElevenLabs reference exists).
- **Disposition**: do not reuse `tts.py`; reuse only the narration schema +
  timings contract (candidate 2).

### 4. Storyboard → procedural animation spec — HOLD (engine too coupled)

- **What**: the 90 KB `engine.js` (SVG stage, tween/timeline API, beat runner,
  player, guide).
- **Finding**: the pilot proved the beat API is a powerful, coherent way to
  express "the picture explains the idea", but reusing it in MPE/House means
  vendoring a 90 KB runtime per project — a parallel visual runtime, i.e.
  exactly the duplication the experiment prohibits. Its topic helpers
  (number lines, algebra tiles) are algebra-specific ballast.
- **Duplication risk**: high. **Coupling**: maximal. **Licensing**: MIT but
  substantial-portion (LICENSE must ship).
- **Minimum adapter surface (if ever chosen)**: fork the engine into the
  consuming project, drop topic helpers, keep stage/timeline/beats/player.
- **Measurable benefit**: high *for animated artifacts only*; CP-01 shows the
  cost of one full chapter ≈ 11 beats of bespoke SVG code even with the engine.
- **Disposition**: HOLD — reconsider only if a project explicitly adopts
  "animated web artifact" as a product surface (e.g., Murat House interactive
  explainers) under a separate owner decision.

### 5. Interactive quiz / checkpoint generation — REUSE (strongest standalone fit)

- **What**: quiz data model — `choice` (wrong options each with their own
  explanation), `blanks` (exact-value numeric parsing, fractions/mixed
  numbers), `grid`, `tap`/`tapEls`/`pickEls` (act on the picture itself),
  first-attempt-only scoring persisted across revisits, show-answer flow,
  finish card aggregating first-try results.
- **Extends**: **1C Tutor KZ** — its MVP loop is literally "check question →
  feedback → points → next step, progress persists" (README §2); the
  Papermorph model adds act-on-the-picture question types and the
  first-attempt-scoring semantics. Also Murat House explainers.
- **Duplication risk**: low for the *data model + grading semantics* (JSON +
  rules, no runtime); 1C Tutor KZ keeps its own React stack — no shared
  runtime created.
- **Coupling to Papermorph**: the engine implements it, but engine.md fully
  documents the model; a project can implement the model against its own UI.
- **Licensing**: MIT; semantics are documentation-level.
- **Minimum adapter surface**: per-question-type: input schema + grader +
  feedback contract (`why`/`hint`/wrong-why).
- **Measurable benefit**: CP-01's 5 quizzes (3 quick checks + 2 practice) all
  trace to source facts with per-mistake explanations; this is the piece an
  existing trainer project can adopt line-by-line.

### 6. Artifact editability / regeneration by scene — REUSE (pattern)

- **What**: each beat is an isolated unit — one `BEATS` entry, one narration
  line, one audio file, one timings entry; `?beat=N&t=S` frozen-frame review;
  scores keyed by stable question ids; progress keyed by URL folder.
- **Extends**: MPE's own "evidence/handoff for the next executor" discipline —
  the same idea applied to a visual artifact: any executor can regenerate one
  scene without full regeneration.
- **Duplication risk**: none (it's a structural pattern). **Coupling**: none.
- **Measurable benefit**: CP-01's audio defect was fixed by rebuilding two
  files; no other beat was touched.

## What was deliberately NOT extracted

- Bookshelf/cover/contents page system (`book.html` + `unit-art.js`): nice, but
  product surface; adopting it would create a mini content platform.
- Guide mascot / view transitions: aesthetic, non-essential.
- The algebra topic helpers: domain-specific.

## Summary for the final recommendation

Two narrow, low-coupling, MIT components are ready for adoption into existing
projects without a parallel platform: **(2) the mark-based narration/visual
sync contract** (→ EXP-24's storyboard/narration layers, incl. the blocked
AI-serial GENERATIVE path) and **(5) the quiz data model with
first-attempt scoring** (→ 1C Tutor KZ). Component **(1)** and the **(6)**
pattern ride along as documentation. Components (3)/(4) HOLD.
