#!/usr/bin/env python3
"""EXP-25 CP-03 + CP-04 deterministic proof runner.

Runs the bounded slice (contact → deal → task → activity timeline) and the
read-first tool surface against the MiniBase contract adapter, on the test
fixture only. Every claim in ``RESULTS.md`` is produced here; the runner exits
non-zero if any check fails.

Usage:
    python3 experiments/exp-25-atomic-crm-component-extraction/harness/run_proof.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HARNESS_DIR))

from crm_slice import (  # noqa: E402
    ACTIVITY,
    CONTACTS,
    DEALS,
    TASKS,
    CrmSlice,
    canonical_id,
    due_bucket,
    load_fixture_file,
)
from minibase_adapter import InMemoryMiniBase, MiniBaseError  # noqa: E402
from tool_surface import AVAILABLE_WRITE_TOOLS, TOOL_SPECS, AuditTrail, ToolSurface  # noqa: E402

EVIDENCE_DIR = HARNESS_DIR.parent / "evidence"


class SequenceClock:
    """Deterministic clock: starts at the fixture instant, advances one second per read."""

    def __init__(self, start: str) -> None:
        self.moment = datetime.fromisoformat(start.replace("Z", "+00:00"))

    def __call__(self) -> str:
        stamp = self.moment.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        self.moment += timedelta(seconds=1)
        return stamp


class CommandRecorder:
    """Stands in for the client: remembers the exact command it last sent.

    CP-05 replay is defined over the normalized payload, so a retry must resend
    byte-identical operations. Holding them here is what lets the proof show both
    a true replay and a conflict.
    """

    def __init__(self, store: InMemoryMiniBase) -> None:
        self.store = store
        self.operations: list[dict[str, object]] = []
        self.key: str | None = None

    def upsert_many(self, operations, idempotency_key):
        self.operations = json.loads(json.dumps(operations))
        self.key = idempotency_key
        return self.store.upsert_many(operations, idempotency_key)

    def __getattr__(self, name: str):
        return getattr(self.store, name)


class ProofRunner:
    def __init__(self) -> None:
        self.checks: list[dict[str, object]] = []
        self.lines: list[str] = []

    def log(self, text: str = "") -> None:
        self.lines.append(text)
        print(text)

    def check(self, name: str, condition: bool, observed: object = None) -> bool:
        self.checks.append({"check": name, "pass": bool(condition), "observed": observed})
        self.log(f"  [{'PASS' if condition else 'FAIL'}] {name}" + (f" — {observed}" if observed is not None else ""))
        return bool(condition)


def run() -> dict[str, object]:
    fixture = load_fixture_file(HARNESS_DIR / "fixtures.json")
    now = datetime.fromisoformat(fixture["now"].replace("Z", "+00:00"))
    clock = SequenceClock(fixture["now"])
    store = InMemoryMiniBase(clock=clock)
    recorder = CommandRecorder(store)
    slice_ = CrmSlice(recorder, clock=clock)
    runner = ProofRunner()

    runner.log("EXP-25 CP-03/CP-04 proof — Atomic CRM component extraction onto the MiniBase contract")
    runner.log(f"Fixture now (UTC): {fixture['now']}   dataset: {fixture['dataset']}   actor: {fixture['actor']}")
    runner.log("")

    # ------------------------------------------------------------------ CP-03
    runner.log("CP-03 — contact → deal → task → activity timeline (test data only)")
    written = slice_.load_fixture(fixture)

    runner.check(
        "fixture written through the slice (contacts/deals/tasks)",
        written == {"contacts": 3, "deals": 4, "tasks": 6},
        written,
    )
    runner.check(
        "every object keeps one canonical record ID",
        [
            store.get(CONTACTS, canonical_id("contact", "c-001"))["id"],
            store.get(DEALS, canonical_id("deal", "d-001"))["id"],
            store.get(TASKS, canonical_id("task", "t-001"))["id"],
        ]
        == ["contact-c-001", "deal-d-001", "task-t-001"],
        ["contact-c-001", "deal-d-001", "task-t-001"],
    )

    deal = store.get(DEALS, canonical_id("deal", "d-001"))
    task = store.get(TASKS, canonical_id("task", "t-001"))
    runner.check(
        "references repeat the same canonical identity (no second id scheme)",
        deal["data"]["contactIds"] == ["contact-c-001"]
        and task["data"]["contactId"] == "contact-c-001"
        and deal["data"]["schemaVersion"] == 1,
        {"deal.contactIds": deal["data"]["contactIds"], "task.contactId": task["data"]["contactId"]},
    )

    # Atomic's activity_log is a SQL UNION view; here each event is appended in the
    # same atomic command as the entity it describes.
    events = store.list(ACTIVITY, order={"field": "id", "direction": "asc"}, limit=100)
    created_pair_count = sum(
        1 for record in events["records"] if record["data"]["type"].endswith(".created")
    )
    runner.check(
        "entity + its history event are written as one CP-05 command (one event per entity: 3+4+6)",
        len(events["records"]) == written["contacts"] + written["deals"] + written["tasks"]
        and created_pair_count == 13,
        {"activityEvents": len(events["records"]), "createdEvents": created_pair_count},
    )

    contact = slice_.create_contact(
        "c-999",
        first_name="Test",
        last_name="Dangling",
        email="dangling@example.test",
        company_name="Nowhere",
        actor=fixture["actor"],
        correlation_id="exp25-ref-check",
    )
    try:
        slice_.create_deal(
            "d-999",
            name="Deal with a missing contact",
            contact_ids=["c-does-not-exist"],
            amount=10.0,
            expected_closing_date="2026-11-01",
            actor=fixture["actor"],
            correlation_id="exp25-ref-check",
        )
        referential_refused = False
    except MiniBaseError as error:
        referential_refused = error.code == "record_not_found"
    runner.check(
        "referential integrity is enforced in the app layer (mb_records has no FK)",
        referential_refused and "deal-d-999" not in {r["id"] for r in store.list(DEALS, limit=100)["records"]},
        {"errorCode": "record_not_found" if referential_refused else None, "danglingDealWritten": False},
    )

    timeline = slice_.timeline(contact_id="c-001")
    runner.check(
        "activity timeline merges contact/deal/task events, newest first, for one contact",
        len(timeline["events"]) == 5
        and sorted(timeline["types"])
        == sorted(
            ["contact.created", "deal.created", "deal.created", "task.created", "task.created"]
        )
        and timeline["events"][0]["data"]["type"] == "task.created"
        and timeline["events"][-1]["data"]["type"] == "contact.created"
        and timeline["events"][0]["data"]["subjects"]["contactIds"] == ["contact-c-001"],
        {"count": len(timeline["events"]), "types": timeline["types"]},
    )
    runner.check(
        "timeline events reference subjects instead of duplicating entity documents",
        all("payload" not in event["data"] for event in timeline["events"])
        and all(event["data"]["provenance"]["dataset"] == "exp-25-test" for event in timeline["events"]),
        {"sampleSubjects": timeline["events"][0]["data"]["subjects"]},
    )

    try:
        store.list(DEALS, filters={"stage": {"eq": "won"}})
        refused_json_filter = False
        refused_code = None
    except MiniBaseError as error:
        refused_json_filter = error.code == "invalid_filter"
        refused_code = error.code
    runner.check(
        "MiniBase refuses a filter on an arbitrary JSON field (the CP-02 fit limit)",
        refused_json_filter,
        {"errorCode": refused_code},
    )

    paged: list[str] = []
    after = None
    pages = 0
    while True:
        page = store.list(TASKS, order={"field": "id", "direction": "asc"}, limit=2, after=after)
        pages += 1
        paged.extend(record["id"] for record in page["records"])
        if not page["hasMore"]:
            break
        after = page["nextAfter"]
    runner.check(
        "keyset paging with hasMore returns every task exactly once",
        len(paged) == 6 and len(set(paged)) == 6 and pages == 3,
        {"pages": pages, "ids": paged},
    )

    # ------------------------------------------------------------ CP-03 result
    runner.log("")
    runner.log("CP-04 — read-first tool surface, one approval-gated write")
    audit = AuditTrail(clock)
    surface = ToolSurface(
        slice_,
        actor="exp-25-agent",
        now=now,
        clock=clock,
        write_budget=1,
        audit=audit,
    )
    runner.check(
        "tool surface exposes 3 reads and exactly 1 write",
        len([spec for spec in TOOL_SPECS if spec["readOnly"]]) == 3
        and AVAILABLE_WRITE_TOOLS == ("create_follow_up_task",),
        {"reads": [s["name"] for s in TOOL_SPECS if s["readOnly"]], "writes": list(AVAILABLE_WRITE_TOOLS)},
    )

    open_deals = surface.dispatch("list_open_deals")
    runner.check(
        "read: list_open_deals excludes won/lost and totals the open amount",
        open_deals["ok"]
        and [item["dealId"] for item in open_deals["result"]["openDeals"]] == ["deal-d-001", "deal-d-002"]
        and open_deals["result"]["openAmountTotal"] == 2430.0
        and open_deals["result"]["byStage"] == {"opportunity": 1, "proposal-sent": 1},
        {
            "openDeals": [item["dealId"] for item in open_deals["result"]["openDeals"]],
            "openAmountTotal": open_deals["result"]["openAmountTotal"],
            "byStage": open_deals["result"]["byStage"],
            "read": open_deals["result"]["read"],
        },
    )

    context = surface.dispatch("get_client_context", {"contactId": "c-001", "correlationId": "exp25-ctx-1"})
    runner.check(
        "read: get_client_context returns identity, deals, tasks, and timeline for one canonical contact",
        context["ok"]
        and context["result"]["contactId"] == "contact-c-001"
        and context["result"]["deals"] == ["deal-d-001", "deal-d-004"]
        and context["result"]["openDealCount"] == 1
        and context["result"]["pendingTaskCount"] == 2
        and context["result"]["activityEventCount"] == 5,
        {
            "contactId": context["result"]["contactId"],
            "deals": context["result"]["deals"],
            "openDealCount": context["result"]["openDealCount"],
            "pendingTaskCount": context["result"]["pendingTaskCount"],
            "activityEventCount": context["result"]["activityEventCount"],
            "reads": context["result"]["reads"],
        },
    )

    due = surface.dispatch("list_due_tasks", {"correlationId": "exp25-due-1"})
    runner.check(
        "read: list_due_tasks buckets pending tasks and drops the completed one",
        due["ok"]
        and due["result"]["bucketCounts"]
        == {"overdue": 1, "today": 1, "tomorrow": 1, "this-week": 1, "later": 1}
        and "task-t-006" not in [
            item["taskId"] for bucket in due["result"]["buckets"].values() for item in bucket
        ],
        {"bucketCounts": due["result"]["bucketCounts"], "read": due["result"]["read"]},
    )
    runner.check(
        "UTC day boundaries drive the buckets (Atomic uses browser-local day boundaries)",
        due_bucket("2026-10-05T15:00:00Z", now) == "overdue"
        and due_bucket("2026-10-07T10:00:00Z", now) == "tomorrow"
        and due_bucket("2026-10-10T23:00:00Z", now) == "this-week",
        {"weekEndExclusiveUtc": "2026-10-11T00:00:00Z"},
    )

    before_write = store.list(TASKS, limit=100)
    unapproved = surface.dispatch(
        "create_follow_up_task",
        {
            "contactId": "c-001",
            "taskId": "fu-c-001-unapproved",
            "text": "Send proposal draft",
            "dueDate": "2026-10-07T10:00:00Z",
            "correlationId": "exp25-write-deny",
        },
    )
    after_unapproved = store.list(TASKS, limit=100)
    runner.check(
        "write without explicit approval is refused and changes nothing",
        not unapproved["ok"]
        and unapproved["error"]["code"] == "approval_required"
        and len(after_unapproved["records"]) == len(before_write["records"]),
        {"errorCode": unapproved["error"]["code"], "tasksBefore": len(before_write["records"]),
         "tasksAfter": len(after_unapproved["records"])},
    )

    # A record that is not part of the EXP-25 test dataset, written straight onto
    # the adapter to simulate data the write must not be allowed to touch.
    store.put(
        CONTACTS,
        canonical_id("contact", "x-live-001"),
        {
            "schemaVersion": 1,
            "firstName": "Outside",
            "lastName": "Scope",
            "email": "outside@not-exp25.test",
            "companyName": "Not EXP-25 test data",
            "dataset": "not-exp-25",
        },
    )
    out_of_bounds = surface.dispatch(
        "create_follow_up_task",
        {
            "contactId": "x-live-001",
            "taskId": "fu-x-live-001",
            "text": "Attempt on a non-test record",
            "dueDate": "2026-10-07T10:00:00Z",
            "correlationId": "exp25-write-bounds",
            "approval": {
                "approved": True,
                "actor": "exp-25-agent",
                "reason": "bounds probe",
                "idempotencyKey": "exp25-bounds-probe",
            },
        },
    )
    runner.check(
        "an approved write is still refused against a record outside the EXP-25 test dataset",
        not out_of_bounds["ok"]
        and out_of_bounds["error"]["code"] == "write_out_of_bounds"
        and "task-fu-x-live-001"
        not in {record["id"] for record in store.list(TASKS, limit=100)["records"]},
        {"errorCode": out_of_bounds["error"]["code"]},
    )

    stage_write = surface.dispatch(
        "change_deal_stage",
        {
            "dealId": "d-001",
            "stage": "proposal-sent",
            "correlationId": "exp25-write-second-tool",
            "approval": {
                "approved": True,
                "actor": "exp-25-agent",
                "reason": "second write attempt",
                "idempotencyKey": "exp25-stage-probe",
            },
        },
    )
    runner.check(
        "the second candidate write (change_deal_stage) is declared but not exposed",
        not stage_write["ok"] and stage_write["error"]["code"] == "tool_not_available",
        {"errorCode": stage_write["error"]["code"]},
    )

    approved = surface.dispatch(
        "create_follow_up_task",
        {
            "contactId": "c-001",
            "dealId": "d-001",
            "taskId": "fu-c-001-proposal",
            "text": "Send proposal draft to Aigul",
            "dueDate": "2026-10-07T10:00:00Z",
            "taskType": "follow-up",
            "correlationId": "exp25-write-1",
            "approval": {
                "approved": True,
                "actor": "exp-25-agent",
                "reason": "Owner approved one bounded follow-up on the test contact",
                "idempotencyKey": "exp25-followup-c-001-1",
            },
        },
    )
    new_task = store.get(TASKS, "task-fu-c-001-proposal")
    runner.check(
        "approved write creates task + activity event in one atomic command",
        approved["ok"]
        and approved["result"]["operationCount"] == 2
        and approved["result"]["writtenRecords"]
        == ["crm_tasks/task-fu-c-001-proposal", "crm_activity_events/event-task-fu-c-001-proposal.task.created"]
        and new_task["data"]["contactId"] == "contact-c-001"
        and new_task["data"]["dealId"] == "deal-d-001",
        {
            "taskId": approved["result"]["taskId"],
            "writtenRecords": approved["result"]["writtenRecords"],
            "commandId": approved["result"]["commandId"],
            "preservedIds": {
                "contactId": new_task["data"]["contactId"],
                "dealId": new_task["data"]["dealId"],
            },
        },
    )

    # A retry is only a replay when the client resends the *identical* normalized
    # payload — including the timestamps it embedded. The recorder holds exactly
    # what the client sent for the approved write.
    replay_command = store.upsert_many(recorder.operations, recorder.key)
    tasks_after_replay = store.list(TASKS, limit=100)
    runner.check(
        "resending the identical command under the same key replays instead of duplicating",
        replay_command["replayed"] is True
        and replay_command["commandId"] == approved["result"]["commandId"]
        and len(tasks_after_replay["records"]) == 7,
        {"replayed": replay_command["replayed"], "taskCount": len(tasks_after_replay["records"])},
    )

    try:
        store.upsert_many(
            [
                {
                    "collection": TASKS,
                    "id": "task-fu-c-001-proposal",
                    "data": {"schemaVersion": 1, "text": "different payload", "dataset": "exp-25-test"},
                }
            ],
            "exp25-followup-c-001-1",
        )
        conflict_code = None
    except MiniBaseError as error:
        conflict_code = error.code
    runner.check(
        "same key with a different payload is an opaque conflict",
        conflict_code == "idempotency_conflict",
        {"errorCode": conflict_code},
    )

    second_write = surface.dispatch(
        "create_follow_up_task",
        {
            "contactId": "c-002",
            "taskId": "fu-c-002-extra",
            "text": "Extra write beyond the budget",
            "dueDate": "2026-10-07T10:00:00Z",
            "correlationId": "exp25-write-2",
            "approval": {
                "approved": True,
                "actor": "exp-25-agent",
                "reason": "Second write attempt in the same run",
                "idempotencyKey": "exp25-followup-c-002-2",
            },
        },
    )
    runner.check(
        "the write budget is finite: a second approved write is refused",
        not second_write["ok"] and second_write["error"]["code"] == "write_budget_exhausted",
        {"errorCode": second_write["error"]["code"], "writesUsed": surface.writes_used},
    )

    due_after = surface.dispatch("list_due_tasks", {"correlationId": "exp25-due-2"})
    runner.check(
        "the written follow-up is visible to a later read in its UTC bucket",
        any(
            item["taskId"] == "task-fu-c-001-proposal"
            for item in due_after["result"]["buckets"]["tomorrow"]
        ),
        {"tomorrow": [item["taskId"] for item in due_after["result"]["buckets"]["tomorrow"]]},
    )

    context_after = surface.dispatch("get_client_context", {"contactId": "c-001", "correlationId": "exp25-ctx-2"})
    runner.check(
        "the same canonical contact now shows one more pending task and one more event",
        context_after["result"]["pendingTaskCount"] == 3
        and context_after["result"]["activityEventCount"] == 6,
        {
            "pendingTaskCount": context_after["result"]["pendingTaskCount"],
            "activityEventCount": context_after["result"]["activityEventCount"],
            "recent": [item["type"] for item in context_after["result"]["recentActivity"][:2]],
        },
    )

    outcomes = [entry["outcome"] for entry in audit.entries]
    runner.check(
        "audit trail records every write and denial, with a key digest instead of the key",
        outcomes.count("success") == 1
        and outcomes.count("denied") == 3
        and all("idempotencyKey" not in json.dumps(entry) for entry in audit.entries)
        and any(entry["metadata"].get("idempotencyDigest") for entry in audit.entries),
        {"outcomes": outcomes, "entries": len(audit.entries)},
    )
    runner.check(
        "successful reads are not audited (MiniBase audits denials and mutations only)",
        all(entry["action"].startswith("crm.task") or entry["action"].startswith("crm.tool") for entry in audit.entries),
        {"actions": sorted({entry["action"] for entry in audit.entries})},
    )

    runner.log("")
    runner.log(
        f"MiniBase statements executed by the whole proof (pages, record reads, commands): {store.statements}"
    )
    runner.log("")

    passed = sum(1 for item in runner.checks if item["pass"])
    failed = len(runner.checks) - passed
    runner.log(f"Checks: {passed} passed, {failed} failed, {len(runner.checks)} total")

    evidence = {
        "experiment": "EXP-25",
        "checkpoints": ["CP-03", "CP-04"],
        "runDate": "2026-10-06",
        "upstreamPin": {
            "donor": "marmelab/atomic-crm",
            "commit": "8b5d47ba32190c68801a427ef7682d7a6afc14e0",
        },
        "hostContractPin": {
            "host": "Murkin1980/minibase-cloudflare",
            "commit": "9ab38d832970b3956cf0f831f9b578f7b9fd9001",
        },
        "fixture": {
            "dataset": fixture["dataset"],
            "now": fixture["now"],
            "counts": {
                "contacts": len(fixture["contacts"]),
                "deals": len(fixture["deals"]),
                "tasks": len(fixture["tasks"]),
                "completedTasks": len(fixture["completedTasks"]),
            },
        },
        "checks": runner.checks,
        "summary": {
            "total": len(runner.checks),
            "passed": passed,
            "failed": failed,
            "minibaseStatements": store.statements,
            "writesUsed": surface.writes_used,
            "auditOutcomes": {
                "success": outcomes.count("success"),
                "denied": outcomes.count("denied"),
            },
        },
        "results": {
            "openDeals": open_deals["result"],
            "clientContextBefore": context["result"],
            "clientContextAfter": context_after["result"],
            "dueTasksBefore": due["result"],
            "dueTasksAfter": due_after["result"],
            "approvedWrite": approved["result"],
            "replayedWrite": {
                "replayed": replay_command["replayed"],
                "commandId": replay_command["commandId"],
            },
            "timelineForContactC001": {
                "types": timeline["types"],
                "scanned": timeline["scanned"],
                "pages": timeline["pages"],
                "truncated": timeline["truncated"],
            },
            "denials": [
                {"tool": item["tool"], "code": item["error"]["code"]}
                for item in (unapproved, out_of_bounds, stage_write, second_write)
            ],
        },
        "auditTrail": audit.entries,
    }

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    (EVIDENCE_DIR / "proof_run.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (EVIDENCE_DIR / "proof_run.log").write_text("\n".join(runner.lines) + "\n", encoding="utf-8")
    return evidence


if __name__ == "__main__":
    result = run()
    sys.exit(1 if result["summary"]["failed"] else 0)
