#!/usr/bin/env python3
"""EXP-25 CP-04 read-first tool surface over the CP-03 slice.

Shape donor: ``supabase/functions/mcp/index.ts`` @ marmelab/atomic-crm
``8b5d47ba`` — a small named tool set with explicit ``readOnlyHint`` /
``destructiveHint`` annotations, where reads are unrestricted and the write is a
single narrow operation (``complete_task``). Atomic's generic ``query`` /
``mutate`` tools take raw SQL and guard it with an AST allowlist
(``validateSql.ts``); that guard exists only because SQL is the interface.
MiniBase never accepts SQL, so the equivalent control here is structural: three
named reads, exactly one named write, and no passthrough of any kind.

Boundaries enforced by this module and asserted by the tests:

- reads need no approval and never mutate;
- the only write is ``create_follow_up_task`` — ``change_deal_stage`` is
  deliberately **not** exposed, because the task allows one controlled write;
- a write needs explicit approval (``approved``, ``actor``, ``reason``) plus a
  client-chosen ``Idempotency-Key``;
- a write is refused unless the target document is marked as EXP-25 test data;
- the write budget is finite for a run;
- every write and every denial is appended to an audit trail shaped like
  MiniBase's ``audit_events`` contract, which stores a SHA-256 digest of the
  idempotency key and never the key itself.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any, Callable

from crm_slice import CONTACTS, DATASET, TASK_TYPES, CrmSlice, canonical_id
from minibase_adapter import MiniBaseError


class ToolError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code
        self.message = message or code


TOOL_SPECS: list[dict[str, Any]] = [
    {
        "name": "list_open_deals",
        "title": "List Open Deals",
        "description": (
            "List deals that are neither won/lost nor archived, with per-stage counts "
            "and the total open amount. Read-only."
        ),
        "annotations": {"readOnlyHint": True},
        "readOnly": True,
    },
    {
        "name": "get_client_context",
        "title": "Get Client Context",
        "description": (
            "Return one contact's canonical identity, their deals, their tasks, and "
            "their merged activity timeline. Read-only."
        ),
        "annotations": {"readOnlyHint": True},
        "readOnly": True,
    },
    {
        "name": "list_due_tasks",
        "title": "List Due Tasks",
        "description": (
            "List pending tasks grouped into overdue / today / tomorrow / this-week / "
            "later buckets. Read-only."
        ),
        "annotations": {"readOnlyHint": True},
        "readOnly": True,
    },
    {
        "name": "create_follow_up_task",
        "title": "Create Follow-up Task",
        "description": (
            "Create exactly one follow-up task for an existing EXP-25 test contact, "
            "writing the task and its activity event in one atomic command. Requires "
            "explicit approval, a reason, and a client-chosen Idempotency-Key."
        ),
        "annotations": {"destructiveHint": True, "idempotentHint": True},
        "readOnly": False,
        "exposed": True,
    },
    {
        # CP-04 allows "create follow-up task OR change deal stage". Both candidates
        # are declared so the choice is explicit, but only one is exposed; calling
        # the other is refused rather than silently available.
        "name": "change_deal_stage",
        "title": "Change Deal Stage",
        "description": (
            "Second CP-04 write candidate. Declared, not exposed: this experiment "
            "tests one controlled write only."
        ),
        "annotations": {"destructiveHint": True},
        "readOnly": False,
        "exposed": False,
    },
]

READ_TOOL_NAMES = tuple(spec["name"] for spec in TOOL_SPECS if spec["readOnly"])
WRITE_TOOL_NAMES = tuple(spec["name"] for spec in TOOL_SPECS if not spec["readOnly"])
# Only one write is exposed for the whole experiment.
AVAILABLE_WRITE_TOOLS = tuple(
    spec["name"] for spec in TOOL_SPECS if not spec["readOnly"] and spec["exposed"]
)


class AuditTrail:
    """Append-only audit entries shaped like MiniBase's ``audit_events`` rows.

    Successful reads are deliberately not audited: MiniBase states that at its
    request volumes data-plane reads would be its largest write source, and only
    denials plus mutations are recorded.
    """

    def __init__(self, clock: Callable[[], str]) -> None:
        self._clock = clock
        self.entries: list[dict[str, Any]] = []

    def record(
        self,
        *,
        action: str,
        outcome: str,
        actor: str,
        entity: str,
        entity_id: str,
        correlation_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        entry = {
            "seq": len(self.entries) + 1,
            "occurredAt": self._clock(),
            "action": action,
            "outcome": outcome,  # success | denied | failed
            "actor": actor,
            "entity": entity,
            "entity_id": entity_id,
            "correlation_id": correlation_id,
            "metadata": metadata or {},
        }
        self.entries.append(entry)
        return entry

    @staticmethod
    def key_digest(idempotency_key: str) -> str:
        return hashlib.sha256(idempotency_key.encode("utf-8")).hexdigest()[:16]


class ToolSurface:
    """Three named reads plus one approval-gated write, with an audit trail."""

    def __init__(
        self,
        slice_: CrmSlice,
        *,
        actor: str,
        now: datetime,
        clock: Callable[[], str],
        write_budget: int = 1,
        audit: AuditTrail | None = None,
    ) -> None:
        self.slice = slice_
        self.actor = actor
        self.now = now
        self.clock = clock
        self.write_budget = write_budget
        self.writes_used = 0
        self.audit = audit or AuditTrail(clock)

    # -------------------------------------------------------------- dispatch

    def dispatch(self, tool: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        spec = next((item for item in TOOL_SPECS if item["name"] == tool), None)
        if spec is None:
            return self._error(tool, "unknown_tool", f"no such tool: {tool}", read_only=None)
        args = arguments or {}
        correlation_id = str(args.get("correlationId") or f"exp25-{tool}")
        try:
            if spec["readOnly"]:
                result = self._read(tool, args)
            else:
                result = self._write(tool, args, correlation_id)
        except ToolError as error:
            return self._error(tool, error.code, error.message, read_only=spec["readOnly"], correlation_id=correlation_id)
        return {
            "tool": tool,
            "readOnly": spec["readOnly"],
            "annotations": spec["annotations"],
            "ok": True,
            "result": result,
            "correlationId": correlation_id,
        }

    def _read(self, tool: str, args: dict[str, Any]) -> dict[str, Any]:
        if tool == "list_open_deals":
            deals = self.slice.open_deals(limit=int(args.get("limit", 50)))
            return {
                "openDeals": [
                    {
                        "dealId": record["id"],
                        "name": record["data"]["name"],
                        "stage": record["data"]["stage"],
                        "amount": record["data"]["amount"],
                        "contactIds": record["data"]["contactIds"],
                        "expectedClosingDate": record["data"]["expectedClosingDate"],
                    }
                    for record in deals["records"]
                ],
                "byStage": deals["byStage"],
                "openAmountTotal": deals["openAmountTotal"],
                "read": {"scanned": deals["scanned"], "pages": deals["pages"], "truncated": deals["truncated"]},
            }
        if tool == "get_client_context":
            contact_id = args.get("contactId")
            if not contact_id:
                raise ToolError("missing_argument", "get_client_context requires contactId")
            context = self.slice.client_context(contact_id)
            context["asOf"] = self.clock()
            return context
        if tool == "list_due_tasks":
            tasks = self.slice.due_tasks(self.now, limit=int(args.get("limit", 50)))
            index = {record["id"]: record["data"] for record in tasks["records"]}
            return {
                "buckets": {
                    name: [
                        {
                            "taskId": task_id,
                            "text": index[task_id]["text"],
                            "dueDate": index[task_id]["dueDate"],
                            "contactId": index[task_id]["contactId"],
                            "dealId": index[task_id]["dealId"],
                        }
                        for task_id in ids
                    ]
                    for name, ids in tasks["buckets"].items()
                },
                "bucketCounts": tasks["bucketCounts"],
                "read": {"scanned": tasks["scanned"], "pages": tasks["pages"], "truncated": tasks["truncated"]},
            }
        raise ToolError("unknown_tool", tool)

    # ----------------------------------------------------------------- write

    def _write(self, tool: str, args: dict[str, Any], correlation_id: str) -> dict[str, Any]:
        if tool not in AVAILABLE_WRITE_TOOLS:
            raise ToolError("tool_not_available", f"write tool not exposed by this experiment: {tool}")
        if self.writes_used >= self.write_budget:
            self.audit.record(
                action="crm.tool.write_refused",
                outcome="denied",
                actor=str(args.get("approval", {}).get("actor", self.actor)),
                entity="task",
                entity_id="-",
                correlation_id=correlation_id,
                metadata={"reason": "write_budget_exhausted", "budget": self.write_budget},
            )
            raise ToolError("write_budget_exhausted", f"write budget for this run is {self.write_budget}")

        approval = args.get("approval")
        if not isinstance(approval, dict) or approval.get("approved") is not True:
            self._deny(tool, args, correlation_id, "approval_required")
        actor = str(approval.get("actor", "")).strip()
        reason = str(approval.get("reason", "")).strip()
        idempotency_key = str(approval.get("idempotencyKey", ""))
        if not actor or not reason or not (1 <= len(idempotency_key) <= 100):
            self._deny(tool, args, correlation_id, "write_not_authorized")

        contact_key = args.get("contactId")
        deal_key = args.get("dealId")
        text = str(args.get("text", "")).strip()
        due_date = str(args.get("dueDate", "")).strip()
        task_type = str(args.get("taskType", "follow-up"))
        if not contact_key or not text or not due_date:
            self._deny(tool, args, correlation_id, "missing_argument")
        if task_type not in TASK_TYPES:
            self._deny(tool, args, correlation_id, "invalid_task_type")

        contact = canonical_id("contact", contact_key)
        try:
            contact_record = self.slice.store.get(CONTACTS, contact)
        except MiniBaseError as error:
            raise ToolError("target_not_found", f"contact {contact} does not exist: {error.code}") from error

        # Bounded to test data: the target document must carry the EXP-25 marker.
        if contact_record["data"].get("dataset") != DATASET:
            self.audit.record(
                action="crm.tool.write_refused",
                outcome="denied",
                actor=actor,
                entity="contact",
                entity_id=contact,
                correlation_id=correlation_id,
                metadata={"reason": "write_out_of_bounds", "expectedDataset": DATASET},
            )
            raise ToolError("write_out_of_bounds", "write is bounded to EXP-25 test data")

        task_key = str(args.get("taskId", f"fu-{contact_key}-{len(self.audit.entries) + 1}"))
        created = self.slice.create_task(
            task_key,
            text=text,
            contact_id=contact_key,
            due_date=due_date,
            task_type=task_type,
            deal_id=deal_key,
            actor=actor,
            correlation_id=correlation_id,
            origin="agent-tool",
            idempotency_key=idempotency_key,
            reason=reason,
        )
        self.writes_used += 1
        task_id = created["task"]["id"]
        self.audit.record(
            action="crm.task.created",
            outcome="success",
            actor=actor,
            entity="task",
            entity_id=task_id,
            correlation_id=correlation_id,
            metadata={
                "contactId": contact,
                "dealId": canonical_id("deal", deal_key) if deal_key else None,
                "reason": reason,
                "tool": tool,
                "commandId": created["command"]["commandId"],
                "operationCount": created["command"]["operationCount"],
                "replayed": created["command"]["replayed"],
                "idempotencyDigest": AuditTrail.key_digest(idempotency_key),
            },
        )
        return {
            "taskId": task_id,
            "contactId": contact,
            "dealId": canonical_id("deal", deal_key) if deal_key else None,
            "commandId": created["command"]["commandId"],
            "operationCount": created["command"]["operationCount"],
            "replayed": created["command"]["replayed"],
            "writtenRecords": [f"{item['collection']}/{item['id']}" for item in created["command"]["records"]],
            "provenance": created["task"]["data"].get("dataset"),
            "audited": True,
        }

    def _deny(self, tool: str, args: dict[str, Any], correlation_id: str, reason: str) -> None:
        approval = args.get("approval") if isinstance(args.get("approval"), dict) else {}
        self.audit.record(
            action="crm.tool.write_refused",
            outcome="denied",
            actor=str(approval.get("actor", self.actor)),
            entity="task",
            entity_id=str(args.get("taskId", "-")),
            correlation_id=correlation_id,
            metadata={"reason": reason, "tool": tool},
        )
        raise ToolError(reason)

    def _error(
        self,
        tool: str,
        code: str,
        message: str,
        *,
        read_only: bool | None,
        correlation_id: str = "-",
    ) -> dict[str, Any]:
        return {
            "tool": tool,
            "readOnly": read_only,
            "ok": False,
            "error": {"code": code, "message": message},
            "correlationId": correlation_id,
        }
