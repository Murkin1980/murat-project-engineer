# EXP-13 — Low-cost evaluation harness: Pilot Batch 1 findings

Experiment contract: [`docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`](../../docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md)
Frozen pre-registration: [`evidence/exp-13/PILOT_BATCH1_PRE_REGISTRATION.json`](../../evidence/exp-13/PILOT_BATCH1_PRE_REGISTRATION.json)
Attempt evidence: [`evidence/exp-13/PILOT_BATCH1_ATTEMPT_2026-09-30/`](../../evidence/exp-13/PILOT_BATCH1_ATTEMPT_2026-09-30/)
Attempt runner (experiment-specific): [`harness/exp13_pilot_attempt.py`](./harness/exp13_pilot_attempt.py)

Attempt date: 2026-09-30 · Base commit: `66dc1c57ef894586677b200274d06e6003699fe2` (`main`)

## Result

**RESULT: BLOCKED**

Pilot Batch 1 was attempted exactly as pre-registered (`usage_ref: null` for
all 18 entries) and stopped at the usage-evidence gate. The contract states:
*"The full pilot must not start until every proceeding route has a valid usage
evidence path."* **15 of 18 entries** (T-001, T-004, T-006, T-010, T-012 ×
routes A / B / premium) would proceed to execution and each requires a real
`USAGE_RECORD`; none exists. No synthetic or estimated usage was substituted,
per the frozen rule "Synthetic usage or cost is not evidence."

This is not a harness failure: the harness refused to execute exactly as
designed (fail-closed). It is a missing-evidence block on the pilot batch
itself.

## Coverage

| Measure | Count |
| --- | --- |
| Registered entries (frozen manifest, `max_runs` 18) | 18 |
| **Attempted** (evaluated through the registered harness) | **18/18** |
| Completed via pre-execution escalation (T-008 → `HUMAN_REVIEW_REQUIRED`, outcome `HUMAN_REQUIRED`) | 3 |
| **Blocked by the usage-evidence gate** (pre-execution said "proceed", no valid usage evidence) | **15** |
| **Proceeded to execution** | **0** |
| Failed (harness misbehaviour: unexpected exception, wrong escalation, fabricated value) | 0 |

Per-case table: `evidence/exp-13/PILOT_BATCH1_ATTEMPT_2026-09-30/ATTEMPT_REPORT.json`
(`cases[]`), console capture: `BATCH_ATTEMPT_CONSOLE.txt`.

## What was verified before the attempt (pre-flight)

- `main` at `66dc1c5`; working branch created from it; frozen inputs unmodified
  (`git diff HEAD -- <frozen inputs>` empty; SHAs pinned in the attempt report).
- Contract SHA-256: `5a6d4a4477ca24cf7b2feee479fd6276716e59f0f4e0c60618c548a34b93316c`.
- Pilot Batch 1 SHA-256: `198b1aab9970b93b2fd34bfb763a169df490415e4f53637791d060a05720cb87`.
- Manifest frozen as expected: `state: PRE_REGISTERED`, `max_runs: 18`,
  18 entries (6 tasks × 3 routes), `usage_ref: null` everywhere; validated
  through the harness's own `plan_batch`.
- Registry/contract/fixture mutually consistent (no NEEDS_REVIEW condition):
  registry `READY_TO_TEST`, "no Pilot Batch 1 runs have executed", next action
  requires valid usage evidence first — matching the contract and the manifest.
- Harness scripts pinned by SHA-256 in the attempt report
  (`scripts/exp13_checks.py`, `scripts/exp13_harness.py`,
  `scripts/triage_engine.py`, `scripts/usage_instrumentation.py`,
  `scripts/usage_from_router_log.py`, `scripts/usage_from_codex_rollout.py`).

## Missing usage evidence (why BLOCKED)

Required per the contract for every proceeding route:

