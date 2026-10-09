# EXP-29 — Results: Arena Bootstrap Harness

- RESULT: **PASS**
- Adoption: **PASS / REUSE_COMPONENT** — reuse the derived-packet pattern for
  context-heavy Arena tasks; the harness stays experiment-scoped
- Primary disposition (per `ARENA_TASK.md`): **REUSE_COMPONENT**
- Run date: 2026-10-09 (UTC)
- Branch: `arena/19fa71aa-murat-project-engineer` (base `bb6f1f85fde993c0b698f7036df2699961ed1478`)
- Commit: `6c6a592` (+ one follow-up commit recording the PR link and regenerating the packet digest)
- PR: https://github.com/Murkin1980/murat-project-engineer/pull/65 — **opened, not merged**
- Start condition: owner explicitly started EXP-29 after EXP-20 was completed
  (registry: EXP-20 `PASS`, updated 2026-10-09)
- No new repository, memory service, vector store, daemon, scheduler,
  persistent agent runtime, Router change, governance change, automatic
  learning, or second source of truth. The only generated artifacts are the
  derived `ARENA_CONTEXT.json` / `ARENA_CONTEXT.md`.

Every number below is produced by `harness/exp29_proof.py` and stored in
`evidence/` (`proof_run.json` is the aggregate; `cp02.json`, `cp03.json`,
`cp04.json`, `proof_run_full.json`; the run also rewrites the committed derived
artifacts deterministically).

Reproduce:

```bash
python3 experiments/exp-29-arena-bootstrap-harness/harness/exp29_proof.py all
python3 -m unittest tests.test_exp29_bootstrap -v
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
    verify --packet experiments/exp-29-arena-bootstrap-harness/ARENA_CONTEXT.json
```

## CP-01 — Existing capability map: COMPLETE

Full map: `CAPABILITY_MAP.md` (`need → existing MPE component → reusable? →
gap → decision`, 15 rows). Summary of dispositions:

| Need | Existing component | Decision |
|---|---|---|
| Task genealogy/context packet | EXP-27 CP-02 `build_packet` + isolated fresh worker (closed) | **EXTEND** (pattern extended inside EXP-29; EXP-27 untouched) |
| Graceful handoff contract | `AGENTS.md` + `contracts/HANDOFF.md`; proven by EXP-27 CP-04 | **KEEP_EXISTING** + **REUSE** (fields parsed into RULES) |
| Source digests | EXP-27 `run_state.sha256_file` pattern | **REUSE** (stdlib helper reimplemented locally, no cross-experiment import) |
| Experiment registry | `experiments/EXPERIMENT_REGISTRY.json` (canonical) | **KEEP_EXISTING** + **REUSE** as packet source |
| Status / nearest action | `STATUS.md` | **KEEP_EXISTING** + **REUSE** as packet source |
| Task-local instructions | per-experiment `ARENA_TASK.md` / `README.md` | **KEEP_EXISTING** + **REUSE** as packet source |
| Accepted lessons | EXP-28 `RESULTS.md` R1/R2/R3 (evidence-gated) | **REUSE** — parsed at build time; scope is this experiment's recorded promotion decision |
| Reusable components | EXP-27 `RESULTS.md` per-pattern disposition table | **REUSE** — parsed at build time |
| Known traps | EXP-27 `RESULTS.md` known limitations | **REUSE** — parsed at build time |
| Fail-closed evidence trust | `scripts/validate_package.py` evidence-trust boundary | **REUSE** (verifier is fail-closed) |
| Progressive disclosure | `context/CONTEXT_MAP.md`, `context/project-context.md` | **KEEP_EXISTING** (consistent; binding §2 priority embedded instead) |
| Runtime coordination helpers | `scripts/runtime_coordination.py` | **KEEP_EXISTING** (not needed; unmodified) |
| Memory service / vector DB / lesson store | EXP-15 (PASS, validated), EXP-QOOPIA (RETIRED) | **REJECT_DUPLICATE** (would duplicate validated memory work and become a second source of truth) |
| Automatic lesson/rule promotion | none (EXP-28 R3 rejected it) | **REJECT_DUPLICATE** (on the EXP-29 stop list) |
| Second registry / lesson index | `EXPERIMENT_REGISTRY.json`, EXP-28 `RESULTS.md` | **REJECT_DUPLICATE** (parse canonical files; cite path + sha256) |

CP-01 PASS: every need is covered by KEEP_EXISTING/REUSE/EXTEND of existing
components; no memory subsystem is necessary, so `DEEP_CHANGE_REQUIRED` does
not trigger.

## CP-02 — Deterministic bootstrap builder: PASS

`harness/bootstrap_builder.py` (stdlib only, no network, no LLM, no wall-clock,
no persistent store):

