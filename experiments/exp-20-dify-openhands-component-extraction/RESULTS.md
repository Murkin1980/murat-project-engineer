# EXP-20 — Results: Dify / OpenHands component extraction

- **RESULT: PASS**
- Final recommendation: **`REUSE_COMPONENT` — pattern-level only. Do not adopt Dify or
  OpenHands, do not deploy either, do not add either as a dependency.** Two narrow
  components are worth a *separately authorized* future change; everything else is
  `KEEP_EXISTING` or `REJECT`, and six component groups hit `DEEP_CHANGE_REQUIRED` and were
  stopped, not implemented.
- Run date: 2026-10-09 (UTC)
- Branch: `arena/6f37b26a-murat-project-engineer` (base `21ad8ba2`)
- Primary disposition: `REUSE_COMPONENT` (unchanged from `README.md`)
- Production changed: **NO** — `evidence/proof_run.json → production_files_changed: []`
  across 11 digested production/governance files
- New repository / platform / control plane / persistent runtime / DB / queue / scheduler /
  sandbox / generic DAG engine: **NONE**

Reproduce every number below:

```bash
python3 experiments/exp-20-dify-openhands-component-extraction/harness/exp20_proof.py all
PYTHONHASHSEED=0 python3 -m unittest tests.test_exp20_component_extraction
```

Artifacts: `UPSTREAM_AUDIT.md` (Phase 0 + CP-01 audit and pins), `COMPONENT_MAP.md` (CP-01
map), `DUPLICATE_FILTER.md` (CP-02), `harness/` (CP-03 proofs), `evidence/` (measurements),
`tests/test_exp20_component_extraction.py` (29 specialized checks).

## Phase 0 — audit: COMPLETE

Read before any change: `AGENTS.md`, `docs/governance/SCOPE-CHANGE-CONTROL.md`,
`STATUS.md`, `docs/NEW_IDEA_FILTER_POLICY.md`, the EXP-20 `README.md`,
`docs/architecture/RUNTIME_COORDINATION_PATTERNS.md` +
`Munder Dufflin/CODEX_MPE_RUNTIME_PATTERNS_EXTENSION_RUN11.md` (Run 11), the runtime
contracts, `gates/registry.yaml`, the seven production scripts used as the control arm, and
EXP-25 / EXP-27 / EXP-28. Full list in `UPSTREAM_AUDIT.md` §3.

**EXP-11 does not exist** in the registry or on disk; the material the instruction meant is
Stage-2 **Run 11** (bounded runtime-coordination patterns). Recorded, not silently repaired.

Upstream pins (read-only sparse clones outside this repository; nothing installed,
deployed, vendored, or executed):

| Upstream | Pin | License |
|---|---|---|
| Dify | `langgenius/dify@b2ce9ac10000cbf3d6bd37e5a11234762e0b6d95` (2026-10-09), nearest release `1.17.1` | Dify Open Source License (modified Apache 2.0 + multi-tenant and logo conditions) |
| OpenHands (as named in `README.md`) | `OpenHands/OpenHands@937d0d6aa201d8ac31cac514e0dc64ce5c434004`, release `v1.26.0` | MIT |
| OpenHands agent SDK (secondary, required) | `OpenHands/software-agent-sdk@33044182505244749928644a4643368a9e998ee7` | MIT |
| Dify's workflow engine (external dependency) | `graphon==0.7.0` (`api/pyproject.toml:48`) | **no license classifier on PyPI** |

Two structural corrections were needed before mapping anything (`UPSTREAM_AUDIT.md` §2):
`OpenHands/OpenHands` is now the TypeScript *Agent Canvas* control center — the agent loop,
workspace/sandbox boundary, event store and failure classification live in
`software-agent-sdk`; and Dify's graph engine, variable pool and generic node set moved out
of `api/core/workflow` into the external `graphon` package.

