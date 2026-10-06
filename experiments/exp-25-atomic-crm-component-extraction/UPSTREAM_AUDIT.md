# EXP-25 UPSTREAM_AUDIT — marmelab/atomic-crm (CP-01)

**Audit date:** 2026-10-06 UTC
**Purpose:** inspect the donor only. Atomic CRM was cloned read-only into a scratch directory outside this repository; it was **not** installed, built, run, deployed, or connected to any data. No upstream source file was copied into MPE. No new repository, database, or CRM was created.

## Pin

| Item | Value |
| --- | --- |
| Repository | `https://github.com/marmelab/atomic-crm` |
| Pinned commit | [`8b5d47ba32190c68801a427ef7682d7a6afc14e0`](https://github.com/marmelab/atomic-crm/tree/8b5d47ba32190c68801a427ef7682d7a6afc14e0) |
| Commit subject / date | `Merge pull request #372 from marmelab/feat/dependency-gate`, 2026-10-05 15:14:23 +0200 |
| `git describe --tags --always` | `8b5d47b` (the shallow clone resolves no tag; the code audit is pinned to the commit above) |
| `package.json` version | `0.1.0` |
| Latest release in `CHANGELOG.md` | `v1.6.0` — 2026-09-22 |
| License | MIT — `LICENSE.md`, "Copyright (c) 2024-present, Francois Zaninotto, Marmelab" |

All file references below are paths inside the pinned commit.

## Stack and delivery shape

- Frontend: React 19, `ra-core` 5.14 (react-admin), Radix/shadcn (`components.json`, style `new-york`), Tailwind 4, `@hello-pangea/dnd` (Kanban drag/drop), `papaparse` + `jsonexport` (CSV), `@nivo/bar`, `@tanstack/react-query` with a persist client.
- Backend: Supabase — `supabase/migrations/` (27 files), `supabase/schemas/` as the declarative source of truth (`01_tables.sql` … `07_storage.sql`), `supabase/functions/` with 6 edge functions (`mcp`, `postmark`, `merge_contacts`, `delete_note_attachments`, `update_password`, `users`) plus a `_shared` module directory.
- Data access: PostgREST through `ra-supabase-core`; row-level security per sale; SQL views for aggregation.
- Packaging: one shadcn registry block — `registry.json` declares a single item `atomic-crm` of type `registry:block` containing **227 files** (222 `registry:component`, 3 `registry:hook`, 1 `registry:lib`, 1 `registry:file`).
- AI/API surface: a Supabase edge function that runs an MCP server (`supabase/functions/mcp/index.ts`, 648 lines) with a SQL-validating guard (`validateSql.ts`) and an MCP-App HTML resource (`taskListUi.ts`).
- Tests: Vitest unit tests next to components (`tasksPredicate.test.ts`, `dealUtils.test.ts`, `DealList.test.tsx`, `parseCell.test.ts`), Playwright specs in `e2e/`, Storybook stories.

## Concept inventory

| Atomic concept | Pinned source | What it actually is |
| --- | --- | --- |
| contact | `src/components/atomic-crm/types.ts` (`Contact`) | flat record; `email_jsonb` / `phone_jsonb` typed arrays; `tags`, `status`, `sales_id`, `first_seen`/`last_seen` |
| company | `types.ts` (`Company`) | flat record with sector/size/address; `nb_contacts`, `nb_deals` counters |
| deal | `types.ts` (`Deal`) | `stage`, `amount`, `contact_ids[]`, `expected_closing_date`, `archived_at`, and an `index` column for Kanban ordering |
| deal stages | `root/defaultConfiguration.ts` | `defaultDealStages` = opportunity, proposal-sent, in-negociation, won, lost, delayed; `defaultDealPipelineStatuses = ["won"]` |
| task / reminder | `types.ts` (`Task`), `root/defaultConfiguration.ts` | `contact_id`, `type` (9 configured types), `text`, `due_date`, `done_date` |
| due-date buckets | `tasks/tasksPredicate.ts` | `isOverdue`, `isDueToday`, `isDueTomorrow`, `isDueThisWeek`, `isDueLater`, `isDone`, `isRecentlyDone` (5-minute anti-flicker window) |
| note | `types.ts` (`ContactNote`, `DealNote`) | text + date + author + attachments; note statuses cold/warm/hot/in-contract |
| activity history | `supabase/migrations/20260314120000_activity_log_view.sql`, `activity/*`, `consts.ts` | a SQL `UNION ALL` **view** `activity_log` with synthetic ids (`'deal.' \|\| d.id \|\| '.created'`), one row per event, paginated by PostgREST range headers |
| derived counters | `supabase/migrations/20260307120000_nb_tasks_pending_only.sql` | `contacts_summary` view: `count(distinct t.id) filter (where t.done_date is null) as nb_tasks` plus flattened `email_fts`/`phone_fts` |
| CSV import/export | `dataImport/*` (`parseCell.ts`, `useCompanyResolver.ts`, `createEachRow.ts`, `fetchRecordsWithCache.ts`, `DataImportDialog.tsx`, `*_sample.csv`) | typed cell coercion, label-or-value matching, resolve-or-create company cache shared by importers, dialog + progress toast, `jsonexport` on the read path |
| contact merge / dedup | `supabase/functions/merge_contacts/index.ts` | server-side merge of duplicate contacts with unique-array/unique-object merging |
| API / AI surface | `supabase/functions/mcp/index.ts`, `validateSql.ts`, `taskListUi.ts` | MCP tools `get_schema`, `query` (SELECT only), `mutate` (INSERT/UPDATE/DELETE), `complete_task`, `display_task_list`, plus an MCP-App UI resource; every tool carries `readOnlyHint` / `destructiveHint` / `idempotentHint` annotations; RLS scopes all reads and writes to the authenticated sale |
| email → note | `supabase/functions/postmark/*` | inbound webhook matches a sale's primary/secondary address, extracts the real recipient, creates a contact note with attachments |
| Kanban board | `deals/DealListContent.tsx`, `deals/stages.ts`, `deals/DealColumn.tsx`, `deals/DealCard.tsx` | `@hello-pangea/dnd` context, stage grouping with unknown-stage fallback to the first stage, in-column ordering by the stored `index`, optimistic reorder then persisted index shifts |
| component packaging | `registry.json`, `components.json`, `scripts/generate-registry.mjs` | the CRM is published as one shadcn registry block so a fork can pull component updates |

## Framework-neutral part vs Atomic/Supabase-specific part

| Concept | Framework-neutral (transferable) | Atomic/Supabase-specific (not transferable) |
| --- | --- | --- |
| activity history | the **event projection** rule: one row per event, a stable composite event id, an explicit `type`, a timestamp, the owning subject ids, and enough payload to render a line — the union is a *derived* view, never a second write path | `UNION ALL` over Postgres tables, `to_json(row)` embedding, PostgREST range pagination, `security_invoker` view, the supporting B-tree indexes |
| entity + history consistency | write the entity and its history event as **one atomic unit**, keyed by ids the caller chose | Supabase triggers (`handle_contact_note_created_or_updated`, `handle_contact_saved`) and DB-side defaults |
| due-date buckets | five named buckets from a due timestamp, plus a short "recently done" grace window | `date-fns` against **browser-local** day boundaries (`startOfToday`, `endOfWeek({weekStartsOn: 0})`) |
| deal pipeline | stage list as configuration; a stage unknown to the configuration falls back to the first stage; "open" is derived from stage + `archived_at`; column order is a stored integer | `index` column maintained by re-indexing neighbours on drag, react-admin data provider, `@hello-pangea/dnd` |
| derived counters | a counter is a projection over children, and it must state what it counts (pending vs all) | SQL `count(...) filter (where ...)` inside a view; no invalidation problem because the view is always live |
| CSV import | typed cell coercion that refuses ambiguous input (`toIsoDate` rejects non-`YYYY-MM-DD` and impossible days; `toConfiguredValue` accepts value **or** label), one shared resolve-or-create cache so a repeated name is created once, preview before commit | PostgREST bulk insert, gravatar/favicon triggers, react-admin data provider, `papaparse` in the browser |
| AI/API surface | a **small named tool set** with explicit read/write annotations, one narrow idempotent write (`complete_task` by id) instead of a general mutation tool, and a validation layer between the model and the store | raw SQL as the tool argument, `pgsql-ast-parser` allowlisting, Supabase JWT/JWKS + RLS, Deno edge runtime, MCP-App HTML resource |
| identity | one id per business object, referenced by that same string from every related record; ids are stable enough to be embedded in event ids | Postgres `bigint`/`uuid` identity columns and FK constraints |
| component packaging | publish UI as a versioned registry block so consumers pull updates instead of forking blindly | shadcn registry schema, Vite/Storybook tooling, the `shadcn-admin-kit` dependency |

## Host assumptions that do not transfer

- **Supabase/PostgREST is the data plane.** Joins, views, FKs, `RETURNING`, RLS, and server-side triggers are all load-bearing in Atomic CRM. MiniBase offers none of them: it is a document store with a closed query contract (see `MINIBASE_FIT.md`).
- **SQL is the AI tool interface.** Atomic's guard exists because the model writes SQL. Any host that does not accept SQL does not need the guard — it needs a closed tool set instead.
- **Auth is per-sale.** `sales_id` scoping and RLS assume a multi-user sales team; MPE hosts do not have that identity model, and this experiment adds none.
- **Browser-local time.** Every date predicate is computed against the user's local day. A UTC-only store needs the boundaries made explicit.

## Audit conclusion

**Donor-only.** Seven concept areas carry transferable structure — activity history as an appended event projection, entity+event atomicity, due-date buckets, stage-as-configuration, derived-counter discipline, defensive CSV cell parsing, and a narrow annotated tool surface. Everything else (Supabase schema, PostgREST/RLS, react-admin data provider, Kanban drag/drop, shadcn registry packaging, Postmark ingestion) is platform- or UI-specific and is not adopted here.

No Atomic CRM component was installed, vendored, or copied. No parallel CRM is proposed. The mapping to Murat hosts is in [`COMPONENT_MAP.md`](COMPONENT_MAP.md).
