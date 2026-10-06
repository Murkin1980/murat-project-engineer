# EXP-25 — Results and component-level recommendation

- **Run date:** 2026-10-06 UTC
- **New Idea Filter disposition:** `REUSE_COMPONENT`
- **Experiment result:** **PASS** (CP-01, CP-02, CP-03, CP-04 all pass)
- **Overall adoption:** **ADOPT_WITH_CHANGES** — pattern-level reuse inside existing systems; no CRM product adoption
- **Donor pin:** `marmelab/atomic-crm` @ `8b5d47ba32190c68801a427ef7682d7a6afc14e0` (MIT)
- **Host pin:** `Murkin1980/minibase-cloudflare` @ `9ab38d832970b3956cf0f831f9b578f7b9fd9001` (read-only; **no file in that repository was changed**)
- **Scope:** bounded, experiment-local, test data only. No CRM deployed, no new repository, no Supabase, no second database, no live-data migration, no production integration, no autonomous writes.

## Executive result

Eight Atomic CRM patterns transfer to `minibase-cloudflare` without a parallel CRM; three candidates were rejected with reasons ([`COMPONENT_MAP.md`](COMPONENT_MAP.md)). The bounded slice `contact → deal → task → activity timeline` runs on the host's existing data contract: four logical collections in one project D1, reads through the CP-04 closed query, writes through the CP-05 `records:upsert-many` command. The read-first tool surface exposes three reads and exactly one approval-gated write, and every write and denial is audited.

The proof is deterministic: **25/25 checks pass**, and two consecutive runs of `evidence/proof_run.json` are byte-identical (`md5 ee50786bf3cd6dd3464f035f785b1560`).

## Checkpoint results

| Checkpoint | Result | Evidence |
| --- | --- | --- |
| CP-01 architecture extraction | **PASS** — 8 patterns mapped to existing hosts (threshold: 5), 3 rejected, no parallel CRM proposed | [`UPSTREAM_AUDIT.md`](UPSTREAM_AUDIT.md), [`COMPONENT_MAP.md`](COMPONENT_MAP.md) |
| CP-02 Minibase fit | **PASS** — one bounded slice fits with canonical identity, no second DB, no data migration, no duplicate identity | [`MINIBASE_FIT.md`](MINIBASE_FIT.md) |
| CP-03 smallest proof | **PASS** — slice works against a MiniBase-compatible adapter without any part of Atomic's runtime | `harness/`, `evidence/proof_run.json` |
| CP-04 read-first AI/tool proof | **PASS** — 3 reads, 1 controlled write; IDs preserved, provenance recorded, auditable, bounded to test data | `harness/tool_surface.py`, `evidence/proof_run.json` |
| Optional Kanban | **Not built** — CP-02 found no UI integration point in the host (MiniBase is a Worker with no frontend), so a board would be scope expansion with no measurable value | [`MINIBASE_FIT.md`](MINIBASE_FIT.md) §CP-02 verdict |

## What the proof measured

Fixture: 3 contacts, 4 deals (2 open, 1 won, 1 lost), 6 tasks (1 already completed), fixed instant `2026-10-06T09:00:00.000Z`, dataset `exp-25-test`.

**CP-03 — the slice**

- One canonical id per object; references repeat the same string (`deal-d-001.contactIds == ["contact-c-001"]`, `task-t-001.contactId == "contact-c-001"`).
- 13 entities produced 13 activity events, each written in the **same** CP-05 command as its entity (`operationCount: 2`).
- A deal pointing at a missing contact is refused `record_not_found` and **nothing** is written — referential integrity enforced in the app layer, because `mb_records` has no foreign keys.
- Timeline for `contact-c-001`: 5 events, newest first (`task.created`, `task.created`, `deal.created`, `deal.created`, `contact.created`); events carry subject ids and a summary, never an embedded entity document.
- The host refuses `filter[stage]` with `invalid_filter` — asserted, so the "no JSON-field filter" limit cannot be silently forgotten later.
- Keyset paging with `limit=2` walked 3 pages and returned all 6 tasks exactly once.

**CP-04 — the tool surface**

