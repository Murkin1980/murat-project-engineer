import json
import tempfile
import unittest
from pathlib import Path

from scripts import usage_from_codex_rollout as adapter
from scripts import usage_instrumentation as usage


def context(turn_id="turn-target", model="gpt-5.6-sol", timestamp="2026-08-25T10:00:00Z"):
    return {"timestamp": timestamp, "type": "turn_context", "payload": {"turn_id": turn_id, "model": model}}


def tokens(input_tokens=100, cached=40, output=20, timestamp="2026-08-25T10:00:05Z"):
    return {"timestamp": timestamp, "type": "event_msg", "payload": {"type": "token_count", "info": {
        "last_token_usage": {"input_tokens": input_tokens, "cached_input_tokens": cached,
                             "output_tokens": output, "total_tokens": input_tokens + output}}}}


SESSION = {"timestamp": "2026-08-25T09:59:59Z", "type": "session_meta",
           "payload": {"id": "session", "model_provider": "openai"}}


EVENTS = [SESSION, context("historical"), tokens(999, 0, 1), context(),
          {"timestamp": "2026-08-25T10:00:01Z", "type": "response_item", "payload": {"content": "private"}},
          tokens(), tokens(50, 10, 5, "2026-08-25T10:00:08Z"),
          context("next-turn", "opencode-go/deepseek-v4-pro", "2026-08-25T10:00:09Z"),
          tokens(777, 0, 7, "2026-08-25T10:00:10Z")]


class CodexRolloutUsageAdapterTests(unittest.TestCase):
    def build(self, events=EVENTS, **overrides):
        options = {"run_id": "EXP13-T-001-premium", "turn_id": "turn-target", "model": "gpt-5.6-sol",
                   "provider": "openai", "expected_calls": 2}
        options.update(overrides)
        return adapter.build_usage_record(events, **options)

    def test_builds_record_for_only_the_explicit_turn(self):
        record = self.build()
        usage.validate_usage_record(record)
        self.assertEqual((150, 50, 25, 2), (record["input_tokens"], record["cached_input_tokens"],
                                                  record["output_tokens"], record["model_calls"]))
        self.assertEqual(("execution_log", "estimated", None),
                         (record["measurement_source"], record["measurement"], record["observed_cost"]))
        self.assertEqual("2026-08-25T10:00:00Z", record["start_time"])
        self.assertEqual("2026-08-25T10:00:08Z", record["end_time"])

    def test_rejects_model_mismatch(self):
        with self.assertRaisesRegex(adapter.CodexRolloutUsageImportError, "target turn model"):
            self.build(model="other")

    def test_rejects_provider_mismatch(self):
        with self.assertRaisesRegex(adapter.CodexRolloutUsageImportError, "session_meta"):
            self.build(provider="other")

    def test_rejects_duplicate_target_context(self):
        with self.assertRaisesRegex(adapter.CodexRolloutUsageImportError, "multiple turn_context"):
            self.build(EVENTS + [context(), tokens()])

    def test_rejects_call_count_mismatch(self):
        with self.assertRaisesRegex(adapter.CodexRolloutUsageImportError, "expected 1 model calls"):
            self.build(expected_calls=1)

    def test_rejects_positive_total_without_breakdown(self):
        event = tokens(0, 0, 0)
        event["payload"]["info"]["last_token_usage"]["total_tokens"] = 6105
        with self.assertRaisesRegex(adapter.CodexRolloutUsageImportError, "total_tokens"):
            self.build([SESSION, context(), event], expected_calls=1)

    def test_rejects_cached_tokens_above_input(self):
        with self.assertRaisesRegex(adapter.CodexRolloutUsageImportError, "cached_input_tokens"):
            self.build([SESSION, context(), tokens(10, 11, 1)], expected_calls=1)

    def test_rejects_missing_token_detail(self):
        broken = {"timestamp": "2026-08-25T10:00:05Z", "type": "event_msg",
                  "payload": {"type": "token_count", "info": {}}}
        with self.assertRaisesRegex(adapter.CodexRolloutUsageImportError, "last_token_usage"):
            self.build([SESSION, context(), broken], expected_calls=1)

    def test_load_events_rejects_malformed_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            path.write_text(json.dumps(context()) + "\nnot-json\n", encoding="utf-8")
            with self.assertRaisesRegex(adapter.CodexRolloutUsageImportError, "invalid JSON"):
                adapter.load_events(path)


if __name__ == "__main__":
    unittest.main()
