"""EXP-13 Pilot Batch 1 attempt runner (experiment-specific, additive only).

Attempts the frozen Pilot Batch 1 pre-registration EXACTLY as registered
(``usage_ref: null`` for every entry) through the registered harness
(``scripts/exp13_harness.py`` / ``scripts/exp13_checks.py``) and records what
happens per case — without fabricating usage telemetry and without editing any
frozen asset:

1. Pre-flight — validate the frozen manifest via the harness's own
   ``plan_batch``; pin the SHA-256 of every frozen input and harness script;
   record git HEAD and confirm the frozen inputs are unmodified.
2. Usage-evidence inventory — for every entry, resolve the usage-evidence path
   the contract requires and check whether real evidence exists (manifest
   ``usage_ref``, ``evidence/exp-13/EXP13-<task>-<route>-USAGE.json``, a Codex
   Router ``usage-events.jsonl``, Codex rollout/session files, any USAGE_RECORD
   in the repository carrying an EXP13 run id).
3. Registered batch attempt — run the harness batch CLI (the documented
   command) against a scratch base directory outside the repository and
   capture its fail-closed behaviour.
4. Per-case attempt — evaluate every manifest entry individually through the
   harness's ``build_record`` with the registered usage (``None``), capturing
   the fail-closed ``ContractError`` per case instead of aborting the loop.
5. Determinism — repeat the per-case evaluation and the batch CLI attempt;
   compare canonical-JSON SHA-256 digests.
6. Integrity checks — every completed record is structurally validated against
   ``contracts/EXP13_EXECUTION_RECORD.schema.json`` semantics and checked for
   false zeros (unobserved must be null, never 0).

Outputs (into --output-dir):

- ``ATTEMPT_REPORT.json``        — full per-case report (deterministic content)
- ``BATCH_ATTEMPT_CONSOLE.txt``  — captured console output of the batch attempts
- ``EXP13-T-008-<route>.json``   — records the harness legitimately produced for
                                   the pre-execution-escalation entries only

This script never writes a usage record, never edits the manifest or any
frozen asset, and never touches production code paths.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts import exp13_checks as ec  # noqa: E402
from scripts import exp13_harness as eh  # noqa: E402
from scripts.triage_engine import ContractError  # noqa: E402
from scripts.usage_instrumentation import validate_usage_record  # noqa: E402

MANIFEST_PATH = ROOT / "evidence" / "exp-13" / "PILOT_BATCH1_PRE_REGISTRATION.json"
DATASET_PATH = ROOT / "experiments" / "exp-13" / "tasks_v2.json"
ROUTES_PATH = ROOT / "experiments" / "exp-13" / "routes.json"
THRESHOLDS_PATH = ROOT / "experiments" / "exp-13" / "thresholds.json"
PRICING_PATH = ROOT / "experiments" / "exp-13" / "pricing_snapshot.json"
CONTRACT_PATH = ROOT / "docs" / "experiments" / "EXP-13_LOW_COST_EVALUATION_HARNESS.md"
RECORD_SCHEMA_PATH = ROOT / "contracts" / "EXP13_EXECUTION_RECORD.schema.json"
REGISTRY_PATH = ROOT / "experiments" / "EXPERIMENT_REGISTRY.json"

FROZEN_INPUT_PATHS = [
    MANIFEST_PATH,
    DATASET_PATH,
    ROUTES_PATH,
    THRESHOLDS_PATH,
    PRICING_PATH,
]
HARNESS_SCRIPT_PATHS = [
    ROOT / "scripts" / "exp13_checks.py",
    ROOT / "scripts" / "exp13_harness.py",
    ROOT / "scripts" / "triage_engine.py",
    ROOT / "scripts" / "usage_instrumentation.py",
    ROOT / "scripts" / "usage_from_router_log.py",
    ROOT / "scripts" / "usage_from_codex_rollout.py",
]

RUN_ID_PATTERN = re.compile(r"^EXP13-T-[0-9]{3}-(A|B|premium)$")
OUTCOMES = {"PASS", "REWORK", "BLOCKED", "HUMAN_REQUIRED"}
ESCALATIONS = {"NONE", "PREMIUM_REQUIRED", "HUMAN_REVIEW_REQUIRED"}
MEASUREMENTS = {"observed", "estimated", "unobserved"}
CHECK_RESULTS = {"PASS", "FAIL", "NOT_APPLICABLE"}

REQUIRED_USAGE_EVIDENCE = {
    "A": (
        "real USAGE_RECORD for this run_id reconstructed by "
        "scripts/usage_from_router_log.py from an isolated, token-metered Codex "
        "Router usage-events.jsonl window of the real execution on route A"
    ),
    "B": (
        "real USAGE_RECORD for this run_id reconstructed by "
        "scripts/usage_from_router_log.py from an isolated, token-metered Codex "
        "Router usage-events.jsonl window of the real execution on route B"
    ),
    "premium": (
        "real USAGE_RECORD for this run_id reconstructed by "
        "scripts/usage_from_codex_rollout.py from one isolated Codex rollout "
        "containing a complete per-call token breakdown for the explicit turn"
    ),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256_bytes(payload.encode("utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def normalize_console(text: str, scratch_dir: str) -> str:
    return text.replace(str(ROOT), "<REPO>").replace(scratch_dir, "<SCRATCH>")


# --------------------------------------------------------------------------- #
# 1. Pre-flight
# --------------------------------------------------------------------------- #


def git_head() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return completed.stdout.strip()


def frozen_inputs_unmodified() -> bool:
    completed = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--"]
        + [str(path.relative_to(ROOT)) for path in FROZEN_INPUT_PATHS + HARNESS_SCRIPT_PATHS],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip() == ""


def pre_flight(dataset: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    entries = eh.plan_batch(manifest, dataset)  # validates run ids, max_runs, fields
    registry = load_json(REGISTRY_PATH)
    exp13 = next(e for e in registry["experiments"] if e["experiment_id"] == "EXP-13")
    return {
        "contract": {
            "path": rel(CONTRACT_PATH),
            "sha256": sha256_file(CONTRACT_PATH),
            "precondition_quote": (
                "The full pilot must not start until every proceeding route has a "
                "valid usage evidence path."
            ),
        },
        "manifest": {
            "path": rel(MANIFEST_PATH),
            "sha256": sha256_file(MANIFEST_PATH),
            "batch_id": manifest["batch_id"],
            "state": manifest["state"],
            "max_runs": manifest["max_runs"],
            "entry_count": len(entries),
            "all_usage_ref_null": all(entry["usage_ref"] is None for entry in entries),
            "validated_by": "scripts.exp13_harness.plan_batch",
        },
        "frozen_assets": [
            {"path": rel(path), "sha256": sha256_file(path)} for path in FROZEN_INPUT_PATHS[1:]
        ],
        "harness_scripts": [
            {"path": rel(path), "sha256": sha256_file(path)} for path in HARNESS_SCRIPT_PATHS
        ],
        "registry_entry_at_attempt": {
            "status": exp13["status"],
            "next_action": exp13["next_action"],
            "result_summary": exp13["result_summary"],
            "updated_at": exp13["updated_at"],
        },
        "git": {
            "head": git_head(),
            "frozen_inputs_unmodified": frozen_inputs_unmodified(),
        },
        "consistency": {
            "manifest_matches_contract_18_runs": len(entries) == 18 and manifest["max_runs"] == 18,
            "registry_consistent_with_contract": (
                exp13["status"] == "READY_TO_TEST"
                and "usage evidence" in exp13["next_action"]
                and "no Pilot Batch 1 runs have executed" in exp13["result_summary"]
            ),
        },
    }


# --------------------------------------------------------------------------- #
# 2. Usage-evidence inventory
# --------------------------------------------------------------------------- #


def router_events_path() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "codex-router" / "usage-events.jsonl"


def codex_home_dir() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))


def scan_repo_for_exp13_usage_records(exclude: Path) -> list[str]:
    """Any file under the repository that looks like a USAGE_RECORD for an EXP13 run."""
    hits: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        if not path.is_file():
            continue
        if exclude in path.parents or ".git" in path.parts:
            continue
        try:
            value = load_json(path)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and RUN_ID_PATTERN.fullmatch(str(value.get("run_id", ""))):
            if "measurement_source" in value and "measurement" in value:
                hits.append(rel(path))
    return hits


def usage_evidence_inventory(manifest: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    evidence_dir = MANIFEST_PATH.parent
    per_entry = []
    for entry in manifest["entries"]:
        run_id = entry["run_id"]
        route = entry["route"]
        task = entry["task_id"]
        candidate = evidence_dir / f"{run_id}-USAGE.json"
        # T-008 legally stops at pre-execution escalation on every route, so it
        # requires no usage evidence; every other entry requires real evidence.
        not_required = task == "T-008"
        required = None if not_required else REQUIRED_USAGE_EVIDENCE[route]
        per_entry.append(
            {
                "run_id": run_id,
                "required_evidence": required,
                "manifest_usage_ref": entry["usage_ref"],
                "candidate_usage_record": {
                    "path": rel(candidate),
                    "exists": candidate.is_file(),
                },
                "evidence_state": (
                    "not_required_pre_execution_escalation"
                    if not_required
                    else ("present" if (entry["usage_ref"] is not None or candidate.is_file()) else "missing")
                ),
            }
        )
    sessions = codex_home_dir() / "sessions"
    rollout_files = sorted(str(p) for p in sessions.rglob("*.jsonl")) if sessions.is_dir() else []
    return {
        "per_entry": per_entry,
        "router_usage_events": {
            "path": str(router_events_path()),
            "exists": router_events_path().is_file(),
        },
        "codex_rollout_files": {
            "searched_dir": str(sessions),
            "count": len(rollout_files),
        },
        "exp13_usage_records_in_repository": scan_repo_for_exp13_usage_records(output_dir),
        "conclusion": (
            "No real usage evidence exists for any proceeding route: the manifest "
            "pre-registers usage_ref null for all 18 entries, no "
            "EXP13-*-USAGE.json file exists, no Codex Router usage-events.jsonl is "
            "present in the execution environment, and no Codex rollout/session "
            "files are present. Only the three T-008 routes legally require no "
            "usage evidence (they stop at pre-execution escalation)."
        ),
    }


# --------------------------------------------------------------------------- #
# 3. Registered batch attempt (documented CLI command, scratch base dir)
# --------------------------------------------------------------------------- #


def attempt_registered_batch(runs: int) -> dict[str, Any]:
    attempts = []
    for index in range(runs):
        with tempfile.TemporaryDirectory(prefix="exp13-batch-attempt-") as scratch:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "exp13_harness.py"),
                    "--batch",
                    str(MANIFEST_PATH),
                    "--base-dir",
                    scratch,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            files_written = sorted(p.name for p in Path(scratch).rglob("*") if p.is_file())
            attempts.append(
                {
                    "run": index + 1,
                    "command": (
                        "python scripts/exp13_harness.py --batch "
                        "evidence/exp-13/PILOT_BATCH1_PRE_REGISTRATION.json "
                        "--base-dir <scratch dir outside the repository>"
                    ),
                    "returncode": completed.returncode,
                    "stdout": normalize_console(completed.stdout, scratch),
                    "stderr": normalize_console(completed.stderr, scratch),
                    "files_written_to_scratch": files_written,
                }
            )
    # The per-attempt "run" index is metadata; determinism compares behaviour.
    content_digests = [
        canonical_digest({key: value for key, value in attempt.items() if key != "run"})
        for attempt in attempts
    ]
    return {
        "attempts": attempts,
        "identical_across_runs": len(set(content_digests)) == 1,
        "fail_closed": all(
            attempt["returncode"] != 0
            and "usage record is required when the run proceeds to execution" in attempt["stderr"]
            and attempt["files_written_to_scratch"] == []
            for attempt in attempts
        ),
    }


# --------------------------------------------------------------------------- #
# 4. Per-case attempt through the registered harness entry point
# --------------------------------------------------------------------------- #


def structurally_validate_record(record: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Structural check against EXP13_EXECUTION_RECORD.schema.json semantics."""
    problems: list[str] = []
    if set(record) != set(schema["required"]):
        problems.append("top-level keys do not match the schema contract")
    if not RUN_ID_PATTERN.fullmatch(record.get("run_id", "")):
        problems.append("run_id does not match the schema pattern")
    if record.get("outcome") not in OUTCOMES:
        problems.append("outcome outside the schema enum")
    if record.get("escalation") not in ESCALATIONS:
        problems.append("escalation outside the schema enum")
    if record.get("cost_measurement") not in MEASUREMENTS:
        problems.append("cost_measurement outside the schema enum")
    if record.get("state") != "EXECUTED":
        problems.append("state must be EXECUTED")
    if record.get("engine_version") != schema["properties"]["engine_version"]["const"]:
        problems.append("engine_version mismatch")
    pre = record.get("pre_execution", {})
    if set(pre) != {"checks", "escalation", "proceeded"}:
        problems.append("pre_execution keys do not match the schema contract")
    for check in pre.get("checks", []) + record.get("checks", []):
        if set(check) != {"check_id", "result", "detail"} or check.get("result") not in CHECK_RESULTS:
            problems.append(f"malformed check entry: {check.get('check_id')}")
            break
    try:
        validate_usage_record(record["usage"])
    except Exception as exc:  # noqa: BLE001 - surfaced as a structural problem
        problems.append(f"embedded usage record invalid: {exc}")
    return problems


