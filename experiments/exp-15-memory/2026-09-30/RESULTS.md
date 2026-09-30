# EXP-15 — Quantitative Results & Comparative Evaluation

**Experiment:** EXP-15 (MPE Project Memory Layer)  
**Run Date:** 2026-09-30 (UTC)  
**Evaluator:** `experiments/exp-15-memory/2026-09-30/harness/run_baseline_comparison.py`  
**Terminal Outcome:** `PASS`  

---

## 1. Comparative Results Summary

The controlled experiment evaluated **Mode A (Current Baseline)** versus **Mode B (Memory-Layer Prototype)** across four real completed MPE tasks.

| Benchmark Task | Metric | Mode A (Current Baseline) | Mode B (Memory Layer) | Delta / Relief |
| :--- | :--- | :--- | :--- | :--- |
| **TASK-MPE-08**<br>(BrowserAct Scrape & Automation) | Unnecessary Repo Reads<br>Context Lines Inspected<br>Rediscovery Steps<br>Decision Recalled<br>Contradictory Guidance | 5 doc reads<br>465 lines<br>6 steps<br>Yes (after scan)<br>No | **0 doc reads**<br>**26 lines**<br>**1 lookup step**<br>**Yes (immediate)**<br>**No** | **-5 reads (-100%)**<br>**-439 lines (-94.4%)**<br>**-5 steps (-83.3%)**<br>Immediate recall<br>0 violations |
| **TASK-MPE-11**<br>(Runtime Coordination Architecture) | Unnecessary Repo Reads<br>Context Lines Inspected<br>Rediscovery Steps<br>Decision Recalled<br>Contradictory Guidance | 4 doc reads<br>382 lines<br>5 steps<br>Yes (after scan)<br>No | **0 doc reads**<br>**26 lines**<br>**1 lookup step**<br>**Yes (immediate)**<br>**No** | **-4 reads (-100%)**<br>**-356 lines (-93.2%)**<br>**-4 steps (-80.0%)**<br>Immediate recall<br>0 violations |
| **TASK-MPE-12**<br>(CLEARS Triage Reliance) | Unnecessary Repo Reads<br>Context Lines Inspected<br>Rediscovery Steps<br>Decision Recalled<br>Contradictory Guidance | 4 doc reads<br>564 lines<br>5 steps<br>Yes (after scan)<br>No | **0 doc reads**<br>**26 lines**<br>**1 lookup step**<br>**Yes (immediate)**<br>**No** | **-4 reads (-100%)**<br>**-538 lines (-95.4%)**<br>**-4 steps (-80.0%)**<br>Immediate recall<br>0 violations |
| **TASK-MPE-18**<br>(Pirate Face Model Resilience) | Unnecessary Repo Reads<br>Context Lines Inspected<br>Rediscovery Steps<br>Decision Recalled<br>Contradictory Guidance | 4 doc reads<br>427 lines<br>5 steps<br>Yes (after scan)<br>No | **0 doc reads**<br>**26 lines**<br>**1 lookup step**<br>**Yes (immediate)**<br>**No** | **-4 reads (-100%)**<br>**-401 lines (-93.9%)**<br>**-4 steps (-80.0%)**<br>Immediate recall<br>0 violations |

---

## 2. Aggregated Comparative Metrics

```text
================================================================================
EXP-15 AGGREGATED METRICS SUMMARY
================================================================================
Benchmark Tasks Tested:                  4 tasks
Total Baseline Document Reads:           17 reads (1,838 lines)
Total Memory Prototype Document Reads:   0 reads (104 lines of bounded context)
--------------------------------------------------------------------------------
Unnecessary Document Reads Reduction:    100.0% (17 reads -> 0 reads)
Context Footprint Reduction:             94.3% (1,838 lines -> 104 lines)
Rediscovery Step Reduction:              81.0% (21 steps -> 4 lookup steps)
Prior Decision Recall Accuracy:          100.0% (4 / 4 tasks)
Contradictory Guidance Rate:             0.0% (0 / 4 tasks)
Provenance Correctness:                  100.0% (8 / 8 items cite valid Git files)
Proposed Memory Delta Validity:          100.0% (4 / 4 valid ProposedMemoryDelta schemas)
Unauthorized Canonical Writes:           0 (fail-closed gating enforced)
Cross-Project Leakage:                   0 (scope isolation strictly enforced)
================================================================================
```

---

## 3. Task-by-Task Qualitative Analysis

### Task 1: TASK-MPE-08 (BrowserAct Scraping and Automation Boundaries)
- **Baseline Observation:** In Mode A, an agent answering whether BrowserAct can be used for authenticated scraping must search the codebase, read `docs/NEW_IDEA_FILTER_POLICY.md` to confirm filter placement, read `docs/evaluations/BROWSERACT_EVALUATION.md` to review the CLI evaluation, read `docs/evaluations/BROWSER_ACQUISITION_ROLE.md` to understand role limitations, and read `evidence/stage2/RUN-08_REPORT.json` to verify runtime cleanup gates. This took 5 document reads and 465 lines of inspection.
- **Memory Prototype Observation:** In Mode B, a single bounded query for `"browseract"` returned `MEM-MPE-001` (approved as `REUSE_COMPONENT`) and `MEM-MPE-002` (strictly `PUBLIC_WEB_ONLY`, delete isolated Chrome after use). The agent immediately answered the query without opening any repository files. The proposed delta was `NO_CHANGE`.

