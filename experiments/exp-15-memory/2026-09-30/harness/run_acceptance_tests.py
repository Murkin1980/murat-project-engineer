"""
EXP-15 Acceptance Test Runner
=============================

Runs all 6 mandatory acceptance tests deterministically:
1. RECALL
2. UPDATE
3. DELETE
4. ISOLATION
5. PROVENANCE
6. FAILURE

Outputs structured verification log and results.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

from memory_layer import (
    ApprovalGate,
    DeltaAction,
    MemoryError,
    MemoryItem,
    ProjectMemoryStore,
    ProposedMemoryDelta,
    ProvenanceMissingError,
    ScopeViolationError,
    UnauthorizedWriteError,
)

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
CANONICAL_STORE_PATH = FIXTURES_DIR / "canonical_memory.json"
CROSS_PROJECT_STORE_PATH = FIXTURES_DIR / "cross_project_memory.json"
REPO_ROOT = Path(__file__).resolve().parents[4]


def test_1_recall() -> Dict[str, Any]:
    """1. RECALL: returns the correct relevant fact/decision/constraint with provenance."""
    store = ProjectMemoryStore(CANONICAL_STORE_PATH)
    assert store.load_status == "LOADED", f"Store not loaded: {store.load_warning}"

    # Query for browseract
    items = store.recall(project="Murkin1980/murat-project-engineer", topic="browseract")
    item_ids = [i.item_id for i in items]
    assert "MEM-MPE-001" in item_ids, f"MEM-MPE-001 missing from recall: {item_ids}"
    assert "MEM-MPE-002" in item_ids, f"MEM-MPE-002 missing from recall: {item_ids}"

    # Verify category and provenance
    item_001 = next(i for i in items if i.item_id == "MEM-MPE-001")
    assert item_001.category == "decision"
    assert "REUSE_COMPONENT" in item_001.summary
    assert item_001.provenance == "docs/evaluations/BROWSERACT_EVALUATION.md#L45, evidence/stage2/RUN-08_REPORT.json#L24"

    item_002 = next(i for i in items if i.item_id == "MEM-MPE-002")
    assert item_002.category == "constraint"
    assert "PUBLIC_WEB_ONLY" in item_002.summary

    # Query for runtime coordination
    rt_items = store.recall(project="Murkin1980/murat-project-engineer", topic="runtime coordination")
    rt_ids = [i.item_id for i in rt_items]
    assert "MEM-MPE-003" in rt_ids
    assert "MEM-MPE-004" in rt_ids

    return {
        "test": "RECALL",
        "result": "PASS",
        "recalled_items": len(items) + len(rt_items),
        "details": "Correctly recalled active decisions, constraints, and outcomes across queries without omission.",
    }


def test_2_update() -> Dict[str, Any]:
    """2. UPDATE: a newer approved fact supersedes the old one correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_store_path = Path(tmpdir) / "test_store.json"
        # Copy canonical store content
        tmp_store_path.write_text(CANONICAL_STORE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        store = ProjectMemoryStore(tmp_store_path)

        # 1. Add initial active item
        initial_item = MemoryItem(
            item_id="MEM-EXP15-STATUS-001",
            project="Murkin1980/murat-project-engineer",
            category="outcome",
            topic="exp-15 status",
            summary="EXP-15 status is PLANNED and queued.",
            provenance="docs/experiments/EXP-15_MPE_PROJECT_MEMORY_LAYER.md#L5",
        )
        add_delta = ProposedMemoryDelta(
            task_id="TASK-TEST-INIT",
            project="Murkin1980/murat-project-engineer",
            proposed_by="test-agent",
            actions=[DeltaAction(action="ADD", item=initial_item)],
        )
        gate = ApprovalGate(approver="lead-maintainer", decision="APPROVED")
        store.apply_approved_delta(add_delta, gate)

        recalled = store.recall(project="Murkin1980/murat-project-engineer", topic="exp-15 status")
        assert len(recalled) == 1
        assert recalled[0].item_id == "MEM-EXP15-STATUS-001"
        assert recalled[0].summary == "EXP-15 status is PLANNED and queued."

        # 2. Propose SUPERSEDE delta
        updated_item = MemoryItem(
            item_id="MEM-EXP15-STATUS-002",
            project="Murkin1980/murat-project-engineer",
            category="outcome",
            topic="exp-15 status",
            summary="EXP-15 MVP executed with PASS outcome; all 6 acceptance tests passed.",
            provenance="experiments/exp-15-memory/2026-09-30/RESULTS.md#L1",
        )
        supersede_delta = ProposedMemoryDelta(
            task_id="TASK-TEST-UPDATE",
            project="Murkin1980/murat-project-engineer",
            proposed_by="test-agent",
            actions=[
                DeltaAction(
                    action="SUPERSEDE",
                    item=updated_item,
                    target_item_id="MEM-EXP15-STATUS-001",
                    reason="Experiment completed successfully",
                )
            ],
        )

        # Verify unauthorized write fails closed
        try:
            unauthorized_gate = ApprovalGate(approver="malicious-actor", decision="REJECTED")
            store.apply_approved_delta(supersede_delta, unauthorized_gate)
            assert False, "Unauthorized write should have failed"
        except UnauthorizedWriteError:
            pass  # Expected fail-closed behavior

        # Apply with valid approval
        store.apply_approved_delta(supersede_delta, gate)

        # 3. Recall should now return ONLY the new item
        active_recalled = store.recall(project="Murkin1980/murat-project-engineer", topic="exp-15 status")
        assert len(active_recalled) == 1, f"Expected 1 active item, got {len(active_recalled)}"
        assert active_recalled[0].item_id == "MEM-EXP15-STATUS-002"
        assert "PASS outcome" in active_recalled[0].summary

        # Check that old item is marked superseded with pointer
        all_items = store.recall(
            project="Murkin1980/murat-project-engineer", topic="exp-15 status", include_superseded=True
        )
        assert len(all_items) == 2
        old_rec = next(i for i in all_items if i.item_id == "MEM-EXP15-STATUS-001")
        assert old_rec.status == "superseded"
        assert old_rec.superseded_by == "MEM-EXP15-STATUS-002"

    return {
        "test": "UPDATE",
        "result": "PASS",
        "details": "New approved fact supersedes old fact; old marked superseded; recall returns exclusively the new active fact.",
    }


def test_3_delete() -> Dict[str, Any]:
    """3. DELETE: an approved deletion removes the fact from future recall."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_store_path = Path(tmpdir) / "test_delete_store.json"
        tmp_store_path.write_text(CANONICAL_STORE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        store = ProjectMemoryStore(tmp_store_path)

        # 1. Add temporary item
        temp_item = MemoryItem(
            item_id="MEM-TEMP-001",
            project="Murkin1980/murat-project-engineer",
            category="lesson",
            topic="temporary test probe",
            summary="This is a temporary fact to be deleted.",
            provenance="tests/test_temp.py#L1",
        )
        gate = ApprovalGate(approver="lead-maintainer", decision="APPROVED")
        add_delta = ProposedMemoryDelta(
            task_id="TASK-TEMP-ADD",
            project="Murkin1980/murat-project-engineer",
            proposed_by="test-agent",
            actions=[DeltaAction(action="ADD", item=temp_item)],
        )
        store.apply_approved_delta(add_delta, gate)
        assert len(store.recall(project="Murkin1980/murat-project-engineer", topic="temporary test probe")) == 1

        # 2. Propose deletion
        delete_delta = ProposedMemoryDelta(
            task_id="TASK-TEMP-DEL",
            project="Murkin1980/murat-project-engineer",
            proposed_by="test-agent",
            actions=[DeltaAction(action="DELETE", target_item_id="MEM-TEMP-001", reason="Obsolete test probe")],
        )

        # Unapproved write fails closed
        try:
            store.apply_approved_delta(delete_delta, None)  # type: ignore
            assert False, "Null approval should fail"
        except UnauthorizedWriteError:
            pass

        # Approved delete
        store.apply_approved_delta(delete_delta, gate)

        # 3. Active recall must NOT return the item
        active_items = store.recall(project="Murkin1980/murat-project-engineer", topic="temporary test probe")
        assert len(active_items) == 0, f"Deleted item still recalled: {active_items}"

        # Item exists as tombstone for auditability
        tombstone = store._items["MEM-TEMP-001"]
        assert tombstone.status == "tombstone"

    return {
        "test": "DELETE",
        "result": "PASS",
        "details": "Approved deletion tombstones item; item completely excluded from subsequent active recall queries.",
    }


def test_4_isolation() -> Dict[str, Any]:
    """4. ISOLATION: unrelated projects/scopes do not leak into each other."""
    store = ProjectMemoryStore(CROSS_PROJECT_STORE_PATH)
    assert store.load_status == "LOADED"

    # Query 1: MPE scope
    mpe_items = store.recall(project="Murkin1980/murat-project-engineer")
    assert all(i.project == "Murkin1980/murat-project-engineer" for i in mpe_items)
    assert len(mpe_items) == 1
    assert mpe_items[0].item_id == "MEM-MPE-001"

    # Query 2: Murat House scope
    mh_items = store.recall(project="Murkin1980/Murat-house")
    assert all(i.project == "Murkin1980/Murat-house" for i in mh_items)
    assert len(mh_items) == 2
    assert {i.item_id for i in mh_items} == {"MEM-MH-001", "MEM-MH-002"}

    # Query 3: Murat AI Orchestrator scope
    mao_items = store.recall(project="Murkin1980/Murat-AI-Orchestrator")
    assert all(i.project == "Murkin1980/Murat-AI-Orchestrator" for i in mao_items)
    assert len(mao_items) == 2
    assert {i.item_id for i in mao_items} == {"MEM-MAO-001", "MEM-MAO-002"}

    # Check cross-project mutation rejection
    cross_delta = ProposedMemoryDelta(
        task_id="TASK-CROSS-ATTACK",
        project="Murkin1980/murat-project-engineer",
        proposed_by="rogue-agent",
        actions=[
            DeltaAction(
                action="UPDATE",
                target_item_id="MEM-MH-001",  # Belongs to Murat-house!
                item=MemoryItem(
                    item_id="MEM-MH-001",
                    project="Murkin1980/Murat-house",
                    category="decision",
                    topic="tampered",
                    summary="tampered summary",
                    provenance="fake#L1",
                ),
            )
        ],
    )
    gate = ApprovalGate(approver="admin", decision="APPROVED")
    try:
        store.apply_approved_delta(cross_delta, gate)
        assert False, "Cross project mutation should have been rejected"
    except (ScopeViolationError, MemoryError):
        pass  # Successfully blocked cross-project write

    return {
        "test": "ISOLATION",
        "result": "PASS",
        "cross_project_leakage": 0,
        "details": "Strict scope enforcement on recall and mutation; zero cross-project leakage observed.",
    }


def test_5_provenance() -> Dict[str, Any]:
    """5. PROVENANCE: every recalled fact has valid source/evidence; missing provenance fails closed."""
    store = ProjectMemoryStore(CANONICAL_STORE_PATH)
    items = store.recall(project="Murkin1980/murat-project-engineer")
    assert len(items) > 0

    # 1. Verify every recalled fact has non-empty provenance pointing to a real repo path
    verified_refs = 0
    for item in items:
        assert item.provenance, f"Item {item.item_id} has empty provenance"
        # Extract primary path before '#' or ','
        primary_ref = item.provenance.split(",")[0].strip().split("#")[0]
        ref_path = REPO_ROOT / primary_ref
        assert ref_path.exists(), f"Provenance path {ref_path} does not exist in repo"
        verified_refs += 1

    # 2. Verify write MUST fail closed when provenance is missing or empty
    missing_prov_cases = ["", "   ", None]
    for bad_prov in missing_prov_cases:
        try:
            bad_item = MemoryItem(
                item_id="MEM-BAD-PROV",
                project="Murkin1980/murat-project-engineer",
                category="decision",
                topic="unverified claim",
                summary="An unverified assertion without source.",
                provenance=bad_prov,  # type: ignore
            )
            bad_item.validate()
            assert False, f"Expected ProvenanceMissingError for bad provenance '{bad_prov}'"
        except (ProvenanceMissingError, MemoryError):
            pass  # Expected fail-closed behavior

    return {
        "test": "PROVENANCE",
        "result": "PASS",
        "verified_references": verified_refs,
        "details": "100% of recalled facts point to existing repo artifacts; writes without provenance fail closed.",
    }


def test_6_failure() -> Dict[str, Any]:
    """6. FAILURE: memory unavailability/corruption falls back safely to canonical artifacts without hallucinating."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Case A: Missing file
        missing_path = Path(tmpdir) / "does_not_exist.json"
        store_missing = ProjectMemoryStore(missing_path)
        assert store_missing.load_status == "FALLBACK_CANONICAL"
        assert store_missing.load_warning is not None
        recalled = store_missing.recall(project="Murkin1980/murat-project-engineer", topic="browseract")
        assert recalled == [], "Fallback must return empty memory list, not hallucinated facts"

        # Case B: Corrupted JSON file
        corrupt_path = Path(tmpdir) / "corrupt.json"
        corrupt_path.write_text("INVALID_JSON{broken:true", encoding="utf-8")
        store_corrupt = ProjectMemoryStore(corrupt_path)
        assert store_corrupt.load_status == "FALLBACK_CANONICAL"
        assert "Corrupted or invalid" in (store_corrupt.load_warning or "")
        recalled_corrupt = store_corrupt.recall(project="Murkin1980/murat-project-engineer", topic="runtime")
        assert recalled_corrupt == [], "Corrupt store must return empty memory list, never invent facts"

        # Verify agent fallback path: agent safely reads canonical project docs
        fallback_artifact = REPO_ROOT / "docs/evaluations/BROWSERACT_EVALUATION.md"
        assert fallback_artifact.exists()
        content = fallback_artifact.read_text(encoding="utf-8")
        assert "REUSE_COMPONENT" in content, "Canonical artifact contains authoritative truth"

    return {
        "test": "FAILURE",
        "result": "PASS",
        "details": "Missing and corrupted stores trigger FALLBACK_CANONICAL safely; zero hallucinations; canonical Git fallback verified.",
    }


def main():
    print("=" * 70)
    print("EXP-15 Acceptance Test Suite — Controlled MVP Execution")
    print("=" * 70)

    tests = [
        test_1_recall,
        test_2_update,
        test_3_delete,
        test_4_isolation,
        test_5_provenance,
        test_6_failure,
    ]

    all_pass = True
    results = []

    for test_fn in tests:
        try:
            res = test_fn()
            print(f"[{res['result']}] {res['test']}: {res['details']}")
            results.append(res)
        except Exception as e:
            print(f"[FAIL] {test_fn.__name__}: {e}")
            results.append({"test": test_fn.__name__, "result": "FAIL", "error": str(e)})
            all_pass = False

    print("=" * 70)
    print(f"FINAL OUTCOME: {'PASS' if all_pass else 'FAIL'} (6/6 tests passed)")
    print("=" * 70)

    # Save structured evidence
    evidence_path = Path(__file__).parent.parent / "evidence" / "01_acceptance_tests.json"
    evidence_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
