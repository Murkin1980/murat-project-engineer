"""EXP-20 CP-03 proof P2 — deterministic failure classification onto the existing MPE gate vocabulary.

Donors (read-only audit):

* OpenHands ``software-agent-sdk`` ``openhands/sdk/event/error_classification.py`` (MIT) —
  a deliberately small, closed failure contract shared by SDK, UI and telemetry:
  ``FailureKind`` (auth, quota, rate_limit, config, transient, agent_action, internal,
  unknown) + ``retryable`` + ``user_action`` (none/retry/settings). Two donor rules are
  borrowed verbatim in spirit: authoritative exception classes are matched **before**
  message heuristics (so incidental wording cannot override a typed failure), and the
  raw ``detail`` text is inspected locally only and is **never** copied into the
  classification that crosses an evidence boundary.
* Dify ``api/core/tools/errors.py`` + ``api/core/tools/tool_engine.py`` +
  ``api/core/workflow/nodes/agent_v2/output_failure_orchestrator.py`` — typed error
  classes per failure cause (provider-not-found, tool-not-found, parameter validation,
  credential validation, invoke error, schema error, SSRF, credential policy), a
  per-invocation ``ToolInvokeMeta`` (``time_cost`` + ``error``) instead of a bare
  exception, and a **state-free** decision orchestrator: the caller owns the attempt
  counter, the orchestrator only computes the decision, and competing strategies are
  merged by a most-restrictive precedence table.

Host (UNCHANGED and authoritative):

* ``gates/registry.yaml`` — each gate already declares ``failure_state``
  (REWORK / BLOCKED / HUMAN_REQUIRED) and a ``retry_policy``;
* ``scripts/execution_runner.py`` + ``scripts/task_acceptance.py`` — the single
  enforcement point, fail-closed;
* ``scripts/dispatch_autonomy.py`` — the existing most-restrictive composition rule
  (``min`` over privilege ceilings). This proof reuses that idea instead of inventing a
  second composition model.

The classifier is an *annotation* derived after the acceptance decision. It cannot grant
execution, cannot lower a gate's declared ``failure_state``, and cannot override the
deep-change or approval path. Everything it emits is either a donor kind name or an
existing MPE gate value.
"""
from __future__ import annotations

import re
from pathlib import Path

# --- donor vocabulary, reused unchanged (no new MPE status model) -------------------
KIND_AUTH = "auth"
KIND_QUOTA = "quota"
KIND_RATE_LIMIT = "rate_limit"
KIND_CONFIG = "config"
KIND_TRANSIENT = "transient"
KIND_AGENT_ACTION = "agent_action"
KIND_INTERNAL = "internal"
KIND_UNKNOWN = "unknown"

FAILURE_KINDS = (
    KIND_AUTH,
    KIND_QUOTA,
    KIND_RATE_LIMIT,
    KIND_CONFIG,
    KIND_TRANSIENT,
    KIND_AGENT_ACTION,
    KIND_INTERNAL,
    KIND_UNKNOWN,
)

ACTION_NONE = "none"
ACTION_RETRY = "retry"
ACTION_SETTINGS = "settings"

# Fail-closed kinds: never auto-retried, always at least HUMAN_REQUIRED.
# ``auth``/``quota`` need a human credential/budget decision (SCOPE-CHANGE-CONTROL §15);
# ``internal``/``unknown`` are not diagnosed, so they must not be retried blindly.
NO_AUTO_RETRY = frozenset({KIND_AUTH, KIND_QUOTA, KIND_INTERNAL, KIND_UNKNOWN})

# Existing MPE gate failure states, ordered least → most restrictive. RETRY is not an MPE
# state: it is the bounded correction a gate's own ``retry_policy`` already allows.
RESTRICTION = {"RETRY": 0, "REWORK": 1, "BLOCKED": 2, "HUMAN_REQUIRED": 3}

# Explicit, auditable derivation of a bounded retry budget from the *registry's own*
# ``retry_policy`` prose. Rules are tried in order, first match wins, and the default is
# 0 (fail-closed). No prose is invented here and no gate is edited.
_BUDGET_RULES: tuple[tuple[str, int], ...] = (
    ("cannot be overridden", 0),
    ("requires a separate explicit human", 0),
    ("report the status", 0),
    ("define rollback before continuing", 0),
    ("surface the anomaly", 0),
    ("once", 1),
    ("correct", 1),
    ("rescan", 1),
    ("regenerate", 1),
    ("supply the missing", 1),
    ("reject the invalid", 1),
    ("create or restore", 1),
    ("isolate writers", 1),
    ("complete the preflight", 1),
)

