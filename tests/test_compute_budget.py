import json
import unittest
from pathlib import Path

from scripts import compute_budget as CB

ROOT = Path(__file__).resolve().parents[1]


def _snapshot(**changes):
    base = {
        "compute_budget": {"currency": "USD", "planned_budget": 80.0, "hard_limit": 100.0},
        "preflight": {
            "input_tokens_min": 780000, "input_tokens_expected": 1200000, "input_tokens_max": 1620000,
            "output_tokens_min": 15600, "output_tokens_expected": 24000, "output_tokens_max": 32400,
            "estimated_cost_min": 0.13, "estimated_cost_expected": 0.2, "estimated_cost_max": 0.27,
            "confidence": "medium",
        },
        "usage": {"input_tokens": 1200000, "cached_input_tokens": 360000, "output_tokens": 24000, "estimated_cost": 38.0, "measurement": "observed"},
        "routing": {"recommended_stack": ["opencode-go/deepseek-v4-flash"], "actual_provider_mix": {"opencode-go/deepseek-v4-flash": 1.0}},
        "project_progress_percent": 62.0,
    }
    base.update(changes)
    return CB.compute_snapshot(**base)


class BudgetHealthTests(unittest.TestCase):
    def test_green_boundary(self):
        self.assertEqual("GREEN", CB.budget_health(70, 100))
        self.assertEqual("GREEN", CB.budget_health(1, 100))

    def test_yellow_boundary(self):
        self.assertEqual("YELLOW", CB.budget_health(70.01, 100))
        self.assertEqual("YELLOW", CB.budget_health(90, 100))

    def test_orange_boundary(self):
        self.assertEqual("ORANGE", CB.budget_health(90.01, 100))
        self.assertEqual("ORANGE", CB.budget_health(110, 100))

    def test_red_boundary(self):
        self.assertEqual("RED", CB.budget_health(110.01, 100))
        self.assertEqual("RED", CB.budget_health(500, 100))

    def test_hard_limit_zero(self):
        self.assertEqual("UNOBSERVED", CB.budget_health(50, 0))

    def test_hard_limit_missing(self):
        self.assertEqual("UNOBSERVED", CB.budget_health(50, None))
        self.assertEqual("UNOBSERVED", CB.budget_health(None, 100))


class BurnRateTests(unittest.TestCase):
    def test_metrics(self):
        metrics = CB.burn_rate_metrics(38.0, 80.0, 62.0)
        self.assertEqual(47.5, metrics["budget_consumed_percent"])
        self.assertAlmostEqual(0.6129, metrics["cost_per_progress_percent"], places=3)
        self.assertAlmostEqual(47.5 / 62.0, metrics["burn_rate_ratio"], places=3)

    def test_progress_zero(self):
        metrics = CB.burn_rate_metrics(38.0, 80.0, 0)
        self.assertEqual(47.5, metrics["budget_consumed_percent"])
        self.assertIsNone(metrics["cost_per_progress_percent"])
        self.assertIsNone(metrics["burn_rate_ratio"])

    def test_missing_cost(self):
        metrics = CB.burn_rate_metrics(None, 80.0, 62.0)
        self.assertIsNone(metrics["budget_consumed_percent"])
        self.assertIsNone(metrics["cost_per_progress_percent"])
        self.assertIsNone(metrics["burn_rate_ratio"])

    def test_burn_rate_anomaly(self):
        self.assertEqual("BURN_RATE_ANOMALY", CB.burn_rate_status(2.8))
        self.assertEqual("BURN_RATE_ANOMALY", CB.burn_rate_status(1.5))
        self.assertEqual("OK", CB.burn_rate_status(1.0))
        self.assertEqual("OK", CB.burn_rate_status(0.766))
        self.assertEqual("UNOBSERVED", CB.burn_rate_status(None))

    def test_burn_rate_anomaly_raised_on_divergence(self):
        snapshot = _snapshot(
            usage={"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": 70.0, "measurement": "observed"},
            project_progress_percent=25.0,
        )
        self.assertEqual("BURN_RATE_ANOMALY", snapshot["status"]["burn_rate_status"])


