# EXP-14 — Phase D: bounded fine-tuning

```text
FINE_TUNING = NOT_RUN
```

Fine-tuning was **not** executed at this checkpoint, and it is **forbidden** at
this checkpoint by the pre-registered plan regardless of how weak the accuracy
result is. No training run was started, no training split was created, no
checkpoint was produced, and no weight file was written anywhere.

This is a deliberate record, not an omission.

---

## 1. Why fine-tuning is closed here

`experiments/exp-14-laya-system-one/README.md` (pre-registered 2026-09-21,
`PRE_REGISTRATION.json` phase `EXP-14D_BOUNDED_FINE_TUNE_CONDITIONAL`) states the
condition explicitly:

> ### EXP-14D — bounded fine-tune
> Run only if EXP-14B/C show enough signal to justify training.

EXP-14B showed no such signal and EXP-14C was not justified
(`CALIBRATION.md`). Specifically:

| Precondition for training | Status | Evidence |
|---|---|---|
| B/C show enough signal to justify training | **not met** | B exact match 0.1628, routine coverage 0/12, blocking safety gate FAIL; B2 exact match 0.1163, routine coverage 1/12. Neither arm approaches the 0.90 exact-match requirement |
| a confidence signal worth calibrating exists | **not met** | `risk_tier` confidence AUC 0.5263 (B) / 0.4878 (B2) — at or below chance; `CONFIDENCE_SIGNAL = NOT_USEFUL` |
| a training split exists that is disjoint from evaluation | **not met — and must not be created from this dataset** | see §2 |
| the safety failure is one that training could plausibly address without masking it | **not assessable at this checkpoint** | B's 5 protected escalation false negatives were produced by a model that never saw MPE's rules; whether a specialised head fixes them is a *new* question requiring a *new* frozen dataset |

The checkpoint instruction is stricter than the pre-registration and was followed
as written: fine-tuning is not automatic and is forbidden at this checkpoint even
if accuracy is weak. Weak accuracy is exactly the situation in which training
would be most tempting and least informative.

## 2. The evaluation dataset must not become a training dataset

The frozen dataset is **43 cases** (`frozen/dataset_v1.json`, sha256
`aef7d8bfcefd2b4132073eaf52e570aee2b5d5aebf318e5d556f6d4d3803b648`), drawn from a
single pre-existing MPE corpus (`datasets/exp-12-backtest.json`,
`experiments/exp-13/tasks_v2.json`, and the governing rule text). It was frozen as
an **evaluation** set.

Splitting 43 cases into train/held-out would leave roughly 30 training examples
and ~13 evaluation examples, of which ~4 would be routine — far too few to
distinguish a real improvement from noise, and it would invalidate every number
recorded in `BASELINE.md`, `LAYA_ZERO_SHOT.md`, `B2.md` and `RESULTS.md`, because
those numbers are defined against *all 43 cases being unseen*.

Held-out status at this checkpoint: **no case was used to fit anything.** No
calibration threshold was adopted, no fine-tuning was run, and both arms are
zero-shot with respect to MPE (`few_shot_examples_supplied: 0`,
`oracle_values_supplied: false`, `calibration_applied: false` in every recorded
pass). The pre-registration's `dataset.held_out_required: true` is therefore
satisfied in substance for EXP-14-CP-01: all 43 cases are held out from the
candidate. It would **not** be satisfied if any of them were later used for
training, which is why that is prohibited here rather than left implicit.

## 3. What a future fine-tuning experiment would have to do differently

Recorded for hand-off. None of this was executed and none of it modifies EXP-14.

1. **A new, larger, separately frozen dataset** — a training split and a held-out
   evaluation split drawn from *different* MPE evidence than the 43 cases here, so
   this checkpoint's numbers remain valid and the new ones are not contaminated.
   The pre-registration's minimum of 30 cases applies per split, not overall.
2. **A new pre-registration** with its own New Idea Filter disposition, its own
   oracle frozen before training, and its own automatic-fail conditions. EXP-14D is
   a phase of a plan, not a licence to train on whatever is at hand.
3. **Evidence that B2's safety behaviour generalises.** B2 (`typed-decisions`)
   reached gate recall 16/16 and escalation recall 22/22 with 0 blocking failures,
   which is the only positive safety signal in this checkpoint — but it came with
   23 gate false positives and 10 escalation false positives, i.e. it is close to
   "always escalate". A fine-tune aimed at routine coverage must be shown not to
   trade that back.
4. **Compute and provenance controls**: pinned base revision, pinned training
   configuration, recorded training data digest, and no automatic promotion of the
   resulting checkpoint into anything with decision authority.
5. **The efficiency question answered on real hardware.** Training and evaluation
   both need a GPU; this checkpoint could only observe CPU inference (3.4–5.1 s per
   decision), so no efficiency claim in either direction was made.

## 4. Recorded state

```text
phase                       = EXP-14D_BOUNDED_FINE_TUNE_CONDITIONAL
FINE_TUNING                 = NOT_RUN
justification_for_not_running = precondition unmet (B/C showed no signal) and explicitly forbidden at this checkpoint
training_split_created      = NO
weights_written             = NO
checkpoint_produced         = NO
evaluation_dataset_used_for_training = NO
dataset_digest_after_phase_D = aef7d8bfcefd2b4132073eaf52e570aee2b5d5aebf318e5d556f6d4d3803b648 (unchanged)
```
