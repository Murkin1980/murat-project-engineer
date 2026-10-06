# EXP-25 — Atomic CRM component extraction

## Disposition

**REUSE_COMPONENT**

Atomic CRM is not adopted as a standalone CRM and no new repository is authorized.

Source:
- https://github.com/marmelab/atomic-crm
- MIT license
- React + shadcn-admin-kit frontend
- Supabase backend
- API integration surface
- shadcn registry for reusable components

## Goal

Identify the smallest reusable CRM building blocks from Atomic CRM that can strengthen existing Murat tools, with **minibase-cloudflare** as the primary candidate host, while avoiding a second source of truth or a parallel CRM platform.

## Reuse candidates

### 1. CRM entity model
Evaluate the transferable domain model around:
- contacts
- companies
- deals
- tasks/reminders
- notes
- activity history

Target:
- Minibase as storage/source layer where appropriate
- Business Discovery as intake/enrichment producer
- Salamat client/order workflows as downstream consumers

Constraint: preserve the MPE identity rule — one business object, one identity, multiple representations.

### 2. Deal pipeline / Kanban
Extract the interaction and state-management pattern for:
- deal stages
- drag/drop stage movement
- stage counters / summaries
- next-action visibility

Potential hosts:
- Minibase CRM module
- Salamat sales dashboard

Do not copy Supabase-specific persistence blindly. UI/state patterns must be adapted to existing APIs.

### 3. Activity timeline
Evaluate a reusable aggregated client timeline combining:
- notes
- deal changes
- tasks
- communication events
- follow-up actions

Potential hosts:
- Minibase
- Business Discovery case/client view
- Salamat client card

### 4. CSV import/export
Reuse or adapt the bounded contact import/export flow:
- field mapping
- validation
- duplicate handling
- preview before commit
- import result report

Primary host:
- Minibase

### 5. API / AI tool surface
Atomic CRM explicitly exposes API integration. Evaluate its command/resource shape as inspiration for an AI-access layer over our existing data.

Candidate operations:
- find open deals
- find overdue tasks
- fetch a client/company context
- create a follow-up task
- change a deal stage

Preferred direction:
- adapt to our existing Minibase/API/tool surface
- no autonomous writes without existing MPE approval rules

### 6. shadcn component reuse/update pattern
Atomic publishes CRM components through a shadcn registry. Evaluate whether its component packaging/update pattern is useful for:
- Minibase UI
- Salamat dashboards
- other React-based internal tools

Do not introduce a second design system. Reuse only components that fit existing project UI rules.

### 7. Email-to-note pattern
Atomic supports capturing email into CRM notes. Evaluate the pattern only, not the whole mail stack.

Potential integration:
- Gmail connector / controlled ingestion
- client timeline in Minibase

Any implementation requires deduplication, provenance, consent/privacy review, and no hidden background ingestion.

## Explicit non-goals

- Do not deploy Atomic CRM as production CRM.
- Do not create a new repository.
- Do not migrate live customer data.
- Do not introduce Supabase as a second source of truth merely because Atomic uses it.
- Do not duplicate Business Discovery.
- Do not create a separate identity system.
- Do not add autonomous CRM writes.
- Do not change production architecture in this experiment.

## Checkpoints

### CP-01 — architecture extraction
Map Atomic's contact/company/deal/task/note/activity structures and identify framework-neutral concepts versus Supabase-specific implementation.

**PASS:** at least 5 reusable patterns are mapped to existing Murat projects with no duplicate system proposal.

### CP-02 — Minibase fit
Map the selected patterns onto minibase-cloudflare:
- canonical IDs
- storage/API contracts
- UI integration points
- migration-free prototype path

**PASS:** a bounded CRM slice can be represented without a second database or conflicting source of truth.

### CP-03 — smallest UI proof
Prototype one narrow slice using test data only:
**contact → deal → task → activity timeline**.

Optional Kanban is included only if CP-02 shows a clean fit.

**PASS:** the slice works against a Minibase-compatible adapter and does not require Atomic's full runtime.

### CP-04 — AI/tool proof
Expose a minimal read-first tool surface:
- list open deals
- get client context
- list due tasks

One controlled write may be tested:
- create follow-up task **or**
- change deal stage

**PASS:** tool actions preserve IDs, provenance, authorization boundaries, and are auditable.

## Adoption rule

After the experiment, each candidate receives one of:
- ADOPT_IN_MINIBASE
- ADOPT_IN_BUSINESS_DISCOVERY
- ADOPT_IN_SALAMAT
- REUSE_UI_ONLY
- REUSE_PATTERN_ONLY
- REJECT

Full Atomic CRM adoption is out of scope unless a separate New Idea Filter later proves that component-level reuse is insufficient.

## Success criteria

The experiment is successful if it identifies a small set of reusable components/patterns that reduce implementation effort in existing projects without adding a parallel CRM, second source of truth, or unnecessary infrastructure.

## Initial priority

High practical value, but behind any currently active blocking production work. The first implementation candidate should be **Minibase CRM slice**, because it can become the reusable data/API layer for multiple existing tools.
