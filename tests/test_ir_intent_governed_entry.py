"""OBS-01 regression suite — MPE IR intent vs Earned Autonomy governed entry.

OBS-01 (observed in the real Arena run ARENA-XEXEC-EXP002-20260916-01, see
``experiments/exp-002-machine-protocol/ARENA_EXECUTION_RECORD.json`` ->
``mpe_governance_observation``):

    Frozen IR intent: autonomy.level=FAST, autonomy.requires_human_approval=false.
    Production governed entry on the IR-derived Task Packet: OBSERVE /
    NOT_PERMITTED / executor_invoked=false — at L0 and at L4 — because the
    trusted history is empty and ``earned_recommended_level=L0``.

This suite fixes the production contract for the chain

    IR intent -> derived Task Packet -> governed entry -> executable permission

without weakening Earned Autonomy:

1. The IR ``autonomy`` / ``decision`` blocks are INTENT + at most a
   TIGHTEN-ONLY constraint (``scripts/mpe_ir_mapping.derive_ir_intent``).
   They are never a permission. ``requires_human_approval: false`` never means
   "execution is authorized"; it only means "no additional human gate is
   requested by this declaration".
2. Executable permission is derived exclusively by the governed entry as the
   MOST RESTRICTIVE of the earned-autonomy ceiling, the approval ceiling and
   the hard safety ceiling (``scripts.dispatch_autonomy``). The earned level
   comes only from trusted history (``scripts.earned_autonomy``).
3. Empty trusted history is handled explicitly and deterministically:
   earned L0 -> OBSERVE -> NOT_PERMITTED, executor never invoked.
4. An intent's ``requires_human_approval: true`` / DEEP-CHANGE request
   TIGHTENS the decision: the human gate stays mandatory even when the
   recomputed triage of the task content would not require one. The intent can
   never remove a gate that triage or governance already requires.

All pipeline behavior is exercised through the existing production paths
(``triage_engine.governed_run`` -> ``execution_runner.run_task`` ->
``task_acceptance`` -> ``dispatch_autonomy`` -> ``earned_autonomy``); only the
executor is faked. No governance logic is duplicated here.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dispatch_autonomy as dispatch  # noqa: E402
import earned_autonomy as earned  # noqa: E402
import execution_runner as runner  # noqa: E402
import task_acceptance as ta  # noqa: E402
import triage_engine as te  # noqa: E402

DEFAULT_GATES = [
    {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "git_status"},
    {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "secrets_scan"},
    {"gate_id": "build", "result": "PASS", "evidence_ref": "compileall"},
]

SELF_REPORTED_GATES = [
    {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "self_reported"},
    {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "self_reported"},
    {"gate_id": "build", "result": "PASS", "evidence_ref": "self_reported"},
]

UNKNOWN_GATES = [
    {"gate_id": "clean_diff_scope", "result": "PASS", "evidence_ref": "model_said_so"},
    {"gate_id": "secrets_scan", "result": "PASS", "evidence_ref": "model_said_so"},
    {"gate_id": "build", "result": "PASS", "evidence_ref": "model_said_so"},
]


def verified_pass(gates=None) -> dict:
    return {"outcome": "PASS", "deterministic_gate_results": gates or DEFAULT_GATES}


def ir_derived_task_packet() -> dict:
    """The Arena-derived Task Packet for the frozen EXP-002 IR (T-001).

    Content fields are the deterministic IR->TRIAGE_INPUT derivable subset;
    ``rollback_known`` / ``ratings`` / ``signals`` are not representable in
    mpe-ir v0.1 and were supplied by the task author exactly as recorded in the
    Arena evidence (EV-05 triage output: execution_confidence=100, all rating
    axes 0, no signals, recommended_risk_tier=FAST).
    """
    return {
        "task_id": "T-001",
        "summary": "Stage 2 status documentation sync for murat-project-engineer",
        "affected_repositories": ["murat-project-engineer"],
        "acceptance_criteria_present": True,
        "rollback_known": True,
        "ratings": {"complexity": 0, "risk": 0, "architectural_impact": 0, "data_sensitivity": 0, "unknowns": 0},
        "signals": [],
    }


def fast_task() -> dict:
    return {
        "task_id": "t-fast-1",
        "summary": "low risk fast task",
        "affected_repositories": ["repo-a"],
        "acceptance_criteria_present": True,
        "rollback_known": True,
        "ratings": {"complexity": 0, "risk": 0, "architectural_impact": 0, "data_sensitivity": 0, "unknowns": 0},
        "signals": [],
    }


def approval_task() -> dict:
    """Triage itself requires human approval (production_change signal)."""
    return {
        "task_id": "t-appr-1",
        "summary": "production change requiring approval",
        "affected_repositories": ["repo-a"],
        "acceptance_criteria_present": True,
        "rollback_known": True,
        "ratings": {"complexity": 1, "risk": 1, "architectural_impact": 1, "data_sensitivity": 0, "unknowns": 0},
        "signals": ["production_change"],
    }


class FakeExecutor:
    """Counts calls; returns a plain self-reported PASS (never trusted)."""

    def __init__(self):
        self.calls = 0

    def __call__(self, decision: dict) -> dict:
        self.calls += 1
        return {"status": "PASS", "task_id": decision.get("task_id")}


class Obs01ReproductionTests(unittest.TestCase):
    """Reproduction of OBS-01 through the unchanged production governed entry.

    Current result (Arena evidence EV-06 / EV-07) == expected semantic result
    under the existing Earned Autonomy contracts: the frozen IR's autonomy
    block is intent only; with an empty trusted history the earned ceiling is
    L0, so the governed entry must deny execution at every owner level.
    """

    def test_obs01_default_l0_denies_execution(self):
        ex = FakeExecutor()
        r = te.governed_run(ir_derived_task_packet(), ex)
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "ACCEPTED_OBSERVE")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertEqual(r["execution_status"], "NOT_PERMITTED")
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertEqual(r["task_risk_tier"], "FAST")
        self.assertEqual(r["current_autonomy_level"], "L0")
        self.assertEqual(r["blocking_reasons"], [])
        self.assertEqual(r["events"], ["acceptance", "enforcement"])

    def test_obs01_elevated_l4_denies_execution(self):
        ex = FakeExecutor()
        r = te.governed_run(ir_derived_task_packet(), ex, history=[], current_level="L4")
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["acceptance_state"], "ACCEPTED_OBSERVE")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertEqual(r["execution_status"], "NOT_PERMITTED")
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertEqual(r["current_autonomy_level"], "L4")

    def test_obs01_frozen_ir_intent_is_not_authorization(self):
        """The frozen IR's intent (FAST / no approval) must never be read as
        executable permission: the produced decision carries no permission and
        the L0-L4 ladder is untouched by the IR."""
        from mpe_ir_mapping import derive_ir_intent  # noqa: PLC0415

        ir = json.loads((ROOT / "experiments" / "exp-002-machine-protocol" / "MPE_IR_FROZEN.json").read_text("utf-8"))
        intent = derive_ir_intent(ir)
        self.assertIsNone(intent["authorization"])
        self.assertEqual(intent["semantics"], "intent_only_never_permission")
        self.assertEqual(intent["requested_risk_tier"], "FAST")
        self.assertFalse(intent["requested_human_approval"])
        # No L0-L4 token anywhere in the intent payload.
        self.assertEqual({"intent_only_never_permission"}, {intent["semantics"]})
        for value in intent.values():
            self.assertNotIn(str(value), {"L0", "L1", "L2", "L3", "L4"})


class EmptyHistoryTests(unittest.TestCase):
    """Empty trusted history is handled explicitly and deterministically."""

    def test_empty_history_is_explicit_l0(self):
        r = dispatch.dispatch_with_autonomy(ir_derived_task_packet(), history=[], current_level="L4")
        self.assertEqual(r["verified_pass_count"], 0)
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertFalse(r["execution_allowed"])

    def test_empty_history_evaluation_is_deterministic(self):
        a = te.governed_run(ir_derived_task_packet(), FakeExecutor(), history=[], current_level="L4")
        b = te.governed_run(ir_derived_task_packet(), FakeExecutor(), history=[], current_level="L4")
        self.assertEqual(a, b)
        self.assertEqual(a["execution_status"], "NOT_PERMITTED")

    def test_empty_history_never_promotes(self):
        r = earned.evaluate_autonomy([], current_level="L0")
        self.assertEqual(r["verified_pass_count"], 0)
        self.assertEqual(r["recommended_level"], "L0")
        self.assertFalse(r["promotion_eligible"])


class IrIntentCannotSelfElevateTests(unittest.TestCase):
    """Negative: an IR / Task Packet can never obtain more autonomy than the
    governance (earned history + approval + safety) allows."""

    def test_owner_level_l4_without_history_still_denied(self):
        ex = FakeExecutor()
        r = te.governed_run(ir_derived_task_packet(), ex, history=[], current_level="L4")
        self.assertEqual(ex.calls, 0)
        self.assertEqual(r["allowed_action"], "OBSERVE")

    def test_intent_false_never_loosens_an_existing_gate(self):
        """``requires_human_approval: false`` must not strip a gate that triage
        already requires: the decision stays EXECUTE_WITH_APPROVAL."""
        r = dispatch.dispatch_with_autonomy(
            approval_task(), history=[verified_pass() for _ in range(5)], current_level="L4",
            requested_human_approval=False,
        )
        self.assertTrue(r["approval_required"])
        self.assertEqual(r["allowed_action"], "EXECUTE_WITH_APPROVAL")

    def test_untrusted_history_cannot_raise_the_earned_ceiling(self):
        ex = FakeExecutor()
        r = te.governed_run(
            ir_derived_task_packet(), ex,
            history=[{"outcome": "PASS", "deterministic_gate_results": SELF_REPORTED_GATES} for _ in range(5)],
            current_level="L4",
        )
        self.assertEqual(ex.calls, 0)
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertEqual(r["execution_status"], "NOT_PERMITTED")

    def test_deeper_risk_claim_in_intent_does_not_grant_earned_levels(self):
        """A doctored IR claiming DEEP-CHANGE/no-approval still cannot execute
        on an empty history — intent never feeds the earned ladder — and with
        earned history it still cannot skip the human gate."""
        from mpe_ir_mapping import derive_ir_intent  # noqa: PLC0415

        ir = json.loads((ROOT / "experiments" / "exp-002-machine-protocol" / "MPE_IR_FROZEN.json").read_text("utf-8"))
        ir = copy.deepcopy(ir)
        ir["autonomy"]["level"] = "DEEP-CHANGE"
        ir["decision"]["risk_tier"] = "DEEP-CHANGE"
        intent = derive_ir_intent(ir)
        self.assertTrue(intent["requested_human_approval"])

        ex = FakeExecutor()
        r = te.governed_run(
            ir_derived_task_packet(), ex, history=[], current_level="L4",
            requested_human_approval=intent["requested_human_approval"],
        )
        self.assertEqual(ex.calls, 0)
        self.assertEqual(r["execution_status"], "NOT_PERMITTED")
        self.assertEqual(r["allowed_action"], "OBSERVE")
        self.assertEqual(r["earned_recommended_level"], "L0")
        self.assertIn("human_approval_required", r["blocking_reasons"])

        # With earned history the DEEP-CHANGE intent still gates execution.
        ex2 = FakeExecutor()
        r2 = te.governed_run(
            ir_derived_task_packet(), ex2, history=[verified_pass() for _ in range(5)], current_level="L4",
            requested_human_approval=intent["requested_human_approval"],
        )
        self.assertEqual(ex2.calls, 0)
        self.assertEqual(r2["allowed_action"], "EXECUTE_WITH_APPROVAL")
        self.assertEqual(r2["execution_status"], "HUMAN_REQUIRED")


class PositivePathTests(unittest.TestCase):
    """A correct IR/Task Packet passes exactly according to the established
    (Earned Autonomy) policy — nothing more, nothing less."""

    def test_earned_l3_with_recorded_approval_runs_once(self):
        ex = FakeExecutor()
        r = te.governed_run(
            ir_derived_task_packet(), ex, history=[verified_pass() for _ in range(5)],
            current_level="L3", approval_recorded=True,
        )
        self.assertEqual(ex.calls, 1)
        self.assertTrue(r["executor_invoked"])
        self.assertEqual(r["execution_status"], "RAN")

    def test_earned_l4_fast_clear_runs_once(self):
        ex = FakeExecutor()
        r = te.governed_run(
            ir_derived_task_packet(), ex, history=[verified_pass() for _ in range(5)], current_level="L4",
        )
        self.assertEqual(ex.calls, 1)
        self.assertEqual(r["allowed_action"], "EXECUTE")
        self.assertEqual(r["execution_status"], "RAN")

    def test_l3_without_approval_still_requires_human_gate(self):
        ex = FakeExecutor()
        r = te.governed_run(
            ir_derived_task_packet(), ex, history=[verified_pass() for _ in range(5)], current_level="L3",
        )
        self.assertEqual(ex.calls, 0)
        self.assertEqual(r["execution_status"], "HUMAN_REQUIRED")


class HumanApprovalIntentTests(unittest.TestCase):
    """``requires_human_approval: true`` keeps the human gate mandatory — the
    intent TIGHTENS the decision and is never silently dropped."""

    def test_ir_approval_intent_preserves_the_human_gate(self):
        from mpe_ir_mapping import derive_ir_intent  # noqa: PLC0415

        ir = json.loads((ROOT / "experiments" / "exp-002-machine-protocol" / "MPE_IR_FROZEN.json").read_text("utf-8"))
        ir = copy.deepcopy(ir)
        ir["autonomy"]["requires_human_approval"] = True
        intent = derive_ir_intent(ir)
        self.assertTrue(intent["requested_human_approval"])

        # Task content triages to FAST with NO triage-level approval reason.
        self.assertFalse(te.triage(fast_task())["human_approval_required"])
        ex = FakeExecutor()
        r = te.governed_run(
            fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4",
            requested_human_approval=intent["requested_human_approval"],
        )
        self.assertEqual(ex.calls, 0)
        self.assertFalse(r["executor_invoked"])
        self.assertEqual(r["allowed_action"], "EXECUTE_WITH_APPROVAL")
        self.assertEqual(r["acceptance_state"], "HUMAN_REQUIRED")
        self.assertEqual(r["execution_status"], "HUMAN_REQUIRED")
        self.assertIn("human_approval_required", r["blocking_reasons"])
        self.assertTrue(r["requested_human_approval"])
        # The dispatch decision itself records the mandatory human gate.
        d = dispatch.dispatch_with_autonomy(
            fast_task(), history=[verified_pass() for _ in range(5)], current_level="L4",
            requested_human_approval=intent["requested_human_approval"],
        )
        self.assertTrue(d["approval_required"])
        self.assertTrue(d["human_gate_required"])

    def test_ir_approval_intent_gate_opens_only_with_recorded_approval(self):
        ex = FakeExecutor()
        r = te.governed_run(
            fast_task(), ex, history=[verified_pass() for _ in range(5)], current_level="L4",
            requested_human_approval=True, approval_recorded=True,
        )
        self.assertEqual(ex.calls, 1)
        self.assertTrue(r["executor_invoked"])
        self.assertEqual(r["execution_status"], "RAN")

    def test_ir_decision_block_approval_requirement_is_kept(self):
        from mpe_ir_mapping import derive_ir_intent  # noqa: PLC0415

        ir = json.loads((ROOT / "experiments" / "exp-002-machine-protocol" / "MPE_IR_FROZEN.json").read_text("utf-8"))
        ir = copy.deepcopy(ir)
        ir["decision"]["human_approval_required"] = True
        intent = derive_ir_intent(ir)
        self.assertTrue(intent["requested_human_approval"])

    def test_ir_deep_change_intent_requests_human_approval(self):
        from mpe_ir_mapping import derive_ir_intent  # noqa: PLC0415

        ir = json.loads((ROOT / "experiments" / "exp-002-machine-protocol" / "MPE_IR_FROZEN.json").read_text("utf-8"))
        ir = copy.deepcopy(ir)
        ir["autonomy"]["level"] = "DEEP-CHANGE"
        intent = derive_ir_intent(ir)
        self.assertEqual(intent["requested_risk_tier"], "DEEP-CHANGE")
        self.assertTrue(intent["requested_human_approval"])


class EvidenceTrustTests(unittest.TestCase):
    """Self-reported / unknown PASS claims never become trusted evidence and
    never raise the earned ceiling."""

    def test_self_reported_pass_is_not_trusted(self):
        r = earned.evaluate_autonomy(
            [{"outcome": "PASS", "deterministic_gate_results": SELF_REPORTED_GATES} for _ in range(5)],
            current_level="L4",
        )
        self.assertEqual(r["verified_pass_count"], 0)
        self.assertEqual(r["recommended_level"], "L0")

    def test_unknown_evidence_pass_is_not_trusted(self):
        r = earned.evaluate_autonomy(
            [{"outcome": "PASS", "deterministic_gate_results": UNKNOWN_GATES} for _ in range(5)],
            current_level="L4",
        )
        self.assertEqual(r["verified_pass_count"], 0)

    def test_mixed_history_counts_only_trusted_runs(self):
        history = [verified_pass(), {"outcome": "PASS", "deterministic_gate_results": SELF_REPORTED_GATES}]
        r = earned.evaluate_autonomy(history, current_level="L0")
        self.assertEqual(r["verified_pass_count"], 1)
        self.assertEqual(r["recommended_level"], "L1")

    def test_self_reported_history_still_denies_execution(self):
        ex = FakeExecutor()
        r = te.governed_run(
            ir_derived_task_packet(), ex,
            history=[{"outcome": "PASS", "deterministic_gate_results": SELF_REPORTED_GATES} for _ in range(5)],
            current_level="L4",
        )
        self.assertEqual(ex.calls, 0)
        self.assertEqual(r["execution_status"], "NOT_PERMITTED")


class IrIntentMappingContractTests(unittest.TestCase):
    """``scripts/mpe_ir_mapping.derive_ir_intent`` — deterministic, fail-closed
    mapping of the IR intent block to tighten-only governed-entry inputs."""

    def _frozen_ir(self) -> dict:
        return json.loads((ROOT / "experiments" / "exp-002-machine-protocol" / "MPE_IR_FROZEN.json").read_text("utf-8"))

    def test_frozen_ir_maps_to_tighten_only_intent(self):
        from mpe_ir_mapping import derive_ir_intent  # noqa: PLC0415

        intent = derive_ir_intent(self._frozen_ir())
        self.assertEqual(intent["ir_task_id"], "T-001")
        self.assertEqual(intent["requested_risk_tier"], "FAST")
        self.assertFalse(intent["requested_human_approval"])
        self.assertIsNone(intent["authorization"])
        self.assertEqual(intent["semantics"], "intent_only_never_permission")
        # Derivable Task Packet fields only; TRIAGE_INPUT stays closed.
        fields = intent["task_packet_fields"]
        self.assertEqual(set(fields), {
            "task_id", "summary", "affected_repositories", "acceptance_criteria_present",
        })
        self.assertEqual(fields["task_id"], "T-001")
        self.assertEqual(fields["affected_repositories"], ["murat-project-engineer"])
        self.assertTrue(fields["acceptance_criteria_present"])

    def test_most_restrictive_risk_tier_wins_on_conflict(self):
        from mpe_ir_mapping import derive_ir_intent  # noqa: PLC0415

        ir = self._frozen_ir()
        ir["decision"]["risk_tier"] = "VERIFIED"
        ir["autonomy"]["level"] = "FAST"
        self.assertEqual(derive_ir_intent(ir)["requested_risk_tier"], "VERIFIED")
        ir["decision"]["risk_tier"] = "FAST"
        ir["autonomy"]["level"] = "DEEP-CHANGE"
        self.assertEqual(derive_ir_intent(ir)["requested_risk_tier"], "DEEP-CHANGE")

    def test_invalid_ir_fails_closed(self):
        from mpe_ir_mapping import derive_ir_intent  # noqa: PLC0415

        for bad in (None, [], "ir", {}, {"protocol": "other"}):
            with self.assertRaises(ValueError):
                derive_ir_intent(bad)  # type: ignore[arg-type]
        broken = self._frozen_ir()
        del broken["autonomy"]
        with self.assertRaises(ValueError):
            derive_ir_intent(broken)
        broken = self._frozen_ir()
        broken["autonomy"]["level"] = "L4"  # wrong vocabulary: L0-L4 is not IR intent
        with self.assertRaises(ValueError):
            derive_ir_intent(broken)
        broken = self._frozen_ir()
        broken["decision"]["human_approval_required"] = "yes"  # not a bool
        with self.assertRaises(ValueError):
            derive_ir_intent(broken)

    def test_non_bool_requested_approval_fails_closed_in_dispatch(self):
        with self.assertRaises(ValueError):
            dispatch.dispatch_with_autonomy(fast_task(), [], "L4", requested_human_approval="yes")  # type: ignore[arg-type]


class GovernedEntryCliTests(unittest.TestCase):
    """End-to-end via the real CLI entry (triage_engine.py)."""

    def _run(self, *extra: str, history=None) -> dict:
        with __import__("tempfile").TemporaryDirectory() as tmp:
            task_path = Path(tmp) / "task.json"
            task_path.write_text(json.dumps(ir_derived_task_packet()), encoding="utf-8")
            cmd = [sys.executable, str(ROOT / "scripts" / "triage_engine.py"), str(task_path), *extra]
            if history is not None:
                hist_path = Path(tmp) / "history.json"
                hist_path.write_text(json.dumps(history), encoding="utf-8")
                cmd += ["--history-file", str(hist_path)]
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    def test_cli_governed_run_still_denies_empty_history(self):
        out = self._run("--governed-run")
        self.assertFalse(out["executor_invoked"])
        self.assertEqual(out["execution_status"], "NOT_PERMITTED")

    def test_cli_requested_human_approval_flag_keeps_gate(self):
        out = self._run(
            "--governed-run", "--level", "L4", "--requested-human-approval",
            history=[verified_pass() for _ in range(5)],
        )
        self.assertFalse(out["executor_invoked"])
        self.assertTrue(out["requested_human_approval"])
        self.assertIn("human_approval_required", out["blocking_reasons"])
        self.assertEqual(out["execution_status"], "HUMAN_REQUIRED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