Murat hosts: `mebelflow-ai@4e16d8dd` was read (public) to evidence the AI-gateway gap;
MiniBase facts were reused from the EXP-25 pin; **`Murkin1980/Murat-AI-Orchestrator` and
`Murkin1980/business-discovery` returned `403` from this session**, so no architecture claim
is made about them.

## CP-01 — Component map: COMPLETE

`COMPONENT_MAP.md`: 14 Dify rows + 17 OpenHands rows, each
`component → existing Murat equivalent → gap → disposition`, covering all ten required
categories (tool execution; sandbox/executor isolation; task/session state; human approval;
retries/error recovery; context packaging; observability; model/provider abstraction;
workflow representation; plugin/tool registry). Only the four allowed dispositions are used.

| Disposition | Count | Rows |
|---|---|---|
| `KEEP_EXISTING` | 9 | D6, D11, D12, O4 (contract), O5, O6, O9, O11, O14, O15, O16 |
| `BORROW` | 3 | D3, O3 (+ the narrow durability slice of O4), O8 |
| `ADAPT` | 3 | D1, D4 (decision shape only), D5 |
| `REJECT` | 15 | D2, D7, D8, D9, D10, D13, D14, O1, O2, O7, O10, O12, O13, O17 (+ donor approval mechanisms inside O5/O6) |

Six rows are `REJECT — DEEP_CHANGE_REQUIRED` (D7, D8, D9, D10, O1/O2, O13): a new persistent
runtime, a shared workflow DB, a separate scheduler/queue, a new canonical source of truth,
a generic DAG engine, or a Router authority change. None was implemented.

### Special-interest verdicts (not forced)

1. **OpenHands sandbox/executor boundary → `REJECT` / `DEEP_CHANGE_REQUIRED`.** The boundary
   is real (`BaseWorkspace.execute_command/file_upload/file_download/git_changes/git_diff`
   with local and remote-httpx implementations, Docker provisioning per conversation), but
   MPE has no executor: Codex/host remains the execution authority and `enforce_execution`
   only gates an injected callable. Hosting it needs a persistent runtime + a new security
   boundary.
   **OpenHands resumable execution → `KEEP_EXISTING` + one narrow `BORROW`.** MPE already has
   the resume contract (graceful handoff, `AGENT_RUNTIME_STATE`, `RUNTIME_EVENT`, EXP-27
   CP-04 fresh-process resume). The measurable gap is durability granularity, which is P1.
2. **Dify workflow representation → `REJECT` / `DEEP_CHANGE_REQUIRED`** (generic DAG engine,
   now a third-party dependency with unverified license).
   **Dify typed tool/provider abstraction → `REJECT` for MPE** (`ToolParameter` with
   `form = schema|form|llm` is good design, but MPE has no tool registry and no tool caller;
   the provider half belongs to the Router). Reference-only for a future gateway tool surface.
   **What Dify does contribute → `BORROW` (D3/D4/D5)**: typed failure classes, a state-free
   failure decision, and most-restrictive precedence — the same mechanism OpenHands'
   `error_classification.py` implements independently. That convergence is P2.

## CP-02 — Duplicate filter: COMPLETE

