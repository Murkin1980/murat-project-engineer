# EXP-14 harness (bounded, temporary)

Experiment tooling only. Nothing here is imported by production code, by
`scripts/`, by any playbook, gate, contract or schema, and no dependency is added
to the repository (`package.json` is untouched; the Python stack lives in a
throwaway virtualenv or on an ephemeral CI runner).

## Files

| File | Role |
|---|---|
| `exp14_common.py` | frozen decision contract, closed vocabularies, deterministic input rendering, `SAFE_ESCALATION_DECISION`, validity check |
| `mpe_oracle_rules.py` | the frozen oracle rule table `O-T1…O-T7`, `O-H1…O-H4`, `O-R1…O-R6`, `O-E1…O-E7` — normative text in `../ORACLE.md` |
| `build_dataset.py` | authors, validates (`G1/G2/G3`) and freezes `../frozen/dataset_v1.json` + digest |
| `render_dataset_md.py` | regenerates `../DATASET.md` from the frozen artifact so no number is hand-transcribed |
| `run_baseline.py` | **Sequence A** — imports `scripts/triage_engine.triage` unmodified and adds the frozen `B-R`/`B-E` derivation layer |
| `probe_laya_access.py` | records host, egress, dependency and real `laya.load` reachability; classifies `ACCESSIBLE` / `INFRASTRUCTURE_BLOCKED` |
| `run_laya.py` | **Sequence B / B2** — pinned checkpoint, four typed questions, one forward pass per case, raw outputs preserved verbatim |
| `evaluate.py` | frozen metric definitions; scores any arm against the frozen oracle; refuses to score a digest mismatch |
| `run_sequence_b.sh` | stage runner for the execution host (probe → digest verify → arms → evaluate → summary) |
| `exp14-laya.workflow.yml` | copy of the temporary CI wrapper, kept as the reproducible method |

## Local usage

```bash
cd experiments/exp-14-laya/2026-09-30

# 1. freeze (deterministic; reproduces the recorded digest byte-for-byte)
python3 harness/build_dataset.py
python3 harness/render_dataset_md.py

# 2. Sequence A
python3 harness/run_baseline.py --passes 3
for p in 1 2 3; do
  python3 harness/evaluate.py --raw raw/baseline_pass$p.json --arm baseline \
      --out raw/metrics_baseline_pass$p.json
done

# 3. access probe (never fabricates a result; classifies the host)
python3 harness/probe_laya_access.py --timeout 20 --out raw/laya_access_probe_sandbox.json

# 4. Sequence B — requires a host that can reach huggingface.co
pip install "laya==0.3.22" torch transformers
python3 harness/run_laya.py --arm B_laya_zero_shot_root --checkpoint root --passes 3
python3 harness/run_laya.py --arm B2_laya_typed_decisions_reference \
    --checkpoint typed-decisions --passes 3
bash harness/run_sequence_b.sh 3 "root typed-decisions"   # or the whole stage at once
```

## Safety properties of the harness

- **Fail-closed on a mutated freeze.** `run_baseline.py`, `run_laya.py` and
  `evaluate.py` all recompute the SHA-256 of `frozen/dataset_v1.json` and abort
  with a non-zero exit if it differs from `frozen/DATASET_SHA256.txt` or from the
  digest recorded in the raw file being scored.
- **No hand repair.** `decode_answers` returns `(None, reason)` for anything
  out-of-contract; the caller substitutes `SAFE_ESCALATION_DECISION`, sets
  `invalid_output = true` and stores the verbatim `failure_reason`. Exceptions
  from the model call are captured the same way.
- **No production import side effects.** The only production symbol imported is
  `scripts.triage_engine.triage` / `.validate_task`, both called read-only.
- **Blocked is a result.** `run_laya.py` writes an `INFRASTRUCTURE_BLOCKED`
  record with the verbatim error instead of an empty or synthetic output, and
  exits `4`.
- **Evidence returns by git, not by artifact CDN**, because the authoring sandbox
  cannot reach `objects.githubusercontent.com`.

## Why a CI runner is the Sequence B host

See `../METHOD.md` sections 2 and 3. Short form: every Hugging Face zone fails
the TLS handshake from the authoring sandbox even though the full pinned Laya
stack installs and the real `laya.load()` path is attempted there, so the pinned
843 MB checkpoint cannot be retrieved in-sandbox. An ephemeral, credential-free
GitHub-hosted runner is used instead — the pattern EXP-18 documented and closed
as `PASS` with `NEW_INFRASTRUCTURE = NO`. The workflow
`.github/workflows/exp14-laya-harness.yml` is temporary, branch-scoped, never
merged to `main`, and removed once the evidence is recorded.
