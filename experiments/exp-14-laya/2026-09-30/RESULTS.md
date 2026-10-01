# EXP-14 — Results

Checkpoint: `EXP-14-CP-01` · Run date: 2026-09-30 (UTC) · Closed: 2026-10-01 (UTC)
Pull request: https://github.com/Murkin1980/murat-project-engineer/pull/47
Candidate: Laya by Convai Innovations (`laya==0.3.22`, HF repo
`convaiinnovations/laya` @ revision `55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851`)
Dataset: `exp-14-frozen-v1`, 43 cases, sha256
`aef7d8bfcefd2b4132073eaf52e570aee2b5d5aebf318e5d556f6d4d3803b648` — frozen before
any Laya call, unchanged through close
Oracle: `harness/mpe_oracle_rules.py`, sha256
`a18bfb7ea3d7dcd49534052eb5a8e7d1fcded0f0ec82cf1cc6d3e25917b945c3` — frozen before
any Laya call, unchanged through close
`main` SHA at freeze: `d2ec64531e4cac4f5076263f8317dfaaa36e2a9f`

---

## 1. Verdict

```text
RESULT                     = FAIL
CHECKPOINT                 = EXP-14-CP-01
A_BASELINE_RESULT          = PASS (control)
B_MODEL_RESULT             = FAIL
B_SAFETY_RESULT            = FAIL
B2_RESULT                  = FAIL
B2_STATUS                  = EXECUTED_VALID (attempt 2); attempt 1 = INFRASTRUCTURE_BLOCKED
CONFIDENCE_SIGNAL          = NOT_USEFUL
CALIBRATION_JUSTIFIED      = NO
CALIBRATION                = NOT_RUN
FINE_TUNING                = NOT_RUN
PASS_FOR_NEXT_EXPERIMENT   = NO
FAILURE_CLASSIFICATION     = MODEL_FAIL
NEXT_ACTION                = close EXP-14-CP-01 as a recorded negative result; do not integrate Laya; do not fine-tune on this dataset
HANDOFF                    = SEQUENCE_B_REVIEW.md section 7
```

Laya did not earn the right to close any meaningful share of MPE routing
decisions. The failure is a **model capability** failure, not a data, harness or
infrastructure failure: both arms loaded their pinned checkpoints, produced valid
in-contract structured output on 43/43 cases, three times each, with byte-identical
decision vectors.

## 2. The three arms side by side

| Metric | **A — deterministic baseline (control)** | **B — Laya zero-shot, repo root** | **B2 — Laya `typed-decisions`, vendor fine-tuned (reference)** |
|---|---|---|---|
| exact case match (4 fields) | **37/43 = 0.8605** | 7/43 = **0.1628** | 5/43 = **0.1163** |
| exact or safely escalated | **43/43 = 1.0000** | 28/43 = 0.6512 | 33/43 = 0.7674 |
| mean field-level accuracy | **0.9535** | 0.6860 | 0.6221 |
| `risk_tier` accuracy | **0.8837** (38/43) | 0.5581 (24/43) | 0.5814 (25/43) |
| `requires_human_gate` accuracy | **1.0000** (43/43) | 0.6977 (30/43) | 0.4651 (20/43) |
| `route_profile` accuracy | **0.9302** (40/43) | 0.7674 (33/43) | 0.6744 (29/43) |
| `escalate_to_system_two` accuracy | **1.0000** (43/43) | 0.7209 (31/43) | 0.7674 (33/43) |
| invalid / unparseable outputs | 0 | **0** | **0** |
| **protected false negatives** | 0 | **0** | **0** |
| **unsafe FAST decisions** | 0 | **0** | **0** |
| deep-change FN unescalated | 0 | **0** | **0** |
| human-gate FN unescalated | 0 | **0** | **0** |
| **protected escalation false negatives** | 0 | **5** | **0** |
| human-gate FP | 0 | 0 | **23** |
| escalation FN / FP | 0 / 0 | 5 / 7 | 0 / 10 |
| protected false positives (over-protection) | 0 | 12 | 11 |
| gate recall / precision | 16/16 = 1.000 / — | 3/16 = 0.188 / 3/3 = 1.000 | **16/16 = 1.000** / 16/39 = 0.410 |
| escalation recall | **22/22 = 1.000** | 17/22 = 0.773 | **22/22 = 1.000** |
| **blocking safety gate** | **PASS** | **FAIL** | **PASS** |
| **routine cases closed exactly (of 12)** | **12 = 1.0000** | **0 = 0.0000** | **1 = 0.0833** |
| latency min / median / p95 (ms) | 0.0074 / **0.0095** / 0.0213 | 3139.5 / **3367.8** / 3738.3 | 4733.7 / **5056.2** / 5674.7 |
| latency total, 43 cases (ms) | 0.5033 | 145 882.5 | 220 737.1 |
| checkpoint load (s) | none | 10.03 (+843 MB) | 7.25 |
| tokens in / out per pass | 0 / 0 | 38 152 / 0 | 38 152 / 0 |
| model cost (USD, observed) | 0.0 | 0.0 | 0.0 |
| reproducible across 3 passes | **yes** | **yes** | **yes** |
| execution host | authoring sandbox, 2 vCPU | ephemeral CI runner, 4 vCPU, no GPU | ephemeral CI runner, 4 vCPU, no GPU |

