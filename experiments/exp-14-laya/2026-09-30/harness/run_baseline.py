"""EXP-14 Sequence A — deterministic baseline over the frozen dataset.

Run:  python3 harness/run_baseline.py [--passes 3] [--out raw/baseline_pass<N>.json]

The baseline is the EXISTING deterministic MPE decision path:
``scripts/triage_engine.triage`` is imported and called unmodified. It supplies
two of the four contract fields directly:

    risk_tier             <- recommended_risk_tier
    requires_human_gate   <- human_approval_required

``route_profile`` and ``escalate_to_system_two`` have **no deterministic
implementation anywhere in this repository** — route-profiles.md states that
"definitions reference profiles, while the coordinator resolves profiles at run
time". Sequence A therefore adds the smallest documented derivation layer over
the engine's own outputs. That layer is authored once here, frozen before
Sequence B, and is never adjusted afterwards. It is experiment tooling: nothing
in ``scripts/`` changes.

Baseline derivation layer (frozen):

    B-R1  recommended_risk_tier == DEEP-CHANGE          -> strong-review
    B-R2  architectural_impact >= 4 or
          data_sensitivity   >= 4                        -> strong-review
    B-R3  work_kind research|implementation|review|
          coordination                                   -> cheap-research|coding|
                                                            strong-review|default

    B-E   recommended_risk_tier == DEEP-CHANGE
          or human_approval_required
          or execution_confidence < 80
          or not acceptance_criteria_present
          or not rollback_known
          or affected_repositories == []

B-R2 reuses the engine's own published thresholds (``maximum_architectural_
impact`` at 4, ``high_data_sensitivity`` at 4). B-E reuses the engine's own FAST
boundary (``execution_confidence < 80``) plus the playbook ``required_inputs``
(playbooks/fast.md, playbooks/verified.md) and the hard ``rollback_available``
gate (gates/registry.yaml).

No cost is claimed: the baseline makes zero model or provider calls, so token
usage is 0 and model cost is an OBSERVED 0.0 USD, not an estimate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO_ROOT = RUN_DIR.parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(HERE))

from exp14_common import (  # noqa: E402
    CHECKPOINT,
    DATASET_ID,
    DECISION_FIELDS,
    EXPERIMENT_ID,
    ROUTE_PROFILES,
    render_state,
    triage_input_only,
)

from scripts.triage_engine import triage  # noqa: E402  (imported unmodified)

BASELINE_ENGINE_VERSION = "0.1.0"
DERIVATION_LAYER_VERSION = "exp14-baseline-derivation-1.0.0"

WORK_KIND_TO_PROFILE = {
    "research": "cheap-research",
    "implementation": "coding",
    "review": "strong-review",
    "coordination": "default",
}


def derive_route_profile(engine_output: dict[str, Any], work_kind: str) -> tuple[str, str]:
    """B-R1..B-R3. Returns (route_profile, rule_id)."""
    if engine_output["recommended_risk_tier"] == "DEEP-CHANGE":
        return "strong-review", "B-R1"
    if engine_output["architectural_impact"] >= 4 or engine_output["data_sensitivity"] >= 4:
        return "strong-review", "B-R2"
    return WORK_KIND_TO_PROFILE[work_kind], "B-R3"


def derive_escalate(engine_output: dict[str, Any], case_input: dict[str, Any]) -> tuple[bool, list[str]]:
    """B-E. Returns (escalate_to_system_two, fired_reasons)."""
    reasons: list[str] = []
    if engine_output["recommended_risk_tier"] == "DEEP-CHANGE":
        reasons.append("deep_change_tier")
    if engine_output["human_approval_required"]:
        reasons.append("human_approval_required")
    if engine_output["execution_confidence"] < 80:
        reasons.append("execution_confidence_below_80")
    if not case_input["acceptance_criteria_present"]:
        reasons.append("acceptance_criteria_absent")
    if not case_input["rollback_known"]:
        reasons.append("rollback_unknown")
    if not case_input["affected_repositories"]:
        reasons.append("no_repository_scope")
    return bool(reasons), reasons


def decide_case(case: dict[str, Any]) -> dict[str, Any]:
    """One baseline decision, timed. Deterministic: no randomness, no I/O."""
    case_input = case["input"]
    started = time.perf_counter_ns()
    engine_output = triage(triage_input_only(case_input))
    route_profile, route_rule = derive_route_profile(engine_output, case_input["work_kind"])
    escalate, escalate_reasons = derive_escalate(engine_output, case_input)
    elapsed_ns = time.perf_counter_ns() - started

    assert route_profile in ROUTE_PROFILES
    decision = {
        "risk_tier": engine_output["recommended_risk_tier"],
        "requires_human_gate": bool(engine_output["human_approval_required"]),
        "route_profile": route_profile,
        "escalate_to_system_two": escalate,
    }
    assert set(decision) == set(DECISION_FIELDS)
    return {
        "case_id": case["case_id"],
        "input_sha256": case["input_sha256"],
        "rendered_state_sha256": hashlib.sha256(render_state(case_input).encode("utf-8")).hexdigest(),
        "decision": decision,
        "engine_output": engine_output,
        "derivation": {
            "route_profile_rule": route_rule,
            "escalate_reasons": escalate_reasons,
        },
        "latency_ms": elapsed_ns / 1_000_000.0,
        "invalid_output": False,
        "failure_reason": None,
        "model_calls": 0,
        "tokens": {"input": 0, "output": 0},
        "model_cost_usd": 0.0,
        "cost_basis": "observed_zero_no_provider_call",
    }


def run_pass(dataset: dict[str, Any], pass_index: int) -> dict[str, Any]:
    results = [decide_case(case) for case in dataset["cases"]]
    latencies = sorted(result["latency_ms"] for result in results)
    count = len(latencies)
    return {
        "experiment_id": EXPERIMENT_ID,
        "checkpoint": CHECKPOINT,
        "sequence": "A_DETERMINISTIC_BASELINE",
        "arm": "baseline",
        "pass_index": pass_index,
        "dataset_id": dataset["dataset_id"],
        "dataset_sha256_expected": dataset.get("_sha256"),
        "baseline": {
            "implementation": "scripts/triage_engine.py (imported unmodified)",
            "engine_version": BASELINE_ENGINE_VERSION,
            "derivation_layer_version": DERIVATION_LAYER_VERSION,
            "derivation_layer": {
                "route_profile": [
                    "B-R1 recommended_risk_tier == DEEP-CHANGE -> strong-review",
                    "B-R2 architectural_impact >= 4 or data_sensitivity >= 4 -> strong-review",
                    "B-R3 work_kind research|implementation|review|coordination -> "
                    "cheap-research|coding|strong-review|default",
                ],
                "escalate_to_system_two": [
                    "B-E DEEP-CHANGE or human_approval_required or execution_confidence < 80 "
                    "or acceptance_criteria_present == false or rollback_known == false "
                    "or affected_repositories == []",
                ],
            },
            "model": None,
            "provider": None,
        },
        "host": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor() or None,
            "machine": platform.machine(),
            "cpu_count": __import__("os").cpu_count(),
        },
        "case_count": count,
        "latency_ms": {
            "min": latencies[0],
            "median": latencies[count // 2] if count % 2 else (latencies[count // 2 - 1] + latencies[count // 2]) / 2,
            "mean": sum(latencies) / count,
            "p95": latencies[max(0, int(round(0.95 * count)) - 1)],
            "max": latencies[-1],
            "total": sum(latencies),
        },
        "invalid_output_count": 0,
        "model_calls": 0,
        "tokens": {"input": 0, "output": 0},
        "model_cost_usd": 0.0,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="EXP-14 Sequence A deterministic baseline")
    parser.add_argument("--passes", type=int, default=3)
    parser.add_argument("--dataset", type=Path, default=RUN_DIR / "frozen/dataset_v1.json")
    parser.add_argument("--out-dir", type=Path, default=RUN_DIR / "raw")
    args = parser.parse_args()

    raw = args.dataset.read_bytes()
    dataset = json.loads(raw.decode("utf-8"))
    dataset_sha = hashlib.sha256(raw).hexdigest()
    dataset["_sha256"] = dataset_sha

    frozen_digest_file = args.dataset.parent / "DATASET_SHA256.txt"
    if frozen_digest_file.exists():
        recorded = frozen_digest_file.read_text(encoding="utf-8").splitlines()
        recorded_sha = next(line.split()[0] for line in recorded if line.endswith("dataset_v1.json"))
        if recorded_sha != dataset_sha:
            print(f"FATAL: frozen dataset digest changed.\n  recorded: {recorded_sha}\n  actual:   {dataset_sha}",
                  file=sys.stderr)
            return 2
        print(f"frozen dataset digest verified: {dataset_sha}")
    assert dataset["dataset_id"] == DATASET_ID
    assert dataset["frozen"] is True

    args.out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    digests: list[str] = []
    for index in range(1, args.passes + 1):
        payload = run_pass(dataset, index)
        rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        out_path = args.out_dir / f"baseline_pass{index}.json"
        out_path.write_text(rendered, encoding="utf-8")
        digest = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
        digests.append(digest)
        written.append(str(out_path.relative_to(REPO_ROOT)))
        print(f"pass {index}: {len(payload['results'])} cases, "
              f"median latency {payload['latency_ms']['median']:.4f} ms, sha256 {digest[:16]}…")

    # Reproducibility: the decision vectors must be byte-identical across passes.
    decision_vectors = []
    for index in range(1, args.passes + 1):
        payload = json.loads((args.out_dir / f"baseline_pass{index}.json").read_text(encoding="utf-8"))
        decision_vectors.append(json.dumps(
            [[r["case_id"], r["decision"]] for r in payload["results"]], sort_keys=True))
    identical = len(set(decision_vectors)) == 1
    summary = {
        "sequence": "A_DETERMINISTIC_BASELINE",
        "dataset_id": DATASET_ID,
        "dataset_sha256": dataset_sha,
        "passes": args.passes,
        "pass_files": written,
        "pass_file_sha256": digests,
        "decisions_identical_across_passes": identical,
        "reproducible": identical,
        "model_calls": 0,
        "model_cost_usd": 0.0,
    }
    (args.out_dir / "baseline_reproducibility.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"decisions identical across {args.passes} passes: {identical}")
    return 0 if identical else 3


if __name__ == "__main__":
    raise SystemExit(main())
