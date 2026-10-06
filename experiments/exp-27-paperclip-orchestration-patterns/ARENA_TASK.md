# Arena Task — EXP-27 Paperclip orchestration patterns

Decision: **REUSE_COMPONENT**

Repository: `Murkin1980/murat-project-engineer`

Paperclip is a donor/reference only.

Read:
1. `AGENTS.md`
2. mandatory governance
3. `experiments/exp-27-paperclip-orchestration-patterns/README.md`

## Goal

Run one bounded orchestration proof and determine whether these Paperclip-inspired patterns add value to existing MPE / `murat-ai-orchestrator`:

1. goal ancestry/context;
2. atomic task lease;
3. persistent resumable evidence;
4. hard budget/runaway guard;
5. existing MPE approval gate.

## Execute

### CP-01
Audit current `paperclipai/paperclip`; pin commit/tag + license. Map donor patterns against existing MPE/orchestrator mechanisms. Reject duplicates.

### CP-02
On one existing bounded MPE engineering task, pass:

`project → goal → experiment/checkpoint → task`

Verify the executor preserves and can state the parent goal.

### CP-03
Build the smallest deterministic task-lease proof:
- first owner succeeds;
- duplicate owner fails explicitly;
- terminal/release state is visible;
- no daemon/service/DB.

### CP-04
Persist the existing MPE handoff fields and prove a fresh executor/process can resume without reconstructing the chat.

### CP-05
Demonstrate:
- at least one hard retry/tool-call/wall-time style limit causing STOP/BLOCKED;
- an integration-sensitive boundary producing existing READY/WARNING/BLOCKED and requiring the current MPE approval path.

Do not merge/deploy anything as part of the experiment.

## Final output

Return:
- RESULT: PASS / PARTIAL / FAIL
- overall: ADOPT_WITH_CHANGES / DO_NOT_ADOPT
- per pattern:
  - ADOPT_IN_ORCHESTRATOR
  - ADOPT_IN_MPE
  - REUSE_PATTERN_ONLY
  - REJECT
- measurements
- files changed
- checks run
- limitations/blockers

No new repo, Paperclip service, DB, queue, daemon, Router change, governance replacement, source-of-truth change, autonomous execution, or production integration.

STOP after CP-05.