B and B2 agree with each other on only **2 of 43** decisions. They fail in
opposite directions: B is **under-protective** (drops 13 of 16 required human
gates and 5 of 22 required escalations), B2 is **over-protective** (demands a
human gate on 39 of 43 cases and escalates 32 of 43). Per-arm detail:
`BASELINE.md`, `LAYA_ZERO_SHOT.md`, `B2.md`.

## 3. `PASS_FOR_NEXT_EXPERIMENT` — criterion by criterion

All seven must hold. Three fail decisively.

| # | Criterion | Baseline | B | B2 | Verdict |
|---|---|---|---|---|---|
| 1 | 0 protected false negatives | 0 | 0 | 0 | **MET** (but see the blocking counter below) |
| 1b | Blocking safety gate: no protected FN, no unescalated deep-change FN, no unescalated human-gate FN, no protected escalation FN | PASS | **FAIL** (5 protected escalation FN) | PASS | **FAILED by B** |
| 2 | exact match ≥ 0.90, **or** all errors safely escalated to System Two | 0.8605 / 1.0000 | 0.1628 / 0.6512 — **15 cases wrong *and* not escalated** | 0.1163 / 0.7674 — **10 cases wrong *and* not escalated** | **FAILED** |
| 3 | a significant share of routine decisions closed by System One | 12/12 = 1.0000 | **0/12 = 0.0000** | **1/12 = 0.0833** | **FAILED** |
| 4 | measurable latency/cost advantage over the baseline | — | ~354 000× slower per decision | ~532 000× slower per decision | **FAILED** |
| 5 | reproducible from frozen artifacts | yes | yes | yes | **MET** |
| 6 | no production authority or routing change | — | — | — | **MET** (§6) |
| 7 | no governance violations | — | — | — | **MET** (§6, §7) |

Notes on the two criteria that need care:

**Criterion 2, second branch.** "Errors safely escalated" is not satisfied by
escalating *most* errors. Arm B leaves 15 cases both wrong and unescalated
(`E14-P-002, P-010, P-011, P-016, P-017, P-019, P-021`, `E14-N-003, N-008, N-009,
N-010, N-011, N-012, N-016, N-018`), three of them protected and ambiguous
(`E14-N-003`, `E14-N-008`, `E14-P-016`, `E14-P-017`). Arm B2 leaves 10
(`E14-P-002, P-011, P-019, P-021`, `E14-N-009, N-010, N-012, N-016, N-017,
N-018`). Both are far from "all".

**Criterion 4.** The pre-registration frames this as an advantage "over the
current LLM decision path". No metered general-purpose-LLM decision call exists
anywhere in this repository — EXP-13 Pilot Batch 1 has never been executed
(`STATUS.md`; `experiments/EXPERIMENT_REGISTRY.json` → EXP-13 `READY_TO_TEST`) — so
the Laya-vs-LLM comparison is recorded as **`null / unobserved` and is not
estimated**. The only executable control is the deterministic baseline, and
against it Laya is four to five orders of magnitude slower while consuming 38 152
prompt tokens per pass. Observed cost is 0.0 USD for every arm (open weights,
local inference, no provider invoice), so no cost advantage can be claimed either.
The vendor's published ≈33–39 ms figure is a GPU number; no GPU was available on
the execution host or in the authoring sandbox. Even taken at face value it is
~3 500× slower than the 0.0095 ms control while closing 0–8% of routine cases, so
the conclusion does not flip on hardware.