class MeasurementTests(unittest.TestCase):
    def test_observed_usage_flows_to_forecast(self):
        snapshot = _snapshot()
        self.assertEqual("observed", snapshot["usage"]["measurement"])
        self.assertIsNotNone(snapshot["forecast"]["estimated_total_cost_expected"])

    def test_estimated_usage_uses_preflight_forecast(self):
        snapshot = _snapshot(
            usage={"input_tokens": 1200000, "cached_input_tokens": 360000, "output_tokens": 24000, "estimated_cost": 0.2, "measurement": "estimated"},
            project_progress_percent=0.0,
        )
        self.assertEqual("estimated", snapshot["usage"]["measurement"])
        self.assertEqual(0.2, snapshot["forecast"]["estimated_total_cost_expected"])

    def test_unobserved_usage_never_fabricates_zeros(self):
        snapshot = _snapshot(
            preflight=None,
            usage={"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": None, "measurement": "unobserved"},
            project_progress_percent=None,
        )
        self.assertEqual("unobserved", snapshot["usage"]["measurement"])
        self.assertEqual("UNOBSERVED", snapshot["status"]["budget_status"])
        self.assertIsNone(snapshot["efficiency"]["budget_consumed_percent"])
        self.assertIsNone(snapshot["forecast"]["estimated_total_cost_expected"])

    def test_preflight_without_usage_still_yields_estimate(self):
        # A preflight estimate is legitimate data: budget status is computed from
        # the projected total vs hard limit, not reported as UNOBSERVED.
        snapshot = _snapshot(
            usage={"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": None, "measurement": "unobserved"},
            project_progress_percent=0.0,
        )
        self.assertIsNotNone(snapshot["forecast"]["estimated_total_cost_expected"])
        self.assertIn(snapshot["status"]["budget_status"], ("GREEN", "YELLOW", "ORANGE", "RED"))

    def test_unobserved_usage_rejects_non_null_cost(self):
        with self.assertRaises(CB.ComputeBudgetError):
            CB.validate_snapshot(_snapshot(
                usage={"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": 12.0, "measurement": "unobserved"},
            ))


class ReforecastTests(unittest.TestCase):
    def test_reforecast_values(self):
        ref = CB.reforecast(5.6, 20.0)
        self.assertEqual(28.0, ref["naive_projected_total"])
        self.assertEqual(28.0, ref["adjusted_projected_total"])
        self.assertEqual(22.4, ref["remaining_projected_cost"])
        self.assertEqual("high", ref["confidence"])

    def test_reforecast_early_progress_adjusts(self):
        ref = CB.reforecast(5.6, 10.0)
        self.assertEqual(56.0, ref["naive_projected_total"])
        self.assertGreater(ref["adjusted_projected_total"], ref["naive_projected_total"])
        self.assertEqual("medium", ref["confidence"])

    def test_reforecast_requires_progress(self):
        self.assertEqual("unobserved", CB.reforecast(5.6, 0)["measurement"])
        self.assertEqual("unobserved", CB.reforecast(None, 20)["measurement"])

    def test_should_reforecast(self):
        self.assertFalse(CB.should_reforecast(19.9))
        self.assertTrue(CB.should_reforecast(20.0))

    def test_reforecast_does_not_mix_preflight(self):
        # The reforecast signature never receives the preflight prior.
        ref = CB.reforecast(38.0, 62.0)
        self.assertNotIn("preflight", ref)
        self.assertNotIn("estimated_cost_expected", ref)


class ProviderScenarioTests(unittest.TestCase):
    def test_two_scenarios_exist(self):
        self.assertEqual(set(CB.SCENARIOS), set(CB.PRICING_SNAPSHOT))
        self.assertTrue(CB.scenario_stack("economy"))
        self.assertTrue(CB.scenario_stack("premium"))

    def test_economy_cheaper_than_premium(self):
        econ = CB.blended_price("economy")
        prem = CB.blended_price("premium")
        self.assertLess(econ[0], prem[0])
        self.assertLess(econ[1], prem[1])

    def test_premium_benchmark_is_not_headline(self):
        # The headline metric is AI Compute Budget (USD), independent of any vendor.
        preflight = CB.estimate_preflight("t", 5, "medium", 10000, 10, scenario="premium")
        self.assertIn("estimated_cost_expected", preflight)
        self.assertNotIn("openai", str(preflight).lower())

    def test_unknown_scenario_rejected(self):
        with self.assertRaises(CB.ComputeBudgetError):
            CB.estimate_preflight("t", 5, "medium", 10000, 10, scenario="nope")

    def test_provider_mix_validation(self):
        snapshot = _snapshot()
        CB.validate_snapshot(snapshot)
        bad = _snapshot()
        bad["routing"]["actual_provider_mix"] = {"slug": 2.0}
        with self.assertRaises(CB.ComputeBudgetError):
            CB.validate_snapshot(bad)


class PreflightTests(unittest.TestCase):
    def test_preflight_deterministic(self):
        args = dict(scope="s", estimated_tasks=5, complexity="medium", expected_context_tokens=10000, expected_calls=10, scenario="economy")
        self.assertEqual(CB.estimate_preflight(**args), CB.estimate_preflight(**args))

    def test_preflight_ranges_ordered(self):
        pf = CB.estimate_preflight("s", 5, "medium", 10000, 10)
        self.assertTrue(pf["input_tokens_min"] <= pf["input_tokens_expected"] <= pf["input_tokens_max"])
        self.assertTrue(pf["output_tokens_min"] <= pf["output_tokens_expected"] <= pf["output_tokens_max"])
        self.assertTrue(pf["estimated_cost_min"] <= pf["estimated_cost_expected"] <= pf["estimated_cost_max"])
        self.assertLessEqual(pf["recommended_budget"], pf["hard_limit"])


