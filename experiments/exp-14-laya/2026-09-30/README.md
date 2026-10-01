# EXP-14 — Laya / System One Decision Layer

Checkpoint: `EXP-14-CP-01`
Run date: 2026-09-30 (UTC) · Closed: 2026-10-01 (UTC)
Owning repository: `Murkin1980/murat-project-engineer`
New Idea Filter disposition: `EXPERIMENT` (already recorded; see
`experiments/exp-14-laya-system-one/README.md`,
`experiments/exp-14-laya-system-one/PRE_REGISTRATION.json` and
`experiments/EXPERIMENT_REGISTRY.json` → `EXP-14`)
Session branch: `arena/01a0f3b0-murat-project-engineer`
`main` SHA at freeze: `d2ec64531e4cac4f5076263f8317dfaaa36e2a9f`

> **Status of this checkpoint: CLOSED.** Every pre-registered stage that was
> authorised to run has run; calibration and fine-tuning were evaluated and
> deliberately **not** run. `RESULTS.md` carries the verdict:
> **`RESULT = FAIL`, `PASS_FOR_NEXT_EXPERIMENT = NO`.** This README is the index.

---

## Question

Can a cheap, fast, non-generative System One model (Laya) safely close a narrow,
repeatable class of MPE triage/routing decisions **without** being given any
authority that belongs to MPE or System Two — while still escalating every
dangerous or ambiguous case?

EXP-14 tested that inside MPE only. It changed no production routing, no
production authority, no existing decision rule and no MPE autonomy setting.

## Answer

**No — not with the checkpoints and encoding available at this checkpoint.**

Laya produced valid structured output on every case (0 invalid outputs), never
downgraded a protected case to `FAST`, and never produced an unsafe FAST decision.
But zero-shot it matched MPE's frozen oracle on **7 of 43** decisions, closed **0
of 12** routine cases, dropped the required System Two hand-off on **5 protected**
cases (tripping the blocking safety gate), and cost **3.37 s** per decision against
**0.0095 ms** for the deterministic control. The vendor's fine-tuned
`typed-decisions` checkpoint (secondary reference arm B2) passes the safety gate
but matches only **5 of 43** decisions and closes **1 of 12** routine cases, at
5.06 s per decision. Its confidence values carry no usable safety signal
(`risk_tier` confidence AUC 0.5263 / 0.4878 — at or below chance), so calibration
is not justified and was not run; fine-tuning is forbidden at this checkpoint and
was not run.

```text
RESULT                   = FAIL            B_MODEL_RESULT        = FAIL
PASS_FOR_NEXT_EXPERIMENT = NO              B_SAFETY_RESULT       = FAIL
FAILURE_CLASSIFICATION   = MODEL_FAIL      B2_RESULT             = FAIL
CONFIDENCE_SIGNAL        = NOT_USEFUL      CALIBRATION_JUSTIFIED = NO
CALIBRATION              = NOT_RUN         FINE_TUNING           = NOT_RUN
```

## Read in this order

| File | What it fixes / reports |
|---|---|
| `CONTRACT.md` | decision schema, protected-decision definition, arms, frozen decoding parameters, PASS/FAIL criteria, governance assertions — all frozen **before** any Laya call |
| `ORACLE.md` | the frozen oracle rule table with a citation per rule, the precedence conflict that was surfaced rather than hidden, and the three validation gates (G1 43/43, G2 25/25, G3 43/43) applied before the freeze |
| `DATASET.md` | the 43 frozen cases, composition, provenance, per-case rationale, and the dataset digest |
| `METHOD.md` | execution order, the Laya-access probe evidence, why an ephemeral CI runner is the Sequence B host, evidence discipline, determinism controls |
| `BASELINE.md` | **Sequence A** — deterministic control: exact 0.8605, gate PASS, routine coverage 1.0000, 0.0095 ms, $0.0 |
| `LAYA_ZERO_SHOT.md` | **Sequence B** — Laya zero-shot (repo root): exact 0.1628, blocking gate **FAIL**, routine coverage 0.0000, per-case table, error mode |
| `B2.md` | **Sequence B2** — `typed-decisions` reference arm: `B2_DEFECT` / `B2_FIX` / `B2_FIX_DIFF` + commit SHAs, then exact 0.1163, gate PASS, routine coverage 0.0833 |
| `SEQUENCE_B_REVIEW.md` | **the stop-and-review record**: `B_MODEL_RESULT`, `B_SAFETY_RESULT`, `B2_RESULT`, `CALIBRATION_JUSTIFIED`, and the recommended next bounded experiment |
| `CALIBRATION.md` | **phase C — `NOT_RUN`, `NOT_JUSTIFIED`**: the confidence evidence (distributions, protected-failure confidence, unsafe-FAST confidence, high-confidence-wrong, exhaustive threshold search) |
| `FINE_TUNING.md` | **phase D — `NOT_RUN`**: why training is closed here and why this dataset must not become a training set |
| `RESULTS.md` | full three-arm comparison, criterion-by-criterion verdict, failure classification, governance ledger, disclosed deviations, reproducibility, handoff |
| `HASHES.txt` | SHA-256 of every artifact + proof that 36/36 production and governing files are unchanged since `d2ec6453` |
| `frozen/` | the immutable dataset + its digest |
| `raw/` | baseline outputs, Laya raw outputs for both arms (3 passes each), per-pass metrics, reproducibility records, access probes, both console logs, the attempt-1 blocked record, and both confidence analyses |
| `harness/` | the runnable method (`harness/README.md`) |
| `fixtures/` | pre-experiment repository state, governing-document hashes, and `B2_FIX_DIFF.patch` |