### Task 2: TASK-MPE-11 (Runtime Coordination Messaging Architecture)
- **Baseline Observation:** In Mode A, evaluating whether to introduce a Redis daemon or persistent agent required reading `docs/architecture/RUNTIME_COORDINATION_PATTERNS.md`, checking `evidence/stage2/RUN-10_REPORT.json` for Munder Difflin failure context, inspecting `evidence/stage2/RUN-11_REPORT.json` for mailbox schemas, and checking `docs/OPINIONATED_WORKSPACE_POLICY.md` for architectural invariants (382 lines total).
- **Memory Prototype Observation:** In Mode B, the query returned `MEM-MPE-003` (file-based coordination approved) and `MEM-MPE-004` (explicit prohibition: NO daemons, background schedulers, persistent agents, or shared databases). The agent immediately avoided repeating the unviable daemon route in 26 context lines.

### Task 3: TASK-MPE-12 (CLEARS Triage Engine Operational Reliance)
- **Baseline Observation:** In Mode A, an agent checking whether `deep_change_probability` can gate production routes had to inspect `docs/experiments/EXP-12_CLEARS_TRIAGE.md`, `evidence/stage2/RUN-12_REPORT.json`, and `scripts/triage_engine.py` (564 lines total). A partial read posed the significant risk of observing the "20/20 backtest pass" and incorrectly assuming production readiness.
- **Memory Prototype Observation:** In Mode B, `MEM-MPE-005` and `MEM-MPE-006` explicitly conveyed that the 20/20 backtest was retrospective only, that `deep_change_probability` is a heuristic score, and that prospective pre-registration is required before operational reliance. Bounded memory prevented a potential production misrouting error.

### Task 4: TASK-MPE-18 (Pirate Face Model Resilience Distribution)
- **Baseline Observation:** In Mode A, determining whether Pirate Face could serve as an active model registry required reading `FINDINGS.md`, `METHOD.md`, and `EXPERIMENT_REGISTRY.json` (427 lines total).
- **Memory Prototype Observation:** In Mode B, `MEM-MPE-007` and `MEM-MPE-008` immediately established that Pirate Face is an optional last-resort fallback retrieval path only, requiring byte-for-byte SHA-256 verification, and that production routing, registries, and seeding clusters are strictly forbidden.

---

## 4. Human Value Delivery Analysis

As defined in `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`:
> *"Resume without rediscovery whenever the necessary context/evidence was already captured."*  
> *"Human involvement should be rewarded with visible relief."*

The memory layer delivers tangible, measured relief:
1. **Zero Context Tax on Resumption:** A new AI session does not burn operator patience, tool quota, or context window re-reading foundational decisions that were settled in prior checkpoints.
2. **Reduced Cognitive Load:** The human operator is spared from repeatedly intervening to warn agents about settled constraints (e.g. "remember, no daemons in this project").
3. **Auditability without Authority Inversion:** Because memory writes require explicit approval and every item cites its source file, the human retains total authority over canonical knowledge.

---

## 5. Verification Against PASS Criteria

As specified in `docs/experiments/EXP-15_MPE_PROJECT_MEMORY_LAYER.md`, terminal `PASS` requires:

1. **All 6 acceptance tests PASS:**  
   `RECALL`, `UPDATE`, `DELETE`, `ISOLATION`, `PROVENANCE`, `FAILURE` all passed deterministically (verified in `ACCEPTANCE_TESTS.md` and `evidence/01_acceptance_tests.log`).
2. **Provenance is present for every promoted memory item:**  
   Verified. 100% of canonical items cite valid file paths and line/gate references. Missing provenance fails closed.
3. **No cross-project memory leakage occurs:**  
   Verified. Measured leakage across MPE, Murat House, and Murat AI Orchestrator is exactly `0`. Cross-project mutation attempts are blocked with `ScopeViolationError`.
4. **No unauthorized canonical memory write occurs:**  
   Verified. Attempts to mutate memory without explicit approval failed closed with `UnauthorizedWriteError`.
5. **Continuity/rediscovery improved measurably:**  
   Verified. Document reads reduced by 100% (17 -> 0), context footprint reduced by 94.3% (1,838 -> 104 lines), steps reduced by 81.0% (21 -> 4 steps).
6. **Git/project artifacts remain the sole Source of Truth:**  
   Verified. Memory is an indexed projection. Corrupted or missing memory stores safely fall back to canonical repository files with zero hallucinations.

---

## 6. Terminal Disposition

```text
RESULT: PASS
```
The prototype successfully validates the hypothesis: a bounded, provenance-aware project memory layer reduces context rediscovery between AI sessions without introducing a second Source of Truth or requiring external production infrastructure.
