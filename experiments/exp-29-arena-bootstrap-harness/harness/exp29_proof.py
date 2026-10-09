#!/usr/bin/env python3
"""EXP-29 — Arena Bootstrap Harness proof (CP-02 … CP-04).

Produces every measurement quoted in ``RESULTS.md`` and stores them in
``evidence/``. Experiment-scoped: no production script, contract, gate,
governance document, or source of truth is modified; the only repository files
written are the two derived artifacts ``ARENA_CONTEXT.json`` / ``ARENA_CONTEXT.md``
in this experiment's directory. No daemon, service, database, network, or LLM is
used; packet construction is deterministic.

Checkpoints:

- CP-02 — determinism, provenance, and generation of the derived artifacts;
- CP-03 — fresh-session A/B comparison on the frozen fixture (EXP-27, a real
  completed context-heavy MPE task): Arm A (normal rediscovery) vs Arm B
  (bootstrap packet), each in an isolated ``python3 -I`` worker process;
- CP-04 — stale/unsafe packet negative controls (fail-closed verification) plus
  canonical-source immutability.

Usage:
    python3 experiments/exp-29-arena-bootstrap-harness/harness/exp29_proof.py all
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = HARNESS_DIR.parent
ROOT = HARNESS_DIR.parents[2]
EVIDENCE_DIR = EXPERIMENT_DIR / "evidence"
WORKER_PATH = HARNESS_DIR / "fresh_session.py"

sys.path.insert(0, str(HARNESS_DIR))

import bootstrap_builder as builder  # noqa: E402

# Frozen fixture: one real, already completed context-heavy MPE task.
FIXTURE = {"experiment_id": "EXP-27", "checkpoint": "CP-05"}

# Canonical sources the builder derives from (must never be written by EXP-29).
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

DERIVED_ARTIFACTS = (
    "experiments/exp-29-arena-bootstrap-harness/ARENA_CONTEXT.json",
    "experiments/exp-29-arena-bootstrap-harness/ARENA_CONTEXT.md",
)

PINNED_GIT = {"git_branch": "arena/proof", "git_head": "0" * 40, "git_base": "1" * 40}

QUESTIONS = (
    "q_project", "q_parent_goal", "q_experiment_path", "q_checkpoints", "q_disposition",
    "q_stop_rules", "q_result_status", "q_next_action", "q_reusable_component",
    "q_known_trap", "q_next_authorized_action",
)

# Hardcoded fixture expectations (independent of the builder's parsers).
FIXTURE_FACTS = {
    "q_project": "Murat Project Engineer",
    "q_disposition": "REUSE_COMPONENT",
    "q_checkpoints": ["CP-01", "CP-02", "CP-03", "CP-04", "CP-05"],
    "q_result_status": "PASS",
    "q_stop_rules_count": 9,
}


def _write_json(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                      encoding="utf-8")
    return target


def _log(message):
    print(message, flush=True)


def _run_worker(arguments, cwd):
    out_path = Path(arguments[arguments.index("--out") + 1])
    cwd.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-I", str(WORKER_PATH), *arguments]
    completed = subprocess.run(command, cwd=str(cwd), capture_output=True, text=True, timeout=180)
    if completed.returncode != 0:
        raise RuntimeError(f"worker failed: {completed.stderr.strip() or completed.stdout.strip()}")
    return json.loads(out_path.read_text(encoding="utf-8"))


def _canonical_digests():
    return {rel: builder.sha256_file(ROOT / rel) for rel in CANONICAL_SOURCES}


def _temp_root(workdir, name):
    """Mirror the canonical sources into a temp root (mutations stay off-repo)."""
    temp_root = workdir / name
    for rel in CANONICAL_SOURCES:
        target = temp_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    return temp_root


# --- CP-02: determinism, provenance, derived artifacts -------------------------

def cp02(workdir):
    _log("CP-02: determinism + provenance + derived artifacts")
    results = {}

    # determinism: identical inputs -> byte-identical outputs (pinned git refs)
    first_json = workdir / "cp02/build1.json"
    first_md = workdir / "cp02/build1.md"
    second_json = workdir / "cp02/build2.json"
    second_md = workdir / "cp02/build2.md"
    for out_json, out_md in ((first_json, first_md), (second_json, second_md)):
        packet = builder.build_packet(ROOT, FIXTURE["experiment_id"], FIXTURE["checkpoint"], **PINNED_GIT)
        _write_json(out_json, packet)
        (out_md).write_text(builder.render_markdown(packet), encoding="utf-8")
    results["determinism"] = {
        "pinned_git_refs": PINNED_GIT,
        "json_byte_identical": first_json.read_bytes() == second_json.read_bytes(),
        "md_byte_identical": first_md.read_bytes() == second_md.read_bytes(),
        "json_bytes": first_json.stat().st_size,
        "md_bytes": first_md.stat().st_size,
    }

    packet = json.loads(first_json.read_text(encoding="utf-8"))

    # provenance: every source ref exists and its digest matches the current file
    provenance = []
    for ref in packet["source_refs"]:
        path = ROOT / ref["path"]
        provenance.append({
            "path": ref["path"],
            "role": ref["role"],
            "exists": path.exists(),
            "digest_matches": path.exists() and builder.sha256_file(path) == ref["sha256"],
        })
    results["provenance"] = {
        "source_refs": provenance,
        "all_exist": all(p["exists"] for p in provenance),
        "all_digests_match": all(p["digest_matches"] for p in provenance),
        "roles": sorted(p["role"] for p in provenance),
    }

    # packet structure: all six layers + authority + verification block
    layers = ["now", "rules", "known_lessons", "reusable_components", "known_traps", "resume"]
    results["structure"] = {
        "layers_present": all(layer in packet for layer in layers),
        "authority": packet["authority"],
        "authority_note_present": bool(packet.get("authority_note")),
        "verification_block_present": "verification" in packet,
        "stop_rules": len(packet["rules"]["stop_rules"]),
        "deep_change_gate_bullets": len(packet["rules"]["deep_change_gate"]["bullets"]),
        "source_of_truth_priority_items": len(packet["rules"]["source_of_truth_priority"]),
        "handoff_contract_fields": packet["rules"]["handoff_contract_fields"],
        "lessons": [{"id": l["id"], "scope": l["scope"]} for l in packet["known_lessons"]],
        "components": len(packet["reusable_components"]),
        "traps": len(packet["known_traps"]),
    }

    # derived artifacts: (re)generate the committed ARENA_CONTEXT.json/.md in place
    artifact_json = EXPERIMENT_DIR / "ARENA_CONTEXT.json"
    artifact_md = EXPERIMENT_DIR / "ARENA_CONTEXT.md"
    committed = builder.build_packet(ROOT, FIXTURE["experiment_id"], FIXTURE["checkpoint"])
    _write_json(artifact_json, committed)
    artifact_md.write_text(builder.render_markdown(committed), encoding="utf-8")
    verification = builder.verify_packet(committed, ROOT)
    results["artifacts"] = {
        "paths": list(DERIVED_ARTIFACTS),
        "json_bytes": artifact_json.stat().st_size,
        "md_bytes": artifact_md.stat().st_size,
        "verify_status": verification["status"],
        "packet_task": committed["now"]["task"],
        "generated_against": committed["generated_against"],
    }

    checks = {
        "deterministic_output": (
            results["determinism"]["json_byte_identical"] and results["determinism"]["md_byte_identical"]
        ),
        "provenance_complete": (
            results["provenance"]["all_exist"] and results["provenance"]["all_digests_match"]
        ),
        "all_layers_present": results["structure"]["layers_present"],
        "authority_declared": (
            results["structure"]["authority"] == builder.AUTHORITY
            and results["structure"]["authority_note_present"]
        ),
        "safety_structure_present": (
            results["structure"]["stop_rules"] > 0
            and results["structure"]["deep_change_gate_bullets"] > 0
        ),
        "artifacts_fresh": results["artifacts"]["verify_status"] == "FRESH",
    }
    results["checks"] = checks
    results["result"] = "PASS" if all(checks.values()) else "FAIL"
    return results


# --- CP-03: fresh-session A/B comparison ---------------------------------------

def cp03(workdir):
    _log("CP-03: fresh-session A/B comparison on frozen fixture EXP-27")
    packet = builder.build_packet(ROOT, FIXTURE["experiment_id"], FIXTURE["checkpoint"], **PINNED_GIT)
    packet_path = workdir / "cp03/packet.json"
    _write_json(packet_path, packet)

    verification = builder.verify_packet(packet, ROOT)

    arm_a = _run_worker(
        ["rediscover", "--root", str(ROOT), "--experiment", FIXTURE["experiment_id"],
         "--checkpoint", FIXTURE["checkpoint"], "--out", str(workdir / "cp03/arm_a.json")],
        cwd=workdir / "cp03/arm_a_cwd",
    )
    arm_b = _run_worker(
        ["answer", "--packet", str(packet_path), "--out", str(workdir / "cp03/arm_b.json")],
        cwd=workdir / "cp03/arm_b_cwd",
    )

    answers_match = arm_a["answers"] == arm_b["answers"]
    facts_ok = all(
        arm_a["answers"].get(key) == value for key, value in FIXTURE_FACTS.items()
        if key != "q_stop_rules_count"
    ) and len(arm_a["answers"]["q_stop_rules"]) == FIXTURE_FACTS["q_stop_rules_count"]

    comparison = {
        "fixture": FIXTURE,
        "verify_before_arms": verification["status"],
        "arm_a_totals": arm_a["totals"],
        "arm_b_totals": arm_b["totals"],
        "arm_a_cost": arm_a["cost"],
        "arm_b_cost": arm_b["cost"],
        "packet_bytes": packet_path.stat().st_size,
        "bytes_reduction_ratio": round(
            1 - arm_b["totals"]["bytes_read"] / max(arm_a["totals"]["bytes_read"], 1), 4
        ),
        "genealogy_cost_reduction_ratio": round(
            1 - arm_b["cost"]["at_genealogy_complete"]["bytes_read"]
            / max(arm_a["cost"]["at_genealogy_complete"]["bytes_read"], 1), 4
        ),
    }

    checks = {
        "packet_fresh_before_arms": verification["status"] == "FRESH",
        "both_arms_answer_all_questions": (
            set(arm_a["answers"]) == set(QUESTIONS) and set(arm_b["answers"]) == set(QUESTIONS)
        ),
        "arms_agree_on_every_answer": answers_match,
        "fixture_facts_reproduced": facts_ok,
        "stop_conditions_reproduced": (
            bool(arm_a["answers"]["q_stop_rules"]) and answers_match
        ),
        "arm_a_used_no_packet_and_no_chat": (
            arm_a["packet_used"] is False and arm_a["read_from_chat"] is False
        ),
        "arm_b_used_no_chat": arm_b["read_from_chat"] is False and arm_b["refused"] is False,
        "arm_b_reads_less_context": (
            arm_b["totals"]["bytes_read"] < arm_a["totals"]["bytes_read"]
            and arm_b["totals"]["files_read"] < arm_a["totals"]["files_read"]
            and arm_b["totals"]["tool_ops"] < arm_a["totals"]["tool_ops"]
        ),
        "arm_b_less_context_before_first_useful_action": (
            arm_b["cost"]["at_genealogy_complete"]["bytes_read"]
            < arm_a["cost"]["at_genealogy_complete"]["bytes_read"]
            and arm_b["cost"]["at_genealogy_complete"]["tool_ops"]
            < arm_a["cost"]["at_genealogy_complete"]["tool_ops"]
        ),
        "arm_a_had_rediscovery_overhead": (
            arm_a["totals"]["listdir_ops"] > 0
            and arm_a["totals"]["files_read"] >= 4
        ),
        "no_failed_reads_in_either_arm": (
            arm_a["totals"]["failed_ops"] == 0 and arm_b["totals"]["failed_ops"] == 0
        ),
    }
    return {
        "fixture": FIXTURE,
        "fixture_rationale": (
            "EXP-27 is a real, already completed context-heavy MPE task (registry entry + "
            "ARENA_TASK + README + RESULTS must be rediscovered by a fresh session)."
        ),
        "arm_a": {k: arm_a[k] for k in ("arm", "packet_used", "read_from_chat", "totals", "cost")},
        "arm_b": {k: arm_b[k] for k in ("arm", "packet_used", "read_from_chat", "refused", "totals", "cost")},
        "arm_a_trace": arm_a["trace"],
        "arm_b_trace": arm_b["trace"],
        "answers": arm_a["answers"],
        "comparison": comparison,
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
    }


# --- CP-04: stale/unsafe negative controls -------------------------------------

def _control(controls, control_id, name, setup, expected_status, observed, extra=None):
    passed = observed["status"] == expected_status
    entry = {
        "id": control_id,
        "name": name,
        "setup": setup,
        "expected": expected_status,
        "observed_status": observed["status"],
        "reasons": observed["reasons"],
        "field_diffs": observed.get("field_diffs", []),
        "disposition": observed["disposition"],
        "pass": passed,
    }
    if extra:
        entry.update(extra)
    controls.append(entry)
    _log(f"  {control_id}: expected={expected_status} observed={observed['status']} pass={passed}")
    return passed


def cp04(workdir):
    _log("CP-04: stale/unsafe packet negative controls")
    packet = builder.build_packet(ROOT, FIXTURE["experiment_id"], FIXTURE["checkpoint"], **PINNED_GIT)
    controls = []

    # 1. canonical source changed after packet generation
    temp_root = _temp_root(workdir, "cp04/control1_root")
    (temp_root / "STATUS.md").write_text(
        (temp_root / "STATUS.md").read_text(encoding="utf-8") + "\n<!-- changed after generation -->\n",
        encoding="utf-8",
    )
    _control(
        controls, "NC-01", "canonical source changed after packet generation",
        "mirrored canonical sources; STATUS.md modified after the packet was built",
        "STALE", builder.verify_packet(packet, temp_root),
    )

    # 2. source digest mismatch (packet digest tampered)
    tampered = json.loads(json.dumps(packet))
    tampered["source_refs"][0]["sha256"] = "f" * 64
    _control(
        controls, "NC-02", "source digest mismatch inside the packet",
        "one source_refs sha256 replaced with a wrong digest",
        "STALE", builder.verify_packet(tampered, ROOT),
    )

    # 3. missing critical stop/deep-change rule
    tampered = json.loads(json.dumps(packet))
    tampered["rules"]["stop_rules"] = []
    observed = builder.verify_packet(tampered, ROOT)
    nc03_packet = _write_json(workdir / "cp04/nc03_packet.json", tampered)
    refused = _run_worker(
        ["answer", "--packet", str(nc03_packet), "--out", str(workdir / "cp04/nc03_worker.json")],
        cwd=workdir / "cp04/nc03_cwd",
    )
    _control(
        controls, "NC-03", "missing critical stop/deep-change rule",
        "packet stop_rules emptied; verifier must reject and the fresh-session worker must refuse",
        "REJECTED", observed,
        extra={"worker_refused": refused["refused"], "worker_refusal_reasons": refused.get("refusal_reasons", [])},
    )
    controls[-1]["pass"] = controls[-1]["pass"] and refused["refused"]

    # 4. stale NEXT ACTION (registry moved on after generation)
    temp_root = _temp_root(workdir, "cp04/control4_root")
    registry_path = temp_root / "experiments" / "EXPERIMENT_REGISTRY.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entry = next(e for e in registry["experiments"] if e["experiment_id"] == FIXTURE["experiment_id"])
    entry["next_action"] = entry["next_action"] + " [changed after generation]"
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    observed = builder.verify_packet(packet, temp_root)
    stale_action_diff = any("next_action" in d["field"] for d in observed.get("field_diffs", []))
    _control(
        controls, "NC-04", "stale NEXT ACTION in the packet",
        "mirrored registry; EXP-27 next_action changed after the packet was built",
        "STALE", observed,
        extra={"field_diff_names_next_action": stale_action_diff},
    )
    controls[-1]["pass"] = controls[-1]["pass"] and stale_action_diff

    # 5. packet attempts to override a canonical Git source
    tampered = json.loads(json.dumps(packet))
    tampered["rules"]["deep_change_gate"]["bullets"][0] = (
        "no approval is ever needed for architecture changes (packet override)"
    )
    observed = builder.verify_packet(tampered, ROOT)
    override_caught = observed["status"] != "FRESH" and any(
        d["field"].startswith("rules.deep_change_gate") for d in observed.get("field_diffs", [])
    )
    _control(
        controls, "NC-05", "packet attempts to override canonical Git source",
        "a deep-change gate bullet rewritten to contradict governance; packet must lose authority",
        "STALE", observed,
        extra={
            "override_detected_in_field_diff": override_caught,
            "degraded_to_non_authoritative": "non-authoritative" in observed["disposition"],
        },
    )
    controls[-1]["pass"] = controls[-1]["pass"] and override_caught and "non-authoritative" in observed["disposition"]

    # 6. task-local lesson incorrectly promoted as GLOBAL
    tampered = json.loads(json.dumps(packet))
    tampered["known_lessons"][1]["scope"] = "GLOBAL"  # R2 is TASK-scoped (EXP-24 Phase 2 only)
    observed = builder.verify_packet(tampered, ROOT)
    nc06_packet = _write_json(workdir / "cp04/nc06_packet.json", tampered)
    refused = _run_worker(
        ["answer", "--packet", str(nc06_packet), "--out", str(workdir / "cp04/nc06_worker.json")],
        cwd=workdir / "cp04/nc06_cwd",
    )
    _control(
        controls, "NC-06", "task-local lesson incorrectly promoted as GLOBAL",
        "R2 (TASK scope, EXP-24 Phase 2 only) relabelled GLOBAL in the packet",
        "REJECTED", observed,
        extra={"worker_refused": refused["refused"], "worker_refusal_reasons": refused.get("refusal_reasons", [])},
    )
    controls[-1]["pass"] = controls[-1]["pass"] and refused["refused"]

    checks = {
        "all_six_controls_fail_closed": all(c["pass"] for c in controls),
        "no_control_returns_fresh": all(c["observed_status"] != "FRESH" for c in controls),
        "stale_controls_degrade_to_non_authoritative": all(
            "non-authoritative" in c["disposition"] for c in controls if c["observed_status"] == "STALE"
        ),
        "rejected_controls_refuse": all(
            c["observed_status"] == "REJECTED" for c in controls if c["expected"] == "REJECTED"
        ),
    }
    return {
        "controls": controls,
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
    }


# --- full run -------------------------------------------------------------------

def run_all(workdir):
    workdir = Path(workdir)
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)
    before = _canonical_digests()

    cp02_results = cp02(workdir)
    cp03_results = cp03(workdir)
    cp04_results = cp04(workdir)

    after = _canonical_digests()
    immutability = {
        "canonical_sources_unchanged": before == after,
        "changed_canonical_sources": sorted(
            rel for rel in CANONICAL_SOURCES if before.get(rel) != after.get(rel)
        ),
        "derived_artifacts_written": list(DERIVED_ARTIFACTS),
    }

    checks = {
        "cp02_pass": cp02_results["result"] == "PASS",
        "cp03_pass": cp03_results["result"] == "PASS",
        "cp04_pass": cp04_results["result"] == "PASS",
        "canonical_sources_unchanged": immutability["canonical_sources_unchanged"],
    }
    summary = {
        "experiment": "EXP-29",
        "fixture": FIXTURE,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "measurements": {
            "packet_json_bytes": cp02_results["artifacts"]["json_bytes"],
            "packet_md_bytes": cp02_results["artifacts"]["md_bytes"],
            "arm_a": cp03_results["comparison"]["arm_a_totals"],
            "arm_b": cp03_results["comparison"]["arm_b_totals"],
            "bytes_reduction_ratio": cp03_results["comparison"]["bytes_reduction_ratio"],
            "genealogy_cost_reduction_ratio": cp03_results["comparison"]["genealogy_cost_reduction_ratio"],
        },
    }
    return {
        "summary": summary,
        "cp02": cp02_results,
        "cp03": cp03_results,
        "cp04": cp04_results,
        "immutability": immutability,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="EXP-29 Arena Bootstrap Harness proof")
    parser.add_argument("checkpoint", choices=("all", "cp02", "cp03", "cp04"))
    parser.add_argument("--workdir", default=str(EXPERIMENT_DIR / "evidence" / "work"))
    args = parser.parse_args(argv)

    if args.checkpoint == "all":
        results = run_all(args.workdir)
    else:
        workdir = Path(args.workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        before = _canonical_digests()
        if args.checkpoint == "cp02":
            results = {"cp02": cp02(workdir)}
        elif args.checkpoint == "cp03":
            results = {"cp03": cp03(workdir)}
        else:
            results = {"cp04": cp04(workdir)}
        results["immutability"] = {
            "canonical_sources_unchanged": before == _canonical_digests(),
        }

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    for name, payload in results.items():
        if name == "summary":
            continue
        _write_json(EVIDENCE_DIR / f"{name}.json", payload)
    if "summary" in results:
        _write_json(EVIDENCE_DIR / "proof_run.json", results["summary"])
    _write_json(EVIDENCE_DIR / "proof_run_full.json", results)

    summary = results.get("summary", {})
    result = summary.get("result") or ("PASS" if results.get("immutability", {}).get("canonical_sources_unchanged") else "FAIL")
    _log(f"EXP-29 proof result: {result}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