# Authoritative exception-class names, matched before any message text (donor ordering).
_CLASS_FIRST: tuple[tuple[frozenset[str], str, bool, str], ...] = (
    (frozenset({"ContractError"}), KIND_AGENT_ACTION, True, ACTION_RETRY),
    (frozenset({"DuplicateEventConflict"}), KIND_AGENT_ACTION, False, ACTION_NONE),
    (frozenset({"FileNotFoundError", "NotADirectoryError"}), KIND_CONFIG, True, ACTION_SETTINGS),
    (frozenset({"PermissionError"}), KIND_AUTH, False, ACTION_SETTINGS),
    (frozenset({"TimeoutError", "asyncio.TimeoutError"}), KIND_TRANSIENT, True, ACTION_RETRY),
    (frozenset({"ConnectionError", "ConnectionResetError", "BrokenPipeError"}), KIND_TRANSIENT, True, ACTION_RETRY),
    (frozenset({"MemoryError"}), KIND_QUOTA, False, ACTION_SETTINGS),
    (frozenset({"RecursionError", "KeyError", "TypeError", "AttributeError", "IndexError", "AssertionError"}), KIND_INTERNAL, False, ACTION_NONE),
    (frozenset({"ComputeBudgetExceeded", "MaxBudgetReached", "QuotaExceeded"}), KIND_QUOTA, False, ACTION_SETTINGS),
    (frozenset({"CredentialError", "AuthenticationError", "UnauthorizedError"}), KIND_AUTH, False, ACTION_SETTINGS),
)

# Message heuristics, applied only to opaque wrapper codes (donor ordering rule 2).
_DETAIL_TOKENS: tuple[tuple[tuple[str, ...], str, bool, str], ...] = (
    (("invalid api key", "incorrect api key", "unauthorized", "error code: 401", "authentication required", "token_not_found"), KIND_AUTH, False, ACTION_SETTINGS),
    (("insufficient balance", "quota", "budget has been exceeded", "hard_limit", "credits"), KIND_QUOTA, False, ACTION_SETTINGS),
    (("rate limit", "error code: 429", "too many requests"), KIND_RATE_LIMIT, True, ACTION_RETRY),
    (("timeout", "bad gateway", "service temporarily unavailable", "connection error", "cannot connect", "error code: 5"), KIND_TRANSIENT, True, ACTION_RETRY),
    (("model not found", "provider not provided", "no models loaded", "invalid params", "endpoint"), KIND_CONFIG, False, ACTION_SETTINGS),
    (("validation error", "does not match the contract", "missing fields", "schema"), KIND_AGENT_ACTION, True, ACTION_RETRY),
)

# Generic wrapper classes whose name alone is not specific enough (donor rule 3).
_WRAPPER_FALLBACK: tuple[tuple[frozenset[str], str, bool, str], ...] = (
    (frozenset({"HTTPError", "RequestException", "HTTPStatusError", "APIError", "GatewayError"}), KIND_TRANSIENT, True, ACTION_RETRY),
    (frozenset({"ValueError", "RuntimeError", "OSError"}), KIND_UNKNOWN, False, ACTION_NONE),
)


def _classification(kind: str, retryable: bool, executor_action: str) -> dict:
    """The only failure metadata allowed to cross an evidence boundary (donor rule).

    Frozen shape, no free text: the exception message is *never* copied here, so a secret
    or a transcript fragment inside a provider error cannot leak into MPE evidence.
    """
    return {
        "kind": kind,
        "retryable": bool(retryable),
        "executor_action": executor_action,
        "evidence_safe": True,
    }


def _class_names(exc: BaseException) -> list[str]:
    """Exception class names, most specific first (the donor's authoritative-first rule)."""
    return [cls.__name__ for cls in type(exc).__mro__ if cls is not object]


def _match_class(name: str, rules) -> dict | None:
    for allowed, kind, retryable, action in rules:
        if name in allowed:
            return _classification(kind, retryable, action)
    return None


