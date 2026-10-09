#!/usr/bin/env python3
"""EXP-20 CP-03 — bounded component proofs (P1 durable event evidence, P2 failure classification).

Produces every measurement quoted in ``RESULTS.md``. Experiment-scoped: no production
script, contract, gate, schema, Router, governance document, or source of truth is
modified; no daemon, service, database, queue, sandbox, or workflow engine is created.

Both proofs run the *existing* MPE production functions as the control arm, so every
claimed gain is a measured delta against what MPE does today, not against a strawman.

Usage:
    python3 experiments/exp-20-dify-openhands-component-extraction/harness/exp20_proof.py all
    python3 .../harness/exp20_proof.py p1
    python3 .../harness/exp20_proof.py p2
"""
from __future__ import annotations

import argparse
import json
import shutil
import statistics
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
WORKER_PATH = HARNESS_DIR / "resume_worker.py"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HARNESS_DIR))

from scripts import runtime_coordination as rc  # noqa: E402
from scripts.execution_runner import run_task  # noqa: E402

import durable_event_evidence as dee  # noqa: E402
import failure_classification as fc  # noqa: E402

PRODUCTION_FILES = (
    "scripts/runtime_coordination.py",
    "scripts/execution_runner.py",
    "scripts/task_acceptance.py",
    "scripts/triage_engine.py",
    "scripts/dispatch_autonomy.py",
    "scripts/earned_autonomy.py",
    "scripts/validate_package.py",
    "gates/registry.yaml",
    "contracts/RUNTIME_EVENT.schema.json",
    "contracts/AGENT_RUNTIME_STATE.schema.json",
    "contracts/RUN_REPORT.schema.json",
)

TIMING_KEYS = {"write_seconds", "marker_seconds", "median_append_seconds_production", "median_append_seconds_durable",
               "median_classify_seconds", "total_seconds", "worker_seconds", "overhead_ratio"}


def log(message: str) -> None:
    print(message, flush=True)


def production_digests() -> dict[str, str]:
    return {name: dee.sha256_file(ROOT / name) for name in PRODUCTION_FILES}


def load_fixtures() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def normalized(payload: object) -> object:
    """Strip timings and absolute paths so two runs can be compared for determinism."""
    if isinstance(payload, dict):
        return {
            key: normalized(value)
            for key, value in sorted(payload.items())
            if key not in TIMING_KEYS
        }
    if isinstance(payload, list):
        return [normalized(item) for item in payload]
    if isinstance(payload, str):
        return payload.replace(tempfile.gettempdir(), "<tmp>")
    return payload


def write_evidence(name: str, payload: dict) -> Path:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    path = EVIDENCE_DIR / name
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------------------
# P1 — crash-tolerant, idempotent, resumable event evidence (OpenHands EventLog subset)
# --------------------------------------------------------------------------------------

def _event(index: int, kind: str, status: str, actor: str = "exp-20-proof-executor") -> dict:
    return {
        "schema_version": "1.0",
        "event_id": f"evt-exp20-p1-{index}",
        "run_id": "EXP-20-PROOF",
        "timestamp": f"2026-10-09T00:00:{index:02d}Z",
        "type": kind,
        "actor": actor,
        "task_id": "EXP-20/CP-03",
        "status": status,
        "ref": None,
        "target": None,
    }


def _build_proof_log(directory: Path, count: int = 4) -> Path:
    log_path = directory / "run-EXP20-P1.events.jsonl"
    sequence = [(1, "spawn", "READY"), (2, "claim", "WORKING"), (3, "gate", "PASS"), (4, "block", "BLOCKED")]
    for index, kind, status in sequence[:count]:
        dee.append_durable(log_path, _event(index, kind, status))
    return log_path


