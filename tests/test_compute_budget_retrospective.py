import json
import unittest
from pathlib import Path

from scripts import compute_budget_retrospective as cr

ROOT = Path(__file__).resolve().parents[1]


class RetrospectiveValidationTests(unittest.TestCase):
    def test_dataset_has_five_runs_all_unobserved(self):
        dataset = json.loads((ROOT / "experiments" / "compute-budget" / "validation_runs.json").read_text(encoding="utf-8"))
        self.assertEqual(5, len(dataset["runs"]))
        self.assertEqual({"UNOBSERVED"}, {run["measurement"] for run in dataset["runs"]})
        # Each run uses null for absent actual usage instead of fabricated zeros.
        for run in dataset["runs"]:
            for key in ("input_tokens", "output_tokens", "cost_usd", "model_calls"):
                self.assertIsNone(run["actual"][key])

    def test_dataset_covers_required_type_spread(self):
        dataset = json.loads((ROOT / "experiments" / "compute-budget" / "validation_runs.json").read_text(encoding="utf-8"))
        types = {run["task_type"] for run in dataset["runs"]}
        self.assertIn("research", types)
        self.assertIn("browser_research", types)
        self.assertIn("architecture", types)
        self.assertIn("implementation", types)
        self.assertIn("evaluation", types)

    def test_retrospective_concludes_insufficient_telemetry(self):
        result = cr.validate()
        self.assertEqual(5, result["run_count"])
        self.assertEqual(0, result["observed_count"])
        self.assertEqual(0, result["estimated_count"])
        self.assertEqual(5, result["unobserved_count"])
        self.assertEqual("INSUFFICIENT_HISTORICAL_TELEMETRY", result["conclusion"])
        self.assertIsNone(result["observed_metrics"])

    def test_retrospective_is_deterministic(self):
        self.assertEqual(cr.validate(), cr.validate())

    def test_preflight_uses_only_blind_inputs(self):
        dataset = json.loads((ROOT / "experiments" / "compute-budget" / "validation_runs.json").read_text(encoding="utf-8"))
        run = dataset["runs"][0]
        row = cr.retrospective_preflight(run)
        est = row["estimated"]
        # Ordered ranges from the estimator.
        self.assertTrue(est["input_tokens_min"] <= est["input_tokens_expected"] <= est["input_tokens_max"])
        self.assertTrue(est["cost_min"] <= est["cost_expected"] <= est["cost_max"])
        # No actual cost leaked into the preflight: the row only carries the
        # blind inputs, never the run's actual (which is null anyway).
        self.assertNotIn("actual", row)

    def test_never_promotes_unobserved_to_observed(self):
        for run in json.loads((ROOT / "experiments" / "compute-budget" / "validation_runs.json").read_text(encoding="utf-8"))["runs"]:
            self.assertEqual("UNOBSERVED", run["measurement"])

    def test_compare_actual_returns_not_evaluable_for_null_cost(self):
        preflight = {"estimated": {"cost_min": 1.0, "cost_expected": 2.0, "cost_max": 3.0}}
        comparison = cr.compare_actual(preflight, {"cost_usd": None})
        self.assertFalse(comparison["evaluable"])
        self.assertIsNone(comparison["range_hit"])

    def test_compare_actual_computes_metrics_when_cost_present(self):
        preflight = {"estimated": {"cost_min": 1.0, "cost_expected": 2.0, "cost_max": 3.0}}
        comparison = cr.compare_actual(preflight, {"cost_usd": 2.0})
        self.assertTrue(comparison["evaluable"])
        self.assertTrue(comparison["range_hit"])
        self.assertEqual(0.0, comparison["expected_error_percent"])


if __name__ == "__main__":
    unittest.main()
