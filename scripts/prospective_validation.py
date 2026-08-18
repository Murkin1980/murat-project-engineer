from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.triage_engine import ContractError, triage, validate_task
except ModuleNotFoundError:  # Direct `python scripts/prospective_validation.py` execution.
    from triage_engine import ContractError, triage, validate_task


RISK_TIERS = {"FAST", "VERIFIED", "DEEP-CHANGE"}
REGISTRATION_KEYS = {"case_id", "registered_at", "baseline_commit", "task", "acceptance_criteria", "non_scope", "triage_input", "pre_registered_human_label", "engine_output", "observed_final_classification", "state"}
LABEL_KEYS = {"risk_tier", "human_approval_required", "rationale"}


def validate_label(label: dict[str, Any], require_rationale: bool = True) -> None:
    expected = LABEL_KEYS if require_rationale else {"risk_tier", "human_approval_required"}
    if not isinstance(label, dict) or set(label) != expected:
        raise ContractError("classification fields do not match the contract")
    if label["risk_tier"] not in RISK_TIERS or not isinstance(label["human_approval_required"], bool):
        raise ContractError("invalid classification")
    if require_rationale and (not isinstance(label["rationale"], str) or not label["rationale"]):
        raise ContractError("human label requires rationale")


def validate_registration(registration: dict[str, Any]) -> None:
    if not isinstance(registration, dict) or set(registration) != REGISTRATION_KEYS:
        raise ContractError("registration fields do not match the contract")
    if registration["state"] != "REGISTERED" or registration["engine_output"] is not None or registration["observed_final_classification"] is not None:
        raise ContractError("pre-registration must not contain post-registration results")
    if not isinstance(registration["case_id"], str) or not re.fullmatch(r"EXP12-P-[0-9]{3}", registration["case_id"]):
        raise ContractError("invalid prospective case_id")
    validate_task(registration["triage_input"])
    if registration["triage_input"]["task_id"] != registration["case_id"]:
        raise ContractError("case_id and triage task_id must match")
    validate_label(registration["pre_registered_human_label"])


def _pair(label: dict[str, Any]) -> tuple[str, bool]:
    return label["risk_tier"], label["human_approval_required"]


def evaluate(registration: dict[str, Any], observed: dict[str, Any], registration_ref: str, registration_bytes: bytes) -> dict[str, Any]:
    validate_registration(registration)
    validate_label(observed, require_rationale=False)
    engine = triage(registration["triage_input"])
    engine_path = Path(__file__).with_name("triage_engine.py")
    engine_label = {"risk_tier": engine["recommended_risk_tier"], "human_approval_required": engine["human_approval_required"]}
    human = registration["pre_registered_human_label"]
    return {
        "case_id": registration["case_id"],
        "registration_ref": registration_ref,
        "registration_sha256": hashlib.sha256(registration_bytes).hexdigest(),
        "engine_ref": "scripts/triage_engine.py",
        "engine_sha256": hashlib.sha256(engine_path.read_bytes()).hexdigest(),
        "engine_output": engine,
        "pre_registered_human_label": human,
        "observed_final_classification": observed,
        "human_engine_agreement": _pair(human) == _pair(engine_label),
        "engine_observed_agreement": _pair(engine_label) == _pair(observed),
        "human_observed_agreement": _pair(human) == _pair(observed),
        "state": "EVALUATED",
        "evaluator_version": "0.1.0"
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate an immutable EXP-12 prospective registration")
    parser.add_argument("registration", type=Path)
    parser.add_argument("--observed-risk-tier", required=True, choices=sorted(RISK_TIERS))
    parser.add_argument("--observed-human-approval", required=True, choices=["true", "false"])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raw = args.registration.read_bytes()
    registration = json.loads(raw.decode("utf-8"))
    observed = {"risk_tier": args.observed_risk_tier, "human_approval_required": args.observed_human_approval == "true"}
    result = evaluate(registration, observed, args.registration.as_posix(), raw)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
