# WaveSpeed Evaluation — experimental series

Date registered: 2026-10-13
Status: PLANNED (registration only; no tests executed)
MPE New Idea Filter: **EXPERIMENT**
Canonical registry: `experiments/EXPERIMENT_REGISTRY.json`

## Rationale and boundaries

Evaluate existing WaveSpeed browser utilities for practical relief in AI Serial, Salamat Mebel, Murat House and Grand Mebel without introducing competing infrastructure. Existing image/video tools, CAD workflows and MPE patterns are control arms. Prefer reuse; **no new repository, runtime, integration, dependencies or production changes**. External service functionality, price, availability, Kazakh support and output formats require runtime verification; catalog marketing is not PASS evidence.

Do not upload customer data, faces without permission, confidential documents or production assets to cloud tools before privacy/licensing assessment. Browser-local claims must be validated. No paid credits, installations, credentials, integrations, manufacturing, merges or deploys without separate authorization.

## Candidate experiments

| ID | Priority | Owner | Experiment | Gate |
|---|---|---|---|---|
| W01 | P0 | AI Serial | Cinematic LUT Bible | PLANNED |
| W02 | P0 | AI Serial | AI Video Restoration | PLANNED |
| W03 | P0 | Salamat Mebel | Image to DXF / CNC | PLANNED |
| W04 | P0 | Salamat Mebel | Image Upscale & Print | PLANNED |
| W05 | P1 | Salamat Mebel | CAD Format Bridge | PLANNED |
| W06 | P1 | AI Serial | Character & Background Isolation | PLANNED |
| W07 | P1 | AI Serial / Murat House | Video Post-production Kit | PLANNED |
| W08 | P1 | AI Serial / Murat House | Kazakh Speech & Subtitles | PLANNED |
| W09 | P2 | Grand Mebel Document Control | Document Quality Pipeline | PLANNED |
| W10 | P2 | Murat Project Engineer | Browser vs Desktop Performance | PLANNED |

## Fixed test cards (hypotheses, not verified capabilities)

### W01 — Cinematic LUT Bible
- Target: AI Serial
- Hypothesis and acceptance: Unify AI Serial color across generators using reusable .cube LUTs; 12 frames, three moods, at least 80% acceptable without manual correction.
- Candidate: https://wavespeed.ai/free-tools/lut-generator
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W02 — AI Video Restoration
- Target: AI Serial
- Hypothesis and acceptance: Compare enhancement/upscaling on three real short AI-generated clips; at least two improve without material new artifacts or unreasonable cost.
- Candidate: https://wavespeed.ai/free-tools
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W03 — Image to DXF / CNC
- Target: Salamat Mebel
- Hypothesis and acceptance: Test WaveSpeed image-to-DXF on Subaru stencil; dimensions, closed contours, bridges, no loose islands and machine import; approve PNG preview before final manufacturing DXF.
- Candidate: https://wavespeed.ai/free-tools/image-to-dxf-converter
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W04 — Image Upscale & Print
- Target: Salamat Mebel
- Hypothesis and acceptance: Compare standard 2x/4x and tiled enhancement on 8x3.2 m banner; preserve faces, no tile seams, verify printer DPI and viewing distance.
- Candidate: https://wavespeed.ai/free-tools/image-upscaler
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W05 — CAD Format Bridge
- Target: Salamat Mebel
- Hypothesis and acceptance: Compare 3D model import/export with existing CAD tools using 3 model fixtures; correct dimensions required. Do not assume OBJ/STL solves PRO100 .meb.
- Candidate: https://wavespeed.ai/free-tools/3d-model-viewer
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W06 — Character & Background Isolation
- Target: AI Serial
- Hypothesis and acceptance: Test subject extraction on ten AI Serial frames; at least eight acceptable masks preserving hair, clothing and outlines.
- Candidate: https://wavespeed.ai/free-tools/segment-anything
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W07 — Video Post-production Kit
- Target: AI Serial / Murat House
- Hypothesis and acceptance: Test 30–60 s complete browser postproduction (format conversion, captions, audio and export), against existing tool chain.
- Candidate: https://wavespeed.ai/free-tools
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W08 — Kazakh Speech & Subtitles
- Target: AI Serial / Murat House
- Hypothesis and acceptance: Measure Kazakh ASR and subtitle alignment with consented sample; WER target <=15%, subtitle drift <=0.3s; assess actual language support first.
- Candidate: https://wavespeed.ai/free-tools/speech-to-text
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W09 — Document Quality Pipeline
- Target: Grand Mebel Document Control
- Hypothesis and acceptance: Test OCR, PDF diff, preflight on anonymized sample invoices/acts; zero errors in mandatory fields; no live financial document uploads.
- Candidate: https://wavespeed.ai/free-tools/document-compare
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

### W10 — Browser vs Desktop Performance
- Target: Murat Project Engineer
- Hypothesis and acceptance: Benchmark mobile-browser vs desktop on identical files; record timings, quality and memory; install only if practical gain is evidenced.
- Candidate: https://wavespeed.ai/desktop
- Baseline: compare with current established workflow on the same fixtures; record time, effort, output quality, failure rate and cost (including setup).
- State: PLANNED / NOT_RUN; record actual capability discovery before proceeding.

## Execution order and evidence

1. P0 (W01–W04) first, independently bounded. Each task pre-registers test inputs (or hashes), device/software environment, baseline, expected benefit, safety and acceptance; select privacy-safe fixtures.
2. Inspect results and decide whether any P1 is worth running; P2 only if genuine recurring friction remains.
3. For each experiment record `RESULTS/Wxx.md` with STATE / EVIDENCE / CHANGES / RESULT / BLOCKER / NEXT ACTION / HANDOFF, baseline measurements, screenshots or artifact hashes, actual money spent, provider limitations, PASS/PARTIAL/BLOCKED, and ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT. No PASS on description alone.
4. After accepted test results, separately decide component reuse in target projects through their own policies and deep-change gates.

Proposed economics: save >=30% handling time versus baseline where applicable, or demonstrate material quality/rework gains. Track verified relief only after real outcome. No new VRU from registration.

## Ownership

MPE keeps experiment registrations and evidence links canonical. Project repos remain the owners of any subsequent project-specific implementation. Dashboard is read-only derived from canonical registry; do not edit dashboard snapshot or deploy as part of registration.
