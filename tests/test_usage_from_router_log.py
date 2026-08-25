import json
import tempfile
import unittest
from pathlib import Path

from scripts import usage_from_router_log as adapter
from scripts import usage_instrumentation as usage


EVENTS = [
    {
        "meteringVersion": 1,
        "at": "2026-08-25T09:00:05Z",
        "model": "opencode-go/deepseek-v4-flash",
        "provider": "opencode-go",
        "status": 200,
        "durationMs": 5000,
        "inputTokens": 100,
        "outputTokens": 20,
        "totalTokens": 120,
    },
    {
        "meteringVersion": 1,
        "at": "2026-08-25T09:00:10Z",
        "model": "opencode-go/deepseek-v4-flash",
        "provider": "opencode-go",
        "status": 200,
        "durationMs": 2000,
        "inputTokens": 50,
        "outputTokens": 10,
        "totalTokens": 60,
    },
]


class RouterUsageAdapterTests(unittest.TestCase):
    def build(self, events=EVENTS, **overrides):
        options = {
            "run_id": "EXP13-T-001-A",
            "model": "opencode-go/deepseek-v4-flash",
            "provider": "opencode-go",
            "start": "2026-08-25T09:00:00Z",
            "end": "2026-08-25T09:01:00Z",
            "expected_calls": 2,
        }
        options.update(overrides)
        return adapter.build_usage_record(events, **options)

    def test_builds_estimated_record_from_real_token_events(self):
        record = self.build()
        usage.validate_usage_record(record)
        self.assertEqual(150, record["input_tokens"])
        self.assertEqual(30, record["output_tokens"])
        self.assertEqual(2, record["model_calls"])
        self.assertIsNone(record["observed_cost"])
        self.assertEqual("execution_log", record["measurement_source"])
        self.assertEqual("estimated", record["measurement"])
        self.assertEqual("2026-08-25T09:00:00Z", record["start_time"])
        self.assertEqual("2026-08-25T09:00:10Z", record["end_time"])

    def test_rejects_mixed_token_bearing_traffic(self):
        events = EVENTS + [{**EVENTS[0], "model": "gpt-5.6-sol"}]
        with self.assertRaisesRegex(adapter.RouterUsageImportError, "outside the requested route"):
            self.build(events)

    def test_rejects_unmetered_match(self):
        event = {key: value for key, value in EVENTS[0].items() if not key.endswith("Tokens")}
        with self.assertRaisesRegex(adapter.RouterUsageImportError, "unmetered request"):
            self.build([event], expected_calls=1)

    def test_rejects_partially_unmetered_match(self):
        event = {key: value for key, value in EVENTS[0].items() if not key.endswith("Tokens")}
        with self.assertRaisesRegex(adapter.RouterUsageImportError, "usage would be incomplete"):
            self.build(EVENTS + [event])

    def test_rejects_call_count_mismatch(self):
        with self.assertRaisesRegex(adapter.RouterUsageImportError, "expected 1 model calls"):
            self.build(expected_calls=1)

    def test_rejects_invalid_expected_calls(self):
        with self.assertRaisesRegex(adapter.RouterUsageImportError, "positive integer"):
            self.build(expected_calls=0)

    def test_rejects_inconsistent_total_tokens(self):
        events = [{**EVENTS[0], "totalTokens": 999}]
        with self.assertRaisesRegex(adapter.RouterUsageImportError, "totalTokens"):
            self.build(events, expected_calls=1)

    def test_load_events_rejects_malformed_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "usage-events.jsonl"
            path.write_text(json.dumps(EVENTS[0]) + "\nnot-json\n", encoding="utf-8")
            with self.assertRaisesRegex(adapter.RouterUsageImportError, "invalid JSON"):
                adapter.load_events(path)


if __name__ == "__main__":
    unittest.main()
