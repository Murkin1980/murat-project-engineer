#!/usr/bin/env python3
"""EXP-25 CP-03 bounded slice: contact → deal → task → activity timeline.

The slice is the *framework-neutral* half of Atomic CRM's domain model, mapped
onto the MiniBase data-plane contract implemented in ``minibase_adapter.py``.
It runs on test data only; there is no CRM runtime, no auth, no network, and no
new storage system.

Donor concepts and where each one lands:

- entity model (``contact`` / ``deal`` / ``task``) — from
  ``src/components/atomic-crm/types.ts`` @ marmelab/atomic-crm ``8b5d47ba``.
  Stored as MiniBase documents in four collections, one canonical record ID per
  business object, ``schemaVersion: 1`` on every document.
- deal stages — from ``root/defaultConfiguration.ts`` (``defaultDealStages``,
  ``defaultDealPipelineStatuses``). Kept as configuration, not as a schema.
- due-date buckets — a UTC port of ``tasks/tasksPredicate.ts``
  (``isOverdue``/``isDueToday``/``isDueTomorrow``/``isDueThisWeek``/``isDueLater``,
  plus the 5-minute ``isRecentlyDone`` window).
- activity history — Atomic derives ``activity_log`` as a SQL ``UNION ALL`` view
  (``supabase/migrations/20260314120000_activity_log_view.sql``) with synthetic
  ids such as ``'deal.' || d.id || '.created'``. MiniBase has no joins or views,
  so the same event list is an **appended collection** written atomically with
  its entity by the CP-05 command. Events carry subject IDs and a short summary,
  never a second copy of the entity document.

Deliberate deviations, all forced by the host contract and recorded in
``MINIBASE_FIT.md``:

- stage/due-date selection is app-side. The CP-04 query contract filters only
  ``id``, ``createdAt``, ``updatedAt``, and ``schemaVersion``; MiniBase refuses a
  filter on an arbitrary JSON field, and that refusal is asserted in the tests.
- derived counters (Atomic's ``nb_tasks`` in ``contacts_summary``) are computed
  from the page that was read, with the read cost reported, not by a view.
- referential integrity is an application check: ``mb_records`` has no foreign
  keys, so a deal must verify its contacts exist before writing.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from minibase_adapter import canonical_utc

SCHEMA_VERSION = 1

# One collection per object type, plus the appended event collection. Every name
# satisfies MiniBase's ^[a-z][a-z0-9_-]{1,62}$ collection pattern and none uses
# the reserved mb_ prefix.
CONTACTS = "crm_contacts"
DEALS = "crm_deals"
TASKS = "crm_tasks"
ACTIVITY = "crm_activity_events"
COLLECTIONS = (CONTACTS, DEALS, TASKS, ACTIVITY)

# One object → one identity → many representations. The record ID *is* the
# canonical identity, and every reference elsewhere repeats that same string.
IDENTITY_PREFIX = {"contact": "contact-", "deal": "deal-", "task": "task-", "event": "event-"}

# Atomic CRM root/defaultConfiguration.ts
DEAL_STAGES = (
    "opportunity",
    "proposal-sent",
    "in-negociation",
    "won",
    "lost",
    "delayed",
)
# defaultDealPipelineStatuses = ["won"]; "lost" is terminal for pipeline purposes.
TERMINAL_STAGES = ("won", "lost")
TASK_TYPES = ("none", "email", "demo", "lunch", "meeting", "follow-up", "thank-you", "ship", "call")

# Activity event types, named after src/components/atomic-crm/consts.ts and
# extended with the two state transitions this slice proves.
EVENT_CONTACT_CREATED = "contact.created"
EVENT_DEAL_CREATED = "deal.created"
EVENT_DEAL_STAGE_CHANGED = "deal.stage_changed"
EVENT_TASK_CREATED = "task.created"

DATASET = "exp-25-test"


def canonical_id(kind: str, key: str) -> str:
    """Build the one canonical record ID for a business object."""
    if kind not in IDENTITY_PREFIX:
        raise ValueError(f"unknown identity kind: {kind}")
    if not key or any(char.isspace() for char in key):
        raise ValueError(f"invalid identity key: {key!r}")
    return f"{IDENTITY_PREFIX[kind]}{key}"


def kind_of(record_id: str) -> str:
    """Recover the object kind from its canonical ID (used by the tool surface)."""
    for kind, prefix in IDENTITY_PREFIX.items():
        if record_id.startswith(prefix):
            return kind
    raise ValueError(f"not a canonical EXP-25 identity: {record_id}")


def start_of_utc_day(moment: datetime) -> datetime:
    return moment.astimezone(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)


def due_bucket(due_date: str, now: datetime) -> str:
    """UTC port of Atomic CRM's ``tasksPredicate.ts`` buckets.

    Atomic computes these against the browser's local day (date-fns
    ``startOfToday`` and friends). MiniBase stores canonical UTC and compares
    timestamps as TEXT, so the bucket boundaries are computed in UTC against an
    injected ``now`` — same five buckets, one unambiguous boundary.
    """
    due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
    today = start_of_utc_day(now)
    end_of_today = today + timedelta(days=1)
    end_of_tomorrow = today + timedelta(days=2)
    # date-fns endOfWeek({ weekStartsOn: 0 }): the week ends on Saturday, so the
    # exclusive upper bound is the instant Sunday 00:00 UTC starts.
    days_until_saturday = (5 - today.weekday()) % 7  # Monday=0 … Sunday=6
    end_of_week = today + timedelta(days=days_until_saturday + 1)

    if due < today:
        return "overdue"
    if due < end_of_today:
        return "today"
    if due < end_of_tomorrow:
        return "tomorrow"
    if due < end_of_week:
        return "this-week"
    return "later"


def is_open_deal(deal: dict[str, Any]) -> bool:
    """A deal is open while it is neither in a terminal stage nor archived."""
    return deal.get("stage") not in TERMINAL_STAGES and not deal.get("archivedAt")


class CrmSlice:
    """The bounded CRM slice over one MiniBase project's data plane."""

    def __init__(
        self,
        store: Any,
        clock: Callable[[], str],
        source: str = "exp-25-proof",
        max_pages: int = 3,
    ) -> None:
        self.store = store
        self.clock = clock
        self.source = source
        # Hard bound on how many keyset pages any derived read may walk. MiniBase
        # offers no server-side filter on a JSON field, so a derived read either
        # stops at a declared budget or it is not bounded.
        self.max_pages = max_pages

    # ------------------------------------------------------------- identities

    @staticmethod
    def _identity_digest(record_id: str) -> str:
        return hashlib.sha256(record_id.encode("utf-8")).hexdigest()[:16]

    def _event(
        self,
        event_type: str,
        actor: str,
        subjects: dict[str, list[str]],
        summary: str,
        correlation_id: str,
        idempotency_key: str,
        change: dict[str, Any] | None = None,
        origin: str = "exp-25-harness",
    ) -> dict[str, Any]:
        """One activity event document: references and a summary, no payload copy."""
        return {
            "schemaVersion": SCHEMA_VERSION,
            "type": event_type,
            "occurredAt": self.clock(),
            "actor": actor,
            "subjects": {kind: list(ids) for kind, ids in subjects.items() if ids},
            "summary": summary,
            "change": change,
            "provenance": {
                "source": self.source,
                "origin": origin,
                "dataset": DATASET,
                "correlationId": correlation_id,
                # The raw idempotency key is never stored, matching MiniBase's
                # rule that only its SHA-256 digest is persisted.
                "idempotencyDigest": hashlib.sha256(idempotency_key.encode("utf-8")).hexdigest()[:16],
            },
        }

    def _write(
        self,
        operations: list[dict[str, Any]],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Entity + its history event in one atomic, replayable command."""
        return self.store.upsert_many(operations, idempotency_key)

    # --------------------------------------------------------------- writes

    def create_contact(
        self,
        contact_id: str,
        *,
        first_name: str,
        last_name: str,
        email: str,
        company_name: str,
        actor: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        record_id = canonical_id("contact", contact_id)
        document = {
            "schemaVersion": SCHEMA_VERSION,
            "firstName": first_name,
            "lastName": last_name,
            "email": email.lower(),
            "companyName": company_name,
            "status": "cold",
            "dataset": DATASET,
        }
        event = self._event(
            EVENT_CONTACT_CREATED,
            actor,
            {"contactIds": [record_id]},
            f"Contact created: {first_name} {last_name} ({company_name})",
            correlation_id,
            f"contact:{record_id}",
        )
        event_id = canonical_id("event", f"{record_id}.{EVENT_CONTACT_CREATED}")
        result = self._write(
            [
                {"collection": CONTACTS, "id": record_id, "data": document},
                {"collection": ACTIVITY, "id": event_id, "data": event},
            ],
            f"contact-create:{record_id}",
        )
        return {"contact": self.store.get(CONTACTS, record_id), "command": result}

    def create_deal(
        self,
        deal_id: str,
        *,
        name: str,
        contact_ids: list[str],
        amount: float,
        stage: str = DEAL_STAGES[0],
        expected_closing_date: str,
        actor: str,
        correlation_id: str,
    ) -> dict[str, Any]:
        record_id = canonical_id("deal", deal_id)
        if stage not in DEAL_STAGES:
            raise ValueError(f"unknown deal stage: {stage}")
        contacts = [canonical_id("contact", key) for key in contact_ids]
        # mb_records has no foreign keys: the reference is checked here, and the
        # check is what keeps a deal from pointing at a contact that does not exist.
        for contact in contacts:
            self.store.get(CONTACTS, contact)

        document = {
            "schemaVersion": SCHEMA_VERSION,
            "name": name,
            "contactIds": contacts,
            "stage": stage,
            "amount": amount,
            "expectedClosingDate": expected_closing_date,
            "archivedAt": None,
            "dataset": DATASET,
        }
        event = self._event(
            EVENT_DEAL_CREATED,
            actor,
            {"dealIds": [record_id], "contactIds": contacts},
            f"Deal created: {name} at stage {stage}",
            correlation_id,
            f"deal:{record_id}",
            change={"field": "stage", "from": None, "to": stage},
        )
        event_id = canonical_id("event", f"{record_id}.{EVENT_DEAL_CREATED}")
        result = self._write(
            [
                {"collection": DEALS, "id": record_id, "data": document},
                {"collection": ACTIVITY, "id": event_id, "data": event},
            ],
            f"deal-create:{record_id}",
        )
        return {"deal": self.store.get(DEALS, record_id), "command": result}

    def create_task(
        self,
        task_id: str,
        *,
        text: str,
        contact_id: str,
        due_date: str,
        task_type: str = "follow-up",
        deal_id: str | None = None,
        actor: str,
        correlation_id: str,
        origin: str = "exp-25-harness",
        idempotency_key: str | None = None,
        reason: str | None = None,
    ) -> dict[str, Any]:
        record_id = canonical_id("task", task_id)
        if task_type not in TASK_TYPES:
            raise ValueError(f"unknown task type: {task_type}")
        contact = canonical_id("contact", contact_id)
        self.store.get(CONTACTS, contact)
        deal = canonical_id("deal", deal_id) if deal_id else None
        if deal:
            self.store.get(DEALS, deal)

        document = {
            "schemaVersion": SCHEMA_VERSION,
            "text": text,
            "type": task_type,
            "contactId": contact,
            "dealId": deal,
            "dueDate": canonical_utc(due_date),
            "doneAt": None,
            "dataset": DATASET,
        }
        subjects: dict[str, list[str]] = {"taskIds": [record_id], "contactIds": [contact]}
        if deal:
            subjects["dealIds"] = [deal]
        event = self._event(
            EVENT_TASK_CREATED,
            actor,
            subjects,
            f"Task created: {text}" + (f" (reason: {reason})" if reason else ""),
            correlation_id,
            idempotency_key or f"task:{record_id}",
            origin=origin,
        )
        event_id = canonical_id("event", f"{record_id}.{EVENT_TASK_CREATED}")
        result = self._write(
            [
                {"collection": TASKS, "id": record_id, "data": document},
                {"collection": ACTIVITY, "id": event_id, "data": event},
            ],
            idempotency_key or f"task-create:{record_id}",
        )
        return {"task": self.store.get(TASKS, record_id), "command": result}

    def change_deal_stage(
        self,
        deal_id: str,
        *,
        stage: str,
        actor: str,
        correlation_id: str,
        reason: str,
    ) -> dict[str, Any]:
        """ID-preserving stage move: the deal keeps its ID, the event records both ends."""
        record_id = canonical_id("deal", deal_id)
        if stage not in DEAL_STAGES:
            raise ValueError(f"unknown deal stage: {stage}")
        current = self.store.get(DEALS, record_id)
        previous_stage = current["data"]["stage"]
        document = dict(current["data"])
        document["stage"] = stage

        event = self._event(
            EVENT_DEAL_STAGE_CHANGED,
            actor,
            {
                "dealIds": [record_id],
                "contactIds": list(current["data"].get("contactIds", [])),
            },
            f"Deal {current['data']['name']} moved {previous_stage} → {stage} (reason: {reason})",
            correlation_id,
            f"deal-stage:{record_id}:{previous_stage}:{stage}",
            change={"field": "stage", "from": previous_stage, "to": stage},
        )
        event_id = canonical_id("event", f"{record_id}.{EVENT_DEAL_STAGE_CHANGED}.{previous_stage}.{stage}")
        result = self._write(
            [
                {"collection": DEALS, "id": record_id, "data": document},
                {"collection": ACTIVITY, "id": event_id, "data": event},
            ],
            f"deal-stage:{record_id}:{previous_stage}:{stage}",
        )
        return {"deal": self.store.get(DEALS, record_id), "command": result, "from": previous_stage, "to": stage}

    # ---------------------------------------------------------- derived reads

    def _scan(
        self,
        collection: str,
        predicate: Callable[[dict[str, Any]], bool],
        *,
        limit: int = 50,
        filters: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Walk keyset pages, select app-side, and report the read cost.

        ``filters`` may only use the CP-04 allowlist. Everything a CRM would
        normally push into a ``WHERE`` clause (stage, due date, subject id) is
        decided here, so the page count is part of the answer.
        """
        matched: list[dict[str, Any]] = []
        scanned = 0
        pages = 0
        after: str | None = None
        truncated = False
        query_filters = {"schemaVersion": {"eq": SCHEMA_VERSION}}
        if filters:
            query_filters.update(filters)

        while True:
            page = self.store.list(
                collection,
                filters=query_filters,
                order={"field": "id", "direction": "asc"},
                limit=limit,
                after=after,
            )
            pages += 1
            scanned += len(page["records"])
            matched.extend(record for record in page["records"] if predicate(record["data"]))
            if not page["hasMore"]:
                break
            if pages >= self.max_pages:
                truncated = True
                break
            after = page["nextAfter"]

        return {"records": matched, "scanned": scanned, "pages": pages, "truncated": truncated}

    def open_deals(self, limit: int = 50) -> dict[str, Any]:
        result = self._scan(DEALS, is_open_deal, limit=limit)
        by_stage: dict[str, int] = {}
        for record in result["records"]:
            stage = record["data"]["stage"]
            by_stage[stage] = by_stage.get(stage, 0) + 1
        result["byStage"] = dict(sorted(by_stage.items()))
        # Atomic reads these counters from a SQL view; here they come from the
        # page that was actually read, which is why the cost is reported with them.
        result["openAmountTotal"] = round(sum(record["data"]["amount"] for record in result["records"]), 2)
        return result

    def due_tasks(self, now: datetime, limit: int = 50) -> dict[str, Any]:
        def predicate(task: dict[str, Any]) -> bool:
            return not task.get("doneAt")

        result = self._scan(TASKS, predicate, limit=limit)
        buckets: dict[str, list[dict[str, Any]]] = {
            name: [] for name in ("overdue", "today", "tomorrow", "this-week", "later")
        }
        for record in result["records"]:
            buckets[due_bucket(record["data"]["dueDate"], now)].append(record)
        result["buckets"] = {name: [item["id"] for item in items] for name, items in buckets.items()}
        result["bucketCounts"] = {name: len(items) for name, items in buckets.items()}
        return result

    def timeline(
        self,
        *,
        contact_id: str | None = None,
        deal_id: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        """One merged history for a subject, newest first.

        Atomic builds this from the ``activity_log`` view; here the events are
        already a collection, and scoping to one contact or deal happens after
        the page is read, because a JSON-field filter is not part of the contract.
        """
        contact = canonical_id("contact", contact_id) if contact_id else None
        deal = canonical_id("deal", deal_id) if deal_id else None
        if contact is None and deal is None:
            raise ValueError("timeline requires a contact or a deal subject")

        def predicate(event: dict[str, Any]) -> bool:
            subjects = event.get("subjects", {})
            return (contact in subjects.get("contactIds", [])) or (deal in subjects.get("dealIds", []))

        result = self._scan(ACTIVITY, predicate, limit=limit)
        result["events"] = sorted(
            result.pop("records"),
            key=lambda record: (record["data"]["occurredAt"], record["id"]),
            reverse=True,
        )
        result["types"] = [event["data"]["type"] for event in result["events"]]
        return result

    def client_context(self, contact_id: str) -> dict[str, Any]:
        """Everything one conversation with a client needs, keyed by canonical ID."""
        contact = canonical_id("contact", contact_id)
        record = self.store.get(CONTACTS, contact)

        deals = self._scan(DEALS, lambda deal: contact in deal.get("contactIds", []))
        tasks = self._scan(TASKS, lambda task: task.get("contactId") == contact)
        history = self.timeline(contact_id=contact_id)

        open_deals = [item for item in deals["records"] if is_open_deal(item["data"])]
        pending_tasks = [item for item in tasks["records"] if not item["data"].get("doneAt")]
        return {
            "contactId": contact,
            "contact": record["data"],
            "identityDigest": self._identity_digest(contact),
            "deals": [item["id"] for item in deals["records"]],
            "openDealIds": [item["id"] for item in open_deals],
            "openDealCount": len(open_deals),  # Atomic: nb_* counters from a SQL view
            "taskIds": [item["id"] for item in tasks["records"]],
            "pendingTaskCount": len(pending_tasks),  # Atomic: nb_tasks in contacts_summary
            "activityEventCount": len(history["events"]),
            "recentActivity": [
                {"id": event["id"], "type": event["data"]["type"], "summary": event["data"]["summary"]}
                for event in history["events"][:5]
            ],
            "reads": {
                "deals": {"scanned": deals["scanned"], "pages": deals["pages"], "truncated": deals["truncated"]},
                "tasks": {"scanned": tasks["scanned"], "pages": tasks["pages"], "truncated": tasks["truncated"]},
                "activity": {
                    "scanned": history["scanned"],
                    "pages": history["pages"],
                    "truncated": history["truncated"],
                },
            },
        }

    # --------------------------------------------------------------- fixtures

    def load_fixture(self, fixture: dict[str, Any]) -> dict[str, int]:
        """Seed the slice from ``fixtures.json`` (test data only)."""
        written = {"contacts": 0, "deals": 0, "tasks": 0}
        actor = fixture["actor"]
        for item in fixture["contacts"]:
            self.create_contact(
                actor=actor,
                correlation_id=f"exp25-seed-contact-{item['contact_id']}",
                **item,
            )
            written["contacts"] += 1
        for item in fixture["deals"]:
            self.create_deal(
                actor=actor,
                correlation_id=f"exp25-seed-deal-{item['deal_id']}",
                **item,
            )
            written["deals"] += 1
        for item in fixture["tasks"]:
            self.create_task(
                actor=actor,
                correlation_id=f"exp25-seed-task-{item['task_id']}",
                **item,
            )
            written["tasks"] += 1
        # Fixture tasks that must already be closed, so the pending-task filter has
        # a real negative case. Applied straight to the stored document: completing a
        # task is not one of the operations this experiment's write surface exposes.
        for item in fixture.get("completedTasks", []):
            record_id = canonical_id("task", item["task_id"])
            document = dict(self.store.get(TASKS, record_id)["data"])
            document["doneAt"] = item["done_at"]
            self.store.put(TASKS, record_id, document)
        return written


def load_fixture_file(path) -> dict[str, Any]:
    """Read the test-data fixture. Distinct from ``CrmSlice.load_fixture``, which writes it."""
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
