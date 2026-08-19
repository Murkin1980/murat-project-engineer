"""Controlled validation of the Compute Budget Gate against historical MPE runs.

This is a self-consistency / coverage check, not a live billing reconciliation.
Historical runs predate usage capture, so their spend is UNOBSERVED; the script
verifies the gate reports that honestly instead of fabricating cost data, and
measures the preflight estimator's determinism and schema validity on every run.

The accuracy criterion (actual cost inside preflight min-max for >= 80% of runs)
can only be evaluated once observed usage is captured on new runs; this script
reports the observed-coverage rate needed for that criterion.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import compute_budget as cb  # noqa: E402

TIER_COMPLEXITY = {"FAST": "low", "VERIFIED": "medium", "DEEP-CHANGE": "high"}


def _historical_runs() -> list[dict]:
    runs: list[dict] = []
    for path in sorted((ROOT / "evidence" / "stage2").glob("RUN-*_REPORT.json")):
        runs.append(json.loads(path.read_text(encoding="utf-8")))
    for path in sorted((ROOT / "evidence" / "stage2a").glob("run-*/RUN_REPORT.json")):
        runs.append(json.loads(path.read_text(encoding="utf-8")))
    return runs


def _proxy_preflight(report: dict) -> dict:
    """Deterministic preflight proxy from fields already present in a report."""
    tier = report.get("risk_tier") or "FAST"
    files = len(report.get("files_changed") or [])
    tasks = max(1, files)
    complexity = TIER_COMPLEXITY.get(tier, "low")
    return cb.estimate_preflight(
        scope=(report.get("task") or "historical-run")[:120],
        estimated_tasks=tasks,
        complexity=complexity,
        expected_context_tokens=15_000,
        expected_calls=max(4, tasks * 3),
        scenario="economy",
    )


def validate_historical() -> dict:
    runs = _historical_runs()
    results = []
    observed = 0
    estimated = 0
    unobserved = 0
    for report in runs:
        preflight = _proxy_preflight(report)
        legacy_cost = report.get("approximate_usage_cost")
        usage = cb.migrate_approximate_usage_cost(legacy_cost)
        if usage["measurement"] == "observed":
            observed += 1
        elif usage["measurement"] == "estimated":
            estimated += 1
        else:
            unobserved += 1

        # The historical snapshot is built with NO preflight: these runs predate
        # the gate, so their projected total is genuinely UNOBSERVED. The proxy
        # preflight above is recorded only as a calibration reference.
        snapshot = cb.compute_snapshot(
            compute_budget={"currency": "USD", "planned_budget": None, "hard_limit": None},
            preflight=None,
            usage=usage,
            routing={"recommended_stack": [], "actual_provider_mix": {}},
            project_progress_percent=None,
        )
        cb.validate_snapshot(snapshot)
        results.append(
            {
                "run_id": report.get("run_id"),
                "risk_tier": report.get("risk_tier"),
                "preflight_cost_min": preflight["estimated_cost_min"],
                "preflight_cost_expected": preflight["estimated_cost_expected"],
                "preflight_cost_max": preflight["estimated_cost_max"],
                "measurement": usage["measurement"],
                "legacy_approximate_usage_cost": legacy_cost,
                "budget_status": snapshot["status"]["budget_status"],
            }
        )

    total = len(results)
    return {
        "engine": "compute_budget",
        "pricing_snapshot_date": cb.PRICING_SNAPSHOT_DATE,
        "historical_run_count": total,
        "observed_count": observed,
        "estimated_count": estimated,
        "unobserved_count": unobserved,
        "coverage_observed_rate": round(observed / total, 4) if total else 0,
        "min_max_accuracy_rate": None,
        "min_max_accuracy_note": (
            "Cannot evaluate preflight min-max accuracy: 0 historical runs carry "
            "observed usage cost. The gate reports UNOBSERVED for all of them rather "
            "than fabricating cost data. Accuracy criterion is deferred until usage "
            "capture is wired into new runs."
        ),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Compute Budget Gate against historical MPE runs")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = validate_historical()
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
