# EXP-27 — Results: Paperclip orchestration patterns

- RESULT: **PASS**
- Overall adoption: **ADOPT_WITH_CHANGES** (pattern level only, no implementation)
- Primary decision: **REUSE_COMPONENT** — Paperclip stays a donor/reference
- Donor as a system: **DO_NOT_ADOPT**
- Run date: 2026-10-06 (UTC)
- Branch: `arena/13fe2dd8-murat-project-engineer` (base `938f146e`, PR #53 supplies the frozen task/registry entry)
- No new repository, Paperclip service, DB, queue, daemon, Router change, governance replacement,
  source-of-truth change, autonomous execution, or production integration.

Every number below is produced by `harness/mpe_proof.py` and stored in `evidence/`
(`proof_run.json` is the aggregate; per-checkpoint files `cp02.json` … `cp05.json`; raw console log `proof_run.log`).

Reproduce:

```bash
python3 experiments/exp-27-paperclip-orchestration-patterns/harness/mpe_proof.py all
```

## CP-01 — Upstream audit + component map: COMPLETE

- `UPSTREAM_AUDIT.md` — donor pinned at `paperclipai/paperclip@d9f600043f13cf19172da1373d1336a0db31664b`
  (MIT; nearest release `v2026.1005.0 = 467125fa`), with per-path freshness reconciliation and the eight
  audited mechanism areas.
- `COMPONENT_MAP.md` — per-pattern `problem → MPE equivalent → overlap → incremental value → required runtime →
  risk → KEEP/BORROW/ADAPT/REJECT`.

CP-01 PASS: at least one donor pattern offers incremental value with **no** parallel control plane requirement
(goal-ancestry packet; lease conflict semantics; evidence digest/completeness; hard-stop budget semantics).
Duplicate/out-of-scope areas were rejected explicitly (Paperclip-shaped service, DB-backed authority,
Router/approval authority transfer, heartbeat fleets, routines).

## CP-02 — Goal ancestry: PASS

Contract: `project → goal → experiment/checkpoint → task`, with the parent goal preserved and no new canonical source.

| Case | Task node | Packet | Without packet | Result |
|---|---|---|---|---|
| EXP-27 (this experiment) | `EXP-27/CP-05` | 2,316 B, 3 hashed source refs | 3 file reads, 49,584 B | parent goal + all 8 genealogy answers preserved in an isolated fresh process |
| EXP-25 (closed bounded MPE task) | `EXP-25/CP-04` | 2,013 B, 3 hashed source refs | 2 file reads, 43,357 B | same |

- Mean packet size **2,164.5 B** vs. mean rediscovery scan **46,470.5 B / 2.5 file reads**.
- Fresh-process verification used `python3 -I` with a temporary working directory and only the packet file:
  `read_from_chat = false`; every field (`project`, `parent_goal`, `experiment_id`, `checkpoints`, `task_id`,
  `disposition`, `stop_condition_count`, `first_stop_conditions`) matched.
- Independent rediscovery by a second parser reproduced the packet contents (cross-check passes).
- No new canonical source: the packet is a derived view; `source_refs` carry the SHA-256 of
  `experiments/EXPERIMENT_REGISTRY.json` + the experiment `ARENA_TASK.md` / `README.md`.

## CP-03 — Atomic task lease: PASS

File-backed single-host proof; no daemon/DB/queue. Built on the same exclusive-create primitive already used by
`scripts/runtime_coordination.py` (`os.open(..., O_CREAT|O_EXCL)` + atomic replace), plus an explicit
expiry/reclaim/release record that the existing helper deliberately does not provide.

| Measurement | Result |
|---|---|
| Race rounds | 3 |
| Concurrent executor processes per round | 8 |
| Winners per round | exactly 1 |
| Explicit `LEASE_CONFLICT` results | 7 per round (21 total), each carrying current owner + expiry |
| Duplicate executions (work markers) | **0** |
| Daemons / services / databases required | 0 / 0 / 0 |
| Expired-lease recovery | `LEASE_ACQUIRED_RECLAIMED` with `reclaimed_from` = previous owner and reason `LEASE_EXPIRED` |
| Stale-owner release attempt | `LEASE_RELEASE_DENIED` (`LEASE_OWNED_BY_OTHER`) |
| Terminal visibility | `RELEASED` record with `released_at` + `release_reason` survives; next acquire keeps `generation` history |

A race defect found during the first run (a second process taking over the small "lock created, record not yet
written" window) was fixed in the proof by a bounded wait that reports `LEASE_INITIALIZING` instead of seizing the
lease; the final evidence reflects the fixed behaviour.

## CP-04 — Persistent evidence + resume: PASS

- First process ran steps S1–S3 and was stopped by the hard tool-call guard (`MAX_TOOL_CALLS`) → persisted
  `BLOCKED` state with the full MPE graceful handoff.
- A second, isolated interpreter (new process, temporary cwd, only the state file) resumed and completed S4–S5.

| Measurement | Result |
|---|---|
| Steps completed before interruption | 3 / 5 |
| Steps completed after resume (fresh process) | 2 / 5 |
| Re-executed steps | **0** |
| Recomputed digest of already-completed work | matches |
| Rediscovery steps | **0** (`read_from_chat = false`, 4,706 B input) |
| Evidence completeness | **21 / 21** fields (7 graceful-handoff labels + 14 typed-handoff fields) |
| Runtime evidence | 6 events (`spawn`, `claim`, `block`, `spawn`, `resume`, `terminal`) valid against `contracts/RUNTIME_EVENT.schema.json`, `summarize_events` outcome `DONE` |

Artifacts: `evidence/cp04_state_after_resume.json`, `evidence/run-EXP27-CP04.events.jsonl`.

## CP-05 — Budget/runaway guard + existing MPE approval gate: PASS

### Hard boundaries (each produced an explicit STOP/BLOCKED, counters recorded, no silent continuation)

| Guard | Limit | Observed | Stop |
|---|---|---|---|
| `max_retries` | 2 retries | 3 attempts (2 retries) | `MAX_RETRIES` |
| `max_tool_calls` | 5 | 5 executed, 6th refused | `MAX_TOOL_CALLS` |
| `max_wall_seconds` | 0.25 (injected deterministic clock, 0.1/call) | crossed on the 3rd tick | `MAX_WALL_TIME` |
| `compute_budget.hard_limit` | 1.0 | projected 1.8 → `budget_health = RED` (existing canonical status; 0.6 → GREEN) | `STOP/BLOCKED` |

### Existing MPE approval path (reused, unchanged)

| Scenario | Decision | Executor |
|---|---|---|
| Integration-sensitive task (`production_change`), earned L4 history, no approval | `allowed_action = EXECUTE_WITH_APPROVAL`, `acceptance_state = HUMAN_REQUIRED`, risk tier FAST | not invoked (delta 0) |
| Same task, `approval_recorded=True` | gate satisfied | invoked exactly once |
| DEEP-CHANGE task with `stop_condition=True`, even with `approval_recorded=True` | `OBSERVE` / `BLOCKED` (`architecture_redesign`, `deep_change_approval_required`, `human_approval_required`, `stop_condition`) | never invoked |
| Composition: budget guard `GREEN` + gate `HUMAN_REQUIRED` | final outcome `HUMAN_REQUIRED` | budget cannot override the gate |

Source: `scripts/task_acceptance.accept_task` + `enforce_execution` (single enforcement point, fail-closed). No new
gate, no Paperclip authority, no merge/deploy/deep-change performed.

## Per-pattern disposition

| # | Pattern | Verdict | Disposition |
|---|---|---|---|
| 1 | Goal ancestry / context | BORROW | **ADOPT_IN_MPE** (derived packet + source digests; Git stays canonical) |
| 2 | Atomic task lease | ADAPT | **ADOPT_IN_ORCHESTRATOR** (single-host lease as an extension of `scripts/runtime_coordination.py`, in a future authorized checkpoint) |
| 3 | Persistent resumable evidence | KEEP + BORROW | **REUSE_PATTERN_ONLY** (add digest/idempotency key + completeness assertion to existing handoffs; no new store) |
| 4 | Budget / runaway guard | ADAPT | **ADOPT_IN_MPE** (enforced bounded-stop mapped onto the existing compute-budget status vocabulary) |
| 5 | Approval / governance gate | REJECT | **REJECT** donor mechanism; keep the existing MPE gate unchanged |
| — | Paperclip as a system/service/DB | REJECT | **DO_NOT_ADOPT** (parallel control plane, second source of truth) |

## Measurements (required list)

| Metric | Value |
|---|---|
| Duplicate task executions | 0 (3 × 8 concurrent claims) |
| Lease conflicts | 21 explicit, owner + expiry reported |
| Rediscovery steps | 3 → 0 (CP-02); 0 (CP-04 resume) |
| Resume success | yes (fresh isolated process) |
| Evidence completeness | 21/21 fields (100%) |
| Retries / tool calls / wall time | 2 of 2; 5 of 5; 0.25 of 0.25 (all stopped hard) |
| Human approval points | 1 (existing MPE gate), 0 executions without recorded approval |
| Parallel control planes created | 0 |
| Databases / queues / daemons / services added | 0 |
| Files added outside `experiments/` | 0 production, contract, Router, or governance files (only the documented dashboard view refresh, below) |
| Proof harness size | 1,471 lines across 4 experiment-only modules (not production code) |
| Runtime of the full proof | ~1 s wall clock on the sandbox |
| VRU claim | none — bounded proof, not a real user workflow |

## Files changed

| Path | Change |
|---|---|
| `experiments/exp-27-paperclip-orchestration-patterns/` | new experiment (README/ARENA_TASK from PR #53, `UPSTREAM_AUDIT.md`, `COMPONENT_MAP.md`, `RESULTS.md`, `harness/*`, `evidence/*`) |
| `experiments/EXPERIMENT_REGISTRY.json` | EXP-27 registered (PR #53) and closed as `PASS` with evidence links |
| `experiments/exp-21-paperclip-agent-organization-control-plane/README.md` | deleted — unregistered duplicate Paperclip draft that collided with the registered EXP-21 (EasyKitchen) |
| `experiments/exp-19-shirman-trend-intake/cp02/**` + `dashboard/public/registry/**` | regenerated with the repository's documented Reladraw ritual because the registry changed (see below) |

No file under `scripts/`, `contracts/`, `gates/`, `docs/governance/`, `skills/`, `experts/`, `playbooks/`, `teams/`,
or `wrangler.jsonc` was modified.

### Dashboard regeneration (adjacent drift, required by the registry change)

`dashboard/README.md` requires the committed Reladraw views to track `EXPERIMENT_REGISTRY.json`. Adding the EXP-27
entry therefore added new failures for the *existing* freshness tests; the documented ritual
(`scripts/registry_to_reladraw.py` + `reladraw@0.13.0` + copy into `dashboard/public/registry/`) was executed.
This also cleared pre-existing drift from the 2026-09-29 snapshot (EXP-18…EXP-26 entries and the `FAIL`/`PARTIAL`/
`RETIRED` status views). No dashboard content or source file was edited by hand; the artifacts are generated.

## Checks run

| Check | Command | Result |
|---|---|---|
| Full unittest suite, before (base `938f146e`, same-directory-name checkout) | `PYTHONHASHSEED=0 python3 -m unittest discover -s tests` | 369 tests — 41 failures, 3 errors, 1 skipped |
| Full unittest suite, after | same | 369 tests — **7 failures, 0 errors, 1 skipped**; the failing set is a strict subset of the baseline (the 7 are pre-existing registry-schema data issues for EXP-16/EXP-26/EXP-QOOPIA-MEMORY/EXP-UX-UI-SKILLS and the pre-existing `index.html` mobile-status reference check). No new failing test. |
| Proof harness | `python3 .../harness/mpe_proof.py all` | exit 0, `summary.result = PASS`, 4/4 patterns PASS, evidence written |
| Dashboard build | `node scripts/build_dashboard.mjs` | exit 0 (43 assets) |
| Dashboard deploy checks | `node scripts/check_dashboard_deploy.mjs` | `ALL CHECKS PASSED: 43/43` |

## Known limitations / blockers

- The lease proof is **single-host, file-backed**. MPE has no shared-filesystem guarantee across executors, so this
  is a pattern proof, not a distributed lock; a production lease would need an explicit single-host contract or an
  already-approved coordination surface.
- The wall-time boundary is demonstrated with an **injected deterministic clock** (the real measured duration of
  that guarded section is ~0.00001 s); the mechanism, not a real timeout, is what was verified.
- Token/cost boundaries were exercised only through the existing `hard_limit`/`budget_health` contract; no live
  provider usage was measured, and no token accounting was added.
- CP-02's "rediscovery cost" is a file-read/byte proxy measured in the harness, not a human user measurement;
  no Verified Relief Unit is claimed.
- The donor was audited by reading, not by running Paperclip; anything about its runtime behaviour is the donor's
  own documented/tested claim.
- 7 pre-existing unittest failures remain (unchanged by this experiment), plus the pre-existing stale
  `dashboard/public/index.html` portfolio brief snapshot noted in `dashboard/README.md`.

## Next authorized action

None inside this experiment — **STOP after CP-05** per `ARENA_TASK.md`. Any implementation of the BORROW/ADAPT
patterns (lease primitive in `scripts/runtime_coordination.py`, ancestry packet helper, enforced bounded-stop
guard) requires a separate owner-authorized checkpoint and its own deep-change assessment. No productionization
is authorized by this result.
