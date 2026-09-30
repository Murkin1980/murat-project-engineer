# EXP-15 — Acceptance Tests Protocol & Results

**Experiment:** EXP-15 (MPE Project Memory Layer)  
**Run Date:** 2026-09-30 (UTC)  
**Test Suite:** `experiments/exp-15-memory/2026-09-30/harness/run_acceptance_tests.py`  
**Execution Environment:** Sandbox Linux Python 3.11.2 (Standard Library Only)  

---

## 1. Acceptance Criteria Overview

As mandated by `docs/experiments/EXP-15_MPE_PROJECT_MEMORY_LAYER.md`, the memory prototype cannot be accepted without passing all six acceptance tests:

| Test ID | Name | Objective | Result |
| :--- | :--- | :--- | :--- |
| **TEST-01** | `RECALL` | Correctly recalls existing decision/constraint for a task | **PASS** |
| **TEST-02** | `UPDATE` | Newer approved fact correctly supersedes old fact | **PASS** |
| **TEST-03** | `DELETE` | Approved deletion excludes old fact from active recall | **PASS** |
| **TEST-04** | `ISOLATION` | Data from different project scopes never mix | **PASS** |
| **TEST-05** | `PROVENANCE` | Every fact cites source; missing provenance fails closed | **PASS** |
| **TEST-06** | `FAILURE` | Unavailability/corruption safely falls back to Git | **PASS** |

**Summary: 6 / 6 Acceptance Tests PASSED.**

---

## 2. Detailed Test Protocols and Verification Logs

### TEST-01: RECALL — Accurate Decision and Constraint Retrieval
- **Goal:** Verify that querying memory returns existing active decisions and constraints without omission or distortion.
- **Protocol:**
  1. Load canonical memory store (`fixtures/canonical_memory.json`).
  2. Query for topic `"browseract"`.
  3. Query for topic `"runtime coordination"`.
  4. Assert all returned records are in `active` status and match expected historical decisions.
- **Observed Results:**
  - Query `"browseract"` returned:
    - `MEM-MPE-001` (Category: `decision`, Summary: `"BrowserAct approved under New Idea Filter as REUSE_COMPONENT for public-web browser acquisition role only."`, Provenance: `"docs/evaluations/BROWSERACT_EVALUATION.md#L45, evidence/stage2/RUN-08_REPORT.json#L24"`)
    - `MEM-MPE-002` (Category: `constraint`, Summary: `"Strictly PUBLIC_WEB_ONLY: no authentication, no forms, no messaging, no purchase, no CAPTCHA bypass; isolated Chrome must be deleted after use."`, Provenance: `"evidence/stage2/RUN-08_REPORT.json#L29, docs/evaluations/BROWSER_ACQUISITION_ROLE.md#L15"`)
  - Query `"runtime coordination"` returned:
    - `MEM-MPE-003` (Category: `decision`, Lightweight file-based coordination approved)
    - `MEM-MPE-004` (Category: `constraint`, No daemons, background schedulers, or persistent agents)
- **Verdict:** **PASS**

---

### TEST-02: UPDATE — Approved Superseding and Lineage Preservation
- **Goal:** Verify that an approved update supersedes an existing fact, updates the active recall set, and maintains an auditable lineage pointer.
- **Protocol:**
  1. Create initial active item `MEM-EXP15-STATUS-001` (`"EXP-15 status is PLANNED and queued."`).
  2. Propose delta with action `SUPERSEDE` pointing to `MEM-EXP15-STATUS-001` with new item `MEM-EXP15-STATUS-002` (`"EXP-15 MVP executed with PASS outcome; all 6 acceptance tests passed."`).
  3. Attempt execution without approval / with rejected approval: assert `UnauthorizedWriteError` raised (fail-closed test).
  4. Apply delta with `ApprovalGate(decision="APPROVED", approver="lead-maintainer")`.
  5. Query active items for `"exp-15 status"`: assert ONLY `MEM-EXP15-STATUS-002` is returned.
  6. Query with `include_superseded=True`: assert `MEM-EXP15-STATUS-001` has `status="superseded"` and `superseded_by="MEM-EXP15-STATUS-002"`.
- **Observed Results:**
  - Unauthorized mutation was rejected immediately.
  - Approved superseding correctly updated active index.
  - Old record preserved as superseded with successor reference.
- **Verdict:** **PASS**

---

### TEST-03: DELETE — Approved Tombstoning and Recall Exclusion
- **Goal:** Verify that an approved deletion removes the item from future recall while preserving auditability.
- **Protocol:**
  1. Register active item `MEM-TEMP-001` (`"This is a temporary fact to be deleted."`).
  2. Propose delta with action `DELETE` targeting `MEM-TEMP-001`.
  3. Attempt unapproved deletion: assert `UnauthorizedWriteError` raised.
  4. Apply deletion with valid approval.
  5. Query active items for topic: assert item count is `0`.
  6. Inspect raw store: assert record remains with `status="tombstone"`.
