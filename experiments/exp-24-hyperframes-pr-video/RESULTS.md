# EXP-24 terminal result — HyperFrames PR to video

Run date: 2026-10-06 (UTC)  
Execution base: `main` / `origin/main` at `7bef090338e334003067d64aa6fe273df149e1cb`; work remained on the required Arena branch.  

```text
RESULT: PARTIAL
EXPERIMENT_STATUS: CLOSED
ADOPTION: ADOPT_WITH_CHANGES
SELECTED_PR: #46 — EXP-15: controlled MVP experiment for bounded project memory layer
BLOCKER: Arena executor has no Chrome; the one attempted headless-Chrome download failed at TLS setup. FFmpeg is also absent from PATH. Preview started, but its lint summary reported 1 error and 6 warnings without rule details.
NEXT_ACTION: In a suitable local/CI executor, resolve the recorded lint error, then validate one render; do not continue environment repair in this Arena run.
```

## Selected PR and frozen evidence

- **Repository / PR:** `Murkin1980/murat-project-engineer` [#46](https://github.com/Murkin1980/murat-project-engineer/pull/46), merged 2026-09-30.
- **Merge commit:** `f36c97212a812f7591c6e554fac07491754d7b9b` (PR head `b1265e4b8fc297a3ed51219bea6c0a51ace69267`).
- **Problem:** MPE sessions repeatedly rediscovered prior decisions and constraints by searching repository documents.
- **Meaningful changes:** an experiment-only file-backed memory prototype/model; a deterministic six-case acceptance harness; frozen fixtures and an A/B baseline evaluator; provenance and approval guardrails with Git retained as the source of truth.
- **Reported verification/result:** six of six acceptance checks passed. Across four completed tasks, document reads changed 17→0, context 1,838→104 lines (94.3% reduction), rediscovery steps 21→4 (81.0% reduction), and prior-decision recall was 4/4. Unauthorized writes and cross-project leakage were both zero. EXP-15 reported PASS.
- **Limitation retained:** this was a controlled four-task experiment, not production validation or proof of broad generalization. No production code or persistent service was added.
- Frozen facts and traceable source paths are in `FIXTURE.json`; the four-scene storyboard is in `STORYBOARD.json`.

## Successful steps and checks

1. Checked the merged-PR list and PR #46 metadata; compared the frozen claims to the local EXP-15 README, results, baseline, acceptance-test record, and evidence logs.
2. Recorded the bounded upstream audit in `UPSTREAM_AUDIT.md`.
3. Authored one 32-second, four-scene storyboard and one plain HTML/CSS composition at `composition/index.html` (1920×1080, 30 fps; no narration, external media, or animation framework).
4. A one-off Python standard-library structural check passed: both JSON files parse; four contiguous eight-second scenes total 32 seconds; the root composition id/dimensions/duration and all four timed clips agree with the storyboard; there are no external HTML `src`/`href` assets.
5. The single `init` invocation exited successfully and scaffolded in a temporary directory. The single preview invocation started HyperFrames Studio on port 3002 and was stopped cleanly. It reported **1 lint error and 6 warnings**; its bounded output did not provide the rule details. Therefore structural checks passed, but clean HyperFrames lint validation is **not** claimed.

## Bounded attempts and exact blocker

| Attempt | Command / check | Outcome |
| --- | --- | --- |
| Runtime preflight | `node --version`; `npm --version`; `npx --version`; checked `ffmpeg` availability | Node `v22.22.3`; npm/npx `10.9.8`; `ffmpeg` not found on `PATH`. |
| One CLI/init attempt | `npx --yes hyperframes@0.8.137 init mpe-exp24-probe` in a temporary `/tmp` directory, bounded to 90 seconds with npm retries disabled | Exit 0; scaffold created, then temporary scaffold removed. The command's built-in skills freshness check was unavailable and fell back to cloning upstream to discover/install ten agent skills. This side effect was not requested; it was not repeated. |
| One preview attempt | `HOST=0.0.0.0 npx --yes hyperframes@0.8.137 preview --foreground --port 3002` | Studio started; summary reported 1 lint error and 6 warnings. Process stopped cleanly. No screenshot or rendered preview artifact was produced. |
| One MP4 render attempt | `npx --yes hyperframes@0.8.137 render -c ./index.html -o ./exp15-pr46.mp4` from `composition/`, bounded to 75 seconds | Exit 1 before capture: **Chrome not found**. HyperFrames attempted to download `chrome-headless-shell 152.0.7977.30`; all providers failed because the client socket disconnected before TLS was established. Preflight had also confirmed **FFmpeg is absent**. No MP4 was produced. |

No second preview, lint command, browser-install command, FFmpeg installation, system-library repair, second render, or upstream build was attempted. The failure is an Arena executor/runtime blocker, not evidence of a HyperFrames product FAIL.

## Evaluation

- **Grounding:** the displayed claims have source references in the frozen fixture and storyboard; no MP4 existed for a frame-by-frame grounding review.
- **Composition:** source is present and passed the bounded structural check. Preview started, but its nonzero lint summary leaves full composition validation unresolved.
- **Render / repeatability:** blocked before video capture. No output hash, deterministic rerender, or MP4 comparison is claimed.
- **Mobile usefulness:** not evaluated on an MP4. The layout uses large, high-contrast 16:9 text, but that is not a substitute for a phone review.
- **Infrastructure:** no production integration or persistent rendering infrastructure was introduced.

## Changed files

- `experiments/exp-24-hyperframes-pr-video/UPSTREAM_AUDIT.md`
- `experiments/exp-24-hyperframes-pr-video/FIXTURE.json`
- `experiments/exp-24-hyperframes-pr-video/STORYBOARD.json`
- `experiments/exp-24-hyperframes-pr-video/composition/index.html`
- `experiments/exp-24-hyperframes-pr-video/composition/.hyperframes/hf-ids-stamped.json` (generated by the one preview attempt)
- `experiments/exp-24-hyperframes-pr-video/RESULTS.md`

No video binary was created. The CLI's temporary scaffold was removed; its install flow also copied ten skills under `~/.claude/skills` and `~/.agents/skills` outside this repository. No cleanup or further environment inspection was done within this closure run.

## Decision and handoff

**PARTIAL / ADOPT_WITH_CHANGES.** Keep HyperFrames as an optional experiment candidate only; this result does not authorize production integration. The bounded next step is one validation in a suitable local/CI executor with Node 22+, Chrome/Chromium, and FFmpeg: resolve the recorded lint error, render once, and then assess repeatability and phone usefulness in a separately authorized checkpoint. Do not spend more time repairing the Arena executor for EXP-24.

**Terminal boundary reached. Stop here.**


---

# EXP-24 Phase 2 authorization — Agentic text → film

Authorization date: 2026-10-08  
Owner decision: **MERGE**  
Status: **REOPENED FOR OWNER-AUTHORIZED PHASE 2**

The Phase 1 terminal result above remains historical and unchanged: **PARTIAL / ADOPT_WITH_CHANGES**.

New production reference:
- https://alexeykrol.com/blog/2026/10/07/video1/

The reference demonstrates a useful end-to-end operating model: source text → semantic scene breakdown → storyboard/montage plan → stock-footage search/acquisition → ElevenLabs narration → programmatic Remotion assembly → titles/graphics/subtitles/music → mobile-focused revision → final render, with the human primarily reviewing meaning and quality rather than manually operating an editing timeline.

## Adopted Phase 2 changes

- HyperFrames is demoted from experiment center to **optional renderer/component**.
- Remotion is the **preferred baseline compositor** for the next bounded proof.
- Storyblocks is a **reference stock provider**, not mandatory infrastructure.
- ElevenLabs is a **reference voice provider** behind a provider-neutral adapter.
- A stable editorial storyboard becomes the central reviewable artifact before media acquisition/render.
- Mobile readability at an effective 360 px player width becomes an explicit acceptance gate.
- Natural-language revision becomes a first-class checkpoint.
- REAL_FOOTAGE and GENERATIVE modes share one storyboard/voice/subtitle/assembly/QA/revision architecture; only the visual-source adapter differs.
- Publishing remains approval-gated and outside automatic experiment authority.

Next execution starts at **CP-06** and must preserve this Phase 1 record.


---

# CP-13 result — Adopt EXP-23 scene timing/sync contract (single-agent proof)

> **Superseded by the resumed run below.** The NOT_EVALUATED / SOURCE_ACCESS_BLOCKED record in this section is kept as history. The owner-authorized sanitized fixture unblocked the run.

Run date: 2026-10-10 (UTC) · Executor: Arena Agent Mode, single agent · Branch: `arena/75c6ba59-murat-project-engineer` · Base: `main` @ `19dd6a096433edfe5742d667cfc70e8fda8d3434`

```text
RESULT: NOT_EVALUATED — SOURCE_ACCESS_BLOCKED
SINGLE_AGENT: YES
FIXTURE: E01-S005 «Молодой продюсер открывает конверт» (Murkin1980/AI-serial-v2 / TEASER_SCENE_SHEETS.md) — NOT READABLE from this session
SOURCE COVERAGE: NOT MEASURED (0 source actions read; 0 mapped; no coverage claim made)
VISUAL BEATS: 0 (no storyboard produced)
MEDIA GENERATIONS USED: 0
REMOTION PREVIEW: NOT BUILT
MOBILE QA: NOT RUN
REVISION A: NOT RUN
REVISION B: NOT RUN
REVISION C: NOT RUN
MINIMAL_DIFF: NOT TESTED
CANON CHANGES: NONE
DEEP_CHANGE: NO
RECOMMENDATION: Keep CP-13 open; do not count the adoption as proven. Re-run after the owner grants read access.
NEXT ACTION: Owner grants this Arena GitHub connection read access to Murkin1980/AI-serial-v2 (or approves a read-only copy of TEASER_SCENE_SHEETS.md), then resume at Step 1 (scene contract freeze).
```

## Startup and bootstrap

- EXP-29 bootstrap built from current `main` checkout with `bootstrap_builder.py build --experiment EXP-24 --checkpoint CP-13`; `verify` returned **FRESH** (`evidence/cp13/ARENA_CONTEXT.json`, `.md`; derived, non-authoritative).
- Governance (`AGENTS.md`), EXP-24 `README.md`, `ARENA_TASK.md` (CP-13 section), `RESULTS.md` and EXP-23 `FINDINGS.md` were read. EXP-23 was not rerun.

## Source access — the stop condition

The fixture is private. The canonical source was checked read-only with `gh` (repo view, API contents/branches), `git clone`, `git ls-remote` and the visible repository list. Every access returned HTTP 403 "Resource not accessible by integration" / "Write access to repository not granted", and `AI-serial-v2` is absent from the visible repository list. No GitHub connector is available to load a different scope. Full log: `evidence/cp13/SOURCE_ACCESS.md`.

Per the task, the run stopped with **`SOURCE_ACCESS_BLOCKED`**. No scene text was reconstructed from memory, no beats were invented, and `AI-serial-v2` was not modified.

## Why the verdict is NOT_EVALUATED, not PARTIAL or FAIL

- PARTIAL requires the contract and revision logic to be working and only one runtime/render/media-cap item to be blocked. None of the contract, storyboard, media, preview or revision steps has run, so that condition does not hold.
- FAIL requires the workflow itself to need excessive manual work or to lose control of changes. No such evidence exists; the single-agent chain was never reached.

The blocker is a source-access permission on the canonical input. It is not evidence about the pipeline's quality, controllability or minimal-diff behaviour.

## Reference evidence not reused as CP-13 proof

EXP-23 CP-02 (20/20 action steps mapped, 0 omitted / 0 added, 6/6 previs stills, E01-S005 APPROVED FOR VISUAL DEVELOPMENT) remains EXP-23 historical evidence. It was produced in an earlier session against the source. It is not re-verified here and is not counted as CP-13 source coverage.

## Adopted schema / contract

None adopted in this run. The contract (scene → ordered beats → marks → cues/timings → per-beat asset, with timing treated as presentation metadata) was specified in the CP-13 task but not yet proven on a fixture, so no schema is claimed as adopted.

## Changed files

- `experiments/exp-24-hyperframes-pr-video/RESULTS.md` (this CP-13 section appended; Phase 1 and Phase 2 records unchanged)
- `experiments/exp-24-hyperframes-pr-video/evidence/cp13/ARENA_CONTEXT.json` (derived bootstrap packet, FRESH)
- `experiments/exp-24-hyperframes-pr-video/evidence/cp13/ARENA_CONTEXT.md` (derived bootstrap view)
- `experiments/exp-24-hyperframes-pr-video/evidence/cp13/SOURCE_ACCESS.md` (access-check log)

No storyboard, media manifest, media files, composition, render or video binary was created. No registry status was changed.

## Graceful handoff

- **STATE:** CP-13 paused before Step 1. Nothing downstream started.
- **EVIDENCE:** `evidence/cp13/SOURCE_ACCESS.md`, `evidence/cp13/ARENA_CONTEXT.*`.
- **CHANGES:** documentation/evidence only (listed above). No canon, no media, no render.
- **RESULT:** NOT_EVALUATED — SOURCE_ACCESS_BLOCKED.
- **BLOCKER:** Arena GitHub connection lacks read access to private `Murkin1980/AI-serial-v2`.
- **NEXT ACTION:** Owner grants read access (or supplies an approved read-only copy of `TEASER_SCENE_SHEETS.md`); then re-run EXP-24 CP-13 from Step 1 using the same bootstrap command (`--experiment EXP-24 --checkpoint CP-13`) after `verify` returns FRESH.
- **HANDOFF:** this PR, for review. Do not merge automatically.


---

# CP-13 resumed — single-agent scene proof (owner-authorized sanitized fixture)

Run date: 2026-10-10 (UTC) · Executor: Arena Agent Mode, single agent · Branch: `arena/75c6ba59-murat-project-engineer` (merged `origin/main` @ `e476115`) · PR #80 updated, not merged.

```text
RESULT: PASS (bounded CP-13 proof; visual quality not an acceptance target)
SINGLE_AGENT: YES
ADOPTION: CP-13 contract ADOPTED for bounded EXP-24 use (scene -> beats -> marks -> cues -> timings -> per-beat asset); no production integration
FIXTURE: E01-S005 via fixtures/E01-S005_SANITIZED.md (canonical blob fd049ca5faafc31203cde607fbdb17bd6b17789b; Murkin1980/AI-serial-v2 episodes/01_SEVEN_MINUTES/TEASER_SCENE_SHEETS.md). Derived fixture, not a canon source.
SOURCE COVERAGE: 20/20 A01-A20 mapped; omitted 0; added 0 (cp13/SCENE_CONTRACT.json; check_cp13.py PASS). Coverage was checked against the sanitized ledger only; the private source itself was not re-read.
VISUAL BEATS: 6 (B01-B06 = owner-suggested grouping; each beat = one asset slot)
MEDIA GENERATIONS USED: 8 of ~10 this turn (6 test visuals; B04 revision: v2 generated and REJECTED as a near-duplicate, v3 generated and used). No audio/TTS generated.
REMOTION PREVIEW: Remotion 4.0.534; preview-v1 rendered (24.0 s, 1280x720, 30 fps, H.264); revised preview rendered (24.5 s). Renders kept outside Git with sha256 (cp13/revisions/render_sha256.txt).
MOBILE QA: PASS at 360 px effective width (scaled MP4 frames, evidence/cp13/mobile360-v1 and mobile360-v2-revised); captions 15.75 px effective, <=2 lines, no clipping, no service/beat labels, no legible text in assets. Known: B01 caption partly covers the envelope (see defects).
REVISION A: PASS. "Make B03 30% longer, no asset/other-beat change": B03 duration 5.0 -> 6.5 s (+30%) and its caption-out cue 4.7 -> 6.2 s. 2 fields changed, both in B03; manifest unchanged. Frame check: B01, B02 identical; B03 head 101/161 by frame index (the rest is H.264 lookahead ahead of the change point at frame 366; stills 330/360 are hash-identical and 380 differs as expected); B04-B06 identical after the 45-frame shift (300/300).
REVISION B: PASS. "Replace B04 visual, keep narration/timing and other approved assets": B04 asset v1 -> v3 (v2 rejected). Storyboard 0 field changes; manifest 1 entry changed (B04) plus disclosed removal of a bookkeeping counter. Frame check: B01, B02, B03, B05, B06 identical; only B04 frames changed (1/90 identical).
REVISION C: PASS. "Make final beat shorter and remove its on-screen text, previous beats unchanged": B06 duration 4.5 -> 3.5 s, caption null, caption cues removed. 3 fields changed, all in B06; manifest unchanged. Frame check: B01-B05 identical; B06 changed (frame 625 hash-identical to the pre-change state, so the residual 9-frame B05 mismatch is encoder noise).
MINIMAL_DIFF: PASS for all 3 revisions (field-level via tools/semantic_diff.py; frame-level via tools/frame_compare.py; diff logs in cp13/revisions/). Nothing was rebuilt wholesale.
CANON CHANGES: NONE (AI-serial-v2 untouched; fixture derived and labelled as non-canon)
DEEP_CHANGE: NO (no new repo/service/DB/queue; no publish)
RECOMMENDATION: Accept the CP-13 contract pattern for bounded EXP-24 use. Do not treat the generated visuals as quality evidence.
NEXT ACTION: Owner review of PR #80. Separate bounded checkpoint for (a) caption placement that avoids key props at 360 px, (b) B04 asset/caption alignment, (c) Remotion company-license check if used beyond individual/small-entity scope.
```

## Step results

| Step | Artifact | Status |
|---|---|---|
| 0 Startup | `evidence/cp13/ARENA_CONTEXT.*` (EXP-29 bootstrap, FRESH) | done (earlier) |
| 1 Scene contract | `cp13/SCENE_CONTRACT.json` (20 actions, 6 beats, coverage ledger, dialogue functions D01/D02, invariants; no timing) | FROZEN |
| 2 Storyboard | `cp13/EDITORIAL_STORYBOARD.json` (purpose, grounding, visual intent, caption, duration, marks, cues, asset slot) | done; revised A/C |
| 3 Test visuals | `remotion/public/assets/beats/` (6 JPEG derived from raw PNG; raw kept outside repo with sha256) | 6 final + 2 B04 attempts |
| 4 Media manifest | `cp13/MEDIA_MANIFEST.json` (one entry per beat, provenance, sha256, attempt, approval) | done; revised B |
| 5 Remotion preview | `remotion/src/` (Root, Scene, data), `remotion/package.json` | preview v1, revised preview |
| 6 Mobile QA | `evidence/cp13/mobile360-v1/`, `mobile360-v2-revised/` | PASS with defects listed |
| 7 Revisions A/B/C | `cp13/revisions/` (snapshots, semantic diffs, frame comparisons) | all PASS |

## Mobile QA detail (360 px)

- Caption font 56 px at 1280 px width, which is 15.75 px effective at 360 px. Readable in every sampled frame.
- Longest captions wrap to 2 lines; no overflow or clipping.
- Frames contain no beat IDs, scene numbers, or service labels.
- Generated images contain no legible text. Some monitors show blurred marks that are not readable at 360 px.
- Automated text-fit check: NOT done (estimated only). Verification is visual on sampled frames, not a DOM measurement.

## Defects and limitations (recorded, not fixed in this run)

1. **B01 caption covers part of the envelope** at 360 px. The key prop is still understandable, but this is a layout defect. Fix would be a separate caption-placement checkpoint.
2. **B04 caption vs. asset mismatch.** Caption says "He looks around. Checks the time." The v3 replacement emphasises the clock; the look-around is weakly shown. Accepted as a test limitation.
3. **Continuity is imperfect.** Each still was generated separately; B04 v3 has a different framing and palette. This is a downstream visual-generation concern, as the contract states.
4. **Encoder lookahead.** Frame-index comparisons show ~34–40 frame differences just before any change point. Stills at those points were hash-identical, so the differences are H.264 rate-control artifacts, not content changes. The method is explained in `frames_*` files.
5. **Remotion licence.** Free for individuals and organisations of up to three employees; a company licence is required beyond that (remotion.dev/license). Owner to confirm before any use beyond this experiment.
6. **Chromium source.** No system browser exists in the sandbox. Chromium 153 came from the `@sparticuz/chromium` npm package (libraries unpacked into `/tmp`, not committed). Render is reproducible only where the same binary is available.
7. **Source verification.** Coverage was checked against the owner-provided sanitized ledger. The private canonical text was not re-read.

## Changed files (this run)

- `RESULTS.md` (this section; earlier CP-13 record marked superseded)
- `cp13/`: `SCENE_CONTRACT.json`, `EDITORIAL_STORYBOARD.json`, `MEDIA_MANIFEST.json`, `README.md`, `revisions/` (v1 snapshot, rev-A/B/C snapshots, semantic diffs, frame comparisons, render hashes)
- `remotion/`: `package.json`, `package-lock.json`, `remotion.config.ts`, `tsconfig.json`, `.gitignore`, `src/{index,Root,Scene,data}.ts(x)`, `public/assets/beats/*.jpg` (B01–B06 v1, B04 v3)
- `tools/`: `check_cp13.py`, `semantic_diff.py`, `frame_compare.py`
- `evidence/cp13/`: `mobile360-v1/`, `mobile360-v2-revised/`, earlier `ARENA_CONTEXT.*`, `SOURCE_ACCESS.md`

Not committed (kept outside Git, hashes recorded): raw PNG originals (`/home/user/exp24-artifacts/raw/`), MP4 renders (`/home/user/exp24-artifacts/renders/`), `remotion/node_modules/`, `remotion/out/`.

## Graceful handoff

- **STATE:** CP-13 resumed and completed as bounded proof. All steps executed by Arena.
- **EVIDENCE:** `cp13/`, `cp13/revisions/`, `evidence/cp13/mobile360-*`.
- **CHANGES:** as listed above; no canon, no publish, no merge.
- **RESULT:** PASS (bounded).
- **BLOCKER:** none for this run. Open items are the defects above.
- **NEXT ACTION:** owner review of PR #80; separate checkpoint for caption placement and B04 alignment; licence check if Remotion goes beyond the free tier.
- **HANDOFF:** PR #80, for review. Do not merge automatically.

