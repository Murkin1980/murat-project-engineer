# EXP-22 — Colibri local inference / Brio routing: FINDINGS

Date: 2026-10-09. Executor: Arena. Branch: `arena/42502a3d-murat-project-engineer`.
Base: `585f078b679a1d7d5a3e36afe8c10dc22b978670` (fresh main, HEAD == main == origin/main).

## 0. Bootstrap preflight (first real-use run of the EXP-29 harness)

- Generated a packet for EXP-22/CP-01 with the unmodified EXP-29 builder:
  JSON 8097 B + MD 6907 B, 7 source refs.
- Verification: **REJECTED** (`missing_stop_rules`), identically on the
  mandated regeneration. All other checks passed (`matches_rebuild`,
  `source_digests_match` true, `field_diffs` empty): **not a source
  conflict — a harness parser-coverage defect**.
- Packet **REFUSED** (not used as authority); all EXP-22 boundaries were taken
  directly from canonical files. The safety check was not bypassed.
- Cost before first useful EXP-22 action: 9 files / 134,732 B / 16 tool ops;
  rediscovery prevented: none.
- Separate harness findings (EXP-29 not modified): **H-1** stop-rule parser
  misses real `## Boundaries` / `## Failure / stop criteria` sections →
  false REJECTED; **H-2** renderer hardcodes `(from EXP-27 RESULTS.md)`
  labels for every experiment; **H-3** checkpoint-chain/disposition parsers
  read only `ARENA_TASK.md` (EXP-22 declares both in `README.md` → empty).
- Full record: `evidence/bootstrap/FIRST_REAL_USE.md` (+ refused packet,
  `verify.json`, `verify_retry.json`).

## 1. Before changing code (report)

- **Existing component to extend/reuse:** none with an inference-provider
  seam. Verified by inspection: the repo has no OpenAI/Anthropic/LLM client
  abstraction (grep over `scripts/`, `tests/` finds only cost/usage metering
  and a Router *log importer*). Functional analogues used as reference:
  `scripts/triage_engine.py` (deterministic rules triage), `experts/*.md`
  (bounded Expert contracts = CP-02 fixed destinations),
  `docs/architecture/MURAT_AI_ORCHESTRATOR_FUTURE_ARCHITECTURE.md`
  Execution Plane ("optional provider adapters or experiments" — the
  sanctioned future socket). `docs/CONTEXT_PROVIDERS.md` is explicitly
  doc-only ("does not define a runtime interface").
- **Why no duplication:** isolated stdlib harness + frozen fixtures under
  this directory only; upstream clone outside the repo, uncommitted; no
  production file touched; no Router/orchestrator logic replicated.
- **Files added (all under `experiments/exp-22-colibri-local-inference/`):**
  `fixtures/cp01.json`, `fixtures/cp02.json`, `harness/run_cp.py`,
  `harness/probe_cp03.py`, `evidence/environment.md`,
  `evidence/cp01-results.json`, `evidence/cp02-results.json`,
  `evidence/cp03-results.json`, `evidence/bootstrap/*`, `FINDINGS.md`.
- **Deep-change trigger:** NO. No new repo/service/deployment, no
  provider switch, no secrets, no Router change, no persistent service
  (test server stopped after the run).

## 2. Model/hardware path chosen

Smallest supported path sufficient for the experiment: Colibri's **decision
(Brio/System One) path** with the **tiny-Laya CI fixture** (numpy-generated
random weights, deterministic SEED 20261002, 2.15 MB) served by `coli serve`
on CPU. Rationale: the decision endpoint (`POST /v1/systemone`, Laya
421M / GLiNER2.5-Decide) is the exact shape CP-01/CP-02 need (typed
choice, calibrated probabilities, no parsing); chat-model paths need
≥22 GB disk and ≥8 GB RAM and are oversized for constrained routing.
Released weights (842 MB) are HuggingFace-only and unreachable from this
sandbox, so the real-checkpoint quality run is NOT RUN (blocked by
environment, not by Colibri).

