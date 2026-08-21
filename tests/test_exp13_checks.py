import json
import unittest
from pathlib import Path

from scripts import exp13_checks as ec
from scripts import usage_instrumentation as ui
from scripts.triage_engine import ContractError

ROOT = Path(__file__).resolve().parents[1]

DATASET = json.loads((ROOT / "experiments" / "exp-13" / "tasks_v2.json").read_text(encoding="utf-8"))
ROUTES = json.loads((ROOT / "experiments" / "exp-13" / "routes.json").read_text(encoding="utf-8"))["routes"]
THRESHOLDS = json.loads((ROOT / "experiments" / "exp-13" / "thresholds.json").read_text(encoding="utf-8"))
PRICING = json.loads((ROOT / "experiments" / "exp-13" / "pricing_snapshot.json").read_text(encoding="utf-8"))


def task(task_id):
    return next(t for t in DATASET["tasks"] if t["task_id"] == task_id)


def make_usage(run_id, retries=0, model_calls=1, tool_calls=0, cost=0.0004, input_tokens=1000, output_tokens=200):
    recorder = ui.UsageRecorder(run_id=run_id).start(
        provider="OpenCode Zen", model="opencode-go/deepseek-v4-flash", timestamp="2026-08-21T09:00:00Z"
    )
    for _ in range(model_calls):
        recorder.record_model_call(input_tokens, output_tokens, cost=cost if model_calls else None)
    for _ in range(tool_calls):
        recorder.record_tool_call()
    for _ in range(retries):
        recorder.record_retry()
    return recorder.to_record("router_billing", end_time="2026-08-21T09:10:00Z")


class EscalationRuleTests(unittest.TestCase):
    def test_human_approval_wins_precedence(self):
        self.assertEqual("HUMAN_REVIEW_REQUIRED", ec.escalation_for("DEEP-CHANGE", True, "A"))

    def test_premium_required_for_deep_change_non_premium(self):
        self.assertEqual("PREMIUM_REQUIRED", ec.escalation_for("DEEP-CHANGE", False, "A"))

    def test_premium_route_is_none_for_deep_change(self):
        self.assertEqual("NONE", ec.escalation_for("DEEP-CHANGE", False, "premium"))

    def test_no_escalation_for_verified(self):
        self.assertEqual("NONE", ec.escalation_for("VERIFIED", False, "A"))


class TaskValidationTests(unittest.TestCase):
    def test_valid_task_accepted(self):
        ec.validate_task(task("T-001"))  # does not raise

    def test_task_rejects_missing_triage_field(self):
        value = dict(task("T-001"))
        del value["signals"]
        with self.assertRaises(ContractError):
            ec.validate_task(value)

    def test_task_rejects_bad_expected_tier(self):
        value = dict(task("T-001"))
        value["expected"] = {"risk_tier": "BOGUS", "human_approval_required": False}
        with self.assertRaises(ContractError):
            ec.validate_task(value)

    def test_task_rejects_non_bool_approval(self):
        value = dict(task("T-001"))
        value["expected"] = {"risk_tier": "FAST", "human_approval_required": "yes"}
        with self.assertRaises(ContractError):
            ec.validate_task(value)

    def test_task_rejects_out_of_range_rating(self):
        value = json.loads(json.dumps(task("T-001")))
        value["ratings"]["complexity"] = 5
        with self.assertRaises(ContractError):
            ec.validate_task(value)


class ResolveSlugTests(unittest.TestCase):
    def test_resolve_slug_for_each_route(self):
        self.assertEqual("opencode-go/deepseek-v4-flash", ec.resolve_model_slug("A", ROUTES))
        self.assertEqual("opencode-go/kimi-k2.7-code", ec.resolve_model_slug("B", ROUTES))
        self.assertEqual("gpt-5.6-sol", ec.resolve_model_slug("premium", ROUTES))

    def test_resolve_slug_rejects_unknown_route(self):
        with self.assertRaises(ContractError):
            ec.resolve_model_slug("C", ROUTES)

    def test_resolve_slug_rejects_missing_slug(self):
        with self.assertRaises(ContractError):
            ec.resolve_model_slug("A", {"A": {"profile": "cheap-research"}})


