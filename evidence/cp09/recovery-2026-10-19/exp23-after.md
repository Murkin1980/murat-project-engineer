# ARENA_CONTEXT — derived launch brief (exp-29-arena-context-v1)

> **DERIVED_VIEW_NON_AUTHORITATIVE**: Derived, non-authoritative launch brief assembled from canonical Git sources. Git remains the only source of truth: on any conflict the canonical files win; verify freshness before use and re-derive or discard this packet on any mismatch.

Verify freshness before use: `python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify --packet <ARENA_CONTEXT.json> --root <repo-root>`. Any source digest mismatch ⇒ STALE; missing stop rule, missing/ambiguous disposition, unsupported active checkpoint, or invalid lesson scope ⇒ REJECTED.

## NOW

- Project: Murat Project Engineer
- Goal: Test whether Papermorph's document/script → structured storyboard → narration → procedural animation/interaction pipeline yields reusable value for existing Murat projects without creating a parallel product or repository.
- Task: EXP-23/CP-03 (checkpoint CP-03)
- Experiment: EXP-23 — Papermorph document → interactive artifact (`experiments/exp-23-papermorph-interactive-artifact`)
- Checkpoint chain: CP-01 → CP-02 → CP-03
- Disposition: REUSE_COMPONENT
- Registry status: PASS (updated 2026-10-10)
- Nearest action: Experiment closed with REUSE_COMPONENT. Do not adopt the Papermorph engine. If the owner accepts reuse, evaluate the mark-based narration↔visual sync contract in EXP-24 and the quiz data model in 1C Tutor KZ through separate bounded owning-project checkpoints. Replacing the 3 CP-01 silent TTS placeholders is optional evidence hygiene, not a blocker.
- Generated against (informational): branch `arena/1d43d7c6-murat-project-engineer`, head `3969b88ff2ad6220fcb1a8c5b3d8d8854e230bec`, base `3969b88ff2ad6220fcb1a8c5b3d8d8854e230bec`

## RULES (mandatory)

Stop rules (experiments/exp-23-papermorph-interactive-artifact/README.md#failure-stop-criteria + experiments/exp-23-papermorph-interactive-artifact/README.md#guardrails):
  > STOP or FAIL if:
- factual hallucination rate makes the artifact unsafe to trust;
- one-shot output looks impressive but requires heavy manual repair;
- useful behavior depends on opaque one-off prompts that cannot be reproduced;
- output is effectively a non-editable final video rather than a reusable pipeline;
- upstream coupling is too strong to reuse components cleanly;
- experiment starts duplicating MPE orchestration, CMS, or AI-serial infrastructure;
- Arena discovers a deep-change requirement.
- No new repository.
- No production deployment.
- No new standalone product.
- No autonomous background service.
- No AI-serial canon change from generated output.
- No automatic publishing.
- Pin upstream revision used for the test.
- Record license and dependency constraints before reuse.
- Keep all evidence under this experiment directory.
- Prefer stock upstream behavior before modifications.
- Do not expand scope beyond the two fixtures until evidence is reviewed.

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

## REUSABLE COMPONENTS (no experiment RESULTS.md present)

- (none parsed)

## KNOWN TRAPS (verified limitations, no experiment RESULTS.md present)

- (none parsed)

## RESUME

- Status: PASS
- Result summary: PASS / REUSE_COMPONENT (2026-10-10). Bootstrap preflight FRESH. CP-01 READY: stock Papermorph @093418e (MIT) on the MPE governance doc produced a playable 11-beat interactive artifact with 0 factual errors, 2 manual corrections and beat-level regeneration. CP-02 READY after correcting the private-r…
- Next action: Experiment closed with REUSE_COMPONENT. Do not adopt the Papermorph engine. If the owner accepts reuse, evaluate the mark-based narration↔visual sync contract in EXP-24 and the quiz data model in 1C Tutor KZ through separate bounded owning-project checkpoints. Replacing the 3 CP-01 silent TTS placeholders is optional evidence hygiene, not a blocker.
- Next authorized action: (none recorded)
- Evidence: `` (full result record in the canonical experiment RESULTS.md)

## PROVENANCE (canonical sources + digests)

| Path | SHA-256 | Role |
|---|---|---|
| `experiments/EXPERIMENT_REGISTRY.json` | `ffc8ca0f74672b71879da4e1f6114f121b301d4ff149edbabc60e2db98dd3834` | registry |
| `experiments/exp-23-papermorph-interactive-artifact/ARENA_TASK.md` | `2be3cd2d346427d86b88e38059d71d622adbee49e9454f3477d703fa31297e92` | task_instructions |
| `experiments/exp-23-papermorph-interactive-artifact/README.md` | `ca2c2337cc2c041646d3864e06327c5c77285616c097a8265f1426df9cd41406` | task_readme |
| `STATUS.md` | `a9c3bc395ac06371913334d8cd920603edeaaed33d2225956445f2e7afdbbfb5` | project_status |
| `AGENTS.md` | `bb4e5e24858c9725980f83c3ab4c1bb4ff2c3b8d44dbb74ef5edff4edfa179e7` | agents_rules |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | `954a9a58fd5d35352b808a8c78600da821893fea078c02aa8b67f46ae593447b` | governance |
| `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md` | `35a98ee8609a4b0b6dbf712b423d677b91aae70d52f0fd7ccd2a82c8966562a8` | accepted_lessons |

## FRESHNESS

- Rule: FRESH only when every source_refs sha256 matches the current file AND the packet equals a deterministic rebuild from current sources; otherwise the packet is STALE or REJECTED and must be treated as a non-authoritative hint.
- Safety invariants: authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE); at least one task stop/deep-change rule present; deep-change gate bullets present; a disposition is declared by a canonical source; a missing or conflicting disposition is never resolved silently (missing/ambiguous disposition ⇒ REJECTED); the active checkpoint is declared in the packet's canonical checkpoint chain (unsupported active checkpoint ⇒ REJECTED); lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)
