# MPE Scope & Change Control — book plan

Read this compact current state for chapter work. The chapter map/status lives in `chapters.md`; storyboards, errata and feedback live in `chapters/chNN.md`.

## Intake
- Readers: engineers and coding agents working in Murat Project Engineer repositories · Tone: plain, precise, never childish · Narration language: English · Guide character: default infinity guide
- Slug: `scope-control` · Primary language code: `en` · Asset approach: code/SVG by default
- Source: `book.pdf` (rendered from canonical `docs/governance/SCOPE-CHANGE-CONTROL.md`, version 2026-09-24) · Page map: `sections.json` · 10 pages, 5 chapters in 3 units.
- Decision record (EXP-23 CP-01 fixture, asked up front with defaults): target readers = the policy's own audience; scope = all 24 sections mapped to 5 chapters, pilot = chapter 1 only; no custom guide; no images (pure code/SVG).

## Conventions (approved in the pilot; later chapters follow them)
- Look: engine default palette on the chalkboard; chalk for the current idea, dim for labels, task (amber) for the rule/number being taught, quiz blue for question cards, good green for right / bad red for crossed-out wrong. A new idea enters as a drawn object (box, rung, chip) that appears at the word that names it; numbers/labels follow.
- Narration: voice `en-US-AndrewMultilingualNeural`, rate `-4%` (stock default). Policy names read literally ("deep-change gate", "STOP").
- Questions: quick checks as `choice` or `tapEls` on drawn tokens, placed in `BAND` or a side card so the figure stays visible; practice full-screen (`SCREEN`), labelled "Chapter practice N of M".
- Subject conventions: section numbers (§1–§24) refer to the source document; quoted phrases are verbatim from the source; counts (6 priorities, 6 checkpoint rules, 11 gate bullets) are exact facts and checked against the source before delivery.

## Visual models / available helpers
- Shrinking-diff model: a large "change" box condenses into a small patch (ch01 `principle`); helper `shrinkBox` in `site/scope-control/ch01/index.html`.
- Priority-ladder model: 6 rungs, top = highest priority (ch01 `ladder`); helper `ladder` in the same file. Reuse for ch02 §7 implementation order (5 steps) if the book continues.
- Rule-chip row: short rules appear as numbered chips in order (ch01 `boundary`); helper `ruleChips`.

## Current decisions
- The book teaches the policy as written; every factual claim in a beat is verified against `pages/chNN/text.md` before delivery (authoring.md content rule).
- No source errors found in the fixture so far (see `chapters/ch01.md` errata).
