# ARENA_CONTEXT — derived launch brief (exp-29-arena-context-v1)

> **DERIVED_VIEW_NON_AUTHORITATIVE**: Derived, non-authoritative launch brief assembled from canonical Git sources. Git remains the only source of truth: on any conflict the canonical files win; verify freshness before use and re-derive or discard this packet on any mismatch.

Verify freshness before use: `python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify --packet <ARENA_CONTEXT.json> --root <repo-root>`. Any source digest mismatch ⇒ STALE; missing stop rule, missing/ambiguous disposition, unsupported active checkpoint, or invalid lesson scope ⇒ REJECTED.

## NOW

- Project: Murat Project Engineer
- Goal: Test whether a deterministic Git-derived startup packet can let a fresh Arena session resume context-heavy MPE work with less rediscovery while preserving Git as the only source of truth and avoiding a separate memory platform.
- Task: EXP-29/CP-09 (checkpoint CP-09)
- Experiment: EXP-29 — Arena Bootstrap Harness (`experiments/exp-29-arena-bootstrap-harness`)
- Checkpoint chain: CP-01 → CP-02 → CP-03 → CP-04 → CP-05 → CP-06 → CP-07 → CP-08
- Disposition: REUSE_COMPONENT
- Registry status: PASS (updated 2026-10-16)
- Nearest action: CP-08 Bootstrap State Consistency Recovery: reconcile registry and current checkpoint state, preserve REUSE_COMPONENT, regenerate and verify a fresh and semantically consistent packet; follow owner instruction in PR #108. Do not merge or deploy without authorization.
- Generated against (informational): branch `arena/1d43d7c6-murat-project-engineer`, head `3969b88ff2ad6220fcb1a8c5b3d8d8854e230bec`, base `3969b88ff2ad6220fcb1a8c5b3d8d8854e230bec`

## RULES (mandatory)

