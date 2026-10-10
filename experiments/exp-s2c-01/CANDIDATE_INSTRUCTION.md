# EXP-S2C-01 — Arm B Candidate Instruction

## Objective
Reconstruct the frozen dashboard screen from `experiments/exp-s2c-01/reference/desktop.png` and `mobile.png` using an explicit render → compare → targeted-edit visual feedback loop.

## Constraints & Rules
1. **Clean Directory**: Start from `experiments/exp-s2c-01/candidate/`. Do NOT copy code from Arm A.
2. **Initial Render**: Write an initial implementation from the reference screenshots, render it in headless Chromium, and capture the initial render (Cycle 0).
3. **Iterative Visual Feedback Loop**:
   - Compare rendered screenshot against frozen reference screenshot.
   - Identify the single largest visual mismatch (layout, spacing, typography hierarchy, component proportions, borders/radii/colors, icon/asset placement).
   - Apply a targeted, minimal-diff edit strictly to the region responsible for that mismatch (following the EXP-24 minimal-diff lesson).
   - Re-render both desktop and mobile views.
   - Record the cycle log entry: mismatch description, changed region/files, before/after comparison, and whether fidelity improved, worsened, or had no effect.
   - Repeat up to a maximum of **5 visual correction cycles**.
4. **No Screenshot-As-Layout**: Forbidden to use the reference screenshot as an image background, slice it into image chunks, or trace pixels.
5. **No Source Inspection**: Do NOT inspect `Murkin1980/salamat-projects-dashboard` source code until both arms are frozen.
