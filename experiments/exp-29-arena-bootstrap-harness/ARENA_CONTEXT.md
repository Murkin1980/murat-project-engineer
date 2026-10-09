# ARENA_CONTEXT — derived launch brief (exp-29-arena-context-v1)

> **DERIVED_VIEW_NON_AUTHORITATIVE**: Derived, non-authoritative launch brief assembled from canonical Git sources. Git remains the only source of truth: on any conflict the canonical files win; verify freshness before use and re-derive or discard this packet on any mismatch.

Verify freshness before use: `python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py verify --packet <ARENA_CONTEXT.json> --root <repo-root>`. Any source digest mismatch ⇒ STALE; missing stop rule or invalid lesson scope ⇒ REJECTED.

## NOW

- Project: Murat Project Engineer
- Goal: Extract and test high-value orchestration patterns from Paperclip—goal context, atomic task lease, persistent resumable evidence, budget/runaway guards, and approval gates—inside existing MPE/murat-ai-orchestrator components without adopting a parallel control plane.
- Task: EXP-27/CP-05 (checkpoint CP-05)
- Experiment: EXP-27 — Paperclip orchestration patterns (`experiments/exp-27-paperclip-orchestration-patterns`)
- Checkpoint chain: CP-01 → CP-02 → CP-03 → CP-04 → CP-05
- Disposition: REUSE_COMPONENT
- Registry status: PASS (updated 2026-10-06)
- Nearest action: Closed at bounded pattern extraction. No production integration, Router change, governance change, or follow-on checkpoint is authorized by this result; a future owner decision is required before any pattern is implemented in an existing component.
- Generated against (informational): branch `arena/19fa71aa-murat-project-engineer`, head `6c6a592a442f0d3c779af8ae5c6e8185b9158bbb`, base `bb6f1f85fde993c0b698f7036df2699961ed1478`

## RULES (mandatory)

Stop rules (experiments/exp-27-paperclip-orchestration-patterns/README.md):
  > Stop and report before:
- new repo;
- persistent Paperclip service;
- new DB/queue/daemon;
- Router authority change;
- governance replacement;
- Git/source-of-truth change;
- autonomous merge/deploy;
- recurring paid infrastructure;
- production integration.

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

- Goal ancestry / context — BORROW → **ADOPT_IN_MPE** (derived packet + source digests; Git stays canonical) (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- Atomic task lease — ADAPT → **ADOPT_IN_ORCHESTRATOR** (single-host lease as an extension of `scripts/runtime_coordination.py`, in a future authorized checkpoint) (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- Persistent resumable evidence — KEEP + BORROW → **REUSE_PATTERN_ONLY** (add digest/idempotency key + completeness assertion to existing handoffs; no new store) (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- Budget / runaway guard — ADAPT → **ADOPT_IN_MPE** (enforced bounded-stop mapped onto the existing compute-budget status vocabulary) (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- Approval / governance gate — REJECT → **REJECT** donor mechanism; keep the existing MPE gate unchanged (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- Paperclip as a system/service/DB — REJECT → **DO_NOT_ADOPT** (parallel control plane, second source of truth) (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)

## KNOWN TRAPS (verified limitations, EXP-27 RESULTS.md)

- The lease proof is **single-host, file-backed**. MPE has no shared-filesystem guarantee across executors, so this (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- The wall-time boundary is demonstrated with an **injected deterministic clock** (the real measured duration of (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- Token/cost boundaries were exercised only through the existing `hard_limit`/`budget_health` contract; no live (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- CP-02's "rediscovery cost" is a file-read/byte proxy measured in the harness, not a human user measurement; (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- The donor was audited by reading, not by running Paperclip; anything about its runtime behaviour is the donor's (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)
- 7 pre-existing unittest failures remain (unchanged by this experiment), plus the pre-existing stale (`experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md`)

## RESUME

- Status: PASS
- Result summary: PASS / ADOPT_WITH_CHANGES at pattern level only. Donor audited at paperclipai/paperclip@d9f60004 (MIT; release tag v2026.1005.0 = 467125fa) and used as reference only. CP-02: a compact ancestry packet derived from the registry + ARENA_TASK let an isolated fresh process state project, parent goal, c…
- Next action: Closed at bounded pattern extraction. No production integration, Router change, governance change, or follow-on checkpoint is authorized by this result; a future owner decision is required before any pattern is implemented in an existing component.
- Next authorized action: None inside this experiment — **STOP after CP-05** per `ARENA_TASK.md`. Any implementation of the BORROW/ADAPT
- Evidence: `experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md` (full result record in the canonical experiment RESULTS.md)

## PROVENANCE (canonical sources + digests)

| Path | SHA-256 | Role |
|---|---|---|
| `experiments/EXPERIMENT_REGISTRY.json` | `55d92619e1a594e160c68a60b94dc06454baa52499bf70f3c636f7217c7425fe` | registry |
| `experiments/exp-27-paperclip-orchestration-patterns/ARENA_TASK.md` | `ed3bed1a1de39eecbc2167efd25e41aece0f7876c6b02b26a61ed88fc803c1e3` | task_instructions |
| `experiments/exp-27-paperclip-orchestration-patterns/README.md` | `dba4d48d997e155e91ec220e2fb13e2525e6100f3ffb110a01086b3689216ef4` | task_readme |
| `experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md` | `8fde29e81e2c05c42a48acb6d1a483077d81e61399573fb1f0653cff2ef9ae5c` | experiment_results |
| `STATUS.md` | `968d47ad10910c5875f83f6c74933369aa0b70486e51cbd2bcb7b65ccb2d96e5` | project_status |
| `AGENTS.md` | `1ac7688bdf097539ea5d7306b152c0216abb6b0ffbc01fafdecb83ce8b9cc2cd` | agents_rules |
| `docs/governance/SCOPE-CHANGE-CONTROL.md` | `c4b747249f37d94dab9e5597b6e03692d2064846a4b7903a5b68036f996a0f9e` | governance |
| `experiments/exp-28-agent-workflow-skills-retro/RESULTS.md` | `35a98ee8609a4b0b6dbf712b423d677b91aae70d52f0fd7ccd2a82c8966562a8` | accepted_lessons |

## FRESHNESS

- Rule: FRESH only when every source_refs sha256 matches the current file AND the packet equals a deterministic rebuild from current sources; otherwise the packet is STALE or REJECTED and must be treated as a non-authoritative hint.
- Safety invariants: authority disclaimer present (DERIVED_VIEW_NON_AUTHORITATIVE); at least one task stop/deep-change rule present; deep-change gate bullets present; lesson scopes limited to GLOBAL/PROJECT/TASK/NO_CHANGE; GLOBAL requires a PROMOTED_TO_GLOBAL marker in the canonical lesson source (no current source has one)
