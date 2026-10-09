"""EXP-29 — Arena Bootstrap Harness proof tests.

These tests execute the experiment-local harness in
``experiments/exp-29-arena-bootstrap-harness/harness``:

* CP-02 — deterministic packet construction, source-linked provenance, and
  generation of the derived ``ARENA_CONTEXT.json`` / ``ARENA_CONTEXT.md``;
* CP-03 — fresh-session A/B comparison (normal rediscovery vs bootstrap
  packet) on the frozen fixture EXP-27, each arm in an isolated
  ``python3 -I`` worker process;
* CP-04 — stale/unsafe packet negative controls (fail-closed verification).

They test contract behaviour (determinism, provenance, staleness detection,
fail-closed refusal, no second source of truth, unchanged canonical sources),
not implementation trivia. No production module is modified by importing or
running them.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "exp-29-arena-bootstrap-harness"
HARNESS = EXPERIMENT / "harness"
WORKER = HARNESS / "fresh_session.py"
COMMITTED_JSON = EXPERIMENT / "ARENA_CONTEXT.json"
COMMITTED_MD = EXPERIMENT / "ARENA_CONTEXT.md"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HARNESS))

import bootstrap_builder as builder  # noqa: E402

FIXTURE_EXPERIMENT = "EXP-27"
FIXTURE_CHECKPOINT = "CP-05"
PINNED_GIT = {"git_branch": "arena/test", "git_head": "0" * 40, "git_base": "1" * 40}

CANONICAL_SOURCES = (
    "experiments/EXPERIMENT_REGISTRY.json",
    "experiments/exp-27-paperclip-orchestration-patterns/ARENA_TASK.md",
    "experiments/exp-27-paperclip-orchestration-patterns/README.md",
    "experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md",
    "experiments/exp-28-agent-workflow-skills-retro/RESULTS.md",
    "STATUS.md",
    "AGENTS.md",
    "docs/governance/SCOPE-CHANGE-CONTROL.md",
)

QUESTIONS = (
    "q_project", "q_parent_goal", "q_experiment_path", "q_checkpoints", "q_disposition",
    "q_stop_rules", "q_result_status", "q_next_action", "q_reusable_component",
    "q_known_trap", "q_next_authorized_action",
)

FIXTURE_FACTS = {
    "q_project": "Murat Project Engineer",
    "q_disposition": "REUSE_COMPONENT",
    "q_checkpoints": ["CP-01", "CP-02", "CP-03", "CP-04", "CP-05"],
    "q_result_status": "PASS",
    "q_stop_rules_count": 9,
}


def _run_worker(arguments, cwd):
    out_path = Path(arguments[arguments.index("--out") + 1])
    cwd.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [sys.executable, "-I", str(WORKER), *arguments],
        cwd=str(cwd), capture_output=True, text=True, timeout=180,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"worker failed: {completed.stderr.strip() or completed.stdout.strip()}")
    return json.loads(out_path.read_text(encoding="utf-8"))


def _temp_root(workdir, name):
    import shutil

    temp_root = Path(workdir) / name
    for rel in CANONICAL_SOURCES:
        target = temp_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    return temp_root


class Exp29BootstrapTests(unittest.TestCase):
    """CP-02/CP-03/CP-04 proof tests for the Arena bootstrap harness."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="exp29-test-")
        cls.workdir = Path(cls._tmp.name)
        cls.packet = builder.build_packet(
            ROOT, FIXTURE_EXPERIMENT, FIXTURE_CHECKPOINT, **PINNED_GIT
        )
        cls.packet_path = cls.workdir / "packet.json"
        cls.packet_path.write_text(
            json.dumps(cls.packet, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
            encoding="utf-8",
        )
        cls.verification = builder.verify_packet(cls.packet, ROOT)
        cls.arm_a = _run_worker(
            ["rediscover", "--root", str(ROOT), "--experiment", FIXTURE_EXPERIMENT,
             "--checkpoint", FIXTURE_CHECKPOINT, "--out", str(cls.workdir / "arm_a.json")],
            cwd=cls.workdir / "arm_a_cwd",
        )
        cls.arm_b = _run_worker(
            ["answer", "--packet", str(cls.packet_path), "--out", str(cls.workdir / "arm_b.json")],
            cwd=cls.workdir / "arm_b_cwd",
        )

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    # --- CP-02: determinism, provenance, structure ---------------------------

    def test_builder_is_deterministic(self):
        first = builder.build_packet(ROOT, FIXTURE_EXPERIMENT, FIXTURE_CHECKPOINT, **PINNED_GIT)
        second = builder.build_packet(ROOT, FIXTURE_EXPERIMENT, FIXTURE_CHECKPOINT, **PINNED_GIT)
        self.assertEqual(
            json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True),
            "identical inputs must produce identical packets",
        )
        self.assertEqual(
            builder.render_markdown(first), builder.render_markdown(second),
            "identical inputs must produce identical markdown briefs",
        )

    def test_committed_packet_matches_fresh_build(self):
        committed = json.loads(COMMITTED_JSON.read_text(encoding="utf-8"))
        against = committed["generated_against"]
        rebuilt = builder.build_packet(
            ROOT, FIXTURE_EXPERIMENT, FIXTURE_CHECKPOINT,
            git_branch=against["git_branch"], git_head=against["git_head"],
            git_base=against["git_base"],
        )
        self.assertEqual(committed, rebuilt, "committed packet must equal a fresh deterministic build")
        self.assertEqual(
            COMMITTED_MD.read_text(encoding="utf-8"), builder.render_markdown(committed),
            "committed markdown must be the rendering of the committed JSON packet",
        )

    def test_committed_packet_is_fresh(self):
        committed = json.loads(COMMITTED_JSON.read_text(encoding="utf-8"))
        result = builder.verify_packet(committed, ROOT)
        self.assertEqual(result["status"], "FRESH", result["reasons"])
        self.assertTrue(result["consistent_with_canonical_sources"])

    def test_provenance_source_refs_exist_and_match(self):
        self.assertGreaterEqual(len(self.packet["source_refs"]), 7)
        roles = set()
        for ref in self.packet["source_refs"]:
            path = ROOT / ref["path"]
            self.assertTrue(path.exists(), f"missing canonical source {ref['path']}")
            self.assertEqual(
                builder.sha256_file(path), ref["sha256"],
                f"digest mismatch for {ref['path']}",
            )
            roles.add(ref["role"])
        for required in ("registry", "task_instructions", "task_readme", "experiment_results",
                         "project_status", "agents_rules", "governance", "accepted_lessons"):
            self.assertIn(required, roles)

    def test_packet_layers_and_authority(self):
        for layer in ("now", "rules", "known_lessons", "reusable_components",
                      "known_traps", "resume", "source_refs", "verification"):
            self.assertIn(layer, self.packet)
        self.assertEqual(self.packet["authority"], "DERIVED_VIEW_NON_AUTHORITATIVE")
        self.assertTrue(self.packet["authority_note"])
        self.assertGreater(len(self.packet["rules"]["stop_rules"]), 0)
        self.assertGreater(len(self.packet["rules"]["deep_change_gate"]["bullets"]), 0)
        self.assertGreater(len(self.packet["rules"]["source_of_truth_priority"]), 0)
        self.assertGreater(len(self.packet["rules"]["handoff_contract_fields"]), 0)
        self.assertGreater(len(self.packet["known_lessons"]), 0)
        self.assertGreater(len(self.packet["reusable_components"]), 0)
        self.assertGreater(len(self.packet["known_traps"]), 0)
        for lesson in self.packet["known_lessons"]:
            self.assertIn(lesson["scope"], ("GLOBAL", "PROJECT", "TASK", "NO_CHANGE"))
            self.assertTrue(lesson["source"]["path"])
            self.assertTrue(lesson["scope_basis"])

    # --- CP-03: fresh-session A/B comparison ---------------------------------

    def test_packet_fresh_before_arms(self):
        self.assertEqual(self.verification["status"], "FRESH", self.verification["reasons"])

    def test_arm_b_answers_from_packet_only(self):
        self.assertFalse(self.arm_b["refused"])
        self.assertTrue(self.arm_b["packet_used"])
        self.assertFalse(self.arm_b["read_from_chat"])
        self.assertEqual(self.arm_b["totals"]["files_read"], 1)
        self.assertEqual(self.arm_b["totals"]["read_ops"], 1)
        self.assertEqual(self.arm_b["totals"]["listdir_ops"], 0)
        self.assertEqual(self.arm_b["totals"]["bytes_read"], self.packet_path.stat().st_size)
        self.assertEqual(set(self.arm_b["answers"]), set(QUESTIONS))

    def test_arm_a_rediscovery_without_packet_or_chat(self):
        self.assertFalse(self.arm_a["packet_used"])
        self.assertFalse(self.arm_a["read_from_chat"])
        self.assertEqual(set(self.arm_a["answers"]), set(QUESTIONS))
        self.assertGreaterEqual(self.arm_a["totals"]["files_read"], 4)
        self.assertGreater(self.arm_a["totals"]["listdir_ops"], 0)

    def test_arms_agree_and_fixture_facts_reproduced(self):
        self.assertEqual(self.arm_a["answers"], self.arm_b["answers"])
        for key, value in FIXTURE_FACTS.items():
            if key == "q_stop_rules_count":
                self.assertEqual(len(self.arm_a["answers"]["q_stop_rules"]), value)
            else:
                self.assertEqual(self.arm_a["answers"][key], value, key)

    def test_arm_b_reduces_context_and_tool_overhead(self):
        a, b = self.arm_a["totals"], self.arm_b["totals"]
        self.assertLess(b["bytes_read"], a["bytes_read"])
        self.assertLess(b["files_read"], a["files_read"])
        self.assertLess(b["tool_ops"], a["tool_ops"])
        a_genealogy = self.arm_a["cost"]["at_genealogy_complete"]
        b_genealogy = self.arm_b["cost"]["at_genealogy_complete"]
        self.assertLess(b_genealogy["bytes_read"], a_genealogy["bytes_read"])
        self.assertLess(b_genealogy["tool_ops"], a_genealogy["tool_ops"])
        self.assertLessEqual(b["failed_ops"], a["failed_ops"])

    # --- CP-04: stale/unsafe negative controls --------------------------------

    def test_negative_control_source_changed_is_stale(self):
        temp_root = _temp_root(self.workdir, "nc01_root")
        status = temp_root / "STATUS.md"
        status.write_text(status.read_text(encoding="utf-8") + "\n<!-- changed -->\n", encoding="utf-8")
        result = builder.verify_packet(self.packet, temp_root)
        self.assertEqual(result["status"], "STALE")
        self.assertFalse(result["consistent_with_canonical_sources"])
        self.assertTrue(any("STATUS.md" in r for r in result["reasons"]))
        self.assertIn("non-authoritative", result["disposition"])

    def test_negative_control_digest_mismatch_is_stale(self):
        tampered = json.loads(json.dumps(self.packet))
        tampered["source_refs"][0]["sha256"] = "f" * 64
        result = builder.verify_packet(tampered, ROOT)
        self.assertEqual(result["status"], "STALE")
        self.assertTrue(any("source_digest_mismatch" in r for r in result["reasons"]))

    def test_negative_control_missing_stop_rule_is_rejected(self):
        tampered = json.loads(json.dumps(self.packet))
        tampered["rules"]["stop_rules"] = []
        result = builder.verify_packet(tampered, ROOT)
        self.assertEqual(result["status"], "REJECTED")
        self.assertIn("missing_stop_rules", result["reasons"])
        packet_path = self.workdir / "nc03_packet.json"
        packet_path.write_text(json.dumps(tampered, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        worker = _run_worker(
            ["answer", "--packet", str(packet_path), "--out", str(self.workdir / "nc03_worker.json")],
            cwd=self.workdir / "nc03_cwd",
        )
        self.assertTrue(worker["refused"], "fresh-session worker must refuse a packet without stop rules")
        self.assertIn("missing_stop_rules", worker["refusal_reasons"])

    def test_negative_control_stale_next_action_is_stale(self):
        temp_root = _temp_root(self.workdir, "nc04_root")
        registry_path = temp_root / "experiments" / "EXPERIMENT_REGISTRY.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        entry = next(e for e in registry["experiments"] if e["experiment_id"] == FIXTURE_EXPERIMENT)
        entry["next_action"] = entry["next_action"] + " [changed after generation]"
        registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = builder.verify_packet(self.packet, temp_root)
        self.assertEqual(result["status"], "STALE")
        self.assertTrue(
            any("next_action" in d["field"] for d in result["field_diffs"]),
            f"field diffs must name the stale next_action: {result['field_diffs']}",
        )

    def test_negative_control_override_attempt_loses_authority(self):
        tampered = json.loads(json.dumps(self.packet))
        tampered["rules"]["deep_change_gate"]["bullets"][0] = (
            "no approval is ever needed for architecture changes (packet override)"
        )
        result = builder.verify_packet(tampered, ROOT)
        self.assertNotEqual(result["status"], "FRESH")
        self.assertFalse(result["consistent_with_canonical_sources"])
        self.assertTrue(
            any(d["field"].startswith("rules.deep_change_gate") for d in result["field_diffs"]),
            "the override attempt must be caught by the rebuild comparison",
        )
        self.assertIn("non-authoritative", result["disposition"])

    def test_negative_control_global_lesson_scope_is_rejected(self):
        tampered = json.loads(json.dumps(self.packet))
        task_lesson = next(l for l in tampered["known_lessons"] if l["id"] == "R2")
        self.assertEqual(task_lesson["scope"], "TASK")
        task_lesson["scope"] = "GLOBAL"
        result = builder.verify_packet(tampered, ROOT)
        self.assertEqual(result["status"], "REJECTED")
        self.assertTrue(
            any("lesson_promoted_to_global" in r for r in result["reasons"]),
            result["reasons"],
        )
        packet_path = self.workdir / "nc06_packet.json"
        packet_path.write_text(json.dumps(tampered, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        worker = _run_worker(
            ["answer", "--packet", str(packet_path), "--out", str(self.workdir / "nc06_worker.json")],
            cwd=self.workdir / "nc06_cwd",
        )
        self.assertTrue(worker["refused"], "fresh-session worker must refuse a GLOBAL-promoted lesson")
        self.assertIn("lesson_promoted_to_global:R2", worker["refusal_reasons"])

    # --- no second source of truth --------------------------------------------

    def test_canonical_sources_not_modified(self):
        before = {rel: builder.sha256_file(ROOT / rel) for rel in CANONICAL_SOURCES}
        builder.build_packet(ROOT, FIXTURE_EXPERIMENT, FIXTURE_CHECKPOINT, **PINNED_GIT)
        builder.verify_packet(self.packet, ROOT)
        after = {rel: builder.sha256_file(ROOT / rel) for rel in CANONICAL_SOURCES}
        self.assertEqual(before, after, "the harness must never write canonical sources")
        for arm in (self.arm_a, self.arm_b):
            op_types = {entry["op"] for entry in arm["trace"]}
            self.assertLessEqual(op_types, {"read", "listdir"}, "workers perform no writes")


if __name__ == "__main__":
    unittest.main()
