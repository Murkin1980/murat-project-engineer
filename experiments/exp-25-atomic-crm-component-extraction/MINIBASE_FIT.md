# EXP-25 MINIBASE_FIT — CP-02 verification against `minibase-cloudflare`

Host pin: `Murkin1980/minibase-cloudflare` @ `9ab38d832970b3956cf0f831f9b578f7b9fd9001` (2026-09-24), `package.json` version `0.28.0`, roadmap `MB9 vNext upgrade — CP-04 of 10`.

Method: the host repository was cloned read-only into a scratch directory outside this repository and inspected (`ARCHITECTURE.md`, `ROADMAP.md`, `AGENTS.md`, `docs/DATA_MODEL.md`, `docs/DATA_API.md`, `docs/CLIENT_SDK.md`, `src/data-api.ts`, `src/record-query.ts`, `src/commands.ts`, `src/errors.ts`, `src/security.ts`, `src/limits.ts`). **No file in `minibase-cloudflare` was modified, and nothing was deployed.** The bounded proof in `harness/` runs against an in-memory adapter that implements the documented contract.

Rule respected throughout: **one object → one identity → many representations.**

## 1. Canonical object identity — PASS

| Requirement | MiniBase fact | EXP-25 result |
| --- | --- | --- |
| ids must satisfy the host's record-id pattern | `^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$` (`src/data-api.ts:16`) | `contact-c-001`, `deal-d-001`, `task-t-001`, `event-task-t-001.task.created` all match |
| one id per business object | `mb_records` primary key is `(collection, id)` | the record id **is** the identity; `deal.data.contactIds` and `task.data.contactId` repeat the same string |
| no second id scheme | — | the proof asserts no alternative id exists; event ids are composed from the entity id, as Atomic composes `'deal.' \|\| d.id \|\| '.created'` |

## 2. Storage / source-of-truth compatibility — PASS

The slice uses **four logical collections inside one project's own D1**: `crm_contacts`, `crm_deals`, `crm_tasks`, `crm_activity_events`. `mb_records` is a document store where "collections are logical partitions inside one physical table", so this needs no table, no column, and no physical schema addition. Every collection name satisfies `^[a-z][a-z0-9_-]{1,62}$` and none uses the reserved `mb_` prefix (`src/commands.ts:93`).

Every document carries `schemaVersion: 1` — the one JSON field MiniBase's query contract understands, and the field its own consumers already use for rolling documents forward.

Source of truth is unchanged: MiniBase remains the store, Git remains the source of truth for this experiment's evidence, and no CRM becomes authoritative over anything.

## 3. API fit — PASS

| Slice operation | MiniBase endpoint used |
| --- | --- |
| read a page of deals/tasks/events | `GET /v1/data/{collection}` with the CP-04 query (`filter[schemaVersion]=1`, `order=id.asc`, `limit`, `after`) |
| read one object | `GET /v1/data/{collection}/{id}` |
| create contact / deal / task, move a deal stage | `POST /v1/commands/records:upsert-many` with `Idempotency-Key` — entity + history event in one call |
| timeline | derived from `crm_activity_events`, newest first, scoped after the page is read |

Cost behavior matches the host's own model: one page is one statement with a `limit + 1` probe row, and `hasMore` (not `nextAfter !== null`) decides whether to continue. The whole proof ran in **75 MiniBase statements** (pages, single-record reads, and commands) — reported by the adapter rather than assumed.

## 4. Migration requirement — PASS for data, with one owner-gated schema step

- **No data migration.** No live customer data is touched; the proof runs on `harness/fixtures.json` (synthetic names, `dataset: exp-25-test`).
- **No relational migration.** No table, column, index, or view is added.
- **One additive, owner-gated schema step for atomic writes.** CP-05's command needs project schema **v6** (`mb_commands` + its static trigger). For a project provisioned before v6, MiniBase requires `GET /v1/projects/{projectId}/schema/verify` and an **owner-approved** `POST /v1/projects/{projectId}/schema/apply`; the command refuses with `409 command_schema_not_ready` until that is done. That step is additive metadata (MiniBase applies project schema forward-only, every statement `IF NOT EXISTS`), not a data migration, and it is the host's own documented gate — not something this experiment may self-approve.
- **Fallback without v6:** the same slice works over legacy `PUT /v1/data/{collection}/{id}`, losing only the guarantee that an entity and its history event commit together.

## 5. No second DB — PASS

One store instance for the entire proof, standing for one project's D1. No Supabase, no second database, no new binding, no new service. The adapter holds `mb_records`-shaped rows and `mb_commands`-shaped idempotency markers and nothing else.

## 6. No duplicate client / company / deal identity — PASS

- Contacts are the only person identity; deals reference contacts by id.
- **No `companies` collection is introduced.** Atomic models `company` as its own entity; here a contact carries `companyName` as a string. Adding a company object would create a second identity for the same real-world business, which the MPE identity rule forbids without an owner decision. Recorded as a boundary, not an oversight.
- Deals keep one id across stage moves: the proof asserts `deal.id` is unchanged and that the stage change is recorded as `{"field": "stage", "from": …, "to": …}` on an event, never as a new deal record.

