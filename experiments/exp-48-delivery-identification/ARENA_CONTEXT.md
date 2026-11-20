# ARENA_CONTEXT — derived launch brief (exp-29-arena-context-v1)

> **DERIVED_VIEW_NON_AUTHORITATIVE**: Derived, non-authoritative launch brief assembled from canonical Git sources. Git remains the only source of truth: on any conflict the canonical files win; verify freshness before use and re-derive or discard this packet on any mismatch.

Verify freshness before use: `python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify --packet <ARENA_CONTEXT.json> --root <repo-root>`. Any source digest mismatch ⇒ STALE; missing stop rule, missing/ambiguous disposition, unsupported active checkpoint, or invalid lesson scope ⇒ REJECTED.

## NOW

- Project: AI Agent Delivery & Search Visibility
- Goal: Measure extraction accuracy and request attribution across equivalent HTML, Markdown and JSON-LD snapshots.
- Task: EXP-48/CP-01 (checkpoint CP-01)
- Experiment: EXP-48 — Agent delivery and request identification (`experiments/exp-48-delivery-identification`)
- Checkpoint chain: CP-01
- Disposition: EXTEND_EXISTING
- Registry status: PLANNED (updated 2026-11-20)
- Nearest action: Await separate owner authorization and agreed budget before research execution.
- Generated against (informational): branch `register/aid-delivery-identification`, head `a3c9f78147525043a9cd795c4b7730a27906eb7f`, base `unknown`

## RULES (mandatory)

Stop rules (experiments/exp-48-delivery-identification/ARENA_TASK.md#scope-stop-rules):
- Await separate owner authorization for Arena and an agreed time and cost ceiling.
- Stop if the approved public snapshot or matched control is unavailable.
- Stop before changes to production, disclosure of private data or paid calls outside the approved ceiling.

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
- Result summary: PLANNED. No observations collected.
- Next action: Await separate owner authorization and agreed budget before research execution.
- Next authorized action: (none recorded)
- Evidence: `` (full result record in the canonical experiment RESULTS.md)

## PROVENANCE (canonical sources + digests)

| Path | SHA-256 | Role |
|---|---|---|
| `experiments/EXPERIMENT_REGISTRY.json` | `92d96d5c50104f5c4ffae7bd548aade406f84aa8135589d3ae6f02f3b235a444` | registry |
| `experiments/exp-48-delivery-identification/ARENA_TASK.md` | `3fb8f7672f5c0c1b91391d9e3b6a8d95cccf9cf90548a2ea835dd3a5af21d74e` | task_instructions |
| `experiments/exp-48-delivery-identification/README.md` | `319ebece8e798820cf83ff5f3189504fec7cecb868f1e8729d2523ab6d717c6d` | task_readme |
| `STATUS.md` | `2b8f4658e5251ef568b9e143c14c1c8a6f141fb55438e296e1e3beaf2de36105` | project_status |
| `AGENTS.md` | `bb4e5e24858c9725980f83c3ab4c1bb4ff2c3b8d44dbb74ef5edff4edfa179e7` | agents_rules |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | `954a9a58fd5d35352b808a8c78600da821893fea078c02aa8b67f46ae593447b` | governance |
| `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md` | `35a98ee8609a4b0b6dbf712b423d677b91aae70d52f0fd7ccd2a82c8966562a8` | accepted_lessons |

## FRESHNESS

- Rule: FRESH only when every source_refs sha256 matches the current file AND the packet equals a deterministic rebuild from current sources; otherwise the packet is STALE or REJECTED and must be treated as a non-authoritative hint.
- Safety invariants: authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE); at least one task stop/deep-change rule present; deep-change gate bullets present; a disposition is declared by a canonical source; a missing or conflicting disposition is never resolved silently (missing/ambiguous disposition ⇒ REJECTED); the active checkpoint is declared in the packet's canonical checkpoint chain (unsupported active checkpoint ⇒ REJECTED); lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)
