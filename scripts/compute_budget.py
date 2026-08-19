"""Deterministic MPE Compute Budget Gate.

Single source of truth for the "AI Compute Budget" contract and its gate logic.
No billing backend, daemon, scheduler, or provider API. Every function here is a
pure, deterministic transform of explicit inputs so historical runs stay
reproducible when vendor prices change.

Design rules
------------
- The top-level metric is *AI Compute Budget*, never an OpenAI-only cost.
- Provider pricing is a dated, overridable snapshot supplied as preflight input,
  not a hidden hard-coded truth.
- ``observed`` / ``estimated`` / ``unobserved`` usage are distinct and never
  conflated: an estimated or unobserved value is never reported as observed.
- The preflight (initial estimate) and the burn-rate reforecast are separate
  blocks. The reforecast is evidence-driven and never folds the initial estimate
  into its projection.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# Contract vocabulary
# --------------------------------------------------------------------------- #

BudgetHealth = str  # GREEN | YELLOW | ORANGE | RED | UNOBSERVED
Measurement = str  # observed | estimated | unobserved
Confidence = str  # low | medium | high
BurnRateStatus = str  # OK | BURN_RATE_ANOMALY | UNOBSERVED

BUDGET_HEALTH_VALUES = ("GREEN", "YELLOW", "ORANGE", "RED", "UNOBSERVED")
MEASUREMENT_VALUES = ("observed", "estimated", "unobserved")
CONFIDENCE_VALUES = ("low", "medium", "high")
BURN_RATE_STATUS_VALUES = ("OK", "BURN_RATE_ANOMALY", "UNOBSERVED")
SCENARIOS = ("economy", "premium")

# Budget health thresholds against the hard limit (fraction).
GREEN_LIMIT = 0.70
YELLOW_LIMIT = 0.90
ORANGE_LIMIT = 1.10

# Burn-rate anomaly: budget consumed at >= this multiple of project progress.
BURN_RATE_ANOMALY_RATIO = 1.5

# Reforecast: minimum progress (percent) before the evidence-based forecast is
# preferred over the preflight point estimate.
REFORECAST_MIN_PROGRESS = 20.0


class ComputeBudgetError(ValueError):
    pass


# --------------------------------------------------------------------------- #
# Provider pricing snapshot (dated, overridable)
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class ProviderPrice:
    slug: str
    input_per_mtok: float
    output_per_mtok: float
    cached_input_per_mtok: float = 0.0


PRICING_SNAPSHOT_DATE = "2026-08-19"

# USD per 1,000,000 tokens. This is an ILLUSTRATIVE snapshot: revalidate and
# override before production use. It exists so preflight is deterministic and so
# an economy routing (DeepSeek / MiniMax / Qwen / Kimi) and a premium benchmark
# (OpenAI / Anthropic) can both be priced without making OpenAI the headline.
PRICING_SNAPSHOT: dict[str, dict[str, ProviderPrice]] = {
    "economy": {
        "opencode-go/deepseek-v4-flash": ProviderPrice("opencode-go/deepseek-v4-flash", 0.14, 0.28, 0.014),
        "opencode-go/kimi-k2.7-code": ProviderPrice("opencode-go/kimi-k2.7-code", 0.60, 2.50, 0.15),
        "qwen-coder-plus": ProviderPrice("qwen-coder-plus", 0.40, 1.60, 0.10),
        "minimax-m2": ProviderPrice("minimax-m2", 0.30, 1.20, 0.08),
    },
    "premium": {
        "gpt-5.6-sol": ProviderPrice("gpt-5.6-sol", 3.00, 12.00, 1.50),
        "claude-sonnet-4-6": ProviderPrice("claude-sonnet-4-6", 3.00, 15.00, 0.30),
    },
}


def scenario_providers(scenario: str) -> list[ProviderPrice]:
    if scenario not in PRICING_SNAPSHOT:
        raise ComputeBudgetError(f"unknown scenario: {scenario}")
    return list(PRICING_SNAPSHOT[scenario].values())


def scenario_stack(scenario: str) -> list[str]:
    """Recommended provider stack (ordered slugs) for a routing scenario."""
    return [p.slug for p in scenario_providers(scenario)]


def blended_price(scenario: str) -> tuple[float, float]:
    """Deterministic blended input/output price (simple mean) for a scenario."""
    providers = scenario_providers(scenario)
    input_price = sum(p.input_per_mtok for p in providers) / len(providers)
    output_price = sum(p.output_per_mtok for p in providers) / len(providers)
    return round(input_price, 6), round(output_price, 6)


def cost_of_tokens(input_tokens: float, output_tokens: float, scenario: str) -> float:
    input_price, output_price = blended_price(scenario)
    cost = (input_tokens / 1_000_000) * input_price + (output_tokens / 1_000_000) * output_price
    return round(cost, 4)


# --------------------------------------------------------------------------- #
# Preflight cost estimate
# --------------------------------------------------------------------------- #

COMPLEXITY_FACTORS = {"low": 1.0, "medium": 1.5, "high": 2.0}


def estimate_preflight(
    scope: str,
    estimated_tasks: int,
    complexity: str,
    expected_context_tokens: int,
    expected_calls: int,
    scenario: str = "economy",
    output_tokens_per_call: Optional[int] = None,
) -> dict[str, Any]:
    """Deterministically build a preflight estimate and a recommended budget.

    The estimator is intentionally simple. It must be deterministic and honest
    about its confidence; it is not expected to predict cost perfectly.
    """
    if complexity not in COMPLEXITY_FACTORS:
        raise ComputeBudgetError(f"unknown complexity: {complexity}")
    if estimated_tasks < 1:
        raise ComputeBudgetError("estimated_tasks must be >= 1")
    if expected_context_tokens < 1 or expected_calls < 1:
        raise ComputeBudgetError("context and call counts must be >= 1")
    if scenario not in PRICING_SNAPSHOT:
        raise ComputeBudgetError(f"unknown scenario: {scenario}")

    factor = COMPLEXITY_FACTORS[complexity]
    per_call_output = output_tokens_per_call if output_tokens_per_call is not None else int(600 * factor)

    input_expected = expected_context_tokens * expected_calls
    output_expected = per_call_output * expected_calls
    spread = 0.35  # deterministic +/- spread around the expected value

    input_min = max(1, int(input_expected * (1 - spread)))
    input_max = int(input_expected * (1 + spread))
    output_min = max(1, int(output_expected * (1 - spread)))
    output_max = int(output_expected * (1 + spread))

    def cost(inp: int, out: int) -> float:
        return cost_of_tokens(inp, out, scenario)

    cost_min = cost(input_min, output_min)
    cost_expected = cost(input_expected, output_expected)
    cost_max = cost(input_max, output_max)

    recommended_budget = round(cost_expected, 2)
    hard_limit = round(max(cost_max * 1.5, recommended_budget * 1.5, 1.0), 2)

    # Confidence falls as inputs become more speculative.
    if output_tokens_per_call is not None and complexity != "high":
        confidence = "high"
    elif complexity == "high":
        confidence = "low"
    else:
        confidence = "medium"

    return {
        "input_tokens_min": input_min,
        "input_tokens_expected": input_expected,
        "input_tokens_max": input_max,
        "output_tokens_min": output_min,
        "output_tokens_expected": output_expected,
        "output_tokens_max": output_max,
        "estimated_cost_min": cost_min,
        "estimated_cost_expected": cost_expected,
        "estimated_cost_max": cost_max,
        "confidence": confidence,
        "recommended_budget": recommended_budget,
        "hard_limit": hard_limit,
        "recommended_stack": scenario_stack(scenario),
        "scope": scope,
        "estimated_tasks": estimated_tasks,
        "complexity": complexity,
        "scenario": scenario,
        "pricing_snapshot_date": PRICING_SNAPSHOT_DATE,
    }


# --------------------------------------------------------------------------- #
# Gate logic
# --------------------------------------------------------------------------- #

def budget_health(projected_total_cost: Optional[float], hard_limit: Optional[float]) -> BudgetHealth:
    """Map projected total vs hard limit to a deterministic budget status."""
    if projected_total_cost is None or hard_limit is None or hard_limit <= 0:
        return "UNOBSERVED"
    if projected_total_cost < 0:
        return "UNOBSERVED"
    ratio = projected_total_cost / hard_limit
    if ratio <= GREEN_LIMIT:
        return "GREEN"
    if ratio <= YELLOW_LIMIT:
        return "YELLOW"
    if ratio <= ORANGE_LIMIT:
        return "ORANGE"
    return "RED"


def burn_rate_metrics(
    observed_cost: Optional[float],
    planned_budget: Optional[float],
    project_progress_percent: Optional[float],
) -> dict[str, Optional[float]]:
    """Compute budget-consumption and progress-efficiency metrics.

    Missing or unusable inputs yield ``None`` instead of invented precision.
    """
    if observed_cost is None or observed_cost < 0:
        return {
            "budget_consumed_percent": None,
            "cost_per_progress_percent": None,
            "burn_rate_ratio": None,
        }

    budget_consumed_percent = None
    if planned_budget is not None and planned_budget > 0:
        budget_consumed_percent = observed_cost / planned_budget * 100.0

    cost_per_progress_percent = None
    burn_rate_ratio = None
    if project_progress_percent is not None and project_progress_percent > 0:
        cost_per_progress_percent = observed_cost / project_progress_percent
        if budget_consumed_percent is not None:
            burn_rate_ratio = budget_consumed_percent / project_progress_percent

    return {
        "budget_consumed_percent": budget_consumed_percent,
        "cost_per_progress_percent": cost_per_progress_percent,
        "burn_rate_ratio": burn_rate_ratio,
    }


def burn_rate_status(
    burn_rate_ratio: Optional[float],
    threshold: float = BURN_RATE_ANOMALY_RATIO,
) -> BurnRateStatus:
    """Raise BURN_RATE_ANOMALY when budget is burning clearly faster than progress."""
    if burn_rate_ratio is None:
        return "UNOBSERVED"
    if burn_rate_ratio >= threshold:
        return "BURN_RATE_ANOMALY"
    return "OK"


# --------------------------------------------------------------------------- #
# Burn-rate reforecast
# --------------------------------------------------------------------------- #

def _adjustment_factor(project_progress_percent: float) -> float:
    """Progress-only correction for early linear extrapolation.

    Linear extrapolation from a small observed prefix tends to under-shoot the
    final total because later tasks carry heavier context and rework. The
    correction decays to 1.0 by ``REFORECAST_MIN_PROGRESS`` percent. It is purely
    a function of progress + observed cost and NEVER uses the preflight prior,
    so the initial estimate and the reforecast stay separate.
    """
    if project_progress_percent >= REFORECAST_MIN_PROGRESS:
        return 1.0
    return 1.0 + (REFORECAST_MIN_PROGRESS - project_progress_percent) / REFORECAST_MIN_PROGRESS * 0.25


def should_reforecast(
    project_progress_percent: Optional[float],
    minimum_progress: float = REFORECAST_MIN_PROGRESS,
) -> bool:
    return project_progress_percent is not None and project_progress_percent >= minimum_progress


def naive_total_from_burn_rate(
    observed_cost: Optional[float], project_progress_percent: Optional[float]
) -> Optional[float]:
    if observed_cost is None or observed_cost < 0:
        return None
    if project_progress_percent is None or project_progress_percent <= 0:
        return None
    return observed_cost * 100.0 / project_progress_percent


def reforecast(
    observed_cost: Optional[float],
    project_progress_percent: Optional[float],
) -> dict[str, Any]:
    """Evidence-based burn-rate reforecast.

    Returns ``observed cost``, ``progress %``, ``cost / 1% progress``, the naive
    projected total, the adjusted projected total, the remaining projected cost
    and a forecast confidence. Does not read the preflight prior.
    """
    if observed_cost is None or observed_cost < 0:
        return _unobserved_forecast()
    if project_progress_percent is None or project_progress_percent <= 0:
        return _unobserved_forecast()

    cost_per_progress_percent = round(observed_cost / project_progress_percent, 6)
    naive_total = round(cost_per_progress_percent * 100.0, 4)
    adjusted_total = round(naive_total * _adjustment_factor(project_progress_percent), 4)
    remaining = round(max(0.0, adjusted_total - observed_cost), 4)

    if project_progress_percent >= REFORECAST_MIN_PROGRESS:
        confidence = "high"
    elif project_progress_percent >= 10.0:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "observed_cost": observed_cost,
        "project_progress_percent": project_progress_percent,
        "cost_per_progress_percent": cost_per_progress_percent,
        "naive_projected_total": naive_total,
        "adjusted_projected_total": adjusted_total,
        "remaining_projected_cost": remaining,
        "confidence": confidence,
        "measurement": "observed",
    }


def _unobserved_forecast() -> dict[str, Any]:
    return {
        "observed_cost": None,
        "project_progress_percent": None,
        "cost_per_progress_percent": None,
        "naive_projected_total": None,
        "adjusted_projected_total": None,
        "remaining_projected_cost": None,
        "confidence": "low",
        "measurement": "unobserved",
    }


# --------------------------------------------------------------------------- #
# Snapshot assembly (canonical contract)
# --------------------------------------------------------------------------- #

def _num(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ComputeBudgetError(f"expected a number, got {value!r}") from exc


def compute_snapshot(
    *,
    compute_budget: dict[str, Any],
    preflight: Optional[dict[str, Any]] = None,
    usage: Optional[dict[str, Any]] = None,
    routing: Optional[dict[str, Any]] = None,
    project_progress_percent: Optional[float] = None,
) -> dict[str, Any]:
    """Derive forecast + efficiency + statuses from the base blocks.

    The caller supplies the observed/estimated base blocks (compute_budget,
    preflight, usage, routing, progress); this function fills the derived
    forecast, efficiency, and status fields deterministically.
    """
    currency = compute_budget.get("currency") or "USD"
    planned_budget = _num(compute_budget.get("planned_budget"))
    hard_limit = _num(compute_budget.get("hard_limit"))

    usage = usage or {}
    measurement = usage.get("measurement", "unobserved")
    if measurement not in MEASUREMENT_VALUES:
        raise ComputeBudgetError(f"invalid measurement: {measurement}")
    observed_cost = _num(usage.get("estimated_cost"))
    input_tokens = usage.get("input_tokens")
    cached_input_tokens = usage.get("cached_input_tokens")
    output_tokens = usage.get("output_tokens")

    # Efficiency ----------------------------------------------------------- #
    metrics = burn_rate_metrics(observed_cost, planned_budget, project_progress_percent)
    budget_consumed_percent = metrics["budget_consumed_percent"]
    cost_per_progress_percent = metrics["cost_per_progress_percent"]
    burn_rate_ratio = metrics["burn_rate_ratio"]

    # Forecast ------------------------------------------------------------- #
    if measurement == "observed" and observed_cost is not None and project_progress_percent:
        ref = reforecast(observed_cost, project_progress_percent)
        estimated_total_expected = round(ref["adjusted_projected_total"], 2)
        estimated_total_min = round(min(ref["naive_projected_total"], ref["adjusted_projected_total"]) * 0.9, 2)
        estimated_total_max = round(max(ref["naive_projected_total"], ref["adjusted_projected_total"]) * 1.1, 2)
        remaining_expected = round(ref["remaining_projected_cost"], 2)
        forecast_confidence = ref["confidence"]
    elif preflight is not None:
        estimated_total_min = preflight.get("estimated_cost_min")
        estimated_total_expected = preflight.get("estimated_cost_expected")
        estimated_total_max = preflight.get("estimated_cost_max")
        remaining_expected = (
            round(estimated_total_expected - observed_cost, 2)
            if estimated_total_expected is not None and observed_cost is not None
            else None
        )
        forecast_confidence = preflight.get("confidence", "low")
    else:
        estimated_total_min = None
        estimated_total_expected = None
        estimated_total_max = None
        remaining_expected = None
        forecast_confidence = "low"

    budget_status = budget_health(estimated_total_expected, hard_limit)
    burn_status = burn_rate_status(burn_rate_ratio)

    routing = routing or {}
    recommended_stack = routing.get("recommended_stack", [])
    actual_provider_mix = routing.get("actual_provider_mix", {})

    snapshot = {
        "compute_budget": {
            "currency": currency,
            "planned_budget": planned_budget,
            "hard_limit": hard_limit,
        },
        "preflight": {
            "input_tokens_min": (preflight or {}).get("input_tokens_min"),
            "input_tokens_expected": (preflight or {}).get("input_tokens_expected"),
            "input_tokens_max": (preflight or {}).get("input_tokens_max"),
            "output_tokens_min": (preflight or {}).get("output_tokens_min"),
            "output_tokens_expected": (preflight or {}).get("output_tokens_expected"),
            "output_tokens_max": (preflight or {}).get("output_tokens_max"),
            "estimated_cost_min": (preflight or {}).get("estimated_cost_min"),
            "estimated_cost_expected": (preflight or {}).get("estimated_cost_expected"),
            "estimated_cost_max": (preflight or {}).get("estimated_cost_max"),
            "confidence": (preflight or {}).get("confidence", "low"),
        },
        "usage": {
            "input_tokens": input_tokens,
            "cached_input_tokens": cached_input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost": observed_cost,
            "measurement": measurement,
        },
        "forecast": {
            "estimated_total_cost_min": estimated_total_min,
            "estimated_total_cost_expected": estimated_total_expected,
            "estimated_total_cost_max": estimated_total_max,
            "remaining_cost_expected": remaining_expected,
            "confidence": forecast_confidence,
        },
        "routing": {
            "recommended_stack": recommended_stack,
            "actual_provider_mix": actual_provider_mix,
        },
        "efficiency": {
            "project_progress_percent": project_progress_percent,
            "budget_consumed_percent": budget_consumed_percent,
            "cost_per_progress_percent": cost_per_progress_percent,
        },
        "status": {
            "budget_status": budget_status,
            "burn_rate_status": burn_status,
            "burn_rate_ratio": burn_rate_ratio,
        },
    }
    return snapshot


def validate_snapshot(snapshot: dict[str, Any]) -> None:
    """Dependency-free validation of the canonical snapshot contract."""
    required_blocks = {"compute_budget", "preflight", "usage", "forecast", "routing", "efficiency"}
    if not isinstance(snapshot, dict) or not required_blocks <= set(snapshot):
        raise ComputeBudgetError(f"snapshot must contain blocks: {sorted(required_blocks)}")

    cb = snapshot["compute_budget"]
    if cb.get("currency") != "USD":
        raise ComputeBudgetError("currency must be USD")
    for key in ("planned_budget", "hard_limit"):
        if key not in cb:
            raise ComputeBudgetError(f"compute_budget missing {key}")
        if cb[key] is not None and (not isinstance(cb[key], (int, float)) or cb[key] < 0):
            raise ComputeBudgetError(f"compute_budget.{key} must be a non-negative number or null")

    measurement = snapshot["usage"].get("measurement")
    if measurement not in MEASUREMENT_VALUES:
        raise ComputeBudgetError(f"usage.measurement must be one of {MEASUREMENT_VALUES}")
    if snapshot["usage"].get("estimated_cost") is not None and measurement == "unobserved":
        raise ComputeBudgetError("usage.estimated_cost must be null when measurement is unobserved")

    confidence = snapshot["forecast"].get("confidence")
    if confidence not in CONFIDENCE_VALUES:
        raise ComputeBudgetError(f"forecast.confidence must be one of {CONFIDENCE_VALUES}")

    actual_provider_mix = snapshot["routing"].get("actual_provider_mix", {})
    for slug, fraction in actual_provider_mix.items():
        if not isinstance(slug, str) or not isinstance(fraction, (int, float)) or not 0 <= fraction <= 1:
            raise ComputeBudgetError(f"invalid provider mix entry: {slug}: {fraction}")


# --------------------------------------------------------------------------- #
# Run Report integration
# --------------------------------------------------------------------------- #

def run_report_budget_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Project the canonical snapshot into the Run Report budget summary block."""
    validate_snapshot(snapshot)
    cb = snapshot["compute_budget"]
    usage = snapshot["usage"]
    forecast = snapshot["forecast"]
    status = snapshot["status"]
    efficiency = snapshot["efficiency"]

    spend = usage["estimated_cost"]
    projected = forecast["estimated_total_cost_expected"]
    remaining = forecast["remaining_cost_expected"]

    return {
        "planned_budget": cb["planned_budget"],
        "hard_limit": cb["hard_limit"],
        "spend": spend,
        "spend_measurement": usage["measurement"],
        "projected_total": projected,
        "projected_remaining": remaining,
        "budget_status": status["budget_status"],
        "burn_rate_status": status["burn_rate_status"],
        "measurement_quality": usage["measurement"],
        "forecast_confidence": forecast["confidence"],
        "provider_model_mix": snapshot["routing"]["actual_provider_mix"],
        "recommended_stack": snapshot["routing"]["recommended_stack"],
        "cost_per_progress_percent": efficiency["cost_per_progress_percent"],
    }


