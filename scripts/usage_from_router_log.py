"""Build an honest USAGE_RECORD from Codex Router usage events.

The Router log contains real request token counts but no per-run identifier or
authoritative USD cost. This adapter therefore requires an explicit, isolated
time window plus a model, rejects mixed token-bearing traffic, and labels the
result ``execution_log`` / ``estimated``. It never reads Router credentials and
never promotes reconstructed data to observed billing.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

try:
    from scripts.usage_instrumentation import classify_measurement, validate_usage_record
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from usage_instrumentation import classify_measurement, validate_usage_record


class RouterUsageImportError(ValueError):
    pass


def default_events_path() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "codex-router" / "usage-events.jsonl"


def parse_timestamp(value: str, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise RouterUsageImportError(f"{field} must be a non-empty ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RouterUsageImportError(f"invalid {field}: {value!r}") from exc
    if parsed.tzinfo is None:
        raise RouterUsageImportError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise RouterUsageImportError(f"Router usage events file not found: {path}")
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RouterUsageImportError(f"invalid JSON at {path}:{line_number}") from exc
        if not isinstance(event, dict):
            raise RouterUsageImportError(f"event at {path}:{line_number} must be an object")
        events.append(event)
    return events


def _token_count(event: dict[str, Any], field: str) -> Optional[int]:
    value = event.get(field)
    if value is None:
        return None
    if type(value) is not int or value < 0:
        raise RouterUsageImportError(f"event {field} must be a non-negative integer")
    return value


def build_usage_record(
    events: list[dict[str, Any]],
    *,
    run_id: str,
    model: str,
    start: str,
    end: str,
    expected_calls: int,
    provider: Optional[str] = None,
) -> dict[str, Any]:
    start_at = parse_timestamp(start, "start")
    end_at = parse_timestamp(end, "end")
    if end_at <= start_at:
        raise RouterUsageImportError("end must be later than start")
    if type(expected_calls) is not int or expected_calls < 1:
        raise RouterUsageImportError("expected_calls must be a positive integer")

    in_window: list[tuple[dict[str, Any], datetime]] = []
    for event in events:
        at_value = event.get("at")
        if not isinstance(at_value, str):
            continue
        at = parse_timestamp(at_value, "event.at")
        if start_at <= at < end_at:
            in_window.append((event, at))

    token_bearing = [
        (event, at)
        for event, at in in_window
        if any(field in event for field in ("inputTokens", "outputTokens", "totalTokens"))
    ]
    unmetered_matches = [
        event for event, _ in in_window
        if event.get("model") == model
        and (provider is None or event.get("provider") == provider)
        and not any(field in event for field in ("inputTokens", "outputTokens", "totalTokens"))
    ]
    if unmetered_matches:
        raise RouterUsageImportError(
            f"matched window contains {len(unmetered_matches)} unmetered request(s); usage would be incomplete"
        )
    mismatched = [
        event for event, _ in token_bearing
        if event.get("model") != model or (provider is not None and event.get("provider") != provider)
    ]
    if mismatched:
        identities = sorted({f"{event.get('provider', 'unknown')}:{event.get('model', 'unknown')}" for event in mismatched})
        raise RouterUsageImportError(
            "time window contains token-bearing traffic outside the requested route: " + ", ".join(identities)
        )

    selected = [
        (event, at) for event, at in token_bearing
        if event.get("model") == model and (provider is None or event.get("provider") == provider)
    ]
    if not selected:
        raise RouterUsageImportError("no metered Router events matched the requested window/model/provider")
    if len(selected) != expected_calls:
        raise RouterUsageImportError(f"expected {expected_calls} model calls, found {len(selected)}")

    providers = {event.get("provider") for event, _ in selected}
    if None in providers or len(providers) != 1:
        raise RouterUsageImportError("matched events do not resolve to exactly one provider")

    input_tokens = sum(_token_count(event, "inputTokens") or 0 for event, _ in selected)
    output_tokens = sum(_token_count(event, "outputTokens") or 0 for event, _ in selected)
    for event, _ in selected:
        total = _token_count(event, "totalTokens")
        event_input = _token_count(event, "inputTokens")
        event_output = _token_count(event, "outputTokens")
        if total is not None and event_input is not None and event_output is not None and total != event_input + event_output:
            raise RouterUsageImportError("event totalTokens does not equal inputTokens + outputTokens")
    completed_at = max(at for _, at in selected)
    durations = [event.get("durationMs") for event, _ in selected]
    if any(not isinstance(value, (int, float)) or value < 0 for value in durations):
        raise RouterUsageImportError("matched event durationMs must be a non-negative number")
    started_at = min(at - timedelta(milliseconds=event["durationMs"]) for event, at in selected)

    record = {
        "schema_version": "1.0",
        "run_id": run_id,
        "provider": providers.pop(),
        "model": model,
        "input_tokens": input_tokens,
        "cached_input_tokens": None,
        "output_tokens": output_tokens,
        "observed_cost": None,
        "model_calls": len(selected),
        "tool_calls": None,
        "retries": None,
        "start_time": started_at.isoformat().replace("+00:00", "Z"),
        "end_time": completed_at.isoformat().replace("+00:00", "Z"),
        "progress_checkpoints": [],
        "measurement_source": "execution_log",
        "measurement": classify_measurement("execution_log"),
    }
    validate_usage_record(record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description="Create USAGE_RECORD from an isolated Codex Router event window")
    parser.add_argument("--events", type=Path, default=default_events_path())
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider")
    parser.add_argument("--start", required=True, help="inclusive event-completion ISO-8601 timestamp")
    parser.add_argument("--end", required=True, help="exclusive event-completion ISO-8601 timestamp")
    parser.add_argument("--expected-calls", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.expected_calls < 1:
        parser.error("--expected-calls must be >= 1")

    record = build_usage_record(
        load_events(args.events),
        run_id=args.run_id,
        model=args.model,
        provider=args.provider,
        start=args.start,
        end=args.end,
        expected_calls=args.expected_calls,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
