# EXP-29 CP-01 — Existing capability map

Scope: `need → existing MPE component → reusable? → gap → decision` for the Arena
Bootstrap Harness. Audited before any EXP-29 code was written (Phase 0):
`AGENTS.md`, `docs/governance/SCOPE-CHANGE-CONTROL.md`, `STATUS.md`,
`experiments/EXPERIMENT_REGISTRY.json`, EXP-27 results/evidence (context packets,
resumable execution), EXP-28 results (evidence-gated retrospective), and the
existing runtime/handoff/context helpers (`scripts/runtime_coordination.py`,
`scripts/task_acceptance.py`, `scripts/validate_package.py`, `context/CONTEXT_MAP.md`,
`context/project-context.md`, `contracts/HANDOFF.md`, EXP-27 `harness/run_state.py`).

Dispositions used (per `ARENA_TASK.md` CP-01): `KEEP_EXISTING`, `REUSE`, `EXTEND`,
`REJECT_DUPLICATE`.

## Map

| # | Need | Existing MPE component | Reusable? | Gap | Decision |
|---|---|---|---|---|---|
| 1 | Task genealogy / context packet (`project → goal → experiment/checkpoint → task`, stop conditions) | EXP-27 CP-02 `harness/mpe_proof.py::build_packet` + `harness/fresh_worker.py` (experiment-scoped, closed; `RESULTS.md` CP-02, `evidence/cp02.json`) | Yes, as a pattern | Packet builder lives only inside the closed EXP-27 harness; no staleness verification; single-layer (genealogy only); not reusable from a fresh Arena session | **EXTEND** — build the EXP-29 bootstrap builder inside this experiment, reusing the EXP-27 parsing conventions (checkpoint regex, `Decision:` line, stop-condition sections, isolated `python3 -I` fresh worker, source digests). Do not modify EXP-27 code |
| 2 | Graceful handoff contract (STATE / EVIDENCE / CHANGES / RESULT / BLOCKER / NEXT ACTION / HANDOFF) | `AGENTS.md` "Graceful handoff contract" + `contracts/HANDOFF.md` typed handoff; proven by EXP-27 CP-04 (`harness/run_state.py`, 21/21 fields) | Yes | No packet assembles the handoff minimum for a fresh session | **KEEP_EXISTING** (contract) + **REUSE** — the builder parses the field labels from `AGENTS.md` and emits them in the RULES layer; no contract change |
| 3 | Source digests (provenance / staleness) | EXP-27 `harness/run_state.py::sha256_file` (3-line stdlib helper) | Yes | None for the mechanism itself | **REUSE** — reimplement the same stdlib `sha256_file` locally in the EXP-29 builder (no cross-experiment import; EXP-27 stays closed and untouched) |
| 4 | Experiment registry (identity, goal, status, next action, evidence links) | `experiments/EXPERIMENT_REGISTRY.json` (canonical) | Yes, as a source | 48 KB — too large to hand to a fresh session verbatim | **KEEP_EXISTING** (canonical source) + **REUSE** — the builder reads the target entry and cites path + sha256; the registry is never copied or condensed into a new store |
| 5 | Status / nearest action | `STATUS.md` ("Next actions", "Boundaries still in force", deep-change rule) | Yes, as a source | Project-level, not task-level; large | **KEEP_EXISTING** + **REUSE** — cited in NOW/RESUME with digest; only the registry `next_action` of the target experiment is promoted into the packet as the nearest action |
| 6 | Task-local instructions (checkpoints, disposition, stop rules) | Per-experiment `ARENA_TASK.md` + `README.md` (stop-conditions fallback, as in EXP-27 CP-02) | Yes, as a source | Scattered across 2–3 files per task | **KEEP_EXISTING** + **REUSE** — parsed at build time; no new instruction store |
| 7 | Accepted lessons from experiment results | EXP-28 `RESULTS.md` recommendations R1/R2/R3 with evidence, scope and verification paths (evidence-gated promotion per EXP-28) | Yes, as a source | Prose-only; no machine-readable lesson index; EXP-28 explicitly rejects automatic promotion (R3) | **REUSE** — parse R1/R2/R3 headings + minimal-change/verification bullets from the canonical EXP-28 `RESULTS.md` at build time; scope (PROJECT/TASK/NO_CHANGE) is this experiment's recorded, evidence-gated promotion decision, documented here and in `RESULTS.md`; **no automatic learning, no new lesson store** |
| 8 | Reusable components (accepted patterns) | EXP-27 `RESULTS.md` "Per-pattern disposition" table (5 patterns with ADOPT/REUSE/REJECT verdicts) | Yes, as a source | Prose table | **REUSE** — parse the table rows at build time into the REUSABLE COMPONENTS layer with source digest |
| 9 | Known traps / verified hazards | EXP-27 `RESULTS.md` "Known limitations / blockers" (6 verified limitations); EXP-28 friction classes | Yes, as a source | Prose bullets | **REUSE** — parse the limitations section at build time into KNOWN TRAPS with source digest |
| 10 | Fail-closed evidence trust (derived claims must be backed by trusted sources) | `scripts/validate_package.py` evidence-trust boundary (EXP-002 Iteration 3): untrusted/unknown evidence fails closed | Yes, as a pattern | Applies to run-report gates, not to packet verification | **REUSE** — the EXP-29 verifier is fail-closed: digest mismatch, rebuild mismatch, missing stop/deep-change rule, or invalid lesson scope ⇒ packet is STALE/REJECTED and non-authoritative; it never silently overrides canonical files |
| 11 | Progressive disclosure / navigation policy | `context/CONTEXT_MAP.md`, `context/project-context.md` (source priority, memory classes: "never auto-promote") | Yes | Documentation only; not a packet | **KEEP_EXISTING** — the packet is consistent with it (derived view, Git canonical, no auto-promotion). Not embedded wholesale; the source-of-truth priority from `docs/governance/SCOPE-CHANGE-CONTROL.md` §2 is embedded instead because it is the binding rule a fresh session needs first |
| 12 | Runtime coordination helpers (events, leases) | `scripts/runtime_coordination.py` (bounded stateless helpers) | Not needed | Packet building is a pure read/derive function; no runtime events required | **KEEP_EXISTING** — no reuse, no modification; EXP-29 adds no runtime helper |
| 13 | A memory service / vector DB / lesson store for the bootstrap | EXP-15 MPE Project Memory Layer (PASS, validated, `experiments/exp-15-memory/`); EXP-QOOPIA-MEMORY (RETIRED) | No | Would duplicate the already-validated memory hypothesis and become a second source of truth; EXP-15 result says reuse as optional pre-execution context injection, not a new store | **REJECT_DUPLICATE** — the bootstrap packet is a derived view of canonical Git sources, exactly the EXP-15/EXP-27 pattern; a store would also be a deep change (STOP rule) |
| 14 | Automatic lesson/rule promotion into future bootstraps | None exists (EXP-28 R3 explicitly rejected an automatic retrospective hook and global promotion) | No | Autonomous promotion is on the EXP-29 stop list | **REJECT_DUPLICATE** — lessons enter the packet only through this experiment's recorded, evidence-gated curation (EXP-28 promotion rule: explicit evidence + known scope + minimal formulation + verification path + no governance conflict) |
| 15 | A second registry / condensed lesson index file | `experiments/EXPERIMENT_REGISTRY.json`, EXP-28 `RESULTS.md` | No | A new index would be a second source of truth | **REJECT_DUPLICATE** — the builder parses the canonical files at generation time and cites path + sha256; nothing new is canonical |

## CP-01 conclusion

No existing component assembles a fresh-session launch packet, and none is needed
beyond an **EXTEND** of the closed EXP-27 CP-02 pattern plus **REUSE** of canonical
sources (registry, task files, STATUS, AGENTS, governance, EXP-27/EXP-28 results).
Every duplicate mechanism (memory store, lesson index, automatic promotion) is
rejected. No memory subsystem is necessary, so the `DEEP_CHANGE_REQUIRED` stop does
not trigger. Proceed to CP-02.