def false_zero_problems(record: dict[str, Any]) -> list[str]:
    """Unobserved usage must stay null — absence of telemetry is never a zero."""
    problems: list[str] = []
    usage = record["usage"]
    if usage["measurement"] == "unobserved":
        for field in (
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "observed_cost",
            "model_calls",
            "tool_calls",
            "retries",
            "start_time",
            "end_time",
        ):
            if usage[field] is not None:
                problems.append(f"unobserved usage field {field} is {usage[field]!r}, must be null")
        if usage["provider"] is not None or usage["model"] is not None:
            problems.append("unobserved usage names a provider/model")
        if usage["measurement_source"] != "none":
            problems.append("unobserved usage must have measurement_source 'none'")
        if record["cost_usd"] is not None:
            problems.append("unobserved run carries a non-null cost_usd")
        if record["cost_measurement"] != "unobserved":
            problems.append("unobserved run is not labelled cost_measurement 'unobserved'")
        for field in ("retries", "model_calls", "tool_calls"):
            if record[field] is not None:
                problems.append(f"unobserved run carries non-null {field}")
    return problems


def evaluate_entry(
    entry: dict[str, Any],
    dataset: dict[str, Any],
    routes: dict[str, Any],
    thresholds: dict[str, Any],
    pricing: dict[str, Any],
    base_dir: Path,
) -> dict[str, Any]:
    """One manifest entry through the harness, exactly as run_batch would treat it."""
    task = eh.load_task(dataset, entry["task_id"])
    usage = load_json(base_dir / entry["usage_ref"]) if entry["usage_ref"] is not None else None
    try:
        record = eh.build_record(
            task, entry["route"], routes, thresholds, pricing, usage=usage, defects=entry["defects"]
        )
    except ContractError as exc:
        pre = ec.pre_execution(task, entry["route"], eh.routes_map(routes))
        return {
            "run_id": entry["run_id"],
            "task_id": entry["task_id"],
            "route": entry["route"],
            "input_classification": {
                "expected_risk_tier": task["expected"]["risk_tier"],
                "expected_human_approval_required": task["expected"]["human_approval_required"],
                "triage_risk_tier": pre["triage"]["recommended_risk_tier"],
                "triage_human_approval_required": pre["triage"]["human_approval_required"],
                "triage_expected_match": next(
                    c["result"] for c in pre["checks"] if c["check_id"] == "triage_expected_match"
                ),
                "human_approval_reasons": pre["triage"]["human_approval_reasons"],
            },
            "usage_evidence_state": "unobserved",
            "usage_evidence_detail": (
                "no USAGE_RECORD exists for this run_id (manifest usage_ref is null; "
                "no Router/rollout telemetry available); none was fabricated"
            ),
            "pre_execution_decision": {
                "escalation": pre["escalation"],
                "proceeded": pre["proceeded"],
                "checks": [{k: c[k] for k in ("check_id", "result")} for c in pre["checks"]],
            },
            "budget_compute_estimate": {
                "produced": False,
                "cost_usd": None,
                "cost_measurement": "unobserved",
                "reason": (
                    "no execution happened; the contract forbids fabricating cost "
                    "without telemetry"
                ),
            },
            "gate_result": "BLOCKED_BY_EVIDENCE_GATE",
            "reason": f"ContractError: {exc}",
            "record_produced": False,
        }

    pre_checks = record["pre_execution"]["checks"]
    return {
        "run_id": record["run_id"],
        "task_id": record["task_id"],
        "route": record["route"],
        "input_classification": {
            "expected_risk_tier": task["expected"]["risk_tier"],
            "expected_human_approval_required": task["expected"]["human_approval_required"],
            "triage_risk_tier": record["triage"]["recommended_risk_tier"],
            "triage_human_approval_required": record["triage"]["human_approval_required"],
            "triage_expected_match": next(
                c["result"] for c in pre_checks if c["check_id"] == "triage_expected_match"
            ),
            "human_approval_reasons": record["triage"]["human_approval_reasons"],
        },
        "usage_evidence_state": record["usage"]["measurement"],
        "usage_evidence_detail": (
            "run stopped at pre-execution escalation before any execution; the "
            "harness stores the empty, unobserved usage record (nulls, no zeros)"
        ),
        "pre_execution_decision": {
            "escalation": record["escalation"],
            "proceeded": record["pre_execution"]["proceeded"],
            "checks": [{k: c[k] for k in ("check_id", "result")} for c in pre_checks],
        },
        "budget_compute_estimate": {
            "produced": False,
            "cost_usd": record["cost_usd"],
            "cost_measurement": record["cost_measurement"],
            "reason": (
                "escalated run is not executed; cost stays null / unobserved by contract"
            ),
        },
        "gate_result": (
            "COMPLETED_PRE_EXECUTION_ESCALATION"
            if record["outcome"] == "HUMAN_REQUIRED"
            else record["outcome"]
        ),
        "reason": (
            "triage mandates human approval ("
            + ", ".join(record["triage"]["human_approval_reasons"])
            + "); the run stops before execution on every route"
        ),
        "record_produced": True,
        "record": record,
    }


