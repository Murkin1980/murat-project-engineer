# EXP-29 — Results: Arena Bootstrap Harness

- RESULT: **PASS**
- Adoption: **PASS / REUSE_COMPONENT** — reuse the derived-packet pattern for
  context-heavy Arena tasks; the harness stays experiment-scoped
- Primary disposition (per `ARENA_TASK.md`): **REUSE_COMPONENT**
- Run date: 2026-10-09 (UTC)
- Branch: `arena/19fa71aa-murat-project-engineer` (base `bb6f1f85fde993c0b698f7036df2699961ed1478`)
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
| fresh-session comparison | CP-03 Arm A vs Arm B (84.94% fewer bytes, 7→1 tool ops, identical answers) |
| no second source of truth | canonical sources digest-identical before/after; only derived artifacts written; packet declares itself non-authoritative |
| no new runtime/service/database | stdlib-only builder; no daemon/scheduler/store; workers are one-shot processes |
| measurable reduction in rediscovery/context/tool overhead | Arm A 5 files / 84,900 B / 7 ops → Arm B 1 file / 12,782 B / 1 op |
| no governance weakening | no file under `scripts/`, `contracts/`, `gates/`, `docs/`, `skills/`, `experts/`, `playbooks/`, `teams/` modified; scope stop rules unchanged and embedded in the packet |

Reuse boundary (per EXP-28 promotion rule): the packet pattern is reusable
for **context-heavy** Arena tasks via the documented builder command. Lesson
scopes stay as recorded (R1 PROJECT, R2 TASK, R3 NO_CHANGE); no lesson was
promoted to GLOBAL, and no automatic learning, packet auto-generation, or
runtime integration is authorized by this result.

## Measurements (required list)

| Metric | Value |
|---|---|
| Packet size | 12,808 B JSON / 10,231 B MD |
| Arm A context (total) | 5 files / 84,900 B / 7 tool ops |
| Arm B context (total) | 1 file / 12,782 B / 1 tool op |
| Reduction (total) | 84.94% fewer bytes; 5→1 files; 7→1 tool ops |
| Reduction (before first useful action) | 82.30% fewer bytes; 4→1 files; 6→1 tool ops |
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
| `experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py` | new — CP-02 deterministic builder + fail-closed verifier + CLI |
| `experiments/exp-29-arena-bootstrap-harness/harness/fresh_session.py` | new — CP-03 isolated Arm A / Arm B workers |
| `experiments/exp-29-arena-bootstrap-harness/harness/exp29_proof.py` | new — CP-02…CP-04 proof harness |
| `experiments/exp-29-arena-bootstrap-harness/ARENA_CONTEXT.json` | new — generated derived packet (fixture EXP-27/CP-05) |
| `experiments/exp-29-arena-bootstrap-harness/ARENA_CONTEXT.md` | new — generated derived launch brief |
| `experiments/exp-29-arena-bootstrap-harness/RESULTS.md` | new — this report |
| `experiments/exp-29-arena-bootstrap-harness/README.md` | status PLANNED → executed/closed |
| `experiments/exp-29-arena-bootstrap-harness/evidence/*` | new — proof evidence (cp02/cp03/cp04/proof_run JSON) |
| `tests/test_exp29_bootstrap.py` | new — 17 EXP-29 proof tests |
| `experiments/EXPERIMENT_REGISTRY.json` | EXP-29 entry closed as `PASS` with evidence links |
| `experiments/exp-19-shirman-trend-intake/cp02/**`, `dashboard/public/registry/**` | regenerated with the repository's documented Reladraw ritual (required by the registry change; clears the pre-existing stale-view failures for the queued EXP-29 entry) |

No file under `scripts/`, `contracts/`, `gates/`, `docs/`, `skills/`, `experts/`,
`playbooks/`, `teams/`, `AGENTS.md`, `STATUS.md`, or `wrangler.jsonc` was
modified. EXP-27 and EXP-28 experiment directories were not modified.

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

## Known limitations / blockers

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

## Next authorized action

None inside this experiment — **STOP after CP-05** per `ARENA_TASK.md`. The PR
is opened but must not be merged as part of EXP-29. Reuse path for a future
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
