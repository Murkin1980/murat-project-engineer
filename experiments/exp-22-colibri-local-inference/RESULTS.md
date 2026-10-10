# EXP-22 — Colibri local inference / Brio routing: RESULTS

- **Run date:** 2026-10-09 UTC
- **Executor:** Arena (branch `arena/42502a3d-murat-project-engineer`, base `585f078`)
- **Experiment result:** **PARTIAL**
- **Recommendation:** **HOLD**
- **Deep change:** NO
- **Scope:** three bounded checkpoints on Colibri's decision path with the tiny-Laya CI fixture; fully isolated under this directory; no production integration.

This file expresses the already-established experiment result — recorded in
`FINDINGS.md` (2026-10-09) and the committed `evidence/cp0{1,2,3}-results.json` —
in the repository's normal result format. It adds no new claims and changes no
conclusion: every number below is quoted from that committed evidence. It exists
so the canonical registry/result path (and any derived bootstrap view) can carry
the experiment's current state without rediscovery from `FINDINGS.md`.

## Executive result

Colibri's constrained decision path (System One, `POST /v1/systemone`) is
structurally sound and trivially cheap to stand up locally: 66/66 fixture
requests returned HTTP 200, 0 malformed constrained outputs, 22/22 items
exactly deterministic across repeats, 7–13 ms tiny-model latency at ~48 MB
server RSS. What the run did NOT prove is decision *quality*: the released
842 MB Laya checkpoint was unavailable in the original sandbox (HuggingFace
only), so accuracy, determinism and latency against real weights were not
measured. The result is therefore **PARTIAL** with recommendation **HOLD** —
not PASS, and not REUSE_COMPONENT.

## Per-pattern disposition

| # | Pattern | Verdict | Disposition |
|---|---|---|---|
| 1 | CP-01 Brio status classifier (READY/WARNING/BLOCKED) | structural PASS (schema-safe, deterministic, fast); quality OPEN | HOLD — not reusable until released-weight quality is measured |
| 2 | CP-02 Agent routing decision (fixed list) | structural PASS; routing-quality OPEN | HOLD — not reusable until released-weight quality is measured |
| 3 | CP-03 Existing-provider compatibility (Jev-shaped decision client) | MET — base-URL switch works; chat-shaped clients fail closed (400) with a pointer to `/v1/systemone` | REUSE_PATTERN_ONLY — one low-risk decision operation can move behind a Colibri provider; chat generation cannot ride the same adapter |
| — | Colibri as a new repository / control plane / parallel orchestration | REJECT (boundary) | DO_NOT_ADOPT |

## Against the success criteria (README)

| # | Criterion | Result |
|---|---|---|
| 1 | Acceptable quality vs reference | NOT MET — unmeasurable here (random weights); released checkpoint unavailable |
| 2 | Schema/constrained-choice safe | MET — 0 malformed in 68 decision replies + fail-closed 422 |
| 3 | Operationally simpler/cheaper | PARTIAL — tiny path: 4 s build, 48 MB RSS, ms latency; real-checkpoint cost unmeasured locally |
| 4 | Adapter/provider extension, not a parallel platform | YES for the decision operation (Jev shape); NO for chat (fail-closed, by design) |
| 5 | No production source-of-truth/deployment change | MET — fully isolated proof |

## Measured value (from FINDINGS.md §3–§7)

- 66/66 fixture requests HTTP 200; 0 malformed constrained outputs; 22/22 items exactly deterministic across repeats; 7–13 ms tiny-model latency; ~48 MB server RSS; CP-03 probes 200/400/400/200/422 as documented.
- Client-measured latency (tiny toy model, NOT the released-model number): CP-01 min 8.3 / mean 10.5 / max 12.3 ms; CP-02 min 7.1 / mean 9.5 / max 13.1 ms.
- Agreement with expected labels: CP-01 5/12, CP-02 2/10 — NON-INFORMATIVE (random weights, near chance).
- Hardware: 2× Xeon 2.6 GHz, 3 GB RAM, no GPU, localhost-only server; model colibri @ `bf24429` (2026-10-06) + tiny-laya fixture (safetensors sha256 `53627dd9…eb4b4`, matches upstream's pinned hash).
- Released Laya per upstream docs (not measured here): 1.7 GB RAM, 842 MB disk, 219 ms/question laptop CPU.

## Evidence

- `FINDINGS.md` — full run record: bootstrap preflight, model/hardware path, per-CP results, success-criteria mapping, measured value and limits.
- `evidence/cp01-results.json`, `evidence/cp02-results.json`, `evidence/cp03-results.json` — raw machine evidence (36 + 30 decision requests + 5 live compatibility probes).
- `evidence/environment.md` — environment record.
- `evidence/bootstrap/` — EXP-29 bootstrap packet record for this experiment (first real-use run, CP-06 repair, CP-07 rebuild).

## Known limitations / blockers

- Released-weight decision quality is NOT measured: the 842 MB Laya checkpoint is HuggingFace-only and was unreachable from the original sandbox; accuracy, calibration and ambiguity handling remain OPEN until the frozen fixtures run against the released checkpoint.
- All latency/footprint numbers are tiny-Laya CI-fixture numbers (numpy-generated random weights, 2.15 MB), not released-model numbers.
- The Laya checkpoint is English-only (collapses on non-Latin scripts while staying confident).
- This repository currently has no provider seam for a Colibri adapter to plug into (future-architecture socket only), so no integration is authorized by this result.

## Next authorized action

Run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available suitable machine (>= 8 GB RAM) and record accuracy/determinism/latency before any adapter work.
CP-01..CP-03 must not be repeated; this is a bounded quality measurement, not production integration, and no production Colibri integration is authorized.

## Result block (canonical, verbatim from FINDINGS.md)

```
RESULT: PARTIAL
RECOMMENDATION: HOLD
BEST_USE_CASE: Local constrained classification/routing (READY/WARNING/BLOCKED, expert queue routing) via Colibri's System One decision endpoint as an optional provider behind a Jev-shaped call.
MEASURED_VALUE: 66/66 local decision requests HTTP 200 with 0 malformed constrained outputs; 22/22 items exactly deterministic across repeats; 7-13 ms tiny-model latency at ~48 MB server RSS; CP-03 probes 200/400/400/200/422 as documented; decision quality NOT measured (released weights unreachable from sandbox).
NEXT_STEP: Run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available ≥8 GB machine and record accuracy/determinism/latency before any adapter work.
DEEP_CHANGE: NO
```