- **Route A / B (10 runs):** a real `USAGE_RECORD` for run id
  `EXP13-<task>-{A,B}` reconstructed by `scripts/usage_from_router_log.py`
  from an isolated, token-metered Codex Router `usage-events.jsonl` window of
  the real execution on that route.
- **Route premium (5 runs):** a real `USAGE_RECORD` for run id
  `EXP13-<task>-premium` reconstructed by `scripts/usage_from_codex_rollout.py`
  from one isolated Codex rollout containing a complete per-call token
  breakdown for the explicit turn.

What actually exists in the execution environment (verified 2026-09-30):

- Manifest `usage_ref` is `null` for all 18 entries (frozen by design).
- No `evidence/exp-13/EXP13-*-USAGE.json` files exist.
- No Codex Router `usage-events.jsonl` (`CODEX_HOME` unset, `~/.codex` absent).
- No Codex rollout/session files at all.
- No `USAGE_RECORD` for any `EXP13-*` run id anywhere in the repository.

The three T-008 routes legally require no usage evidence (they stop at
pre-execution escalation; `usage_ref: null` is the correct frozen value for
them).

Producing the missing evidence requires really executing the 15 proceeding
runs through the Router/Codex and capturing their telemetry — which was not
done here (no compute spent, no credentials added, no external paid API
called). Substituting synthetic values is forbidden by the contract.

## Findings (observed only)

1. **Deterministic decisions.** All 18 per-case pre-execution decisions are
   identical across 3 in-process repetitions and an independent full re-run of
   the attempt runner (per-case canonical-JSON SHA-256 digests match; the three
   produced records are byte-identical). The registered batch CLI also failed
   identically (same return code, same error, zero output files) across
   repeated invocations.
2. **Unsuitable route cut before compute.** T-008 (`production_change` signal)
   escalates to `HUMAN_REVIEW_REQUIRED` / outcome `HUMAN_REQUIRED` on **every**
   route (A, B, premium) before any execution; `human_review_due` fails and the
   run never proceeds. No route exception, no bypass via premium.
3. **Fail-closed evidence gate.** All 15 proceeding entries are refused by the
   harness with `ContractError: usage record is required when the run proceeds
   to execution`. The registered batch entry point (`run_batch` via the CLI)
   aborts (exit 1) with **zero files written** — no partial records, no
   summary that could masquerade as a completed batch.
4. **unobserved ≠ 0.** The three produced records carry the empty
   `USAGE_RECORD` (all fields `null`, `measurement_source: "none"`,
   `measurement: "unobserved"`), `cost_usd: null`,
   `cost_measurement: "unobserved"`, and `null` retries/model_calls/tool_calls.
   No zero was fabricated anywhere. Usage evidence states across the 18
   attempted cases: **observed 0 / estimated 0 / unobserved 18**.
5. **No estimated cost presented as fact.** No cost or budget estimate was
   produced at all: estimated cost is only permitted from real token
   telemetry (which does not exist), and escalated runs are `unobserved` by
   definition.
6. **Triage labels reproduced.** `triage_expected_match` passes in all 18
   cases — the deterministic triage engine reproduces the 6 frozen expected
   labels for the pilot tasks.
7. **Evidence integrity.** Every per-case result references the frozen
   manifest entry, the SHA-256-pinned frozen assets, and the harness entry
   points; produced records are structurally valid against
   `contracts/EXP13_EXECUTION_RECORD.schema.json` (no `jsonschema` dependency
   was added; the structural check is implemented in the attempt runner).
8. **Test suite.** All 93 EXP-13 / contracts / evidence-trust tests pass,
   including 7 new regression guards (`tests/test_exp13_pilot_attempt.py`)
   locking the verified invariants: every proceeding entry of the frozen
   manifest fails closed without usage, the three T-008 routes complete via
   pre-execution escalation, unobserved records carry nulls (never zeros), and
   the committed attempt evidence stays self-consistent and reproducible from
   the frozen assets. (See "Pre-existing main-suite failures" under Harness
   defects for the unrelated dashboard failures present on `main`.)

## Harness defects

