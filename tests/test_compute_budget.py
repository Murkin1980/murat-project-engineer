from src.mpe_compute_budget import (
    budget_health,
    burn_rate_metrics,
    naive_total_from_burn_rate,
    should_reforecast,
)


def test_budget_health_thresholds():
    assert budget_health(70, 100) == "GREEN"
    assert budget_health(80, 100) == "YELLOW"
    assert budget_health(100, 100) == "ORANGE"
    assert budget_health(111, 100) == "RED"
    assert budget_health(None, 100) == "UNOBSERVED"
    assert budget_health(10, None) == "UNOBSERVED"


def test_burn_rate_metrics_example():
    metrics = burn_rate_metrics(observed_cost=70, planned_budget=100, project_progress_percent=25)
    assert metrics["budget_consumed_percent"] == 70
    assert metrics["cost_per_progress_percent"] == 2.8
    assert metrics["burn_rate_ratio"] == 2.8


def test_burn_rate_does_not_invent_missing_values():
    metrics = burn_rate_metrics(observed_cost=None, planned_budget=100, project_progress_percent=20)
    assert metrics == {
        "budget_consumed_percent": None,
        "cost_per_progress_percent": None,
        "burn_rate_ratio": None,
    }


def test_naive_reforecast_example():
    assert naive_total_from_burn_rate(5.6, 20) == 28
    assert naive_total_from_burn_rate(5.6, 0) is None


def test_reforecast_gate():
    assert should_reforecast(9.9) is False
    assert should_reforecast(10) is True
    assert should_reforecast(20) is True
