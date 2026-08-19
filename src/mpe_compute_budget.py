"""Deterministic helpers for the MPE Compute Budget Gate.

This module deliberately does not know provider pricing. Pricing snapshots belong to
preflight inputs so historical runs remain reproducible when vendor prices change.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

BudgetHealth = Literal["GREEN", "YELLOW", "ORANGE", "RED", "UNOBSERVED"]
Measurement = Literal["observed", "estimated", "unobserved"]


@dataclass(frozen=True)
class BudgetForecast:
    hard_limit: Optional[float]
    projected_total_cost: Optional[float]
    observed_cost: Optional[float]
    project_progress_percent: Optional[float]
    measurement: Measurement = "unobserved"


def budget_health(projected_total_cost: Optional[float], hard_limit: Optional[float]) -> BudgetHealth:
    """Return the MPE budget-health state from projected total / hard limit."""
    if projected_total_cost is None or hard_limit is None or hard_limit <= 0:
        return "UNOBSERVED"
    ratio = projected_total_cost / hard_limit
    if ratio <= 0.70:
        return "GREEN"
    if ratio <= 0.90:
        return "YELLOW"
    if ratio <= 1.10:
        return "ORANGE"
    return "RED"


def burn_rate_metrics(
    observed_cost: Optional[float],
    planned_budget: Optional[float],
    project_progress_percent: Optional[float],
) -> dict[str, Optional[float]]:
    """Compute budget-consumption and progress-efficiency metrics.

    Missing or unusable inputs produce None instead of invented precision.
    """
    if observed_cost is None or observed_cost < 0:
        return {
            "budget_consumed_percent": None,
            "cost_per_progress_percent": None,
            "burn_rate_ratio": None,
        }

    budget_consumed = None
    if planned_budget is not None and planned_budget > 0:
        budget_consumed = observed_cost / planned_budget * 100.0

    cost_per_progress = None
    burn_rate_ratio = None
    if project_progress_percent is not None and project_progress_percent > 0:
        cost_per_progress = observed_cost / project_progress_percent
        if budget_consumed is not None:
            burn_rate_ratio = budget_consumed / project_progress_percent

    return {
        "budget_consumed_percent": budget_consumed,
        "cost_per_progress_percent": cost_per_progress,
        "burn_rate_ratio": burn_rate_ratio,
    }


def naive_total_from_burn_rate(
    observed_cost: Optional[float], project_progress_percent: Optional[float]
) -> Optional[float]:
    """Project total cost linearly from observed spend and progress.

    This is a fallback signal only. MPE should prefer calibrated forecasts when
    comparable-run evidence is available.
    """
    if observed_cost is None or observed_cost < 0:
        return None
    if project_progress_percent is None or project_progress_percent <= 0:
        return None
    return observed_cost * 100.0 / project_progress_percent


def should_reforecast(project_progress_percent: Optional[float], minimum_progress: float = 10.0) -> bool:
    """Return whether enough progress exists to consider a burn-rate reforecast."""
    return project_progress_percent is not None and project_progress_percent >= minimum_progress