def attempt_all_entries(
    manifest: dict[str, Any],
    dataset: dict[str, Any],
    routes: dict[str, Any],
    thresholds: dict[str, Any],
    pricing: dict[str, Any],
    base_dir: Path,
) -> list[dict[str, Any]]:
    results = []
    for entry in manifest["entries"]:
        results.append(evaluate_entry(entry, dataset, routes, thresholds, pricing, base_dir))
    return results


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> int:
    parser = argparse.ArgumentParser(description="Attempt the frozen EXP-13 Pilot Batch 1 registration")
    parser.add_argument("--date", required=True, help="attempt date (YYYY-MM-DD), also the report date")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=3, help="per-case determinism repetitions")
    parser.add_argument("--batch-cli-runs", type=int, default=2, help="registered batch CLI attempts")
    args = parser.parse_args()
    if args.repetitions < 2 or args.batch_cli_runs < 2:
        parser.error("--repetitions and --batch-cli-runs must be >= 2 for determinism checks")

    manifest = load_json(MANIFEST_PATH)
    dataset = load_json(DATASET_PATH)
    routes = load_json(ROUTES_PATH)
    thresholds = load_json(THRESHOLDS_PATH)
    pricing = load_json(PRICING_PATH)
    record_schema = load_json(RECORD_SCHEMA_PATH)

    output_dir = args.output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise SystemExit(f"output dir not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Pre-flight
    pre = pre_flight(dataset, manifest)

    # 2. Usage-evidence inventory
    inventory = usage_evidence_inventory(manifest, output_dir)

    # 3. Registered batch attempt (fail-closed capture)
    batch_attempt = attempt_registered_batch(args.batch_cli_runs)

    # 4. Per-case attempt, repeated for determinism
    repetitions = []
    for _ in range(args.repetitions):
        repetitions.append(
            attempt_all_entries(manifest, dataset, routes, thresholds, pricing, MANIFEST_PATH.parent)
        )
    first = repetitions[0]
    per_case_digests = [
        {
            "run_id": case["run_id"],
            "digest": canonical_digest(case),
            "identical_across_repetitions": all(
                canonical_digest(rep[index]) == canonical_digest(case)
                for rep in repetitions
            ),
        }
        for index, case in enumerate(first)
    ]
    determinism_pass = all(item["identical_across_repetitions"] for item in per_case_digests) and (
        batch_attempt["identical_across_runs"]
    )

    # 5. Structural + no-false-zero validation of every produced record
    structural_problems: dict[str, list[str]] = {}
    false_zeros: dict[str, list[str]] = {}
    for case in first:
        if case["record_produced"]:
            problems = structurally_validate_record(case["record"], record_schema)
            zeros = false_zero_problems(case["record"])
            if problems:
                structural_problems[case["run_id"]] = problems
            if zeros:
                false_zeros[case["run_id"]] = zeros

    # 6. Write the records the harness legitimately produced (pre-execution
    #    escalations only — proceeding runs produced none).
    record_outputs = []
    for case in first:
        if not case["record_produced"]:
            continue
        path = output_dir / f"{case['run_id']}.json"
        rendered = json.dumps(case["record"], ensure_ascii=False, indent=2) + "\n"
        path.write_text(rendered, encoding="utf-8")
        record_outputs.append(
            {
                "run_id": case["run_id"],
                "path": rel(path),
                "sha256": sha256_bytes(rendered.encode("utf-8")),
            }
        )
        case.pop("record")

    completed = [case for case in first if case["gate_result"] == "COMPLETED_PRE_EXECUTION_ESCALATION"]
    blocked = [case for case in first if case["gate_result"] == "BLOCKED_BY_EVIDENCE_GATE"]
    unexpected = [
        case["run_id"] for case in first if case["gate_result"] not in {
            "COMPLETED_PRE_EXECUTION_ESCALATION", "BLOCKED_BY_EVIDENCE_GATE"
        }
    ]
    executed = [
        case["run_id"]
        for case in first
        if case["record_produced"] and case["pre_execution_decision"]["proceeded"]
    ]

    coverage = {
        "total_registered": len(manifest["entries"]),
        "attempted": len(first),
        "completed_via_pre_execution_escalation": len(completed),
        "blocked_by_evidence_gate": len(blocked),
        "proceeded_to_execution": len(executed),
        "proceeded_run_ids": executed,
        "unexpected_gate_results": unexpected,
    }

    integrity = {
        "records_structurally_valid": not structural_problems,
        "structural_problems": structural_problems,
        "no_false_zeros_verified": not false_zeros,
        "false_zero_findings": false_zeros,
        "budget_gate_fail_closed": {
            "preflight_failure_never_proceeds": all(
                case["pre_execution_decision"]["proceeded"] is False
                and case["pre_execution_decision"]["escalation"] == "HUMAN_REVIEW_REQUIRED"
                for case in completed
            ),
            "missing_usage_never_passes": all(
                case["record_produced"] is False for case in blocked
            ),
            "registered_batch_cli_failed_closed_with_no_partial_writes": batch_attempt["fail_closed"],
        },
        "usage_evidence_states_observed": {
            "observed": sum(1 for c in first if c["usage_evidence_state"] == "observed"),
            "estimated": sum(1 for c in first if c["usage_evidence_state"] == "estimated"),
            "unobserved": sum(1 for c in first if c["usage_evidence_state"] == "unobserved"),
        },
    }

    evidence_refs = {
        "manifest": {"path": rel(MANIFEST_PATH), "sha256": sha256_file(MANIFEST_PATH)},
        "task_dataset": {"path": rel(DATASET_PATH), "sha256": sha256_file(DATASET_PATH)},
        "routes": {"path": rel(ROUTES_PATH), "sha256": sha256_file(ROUTES_PATH)},
        "thresholds": {"path": rel(THRESHOLDS_PATH), "sha256": sha256_file(THRESHOLDS_PATH)},
        "pricing": {"path": rel(PRICING_PATH), "sha256": sha256_file(PRICING_PATH)},
        "harness_entry_points": [rel(p) for p in HARNESS_SCRIPT_PATHS[:2]],
        "produced_records": record_outputs,
    }

    report = {
        "report_version": "1.0",
        "attempt_id": f"EXP13-PILOT-BATCH1-ATTEMPT-{args.date}",
        "attempt_date": args.date,
        "experiment": "EXP-13",
        "batch_state_after_attempt": (
            "ATTEMPTED_NOT_EXECUTED — the registered batch fails closed at the "
            "usage-evidence gate; no run proceeded to execution and no usage or "
            "cost value was fabricated"
        ),
        "pre_flight": pre,
        "usage_evidence_inventory": inventory,
        "registered_batch_attempt": batch_attempt,
        "cases": first,
        "coverage": coverage,
        "determinism": {
            "repetitions": args.repetitions,
            "batch_cli_runs": args.batch_cli_runs,
            "per_case_digests": per_case_digests,
            "batch_attempt_identical_across_runs": batch_attempt["identical_across_runs"],
            "deterministic": determinism_pass,
        },
        "integrity_checks": integrity,
        "evidence_references": evidence_refs,
    }

    report_path = output_dir / "ATTEMPT_REPORT.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    console = []
    console.append(f"EXP-13 Pilot Batch 1 attempt — {args.date}")
    console.append(f"repo HEAD: {pre['git']['head']}")
    console.append(f"manifest: {rel(MANIFEST_PATH)} sha256={pre['manifest']['sha256']}")
    console.append("")
    console.append("== Registered batch CLI attempts (fail-closed capture) ==")
    for attempt in batch_attempt["attempts"]:
        console.append(f"run {attempt['run']}: returncode={attempt['returncode']} files_written={attempt['files_written_to_scratch']}")
        for line in attempt["stderr"].strip().splitlines()[-3:]:
            console.append(f"  | {line}")
    console.append("")
    console.append("== Per-case attempt results ==")
    for case in first:
        console.append(
            f"{case['run_id']}: {case['gate_result']} "
            f"(escalation={case['pre_execution_decision']['escalation']}, "
            f"proceeded={case['pre_execution_decision']['proceeded']}, "
            f"usage={case['usage_evidence_state']})"
        )
    console.append("")
    console.append(f"coverage: {json.dumps(coverage)}")
    console.append(f"determinism: deterministic={determinism_pass}")
    console.append(f"integrity: {json.dumps(integrity['budget_gate_fail_closed'])}")
    console_path = output_dir / "BATCH_ATTEMPT_CONSOLE.txt"
    console_path.write_text("\n".join(console) + "\n", encoding="utf-8")

    print(json.dumps({
        "report": rel(report_path),
        "console": rel(console_path),
        "coverage": coverage,
        "deterministic": determinism_pass,
        "fail_closed": batch_attempt["fail_closed"],
        "records_structurally_valid": integrity["records_structurally_valid"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
