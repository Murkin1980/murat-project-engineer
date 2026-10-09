# EXP-22 — Results: Colibri local inference / Brio routing

- RESULT: **PARTIAL**
- RECOMMENDATION: **HOLD**
- DEEP_CHANGE: **NO**
- Primary disposition: **EXPERIMENT** (unchanged from `README.md`)
- Checkpoints: **CP-01, CP-02, CP-03 executed** (CP-03 ran because CP-01/CP-02 showed the structural signal)
- Run date: 2026-10-09 (UTC)
- Branch: `arena/42502a3d-murat-project-engineer` (base `585f078b679a1d7d5a3e36afe8c10dc22b978670`)
- Executor: Arena. Full record: `FINDINGS.md`; measurements: `evidence/cp01-results.json`,
  `evidence/cp02-results.json`, `evidence/cp03-results.json`, `evidence/environment.md`
- No new repository, production deployment, provider switch, control plane, secrets,
  background service, or deep-change.

Every number below is copied from the committed EXP-22 evidence (`FINDINGS.md` +
`evidence/*`, tiny-Laya CI fixture, colibri @ `bf24429`); nothing here re-runs or
reinterprets the experiment.

## CP-01 — Brio status classifier (READY/WARNING/BLOCKED): COMPLETE

- Fixture: 12 frozen MPE status blurbs + rubric + System One `choice` question;
  `harness/run_cp.py --fixture fixtures/cp01.json --repeats 3` → 36 requests.
- Latency (client-measured, tiny toy model): min 8.3 ms, mean 10.5 ms, max 12.3 ms.
- Malformed outputs: **0/36**; every reply `choice` ∈ {READY, WARNING, BLOCKED} with
  probability keys summing ≈ 1 and `choice` = argmax.
- Determinism: **12/12** items byte-identical across 3 repeats.
- Agreement with expected: 5/12 — NON-INFORMATIVE (random weights; near chance).
- Verdict: structural PASS (schema-safe, deterministic, fast); quality OPEN.

## CP-02 — Agent routing decision (fixed list): COMPLETE

- Fixture: 10 frozen MPE tasks → fixed destinations {architect, coder, researcher,
  reviewer} from `experts/*.md`; no new agents; 30 requests.
- Latency: min 7.1 ms, mean 9.5 ms, max 13.1 ms. Malformed: **0/30**. Determinism: **10/10**.
- Agreement: 2/10 — NON-INFORMATIVE (random weights). Ambiguity handling not measurable
  here; each decision is structurally `output_tokens: 0, cost: 0` local.
- Verdict: structural PASS; routing quality OPEN (same blocker as CP-01).

## CP-03 — Existing-provider compatibility: COMPLETE

Live probes (`harness/probe_cp03.py` → `evidence/cp03-results.json`): `GET /v1/models`
200 (OpenAI list shape); `POST /v1/chat/completions` 400 (OpenAI-style, points to
`/v1/systemone`); `POST /v1/messages` 400 (Anthropic-style); `POST /v1/systemone`
200 (typed reply); bad question type 422 with field-level validation. A Jev-shaped
decision client switches by base URL; chat-shaped clients fail closed — one low-risk
decision operation can move behind a Colibri provider without redesigning the caller;
chat generation cannot ride the same adapter. No production routing was touched.

## Measured value (established)

66/66 fixture requests HTTP 200; 0 malformed constrained outputs; 22/22 items exactly
deterministic; 7–13 ms tiny-model latency at ~48 MB server RSS; 5/5 CP-03 probes
200/400/400/200/422 as documented. The constrained-decision property is *structural*
(holds even with random weights); the local serving path is trivially cheap to stand up;
the compatibility boundary is crisp.

## Against the success criteria (README)

1. Acceptable quality vs reference: **NOT MET** (unmeasurable here — random weights).
2. Schema/constrained-choice safe: **MET** (0 malformed in 68 decision replies + fail-closed 422).
3. Operationally simpler/cheaper: **PARTIAL** (tiny path cheap; real-checkpoint cost unmeasured locally).
4. Expressible as adapter/provider extension: **YES** for the decision operation (Jev shape); **NO** for chat (fail-closed, by design).
5. No prod source-of-truth/deployment change: **YES** (fully isolated proof).

Not all PASS conditions are true → not PASS. Per `README.md` final-decision vocabulary
(REUSE_COMPONENT / HOLD / REJECT) the recommendation is **HOLD**.

## Per-pattern disposition

| # | Pattern | Verdict | Disposition |
|---|---|---|---|
| 1 | Local constrained decision endpoint (Colibri System One / Brio `choice`) behind a Jev-shaped call | PROVEN structurally (quality OPEN) | **HOLD** — candidate optional provider; adopt only after the released-weight quality run |
| 2 | OpenAI/Anthropic chat-shaped adapter for decision models | REJECT (fail-closed 400 by design) | **KEEP_EXISTING** — do not extend the decision adapter to chat completions |

## Known limitations / blockers

- Decision quality (accuracy, calibration, ambiguity handling) is **NOT measured** on released weights: the 842 MB Laya checkpoint was HuggingFace-only and unreachable from the original sandbox. It stays the blocker for any adoption decision.
- Tiny-Laya numbers (7–13 ms, ~48 MB RSS, random CI-fixture weights) are structural only — not released-model quality or latency (upstream released path: 219 ms/question, laptop CPU).
- Laya is English-only (collapses on non-Latin scripts while staying confident); routing probability thresholds stay uncalibrated in this run.
- This repository currently has no provider seam for the adapter to plug into (future-architecture socket only); no production integration is authorized.

## Next authorized action

Run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available ≥8 GB machine and record accuracy/determinism/latency before any adapter work; no production integration is authorized.

CP-01, CP-02 and CP-03 are already executed — do not repeat them; the released-weight
run is a new measurement against the same frozen fixtures (`fixtures/cp01.json`,
`fixtures/cp02.json`).