| Action | Result |
| --- | --- |
| `list_open_deals` | 2 open deals (`deal-d-001`, `deal-d-002`), `{opportunity: 1, proposal-sent: 1}`, open amount total `2430.0`, read cost 4 records / 1 page |
| `get_client_context(c-001)` | 2 deals, 1 open deal, 2 pending tasks, 5 activity events, per-read cost reported |
| `list_due_tasks` | buckets `overdue 1 / today 1 / tomorrow 1 / this-week 1 / later 1`; the completed task is excluded |
| `create_follow_up_task` **without** approval | refused `approval_required`, 0 mutations |
| approved write against a record outside the test dataset | refused `write_out_of_bounds`, 0 mutations |
| `change_deal_stage` (second write candidate) | declared, **not exposed** → `tool_not_available` |
| `create_follow_up_task` **with** approval | `task-fu-c-001-proposal` + its event in one command (`operationCount: 2`, `commandId ff4c82f6bb15797b6d806fa811bcd89e9fbc`); `contactId`/`dealId` preserved verbatim |
| identical resend under the same key | `replayed: true`, same `commandId`, no duplicate record (7 tasks, not 8) |
| same key, different payload | `idempotency_conflict`, stored value untouched |
| second approved write in the same run | refused `write_budget_exhausted` |
| read after the write | the new task appears in the `tomorrow` bucket; the contact now shows 3 pending tasks and 6 events |

Audit trail: **1 `success`, 3 `denied`, 0 read entries** (MiniBase audits denials and mutations, not successful reads). The raw `Idempotency-Key` is never stored — only a 16-hex SHA-256 digest, and the test asserts the raw key does not appear in any audit entry.

Whole proof cost: **75 MiniBase statements** (pages, single-record reads, commands), counted by the adapter.

## Per-component disposition

