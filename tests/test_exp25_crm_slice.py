"""EXP-25 — Atomic CRM component extraction onto the MiniBase contract.

These tests execute the experiment-local proof in
``experiments/exp-25-atomic-crm-component-extraction/harness``: the in-memory
MiniBase data-plane adapter, the CP-03 slice (contact → deal → task → activity
timeline), and the CP-04 read-first tool surface. They test contract behavior
(the closed CP-04 query allowlist, CP-05 idempotency, canonical UTC timestamps,
approval-gated writes), not implementation trivia.
"""

import contextlib
import io
import json
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "experiments" / "exp-25-atomic-crm-component-extraction" / "harness"
sys.path.insert(0, str(HARNESS))

import crm_slice  # noqa: E402
import run_proof  # noqa: E402
from crm_slice import ACTIVITY, CONTACTS, DEALS, TASKS, CrmSlice, canonical_id, due_bucket  # noqa: E402
from minibase_adapter import InMemoryMiniBase, MiniBaseError, canonical_utc  # noqa: E402
from tool_surface import AVAILABLE_WRITE_TOOLS, TOOL_SPECS, AuditTrail, ToolSurface  # noqa: E402

FIXTURE = json.loads((HARNESS / "fixtures.json").read_text(encoding="utf-8"))
NOW = datetime.fromisoformat(FIXTURE["now"].replace("Z", "+00:00"))


def seeded_slice():
    clock = run_proof.SequenceClock(FIXTURE["now"])
    store = InMemoryMiniBase(clock=clock)
    slice_ = CrmSlice(store, clock=clock)
    slice_.load_fixture(FIXTURE)
    return store, slice_, clock