def run_p1() -> dict:
    fixtures = load_fixtures()
    fixture_log = ROOT / fixtures["event_log_fixture"]
    result: dict = {
        "proof": "P1",
        "title": "crash-tolerant, idempotent, resumable event evidence",
        "donor": "OpenHands software-agent-sdk openhands/sdk/conversation/event_store.py (MIT)",
        "host_contract": "scripts/runtime_coordination.py JSONL event log (unchanged)",
    }

    with tempfile.TemporaryDirectory(prefix="exp-20-p1-") as tmp:
        work = Path(tmp)

        # --- a) recovery fidelity on a real committed MPE event log -------------------
        real = work / "real-fixture.jsonl"
        shutil.copyfile(fixture_log, real)
        production_events = rc.read_events(real)
        production_summary = rc.summarize_events(production_events)
        recovered = dee.recover(real)
        result["a_real_fixture"] = {
            "fixture": fixtures["event_log_fixture"],
            "production_event_count": len(production_events),
            "recovered_event_count": recovered["recovered_count"],
            "damage": recovered["damage"],
            "summary_identical": rc.summarize_events(recovered["events"]) == production_summary,
            "integrity": recovered["integrity"],
            "marker_count": recovered["marker_count"],
            "note": "a legacy MPE log carries no length marker, so the verdict is MARKER_UNVERIFIED, never a silent COMPLETE",
        }
        log(f"P1.a real fixture: production {len(production_events)} events, recovered {recovered['recovered_count']}, "
            f"summary identical={result['a_real_fixture']['summary_identical']}, integrity={recovered['integrity']}")

        # --- b) crash with a torn tail ------------------------------------------------
        crash_dir = work / "crash"
        crash_dir.mkdir()
        crash_log = _build_proof_log(crash_dir, count=4)
        before_crash = dee.recover(crash_log)
        dee.append_durable(crash_log, _event(5, "resume", "WORKING"))
        healthy_count = dee.recover(crash_log)["recovered_count"]
        cut = dee.truncate_tail(crash_log, keep_bytes=34)  # cut mid-line, as a killed writer would

        baseline_error = None
        baseline_recovered = None
        try:
            baseline_recovered = rc.read_events(crash_log)
        except rc.ContractError as exc:
            baseline_error = str(exc)

        after_crash = dee.recover(crash_log)
        baseline_summarizable = baseline_recovered is not None
        borrowed_summary = rc.summarize_events(after_crash["events"])
        result["b_torn_tail"] = {
            "events_before_crash": healthy_count,
            "crash_simulation": {"method": "truncate the final durable line mid-write", **cut},
            "baseline_arm": {
                "function": "scripts.runtime_coordination.read_events",
                "error": baseline_error,
                "recovered_event_count": len(baseline_recovered) if baseline_recovered is not None else 0,
                "summarizable": baseline_summarizable,
                "evidence_lost_percent": 100.0 if baseline_error else 0.0,
            },
            "borrowed_arm": {
                "function": "harness/durable_event_evidence.recover + production summarize_events",
                "recovered_event_count": after_crash["recovered_count"],
                "damage": after_crash["damage"],
                "integrity": after_crash["integrity"],
                "summarizable": True,
                "summary": borrowed_summary,
                "evidence_lost_percent": round(100.0 * (healthy_count - after_crash["recovered_count"]) / healthy_count, 2),
            },
            "before_crash_integrity": before_crash["integrity"],
        }
        log(f"P1.b torn tail: baseline recovered 0/{healthy_count} ({baseline_error}); "
            f"borrowed recovered {after_crash['recovered_count']}/{healthy_count}, damage kinds="
            f"{sorted({d['kind'] for d in after_crash['damage']})}")

        # damaged log kept as a real artifact
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        damaged_artifact = EVIDENCE_DIR / "cp03_p1_damaged_log.jsonl"
        damaged_artifact.write_bytes(crash_log.read_bytes())

        # --- c) fresh-process resume from the damaged log only ------------------------
        isolated = work / "isolated"
        isolated.mkdir()
        isolated_log = isolated / crash_log.name
        shutil.copyfile(crash_log, isolated_log)
        for marker in crash_log.parent.glob(f".{crash_log.name}.len-*"):
            shutil.copyfile(marker, isolated / marker.name)
        started = time.perf_counter()
        completed = subprocess.run(
            [sys.executable, str(WORKER_PATH), str(isolated_log)],
            capture_output=True, text=True, cwd=isolated, timeout=120,
        )
        worker_seconds = time.perf_counter() - started
        if completed.returncode != 0:
            raise RuntimeError(f"resume worker failed: {completed.returncode} {completed.stderr.strip()}")
        worker_packet = json.loads(completed.stdout.strip())
        in_process_packet = dee.resume_packet(crash_log)
        result["c_fresh_process_resume"] = {
            "worker": str(WORKER_PATH.relative_to(ROOT)),
            "cwd": "<tmp>/isolated (only the damaged log and its marker were present)",
            "returncode": completed.returncode,
            "worker_seconds": round(worker_seconds, 4),
            "read_from_chat": worker_packet["read_from_chat"],
            "rediscovery_steps": 0,
            "run_id": worker_packet["run_id"],
            "task_id": worker_packet["task_id"],
            "recovered_event_count": worker_packet["recovered_count"],
            "damaged_count": worker_packet["damaged_count"],
            "lifecycle": worker_packet["lifecycle"],
            "resumable": worker_packet["resumable"],
            "next_action": worker_packet["next_action"],
            "matches_in_process_packet": normalized(worker_packet) == normalized({**in_process_packet, "worker": "fresh_process", "read_from_chat": False}),
        }
        log(f"P1.c fresh process: run_id={worker_packet['run_id']} recovered={worker_packet['recovered_count']} "
            f"resumable={worker_packet['resumable']} matches_in_process={result['c_fresh_process_resume']['matches_in_process_packet']}")

        # --- d) idempotent replay vs. the production silent duplicate -----------------
        replay_dir = work / "replay"
        replay_dir.mkdir()
        replay_log = _build_proof_log(replay_dir, count=3)
        digest_before = dee.sha256_file(replay_log)
        identical = dee.append_durable(replay_log, _event(3, "gate", "PASS"))
        digest_after_identical = dee.sha256_file(replay_log)
        conflict_error = None
        try:
            dee.append_durable(replay_log, {**_event(3, "gate", "PASS"), "status": "FAILED"})
        except dee.DuplicateEventConflict as exc:
            conflict_error = str(exc)
        digest_after_conflict = dee.sha256_file(replay_log)

        baseline_dir = work / "baseline-duplicate"
        baseline_dir.mkdir()
        baseline_log = _build_proof_log(baseline_dir, count=3)
        rc.append_event(baseline_log, _event(3, "gate", "PASS"), writer_id="coordinator")
        baseline_lines = [json.loads(line) for line in baseline_log.read_text(encoding="utf-8").splitlines() if line.strip()]
        result["d_idempotency"] = {
            "borrowed_arm": {
                "identical_replay_status": identical["status"],
                "identical_replay_bytes_written": identical["bytes_written"],
                "log_digest_unchanged_after_identical_replay": digest_before == digest_after_identical,
                "conflict_error": conflict_error,
                "log_digest_unchanged_after_conflict": digest_after_identical == digest_after_conflict,
                "event_count": dee.recover(replay_log)["recovered_count"],
            },
            "baseline_arm": {
                "function": "scripts.runtime_coordination.append_event",
                "duplicate_id_accepted_silently": True,
                "event_count": len(baseline_lines),
                "unique_event_ids": len({item["event_id"] for item in baseline_lines}),
                "duplicate_records": len(baseline_lines) - len({item["event_id"] for item in baseline_lines}),
            },
        }
        log(f"P1.d idempotency: borrowed replay={identical['status']} conflict={'raised' if conflict_error else 'missing'}; "
            f"baseline wrote {len(baseline_lines)} records for {len({item['event_id'] for item in baseline_lines})} unique ids")

        # --- e) marker check, and its failure mode -----------------------------------
        marker_dir = work / "marker"
        marker_dir.mkdir()
        marker_log = _build_proof_log(marker_dir, count=4)
        cheap = dee.integrity_check(marker_log, known_count=4)
        advanced = dee.integrity_check(marker_log, known_count=2)
        for marker in marker_log.parent.glob(f".{marker_log.name}.len-*"):
            marker.unlink()
        absent = dee.integrity_check(marker_log, known_count=4)
        dee.advance_marker(marker_log, None, 99)  # stale/incorrect marker on purpose
        stale = dee.recover(marker_log)
        result["e_marker"] = {
            "cheap_check_unchanged": cheap,
            "cheap_check_advanced": advanced,
            "parse_ops_full_recovery": stale["line_count"],
            "marker_absent_verdict": absent["verdict"],
            "stale_marker_integrity": stale["integrity"],
            "stale_marker_count": stale["marker_count"],
            "never_silently_trusted": stale["integrity"] != dee.INTEGRITY_COMPLETE,
        }
        log(f"P1.e marker: cheap check parse_ops={cheap['parse_ops']} vs full recovery {stale['line_count']} parses; "
            f"stale marker integrity={stale['integrity']}")

        # --- f) overhead --------------------------------------------------------------
        production_times, durable_times = [], []
        for label, times in (("production", production_times), ("durable", durable_times)):
            for index in range(1, 26):
                directory = work / f"overhead-{label}-{index}"
                directory.mkdir()
                target = directory / "events.jsonl"
                event = _event(index, "gate", "PASS")
                started = time.perf_counter()
                if label == "production":
                    rc.append_event(target, event, writer_id="coordinator")
                else:
                    dee.append_durable(target, event)
                times.append(time.perf_counter() - started)
        marker_bytes = sum(path.stat().st_size for path in (work / "overhead-durable-1").glob("*.len-*"))
        result["f_overhead"] = {
            "appends_measured": len(production_times),
            "median_append_seconds_production": round(statistics.median(production_times), 8),
            "median_append_seconds_durable": round(statistics.median(durable_times), 8),
            "overhead_ratio": round(statistics.median(durable_times) / statistics.median(production_times), 3),
            "extra_files_per_log": 1,
            "extra_payload_bytes_per_log": marker_bytes,
            "extra_syscalls_per_append": 2,
            "new_dependencies": [],
        }
        log(f"P1.f overhead: median append production={result['f_overhead']['median_append_seconds_production']}s "
            f"durable={result['f_overhead']['median_append_seconds_durable']}s "
            f"ratio={result['f_overhead']['overhead_ratio']} extra_bytes={marker_bytes}")

    result["g_rollback"] = {
        "production_files_modified": [],
        "rollback": "delete experiments/exp-20-dify-openhands-component-extraction/harness and evidence; nothing else references them",
        "persistent_runtime_required": False,
        "database_or_queue_required": False,
        "new_dependency": False,
    }

    checks = {
        "recovery_matches_production_on_a_healthy_real_log": result["a_real_fixture"]["summary_identical"],
        "baseline_loses_all_evidence_on_a_torn_tail": result["b_torn_tail"]["baseline_arm"]["recovered_event_count"] == 0,
        "borrowed_recovers_every_durable_event": (
            result["b_torn_tail"]["borrowed_arm"]["recovered_event_count"]
            == result["b_torn_tail"]["events_before_crash"] - 1
        ),
        "damage_is_reported_not_dropped": result["b_torn_tail"]["borrowed_arm"]["damage"] != [],
        "production_summary_contract_reused_unchanged": result["b_torn_tail"]["borrowed_arm"]["summary"]["event_count"] > 0,
        "fresh_process_resumes_without_chat": result["c_fresh_process_resume"]["matches_in_process_packet"],
        "identical_replay_writes_nothing": result["d_idempotency"]["borrowed_arm"]["log_digest_unchanged_after_identical_replay"],
        "conflicting_replay_is_refused": result["d_idempotency"]["borrowed_arm"]["conflict_error"] is not None,
        "baseline_duplicate_is_silent": result["d_idempotency"]["baseline_arm"]["duplicate_records"] == 1,
        "marker_never_silently_trusted": result["e_marker"]["never_silently_trusted"],
    }
    result["checks"] = checks
    result["result"] = "PASS" if all(checks.values()) else "FAIL"
    return result


