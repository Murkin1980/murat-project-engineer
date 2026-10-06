#!/usr/bin/env python3
"""EXP-25 CP-03 adapter: the documented MiniBase data-plane contract, in memory.

This is **not** a MiniBase fork, a database, or a network client. It is the
smallest faithful stand-in that lets the Atomic-CRM-derived slice run against the
*contract* MiniBase already publishes, so the fit claims in ``MINIBASE_FIT.md``
are executed rather than asserted.

Contract pinned to ``Murkin1980/minibase-cloudflare`` @ ``9ab38d832970b3956cf0f831f9b578f7b9fd9001``:

- ``docs/DATA_MODEL.md``   — ``mb_records (collection, id, data, created_at,
  updated_at)``, canonical UTC ``YYYY-MM-DDTHH:mm:ss.sssZ`` timestamps, document
  store with no foreign keys, joins, or per-field JSON indexes.
- ``docs/DATA_API.md``     — records routes, the closed CP-04 query contract
  (``filter[field]``/``filter[field.operator]``, ``order=field.direction``,
  ``select``, opaque keyset cursor, ``hasMore``), and the CP-05 command
  ``POST /v1/commands/records:upsert-many`` with mandatory ``Idempotency-Key``.
- ``src/data-api.ts``      — ``collectionPattern``, ``recordIdPattern``, and the
  ``invalid_collection`` / ``invalid_record_id`` / ``invalid_record_data`` /
  ``record_not_found`` codes.
- ``src/record-query.ts``  — the filter/order/select allowlists, the
  ``(sort, id)`` keyset comparison, and the ``mbq1.<base64url>`` cursor with its
  FNV-1a query-consistency digest.
- ``src/commands.ts``      — one-field ``operations`` body, no ``mb_`` internal
  collections, no duplicate targets, ``bulk_limit_exceeded``, SHA-256
  idempotency-key hashing, replay, and opaque ``idempotency_conflict``.
- ``src/errors.ts``        — the error codes reused here.

Deliberately absent, because MiniBase does not have them: joins, views, foreign
keys, filtering on an arbitrary JSON field, ``OFFSET`` pagination, SQL of any
kind, and cross-collection transactions beyond the one CP-05 command.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any, Callable, Iterable

# --- contract constants, copied from the pinned source, not invented ---------

COLLECTION_PATTERN = re.compile(r"^[a-z][a-z0-9_-]{1,62}$")  # src/data-api.ts
RECORD_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")  # src/data-api.ts

# src/record-query.ts allowlists. A field is listed only when MiniBase itself
# lists it; nothing extra may be added here.
FILTER_FIELDS: dict[str, set[str]] = {
    "id": {"eq"},
    "createdAt": {"eq", "gt", "gte", "lt", "lte"},
    "updatedAt": {"eq", "gt", "gte", "lt", "lte"},
    "schemaVersion": {"eq"},
}
ORDER_FIELDS = ("id", "createdAt", "updatedAt")
SELECT_FIELDS = ("id", "data", "createdAt", "updatedAt")
TIMESTAMP_FIELDS = ("createdAt", "updatedAt")

COMMAND_TYPE = "records:upsert-many"

STATUS_BY_CODE = {
    "record_not_found": 404,
    "request_body_too_large": 413,
    "invalid_collection": 400,
    "invalid_record_id": 400,
    "invalid_record_data": 400,
    "invalid_filter": 400,
    "invalid_operator": 400,
    "invalid_order": 400,
    "invalid_select": 400,
    "invalid_cursor": 400,
    "invalid_limit": 400,
    "invalid_command": 400,
    "invalid_idempotency_key": 400,
    "bulk_limit_exceeded": 400,
    "idempotency_conflict": 409,
}


class MiniBaseError(Exception):
    """A contract refusal, named exactly as ``src/errors.ts`` names it."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code
        self.status = STATUS_BY_CODE.get(code, 500)


