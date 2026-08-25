import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import exp13_harness as eh
from scripts import usage_instrumentation as ui
from scripts.triage_engine import ContractError

ROOT = Path(__file__).resolve().parents[1]

DATASET = json.loads((ROOT / "experiments" / "exp-13" / "tasks_v2.json").read_text(encoding="utf-8"))
ROUTES = json.loads((ROOT / "experiments" / "exp-13" / "routes.json").read_text(encoding="utf-8"))["routes"]
THRESHOLDS = json.loads((ROOT / "experiments" / "exp-13" / "thresholds.json").read_text(encoding="utf-8"))
PRICING = json.loads((ROOT / "experiments" / "exp-13" / "pricing_snapshot.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "contracts" / "EXP13_EXECUTION_RECORD.schema.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ROOT / "evidence" / "exp-13" / "PILOT_BATCH1_PRE_REGISTRATION.json").read_text(encoding="utf-8"))

PILOT_TASKS = ["T-001", "T-004", "T-006", "T-008", "T-010", "T-012"]


def task(task_id):
    return next(t for t in DATASET["tasks"] if t["task_id"] == task_id)


def make_usage(run_id, retries=0, cost=0.0004):
    return (
        ui.UsageRecorder(run_id=run_id)
        .start(provider="OpenCode Zen", model="opencode-go/deepseek-v4-flash", timestamp="2026-08-21T09:00:00Z")
        .record_model_call(1000, 200, cost=cost)
        .to_record("router_billing", end_time="2026-08-21T09:10:00Z")
    )


class RunIdTests(unittest.TestCase):
    def test_make_run_id(self):
        self.assertEqual("EXP13-T-001-A", eh.make_run_id("T-001", "A"))
        self.assertEqual("EXP13-T-008-premium", eh.make_run_id("T-008", "premium"))

    def test_make_run_id_rejects_bad_task_id(self):
        with self.assertRaises(ContractError):
            eh.make_run_id("T-1", "A")

    def test_make_run_id_rejects_bad_route(self):
        with self.assertRaises(ContractError):
            eh.make_run_id("T-001", "premium-plus")


class LoadTaskTests(unittest.TestCase):
    def test_load_task_found(self):
        self.assertEqual("T-004", eh.load_task(DATASET, "T-004")["task_id"])

    def test_load_task_missing_raises(self):
        with self.assertRaises(ContractError):
            eh.load_task(DATASET, "T-999")


class BuildRecordTests(unittest.TestCase):
    def test_build_record_pass(self):
        record = eh.build_record(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=make_usage("EXP13-T-001-A"), defects=[], budget=10.0)
        self.assertEqual("EXP13-T-001-A", record["run_id"])
        self.assertEqual("PASS", record["outcome"])
        self.assertEqual("EXECUTED", record["state"])
        self.assertEqual("observed", record["cost_measurement"])

    def test_build_record_human_review_for_t008(self):
        record = eh.build_record(task("T-008"), "B", ROUTES, THRESHOLDS, PRICING, usage=None, defects=[])
        self.assertEqual("HUMAN_REQUIRED", record["outcome"])
        self.assertEqual("HUMAN_REVIEW_REQUIRED", record["escalation"])
        self.assertIsNone(record["cost_usd"])
        self.assertEqual("unobserved", record["usage"]["measurement"])

    def test_build_record_requires_usage_when_proceeding(self):
        with self.assertRaises(ContractError):
            eh.build_record(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=None, defects=[])

    def test_build_record_usage_run_id_mismatch(self):
        with self.assertRaises(ContractError):
            eh.build_record(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=make_usage("EXP13-T-002-A"), defects=[])

    def test_build_record_schema_roundtrip(self):
        record = eh.build_record(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=make_usage("EXP13-T-001-A"), defects=[], budget=10.0)
        self.assertEqual(set(SCHEMA["required"]), set(record))

    def test_build_record_cost_reconstructed(self):
        usage = make_usage("EXP13-T-001-A", cost=None)
        usage["observed_cost"] = None
        usage["input_tokens"] = 1_000_000
        usage["output_tokens"] = 0
        usage["cached_input_tokens"] = 0
        record = eh.build_record(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=usage, defects=[], budget=10.0)
        self.assertEqual("estimated", record["cost_measurement"])
        self.assertEqual(0.14, record["cost_usd"])

    def test_build_record_defects_rework(self):
        record = eh.build_record(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=make_usage("EXP13-T-001-A"), defects=["D-1"], budget=10.0)
        self.assertEqual("REWORK", record["outcome"])