- **Observed Results:**
  - Unauthorized deletion blocked.
  - Approved deletion tombstoned the item.
  - Subsequent active queries returned empty list (`0` items).
- **Verdict:** **PASS**

---

### TEST-04: ISOLATION — Multi-Project Scope Separation
- **Goal:** Verify that facts belonging to different repositories/projects never leak into each other's query responses or mutation paths.
- **Protocol:**
  1. Load multi-project fixture `cross_project_memory.json` containing items for:
     - `Murkin1980/murat-project-engineer` (`MEM-MPE-001`)
     - `Murkin1980/Murat-house` (`MEM-MH-001`, `MEM-MH-002`)
     - `Murkin1980/Murat-AI-Orchestrator` (`MEM-MAO-001`, `MEM-MAO-002`)
  2. Execute query scoped to `Murkin1980/murat-project-engineer`: verify 0 items from other projects are returned.
  3. Execute query scoped to `Murkin1980/Murat-house`: verify 0 items from MPE or Orchestrator are returned.
  4. Execute query scoped to `Murkin1980/Murat-AI-Orchestrator`: verify 0 items from other projects are returned.
  5. Propose cross-project mutation (an MPE delta attempting to mutate `MEM-MH-001`): assert rejected with `ScopeViolationError`.
- **Observed Results:**
  - Cross-project leakage count: **EXACTLY 0**.
  - Cross-project mutation attempt: **BLOCKED**.
- **Verdict:** **PASS**

---

### TEST-05: PROVENANCE — Source Validation and Fail-Closed Write Gating
- **Goal:** Verify that every recalled memory fact has verifiable source evidence, and that writes without provenance fail closed.
- **Protocol:**
  1. Inspect all items in canonical memory.
  2. Extract primary file path from `item.provenance` and verify that the file exists in the repository.
  3. Attempt to instantiate or validate items with missing, empty, or whitespace provenance (`""`, `"   "`, `None`).
  4. Assert `ProvenanceMissingError` is raised in all missing provenance cases.
- **Observed Results:**
  - 100% (8/8) canonical memory items cite real, existing files in the repository (`docs/evaluations/BROWSERACT_EVALUATION.md`, `evidence/stage2/RUN-08_REPORT.json`, `docs/architecture/RUNTIME_COORDINATION_PATTERNS.md`, `evidence/stage2/RUN-11_REPORT.json`, `evidence/stage2/RUN-12_REPORT.json`, `docs/experiments/EXP-12_CLEARS_TRIAGE.md`, `experiments/exp-18-pirateface-model-resilience/FINDINGS.md`).
  - All write attempts lacking provenance failed closed.
- **Verdict:** **PASS**

---

### TEST-06: FAILURE — Resilient Fallback to Canonical Git Artifacts
- **Goal:** Verify that when the memory layer is unavailable or corrupted, the system falls back safely to reading canonical repository files without crashing or inventing facts.
- **Protocol:**
  1. Attempt to load a store with a non-existent path. Assert `load_status == "FALLBACK_CANONICAL"` and active recall returns `[]` (zero hallucinations).
  2. Attempt to load a store with corrupted JSON syntax (`"INVALID_JSON{broken:true"`). Assert `load_status == "FALLBACK_CANONICAL"`, warning is recorded, and active recall returns `[]`.
  3. Verify agent fallback: assert that canonical project artifacts (`docs/evaluations/BROWSERACT_EVALUATION.md`) exist and provide the authoritative truth.
- **Observed Results:**
  - Non-existent and malformed stores handled gracefully.
  - Zero fabricated items returned.
  - Safe fallback to Git source of truth confirmed.
- **Verdict:** **PASS**

---

## 3. Execution Log Transcript

```text
======================================================================
EXP-15 Acceptance Test Suite — Controlled MVP Execution
======================================================================
[PASS] RECALL: Correctly recalled active decisions, constraints, and outcomes across queries without omission.
[PASS] UPDATE: New approved fact supersedes old fact; old marked superseded; recall returns exclusively the new active fact.
[PASS] DELETE: Approved deletion tombstones item; item completely excluded from subsequent active recall queries.
[PASS] ISOLATION: Strict scope enforcement on recall and mutation; zero cross-project leakage observed.
[PASS] PROVENANCE: 100% of recalled facts point to existing repo artifacts; writes without provenance fail closed.
[PASS] FAILURE: Missing and corrupted stores trigger FALLBACK_CANONICAL safely; zero hallucinations; canonical Git fallback verified.
======================================================================
FINAL OUTCOME: PASS (6/6 tests passed)
======================================================================
```
