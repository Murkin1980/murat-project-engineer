# EXP-14 — Method, execution host and evidence rules

This file records *how* the EXP-14 evidence is produced. The contract is
`CONTRACT.md`; the ground truth is `ORACLE.md`; the frozen input is
`frozen/dataset_v1.json`.

---

## 1. Execution order (hard, not advisory)

```text
read governing docs
   -> capture pre-experiment repository state
   -> author + validate + FREEZE dataset and oracle   (gate G1/G2/G3, digest written)
   -> Sequence A: deterministic baseline, 3 passes, hashed
   -> probe Laya access, record evidence
   -> Sequence B: Laya zero-shot, 3 passes, same frozen inputs
   -> STOP and evaluate
   -> decide about stage C / stage D only from the recorded results
```

No stage was entered before the previous stage's evidence existed on disk. The
dataset digest is re-verified at the start of every runner and every evaluation,
so a mutated freeze aborts the run instead of silently scoring a different
dataset.

## 2. Why the authoring sandbox cannot execute Sequence B

The sandbox has an allow-listed network egress. Probed and recorded verbatim in
`raw/laya_access_probe_sandbox.json` on 2026-09-30:

| Destination | Observed |
|---|---|
| `huggingface.co:443` | TCP connects, **TLS handshake closed** (`SSLZeroReturnError`) |
| `hf.co:443` | TCP connects, TLS closed |
| `cas-bridge.xethub.hf.co:443` | TCP connects, TLS closed |
| `cdn-lfs.huggingface.co:443` | **DNS failure** (`gaierror -5`) |
| `hf-mirror.com:443` | TCP connects, TLS closed |
| `modelscope.cn:443` | TCP connects, TLS closed |
| `pirateface.co:443` | TCP connects, TLS closed |
| `systemonemodels.tech:443` | TCP connects, TLS closed |
| `objects.githubusercontent.com:443` | TCP connects, TLS closed (Actions artifact CDN) |
| `pypi.org`, `files.pythonhosted.org` | **TLS OK** |
| `github.com`, `api.github.com`, `codeload.github.com` | **TLS OK** |

The probe did not stop at socket tests. The **complete pinned Laya stack was
installed** in an isolated virtualenv and the real load path was executed:

```text
laya 0.3.22   torch 2.14.1+cu130   transformers 5.18.0
huggingface_hub 1.33.0   safetensors 0.8.0   numpy 2.4.6
```

| Attempt | Result |
|---|---|
| `huggingface_hub.hf_hub_download("convaiinnovations/laya", "config.json", revision=55cf4c4e…)` | `LocalEntryNotFoundError` after 5 retries — `TLS/SSL connection has been closed (EOF)` on `HEAD …/resolve/55cf4c4e…/config.json` |
| `laya.load("convaiinnovations/laya", revision=55cf4c4e…)` | `ConnectError: TLS/SSL connection has been closed (EOF) (_ssl.c:992)` |

So the blocker is **not** a missing dependency, a missing GPU, or an untried path.
The pinned 843 MB checkpoint is published only on Hugging Face (`model.safetensors`,
repo root), the HF zone is unreachable from this sandbox, and the vendor's own
SDK fails at the first metadata request. A second, independent constraint is
recorded for completeness: the sandbox has 2 vCPU, 4 GB RAM and no GPU, which is
marginal for a 421M-parameter F32 encoder even if the weights were present.