Stop rules (experiments/exp-29-arena-bootstrap-harness/ARENA_TASK.md#scope-stop-rules + experiments/exp-29-arena-bootstrap-harness/README.md#boundaries):
  > Stop before implementation and return `DEEP_CHANGE_REQUIRED` if the solution needs any of: / This experiment must not create:
- memory database/vector store;
- daemon/scheduler;
- automatic persistent learning;
- Router authority;
- autonomous promotion of rules;
- shared orchestration state;
- new canonical source of truth;
- generic workflow engine.
- a memory service;
- a vector database;
- a daemon or scheduler;
- automatic memory promotion;
- a persistent agent runtime;
- a second canonical source of truth;
- Router authority changes;
- global AGENTS.md rule growth merely to feed the packet.

Deep-change gate (docs/governance/SCOPE-CHANGE-CONTROL.md §6):
  > Do not execute a substantial change without explicit approval when it:
- changes fundamental architecture;
- breaks an approved invariant;
- changes a public contract;
- requires data migration;
- changes the source of truth;
- introduces a new infrastructure platform;
- creates a new repository;
- materially changes security boundaries;
- creates unapproved recurring cost;
- is difficult to reverse;
- exceeds the approved checkpoint boundary.

Source-of-truth priority (docs/governance/SCOPE-CHANGE-CONTROL.md §2):
1. Explicit current owner instruction.
2. Current approved checkpoint/spec.
3. Repository-local mandatory governance and project instructions.
4. Existing architecture/product/domain contracts.
5. Existing code and tests.
6. Historical conventions and prior decisions.

Graceful handoff minimum (AGENTS.md): STATE, EVIDENCE, CHANGES, RESULT, BLOCKER, NEXT ACTION, HANDOFF

## KNOWN LESSONS (evidence-gated, from experiments/exp-28-agent-workflow-skills-retro/RESULTS.md)

- **R1 [PROJECT]** Use the existing context-packet pattern for context-heavy handoffs (**recommended; immediately usable**)
  - change: For a task that actually spans several context files, place a short **derived** ancestry brief in the existing task/handoff: project, goal, checkpoint/task, stop conditions, and source paths + digest…
  - verify: On the next comparable, separately authorized run, give a fresh isolated executor only the packet; require all eight genealogy answers to match the canonical files, verify each digest, count packet b…
  - source: `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md#R1` — EXP-28 RESULTS.md R1 targets context-heavy MPE handoffs (one project line); EXP-28 records 'Two synthetic/fixed cases are too small to show generality', so R1 is not GLOBAL.
- **R2 [TASK]** Bound HyperFrames bootstrap side effects in the existing EXP-24 Phase 2 task (**applied task-locally**)
  - change: Add a short conditional guard to `experiments/exp-24-hyperframes-pr-video/ARENA_TASK.md`: if HyperFrames is selected, reuse the existing local composition rather than rerunning broad `init` unless si…
  - verify: In the next authorized EXP-24 Phase 2 run, if HyperFrames is selected, record the exact preflight command and renderer version; verify no global agent-skill/config mutation and no second bootstrap af…
  - source: `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md#R2` — EXP-28 RESULTS.md R2 heading records 'applied task-locally' — EXP-24 Phase 2 only.
- **R3 [NO_CHANGE]** Add an automatic retrospective hook and promote every finding to global instructions (**rejected**)
  - change: `NO_CHANGE`—do not add an after-every-run hook, global rule, new standards file, or automatic memory promotion.
  - verify: In any future promotion proposal, require recurrence or high, evidenced cost across independent runs, show it maps to an existing instruction/check location, and demonstrate that the change prevents…
  - source: `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md#R3` — EXP-28 RESULTS.md R3 heading records 'rejected' — observed, not promoted into the bootstrap.

## REUSABLE COMPONENTS (from experiments/exp-29-arena-bootstrap-harness/RESULTS.md)

- (none parsed)

## KNOWN TRAPS (verified limitations, from experiments/exp-29-arena-bootstrap-harness/RESULTS.md)

- **CP-06 — prose STOP sentences are not parsed.** EXP-22's (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-06 — boundary titles are an explicit list** (`STOP_SECTION_TITLES`). A (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-06 — every `## Guardrails` bullet is a rule, preferences included** (for (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-06 — union is not reconciliation.** Rules from different sections are all (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-06 — disposition conflicts are checked only between ARENA_TASK.md and (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-06 — FRESH is not complete startup.** The EXP-22 packet is FRESH but lacks (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-06 — point-in-time EXP-22 packet.** `evidence/bootstrap/cp06/` becomes (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **Pre-existing, not changed:** the EXP-29 README top line `Status: PLANNED` (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **Registry not updated for CP-06.** The EXP-29 registry entry still describes (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-07 — registry status enum has no `PARTIAL`.** The EXP-22 entry records (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-07 — the registry carries run state as free text.** `result_summary` / (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- **CP-07 — point-in-time EXP-22 packet.** `evidence/bootstrap/cp07/` (like (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- The A/B comparison is a **retrieval-cost proxy** (bytes/files/tool ops counted (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- One frozen fixture (EXP-27). EXP-27 CP-02 additionally verified EXP-25 with (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- The builder parses canonical prose (headings, tables, bullets). A formatting (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- `generated_against` git refs are informational and excluded from the (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- The worker refuses any GLOBAL lesson scope outright (it cannot check the (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)
- The 7 pre-existing unittest failures (registry-status schema mismatches for (`experiments/exp-29-arena-bootstrap-harness/RESULTS.md`)

## RESUME

- Status: PASS
- Result summary: PASS / REUSE_COMPONENT: a deterministic, LLM-free bootstrap builder derives ARENA_CONTEXT.json/.md from canonical Git sources (registry, task files, STATUS, AGENTS, governance, EXP-27/EXP-28 results) with sha256 provenance for every source and every item source-linked. Fresh-session A/B on the froz…
- Next action: CP-08 Bootstrap State Consistency Recovery: reconcile registry and current checkpoint state, preserve REUSE_COMPONENT, regenerate and verify a fresh and semantically consistent packet; follow owner instruction in PR #108. Do not merge or deploy without authorization.
- Next authorized action: CP-08 (bootstrap state consistency recovery) is complete as a bounded checkpoint and is the current authorized action: the committed `ARENA_CONTEXT.json` / `.md` describe the current task (`EXP-29/CP-08`) with the `REUSE_COMPONENT` disposition and a complete resume action, an absent disposition or an undeclared active checkpoint now fails closed, and the documented ritual publishes the current task for this experiment instead of the frozen CP-03 fixture (`evidence/cp08.json`). Its PR is opened and must not be merged as part of this checkpoint: **STOP after PR delivery and await owner review.** Recording CP-08 completion in the EXP-29 registry entry, and any broader adoption (automatic packet generation per session, GLOBAL lesson promotion, runtime integration), remain separate owner decisions with their own New Idea Filter / deep-change assessment.
- Evidence: `experiments/exp-29-arena-bootstrap-harness/RESULTS.md` (full result record in the canonical experiment RESULTS.md)

## PROVENANCE (canonical sources + digests)

| Path | SHA-256 | Role |
|---|---|---|
| `experiments/EXPERIMENT_REGISTRY.json` | `ffc8ca0f74672b71879da4e1f6114f121b301d4ff149edbabc60e2db98dd3834` | registry |
| `experiments/exp-29-arena-bootstrap-harness/ARENA_TASK.md` | `cf4d92a7b865c4bc8a6dd21fd4397d7f05f164504a0f7e4224e151cb1668ae55` | task_instructions |
| `experiments/exp-29-arena-bootstrap-harness/README.md` | `5003d01416b2a8a3665676bec390a6d5ddb6c8d90e91d7c06a4cb5323cffab64` | task_readme |
| `experiments/exp-29-arena-bootstrap-harness/RESULTS.md` | `09456d90e71a5199a24e3e06b165e96fa0d89c8a13cca99043017a1d46d74ab4` | experiment_results |
| `STATUS.md` | `a9c3bc395ac06371913334d8cd920603edeaaed33d2225956445f2e7afdbbfb5` | project_status |
| `AGENTS.md` | `bb4e5e24858c9725980f83c3ab4c1bb4ff2c3b8d44dbb74ef5edff4edfa179e7` | agents_rules |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | `954a9a58fd5d35352b808a8c78600da821893fea078c02aa8b67f46ae593447b` | governance |
| `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md` | `35a98ee8609a4b0b6dbf712b423d677b91aae70d52f0fd7ccd2a82c8966562a8` | accepted_lessons |

## FRESHNESS

- Rule: FRESH only when every source_refs sha256 matches the current file AND the packet equals a deterministic rebuild from current sources; otherwise the packet is STALE or REJECTED and must be treated as a non-authoritative hint.
- Safety invariants: authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE); at least one task stop/deep-change rule present; deep-change gate bullets present; a disposition is declared by a canonical source; a missing or conflicting disposition is never resolved silently (missing/ambiguous disposition ⇒ REJECTED); the active checkpoint is declared in the packet's canonical checkpoint chain (unsupported active checkpoint ⇒ REJECTED); lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)
