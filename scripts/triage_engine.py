from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEEP_CHANGE_SIGNALS = {
    "architecture_redesign",
    "new_orchestration_authority",
    "persistent_agents",
    "persistent_runtime_state",
    "router_authority_change",
    "workflow_engine",
}

APPROVAL_SIGNALS = DEEP_CHANGE_SIGNALS | {
    "destructive_operation",
    "production_change",
    "security_or_permissions_change",
    "sensitive_data_write",
}

ALLOWED_SIGNALS = APPROVAL_SIGNALS | {"shared_component"}
RATING_KEYS = {"complexity", "risk", "architectural_impact", "data_sensitivity", "unknowns"}
INPUT_KEYS = {"task_id", "summary", "affected_repositories", "acceptance_criteria_present", "rollback_known", "ratings", "signals"}


class ContractError(ValueError):
    pass


def validate_task(task: dict[str, Any]) -> None:
    if not isinstance(task, dict) or set(task) != INPUT_KEYS:
        raise ContractError("triage input fields do not match the contract")
    if not isinstance(task["task_id"], str) or not task["task_id"] or not isinstance(task["summary"], str) or not task["summary"]:
        raise ContractError("task_id and summary must be non-empty strings")
    repos = task["affected_repositories"]
    if not isinstance(repos, list) or any(not isinstance(item, str) or not item for item in repos) or len(repos) != len(set(repos)):
        raise ContractError("affected_repositories must contain unique non-empty strings")
    if not isinstance(task["acceptance_criteria_present"], bool) or not isinstance(task["rollback_known"], bool):
        raise ContractError("acceptance_criteria_present and rollback_known must be booleans")
    ratings = task["ratings"]
    if not isinstance(ratings, dict) or set(ratings) != RATING_KEYS:
        raise ContractError("ratings fields do not match the contract")
    if any(type(value) is not int or not 0 <= value <= 4 for value in ratings.values()):
        raise ContractError("ratings must be integers from 0 through 4")
    signals = task["signals"]
    if not isinstance(signals, list) or len(signals) != len(set(signals)) or not set(signals) <= ALLOWED_SIGNALS:
        raise ContractError("signals must be unique values from the contract vocabulary")


def _clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, value))


def triage(task: dict[str, Any]) -> dict[str, Any]:
    validate_task(task)
    signals = set(task["signals"])
    affected = task["affected_repositories"]
    ratings = task["ratings"]

    unknowns = ratings["unknowns"]
    execution_confidence = _clamp(
        100
        - unknowns * 15
        - (0 if task["acceptance_criteria_present"] else 20)
        - (0 if task["rollback_known"] else 10)
        - (10 if not affected else 0)
    )

    blast_radius = min(
        4,
        max(0, len(affected) - 1)
        + (1 if "shared_component" in signals else 0)
        + (1 if "production_change" in signals else 0),
    )
    architectural_impact = max(
        ratings["architectural_impact"],
        4 if signals & DEEP_CHANGE_SIGNALS else 0,
        2 if "shared_component" in signals else 0,
    )
    data_sensitivity = max(
        ratings["data_sensitivity"],
        4 if "sensitive_data_write" in signals else 0,
        3 if "security_or_permissions_change" in signals else 0,
    )
    complexity = ratings["complexity"]
    risk = max(ratings["risk"], architectural_impact, data_sensitivity, blast_radius)

    deep_change_probability = _clamp(
        architectural_impact * 12
        + unknowns * 5
        + min(20, max(0, len(affected) - 1) * 5)
        + min(40, len(signals & DEEP_CHANGE_SIGNALS) * 20)
    )
    human_reasons = sorted(signals & APPROVAL_SIGNALS)
    if architectural_impact >= 4 and not signals & DEEP_CHANGE_SIGNALS:
        human_reasons.append("maximum_architectural_impact")
    if data_sensitivity >= 4 and "sensitive_data_write" not in human_reasons:
        human_reasons.append("high_data_sensitivity")
    if deep_change_probability >= 50 and not signals & DEEP_CHANGE_SIGNALS:
        human_reasons.append("deep_change_probability_threshold")

    if architectural_impact >= 4 or deep_change_probability >= 50 or signals & DEEP_CHANGE_SIGNALS:
        risk_tier = "DEEP-CHANGE"
    elif risk >= 2 or complexity >= 2 or unknowns >= 2 or execution_confidence < 80:
        risk_tier = "VERIFIED"
    else:
        risk_tier = "FAST"

    return {
        "task_id": task["task_id"],
        "execution_confidence": execution_confidence,
        "complexity": complexity,
        "risk": risk,
        "blast_radius": blast_radius,
        "affected_repositories": affected,
        "architectural_impact": architectural_impact,
        "data_sensitivity": data_sensitivity,
        "unknowns": unknowns,
        "deep_change_probability": deep_change_probability,
        "human_approval_required": bool(human_reasons),
        "human_approval_reasons": human_reasons,
        "recommended_risk_tier": risk_tier,
        "engine_version": "0.1.0",
    }


