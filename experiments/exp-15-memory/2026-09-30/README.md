# EXP-15 — Bounded Provenance-Aware Project Memory Layer

**Experiment ID:** EXP-15  
**Owning project:** Murkin1980/murat-project-engineer  
**New Idea Filter Decision:** `EXTEND_EXISTING`  
**Run Date:** 2026-09-30 (UTC)  
**Status:** PASS  
**Execution Type:** Controlled MVP Experiment (Baseline Mode A vs Memory Layer Mode B)  

---

## 1. Executive Summary

EXP-15 evaluates whether a compact, structured, provenance-aware project memory layer reduces repeated context rediscovery between AI coding sessions without introducing a second Source of Truth or requiring a persistent production service.

The experiment was conducted on a frozen benchmark of **4 real completed MPE development tasks** with existing canonical artifacts and evidence (`RUN-08`, `RUN-11`, `RUN-12`, `EXP-18`), comparing:
- **Mode A (Current Baseline):** Task Packet + manual repository/docs/evidence search without memory context.
- **Mode B (Memory-Layer Prototype):** Bounded Project Memory → Task Packet → Agent → PR/Evidence → proposed Memory Delta.

All **6 mandatory acceptance tests** (`RECALL`, `UPDATE`, `DELETE`, `ISOLATION`, `PROVENANCE`, `FAILURE`) were executed deterministically and **PASSED**.

### Key Measured Outcomes
- **Unnecessary Repo/Document Reads:** Reduced from **17 reads to 0 reads (100% reduction)**.
- **Context Footprint:** Reduced from **1,838 lines to 104 lines (94.3% reduction)** for decision and constraint recovery.
- **Rediscovery Steps:** Reduced from **21 steps to 4 lookup steps (81.0% reduction)**.
- **Prior Decision Recall:** **100%** correct across all benchmark tasks.
- **Contradictory Guidance:** **0%** observed.
- **Provenance Correctness:** **100%** of recalled facts link to verified canonical files.
- **Unauthorized Canonical Writes:** **0** (fail-closed approval gate strictly enforced).
- **Cross-Project Memory Leakage:** **0** (scope isolation strictly enforced across `Murat Project Engineer`, `Murat House`, and `Murat AI Orchestrator`).
- **Source of Truth:** Git and canonical project files remain the **sole authority**. When memory is unavailable or corrupted, the system falls back safely to canonical Git artifacts with zero hallucinations.

**Terminal Outcome:** `PASS`

---

## 2. Guardrails Ledger

| Guardrail Constraint | Mandate | Observed Status | Evidence |
| :--- | :--- | :--- | :--- |
| **No New Repository** | EXP-15 must live within `murat-project-engineer` | **MET** | Implemented under `experiments/exp-15-memory/2026-09-30/` |
| **No Production Memory Service** | No daemons, background schedulers, VectorDBs, or external services | **MET** | Zero-dependency, file-backed local prototype (`memory_layer.py`) |
| **No MPE Governance Changes** | MPE constitutional rules and policies remain unchanged | **MET** | Read-only compliance with `AGENTS.md`, `SCOPE-CHANGE-CONTROL.md` |
| **Git as Sole Source of Truth** | Memory must not become an independent authority | **MET** | Memory is an indexed projection; failure falls back safely to canonical Git files |
| **Mandatory Provenance** | Every memory item must cite canonical source/evidence | **MET** | 100% items cite valid repo paths; missing provenance fails closed |
| **Approval-Gated Writes** | No autonomous memory promotion | **MET** | Proposed deltas default to `PENDING_APPROVAL`; unauthorized writes fail closed |
| **Scope Isolation** | No cross-project memory contamination | **MET** | Verified 0 leakage across MPE, Murat House, and Murat AI Orchestrator |
| **Safe Terminal State** | Graceful handoff; no half-written or corrupted state | **MET** | Handoff and evaluation summary deterministically recorded |
| **Only Experiment Evidence** | No production code or routing changed | **MET** | Changes strictly confined to `experiments/exp-15-memory/2026-09-30/` |

---

## 3. Directory Index

```text
experiments/exp-15-memory/2026-09-30/
├── README.md                      # This executive summary and guardrail ledger
├── BASELINE.md                    # Baseline definition, benchmark tasks, and Mode A execution trace
├── MEMORY_MODEL.md                # Formal bounded memory schema, delta lifecycle, and failure contract
├── ACCEPTANCE_TESTS.md            # Detailed protocol and results for all 6 acceptance tests
├── RESULTS.md                     # Quantitative metrics, A vs B comparison tables, and terminal justification
├── HASHES.txt                     # SHA-256 hashes of frozen inputs, fixtures, and generated artifacts
├── harness/
│   ├── memory_layer.py            # Bounded, zero-dependency, local-first memory store and validator
│   ├── run_acceptance_tests.py    # Deterministic test runner for RECALL, UPDATE, DELETE, ISOLATION, PROVENANCE, FAILURE
│   └── run_baseline_comparison.py # Comparative evaluator measuring Mode A vs Mode B metrics
├── fixtures/
│   ├── canonical_memory.json      # Initial frozen project memory store derived from MPE history
│   ├── cross_project_memory.json  # Multi-project fixture for isolation testing
│   └── benchmark_tasks.json       # Frozen benchmark tasks with queries, required files, and canonical facts
└── evidence/
    ├── 01_acceptance_tests.log    # Raw console log of acceptance tests execution
    ├── 01_acceptance_tests.json   # Machine-readable acceptance tests report
    ├── 02_baseline_comparison.log # Raw console log of Mode A vs Mode B comparison
    └── 02_baseline_comparison.json# Machine-readable comparative metrics
```

---

## 4. Terminal Disposition & Recommendation

- **Disposition:** `PASS`
- **Architectural Finding:** A lightweight, local-first, file-backed project memory layer (inspired by MemoryOS/MemoryWiki patterns) measurably eliminates the rediscovery tax between AI sessions while strictly respecting MPE's single-source-of-truth invariant.
- **Next Step:** Keep EXP-15 as a validated experiment evidence record. When MPE task runners are next extended, reuse the bounded memory contract as an optional pre-execution context injection step without altering production routing or adding background infrastructure.
