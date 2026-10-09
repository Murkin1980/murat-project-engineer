"""EXP-29 — Arena Bootstrap Harness proof tests.

These tests execute the experiment-local harness in
``experiments/exp-29-arena-bootstrap-harness/harness``:

* CP-02 — deterministic packet construction, source-linked provenance, and
  generation of the derived ``ARENA_CONTEXT.json`` / ``ARENA_CONTEXT.md``;
* CP-03 — fresh-session A/B comparison (normal rediscovery vs bootstrap
  packet) on the frozen fixture EXP-27, each arm in an isolated
  ``python3 -I`` worker process;
* CP-04 — stale/unsafe packet negative controls (fail-closed verification);
* CP-06 — first real-use repair: H-1 stop-rule boundary sections, H-2 source-true
  markdown labels, H-3 README-declared checkpoint chain / disposition, using
  EXP-22-shaped fixtures plus the EXP-27 fixture, and a live EXP-22/CP-01 FRESH check;
* CP-07 — canonical current-state gap: the EXP-22 registry entry + RESULTS.md carry
  the truthful PARTIAL / HOLD state, the rebuilt EXP-22/CP-01 packet is FRESH *and*
  current, and an isolated state consumer answers the six state questions from the
  packet alone (never from FINDINGS.md).

They test contract behaviour (determinism, provenance, staleness detection,
fail-closed refusal, no second source of truth, unchanged canonical sources),
not implementation trivia. No production module is modified by importing or
running them.
"""

import json
import shutil
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

# --- CP-06: first real-use repair (H-1 / H-2 / H-3) ---------------------------

SHARED_SOURCES = (
    "STATUS.md",
    "AGENTS.md",
    "docs/governance/SCOPE-CHANGE-CONTROL.md",
    "experiments/exp-28-agent-workflow-skills-retro/RESULTS.md",
)

EXP22_PATH = "experiments/exp-22-colibri-local-inference"

# EXP-22-shaped fixture: the same heading and declaration structure as the canonical
# EXP-22 files that failed the first real-use run (Boundaries with Allowed / Not
# allowed lists, README-declared Decision and CP-01..03, Failure / stop criteria,
# Guardrails, and no RESULTS.md yet).
EXP22_TASK = """# Arena task — EXP-22 Colibri (fixture)

## Before changing code

Report the reuse decision first.

If a deep-change is required, STOP and report it. Do not implement it.

## Boundaries

Allowed:
- files under `experiments/exp-22-colibri-local-inference/`;
- read-only inspection of existing project code;

Not allowed:
- new repository;
- production deployment;

## Deliverable

Write the result.
"""

EXP22_README = """# EXP-22 — Colibri local inference / Brio routing (fixture)

Status: PLANNED
Decision: EXPERIMENT

## Experiment scope

### CP-01 — Brio status classifier

Classify the status.

### CP-02 — Agent routing decision

Decide the routing.

### CP-03 — Existing-provider compatibility

Check compatibility.

## Failure / stop criteria

STOP or FAIL if:
- setup cost exceeds the value of the narrow task;
- Arena discovers a deep-change requirement;

## Guardrails

- No production traffic.
- No secrets committed.
"""


def _real_use_root(workdir, name, *, task=EXP22_TASK, readme=EXP22_README, results=None):
    """Temp repo root: real shared canonical sources plus an EXP-22-shaped experiment."""
    root = Path(workdir) / name
    for rel in SHARED_SOURCES:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    registry = root / "experiments" / "EXPERIMENT_REGISTRY.json"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps({"experiments": [{
        "experiment_id": "EXP-22",
        "name": "Colibri local inference / Brio routing",
        "owning_project": "Murat Project Engineer",
        "status": "PLANNED",
        "why": "Evaluate Colibri as a bounded local inference provider.",
        "next_action": "Run CP-01.",
        "experiment_path": EXP22_PATH,
        "updated_at": "2026-10-09",
    }]}, indent=2) + "\n", encoding="utf-8")
    experiment = root / EXP22_PATH
    experiment.mkdir(parents=True, exist_ok=True)
    (experiment / "ARENA_TASK.md").write_text(task, encoding="utf-8")
    (experiment / "README.md").write_text(readme, encoding="utf-8")
    if results is not None:
        (experiment / "RESULTS.md").write_text(results, encoding="utf-8")
    return root


