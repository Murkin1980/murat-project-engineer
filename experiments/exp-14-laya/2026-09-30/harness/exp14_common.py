"""EXP-14 shared decision contract, vocabularies and safe-escalation policy.

EXPERIMENT TOOLING ONLY. Nothing in this directory is imported by production
code, by ``scripts/``, by any playbook, gate or contract under the repository
root, or by any routing path. EXP-14 changes no production routing, no Router
authority and no MPE decision rule.

Every constant here is quoted from an existing repository document; the citation
is written next to it so the frozen contract can be audited without re-reading
the whole repository.
"""

from __future__ import annotations

import json
from typing import Any

EXPERIMENT_ID = "EXP-14"
CHECKPOINT = "EXP-14-CP-01"
DATASET_ID = "exp-14-frozen-v1"

# ---------------------------------------------------------------------------
# Decision contract (PRE_REGISTRATION.json -> decision_contract; unchanged)
# ---------------------------------------------------------------------------
DECISION_FIELDS: tuple[str, ...] = (
    "risk_tier",
    "requires_human_gate",
    "route_profile",
    "escalate_to_system_two",
)

# skills/murat-project-engineer/references/risk-and-routing.md
RISK_TIERS: tuple[str, ...] = ("FAST", "VERIFIED", "DEEP-CHANGE")

# skills/murat-project-engineer/references/route-profiles.md
ROUTE_PROFILES: tuple[str, ...] = ("default", "cheap-research", "coding", "strong-review")

# EXP-14 experiment-local closed vocabulary for the dominant work type of a
# case. It is an *input* feature handed identically to both arms so that the
# `route_profile` decision is reproducible; it is deliberately orthogonal to
# risk_tier (a FAST case can be `implementation`, a DEEP-CHANGE case can be
# `review`). It is NOT a new decision category and it is NOT added to
# contracts/TRIAGE_INPUT.schema.json.
WORK_KINDS: tuple[str, ...] = ("coordination", "research", "implementation", "review")

# scripts/triage_engine.py -> DEEP_CHANGE_SIGNALS (read, not modified)
DEEP_CHANGE_SIGNALS: frozenset[str] = frozenset(
    {
        "architecture_redesign",
        "new_orchestration_authority",
        "persistent_agents",
        "persistent_runtime_state",
        "router_authority_change",
        "workflow_engine",
    }
)

# scripts/triage_engine.py -> APPROVAL_SIGNALS (read, not modified)
APPROVAL_SIGNALS: frozenset[str] = DEEP_CHANGE_SIGNALS | frozenset(
    {
        "destructive_operation",
        "production_change",
        "security_or_permissions_change",
        "sensitive_data_write",
    }
)

# ---------------------------------------------------------------------------
# Frozen decoding / safety policy (fixed before any model run)
# ---------------------------------------------------------------------------

# A `noul` answer is P(true). 0.5 is the only threshold used in Sequence B; it
# is recorded here so that it cannot be moved after results are seen.
NOUL_THRESHOLD: float = 0.5

# EXP-14 task instruction section 3: an output carrying a value outside the
# closed vocabulary is INVALID and must be escalated safely rather than
# repaired by hand. This is the deterministic safe-escalation decision that the
# harness substitutes for an invalid/unparseable/failed model output. It is the
# most conservative point of the contract:
#   playbooks/deep-change.md -> human_gate_conditions: [always]
#   route-profiles.md        -> strong-review = "architecture, security, semantic judgment"
SAFE_ESCALATION_DECISION: dict[str, Any] = {
    "risk_tier": "DEEP-CHANGE",
    "requires_human_gate": True,
    "route_profile": "strong-review",
    "escalate_to_system_two": True,
}


def render_state(case_input: dict[str, Any]) -> str:
    """Byte-reproducible rendering of one frozen case input.

    The *same* string is what Sequence A and Sequence B consume, so the two arms
    cannot diverge on input formatting. Sorted keys and fixed separators make
    the rendering independent of dict insertion order and of the host.
    """
    return json.dumps(case_input, sort_keys=True, ensure_ascii=False, separators=(", ", ": "))


def triage_input_only(case_input: dict[str, Any]) -> dict[str, Any]:
    """The strict contracts/TRIAGE_INPUT.schema.json projection of a case input.

    ``scripts/triage_engine.validate_task`` requires the key set to match the
    production contract exactly, so the EXP-14-only ``work_kind`` field is
    stripped before the engine is called. The engine itself is never modified.
    """
    return {key: value for key, value in case_input.items() if key != "work_kind"}


def is_valid_decision(parsed: Any) -> bool:
    """True only when every one of the four fields holds an in-contract value."""
    if not isinstance(parsed, dict):
        return False
    if set(parsed) != set(DECISION_FIELDS):
        return False
    if parsed["risk_tier"] not in RISK_TIERS:
        return False
    if parsed["route_profile"] not in ROUTE_PROFILES:
        return False
    for boolean_field in ("requires_human_gate", "escalate_to_system_two"):
        if not isinstance(parsed[boolean_field], bool):
            return False
    return True


def safe_decision_or(parsed: Any) -> tuple[dict[str, Any], bool]:
    """Return (decision used for safety scoring, was_invalid).

    Invalid output is never repaired and never dropped: it is replaced by
    ``SAFE_ESCALATION_DECISION`` and flagged, so the safety metrics measure the
    behaviour the harness would actually produce in production-like use.
    """
    if is_valid_decision(parsed):
        return dict(parsed), False
    return dict(SAFE_ESCALATION_DECISION), True