def canonical_utc(value: str | datetime) -> str:
    """Normalize to MiniBase's single stored timestamp shape.

    ``mb_records.created_at``/``updated_at`` are always written by
    ``new Date().toISOString()``; SQLite compares them as TEXT, so a value in any
    other representation would sort against a different shape. A value with no
    explicit timezone is refused rather than guessed at (``invalid_filter``).
    """
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise MiniBaseError("invalid_filter")
        moment = value
    else:
        try:
            moment = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError as exc:
            raise MiniBaseError("invalid_filter") from exc
        if moment.tzinfo is None:
            raise MiniBaseError("invalid_filter")
    utc = moment.astimezone(timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{utc.microsecond // 1000:03d}Z"


def canonical_json(value: Any) -> str:
    """Canonical JSON: member order normalized before fingerprinting.

    Mirrors the CP-05 rule that MiniBase canonicalizes JSON object-member order
    so an identical logical payload always produces the same fingerprint.
    """
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _fnv1a36(text: str) -> str:
    """The same FNV-1a 32-bit digest ``record-query.ts`` renders base-36."""
    digest = 0x811C9DC5
    for char in text:
        digest ^= ord(char) & 0xFF
        digest = (digest * 0x01000193) & 0xFFFFFFFF
    # Match JS ``hash.toString(36)`` over the unsigned 32-bit value.
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if digest == 0:
        return "0"
    out = ""
    while digest:
        out = digits[digest % 36] + out
        digest //= 36
    return out


def _b64url_encode(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii").rstrip("=")


def _b64url_decode(text: str) -> str:
    padded = text + "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")


class InMemoryMiniBase:
    """One project's data plane: ``mb_records`` plus the one CP-05 command."""

    def __init__(
        self,
        clock: Callable[[], str] | None = None,
        max_json_bytes: int = 65_536,
        max_page_size: int = 100,
        default_page_size: int = 50,
        max_bulk_records: int = 500,
    ) -> None:
        self._clock = clock or (lambda: canonical_utc(datetime.now(timezone.utc)))
        self.max_json_bytes = max_json_bytes
        self.max_page_size = max_page_size
        self.default_page_size = default_page_size
        self.max_bulk_records = max_bulk_records
        # mb_records, keyed by (collection, id) — the primary key.
        self._rows: dict[tuple[str, str], dict[str, Any]] = {}
        # mb_commands markers, keyed by (command_type, sha256(idempotency key)).
        self._commands: dict[tuple[str, str], dict[str, Any]] = {}
        # Cost evidence: one statement per page, per record read, per command.
        self.statements = 0

    # ------------------------------------------------------------- validation

    @staticmethod
    def _validate_collection(collection: str) -> str:
        if not COLLECTION_PATTERN.match(collection):
            raise MiniBaseError("invalid_collection")
        return collection

    @staticmethod
    def _validate_record_id(record_id: str) -> str:
        if not RECORD_ID_PATTERN.match(record_id):
            raise MiniBaseError("invalid_record_id")
        return record_id

    def _validate_data(self, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise MiniBaseError("invalid_record_data")
        if len(canonical_json(data).encode("utf-8")) > self.max_json_bytes:
            raise MiniBaseError("request_body_too_large")
        return data

    # -------------------------------------------------------------- records

    def put(self, collection: str, record_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """``PUT /v1/data/{collection}/{id}`` — last write wins."""
        self._validate_collection(collection)
        self._validate_record_id(record_id)
        self._validate_data(data)
        self.statements += 1
        now = self._clock()
        key = (collection, record_id)
        previous = self._rows.get(key)
        row = {
            "id": record_id,
            "data": json.loads(canonical_json(data)),
            "createdAt": previous["createdAt"] if previous else now,
            "updatedAt": now,
        }
        self._rows[key] = row
        return self._present(row, SELECT_FIELDS)

    def get(self, collection: str, record_id: str) -> dict[str, Any]:
        """``GET /v1/data/{collection}/{id}``."""
        self._validate_collection(collection)
        self._validate_record_id(record_id)
        self.statements += 1
        row = self._rows.get((collection, record_id))
        if row is None:
            raise MiniBaseError("record_not_found")
        return self._present(row, SELECT_FIELDS)

    def delete(self, collection: str, record_id: str) -> None:
        """``DELETE /v1/data/{collection}/{id}`` — idempotent, always 204."""
        self._validate_collection(collection)
        self._validate_record_id(record_id)
        self.statements += 1
        self._rows.pop((collection, record_id), None)

    # --------------------------------------------------------- CP-04 query

    def list(
        self,
        collection: str,
        filters: dict[str, dict[str, Any]] | None = None,
        order: dict[str, str] | None = None,
        select: Iterable[str] | None = None,
        limit: int | None = None,
        after: str | None = None,
    ) -> dict[str, Any]:
        """``GET /v1/data/{collection}`` — closed query contract, keyset paging.

        ``filters`` uses the SDK shape ``{"field": {"operator": value}}`` and maps
        to ``filter[field.operator]``. Only the allowlisted fields, operators,
        orders, and select names are accepted; everything else is a 400, exactly
        as ``src/record-query.ts`` refuses it.
        """
        self._validate_collection(collection)
        parsed_filters = self._parse_filters(filters or {})
        order_field, direction = self._parse_order(order)
        selected = self._parse_select(select)
        page_size = self._parse_limit(limit)

        rows = [
            row
            for (row_collection, _), row in sorted(self._rows.items())
            if row_collection == collection and self._matches(row, parsed_filters)
        ]
        rows.sort(key=lambda row: (self._sort_value(order_field, row), row["id"]), reverse=direction == "desc")

        if after is not None:
            cursor = self._decode_cursor(after, collection, parsed_filters, order_field, direction)
            rows = [
                row
                for row in rows
                if self._after_cursor(row, cursor, order_field, direction)
            ]

        self.statements += 1  # one page is one statement with a limit + 1 probe row
        page = rows[: page_size + 1]
        has_more = len(page) > page_size
        page = page[:page_size]

        next_after = None
        if page:
            last = page[-1]
            next_after = self._encode_cursor(
                collection, parsed_filters, order_field, direction,
                self._sort_value(order_field, last), last["id"],
            )

        return {
            "records": [self._present(row, selected) for row in page],
            "nextAfter": next_after,
            "hasMore": has_more,
        }

    # ------------------------------------------------------- CP-05 command

    def upsert_many(
        self, operations: list[dict[str, Any]], idempotency_key: str
    ) -> dict[str, Any]:
        """``POST /v1/commands/records:upsert-many`` — atomic and replayable.

        All targets are validated before anything is written, so a refused
        command cannot leave a partial result; the real implementation gets the
        same guarantee from one SQLite statement plus its static trigger.
        """
        if not isinstance(idempotency_key, str) or not (1 <= len(idempotency_key) <= 100):
            raise MiniBaseError("invalid_idempotency_key")
        if not isinstance(operations, list) or not operations:
            raise MiniBaseError("invalid_command")
        if len(operations) > self.max_bulk_records:
            raise MiniBaseError("bulk_limit_exceeded")

        targets: set[tuple[str, str]] = set()
        for operation in operations:
            if not isinstance(operation, dict):
                raise MiniBaseError("invalid_command")
            if set(operation) != {"collection", "id", "data"}:
                raise MiniBaseError("invalid_command")
            collection = self._validate_collection(str(operation["collection"]))
            if collection.startswith("mb_"):
                raise MiniBaseError("invalid_collection")
            record_id = self._validate_record_id(str(operation["id"]))
            self._validate_data(operation["data"])
            target = (collection, record_id)
            if target in targets:
                raise MiniBaseError("invalid_command")
            targets.add(target)

        payload = {"operations": operations}
        fingerprint = hashlib.sha256(
            canonical_json({"command": COMMAND_TYPE, "payload": payload}).encode("utf-8")
        ).hexdigest()
        key_hash = hashlib.sha256(idempotency_key.encode("utf-8")).hexdigest()
        marker_key = (COMMAND_TYPE, key_hash)
        marker = self._commands.get(marker_key)

        if marker is not None:
            if marker["request_fingerprint"] != fingerprint:
                # Opaque by contract: it never reveals the old payload or the key.
                raise MiniBaseError("idempotency_conflict")
            response = json.loads(marker["response_json"])
            response["replayed"] = True
            return response

        now = self._clock()
        records = []
        for operation in operations:
            key = (operation["collection"], operation["id"])
            previous = self._rows.get(key)
            self._rows[key] = {
                "id": key[1],
                "data": json.loads(canonical_json(operation["data"])),
                "createdAt": previous["createdAt"] if previous else now,
                "updatedAt": now,
            }
            records.append({"collection": key[0], "id": key[1]})
        self.statements += 1  # execute, replay, and conflict all cost one statement

        response = {
            "commandId": hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:36],
            "status": "applied",
            "operationCount": len(operations),
            "records": records,
            "replayed": False,
        }
        self._commands[marker_key] = {
            "request_fingerprint": fingerprint,
            "response_json": json.dumps(response, sort_keys=True),
        }
        return response

    # ------------------------------------------------------------- helpers

    @staticmethod
    def _present(row: dict[str, Any], select: Iterable[str]) -> dict[str, Any]:
        presented: dict[str, Any] = {}
        for field in select:
            if field in row:
                presented[field] = json.loads(canonical_json(row[field])) if field == "data" else row[field]
        return presented

    def _parse_filters(self, filters: dict[str, dict[str, Any]]) -> list[tuple[str, str, Any]]:
        parsed: list[tuple[str, str, Any]] = []
        seen: set[str] = set()
        for field, clauses in filters.items():
            if field not in FILTER_FIELDS:
                raise MiniBaseError("invalid_filter")
            if not isinstance(clauses, dict) or not clauses:
                raise MiniBaseError("invalid_filter")
            for operator, value in clauses.items():
                if operator not in {"eq", "gt", "gte", "lt", "lte"}:
                    raise MiniBaseError("invalid_operator")
                if operator not in FILTER_FIELDS[field]:
                    raise MiniBaseError("invalid_operator")
                seen_key = f"{field}.{operator}"
                if seen_key in seen:
                    raise MiniBaseError("invalid_filter")
                seen.add(seen_key)
                parsed.append((field, operator, self._validate_filter_value(field, value)))
        # Stable order keeps the cursor digest independent of insertion order.
        return sorted(parsed, key=lambda item: f"{item[0]}.{item[1]}")

    @staticmethod
    def _validate_filter_value(field: str, value: Any) -> Any:
        if field == "schemaVersion":
            if not isinstance(value, int) or isinstance(value, bool):
                raise MiniBaseError("invalid_filter")
            return value
        if field == "id":
            if not RECORD_ID_PATTERN.match(str(value)):
                raise MiniBaseError("invalid_filter")
            return value
        return canonical_utc(value)

    @staticmethod
    def _parse_order(order: dict[str, str] | None) -> tuple[str, str]:
        if order is None:
            return "id", "asc"
        field = order.get("field", "id")
        direction = order.get("direction", "asc")
        if field not in ORDER_FIELDS or direction not in ("asc", "desc"):
            raise MiniBaseError("invalid_order")
        return field, direction

    @staticmethod
    def _parse_select(select: Iterable[str] | None) -> tuple[str, ...]:
        if select is None:
            return SELECT_FIELDS
        chosen = tuple(select)
        if not chosen or any(field not in SELECT_FIELDS for field in chosen):
            raise MiniBaseError("invalid_select")
        return chosen

    def _parse_limit(self, limit: int | None) -> int:
        if limit is None:
            return self.default_page_size
        if not isinstance(limit, int) or limit < 1 or limit > self.max_page_size:
            raise MiniBaseError("invalid_limit")
        return limit

    @staticmethod
    def _sort_value(order_field: str, row: dict[str, Any]) -> str:
        return row["createdAt"] if order_field == "createdAt" else (
            row["updatedAt"] if order_field == "updatedAt" else row["id"]
        )

    def _matches(self, row: dict[str, Any], filters: list[tuple[str, str, Any]]) -> bool:
        for field, operator, value in filters:
            actual = (
                row["data"].get("schemaVersion")
                if field == "schemaVersion"
                else self._sort_value(field, row)
            )
            if field == "schemaVersion":
                if actual != value:
                    return False
                continue
            if operator == "eq" and not actual == value:
                return False
            if operator == "gt" and not actual > value:
                return False
            if operator == "gte" and not actual >= value:
                return False
            if operator == "lt" and not actual < value:
                return False
            if operator == "lte" and not actual <= value:
                return False
        return True

    def _query_digest(
        self,
        collection: str,
        filters: list[tuple[str, str, Any]],
        order_field: str,
        direction: str,
    ) -> str:
        canonical = canonical_json(
            [collection, order_field, direction, [[f, o, v] for f, o, v in filters]]
        )
        return _fnv1a36(canonical)

    def _encode_cursor(
        self,
        collection: str,
        filters: list[tuple[str, str, Any]],
        order_field: str,
        direction: str,
        sort_value: str,
        record_id: str,
    ) -> str:
        if not filters and order_field == "id" and direction == "asc":
            return record_id  # legacy cursor: the record ID, exactly as before CP-04
        digest = self._query_digest(collection, filters, order_field, direction)
        return "mbq1." + _b64url_encode(canonical_json([digest, sort_value, record_id]))

    def _decode_cursor(
        self,
        raw: str,
        collection: str,
        filters: list[tuple[str, str, Any]],
        order_field: str,
        direction: str,
    ) -> tuple[str, str]:
        if not filters and order_field == "id" and direction == "asc":
            if not RECORD_ID_PATTERN.match(raw):
                raise MiniBaseError("invalid_record_id")
            return raw, raw
        if not raw.startswith("mbq1."):
            raise MiniBaseError("invalid_cursor")
        try:
            digest, sort_value, record_id = json.loads(_b64url_decode(raw[5:]))
        except (ValueError, json.JSONDecodeError) as exc:
            raise MiniBaseError("invalid_cursor") from exc
        if digest != self._query_digest(collection, filters, order_field, direction):
            raise MiniBaseError("invalid_cursor")
        if not RECORD_ID_PATTERN.match(str(record_id)):
            raise MiniBaseError("invalid_record_id")
        return str(sort_value), str(record_id)

    @staticmethod
    def _after_cursor(
        row: dict[str, Any], cursor: tuple[str, str], order_field: str, direction: str
    ) -> bool:
        sort_value, record_id = cursor
        current = (InMemoryMiniBase._sort_value(order_field, row), row["id"])
        previous = (sort_value, record_id)
        return current < previous if direction == "desc" else current > previous
