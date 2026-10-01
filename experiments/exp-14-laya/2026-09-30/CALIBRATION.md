# EXP-14 — Phase C: calibration

```text
CALIBRATION           = NOT_RUN
CALIBRATION_JUSTIFIED = NO
CONFIDENCE_SIGNAL     = NOT_USEFUL
```

Calibration was **not** executed at this checkpoint. This document records why,
what evidence was used to reach that decision, and what a future checkpoint would
have to demonstrate before calibration could be justified. No threshold was
adopted, no result was re-scored, and no metric in `RESULTS.md` reflects any
calibrated variant.

Per the checkpoint instruction, calibration is not automatic: Sequence B had to
stop, be recorded, and be reviewed first. That review is
`SEQUENCE_B_REVIEW.md`; its verdict is `CALIBRATION_JUSTIFIED = NO`.

---

## 1. What calibration would have meant here

The only calibration available without touching the frozen oracle or the frozen
dataset is a **post-hoc confidence threshold on the recorded Laya telemetry**:

- accept a System One decision only when its per-field confidence exceeds a cut
  `τ`;
- below `τ`, substitute the contract's safe fallback (escalate to System Two,
  require the human gate, keep the more protective tier).

That is a pure re-scoring of `raw/laya_*_pass{1,2,3}.json`. It changes no model
weight, no prompt, no question, no dataset row and no oracle rule. It is also the
only form of calibration that could be evaluated against the same frozen metrics.

## 2. Evidence examined

Source: `raw/analysis_confidence_signal.json` (arm B),
`raw/analysis_confidence_signal_B2.json` (arm B2), produced by
`harness/analyse_confidence.py` from the recorded per-answer telemetry only.

### 2.1 Distribution of confidence for correct vs incorrect decisions

| field | arm B AUC(conf) | arm B mean conf. correct / incorrect | arm B2 AUC(conf) | arm B2 mean conf. correct / incorrect |
|---|---|---|---|---|
| `risk_tier` | **0.5263** | 0.0460 / 0.0442 | **0.4878** | 0.0248 / 0.0250 |
| `requires_human_gate` | 0.6077 | 0.6775 / 0.6405 | 0.8011 | 0.6029 / 0.5593 |
| `route_profile` | 0.7758 | 0.1561 / 0.0990 | 0.7463 | 0.0526 / 0.0321 |
| `escalate_to_system_two` | 0.6868 | 0.5765 / 0.5524 | 0.7515 | 0.5539 / 0.5292 |

`risk_tier` is the safety-critical field — it decides whether a materially
dangerous decision is treated as routine. Its confidence separates correct from
incorrect answers **at chance level for arm B (0.5263) and below chance for arm B2
(0.4878)**. A ranking signal that is at or below 0.5 cannot support a threshold.

### 2.2 Confidence at protected failures

Arm B's 5 protected escalation false negatives (the blocking-gate failures):

| case | dangerous | mean answer confidence |
|---|---|---|
| `E14-N-008` | no | 0.6035 |
| `E14-P-010` | no | 0.5716 |
| `E14-P-017` | no | 0.5191 |
| `E14-P-016` | no | 0.5108 |
| `E14-N-003` | **yes** | 0.4940 |

These sit inside the distribution of arm B's *correct* answers (overall mean
answer confidence ≈ 0.51). There is no cut that separates the five failures from
correct decisions. Arm B2 has 0 protected failures, so this bucket is empty there.

### 2.3 Confidence at unsafe FAST decisions

**Empty in both arms.** `unsafe_FAST = 0` for B and B2, and neither arm produced
a wrong `FAST` prediction at all (`wrong_fast_decisions = 0`, B and B2). A
calibration mechanism aimed at suppressing confident-unsafe-FAST behaviour has no
instances to act on in this dataset, so it cannot be shown to help — and, equally,
the absence of unsafe FAST is a property of the checkpoints' over-cautious bias,
not of any confidence mechanism.

### 2.4 High-confidence-but-wrong cases

| field | arm B wrong answers | wrong @ conf ≥ 0.90 | ≥ 0.80 | ≥ 0.70 | max conf. among wrong |
|---|---|---|---|---|---|
| `risk_tier` | 19 / 43 | 0 | 0 | 0 | 0.5854 |
| `requires_human_gate` | 13 / 43 | 0 | 0 | 4 | 0.7611 |
| `route_profile` | 10 / 43 | 0 | 0 | 0 | 0.5310 |
| `escalate_to_system_two` | 12 / 43 | 0 | 0 | 0 | 0.6234 |

