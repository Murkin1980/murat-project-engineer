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
- Registry status: PARTIAL (updated 2026-10-09)
- Nearest action: Do not repeat CP-01…CP-03 (already executed). Recommendation HOLD: run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available ≥8 GB machine and record accuracy/determinism/latency before any adapter work; no production integration is authorized.
- Generated against (informational): branch `arena/0ed937e3-murat-project-engineer`, head `a5a16bbf2cf339a3ff2eac398486ba9ad7c9e41f`, base `a5a16bbf2cf339a3ff2eac398486ba9ad7c9e41f`

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

- Local constrained decision endpoint (Colibri System One / Brio `choice`) behind a Jev-shaped call — PROVEN structurally (quality OPEN) → **HOLD** — candidate optional provider; adopt only after the released-weight quality run (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- OpenAI/Anthropic chat-shaped adapter for decision models — REJECT (fail-closed 400 by design) → **KEEP_EXISTING** — do not extend the decision adapter to chat completions (`experiments/exp-22-colibri-local-inference/RESULTS.md`)

## KNOWN TRAPS (verified limitations, from experiments/exp-22-colibri-local-inference/RESULTS.md)

- Decision quality (accuracy, calibration, ambiguity handling) is **NOT measured** on released weights: the 842 MB Laya checkpoint was HuggingFace-only and unreachable from the original sandbox. It stays the blocker for any adoption decision. (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- Tiny-Laya numbers (7–13 ms, ~48 MB RSS, random CI-fixture weights) are structural only — not released-model quality or latency (upstream released path: 219 ms/question, laptop CPU). (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- Laya is English-only (collapses on non-Latin scripts while staying confident); routing probability thresholds stay uncalibrated in this run. (`experiments/exp-22-colibri-local-inference/RESULTS.md`)
- This repository currently has no provider seam for the adapter to plug into (future-architecture socket only); no production integration is authorized. (`experiments/exp-22-colibri-local-inference/RESULTS.md`)

## RESUME

- Status: PARTIAL
- Result summary: RESULT: PARTIAL; RECOMMENDATION: HOLD; DEEP_CHANGE: NO. Executed checkpoints: CP-01, CP-02, CP-03. 66/66 HTTP 200, 0 malformed, 22/22 deterministic, 7-13 ms at ~48 MB RSS (tiny fixture). Decision quality NOT measured on released weights. No production integration.
- Next action: Do not repeat CP-01…CP-03 (already executed). Recommendation HOLD: run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available ≥8 GB machine and record accuracy/determinism/latency before any adapter work; no production integration is authorized.
- Next authorized action: Run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available ≥8 GB machine and record accuracy/determinism/latency before any adapter work; no production integration is authorized.
- Evidence: `experiments/exp-22-colibri-local-inference/RESULTS.md` (full result record in the canonical experiment RESULTS.md)

## PROVENANCE (canonical sources + digests)

| Path | SHA-256 | Role |
|---|---|---|
| `experiments/EXPERIMENT_REGISTRY.json` | `d2e68fda1f1289ba76ff1ac41eb63d508dd2ab66e8ce685f9abd72f511d10f11` | registry |
| `experiments/exp-22-colibri-local-inference/ARENA_TASK.md` | `3504512bd7d0ab09e9448388149401a8aee84ec0b76310164e340c6b7a9a8bd4` | task_instructions |
| `experiments/exp-22-colibri-local-inference/README.md` | `a102a28dac4fcd40cef4033cf73c79eb22d5de344d6cc877cf303c8587fd8925` | task_readme |
| `experiments/exp-22-colibri-local-inference/RESULTS.md` | `bca8fd164d0b442881ae329a248679392331248256036d5938b78ecf32500363` | experiment_results |
| `STATUS.md` | `968d47ad10910c5875f83f6c74933369aa0b70486e51cbd2bcb7b65ccb2d96e5` | project_status |
| `AGENTS.md` | `d440af35dffc0c58b238a84965ede010aa94d78e07a6ea06e701bcf41e25771d` | agents_rules |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | `c4b747249f37d94dab9e5597b6e03692d2064846a4b7903a5b68036f996a0f9e` | governance |
| `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md` | `35a98ee8609a4b0b6dbf712b423d677b91aae70d52f0fd7ccd2a82c8966562a8` | accepted_lessons |

## FRESHNESS

- Rule: FRESH only when every source_refs sha256 matches the current file AND the packet equals a deterministic rebuild from current sources; otherwise the packet is STALE or REJECTED and must be treated as a non-authoritative hint.
- Safety invariants: authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE); at least one task stop/deep-change rule present; deep-change gate bullets present; lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)
