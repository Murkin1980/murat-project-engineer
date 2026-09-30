"""Regression guards for the EXP-13 Pilot Batch 1 evidence-gate semantics.

The 2026-09-30 blocked attempt (evidence/exp-13/PILOT_BATCH1_ATTEMPT_2026-09-30,
analysis in experiments/exp-13/FINDINGS.md) verified that the frozen
pre-registration fails closed for every proceeding entry and never fabricates
usage, while the three T-008 routes legally complete via pre-execution
escalation. These tests lock that invariant in.
"""

import hashlib
import json
import unittest
from pathlib import Path

from scripts import exp13_harness as eh
from scripts.triage_engine import ContractError

ROOT = Path(__file__).resolve().parents[1]

DATASET = json.loads((ROOT / "experiments" / "exp-13" / "tasks_v2.json").read_text(encoding="utf-8"))
ROUTES = json.loads((ROOT / "experiments" / "exp-13" / "routes.json").read_text(encoding="utf-8"))
THRESHOLDS = json.loads((ROOT / "experiments" / "exp-13" / "thresholds.json").read_text(encoding="utf-8"))
PRICING = json.loads((ROOT / "experiments" / "exp-13" / "pricing_snapshot.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ROOT / "evidence" / "exp-13" / "PILOT_BATCH1_PRE_REGISTRATION.json").read_text(encoding="utf-8"))
ATTEMPT_DIR = ROOT / "evidence" / "exp-13" / "PILOT_BATCH1_ATTEMPT_2026-09-30"


def task(task_id):
    return next(t for t in DATASET["tasks"] if t["task_id"] == task_id)


class EvidenceGateSemanticsTests(unittest.TestCase):
    def test_registered_manifest_fails_closed_for_every_proceeding_entry(self):
        """A proceeding entry without a usage record must never produce a record."""
        blocked = 0
        for entry in MANIFEST["entries"]:
            with self.subTest(run_id=entry["run_id"]):
                try:
                    eh.build_record(
                        task(entry["task_id"]), entry["route"], ROUTES, THRESHOLDS, PRICING,
                        usage=None, defects=entry["defects"],
                    )
                except ContractError as exc:
                    self.assertIn(
                        "usage record is required when the run proceeds to execution", str(exc)
                    )
                    blocked += 1
        self.assertEqual(15, blocked)

    def test_t008_routes_complete_via_pre_execution_escalation_without_usage(self):
        for route in ("A", "B", "premium"):
            with self.subTest(route=route):
                record = eh.build_record(
                    task("T-008"), route, ROUTES, THRESHOLDS, PRICING, usage=None, defects=[]
                )
                self.assertEqual("HUMAN_REVIEW_REQUIRED", record["escalation"])
                self.assertEqual("HUMAN_REQUIRED", record["outcome"])
                self.assertFalse(record["pre_execution"]["proceeded"])
                self.assertEqual("unobserved", record["usage"]["measurement"])
                self.assertIsNone(record["cost_usd"])
                self.assertEqual("unobserved", record["cost_measurement"])

    def test_unobserved_records_carry_nulls_never_zeros(self):
        for route in ("A", "B", "premium"):
            record = eh.build_record(
                task("T-008"), route, ROUTES, THRESHOLDS, PRICING, usage=None, defects=[]
            )
            for field in (
                "input_tokens", "cached_input_tokens", "output_tokens", "observed_cost",
                "model_calls", "tool_calls", "retries", "start_time", "end_time",
            ):
                self.assertIsNone(record["usage"][field], field)
            for field in ("retries", "model_calls", "tool_calls"):
                self.assertIsNone(record[field], field)


class CommittedAttemptEvidenceTests(unittest.TestCase):
    """The committed 2026-09-30 attempt evidence must stay self-consistent."""

    def setUp(self):
        self.report = json.loads((ATTEMPT_DIR / "ATTEMPT_REPORT.json").read_text(encoding="utf-8"))
        self.produced = {
            item["run_id"]: item
            for item in self.report["evidence_references"]["produced_records"]
        }

    def test_report_exists_with_expected_coverage(self):
        coverage = self.report["coverage"]
        self.assertEqual(18, coverage["total_registered"])
        self.assertEqual(18, coverage["attempted"])
        self.assertEqual(3, coverage["completed_via_pre_execution_escalation"])
        self.assertEqual(15, coverage["blocked_by_evidence_gate"])
        self.assertEqual(0, coverage["proceeded_to_execution"])
        self.assertEqual([], coverage["unexpected_gate_results"])
        self.assertTrue(self.report["determinism"]["deterministic"])
        self.assertTrue(self.report["registered_batch_attempt"]["fail_closed"])
        self.assertTrue(self.report["integrity_checks"]["records_structurally_valid"])
        self.assertTrue(self.report["integrity_checks"]["no_false_zeros_verified"])

    def test_reported_usage_evidence_states_are_all_unobserved(self):
        states = self.report["integrity_checks"]["usage_evidence_states_observed"]
        self.assertEqual({"observed": 0, "estimated": 0, "unobserved": 18}, states)

    def test_committed_records_match_their_recorded_digests(self):
        self.assertEqual(
            {"EXP13-T-008-A", "EXP13-T-008-B", "EXP13-T-008-premium"}, set(self.produced)
        )
        for run_id, item in self.produced.items():
            path = ROOT / item["path"]
            self.assertTrue(path.is_file(), f"missing committed record {run_id}")
            self.assertEqual(item["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), run_id)

    def test_committed_records_match_a_fresh_evaluation_of_the_frozen_assets(self):
        """The attempt evidence must stay reproducible from the frozen inputs."""
        for run_id, item in self.produced.items():
            parts = run_id.split("-")  # EXP13 - T - 008 - (A | B | premium)
            task_id, route = f"{parts[1]}-{parts[2]}", parts[-1]
            fresh = eh.build_record(
                task(task_id), route, ROUTES, THRESHOLDS, PRICING, usage=None, defects=[]
            )
            committed = json.loads((ROOT / item["path"]).read_text(encoding="utf-8"))
            self.assertEqual(committed, fresh, run_id)


if __name__ == "__main__":
    unittest.main()