## 7. Reuse of existing MiniBase components — PASS

| Reused as-is | Evidence |
| --- | --- |
| CP-04 closed query contract, incl. the opaque `mbq1.<base64url>` cursor with its FNV-1a query-consistency digest | adapter implements the same allowlists and cursor format; a cursor from a different query is refused `invalid_cursor` |
| CP-05 command validation and idempotency (SHA-256 of the key, canonical JSON fingerprint, replay, opaque `idempotency_conflict`) | proven: identical resend replays with the same `commandId`; a changed payload under the same key is a conflict and the stored value is untouched |
| canonical UTC timestamps as an invariant | proven: stored values match `YYYY-MM-DDTHH:mm:ss.sssZ`; a filter value with no timezone is refused `invalid_filter` |
| documented error codes from `src/errors.ts` | `invalid_collection`, `invalid_record_id`, `invalid_record_data`, `record_not_found`, `invalid_filter`, `invalid_operator`, `invalid_order`, `invalid_select`, `invalid_cursor`, `invalid_limit`, `invalid_command`, `invalid_idempotency_key`, `bulk_limit_exceeded`, `idempotency_conflict`, `request_body_too_large` |
| audit shape (`action`, `outcome`, `actor`, `entity`, `entity_id`, `correlation_id`, `metadata`) and the rule that only denials and mutations are audited | CP-04 audit trail: 1 `success`, 3 `denied`, 0 read entries; the raw idempotency key is never stored, only a 16-hex digest |

Nothing had to be invented where MiniBase already defined it. The only new code is the CRM slice itself and its tool surface.

## 8. Fit limits found (and how the slice absorbs them)

These are host facts, verified by executing them in the proof, not opinions.

| MiniBase limit | Source | How the slice handles it |
| --- | --- | --- |
| No filter on an arbitrary JSON field | `docs/DATA_API.md` — "Filtering on an arbitrary JSON field is not supported and will not be until a real consumer need and an index exist for it" | `stage`, `dueDate`, and subject scoping are decided app-side after the page is read; the proof asserts the host refuses `filter[stage]` with `invalid_filter`, so the limit cannot be forgotten later |
| No joins, no views, no FK | `docs/DATA_MODEL.md` — "There are no foreign keys, joins, or per-field indexes reachable through the data API" | counters (`openDealCount`, `pendingTaskCount`) are computed from the read page and reported with `reads.scanned` / `reads.pages`; a deal verifies its contacts exist before writing, and a dangling reference is refused `record_not_found` with nothing written |
| Keyset pagination only, no `OFFSET` | `docs/DATA_API.md` §Pagination | every derived read walks `hasMore` pages up to a declared `max_pages` budget and reports `truncated: true` when it stops early |
| Ordering only by `id`, `createdAt`, `updatedAt` | `src/record-query.ts` `orderFields` | scans use `order=id.asc` (the stable keyset order); the timeline sorts by `occurredAt` after the read |
| One canonical UTC timestamp representation | `docs/DATA_MODEL.md` | Atomic's browser-local day boundaries were replaced with explicit UTC boundaries; buckets are asserted at the exact instants `2026-10-06T00:00:00Z` and `2026-10-11T00:00:00Z` |
| Document size ceiling (`MB_MAX_JSON_BYTES`, default 65 536 B) | `src/limits.ts`, `docs/DATA_API.md` §Limits | activity events store subject ids + a one-line summary, never an embedded entity document |
| Writes need `mb_secret_*`; publishable keys are read-only | `docs/DATA_API.md` §Commands, `docs/CLIENT_SDK.md` | the CP-04 write is server-side by construction; a browser-held publishable key could not perform it, which is why the tool surface is not a client SDK |
| Bulk ceiling `maxBulkRecords` (default 500, per-project quota can only tighten) | `docs/DATA_API.md` §Limits | each write is 2 operations; the adapter enforces the ceiling and the proof exercises `bulk_limit_exceeded` |

## 9. Deep-change assessment — none triggered

Checked against `docs/governance/SCOPE-CHANGE-CONTROL.md` §6: no fundamental architecture change, no approved invariant broken, no public contract changed, no data migration, no source-of-truth change, no new infrastructure platform, no new repository, no security-boundary change, no recurring cost, nothing hard to reverse, and nothing beyond the approved checkpoint. The one owner-gated action named above (schema apply to v6 on a pre-v6 project) is MiniBase's existing documented gate, and this experiment did not perform it.

## CP-02 verdict

**PASS.** One bounded CRM slice — contact → deal → task → activity timeline — is representable on `minibase-cloudflare` as four collections in the project's own D1, served by the existing CP-04 query and CP-05 command, with canonical identities preserved and no second database, no data migration, and no duplicate identity. The costs are explicit and bounded rather than hidden: derived reads are app-side with a declared page budget, and atomic writes require the host's existing v6 schema gate.

Because both CP-01 and CP-02 pass, CP-03 was executed — see [`RESULTS.md`](RESULTS.md) and `evidence/proof_run.json`. The optional Kanban was **not** built: CP-02 found no UI integration point in the host (MiniBase is a Worker with no frontend), so a board would have been scope expansion with no measurable value.