`DUPLICATE_FILTER.md` rejects, with the existing mechanism named, everything that duplicates
MPE governance (approval/autonomy composition, locks, context packaging, event sourcing,
usage telemetry), the **Router** (both donors' model/provider abstraction), **MiniBase**
(Dify RAG/vector-store pipeline would be a second data plane), the **existing
approval/evidence model** (OpenHands confirmation policy + security analyzers; Dify HITL;
external tracing backends vs. the trusted-`evidence_ref` rule), **`murat-ai-orchestrator`**
(Dify SQLAlchemy/Celery repositories, Canvas backend registry + automations = the parallel
control plane the orchestrator exists to be), and **Paperclip-derived patterns** from EXP-27
(OpenHands `StuckDetector` overlaps the already-recommended bounded-stop guard; lease/FIFO
locks overlap the EXP-27 single-host lease; the condenser overlaps the measured ancestry
packet).

Rule enforced: no component was accepted for being better implemented. Each survivor carries
a measured delta against MPE's own production code (below).

## CP-03 — Bounded proofs: 2 of 2 PASS

Both proofs run the existing production functions as the control arm in the same process, on
the same fixtures, and neither modifies production code.

### P1 — crash-tolerant, idempotent, resumable event evidence — `BORROW` — **PASS**

Donor: OpenHands `EventLog` (one durable record per event, delete-first length marker,
duplicate-id rejection, scan-and-build-index resume). Host: the MPE JSONL event log in
`scripts/runtime_coordination.py`, unchanged. Real fixture: the committed
`experiments/exp-27-paperclip-orchestration-patterns/evidence/run-EXP27-CP04.events.jsonl`.

| Check | Control arm (existing MPE production code) | Borrowed arm | Measured delta |
|---|---|---|---|
| Torn tail (34 bytes cut mid-line, 5-event log) | `read_events` raises `ContractError: invalid JSONL line 5`; **0/5** events recoverable; no summary possible | **4/5** recovered + 1 explicit damage record (`torn_tail`, line 5, 214 B, `terminated: false`); production `summarize_events` still returns a summary | evidence loss **100 % → 20 %**; the run stays resumable |
| Healthy real MPE log (6 events) | 6 events, summary S | 6 events, summary **identical to S**, 0 damage, verdict `MARKER_UNVERIFIED` (a legacy log has no marker) | no regression, no silent `COMPLETE` |
| Duplicate `event_id` | `append_event` accepts it: **4 records for 3 unique ids**, 1 duplicate | identical replay → `DUPLICATE_REPLAYED`, **0 bytes written**, digest unchanged; different payload under the same id → `DuplicateEventConflict`, digest unchanged | duplicate evidence records **1 → 0** |
| Resume after the crash | impossible (the reader raises first) | isolated interpreter, only the damaged log present: `returncode 0`, `read_from_chat false`, **0 rediscovery steps**, correct `run_id`/`task_id`/lifecycle `[READY, BLOCKED]`, `resumable true`, packet identical to the in-process one | resume becomes possible |
| Cheap length check | full parse: 4 parses for a 4-event log | marker-only: **0 parses**, verdicts `UNCHANGED` / `ADVANCED` / `MARKER_ABSENT`; stale marker (99) → `MARKER_UNVERIFIED` | secondary gain only — see limitation |
| Overhead | median append 0.00094 s (25 appends) | median append 0.00106 s, **ratio 1.124**, +1 empty sidecar file, +2 syscalls, **0 new dependencies**, 0 extra payload bytes | ~12 % on a micro-benchmark |
| Failure mode | — | a damaged interior line, an unparsable-but-valid-JSON event and a duplicate id are each reported with line number and kind; nothing is dropped silently; `recover()` never writes to the log | explicit, fail-closed reporting |
| Rollback | — | delete `harness/` + `evidence/`; nothing else references them; 11 production digests unchanged before/after | zero production rollback surface |
| Determinism | — | two full passes produce byte-identical normalized evidence (`p1_second_pass_identical: true`) | deterministic |

### P2 — deterministic failure classification onto the existing gate vocabulary — `BORROW` — **PASS**

Donors: OpenHands `event/error_classification.py` (closed `FailureKind`, `retryable`,
`user_action`, authoritative-class-first ordering, detail never copied into evidence) + Dify
`api/core/tools/errors.py` and `output_failure_orchestrator.py` (typed failure classes,
state-free decision, most-restrictive precedence). Host: the real `gates/registry.yaml`
(20 gates parsed, none edited) and the real `scripts/execution_runner.run_task` path, driven
by the `tests/test_execution_runner.py` fixture (5 trusted VERIFIED PASS runs at L4, which is
what it takes for the executor to be invoked at all). 14 failure cases, each a real MPE
exception class attached to a real `gate_id`.

| Check | Control arm | Borrowed arm | Measured delta |
|---|---|---|---|
| Differentiation | `execution_status = "ERROR"` for **all 14** cases — **1** distinct value; executor invoked exactly once per case | **8** distinct kinds → **4** distinct decisions (`RETRY`, `REWORK`, `BLOCKED`, `HUMAN_REQUIRED`), each anchored to the gate's declared `failure_state` | 1 → 8 distinguishable outcomes; **8** cases get a bounded retry inside the gate's own policy |
| Authority | — | `allowed_action`, `acceptance_state`, `executor_invoked`, `execution_status`, `blocking_reasons`, `task_risk_tier`, `dispatch_evaluation_id`, `events` identical in **14/14** cases | annotation only — measured, not asserted |
| Gate authority floor | — | **0** cases downgraded below the declared state; **2** escalated (fail-closed `auth`, `internal`); **4/14** land exactly on the state the registry already declares (`compute_budget_health` and `deep_change_check` → `HUMAN_REQUIRED`) | independent convergence with MPE's own rules |
| Deep-change authority | `run_task(deep_change_task, …, L4, 5 verified PASS, stop_condition=True)` → `OBSERVE` / `BLOCKED`, executor calls **0** | classifier adds `kind=unknown`, `decision=HUMAN_REQUIRED`, `retry_budget=0`, `classifier_granted_execution=false` | **0** executions granted by the new layer |
| Evidence hygiene | the production arm copies raw exception text into `execution_result`; the planted synthetic marker appears in **1** case | classification carries `kind`/`retryable`/`executor_action` only: planted-marker occurrences **0**, cases copying raw text **0** | a credential-looking string stops travelling with the evidence |
| Determinism / cost | — | 3 identical passes, order-independent, median classify **4.2 µs**, 0 new dependencies, gate registry read by a ~30-line dependency-free parser (MPE has no YAML dependency and gains none) | deterministic and free |
| Composition | — | `{rate_limit, auth, quota}` over `{integration_tests, build, compute_budget_health}` → `HUMAN_REQUIRED`, reusing `dispatch_autonomy`'s most-restrictive rule; a foreign word (`ESCALATE_TO_CLOUD`) is rejected | no second composition model |

Second concrete consumer (why this is not a one-off abstraction, SCOPE-CHANGE-CONTROL §10):
MebelFlow AI `packages/ai-gateway/src/index.ts` (`4e16d8dd`) throws 7 string sentinels as
generic `Error` (`GATEWAY_BUSY:275`, `SESSION_REQUEST_IN_PROGRESS:277`,
`SESSION_CALL_LIMIT:289,310`, `TENANT_BUDGET_EXCEEDED:296`, `BUDGET_RESERVATION_MISSING:233`),
collapses a provider HTTP failure into prose (`:121-122`) and contains **0** occurrences of
"retry". Same gap, same fix, no change made to that repository.

### Volume of new code

| Path | Lines | Production? |
|---|---|---|
| `harness/durable_event_evidence.py` | 301 | no — experiment-only |
| `harness/failure_classification.py` | 280 | no — experiment-only |
| `harness/exp20_proof.py` | 675 | no — measurement runner |
| `harness/resume_worker.py` | 40 | no — fresh-process worker |
| `tests/test_exp20_component_extraction.py` | 410 | test-only |
| documents (`UPSTREAM_AUDIT`, `COMPONENT_MAP`, `DUPLICATE_FILTER`, `ARENA_TASK`, `RESULTS`) | ~700 | documentation |

If P1+P2 were ever authorized for production, the estimate in `COMPONENT_MAP.md` §3 is
~60 lines (P1, additive beside `read_events`/`append_event`) and ~120 lines (P2, annotation
on the `run_task` outcome) — **not** done here.

## Rejected as duplication (summary)

Router-level model/provider abstraction (both donors) · OpenHands confirmation policy,
security analyzers and hook scripts · Dify HITL pause/resume · OpenHands condenser and Dify
variable pool (context packaging) · OpenHands event tree/branching (event sourcing) ·
OpenHands FIFO/resource locks (EXP-27 lease territory) · OpenHands `StuckDetector` (EXP-27
bounded-stop guard) · OpenHands token/cost telemetry (existing fail-closed usage adapters) ·
OpenHands secret registry (MPE persists no secrets) · Dify RAG/vector pipeline (MiniBase is
the data plane) · Dify trace providers/OTel (existing trusted-`evidence_ref` model) · Dify
plugin daemon and both tool registries (no consumer) · Dify SQLAlchemy/Celery repositories
and Canvas automations (parallel control plane) · both sandbox/executor layers (Codex is the
execution authority).

## Full-platform adoption is not needed — proven

Two components, 1,296 lines of experiment-scoped Python + 410 lines of tests, **0** new
dependencies, **0** services/databases/queues/daemons/sandboxes/workflow engines
(`evidence/proof_run.json` records each as `false`), **0** production files changed, whole
proof run in **0.24 s**. Both proofs call the existing production functions instead of
replacing them: the strict reader and the single enforcement point remain the defaults.
Neither donor was executed, installed, or deployed.

## Checks

| Check | Command | Result |
|---|---|---|
| Package validator | `python3 scripts/validate_package.py .` | **VALIDATION PASSED** — 4 experts, 3 teams, 5 playbooks, contracts, 20 gates |
| Full unittest baseline **before** (base `21ad8ba2`) | `PYTHONHASHSEED=0 python3 -m unittest discover -s tests` | 369 tests — **7 failures**, 0 errors, 1 skipped |
| Full unittest **after** | same | 398 tests — **7 failures**, 0 errors, 1 skipped; the failing set is *identical* to the baseline (4 registry-field failures for EXP-16 / EXP-26 / EXP-QOOPIA-MEMORY / EXP-UX-UI-SKILLS, 3 `index.html` mobile-status reference failures). **No new failing test**; 29 new tests all pass |
| Specialized proof tests | `PYTHONHASHSEED=0 python3 -m unittest tests.test_exp20_component_extraction` | 29 tests — **OK** |
| Proof harness | `python3 …/harness/exp20_proof.py all` | exit **0**, `result: PASS`, `p1: PASS`, `p2: PASS`, both determinism flags true |
| Whitespace/conflict markers | `git diff --check` | clean |
| Secrets | `grep -rnE "(api[_-]?key\|secret\|token\|password)\s*[:=]\s*['\"][A-Za-z0-9_-]{16,}"` over the new files | no matches. The only credential-looking string is the synthetic marker `PLANTED-PROOF-TOKEN-not-a-real-credential-9f3c` in `harness/fixtures.json`; it exists to prove the leak, is redacted in every evidence field that quotes a production reason, and appears **0** times in the classification evidence |
| Scope | `git status --short` | changes confined to `experiments/exp-20-…`, `experiments/EXPERIMENT_REGISTRY.json`, the registry-driven dashboard views, and `tests/` |

Pre-existing failures were **not** fixed here (instruction: do not fix them inside EXP-20
without direct necessity). The registry change did require the documented Reladraw
regeneration ritual, because `dashboard/README.md` makes the committed views track
`EXPERIMENT_REGISTRY.json` and `tests/test_dashboard_registry_views.py` enforces freshness.

## Known limitations

- Neither upstream was executed; all donor statements are read from source, docstrings and
  their own tests. No property of Dify or OpenHands was measured.
- The torn tail is a **simulated** crash (truncating the final durable line), not a real
  `SIGKILL` during `os.write`. MPE's writer already does one `os.write` + `fsync` per line, so
  a partial line is possible but was not reproduced from a real kill.
- P1's length marker is **not** an integrity proof. Under MPE's existing single-writer claim
  its measured value is small (0 parses vs 4 on a 4-event log); it is recorded as
  borrow-secondary and should be dropped if P1 is ever adopted without it.
- P2's retry budgets are derived from the registry's **prose** `retry_policy` through an
  explicit rule table in the harness. That table is an interpretation; adopting P2 in
  production should either make the budget a declared registry field (a contract change, out
  of scope here) or keep the table under test.
- P2 classifies failures only for the MPE runner path and (as evidence) the MebelFlow gateway;
  `murat-ai-orchestrator` could not be read (`403`), so no claim is made about it.
- No Verified Relief Unit is claimed: both proofs are bounded engineering proofs on fixtures,
  not relief delivered to a real user workflow.
- 7 pre-existing unittest failures remain, unchanged.

## Next authorized action

**None inside EXP-20 — STOP after CP-03.** Any implementation of P1 (additive recovery +
idempotent append in `scripts/runtime_coordination.py`) or P2 (failure annotation on the
`scripts/execution_runner.run_task` outcome) requires its own owner-authorized checkpoint,
its own tests, and — because both touch the runtime-evidence and execution paths — a
deep-change assessment before editing production. No productionization, no cross-repository
change, and no Dify/OpenHands dependency is authorized by this result.

## Delivery

- Changed files: see the table below and `git show --stat` on the commit.
- Commit SHA: `6b118cb830a703aa6ca323ffe03ed466811d93b0` (experiment, harness, evidence, tests,
  registry and regenerated views); the SHA/PR record itself is the follow-up commit on the same branch.
- PR: <https://github.com/Murkin1980/murat-project-engineer/pull/63> — opened from
  `arena/6f37b26a-murat-project-engineer`, **not merged** (no merge authority was granted for this run).

| Path | Change |
|---|---|
| `experiments/exp-20-dify-openhands-component-extraction/ARENA_TASK.md` | new — frozen owner instruction |
| `experiments/exp-20-dify-openhands-component-extraction/UPSTREAM_AUDIT.md` | new — Phase 0 + CP-01 audit, pins, licenses, per-category facts |
| `experiments/exp-20-dify-openhands-component-extraction/COMPONENT_MAP.md` | new — CP-01 map (31 rows) + landing targets |
| `experiments/exp-20-dify-openhands-component-extraction/DUPLICATE_FILTER.md` | new — CP-02 duplicate register, measured deltas, stop rules |
| `experiments/exp-20-dify-openhands-component-extraction/RESULTS.md` | new — this report |
| `experiments/exp-20-dify-openhands-component-extraction/README.md` | status header updated to COMPLETED — PASS + checkpoint-vocabulary note; planning text preserved |
| `experiments/exp-20-dify-openhands-component-extraction/harness/{durable_event_evidence,failure_classification,exp20_proof,resume_worker}.py`, `harness/fixtures.json` | new — CP-03 proofs (experiment-scoped) |
| `experiments/exp-20-dify-openhands-component-extraction/evidence/*` | new — `proof_run.json`, `proof_run.log`, `cp03_p1_durable_event_evidence.json`, `cp03_p2_failure_classification.json`, `cp03_p1_damaged_log.jsonl` |
| `tests/test_exp20_component_extraction.py` | new — 29 specialized proof tests |
| `experiments/EXPERIMENT_REGISTRY.json` | EXP-20 `PLANNED → PASS` with the measured summary, next action and evidence links |
| `experiments/exp-19-shirman-trend-intake/cp02/**`, `dashboard/public/registry/**` | regenerated with the documented Reladraw ritual because the registry changed (generated artifacts, not hand-edited) |

No file under `scripts/`, `contracts/`, `gates/`, `docs/governance/`, `skills/`, `experts/`,
`playbooks/`, `teams/`, `.github/`, or `wrangler.jsonc` was modified.
