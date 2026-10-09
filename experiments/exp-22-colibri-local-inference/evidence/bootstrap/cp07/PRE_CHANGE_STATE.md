# EXP-29 / CP-07 — Pre-change reproduction: FRESH-but-stale-state (EXP-22 / CP-01)

Date: 2026-10-09. Executor: Arena. Base: `main` @ `a5a16bbf2cf339a3ff2eac398486ba9ad7c9e41f`
("authorize EXP-29 CP-07 canonical state repair"). Recorded **before any CP-07 edit**,
exactly as required by `experiments/exp-29-arena-bootstrap-harness/ARENA_TASK.md` CP-07
step 1.

## Commands

```bash
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
    build --experiment EXP-22 --checkpoint CP-01 \
    --out-json experiments/exp-22-colibri-local-inference/evidence/bootstrap/cp07/pre_change_packet.json \
    --out-md /tmp/pre_change_packet.md
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
    verify --packet experiments/exp-22-colibri-local-inference/evidence/bootstrap/cp07/pre_change_packet.json \
    --json > experiments/exp-22-colibri-local-inference/evidence/bootstrap/cp07/pre_change_verify.json
```

Artifacts: `pre_change_packet.json` (9,802 B, 7 source refs), `pre_change_verify.json`.

## 1. The packet verifies FRESH (the technical defect is gone since CP-06)

`pre_change_verify.json`: `status = FRESH`, `reasons = []`, every check true
(`source_digests_match`, `matches_rebuild`, `stop_rules_present`,
`deep_change_gate_present`, `lesson_scopes_valid`, `disposition_unambiguous`,
`authority_disclaimer`). Checkpoint chain `CP-01 → CP-02 → CP-03`, disposition
`EXPERIMENT`, 25 stop rules — all correct.

## 2. …yet the packet reports stale task state

| Packet field | Value in this FRESH packet | Truth (committed evidence) |
|---|---|---|
| `now.registry_status` / `resume.status` | `PLANNED` (registry `updated_at` 2026-10-06) | CP-01…CP-03 executed 2026-10-09 |
| `now.nearest_action` / `resume.next_action` | "Arena: execute CP-01 READY/WARNING/BLOCKED classification, CP-02 fixed-agent routing, and CP-03 isolated provider compatibility only if earlier checkpoints show useful signal." | CP-01…CP-03 already ran; repeating them is wrong |
| `resume.result_summary` | "Planned. Primary disposition EXPERIMENT. …" | `RESULT: PARTIAL` / `RECOMMENDATION: HOLD` |
| `resume.next_authorized_action` | `''` (→ renders "(none recorded)") | frozen-fixture run against the released Laya checkpoint on a weights-available machine |
| `known_traps` | `[]` (→ renders "(none parsed)") | decision quality NOT measured on released weights; English-only checkpoint; no provider seam |
| `resume.evidence.path` | `''` (no `RESULTS.md` exists) | — |

## 3. The canonical evidence already records the completed state

`experiments/exp-22-colibri-local-inference/FINDINGS.md` (2026-10-09) records:

- `## 3. CP-01 — Brio status classifier` — executed (36 requests, 0 malformed, 12/12 deterministic);
- `## 4. CP-02 — Agent routing decision` — executed (30 requests, 0 malformed, 10/10 deterministic);
- `## 5. CP-03 — Existing-provider compatibility` — executed (5 probes: 200/400/400/200/422);
- terminal block: `RESULT: PARTIAL`, `RECOMMENDATION: HOLD`, `DEEP_CHANGE: NO`,
  `NEXT_STEP: Run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya
  checkpoint on a weights-available ≥8 GB machine … before any adapter work.`

`FINDINGS.md` is deliberately **not** one of the packet's source roles
(`pre_change_packet.json` `source_refs`: registry, task_instructions, task_readme,
experiment_results, project_status, agents_rules, governance, accepted_lessons —
`FINDINGS in source_refs = False`). It must not become one.

## 4. Failure mode for a fresh consumer

A fresh Arena session that trusts this FRESH packet sees `PLANNED` and the nearest
action **"execute CP-01 …"** and would re-run already-completed checkpoints
(the exact CP-07 trigger). The experiment result (`PARTIAL` / `HOLD`), the
completed checkpoints, the released-weights limitation and the next authorized
action are unobtainable from the packet alone.

## 5. Audit conclusion (CP-07 step 2) — the gap is representational, not semantic

Existing canonical state mechanisms (no new source role needed):

| Fact to express | Existing channel | Feeds packet field |
|---|---|---|
| RESULT / status | registry `status` (+ `result_summary` `RESULT:` key) | `resume.status`, `resume.result_summary` |
| RECOMMENDATION | registry `result_summary` (`RECOMMENDATION:` key) | `resume.result_summary` |
| Executed checkpoints | registry `result_summary` (`Executed checkpoints:` key) | `resume.result_summary` |
| Blocker / limitation | `RESULTS.md` `## Known limitations / blockers` | `known_traps` |
| Next authorized action | `RESULTS.md` `## Next authorized action` + registry `next_action` | `resume.next_authorized_action`, `resume.next_action` |
| Full result record | `RESULTS.md` (role `experiment_results`, already a source role) | `resume.evidence` |

- `contracts/EXPERIMENT_REGISTRY.schema.json` `status` enum
  (`IDEA, PLANNED, READY_TO_TEST, RUNNING, PASS, FAIL, HOLD, ADOPTED`) lags practice:
  `RETIRED` ×3 (EXP-QOOPIA-MEMORY, EXP-UX-UI-SKILLS, EXP-16) and `PARTIAL` (EXP-26) are
  already outside the enum — 4 pre-existing contract-test subtest failures. Governance
  §24 defines `RESULT: PASS / BLOCKED / PARTIAL`. `scripts/registry_to_reladraw.py`
  `STATUS_ORDER` already renders `PARTIAL` and `HOLD` columns (mobile views exist).
  The schema is a contract and must not change in CP-07.
- The builder's target-results source role (`experiment_results` → `RESULTS.md`) already
  parses `## Next authorized action`, `## Known limitations / blockers`,
  `## Per-pattern disposition` — the missing piece is only that EXP-22 has no
  `RESULTS.md` yet and the registry entry was never updated after the run.

**Exact gap:** the registry EXP-22 entry (`status: PLANNED`, pre-run `next_action`) and
the absent `experiments/exp-22-colibri-local-inference/RESULTS.md`. Both are fixable
through the existing registry/results path. Registry + RESULTS **can** represent the
current state (`RESULT: PARTIAL`, `RECOMMENDATION: HOLD`, executed CP-01…CP-03,
released-weights limitation, next authorized action) without any change to bootstrap
source semantics — so CP-07 does **not** stop, and no new source role is added.
