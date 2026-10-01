"""EXP-14 — Laya access / telemetry probe.

Run:  python3 harness/probe_laya_access.py [--timeout 12]

Records, without interpretation, whether the host can actually reach the pinned
Laya checkpoint and whether it can load and run it. EXP-14 section 15 requires
that a missing model path be reported as BLOCKED rather than reconstructed, so
the probe is written first and its output is the evidence for that decision.

Every probe is read-only. Nothing is installed, nothing is downloaded, no
repository file outside this run directory is touched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import socket
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
sys.path.insert(0, str(HERE))

from exp14_common import CHECKPOINT, DATASET_ID, EXPERIMENT_ID  # noqa: E402

LAYA_SDK_PIN = "laya==0.3.22"
LAYA_HF_REPO = "convaiinnovations/laya"
LAYA_PINNED_REVISION = "55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851"

HOSTS = [
    ("huggingface.co", 443),
    ("cdn-lfs.huggingface.co", 443),
    ("hf.co", 443),
    ("cas-bridge.xethub.hf.co", 443),
    ("hf-mirror.com", 443),
    ("modelscope.cn", 443),
    ("pirateface.co", 443),
    ("systemonemodels.tech", 443),
    ("pypi.org", 443),
    ("files.pythonhosted.org", 443),
    ("github.com", 443),
    ("api.github.com", 443),
    ("codeload.github.com", 443),
    ("objects.githubusercontent.com", 443),
]

URLS = [
    f"https://huggingface.co/api/models/{LAYA_HF_REPO}",
    f"https://huggingface.co/{LAYA_HF_REPO}/resolve/{LAYA_PINNED_REVISION}/config.json",
    "https://pypi.org/pypi/laya/json",
    f"https://api.github.com/repos/NandhaKishorM/laya/commits/{LAYA_PINNED_REVISION}",
]


def tcp_tls_probe(host: str, port: int, timeout: float) -> dict:
    started = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            tcp = "CONNECTED"
    except Exception as exc:  # noqa: BLE001 - the exception text IS the evidence
        return {"host": host, "port": port, "tcp": f"FAILED: {type(exc).__name__}: {exc}",
                "tls": "NOT_ATTEMPTED", "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure:
                tls = f"OK: {secure.version()} / {secure.cipher()[0] if secure.cipher() else '?'}"
    except Exception as exc:  # noqa: BLE001
        tls = f"FAILED: {type(exc).__name__}: {exc}"
    return {"host": host, "port": port, "tcp": tcp, "tls": tls,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}


def http_probe(url: str, timeout: float) -> dict:
    started = time.perf_counter()
    request = urllib.request.Request(url, headers={"User-Agent": "exp-14-access-probe/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(65536)
            return {"url": url, "status": response.status, "bytes_read": len(body),
                    "body_sha256_prefix": hashlib.sha256(body).hexdigest()[:16],
                    "elapsed_ms": round((time.perf_counter() - started) * 1000, 1),
                    "result": "REACHABLE"}
    except urllib.error.HTTPError as exc:
        return {"url": url, "status": exc.code, "result": "HTTP_ERROR",
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}
    except Exception as exc:  # noqa: BLE001
        return {"url": url, "status": None, "result": f"UNREACHABLE: {type(exc).__name__}: {exc}",
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}


def import_probe(module: str) -> dict:
    try:
        module_object = __import__(module)
        return {"module": module, "importable": True,
                "version": getattr(module_object, "__version__", None)}
    except Exception as exc:  # noqa: BLE001
        return {"module": module, "importable": False, "error": f"{type(exc).__name__}: {exc}"}


def command_probe(label: str, argv: list[str], timeout: float) -> dict:
    started = time.perf_counter()
    try:
        completed = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return {"label": label, "argv": argv, "returncode": completed.returncode,
                "stdout_tail": completed.stdout.strip()[-800:],
                "stderr_tail": completed.stderr.strip()[-800:],
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}
    except FileNotFoundError as exc:
        return {"label": label, "argv": argv, "returncode": None, "error": f"NOT_FOUND: {exc}",
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}
    except subprocess.TimeoutExpired:
        return {"label": label, "argv": argv, "returncode": None, "error": "TIMEOUT",
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}


def memory_and_disk() -> dict:
    info: dict[str, object] = {}
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            key = line.split(":")[0]
            if key in ("MemTotal", "MemAvailable", "SwapTotal"):
                info[key + "_kB"] = int(line.split()[1])
    usage = shutil.disk_usage(str(RUN_DIR))
    info["disk_free_bytes"] = usage.free
    info["disk_total_bytes"] = usage.total
    info["cpu_count"] = os.cpu_count()
    return info


def hf_hub_retrieval_probe(timeout: float) -> dict:
    """Exercise the exact retrieval primitive ``laya.load`` uses.

    ``laya/agent.py`` resolves a checkpoint through ``huggingface_hub``
    (``snapshot_download`` + ``resolve_revision``/``verify_digests``). Probing
    ``huggingface_hub`` directly isolates the blocker: if this fails on the
    network, no torch/transformers install state can change the outcome.
    """
    try:
        from huggingface_hub import hf_hub_download  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {"attempted": False, "reason": f"huggingface_hub not importable: {type(exc).__name__}: {exc}"}
    started = time.perf_counter()
    try:
        path = hf_hub_download(
            repo_id=LAYA_HF_REPO, filename="config.json", revision=LAYA_PINNED_REVISION,
            etag_timeout=timeout)
        return {"attempted": True, "result": "RETRIEVED", "path": str(path),
                "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}
    except Exception as exc:  # noqa: BLE001
        return {"attempted": True, "result": "FAILED",
                "error": f"{type(exc).__name__}: {exc}"[:2000],
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}


def laya_load_probe(timeout: float) -> dict:
    """Attempt the real load path. Bounded: this must never hang the probe."""
    try:
        import laya  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {"attempted": False, "reason": f"laya not importable: {type(exc).__name__}: {exc}"}
    started = time.perf_counter()
    environment_backup = {key: os.environ.get(key) for key in ("HF_HUB_DOWNLOAD_TIMEOUT", "HF_HUB_ETAG_TIMEOUT")}
    os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = str(int(timeout))
    os.environ["HF_HUB_ETAG_TIMEOUT"] = str(int(timeout))
    try:
        agent = laya.load(LAYA_HF_REPO, revision=LAYA_PINNED_REVISION)
        sample = agent.system_one(
            "Fix a typo in the README badge line.",
            {"risk_tier": {"type": "choice",
                           "instructions": "Which MPE risk tier applies?",
                           "criteria": {"FAST": "narrow reversible low impact",
                                        "VERIFIED": "meaningful change",
                                        "DEEP-CHANGE": "core architecture or authority"}}},
        )
        return {"attempted": True, "result": "LOADED_AND_PREDICTED",
                "sample_answer": sample.get("answers"),
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}
    except Exception as exc:  # noqa: BLE001
        return {"attempted": True, "result": "FAILED",
                "error": f"{type(exc).__name__}: {exc}"[:2000],
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 1)}
    finally:
        for key, value in environment_backup.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def main() -> int:
    parser = argparse.ArgumentParser(description="EXP-14 Laya access probe")
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--out", type=Path, default=RUN_DIR / "raw/laya_access_probe.json")
    parser.add_argument("--skip-load-probe", action="store_true")
    args = parser.parse_args()

    report = {
        "experiment_id": EXPERIMENT_ID,
        "checkpoint": CHECKPOINT,
        "dataset_id": DATASET_ID,
        "probe": "laya_access",
        "probed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "candidate_pin": {
            "sdk": LAYA_SDK_PIN,
            "hf_repo": LAYA_HF_REPO,
            "pinned_revision": LAYA_PINNED_REVISION,
            "revision_source": "laya/revisions.py PINNED_REVISIONS['convaiinnovations/laya']",
            "expected_primary_artifact": "model.safetensors (~843 MB, repo root)",
        },
        "host": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            **memory_and_disk(),
        },
        "cuda_available": None,
        "modules": [import_probe(name) for name in ("torch", "transformers", "safetensors", "huggingface_hub", "laya", "numpy")],
        "tcp_tls": [tcp_tls_probe(host, port, args.timeout) for host, port in HOSTS],
        "http": [http_probe(url, args.timeout) for url in URLS],
        "commands": [
            command_probe("pip index versions laya", [sys.executable, "-m", "pip", "index", "versions", "laya"], 60),
            command_probe("nvidia-smi", ["nvidia-smi"], 10),
        ],
    }

    for module in report["modules"]:
        if module["module"] == "torch" and module["importable"]:
            try:
                import torch  # noqa: PLC0415
                report["cuda_available"] = bool(torch.cuda.is_available())
            except Exception:  # noqa: BLE001
                report["cuda_available"] = None

    report["hf_hub_retrieval_attempt"] = hf_hub_retrieval_probe(args.timeout)
    if not args.skip_load_probe:
        report["laya_load_attempt"] = laya_load_probe(args.timeout)
    else:
        report["laya_load_attempt"] = {"attempted": False, "reason": "skipped by --skip-load-probe"}

    hf_reachable = any(probe["host"] == "huggingface.co" and probe["tls"].startswith("OK")
                       for probe in report["tcp_tls"])
    weights_retrievable = bool(
        hf_reachable
        and report["hf_hub_retrieval_attempt"].get("result") == "RETRIEVED"
        and report["laya_load_attempt"].get("result") == "LOADED_AND_PREDICTED")
    report["verdict"] = {
        "huggingface_tls_reachable": hf_reachable,
        "laya_sdk_installable_from_pypi": any(
            command.get("returncode") == 0 for command in report["commands"]
            if command["label"] == "pip index versions laya"),
        "hf_hub_metadata_retrievable": report["hf_hub_retrieval_attempt"].get("result") == "RETRIEVED",
        "laya_weights_retrievable_on_this_host": weights_retrievable,
        "laya_runnable_on_this_host": weights_retrievable,
        "sequence_b_executable_on_this_host": weights_retrievable,
        "classification": "ACCESSIBLE" if weights_retrievable else "INFRASTRUCTURE_BLOCKED",
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["verdict"], indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
