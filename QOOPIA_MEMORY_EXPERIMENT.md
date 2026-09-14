# QOOPIA MEMORY EXPERIMENT
## Cross-session retrievable memory for Murat Project Engineer

**Date:** 2026-09-14
**Primary governing repository:** `Murkin1980/murat-project-engineer`
**Primary decision:** `EXPERIMENT`
**New repository:** `NO`
**Deep change:** `NOT AUTHORIZED`
**Status:** `QUEUED / NOT STARTED`

---

# 0. EXECUTIVE DIRECTIVE

Evaluate Qoopia as an optional retrievable memory/cache layer for AI agents working with Murat Project Engineer.

The experiment must answer one practical question:

> Can a new AI session recover the correct project context with materially less manual handoff, without replacing MPE/GitHub as the source of truth?

Do NOT make Qoopia canonical storage.
Do NOT migrate governance, evidence, project status, task packets, or architectural decisions into Qoopia.
Do NOT create a new repository.
Do NOT enable production use during this experiment.

---

# 1. MURAT PROJECT ENGINEER NEW IDEA FILTER

```text
MURAT_PROJECT_ENGINEER_NEW_IDEA_FILTER

Idea:
Use Qoopia as a retrievable memory/cache layer shared across AI sessions and compatible agents.

Decision:
EXPERIMENT

Why:
- MPE already has the canonical project/governance layer; replacing it would duplicate infrastructure.
- The value hypothesis is narrow and measurable: reduce repeated context reconstruction after new sessions.
- The experiment can run inside the existing MPE workflow without a new repository.
- Existing project data and Task Packets remain authoritative.
- Failure is cheap and reversible.
- No deep architecture change is required for the first test.
```

---

# 2. ARCHITECTURAL BOUNDARY

```text
GitHub / MPE = SOURCE OF TRUTH
Qoopia = RETRIEVABLE MEMORY / CACHE ONLY
```

Qoopia may store temporary or derived context useful for retrieval, but canonical project state must remain in repository-controlled artifacts.

Qoopia must not become authoritative for:
- governance decisions;
- project status;
- evidence;
- accepted execution results;
- Task Packets;
- architecture decisions;
- security policy;
- release state.

---

# 3. MINIMUM EXPERIMENT

Use one non-sensitive test project, preferably `ai-microtask-factory`, and a synthetic context packet where needed.

Phase A — write context:
1. Start Session A.
2. Store 5–10 representative project facts in Qoopia.
3. Include current stage, accepted result, key constraints, blocker/next step, and one irrelevant decoy fact.
4. End Session A.

Phase B — cold recovery:
1. Start a fresh Session B with no copied conversation history.
2. Give only the project identifier and access to the Qoopia integration.
3. Ask the agent to reconstruct the working context.
4. Compare returned context against GitHub/MPE source-of-truth artifacts.

Phase C — isolation:
1. Add context for a second synthetic project.
2. Query only the first project.
3. Verify no unrelated facts leak into the answer.

---

# 4. PASS / FAIL CRITERIA

PASS requires all of the following:

- Context recovery accuracy >= 90% for the selected facts.
- No cross-project leakage in the isolation test.
- No canonical MPE/GitHub artifact is replaced by Qoopia.
- Fresh-session recovery requires materially less manual context transfer than the current workflow.
- Revoking or removing Qoopia does not break the canonical project workflow.

FAIL if any of the following occurs:

- stale memory is presented as authoritative current state;
- project isolation fails;
- secrets or sensitive operational data are required for useful operation;
- setup/maintenance cost outweighs the handoff reduction;
- MPE must be structurally redesigned around Qoopia;
- the integration creates a second source of truth.

---

# 5. SECURITY / DATA RULES

- Use synthetic or non-sensitive data for the first run.
- Do not store tokens, API keys, passwords, personal secrets, or production credentials.
- Preserve existing MPE secret-management rules.
- Prefer least-privilege/read-oriented access for experiment integrations.
- Any request for broader write access or deep-change requires explicit user approval before proceeding.

---

# 6. EVIDENCE TO CAPTURE

For each run record:

```yaml
experiment: qoopia-memory
session_a:
  facts_written:
  duration_or_steps:
session_b:
  facts_recovered:
  incorrect_facts:
  missing_facts:
  unrelated_facts:
accuracy_percent:
isolation_pass:
manual_handoff_reduction:
source_of_truth_preserved:
terminal_state: PASS | FAIL | HUMAN_REQUIRED
```

---

# 7. NEXT ACTION

Do not install or integrate Qoopia yet.

When this experiment reaches priority, first inspect current Qoopia source/docs and current MPE architecture, then prepare a disposable local/sandbox test plan. Any production connection, persistent deployment, or architectural promotion requires a new explicit decision after evidence is collected.
