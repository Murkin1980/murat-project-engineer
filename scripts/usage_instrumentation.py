"""Run Usage Instrumentation for MPE.

Deterministic, stateless capture of per-run usage telemetry. This is the
forward-validation companion to the Compute Budget Gate: it records the minimum
fields (provider, model, input/cached/output tokens, observed cost, model/tool
calls, retries, start/end timestamps, progress checkpoints, measurement_source)
that every new run MUST write so the Compute Budget Estimator can later be
validated on OBSERVED data.

Design rules
------------
- ``observed`` / ``estimated`` / ``unobserved`` are DERIVED from
  ``measurement_source`` and never promoted: an estimated reconstruction is
  never reported as observed, and missing data is recorded as null, never as a
  fabricated zero.
- The recorder is stateless and deterministic: the same sequence of events
  produces the same record.
- This module writes telemetry only. It does not enforce a budget, block a run,
  or change the (still experimental) Compute Budget Gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

MEASUREMENT_SOURCES = (
    "provider_api",          # authoritative usage/billing API from the model provider
    "router_billing",        # Codex Router billing record
    "usage_api",             # any other authoritative usage API
    "execution_log",         # tokens parsed from committed execution logs
    "price_reconstruction",  # known calls x dated pricing snapshot
    "operator_estimate",     # human estimate
    "none",                  # no telemetry available
)

OBSERVED_SOURCES = {"provider_api", "router_billing", "usage_api"}
ESTIMATED_SOURCES = {"execution_log", "price_reconstruction", "operator_estimate"}

MEASUREMENTS = ("observed", "estimated", "unobserved")

USAGE_RECORD_REQUIRED = (
    "schema_version", "run_id", "provider", "model", "input_tokens",
    "cached_input_tokens", "output_tokens", "observed_cost", "model_calls",
    "tool_calls", "retries", "start_time", "end_time",
    "progress_checkpoints", "measurement_source", "measurement",
)


class UsageInstrumentationError(ValueError):
    pass


def classify_measurement(measurement_source: Optional[str]) -> str:
    """Derive the measurement quality from its source. Never promoted."""
    if measurement_source in OBSERVED_SOURCES:
        return "observed"
    if measurement_source in ESTIMATED_SOURCES:
        return "estimated"
    return "unobserved"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class UsageRecorder:
    """Accumulate per-run usage events and emit a canonical usage record."""

    run_id: str
    provider: Optional[str] = None
    model: Optional[str] = None
    start_time: Optional[str] = None
    input_tokens: Optional[int] = None
    cached_input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    observed_cost: Optional[float] = None
    model_calls: Optional[int] = None
    tool_calls: Optional[int] = None
    retries: Optional[int] = None
    progress_checkpoints: list[dict] = field(default_factory=list)

    def start(self, provider: Optional[str] = None, model: Optional[str] = None, timestamp: Optional[str] = None) -> "UsageRecorder":
        self.provider = provider
        self.model = model
        self.start_time = timestamp or now_iso()
        return self

    def record_model_call(
        self,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cached_input_tokens: int = 0,
        cost: Optional[float] = None,
    ) -> "UsageRecorder":
        if input_tokens < 0 or output_tokens < 0 or cached_input_tokens < 0:
            raise UsageInstrumentationError("token counts must be >= 0")
        self.input_tokens = (self.input_tokens or 0) + input_tokens
        self.output_tokens = (self.output_tokens or 0) + output_tokens
        self.cached_input_tokens = (self.cached_input_tokens or 0) + cached_input_tokens
        self.model_calls = (self.model_calls or 0) + 1
        if cost is not None:
            if cost < 0:
                raise UsageInstrumentationError("cost must be >= 0")
            self.observed_cost = (self.observed_cost or 0.0) + cost
        return self

    def record_tool_call(self, count: int = 1) -> "UsageRecorder":
        if count < 0:
            raise UsageInstrumentationError("tool call count must be >= 0")
        self.tool_calls = (self.tool_calls or 0) + count
        return self

    def record_retry(self, count: int = 1) -> "UsageRecorder":
        if count < 0:
            raise UsageInstrumentationError("retry count must be >= 0")
        self.retries = (self.retries or 0) + count
        return self

    def record_checkpoint(self, progress_percent: float, cost_usd: float, measurement_source: str) -> "UsageRecorder":
        if not 0 <= progress_percent <= 100:
            raise UsageInstrumentationError("progress_percent must be in [0, 100]")
        if cost_usd < 0:
            raise UsageInstrumentationError("cost_usd must be >= 0")
        if measurement_source not in MEASUREMENT_SOURCES:
            raise UsageInstrumentationError(f"invalid measurement_source: {measurement_source}")
        self.progress_checkpoints.append({
            "progress_percent": progress_percent,
            "cost_usd": cost_usd,
            "measurement_source": measurement_source,
        })
        return self

    def to_record(self, measurement_source: str = "none", end_time: Optional[str] = None) -> dict:
        if measurement_source not in MEASUREMENT_SOURCES:
            raise UsageInstrumentationError(f"invalid measurement_source: {measurement_source}")
        record = {
            "schema_version": "1.0",
            "run_id": self.run_id,
            "provider": self.provider,
            "model": self.model,
            "input_tokens": self.input_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "output_tokens": self.output_tokens,
            "observed_cost": self.observed_cost,
            "model_calls": self.model_calls,
            "tool_calls": self.tool_calls,
            "retries": self.retries,
            "start_time": self.start_time,
            "end_time": end_time or now_iso(),
            "progress_checkpoints": self.progress_checkpoints,
            "measurement_source": measurement_source,
            "measurement": classify_measurement(measurement_source),
        }
        validate_usage_record(record)
        return record


# --------------------------------------------------------------------------- #
# Validation and projection
# --------------------------------------------------------------------------- #

def _require_iso(value: Any, field: str) -> None:
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        raise UsageInstrumentationError(f"invalid {field}")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise UsageInstrumentationError(f"invalid {field}: timezone/format required") from exc


def _require_nonneg_int_or_null(value: Any, field: str) -> None:
    if value is None:
        return
    if type(value) is not int or value < 0:
        raise UsageInstrumentationError(f"{field} must be a non-negative integer or null")


def validate_usage_record(record: dict) -> None:
    """Validate a usage record against the canonical contract."""
    if not isinstance(record, dict) or set(record) != set(USAGE_RECORD_REQUIRED):
        missing = sorted(set(USAGE_RECORD_REQUIRED) - set(record))
        raise UsageInstrumentationError(f"usage record fields mismatch; missing: {missing}")

    if record["schema_version"] != "1.0":
        raise UsageInstrumentationError("schema_version must be 1.0")
    if not isinstance(record["run_id"], str) or not record["run_id"].strip():
        raise UsageInstrumentationError("run_id must be a non-empty string")

    for field in ("provider", "model"):
        if record[field] is not None and (not isinstance(record[field], str) or not record[field].strip()):
            raise UsageInstrumentationError(f"{field} must be a non-empty string or null")

    for field in ("input_tokens", "cached_input_tokens", "output_tokens", "model_calls", "tool_calls", "retries"):
        _require_nonneg_int_or_null(record[field], field)

    if record["observed_cost"] is not None:
        if not isinstance(record["observed_cost"], (int, float)) or record["observed_cost"] < 0:
            raise UsageInstrumentationError("observed_cost must be a non-negative number or null")

    _require_iso(record["start_time"], "start_time")
    _require_iso(record["end_time"], "end_time")

    measurement_source = record["measurement_source"]
    if measurement_source not in MEASUREMENT_SOURCES:
        raise UsageInstrumentationError(f"invalid measurement_source: {measurement_source}")
    expected = classify_measurement(measurement_source)
    if record["measurement"] != expected:
        raise UsageInstrumentationError(
            f"measurement {record['measurement']!r} does not match measurement_source {measurement_source!r} (expected {expected!r})"
        )
    if expected == "unobserved" and record["observed_cost"] is not None:
        raise UsageInstrumentationError("observed_cost must be null when measurement is unobserved")

    for checkpoint in record["progress_checkpoints"]:
        if not isinstance(checkpoint, dict) or set(checkpoint) != {"progress_percent", "cost_usd", "measurement_source"}:
            raise UsageInstrumentationError("progress checkpoint fields mismatch")
        progress = checkpoint["progress_percent"]
        if not isinstance(progress, (int, float)) or not 0 <= progress <= 100:
            raise UsageInstrumentationError("checkpoint progress_percent must be in [0, 100]")
        if not isinstance(checkpoint["cost_usd"], (int, float)) or checkpoint["cost_usd"] < 0:
            raise UsageInstrumentationError("checkpoint cost_usd must be >= 0")
        if checkpoint["measurement_source"] not in MEASUREMENT_SOURCES:
            raise UsageInstrumentationError(f"invalid checkpoint measurement_source: {checkpoint['measurement_source']}")


def summarize_usage(record: dict) -> dict:
    """Return a compact summary of a validated canonical usage record."""
    validate_usage_record(record)
    total_tokens = sum(
        record[field] or 0
        for field in ("input_tokens", "cached_input_tokens", "output_tokens")
    )
    return {
        "run_id": record["run_id"],
        "provider": record["provider"],
        "model": record["model"],
        "total_tokens": total_tokens,
        "model_calls": record["model_calls"],
        "tool_calls": record["tool_calls"],
        "retries": record["retries"],
        "cost": record["observed_cost"],
        "measurement": record["measurement"],
    }


def usage_to_compute_budget(record: dict) -> dict:
    """Project a usage record onto the compute-budget ``usage`` block.

    This is the ONLY projection path from ``USAGE_RECORD`` (the canonical usage
    source of truth) into ``COMPUTE_BUDGET.usage``; the compute-budget block must
    not be written independently.

    ``estimated_cost`` here is a generic destination field name, not a quality
    claim. The usage record's ``observed_cost`` maps onto it without changing its
    provenance: the quality is carried by ``measurement``, so an observed value
    stays observed even though it lands in a field named ``estimated_cost``.
    """
    validate_usage_record(record)
    return {
        "input_tokens": record["input_tokens"],
        "cached_input_tokens": record["cached_input_tokens"],
        "output_tokens": record["output_tokens"],
        "estimated_cost": record["observed_cost"],
        "measurement": record["measurement"],
    }


def usage_to_run_report(record: dict) -> dict:
    """Project a usage record onto the Run Report ``usage`` block."""
    validate_usage_record(record)
    return {key: value for key, value in record.items() if key not in ("schema_version", "run_id")}


def empty_record(run_id: str) -> dict:
    """An explicit UNOBSERVED record — nulls, never fake zeros."""
    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "provider": None,
        "model": None,
        "input_tokens": None,
        "cached_input_tokens": None,
        "output_tokens": None,
        "observed_cost": None,
        "model_calls": None,
        "tool_calls": None,
        "retries": None,
        "start_time": None,
        "end_time": None,
        "progress_checkpoints": [],
        "measurement_source": "none",
        "measurement": "unobserved",
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(description="MPE run usage instrumentation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("record", nargs="?", type=Path, help="validate a usage record JSON file")
    group.add_argument("--template", metavar="RUN_ID", help="emit an empty UNOBSERVED record for RUN_ID")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.template:
        payload = empty_record(args.template)
    else:
        payload = json.loads(args.record.read_text(encoding="utf-8"))
        validate_usage_record(payload)

    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
