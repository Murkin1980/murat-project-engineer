# EXP-15 — Baseline Definition & Comparative Methodology

**Experiment:** EXP-15 (MPE Project Memory Layer)  
**Run Date:** 2026-09-30 (UTC)  
**Project:** Murkin1980/murat-project-engineer  

---

## 1. Context and Problem Statement

Under MPE governance (`AGENTS.md`, `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`), two fundamental operating invariants guide AI-assisted work:
1. *"Human involvement should be rewarded with visible relief."*
2. *"Resume without rediscovery whenever the necessary context/evidence was already captured."*

In practice, AI coding agents operate across distinct, bounded execution sessions. Between sessions, context is discarded. In the current MPE workflow, an agent starting a new task must reconstruct past architectural decisions, constraints, lessons, and failed attempts entirely through exploratory search across repository files, markdown specifications, run reports, and evidence trees.

This introduces measurable friction:
- **Rediscovery Tax:** 4 to 5 full document reads per task, requiring thousands of lines of context inspection.
- **Cognitive Load & Latency:** Repeated tool calls to locate historical rationales.
- **Drift Risk:** If an agent searches incompletely, it risks violating established constraints (e.g., attempting to install a background daemon, missing the requirement to clean up temporary browser instances, or treating experimental heuristics as calibrated production probabilities).

The goal of EXP-15 is to measure whether a compact, structured, provenance-aware **Project Memory Layer** eliminates this rediscovery tax without compromising Git as the sole Source of Truth.

---

## 2. Compared Operating Modes

```text
MODE A — CURRENT BASELINE:
[Task Packet] ───────────► [Repo / Docs / Evidence Scan] ──► [Agent Execution] ──► [PR / Evidence]
(No dedicated memory context; agent must rediscover prior decisions from scratch)

MODE B — MEMORY-LAYER PROTOTYPE:
[Project Memory]
       │ (bounded recall)
       ▼
[Task Packet] ───────────► [Enriched Bounded Context] ────► [Agent Execution] ──► [PR / Evidence]
                                                                                       │
                                                                                       ▼
                                                                             [Proposed Memory Delta]
                                                                                       │
                                                                                       ▼ (Approval Gate)
                                                                             [Project Memory Update]
```

### Mode A: Current Baseline Workflow
1. An incoming Task Packet defines the task objective.
2. The agent has no pre-injected memory of past decisions or failed attempts.
3. The agent must perform multiple search queries (`git grep`, directory listing, file reading) across `docs/`, `evidence/stage2/`, `STATUS.md`, and `contracts/`.
4. The agent infers constraints from scattered historical documents.
5. The agent implements the task and generates standard MPE evidence.
6. **No memory delta is produced; subsequent sessions must repeat the same discovery cycle.**

### Mode B: Memory-Layer Prototype Workflow
1. Before execution, the system performs a bounded recall query scoped to `project` and the task's `topic`.
2. The agent receives a compact packet containing only relevant, active facts:
   - `decision` (approved choices and architectural placements)
   - `outcome` (verified historical outcomes)
   - `constraint` (governing invariants and safety boundaries)
   - `lesson` (verified operational insights)
   - `failed_attempt` (known dead-ends to avoid repeating)
   - `provenance` (canonical file, commit SHA, or run report link)
3. The agent executes with full awareness of prior decisions and constraints in zero exploratory reads.
4. Post-execution, the agent proposes a bounded **Memory Delta**:
   - `ADD` (new verified fact)
   - `UPDATE` (clarify existing fact)
   - `SUPERSEDE` (replace fact with new approved fact)
   - `DELETE` (tombstone obsolete fact)
   - `NO_CHANGE` (no changes needed)
5. The proposed delta is **strictly approval-gated**. It never mutates canonical memory automatically.
6. If provenance is missing, write attempts **fail closed**.

---

## 3. Benchmark Tasks (Real MPE History)

To guarantee reproducible, non-synthetic evaluation, 4 real completed MPE development tasks with frozen artifacts in the repository were selected:

### Task 1: TASK-MPE-08 — BrowserAct Scraping and Automation Boundaries
- **Historical Basis:** `RUN-08` / `EXP-08` (BrowserAct public-web browser acquisition evaluation).
- **Core Dilemma:** Can BrowserAct be used for authenticated scraping and form submission across private client portals?
- **Canonical Decision:** `REUSE_COMPONENT` under New Idea Filter for public-web browser acquisition role only.
- **Canonical Constraints:** Strictly `PUBLIC_WEB_ONLY`: no authentication, no forms, no messaging, no purchase, no CAPTCHA bypass; isolated Chrome must be deleted after use.
- **Mode A Required Files (5 files, 465 lines):**
  1. `docs/NEW_IDEA_FILTER_POLICY.md` (55 lines)
  2. `docs/evaluations/BROWSERACT_EVALUATION.md` (126 lines)
  3. `docs/evaluations/BROWSER_ACQUISITION_ROLE.md` (30 lines)
  4. `evidence/stage2/RUN-08_REPORT.json` (117 lines)
  5. `STATUS.md` (137 lines)
