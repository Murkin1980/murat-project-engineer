# Arena Task — EXP-25 Atomic CRM component extraction

Decision: **REUSE_COMPONENT**

Repository: `Murkin1980/murat-project-engineer`

Primary target for fit analysis: existing project `minibase-cloudflare`.

Do not create a new repository. Do not deploy Atomic CRM. Do not add Supabase as a second source of truth. Do not migrate live customer data.

Read:
1. `AGENTS.md`
2. mandatory MPE governance
3. `experiments/exp-25-atomic-crm-component-extraction/README.md`

## Goal

Extract only reusable Atomic CRM components/patterns that can strengthen existing Murat systems, primarily Minibase.

Source:
`https://github.com/marmelab/atomic-crm`

## Execute in order

### CP-01 — architecture extraction

Audit current Atomic CRM and pin the upstream commit/tag used.

Map:
- contact
- company
- deal
- task/reminder
- note
- activity history
- CSV import/export
- API/AI surface
- relevant reusable UI/component packaging

For each candidate record:

```text
Atomic concept/component
→ problem solved
→ framework-neutral part
→ Atomic/Supabase-specific part
→ existing Murat host
→ overlap/duplication risk
→ expected value
→ keep/reject
```

PASS only if at least 5 useful patterns map to existing projects without proposing a parallel CRM.

### CP-02 — Minibase fit

Map selected candidates onto existing `minibase-cloudflare` architecture.

Verify:
- canonical object identity;
- storage/source-of-truth compatibility;
- API fit;
- no migration requirement;
- no second DB;
- no duplicate client/company/deal identity;
- reuse of existing Minibase components where possible.

Respect:
**one object → one identity → many representations**.

PASS only if one bounded CRM slice fits without deep-change.

### CP-03 — smallest proof

Only if CP-01 and CP-02 pass, create the smallest experiment-local proof with test data:

```text
contact
→ deal
→ task
→ activity timeline
```

Use a Minibase-compatible adapter/contract.

Optional Kanban only if it adds measurable value without scope expansion.

Do not build:
- full CRM;
- auth;
- separate backend;
- separate DB;
- email ingestion service;
- generic workflow engine.

### CP-04 — read-first AI/tool proof

Only after CP-03 passes, test a minimal tool surface:

Read:
- list open deals
- get client context
- list due tasks

At most one controlled write:
- create follow-up task
OR
- change deal stage

The write must be explicit, auditable, ID-preserving, provenance-aware, and bounded to test data.

## Required evidence

Store under:

`experiments/exp-25-atomic-crm-component-extraction/`

Minimum:
- `UPSTREAM_AUDIT.md`
- `COMPONENT_MAP.md`
- `MINIBASE_FIT.md`
- proof fixture/harness if created
- `RESULTS.md`

## Final result

Return:

- RESULT: PASS / PARTIAL / FAIL
- overall adoption: ADOPT_WITH_CHANGES / DO_NOT_ADOPT
- per-component disposition:
  - ADOPT_IN_MINIBASE
  - ADOPT_IN_BUSINESS_DISCOVERY
  - ADOPT_IN_SALAMAT
  - REUSE_UI_ONLY
  - REUSE_PATTERN_ONLY
  - REJECT
- exact components worth reusing
- files changed
- checks run
- blockers/limitations

## Stop conditions

Stop and report before:
- new repo;
- production CRM deployment;
- Supabase introduction;
- live customer migration;
- second source of truth;
- autonomous writes;
- production email ingestion;
- identity-system change;
- deep-change.

STOP after the bounded experiment. No production integration.