| # | Component / pattern | Disposition |
| --- | --- | --- |
| 1 | Activity history as an appended event projection | **ADOPT_IN_MINIBASE** |
| 2 | Entity + history event as one atomic write (CP-05 command) | **ADOPT_IN_MINIBASE** |
| 3 | Due-date bucket predicates (UTC port) | **ADOPT_IN_MINIBASE** |
| 4 | Stage-as-configuration + derived open/closed | **REUSE_PATTERN_ONLY** |
| 4b | Kanban drag/drop board | **REJECT** (no UI host; CP-03's optional clause not triggered) |
| 5 | Derived counters (`nb_tasks` and friends) | **REUSE_PATTERN_ONLY** (compute from the read page, report the cost; no persisted counter) |
| 6 | CSV import cell parsing + resolve-or-create dedup | **ADOPT_IN_MINIBASE** (pattern only — not implemented in this experiment) |
| 7 | Small annotated tool set, one narrow idempotent write | **ADOPT_IN_MINIBASE** |
| 8 | One object → one identity → many representations | **ADOPT_IN_MINIBASE** |
| 9 | shadcn registry packaging of CRM components | **REJECT** (no UI consumer; would introduce a second design system) |
| 10 | Email-to-note capture (Postmark) | **REJECT** (production email ingestion is a stop condition) |
| 11 | Server-side contact merge / dedup | **REJECT** (identity churn risk; belongs to a future import design) |
| — | Atomic CRM as a product / Supabase backend / react-admin data provider | **REJECT** |

`ADOPT_IN_BUSINESS_DISCOVERY` and `ADOPT_IN_SALAMAT` were **not** used: business-discovery is named in this repository's portfolio snapshot but its repository is not readable from this session, and `salamat-projects-dashboard` is a dashboard, not a CRM host. Both are noted as plausible future consumers of patterns 1 and 3, with no architecture claim attached.

## Exact components worth reusing

1. **Appended activity-event collection** (`crm_activity_events`-shaped): one record per event with `type`, `occurredAt`, `actor`, `subjects` (canonical ids), a one-line `summary`, an optional `change {field, from, to}`, and a `provenance` block. Replaces Atomic's SQL `activity_log` view on a join-less store.
2. **Entity + event atomic write unit** on `POST /v1/commands/records:upsert-many` with a client-chosen `Idempotency-Key`: 2 operations, replayable, conflict-opaque. This is the single highest-value transfer — it gives history consistency without triggers.
3. **UTC due-date buckets** (`overdue / today / tomorrow / this-week / later`) with explicit UTC day boundaries, plus a short "recently done" grace window.
4. **Derived-read discipline**: a derived read declares its page budget, reports `scanned` / `pages` / `truncated`, and computes counters from the page it read. This is what makes "no JSON-field filter, no joins" survivable in practice.
5. **Read-first tool surface**: three named reads + one approval-gated write with actor, reason, idempotency key, test-data bounds, a finite write budget, and an append-only audit trail.
6. **Canonical identity discipline**: record id = business identity, repeated verbatim by every reference, composed into event ids.

## Files changed

All changes are additive and confined to this experiment plus one test module.

| File | Lines | Role |
| --- | ---: | --- |
| `experiments/exp-25-atomic-crm-component-extraction/UPSTREAM_AUDIT.md` | new | CP-01 upstream audit and pin |
| `experiments/exp-25-atomic-crm-component-extraction/COMPONENT_MAP.md` | new | CP-01 candidate map with per-component disposition |
| `experiments/exp-25-atomic-crm-component-extraction/MINIBASE_FIT.md` | new | CP-02 verification against the host contract |
| `experiments/exp-25-atomic-crm-component-extraction/RESULTS.md` | new | this file |
| `experiments/exp-25-atomic-crm-component-extraction/harness/minibase_adapter.py` | new | in-memory implementation of the documented MiniBase data-plane contract |
| `experiments/exp-25-atomic-crm-component-extraction/harness/crm_slice.py` | new | CP-03 slice: identity, atomic entity+event writes, timeline, derived reads |
| `experiments/exp-25-atomic-crm-component-extraction/harness/tool_surface.py` | new | CP-04 read-first tool surface + approval-gated write + audit trail |
| `experiments/exp-25-atomic-crm-component-extraction/harness/fixtures.json` | new | synthetic test data (no live customer data) |
| `experiments/exp-25-atomic-crm-component-extraction/harness/run_proof.py` | new | deterministic runner; writes the evidence files |
| `experiments/exp-25-atomic-crm-component-extraction/evidence/proof_run.json` | generated | machine evidence for all 25 checks |
| `experiments/exp-25-atomic-crm-component-extraction/evidence/proof_run.log` | generated | human-readable runner output |
| `tests/test_exp25_crm_slice.py` | new | 26 unittest cases over the adapter, slice, and tool surface |
| `experiments/EXPERIMENT_REGISTRY.json` | edited | EXP-25 entry: `PLANNED` → `PASS`, result summary, evidence links |

No file outside this repository was modified. `minibase-cloudflare` was cloned read-only into a scratch directory for inspection.

## Checks run

| Check | Command | Result |
| --- | --- | --- |
| Bounded proof (CP-03 + CP-04) | `python3 experiments/exp-25-atomic-crm-component-extraction/harness/run_proof.py` | exit 0 — **25 passed, 0 failed** |
| Proof determinism | run twice, compare `md5sum evidence/proof_run.json` | identical (`ee50786bf3cd6dd3464f035f785b1560`) |
| New tests | `python3 -m unittest tests.test_exp25_crm_slice` | **26 tests, OK** — exercises `InMemoryMiniBase.upsert_many` replay/conflict, `list()` filter refusals, `CrmSlice.timeline`, `ToolSurface.dispatch` denials and the approved write |
| Byte-compile | `python3 -m py_compile experiments/exp-25-atomic-crm-component-extraction/harness/*.py` | OK |
| Evidence JSON | `python3 -m json.tool experiments/exp-25-atomic-crm-component-extraction/evidence/proof_run.json` (and the test `test_evidence_artifacts_are_valid_json`) | parses |
| Registry JSON + schema | `python3 -m json.tool experiments/EXPERIMENT_REGISTRY.json`; `tests.test_contracts` status-enum assertion | parses; EXP-25 status `PASS` is inside the schema enum |
| Full suite, before this change | `PYTHONHASHSEED=0 python3 -m unittest discover -s tests` | 343 tests — 41 failures, 3 errors, 1 skipped (all pre-existing dashboard/registry-view drift) |
| Full suite, after this change | `PYTHONHASHSEED=0 python3 -m unittest discover -s tests` | 369 tests — **41 failures, 3 errors, 1 skipped**; the FAIL/ERROR set is byte-identical to the pre-change run (`diff` empty), so this change adds 26 passing tests and **no new failures** |

### Pre-existing repository breakage (not caused by, and not fixed by, this experiment)

- `tests/test_dashboard_registry_views.py` and `tests/test_dashboard_navigation.py` fail because the committed dashboard snapshot (`dashboard/public/index.html`, `dashboard/public/registry/*.svg`) still stops at **EXP-19** while the registry holds 27 experiments; `status-fail.svg`, `status-retired.svg`, and `status-partial.svg` are missing.
- `tests/test_contracts.py::…required_identity_and_status_fields` fails 4 times because the registry contains statuses outside the `contracts/EXPERIMENT_REGISTRY.schema.json` enum (`PARTIAL` ×1, `RETIRED` ×3). EXP-25 deliberately uses `PASS`, which is in the enum.
- Those counts vary between processes (41/3, 42/2, 69/2 observed) because the failing tests iterate a Python `set` of statuses and hash order is randomized per process. With `PYTHONHASHSEED=0` the results are stable and identical with and without this experiment's test module.
- Fixing this is a separate dashboard-refresh/registry-hygiene task (it would rewrite the frozen `exp-19/cp02` artifacts the tests compare against). Per `docs/governance/SCOPE-CHANGE-CONTROL.md` §12 it was recorded, not folded into EXP-25.

## Blockers and limitations

1. **Adapter, not a live worker.** The proof runs against an in-memory implementation of the documented MiniBase contract, not a deployed Worker with real D1. That is what the checkpoint asks for ("use a Minibase-compatible adapter/contract"), but it does not verify real D1 REST latency, real quotas, or Cloudflare-side behavior. A live-host smoke run would need owner-approved resources.
2. **Atomic writes need the host's v6 schema gate.** `records:upsert-many` requires project schema v6; on a pre-v6 project that is an owner-approved `POST /v1/projects/{id}/schema/apply` (additive metadata, no data migration). Without it the slice still works via legacy `PUT`, losing entity+event atomicity.
3. **Derived reads scale with page count, not with a WHERE clause.** "Open deals", "due tasks", and "timeline for one contact" are app-side selections over bounded keyset pages. The proof dataset is tiny (4 deals, 6 tasks, 14 events, all in one page each); at real volume these reads need either a per-project page budget that is honestly reported (implemented: `truncated`), or a host-side filter field added only when a real consumer and an index justify it — a separate host decision.
4. **No company object.** Atomic models `company` separately; here `companyName` is a string on the contact, deliberately, to avoid a second identity for the same business. Introducing a company entity is an owner decision, not an experiment outcome.
5. **No VRU claimed.** No live or production-like workflow was changed or measured, so no Verified Relief Unit is recorded (`docs/VALUE_UNIT_ECONOMICS.md`). The value proven here is implementation-effort reduction for a future MiniBase consumer, not delivered relief.
6. **No production AI surface.** CP-04 proves the tool *shape* locally. Exposing an MCP/AI endpoint over real MiniBase data would need authentication, key scoping (`mb_secret_*` server-side only), and owner approval — none of which this experiment performed.

## Next authorized action

Stop here. The bounded experiment is complete; no production integration is authorized by this result. If the owner wants to continue, the smallest next step is a separate, explicitly approved checkpoint that ports **pattern 2** (entity + event via `records:upsert-many`) into a real MiniBase consumer project with owner-approved schema verification — not a CRM.

**Change-size note (`docs/governance/SCOPE-CHANGE-CONTROL.md` §21):** this change adds **3,109 handwritten lines** (2,159 harness + 415 tests + 535 documents) plus 11 changed lines in the registry and ≈0.8k generated evidence lines. That is at the **MERGE CHECKPOINT** threshold: this branch is a stable, testable boundary and should be reviewed/merged before any further checkpoint is started on it. No PR or merge was opened — merge authority was not granted for this task, and the work stays on the session branch `arena/19e8a6f6-murat-project-engineer`.
