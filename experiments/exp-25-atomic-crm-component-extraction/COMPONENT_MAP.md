# EXP-25 COMPONENT_MAP — Atomic CRM candidates → existing Murat hosts (CP-01)

Donor pin: `marmelab/atomic-crm` @ `8b5d47ba32190c68801a427ef7682d7a6afc14e0` (see [`UPSTREAM_AUDIT.md`](UPSTREAM_AUDIT.md)).

Hosts named below:
- **minibase-cloudflare** — inspected in this session at `Murkin1980/minibase-cloudflare` @ `9ab38d832970b3956cf0f831f9b578f7b9fd9001` (`ARCHITECTURE.md`, `docs/DATA_API.md`, `docs/DATA_MODEL.md`, `src/record-query.ts`, `src/commands.ts`).
- **salamat-projects-dashboard** — public, described as the portfolio control plane; not inspected beyond its description in this session.
- **business-discovery** — named as an active project in this repository's portfolio snapshot (`dashboard/public/index.html`); the repository is not readable from this session, so no architecture claim is made about it.

No candidate below proposes a new CRM, a new repository, or a second source of truth.

---

## 1. Activity history as an appended event projection — **ADOPT_IN_MINIBASE**

```text
Atomic concept/component  activity_log SQL UNION view + activity/* renderers + consts.ts event types
→ problem solved          one chronological history per client/company that merges contacts, deals,
                          notes, and tasks without asking the user to open four lists
→ framework-neutral part  the event shape: one row per event, stable composite event id,
                          explicit type, timestamp, owning subject ids, and only enough payload
                          to render one line; history is derived, never a second write path
→ Atomic/Supabase part    UNION ALL over Postgres tables, to_json(row) embedding, PostgREST
                          range pagination, security_invoker view, supporting B-tree indexes
→ existing Murat host     minibase-cloudflare: an appended collection in the project's own D1,
                          written by the CP-05 command; also a client-card history for
                          business-discovery and salamat-projects-dashboard consumers
→ overlap/duplication     risk of a second copy of entity data inside events; avoided by storing
                          subject ids + a summary only (proven: no `payload` key on any event)
→ expected value          a client timeline without joins, and without a new storage system
→ keep/reject             KEEP (proven in CP-03)
```

## 2. Entity + history event written as one atomic unit — **ADOPT_IN_MINIBASE**

```text
Atomic concept/component  DB triggers that keep related rows consistent on insert/update
→ problem solved          history can never drift from the entity it describes
→ framework-neutral part  "entity write + its history event" is one transaction, with ids chosen
                          by the caller so a retry cannot invent a second identity
→ Atomic/Supabase part    Postgres triggers, SECURITY DEFINER functions, column defaults
→ existing Murat host     minibase-cloudflare CP-05 POST /v1/commands/records:upsert-many with
                          Idempotency-Key — 2 operations, one atomic statement, replayable
→ overlap/duplication     none; it replaces per-record PUTs, it does not add a layer
→ expected value          atomic entity+event writes with a replay receipt; a client retry cannot
                          duplicate history
→ keep/reject             KEEP (proven in CP-03 and CP-04)
```

## 3. Due-date bucket predicates — **ADOPT_IN_MINIBASE**

```text
Atomic concept/component  tasks/tasksPredicate.ts (isOverdue / isDueToday / isDueTomorrow /
                          isDueThisWeek / isDueLater, isDone, isRecentlyDone)
→ problem solved          "what do I have to do?" answered in five groups instead of a date list
→ framework-neutral part  five named buckets from one due timestamp, plus a short grace window so
                          a just-completed item does not flicker out of the list
→ Atomic/Supabase part    date-fns against browser-local day boundaries; weekStartsOn: 0
→ existing Murat host     minibase-cloudflare consumers (follow-up queues); same buckets suit
                          business-discovery follow-up actions and salamat-projects-dashboard
                          "what is due" views
→ overlap/duplication     none — no equivalent exists in the inspected MiniBase source
→ expected value          a stable follow-up queue; the UTC port removes timezone ambiguity when
                          the store only holds canonical UTC timestamps
→ keep/reject             KEEP (ported to explicit UTC boundaries and proven in CP-04)
```

## 4. Deal pipeline: stage as configuration + derived open/closed — **REUSE_PATTERN_ONLY**