- `build_packet(root, experiment_id, checkpoint, git refs)` derives the packet
  from 8 canonical sources: experiment registry, the target experiment's
  `ARENA_TASK.md` / `README.md` / `RESULTS.md`, `STATUS.md`, `AGENTS.md`,
  `docs/governance/SCOPE-CHANGE-CONTROL.md`, and EXP-28 `RESULTS.md`
  (accepted lessons).
- Determinism: two builds with identical inputs are byte-identical (JSON and
  markdown); `generated_against` git refs are inputs and are excluded from the
  freshness gate.
- Provenance: every packet item is source-linked; `source_refs` records the
  SHA-256 of every canonical source (8 refs, all verified).
- The only files the builder writes are the two derived artifacts named on the
  command line; canonical sources are read-only (digest-identical before/after
  the full proof run).
- `verify_packet` is fail-closed: FRESH only when every source digest matches
  AND the packet equals a deterministic rebuild from current sources;
  otherwise STALE (degrade to a non-authoritative hint) or REJECTED (safety
  invariant violated). CLI exit codes: 0 FRESH / 2 STALE / 3 REJECTED.

### Packet schema/fields (`exp-29-arena-context-v1`)

| Field | Content |
|---|---|
| `packet_version`, `authority`, `authority_note` | `DERIVED_VIEW_NON_AUTHORITATIVE` + Git-wins disclaimer |
| `generated_against` | git branch/head/base (informational; excluded from freshness gate) |
| `now` | project, parent goal, experiment id/name/path, checkpoint chain, disposition, task id, registry status/updated_at, nearest action |
| `rules` | task stop rules (+intro, +source), deep-change gate bullets (governance §6), source-of-truth priority (§2), graceful-handoff fields (`AGENTS.md`) |
| `known_lessons` | EXP-28 R1/R2/R3 with `scope` (PROJECT/TASK/NO_CHANGE), `scope_basis`, minimal change, verification, source anchor |
| `reusable_components` | EXP-27 per-pattern rows (pattern, verdict, disposition, source) |
| `known_traps` | EXP-27 known-limitations bullets (source-linked) |
| `resume` | status, result summary (truncated), next action, next authorized action, evidence pointer |
| `source_refs` | path + sha256 + role for all 8 canonical sources |
| `verification` | verify command, freshness rule, safety invariants |

Generated artifacts: `ARENA_CONTEXT.json` (12,808 B, machine-readable) and
`ARENA_CONTEXT.md` (10,231 B, human-readable launch brief) — committed as the
derived evidence for the frozen fixture; regenerate for any task with
`bootstrap_builder.py build --experiment <ID> --checkpoint <CP>`.

## CP-03 — Fresh-session A/B comparison: PASS

> **Byte figures in this section are superseded by CP-06.** They were measured
> on the EXP-27 packet before CP-06 regenerated it. Current values: Arm A
> 84,978 B / 7 ops, Arm B 13,087 B / 1 op, 84.60% reduction. See the CP-06
> section. The original values are kept below as the CP-03 record.

Fixture: **EXP-27 @ CP-05** — a real, already completed context-heavy MPE task
(registry entry + `ARENA_TASK.md` + `README.md` + `RESULTS.md` must be
rediscovered by a fresh session). Both arms run as isolated `python3 -I`
workers with a temporary working directory; neither sees the chat
(`read_from_chat = false`) and neither performs writes.

| Metric | Arm A — normal rediscovery | Arm B — bootstrap packet |
|---|---:|---:|
| Files read (total) | 5 (STATUS, README, registry, ARENA_TASK, RESULTS) | **1** (the packet) |
| Context bytes read (total) | 84,900 B | **12,782 B** |
| Tool calls / traced ops (total) | 7 (5 reads + 2 directory listings) | **1** (1 read) |
| Wrong/failed paths | 0 failed reads; 1 redundant read (STATUS) + 2 exploration listings | 0 |
| Files before first useful action (genealogy + stop conditions) | 4 files / 72,217 B / 6 ops | **1 file / 12,782 B / 1 op** |
| Rediscovery steps | 7 discovery ops to reconstruct the context | 0 (packet handed over after a FRESH verify) |
| Answers (11 questions) | all correct | all correct |

- Reduction: **84.94% fewer context bytes** (total) and **82.30% fewer bytes
  before the first useful task action**; files 5→1 (4→1 before first useful
  action); tool calls 7→1 (6→1). This is a measured retrieval-cost proxy
  (bytes/files/tool ops in isolated deterministic workers), **not** a wall-clock
  or human-time claim.