class MiniBaseAdapterContractTests(unittest.TestCase):
    def setUp(self):
        self.clock = run_proof.SequenceClock(FIXTURE["now"])
        self.store = InMemoryMiniBase(clock=self.clock, max_bulk_records=3)

    def test_collection_and_record_id_patterns_are_enforced(self):
        with self.assertRaises(MiniBaseError) as raised:
            self.store.put("Bad Collection", "rec-1", {"schemaVersion": 1})
        self.assertEqual(raised.exception.code, "invalid_collection")
        with self.assertRaises(MiniBaseError) as raised:
            self.store.put("crm_contacts", "bad id!", {"schemaVersion": 1})
        self.assertEqual(raised.exception.code, "invalid_record_id")
        with self.assertRaises(MiniBaseError) as raised:
            self.store.put("crm_contacts", "contact-c-001", ["not", "an", "object"])
        self.assertEqual(raised.exception.code, "invalid_record_data")

    def test_timestamps_are_stored_in_canonical_utc(self):
        record = self.store.put("crm_contacts", "contact-c-001", {"schemaVersion": 1})
        self.assertRegex(record["createdAt"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
        self.assertEqual(record["createdAt"], record["updatedAt"])
        self.assertEqual(canonical_utc("2026-10-06T05:00:00+05:00"), "2026-10-06T00:00:00.000Z")
        with self.assertRaises(MiniBaseError) as raised:
            canonical_utc("2026-10-06T00:00:00")  # no timezone: refused, not guessed
        self.assertEqual(raised.exception.code, "invalid_filter")

    def test_json_field_filters_are_refused_by_the_closed_query_contract(self):
        self.store.put(DEALS, "deal-d-001", {"schemaVersion": 1, "stage": "won"})
        for filters in ({"stage": {"eq": "won"}}, {"data.stage": {"eq": "won"}}, {"contactIds": {"eq": "x"}}):
            with self.subTest(filters=filters):
                with self.assertRaises(MiniBaseError) as raised:
                    self.store.list(DEALS, filters=filters)
                self.assertEqual(raised.exception.code, "invalid_filter")
        # The one JSON field the contract does allow.
        page = self.store.list(DEALS, filters={"schemaVersion": {"eq": 1}})
        self.assertEqual([record["id"] for record in page["records"]], ["deal-d-001"])

    def test_order_select_limit_and_cursor_are_validated(self):
        self.store.put(TASKS, "task-t-001", {"schemaVersion": 1})
        with self.assertRaises(MiniBaseError) as raised:
            self.store.list(TASKS, order={"field": "stage", "direction": "asc"})
        self.assertEqual(raised.exception.code, "invalid_order")
        with self.assertRaises(MiniBaseError) as raised:
            self.store.list(TASKS, select=["id", "collection"])
        self.assertEqual(raised.exception.code, "invalid_select")
        with self.assertRaises(MiniBaseError) as raised:
            self.store.list(TASKS, limit=0)
        self.assertEqual(raised.exception.code, "invalid_limit")
        with self.assertRaises(MiniBaseError) as raised:
            self.store.list(TASKS, order={"field": "updatedAt", "direction": "desc"}, after="not-a-cursor")
        self.assertEqual(raised.exception.code, "invalid_cursor")

    def test_a_cursor_from_another_query_is_refused(self):
        for index in range(4):
            self.store.put(TASKS, f"task-t-00{index}", {"schemaVersion": 1})
        page = self.store.list(TASKS, filters={"schemaVersion": {"eq": 1}}, limit=2)
        self.assertTrue(page["hasMore"])
        with self.assertRaises(MiniBaseError) as raised:
            self.store.list(TASKS, filters={"schemaVersion": {"eq": 2}}, limit=2, after=page["nextAfter"])
        self.assertEqual(raised.exception.code, "invalid_cursor")

    def test_keyset_paging_never_skips_or_repeats_a_record(self):
        ids = [f"task-t-{index:03d}" for index in range(7)]
        for record_id in ids:
            self.store.put(TASKS, record_id, {"schemaVersion": 1})
        seen, after = [], None
        while True:
            page = self.store.list(TASKS, order={"field": "id", "direction": "asc"}, limit=3, after=after)
            seen.extend(record["id"] for record in page["records"])
            if not page["hasMore"]:
                break
            after = page["nextAfter"]
        self.assertEqual(seen, sorted(ids))

    def test_command_is_atomic_replayable_and_conflict_opaque(self):
        operations = [
            {"collection": TASKS, "id": "task-t-001", "data": {"schemaVersion": 1, "text": "a"}},
            {"collection": ACTIVITY, "id": "event-e-001", "data": {"schemaVersion": 1, "type": "task.created"}},
        ]
        first = self.store.upsert_many(operations, "key-1")
        self.assertFalse(first["replayed"])
        self.assertEqual(first["operationCount"], 2)

        replayed = self.store.upsert_many(operations, "key-1")
        self.assertTrue(replayed["replayed"])
        self.assertEqual(replayed["commandId"], first["commandId"])

        changed = [dict(operations[0], data={"schemaVersion": 1, "text": "b"}), operations[1]]
        with self.assertRaises(MiniBaseError) as raised:
            self.store.upsert_many(changed, "key-1")
        self.assertEqual(raised.exception.code, "idempotency_conflict")
        self.assertEqual(self.store.get(TASKS, "task-t-001")["data"]["text"], "a")

    def test_command_validation_refuses_internal_collections_duplicates_and_oversize(self):
        with self.assertRaises(MiniBaseError) as raised:
            self.store.upsert_many([{"collection": "mb_records", "id": "x", "data": {}}], "key-2")
        self.assertEqual(raised.exception.code, "invalid_collection")
        duplicate = [
            {"collection": TASKS, "id": "task-t-001", "data": {"schemaVersion": 1}},
            {"collection": TASKS, "id": "task-t-001", "data": {"schemaVersion": 1}},
        ]
        with self.assertRaises(MiniBaseError) as raised:
            self.store.upsert_many(duplicate, "key-3")
        self.assertEqual(raised.exception.code, "invalid_command")
        oversized = [{"collection": TASKS, "id": f"task-t-{i}", "data": {"schemaVersion": 1}} for i in range(4)]
        with self.assertRaises(MiniBaseError) as raised:
            self.store.upsert_many(oversized, "key-4")
        self.assertEqual(raised.exception.code, "bulk_limit_exceeded")
        with self.assertRaises(MiniBaseError) as raised:
            self.store.upsert_many(
                [{"collection": TASKS, "id": "task-t-001", "data": {"schemaVersion": 1}}], ""
            )
        self.assertEqual(raised.exception.code, "invalid_idempotency_key")

    def test_a_refused_command_writes_nothing(self):
        mixed = [
            {"collection": TASKS, "id": "task-t-001", "data": {"schemaVersion": 1}},
            {"collection": "Bad Collection", "id": "x", "data": {}},
        ]
        with self.assertRaises(MiniBaseError):
            self.store.upsert_many(mixed, "key-5")
        self.assertEqual(self.store.list(TASKS, limit=10)["records"], [])


class CrmSliceTests(unittest.TestCase):
    def setUp(self):
        self.store, self.slice, self.clock = seeded_slice()

    def test_one_object_one_identity_many_representations(self):
        deal = self.store.get(DEALS, "deal-d-001")
        task = self.store.get(TASKS, "task-t-001")
        events = self.store.list(ACTIVITY, filters={"id": {"eq": "event-deal-d-001.deal.created"}})
        self.assertEqual(deal["data"]["contactIds"], ["contact-c-001"])
        self.assertEqual(task["data"]["contactId"], "contact-c-001")
        self.assertEqual(
            events["records"][0]["data"]["subjects"],
            {"dealIds": ["deal-d-001"], "contactIds": ["contact-c-001"]},
        )
        self.assertEqual(canonical_id("deal", "d-001"), "deal-d-001")
        self.assertEqual(crm_slice.kind_of("contact-c-001"), "contact")

    def test_entity_and_history_event_are_written_by_one_command(self):
        statements_before = self.store.statements
        self.slice.create_task(
            "t-100",
            text="Extra task",
            contact_id="c-001",
            due_date="2026-10-08T09:00:00Z",
            actor="exp-25-owner",
            correlation_id="exp25-test-atomic",
        )
        self.assertEqual(self.store.statements - statements_before, 3)  # command + 2 confirming reads
        self.assertIsNotNone(self.store.get(TASKS, "task-t-100"))
        self.assertIsNotNone(self.store.get(ACTIVITY, "event-task-t-100.task.created"))

    def test_a_deal_cannot_reference_a_missing_contact(self):
        with self.assertRaises(MiniBaseError) as raised:
            self.slice.create_deal(
                "d-404",
                name="Dangling",
                contact_ids=["c-missing"],
                amount=1.0,
                expected_closing_date="2026-11-01",
                actor="exp-25-owner",
                correlation_id="exp25-test-fk",
            )
        self.assertEqual(raised.exception.code, "record_not_found")
        self.assertEqual(
            [record["id"] for record in self.store.list(DEALS, limit=50)["records"]],
            ["deal-d-001", "deal-d-002", "deal-d-003", "deal-d-004"],
        )

    def test_stage_change_preserves_identity_and_records_both_ends(self):
        before = self.slice.change_deal_stage(
            "d-001",
            stage="proposal-sent",
            actor="exp-25-owner",
            correlation_id="exp25-test-stage",
            reason="Owner approved the stage move",
        )
        self.assertEqual(before["deal"]["id"], "deal-d-001")
        self.assertEqual((before["from"], before["to"]), ("opportunity", "proposal-sent"))
        events = self.slice.timeline(deal_id="d-001")
        self.assertEqual(events["types"][0], "deal.stage_changed")
        self.assertEqual(
            events["events"][0]["data"]["change"],
            {"field": "stage", "from": "opportunity", "to": "proposal-sent"},
        )

    def test_timeline_is_scoped_to_one_subject_and_newest_first(self):
        timeline = self.slice.timeline(contact_id="c-001")
        self.assertEqual(len(timeline["events"]), 5)
        stamps = [event["data"]["occurredAt"] for event in timeline["events"]]
        self.assertEqual(stamps, sorted(stamps, reverse=True))
        for event in timeline["events"]:
            self.assertIn("contact-c-001", event["data"]["subjects"]["contactIds"])
            self.assertNotIn("payload", event["data"])
        with self.assertRaises(ValueError):
            self.slice.timeline()

    def test_derived_reads_report_their_page_cost(self):
        result = self.slice.open_deals(limit=50)
        self.assertEqual([record["id"] for record in result["records"]], ["deal-d-001", "deal-d-002"])
        self.assertEqual(result["byStage"], {"opportunity": 1, "proposal-sent": 1})
        self.assertEqual(result["openAmountTotal"], 2430.0)
        self.assertEqual(result["scanned"], 4)
        self.assertFalse(result["truncated"])

        bounded = CrmSlice(self.store, clock=self.clock, max_pages=1).open_deals(limit=2)
        self.assertTrue(bounded["truncated"])
        self.assertEqual(bounded["pages"], 1)

    def test_due_buckets_use_utc_day_boundaries(self):
        self.assertEqual(due_bucket("2026-10-05T23:59:59Z", NOW), "overdue")
        self.assertEqual(due_bucket("2026-10-06T00:00:00Z", NOW), "today")
        self.assertEqual(due_bucket("2026-10-06T23:59:59Z", NOW), "today")
        self.assertEqual(due_bucket("2026-10-07T00:00:00Z", NOW), "tomorrow")
        self.assertEqual(due_bucket("2026-10-10T23:59:59Z", NOW), "this-week")
        self.assertEqual(due_bucket("2026-10-11T00:00:00Z", NOW), "later")

        due = self.slice.due_tasks(NOW)
        self.assertEqual(
            due["bucketCounts"],
            {"overdue": 1, "today": 1, "tomorrow": 1, "this-week": 1, "later": 1},
        )
        self.assertNotIn("task-t-006", due["buckets"]["today"])  # completed task excluded


class ToolSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.store, self.slice, self.clock = seeded_slice()
        self.audit = AuditTrail(self.clock)
        self.surface = ToolSurface(
            self.slice, actor="exp-25-agent", now=NOW, clock=self.clock, write_budget=1, audit=self.audit
        )
        self.approval = {
            "approved": True,
            "actor": "exp-25-agent",
            "reason": "Owner approved one bounded follow-up",
            "idempotencyKey": "test-key-1",
        }

    def test_surface_shape_is_three_reads_and_one_exposed_write(self):
        self.assertEqual(
            [spec["name"] for spec in TOOL_SPECS if spec["readOnly"]],
            ["list_open_deals", "get_client_context", "list_due_tasks"],
        )
        self.assertEqual(AVAILABLE_WRITE_TOOLS, ("create_follow_up_task",))

    def test_reads_do_not_mutate(self):
        before = self.store.statements
        for tool, args in (
            ("list_open_deals", {}),
            ("get_client_context", {"contactId": "c-001"}),
            ("list_due_tasks", {}),
        ):
            with self.subTest(tool=tool):
                result = self.surface.dispatch(tool, args)
                self.assertTrue(result["ok"])
        self.assertEqual(self.audit.entries, [])  # successful reads are not audited
        self.assertEqual(
            len(self.store.list(TASKS, limit=50)["records"]),
            len(FIXTURE["tasks"]),
        )
        self.assertGreater(self.store.statements, before)

    def test_unknown_tool_and_missing_arguments_are_refused(self):
        unknown = self.surface.dispatch("drop_everything")
        self.assertFalse(unknown["ok"])
        self.assertEqual(unknown["error"]["code"], "unknown_tool")
        missing = self.surface.dispatch("get_client_context", {})
        self.assertEqual(missing["error"]["code"], "missing_argument")

    def test_write_requires_explicit_approval(self):
        result = self.surface.dispatch(
            "create_follow_up_task",
            {"contactId": "c-001", "text": "No approval", "dueDate": "2026-10-07T10:00:00Z"},
        )
        self.assertEqual(result["error"]["code"], "approval_required")
        self.assertEqual(self.audit.entries[-1]["outcome"], "denied")
        self.assertEqual(len(self.store.list(TASKS, limit=50)["records"]), len(FIXTURE["tasks"]))

    def test_approved_write_is_atomic_id_preserving_and_audited(self):
        result = self.surface.dispatch(
            "create_follow_up_task",
            {
                "contactId": "c-001",
                "dealId": "d-001",
                "taskId": "fu-1",
                "text": "Send proposal draft",
                "dueDate": "2026-10-07T10:00:00Z",
                "approval": self.approval,
                "correlationId": "test-write-1",
            },
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["result"]["operationCount"], 2)
        self.assertEqual(result["result"]["contactId"], "contact-c-001")
        self.assertEqual(result["result"]["dealId"], "deal-d-001")
        task = self.store.get(TASKS, result["result"]["taskId"])
        self.assertEqual(task["data"]["contactId"], "contact-c-001")
        self.assertEqual(task["data"]["dealId"], "deal-d-001")

        entry = self.audit.entries[-1]
        self.assertEqual((entry["action"], entry["outcome"]), ("crm.task.created", "success"))
        self.assertEqual(entry["correlation_id"], "test-write-1")
        self.assertNotIn("test-key-1", json.dumps(entry))  # only the digest is stored
        self.assertEqual(len(entry["metadata"]["idempotencyDigest"]), 16)

    def test_write_is_bounded_to_exp25_test_data(self):
        self.store.put(
            CONTACTS,
            "contact-x-live",
            {"schemaVersion": 1, "firstName": "Out", "lastName": "OfScope", "dataset": "live"},
        )
        result = self.surface.dispatch(
            "create_follow_up_task",
            {
                "contactId": "x-live",
                "text": "Should be refused",
                "dueDate": "2026-10-07T10:00:00Z",
                "approval": dict(self.approval, idempotencyKey="test-key-bounds"),
            },
        )
        self.assertEqual(result["error"]["code"], "write_out_of_bounds")
        self.assertEqual(self.audit.entries[-1]["outcome"], "denied")
        self.assertEqual(self.surface.writes_used, 0)  # a denial spends no budget

    def test_second_candidate_write_is_not_exposed(self):
        result = self.surface.dispatch(
            "change_deal_stage",
            {"dealId": "d-001", "stage": "won", "approval": self.approval},
        )
        self.assertEqual(result["error"]["code"], "tool_not_available")

    def test_write_budget_is_finite(self):
        for index in (1, 2):
            self.surface.dispatch(
                "create_follow_up_task",
                {
                    "contactId": "c-001",
                    "taskId": f"fu-{index}",
                    "text": f"Follow-up {index}",
                    "dueDate": "2026-10-07T10:00:00Z",
                    "approval": dict(self.approval, idempotencyKey=f"test-key-{index}"),
                },
            )
        self.assertEqual(self.surface.writes_used, 1)
        self.assertEqual(self.audit.entries[-1]["metadata"]["reason"], "write_budget_exhausted")
        self.assertEqual(len(self.store.list(TASKS, limit=50)["records"]), len(FIXTURE["tasks"]) + 1)


class ProofRunnerTests(unittest.TestCase):
    def test_the_full_proof_runs_with_zero_failing_checks(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            evidence = run_proof.run()
        self.assertEqual(evidence["summary"]["failed"], 0)
        self.assertEqual(evidence["summary"]["total"], len(evidence["checks"]))
        self.assertGreaterEqual(evidence["summary"]["total"], 20)
        self.assertEqual(evidence["summary"]["auditOutcomes"], {"success": 1, "denied": 3})
        self.assertEqual(
            evidence["results"]["openDeals"]["openDeals"][0]["dealId"], "deal-d-001"
        )

    def test_evidence_artifacts_are_valid_json(self):
        evidence_path = HARNESS.parent / "evidence" / "proof_run.json"
        self.assertTrue(evidence_path.is_file())
        payload = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["experiment"], "EXP-25")
        self.assertEqual(payload["hostContractPin"]["host"], "Murkin1980/minibase-cloudflare")
        self.assertTrue((HARNESS.parent / "evidence" / "proof_run.log").is_file())


if __name__ == "__main__":
    unittest.main()