Per the EXP-14 instruction ("если … Laya access … недоступны — BLOCKED, а не
реконструировать данные"), the correct in-sandbox classification is
`INFRASTRUCTURE_BLOCKED`, and no Laya output was fabricated, simulated, or
substituted by a different model.

## 3. Execution host for Sequence B, and why it is not "new infrastructure"

Sequence B is executed on an **ephemeral GitHub-hosted runner** through a
temporary workflow. This is the same bounded pattern EXP-18 used and documented
in `experiments/exp-18-pirateface-model-resilience/METHOD.md` ("Test host: why a
temporary CI runner, not the authoring sandbox"), which was closed `PASS` with
`NEW_INFRASTRUCTURE = NO`.

The runner is:

- **temporary** — destroyed at the end of the job;
- **credential-free** — no repository secret or variable is read; the workflow
  declares `permissions: contents: write` only so it can commit its own evidence
  back to the experiment branch;
- **non-production** — it builds nothing, deploys nothing, publishes nothing,
  touches no Cloudflare/Dashboard path, and no repository code or runtime imports
  or depends on it;
- **branch-scoped** — `on.push.branches` is the session branch only; it is never
  merged to `main`;
- **removed** — `.github/workflows/exp14-laya-harness.yml` is deleted once the
  evidence is committed. The copy under `harness/exp14-laya.workflow.yml` is kept
  as the reproducible method, exactly as EXP-18 kept its harness.

The sandbox can reach `github.com` but not `objects.githubusercontent.com`, so
Actions **artifacts** cannot be downloaded here. Evidence therefore returns by
git: the runner commits `raw/` to the experiment branch and the sandbox pulls it.
This is the EXP-18 mechanism and it keeps every byte of evidence inside version
control, which is the repository's source of truth.

Governance accounting for this execution:

```text
PRODUCTION_CHANGED          = NO   (no commit to main; no production file touched)
NEW_INFRASTRUCTURE          = NO   (ephemeral credential-free CI runner, removed after
                                    the run; no service, daemon, queue, database,
                                    registry, runtime or dependency added to the project)
DEEP_CHANGE                 = NO
PRODUCTION_ROUTING_CHANGED  = NO
```

If any of these had become YES the run would have stopped and reported instead of
continuing.

## 4. Stage table

| Stage | Action | Evidence |
|---|---|---|
| 0 | read governing docs; capture `main` SHA and pre-experiment repository state with hashes of every document that defines routing, autonomy and decision authority | `fixtures/PRE_EXPERIMENT_REPO_STATE.txt` |
| 1 | author, validate and **freeze** the 43-case dataset and oracle; write the digest | `frozen/dataset_v1.json`, `frozen/DATASET_SHA256.txt`, `DATASET.md`, `ORACLE.md` |
| A | deterministic baseline, 3 passes, over the frozen dataset | `raw/baseline_pass{1,2,3}.json`, `raw/metrics_baseline_pass{1,2,3}.json`, `raw/baseline_reproducibility.json`, `BASELINE.md` |
| P | Laya access probe (sandbox + execution host) | `raw/laya_access_probe_sandbox.json`, `raw/laya_access_probe_execution_host.json` |
| B | **Laya zero-shot**, primary pre-registered candidate, 3 passes | `raw/laya_B_laya_zero_shot_root_pass{1,2,3}.json`, `raw/metrics_…`, `raw/laya_…_reproducibility.json`, `LAYA_ZERO_SHOT.md` |
| B2 | Laya `typed-decisions` subfolder, **secondary reference only**, 3 passes | `raw/laya_B2_laya_typed_decisions_reference_pass{1,2,3}.json`, `raw/metrics_…` |
| E | evaluation, comparison against the control, verdict | `RESULTS.md` |
| C | calibration — **only** if the gate in `CONTRACT.md` §9 allows it | `CALIBRATION.md` when run |
| D | fine-tuning — **not** run automatically | `FINE_TUNING.md` when justified |
| – | hashes of every artifact | `HASHES.txt` |

## 5. Evidence discipline

- `OBSERVED` — a value read from a file this run produced, a HTTP response, a
  measurement, or a hash computed from real bytes.
- `INFERRED` — labelled as inference wherever it appears.
- `UNKNOWN` / `null` — left empty rather than filled with an assumption. This
  follows the Run 05 / Stage 2A finding recorded in `STATUS.md` ("retrospective
  baselines need a distinction between zero and unknown").
- No cost is ever reconstructed. The baseline and both Laya arms run locally with
  no provider invoice, so `model_cost_usd = 0.0` with
  `cost_basis = observed_zero…`. The general-purpose LLM decision call that Laya
  would *replace* has no metered cost available in this repository (EXP-13 Pilot
  Batch 1 has never been executed), so that comparison is reported as `null /
  unobserved` and never estimated.
- No private chain-of-thought is stored. Laya is non-autoregressive and emits no
  reasoning text; the recorded `raw_output` is the SDK's answer block
  (`answers`, `usage`) plus per-question probabilities and confidence.
- Raw model outputs are preserved verbatim, including failures. A model that
  cannot produce structured output is recorded as a result, not corrected.

## 6. Determinism and reproducibility

| Element | Control |
|---|---|
| dataset bytes | builder is deterministic; digest re-verified by every runner and evaluator |
| model input | `render_state()` — sorted keys, fixed separators, UTF-8; per-case `input_sha256` and `rendered_state_sha256` recorded |
| decoding | frozen in `exp14_common` / `run_laya.decode_answers`; `noul` threshold `0.5` fixed before the run |
| model | pinned revision from the SDK's own `PINNED_REVISIONS`; `resolved_revision` and `revision_matches_pin` recorded per pass |
| sampling | none — Laya is a single deterministic forward pass (argmax / probability), no temperature, no seed needed |
| device | `cpu` explicitly, recorded |
| passes | 3 per arm; decision vectors compared for byte equality |
| invalid handling | frozen `SAFE_ESCALATION_DECISION`; never hand-repaired |

A run is called reproducible only when the **decision vectors** are identical
across passes. Wall-clock latency is reported per pass and is explicitly *not*
part of the reproducibility assertion, because it is host-noise dominated.
