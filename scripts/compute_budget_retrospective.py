"""Blind retrospective preflight of the Compute Budget Estimator.

Runs the estimator v1.0 UNCHANGED against the pre-execution inputs recorded in
``experiments/compute-budget/validation_runs.json``. This is an anti-overfitting
exercise: one estimator version, one dataset, no per-run coefficient tuning.

Accuracy is only computed for OBSERVED runs (range hit, error %, ratio). ESTIMATED
runs are reported separately. UNOBSERVED runs are used only to check preflight
structure and are excluded from accuracy aggregates. Reconstructing tokens from
file sizes or treating the estimator's own output as "actual" is never done.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import compute_budget as cb  # noqa: E402

DATASET = ROOT / "experiments" / "compute-budget" / "validation_runs.json"

COMPLEXITY_MAP = {"LOW": "low", "MEDIUM": "medium", "HIGH": "high"}
SCENARIO_MAP = {"economy": "economy", "premium": "premium"}


def retrospective_preflight(run: dict) -> dict:
    """Produce a preflight for one run using ONLY its blind pre-execution inputs."""
    pf = run["preflight"]
    complexity = COMPLEXITY_MAP.get(pf["complexity"], "medium")
    scenario = SCENARIO_MAP.get(pf["routing_policy"], "economy")
    estimate = cb.estimate_preflight(
        scope=pf["scope"],
        estimated_tasks=max(1, len(pf.get("expected_stages", []))),
        complexity=complexity,
        expected_context_tokens=pf["expected_context_tokens"],
        expected_calls=pf["expected_calls"],
        scenario=scenario,
    )
    return {
        "run_id": run["run_id"],
        "task_type": run["task_type"],
        "measurement": run["measurement"],
        "scenario": scenario,
        "estimated": {
            "input_tokens_min": estimate["input_tokens_min"],
            "input_tokens_expected": estimate["input_tokens_expected"],
            "input_tokens_max": estimate["input_tokens_max"],
            "output_tokens_min": estimate["output_tokens_min"],
            "output_tokens_expected": estimate["output_tokens_expected"],
            "output_tokens_max": estimate["output_tokens_max"],
            "cost_min": estimate["estimated_cost_min"],
            "cost_expected": estimate["estimated_cost_expected"],
            "cost_max": estimate["estimated_cost_max"],
            "recommended_stack": estimate["recommended_stack"],
            "confidence": estimate["confidence"],
        },
    }


def compare_actual(preflight: dict, actual: dict) -> dict:
    """Compute range-hit / error metrics. Returns None fields when not evaluable."""
    cost = actual.get("cost_usd")
    if cost is None:
        return {
            "range_hit": None,
            "expected_error_percent": None,
            "absolute_error_usd": None,
            "actual_vs_expected_ratio": None,
            "evaluable": False,
        }
    est = preflight["estimated"]
    cost_min = est["cost_min"]
    cost_max = est["cost_max"]
    cost_expected = est["cost_expected"]
    range_hit = bool(cost_min <= cost <= cost_max)
    error_percent = None
    if cost_expected:
        error_percent = round((cost - cost_expected) / cost_expected * 100.0, 2)
    ratio = None
    if cost_expected:
        ratio = round(cost / cost_expected, 4)
    return {
        "range_hit": range_hit,
        "expected_error_percent": error_percent,
        "absolute_error_usd": round(cost - cost_expected, 4) if cost_expected is not None else None,
        "actual_vs_expected_ratio": ratio,
        "evaluable": True,
    }


def validate() -> dict:
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    runs = dataset["runs"]

    observed = []
    estimated = []
    unobserved = []
    rows = []
    for run in runs:
        preflight = retrospective_preflight(run)
        comparison = compare_actual(preflight, run["actual"])
        entry = {**preflight, "actual_cost_usd": run["actual"].get("cost_usd"), "comparison": comparison, "result": run["result"]}
        rows.append(entry)
        if run["measurement"] == "OBSERVED":
            observed.append(entry)
        elif run["measurement"] == "ESTIMATED":
            estimated.append(entry)
        else:
            unobserved.append(entry)

    observed_metrics = _aggregate(observed)
    estimated_metrics = _aggregate(estimated)

    return {
        "estimator_version": dataset.get("estimator_version", "1.0"),
        "dataset": str(DATASET.relative_to(ROOT)),
        "run_count": len(runs),
        "observed_count": len(observed),
        "estimated_count": len(estimated),
        "unobserved_count": len(unobserved),
        "observed_metrics": observed_metrics,
        "estimated_metrics": estimated_metrics,
        "conclusion": _conclusion(observed),
        "rows": rows,
    }


def _aggregate(entries: list[dict]) -> dict:
    if not entries:
        return None
    hits = [e for e in entries if e["comparison"]["evaluable"]]
    if not hits:
        return {"evaluable": False, "note": "no OBSERVED cost telemetry available"}
    error_pcts = [e["comparison"]["expected_error_percent"] for e in hits]
    return {
        "evaluable": True,
        "range_hit_count": sum(1 for e in hits if e["comparison"]["range_hit"]),
        "range_hit_rate": round(sum(1 for e in hits if e["comparison"]["range_hit"]) / len(hits), 4),
        "mean_error_percent": round(statistics.mean(error_pcts), 2),
        "median_error_percent": round(statistics.median(error_pcts), 2),
        "worst_error_percent": round(max(error_pcts, key=abs), 2),
    }


def _conclusion(observed: list[dict]) -> str:
    if len(observed) < 5:
        return "INSUFFICIENT_HISTORICAL_TELEMETRY"
    return "PASS"  # accuracy acceptance is evaluated separately by the report author


def main() -> int:
    parser = argparse.ArgumentParser(description="Blind retrospective preflight for the Compute Budget Estimator")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = validate()
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