def classify_failure(exc: BaseException) -> dict:
    """Classify one failure into the closed donor vocabulary (deterministic, no I/O).

    Order (donor rule): authoritative exception classes first — walked from the most
    specific class outward, so a subclass such as ``DuplicateEventConflict`` is never
    swallowed by its ``ContractError`` base — then message heuristics for opaque wrappers,
    then the generic wrapper fallback, then UNKNOWN (fail-closed).
    """
    names = _class_names(exc)
    detail = str(exc).casefold()

    for name in names:
        matched = _match_class(name, _CLASS_FIRST)
        if matched:
            return matched

    for tokens, kind, retryable, action in _DETAIL_TOKENS:
        if any(token in detail for token in tokens):
            return _classification(kind, retryable, action)

    for name in names:
        matched = _match_class(name, _WRAPPER_FALLBACK)
        if matched:
            return matched

    return _classification(KIND_UNKNOWN, False, ACTION_NONE)


def load_gates(registry_path: Path) -> dict[str, dict]:
    """Read the real ``gates/registry.yaml`` with a minimal, dependency-free parser.

    MPE has no YAML dependency (``scripts/validate_package.py`` also reads this file with
    regular expressions), and this proof adds none.
    """
    text = registry_path.read_text(encoding="utf-8")
    gates: dict[str, dict] = {}
    current: dict | None = None
    for line in text.splitlines():
        if re.match(r"^\s*-\s+gate_id:\s*([a-z_]+)\s*$", line):
            gate_id = re.match(r"^\s*-\s+gate_id:\s*([a-z_]+)\s*$", line).group(1)
            current = {"gate_id": gate_id}
            gates[gate_id] = current
            continue
        if current is None:
            continue
        match = re.match(r"^\s+([a-z_]+):\s*(.+?)\s*$", line)
        if match:
            key, value = match.group(1), match.group(2)
            if key == "hard":
                current[key] = value == "true"
            else:
                current[key] = value
    for gate in gates.values():
        gate.setdefault("failure_state", "REWORK")
        gate.setdefault("retry_policy", "")
        if gate["failure_state"] not in RESTRICTION:
            raise ValueError(f"unexpected failure_state in registry: {gate['gate_id']}")
    return gates


def retry_budget(gate: dict) -> int:
    """Bounded retry allowance derived from the gate's own declared ``retry_policy``."""
    policy = (gate.get("retry_policy") or "").casefold()
    for token, budget in _BUDGET_RULES:
        if token in policy:
            return budget
    return 0


def decide(classification: dict, gate: dict, attempt: int = 0) -> dict:
    """State-free decision (donor): the caller owns the counter, this only computes.

    The gate's declared ``failure_state`` is the authority floor. A retry is offered only
    when the donor kind is retryable, the gate's own policy allows a bounded correction,
    and the gate is not already more restrictive than REWORK. Fail-closed kinds are never
    retried and always land at HUMAN_REQUIRED or stricter.
    """
    failure_state = gate["failure_state"]
    budget = retry_budget(gate)
    kind = classification["kind"]
    retryable = bool(classification["retryable"]) and kind not in NO_AUTO_RETRY

    if retryable and attempt < budget and RESTRICTION[failure_state] <= RESTRICTION["REWORK"]:
        decision = "RETRY"
    else:
        decision = failure_state

    if kind in NO_AUTO_RETRY:
        decision = most_restrictive(decision, "HUMAN_REQUIRED")

    return {
        "gate_id": gate["gate_id"],
        "kind": kind,
        "retryable": retryable,
        "executor_action": classification["executor_action"],
        "attempt": attempt,
        "retry_budget": budget,
        "declared_failure_state": failure_state,
        "decision": decision,
        "reason": (
            f"{kind} failure at gate {gate['gate_id']}: {decision}"
            + (f" (retry {attempt + 1} of {budget})" if decision == "RETRY" else "")
        ),
    }


def most_restrictive(*decisions: str) -> str:
    """Reuse MPE's existing composition rule: the strictest ceiling wins."""
    unknown = [item for item in decisions if item not in RESTRICTION]
    if unknown:
        raise ValueError(f"decision outside the existing MPE vocabulary: {sorted(unknown)}")
    return max(decisions, key=lambda item: RESTRICTION[item])


def compose(decisions: list[dict]) -> dict:
    """Merge several classified failures into one outcome (donor precedence table)."""
    if not decisions:
        raise ValueError("compose() requires at least one classified failure")
    final = most_restrictive(*(item["decision"] for item in decisions))
    retries = sum(1 for item in decisions if item["decision"] == "RETRY")
    return {
        "decision": final,
        "classified_failures": len(decisions),
        "retryable_failures": retries,
        "kinds": sorted({item["kind"] for item in decisions}),
        "gates": sorted({item["gate_id"] for item in decisions}),
        "authority_source": "gates/registry.yaml failure_state + scripts/dispatch_autonomy most-restrictive rule",
    }
