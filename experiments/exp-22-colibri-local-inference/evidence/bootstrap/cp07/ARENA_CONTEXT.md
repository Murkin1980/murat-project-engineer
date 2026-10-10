# ARENA_CONTEXT — derived launch brief (exp-29-arena-context-v1)

> **DERIVED_VIEW_NON_AUTHORITATIVE**: Derived, non-authoritative launch brief assembled from canonical Git sources. Git remains the only source of truth: on any conflict the canonical files win; verify freshness before use and re-derive or discard this packet on any mismatch.

Verify freshness before use: `python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify --packet <ARENA_CONTEXT.json> --root <repo-root>`. Any source digest mismatch ⇒ STALE; missing stop rule or invalid lesson scope ⇒ REJECTED.

## NOW

- Project: Murat Project Engineer
- Goal: Test whether Colibri can provide measurable value as an optional local inference component for constrained MPE classification and routing without creating a parallel orchestration system.
- Task: EXP-22/CP-01 (checkpoint CP-01)
- Experiment: EXP-22 — Colibri local inference / Brio routing (`experiments/exp-22-colibri-local-inference`)
- Checkpoint chain: CP-01 → CP-02 → CP-03
- Disposition: EXPERIMENT
- Registry status: HOLD (updated 2026-10-10)
- Nearest action: Bounded released-weight quality run: execute the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available suitable machine (>= 8 GB RAM) and record accuracy/determinism/latency before any adapter work. CP-01..CP-03 must not be repeated; no production integration is authorized.
- Generated against (informational): branch `arena/4c9d8b8c-murat-project-engineer`, head `a5a16bbf2cf339a3ff2eac398486ba9ad7c9e41f`, base `a5a16bbf2cf339a3ff2eac398486ba9ad7c9e41f`

## RULES (mandatory)

Stop rules (experiments/exp-22-colibri-local-inference/ARENA_TASK.md#boundaries + experiments/exp-22-colibri-local-inference/README.md#failure-stop-criteria + experiments/exp-22-colibri-local-inference/README.md#guardrails):
  > Not allowed: / STOP or FAIL if:
- new repository;
- production deployment;
- production configuration changes;
- default-provider changes;
- secrets;
- new control plane/router;
- refactor of unrelated MPE code;
- merging any production integration as part of this experiment.
- setup cost exceeds the value of the narrow task;
- latency makes the workflow impractical;
- quality materially trails the reference path;
- hardware/storage requirements are unreasonable for intended deployment;
- compatibility requires invasive changes;
- Arena discovers a deep-change requirement;
- the experiment starts duplicating `murat-ai-orchestrator`.
- No new repository.
- No production deployment.
- No production traffic.
- No secrets committed.
- No autonomous background service.
- No replacement of existing orchestrator/router.
- No model download larger than needed for the smallest useful proof without documenting the reason first.
- Prefer a small supported MoE model for the first run.
- Pin model/version and record exact hashes/revisions where practical.
- Keep all evidence under this experiment directory.

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

## REUSABLE COMPONENTS (from experiments/exp-22-colibri-local-inference/RESULTS.md)

- CP-01 Brio status classifier (READY/WARNING/BLOCKED) — structural PASS (schema-safe, deterministic, fast); quality OPEN → HOLD — not reusable until released-weight quality is measured (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- CP-02 Agent routing decision (fixed list) — structural PASS; routing-quality OPEN → HOLD — not reusable until released-weight quality is measured (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- CP-03 Existing-provider compatibility (Jev-shaped decision client) — MET — base-URL switch works; chat-shaped clients fail closed (400) with a pointer to `/v1/systemone` → REUSE_PATTERN_ONLY — one low-risk decision operation can move behind a Colibri provider; chat generation cannot ride the same adapter (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- Colibri as a new repository / control plane / parallel orchestration — REJECT (boundary) → DO_NOT_ADOPT (`experiments/exp-22-colibri-local-inference/RESULTS.md`)

## KNOWN TRAPS (verified limitations, from experiments/exp-22-colibri-local-inference/RESULTS.md)

- Released-weight decision quality is NOT measured: the 842 MB Laya checkpoint is HuggingFace-only and was unreachable from the original sandbox; accuracy, calibration and ambiguity handling remain OPEN until the frozen fixtures run against the released checkpoint. (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- All latency/footprint numbers are tiny-Laya CI-fixture numbers (numpy-generated random weights, 2.15 MB), not released-model numbers. (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- The Laya checkpoint is English-only (collapses on non-Latin scripts while staying confident). (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- This repository currently has no provider seam for a Colibri adapter to plug into (future-architecture socket only), so no integration is authorized by this result. (`experiments/exp-22-colibri-local-inference/RESULTS.md`)

## RESUME

- Status: HOLD
- Result summary: PARTIAL / HOLD (2026-10-09). CP-01..CP-03 executed: structural decision path proven (66/66 HTTP 200, 0 malformed constrained outputs, 22/22 deterministic, 7-13 ms at ~48 MB RSS); released-weight decision quality NOT measured (checkpoint unavailable in sandbox). Next: bounded released-weight quality…
- Next action: Bounded released-weight quality run: execute the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available suitable machine (>= 8 GB RAM) and record accuracy/determinism/latency before any adapter work. CP-01..CP-03 must not be repeated; no production integration is authorized.
- Next authorized action: Run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available suitable machine (>= 8 GB RAM) and record accuracy/determinism/latency before any adapter work.
- Evidence: `experiments/exp-22-colibri-local-inference/RESULTS.md` (full result record in the canonical experiment RESULTS.md)

## PROVENANCE (canonical sources + digests)

| Path | SHA-256 | Role |
|---|---|---|
| `experiments/EXPERIMENT_REGISTRY.json` | `ef3ca4dd38a172146f4ae0f1574be5fbf2cd4ca682ee730c146e1ed54d2bd6c7` | registry |
| `experiments/exp-22-colibri-local-inference/ARENA_TASK.md` | `3504512bd7d0ab09e9448388149401a8aee84ec0b76310164e340c6b7a9a8bd4` | task_instructions |
| `experiments/exp-22-colibri-local-inference/README.md` | `d5a639f5d579485be0373247514cd22fa97e3daf48dacf46df277be4fa103dd0` | task_readme |
| `experiments/exp-22-colibri-local-inference/RESULTS.md` | `0f9911007403f0b65411ada71fd2a21d20e8d6ebb2205eca7583046f57eb0a12` | experiment_results |
| `STATUS.md` | `968d47ad10910c5875f83f6c74933369aa0b70486e51cbd2bcb7b65ccb2d96e5` | project_status |
| `AGENTS.md` | `d440af35dffc0c58b238a84965ede010aa94d78e07a6ea06e701bcf41e25771d` | agents_rules |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | `c4b747249f37d94dab9e5597b6e03692d2064846a4b7903a5b68036f996a0f9e` | governance |
| `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md` | `35a98ee8609a4b0b6dbf712b423d677b91aae70d52f0fd7ccd2a82c8966562a8` | accepted_lessons |

## FRESHNESS

- Rule: FRESH only when every source_refs sha256 matches the current file AND the packet equals a deterministic rebuild from current sources; otherwise the packet is STALE or REJECTED and must be treated as a non-authoritative hint.
- Safety invariants: authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE); at least one task stop/deep-change rule present; deep-change gate bullets present; lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)
