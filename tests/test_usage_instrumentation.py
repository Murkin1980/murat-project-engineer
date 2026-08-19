import json
import unittest
from pathlib import Path

from scripts import compute_budget as cb
from scripts import usage_instrumentation as ui

ROOT = Path(__file__).resolve().parents[1]


class ClassificationTests(unittest.TestCase):
    def test_observed_sources(self):
        for source in ("provider_api", "router_billing", "usage_api"):
            self.assertEqual("observed", ui.classify_measurement(source))

    def test_estimated_sources(self):
        for source in ("execution_log", "price_reconstruction", "operator_estimate"):
            self.assertEqual("estimated", ui.classify_measurement(source))

    def test_unobserved_sources(self):
        for source in ("none", None, "bogus"):
            self.assertEqual("unobserved", ui.classify_measurement(source))


class RecorderTests(unittest.TestCase):
    def _recorder(self):
        return ui.UsageRecorder(run_id="RUN-A").start(
            provider="OpenCode Zen",
            model="opencode-go/deepseek-v4-flash",
            timestamp="2026-08-20T09:00:00Z",
        )

    def test_recorder_accumulates_deterministically(self):
        a = self._recorder().record_model_call(100, 40, cached_input_tokens=10, cost=0.02).record_model_call(200, 80).record_tool_call().record_retry()
        b = self._recorder().record_model_call(100, 40, cached_input_tokens=10, cost=0.02).record_model_call(200, 80).record_tool_call().record_retry()
        rec_a = a.to_record("router_billing", end_time="2026-08-20T09:22:00Z")
        rec_b = b.to_record("router_billing", end_time="2026-08-20T09:22:00Z")
        self.assertEqual(rec_a, rec_b)
        self.assertEqual(300, rec_a["input_tokens"])
        self.assertEqual(120, rec_a["output_tokens"])
        self.assertEqual(10, rec_a["cached_input_tokens"])
        self.assertEqual(0.02, rec_a["observed_cost"])
        self.assertEqual(2, rec_a["model_calls"])
        self.assertEqual(1, rec_a["tool_calls"])
        self.assertEqual(1, rec_a["retries"])

    def test_unrecorded_fields_stay_null_not_zero(self):
        record = self._recorder().to_record("none", end_time="2026-08-20T09:22:00Z")
        self.assertIsNone(record["input_tokens"])
        self.assertIsNone(record["model_calls"])
        self.assertIsNone(record["retries"])
        self.assertEqual("unobserved", record["measurement"])

    def test_negative_tokens_rejected(self):
        with self.assertRaises(ui.UsageInstrumentationError):
            self._recorder().record_model_call(-1, 0)

    def test_checkpoint_recorded(self):
        rec = self._recorder().record_checkpoint(20, 0.11, "router_billing").to_record("router_billing", end_time="2026-08-20T09:22:00Z")
        self.assertEqual([{"progress_percent": 20, "cost_usd": 0.11, "measurement_source": "router_billing"}], rec["progress_checkpoints"])

    def test_bad_checkpoint_progress_rejected(self):
        with self.assertRaises(ui.UsageInstrumentationError):
            self._recorder().record_checkpoint(101, 0.11, "router_billing")

    def test_bad_measurement_source_rejected(self):
        with self.assertRaises(ui.UsageInstrumentationError):
            self._recorder().to_record("imaginary", end_time="2026-08-20T09:22:00Z")


class ValidationTests(unittest.TestCase):
    def test_example_valid(self):
        record = json.loads((ROOT / "contracts" / "USAGE_RECORD.example.json").read_text(encoding="utf-8"))
        ui.validate_usage_record(record)  # does not raise

    def test_empty_record_is_unobserved_and_valid(self):
        record = ui.empty_record("RUN-X")
        ui.validate_usage_record(record)
        self.assertEqual("unobserved", record["measurement"])
        self.assertIsNone(record["observed_cost"])

    def test_unobserved_with_cost_rejected(self):
        record = ui.empty_record("RUN-X")
        record["observed_cost"] = 1.0
        with self.assertRaises(ui.UsageInstrumentationError):
            ui.validate_usage_record(record)

    def test_measurement_must_match_source(self):
        record = json.loads((ROOT / "contracts" / "USAGE_RECORD.example.json").read_text(encoding="utf-8"))
        record["measurement"] = "estimated"  # inconsistent with router_billing -> observed
        with self.assertRaises(ui.UsageInstrumentationError):
            ui.validate_usage_record(record)

    def test_missing_field_rejected(self):
        record = ui.empty_record("RUN-X")
        del record["retries"]
        with self.assertRaises(ui.UsageInstrumentationError):
            ui.validate_usage_record(record)

    def test_invalid_timestamp_rejected(self):
        record = ui.empty_record("RUN-X")
        record["start_time"] = "not-a-time"
        with self.assertRaises(ui.UsageInstrumentationError):
            ui.validate_usage_record(record)


class ProjectionTests(unittest.TestCase):
    def test_usage_to_compute_budget(self):
        record = json.loads((ROOT / "contracts" / "USAGE_RECORD.example.json").read_text(encoding="utf-8"))
        block = ui.usage_to_compute_budget(record)
        self.assertEqual(record["input_tokens"], block["input_tokens"])
        self.assertEqual(record["observed_cost"], block["estimated_cost"])
        self.assertEqual("observed", block["measurement"])

    def test_usage_to_run_report_drops_envelope(self):
        record = json.loads((ROOT / "contracts" / "USAGE_RECORD.example.json").read_text(encoding="utf-8"))
        block = ui.usage_to_run_report(record)
        self.assertNotIn("schema_version", block)
        self.assertNotIn("run_id", block)
        self.assertIn("provider", block)

    def test_round_trip_into_snapshot(self):
        record = json.loads((ROOT / "contracts" / "USAGE_RECORD.example.json").read_text(encoding="utf-8"))
        usage = ui.usage_to_compute_budget(record)
        snapshot = cb.compute_snapshot(
            compute_budget={"currency": "USD", "planned_budget": 80.0, "hard_limit": 100.0},
            preflight=None,
            usage=usage,
            routing={"recommended_stack": ["opencode-go/deepseek-v4-flash"], "actual_provider_mix": {"opencode-go/deepseek-v4-flash": 1.0}},
            project_progress_percent=50.0,
        )
        cb.validate_snapshot(snapshot)
        self.assertEqual("observed", snapshot["usage"]["measurement"])


class RunReportIntegrationTests(unittest.TestCase):
    def test_run_report_schema_has_usage_block(self):
        schema = json.loads((ROOT / "contracts" / "RUN_REPORT.schema.json").read_text(encoding="utf-8"))
        self.assertIn("usage", schema["properties"])
        self.assertNotIn("usage", schema["required"])  # optional for backward compat

    def test_run_report_example_usage_validates(self):
        example = json.loads((ROOT / "contracts" / "RUN_REPORT.example.json").read_text(encoding="utf-8"))
        block = example["usage"]
        # The run-report usage block omits schema_version/run_id; validate as a full record.
        record = {"schema_version": "1.0", "run_id": example["run_id"], **block}
        ui.validate_usage_record(record)

    def test_usage_record_template_fields_complete(self):
        text = (ROOT / "contracts" / "USAGE_RECORD.md").read_text(encoding="utf-8")
        for field in ui.USAGE_RECORD_REQUIRED:
            if field in ("schema_version", "run_id"):
                continue
            self.assertIn(field, text)


if __name__ == "__main__":
    unittest.main()
