# EXP-19 — Shir-man Trend Intake and Agent-Readable Surface

- **Experiment ID**: EXP-19
- **Checkpoint**: CP-01
- **Owning Project**: Murat Project Engineer
- **Status**: PASS
- **Date**: 2026-09-29
- **Source Reference**: https://shir-man.com/homepage/

---

## 1. Goal

Test whether the trend intake mechanics and summary patterns from **Shir-man** (Denis Trends) can provide **Murat Project Engineer (MPE)** with a lightweight, agent-readable layer for:
1. Fast intake of external product/technology signals.
2. Conversion into a compact, standardized signal card schema.
3. Batch filtering through the **Murat Project Engineer New Idea Filter** (`docs/NEW_IDEA_FILTER_POLICY.md`).
4. Extracting actionable, high-value signals with measurable outcomes for existing active portfolio projects without manual re-processing.

---

## 2. Methodology & Scope (CP-01)

This experiment is strictly bounded within `experiments/exp-19-shirman-trend-intake/` under MPE Guardrails:
- **No new repository** created.
- **No background crawler, scraper daemon, or persistent queue** introduced.
- **No database** added.
- **No changes** to core MPE execution contracts or Option A+ boundaries.

### CP-01 Steps Executed:
1. **Source Study**: Analyzed Shir-man (`https://shir-man.com/homepage/`) patterns: concise 1-2 sentence delta summaries ("what changed"), multi-channel categorization, uniform item cards.
2. **Signal Intake**: Curated 15 real external developer tools, agent skills, model benchmarks, and tech trends.
3. **New Idea Filter Evaluation**: Passed every signal through `docs/NEW_IDEA_FILTER_POLICY.md` rules and assigned exact MPE dispositions (`EXTEND_EXISTING`, `REUSE_COMPONENT`, `EXPERIMENT`, `HOLD`, `REJECT`).
4. **Agent-Readable Schema**: Designed a token-efficient Markdown/JSON schema (`FORMAT.md`) for downstream AI agent consumption without context blowout or manual re-formatting.
5. **Shortlist & Evidence Consolidation**: Extracted high-value signals targeting active portfolio projects (`murat-project-engineer`, `ai-microtask-factory`, `mebelflow-ai`, `mebeldocs-ai`) and documented findings (`FINDINGS.md`).

---

## 3. Results & Findings Summary

| Metric | Result | Target / Criteria |
| :--- | :--- | :--- |
| **Processed Signals** | **15** | $\ge 10$ |
| **New Idea Filter Coverage** | **100% (15/15)** | 100% |
| **Actionable Useful Signals** | **7** | $\ge 3$ |
| **Target Projects Covered** | **4 active projects** (`MPE`, `ai-microtask-factory`, `mebelflow-ai`, `mebeldocs-ai`) | Active portfolio projects |
| **Token Savings vs Raw Text** | **~68% reduction** (~180 tokens/card vs ~550 tokens raw article) | Reduced manual context load |
| **Infrastructure Overhead** | **0 bytes / 0 services** (Pure file-based artifact) | No new DB/crawler/queue |
| **Deep Change Triggered** | **NO (`false`)** | Must be `false` |
| **Final Result** | **PASS** | PASS |

---

## 4. Top 3 Actionable Next Steps

1. **MPE Agent Architecture Diagrams (`reladraw/reladraw`)**:
   - **Disposition**: `REUSE_COMPONENT`
   - **Target**: `murat-project-engineer`
   - **Next Step**: Adopt Reladraw's relative text-based diagram schema into `contracts/` and Expert Playbooks so agents generate clean, deterministically editable architecture diagrams in Run Reports without Mermaid layout bugs.

2. **MebelFlow AI Showroom Audio Intake (`SonicloudTech/sonicloud_opensdk`)**:
   - **Disposition**: `REUSE_COMPONENT`
   - **Target**: `mebelflow-ai`
   - **Next Step**: Reuse BLE audio intake SDK client patterns for MebelFlow AI rep badge recording in showroom pilots to achieve zero-latency offline capture.

3. **AI Microtask Offline Acceptance Receipts (`seamusc/papermono-shopping-list`)**:
   - **Disposition**: `EXTEND_EXISTING`
   - **Target**: `ai-microtask-factory`
   - **Next Step**: Extend Stage 4 Spreadsheet Cleanup with PaperMono's local-first sync and acceptance receipt state pattern for offline field microtask verification.

---

## 5. Artifact Index

- **`SIGNALS.md`**: Complete catalog of 15 processed signal cards with 10 mandatory fields and New Idea Filter decisions.
- **`FORMAT.md`**: Canonical agent-readable JSON Schema, Markdown card specification, and token-efficiency analysis.
- **`FINDINGS.md`**: Detailed evaluation of Shir-man mechanics, noise ratio, portfolio alignment, guardrail check, and final decision.

---

## 6. Final Decision & Recommendation

- **Verdict**: **PASS**
- **Decision**: **CONTINUE** (Adopt Shir-man compact signal intake format as a standard file-based intake pattern for MPE backlog grooming; do NOT build persistent crawlers or scrapers).