- Correctness: both arms answer all 11 questions identically (project, parent
  goal, experiment path, checkpoint chain, disposition, 9 stop rules, result
  status, next action, reusable component, known trap, next authorized action);
  fixture facts independently hardcoded in the tests match; task genealogy and
  stop conditions are reproduced correctly in both arms.
- Packet consistency: `verify` returned FRESH before the arms (all 8 source
  digests match; packet equals a rebuild from current canonical sources).
- Arm A trace (rediscovery order a careful executor follows):
  `STATUS.md` → listdir `experiments/` → listdir experiment dir → `README.md`
  → `EXPERIMENT_REGISTRY.json` → `ARENA_TASK.md` → `RESULTS.md`.

Comparison with the reused evidence: EXP-27 CP-02 measured a 2,164.5 B
single-layer genealogy packet vs a 46,542.5 B scan (95.35% fewer bytes). The
EXP-29 packet is larger (12.8 KB) because it carries all six required layers,
and the Arm A baseline is larger for the same reason; the direction and
mechanism agree with EXP-27/EXP-28.

## CP-04 — Stale/unsafe packet negative controls: PASS (all six fail closed)

All mutations happen on temp copies; the repository is never touched
(canonical-source digests identical before/after the whole proof).

| # | Control | Setup | Expected | Observed |
|---|---|---|---|---|
| NC-01 | canonical source changed after packet generation | mirrored sources; `STATUS.md` modified post-build | STALE | **STALE** (`source_digest_mismatch:STATUS.md`) |
| NC-02 | source digest mismatch | one `source_refs` sha256 replaced | STALE | **STALE** (`source_digest_mismatch`) |
| NC-03 | missing critical stop/deep-change rule | `rules.stop_rules` emptied | REJECTED | **REJECTED** (`missing_stop_rules`); fresh-session worker also refuses |
| NC-04 | stale NEXT ACTION | mirrored registry; EXP-27 `next_action` changed post-build | STALE | **STALE**; field diff names `now.nearest_action` / `resume.next_action` |
| NC-05 | packet attempts to override canonical Git source | deep-change bullet rewritten to contradict governance | not FRESH | **STALE**; field diff on `rules.deep_change_gate.bullets[0]`; disposition degrades to non-authoritative hint |
| NC-06 | task-local lesson incorrectly promoted as GLOBAL | R2 (TASK, EXP-24 Phase 2 only) relabelled GLOBAL | REJECTED | **REJECTED** (`lesson_promoted_to_global_without_canonical_marker:R2`); fresh-session worker also refuses |

Expected outcome per `ARENA_TASK.md` — the packet is rejected, flagged stale,
or degraded to a non-authoritative hint; it never silently overrides canonical
files. Additionally: GLOBAL lesson scope requires a `PROMOTED_TO_GLOBAL` marker
in the canonical lesson source (no current source has one), the worker
fail-closed refuses packets missing the authority disclaimer / stop rules /
deep-change gate, and workers perform only read/listdir operations (no writes).

## CP-05 — Adoption decision: PASS / REUSE_COMPONENT

PASS criteria from `ARENA_TASK.md`:

| Criterion | Evidence |
|---|---|
| deterministic packet generation | byte-identical rebuilds (CP-02, test `test_builder_is_deterministic`) |
| source-linked provenance | 8 source refs, all digests verified; every layer item source-linked |
| stale-packet detection | NC-01/02/04 → STALE with reasons and field diffs |
| fresh-session comparison | CP-03 Arm A vs Arm B (84.94% fewer bytes, 7→1 tool ops, identical answers) — *byte figure superseded by CP-06: 84.60%* |
| no second source of truth | canonical sources digest-identical before/after; only derived artifacts written; packet declares itself non-authoritative |
| no new runtime/service/database | stdlib-only builder; no daemon/scheduler/store; workers are one-shot processes |
| measurable reduction in rediscovery/context/tool overhead | Arm A 5 files / 84,900 B / 7 ops → Arm B 1 file / 12,782 B / 1 op — *superseded by CP-06: 84,978 B → 13,087 B* |
| no governance weakening | no file under `scripts/`, `contracts/`, `gates/`, `docs/`, `skills/`, `experts/`, `playbooks/`, `teams/` modified; scope stop rules unchanged and embedded in the packet |

Reuse boundary (per EXP-28 promotion rule): the packet pattern is reusable
for **context-heavy** Arena tasks via the documented builder command. Lesson
scopes stay as recorded (R1 PROJECT, R2 TASK, R3 NO_CHANGE); no lesson was
promoted to GLOBAL, and no automatic learning, packet auto-generation, or
runtime integration is authorized by this result.

## CP-06 — First real-use repair (H-1 / H-2 / H-3): PASS