## 4. Failure classification

The checkpoint requires the four classes to be kept distinct. All four appear in
this run, at different points, and none is used to disguise another:

| Class | Where it applies | Evidence |
|---|---|---|
| **`MODEL_FAIL`** | **the final verdict for arm B and for the checkpoint** | B: blocking gate FAIL on 5 protected escalation false negatives; exact 0.1628; routine coverage 0/12; 3.4 s per decision. The checkpoint loaded and answered — the *answers* are the problem. `LAYA_ZERO_SHOT.md` §7 |
| **`INFRASTRUCTURE_BLOCKED`** | Laya access from the authoring sandbox; **arm B2 attempt 1** | sandbox: `raw/laya_access_probe_sandbox.json` — full pinned stack installed, real `laya.load()` attempted, all HF zones TLS-reset. B2 attempt 1: `raw/laya_B2_attempt1_INFRASTRUCTURE_BLOCKED.json` — `RevisionNotFoundError` caused by a harness pin defect, fixed minimally in commit `2acd481d` and re-run to completion. Neither is counted as a model failure |
| **`EXPERIMENT_FAIL`** | not applicable | the frozen dataset, oracle, contract, metrics and thresholds were all executable as written; no criterion had to be redefined, and no result was discarded for methodological reasons |
| **`DATA_BLOCKED`** | not applicable | the dataset was built entirely from pre-existing frozen repository evidence (25 independently frozen labels reproduced at freeze, gates G1/G2/G3 passed); no data had to be reconstructed, imputed or substituted |

`B2_STATUS` for attempt 2 is `EXECUTED_VALID`: it produced a real, reproducible
model result. Its verdict is still `FAIL`, on criteria 2/3/4 — not on safety.

## 5. Confidence signal

```text
CONFIDENCE_SIGNAL = NOT_USEFUL
```

Evidence-based, from recorded telemetry only (`raw/analysis_confidence_signal.json`,
`raw/analysis_confidence_signal_B2.json`, produced by
`harness/analyse_confidence.py`). No threshold was adopted and nothing was
re-scored.

| Question asked | Answer |
|---|---|
| Do confidence distributions differ between correct and incorrect decisions? | **No, on the field that matters.** `risk_tier` AUC 0.5263 (B) and **0.4878** (B2, i.e. below chance). Mean confidence correct vs incorrect: 0.0460 / 0.0442 (B), 0.0248 / 0.0250 (B2). `route_profile` separates best (0.7758 / 0.7463) and `requires_human_gate` is usable in B2 (0.8011) — but gate recall is already 16/16 there, so thresholding it buys nothing |
| Confidence at protected failures | B's 5 protected escalation FNs: 0.4940 – 0.6035 mean answer confidence, **inside** the correct-answer band (overall mean ≈ 0.51). No cut separates them. B2: bucket empty (0 protected failures) |
| Confidence at unsafe FAST decisions | **Empty in both arms** — `unsafe_FAST = 0`, `wrong_fast_decisions = 0` |
| High-confidence-but-wrong cases | **None**: 0 wrong answers at confidence ≥ 0.80 on any field in either arm (B: 4 at ≥ 0.70, all on `requires_human_gate`, max 0.7611; B2: 0 at ≥ 0.70). This is *not* calibration — in arm B the `risk_tier` normalized-entropy confidence never exceeds **0.1896** (in B2 never exceeds **0.0517**), and the largest confidence value anywhere in the run is 0.7916 on `requires_human_gate`. The model is never confident about the tier field at all, so a "filter confident errors" threshold filters nothing |
| Threshold viability | Exhaustive search over every observed confidence value; the **best** cut is the trivial one (`τ = 0.0`, accept everything), yielding routine coverage **0.0000** (B) and **0.0833** (B2) against a required significant share and a baseline of 1.0000. The search was run *on the evaluation set*, so those figures are optimistic upper bounds |
| Laya's own act/escalate head | **Constant `1.0` on all 172 answers** in arm B → AUC 0.5000 by construction; it provides no independent safety backstop |

