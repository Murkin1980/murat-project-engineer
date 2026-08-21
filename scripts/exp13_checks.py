"""EXP-13 low-cost evaluation checks.

Deterministic, dependency-free check pipeline for the EXP-13 low-cost
evaluation harness. The harness evaluates whether a task can be executed
safely on a chosen route (A / B / premium) BEFORE spending real budget, and
records the outcome in an ``EXP13_EXECUTION_RECORD``.

Frozen semantics (change only in a new dataset / thresholds / pricing version)
------------------------------------------------------------------------------
- Routes A / B / premium resolve through the frozen ``routes.json`` to explicit
  model slugs priced in the frozen ``pricing_snapshot.json``.
- Pre-execution checks (cheap, run before any execution):
  ``route_resolves``, ``triage_expected_match``, ``acceptance_present``,
  ``human_review_due``.
- Execution checks (run only when the pre-execution stage proceeds):
  ``usage_valid``, ``usage_consistent``, ``retries_within_limit``,
  ``defects_within_limit``, ``cost_within_limit``.
- Escalation is DERIVED, never hand-set:
  ``HUMAN_REVIEW_REQUIRED`` when triage mandates human approval;
  ``PREMIUM_REQUIRED`` when a DEEP-CHANGE task is routed to a non-premium
  route; otherwise ``NONE``.
- Outcome is DERIVED, never hand-set:
  ``HUMAN_REQUIRED`` for a human-approval escalation;
  ``REWORK`` for a premium escalation or any non-fatal check failure;
  ``BLOCKED`` when the usage evidence is invalid;
  ``PASS`` when every check passes.
- Cost is never fabricated: observed spend stays observed; reconstructed spend
  stays estimated; missing spend stays null (unobserved).
"""

from __future__ import annotations

from typing import Any, Optional

try:
    from scripts.triage_engine import INPUT_KEYS, ContractError, triage, validate_task as validate_triage_task
    from scripts.usage_instrumentation import UsageInstrumentationError, empty_record, validate_usage_record
except ModuleNotFoundError:  # Direct `python scripts/exp13_checks.py` execution.
    from triage_engine import INPUT_KEYS, ContractError, triage, validate_task as validate_triage_task
    from usage_instrumentation import UsageInstrumentationError, empty_record, validate_usage_record

ROUTES = ("A", "B", "premium")
RISK_TIERS = ("FAST", "VERIFIED", "DEEP-CHANGE")
ESCALATIONS = ("NONE", "PREMIUM_REQUIRED", "HUMAN_REVIEW_REQUIRED")
OUTCOMES = ("PASS", "REWORK", "BLOCKED", "HUMAN_REQUIRED")
CHECK_RESULTS = ("PASS", "FAIL", "NOT_APPLICABLE")
MEASUREMENTS = ("observed", "estimated", "unobserved")

PRE_EXECUTION_CHECK_IDS = (
    "route_resolves",
    "triage_expected_match",
    "acceptance_present",
    "human_review_due",
)
EXECUTION_CHECK_IDS = (
    "usage_valid",
    "usage_consistent",
    "retries_within_limit",
    "defects_within_limit",
    "cost_within_limit",
)
ALL_CHECK_IDS = PRE_EXECUTION_CHECK_IDS + EXECUTION_CHECK_IDS

ENGINE_VERSION = "0.1.0"

EXPECTED_KEYS = {"risk_tier", "human_approval_required"}


def validate_expected(label: dict[str, Any]) -> None:
    """Validate a frozen expected label (risk tier + human approval)."""
    if not isinstance(label, dict) or set(label) != EXPECTED_KEYS:
        raise ContractError("expected label fields do not match the contract")
    if label["risk_tier"] not in RISK_TIERS:
        raise ContractError("expected risk_tier must be FAST | VERIFIED | DEEP-CHANGE")
    if not isinstance(label["human_approval_required"], bool):
        raise ContractError("expected human_approval_required must be a boolean")


def validate_task(task: dict[str, Any]) -> None:
    """Validate a dataset v2 task (triage input + frozen expected label)."""
    if not isinstance(task, dict):
        raise ContractError("task must be an object")
    if set(INPUT_KEYS) - set(task):
        raise ContractError(f"task missing triage input fields: {sorted(set(INPUT_KEYS) - set(task))}")
    if "expected" not in task:
        raise ContractError("task missing expected label")
    validate_triage_task({key: task[key] for key in INPUT_KEYS})
    validate_expected(task["expected"])


def task_input(task: dict[str, Any]) -> dict[str, Any]:
    """The triage-engine input subset of a dataset v2 task."""
    return {key: task[key] for key in INPUT_KEYS}


def _slug_for(route: str, routes: dict[str, Any]) -> Optional[str]:
    entry = routes.get(route) if isinstance(routes, dict) else None
    if not isinstance(entry, dict):
        return None
    slug = entry.get("slug")
    return slug if isinstance(slug, str) and slug else None


def resolve_model_slug(route: str, routes: dict[str, Any]) -> str:
    """Resolve a route to its frozen model slug (raises on unknown route/slug)."""
    slug = _slug_for(route, routes)
    if slug is None:
        raise ContractError(f"route {route!r} does not resolve to a model slug")
    return slug