Trigger: the first real-use bootstrap for EXP-22/CP-01 returned `REJECTED`
(`missing_stop_rules`) with matching source digests. Evidence:
`experiments/exp-22-colibri-local-inference/evidence/bootstrap/FIRST_REAL_USE.md`.
Scope is limited to the three confirmed harness defects in `ARENA_TASK.md`
(section CP-06, owner-authorized).

Provenance note: the earlier repair commit `2ae7ad3` referenced by the
authorization is absent locally, on the remote and on GitHub. The repair was
therefore rebuilt on this branch from the defect evidence, not from a recovered
diff.

### Reproduction (before editing)

All three defects were reproduced on the committed refused EXP-22 packet and on
`main` 4b3dd35:

| Defect | Reproduced as | Cause in the pre-repair builder |
|---|---|---|
| H-1 | `stop_rules` = 0 → `REJECTED` `missing_stop_rules` | `_parse_stop_rules` matched only `## Stop conditions` / `## Scope stop rules`. EXP-22 declares `## Boundaries` (ARENA_TASK.md) and `## Failure / stop criteria` / `## Guardrails` (README.md). |
| H-2 | EXP-22 markdown says `REUSABLE COMPONENTS (from EXP-27 RESULTS.md)` and `KNOWN TRAPS (… EXP-27 RESULTS.md)` | Labels hardcoded in `render_markdown`. EXP-22 has no RESULTS.md. |
| H-3 | `checkpoints` = `[]`, `disposition` = `''` | `_parse_checkpoints` and `_parse_disposition` read ARENA_TASK.md only. EXP-22 declares CP-01..03 and `Decision: EXPERIMENT` in README.md. |

### Repair (smallest targeted change; no new parser layer, store, or source of truth)

- **H-1 stop rules.** Union over recognised `##` boundary sections, ARENA_TASK.md
  first, then README.md. Recognised titles: Stop conditions, Scope stop rules,
  Stop rules, Deep-change stop conditions, Failure / stop criteria, Boundaries,
  Guardrails. `## Completion boundary` is excluded because it states the finish
  line, not a stop rule. Inside `## Boundaries` only the `Not allowed:` bullets
  are rules; `Allowed:` lists are permissions and never become rules. Exact
  duplicates are removed. `stop_rules_source` lists every contributing section
  as `<path>#<anchor>`. The `^STOP` line fallback runs only when no section
  yields rules. Zero rules still gives `REJECTED`, so prose-only boundaries stay
  fail-closed.
- **H-2 labels.** Section labels come from the packet's own `source_refs` roles
  (`experiment_results`, `accepted_lessons`). With no experiment RESULTS.md the
  label says so: `(no experiment RESULTS.md present)`. Empty lists print
  `- (none parsed)`.
- **H-3 genealogy.** Checkpoint chain: union over ARENA_TASK.md then README.md,
  in first-appearance order. Disposition: first declared value, with every
  declared value kept in the new `now.disposition_sources` (`{path, value}`).
  Differing non-empty values give `REJECTED` `ambiguous_disposition` (verify check
  `disposition_unambiguous`). The Arm B worker refuses the same packet by
  mirroring that check; it has no separate parsing logic.
- **Schema changes are additive only:** `now.disposition_sources`, the composite
  `rules.stop_rules_source`, the `ambiguous_disposition` reason, and the
  `disposition_unambiguous` check. No canonical file was modified.

### Before / after: same case (EXP-22/CP-01)

| Measure | Before (recorded run) | After (CP-06, rebuilt from current Git) |
|---|---|---|
| Verdict | `REJECTED`, `missing_stop_rules` | `FRESH`, no reasons; all 7 checks true |
| Stop rules | 0 | 25: `ARENA_TASK.md#boundaries` 8, `README.md#failure-stop-criteria` 7, `README.md#guardrails` 10 |
| Checkpoint chain | `[]` | CP-01 → CP-02 → CP-03 |
| Disposition | `''` | `EXPERIMENT` (README.md; one declaration, no conflict) |
| Markdown labels | EXP-27 names on an EXP-22 packet | `(no experiment RESULTS.md present)`, derived |
| Packet size | 8,097 B JSON / 6,907 B MD (refused) | 9,802 B JSON / 8,302 B MD |
| Startup reads | 9 files / 134,732 B / 16 tool ops, as recorded in FIRST_REAL_USE.md (includes diagnostic reads of harness code) | 4 files / 28,339 B: the packet plus 3 canonical files it cannot replace (see *Remaining rediscovery*) |
| Startup reads without any packet | not measured | 4 files / 71,163 B (STATUS.md, EXP-22 README, registry, EXP-22 ARENA_TASK) |