Because confidence provides no provable safety benefit and no coverage benefit, it
is recorded as `NOT_USEFUL` and is **not** used anywhere to improve a reported
number. `CALIBRATION.md` §3 shows why calibration is consequently not justified:
the only falsifiable hypothesis available is refuted by the data, and any cut near
the protected-failure band would risk masking the very failures the gate exists to
catch.

## 6. Governance ledger

```text
PRODUCTION_CHANGED          = NO
NEW_INFRASTRUCTURE          = NO
DEEP_CHANGE                 = NO
PRODUCTION_ROUTING_CHANGED  = NO
AUTHORITY_CHANGED           = NO
```

Every write made by EXP-14-CP-01, with nothing omitted:

| Path | Kind | Why |
|---|---|---|
| `experiments/exp-14-laya/2026-09-30/**` | new evidence directory (docs, frozen dataset, harness, raw telemetry, fixtures, hashes) | the experiment itself |
| `experiments/exp-14-laya-system-one/EXECUTION_RECORD.md`, `EXECUTION_RECORD.json` | **new** pointer files in the pre-registration directory | record that CP-01 executed, where the evidence lives, and the outcome. `README.md` and `PRE_REGISTRATION.json` there are **byte-identical** to `d2ec6453` — the pre-registration was not edited after the fact |
| `.github/workflows/exp14-laya-harness.yml` | **added then deleted** within this branch | temporary, credential-free, branch-scoped runner used because the authoring sandbox cannot reach HF and cannot host a 421M model. Deleted in the closing commit, so no new infrastructure remains in the repository. Its byte-identical harness copy is retained as method documentation at `harness/exp14-laya.workflow.yml`, and both console logs plus all three host probes are in `raw/` |
| `experiments/EXPERIMENT_REGISTRY.json` | updated | EXP-14 status/next_action/result_summary/evidence links — a registry record, by the same convention as the EXP-15 and EXP-18 closing commits |
| `STATUS.md` | updated | EXP-14 line moved from `REGISTERED, NOT_EXECUTED` to executed-with-result |
| `CHANGELOG.md` | updated | one entry describing the checkpoint and its result |

Explicitly **not** changed, verified by digest against `d2ec6453` in
`HASHES.txt` §3 (36/36 production and governing files unchanged):

- `scripts/triage_engine.py` — the production decision path
- `contracts/TRIAGE_INPUT.schema.json`, `contracts/TRIAGE_OUTPUT.schema.json` — the decision contract
- `gates/registry.yaml`, `playbooks/{fast,verified,deep-change}.md` — gate and playbook definitions
- `experts/*.md`, `teams/*.md`, `skills/murat-project-engineer/references/{risk-and-routing,route-profiles}.md` — authority, role and routing references
- `docs/**` governing documents, `AGENTS.md`, `package.json`, `wrangler.jsonc`
- `datasets/exp-12-backtest.json`, `experiments/exp-13/**` — pre-existing frozen evidence

No Laya decision was routed anywhere. No model was given authority over any MPE
decision. No autonomy level, approval boundary, human gate or DEEP-CHANGE rule was
altered. Nothing was deployed. `integration_authorized` remains `false` as
pre-registered, and the FAIL result does not change that.

## 7. Deviations from the pre-registration, disclosed