class Exp29RealUseRepairTests(unittest.TestCase):
    """CP-06 regression tests for the three defects found by the first real-use run."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="exp29-cp06-")
        cls.workdir = Path(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def _packet(self, root, checkpoint="CP-01"):
        return builder.build_packet(root, "EXP-22", checkpoint, **PINNED_GIT)

    # H-1 — stop-rule parser must read real boundary sections, fail closed otherwise

    def test_h1_boundary_sections_yield_stop_rules_and_verify_fresh(self):
        root = _real_use_root(self.workdir, "h1_boundaries")
        packet = self._packet(root)
        rules = packet["rules"]["stop_rules"]
        self.assertIn("new repository;", rules, "ARENA_TASK ## Boundaries (Not allowed) is a stop rule")
        self.assertIn("setup cost exceeds the value of the narrow task;", rules,
                      "README ## Failure / stop criteria is a stop rule")
        self.assertIn("No production traffic.", rules, "README ## Guardrails is a boundary rule")
        self.assertFalse(
            any(rule.startswith("files under") for rule in rules),
            "Allowed items are permissions, not stop rules",
        )
        for anchor in ("ARENA_TASK.md#boundaries", "README.md#failure-stop-criteria",
                       "README.md#guardrails"):
            self.assertIn(anchor, packet["rules"]["stop_rules_source"])
        result = builder.verify_packet(packet, root)
        self.assertEqual(result["status"], "FRESH", result["reasons"])

    def test_h1_prose_only_boundaries_stay_fail_closed(self):
        task = (
            "# Arena task — EXP-22 (fixture)\n\n"
            "## Boundaries\n\n"
            "No new repository and no production deployment are allowed.\n"
        )
        readme = (
            "# EXP-22 (fixture)\n\nDecision: EXPERIMENT  \n\n"
            "### CP-01 — Brio status classifier\n\n"
            "## Failure / stop criteria\n\n"
            "Stop the run if the setup cost is too high.\n"
        )
        root = _real_use_root(self.workdir, "h1_prose", task=task, readme=readme)
        packet = self._packet(root)
        self.assertEqual(packet["rules"]["stop_rules"], [])
        result = builder.verify_packet(packet, root)
        self.assertEqual(result["status"], "REJECTED")
        self.assertIn("missing_stop_rules", result["reasons"])

    def test_h1_allowed_list_alone_is_not_a_stop_rule(self):
        task = (
            "# Arena task (fixture)\n\n"
            "## Boundaries\n\n"
            "Allowed:\n"
            "- files under `experiments/exp-22-colibri-local-inference/`;\n"
            "- read-only inspection;\n"
        )
        readme = "# EXP-22 (fixture)\n\nDecision: EXPERIMENT  \n\n### CP-01 — x\n"
        root = _real_use_root(self.workdir, "h1_allowed_only", task=task, readme=readme)
        packet = self._packet(root)
        self.assertEqual(packet["rules"]["stop_rules"], [])
        self.assertEqual(builder.verify_packet(packet, root)["status"], "REJECTED")

    # H-2 — markdown labels describe the packet's actual sources

    def test_h2_labels_describe_the_actual_sources_when_no_results_exist(self):
        root = _real_use_root(self.workdir, "h2_no_results")
        markdown = builder.render_markdown(self._packet(root))
        headings = [line for line in markdown.splitlines() if line.startswith("## ")]
        self.assertIn("## REUSABLE COMPONENTS (no experiment RESULTS.md present)", headings)
        self.assertIn(
            "## KNOWN TRAPS (verified limitations, no experiment RESULTS.md present)", headings,
        )
        self.assertFalse(any("EXP-27" in heading for heading in headings), headings)
        self.assertIn(
            "## KNOWN LESSONS (evidence-gated, from "
            "experiments/exp-28-agent-workflow-skills-retro/RESULTS.md)",
            headings,
        )

    def test_h2_labels_name_the_experiment_results_when_present(self):
        results = (
            "# EXP-22 — Results (fixture)\n\n"
            "## Per-pattern disposition\n\n"
            "| # | Pattern | Verdict | Disposition |\n"
            "|---|---|---|---|\n"
            "| 1 | Brio status classifier | BORROW | REUSE_COMPONENT |\n\n"
            "## Known limitations / blockers\n\n"
            "- Provider latency is unmeasured.\n"
        )
        root = _real_use_root(self.workdir, "h2_with_results", results=results)
        packet = self._packet(root)
        markdown = builder.render_markdown(packet)
        self.assertIn(f"## REUSABLE COMPONENTS (from {EXP22_PATH}/RESULTS.md)", markdown)
        self.assertIn(
            f"## KNOWN TRAPS (verified limitations, from {EXP22_PATH}/RESULTS.md)", markdown,
        )
        self.assertEqual(packet["reusable_components"][0]["pattern"], "Brio status classifier")
        self.assertEqual(packet["known_traps"][0]["trap"], "Provider latency is unmeasured.")

    # H-3 — checkpoint chain and disposition read the README-declared fields

    def test_h3_checkpoint_chain_and_disposition_come_from_the_readme(self):
        root = _real_use_root(self.workdir, "h3_genealogy")
        packet = self._packet(root)
        self.assertEqual(packet["now"]["checkpoints"], ["CP-01", "CP-02", "CP-03"])
        self.assertEqual(packet["now"]["disposition"], "EXPERIMENT")
        self.assertEqual(
            packet["now"]["disposition_sources"],
            [{"path": f"{EXP22_PATH}/README.md", "value": "EXPERIMENT"}],
        )
        self.assertEqual(builder.verify_packet(packet, root)["status"], "FRESH")

    def test_h3_conflicting_disposition_is_rejected_not_silently_resolved(self):
        task = EXP22_TASK.replace(
            "## Before changing code",
            "Decision: **REUSE_COMPONENT**\n\n## Before changing code",
            1,
        )
        root = _real_use_root(self.workdir, "h3_conflict", task=task)
        packet = self._packet(root)
        result = builder.verify_packet(packet, root)
        self.assertEqual(result["status"], "REJECTED")
        self.assertIn("ambiguous_disposition", result["reasons"])
        self.assertFalse(result["checks"]["disposition_unambiguous"])
        packet_path = self.workdir / "h3_conflict_packet.json"
        packet_path.write_text(json.dumps(packet, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        worker = _run_worker(
            ["answer", "--packet", str(packet_path), "--out", str(self.workdir / "h3_worker.json")],
            cwd=self.workdir / "h3_cwd",
        )
        self.assertTrue(worker["refused"], "fresh-session worker must refuse a conflicting disposition")
        self.assertIn("ambiguous_disposition", worker["refusal_reasons"])

    # Real-use and fixture preservation

    def test_exp22_cp01_bootstrap_is_fresh_from_live_git_sources(self):
        packet = builder.build_packet(ROOT, "EXP-22", "CP-01", **PINNED_GIT)
        result = builder.verify_packet(packet, ROOT)
        self.assertEqual(result["status"], "FRESH", result["reasons"] or result["field_diffs"])
        self.assertEqual(packet["now"]["checkpoints"], ["CP-01", "CP-02", "CP-03"])
        self.assertEqual(packet["now"]["disposition"], "EXPERIMENT")
        self.assertTrue(packet["rules"]["stop_rules"])
        markdown = builder.render_markdown(packet)
        self.assertFalse(
            any("EXP-27" in line for line in markdown.splitlines() if line.startswith("## ")),
        )

    def test_exp27_fixture_rules_genealogy_and_labels_are_preserved(self):
        packet = builder.build_packet(ROOT, FIXTURE_EXPERIMENT, FIXTURE_CHECKPOINT, **PINNED_GIT)
        self.assertEqual(len(packet["rules"]["stop_rules"]), 9)
        self.assertEqual(
            packet["rules"]["stop_rules_source"],
            "experiments/exp-27-paperclip-orchestration-patterns/README.md#stop-conditions",
        )
        self.assertEqual(packet["now"]["checkpoints"], FIXTURE_FACTS["q_checkpoints"])
        self.assertEqual(packet["now"]["disposition"], FIXTURE_FACTS["q_disposition"])
        markdown = builder.render_markdown(packet)
        self.assertIn(
            "## REUSABLE COMPONENTS "
            "(from experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md)",
            markdown,
        )
        self.assertEqual(builder.verify_packet(packet, ROOT)["status"], "FRESH")


# --- CP-07: canonical current-state gap (registry + RESULTS repair) -------------

STATE_ANSWERS = {
    "q_state_result_status": "PARTIAL",
    "q_state_completed_checkpoints": ["CP-01", "CP-02", "CP-03"],
    "q_state_recommendation": "HOLD",
    "q_state_should_cp01_run_again": "NO",
}

PRE_CHANGE_PACKET = (
    ROOT / "experiments" / "exp-22-colibri-local-inference" / "evidence" / "bootstrap"
    / "cp07" / "pre_change_packet.json"
)


class Exp29CanonicalStateTests(unittest.TestCase):
    """CP-07: the FRESH-but-stale-state gap is closed through the registry + RESULTS path."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="exp29-cp07-")
        cls.workdir = Path(cls._tmp.name)
        cls.packet = builder.build_packet(ROOT, "EXP-22", "CP-01", **PINNED_GIT)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def _state_worker(self, packet, name):
        packet_path = self.workdir / f"{name}.json"
        packet_path.write_text(
            json.dumps(packet, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
            encoding="utf-8",
        )
        return _run_worker(
            ["state", "--packet", str(packet_path), "--out", str(self.workdir / f"{name}_state.json")],
            cwd=self.workdir / f"{name}_cwd",
        )

    def test_registry_entry_records_the_current_state(self):
        registry = json.loads(
            (ROOT / "experiments" / "EXPERIMENT_REGISTRY.json").read_text(encoding="utf-8")
        )
        entry = next(e for e in registry["experiments"] if e["experiment_id"] == "EXP-22")
        self.assertEqual(entry["status"], "PARTIAL")
        self.assertIn("RESULT: PARTIAL", entry["result_summary"])
        self.assertIn("RECOMMENDATION: HOLD", entry["result_summary"])
        self.assertIn("Executed checkpoints: CP-01, CP-02, CP-03", entry["result_summary"])
        self.assertIn("NOT measured", entry["result_summary"])
        self.assertIn("Do not repeat CP-01", entry["next_action"])
        self.assertIn("released 842 MB Laya checkpoint", entry["next_action"])
        self.assertEqual(entry["updated_at"], "2026-10-09")

    def test_exp22_results_md_follows_the_result_convention(self):
        results_path = ROOT / "experiments" / "exp-22-colibri-local-inference" / "RESULTS.md"
        self.assertTrue(results_path.is_file())
        text = results_path.read_text(encoding="utf-8")
        self.assertIn("RESULT: **PARTIAL**", text)
        self.assertIn("RECOMMENDATION: **HOLD**", text)
        self.assertIn("## Next authorized action", text)
        self.assertIn("## Known limitations / blockers", text)
        self.assertIn("## Per-pattern disposition", text)
        packet = self.packet
        self.assertTrue(packet["known_traps"])
        self.assertTrue(packet["reusable_components"])
        self.assertIn("released 842 MB Laya checkpoint", packet["resume"]["next_authorized_action"])

    def test_exp22_cp01_bootstrap_is_fresh_and_reports_current_state(self):
        result = builder.verify_packet(self.packet, ROOT)
        self.assertEqual(result["status"], "FRESH", result["reasons"] or result["field_diffs"])
        now, resume = self.packet["now"], self.packet["resume"]
        self.assertEqual(now["registry_status"], "PARTIAL")
        self.assertEqual(resume["status"], "PARTIAL")
        self.assertIn("RESULT: PARTIAL", resume["result_summary"])
        self.assertIn("Do not repeat CP-01", resume["next_action"])
        serialized = json.dumps({"now": now, "resume": resume}, ensure_ascii=False)
        self.assertNotIn('"PLANNED"', serialized)
        self.assertNotIn("Planned.", serialized)
        self.assertNotIn("execute CP-01 READY", serialized)

    def test_state_consumer_answers_from_packet_without_findings(self):
        worker = self._state_worker(self.packet, "state_live")
        self.assertFalse(worker["refused"])
        answers = worker["answers"]
        for key, value in STATE_ANSWERS.items():
            self.assertEqual(answers[key], value, key)
        self.assertIn("NOT measured", answers["q_state_blocker"])
        self.assertIn("released 842 MB Laya checkpoint", answers["q_state_next_authorized_action"])
        self.assertEqual(worker["totals"]["files_read"], 1)
        self.assertEqual(worker["totals"]["tool_ops"], 1)
        self.assertFalse(any("FINDINGS" in entry["path"] for entry in worker["trace"]))
        self.assertFalse(worker["read_from_chat"])

    def test_state_consumer_refuses_unsafe_packets(self):
        tampered = json.loads(json.dumps(self.packet))
        tampered["rules"]["stop_rules"] = []
        worker = self._state_worker(tampered, "state_unsafe")
        self.assertTrue(worker["refused"], "state consumer must keep fail-closed refusal")
        self.assertIn("missing_stop_rules", worker["refusal_reasons"])
        self.assertEqual(worker["answers"], {})

    def test_prechange_packet_reproduces_the_stale_state_gap(self):
        self.assertTrue(PRE_CHANGE_PACKET.is_file(), "committed reproduction evidence")
        pre = json.loads(PRE_CHANGE_PACKET.read_text(encoding="utf-8"))
        self.assertEqual(pre["now"]["registry_status"], "PLANNED")
        self.assertIn("execute CP-01", pre["now"]["nearest_action"])
        worker = self._state_worker(pre, "state_prechange")
        self.assertFalse(worker["refused"], "the stale packet was technically FRESH, not refused")
        self.assertEqual(worker["answers"]["q_state_result_status"], "PLANNED")
        self.assertEqual(worker["answers"]["q_state_completed_checkpoints"], [])
        self.assertEqual(
            worker["answers"]["q_state_should_cp01_run_again"], "YES",
            "the stale packet would have re-run CP-01 — the exact CP-07 trigger",
        )

    def test_exp27_regression_state_and_fixture_untouched(self):
        packet = builder.build_packet(ROOT, FIXTURE_EXPERIMENT, FIXTURE_CHECKPOINT, **PINNED_GIT)
        self.assertEqual(builder.verify_packet(packet, ROOT)["status"], "FRESH")
        self.assertEqual(packet["now"]["registry_status"], "PASS")
        self.assertEqual(packet["now"]["checkpoints"], FIXTURE_FACTS["q_checkpoints"])


if __name__ == "__main__":
    unittest.main()