Basis: the "after" figures are computed from the bytes of the files a fresh
executor needs, the same retrieval-cost proxy as CP-03. The "before" figures are
the recorded run. Its 16 tool operations include builds, verifications and
harness reads, so the two tool-operation counts are not comparable. No
wall-clock or human-time saving is claimed.

Evidence: `experiments/exp-22-colibri-local-inference/evidence/bootstrap/cp06/`
(ARENA_CONTEXT.json / .md, and `verify.json` = `FRESH`, exit 0) and
`evidence/cp06.json` for the proof step. The refused pre-repair packet and its
verify output are kept unchanged for audit.

### Regression coverage (`Exp29RealUseRepairTests`, 9 tests)

Fixtures are EXP-22-shaped: `Allowed:` / `Not allowed:` lists, README
`Decision:`, CP-01..03, `Failure / stop criteria`, `Guardrails`, and no
RESULTS.md, built on real copies of the shared canonical sources (STATUS,
AGENTS, governance SCOPE-CHANGE-CONTROL, EXP-28 RESULTS).

To confirm the tests detect the defects, they were also run against the
pre-repair builder (committed `HEAD`, exported with `git archive` to a temp
directory). Seven of nine fail there. The two that pass are the deliberate
fail-closed guards: prose-only and Allowed-only boundaries must still produce no
rules.

| Test | Covers | Pre-repair builder | After CP-06 |
|---|---|---|---|
| `test_h1_boundary_sections_yield_stop_rules_and_verify_fresh` | H-1 | FAIL | PASS |
| `test_h1_prose_only_boundaries_stay_fail_closed` | H-1 guard | PASS | PASS |
| `test_h1_allowed_list_alone_is_not_a_stop_rule` | H-1 guard | PASS | PASS |
| `test_h2_labels_describe_the_actual_sources_when_no_results_exist` | H-2 | FAIL | PASS |
| `test_h2_labels_name_the_experiment_results_when_present` | H-2 | FAIL | PASS |
| `test_h3_checkpoint_chain_and_disposition_come_from_the_readme` | H-3 | FAIL | PASS |
| `test_h3_conflicting_disposition_is_rejected_not_silently_resolved` | H-3 (verifier and worker refuse) | FAIL | PASS |
| `test_exp22_cp01_bootstrap_is_fresh_from_live_git_sources` | real-use case | FAIL | PASS |
| `test_exp27_fixture_rules_genealogy_and_labels_are_preserved` | EXP-27 fixture | FAIL | PASS |

### Six negative controls (CP-04 re-run)

| Control | Mutation | Expected | Observed |
|---|---|---|---|
| NC-01 | canonical source changed after packet generation | STALE | STALE |
| NC-02 | source digest mismatch inside the packet | STALE | STALE |
| NC-03 | missing critical stop/deep-change rule | REJECTED | REJECTED (`missing_stop_rules`) |
| NC-04 | stale NEXT ACTION in the packet | STALE | STALE |
| NC-05 | packet attempts to override canonical Git source | STALE | STALE |
| NC-06 | task-local lesson promoted to GLOBAL | REJECTED | REJECTED |

All six still fail closed: 4 STALE, 2 REJECTED, same as CP-04.

### EXP-27 fixture status

- **Before CP-06:** the committed `ARENA_CONTEXT.json` was `STALE`
  (`source_digest_mismatch:AGENTS.md`). PR #66 changed AGENTS.md after the packet
  was generated. This was not a builder defect.
- **After CP-06:** regenerated, and verified `FRESH` (exit 0). Still 9 stop
  rules, checkpoints CP-01..05, disposition `REUSE_COMPONENT`. The stop-rule
  source is now `README.md#stop-conditions`, and the markdown labels are
  path-derived with the same EXP-27 wording.
- The diff against the previous committed packet is limited to: `generated_against`
  (informational git refs), the additive `now.disposition_sources`, the
  `stop_rules_source` anchor, the AGENTS.md digest refresh (`1ac7688b…` →
  `d440af35…`), and the markdown labels. The packet grew by 305 B (12,808 →
  13,113 B), from the additive field.

### CP-03 byte figures: superseded

The CP-03 A/B byte figures were measured on the pre-CP-06 EXP-27 packet. The same
CP-03 comparison, re-run after regeneration, gives Arm A 5 files / 84,978 B /
7 ops, Arm B 1 file / 13,087 B / 1 op, and a 84.60% reduction (previously 84.94%).
Answers, fixture facts and the nine stop rules are identical in both arms. The
original numbers stay in this file as the CP-03 record and are marked superseded
where they appear.

### Remaining EXP-22 startup rediscovery (not closed by CP-06)

The packet is FRESH, but it is not sufficient to start EXP-22 on its own:

- `experiments/exp-22-colibri-local-inference/README.md`: the CP-01 acceptance
  text. The packet has no checkpoint-scope layer. 4,566 B.
- `ARENA_TASK.md`: mission, required order and evaluation. The packet carries only
  its boundary rules. 3,903 B.
- `FINDINGS.md`: the recorded EXP-22 state. 10,068 B. The registry (updated
  2026-10-06) and the packet still say `PLANNED`, with "execute CP-01" as the
  nearest action. FINDINGS.md (2026-10-09) records CP-01..03 as run, with
  structural PASS and routing quality OPEN. A fresh executor that reads only the
  packet would repeat CP-01. FINDINGS.md is not one of the packet's source roles,
  and EXP-22 has no RESULTS.md that could carry the same state.

Extra rediscovery is therefore still necessary: 3 files / 18,537 B on top of the
packet. Carrying FINDINGS-level state would need a new source role or an
owner-side RESULTS.md for EXP-22. Neither is implemented here.

## Measurements (required list)

> Byte and packet-size rows below are the CP-05 record. They are superseded by the CP-06 values (Arm A 84,978 B / 7 ops; Arm B 13,087 B / 1 op; 84.60%; committed JSON 13,113 B). See the CP-06 section.

| Metric | Value |
|---|---|
| Packet size | 12,808 B JSON / 10,231 B MD (superseded: 13,113 B JSON after CP-06) |
| Arm A context (total) | 5 files / 84,900 B / 7 tool ops (superseded: 84,978 B) |
| Arm B context (total) | 1 file / 12,782 B / 1 tool op (superseded: 13,087 B) |
| Reduction (total) | 84.94% fewer bytes; 5→1 files; 7→1 tool ops (superseded: 84.60%) |
| Reduction (before first useful action) | 82.30% fewer bytes; 4→1 files; 6→1 tool ops (superseded by CP-06 re-run; see CP-06) |
| Rediscovery steps | Arm A 7 discovery ops; Arm B 0 |
| Answers correct / identical | 11/11 questions, both arms, fixture facts match |
| Stop conditions reproduced | 9/9 rules, both arms |
| Negative controls fail-closed | 6/6 (4 STALE, 2 REJECTED) |
| Canonical sources modified | 0 (digests identical before/after) |
| Derived artifacts written | 2 (`ARENA_CONTEXT.json`, `ARENA_CONTEXT.md`) |
| New dependencies / services / daemons / DBs | 0 / 0 / 0 / 0 |
| Wall-clock savings claimed | none (retrieval-cost proxy only) |
| VRU claim | none — bounded proof, not a real user workflow |

## Files changed

| Path | Change |
|---|---|
| `experiments/exp-29-arena-bootstrap-harness/CAPABILITY_MAP.md` | new — CP-01 capability map |
| `experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py` | new — CP-02 deterministic builder + fail-closed verifier + CLI; CP-06 modified (H-1/H-2/H-3 repair, `ambiguous_disposition` refusal) |
| `experiments/exp-29-arena-bootstrap-harness/harness/fresh_session.py` | new — CP-03 isolated Arm A / Arm B workers; CP-06 modified (Arm B also refuses `ambiguous_disposition`) |
| `experiments/exp-29-arena-bootstrap-harness/harness/exp29_proof.py` | new — CP-02…CP-04 proof harness; CP-06 adds the `cp06` step to the CLI and `run_all` |
| `experiments/exp-29-arena-bootstrap-harness/ARENA_CONTEXT.json` | new — generated derived packet (fixture EXP-27/CP-05); CP-06 regenerated it (was STALE, now FRESH) |
| `experiments/exp-29-arena-bootstrap-harness/ARENA_CONTEXT.md` | new — generated derived launch brief |
| `experiments/exp-29-arena-bootstrap-harness/RESULTS.md` | new — this report; CP-06 section and supersession notes added |
| `experiments/exp-29-arena-bootstrap-harness/README.md` | status PLANNED → executed/closed |
| `experiments/exp-29-arena-bootstrap-harness/evidence/*` | new — proof evidence (cp02/cp03/cp04/proof_run JSON); CP-06 regenerated cp02/cp03/cp04/proof_run/proof_run_full and added `cp06.json` |
| `tests/test_exp29_bootstrap.py` | new in CP-02…CP-04 (17 tests); CP-06 adds class `Exp29RealUseRepairTests` (9 tests) — 26 total |
| `experiments/EXPERIMENT_REGISTRY.json` | EXP-29 entry closed as `PASS` with evidence links |
| `experiments/exp-19-shirman-trend-intake/cp02/**`, `dashboard/public/registry/**` | regenerated with the repository's documented Reladraw ritual (required by the registry change; clears the pre-existing stale-view failures for the queued EXP-29 entry) |

