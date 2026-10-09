# EXP-22 environment

Date: 2026-10-09. Branch: `arena/42502a3d-murat-project-engineer`.
Base: `585f078b679a1d7d5a3e36afe8c10dc22b978670`.

## Sandbox hardware

- CPU: 2 x Intel Xeon @ 2.60 GHz (x86_64)
- RAM: 3 GB total, no swap
- Disk: 20 GB free (21 GB volume)
- GPU: none
- Network policy: outbound only to github.com, codeload.github.com,
  api.github.com, registry.npmjs.org, pypi.org, files.pythonhosted.org.
  huggingface.co is NOT reachable (verified: connection fails), so no
  released model weights could be downloaded in-sandbox.

## Colibri revision

- Upstream: https://github.com/JustVugg/colibri @
  `bf2442915d6e3dd4cdfd2eb9c2a3d2aa44a25850` (2026-10-06, shallow clone,
  kept outside the repo at `/home/user/colibri-upstream`, not committed)
- Engine: `c/laya` built with system gcc 12.2.0, `-O3 -march=native -fopenmp`,
  CPU-only, no Vulkan/CUDA/Metal. Build time ~4 s. Binary 469,272 B.
- Decision path: `coli serve` (Python gateway) + `laya` engine binary,
  `POST /v1/systemone` (Jev-compatible shape).

## Smallest model/hardware path chosen

Upstream's CI tiny-Laya fixture (numpy-generated, deterministic, SEED 20261002):

- Generator: `c/tools/make_laya_tiny.py` (numpy 2.4.6 from PyPI, stdlib otherwise)
- Geometry: ModernBERT 4 layers x hidden 128, 4 heads; decision head 2 layers;
  max_len 160, head_max_len 64
- Checkpoint bytes: 2,150,730 B total on disk
- `model.safetensors` sha256:
  `53627dd9a910415c5a82a72fe24c23972239e5b0779a4ab79f05c2dc594eb4b4`
  (matches the SHA-256 pinned in committed `c/laya_tiny/ref.json`)
- Reference oracle: committed `ref.json` from the `laya` package 0.3.24
  (torch 2.12.1, transformers 5.12.1), maintainer-run
- Weights are RANDOM (fixture for engine/gateway correctness, not quality).
  Quality-vs-reference measurement requires the released 842 MB checkpoint
  and was NOT RUN (weights unreachable, see network policy).

## Validation of the local stack (before CP-01)

`LAYA_TINY_REQUIRED=1 python3 -m unittest tests.test_laya_tiny tests.test_decision_serve`
from `c/`: **25 tests OK (2 skipped) in 7.7 s** — engine answers match the
`laya` reference package within tolerance on the pinned fixture, and the
gateway serves `POST /v1/systemone` end to end.

## Serve command (localhost-only, stopped after the run)

```bash
./coli serve --model ./laya_tiny --host 127.0.0.1 --port 8000 --gpu none
```

Model loaded in 0.0 s. No persistent service remains.

## Measured footprint (tiny path, 4 server processes)

- Total RSS during CP runs: 48,732–49,400 KB (~48 MB)
- Peak single-process HWM: 35,868 KB (~35 MB)

## Released-checkpoint footprint (upstream docs, not measured here)

- Laya (convaiinnovations/laya, 421M, Apache-2.0): 842 MB download,
  1.7 GB RAM, 219 ms for one Jev question through `coli serve` on a laptop CPU
- GLiNER2.5-Decide (fastino, Apache-2.0): 1.9 GB download, 1.81–1.88 GB RAM,
  294 ms one question / 897 ms three questions on a busy laptop CPU

## Reproduce

```bash
git clone https://github.com/JustVugg/colibri && cd colibri/c
make laya && python3 tools/make_laya_tiny.py --output ./laya_tiny
./coli serve --model ./laya_tiny --host 127.0.0.1 --port 8000 --gpu none
# from murat-project-engineer:
python3 experiments/exp-22-colibri-local-inference/harness/run_cp.py \
  --fixture experiments/exp-22-colibri-local-inference/fixtures/cp01.json \
  --server-pid <coli-pid> \
  --out experiments/exp-22-colibri-local-inference/evidence/cp01-results.json
python3 experiments/exp-22-colibri-local-inference/harness/probe_cp03.py
```
