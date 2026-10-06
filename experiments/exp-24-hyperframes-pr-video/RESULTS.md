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