def backtest(dataset: dict[str, Any]) -> dict[str, Any]:
    cases = []
    exact = 0
    approval_exact = 0
    deep_false_negatives = 0
    for case in dataset["cases"]:
        output = triage(case["input"])
        tier_match = output["recommended_risk_tier"] == case["expected"]["risk_tier"]
        approval_match = output["human_approval_required"] == case["expected"]["human_approval_required"]
        exact += int(tier_match and approval_match)
        approval_exact += int(approval_match)
        deep_false_negatives += int(case["expected"]["risk_tier"] == "DEEP-CHANGE" and output["recommended_risk_tier"] != "DEEP-CHANGE")
        cases.append({"case_id": case["case_id"], "tier_match": tier_match, "approval_match": approval_match, "output": output})
    count = len(cases)
    return {
        "engine_version": "0.1.0",
        "dataset_version": dataset["dataset_version"],
        "case_count": count,
        "exact_match_count": exact,
        "exact_match_rate": round(exact / count, 4) if count else 0,
        "approval_match_rate": round(approval_exact / count, 4) if count else 0,
        "deep_change_false_negatives": deep_false_negatives,
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# Governed task entry — EXTEND_EXISTING wiring of the real Task Packet intake
# to the already-validated execution path.
#
# The triage CLI is the canonical production-like entry point that ingests a
# Task Packet. This opt-in ``governed_run`` mode routes that SAME Task Packet
# through ``execution_runner.run_task`` (accept_task -> dispatch_with_autonomy
# -> evaluate_autonomy -> enforce_execution -> [injected executor]) instead of
# only printing the risk tier. It adds no new orchestration framework,
# storage, queue, daemon, API, or provider: the executor stays an injected,
# provider-neutral callable (the CLI default is a non-mutating dry-run probe
# that performs zero real work). Safety/history/level are conservative by
# default (history=[], current_level="L0", every hard-safety signal False),
# trust is never inferred from executor identity, and every error fails closed
# (no executor call, deterministic BLOCKED result). The default triage /
# backtest behavior is unchanged.
# ---------------------------------------------------------------------------

_DEFAULT_LEVEL = "L0"


def governed_dry_run_executor(decision: dict[str, Any]) -> dict[str, Any]:
    """Non-mutating default executor for the governed-run intake.

    Performs NO real work and NO provider call — it only acknowledges that the
    single enforcement gate permitted execution, so the CLI can exercise the
    acceptance/dispatch boundary without mutating anything. Real executors are
    injected programmatically; none are shipped here.
    """
    return {
        "status": "PROBE_ONLY",
        "executed": False,
        "note": "dry-run executor: no work performed; inject a real executor for execution",
        "task_id": decision.get("task_id") if isinstance(decision, dict) else None,
    }


def governed_run(
    task: dict[str, Any],
    executor=None,
    history: list[dict[str, Any]] | None = None,
    current_level: str = _DEFAULT_LEVEL,
    *,
    approval_recorded: bool = False,
    scope_violation: bool = False,
    security_violation: bool = False,
    secrets_restricted: bool = False,
    production_restricted: bool = False,
    stop_condition: bool = False,
    required_checks: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Run one real Task Packet through the governed execution path.

    Thin intake adapter over ``execution_runner.run_task`` — it contains no
    acceptance/dispatch logic of its own and never calls an executor directly.
    Fail-closed: any parsing / integration / wiring error returns a deterministic
    BLOCKED result with ``executor_invoked = False`` and never invokes the
    executor.
    """
    safe_task_id = task.get("task_id") if isinstance(task, dict) else None
    try:
        try:  # normal package / module import
            from scripts.execution_runner import run_task
        except Exception:  # when loaded standalone via the scripts/ path (CLI, tests)
            from execution_runner import run_task  # type: ignore

        if executor is None:
            executor = governed_dry_run_executor

        result = run_task(
            task,
            executor,
            history=[] if history is None else history,
            current_level=current_level,
            approval_recorded=approval_recorded,
            scope_violation=scope_violation,
            security_violation=security_violation,
            secrets_restricted=secrets_restricted,
            production_restricted=production_restricted,
            stop_condition=stop_condition,
            required_checks=required_checks,
        )
        if not isinstance(result, dict) or "executor_invoked" not in result:
            raise ValueError("runner returned an invalid result contract")
        return result
    except Exception as exc:  # fail-closed: never call executor, deterministic block
        return {
            "task_id": safe_task_id,
            "acceptance_state": "BLOCKED",
            "allowed_action": "OBSERVE",
            "executor_invoked": False,
            "approval_recorded": approval_recorded,
            "execution_status": "BLOCKED",
            "execution_result": None,
            "blocking_reasons": ["entry_integration_error"],
            "reason": f"fail-closed entry error: {type(exc).__name__}: {exc}",
            "events": ["intake"],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic MPE task triage")
    parser.add_argument("input", type=Path)
    parser.add_argument("--backtest", action="store_true")
    parser.add_argument(
        "--governed-run",
        action="store_true",
        help="route the Task Packet through the governed execution path "
        "(accept_task -> dispatch -> enforce_execution) instead of only triaging",
    )
    parser.add_argument("--level", default=_DEFAULT_LEVEL, help="current autonomy level L0-L4")
    parser.add_argument("--approval-recorded", action="store_true")
    parser.add_argument("--scope-violation", action="store_true")
    parser.add_argument("--security-violation", action="store_true")
    parser.add_argument("--secrets-restricted", action="store_true")
    parser.add_argument("--production-restricted", action="store_true")
    parser.add_argument("--stop-condition", action="store_true")
    parser.add_argument(
        "--history-file",
        type=Path,
        help="JSON file with a trusted run-history list for the governed run "
        "(injected; defaults to empty history — no storage is built here)",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if args.backtest and args.governed_run:
        parser.error("--backtest and --governed-run are mutually exclusive")
    if args.governed_run:
        history = []
        if args.history_file:
            history = json.loads(args.history_file.read_text(encoding="utf-8"))
        result = governed_run(
            payload,
            history=history,
            current_level=args.level,
            approval_recorded=args.approval_recorded,
            scope_violation=args.scope_violation,
            security_violation=args.security_violation,
            secrets_restricted=args.secrets_restricted,
            production_restricted=args.production_restricted,
            stop_condition=args.stop_condition,
        )
    else:
        result = backtest(payload) if args.backtest else triage(payload)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