Cross-reference: `experiments/exp-14-laya-system-one/EXECUTION_RECORD.md` (and
`.json`) is the pointer filed in the pre-registration directory. The
pre-registration itself was **not** edited after execution.

## Execution state

```text
[done]  stage 0  governing docs read; pre-experiment repository state captured
[done]  stage 1  dataset + oracle authored, validated (G1/G2/G3) and FROZEN
                 sha256 aef7d8bfcefd2b4132073eaf52e570aee2b5d5aebf318e5d556f6d4d3803b648
[done]  stage A  deterministic baseline, 3 passes, reproducible, hashed, committed
[done]  stage P  Laya access probed in the authoring sandbox -> INFRASTRUCTURE_BLOCKED
                 (full pinned stack installed; real laya.load() attempted; HF TLS closed)
[done]  stage B  Laya zero-shot on an ephemeral CI runner (run 36765874259), 3 passes,
                 reproducible -> MODEL_FAIL, blocking safety gate FAIL
[done]  stage B2 typed-decisions reference arm. attempt 1 (run 36765874259)
                 INFRASTRUCTURE_BLOCKED by a harness pin defect; minimal fix in
                 commit 2acd481d; attempt 2 (run 36767177438) 3 passes,
                 reproducible -> FAIL on criteria 2/3/4, gate PASS
[done]  stage E  evaluation, confidence analysis, SEQUENCE_B_REVIEW.md, RESULTS.md
[done]  stage C  calibration evaluated -> NOT_JUSTIFIED -> NOT_RUN (no threshold adopted)
[done]  stage D  fine-tuning -> NOT_RUN (forbidden at this checkpoint; precondition unmet)
[done]  stage X  temporary CI workflow deleted; registry/status/changelog records updated;
                 HASHES.txt regenerated; checkpoint closed
[ n/a ] stage J  Jev optional reference comparator -> NOT_RUN (closed third-party
                 service; would require new credentials/infrastructure)
```

## Headline numbers

| | **A baseline (control)** | **B Laya zero-shot** | **B2 Laya typed-decisions** |
|---|---|---|---|
| exact case match | **0.8605** | 0.1628 | 0.1163 |
| protected false negatives | **0** | **0** | **0** |
| unsafe FAST decisions | **0** | **0** | **0** |
| protected escalation false negatives | **0** | **5** | 0 |
| blocking safety gate | **PASS** | **FAIL** | PASS |
| routine coverage (of 12) | **1.0000** | 0.0000 | 0.0833 |
| escalation recall | **1.0000** | 0.7727 | 1.0000 |
| median latency | **0.0095 ms** | 3367.8 ms | 5056.2 ms |
| model cost (observed) | **0.0 USD** | 0.0 USD | 0.0 USD |
| reproducible, 3 passes | **yes** | yes | yes |

The baseline is safe, free and sub-millisecond, but it under-tiers five
`DEEP-CHANGE` cases to `VERIFIED` because `scripts/triage_engine.py` has no
deep-change signal for credentials/security, destructive-without-rollback, or
source-of-truth changes that the MPE rule text does cover. Every one of those
still raises a human gate and still escalates, so the baseline's blocking gate
passes. Details and the resulting scope boundary: `BASELINE.md` §3–5. That gap is
a **rule-coverage** problem in the deterministic engine and is the cheapest thing
this checkpoint found worth fixing — but fixing it touches the production decision
path, so it requires its own New Idea Filter decision and was **not** done here.

## Governance

```text
PRODUCTION_CHANGED          = NO
NEW_INFRASTRUCTURE          = NO
DEEP_CHANGE                 = NO
PRODUCTION_ROUTING_CHANGED  = NO
AUTHORITY_CHANGED           = NO
```

All experiment changes live under `experiments/exp-14-laya/`. Outside it, EXP-14
wrote only evidence records: the two pointer files in
`experiments/exp-14-laya-system-one/`, `experiments/EXPERIMENT_REGISTRY.json`,
`STATUS.md` and `CHANGELOG.md`. `HASHES.txt` §3 proves 36/36 production and
governing files — including `scripts/triage_engine.py`, the triage contracts,
`gates/registry.yaml`, the playbooks, experts, teams and routing references — are
digest-identical to `main` @ `d2ec6453`.

The single deliberate exception during execution was a temporary, credential-free,
branch-scoped CI workflow used to reach the pinned checkpoint from an ephemeral
runner (the authoring sandbox cannot reach Hugging Face and cannot host a 421M
model). It follows the pattern EXP-18 documented and is **deleted in the closing
commit**, so no new infrastructure remains in the repository. See `METHOD.md` §3
and `CONTRACT.md` §10.

No Laya decision was routed anywhere. No model was given authority over any MPE
decision. `integration_authorized` remains `false`.

`PASS_FOR_NEXT_EXPERIMENT`, had it been returned, would have authorised only
*considering* a further bounded experiment — not production use of Laya and not
any decision authority for it. It was not returned.
