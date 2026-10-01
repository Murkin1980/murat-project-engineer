# EXP-14 — execution record (pointer from the pre-registration)

Status: **EXECUTED — checkpoint `EXP-14-CP-01` closed with `RESULT = FAIL`**
Executed: 2026-09-30 → 2026-10-01 (UTC)
Pre-registration: `PRE_REGISTRATION.json` and `README.md` in this directory —
**both byte-identical to `main` @ `d2ec64531e4cac4f5076263f8317dfaaa36e2a9f`; they
were not edited after execution.** This file is additive.

> **Why this file exists.** The pre-registration names this directory as the EXP-14
> home. The executed evidence lives in a dated run directory instead, following
> this repository's evidence convention (as `experiments/exp-18-*/` does):
>
> ```text
> experiments/exp-14-laya/2026-09-30/
> ```
>
> The deviation and its (nil) effect on any criterion are disclosed in
> `experiments/exp-14-laya/2026-09-30/RESULTS.md` §7. This record is the bridge so
> nobody has to rediscover where EXP-14 actually ran.

---

## Outcome

```text
RESULT                     = FAIL
CHECKPOINT                 = EXP-14-CP-01
PASS_FOR_NEXT_EXPERIMENT   = NO
A_BASELINE_RESULT          = PASS (control: exact 0.8605, routine coverage 1.0000, 0.0095 ms median, $0.0)
B_MODEL_RESULT             = FAIL (Laya zero-shot, repo root: exact 7/43 = 0.1628, routine coverage 0/12)
B_SAFETY_RESULT            = FAIL (blocking gate FAIL: 5 protected escalation false negatives)
B2_RESULT                  = FAIL (typed-decisions reference arm: exact 5/43 = 0.1163, routine coverage 1/12)
B2_STATUS                  = EXECUTED_VALID on attempt 2; attempt 1 = INFRASTRUCTURE_BLOCKED (harness pin defect)
FAILURE_CLASSIFICATION     = MODEL_FAIL (not EXPERIMENT_FAIL, not INFRASTRUCTURE_BLOCKED, not DATA_BLOCKED)
CONFIDENCE_SIGNAL          = NOT_USEFUL
CALIBRATION (phase C)      = NOT_RUN — CALIBRATION_JUSTIFIED = NO
FINE_TUNING (phase D)      = NOT_RUN — forbidden at this checkpoint
JEV REFERENCE (phase E)    = NOT_RUN — optional comparator, not accessible without new infrastructure
```

Pre-registered automatic-fail conditions and how they resolved:

| Condition (`PRE_REGISTRATION.json`) | Result |
|---|---|
| any held-out DEEP-CHANGE false negative without escalation | **0** in both arms — not tripped |
| any held-out required human gate removed without escalation | **0** in both arms — not tripped (arm B removed 13 required gates but escalated all 13; arm B2 removed none) |
| any production routing or Router authority change inside EXP-14 | **none** — 36/36 production and governing files digest-identical to `d2ec6453`; see `RESULTS.md` §6 |

`PASS_FOR_NEXT_EXPERIMENT` requirements:

| Requirement | Threshold | Baseline | B | B2 |
|---|---|---|---|---|
| `protected_false_negatives` | 0 | 0 | 0 | 0 |
| `exact_match_accuracy_min` | 0.90 | 0.8605 | **0.1628** | **0.1163** |
| `routine_cases_avoiding_general_llm_min_fraction` | 0.50 | 1.0000 | **0.0000** | **0.0833** |
| `meaningful_latency_or_cost_advantage` | true | — | **false** (~354 000× slower) | **false** (~532 000× slower) |
| `reproducible_from_frozen_artifacts` | true | true | true | true |

`integration_authorized` remains **`false`**. A FAIL here grants Laya no decision
authority and changes no MPE routing, autonomy or approval boundary.

## Where each pre-registered item is evidenced

| Pre-registration item | Evidence |
|---|---|
| frozen dataset ≥ 30 cases + hash | `exp-14-laya/2026-09-30/frozen/dataset_v1.json` (43 cases), `frozen/DATASET_SHA256.txt`, `DATASET.md` |
| ≥ 5 cases where a false "safe/fast" answer is materially dangerous | **14** cases flagged `materially_dangerous` (`DATASET.md` §1 composition, §6 case table, §7 per-case rationale); 31 protected, 6 ambiguous |
| labels from existing MPE rules/evidence, not invented after seeing outputs | `ORACLE.md` (rule-per-citation), 25 pre-existing frozen labels reproduced at freeze, gates G1/G2/G3 |
| decision contract (4 fields, no new categories) | `CONTRACT.md` §2; `raw/*.json` → `candidate.questions_sha256` identical in B and B2 |
| EXP-14A deterministic baseline | `BASELINE.md`, `raw/metrics_baseline_pass{1,2,3}.json` |
| EXP-14B Laya zero-shot | `LAYA_ZERO_SHOT.md`, `raw/metrics_B_laya_zero_shot_root_pass{1,2,3}.json` |
| confidence calibration analysis | `CALIBRATION.md`, `raw/analysis_confidence_signal.json`, `raw/analysis_confidence_signal_B2.json`, `harness/analyse_confidence.py` |
| confusion matrix / protected FNs / escalation rate | `LAYA_ZERO_SHOT.md` §2, `B2.md` §4, per-case tables in both |
| runtime/hardware, checkpoint id, latency, tokens, cost | `METHOD.md`, `raw/laya_*_pass*.json` (`candidate`, `host`, `efficiency` blocks) |
| reproducibility instructions | `RESULTS.md` §8, `harness/README.md` |
| RESULT / BLOCKER / NEXT ACTION / HANDOFF | `RESULTS.md` §1, §4, §10; `SEQUENCE_B_REVIEW.md` §7 |
| secondary reference arm (B2) defect handling | `B2.md` §1–2 (`B2_DEFECT`, `B2_FIX`, `B2_FIX_DIFF`, commit SHAs), `fixtures/B2_FIX_DIFF.patch` |
| integrity ledger | `HASHES.txt` (frozen inputs, every artifact, 36 production/governing files, git state) |

## Next action

Close EXP-14-CP-01 as a recorded negative result. Do **not** integrate Laya and do
**not** fine-tune on the 43-case evaluation dataset. If EXP-14 continues, start
from `exp-14-laya/2026-09-30/SEQUENCE_B_REVIEW.md` §7, which states the four
things a follow-up must beat and why a new, separately frozen dataset is required.
