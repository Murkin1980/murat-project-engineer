"""
EXP-15 Memory Layer Prototype
=============================

Bounded, local-first, provenance-aware project memory layer for Murat Project Engineer.

Constraints:
1. Git / project files remain the sole Source of Truth.
2. Memory items must belong to allowed categories:
   - decision
   - outcome
   - constraint
   - lesson
   - failed_attempt
3. Every memory item MUST have valid provenance (file path, commit SHA, run ID, or evidence link).
   If provenance is missing or empty, writes MUST fail closed.
4. Memory deltas are proposals only (ADD, UPDATE, SUPERSEDE, DELETE, NO_CHANGE).
   Canonical updates MUST be explicitly approval-gated.
   Unauthorized writes are rejected.
5. Strict scope isolation between projects (no cross-project leakage).
6. Failure handling: if memory is corrupt or unavailable, falls back safely to
   canonical Git artifacts without fabricating memory.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional


ALLOWED_CATEGORIES = {
    "decision",
    "outcome",
    "constraint",
    "lesson",
    "failed_attempt",
}

ALLOWED_DELTA_ACTIONS = {
    "ADD",
    "UPDATE",
    "SUPERSEDE",
    "DELETE",
    "NO_CHANGE",
}

ALLOWED_STATUSES = {
    "active",
    "superseded",
    "tombstone",
}


class MemoryError(Exception):
    """Base exception for memory layer errors."""
    pass


class ProvenanceMissingError(MemoryError):
    """Raised when an item lacks mandatory provenance."""
    pass


class UnauthorizedWriteError(MemoryError):
    """Raised when an attempt is made to mutate canonical memory without required approval."""
    pass


class InvalidCategoryError(MemoryError):
    """Raised when an item has a category outside the allowed vocabulary."""
    pass


class InvalidDeltaActionError(MemoryError):
    """Raised when a delta action is not in the allowed vocabulary."""
    pass


class ScopeViolationError(MemoryError):
    """Raised when an operation attempts cross-project scope violation."""
    pass


@dataclass
class MemoryItem:
    item_id: str
    project: str
    category: str
    topic: str
    summary: str
    provenance: str
    rationale: str = ""
    status: str = "active"
    superseded_by: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    approved_by: Optional[str] = None

    def validate(self) -> None:
        if not self.item_id or not isinstance(self.item_id, str):
            raise MemoryError("item_id must be a non-empty string")
        if not self.project or not isinstance(self.project, str):
            raise MemoryError("project must be a non-empty string")
        if self.category not in ALLOWED_CATEGORIES:
            raise InvalidCategoryError(
                f"Category '{self.category}' not allowed. Allowed: {sorted(ALLOWED_CATEGORIES)}"
            )
        if not self.topic or not isinstance(self.topic, str):
            raise MemoryError("topic must be a non-empty string")
        if not self.summary or not isinstance(self.summary, str):
            raise MemoryError("summary must be a non-empty string")
        if not self.provenance or not isinstance(self.provenance, str) or not self.provenance.strip():
            raise ProvenanceMissingError(
                f"Item '{self.item_id}' lacks mandatory provenance. Memory write fails closed."
            )
        if self.status not in ALLOWED_STATUSES:
            raise MemoryError(f"Status '{self.status}' not allowed. Allowed: {sorted(ALLOWED_STATUSES)}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryItem":
        item = cls(
            item_id=data["item_id"],
            project=data["project"],
            category=data["category"],
            topic=data["topic"],
            summary=data["summary"],
            provenance=data["provenance"],
            rationale=data.get("rationale", ""),
            status=data.get("status", "active"),
            superseded_by=data.get("superseded_by"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            approved_by=data.get("approved_by"),
        )
        item.validate()
        return item


@dataclass
class DeltaAction:
    action: str  # ADD, UPDATE, SUPERSEDE, DELETE, NO_CHANGE
    item: Optional[MemoryItem] = None
    target_item_id: Optional[str] = None
    reason: str = ""

    def validate(self) -> None:
        if self.action not in ALLOWED_DELTA_ACTIONS:
            raise InvalidDeltaActionError(
                f"Action '{self.action}' not in allowed actions: {sorted(ALLOWED_DELTA_ACTIONS)}"
            )
        if self.action in {"ADD", "UPDATE", "SUPERSEDE"}:
            if self.item is None:
                raise MemoryError(f"Action '{self.action}' requires an item payload")
            self.item.validate()
        if self.action in {"UPDATE", "SUPERSEDE", "DELETE"}:
            if not self.target_item_id:
                raise MemoryError(f"Action '{self.action}' requires target_item_id")

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "target_item_id": self.target_item_id,
            "reason": self.reason,
            "item": self.item.to_dict() if self.item else None,
        }


@dataclass
class ProposedMemoryDelta:
    task_id: str
    project: str
    proposed_by: str
    actions: List[DeltaAction] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    approval_status: str = "PENDING_APPROVAL"  # PENDING_APPROVAL, APPROVED, REJECTED
    approved_by: Optional[str] = None
    approval_notes: str = ""

    def validate(self) -> None:
        if not self.task_id or not isinstance(self.task_id, str):
            raise MemoryError("task_id must be non-empty string")
        if not self.project or not isinstance(self.project, str):
            raise MemoryError("project must be non-empty string")
        for action in self.actions:
            action.validate()
            if action.item and action.item.project != self.project:
                raise ScopeViolationError(
                    f"Action item project '{action.item.project}' does not match delta project '{self.project}'"
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "project": self.project,
            "proposed_by": self.proposed_by,
            "actions": [a.to_dict() for a in self.actions],
            "created_at": self.created_at,
            "approval_status": self.approval_status,
            "approved_by": self.approved_by,
            "approval_notes": self.approval_notes,
        }


@dataclass
class ApprovalGate:
    approver: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    decision: str = "APPROVED"  # APPROVED or REJECTED
    notes: str = ""


class ProjectMemoryStore:
    """Bounded, file-backed project memory store with strict approval gating and scope isolation."""

    def __init__(self, store_path: Optional[Path] = None):
        self.store_path = store_path
        self._items: dict[str, MemoryItem] = {}
        self._load_status: str = "INITIAL"
        self._load_warning: Optional[str] = None
        if self.store_path:
            self.load()

    @property
    def load_status(self) -> str:
        return self._load_status

    @property
    def load_warning(self) -> Optional[str]:
        return self._load_warning

    def load(self) -> None:
        """Load memory store from JSON. Fails safely on corruption without hallucinating."""
        if not self.store_path or not self.store_path.exists():
            self._load_status = "FALLBACK_CANONICAL"
            self._load_warning = "Store file does not exist; safely falling back to canonical project artifacts."
            self._items = {}
            return

        try:
            content = self.store_path.read_text(encoding="utf-8")
            data = json.loads(content)
            items = {}
            for raw_item in data.get("items", []):
                item = MemoryItem.from_dict(raw_item)
                items[item.item_id] = item
            self._items = items
            self._load_status = "LOADED"
            self._load_warning = None
        except Exception as e:
            # Failure test behavior: do not invent items, log fallback warning
            self._items = {}
            self._load_status = "FALLBACK_CANONICAL"
            self._load_warning = f"Corrupted or invalid memory store ({e}); safely falling back to canonical project artifacts."

    def save(self) -> None:
        """Persist memory store to JSON file."""
        if not self.store_path:
            return
        data = {
            "schema_version": "1.0.0",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "items": [item.to_dict() for item in self._items.values()],
        }
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        self.store_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def recall(
        self,
        project: str,
        topic: Optional[str] = None,
        category: Optional[str] = None,
        include_superseded: bool = False,
    ) -> List[MemoryItem]:
        """
        Recall active items matching project scope and optional filters.
        Enforces project isolation: never returns items from outside the requested project.
        """
        if self._load_status == "FALLBACK_CANONICAL":
            # Store is unavailable or corrupt; caller must fall back to canonical repo artifacts
            return []

        results = []
        for item in self._items.values():
            # Strict project isolation
            if item.project != project:
                continue

            # Active status check
            if not include_superseded and item.status != "active":
                continue

            # Category filter
            if category and item.category != category:
                continue

            # Topic / text search
            if topic:
                topic_lower = topic.lower()
                matches = (
                    topic_lower in item.topic.lower()
                    or topic_lower in item.summary.lower()
                    or any(part in item.topic.lower() for part in topic_lower.split())
                )
                if not matches:
                    continue

            results.append(item)

        # Stable sort by item_id
        results.sort(key=lambda x: x.item_id)
        return results

    def apply_approved_delta(
        self,
        delta: ProposedMemoryDelta,
        approval: ApprovalGate,
    ) -> dict[str, Any]:
        """
        Apply a proposed memory delta to the canonical store.
        MUST fail closed if approval is missing or decision is not APPROVED.
        """
        delta.validate()

        if approval is None or approval.decision != "APPROVED":
            raise UnauthorizedWriteError(
                "Cannot apply memory delta: explicit ApprovalGate decision 'APPROVED' is required."
            )
        if not approval.approver or not approval.approver.strip():
            raise UnauthorizedWriteError(
                "Cannot apply memory delta: approver identifier cannot be empty."
            )

        applied_actions = []

        for action in delta.actions:
            if action.action == "NO_CHANGE":
                applied_actions.append({"action": "NO_CHANGE", "result": "OK"})
                continue

            if action.action == "ADD":
                assert action.item is not None
                action.item.approved_by = approval.approver
                self._items[action.item.item_id] = action.item
                applied_actions.append({"action": "ADD", "item_id": action.item.item_id, "result": "ADDED"})

            elif action.action == "UPDATE":
                assert action.item is not None
                assert action.target_item_id is not None
                if action.target_item_id not in self._items:
                    raise MemoryError(f"Target item '{action.target_item_id}' not found for UPDATE")
                # Ensure scope isolation
                if self._items[action.target_item_id].project != delta.project:
                    raise ScopeViolationError("Cannot UPDATE item belonging to different project")
                action.item.approved_by = approval.approver
                self._items[action.target_item_id] = action.item
                applied_actions.append({"action": "UPDATE", "item_id": action.target_item_id, "result": "UPDATED"})

            elif action.action == "SUPERSEDE":
                assert action.item is not None
                assert action.target_item_id is not None
                if action.target_item_id not in self._items:
                    raise MemoryError(f"Target item '{action.target_item_id}' not found for SUPERSEDE")
                old_item = self._items[action.target_item_id]
                if old_item.project != delta.project:
                    raise ScopeViolationError("Cannot SUPERSEDE item belonging to different project")
                # Mark old item as superseded
                old_item.status = "superseded"
                old_item.superseded_by = action.item.item_id
                # Add new item as active
                action.item.approved_by = approval.approver
                self._items[action.item.item_id] = action.item
                applied_actions.append({
                    "action": "SUPERSEDE",
                    "superseded_item_id": old_item.item_id,
                    "new_item_id": action.item.item_id,
                    "result": "SUPERSEDED",
                })

            elif action.action == "DELETE":
                assert action.target_item_id is not None
                if action.target_item_id not in self._items:
                    raise MemoryError(f"Target item '{action.target_item_id}' not found for DELETE")
                target = self._items[action.target_item_id]
                if target.project != delta.project:
                    raise ScopeViolationError("Cannot DELETE item belonging to different project")
                # Mark item as tombstone (soft delete preserving auditability)
                target.status = "tombstone"
                applied_actions.append({"action": "DELETE", "item_id": target.item_id, "result": "TOMBSTONED"})

        delta.approval_status = "APPROVED"
        delta.approved_by = approval.approver
        delta.approval_notes = approval.notes

        if self.store_path:
            self.save()

        return {
            "task_id": delta.task_id,
            "project": delta.project,
            "approval_status": "APPROVED",
            "applied_actions": applied_actions,
        }
