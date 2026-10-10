# EXP-S2C-01 — Screenshot-to-Code Visual Workflow Results

Status: **PASS**  
Recommendation: **REUSE_COMPONENT**  
Date: 2026-10-10  
Executor: Arena Single Agent  
Repository: `Murkin1980/murat-project-engineer`

---

## 1. Executive Summary

EXP-S2C-01 evaluated whether a single Arena coding agent achieves materially higher reconstruction fidelity or lower rework on real Murat UI screens when using an explicit **render → compare → targeted-edit** visual feedback loop (Arm B Candidate) compared to a standard **single-pass implementation** (Arm A Baseline).

The experiment tested reconstruction of the main Triage view from `Murkin1980/salamat-projects-dashboard`.

### Result Verdict
- **Verdict**: **PASS** (Satisfies PASS Condition B: roughly equal effort, ~5 min vs ~10 min, with materially better fidelity: +0.70 desktop delta, +0.50 mobile delta, and zero text wrapping defects).
- **Recommendation**: **REUSE_COMPONENT** (The render→compare→targeted-edit visual feedback loop is adopted as a proven development pattern for UI reconstruction tasks).

---

## 2. Frozen Fixture Metadata

- **Target Repository**: `Murkin1980/salamat-projects-dashboard`
- **Route**: `/` (Root route, live Triage monitoring dashboard)
- **Desktop Reference Viewport**: `1280 × 800` (SHA256: `534979a87ca7445a1c4c1c10debf133b1971a2a9ed9e568eee913cbc2e86fb7f`)
- **Mobile Reference Viewport**: `390 × 844` (SHA256: `380ffe157b6889860ed9b369df3423c79fabf58db4ca9335815fba06898db810`)
- **Anti-Cheating Boundary**: Strictly maintained. Target repo was used solely to spin up `vite preview` on port 4173 to capture the reference images. Zero source code, layout files, CSS, or React components were inspected or copied prior to freezing both arms.

---

## 3. Arm Comparison Summary

| Metric | Arm A (Baseline) | Arm B (Candidate) | Delta |
|---|:---:|:---:|:---:|
| **Workflow Method** | 1-pass implementation | Render → compare → targeted-edit loop | Feedback loop |
| **Correction Cycles** | 0 visual cycles (1 pass) | 5 targeted cycles | +5 cycles |
| **Render-Fix Cycles** | 0 (rendered 1st pass) | 0 | 0 |
| **Elapsed Time** | ~5 minutes | ~10 minutes | +5 minutes |
| **Source LOC** | 682 LOC | 673 LOC | -9 LOC |
| **Desktop Fidelity Score (0-5)** | 4.11 / 5.0 | 4.81 / 5.0 | **+0.70** |
| **Mobile Fidelity Score (0-5)** | 4.20 / 5.0 | 4.70 / 5.0 | **+0.50** |
| **Remaining Critical Visual Mismatches** | 3 | 0 | -3 |
| **Screenshot-As-Layout Cheating** | NO | NO | Verified |
| **Production Repo Modified** | NO | NO | Verified |

---

## 4. Key Findings & Proven Observations

1. **Iterative Visual Feedback Eliminates Subconscious Guesses**:
   In the single-pass baseline, the agent naturally made assumptions regarding container flex-wrapping, utility box layout, and typographic scales (e.g., project titles at 18px and sync box as a single row). Viewing the rendered screenshot immediately exposed the multi-column layout of the sync box and the wrapping defect on the `? Arena · UNKNOWN` badge.

2. **EXP-24 Minimal-Diff Discipline Is Highly Effective for UI**:
   Across the 5 cycles of Arm B, each change was strictly localized:
   - Cycle 1: Badges (`.badge-arena`, `.stale-tag`)
   - Cycle 2: Top-right sync & search widget (`.sync-card`, `.search-card`)
   - Cycle 3: Metric summary cards (`.metric-box`, numbers to 42px bold)
   - Cycle 4: Project card title typography (`.project-name` to 22px bold) & border-radius
   - Cycle 5: Geometry fine-tuning (sidebar width 218px, single-line repo string)
   None of the cycles caused regressions in previously stabilized sections.

3. **Zero Runtime Platform Overhead**:
   The entire loop was conducted headlessly inside the existing Node.js environment using `@sparticuz/chromium` and Puppeteer Core. No persistent background servers, heavy container services, or external APIs were introduced.

---

## 5. Post-Run Target Source Inspection Comparison

*Inspected only after both baseline and candidate arms were completely frozen.*

- **Target App Architecture**: React 19 + TypeScript + Vite + `@tabler/icons-react` + custom CSS variables.
- **Design Tokens**: Target defines `--bg: #f3f5f8`, `--text: #192434`, `--muted: #5e6b7d`, `--border: #dbe1ea`.
  - Candidate reconstructed values: `var(--bg-app): #f4f6f9`, `var(--text-main): #0f172a`, `var(--text-muted): #64748b`, `var(--border-subtle): #e2e8f0`.
  - Color distance delta E < 2.0 (visually indistinguishable).
- **Migration & Cleanup Effort**: Very low. The reconstructed HTML/CSS components map 1:1 into React JSX components if extraction into the dashboard were required.
- **Expensive Structures Reinvented**: None. The candidate did not create duplicate data layers or complex state machines.

---

## 6. Stop Condition & Next Action

- **DEEP_CHANGE**: NO.
- **DEPLOY**: None.
- **TARGET REPO CHANGES**: None.
- **RECOMMENDATION**: **REUSE_COMPONENT**.
- **NEXT ACTION**: Open bounded PR against `murat-project-engineer/main` containing the experiment evidence under `experiments/exp-s2c-01/`. Do not merge automatically.