No defect was found in the EXP-13 harness itself. Recorded observations:

1. **`run_batch` aborts the whole batch at the first proceeding entry lacking
   usage** (no per-entry error isolation, no partial-failure summary). This is
   fail-closed **by design** (`tests/test_exp13_harness.py::
   test_run_batch_requires_usage`), but it means the registered batch runner
   cannot itself record the "3 escalated / 15 blocked" picture — the attempt
   required an experiment-specific per-case runner. Not fixed: a change to
   frozen harness behaviour is unnecessary for correct measurement and out of
   experiment scope.
2. **Pre-existing main-suite failures (not EXP-13):** 8 dashboard staleness
   failures (`test_dashboard_registry_views`,
   `test_registry_to_reladraw::test_committed_diagram_is_fresh`,
   `test_committed_mobile_views_are_fresh`) — committed SVG renders lag the
   registry. Present on `main` before this experiment. The registry status
   update in this change (EXP-13 → `HOLD`) adds 4 more EXP-13 subtest failures
   to the same already-stale views (12 total). The dashboard refresh is a
   separate bounded maintenance ritual (STATUS.md next-action 8) and was
   deliberately not performed inside this experiment's change to avoid baking
   other experiments' rendered content into it. One unrelated skip (Windows
   junction test).
3. **Contract reconstruction note drift (cosmetic):** the contract records
   "180 tests OK (1 skip)" from its reconstruction; the suite is now 343 tests
   (other experiments added tests). No frozen semantics depend on the count.

## Limitations (what this experiment did not prove)

- No proceeding run executed, so the execution-stage checks
  (`usage_valid`, `usage_consistent`, `retries_within_limit`,
  `defects_within_limit`, `cost_within_limit`) remain unexercised on pilot
  data — covered only by unit tests.
- The `estimated` cost-reconstruction path and the `observed` path were not
  exercised on real pilot telemetry (no token data exists).
- The premium evidence path (`usage_from_codex_rollout.py`) was not exercised
  on a real rollout file in this environment; its fail-closed behaviour on
  incomplete token breakdowns is verified only by unit tests.
- The `PREMIUM_REQUIRED` escalation class never occurs in Pilot Batch 1 (no
  DEEP-CHANGE task among the 6 pilot tasks; T-009 is not in the batch) —
  end-to-end premium escalation remains unit-test-only.
- No conclusion is possible yet about the harness's effect on rework, cost
  avoidance, or escalation quality; that requires the completed 18-run batch
  with real usage evidence.
- BLOCKED means the central hypothesis (cheap pre-execution control pays for
  itself) is **supported only at the pre-execution stage**, not demonstrated
  end-to-end on real spend.

## Production impact

- PRODUCTION_CHANGED: NO
- NEW_INFRASTRUCTURE: NO
- DEEP_CHANGE: NO

Only additive experiment artifacts: attempt evidence, an experiment-specific
runner under `experiments/exp-13/harness/`, documentation (FINDINGS, evidence
README, STATUS EXP-13 bullet), a regression test, and registry/README updates.
No Router, MASTER, runtime, scheduler, telemetry-service, credential, or
production-route change; no new runtime dependency; EXP-13 remains an
experiment, not a production gate.

## Recommendation (bounded)

Do **not** treat EXP-13 as passed or adopted, and do not promote the harness
into any production path. To unblock — no architecture change required:

1. Capture real usage evidence for the 15 proceeding runs: isolated,
   token-metered Router windows for the 10 A/B runs
   (`scripts/usage_from_router_log.py`, run ids `EXP13-T-00x-{A,B}`) and
   complete per-call Codex rollouts for the 5 premium runs
   (`scripts/usage_from_codex_rollout.py`).
2. Re-run the registered 18-entry batch under the frozen contract (the
   attempt runner already supports it once usage records exist), then STOP
   after 18 runs and analyse.
3. Keep the registry status `HOLD` until the full batch completes.

This experiment's result is **not** authorization for any production rollout.
