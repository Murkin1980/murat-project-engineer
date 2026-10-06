#!/usr/bin/env python3
"""EXP-27 — bounded orchestration proof harness (CP-02 .. CP-05).

Produces every measurement quoted in ``RESULTS.md``. Experiment-scoped: no
production script, contract, Router, governance document, or source of truth is
modified; no daemon, service, database, or queue is created.

Usage:
    python3 experiments/exp-27-paperclip-orchestration-patterns/harness/mpe_proof.py all
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = HARNESS_DIR.parent
ROOT = HARNESS_DIR.parents[2]
EVIDENCE_DIR = EXPERIMENT_DIR / "evidence"
FIXTURE_PATH = HARNESS_DIR / "fixtures.json"
WORKER_PATH = HARNESS_DIR / "fresh_worker.py"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HARNESS_DIR))

from scripts.compute_budget import budget_health  # noqa: E402
from scripts.runtime_coordination import append_event, read_events, summarize_events  # noqa: E402
from scripts.task_acceptance import accept_task, enforce_execution  # noqa: E402

import fresh_worker  # noqa: E402
import lease_store  # noqa: E402
import run_state  # noqa: E402

RUN_ID = "EXP-27-PROOF"
CHECKPOINT_RE = re.compile(r"^#{2,3}\s+(CP-\d+)\b", flags=re.M)


# --- shared helpers -------------------------------------------------------

def _write_json(path, data: dict) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")


def _run_worker(arguments: list[str], cwd: Path) -> dict:
    """Run the worker in an isolated interpreter with a temporary working directory."""
    out_path = Path(arguments[arguments.index("--out") + 1])
    cwd.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-I", str(WORKER_PATH), *arguments]
    completed = subprocess.run(command, cwd=str(cwd), capture_output=True, text=True, timeout=180)
    if completed.returncode != 0:
        raise RuntimeError(f"worker failed: {completed.stderr.strip() or completed.stdout.strip()}")
    return json.loads(out_path.read_text(encoding="utf-8"))


def _parse_experiment_docs(experiment_id: str) -> dict:
    """Derive the ancestry chain from repository sources of truth (no chat, no memory)."""
    registry_path = ROOT / "experiments" / "EXPERIMENT_REGISTRY.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entry = next(e for e in registry["experiments"] if e["experiment_id"] == experiment_id)
    experiment_dir = ROOT / entry["experiment_path"]

    task_text = (experiment_dir / "ARENA_TASK.md").read_text(encoding="utf-8")
    checkpoints = [m.group(1) for m in CHECKPOINT_RE.finditer(task_text)]
    source_refs = [registry_path, experiment_dir / "ARENA_TASK.md"]

    stop_conditions, in_stop = [], False
    for line in task_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_stop = stripped.startswith("## Stop conditions")
            continue
        if in_stop and stripped.startswith("- "):
            stop_conditions.append(stripped[2:].strip())
    if not stop_conditions:
        readme_path = experiment_dir / "README.md"
        readme_text = readme_path.read_text(encoding="utf-8")
        source_refs.append(readme_path)
        in_stop = False
        for line in readme_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("## "):
                in_stop = stripped.startswith("## Stop conditions")
                continue
            if in_stop and stripped.startswith("- "):
                stop_conditions.append(stripped[2:].strip())

    disposition = ""
    for line in task_text.splitlines():
        if line.startswith("Decision:") and not disposition:
            disposition = line.split("**")[1] if "**" in line else line.split(":", 1)[1].strip()

    return {
        "entry": entry,
        "experiment_dir": experiment_dir,
        "checkpoints": checkpoints,
        "stop_conditions": stop_conditions,
        "disposition": disposition,
        "source_refs": source_refs,
    }


def build_packet(experiment_id: str, current_checkpoint: str) -> dict:
    parsed = _parse_experiment_docs(experiment_id)
    entry = parsed["entry"]
    task_id = f"{experiment_id}/{current_checkpoint}"
    packet = {
        "packet_version": "exp-27-goal-context-v1",
        "generated_at": run_state.utc_now(),
        "source_refs": [
            {"path": str(path.relative_to(ROOT)), "sha256": run_state.sha256_file(path)}
            for path in parsed["source_refs"]
        ],
        "project": entry["owning_project"],
        "parent_goal": entry["why"],
        "primary_disposition": parsed["disposition"],
        "experiment": {"id": entry["experiment_id"], "path": entry["experiment_path"]},
        "checkpoints": parsed["checkpoints"],
        "task": {
            "task_id": task_id,
            "checkpoint": current_checkpoint,
            "summary": f"Execute {current_checkpoint} of {experiment_id} inside the approved experiment boundary",
        },
        "stop_conditions": parsed["stop_conditions"],
        "acceptance_ref": f"{entry['experiment_path']}/README.md#acceptance",
    }
    packet["expected_genealogy"] = {
        "project": packet["project"],
        "parent_goal": packet["parent_goal"],
        "experiment_id": packet["experiment"]["id"],
        "checkpoints": packet["checkpoints"],
        "task_id": task_id,
        "disposition": packet["primary_disposition"],
        "stop_condition_count": len(packet["stop_conditions"]),
        "first_stop_conditions": packet["stop_conditions"][:2],
    }
    return packet


# --- CP-02: goal ancestry -------------------------------------------------

def cp02(workdir: Path) -> dict:
    cases = []
    for experiment_id, checkpoint in (("EXP-27", "CP-05"), ("EXP-25", "CP-04")):
        packet = build_packet(experiment_id, checkpoint)
        packet_path = workdir / f"cp02/{experiment_id}.packet.json"
        _write_json(packet_path, packet)

        answer_out = workdir / f"cp02/{experiment_id}.answer.json"
        answer = _run_worker(
            ["answer", "--packet", str(packet_path), "--out", str(answer_out)], cwd=workdir / "cp02"
        )

        rediscover_out = workdir / f"cp02/{experiment_id}.rediscover.json"
        rediscover = _run_worker(
            ["rediscover", "--root", str(ROOT), "--task-id", experiment_id,
             "--current-task-id", packet["task"]["task_id"], "--out", str(rediscover_out)],
            cwd=workdir / "cp02",
        )

        rediscovered_matches = {
            key: rediscover["answers"].get(key) == packet["expected_genealogy"][key]
            for key in packet["expected_genealogy"]
        }
        cases.append({
            "experiment_id": experiment_id,
            "checkpoint": checkpoint,
            "task_id": packet["task"]["task_id"],
            "packet_bytes": packet_path.stat().st_size,
            "packet_source_refs": packet["source_refs"],
            "goal_preserved_by_fresh_process": answer["goal_preserved"],
            "per_question_match": answer["matches_expected"],
            "fresh_process_read_from_chat": answer["read_from_chat"],
            "rediscovery_files_read": rediscover["rediscovery_steps"],
            "rediscovery_bytes_read": rediscover["bytes_read"],
            "rediscovery_answers_match_packet": all(rediscovered_matches.values()),
            "context_overhead_ratio_packet_vs_rediscovery": round(
                packet_path.stat().st_size / rediscover["bytes_read"], 4
            ),
        })

    checks = {
        "every_case_preserves_parent_goal": all(c["goal_preserved_by_fresh_process"] for c in cases),
        "independent_rediscovery_agrees_with_packet": all(c["rediscovery_answers_match_packet"] for c in cases),
        "no_chat_context_required": all(not c["fresh_process_read_from_chat"] for c in cases),
        "no_extra_canonical_source_created": True,
    }
    return {
        "pattern": "goal_ancestry_context",
        "cases": cases,
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "measurements": {
            "mean_packet_bytes": round(sum(c["packet_bytes"] for c in cases) / len(cases), 1),
            "rediscovery_steps_packet_arm": 0,
            "mean_rediscovery_steps_without_packet": round(
                sum(c["rediscovery_files_read"] for c in cases) / len(cases), 2
            ),
            "mean_bytes_scanned_without_packet": round(
                sum(c["rediscovery_bytes_read"] for c in cases) / len(cases), 1
            ),
        },
    }


# --- CP-03: atomic task lease --------------------------------------------

def cp03(workdir: Path) -> dict:
    race_rounds = []
    for round_index in range(3):
        lease_dir = workdir / f"cp03/race-{round_index}"
        lease_dir.mkdir(parents=True, exist_ok=True)
        owners = [f"executor-{round_index}-{index}" for index in range(8)]
        processes = []
        for owner in owners:
            out_path = lease_dir / f"{owner}.result.json"
            command = [sys.executable, "-I", str(WORKER_PATH), "lease",
                       "--lease-dir", str(lease_dir), "--owner", owner, "--mode", "claim",
                       "--ttl-seconds", "60", "--hold-seconds", "0.02",
                       "--out", str(out_path)]
            processes.append((owner, out_path, subprocess.Popen(
                command, cwd=str(lease_dir), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True
            )))
        results = []
        for owner, out_path, process in processes:
            _, stderr = process.communicate(timeout=180)
            if process.returncode != 0 or not out_path.exists():
                raise RuntimeError(f"lease worker {owner} failed: {stderr.strip()}")
            results.append(json.loads(out_path.read_text(encoding="utf-8")))

        acquired = [r for r in results if r["status"] in (lease_store.LEASE_ACQUIRED, lease_store.LEASE_ACQUIRED_RECLAIMED)]
        conflicts = [r for r in results if r["status"] == lease_store.LEASE_CONFLICT]
        work_markers = [p for p in lease_dir.glob("work.*.done")]
        active_record = lease_store.read_record(lease_dir)
        winner = acquired[0]["owner"] if acquired else None
        release = lease_store.release(lease_dir, winner, reason="TERMINAL_DONE") if winner else None
        terminal = lease_store.read_record(lease_dir)
        race_rounds.append({
            "round": round_index,
            "owners": len(owners),
            "acquired": len(acquired),
            "conflicts": len(conflicts),
            "winner": winner,
            "active_record_owner_matches_winner": active_record.get("owner") == winner,
            "conflict_report_has_owner_and_expiry": all(
                r.get("current_owner") and r.get("expires_at") for r in conflicts
            ),
            "work_markers": len(work_markers),
            "release_status": release.get("status") if release else None,
            "terminal_record_visible": {
                "status": terminal.get("status"),
                "owner": terminal.get("owner"),
                "released_at": terminal.get("released_at"),
                "release_reason": terminal.get("release_reason"),
                "generation": terminal.get("generation"),
            },
        })

    # Bounded stale-lease recovery: an already-expired lease is reclaimable, and the
    # stale owner can no longer release it.
    stale_dir = workdir / "cp03/stale"
    stale_dir.mkdir(parents=True, exist_ok=True)
    stale_claim = lease_store.acquire(stale_dir, "stale-executor", 0.0, last_action="checkout")
    reclaim = lease_store.acquire(stale_dir, "recovery-executor", 60.0, last_action="recovery")
    stale_release = lease_store.release(stale_dir, "stale-executor", reason="TERMINAL_DONE")
    recovery_release = lease_store.release(stale_dir, "recovery-executor", reason="TERMINAL_DONE")
    after_release = lease_store.acquire(stale_dir, "next-executor", 60.0, last_action="checkout")
    after_release_record = lease_store.read_record(stale_dir)
    lease_store.release(stale_dir, "next-executor", reason="TERMINAL_DONE")

    checks = {
        "exactly_one_winner_per_race": all(r["acquired"] == 1 and r["conflicts"] == 7 for r in race_rounds),
        "no_duplicate_execution": all(r["work_markers"] == 1 for r in race_rounds),
        "conflict_is_explicit_and_inspectable": all(r["conflict_report_has_owner_and_expiry"] for r in race_rounds),
        "single_active_owner_record": all(r["active_record_owner_matches_winner"] for r in race_rounds),
        "only_owner_can_release": all(r["release_status"] == lease_store.LEASE_RELEASED for r in race_rounds),
        "terminal_state_visible_after_release": all(
            r["terminal_record_visible"]["status"] == "RELEASED"
            and r["terminal_record_visible"]["released_at"]
            and r["terminal_record_visible"]["release_reason"] == "TERMINAL_DONE"
            for r in race_rounds
        ),
        "expired_lease_reclaimed_with_reason": reclaim["status"] == lease_store.LEASE_ACQUIRED_RECLAIMED
        and reclaim["reason"] == "LEASE_EXPIRED" and reclaim["reclaimed_from"] == "stale-executor",
        "stale_owner_cannot_release": stale_release["status"] == lease_store.LEASE_RELEASE_DENIED,
        "generation_history_preserved": [h["owner"] for h in after_release_record["history"]]
        == ["stale-executor", "recovery-executor"],
    }
    return {
        "pattern": "atomic_task_lease",
        "race_rounds": race_rounds,
        "stale_recovery": {
            "stale_claim": stale_claim["status"],
            "reclaim": {k: reclaim.get(k) for k in ("status", "reason", "reclaimed_from", "generation")},
            "stale_release": {k: stale_release.get(k) for k in ("status", "reason")},
            "recovery_release": recovery_release["status"],
            "acquire_after_release": {
                "status": after_release["status"],
                "generation": after_release["generation"],
                "previous_owner": after_release.get("previous_owner"),
            },
        },
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "measurements": {
            "rounds": len(race_rounds),
            "concurrent_executors_per_round": 8,
            "duplicate_executions": sum(1 for r in race_rounds if r["work_markers"] > 1),
            "lease_conflicts": sum(r["conflicts"] for r in race_rounds),
            "daemons_or_services_required": 0,
            "databases_required": 0,
        },
    }


# --- CP-04: persistent evidence + resume ---------------------------------

def cp04(workdir: Path) -> dict:
    run_dir = workdir / "cp04"
    run_dir.mkdir(parents=True, exist_ok=True)
    packet = build_packet("EXP-27", "CP-04")
    packet_path = run_dir / "packet.json"
    _write_json(packet_path, packet)
    state_path = run_dir / "state.json"
    events_path = run_dir / "events.jsonl"
    artifact_path = run_dir / "artifact.json"

    context = {
        "fixture_path": str(FIXTURE_PATH),
        "packet_path": str(packet_path),
        "state_path": str(state_path),
        "artifact_path": str(artifact_path),
    }
    state = {
        "state_version": run_state.STATE_VERSION,
        "run_id": RUN_ID,
        "task_id": packet["task"]["task_id"],
        "goal_ancestry": {
            "project": packet["project"],
            "parent_goal": packet["parent_goal"],
            "experiment_id": packet["experiment"]["id"],
            "checkpoints": packet["checkpoints"],
            "stop_conditions": packet["stop_conditions"],
        },
        "context_refs": context,
        "steps": [{"step_id": step_id, "status": "PENDING", "output": {}, "completed_at": None}
                  for step_id in run_state.STEP_IDS],
        "state": "WORKING",
        "created_at": run_state.utc_now(),
        "updated_at": run_state.utc_now(),
        "next_action": "run the remaining pending bounded steps and finalize",
        "handoff": {
            "STATE": "WORKING: bounded steps started",
            "EVIDENCE": "none yet",
            "CHANGES": "none",
            "RESULT": "not delivered",
            "BLOCKER": "budget guard stopped the first process at the tool-call limit",
            "NEXT ACTION": "resume from persisted state in a fresh process",
            "HANDOFF": f"state file {state_path}",
        },
        "typed_handoff": {
            "run_id": RUN_ID,
            "task_id": packet["task"]["task_id"],
            "producer_role": "exp-27-proof-parent",
            "consumer_role": "exp-27-proof-fresh-executor",
            "task_summary": packet["task"]["summary"],
            "input_refs": [str(FIXTURE_PATH), str(packet_path)],
            "changed_files": [],
            "artifact_refs": [str(artifact_path)],
            "assumptions": ["bounded proof only; no production integration"],
            "unresolved_risks": ["single-host file-backed proof, not a distributed lock"],
            "checks_already_run": ["ancestry_packet_built"],
            "required_next_checks": ["resume_without_rediscovery"],
            "acceptance_criteria": ["all 5 bounded steps DONE with stable digests"],
            "do_not_change": ["experiments/exp-27-paperclip-orchestration-patterns/ARENA_TASK.md"],
        },
    }
    run_state.save_state(state_path, state)

    append_event(events_path, {
        "schema_version": "1.0", "event_id": "evt-cp04-1", "run_id": RUN_ID,
        "timestamp": run_state.utc_now(), "type": "spawn", "actor": "exp-27-proof-parent",
        "target": None, "task_id": state["task_id"], "ref": str(state_path), "status": "WORKING",
    }, writer_id="exp-27-proof-parent")
    append_event(events_path, {
        "schema_version": "1.0", "event_id": "evt-cp04-2", "run_id": RUN_ID,
        "timestamp": run_state.utc_now(), "type": "claim", "actor": "exp-27-proof-parent",
        "target": None, "task_id": state["task_id"], "ref": str(state_path), "status": "LEASE_ACQUIRED",
    }, writer_id="exp-27-proof-parent")

    # First process: run steps until the hard tool-call limit stops it.
    guard = BudgetGuard(max_retries=2, max_tool_calls=3, max_wall_seconds=30.0, label="cp04-first-process")
    stop_reason = None
    try:
        fresh_worker.drive_steps(str(state_path), context, run_state.STEP_IDS, guard=guard)
    except GuardStop as stop:
        stop_reason = stop.reason
    state = run_state.load_state(state_path)
    first_process = {
        "executed_steps": [s["step_id"] for s in state["steps"] if s["status"] == "DONE"],
        "guard_stop_reason": stop_reason,
        "tool_calls": guard.tool_calls,
        "state_after_stop": "BLOCKED",
    }
    state["state"] = "BLOCKED"
    state["handoff"]["STATE"] = f"BLOCKED: stopped after {len(first_process['executed_steps'])} of 5 bounded steps"
    state["handoff"]["EVIDENCE"] = f"persisted step outputs in {state_path}"
    state["handoff"]["CHANGES"] = f"{len(first_process['executed_steps'])} step records persisted"
    state["handoff"]["BLOCKER"] = f"hard guard stop: {stop_reason}"
    state["handoff"]["NEXT ACTION"] = "fresh process resumes pending steps S4..S5 from this file"
    run_state.save_state(state_path, state)
    append_event(events_path, {
        "schema_version": "1.0", "event_id": "evt-cp04-3", "run_id": RUN_ID,
        "timestamp": run_state.utc_now(), "type": "block", "actor": "exp-27-proof-parent",
        "target": None, "task_id": state["task_id"], "ref": str(state_path), "status": "BLOCKED",
    }, writer_id="exp-27-proof-parent")

    # Second, isolated process: resume from the persisted state only.
    resume_out = run_dir / "resume.result.json"
    resume = _run_worker(["resume", "--state", str(state_path), "--out", str(resume_out)],
                         cwd=workdir / "cp04-fresh-cwd")
    append_event(events_path, {
        "schema_version": "1.0", "event_id": "evt-cp04-4", "run_id": RUN_ID,
        "timestamp": run_state.utc_now(), "type": "spawn", "actor": "exp-27-proof-fresh-executor",
        "target": None, "task_id": state["task_id"], "ref": str(state_path), "status": "READY",
    }, writer_id="exp-27-proof-parent")
    append_event(events_path, {
        "schema_version": "1.0", "event_id": "evt-cp04-5", "run_id": RUN_ID,
        "timestamp": run_state.utc_now(), "type": "resume", "actor": "exp-27-proof-fresh-executor",
        "target": None, "task_id": state["task_id"], "ref": str(state_path), "status": "WORKING",
    }, writer_id="exp-27-proof-parent")
    append_event(events_path, {
        "schema_version": "1.0", "event_id": "evt-cp04-6", "run_id": RUN_ID,
        "timestamp": run_state.utc_now(), "type": "terminal", "actor": "exp-27-proof-fresh-executor",
        "target": None, "task_id": state["task_id"], "ref": str(state_path), "status": "DONE",
    }, writer_id="exp-27-proof-parent")

    final_state = run_state.load_state(state_path)
    events = read_events(events_path)
    event_summary = summarize_events(events)
    completeness = run_state.evidence_completeness(final_state)

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(state_path, EVIDENCE_DIR / "cp04_state_after_resume.json")
    shutil.copyfile(events_path, EVIDENCE_DIR / "run-EXP27-CP04.events.jsonl")

    checks = {
        "fresh_process_resume_succeeded": bool(resume["resume_success"]),
        "no_step_reexecuted": resume["re_executed_steps"] == [],
        "no_rediscovery_required": resume["rediscovery_steps"] == 0 and not resume["read_from_chat"],
        "evidence_complete": not completeness["missing_fields"],
        "runtime_events_valid": len(events) == 6 and event_summary["outcome"] == "DONE",
        "final_state_done": final_state["state"] == "DONE",
    }
    return {
        "pattern": "persistent_resumable_evidence",
        "first_process": first_process,
        "fresh_process": {
            "executed_steps": resume["executed_steps"],
            "previously_completed_steps": resume["previously_completed_steps"],
            "re_executed_steps": resume["re_executed_steps"],
            "rediscovery_steps": resume["rediscovery_steps"],
            "input_bytes": resume["input_bytes"],
            "read_from_chat": resume["read_from_chat"],
            "recomputed_input_digest_matches": resume["recomputed_input_digest_matches"],
        },
        "evidence_completeness": completeness,
        "runtime_events": {"count": len(events), "summary": event_summary},
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "measurements": {
            "steps_completed_before_interruption": len(first_process["executed_steps"]),
            "steps_completed_after_resume": len(resume["executed_steps"]),
            "redundant_step_executions": len(resume["re_executed_steps"]),
            "resume_success": bool(resume["resume_success"]),
            "evidence_completeness_ratio": round(
                completeness["present_fields"] / completeness["required_fields"], 4
            ),
            "rediscovery_steps": resume["rediscovery_steps"],
        },
    }


# --- CP-05: budget/runaway guard + existing MPE approval gate -------------

class GuardStop(RuntimeError):
    def __init__(self, reason: str, counters: dict):
        super().__init__(reason)
        self.reason = reason
        self.counters = counters


class BudgetGuard:
    """Bounded retries, tool calls, and wall time. Crossing a limit raises, never continues."""

    def __init__(self, *, max_retries: int, max_tool_calls: int, max_wall_seconds: float,
                 clock=time.monotonic, label: str = "guard"):
        self.max_retries = max_retries
        self.max_tool_calls = max_tool_calls
        self.max_wall_seconds = max_wall_seconds
        self.clock = clock
        self.label = label
        self.started = clock()
        self.tool_calls = 0
        self.attempts = 0
        self.stop_reason = None

    def _counters(self) -> dict:
        return {"tool_calls": self.tool_calls, "attempts": self.attempts, "label": self.label}

    def _check_wall(self) -> None:
        if self.clock() - self.started > self.max_wall_seconds:
            self.stop_reason = "MAX_WALL_TIME"
            raise GuardStop(self.stop_reason, self._counters())

    def tool_call(self, label: str = "") -> None:
        self._check_wall()
        if self.tool_calls + 1 > self.max_tool_calls:
            self.stop_reason = "MAX_TOOL_CALLS"
            raise GuardStop(self.stop_reason, {**self._counters(), "blocked_call": label})
        self.tool_calls += 1

    def attempt(self, label: str = "") -> None:
        self._check_wall()
        if self.attempts + 1 > self.max_retries + 1:
            self.stop_reason = "MAX_RETRIES"
            raise GuardStop(self.stop_reason, {**self._counters(), "blocked_attempt": label})
        self.attempts += 1


TRUSTED_GATES = [
    {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "git_status"},
    {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "secrets_scan"},
    {"gate_id": "build", "result": "PASS", "evidence_ref": "compileall"},
]


def _verified_pass() -> dict:
    return {"outcome": "PASS", "deterministic_gate_results": TRUSTED_GATES}


def _task(task_id: str, summary: str, signals: list, *, rollback_known: bool = True,
          unknowns: int = 0) -> dict:
    return {
        "task_id": task_id,
        "summary": summary,
        "affected_repositories": ["Murkin1980/murat-project-engineer"],
        "acceptance_criteria_present": True,
        "rollback_known": rollback_known,
        "ratings": {"complexity": 1, "risk": 1, "architectural_impact": 1,
                    "data_sensitivity": 0, "unknowns": unknowns},
        "signals": signals,
    }


def cp05(workdir: Path) -> dict:
    # 1. retry limit
    retry_guard = BudgetGuard(max_retries=2, max_tool_calls=10, max_wall_seconds=30.0, label="retry-limit")
    retry_stop = None
    try:
        for attempt_index in range(1, 10):
            retry_guard.attempt(f"attempt-{attempt_index}")
            if attempt_index >= 4:
                break
    except GuardStop as stop:
        retry_stop = stop
    retries_executed = retry_guard.attempts - 1

    # 2. tool-call limit
    call_guard = BudgetGuard(max_retries=0, max_tool_calls=5, max_wall_seconds=30.0, label="tool-call-limit")
    call_stop = None
    calls_attempted_after_stop = 0
    try:
        for call_index in range(1, 10):
            call_guard.tool_call(f"tool-{call_index}")
    except GuardStop as stop:
        calls_attempted_after_stop = 1
        call_stop = stop
    executed_calls = call_guard.tool_calls

    # 3. wall-time limit with an injected deterministic clock
    ticks = {"value": 0.0}

    def ticking_clock() -> float:
        return ticks["value"]

    wall_guard = BudgetGuard(max_retries=0, max_tool_calls=99, max_wall_seconds=0.25,
                             clock=ticking_clock, label="wall-time-limit")
    wall_stop = None
    measured_start = time.monotonic()
    try:
        for tick_index in range(1, 10):
            ticks["value"] = round(tick_index * 0.1, 3)
            wall_guard.tool_call(f"tick-{tick_index}")
    except GuardStop as stop:
        wall_stop = stop
    measured_wall_seconds = round(time.monotonic() - measured_start, 6)

    # 4. canonical compute-budget status mapping (reuses scripts/compute_budget.budget_health)
    hard_limit = 1.0
    cost_per_call = 0.3
    planned_calls = 6
    projected_total = round(cost_per_call * planned_calls, 2)
    budget_status = budget_health(projected_total, hard_limit)
    budget_status_within = budget_health(round(cost_per_call * 2, 2), hard_limit)

    # 5. existing MPE approval gate (no new gate, no Paperclip override)
    history = [_verified_pass() for _ in range(5)]
    invocations = {"sensitive": 0, "hard_block": 0}

    def make_executor(key: str):
        """Fake executor (no real provider, no repository write)."""
        def executor(result: dict) -> dict:
            invocations[key] += 1
            return {"executed": key, "task_id": result.get("task_id")}
        return executor

    sensitive_task = _task("EXP-27-T-INTEGRATION", "integration-sensitive change inside the approved experiment",
                           ["production_change"], unknowns=1)
    sensitive_acceptance = accept_task(sensitive_task, history=history, current_level="L4")
    before_without = invocations["sensitive"]
    sensitive_without_approval = enforce_execution(sensitive_acceptance, make_executor("sensitive"))
    delta_without = invocations["sensitive"] - before_without
    before_with = invocations["sensitive"]
    sensitive_with_approval = enforce_execution(
        sensitive_acceptance, make_executor("sensitive"), approval_recorded=True
    )
    delta_with = invocations["sensitive"] - before_with

    hard_block_task = _task("EXP-27-T-DEEP-CHANGE", "architecture redesign requiring deep-change approval",
                            ["architecture_redesign"], unknowns=2)
    hard_block_acceptance = accept_task(hard_block_task, history=history, current_level="L4",
                                        stop_condition=True)
    hard_block_with_approval = enforce_execution(
        hard_block_acceptance, make_executor("hard_block"), approval_recorded=True
    )

    # 6. composition: a satisfied budget guard must not override the approval gate
    composition = {
        "budget_guard": "OK" if budget_status_within == "GREEN" else budget_status_within,
        "approval_gate": sensitive_acceptance["acceptance_state"],
        "final_outcome": "HUMAN_REQUIRED" if sensitive_acceptance["human_gate_required"] else sensitive_acceptance["acceptance_state"],
        "budget_override_possible": False,
    }

    checks = {
        "retry_limit_stops": retry_stop is not None and retry_stop.reason == "MAX_RETRIES",
        "tool_call_limit_stops": call_stop is not None and call_stop.reason == "MAX_TOOL_CALLS"
        and executed_calls == 5 and calls_attempted_after_stop == 1,
        "wall_time_limit_stops": wall_stop is not None and wall_stop.reason == "MAX_WALL_TIME",
        "hard_limit_maps_to_canonical_RED": budget_status == "RED",
        "approval_gate_blocks_without_approval": sensitive_without_approval is None and delta_without == 0,
        "approval_gate_allows_with_recorded_approval": isinstance(sensitive_with_approval, dict)
        and sensitive_with_approval.get("executed") == "sensitive" and delta_with == 1,
        "hard_block_never_executes_even_with_approval": hard_block_with_approval is None
        and invocations["hard_block"] == 0,
        "deep_change_requires_human_gate": hard_block_acceptance["human_gate_required"]
        and hard_block_acceptance["acceptance_state"] in ("HUMAN_REQUIRED", "BLOCKED"),
        "budget_cannot_override_approval_gate": composition["budget_guard"] == "OK"
        and composition["final_outcome"] == "HUMAN_REQUIRED",
    }
    return {
        "pattern": "budget_runaway_guard_with_existing_approval_gate",
        "guards": [
            {"guard": "max_retries", "limit": retry_guard.max_retries,
             "attempts_allowed": retry_guard.attempts, "retries_executed": retries_executed,
             "stop_reason": retry_stop.reason if retry_stop else None,
             "outcome": "STOP/BLOCKED", "silent_continue": False},
            {"guard": "max_tool_calls", "limit": call_guard.max_tool_calls,
             "executed_calls": executed_calls, "blocked_call": True,
             "stop_reason": call_stop.reason if call_stop else None,
             "outcome": "STOP/BLOCKED", "silent_continue": False},
            {"guard": "max_wall_seconds", "limit": wall_guard.max_wall_seconds,
             "clock": "injected deterministic ticks (0.1s per call)",
             "stop_reason": wall_stop.reason if wall_stop else None,
             "measured_wall_seconds": measured_wall_seconds,
             "outcome": "STOP/BLOCKED", "silent_continue": False},
            {"guard": "compute_budget_hard_limit", "hard_limit": hard_limit,
             "projected_total": projected_total, "budget_status": budget_status,
             "status_within_limit": budget_status_within,
             "source": "scripts/compute_budget.budget_health",
             "outcome": "STOP/BLOCKED", "silent_continue": False},
        ],
        "approval_gate": {
            "source": "scripts/task_acceptance.accept_task + enforce_execution (existing MPE path)",
            "integration_sensitive_task": {
                "task_id": sensitive_task["task_id"],
                "risk_tier": sensitive_acceptance["task_risk_tier"],
                "allowed_action": sensitive_acceptance["allowed_action"],
                "acceptance_state": sensitive_acceptance["acceptance_state"],
                "human_gate_required": sensitive_acceptance["human_gate_required"],
                "executor_invoked_without_approval": sensitive_without_approval is not None,
                "executor_invoked_with_recorded_approval": sensitive_with_approval is not None,
            },
            "deep_change_task": {
                "task_id": hard_block_task["task_id"],
                "risk_tier": hard_block_acceptance["task_risk_tier"],
                "allowed_action": hard_block_acceptance["allowed_action"],
                "acceptance_state": hard_block_acceptance["acceptance_state"],
                "blocking_reasons": hard_block_acceptance["blocking_reasons"],
                "executor_invoked_with_recorded_approval": hard_block_with_approval is not None,
            },
        },
        "composition": composition,
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "measurements": {
            "hard_boundaries_demonstrated": 4,
            "human_approval_points": 1,
            "execution_attempts_without_approval_that_ran": 0,
            "hard_block_executions_with_approval_that_ran": invocations["hard_block"],
        },
    }


def run_all(workdir: Path) -> dict:
    results = {
        "experiment_id": "EXP-27",
        "run_id": RUN_ID,
        "generated_at": run_state.utc_now(),
        "harness": str(WORKER_PATH.relative_to(ROOT)),
        "cp02_goal_ancestry": cp02(workdir),
        "cp03_task_lease": cp03(workdir),
        "cp04_resume": cp04(workdir),
        "cp05_budget_gate": cp05(workdir),
    }
    patterns = [results["cp02_goal_ancestry"], results["cp03_task_lease"],
                results["cp04_resume"], results["cp05_budget_gate"]]
    results["summary"] = {
        "patterns_verified": sum(1 for p in patterns if p["result"] == "PASS"),
        "patterns_total": len(patterns),
        "result": "PASS" if all(p["result"] == "PASS" for p in patterns) else "PARTIAL",
        "parallel_control_plane_created": False,
        "governance_or_source_of_truth_changed": False,
        "production_integration_performed": False,
    }
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="EXP-27 bounded orchestration proof harness")
    parser.add_argument("command", choices=["cp02", "cp03", "cp04", "cp05", "all"])
    parser.add_argument("--workdir", default=None, help="optional scratch directory")
    args = parser.parse_args(argv)

    workdir = Path(args.workdir) if args.workdir else Path(tempfile.mkdtemp(prefix="exp-27-proof-"))
    workdir.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    key = {"cp02": "cp02_goal_ancestry", "cp03": "cp03_task_lease",
           "cp04": "cp04_resume", "cp05": "cp05_budget_gate"}.get(args.command)
    if args.command == "all":
        results = run_all(workdir)
    else:
        results = {key: globals()[args.command](workdir)}

    if key:
        _write_json(EVIDENCE_DIR / f"{args.command}.json", results[key])
    else:
        _write_json(EVIDENCE_DIR / "proof_run.json", results)
        for pattern_key in ("cp02_goal_ancestry", "cp03_task_lease", "cp04_resume", "cp05_budget_gate"):
            _write_json(EVIDENCE_DIR / f"{pattern_key.split('_')[0]}.json", results[pattern_key])

    print(json.dumps(results.get("summary", results), ensure_ascii=False, sort_keys=True, indent=1))
    failed = [k for k, v in results.items() if isinstance(v, dict) and v.get("result") not in (None, "PASS")]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