No file under `scripts/`, `contracts/`, `gates/`, `docs/`, `skills/`, `experts/`,
`playbooks/`, `teams/`, `AGENTS.md`, `STATUS.md`, or `wrangler.jsonc` was
modified. EXP-27 and EXP-28 experiment directories were not modified. CP-06 also
adds `experiments/exp-22-colibri-local-inference/evidence/bootstrap/cp06/` (generated
EXP-22 bootstrap evidence; the EXP-22 README, ARENA_TASK, FINDINGS and Colibri
conclusions are unchanged) and leaves `experiments/EXPERIMENT_REGISTRY.json` and the
reladraw outputs unchanged.

## Checks run

| Check | Command | Result |
|---|---|---|
| EXP-29 proof harness | `python3 …/harness/exp29_proof.py all` | exit 0, `summary.result = PASS` (CP-02/03/04 PASS, 6/6 controls) |
| EXP-29 proof tests | `python3 -m unittest tests.test_exp29_bootstrap -v` | 17 tests — OK |
| Full unittest suite, before EXP-29 edits | `PYTHONHASHSEED=0 python3 -m unittest discover -s tests` | 398 tests — 15 failures, 1 skipped (all pre-existing: 4 registry-status schema mismatches, 3 missing mobile-status views, 8 stale dashboard views for the queued EXP-29 entry) |
| Full unittest suite, after EXP-29 edits | same | 415 tests — 7 failures, 1 skipped; the 7 are the known pre-existing registry-status schema mismatches and missing mobile-status references; the 8 stale-view failures are cleared by the documented Reladraw ritual; **no new failure** |
| Package validator | `python3 scripts/validate_package.py .` | VALIDATION PASSED |
| Whitespace check | `git diff --check` | PASS |
| Secrets check | grep for token/key patterns over changed files | no matches (no credentials added) |
| Scope check | `git diff --name-only` vs allowed set | only `experiments/exp-29-arena-bootstrap-harness/**`, `tests/test_exp29_bootstrap.py`, `experiments/EXPERIMENT_REGISTRY.json`, and the documented Reladraw ritual outputs |
| Dashboard build/deploy checks | `npm run build` + `npm run check` | exit 0; ALL CHECKS PASSED |

### CP-06 gate results (final tree)

| Gate | Command | Result |
|---|---|---|
| EXP-22/CP-01 bootstrap = FRESH | `bootstrap_builder.py build --experiment EXP-22 --checkpoint CP-01`, then `verify --json` | exit 0, `FRESH`, no reasons, all checks true (`evidence/bootstrap/cp06/verify.json`) |
| H-1 / H-2 / H-3 regression tests | `python3 -m unittest tests.test_exp29_bootstrap` | 26 tests, OK (9 new; 7 of them fail on the pre-repair builder) |
| Six negative controls fail closed | `exp29_proof.py all --workdir /tmp/exp29-work` | NC-01..06 pass: 4 STALE, 2 REJECTED; `summary.result = PASS` |
| EXP-27 fixture passes | `bootstrap_builder.py verify --packet ARENA_CONTEXT.json` | exit 0, `FRESH` (was STALE on `main`) |
| Full unit suite | `PYTHONHASHSEED=0 python3 -m unittest discover -s tests` | 424 tests, 1 skipped, 7 failures: exactly the pre-existing set (4 registry-status schema, 3 dashboard mobile views). The 2 EXP-29 stale-packet failures are cleared. No new failure. |
| Package validator | `python3 scripts/validate_package.py .` | VALIDATION PASSED (first run on this baseline) |
| Whitespace | `git diff --check`, plus whitespace check of new files | clean |
| Scope | `git diff --name-only 4b3dd35` plus untracked files | 17 files, all in the allowed paths (`experiments/exp-29-arena-bootstrap-harness/**`, `experiments/exp-22-colibri-local-inference/evidence/bootstrap/cp06/**`, `tests/test_exp29_bootstrap.py`) |
| Secrets | pattern scan (tokens, keys, private keys, password/secret assignments) over the 17 changed files | 0 hits; positive control matched |

## Known limitations / blockers

- **CP-06 — prose STOP sentences are not parsed.** EXP-22's
  `## Before changing code` section contains "If a deep-change is required, STOP
  and report it." That section is not a recognised boundary title, so the
  sentence is not in the packet. The deep-change trigger is still carried by the
  packet's deep-change gate (SCOPE-CHANGE-CONTROL §6).
- **CP-06 — boundary titles are an explicit list** (`STOP_SECTION_TITLES`). A
  boundary under any other heading is not captured. If other recognised sections
  still yield rules, the packet can be FRESH while omitting it. Adding a title is
  a deliberate, reviewed change.
