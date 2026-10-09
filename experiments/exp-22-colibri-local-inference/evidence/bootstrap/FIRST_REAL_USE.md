# EXP-29 Bootstrap — first real-use run (EXP-22 / CP-01)

Date: 2026-10-09. Executor: Arena. Branch: `arena/42502a3d-murat-project-engineer`.
Base: `585f078b679a1d7d5a3e36afe8c10dc22b978670` (HEAD == main == origin/main, fresh).

Harness: `experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py` (unmodified).

## Commands

```bash
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
  build --experiment EXP-22 --checkpoint CP-01 \
  --out-json experiments/exp-22-colibri-local-inference/evidence/bootstrap/ARENA_CONTEXT.json \
  --out-md   experiments/exp-22-colibri-local-inference/evidence/bootstrap/ARENA_CONTEXT.md
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
  verify --packet experiments/exp-22-colibri-local-inference/evidence/bootstrap/ARENA_CONTEXT.json --json
# mandated retry on non-FRESH: delete artifacts, rebuild from current Git, verify again
```

## Result

- Initial verification: **REJECTED** (`missing_stop_rules`, exit 3).
- Retry after regeneration from current Git: **REJECTED** (byte-identical packet, same reason).
- No other check failed: `authority_disclaimer`, `deep_change_gate_present`,
  `lesson_scopes_valid`, `source_digests_match`, `matches_rebuild` all true;
  `field_diffs` empty.
- This is **not a source conflict**. Digests match and the packet equals a
  deterministic rebuild. The failure is harness parser coverage (see Finding H-1).
- Packet **REFUSED**: not used as authority for any EXP-22 action. All EXP-22
  stop/deep-change boundaries below were taken directly from canonical
  `ARENA_TASK.md` / `README.md` / governance files. The safety check was not
  bypassed — the rejected packet was discarded as the verifier instructs.

## Startup measurements (required evidence)

- Packet bytes: JSON **8097**, MD **6907**, total **15004**.
- Source-ref count: **7** (registry, task_instructions, task_readme,
  project_status, agents_rules, governance, accepted_lessons).
  `experiment_results` correctly absent: EXP-22 has no `RESULTS.md` yet (PLANNED).
- Files read before first useful EXP-22 action: **9 distinct files,
  134,732 bytes** (EXP-22 ARENA_TASK 3903 + README 4566; EXP-29 README 2580 +
  ARENA_TASK 6913 + bootstrap_builder.py 28764 + exp29_proof.py 22389;
  EXPERIMENT_REGISTRY.json 50613; generated ARENA_CONTEXT.json 8097 + .md 6907).
- Tool operations before first useful EXP-22 action: **16** (9 reads/file
  queries + build + 2 verifies + 4 inspection bashes).
- Rediscovery prevented by the packet: **none** — the packet was REJECTED, so
  every EXP-22 fact had to be established by direct canonical reads. Even the
  successfully parsed layers carried gaps (below) that would have forced
  re-reads under a FRESH verdict too.
- Stale/incorrect lessons: **none**. R1/R2/R3 titles match the canonical
  EXP-28 `RESULTS.md` headings verbatim; scopes PROJECT/TASK/NO_CHANGE are
  consistent with the headings ("applied task-locally" → TASK,
  "rejected" → NO_CHANGE). Note: R2 is correctly scoped but is noise for
  EXP-22 (HyperFrames EXP-24-only lesson shipped in every packet).
- Genealogy correctness: **partial**.
  - Correct: project, parent goal, experiment id/name/path, task `EXP-22/CP-01`,
    checkpoint `CP-01`, registry status/updated, nearest action, resume block.
  - Missing: checkpoint chain (empty; parser scans only `ARENA_TASK.md` for
    `##/### CP-NN` headings, but EXP-22 declares CP-01..CP-03 in `README.md`
    as `### CP-01/02/03`) and disposition (empty; parser wants a `Decision:`
    line in `ARENA_TASK.md`, but EXP-22 declares `Decision: EXPERIMENT` only
    in `README.md`).
- Stop/deep-change boundary correctness: **stop rules missing (caused the
  REJECTED verdict); deep-change gate correct**.
  - `stop_rules: []` although canonical boundaries exist: `ARENA_TASK.md`
    "Before changing code" ("If a deep-change is required, STOP and report
    it.") and "## Boundaries" (Not allowed list), plus `README.md`
    "## Failure / stop criteria" and "## Guardrails". The parser only accepts
    sections titled exactly `Stop conditions` / `Scope stop rules` or lines
    starting with `STOP`, so it extracts none of them.
  - Deep-change gate: 11 bullets + intro, verified against
    `docs/governance/SCOPE-CHANGE-CONTROL.md` §6 — correct.
  - Source-of-truth priority (6 items) and handoff fields (7: STATE, EVIDENCE,
    CHANGES, RESULT, BLOCKER, NEXT ACTION, HANDOFF — verified against
    `AGENTS.md` §"Graceful handoff contract", lines 73–79) — correct.

## Separate harness findings (EXP-29 not modified, per task boundary)

- **H-1 (blocking for reuse): stop-rule parser too narrow → false REJECTED.**
  `_parse_stop_rules` misses real boundaries phrased as `## Boundaries` /
  `## Failure / stop criteria` / mid-sentence `STOP`. Fail-closed direction
  is safe, but first real use outside the EXP-27 fixture cannot reach FRESH.
- **H-2 (misleading): renderer hardcodes EXP-27 fixture labels.**
  `render_markdown` prints `## REUSABLE COMPONENTS (from EXP-27 RESULTS.md)`
  and `## KNOWN TRAPS (verified limitations, EXP-27 RESULTS.md)` for every
  experiment (builder lines 474, 482), while the data actually comes from the
  target experiment's own `RESULTS.md`. For EXP-22 the sections are empty but
  misattributed.
- **H-3 (coverage): checkpoint-chain and disposition parsers read only
  `ARENA_TASK.md`.** Experiments declaring checkpoints/disposition in
  `README.md` (as EXP-22 does) get empty genealogy fields without any warning.

## Artifacts

- `ARENA_CONTEXT.json` (8097 B, refused packet, kept for audit)
- `ARENA_CONTEXT.md` (6907 B, refused packet, kept for audit)
- `verify.json`, `verify_retry.json` (both REJECTED, identical reasons)
