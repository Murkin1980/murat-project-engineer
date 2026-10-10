# EXP-23 — Papermorph document → interactive artifact — FINDINGS

Date: 2026-10-10 (UTC) · Executor: Arena Agent Mode (fresh session,
EXP-29 bootstrap-verified FRESH — see `evidence/bootstrap/`)
Upstream: Papermorph @ `093418e1d23026f93fe2b12a7ea203dde5361455` (MIT)
Queue condition: EXP-22 Colibri is HOLD (not finished); this run proceeded on
the explicit owner reprioritization in the session instruction (recorded in
`evidence/bootstrap/BOOTSTRAP_START.md`).

## Checkpoint verdicts

| CP | Scope | Verdict | Evidence |
|---|---|---|---|
| Bootstrap preflight (EXP-29) | fresh-session startup packet | **FRESH** (all 7 fail-closed checks) | `evidence/bootstrap/` |
| CP-01 | technical/business document fixture (MPE governance doc, §1–§3) | **READY** | `evidence/cp01-document-results.md`, pilot book `work/site/scope-control/` |
| CP-02 | AI-serial script fixture | **BLOCKED** — no existing AI-serial scene/episode exists in any accessible canonical source (repo, all 37 GitHub repos, portfolio dashboard, code search) | `evidence/cp02-ai-serial-results.md` |
| CP-03 | component extraction review | **READY** (analysis only) | `evidence/cp03-component-map.md` |

## What the document fixture proved (CP-01)

- Stock pipeline (intake → split → book map → initialize → pilot chapter loop)
  executed end-to-end on a 10-page, verifiable governance document; the pilot
  chapter is a playable, narrated, interactive 11-beat web book (live preview
  served during the run; `python3 -m http.server 8765 -d site`).
- **Factual fidelity: 0 errors, 0 unsupported claims** — every narrated and
  on-screen fact verbatim-checked against the source (2 flagged shortenings,
  no meaning change).
- **Manual corrections: 2** on the generated artifact (a unit-sketch code typo;
  an MP3 first-frame bitrate defect on clip concatenation) — both caught by
  local checks before human review; 4 dev-tooling fixes counted separately.
  This is *not* the "impressive one-shot requiring heavy repair" failure mode.
- **Editability: beat-level** — any scene regenerates from one BEATS entry +
  one narration line + one audio file; timings recompute deterministically.
- Environment deviations (measured, documented, none are Papermorph defects):
  Edge TTS blocked → Arena TTS fallback; no Playwright → headless beat
  execution + static geometry review; 3 of 11 beats carry silent placeholder
  audio (TTS per-turn limit) with captions — one regeneration away from voice.

## Success criteria score

1. Fixture factually faithful enough for practical use — **PASS**
2. Acceptably low manual correction — **PASS** (2)
3. ≥ 1 pipeline component reusable inside an existing project without a
   parallel platform — **PASS** (sync contract + quiz model; see below)
4. AI-serial fixture useful as storyboard/previs, or clearly why not —
   **UNANSWERABLE** (fixture does not exist; external gap, CP-02 BLOCKED)
5. Editable/regenerable at scene/section level — **PASS**
6. No deep-change or new repository required — **PASS**

## Final recommendation (exactly one)

# **REUSE_COMPONENT**

Adopt **two narrow Papermorph components** into existing projects, with the
engine explicitly NOT adopted:

1. **The mark-based narration ↔ visual sync contract** —
   `narration.<lang>.json` with `[[mark]]` tags + `timings.js`
   `{beat: {dur, marks, cues}}`.
   - Target: EXP-24 HyperFrames' shared storyboard/narration layers —
     including its GENERATIVE mode, which is the documented home for
     AI-serial work; this contract is the missing piece CP-02 could not
     evaluate, and it is what makes "script → storyboard with low manual
     correction" concrete (23 marks / 0 sync defects in CP-01).
   - Also fits MPE document → skill-workflow artifacts needing timed reveals.
2. **The quiz data model with first-attempt scoring** — `choice`/`blanks`/
   `grid`/`tap` types, per-mistake explanations, first-attempt-only scores,
   show-answer flow, finish card.
   - Target: 1C Tutor KZ (its MVP loop is check question → feedback → points →
     next step; the model adds act-on-the-picture types and scoring semantics).

Adoption conditions: MIT license notice retained; components stay schemas +
documented semantics (no 90 KB engine vendored into MPE — that is the
parallel-runtime trap, component 4 = HOLD); adoption happens in the owning
projects' own bounded runs, not in this experiment. **This PASS does not
authorize production integration** (per README).

HOLDs: TTS tooling (provider-dependent; reuse the schema, not `tts.py`);
engine/animation runtime (revisit only if a project explicitly adopts animated
web artifacts as a product surface, under a separate owner decision).

## Follow-ups (next authorized actions, none started here)

- CP-02 rerun when the owner supplies an AI-serial fixture or location.
- Replace the 3 silent placeholder beats (wrap/final1/finish) with real TTS —
  one bounded regeneration using `tools/build_timings.py` + re-verify.
- Optional EXP-29 data point: packet regeneration after registry update
  (post-run) to exercise the STALE→rebuild path on a real post-run update.
- Register the reuse decision (if accepted) in the owning projects'
  checkpoint specs, with license notice.

## Guardrail compliance

No new repository · no production deployment · no standalone product · no
autonomous service · no AI-serial canon touched (none exists) · no publishing ·
upstream pinned + license recorded · evidence under this experiment directory ·
stock behavior preferred (deviations measured and recorded in
`evidence/upstream.md`) · scope stayed within the two fixtures + component map.