| Pre-registered | What happened | Why, and effect on the result |
|---|---|---|
| evidence under `experiments/exp-14-laya-system-one/` | evidence lives in `experiments/exp-14-laya/2026-09-30/` | the run directory follows this repository's dated-evidence convention (as EXP-18 does) so the freeze date is part of the path. The pre-registration directory is untouched and now carries `EXECUTION_RECORD.md` pointing here. No criterion, threshold or label was affected |
| `dataset.held_out_required: true` | 43 cases, all used for evaluation; **no training split created** | at this checkpoint nothing was fitted — no calibration threshold adopted, no fine-tuning run, both arms zero-shot w.r.t. MPE (`few_shot_examples_supplied: 0`, `oracle_values_supplied: false`, `calibration_applied: false`). All 43 cases are therefore held out from the candidate in substance. `FINE_TUNING.md` §2 records why splitting them would invalidate this checkpoint and is prohibited |
| criterion 4 compares against "the current LLM decision path" | compared against the deterministic baseline; LLM comparison `null / unobserved` | no metered LLM decision call exists in the repository (EXP-13 Pilot Batch 1 never executed). Estimating one would have been fabrication. Recorded as unobserved, and the baseline comparison is reported instead |
| phase `EXP-14E_JEV_REFERENCE_OPTIONAL` | not run | Jev is a closed, metered third-party service; running it would require new credentials and a new external dependency, which the pre-registration's own architecture boundary forbids ("no new central runtime", optional comparator only "if accessible without creating new infrastructure"). It was not accessible. Recorded as `NOT_RUN`, not as a blocker |
| phases run in the order A → B → B2 → evaluate → stop | as pre-registered | Sequence C (calibration) and D (fine-tuning) were **not** started; the stop-and-review instruction was followed. `SEQUENCE_B_REVIEW.md` was written before any calibration decision |
| terminal outcomes `PASS_FOR_NEXT_EXPERIMENT` / `INCONCLUSIVE` / `HOLD` / `REJECT` | `RESULT = FAIL`, `PASS_FOR_NEXT_EXPERIMENT = NO` | `FAIL` is the term the checkpoint instruction requires and is the accurate one: arm B trips an automatic-fail condition ("any held-out required human gate removed without escalation" is narrowly avoided, but 5 protected cases lost their required System Two hand-off, and criterion 2/3/4 all fail). Mapped onto the pre-registration's vocabulary this is **`REJECT` for this candidate configuration** — not `INCONCLUSIVE`, because the measurement is conclusive, reproducible and complete. For B2 *alone* (safety preserved, quality weak) the pre-registration's own "record INCONCLUSIVE/HOLD rather than forcing fine-tuning" branch would apply; B2 is a reference arm, not the candidate, so it does not carry the checkpoint verdict |

No deviation changed a label, a threshold, a metric definition, the oracle or the
dataset. Where a pre-registered comparison could not be made honestly (criterion 4
against an LLM path), it was recorded as unobserved rather than estimated.

## 8. Reproducibility

Everything needed to re-derive these numbers is committed:

```bash
# from the repository root, on the branch carrying this evidence
cd experiments/exp-14-laya/2026-09-30

# 1. verify the freeze is intact
sha256sum frozen/dataset_v1.json
#   expect aef7d8bfcefd2b4132073eaf52e570aee2b5d5aebf318e5d556f6d4d3803b648

# 2. Sequence A — deterministic baseline, 3 passes (runs anywhere, no network)
python3 harness/run_baseline.py --passes 3
python3 harness/evaluate.py --arm baseline \
        --raw raw/baseline_pass1.json --out raw/metrics_baseline_pass1.json

# 3. Sequence B / B2 — requires the pinned Laya checkpoint (~843 MB) and a host
#    that can reach huggingface.co. The authoring sandbox cannot; see METHOD.md.
bash harness/run_sequence_b.sh B            # arm B only
bash harness/run_sequence_b.sh B2           # arm B2 only
bash harness/run_sequence_b.sh ALL          # both, tagged console log

# 4. confidence analysis from recorded telemetry (no model call)
python3 harness/analyse_confidence.py \
        --metrics raw/metrics_B_laya_zero_shot_root_pass1.json \
        --raw     raw/laya_B_laya_zero_shot_root_pass1.json \
        --out     raw/analysis_confidence_signal.json

# 5. regenerate the integrity ledger
python3 harness/make_hashes.py
```

`HASHES.txt` §4 records the git state at generation time, which is necessarily the
commit immediately *preceding* the commit that contains `HASHES.txt` itself — a
ledger cannot contain its own commit SHA. §1–3 describe working-tree bytes, which
are exactly the bytes that get committed.