class FrozenAssetsTests(unittest.TestCase):
    def test_dataset_has_12_tasks(self):
        self.assertEqual(12, len(DATASET["tasks"]))
        self.assertEqual([f"T-{n:03d}" for n in range(1, 13)], [t["task_id"] for t in DATASET["tasks"]])

    def test_t008_expects_human_approval(self):
        self.assertTrue(task("T-008")["expected"]["human_approval_required"])

    def test_pilot_t008_evidence_matches_pre_registered_stop(self):
        for route in ("A", "B", "premium"):
            record = json.loads(
                (ROOT / "evidence" / "exp-13" / f"EXP13-T-008-{route}.json").read_text(encoding="utf-8")
            )
            self.assertEqual(set(SCHEMA["required"]), set(record))
            self.assertEqual(f"EXP13-T-008-{route}", record["run_id"])
            self.assertFalse(record["pre_execution"]["proceeded"])
            self.assertEqual("HUMAN_REVIEW_REQUIRED", record["escalation"])
            self.assertEqual("HUMAN_REQUIRED", record["outcome"])
            self.assertEqual("unobserved", record["usage"]["measurement"])
            self.assertIsNone(record["cost_usd"])

    def test_all_tasks_triage_match_expected(self):
        from scripts.triage_engine import triage

        for value in DATASET["tasks"]:
            with self.subTest(task_id=value["task_id"]):
                triage_input = {key: value[key] for key in ("task_id", "summary", "affected_repositories", "acceptance_criteria_present", "rollback_known", "ratings", "signals")}
                output = triage(triage_input)
                self.assertEqual(value["expected"]["risk_tier"], output["recommended_risk_tier"])
                self.assertEqual(value["expected"]["human_approval_required"], output["human_approval_required"])

    def test_routes_map_to_known_slugs(self):
        self.assertEqual("opencode-go/deepseek-v4-flash", ROUTES["A"]["slug"])
        self.assertEqual("opencode-go/kimi-k2.7-code", ROUTES["B"]["slug"])
        self.assertEqual("gpt-5.6-sol", ROUTES["premium"]["slug"])

    def test_pricing_covers_all_route_slugs(self):
        per_mtok = PRICING["per_mtok"]
        for route in ("A", "B", "premium"):
            self.assertIn(ROUTES[route]["slug"], per_mtok)

    def test_pilot_tasks_present(self):
        for task_id in PILOT_TASKS:
            self.assertIsNotNone(eh.load_task(DATASET, task_id))


class BatchTests(unittest.TestCase):
    def test_plan_batch_accepts_18_entries(self):
        self.assertEqual(18, len(eh.plan_batch(MANIFEST, DATASET)))

    def test_plan_batch_rejects_over_max_runs(self):
        manifest = json.loads(json.dumps(MANIFEST))
        manifest["entries"] = manifest["entries"] + [dict(manifest["entries"][0])]
        with self.assertRaises(ContractError):
            eh.plan_batch(manifest, DATASET)

    def test_plan_batch_enforces_run_id(self):
        manifest = json.loads(json.dumps(MANIFEST))
        manifest["entries"][0]["run_id"] = "EXP13-T-999-A"
        with self.assertRaises(ContractError):
            eh.plan_batch(manifest, DATASET)

    def test_pre_registration_manifest_is_frozen(self):
        self.assertEqual("PRE_REGISTERED", MANIFEST["state"])
        self.assertEqual(18, MANIFEST["max_runs"])
        self.assertTrue(all(entry["usage_ref"] is None for entry in MANIFEST["entries"]))
        self.assertEqual(
            [task_id for task_id in PILOT_TASKS for _ in ("A", "B", "premium")],
            [entry["task_id"] for entry in MANIFEST["entries"]],
        )

    def test_run_batch_requires_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ContractError):
                eh.run_batch(MANIFEST, DATASET, ROUTES, THRESHOLDS, PRICING, Path(tmp))

    def test_run_batch_allows_missing_usage_for_pre_execution_escalation(self):
        manifest = {
            "batch_id": "EXP13-T008-SMOKE",
            "max_runs": 3,
            "entries": [
                {
                    "run_id": eh.make_run_id("T-008", route),
                    "task_id": "T-008",
                    "route": route,
                    "usage_ref": None,
                    "defects": [],
                }
                for route in ("A", "B", "premium")
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            result = eh.run_batch(manifest, DATASET, ROUTES, THRESHOLDS, PRICING, Path(tmp))

        self.assertEqual(3, len(result["records"]))
        for record in result["records"]:
            self.assertEqual("HUMAN_REVIEW_REQUIRED", record["escalation"])
            self.assertEqual("HUMAN_REQUIRED", record["outcome"])
            self.assertEqual("unobserved", record["usage"]["measurement"])
            self.assertIsNone(record["cost_usd"])


class SummaryTests(unittest.TestCase):
    def _records(self):
        a = eh.build_record(task("T-001"), "A", ROUTES, THRESHOLDS, PRICING, usage=make_usage("EXP13-T-001-A"), defects=[], budget=10.0)
        b = eh.build_record(task("T-008"), "B", ROUTES, THRESHOLDS, PRICING, usage=None, defects=[])
        return [a, b]

    def test_summarize_counts(self):
        summary = eh.summarize(self._records())
        self.assertEqual(2, summary["run_count"])
        self.assertEqual({"PASS": 1, "HUMAN_REQUIRED": 1}, summary["outcomes"])

    def test_summarize_by_route(self):
        summary = eh.summarize(self._records())
        self.assertIn("A", summary["by_route"])
        self.assertIn("B", summary["by_route"])


class CliTests(unittest.TestCase):
    def test_cli_single_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            usage_path = Path(tmp) / "usage.json"
            usage_path.write_text(json.dumps(make_usage("EXP13-T-001-A")), encoding="utf-8")
            output = Path(tmp) / "record.json"
            completed = subprocess.run(
                [
                    sys.executable, str(ROOT / "scripts" / "exp13_harness.py"),
                    "--task", "T-001", "--route", "A", "--usage", str(usage_path), "--output", str(output),
                ],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual("PASS", json.loads(output.read_text(encoding="utf-8"))["outcome"])

    def test_cli_human_required_without_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "record.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "exp13_harness.py"), "--task", "T-008", "--route", "A", "--output", str(output)],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual("HUMAN_REQUIRED", json.loads(output.read_text(encoding="utf-8"))["outcome"])


if __name__ == "__main__":
    unittest.main()