class PreExecutionTests(unittest.TestCase):
    def test_fast_task_route_a_proceeds(self):
        pre = ec.pre_execution(task("T-001"), "A", ROUTES)
        self.assertEqual("NONE", pre["escalation"])
        self.assertTrue(pre["proceeded"])
        self.assertTrue(all(check["result"] == "PASS" for check in pre["checks"]))

    def test_production_change_escalates_human(self):
        pre = ec.pre_execution(task("T-008"), "B", ROUTES)
        self.assertEqual("HUMAN_REVIEW_REQUIRED", pre["escalation"])
        self.assertFalse(pre["proceeded"])

    def test_deep_change_escalates_human_not_premium(self):
        pre = ec.pre_execution(task("T-009"), "A", ROUTES)
        self.assertEqual("HUMAN_REVIEW_REQUIRED", pre["escalation"])

    def test_route_resolves_fails_when_slug_missing(self):
        pre = ec.pre_execution(task("T-001"), "A", {"A": {"profile": "cheap-research"}})
        self.assertEqual("FAIL", pre["checks"][0]["result"])

    def test_triage_mismatch_fails(self):
        value = json.loads(json.dumps(task("T-001")))
        value["expected"] = {"risk_tier": "VERIFIED", "human_approval_required": False}
        pre = ec.pre_execution(value, "A", ROUTES)
        by_id = {check["check_id"]: check["result"] for check in pre["checks"]}
        self.assertEqual("FAIL", by_id["triage_expected_match"])

    def test_acceptance_absent_fails(self):
        value = json.loads(json.dumps(task("T-001")))
        value["acceptance_criteria_present"] = False
        pre = ec.pre_execution(value, "A", ROUTES)
        by_id = {check["check_id"]: check["result"] for check in pre["checks"]}
        self.assertEqual("FAIL", by_id["acceptance_present"])

    def test_human_review_due_fails_for_approval(self):
        pre = ec.pre_execution(task("T-008"), "premium", ROUTES)
        by_id = {check["check_id"]: check["result"] for check in pre["checks"]}
        self.assertEqual("FAIL", by_id["human_review_due"])


class ExecutionChecksTests(unittest.TestCase):
    def test_all_checks_pass(self):
        usage = make_usage("EXP13-T-001-A", retries=1, tool_calls=1)
        checks = ec.execution_checks(usage, [], 1, 1, 1, 0.0004, 10.0, THRESHOLDS)
        self.assertTrue(all(check["result"] == "PASS" for check in checks))

    def test_usage_invalid_fails(self):
        usage = make_usage("EXP13-T-001-A")
        usage["measurement"] = "estimated"  # inconsistent with router_billing source
        checks = ec.execution_checks(usage, [], 0, 1, 0, 0.0004, 10.0, THRESHOLDS)
        by_id = {check["check_id"]: check["result"] for check in checks}
        self.assertEqual("FAIL", by_id["usage_valid"])

    def test_usage_consistent_mismatch_fails(self):
        usage = make_usage("EXP13-T-001-A", retries=0)
        checks = ec.execution_checks(usage, [], 1, 1, 0, 0.0004, 10.0, THRESHOLDS)
        by_id = {check["check_id"]: check["result"] for check in checks}
        self.assertEqual("FAIL", by_id["usage_consistent"])

    def test_retries_over_limit_fails(self):
        usage = make_usage("EXP13-T-001-A", retries=3)
        checks = ec.execution_checks(usage, [], 3, 1, 0, 0.0004, 10.0, THRESHOLDS)
        by_id = {check["check_id"]: check["result"] for check in checks}
        self.assertEqual("FAIL", by_id["retries_within_limit"])

    def test_defects_over_limit_fails(self):
        usage = make_usage("EXP13-T-001-A")
        checks = ec.execution_checks(usage, ["D-1"], 0, 1, 0, 0.0004, 10.0, THRESHOLDS)
        by_id = {check["check_id"]: check["result"] for check in checks}
        self.assertEqual("FAIL", by_id["defects_within_limit"])

    def test_cost_over_limit_fails(self):
        usage = make_usage("EXP13-T-001-A")
        checks = ec.execution_checks(usage, [], 0, 1, 0, 5.0, 1.0, THRESHOLDS)
        by_id = {check["check_id"]: check["result"] for check in checks}
        self.assertEqual("FAIL", by_id["cost_within_limit"])

    def test_cost_missing_not_applicable(self):
        usage = make_usage("EXP13-T-001-A")
        checks = ec.execution_checks(usage, [], 0, 1, 0, None, 10.0, THRESHOLDS)
        by_id = {check["check_id"]: check["result"] for check in checks}
        self.assertEqual("NOT_APPLICABLE", by_id["cost_within_limit"])


