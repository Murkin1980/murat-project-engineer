# ARENA_CONTEXT — derived launch brief (exp-29-arena-context-v1)

> **DERIVED_VIEW_NON_AUTHORITATIVE**: Derived, non-authoritative launch brief assembled from canonical Git sources. Git remains the only source of truth: on any conflict the canonical files win; verify freshness before use and re-derive or discard this packet on any mismatch.

Verify freshness before use: `python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify --packet <ARENA_CONTEXT.json> --root <repo-root>`. Any source digest mismatch ⇒ STALE; missing stop rule or invalid lesson scope ⇒ REJECTED.

## NOW

- Project: Murat Project Engineer
- Goal: Test whether Colibri can provide measurable value as an optional local inference component for constrained MPE classification and routing without creating a parallel orchestration system.
- Task: EXP-22/CP-01 (checkpoint CP-01)
- Experiment: EXP-22 — Colibri local inference / Brio routing (`experiments/exp-22-colibri-local-inference`)
- Checkpoint chain: n/a
- Disposition: n/a
- Registry status: PLANNED (updated 2026-10-06)
- Nearest action: Arena: execute CP-01 READY/WARNING/BLOCKED classification, CP-02 fixed-agent routing, and CP-03 isolated provider compatibility only if earlier checkpoints show useful signal.
- Generated against (informational): branch `arena/42502a3d-murat-project-engineer`, head `585f078b679a1d7d5a3e36afe8c10dc22b978670`, base `585f078b679a1d7d5a3e36afe8c10dc22b978670`

## RULES (mandatory)

Stop rules (experiments/exp-22-colibri-local-inference/ARENA_TASK.md):
- (none parsed)

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

## KNOWN LESSONS (evidence-gated, from EXP-28 RESULTS.md)

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

## REUSABLE COMPONENTS (from EXP-27 RESULTS.md)


## KNOWN TRAPS (verified limitations, EXP-27 RESULTS.md)


## RESUME

- Status: PLANNED
- Result summary: Planned. Primary disposition EXPERIMENT. No new repository, production deployment, provider switch, control plane, or deep-change is authorized.
- Next action: Arena: execute CP-01 READY/WARNING/BLOCKED classification, CP-02 fixed-agent routing, and CP-03 isolated provider compatibility only if earlier checkpoints show useful signal.
- Next authorized action: 
- Evidence: `` (full result record in the canonical experiment RESULTS.md)

## PROVENANCE (canonical sources + digests)

| Path | SHA-256 | Role |
|---|---|---|
| `experiments/EXPERIMENT_REGISTRY.json` | `55d92619e1a594e160c68a60b94dc06454baa52499bf70f3c636f7217c7425fe` | registry |
| `experiments/exp-22-colibri-local-inference/ARENA_TASK.md` | `3504512bd7d0ab09e9448388149401a8aee84ec0b76310164e340c6b7a9a8bd4` | task_instructions |
| `experiments/exp-22-colibri-local-inference/README.md` | `1acba5dbc0326de051a9594d1266fdb87b2c5db3bcfd44c792e572f6b797fc50` | task_readme |
| `STATUS.md` | `968d47ad10910c5875f83f6c74933369aa0b70486e51cbd2bcb7b65ccb2d96e5` | project_status |
| `AGENTS.md` | `d440af35dffc0c58b238a84965ede010aa94d78e07a6ea06e701bcf41e25771d` | agents_rules |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | `c4b747249f37d94dab9e5597b6e03692d2064846a4b7903a5b68036f996a0f9e` | governance |
| `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md` | `35a98ee8609a4b0b6dbf712b423d677b91aae70d52f0fd7ccd2a82c8966562a8` | accepted_lessons |

## FRESHNESS

- Rule: FRESH only when every source_refs sha256 matches the current file AND the packet equals a deterministic rebuild from current sources; otherwise the packet is STALE or REJECTED and must be treated as a non-authoritative hint.
- Safety invariants: authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE); at least one task stop/deep-change rule present; deep-change gate bullets present; lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)