```text
Atomic concept/component  root/defaultConfiguration.ts (defaultDealStages,
                          defaultDealPipelineStatuses), deals/stages.ts (getDealsByStage),
                          deals/DealListContent.tsx (drag/drop, stored index)
→ problem solved          pipeline state that an owner can rename/reorder without a schema change,
                          and a board that keeps manual column ordering
→ framework-neutral part  stage list as configuration; an unknown stage falls back to the first
                          configured stage; "open" derived from stage + archived flag; per-stage
                          counts derived from the same read
→ Atomic/Supabase part    `index` column re-numbered on drag, @hello-pangea/dnd, react-admin
                          data provider, Supabase persistence
→ existing Murat host     minibase-cloudflare as stored `stage` on a deal document; a board UI
                          would belong to a consumer app, not to MiniBase
→ overlap/duplication     Kanban would duplicate a UI layer MiniBase does not have and this
                          experiment did not justify; no second pipeline model is introduced
→ expected value          stage configuration + open-deal derivation reused; board interaction
                          deferred until a real UI consumer exists
→ keep/reject             KEEP pattern (stage config + open derivation proven); REJECT Kanban UI
                          here — CP-03's optional Kanban clause was not triggered because CP-02
                          found no UI integration point
```

## 5. Derived counters (`nb_tasks`, `nb_contacts`, `nb_deals`) — **REUSE_PATTERN_ONLY**

```text
Atomic concept/component  contacts_summary view: count(distinct t.id) filter (where done_date is null)
→ problem solved          list rows show pending follow-ups without an N+1 query
→ framework-neutral part  a counter is a projection over children and must state exactly what it
                          counts (pending vs all); it is derived, not authoritative
→ Atomic/Supabase part    SQL aggregate inside an always-live view, so it never needs invalidation
→ existing Murat host     minibase-cloudflare consumers compute it from the page they already read
                          and report the page cost (proven: openDealCount / pendingTaskCount plus
                          reads.scanned / reads.pages / reads.truncated)
→ overlap/duplication     a *persisted* counter would be a second representation of the same fact
                          and would need an invalidation path — rejected without a real consumer
→ expected value          honest counters with visible read cost instead of a denormalized column
→ keep/reject             KEEP pattern (app-side derivation proven); persisted counters rejected
```

## 6. CSV import: defensive cell parsing + resolve-or-create dedup — **ADOPT_IN_MINIBASE** (pattern only, not proven here)

```text
Atomic concept/component  dataImport/parseCell.ts (toText/toNumber/toInteger/toIsoDate/
                          toConfiguredValue), useCompanyResolver.ts + fetchRecordsWithCache.ts,
                          DataImportDialog.tsx, *_sample.csv, jsonexport export
→ problem solved          a CSV from a human is dirty: ambiguous dates, labels instead of values,
                          the same company name repeated on every row
→ framework-neutral part  coerce per type and refuse ambiguity (only YYYY-MM-DD, impossible days
                          rejected, value-or-label matching); one shared cache so a name repeated
                          in the file is created once; preview before commit; result report after
→ Atomic/Supabase part    PostgREST bulk insert, papaparse in the browser, gravatar/favicon
                          triggers, react-admin data provider
→ existing Murat host     minibase-cloudflare consumer flow: parse → preview → CP-05 upsert-many
                          (batched, idempotent) — the command already provides the atomic,
                          replayable commit this flow needs
→ overlap/duplication     MiniBase's Supabase import path (docs/SUPABASE_MIGRATION.md) already
                          owns bulk migration with manifest/checksums; a CSV contact import must
                          not become a second import mechanism for the same data
→ expected value          a bounded contact import that cannot silently create duplicate
                          companies or shift dates by a timezone
→ keep/reject             KEEP as pattern; not implemented in this experiment (CP-03 scope is
                          contact → deal → task → timeline only)
```

## 7. AI/tool surface: small annotated tool set, one narrow idempotent write — **ADOPT_IN_MINIBASE**

```text
Atomic concept/component  supabase/functions/mcp/index.ts tools (get_schema, query, mutate,
                          complete_task, display_task_list) + validateSql.ts + MCP-App resource
→ problem solved          give a model useful CRM actions without giving it the whole database
→ framework-neutral part  a few named tools with explicit readOnly/destructive/idempotent
                          annotations; reads unrestricted, writes narrow and id-based; a
                          validation layer between the model and the store
→ Atomic/Supabase part    raw SQL as the tool argument, pgsql-ast-parser allowlisting, Supabase
                          JWT/JWKS + RLS, Deno edge runtime, MCP-App HTML resource
→ existing Murat host     minibase-cloudflare's own contract already forbids SQL, so the
                          equivalent control is structural: three named reads + one approval-gated
                          write over /v1/data and /v1/commands (proven in CP-04)
→ overlap/duplication     no new server: the experiment-local surface sits on the existing data
                          plane; production exposure would be a separate owner decision
→ expected value          read-first AI assistance with one auditable, replayable write
→ keep/reject             KEEP (shape proven in CP-04; production MCP exposure not authorized)
```

