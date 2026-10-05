# Research → Execute → Review Playbook Pattern

**Status:** ACTIVE / PLAYBOOK SPECIFICATION  
**Date:** 2026-10-05  
**Scope:** MPE substantial implementation tasks (`VERIFIED` risk tier).

## Purpose

This document specifies the standard six-stage execution pattern for substantial implementation work across Murat Project Engineer. It governs how research, planning, execution, deterministic verification, and independent semantic review coordinate to eliminate unsubstantiated agent claims and scope drift.

---

## The Six Canonical Stages

```text
[1. Research] → [2. Task Packet] → [3. Execute Minimal] → [4. Deterministic Gates] → [5. Independent Review] → [6. Terminal Report]
```

### 1. Research Source-of-Truth and Constraints
- **Role:** Researcher or Architect.
- **Action:** Read governing project context files (`AGENTS.md`, `FOUNDATION.md`, `DESIGN.md`, `STATUS.md`).
- **Input:** Task statement, active project context, repository path.
- **Output:** Sourced facts, verified dependencies, identified constraints, resolved Opinionated Workspace defaults.
- **Constraint:** Research must use authoritative local or verified primary sources; never guess or assume unverified constraints.

### 2. Produce Bounded Implementation Plan / Task Packet
- **Role:** Architect.
- **Action:** Produce a bounded contract or Task Packet defining scope.
- **Output:** Objective, affected components, explicit non-goals ("do not build"), acceptance criteria, likely files, test strategy, rollback procedure, and deep-change assessment.
- **Handoff:** Typed Handoff via `contracts/HANDOFF.md` from Architect to Coder.

### 3. Execute the Smallest Sufficient Change
- **Role:** Coder.
- **Action:** Implement strictly the minimal diff necessary to meet acceptance criteria.
- **Output:** Changed files, tests added/modified, deviations reported, unresolved risks documented.
- **Constraint:** No speculative refactoring, no premature abstractions, no scope expansion without explicit re-planning.

### 4. Run Deterministic Checks
- **Role:** Coordinator / Deterministic Harness.
- **Action:** Run applicable hard deterministic gates (`build`, `typecheck`, `lint`, `unit_tests`, `integration_tests`, `secrets_scan`, `clean_diff_scope`, `rollback_available`).
- **Output:** Verifiable tool traces, terminal command exit codes, execution counts.
- **Fail-Closed:** Any failure halts execution or triggers at most one bounded rework cycle.

### 5. Perform Independent Semantic Review
- **Role:** Reviewer (strictly independent invocation; must not have written or edited the candidate code).
- **Action:** Evaluate the candidate diff and execution artifacts against acceptance criteria.
- **Foundational Rule:** **Agent claims are not evidence.**
  - The reviewer must independently examine command exit codes, test outputs, and diffs.
  - Assertions such as "tests pass" or "deployment succeeded" without captured evidence are marked `UNKNOWN/UNVERIFIED`.
- **Output:** Reviewer Verdict (`PASS`, `REWORK`, `INCONCLUSIVE`, `HUMAN_REQUIRED`), critical findings, noncritical findings, confidence.

### 6. Emit One Terminal State and Run Report
- **Role:** Coordinator.
- **Action:** Record the execution evidence, gate results, tool invocations, and final outcome in `contracts/RUN_REPORT.md`.
- **Terminal States:** Exactly one of `PASS`, `REWORK`, `BLOCKED`, or `HUMAN_REQUIRED`.

---

## Fail-Closed and Rework Invariants

- **Maximum Rework Cycles:** At most one rework cycle is permitted for `VERIFIED` tasks. If defects persist after one rework cycle, the outcome defaults to `REWORK` or `HUMAN_REQUIRED`.
- **Deep-Change Detection:** If a deep change is detected at any stage, implementation immediately stops, emits `DEEP_CHANGE_REQUIRES_USER_APPROVAL`, and returns `HUMAN_REQUIRED`.
- **No Self-Review:** An agent or expert that authored a change must never act as its independent reviewer.
