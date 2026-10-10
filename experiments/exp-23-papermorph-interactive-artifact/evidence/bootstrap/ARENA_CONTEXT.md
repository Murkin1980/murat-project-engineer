# ARENA_CONTEXT — derived launch brief (exp-29-arena-context-v1)

> **DERIVED_VIEW_NON_AUTHORITATIVE**: Derived, non-authoritative launch brief assembled from canonical Git sources. Git remains the only source of truth: on any conflict the canonical files win; verify freshness before use and re-derive or discard this packet on any mismatch.

Verify freshness before use: `python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify --packet <ARENA_CONTEXT.json> --root <repo-root>`. Any source digest mismatch ⇒ STALE; missing stop rule or invalid lesson scope ⇒ REJECTED.

## NOW

- Project: Murat Project Engineer
- Goal: Test whether Papermorph's document/script → structured storyboard → narration → procedural animation/interaction pipeline yields reusable value for existing Murat projects without creating a parallel product or repository.
- Task: EXP-23/CP-01 (checkpoint CP-01)
- Experiment: EXP-23 — Papermorph document → interactive artifact (`experiments/exp-23-papermorph-interactive-artifact`)
- Checkpoint chain: CP-01 → CP-02 → CP-03
- Disposition: EXPERIMENT
- Registry status: PLANNED (updated 2026-10-06)
- Nearest action: After EXP-22 Colibri completes, Arena runs one technical/business document fixture, one bounded AI-serial script fixture, then maps reusable components to existing projects.
- Generated against (informational): branch `arena/480eb267-murat-project-engineer`, head `d7627d9033faeb43c0aaab98e0bf1595eb99db1b`, base `d7627d9033faeb43c0aaab98e0bf1595eb99db1b`

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

- Status: PLANNED
- Result summary: Planned. Primary disposition EXPERIMENT. No new repository, production integration, autonomous service, automatic publishing, or AI-serial canon change is authorized.
- Next action: After EXP-22 Colibri completes, Arena runs one technical/business document fixture, one bounded AI-serial script fixture, then maps reusable components to existing projects.
- Next authorized action: (none recorded)
- Evidence: `` (full result record in the canonical experiment RESULTS.md)

## PROVENANCE (canonical sources + digests)

| Path | SHA-256 | Role |
|---|---|---|
| `experiments/EXPERIMENT_REGISTRY.json` | `ef3ca4dd38a172146f4ae0f1574be5fbf2cd4ca682ee730c146e1ed54d2bd6c7` | registry |
| `experiments/exp-23-papermorph-interactive-artifact/ARENA_TASK.md` | `2be3cd2d346427d86b88e38059d71d622adbee49e9454f3477d703fa31297e92` | task_instructions |
| `experiments/exp-23-papermorph-interactive-artifact/README.md` | `64aacfd42035f26147a84e45249405422b332b881682c6f581f0d275dc82f07d` | task_readme |
| `STATUS.md` | `968d47ad10910c5875f83f6c74933369aa0b70486e51cbd2bcb7b65ccb2d96e5` | project_status |
| `AGENTS.md` | `d440af35dffc0c58b238a84965ede010aa94d78e07a6ea06e701bcf41e25771d` | agents_rules |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | `c4b747249f37d94dab9e5597b6e03692d2064846a4b7903a5b68036f996a0f9e` | governance |
| `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md` | `35a98ee8609a4b0b6dbf712b423d677b91aae70d52f0fd7ccd2a82c8966562a8` | accepted_lessons |

## FRESHNESS

- Rule: FRESH only when every source_refs sha256 matches the current file AND the packet equals a deterministic rebuild from current sources; otherwise the packet is STALE or REJECTED and must be treated as a non-authoritative hint.
- Safety invariants: authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE); at least one task stop/deep-change rule present; deep-change gate bullets present; lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)