## 8. Identity discipline: one object → one identity → many representations — **ADOPT_IN_MINIBASE**

```text
Atomic concept/component  ids referenced by string across contacts/deals/tasks/notes, and ids
                          embedded in synthetic activity ids ('deal.' || d.id || '.created')
→ problem solved          the same client is one thing everywhere, so history and counters can be
                          joined by the user's own mental model
→ framework-neutral part  one canonical id per business object, repeated verbatim by every
                          reference; ids stable enough to compose event ids from
→ Atomic/Supabase part    Postgres identity/uuid columns and FK constraints
→ existing Murat host     MiniBase record ids already match ^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$,
                          so canonical ids (contact-c-001, deal-d-001, task-t-001,
                          event-…) need no new id system
→ overlap/duplication     none; this is the existing MPE identity rule, and the proof shows no
                          second id scheme was needed
→ expected value          no duplicate client/company/deal identity in MiniBase
→ keep/reject             KEEP (proven in CP-03)
```

## 9. shadcn registry packaging for CRM components — **REJECT**

```text
Atomic concept/component  registry.json (one registry:block, 227 files), components.json,
                          scripts/generate-registry.mjs
→ problem solved          a fork can pull component updates instead of drifting
→ framework-neutral part  publish UI as a versioned block consumers install by name
→ Atomic/Supabase part    shadcn registry schema, Vite/Storybook, shadcn-admin-kit dependency
→ existing Murat host     none: minibase-cloudflare has no frontend (src/ is a Worker), and this
                          experiment adds no UI
→ overlap/duplication     would introduce a second design system into a portfolio that has none
                          for internal tools
→ expected value          zero today; a second design system is a cost, not a benefit
→ keep/reject             REJECT — no current consumer; revisit only if a real UI host appears
```

## 10. Email-to-note capture (Postmark) — **REJECT**

```text
Atomic concept/component  supabase/functions/postmark/* (recipient matching against primary and
                          secondary sale addresses, forwarded-mail parsing, attachment extraction,
                          note creation)
→ problem solved          communication lands in the client history without manual copy/paste
→ framework-neutral part  match an inbound message to a known identity, deduplicate, attach
                          provenance, store as one note event
→ Atomic/Supabase part    Postmark webhook, Supabase storage bucket, sale secondary_emails,
                          server-side attachment extraction
→ existing Murat host     none in scope; production email ingestion is an EXP-25 stop condition
→ overlap/duplication     would need consent/privacy review, deduplication, and an ingestion
                          service — all outside this bounded experiment
→ expected value          unproven here
→ keep/reject             REJECT for this experiment (pattern noted only)
```

## 11. Server-side contact merge / dedup — **REJECT**

```text
Atomic concept/component  supabase/functions/merge_contacts/index.ts
→ problem solved          two records for one human collapse into one surviving identity
→ framework-neutral part  merge child references and unique arrays before retiring a duplicate
→ Atomic/Supabase part    Kysely SQL over Postgres, auth middleware, transactional update
→ existing Murat host     none; MiniBase has no relational merge, and identity merging is an
                          identity-system change
→ overlap/duplication     a merge tool would silently rewrite canonical ids, which the MPE
                          identity rule protects
→ expected value          unproven; the risk is identity churn
→ keep/reject             REJECT — dedup belongs to a future CSV import design (candidate 6),
                          not to this slice
```

---

## CP-01 verdict

**PASS.** Eight patterns (1–8) map onto existing Murat systems — primarily `minibase-cloudflare`, with named secondary relevance for business-discovery and salamat-projects-dashboard — and three candidates (9–11) are rejected with reasons. The threshold was five useful patterns with no parallel-CRM proposal; the result is eight keeps and zero new systems. No Atomic CRM code was copied, installed, or vendored.

Per-candidate dispositions are repeated in [`RESULTS.md`](RESULTS.md); the MiniBase-specific verification is in [`MINIBASE_FIT.md`](MINIBASE_FIT.md).
