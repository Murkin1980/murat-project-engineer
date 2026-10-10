# Lightweight Git-Native Knowledge Model

**Status:** ACTIVE / SPECIFICATION  
**Date:** 2026-10-05  
**Scope:** Minimal Git-native knowledge representation for Murat Project Engineer.

## Purpose

This document defines a minimal, Git-native information model for five core knowledge entities:
1. **Ideas**
2. **Decisions**
3. **Experiments**
4. **Knowledge**
5. **Skills**

This is a documentation and contract model preparing for bounded experiments (e.g., EXP-15). It does **NOT** implement or introduce a database, daemon, scheduler, vector DB, knowledge graph, memory service, or external synchronization system (such as Notion). All artifacts reside as plain text (Markdown, JSON, YAML) directly within the Git repository.

---

## Entity Specifications

```text
       ┌──────────┐
       │   Idea   │ (Intake & New Idea Filter)
       └────┬─────┘
            │
            ├───────────────┬──────────────┐
            ▼               ▼              ▼
     [EXTEND/REUSE]   [EXPERIMENT]     [HOLD/REJECT]
            │               │              │
            │               ▼              ▼
            │        ┌──────────────┐ (Archive)
            │        │  Experiment  │
            │        └──────┬───────┘
            │               │
            ▼               ▼
     ┌──────────────┐◄──────┘
     │   Decision   │ (ADR / Policy Lock)
     └──────┬───────┘
            │
            ├──────────────────────────────┐
            ▼                              ▼
     ┌──────────────┐               ┌──────────────┐
     │  Knowledge   │ (Docs/Context)│    Skill     │ (Executable Procedure)
     └──────────────┘               └──────────────┘
```

---

### 1. Ideas
- **Definition:** Unvetted proposals, feature requests, product expansions, or architectural ideas.
- **Repository Location:**
  - Task Packets: `docs/tasks/TP-*.md`
  - Filter Evaluations: governed by `contracts/NEW_IDEA_FILTER.md` and `contracts/NEW_IDEA_FILTER.schema.json`.
- **Lifecycle States:**
  `SUBMITTED` → `EVALUATING` → (one of 7 terminal decisions: `EXTEND_EXISTING`, `REUSE_COMPONENT`, `MERGE`, `EXPERIMENT`, `HOLD`, `NEW_REPOSITORY`, `REJECT`).
- **Storage Format:** Versioned Markdown Task Packet or structured evaluation JSON.
- **Governance:** Evaluated strictly against the nine checks of `docs/NEW_IDEA_FILTER_POLICY.md`. Fails closed on deep-change or anti-roadmap conflicts. Never contains private personal data.

### 2. Decisions
- **Definition:** Authoritative Architecture Decision Records (ADRs), scope locks, tool adoption dispositions, or portfolio policies.
- **Repository Location:**
  - Architecture decisions: `docs/architecture/`
  - Tool/stack evaluations: `docs/evaluations/`
  - Portfolio/governance locks: `docs/governance/` and root `*_DECISION.md`.
- **Lifecycle States:**
  `PROPOSED` → `UNDER_REVIEW` → `ADOPTED` | `REJECTED` | `SUPERSEDED`.
- **Storage Format:** Markdown document containing:
  - Context and problem statement;
  - Options evaluated with trade-offs;
  - Decision outcome and rationale;
  - Deep-change impact assessment;
  - Explicit rollback plan.
- **Governance:** Decisions are immutable once committed. Modifying a settled architectural decision requires an explicit superseding decision document referencing the previous decision and SHA.

### 3. Experiments
- **Definition:** Bounded, empirical evaluations designed to test concrete hypotheses (e.g. model routing, prompt techniques, tool integrations) with verifiable evidence.
- **Repository Location:**
  - Canonical Registry: `experiments/EXPERIMENT_REGISTRY.json`
  - Experiment folders: `experiments/<experiment-id>/`
  - Captured evidence: `evidence/`
- **Lifecycle States:**
  `IDEA` → `PLANNED` → `READY_TO_TEST` → `RUNNING` → `PASS` | `FAIL` | `HOLD` | `ADOPTED`.
- **Storage Format:**
  - `README.md`: Hypothesis, method, acceptance criteria, and findings.
  - `PRE_REGISTRATION.json`: Pre-execution boundary and criteria lock.
  - `EXECUTION_RECORD.json`: Captured runtime telemetry adhering to `contracts/EXPERIMENT_RECORD.schema.json`.
- **Governance:** Pre-registration is mandatory prior to execution. Claims require verifiable tool traces; unverified assertions fail closed.

### 4. Knowledge
- **Definition:** Curated domain rules, architectural standards, progressive context manifests, operational procedures, and validated lessons.
- **Repository Location:**
  - System architecture: `docs/architecture/`
  - Context manifests: `context/project-context.md`, `context/CONTEXT_MAP.md`
  - Operating models: `docs/OPERATING_MODEL.md`, `docs/GLOBAL_MPE_ENFORCEMENT.md`
  - Lessons candidate queue: `LESSONS_CANDIDATE.md` (when present in target projects).
- **Lifecycle States:**
  `OBSERVATION` (session-ephemeral) → `CANDIDATE` → `VERIFIED_EVIDENCE` → `CURATED_KNOWLEDGE`.
- **Storage Format:** Plain-text Markdown organized by progressive disclosure priority (Priority 1 to 8 in `context/project-context.md`).
- **Governance:**
  - **No Auto-Promotion:** Session logs, chat history, and model reasoning are ephemeral and must never be auto-promoted into permanent repository knowledge.
  - **Write-Gated:** Only reviewed, evidence-backed findings may be committed to permanent knowledge docs.
  - **Git-Native:** Git is the single source of truth; no external synchronization (e.g. Notion, Confluence).

### 5. Skills
- **Definition:** Reusable, executable capability definitions, operational procedures, and domain tool-use instructions for bounded agents.
- **Repository Location:**
  - Skill directories: `skills/<skill-name>/`
  - Entry point: `skills/<skill-name>/SKILL.md`
  - Supporting references: `skills/<skill-name>/references/`
- **Lifecycle States:**
  `DRAFT` → `TESTED_IN_HARNESS` → `ACTIVE` | `RETIRED`.
- **Storage Format:** `SKILL.md` with YAML frontmatter:
  - `name`: unique skill slug.
  - `description`: concise invocation summary and applicability trigger.
  - Markdown body: operational instructions, input contracts, reference mappings, and error handling.
- **Governance:**
  - Skills are bounded procedural guides, not autonomous daemons or persistent agents.
  - Skills must adhere to MPE non-negotiable rules and cannot bypass Review Gates or router boundaries.

---

## Architectural Invariants

1. **Git Repository is the Single Source of Truth:** No external database, vector store, or SaaS knowledge base is permitted to hold authoritative state.
2. **Minimal Sufficient Artifacts:** Use simple Markdown, JSON, and YAML. Do not construct multi-tier metadata schemas when plain documents suffice.
3. **Traceability and Provenance:** Every promoted piece of knowledge or decision must reference its origin (e.g., Task Packet ID, Experiment ID, or Git commit hash).
4. **No Premature Automation:** Retrieval occurs via Git-native paths and progressive disclosure, not autonomous vector search or background indexing agents.