def migrate_approximate_usage_cost(approximate_usage_cost: Any) -> Optional[dict[str, Any]]:
    """Derive a usage block from the legacy ``approximate_usage_cost`` field.

    A numeric legacy value is treated as an *estimated* (never observed) spend.
    ``None`` / empty / non-numeric values yield an ``unobserved`` usage block so
    a report with missing telemetry never fabricates zeros.
    """
    value = approximate_usage_cost
    if isinstance(value, str):
        stripped = value.strip().lstrip("$").replace(",", "")
        try:
            value = float(stripped)
        except ValueError:
            value = None
    if value is None or value == "":
        return {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": None, "measurement": "unobserved"}
    try:
        cost = float(value)
    except (TypeError, ValueError):
        return {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": None, "measurement": "unobserved"}
    if cost < 0:
        return {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": None, "measurement": "unobserved"}
    return {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": round(cost, 4), "measurement": "estimated"}


# --------------------------------------------------------------------------- #
# Dashboard rendering
# --------------------------------------------------------------------------- #

def dashboard_budget_block(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Render the canonical snapshot into dashboard card values.

    When usage is not observed this returns an explicit ``UNOBSERVED`` marker
    rather than fake zeros.
    """
    validate_snapshot(snapshot)
    cb = snapshot["compute_budget"]
    usage = snapshot["usage"]
    forecast = snapshot["forecast"]
    status = snapshot["status"]
    efficiency = snapshot["efficiency"]

    progress = efficiency["project_progress_percent"]
    spent = usage["estimated_cost"]
    planned = cb["planned_budget"]
    projected_min = forecast["estimated_total_cost_min"]
    projected_max = forecast["estimated_total_cost_max"]
    remaining_min = None
    remaining_max = None
    if projected_min is not None and spent is not None:
        remaining_min = max(0.0, round(projected_min - spent, 2))
    if projected_max is not None and spent is not None:
        remaining_max = max(0.0, round(projected_max - spent, 2))

    budget_percent = efficiency["budget_consumed_percent"]
    if budget_percent is not None:
        budget_percent = round(budget_percent, 1)

    unobserved = usage["measurement"] == "unobserved"

    return {
        "project_progress_percent": progress,
        "budget_consumed_percent": budget_percent,
        "spent": spent,
        "planned_budget": planned,
        "projected_total_min": projected_min,
        "projected_total_max": projected_max,
        "remaining_min": remaining_min,
        "remaining_max": remaining_max,
        "cost_per_progress_percent": efficiency["cost_per_progress_percent"],
        "forecast_confidence": forecast["confidence"],
        "budget_status": status["budget_status"],
        "burn_rate_status": status["burn_rate_status"],
        "unobserved": unobserved,
    }


def render_dashboard_budget(snapshot: dict[str, Any]) -> str:
    """Human-readable dashboard budget block (text form used by the UI/tests)."""
    block = dashboard_budget_block(snapshot)
    if block["unobserved"]:
        return (
            "AI BUDGET\n░░░░░░░░░░ UNOBSERVED\n\n"
            "Spent: —\nProjected total: —\nRemaining: —\n"
            "Efficiency: —\nForecast: UNOBSERVED\nStatus: UNOBSERVED"
        )

    progress = block["project_progress_percent"] or 0.0
    budget = block["budget_consumed_percent"]
    budget_label = f"{budget:g}%" if budget is not None else "UNOBSERVED"

    def money(value: Optional[float]) -> str:
        return f"${value:,.2f}" if value is not None else "—"

    projected = "—"
    if block["projected_total_min"] is not None and block["projected_total_max"] is not None:
        projected = f"${block['projected_total_min']:,.0f}–{block['projected_total_max']:,.0f}"
    remaining = "—"
    if block["remaining_min"] is not None and block["remaining_max"] is not None:
        remaining = f"${block['remaining_min']:,.0f}–{block['remaining_max']:,.0f}"
    efficiency = "—"
    if block["cost_per_progress_percent"] is not None:
        efficiency = f"${block['cost_per_progress_percent']:,.2f} / 1% progress"

    return (
        f"PROJECT PROGRESS\n{_bar(progress)} {progress:g}%\n\n"
        f"AI BUDGET\n{_bar(budget) if budget is not None else _bar(0)} {budget_label}\n\n"
        f"Spent: {money(block['spent'])} / {money(block['planned_budget'])}\n"
        f"Projected total: {projected}\n"
        f"Remaining: {remaining}\n"
        f"Efficiency: {efficiency}\n"
        f"Forecast: {block['forecast_confidence'].upper()}\n"
        f"Status: {block['budget_status']}"
    )


def _bar(percent: float, width: int = 10) -> str:
    percent = max(0.0, min(100.0, float(percent)))
    filled = int(round(percent / 100.0 * width))
    return "█" * filled + "░" * (width - filled)


if __name__ == "__main__":
    import json

    preflight = estimate_preflight(
        scope="Add Compute Budget Gate MVP to murat-project-engineer",
        estimated_tasks=12,
        complexity="medium",
        expected_context_tokens=30_000,
        expected_calls=40,
        scenario="economy",
    )
    snapshot = compute_snapshot(
        compute_budget={"currency": "USD", "planned_budget": preflight["recommended_budget"], "hard_limit": preflight["hard_limit"]},
        preflight=preflight,
        usage={"input_tokens": 1_200_000, "cached_input_tokens": 360_000, "output_tokens": 24_000, "estimated_cost": preflight["estimated_cost_expected"], "measurement": "estimated"},
        routing={"recommended_stack": preflight["recommended_stack"], "actual_provider_mix": {preflight["recommended_stack"][0]: 1.0}},
        project_progress_percent=0.0,
    )
    print(json.dumps(snapshot, indent=2))