class DeriveOutcomeTests(unittest.TestCase):
    def test_human_required(self):
        self.assertEqual("HUMAN_REQUIRED", ec.derive_outcome({"escalation": "HUMAN_REVIEW_REQUIRED"}, []))

    def test_premium_rework(self):
        self.assertEqual("REWORK", ec.derive_outcome({"escalation": "PREMIUM_REQUIRED"}, []))

    def test_blocked_on_usage_invalid(self):
        execution = [
            {"check_id": "usage_valid", "result": "FAIL", "detail": ""},
            {"check_id": "usage_consistent", "result": "PASS", "detail": ""},
        ]
        self.assertEqual("BLOCKED", ec.derive_outcome({"escalation": "NONE"}, execution))

    def test_rework_on_defects(self):
        execution = [
            {"check_id": "usage_valid", "result": "PASS", "detail": ""},
            {"check_id": "usage_consistent", "result": "PASS", "detail": ""},
            {"check_id": "retries_within_limit", "result": "PASS", "detail": ""},
            {"check_id": "defects_within_limit", "result": "FAIL", "detail": ""},
            {"check_id": "cost_within_limit", "result": "PASS", "detail": ""},
        ]
        self.assertEqual("REWORK", ec.derive_outcome({"escalation": "NONE"}, execution))

    def test_pass(self):
        execution = [
            {"check_id": "usage_valid", "result": "PASS", "detail": ""},
            {"check_id": "usage_consistent", "result": "PASS", "detail": ""},
            {"check_id": "retries_within_limit", "result": "PASS", "detail": ""},
            {"check_id": "defects_within_limit", "result": "PASS", "detail": ""},
            {"check_id": "cost_within_limit", "result": "PASS", "detail": ""},
        ]
        self.assertEqual("PASS", ec.derive_outcome({"escalation": "NONE"}, execution))


class ComputeCostTests(unittest.TestCase):
    def test_observed_cost_returned(self):
        usage = make_usage("EXP13-T-001-A", cost=0.0004)
        cost, measurement = ec.compute_cost(usage, PRICING, "opencode-go/deepseek-v4-flash")
        self.assertEqual(0.0004, cost)
        self.assertEqual("observed", measurement)

    def test_reconstructed_from_tokens_estimated(self):
        usage = make_usage("EXP13-T-001-A", cost=None, input_tokens=1_000_000, output_tokens=0, model_calls=1)
        usage["observed_cost"] = None
        cost, measurement = ec.compute_cost(usage, PRICING, "opencode-go/deepseek-v4-flash")
        self.assertEqual(0.14, cost)
        self.assertEqual("estimated", measurement)

    def test_unobserved_when_no_execution(self):
        cost, measurement = ec.compute_cost(None, PRICING, "opencode-go/deepseek-v4-flash")
        self.assertIsNone(cost)
        self.assertEqual("unobserved", measurement)

    def test_unobserved_when_no_data(self):
        usage = ui.empty_record("EXP13-T-001-A")
        cost, measurement = ec.compute_cost(usage, PRICING, "opencode-go/deepseek-v4-flash")
        self.assertIsNone(cost)
        self.assertEqual("unobserved", measurement)


class EvaluateTests(unittest.TestCase):
    def test_evaluate_pass_end_to_end(self):
        usage = make_usage("EXP13-T-001-A")
        result = ec.evaluate(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=usage, defects=[], budget=10.0)
        self.assertEqual("PASS", result["outcome"])
        self.assertEqual("NONE", result["escalation"])
        self.assertEqual(9, len(result["checks"]))

    def test_evaluate_human_required_end_to_end(self):
        result = ec.evaluate(task("T-008"), "A", ROUTES, THRESHOLDS, PRICING, usage=None, defects=[])
        self.assertEqual("HUMAN_REQUIRED", result["outcome"])
        self.assertEqual("HUMAN_REVIEW_REQUIRED", result["escalation"])
        self.assertIsNone(result["cost_usd"])

    def test_evaluate_requires_usage_when_proceeding(self):
        with self.assertRaises(ContractError):
            ec.evaluate(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=None, defects=[])


if __name__ == "__main__":
    unittest.main()
