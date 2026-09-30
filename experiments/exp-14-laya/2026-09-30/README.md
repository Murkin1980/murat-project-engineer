# EXP-14 — Laya / System One Decision Layer

Checkpoint: `EXP-14-CP-01`
Run date: 2026-09-30 (UTC)
Owning repository: `Murkin1980/murat-project-engineer`
New Idea Filter disposition: `EXPERIMENT` (already recorded; see
`experiments/exp-14-laya-system-one/README.md` and `experiments/EXPERIMENT_REGISTRY.json` → `EXP-14`)
Session branch: `arena/01a0f3b0-murat-project-engineer`
`main` SHA at freeze: `d2ec64531e4cac4f5076263f8317dfaaa36e2a9f`

> **Status of this file:** Sequence A is complete and frozen; Sequence B is in
> progress. `RESULTS.md` carries the verdict. This README is the index.

---

## Question

Can a cheap, fast, non-generative System One model (Laya) safely close a narrow,
repeatable class of MPE triage/routing decisions **without** being given any
authority that belongs to MPE or System Two — while still escalating every
dangerous or ambiguous case?

EXP-14 tests that inside MPE only. It changes no production routing, no
production authority, no existing decision rule and no MPE autonomy setting.

## Read in this order

| File | What it fixes |
|---|---|
| `CONTRACT.md` | decision schema, protected-decision definition, arms, frozen decoding parameters, PASS/FAIL criteria, governance assertions |
| `ORACLE.md` | the frozen oracle rule table with a citation per rule, the precedence conflict that was surfaced rather than hidden, and the three validation gates applied before the freeze |
| `DATASET.md` | the 43 frozen cases, composition, provenance, per-case rationale, and the dataset digest |
| `METHOD.md` | execution order, the Laya-access probe evidence, why an ephemeral CI runner is the Sequence B host, evidence discipline, determinism controls |
| `BASELINE.md` | **Sequence A** results and interpretation |
| `LAYA_ZERO_SHOT.md` | **Sequence B** results |
| `RESULTS.md` | comparison, verdict, governance ledger, handoff |
| `HASHES.txt` | SHA-256 of every artifact |
| `frozen/` | the immutable dataset + its digest |
| `raw/` | baseline outputs, Laya raw outputs, parsed outputs, per-pass metrics, probes, reproducibility records |
| `harness/` | the runnable method (`harness/README.md`) |
| `fixtures/` | pre-experiment repository state and governing-document hashes |

## Execution state

```text
[done]  stage 0  governing docs read; pre-experiment repository state captured
[done]  stage 1  dataset + oracle authored, validated (G1/G2/G3) and FROZEN
                 sha256 aef7d8bfcefd2b4132073eaf52e570aee2b5d5aebf318e5d556f6d4d3803b648
[done]  stage A  deterministic baseline, 3 passes, reproducible, hashed, committed
[done]  stage P  Laya access probed in the authoring sandbox -> INFRASTRUCTURE_BLOCKED
                 (full pinned stack installed; real laya.load() attempted; HF TLS closed)
[ ... ] stage B  Laya zero-shot on an ephemeral CI runner
[ ... ] stage B2 Laya typed-decisions reference arm (secondary, never mixed with B)
[ ... ] stage E  evaluation and verdict
[ ... ] stage C  calibration — only if CONTRACT.md section 9 permits it
[ ... ] stage D  fine-tuning — not run automatically
```

## Headline control numbers (Sequence A)

| | baseline |
|---|---|
| exact case match | 37/43 = **0.8605** |
| exact or safely escalated | 43/43 = **1.0000** |
| protected false negatives | **0** |
| unsafe FAST decisions | **0** |
| routine coverage | 12/12 = **1.0000** |
| escalation recall | 22/22 = **1.0000** |
| median latency | **0.0095 ms** |
| model cost | **0.0 USD (observed, no provider call)** |
| reproducible | **yes** (identical decision vectors, 3 passes) |

The baseline is safe, free and sub-millisecond, but it under-tiers five
DEEP-CHANGE cases to VERIFIED because `scripts/triage_engine.py` has no
deep-change signal for credentials/security, destructive-without-rollback, or
source-of-truth changes that the MPE rule text does cover. Every one of those
still raises a human gate and still escalates. Details and the resulting scope
boundary: `BASELINE.md` sections 3–5.

## Governance

```text
PRODUCTION_CHANGED          = NO
NEW_INFRASTRUCTURE          = NO
DEEP_CHANGE                 = NO
PRODUCTION_ROUTING_CHANGED  = NO
```

All changes live under `experiments/exp-14-laya/`. The single deliberate
exception is the temporary, credential-free, branch-scoped CI workflow used to
reach the pinned checkpoint; it follows the pattern EXP-18 documented and is
removed once the evidence is recorded. See `METHOD.md` section 3 and
`CONTRACT.md` section 10.

`PASS_FOR_NEXT_EXPERIMENT`, if returned, authorises only *considering* a further
bounded experiment. It is not permission to use Laya in production and it grants
Laya no decision authority.
