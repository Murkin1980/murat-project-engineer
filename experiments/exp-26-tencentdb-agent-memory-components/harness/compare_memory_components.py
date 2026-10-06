#!/usr/bin/env python3
"""Deterministic, read-only A/B/C comparison over the frozen EXP-15 memory cases.

A = current EXP-15 file-backed memory output.
B = a transient Mermaid-like symbolic packet with the same facts and source refs.
C = a transient L2 scenario card that points to L1 memory IDs for provenance drill-down.

This tests context representation and lookup shape only. EXP-15 contains no frozen raw
session/tool logs, so B is not a test of production log offloading or LLM summarization.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
EXP15_DIR = REPO_ROOT / "experiments/exp-15-memory/2026-09-30"
EXP26_DIR = REPO_ROOT / "experiments/exp-26-tencentdb-agent-memory-components"
FIXTURES_DIR = EXP15_DIR / "fixtures"

sys.path.insert(0, str(EXP15_DIR / "harness"))
from memory_layer import (  # noqa: E402
    DeltaAction,
    ProjectMemoryStore,
    ProposedMemoryDelta,
    UnauthorizedWriteError,
)

PROJECT = "Murkin1980/murat-project-engineer"
FROZEN_INPUTS = {
    "benchmark_tasks.json": "dcb0d2f920ba8d95e9a2dfd6641f6855c20a5aa586fb021c21ab8303a70951e1",
    "canonical_memory.json": "24b2a00bc9627ebda9cf92bb6b06a269e4f0857577d1d57185dbe09f8a6623df",
    "cross_project_memory.json": "9705d797f766558ecffb7a1a4038a4e1f4e649fed42daff8b91cda51716e543e",
    "memory_layer.py": "15266ce759223c43973c7a3cb1d2a5bad1e7e3615d98d1859df080f45eab3de7",
}

# Predicate checks are a small, frozen answer oracle derived from the EXP-15
# canonical decision/constraint fields. They assert required concepts, not style.
REQUIRED_PREDICATES: dict[str, dict[str, list[str]]] = {
    "TASK-MPE-08": {
        "decision": ["REUSE_COMPONENT", "public-web browser acquisition role only"],
        "constraint": [
            "PUBLIC_WEB_ONLY", "no authentication", "no forms", "no messaging",
            "no purchase", "no CAPTCHA bypass", "isolated Chrome must be deleted",
        ],
    },
    "TASK-MPE-11": {
        "decision": [
            "lightweight file-based coordination", "typed mailbox envelopes",
            "append-only JSONL events", "ephemeral state",
        ],
        "constraint": [
            "NO daemon", "background scheduler", "persistent agent", "shared database",
            "Router authority change", "single-filesystem only", "Windows junction rejection",
        ],
    },
    "TASK-MPE-12": {
        "decision": ["20/20 retrospective cases", "status remains EXPERIMENT"],
        "constraint": [
            "deep_change_probability", "deterministic heuristic score",
            "NOT a calibrated statistical probability", "prospective pre-registered cases",
            "operational reliance",
        ],
    },
    "TASK-MPE-18": {
        "decision": [
            "verified byte-for-byte retrieval", "29/29 files",
            "pinned sentence-transformers/all-MiniLM-L6-v2", "primary source loss",
        ],
        "constraint": [
            "last-resort fallback path ONLY", "SHA-256 manifest check",
            "DO NOT add production routing", "a registry", "seeding infrastructure",
        ],
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def item_for(items: list[Any], *categories: str) -> Any:
    matches = [item for item in items if item.category in categories]
    if len(matches) != 1:
        raise AssertionError(f"Expected one item in {categories}, found {len(matches)}")
    return matches[0]


def serialize_current(items: list[Any]) -> str:
    # Match EXP-15's per-item pretty-JSON context accounting.
    return "\n".join(json.dumps(item.to_dict(), indent=2, ensure_ascii=False) for item in items)


def mermaid_label(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "<br/>")


def symbolic_packet(project: str, items: list[Any]) -> str:
    """Transient compact board; preserves each full summary, ID, and source string."""
    rows = ["flowchart LR", f"%% scope: {project}"]
    for index, item in enumerate(items, start=1):
        node = f"F{index}"
        ref_node = f"R{index}"
        rows.append(f'  {node}["{mermaid_label(item.category)}: {mermaid_label(item.summary)}"]')
        rows.append(f'  {node} -. {item.item_id} .-> {ref_node}["{mermaid_label(item.provenance)}"]')
    return "\n".join(rows)


def scenario_card(project: str, topic: str, items: list[Any]) -> dict[str, Any]:
    decision = item_for(items, "decision", "outcome")
    constraint = item_for(items, "constraint")
    return {
        "project": project,
        "scenario": topic,
        "decision_or_outcome": decision.summary,
        "constraints": constraint.summary,
        "fact_refs": [
            {"id": decision.item_id, "provenance": decision.provenance},
            {"id": constraint.item_id, "provenance": constraint.provenance},
        ],
    }


def context_metrics(text: str) -> dict[str, int]:
    byte_count = len(text.encode("utf-8"))
    return {
        "context_lines": len(text.splitlines()),
        "context_utf8_bytes": byte_count,
        "approx_tokens_utf8_bytes_div_4": math.ceil(byte_count / 4),
    }


def required_recall_ok(task_id: str, decision_summary: str, constraint_summary: str) -> dict[str, Any]:
    oracle = REQUIRED_PREDICATES[task_id]
    missing_decision = [
        phrase for phrase in oracle["decision"] if phrase.casefold() not in decision_summary.casefold()
    ]
    missing_constraint = [
        phrase for phrase in oracle["constraint"] if phrase.casefold() not in constraint_summary.casefold()
    ]
    return {
        "decision_ok": not missing_decision,
        "constraint_ok": not missing_constraint,
        "missing_decision_predicates": missing_decision,
        "missing_constraint_predicates": missing_constraint,
    }


def provenance_refs(item: Any) -> list[str]:
    return [part.strip() for part in item.provenance.split(",") if part.strip()]


def validate_provenance(items: list[Any]) -> dict[str, Any]:
    """Check local source-path existence and line-anchor range, not semantic wording."""
    line_cache: dict[Path, list[str]] = {}
    refs: list[dict[str, Any]] = []
    for item in items:
        for ref in provenance_refs(item):
            match = re.fullmatch(r"(.+?)(?:#L(\d+))?", ref)
            if not match:
                refs.append({"item_id": item.item_id, "reference": ref, "path_exists": False, "anchor_valid": False})
                continue
            rel_path, raw_line = match.groups()
            source = (REPO_ROOT / rel_path).resolve()
            try:
                source.relative_to(REPO_ROOT.resolve())
                inside_repo = True
            except ValueError:
                inside_repo = False
            exists = inside_repo and source.is_file()
            line_number = int(raw_line) if raw_line else None
            if exists and source not in line_cache:
                line_cache[source] = source.read_text(encoding="utf-8").splitlines()
            lines = line_cache.get(source, [])
            anchor_valid = line_number is None or (exists and 1 <= line_number <= len(lines))
            refs.append({
                "item_id": item.item_id,
                "reference": ref,
                "path_exists": exists,
                "line_number": line_number,
                "source_line_count": len(lines) if exists else None,
                "anchor_valid": anchor_valid,
            })
    invalid = [ref for ref in refs if not ref["path_exists"] or not ref["anchor_valid"]]
    return {
        "references_checked": len(refs),
        "source_paths_found": sum(ref["path_exists"] for ref in refs),
        "line_anchors_valid": sum(ref["anchor_valid"] for ref in refs),
        "unique_source_files_read_for_validation": len(line_cache),
        "invalid_references": invalid,
        "scope_note": "Line-range and path checks only; source text was not semantically re-adjudicated.",
    }


def unauthorized_write_probe(mode: str, source_bytes: bytes) -> dict[str, Any]:
    """Try a no-change delta against a temporary copy; prove fail-closed, not mutation."""
    with tempfile.TemporaryDirectory(prefix="exp26-write-gate-") as temp_dir:
        temp_store = Path(temp_dir) / "memory.json"
        temp_store.write_bytes(source_bytes)
        before = sha256(temp_store)
        store = ProjectMemoryStore(temp_store)
        delta = ProposedMemoryDelta(
            task_id=f"EXP26-{mode}-WRITE-GATE",
            project=PROJECT,
            proposed_by="exp26-deterministic-harness",
            actions=[DeltaAction(action="NO_CHANGE", reason="Read-only gate probe")],
        )
        rejected = False
        try:
            store.apply_approved_delta(delta, None)  # type: ignore[arg-type]
        except UnauthorizedWriteError:
            rejected = True
        after = sha256(temp_store)
        if not rejected or before != after:
            raise AssertionError(f"{mode}: unauthorized write was not safely rejected")
        return {
            "attempted": 1,
            "rejected_by_approval_gate": 1 if rejected else 0,
            "temporary_store_changed": before != after,
            "canonical_store_touched": False,
        }


def check_isolation(cross_path: Path) -> dict[str, Any]:
    store = ProjectMemoryStore(cross_path)
    mpe_items = store.recall(project=PROJECT)
    expected = {"MEM-MPE-001"}
    if {item.item_id for item in mpe_items} != expected:
        raise AssertionError("A: cross-project fixture returned unexpected MPE items")
    foreign_ids = {"MEM-MH-001", "MEM-MH-002", "MEM-MAO-001", "MEM-MAO-002"}

    b_text = symbolic_packet(PROJECT, mpe_items)
    b_leaks = sorted(item_id for item_id in foreign_ids if item_id in b_text)

    c_card = {
        "project": PROJECT,
        "scenario": "browseract",
        "fact_refs": [{"id": item.item_id} for item in mpe_items],
    }
    c_ids = {ref["id"] for ref in c_card["fact_refs"]}
    c_leaks = sorted(item_id for item_id in foreign_ids if item_id in c_ids)
    if b_leaks or c_leaks or any(item.project != PROJECT for item in mpe_items):
        raise AssertionError("Cross-project memory leakage detected")
    return {
        "fixture": "EXP-15 cross_project_memory.json",
        "expected_scoped_item_ids": sorted(expected),
        "foreign_item_ids_checked": sorted(foreign_ids),
        "A_leaked_ids": [],
        "B_leaked_ids": b_leaks,
        "C_leaked_ids": c_leaks,
        "isolation_violations": 0,
    }


def run() -> dict[str, Any]:
    paths = {
        "benchmark_tasks.json": FIXTURES_DIR / "benchmark_tasks.json",
        "canonical_memory.json": FIXTURES_DIR / "canonical_memory.json",
        "cross_project_memory.json": FIXTURES_DIR / "cross_project_memory.json",
        "memory_layer.py": EXP15_DIR / "harness/memory_layer.py",
    }
    actual_hashes = {name: sha256(path) for name, path in paths.items()}
    for name, expected_hash in FROZEN_INPUTS.items():
        if actual_hashes[name] != expected_hash:
            raise AssertionError(f"Frozen EXP-15 input changed: {name} ({actual_hashes[name]})")

    task_data = load_json(paths["benchmark_tasks.json"])["tasks"]
    source_memory_bytes = paths["canonical_memory.json"].read_bytes()
    store = ProjectMemoryStore(paths["canonical_memory.json"])
    if store.load_status != "LOADED":
        raise AssertionError(f"EXP-15 memory fixture did not load: {store.load_status}")
    all_items = store.recall(project=PROJECT)
    item_by_id = {item.item_id: item for item in all_items}
    if len(task_data) != 4:
        raise AssertionError(f"Expected the four frozen EXP-15 cases; found {len(task_data)}")

    # Precompute the transient C-arm scenario index from the same frozen memory items.
    scenario_index: dict[str, dict[str, Any]] = {}
    scenario_items: dict[str, list[Any]] = {}
    for task in task_data:
        selected = store.recall(project=task["project"], topic=task["topic"])
        scenario_index[task["topic"]] = scenario_card(task["project"], task["topic"], selected)
        scenario_items[task["topic"]] = selected

    case_results: list[dict[str, Any]] = []
    per_mode: dict[str, list[dict[str, Any]]] = {"A": [], "B": [], "C": []}
    for task in task_data:
        topic = task["topic"]
        expected_ids = set(task["expected_memory_ids"])

        # A: the actual EXP-15 file-backed recall implementation and record format.
        items_a = store.recall(project=task["project"], topic=topic)
        ids_a = {item.item_id for item in items_a}
        if ids_a != expected_ids:
            raise AssertionError(f"A {task['task_id']}: recall IDs {sorted(ids_a)} != {sorted(expected_ids)}")
        decision_a = item_for(items_a, "decision", "outcome")
        constraint_a = item_for(items_a, "constraint")
        a_text = serialize_current(items_a)
        a_recall = required_recall_ok(task["task_id"], decision_a.summary, constraint_a.summary)
        if not a_recall["decision_ok"] or not a_recall["constraint_ok"]:
            raise AssertionError(f"A {task['task_id']}: frozen answer predicate failed: {a_recall}")
        a_metric = {
            "context": context_metrics(a_text),
            "recalled_ids": sorted(ids_a),
            "false_positive_ids": sorted(ids_a - expected_ids),
            "recall": a_recall,
            "provenance_refs_in_initial_context": True,
            "provenance_drilldown_lookups": 0,
            "optional_detail_drilldown_lookups": 0,
            "logical_case_lookup_count": 1,
            "context_text": a_text,
        }

        # B: same source facts in a compact symbolic packet with explicit item->source refs.
        b_text = symbolic_packet(task["project"], items_a)
        b_recall = required_recall_ok(task["task_id"], decision_a.summary, constraint_a.summary)
        required_payload = [decision_a.summary, constraint_a.summary, decision_a.provenance, constraint_a.provenance]
        if not all(payload in b_text for payload in required_payload):
            raise AssertionError(f"B {task['task_id']}: symbolic packet dropped required text or provenance")
        b_metric = {
            "context": context_metrics(b_text),
            "recalled_ids": sorted(ids_a),
            "false_positive_ids": [],
            "recall": b_recall,
            "provenance_refs_in_initial_context": True,
            "provenance_drilldown_lookups": 0,
            "optional_detail_drilldown_lookups": 0,
            "logical_case_lookup_count": 1,
            "context_text": b_text,
        }

        # C: load an L2 topic/scenario capsule with source refs; follow fact IDs to L1 for optional details.
        c_card = scenario_index[topic]
        if c_card["project"] != task["project"]:
            raise AssertionError(f"C {task['task_id']}: scenario scope mismatch")
        c_selected = scenario_items[topic]
        c_ids = {fact_ref["id"] for fact_ref in c_card["fact_refs"]}
        if c_ids != expected_ids:
            raise AssertionError(f"C {task['task_id']}: scenario IDs {sorted(c_ids)} != {sorted(expected_ids)}")
        c_text = json.dumps(c_card, indent=2, ensure_ascii=False)
        c_recall = required_recall_ok(
            task["task_id"], c_card["decision_or_outcome"], c_card["constraints"]
        )
        if not c_recall["decision_ok"] or not c_recall["constraint_ok"]:
            raise AssertionError(f"C {task['task_id']}: frozen answer predicate failed: {c_recall}")
        if not all(item.provenance in c_text for item in (decision_a, constraint_a)):
            raise AssertionError(f"C {task['task_id']}: scenario card dropped source references")
        # Optional deep-detail query follows the L2 item IDs to both L1 records in one lookup.
        l1_details = [item_by_id[item_id] for item_id in c_ids]
        if {item.item_id for item in l1_details} != expected_ids:
            raise AssertionError(f"C {task['task_id']}: L1 drill-down did not resolve all pointers")
        c_full_text = c_text + "\\n" + serialize_current(l1_details)
        c_metric = {
            "context": context_metrics(c_text),
            "recalled_ids": sorted(c_ids),
            "false_positive_ids": [],
            "recall": c_recall,
            "provenance_refs_in_initial_context": True,
            "provenance_pointer_ids": sorted(c_ids),
            "provenance_resolved_via_l1": True,
            "provenance_drilldown_lookups": 0,
            "optional_detail_drilldown_lookups": 1,
            "optional_detail_context": context_metrics(c_full_text),
            "logical_case_lookup_count": 1,
            "full_item_provenance_refs_resolved": sum(len(provenance_refs(item)) for item in l1_details),
            "context_text": c_text,
        }

        for name, metric in (("A", a_metric), ("B", b_metric), ("C", c_metric)):
            per_mode[name].append(metric)
        case_results.append({
            "task_id": task["task_id"],
            "name": task["name"],
            "query": task["query"],
            "topic_key_used_by_all_arms": topic,
            "expected_memory_ids": sorted(expected_ids),
            "mode_results": {"A": a_metric, "B": b_metric, "C": c_metric},
        })

    provenance = validate_provenance(all_items)
    write_probes = {
        mode: unauthorized_write_probe(mode, source_memory_bytes) for mode in ("A", "B", "C")
    }
    isolation = check_isolation(paths["cross_project_memory.json"])
    post_hashes = {name: sha256(path) for name, path in paths.items()}
    if post_hashes != actual_hashes:
        raise AssertionError("A frozen EXP-15 input changed during the experiment")

    aggregate: dict[str, Any] = {}
    total_lines_a = sum(m["context"]["context_lines"] for m in per_mode["A"])
    total_bytes_a = sum(m["context"]["context_utf8_bytes"] for m in per_mode["A"])
    total_tokens_a = sum(m["context"]["approx_tokens_utf8_bytes_div_4"] for m in per_mode["A"])
    for mode, metrics in per_mode.items():
        total_lines = sum(m["context"]["context_lines"] for m in metrics)
        total_bytes = sum(m["context"]["context_utf8_bytes"] for m in metrics)
        total_tokens = sum(m["context"]["approx_tokens_utf8_bytes_div_4"] for m in metrics)
        aggregate[mode] = {
            "cases": len(metrics),
            "prior_decisions_recalled": sum(m["recall"]["decision_ok"] for m in metrics),
            "constraints_recalled": sum(m["recall"]["constraint_ok"] for m in metrics),
            "false_positive_items": sum(len(m["false_positive_ids"]) for m in metrics),
            "context_lines_total": total_lines,
            "context_lines_per_case": [m["context"]["context_lines"] for m in metrics],
            "context_utf8_bytes_total": total_bytes,
            "context_utf8_bytes_per_case": [m["context"]["context_utf8_bytes"] for m in metrics],
            "approx_tokens_utf8_bytes_div_4_total": total_tokens,
            "approx_tokens_per_case": [m["context"]["approx_tokens_utf8_bytes_div_4"] for m in metrics],
            "source_doc_or_raw_log_reads_for_recall": 0,
            "logical_case_lookup_count": sum(m["logical_case_lookup_count"] for m in metrics),
            "provenance_drilldown_lookups": sum(m["provenance_drilldown_lookups"] for m in metrics),
            "optional_detail_drilldown_lookups": sum(
                m.get("optional_detail_drilldown_lookups", 0) for m in metrics
            ),
            "optional_detail_context_lines_total": sum(
                m.get("optional_detail_context", {}).get("context_lines", 0) for m in metrics
            ),
            "optional_detail_context_utf8_bytes_total": sum(
                m.get("optional_detail_context", {}).get("context_utf8_bytes", 0) for m in metrics
            ),
            "optional_detail_approx_tokens_total": sum(
                m.get("optional_detail_context", {}).get("approx_tokens_utf8_bytes_div_4", 0) for m in metrics
            ),
            "provenance_paths_in_initial_context_cases": sum(
                m["provenance_refs_in_initial_context"] for m in metrics
            ),
            "implementation_complexity": {
                "A": "None beyond the existing EXP-15 file-backed memory lookup.",
                "B": "Low: one transient deterministic renderer; no persistent state or dependency.",
                "C": "Low-medium: transient scoped scenario index plus L1 pointer resolver; one optional extra lookup for full item details.",
            }[mode],
            "new_production_files": 0,
            "new_dependencies": 0,
            "new_services_databases_or_vector_stores": 0,
            "persistent_writes": 0,
        }
        aggregate[mode]["context_line_reduction_vs_A_percent"] = round(
            (total_lines_a - total_lines) / total_lines_a * 100, 1
        ) if total_lines_a else 0.0
        aggregate[mode]["context_byte_reduction_vs_A_percent"] = round(
            (total_bytes_a - total_bytes) / total_bytes_a * 100, 1
        ) if total_bytes_a else 0.0
        aggregate[mode]["approx_token_reduction_vs_A_percent"] = round(
            (total_tokens_a - total_tokens) / total_tokens_a * 100, 1
        ) if total_tokens_a else 0.0

    result = {
        "experiment_id": "EXP-26",
        "run_date_utc": "2026-10-06",
        "primary_disposition": "REUSE_COMPONENT",
        "result": "PARTIAL",
        "adoption": "ADOPT_WITH_CHANGES",
        "upstream_pin": {
            "repository": "https://github.com/TencentCloud/TencentDB-Agent-Memory",
            "audited_default_branch": "feat/server_team",
            "audited_commit": "8b86874a2daea49e3ff0fb53d699203146c5c77d",
            "latest_stable_release_at_audit": "v2.0.1",
            "latest_stable_commit": "a5dcbe6e9fee0d1d1e32d935326f1d3bcf927fdb",
            "license_text": "MIT",
            "upstream_source_copied": False,
            "platform_installed": False,
        },
        "case_freeze": {
            "source": "EXP-15 2026-09-30 frozen benchmark; no EXP-15 fixture changes",
            "arm_a_definition": "User-directed current memory: EXP-15 file-backed memory recall (the memory-enabled arm in the original EXP-15 comparison).",
            "case_count": len(case_results),
            "task_ids": [case["task_id"] for case in case_results],
            "frozen_input_sha256_before": actual_hashes,
            "frozen_input_sha256_after": post_hashes,
            "note": "Original EXP-15 no-memory Mode A was not re-run or relabeled as this task's A arm.",
        },
        "measurement_scope": {
            "b_short_term_compaction": "Serialization-only proxy over current memory records: concise symbolic board retains full summaries, item IDs, and file/line refs. No frozen raw tool logs exist, so no claim is made about long-log compression or task success.",
            "c_progressive_recall": "Ephemeral L2 topic/scenario card preserves exact decision/constraint text, provenance refs, and L1 item IDs; optional details require one batched L1 pointer lookup. No persistent index was created.",
            "token_estimate": "ceil(UTF-8 bytes / 4); deterministic approximation, not model-tokenizer measurement.",
            "source_validation": "Shared evaluator read-only validation checks every referenced path and line-anchor range; it does not semantically re-adjudicate cited text.",
        },
        "summary": {
            "modes": aggregate,
            "provenance_validation": provenance,
            "isolation": isolation,
            "unauthorized_write_probes": write_probes,
            "unauthorized_write_attempts": sum(probe["attempted"] for probe in write_probes.values()),
            "unauthorized_mutations": sum(probe["temporary_store_changed"] for probe in write_probes.values()),
            "canonical_fixture_mutated": actual_hashes["canonical_memory.json"] != post_hashes["canonical_memory.json"],
            "all_frozen_input_hashes_match": actual_hashes == post_hashes == FROZEN_INPUTS,
            "all_frozen_inputs_unchanged": actual_hashes == post_hashes,
        },
        "cases": case_results,
        "disposition_rationale": [
            "B and C preserve all required decision and constraint predicates in the four frozen cases while reducing the injected context footprint.",
            "C carries source refs in the initial L2 card; a separate optional detail request costs one L1 lookup per case.",
            "The EXP-15 fixture has one inherited out-of-range citation (MEM-MPE-006 -> evidence/stage2/RUN-12_REPORT.json#L41); the alternate documentation citation remains present. No frozen fixture was edited.",
            "B cannot validate upstream raw tool-result offloading on this dataset; the result is a representation-level signal, not a production-performance claim.",
        ],
    }

    evidence_dir = EXP26_DIR / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "comparison.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (evidence_dir / "comparison.log").write_text(render_log(result), encoding="utf-8")
    return result


def render_log(result: dict[str, Any]) -> str:
    modes = result["summary"]["modes"]
    provenance = result["summary"]["provenance_validation"]
    lines = [
        "EXP-26 deterministic A/B/C memory-component comparison",
        f"Date (UTC): {result['run_date_utc']}",
        "A = current EXP-15 file-backed memory; B = symbolic packet; C = layered scenario card.",
        "Frozen cases: " + ", ".join(result["case_freeze"]["task_ids"]),
        "",
        "Aggregate injected-context footprint (4 cases):",
    ]
    for mode in ("A", "B", "C"):
        metric = modes[mode]
        lines.append(
            f"  {mode}: {metric['context_lines_total']} lines, "
            f"{metric['context_utf8_bytes_total']} UTF-8 bytes, "
            f"~{metric['approx_tokens_utf8_bytes_div_4_total']} tokens (bytes/4); "
            f"decision {metric['prior_decisions_recalled']}/4, "
            f"constraints {metric['constraints_recalled']}/4, "
            f"false positives {metric['false_positive_items']}, "
            f"source-doc/raw-log reads {metric['source_doc_or_raw_log_reads_for_recall']}, "
            f"provenance drilldowns {metric['provenance_drilldown_lookups']}, "
            f"optional detail drilldowns {metric['optional_detail_drilldown_lookups']}"
        )
    c_metrics = modes["C"]
    lines.extend([
        "",
        f"C with optional L1 detail: {c_metrics['optional_detail_context_lines_total']} lines, "
        f"{c_metrics['optional_detail_context_utf8_bytes_total']} UTF-8 bytes, "
        f"~{c_metrics['optional_detail_approx_tokens_total']} tokens; "
        f"{c_metrics['optional_detail_drilldown_lookups']} batched L1 lookups.",
        f"Context reduction vs A: B {modes['B']['context_line_reduction_vs_A_percent']}% lines / "
        f"{modes['B']['context_byte_reduction_vs_A_percent']}% bytes; C "
        f"{modes['C']['context_line_reduction_vs_A_percent']}% lines / "
        f"{modes['C']['context_byte_reduction_vs_A_percent']}% bytes.",
        f"Provenance: {provenance['source_paths_found']}/{provenance['references_checked']} paths exist; "
        f"{provenance['line_anchors_valid']}/{provenance['references_checked']} line anchors in range; "
        f"{provenance['unique_source_files_read_for_validation']} unique source files read by the shared validator.",
        "Isolation violations: " + str(result["summary"]["isolation"]["isolation_violations"]),
        f"Approval-gate probes: {result['summary']['unauthorized_write_attempts']} rejected; "
        f"unauthorized mutations: {result['summary']['unauthorized_mutations']}; "
        f"canonical fixture mutated: {result['summary']['canonical_fixture_mutated']}.",
        "",
        "INHERITED INVALID ANCHOR:",
    ])
    for bad_ref in provenance["invalid_references"]:
        lines.append(f"  {bad_ref['item_id']}: {bad_ref['reference']}")
    lines.extend([
        "",
        "LIMITATION: B is a deterministic context-format proxy; frozen EXP-15 cases have no raw session/tool-log fixture.",
        "RESULT: PARTIAL / ADOPT_WITH_CHANGES; do not install the upstream platform or integrate into production.",
    ])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    comparison = run()
    print(render_log(comparison), end="")
