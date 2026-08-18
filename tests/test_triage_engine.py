import json
import unittest
from pathlib import Path

from scripts.triage_engine import ContractError, backtest, triage


ROOT = Path(__file__).resolve().parents[1]


class TriageEngineTests(unittest.TestCase):
    def test_fast_low_risk_task(self):
        result = triage({
            "task_id": "t", "summary": "docs", "affected_repositories": ["repo"],
            "acceptance_criteria_present": True, "rollback_known": True,
            "ratings": {"complexity": 1, "risk": 1, "architectural_impact": 0, "data_sensitivity": 0, "unknowns": 0},
            "signals": []
        })
        self.assertEqual("FAST", result["recommended_risk_tier"])
        self.assertEqual(100, result["execution_confidence"])
        self.assertFalse(result["human_approval_required"])

    def test_deep_change_never_silently_downgrades(self):
        result = triage({
            "task_id": "t", "summary": "router", "affected_repositories": ["repo"],
            "acceptance_criteria_present": True, "rollback_known": True,
            "ratings": {"complexity": 1, "risk": 1, "architectural_impact": 0, "data_sensitivity": 0, "unknowns": 0},
            "signals": ["router_authority_change"]
        })
        self.assertEqual("DEEP-CHANGE", result["recommended_risk_tier"])
        self.assertTrue(result["human_approval_required"])

    def test_maximum_architectural_impact_requires_approval_without_signal(self):
        result = triage({
            "task_id": "t", "summary": "core architecture", "affected_repositories": ["repo"],
            "acceptance_criteria_present": True, "rollback_known": True,
            "ratings": {"complexity": 1, "risk": 1, "architectural_impact": 4, "data_sensitivity": 0, "unknowns": 0},
            "signals": []
        })
        self.assertEqual("DEEP-CHANGE", result["recommended_risk_tier"])
        self.assertTrue(result["human_approval_required"])

    def test_high_data_sensitivity_requires_approval(self):
        result = triage({
            "task_id": "t", "summary": "sensitive data", "affected_repositories": ["repo"],
            "acceptance_criteria_present": True, "rollback_known": True,
            "ratings": {"complexity": 1, "risk": 1, "architectural_impact": 0, "data_sensitivity": 4, "unknowns": 0},
            "signals": []
        })
        self.assertTrue(result["human_approval_required"])

    def test_invalid_rating_rejected(self):
        with self.assertRaises(ContractError):
            triage({
                "task_id": "t", "summary": "invalid", "affected_repositories": ["repo"],
                "acceptance_criteria_present": True, "rollback_known": True,
                "ratings": {"complexity": 5, "risk": 1, "architectural_impact": 0, "data_sensitivity": 0, "unknowns": 0},
                "signals": []
            })

    def test_backtest_has_no_deep_change_false_negatives(self):
        dataset = json.loads((ROOT / "datasets" / "exp-12-backtest.json").read_text(encoding="utf-8"))
        result = backtest(dataset)
        self.assertGreaterEqual(result["case_count"], 20)
        self.assertEqual(0, result["deep_change_false_negatives"])
        self.assertGreaterEqual(result["exact_match_rate"], 0.8)


if __name__ == "__main__":
    unittest.main()