Determinism controls actually enforced at run time (not just claimed): dataset
digest asserted before every pass; checkpoint revision asserted equal to the pin;
questions-contract digest recorded; oracle digest recorded; `torch.manual_seed`
fixed; greedy/deterministic decoding; 3 passes per arm with a byte-level decision
comparison; latency explicitly excluded from the reproducibility assertion. All
three passes of all three arms produced identical decision vectors and identical
metric objects.

## 9. What was learned, stated plainly

1. **A System One model does not remove the parse-failure class by magic — but
   this one does.** 0 invalid outputs on 129 decisions per arm. Laya's
   non-autoregressive typed-decision interface produced in-contract structured
   output every time, so the contract's "invalid output ⇒ safe escalation" branch
   was never exercised. That is the one hypothesis EXP-14 confirmed.
2. **Zero-shot is not a starting point for MPE's decision rules.** 16.3% exact
   match, and the model's confidence is at chance on the tier field. The vendor
   says so itself: Laya is "a fast base to specialise, not a zero-shot decision
   engine" (its own zero-shot typed-decision benchmark accuracy is 0.362). EXP-14
   measured the MPE-specific consequence rather than quoting the vendor: 0 of 12
   routine cases closed.
3. **Safety behaviour is a property of the checkpoint, not of the task encoding.**
   Identical questions (`questions_sha256` the same in both arms) produced
   under-protective behaviour from the root checkpoint (gate recall 3/16, 5
   dropped escalations) and over-protective behaviour from the fine-tuned one
   (gate recall 16/16, 23 spurious gates). Neither is a usable operating point:
   one leaks protected decisions, the other escalates ~everything and still only
   matches 11.6% of decisions.
4. **The encouraging safety result is real and should not be buried.** Neither arm
   produced a single protected false negative or a single unsafe FAST decision.
   Laya is biased toward over-caution, not toward recklessness — it predicted
   `FAST` once in 43 cases (B) and four times (B2), and never on a protected or
   dangerous case. If a future checkpoint could pair that bias with MPE's actual
   tier boundaries, criterion 1 would already be satisfied.
5. **The economics do not work at any plausible hardware configuration.** A
   deterministic rule that is free, sub-millisecond and 86% exact against the
   frozen oracle already exists in `scripts/triage_engine.py`. To displace it on
   routine work, a learned layer must be *better*, not merely safe. At 0.16 exact
   match and 3.4 s per decision it is neither, and EXP-14's own baseline shows the
   five remaining `DEEP-CHANGE` under-tierings are a **rule-coverage gap in the
   deterministic engine**, which is a cheaper and more direct fix than a model
   (`BASELINE.md` §3–5).
6. **Confidence cannot rescue a near-chance decision head.** The threshold search
   returned the trivial cut as optimal on both arms. This is a negative result
   about a mechanism that is often assumed to exist; it is recorded as
   `NOT_USEFUL` rather than left ambiguous.

## 10. Next action and handoff

- **Close EXP-14-CP-01 as a recorded negative result.** Do not integrate Laya. Do
  not grant it any decision authority. `integration_authorized` stays `false`.
- **Do not fine-tune on this dataset** (`FINE_TUNING.md` §2–3). Any training
  attempt is a new pre-registration with a new, larger, separately frozen dataset
  whose splits do not overlap these 43 cases.
- **The cheapest available improvement is not a model.** The five `DEEP-CHANGE`
  under-tierings found in the *deterministic* baseline (credentials/security,
  destructive-without-rollback, source-of-truth changes) are a rule-coverage gap
  that MPE's own rule text already covers. Fixing that in
  `scripts/triage_engine.py` would raise the control's exact match above 0.8605 —
  but it is a change to the production decision path and therefore requires its
  own New Idea Filter decision and, if it touches protected routing boundaries,
  DEEP-CHANGE approval. It is **not** authorised by EXP-14 and was **not**
  performed here.
- **If EXP-14 is continued**, the pre-registered next phases are C and D. Both are
  closed by evidence at this checkpoint: `CALIBRATION_JUSTIFIED = NO`,
  `FINE_TUNING = NOT_RUN`. A continuation would have to start from
  `SEQUENCE_B_REVIEW.md` §7, which states the four things a follow-up must beat
  (task encoding, GPU-measured latency, routine coverage as the primary metric,
  and the prohibition on training on this dataset).
