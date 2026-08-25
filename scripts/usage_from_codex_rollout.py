"""Build an honest USAGE_RECORD from one explicit Codex rollout turn."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.usage_instrumentation import classify_measurement, validate_usage_record
except ModuleNotFoundError:
    from usage_instrumentation import classify_measurement, validate_usage_record


class CodexRolloutUsageImportError(ValueError):
    pass


def _timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise CodexRolloutUsageImportError(f"{field} must be a non-empty ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CodexRolloutUsageImportError(f"invalid {field}: {value!r}") from exc
    if parsed.tzinfo is None:
        raise CodexRolloutUsageImportError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise CodexRolloutUsageImportError(f"Codex rollout file not found: {path}")
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CodexRolloutUsageImportError(f"invalid JSON at {path}:{line_number}") from exc
        if not isinstance(event, dict):
            raise CodexRolloutUsageImportError(f"event at {path}:{line_number} must be an object")
        events.append(event)
    return events


def _nonnegative_int(value: Any, field: str) -> int:
    if type(value) is not int or value < 0:
        raise CodexRolloutUsageImportError(f"{field} must be a non-negative integer")
    return value


def _usage(event: dict[str, Any]) -> dict[str, int] | None:
    if event.get("type") != "event_msg":
        return None
    payload = event.get("payload")
    if not isinstance(payload, dict) or payload.get("type") != "token_count":
        return None
    info = payload.get("info")
    last = info.get("last_token_usage") if isinstance(info, dict) else None
    if not isinstance(last, dict):
        raise CodexRolloutUsageImportError("token_count event has no last_token_usage object")
    values = {
        field: _nonnegative_int(last.get(field), f"last_token_usage.{field}")
        for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")
    }
    if values["cached_input_tokens"] > values["input_tokens"]:
        raise CodexRolloutUsageImportError("cached_input_tokens exceeds input_tokens")
    if values["total_tokens"] != values["input_tokens"] + values["output_tokens"]:
        raise CodexRolloutUsageImportError("total_tokens does not equal input_tokens + output_tokens")
    return values


def build_usage_record(events: list[dict[str, Any]], *, run_id: str, turn_id: str,
                       model: str, provider: str, expected_calls: int) -> dict[str, Any]:
    for field, value in (("run_id", run_id), ("turn_id", turn_id), ("model", model), ("provider", provider)):
        if not isinstance(value, str) or not value.strip():
            raise CodexRolloutUsageImportError(f"{field} must be a non-empty string")
    if type(expected_calls) is not int or expected_calls < 1:
        raise CodexRolloutUsageImportError("expected_calls must be a positive integer")

    session_providers = []
    for event in events:
        if event.get("type") == "session_meta":
            payload = event.get("payload")
            if not isinstance(payload, dict) or not isinstance(payload.get("model_provider"), str):
                raise CodexRolloutUsageImportError("session_meta has no model_provider")
            session_providers.append(payload["model_provider"])
    if session_providers != [provider]:
        raise CodexRolloutUsageImportError(
            f"rollout must contain exactly one session_meta for provider {provider!r}"
        )

    selected: list[tuple[dict[str, int], datetime]] = []
    started_at: datetime | None = None
    target_contexts = 0
    active = False
    for event in events:
        if event.get("type") == "turn_context":
            payload = event.get("payload")
            if not isinstance(payload, dict):
                raise CodexRolloutUsageImportError("turn_context payload must be an object")
            if payload.get("turn_id") == turn_id:
                target_contexts += 1
                if target_contexts > 1:
                    raise CodexRolloutUsageImportError("target turn_id appears in multiple turn_context events")
                if payload.get("model") != model:
                    raise CodexRolloutUsageImportError(f"target turn model is {payload.get('model')!r}, expected {model!r}")
                started_at = _timestamp(event.get("timestamp"), "turn_context.timestamp")
                active = True
            elif active:
                active = False
        elif active:
            usage = _usage(event)
            if usage is not None:
                selected.append((usage, _timestamp(event.get("timestamp"), "token_count.timestamp")))

    if target_contexts != 1 or started_at is None:
        raise CodexRolloutUsageImportError("target turn_id was not found exactly once")
    if not selected:
        raise CodexRolloutUsageImportError("target turn contains no complete token_count events")
    if len(selected) != expected_calls:
        raise CodexRolloutUsageImportError(f"expected {expected_calls} model calls, found {len(selected)}")
    if any(at < started_at for _, at in selected):
        raise CodexRolloutUsageImportError("token_count timestamp precedes the target turn")

    record = {
        "schema_version": "1.0", "run_id": run_id, "provider": provider, "model": model,
        "input_tokens": sum(item["input_tokens"] for item, _ in selected),
        "cached_input_tokens": sum(item["cached_input_tokens"] for item, _ in selected),
        "output_tokens": sum(item["output_tokens"] for item, _ in selected),
        "observed_cost": None, "model_calls": len(selected), "tool_calls": None, "retries": None,
        "start_time": started_at.isoformat().replace("+00:00", "Z"),
        "end_time": max(at for _, at in selected).isoformat().replace("+00:00", "Z"),
        "progress_checkpoints": [], "measurement_source": "execution_log",
        "measurement": classify_measurement("execution_log"),
    }
    validate_usage_record(record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description="Create USAGE_RECORD from one explicit Codex rollout turn")
    parser.add_argument("--rollout", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--turn-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--expected-calls", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.expected_calls < 1:
        parser.error("--expected-calls must be >= 1")
    record = build_usage_record(load_events(args.rollout), run_id=args.run_id, turn_id=args.turn_id,
                                model=args.model, provider=args.provider, expected_calls=args.expected_calls)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
