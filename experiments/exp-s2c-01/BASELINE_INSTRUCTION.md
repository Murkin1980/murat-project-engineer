# EXP-S2C-01 — Arm A Baseline Instruction

## Objective
Reconstruct the frozen dashboard screen from `experiments/exp-s2c-01/reference/desktop.png` and `mobile.png` using a standard one-pass screenshot-to-code implementation.

## Constraints & Rules
1. **Single-Pass**: The agent inspects the frozen reference images and writes a complete, standalone frontend implementation in `experiments/exp-s2c-01/baseline/`.
2. **No Visual Feedback Loop**: Do NOT compare rendered output against the reference screenshot during authoring. Do not run iterative visual correction passes.
3. **Render-Fixes Only**: Only technical bugfixes necessary to get the HTML/CSS/JS page to render in the browser are permitted (e.g. syntax error or missing tag); no visual styling iterations.
4. **No Screenshot-As-Layout**: Forbidden to use the reference screenshot as an image background, slice it into image chunks, or trace pixels. Must be real HTML and CSS elements.
5. **No Source Inspection**: Do NOT inspect `Murkin1980/salamat-projects-dashboard` source code.
6. Once rendered, freeze the baseline output, capture desktop and mobile renders, record LOC, time, and cycle count, and do not polish further.