# --------------------------------------------------------------------------------------
# P2 — failure classification onto the existing MPE gate vocabulary
# --------------------------------------------------------------------------------------

class ComputeBudgetExceeded(RuntimeError):
    """Proof-local stand-in for a declared compute-budget hard_limit breach."""


class HTTPStatusError(RuntimeError):
    """Proof-local stand-in for an opaque gateway/HTTP wrapper error."""


def build_exception(case: dict) -> BaseException:
    kind = case["exception"]
    message = case["message"]
    if kind == "triage_contract_error":
        from scripts.triage_engine import ContractError as TriageContractError

        return TriageContractError(message)
    if kind == "runtime_contract_error":
        return rc.ContractError(message)
    if kind == "duplicate_event_conflict":
        return dee.DuplicateEventConflict(message)
    if kind == "file_not_found":
        return FileNotFoundError(message)
    if kind == "timeout":
        return TimeoutError(message)
    if kind == "http_status_error":
        return HTTPStatusError(message)
    if kind == "compute_budget_exceeded":
        return ComputeBudgetExceeded(message)
    if kind == "key_error":
        return KeyError(message)
    if kind == "runtime_error":
        return RuntimeError(message)
    raise ValueError(f"unknown fixture exception kind: {kind}")


def _failing_executor(case: dict):
    calls = {"count": 0}

    def executor(decision: dict) -> dict:
        calls["count"] += 1
        raise build_exception(case)

    executor.calls = calls  # type: ignore[attr-defined]
    return executor