- **CP-06 — every `## Guardrails` bullet is a rule, preferences included** (for
  example "Prefer a small supported MoE model for the first run"). Over-inclusion
  is the fail-safe direction: more constraints are carried, never fewer.
- **CP-06 — union is not reconciliation.** Rules from different sections are all
  carried, with anchors. Contradictory wording between them is not detected.
- **CP-06 — disposition conflicts are checked only between ARENA_TASK.md and
  README.md.** The registry result text is not compared with the disposition.
- **CP-06 — FRESH is not complete startup.** The EXP-22 packet is FRESH but lacks
  the CP-01 acceptance text, ARENA_TASK's mission/order/evaluation, and the
  FINDINGS.md state. See *Remaining EXP-22 startup rediscovery* in CP-06.
- **CP-06 — point-in-time EXP-22 packet.** `evidence/bootstrap/cp06/` becomes
  STALE when EXP-22 sources change, by design. The live test builds from current
  sources and does not depend on that file.
- **Pre-existing, not changed:** the EXP-29 README top line `Status: PLANNED`
  predates CP-05; the registry and this file say PASS. CP-06 does not own that
  line, so it was left as is.
- **Registry not updated for CP-06.** The EXP-29 registry entry still describes
  the CP-05 close. Updating it needs the Reladraw regeneration of
  `dashboard/public/registry/**` and `exp-19 cp02`, which the CP-06 gate did not
  require.
- The A/B comparison is a **retrieval-cost proxy** (bytes/files/tool ops counted
  in isolated deterministic workers). No wall-clock, token, or human-time
  savings are claimed; a real Arena session also spends turns on planning.
- One frozen fixture (EXP-27). EXP-27 CP-02 additionally verified EXP-25 with
  the same single-layer pattern; the six-layer packet was exercised on one
  fixture, so generality across task shapes is plausible but not proven.
- The builder parses canonical prose (headings, tables, bullets). A formatting
  change in a canonical source changes its digest and makes existing packets
  STALE — which is the intended fail-closed behaviour, but it means packets
  must be regenerated after any source edit (cheap and deterministic).
- `generated_against` git refs are informational and excluded from the
  freshness gate; freshness is defined purely by source digests + rebuild
  equality.
- The worker refuses any GLOBAL lesson scope outright (it cannot check the
  canonical promotion marker without reading sources); the builder's `verify`
  is the authoritative gate for that invariant.
- The 7 pre-existing unittest failures (registry-status schema mismatches for
  EXP-16/EXP-26/EXP-QOOPIA-MEMORY/EXP-UX-UI-SKILLS and the 3 missing
  mobile-status references in `dashboard/public/index.html`) are recorded, not
  repaired — fixing the status contract is a separate decision (per EXP-28).

## Rollback

EXP-29 touches no production code, contract, gate, or governance file. Rollback
= close the PR without merging and, if ever needed on `main`:
`git revert` of the EXP-29 commits, or delete
`experiments/exp-29-arena-bootstrap-harness/`, restore the EXP-29 registry entry
to `PLANNED`, and re-run the documented Reladraw ritual. The derived
`ARENA_CONTEXT.*` artifacts are regenerable at any time from canonical sources
with the builder command; nothing depends on them.

**CP-06 rollback:** revert the CP-06 commit to restore the pre-repair builder. EXP-22
then returns to `REJECTED` (`missing_stop_rules`), as recorded in FIRST_REAL_USE.md,
and the EXP-27 packet returns to `STALE`, its state on `main` before CP-06. Deleting
`experiments/exp-22-colibri-local-inference/evidence/bootstrap/cp06/` only removes
the point-in-time EXP-22 packet. Nothing outside EXP-29 and that folder depends on
these files.

## Next authorized action

CP-06 (first real-use repair) is complete as a bounded checkpoint. Its PR is
opened and must not be merged as part of this checkpoint. Any follow-up is a
separate owner decision, for example whether the packet should carry EXP-22's
FINDINGS.md state (new source role or owner-side RESULTS.md), or a registry
update.

Earlier status: **STOP after CP-05** per `ARENA_TASK.md`; the CP-05 PR was opened,
not merged. Reuse path for a future
context-heavy Arena task:

```bash
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
    build --experiment <EXP-ID> --checkpoint <CP> \
    --out-json ARENA_CONTEXT.json --out-md ARENA_CONTEXT.md
python3 experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py \
    verify --packet ARENA_CONTEXT.json   # FRESH required before use
```

Any broader adoption (automatic packet generation per session, GLOBAL lesson
promotion, runtime integration) requires a separate owner decision and its own
New Idea Filter / deep-change assessment.