- **Mode A Discovery Cost:** 6 steps (1 search + 5 file reads), 465 lines inspected.

### Task 2: TASK-MPE-11 — Runtime Coordination Messaging Architecture
- **Historical Basis:** `RUN-10` / `RUN-11` (Munder Difflin pilot and Runtime Coordination Patterns).
- **Core Dilemma:** Should MPE use a background Redis daemon or persistent process broker for multi-expert handoffs?
- **Canonical Decision:** Approved lightweight file-based coordination (typed mailbox envelopes, append-only JSONL events, ephemeral worktree metadata).
- **Canonical Constraints:** NO daemon, background scheduler, persistent agent, shared database, or Router authority change allowed. Atomic publication single-filesystem only; Windows junction rejection enforced.
- **Mode A Required Files (4 files, 382 lines):**
  1. `docs/architecture/RUNTIME_COORDINATION_PATTERNS.md` (35 lines)
  2. `evidence/stage2/RUN-10_REPORT.json` (37 lines)
  3. `evidence/stage2/RUN-11_REPORT.json` (202 lines)
  4. `docs/OPINIONATED_WORKSPACE_POLICY.md` (108 lines)
- **Mode A Discovery Cost:** 5 steps (1 search + 4 file reads), 382 lines inspected.

### Task 3: TASK-MPE-12 — CLEARS Triage Engine Operational Reliance
- **Historical Basis:** `RUN-12` / `EXP-12` (CLEARS deterministic triage engine backtest).
- **Core Dilemma:** Can `deep_change_probability` from CLEARS triage engine be used as an autonomous gate in production routing?
- **Canonical Decision:** Retrospective backtest passed (20/20 cases), but status remains `EXPERIMENT`.
- **Canonical Constraints:** `deep_change_probability` is a deterministic heuristic score, NOT a calibrated statistical probability; prospective pre-registered cases required before operational reliance.
- **Mode A Required Files (4 files, 564 lines):**
  1. `docs/experiments/EXP-12_CLEARS_TRIAGE.md` (176 lines)
  2. `evidence/stage2/RUN-12_REPORT.json` (50 lines)
  3. `scripts/triage_engine.py` (312 lines)
  4. `datasets/exp-12-backtest.json` (26 lines)
- **Mode A Discovery Cost:** 5 steps (1 search + 4 file reads), 564 lines inspected.

### Task 4: TASK-MPE-18 — Pirate Face Model Distribution Architecture
- **Historical Basis:** `EXP-18` (Pirate Face model resilience evaluation).
- **Core Dilemma:** Should Pirate Face be deployed as an active model registry and seeding cluster in production?
- **Canonical Decision:** EXP-18 PASS: verified byte-for-byte retrieval (29/29 files) of pinned `sentence-transformers/all-MiniLM-L6-v2` artifact under primary source loss.
- **Canonical Constraints:** Optional last-resort fallback path ONLY; mandatory SHA-256 manifest check; DO NOT add production routing, a registry, or seeding infrastructure.
- **Mode A Required Files (4 files, 427 lines):**
  1. `experiments/exp-18-pirateface-model-resilience/README.md` (100 lines)
  2. `experiments/exp-18-pirateface-model-resilience/FINDINGS.md` (230 lines)
  3. `experiments/exp-18-pirateface-model-resilience/METHOD.md` (70 lines)
  4. `experiments/EXPERIMENT_REGISTRY.json` (27 lines)
- **Mode A Discovery Cost:** 5 steps (1 search + 4 file reads), 427 lines inspected.

---

## 4. Evaluation Metrics

For each benchmark task, Mode A and Mode B are evaluated across 7 standardized criteria:

1. **Prior Decision Recalled:** Did the session correctly recall the prior approved decision? (`Yes` / `No`)
2. **Contradictory Guidance:** Did the session produce guidance violating documented project invariants? (`Yes` / `No`)
3. **Rediscovery Steps:** Number of exploratory tool calls / steps required to locate the context.
4. **Unnecessary Repo/Document Reads:** Count of exploratory file reads spent on rediscovering settled facts.
5. **Context Footprint:** Number of lines of context ingested to resolve the decision/constraint.
6. **Provenance Correctness:** Is the recalled fact backed by an explicit, verifiable canonical file reference?
7. **Unauthorized Writes:** Number of unapproved mutations to canonical project state (must be `0`).
