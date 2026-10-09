"""EXP-20 — Dify/OpenHands component extraction proofs.

These tests execute the experiment-local proofs in
``experiments/exp-20-dify-openhands-component-extraction/harness``:

* P1 — crash-tolerant, idempotent, resumable event evidence (OpenHands ``EventLog``
  subset) measured against the *production* ``scripts/runtime_coordination.py``;
* P2 — deterministic failure classification onto the existing ``gates/registry.yaml``
  vocabulary (OpenHands ``error_classification`` + Dify typed tool errors) measured
  against the *production* ``scripts/execution_runner.run_task``.

They test contract behaviour (recovery is explicit and never silent, idempotency, the
donor's authoritative-class-first ordering, fail-closed kinds, no downgrade of a declared
gate state, no exception detail in evidence, unchanged authority), not implementation
trivia. No production module is modified by importing or running them.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "exp-20-dify-openhands-component-extraction"
HARNESS = EXPERIMENT / "harness"
EVIDENCE = EXPERIMENT / "evidence"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HARNESS))

from scripts import runtime_coordination as rc  # noqa: E402
from scripts.execution_runner import run_task  # noqa: E402

import durable_event_evidence as dee  # noqa: E402
import exp20_proof as proof  # noqa: E402
import failure_classification as fc  # noqa: E402

FIXTURES = json.loads((HARNESS / "fixtures.json").read_text(encoding="utf-8"))
REAL_LOG = ROOT / FIXTURES["event_log_fixture"]
PLANTED = FIXTURES["planted_token"]


def event(index: int, kind: str = "gate", status: str = "PASS", actor: str = "exp-20-test") -> dict:
    return {
        "schema_version": "1.0",
        "event_id": f"evt-exp20-test-{index}",
        "run_id": "EXP-20-TEST",
        "timestamp": f"2026-10-09T00:00:{index:02d}Z",
        "type": kind,
        "actor": actor,
        "task_id": "EXP-20/CP-03",
        "status": status,
        "ref": None,
        "target": None,
    }


class DurableEventEvidenceTests(unittest.TestCase):
    """P1 — the borrowed durability mechanics, and the measured gap they close."""

    def test_recovery_matches_production_on_a_real_committed_mpe_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "real.jsonl"
            log.write_bytes(REAL_LOG.read_bytes())
            production = rc.read_events(log)
            recovered = dee.recover(log)
            self.assertEqual(len(production), recovered["recovered_count"])
            self.assertEqual([], recovered["damage"])
            self.assertEqual(rc.summarize_events(production), rc.summarize_events(recovered["events"]))
            self.assertEqual(dee.INTEGRITY_MARKER_UNVERIFIED, recovered["integrity"])
            self.assertIsNone(recovered["marker_count"])

    def test_torn_tail_destroys_everything_for_the_production_reader(self):
        """The baseline gap: one damaged line loses the whole run's evidence."""
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            for index in range(1, 6):
                dee.append_durable(log, event(index))
            dee.truncate_tail(log, keep_bytes=34)
            with self.assertRaises(rc.ContractError):
                rc.read_events(log)
            recovered = dee.recover(log)
            self.assertEqual(4, recovered["recovered_count"])
            self.assertEqual(dee.INTEGRITY_DAMAGED, recovered["integrity"])
            self.assertEqual(1, len(recovered["damage"]))
            self.assertEqual(dee.DAMAGE_TORN_TAIL, recovered["damage"][0]["kind"])
            self.assertEqual(5, recovered["damage"][0]["line"])
            self.assertFalse(recovered["damage"][0]["terminated"])
            self.assertEqual(4, rc.summarize_events(recovered["events"])["event_count"])

    def test_interior_damage_and_invalid_events_are_reported_never_dropped(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            lines = [
                json.dumps(event(1), sort_keys=True),
                "{not json at all",
                json.dumps(event(3), sort_keys=True),
                json.dumps({**event(4), "type": "thought"}, sort_keys=True),
                json.dumps(event(5, "terminal", "DONE"), sort_keys=True),
            ]
            log.write_text("\n".join(lines) + "\n", encoding="utf-8")
            recovered = dee.recover(log)
            kinds = [(record["line"], record["kind"]) for record in recovered["damage"]]
            self.assertEqual([(2, dee.DAMAGE_INTERIOR), (4, dee.DAMAGE_INVALID_EVENT)], kinds)
            self.assertEqual(3, recovered["recovered_count"])
            self.assertEqual("DONE", rc.summarize_events(recovered["events"])["outcome"])

    def test_duplicate_event_ids_are_reported_and_the_first_record_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            log.write_text(
                json.dumps(event(1), sort_keys=True) + "\n" + json.dumps(event(1), sort_keys=True) + "\n",
                encoding="utf-8",
            )
            recovered = dee.recover(log)
            self.assertEqual(1, recovered["recovered_count"])
            self.assertEqual(dee.INTEGRITY_DUPLICATE_EVENTS, recovered["integrity"])
            self.assertEqual(dee.DAMAGE_DUPLICATE_ID, recovered["damage"][0]["kind"])

    def test_recovery_never_writes_to_the_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            dee.append_durable(log, event(1))
            before = dee.sha256_file(log)
            dee.recover(log)
            dee.resume_packet(log)
            self.assertEqual(before, dee.sha256_file(log))

    def test_identical_replay_writes_nothing_and_a_conflicting_replay_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            dee.append_durable(log, event(1))
            digest = dee.sha256_file(log)
            replay = dee.append_durable(log, event(1))
            self.assertEqual("DUPLICATE_REPLAYED", replay["status"])
            self.assertEqual(0, replay["bytes_written"])
            self.assertEqual(digest, dee.sha256_file(log))
            with self.assertRaises(dee.DuplicateEventConflict):
                dee.append_durable(log, {**event(1), "status": "FAILED"})
            self.assertEqual(digest, dee.sha256_file(log))
            self.assertEqual(1, dee.recover(log)["recovered_count"])

    def test_production_append_still_accepts_a_silent_duplicate(self):
        """Documents the measured baseline: the production writer has no id idempotency."""
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            rc.append_event(log, event(1), writer_id="coordinator")
            rc.append_event(log, event(1), writer_id="coordinator")
            events = rc.read_events(log)
            self.assertEqual(2, len(events))
            self.assertEqual(1, len({item["event_id"] for item in events}))

    def test_marker_check_is_cheap_and_is_never_trusted_as_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            for index in range(1, 5):
                dee.append_durable(log, event(index))
            self.assertEqual("UNCHANGED", dee.integrity_check(log, known_count=4)["verdict"])
            self.assertEqual("ADVANCED", dee.integrity_check(log, known_count=2)["verdict"])
            self.assertEqual(0, dee.integrity_check(log, known_count=4)["parse_ops"])
            for marker in log.parent.glob(f".{log.name}.len-*"):
                marker.unlink()
            self.assertEqual("MARKER_ABSENT", dee.integrity_check(log, known_count=4)["verdict"])
            dee.advance_marker(log, None, 99)
            recovered = dee.recover(log)
            self.assertEqual(dee.INTEGRITY_MARKER_UNVERIFIED, recovered["integrity"])
            self.assertNotEqual(dee.INTEGRITY_COMPLETE, recovered["integrity"])

    def test_marker_is_complete_only_when_it_agrees_with_the_recovered_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "events.jsonl"
            for index in range(1, 4):
                dee.append_durable(log, event(index))
            self.assertEqual(dee.INTEGRITY_COMPLETE, dee.recover(log)["integrity"])

    def test_a_fresh_process_resumes_from_a_damaged_log_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            log = work / "events.jsonl"
            for index in range(1, 5):
                dee.append_durable(log, event(index, "spawn" if index == 1 else "gate", "READY" if index == 1 else "PASS"))
            dee.append_durable(log, event(5, "block", "BLOCKED"))
            dee.truncate_tail(log, keep_bytes=34)
            expected = dee.resume_packet(log)
            completed = subprocess.run(
                [sys.executable, str(HARNESS / "resume_worker.py"), str(log)],
                capture_output=True, text=True, cwd=work, timeout=120,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            packet = json.loads(completed.stdout.strip())
            self.assertFalse(packet["read_from_chat"])
            self.assertEqual(expected["recovered_count"], packet["recovered_count"])
            self.assertEqual(expected["run_id"], packet["run_id"])
            self.assertEqual(expected["task_id"], packet["task_id"])
            self.assertEqual(expected["damage"], packet["damage"])
            self.assertTrue(packet["resumable"])


class FailureClassificationTests(unittest.TestCase):
    """P2 — the borrowed failure contract, anchored to the real gate registry."""

    @classmethod
    def setUpClass(cls):
        cls.gates = fc.load_gates(ROOT / "gates" / "registry.yaml")

    def test_the_real_gate_registry_is_parsed_without_a_yaml_dependency(self):
        self.assertEqual(20, len(self.gates))
        self.assertIn("deep_change_check", self.gates)
        for gate in self.gates.values():
            self.assertIn(gate["failure_state"], {"REWORK", "BLOCKED", "HUMAN_REQUIRED"})

    def test_retry_budgets_are_derived_from_the_registry_text(self):
        self.assertEqual(1, fc.retry_budget(self.gates["unit_tests"]))
        self.assertEqual(0, fc.retry_budget(self.gates["deep_change_check"]))
        self.assertEqual(0, fc.retry_budget(self.gates["compute_budget_health"]))
        self.assertEqual(0, fc.retry_budget({"retry_policy": "an undocumented policy"}))

    def test_an_authoritative_class_beats_incidental_message_wording(self):
        classified = fc.classify_failure(rc.ContractError("invalid api key inside a contract message"))
        self.assertEqual(fc.KIND_AGENT_ACTION, classified["kind"])
        self.assertNotEqual(fc.KIND_AUTH, classified["kind"])

    def test_a_specific_subclass_is_not_swallowed_by_its_base(self):
        classified = fc.classify_failure(dee.DuplicateEventConflict("event_id already durable"))
        self.assertEqual(fc.KIND_AGENT_ACTION, classified["kind"])
        self.assertFalse(classified["retryable"])

    def test_opaque_wrappers_use_message_heuristics(self):
        cases = {
            "error code: 429 - rate limit exceeded": fc.KIND_RATE_LIMIT,
            "error code: 401 - invalid api key": fc.KIND_AUTH,
            "projected total exceeds the declared hard_limit": fc.KIND_QUOTA,
            "upstream returned an unexpected payload": fc.KIND_TRANSIENT,
        }
        for message, kind in cases.items():
            with self.subTest(message=message):
                self.assertEqual(kind, fc.classify_failure(proof.HTTPStatusError(message))["kind"])

    def test_an_undiagnosed_failure_fails_closed(self):
        classified = fc.classify_failure(RuntimeError("architecture redesign detected"))
        self.assertEqual(fc.KIND_UNKNOWN, classified["kind"])
        self.assertFalse(classified["retryable"])
        decision = fc.decide(classified, self.gates["deep_change_check"])
        self.assertEqual("HUMAN_REQUIRED", decision["decision"])
        self.assertEqual(0, decision["retry_budget"])

    def test_no_exception_detail_is_copied_into_the_classification(self):
        classified = fc.classify_failure(proof.HTTPStatusError(f"error code: 401 - invalid api key {PLANTED}"))
        self.assertNotIn(PLANTED, json.dumps(classified, sort_keys=True))
        self.assertTrue(classified["evidence_safe"])
        self.assertEqual({"kind", "retryable", "executor_action", "evidence_safe"}, set(classified))

    def test_a_retry_is_bounded_by_the_gate_policy_and_never_downgrades_a_declared_state(self):
        classified = fc.classify_failure(rc.ContractError("invalid JSONL line 5"))
        first = fc.decide(classified, self.gates["event_log_valid"], attempt=0)
        second = fc.decide(classified, self.gates["event_log_valid"], attempt=1)
        self.assertEqual("RETRY", first["decision"])
        self.assertEqual("REWORK", second["decision"])
        blocked = fc.decide(fc.classify_failure(FileNotFoundError("missing artifact")), self.gates["artifact_exists"])
        self.assertEqual("BLOCKED", blocked["decision"])
        self.assertEqual("BLOCKED", blocked["declared_failure_state"])

    def test_fail_closed_kinds_escalate_instead_of_retrying(self):
        for kind, exc, gate_id in (
            (fc.KIND_AUTH, proof.HTTPStatusError("error code: 401 - invalid api key"), "build"),
            (fc.KIND_QUOTA, proof.ComputeBudgetExceeded("hard_limit exceeded"), "compute_budget_health"),
            (fc.KIND_INTERNAL, KeyError("acceptance_criteria"), "acceptance_tests"),
        ):
            with self.subTest(kind=kind):
                classified = fc.classify_failure(exc)
                self.assertEqual(kind, classified["kind"])
                decision = fc.decide(classified, self.gates[gate_id])
                self.assertNotEqual("RETRY", decision["decision"])
                self.assertGreaterEqual(
                    fc.RESTRICTION[decision["decision"]], fc.RESTRICTION[self.gates[gate_id]["failure_state"]]
                )

    def test_composition_reuses_the_most_restrictive_rule_and_rejects_foreign_vocabulary(self):
        decisions = [
            fc.decide(fc.classify_failure(proof.HTTPStatusError("error code: 429")), self.gates["integration_tests"]),
            fc.decide(fc.classify_failure(proof.HTTPStatusError("error code: 401 - unauthorized")), self.gates["build"]),
        ]
        self.assertEqual("HUMAN_REQUIRED", fc.compose(decisions)["decision"])
        with self.assertRaises(ValueError):
            fc.most_restrictive("RETRY", "ESCALATE_TO_CLOUD")

    def test_classification_is_deterministic_and_order_independent(self):
        cases = FIXTURES["failure_cases"]
        forward = [fc.classify_failure(proof.build_exception(case)) for case in cases]
        again = [fc.classify_failure(proof.build_exception(case)) for case in cases]
        backward = {
            case["case_id"]: fc.classify_failure(proof.build_exception(case)) for case in reversed(cases)
        }
        self.assertEqual(forward, again)
        for case, classified in zip(cases, forward):
            self.assertEqual(classified, backward[case["case_id"]])

    def test_annotation_never_changes_production_authority(self):
        task = FIXTURES["task_fast"]
        for case in FIXTURES["failure_cases"]:
            with self.subTest(case=case["case_id"]):
                executor = proof._failing_executor(case)
                production = run_task(task, executor, history=proof.TRUSTED_HISTORY, current_level="L4")
                self.assertEqual("ERROR", production["execution_status"])
                self.assertEqual(1, executor.calls["count"])
                classified = fc.classify_failure(proof.build_exception(case))
                decision = fc.decide(classified, self.gates[case["gate_id"]])
                annotated = {**production, "failure_classification": classified, "gate_decision": decision}
                for field in ("allowed_action", "acceptance_state", "executor_invoked", "execution_status",
                              "blocking_reasons", "task_risk_tier", "dispatch_evaluation_id", "events"):
                    self.assertEqual(production[field], annotated[field], field)

    def test_a_deep_change_task_still_never_reaches_the_executor(self):
        calls = {"count": 0}

        def executor(decision: dict) -> dict:
            calls["count"] += 1
            return {"status": "PASS"}

        result = run_task(
            FIXTURES["task_deep_change"], executor, history=proof.TRUSTED_HISTORY, current_level="L4",
            stop_condition=True,
        )
        self.assertEqual("OBSERVE", result["allowed_action"])
        self.assertEqual("BLOCKED", result["acceptance_state"])
        self.assertFalse(result["executor_invoked"])
        self.assertEqual(0, calls["count"])


class ProofEvidenceTests(unittest.TestCase):
    """The committed evidence must say what RESULTS.md claims."""

    @classmethod
    def setUpClass(cls):
        cls.summary = json.loads((EVIDENCE / "proof_run.json").read_text(encoding="utf-8"))
        cls.p1 = json.loads((EVIDENCE / "cp03_p1_durable_event_evidence.json").read_text(encoding="utf-8"))
        cls.p2 = json.loads((EVIDENCE / "cp03_p2_failure_classification.json").read_text(encoding="utf-8"))

    def test_both_proofs_pass_and_production_is_untouched(self):
        self.assertEqual("PASS", self.summary["result"])
        self.assertEqual({"p1": "PASS", "p2": "PASS"}, self.summary["proofs"])
        self.assertEqual([], self.summary["production_files_changed"])
        self.assertTrue(self.summary["production_untouched"])
        self.assertTrue(self.summary["determinism"]["p1_second_pass_identical"])
        self.assertTrue(self.summary["determinism"]["p2_second_pass_identical"])
        for flag in ("persistent_runtime_created", "database_or_queue_created",
                     "sandbox_or_executor_service_created", "workflow_engine_created"):
            self.assertFalse(self.summary[flag], flag)
        self.assertEqual([], self.summary["new_dependencies"])

    def test_every_declared_check_passed(self):
        for proof_id in ("p1", "p2"):
            for name, passed in self.summary["checks"][proof_id].items():
                with self.subTest(proof=proof_id, check=name):
                    self.assertTrue(passed, name)

    def test_the_measured_deltas_are_the_ones_quoted(self):
        self.assertEqual(0, self.p1["b_torn_tail"]["baseline_arm"]["recovered_event_count"])
        self.assertEqual(100.0, self.p1["b_torn_tail"]["baseline_arm"]["evidence_lost_percent"])
        self.assertEqual(4, self.p1["b_torn_tail"]["borrowed_arm"]["recovered_event_count"])
        self.assertEqual(20.0, self.p1["b_torn_tail"]["borrowed_arm"]["evidence_lost_percent"])
        self.assertEqual(1, self.p1["d_idempotency"]["baseline_arm"]["duplicate_records"])
        self.assertEqual(0, self.p1["d_idempotency"]["borrowed_arm"]["identical_replay_bytes_written"])
        measurements = self.p2["measurements"]
        self.assertEqual(14, measurements["failure_cases"])
        self.assertEqual(1, measurements["distinct_production_status_count"])
        self.assertEqual(8, measurements["distinct_kind_count"])
        self.assertEqual(0, measurements["cases_downgraded_below_declared_state"])
        self.assertEqual(0, measurements["planted_token_in_classification_evidence"])
        self.assertEqual(1, measurements["cases_where_production_copies_raw_exception_text"])
        self.assertTrue(measurements["authority_unchanged_in_every_case"])
        self.assertEqual(0, self.p2["deep_change_authority"]["executor_calls"])

    def test_the_damaged_log_artifact_is_committed_and_really_is_damaged(self):
        artifact = EVIDENCE / "cp03_p1_damaged_log.jsonl"
        self.assertTrue(artifact.is_file())
        text = artifact.read_text(encoding="utf-8")
        self.assertFalse(text.endswith("\n"))
        with self.assertRaises(rc.ContractError):
            rc.read_events(artifact)

    def test_the_component_map_uses_only_the_four_checkpoint_dispositions(self):
        text = (EXPERIMENT / "COMPONENT_MAP.md").read_text(encoding="utf-8")
        for token in ("KEEP_EXISTING", "BORROW", "ADAPT", "REJECT"):
            self.assertIn(token, text)
        # the planning README's older vocabulary must not leak into the CP-01 map
        self.assertNotIn("IGNORE", text)
        rows = [line for line in text.splitlines() if line.startswith("| D") or line.startswith("| O")]
        self.assertGreaterEqual(len(rows), 30)
        for row in rows:
            disposition = row.rstrip("|").rsplit("|", 1)[-1]
            self.assertTrue(
                any(token in disposition for token in ("KEEP_EXISTING", "BORROW", "ADAPT", "REJECT")),
                disposition,
            )

    def test_both_upstreams_are_pinned_in_the_audit(self):
        text = (EXPERIMENT / "UPSTREAM_AUDIT.md").read_text(encoding="utf-8")
        for pin in (
            "b2ce9ac10000cbf3d6bd37e5a11234762e0b6d95",
            "937d0d6aa201d8ac31cac514e0dc64ce5c434004",
            "33044182505244749928644a4643368a9e998ee7",
        ):
            self.assertIn(pin, text)
        self.assertIn("graphon==0.7.0", text)


if __name__ == "__main__":
    unittest.main()
