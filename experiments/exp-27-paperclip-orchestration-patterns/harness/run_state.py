"""EXP-27 CP-04 — persistent, resumable run state on the existing MPE handoff contract.

Experiment-scoped proof only; it adds no storage service and does not replace the
repository as source of truth. The persisted record reuses:

- the MPE graceful-handoff fields (AGENTS.md / docs/GLOBAL_MPE_ENFORCEMENT.md):
  STATE, EVIDENCE, CHANGES, RESULT, BLOCKER, NEXT ACTION, HANDOFF;
- the typed handoff contract in ``contracts/HANDOFF.md``;
- ``contracts/AGENT_RUNTIME_STATE.schema.json`` lifecycle vocabulary for ``state``.

Nothing here is imported by production scripts.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STATE_VERSION = "exp-27-run-state-v1"

# contracts/AGENT_RUNTIME_STATE.schema.json lifecycle vocabulary.
LIFECYCLE_STATES = {"CREATED", "READY", "WORKING", "BLOCKED", "WAITING", "REVIEWING", "DONE", "FAILED", "CANCELLED"}

# MPE graceful-handoff minimum contract (AGENTS.md) — labels kept verbatim.
GRACEFUL_HANDOFF_FIELDS = ("STATE", "EVIDENCE", "CHANGES", "RESULT", "BLOCKER", "NEXT ACTION", "HANDOFF")

# contracts/HANDOFF.md typed handoff fields.
TYPED_HANDOFF_FIELDS = (
    "run_id", "task_id", "producer_role", "consumer_role", "task_summary", "input_refs",
    "changed_files", "artifact_refs", "assumptions", "unresolved_risks", "checks_already_run",
    "required_next_checks", "acceptance_criteria", "do_not_change",
)

STEP_IDS = ("S1_input_digest", "S2_goal_binding", "S3_artifact_write", "S4_artifact_verify", "S5_finalize")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def save_state(path, state: dict) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".state-", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(state, stream, ensure_ascii=False, sort_keys=True, indent=1)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, target)
    except BaseException:
        Path(temp_name).unlink(missing_ok=True)
        raise


def load_state(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evidence_completeness(state: dict) -> dict:
    """A field counts as present when it exists and is not None/empty-string.

    An explicitly empty list (for example ``changed_files`` on a proof that changed
    no production file) is a deliberate statement, not a missing field.
    """
    handoff = state.get("handoff", {})
    typed = state.get("typed_handoff", {})
    missing = [f for f in GRACEFUL_HANDOFF_FIELDS if handoff.get(f) in (None, "")]
    missing += [f"typed_handoff.{f}" for f in TYPED_HANDOFF_FIELDS if f not in typed or typed.get(f) in (None, "")]
    required = len(GRACEFUL_HANDOFF_FIELDS) + len(TYPED_HANDOFF_FIELDS)
    return {"required_fields": required, "present_fields": required - len(missing), "missing_fields": missing}


# --- deterministic bounded task steps -------------------------------------

def _read_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def step_input_digest(context: dict) -> dict:
    fixture = _read_json(context["fixture_path"])
    payload = fixture["task_input"].encode("utf-8")
    return {"input_digest": sha256_bytes(payload), "fixture_ref": str(context["fixture_path"]),
            "fixture_version": fixture.get("fixture_version")}


def step_goal_binding(context: dict) -> dict:
    packet = _read_json(context["packet_path"])
    return {"project": packet["project"], "parent_goal": packet["parent_goal"],
            "experiment_id": packet["experiment"]["id"], "task_id": packet["task"]["task_id"],
            "packet_sha256": sha256_file(context["packet_path"])}


def step_artifact_write(context: dict) -> dict:
    state = load_state(context["state_path"])
    outputs = {step["step_id"]: step.get("output", {}) for step in state["steps"]}
    artifact = {
        "artifact_version": "exp-27-proof-artifact-v1",
        "run_id": state["run_id"],
        "task_id": state["task_id"],
        "input_digest": outputs["S1_input_digest"]["input_digest"],
        "goal_binding": outputs["S2_goal_binding"],
    }
    path = Path(context["artifact_path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")
    return {"artifact_path": str(path), "artifact_digest": sha256_file(path)}


def step_artifact_verify(context: dict) -> dict:
    state = load_state(context["state_path"])
    outputs = {step["step_id"]: step.get("output", {}) for step in state["steps"]}
    expected = outputs["S3_artifact_write"]["artifact_digest"]
    actual = sha256_file(outputs["S3_artifact_write"]["artifact_path"])
    return {"artifact_verified": actual == expected, "verified_digest": actual}


def step_finalize(context: dict) -> dict:
    state = load_state(context["state_path"])
    outputs = {step["step_id"]: step.get("output", {}) for step in state["steps"]}
    result_payload = json.dumps(
        {step_id: outputs.get(step_id, {}) for step_id in STEP_IDS[:4] if step_id in outputs},
        ensure_ascii=False, sort_keys=True,
    ).encode("utf-8")
    return {"result_digest": sha256_bytes(result_payload), "terminal": "DONE"}


_STEP_FUNCTIONS = {
    "S1_input_digest": step_input_digest,
    "S2_goal_binding": step_goal_binding,
    "S3_artifact_write": step_artifact_write,
    "S4_artifact_verify": step_artifact_verify,
    "S5_finalize": step_finalize,
}


def execute_steps(step_ids, context: dict) -> list[dict]:
    """Run only the requested steps; each step re-reads persisted state."""
    executed = []
    for step_id in step_ids:
        output = _STEP_FUNCTIONS[step_id](context)
        executed.append({"step_id": step_id, "output": output})
    return executed
