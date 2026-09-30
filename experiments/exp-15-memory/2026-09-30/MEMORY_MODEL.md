# EXP-15 — Bounded Memory Layer Specification & Data Model

**Experiment:** EXP-15 (MPE Project Memory Layer)  
**Run Date:** 2026-09-30 (UTC)  
**Project:** Murkin1980/murat-project-engineer  
**New Idea Filter Disposition:** `EXTEND_EXISTING`  

---

## 1. Architectural Foundation & Single Source of Truth

The MPE Project Memory Layer is designed under strict adherence to `AGENTS.md` and `docs/governance/SCOPE-CHANGE-CONTROL.md`:

1. **Git is the Sole Source of Truth:**
   The memory layer is an **indexed, provenance-aware projection** of previously verified project artifacts. It is **not** an independent authority. It does not replace, override, or compete with Git commits, repository documentation, run reports, or contracts.
2. **Local-First & Bounded:**
   The memory layer requires **no external daemon, background scheduler, or cloud service**. It operates as a local-first, file-backed data store (inspired by the MemoryOS and MemoryWiki patterns).
3. **Fail-Closed Provenance:**
   Every fact stored in or returned by memory must trace directly to a verifiable project artifact. If an item lacks provenance, any write operation **fails closed**.
4. **Approval-Gated Mutation:**
   Coding agents can only **propose** a Memory Delta. Autonomous promotion is strictly prohibited. Canonical memory is updated only when an explicit human or gate approval is supplied.
5. **Safe Fallback Invariant:**
   If the memory layer is missing, damaged, or unreadable, the system falls back safely to reading canonical repository files directly. It **never fabricates or hallucinates** memory.

---

## 2. Allowed Memory Vocabulary (Strict Categories)

To prevent memory bloat, chat transcript dumping, or conversational leakage, memory items are strictly restricted to **five allowed categories**:

| Category | Definition | Allowed Content | Prohibited Content |
| :--- | :--- | :--- | :--- |
| `decision` | Approved architectural, governance, or portfolio choices | Filter dispositions (`EXTEND_EXISTING`, `REUSE_COMPONENT`), architectural locks | Raw conversational turns, unapproved proposals |
| `outcome` | Verified empirical results from runs or experiments | Gate verdicts, pass/hold classifications, benchmark results | Subjective impressions, unverified claims |
| `constraint` | Mandatory negative and positive boundaries | Safety limits, banned patterns (no daemons, public web only), security rules | Temporary preferences, arbitrary instructions |
| `lesson` | Verified technical or operational discoveries | OS-specific quirks (e.g. Windows junction behavior, Cyrillic path issues) | Speculative commentary, general AI advice |
| `failed_attempt` | Documented dead-ends or unviable implementation paths | Tool failures, incompatible adapters, non-reproducible runs | Blame assignments, unverified bug reports |

Any item submitted with a category outside this vocabulary is rejected with `InvalidCategoryError`.

---

## 3. Data Schema

### 3.1 MemoryItem Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MemoryItem",
  "type": "object",
  "required": ["item_id", "project", "category", "topic", "summary", "provenance", "status"],
  "properties": {
    "item_id": {
      "type": "string",
      "pattern": "^MEM-[A-Z0-9_-]+$",
      "description": "Unique identifier for the memory record"
    },
    "project": {
      "type": "string",
      "description": "Owning repository or project scope identifier (e.g. Murkin1980/murat-project-engineer)"
    },
    "category": {
      "type": "string",
      "enum": ["decision", "outcome", "constraint", "lesson", "failed_attempt"]
    },
    "topic": {
      "type": "string",
      "description": "Concise search/matching slug (e.g. 'browseract scraping policy')"
    },
    "summary": {
      "type": "string",
      "description": "Clear, factual, non-conversational statement of the item"
    },
    "provenance": {
      "type": "string",
      "minLength": 3,
      "description": "Mandatory reference to canonical source artifact (file path, line number, run ID, commit SHA)"
    },
    "rationale": {
      "type": "string",
      "description": "Optional brief context explaining why this decision/constraint exists"
    },
    "status": {
      "type": "string",
      "enum": ["active", "superseded", "tombstone"],
      "default": "active"
    },
    "superseded_by": {
      "type": ["string", "null"],
      "description": "Reference to the newer MemoryItem that replaced this record"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "approved_by": {
      "type": ["string", "null"],
      "description": "Gate or human authority that approved canonical promotion"
    }
  }
}
```

---

## 4. Proposed Memory Delta Contract

At the conclusion of a task, an agent must **not** modify canonical memory directly. Instead, the agent proposes a **Memory Delta**:

```text
[Agent Execution Complete]
           │
           ▼
[Construct ProposedMemoryDelta]
  ├── task_id: "TASK-MPE-15"
  ├── actions:
  │     ├── NO_CHANGE
  │     ├── ADD (item + mandatory provenance)
  │     ├── UPDATE (target_item_id + item + mandatory provenance)
  │     ├── SUPERSEDE (target_item_id + new item + mandatory provenance)
  │     └── DELETE (target_item_id + reason)
  └── approval_status: "PENDING_APPROVAL"
           │
           ▼ (Approval Gate: must be explicitly approved by human/gate)
[apply_approved_delta()] ──► [Canonical Memory Store Persisted]
```

### 4.1 Allowed Delta Actions
1. **`NO_CHANGE`:** Explicit declaration that execution did not generate new architectural facts or alter existing constraints.
2. **`ADD`:** Proposal to register a new verified fact with mandatory provenance.
3. **`UPDATE`:** Proposal to clarify or amend an existing active fact.
4. **`SUPERSEDE`:** Proposal to retire an older fact in favor of a newer approved fact (maintains audit lineage).
5. **`DELETE`:** Proposal to tombstone an invalid or obsolete fact (excludes it from active recall).

### 4.2 Fail-Closed Invariants
- If `action` is `ADD`, `UPDATE`, or `SUPERSEDE` and `item.provenance` is empty or missing: **REJECT with `ProvenanceMissingError`**.
- If `apply_approved_delta()` is called without an `ApprovalGate(decision="APPROVED")`: **REJECT with `UnauthorizedWriteError`**.
- If an action references an item in a different `project`: **REJECT with `ScopeViolationError`**.

---

## 5. Scope Isolation Invariant

Multi-project repositories and cross-project portfolios (e.g. `Murat Project Engineer`, `Murat House`, `Murat AI Orchestrator`) must never contaminate each other's memory contexts:

1. Every item possesses a mandatory `project` attribute.
2. Retrieval queries require an explicit `project` argument; items belonging to different projects are filtered out at query time.
3. Mutation operations verify that the delta's project matches the target item's project; cross-project modification attempts fail closed.

---

## 6. Safe Failure and Fallback Model

If the memory store file is missing, unreadable, or corrupted (e.g., malformed JSON syntax or hash mismatch):

1. `ProjectMemoryStore.load()` catches the error cleanly.
2. Store transitions to `load_status = "FALLBACK_CANONICAL"`.
3. An explicit warning is recorded: `"Corrupted or invalid memory store; safely falling back to canonical project artifacts."`
4. Active recall queries return an empty list (`[]`), **never** guessing or fabricating facts.
5. The calling agent proceeds using standard MPE exploratory file reads against canonical Git files (`docs/`, `evidence/`, `contracts/`).