class SchemaValidationTests(unittest.TestCase):
    def test_example_validates_against_schema_blocks(self):
        example = json.loads((ROOT / "contracts" / "COMPUTE_BUDGET.example.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "contracts" / "COMPUTE_BUDGET.schema.json").read_text(encoding="utf-8"))
        self.assertTrue(set(schema["required"]) <= set(example))
        for block in ("compute_budget", "preflight", "usage", "forecast", "routing", "efficiency", "status"):
            self.assertIn(block, schema["properties"])

    def test_engine_snapshot_validates(self):
        snapshot = _snapshot()
        snapshot["schema_version"] = "1.0"
        snapshot["run_id"] = "RUN-X"
        snapshot["project"] = "p"
        CB.validate_snapshot(snapshot)  # does not raise


class BackwardCompatibilityTests(unittest.TestCase):
    def test_run_report_schema_keeps_approximate_usage_cost(self):
        schema = json.loads((ROOT / "contracts" / "RUN_REPORT.schema.json").read_text(encoding="utf-8"))
        self.assertIn("approximate_usage_cost", schema["properties"])
        self.assertIn("compute_budget", schema["properties"])

    def test_migrate_numeric_cost_is_estimated(self):
        usage = CB.migrate_approximate_usage_cost(12.5)
        self.assertEqual("estimated", usage["measurement"])
        self.assertEqual(12.5, usage["estimated_cost"])

    def test_migrate_string_cost(self):
        usage = CB.migrate_approximate_usage_cost("$12.50")
        self.assertEqual(12.5, usage["estimated_cost"])
        self.assertEqual("estimated", usage["measurement"])

    def test_migrate_null_cost_is_unobserved(self):
        usage = CB.migrate_approximate_usage_cost(None)
        self.assertEqual("unobserved", usage["measurement"])
        self.assertIsNone(usage["estimated_cost"])

    def test_migrate_garbage_cost_is_unobserved(self):
        for value in ("not-a-number", -3):
            usage = CB.migrate_approximate_usage_cost(value)
            self.assertEqual("unobserved", usage["measurement"], value)

    def test_migration_never_reports_observed(self):
        self.assertNotEqual("observed", CB.migrate_approximate_usage_cost(12.5)["measurement"])


class DashboardRenderingTests(unittest.TestCase):
    def test_dashboard_block_with_data(self):
        block = CB.dashboard_budget_block(_snapshot())
        self.assertEqual(62.0, block["project_progress_percent"])
        self.assertEqual(47.5, block["budget_consumed_percent"])
        self.assertEqual("GREEN", block["budget_status"])

    def test_dashboard_missing_budget_data_is_unobserved(self):
        snapshot = _snapshot(
            usage={"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": None, "measurement": "unobserved"},
            project_progress_percent=None,
        )
        block = CB.dashboard_budget_block(snapshot)
        self.assertTrue(block["unobserved"])
        self.assertIsNone(block["budget_consumed_percent"])

    def test_dashboard_text_missing_budget_has_no_fake_zeros(self):
        snapshot = _snapshot(
            usage={"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "estimated_cost": None, "measurement": "unobserved"},
            project_progress_percent=None,
        )
        text = CB.render_dashboard_budget(snapshot)
        self.assertIn("UNOBSERVED", text)
        self.assertNotIn("$0", text)

    def test_dashboard_text_with_data(self):
        text = CB.render_dashboard_budget(_snapshot())
        self.assertIn("PROJECT PROGRESS", text)
        self.assertIn("AI BUDGET", text)
        self.assertIn("Status: GREEN", text)


class HistoricalValidationTests(unittest.TestCase):
    def test_historical_runs_reported_as_unobserved(self):
        from scripts import compute_budget_validation as cval

        result = cval.validate_historical()
        self.assertGreaterEqual(result["historical_run_count"], 5)
        self.assertEqual(result["observed_count"], 0)
        self.assertEqual(result["unobserved_count"], result["historical_run_count"])
        self.assertIsNone(result["min_max_accuracy_rate"])
        for entry in result["results"]:
            self.assertEqual("unobserved", entry["measurement"])
            self.assertEqual("UNOBSERVED", entry["budget_status"])


class RunReportSummaryTests(unittest.TestCase):
    def test_summary_fields(self):
        summary = CB.run_report_budget_summary(_snapshot())
        self.assertEqual(80.0, summary["planned_budget"])
        self.assertEqual(100.0, summary["hard_limit"])
        self.assertEqual(38.0, summary["spend"])
        self.assertEqual("GREEN", summary["budget_status"])
        self.assertEqual("observed", summary["measurement_quality"])


if __name__ == "__main__":
    unittest.main()