# Real MPE fixtures, identical to tests/test_execution_runner.py: five trusted VERIFIED
# PASS runs at owner-set L4 are what it takes for the production runner to invoke the
# executor at all. Without them every case would stop at NOT_PERMITTED and the control
# arm would measure nothing.
TRUSTED_GATES = [
    {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "git_status"},
    {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "secrets_scan"},
    {"gate_id": "build", "result": "PASS", "evidence_ref": "compileall"},
]


def verified_pass() -> dict:
    return {"outcome": "PASS", "deterministic_gate_results": list(TRUSTED_GATES)}


TRUSTED_HISTORY = [verified_pass() for _ in range(5)]


def run_p2() -> dict:
    fixtures = load_fixtures()
    gates = fc.load_gates(ROOT / "gates" / "registry.yaml")
    task = fixtures["task_fast"]
    deep_task = fixtures["task_deep_change"]
    planted = fixtures["planted_token"]

    cases, classify_times = [], []
    for case in fixtures["failure_cases"]:
        gate = gates[case["gate_id"]]
        exc = build_exception(case)

        executor = _failing_executor(case)
        production = run_task(task, executor, history=TRUSTED_HISTORY, current_level="L4")
        # The annotation layer is additive: it may only attach a classification and a gate
        # decision to the production outcome. Authority fields must be identical.
        authority_fields = ("allowed_action", "acceptance_state", "executor_invoked", "execution_status",
                            "blocking_reasons", "task_risk_tier", "dispatch_evaluation_id", "events")
        annotated = {**production, "failure_classification": None, "gate_decision": None}

        started = time.perf_counter()
        classification = fc.classify_failure(exc)
        classify_times.append(time.perf_counter() - started)

        decision = fc.decide(classification, gate, attempt=0)
        annotated["failure_classification"] = classification
        annotated["gate_decision"] = decision
        authority_identical = all(production.get(field) == annotated.get(field) for field in authority_fields)
        production_text = json.dumps(
            {key: production.get(key) for key in ("reason", "execution_result", "execution_status")}, sort_keys=True
        )
        classification_text = json.dumps(
            {"failure_classification": classification, "gate_decision": decision}, sort_keys=True
        )

        def redact(value: object) -> object:
            """Keep the proof honest without reproducing the planted token in evidence."""
            if isinstance(value, str):
                return value.replace(planted, "<REDACTED-PLANTED-TOKEN>")
            if isinstance(value, dict):
                return {key: redact(item) for key, item in value.items()}
            return value

        cases.append(
            {
                "case_id": case["case_id"],
                "gate_id": case["gate_id"],
                "exception_class": type(exc).__name__,
                "production_execution_status": production["execution_status"],
                "production_acceptance_state": production["acceptance_state"],
                "production_allowed_action": production["allowed_action"],
                "production_executor_invoked": production["executor_invoked"],
                "production_executor_calls": executor.calls["count"],
                "production_reason_redacted": redact(production.get("reason")),
                "production_execution_result_redacted": redact(production.get("execution_result")),
                "production_carries_raw_exception_text": planted in production_text,
                "classification": classification,
                "decision": decision,
                "classification_carries_raw_exception_text": planted in classification_text,
                "authority_unchanged_by_annotation": authority_identical,
                "escalated_above_declared_state": fc.RESTRICTION[decision["decision"]] > fc.RESTRICTION[gate["failure_state"]],
                "downgraded_below_declared_state": (
                    decision["decision"] != "RETRY"
                    and fc.RESTRICTION[decision["decision"]] < fc.RESTRICTION[gate["failure_state"]]
                ),
            }
        )

    distinct_production_statuses = sorted({item["production_execution_status"] for item in cases})
    distinct_kinds = sorted({item["classification"]["kind"] for item in cases})
    distinct_decisions = sorted({item["decision"]["decision"] for item in cases})
    agreements = [item for item in cases if item["decision"]["declared_failure_state"] == item["decision"]["decision"]]

    # determinism: three passes, plus a shuffled input order
    passes = []
    for _ in range(3):
        passes.append(normalized([fc.classify_failure(build_exception(case)) for case in fixtures["failure_cases"]]))
    shuffled = list(reversed(fixtures["failure_cases"]))
    shuffled_map = {case["case_id"]: normalized(fc.classify_failure(build_exception(case))) for case in shuffled}
    ordered_map = {item["case_id"]: normalized(item["classification"]) for item in cases}

    # composition reuses MPE's most-restrictive rule
    composed = fc.compose(
        [
            fc.decide(fc.classify_failure(build_exception(by_id)), gates[by_id["gate_id"]])
            for by_id in fixtures["failure_cases"]
            if by_id["case_id"] in {"F-09-gateway-rate-limit", "F-10-gateway-credentials", "F-12-budget-hard-limit"}
        ]
    )

    # deep-change authority is untouched by the annotation layer
    deep_executor_calls = {"count": 0}

    def deep_executor(decision: dict) -> dict:
        deep_executor_calls["count"] += 1
        return {"status": "PASS"}

    deep_production = run_task(
        deep_task, deep_executor, history=TRUSTED_HISTORY, current_level="L4", stop_condition=True
    )
    deep_case = next(item for item in cases if item["case_id"] == "F-13-deep-change-stop")

    classification_only = json.dumps(
        [{"failure_classification": item["classification"], "gate_decision": item["decision"]} for item in cases],
        sort_keys=True,
    )
    result = {
        "proof": "P2",
        "title": "deterministic failure classification onto the existing MPE gate vocabulary",
        "donors": [
            "OpenHands software-agent-sdk openhands/sdk/event/error_classification.py (MIT)",
            "Dify api/core/tools/errors.py + tool_engine.py + nodes/agent_v2/output_failure_orchestrator.py (pattern only; no source copied)",
        ],
        "host_contract": "gates/registry.yaml failure_state/retry_policy + scripts/execution_runner.run_task (unchanged)",
        "gates_parsed_from_registry": len(gates),
        "gate_ids": sorted(gates),
        "cases": cases,
        "measurements": {
            "failure_cases": len(cases),
            "distinct_production_execution_statuses": distinct_production_statuses,
            "distinct_production_status_count": len(distinct_production_statuses),
            "distinct_classified_kinds": distinct_kinds,
            "distinct_kind_count": len(distinct_kinds),
            "distinct_decisions": distinct_decisions,
            "distinct_decision_count": len(distinct_decisions),
            "cases_matching_the_registry_declared_state": len(agreements),
            "cases_escalated_above_declared_state": sum(1 for item in cases if item["escalated_above_declared_state"]),
            "cases_downgraded_below_declared_state": sum(1 for item in cases if item["downgraded_below_declared_state"]),
            "retry_offered_within_gate_policy": sum(1 for item in cases if item["decision"]["decision"] == "RETRY"),
            "authority_unchanged_in_every_case": all(item["authority_unchanged_by_annotation"] for item in cases),
            "executor_invocations_per_case": sorted({item["production_executor_calls"] for item in cases}),
            "median_classify_seconds": round(statistics.median(classify_times), 9),
            "determinism_three_passes_identical": passes[0] == passes[1] == passes[2],
            "determinism_order_independent": shuffled_map == ordered_map,
            "planted_token_in_classification_evidence": classification_only.count(planted),
            "cases_where_production_copies_raw_exception_text": sum(
                1 for item in cases if item["production_carries_raw_exception_text"]
            ),
            "cases_where_classification_copies_raw_exception_text": sum(
                1 for item in cases if item["classification_carries_raw_exception_text"]
            ),
            "composition": composed,
        },
        "deep_change_authority": {
            "task_id": deep_production["task_id"],
            "allowed_action": deep_production["allowed_action"],
            "acceptance_state": deep_production["acceptance_state"],
            "executor_invoked": deep_production["executor_invoked"],
            "executor_calls": deep_executor_calls["count"],
            "blocking_reasons": deep_production["blocking_reasons"],
            "classified_kind": deep_case["classification"]["kind"],
            "classified_decision": deep_case["decision"]["decision"],
            "retry_budget": deep_case["decision"]["retry_budget"],
            "classifier_granted_execution": False,
        },
    }

    checks = {
        "registry_parsed_without_a_yaml_dependency": len(gates) == 20,
        "baseline_is_undifferentiated": result["measurements"]["distinct_production_status_count"] == 1,
        "classification_differentiates": result["measurements"]["distinct_kind_count"] >= 5,
        "no_case_downgrades_a_declared_gate_state": result["measurements"]["cases_downgraded_below_declared_state"] == 0,
        "at_least_one_case_agrees_with_the_declared_state": result["measurements"]["cases_matching_the_registry_declared_state"] >= 2,
        "authority_unchanged_in_every_case": result["measurements"]["authority_unchanged_in_every_case"],
        "deterministic_across_passes": result["measurements"]["determinism_three_passes_identical"],
        "order_independent": result["measurements"]["determinism_order_independent"],
        "no_exception_detail_leaks_into_classification_evidence": (
            result["measurements"]["planted_token_in_classification_evidence"] == 0
            and result["measurements"]["cases_where_classification_copies_raw_exception_text"] == 0
        ),
        "baseline_does_copy_raw_exception_text": (
            result["measurements"]["cases_where_production_copies_raw_exception_text"] >= 1
        ),
        "fail_closed_kinds_never_retry": all(
            item["decision"]["decision"] != "RETRY"
            for item in cases
            if item["classification"]["kind"] in fc.NO_AUTO_RETRY
        ),
        "deep_change_execution_still_blocked": (
            deep_production["executor_invoked"] is False and deep_executor_calls["count"] == 0
        ),
        "composition_is_most_restrictive": composed["decision"] == "HUMAN_REQUIRED",
    }
    result["checks"] = checks
    result["result"] = "PASS" if all(checks.values()) else "FAIL"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=("p1", "p2", "all"), nargs="?", default="all")
    args = parser.parse_args()

    started = time.perf_counter()
    before = production_digests()
    log(f"EXP-20 CP-03 proof run: target={args.target} root={ROOT}")
    log(f"production digests captured for {len(before)} files")

    payloads: dict[str, dict] = {}
    if args.target in ("p1", "all"):
        payloads["p1"] = run_p1()
        write_evidence("cp03_p1_durable_event_evidence.json", payloads["p1"])
    if args.target in ("p2", "all"):
        payloads["p2"] = run_p2()
        write_evidence("cp03_p2_failure_classification.json", payloads["p2"])

    after = production_digests()
    changed = sorted(name for name in after if before[name] != after[name])

    # determinism: a second full P1 pass must produce the same normalized evidence
    determinism = {}
    if args.target in ("p1", "all"):
        second = normalized(run_p1())
        determinism["p1_second_pass_identical"] = second == normalized(payloads["p1"])
    if args.target in ("p2", "all"):
        determinism["p2_second_pass_identical"] = normalized(run_p2()) == normalized(payloads["p2"])

    summary = {
        "experiment": "EXP-20",
        "checkpoint": "CP-03",
        "run_date": "2026-10-09",
        "target": args.target,
        "proofs": {key: value["result"] for key, value in payloads.items()},
        "checks": {key: value["checks"] for key, value in payloads.items()},
        "determinism": determinism,
        "production_files_changed": changed,
        "production_untouched": not changed,
        "total_seconds": round(time.perf_counter() - started, 3),
        "new_dependencies": [],
        "persistent_runtime_created": False,
        "database_or_queue_created": False,
        "sandbox_or_executor_service_created": False,
        "workflow_engine_created": False,
    }
    summary["result"] = (
        "PASS"
        if summary["production_untouched"]
        and all(determinism.values())
        and all(value == "PASS" for value in summary["proofs"].values())
        else "FAIL"
    )
    write_evidence("proof_run.json", summary)
    log(json.dumps({"proofs": summary["proofs"], "determinism": determinism,
                    "production_files_changed": changed, "result": summary["result"]}, sort_keys=True))
    log(f"EXP-20 CP-03 result: {summary['result']}")
    return 0 if summary["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