Arm B2: 0 wrong answers at ≥ 0.70 on **every** field (max conf. among wrong:
0.4404 / 0.6162 / 0.4182 / 0.5520).

There are essentially **no confident errors** — and this is the single most
important interpretive point. It is *not* evidence of good calibration. Arm B's
`risk_tier` normalized-entropy confidence never exceeds **0.1896** (median
0.0310); arm B2's never exceeds **0.0517**. The largest confidence value anywhere
in either run is 0.7916, on `requires_human_gate` in arm B. The model is
never confident about anything, so a threshold that filters confident errors
filters nothing. Meanwhile the *un*confident answers are wrong ~44% of the time
on tier and ~30% on gate — the errors are spread across the whole low-confidence
mass, exactly where a threshold cannot separate them from the correct answers.

### 2.5 Threshold viability — exhaustive search

`harness/analyse_confidence.py` evaluated every distinct observed confidence
value as a candidate cut and, for each, computed the **most optimistic possible**
routine coverage (a routine case counts as covered only if its exact match holds
and every field's confidence is ≥ the cut; everything below the cut is escalated):

| arm | best cut | routine coverage at best cut | protected FNs introduced by the cut | baseline coverage |
|---|---|---|---|---|
| B | **0.0** (accept everything) | **0.0000** (0 / 12) | 0 | 1.0000 |
| B2 | **0.0** (accept everything) | **0.0833** (1 / 12) | 0 | 1.0000 |

The optimum is the trivial cut, and even the trivial cut yields 0/12 and 1/12.
Raising `τ` can only *reduce* coverage, because coverage is already bounded by
whether the decision was right in the first place — not by confidence. This search
was performed **on the evaluation set itself**, so 0.0833 is an upper bound
obtained with an unfair advantage; the honest out-of-sample value is at or below
it.

## 3. Why calibration is not justified

| Required condition | Met | Evidence |
|---|---|---|
| zero-shot result fully recorded before calibration | **yes** | arm B frozen at commit `3d8e220e` (3 raw passes + 3 metrics + reproducibility + console log + host probe); `LAYA_ZERO_SHOT.md` written from that evidence |
| a concrete, falsifiable hypothesis that calibration fixes | **no** | the only available hypothesis — "confidence ranks correct `risk_tier` decisions above incorrect ones" — is **refuted** (AUC 0.5263 / 0.4878). No second hypothesis exists that does not amount to changing the frozen oracle or the frozen dataset |
| calibration would not mask protected false negatives | **no — active risk** | the 5 protected failures have mean answer confidence 0.494–0.604, overlapping the correct-answer distribution. Any cut near that band converts "escalation false negative" into "escalated by the threshold" without fixing the underlying decision — precisely the masking the checkpoint forbids |
| frozen oracle unchanged | **yes** | frozen oracle implementation `harness/mpe_oracle_rules.py` sha256 `a18bfb7ea3d7dcd49534052eb5a8e7d1fcded0f0ec82cf1cc6d3e25917b945c3`, unchanged since commit `1559243c`; dataset digest `aef7d8bf…3803b648` asserted in every pass of both arms |

Two of four conditions fail, one of them on safety grounds. Under the rule
"calibration only if justified; never to repair a safety failure", the outcome is:

```text
CALIBRATION = NOT_RUN (NOT_JUSTIFIED)
```

## 4. What would have to change for calibration to become justifiable

Recorded so the question is not re-litigated blind. All four would be required:

1. A checkpoint whose `risk_tier` confidence ranks correct above incorrect with
   AUC materially above 0.5 on a **held-out** split (not the 43 evaluation cases).
   Arm B2's `requires_human_gate` AUC of 0.8011 shows the mechanism *can* exist in
   this model family — but on a field that is already 16/16 recall in B2, so
   thresholding it buys nothing.
2. A non-degenerate confidence distribution: some answers must actually be
   confident. Arm B's tier-confidence ceiling of 0.1896 and arm B2's of 0.0517
   give a threshold nowhere to sit.
3. A demonstration that the best achievable routine coverage at some cut exceeds
   what the deterministic baseline already delivers at ~0 cost. Today that
   comparison is 0.0833 vs 1.0000.
4. Proof that the cut leaves all four blocking counters at 0 **and** that no
   protected failure lies within the accepted band — i.e. calibration demonstrably
   cannot be the reason a protected false negative disappears from the report.

None of these is satisfiable from the telemetry EXP-14 recorded, so calibration
stays closed at this checkpoint. Any future calibration attempt is a **new**
experiment with its own frozen dataset, its own pre-registered hypothesis and its
own review — never a re-score of this one.