- Model + revision: colibri @ `bf24429` (2026-10-06) + tiny-laya fixture
  (safetensors sha256 `53627dd9…eb4b4`, matches upstream's pinned hash);
  upstream oracle `tests.test_laya_tiny + tests.test_decision_serve`:
  25 OK / 2 skipped on this machine.
- Hardware: 2× Xeon 2.6 GHz, 3 GB RAM, no GPU, localhost-only server.
- Footprint (tiny path): server RSS ~48 MB total, peak HWM ~35 MB;
  released Laya per upstream docs: 1.7 GB RAM, 842 MB disk, 219 ms/question
  laptop CPU.

## 3. CP-01 — Brio status classifier (READY/WARNING/BLOCKED)

- Fixture: 12 frozen MPE status blurbs + written rubric + System One `choice`
  question; reference = deterministic keyword baseline, verified to
  reproduce all 12 expected labels (one rubric bug found and fixed
  in-harness: "0 failed" tripping the "fail" keyword).
- Commands: `harness/run_cp.py --fixture fixtures/cp01.json --repeats 3`
  → `evidence/cp01-results.json` (36 requests).
- Latency (client-measured): min 8.3 ms, mean 10.5 ms, max 12.3 ms
  (tiny toy model; NOT the released-model number).
- Malformed outputs: **0/36**. Every reply: `choice` ∈ {READY, WARNING,
  BLOCKED}, probability keys exactly the options, sum ≈ 1, choice = argmax,
  confidence + usage present.
- Determinism: **12/12 items** byte-identical choice+probabilities across
  3 repeats.
- Agreement with expected: 5/12 — NON-INFORMATIVE (random weights; near
  chance 33%). Quality vs reference: NOT MEASURED (needs real checkpoint).
- Failure modes observed: none structural. Notable: near-uniform
  probabilities (confidence ~0.03–0.05) correctly reflect random weights —
  the model reports uncertainty rather than bluffing.
- Verdict: structural PASS (schema-safe, deterministic, fast); quality OPEN.

## 4. CP-02 — Agent routing decision (fixed list)

- Fixture: 10 frozen MPE tasks → fixed destinations {architect, coder,
  researcher, reviewer} from `experts/*.md`; no new agents; rubric +
  keyword reference reproducing all 10 expected labels.
- Commands: same harness, `fixtures/cp02.json` → `evidence/cp02-results.json`
  (30 requests).
- Latency: min 7.1 ms, mean 9.5 ms, max 13.1 ms. Malformed: **0/30**.
  Determinism: **10/10**. Agreement: 2/10 — NON-INFORMATIVE (random weights).
- Ambiguity handling: not measurable with random weights (all outputs
  near-uniform); the probability+confidence channel exists for thresholding
  but is uncalibrated here.
- Token/cloud-cost avoided: 0 measured (no cloud reference calls were made
  or avoided in this sandbox run); structurally each decision is
  `output_tokens: 0, cost: 0` local.
- Verdict: structural PASS; routing-quality OPEN (same blocker as CP-01).

## 5. CP-03 — Existing-provider compatibility (ran: CP-01/02 showed the structural signal)

Live probes against the running server (`harness/probe_cp03.py` →
`evidence/cp03-results.json`):

| probe | result |
|---|---|
| `GET /v1/models` | 200, OpenAI list shape; model advertises `capabilities: [systemone, decision]` |
| `POST /v1/chat/completions` | 400 OpenAI-style error, points to `/v1/systemone` (decision models don't generate) |
| `POST /v1/messages` (Anthropic shape) | 400 Anthropic-style error, points to `/v1/systemone` |
| `POST /v1/systemone` (Jev shape) | 200, full typed reply (choice + probabilities + confidence + usage) |
| `POST /v1/systemone` (bad question type) | 422 with precise field-level validation error |

Compatibility boundary precisely established: a **Jev-shaped decision
client switches by base URL** (upstream's SDK claim; reply shape verified
live); an **OpenAI/Anthropic chat-shaped client does NOT get completions**
from decision models — fail-closed 400 with a pointer, not silent wrong
output. So one low-risk *decision* operation can move behind a Colibri
provider without redesigning the caller; chat generation cannot ride the
same adapter. No production routing was touched.

## 6. Against the success criteria (README)

1. Acceptable quality vs reference: NOT MET (unmeasurable here — random weights).
2. Schema/constrained-choice safe: MET (0 malformed in 68 decision replies + fail-closed 422).
3. Operationally simpler/cheaper: PARTIAL (tiny path: 4 s build, 48 MB RSS, ms latency; real-checkpoint cost unmeasured locally).
4. Expressible as adapter/provider extension: YES for the decision operation (Jev shape); NO for chat (fail-closed, by design).
5. No prod source-of-truth/deployment change: YES (fully isolated proof).
- STOP/FAIL checklist: setup cost did not exceed value; latency practical;
  hardware reasonable for the decision path (1.7 GB real); no invasive
  changes needed for Jev-shape callers; no deep-change; no orchestrator
  duplication. Not all PASS conditions are true → not PASS.

## 7. Measured value and limits

- Numbers: 66/66 fixture requests HTTP 200; 0 malformed constrained outputs;
  22/22 items exactly deterministic; 7–13 ms tiny-model latency; ~48 MB
  server RSS; 5/5 CP-03 probes behave as documented (200/400/400/200/422).
- What this proves: the constrained-decision property is *structural*
  (holds even with random weights), the local serving path is trivially
  cheap to stand up, and the compat boundary is crisp.
- What it does NOT prove: decision *quality* (accuracy, calibration,
  ambiguity handling) — requires the 842 MB Laya checkpoint on a
  weights-available machine. Upstream's own numbers for that path: 219 ms
  one-question on laptop CPU, 117/117 decisions identical to the `laya`
  reference package. Also: Laya checkpoint is English-only (collapses on
  non-Latin scripts while staying confident), and this repo currently has
  no provider seam for the adapter to plug into (future-architecture
  socket only).

```
RESULT: PARTIAL
RECOMMENDATION: HOLD
BEST_USE_CASE: Local constrained classification/routing (READY/WARNING/BLOCKED, expert queue routing) via Colibri's System One decision endpoint as an optional provider behind a Jev-shaped call.
MEASURED_VALUE: 66/66 local decision requests HTTP 200 with 0 malformed constrained outputs; 22/22 items exactly deterministic across repeats; 7-13 ms tiny-model latency at ~48 MB server RSS; CP-03 probes 200/400/400/200/422 as documented; decision quality NOT measured (released weights unreachable from sandbox).
NEXT_STEP: Run the frozen CP-01/CP-02 fixtures against the released 842 MB Laya checkpoint on a weights-available ≥8 GB machine and record accuracy/determinism/latency before any adapter work.
DEEP_CHANGE: NO
```