def escalation_for(risk_tier: str, human_approval_required: bool, route: str) -> str:
    """Derive the escalation from triage + route (precedence: human > premium)."""
    if human_approval_required:
        return "HUMAN_REVIEW_REQUIRED"
    if risk_tier == "DEEP-CHANGE" and route != "premium":
        return "PREMIUM_REQUIRED"
    return "NONE"


def pre_execution(task: dict[str, Any], route: str, routes: dict[str, Any]) -> dict[str, Any]:
    """Run the cheap pre-execution checks and derive the escalation decision."""
    validate_task(task)
    triage_output = triage(task_input(task))
    slug = _slug_for(route, routes)
    route_ok = route in ROUTES and slug is not None

    tier_match = (triage_output["recommended_risk_tier"], triage_output["human_approval_required"]) == (
        task["expected"]["risk_tier"],
        task["expected"]["human_approval_required"],
    )
    acceptance_ok = bool(task["acceptance_criteria_present"])
    human_due = bool(triage_output["human_approval_required"])

    checks = [
        {
            "check_id": "route_resolves",
            "result": "PASS" if route_ok else "FAIL",
            "detail": slug or f"route {route!r} does not resolve to a model slug",
        },
        {
            "check_id": "triage_expected_match",
            "result": "PASS" if tier_match else "FAIL",
            "detail": (
                "triage matches the frozen expected label"
                if tier_match
                else f"triage {triage_output['recommended_risk_tier']}/{triage_output['human_approval_required']} != expected {task['expected']['risk_tier']}/{task['expected']['human_approval_required']}"
            ),
        },
        {
            "check_id": "acceptance_present",
            "result": "PASS" if acceptance_ok else "FAIL",
            "detail": "acceptance criteria present" if acceptance_ok else "acceptance criteria absent",
        },
        {
            "check_id": "human_review_due",
            "result": "FAIL" if human_due else "PASS",
            "detail": (
                "human approval required: " + ", ".join(triage_output["human_approval_reasons"])
                if human_due
                else "no human approval required"
            ),
        },
    ]

    escalation = escalation_for(triage_output["recommended_risk_tier"], triage_output["human_approval_required"], route)

    return {
        "checks": checks,
        "escalation": escalation,
        "proceeded": escalation == "NONE",
        "triage": triage_output,
        "model_slug": slug,
    }


def execution_checks(
    usage: Optional[dict[str, Any]],
    defects: list[str],
    retries: Optional[int],
    model_calls: Optional[int],
    tool_calls: Optional[int],
    cost_usd: Optional[float],
    budget: Optional[float],
    thresholds: dict[str, Any],
) -> list[dict[str, Any]]:
    """Run the execution-stage checks.

    When ``usage`` is None the run did not execute and every execution check is
    ``NOT_APPLICABLE``.
    """
    max_retries = thresholds["max_retries"]
    max_defects = thresholds["max_defects"]
    hard_ratio = thresholds["cost_budget_ratio_hard"]

    if usage is None:
        return [
            {"check_id": check_id, "result": "NOT_APPLICABLE", "detail": "run did not proceed to execution"}
            for check_id in EXECUTION_CHECK_IDS
        ]

    try:
        validate_usage_record(usage)
        usage_valid = True
        usage_detail = "usage record valid"
    except UsageInstrumentationError as exc:
        usage_valid = False
        usage_detail = f"usage record invalid: {exc}"

    consistent = (
        retries == usage.get("retries")
        and model_calls == usage.get("model_calls")
        and tool_calls == usage.get("tool_calls")
    )

    retries_ok = (retries or 0) <= max_retries
    defects_ok = len(defects) <= max_defects
    if cost_usd is None or budget is None:
        cost_result = "NOT_APPLICABLE"
        cost_detail = "cost or budget missing"
    elif cost_usd <= budget * hard_ratio:
        cost_result = "PASS"
        cost_detail = f"cost {cost_usd} within hard limit {budget}"
    else:
        cost_result = "FAIL"
        cost_detail = f"cost {cost_usd} exceeds hard limit {budget}"

    return [
        {
            "check_id": "usage_valid",
            "result": "PASS" if usage_valid else "FAIL",
            "detail": usage_detail,
        },
        {
            "check_id": "usage_consistent",
            "result": "PASS" if consistent else "FAIL",
            "detail": "summary counts match the usage record" if consistent else "summary counts differ from the usage record",
        },
        {
            "check_id": "retries_within_limit",
            "result": "PASS" if retries_ok else "FAIL",
            "detail": f"retries {retries} within limit {max_retries}" if retries_ok else f"retries {retries} exceed limit {max_retries}",
        },
        {
            "check_id": "defects_within_limit",
            "result": "PASS" if defects_ok else "FAIL",
            "detail": f"defects {len(defects)} within limit {max_defects}" if defects_ok else f"defects {len(defects)} exceed limit {max_defects}",
        },
        {
            "check_id": "cost_within_limit",
            "result": cost_result,
            "detail": cost_detail,
        },
    ]


