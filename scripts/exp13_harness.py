"""EXP-13 low-cost evaluation harness.

Deterministic wrapper around ``scripts/exp13_checks.py`` that turns a task and
a route into an immutable ``EXP13_EXECUTION_RECORD``. The harness never invents
telemetry: a run that proceeds to execution requires a real ``USAGE_RECORD`` as
input, and a run that escalates before execution stores an empty, unobserved
usage record.

Batch rules
-----------
The Pilot Batch 1 manifest pre-registers 6 tasks x 3 routes = 18 runs. The
harness enforces the frozen STOP rule: it never processes more than
``max_runs`` entries from a manifest, and a manifest with more entries is
rejected.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Optional

try:
    from scripts.exp13_checks import (
        ContractError,
        evaluate,
        empty_usage,
        resolve_model_slug,
    )
    from scripts.usage_instrumentation import validate_usage_record
except ModuleNotFoundError:  # Direct `python scripts/exp13_harness.py` execution.
    from exp13_checks import ContractError, evaluate, empty_usage, resolve_model_slug
    from usage_instrumentation import validate_usage_record

ROOT = Path(__file__).resolve().parents[1]

TASK_ID_PATTERN = re.compile(r"^T-[0-9]{3}$")

DEFAULT_TASKS = ROOT / "experiments" / "exp-13" / "tasks_v2.json"
DEFAULT_ROUTES = ROOT / "experiments" / "exp-13" / "routes.json"
DEFAULT_THRESHOLDS = ROOT / "experiments" / "exp-13" / "thresholds.json"
DEFAULT_PRICING = ROOT / "experiments" / "exp-13" / "pricing_snapshot.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def routes_map(routes: dict[str, Any]) -> dict[str, Any]:
    """Accept either the raw A/B/premium map or the routes.json envelope."""
    if "routes" in routes and isinstance(routes["routes"], dict):
        return routes["routes"]
    return routes


def make_run_id(task_id: str, route: str) -> str:
    if not TASK_ID_PATTERN.fullmatch(task_id):
        raise ContractError(f"invalid task_id: {task_id!r}")
    if route not in ("A", "B", "premium"):
        raise ContractError(f"invalid route: {route!r}")
    return f"EXP13-{task_id}-{route}"


def load_task(dataset: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = dataset.get("tasks")
    if not isinstance(tasks, list):
        raise ContractError("dataset must contain a tasks list")
    for task in tasks:
        if isinstance(task, dict) and task.get("task_id") == task_id:
            return task
    raise ContractError(f"task not found in dataset: {task_id!r}")


def build_record(
    task: dict[str, Any],
    route: str,
    routes: dict[str, Any],
    thresholds: dict[str, Any],
    pricing: dict[str, Any],
    usage: Optional[dict[str, Any]] = None,
    defects: Optional[list[str]] = None,
    budget: Optional[float] = None,
) -> dict[str, Any]:
    """Build an EXP13_EXECUTION_RECORD for one task + route."""
    task_id = task["task_id"]
    run_id = make_run_id(task_id, route)
    routes = routes_map(routes)
    model_slug = resolve_model_slug(route, routes)

    if usage is not None:
        validate_usage_record(usage)
        if usage["run_id"] != run_id:
            raise ContractError(f"usage run_id {usage['run_id']!r} does not match record run_id {run_id!r}")

    payload = evaluate(task, route, routes, thresholds, pricing, usage=usage, defects=defects, budget=budget)
    # An escalated run never executes, so its stored usage is the empty,
    # unobserved record regardless of any caller-supplied usage.
    record_usage = usage if payload["pre_execution"]["proceeded"] else empty_usage(run_id)

    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "task_id": task_id,
        "route": route,
        "model_slug": model_slug,
        "triage": payload["triage"],
        "pre_execution": payload["pre_execution"],
        "checks": payload["checks"],
        "usage": record_usage,
        "defects": payload["defects"],
        "retries": payload["retries"],
        "model_calls": payload["model_calls"],
        "tool_calls": payload["tool_calls"],
        "escalation": payload["escalation"],
        "outcome": payload["outcome"],
        "cost_usd": payload["cost_usd"],
        "cost_measurement": payload["cost_measurement"],
        "engine_version": payload["engine_version"],
        "state": "EXECUTED",
    }


def validate_manifest(manifest: dict[str, Any]) -> None:
    if not isinstance(manifest, dict) or "entries" not in manifest or "max_runs" not in manifest:
        raise ContractError("manifest must contain entries and max_runs")
    if type(manifest["max_runs"]) is not int or manifest["max_runs"] < 1:
        raise ContractError("max_runs must be a positive integer")
    entries = manifest["entries"]
    if not isinstance(entries, list) or not entries:
        raise ContractError("manifest entries must be a non-empty list")
    if len(entries) > manifest["max_runs"]:
        raise ContractError(
            f"manifest has {len(entries)} entries which exceeds max_runs {manifest['max_runs']}; STOP, do not auto-continue"
        )


def plan_batch(manifest: dict[str, Any], dataset: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate a batch manifest and return its pre-registered entries."""
    validate_manifest(manifest)
    for entry in manifest["entries"]:
        if not isinstance(entry, dict) or set(entry) != {"run_id", "task_id", "route", "usage_ref", "defects"}:
            raise ContractError("manifest entry fields do not match the contract")
        expected = make_run_id(entry["task_id"], entry["route"])
        if entry["run_id"] != expected:
            raise ContractError(f"entry run_id {entry['run_id']!r} must equal {expected!r}")
        load_task(dataset, entry["task_id"])
        if entry["usage_ref"] is not None and not isinstance(entry["usage_ref"], str):
            raise ContractError("usage_ref must be a string or null")
        if not isinstance(entry["defects"], list) or not all(isinstance(item, str) and item for item in entry["defects"]):
            raise ContractError("entry defects must be a list of non-empty strings")
    return list(manifest["entries"])