def derive_outcome(pre: dict[str, Any], execution: list[dict[str, Any]]) -> str:
    """Derive the run outcome from the escalation and the check results."""
    escalation = pre["escalation"]
    if escalation == "HUMAN_REVIEW_REQUIRED":
        return "HUMAN_REQUIRED"
    if escalation == "PREMIUM_REQUIRED":
        return "REWORK"

    by_id = {check["check_id"]: check["result"] for check in execution}
    if by_id.get("usage_valid") == "FAIL":
        return "BLOCKED"
    for check_id in ("usage_consistent", "retries_within_limit", "defects_within_limit", "cost_within_limit"):
        if by_id.get(check_id) == "FAIL":
            return "REWORK"
    return "PASS"


def compute_cost(usage: Optional[dict[str, Any]], pricing: dict[str, Any], model_slug: Optional[str]) -> tuple[Optional[float], str]:
    """Return ``(cost_usd, measurement)`` for a run.

    Observed spend stays observed; reconstructed spend stays estimated; missing
    spend (no execution or no data) stays ``None`` / ``unobserved``. A cost of
    zero is never fabricated.
    """
    if usage is None:
        return None, "unobserved"

    observed = usage.get("observed_cost")
    if observed is not None:
        return round(float(observed), 4), "observed"

    rates = (pricing.get("per_mtok", {}) or {}).get(model_slug or "")
    if isinstance(rates, dict) and any(usage.get(field) is not None for field in ("input_tokens", "cached_input_tokens", "output_tokens")):
        input_tokens = usage.get("input_tokens") or 0
        cached_tokens = usage.get("cached_input_tokens") or 0
        output_tokens = usage.get("output_tokens") or 0
        cost = (
            input_tokens / 1_000_000 * float(rates.get("input", 0.0))
            + cached_tokens / 1_000_000 * float(rates.get("cached_input", 0.0))
            + output_tokens / 1_000_000 * float(rates.get("output", 0.0))
        )
        return round(cost, 4), "estimated"

    return None, "unobserved"


def evaluate(
    task: dict[str, Any],
    route: str,
    routes: dict[str, Any],
    thresholds: dict[str, Any],
    pricing: dict[str, Any],
    usage: Optional[dict[str, Any]] = None,
    defects: Optional[list[str]] = None,
    budget: Optional[float] = None,
) -> dict[str, Any]:
    """Run the full EXP-13 check pipeline for one task + route.

    Returns the check/evaluation payload that ``exp13_harness`` wraps into an
    ``EXP13_EXECUTION_RECORD`` (it adds ``run_id`` / ``schema_version`` /
    ``state`` and substitutes an empty USAGE_RECORD when no execution happened).
    """
    validate_task(task)
    defects = list(defects) if defects is not None else []
    if not all(isinstance(item, str) and item for item in defects):
        raise ContractError("defects must be non-empty strings")

    model_slug = resolve_model_slug(route, routes)
    pre = pre_execution(task, route, routes)
    proceeded = pre["proceeded"]

    if proceeded and usage is None:
        raise ContractError("usage record is required when the run proceeds to execution")

    if proceeded:
        validate_usage_record(usage)
        retries = usage["retries"]
        model_calls = usage["model_calls"]
        tool_calls = usage["tool_calls"]
        cost_usd, cost_measurement = compute_cost(usage, pricing, model_slug)
        execution = execution_checks(usage, defects, retries, model_calls, tool_calls, cost_usd, budget, thresholds)
    else:
        retries = None
        model_calls = None
        tool_calls = None
        execution = execution_checks(None, defects, None, None, None, None, budget, thresholds)
        cost_usd, cost_measurement = None, "unobserved"

    outcome = derive_outcome(pre, execution)
    checks = list(pre["checks"]) + execution

    return {
        "task_id": task["task_id"],
        "route": route,
        "model_slug": model_slug,
        "triage": pre["triage"],
        "pre_execution": {
            "checks": pre["checks"],
            "escalation": pre["escalation"],
            "proceeded": proceeded,
        },
        "checks": checks,
        "usage": usage,
        "defects": defects,
        "retries": retries,
        "model_calls": model_calls,
        "tool_calls": tool_calls,
        "escalation": pre["escalation"],
        "outcome": outcome,
        "cost_usd": cost_usd,
        "cost_measurement": cost_measurement,
        "engine_version": ENGINE_VERSION,
    }


def empty_usage(run_id: str) -> dict[str, Any]:
    """The honest empty USAGE_RECORD used when a run escalates before execution."""
    return empty_record(run_id)


__all__ = [
    "ROUTES",
    "ESCALATIONS",
    "OUTCOMES",
    "CHECK_RESULTS",
    "MEASUREMENTS",
    "PRE_EXECUTION_CHECK_IDS",
    "EXECUTION_CHECK_IDS",
    "ALL_CHECK_IDS",
    "ENGINE_VERSION",
    "ContractError",
    "validate_expected",
    "validate_task",
    "task_input",
    "resolve_model_slug",
    "escalation_for",
    "pre_execution",
    "execution_checks",
    "derive_outcome",
    "compute_cost",
    "evaluate",
    "empty_usage",
]