def run_batch(
    manifest: dict[str, Any],
    dataset: dict[str, Any],
    routes: dict[str, Any],
    thresholds: dict[str, Any],
    pricing: dict[str, Any],
    base_dir: Path,
) -> dict[str, Any]:
    """Execute a batch manifest (bounded by max_runs) and write records + summary."""
    entries = plan_batch(manifest, dataset)
    records: list[dict[str, Any]] = []
    for entry in entries:
        task = load_task(dataset, entry["task_id"])
        if entry["usage_ref"] is None:
            raise ContractError(
                f"entry {entry['run_id']} has no usage_ref; real USAGE_RECORD evidence is required after merge"
            )
        usage = load_json(base_dir / entry["usage_ref"])
        record = build_record(task, entry["route"], routes, thresholds, pricing, usage=usage, defects=entry["defects"])
        records.append(record)
        out = base_dir / f"{record['run_id']}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = summarize(records)
    summary_path = base_dir / f"{manifest.get('batch_id', 'batch')}_SUMMARY.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"batch_id": manifest.get("batch_id"), "records": records, "summary": summary}


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate a list of EXP13_EXECUTION_RECORD values for post-batch analysis."""
    by_outcome = Counter(record["outcome"] for record in records)
    by_escalation = Counter(record["escalation"] for record in records)
    by_route = {}
    defects_total = 0
    cost_total = 0.0
    for record in records:
        route = record["route"]
        bucket = by_route.setdefault(route, {"runs": 0, "cost_usd": 0.0, "outcomes": Counter()})
        bucket["runs"] += 1
        if record["cost_usd"] is not None:
            bucket["cost_usd"] = round(bucket["cost_usd"] + record["cost_usd"], 4)
            cost_total = round(cost_total + record["cost_usd"], 4)
        bucket["outcomes"][record["outcome"]] += 1
        defects_total += len(record["defects"])
    for bucket in by_route.values():
        bucket["outcomes"] = dict(bucket["outcomes"])
    return {
        "run_count": len(records),
        "outcomes": dict(by_outcome),
        "escalations": dict(by_escalation),
        "defects_total": defects_total,
        "cost_usd_total": cost_total,
        "by_route": by_route,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="EXP-13 low-cost evaluation harness")
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--routes", type=Path, default=DEFAULT_ROUTES)
    parser.add_argument("--thresholds", type=Path, default=DEFAULT_THRESHOLDS)
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING)
    parser.add_argument("--task", help="task_id (e.g. T-001) for a single run")
    parser.add_argument("--route", choices=["A", "B", "premium"], help="route for a single run")
    parser.add_argument("--usage", type=Path, help="USAGE_RECORD JSON for an executed run")
    parser.add_argument("--defects", help="comma-separated defect ids")
    parser.add_argument("--budget", type=float, help="hard budget limit for the cost check")
    parser.add_argument("--batch", type=Path, help="batch manifest (bounded by max_runs)")
    parser.add_argument("--base-dir", type=Path, help="directory for batch outputs/usage refs")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    dataset = load_json(args.tasks)
    routes = load_json(args.routes)
    thresholds = load_json(args.thresholds)
    pricing = load_json(args.pricing)

    if args.batch:
        manifest = load_json(args.batch)
        base_dir = (args.base_dir or args.batch.parent).resolve()
        result = run_batch(manifest, dataset, routes, thresholds, pricing, base_dir)
        print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
        return 0

    if not args.task or not args.route:
        parser.error("--task and --route are required without --batch")

    task = load_task(dataset, args.task)
    usage = load_json(args.usage) if args.usage else None
    defects = [item for item in (args.defects or "").split(",") if item] if args.defects else []
    record = build_record(task, args.route, routes, thresholds, pricing, usage=usage, defects=defects, budget=args.budget)
    rendered = json.dumps(record, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
