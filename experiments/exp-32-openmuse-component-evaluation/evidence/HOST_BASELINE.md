# EXP-32 / CP-01 — Host-project baselines and duplication check

Rule applied: no baseline capability is asserted unless it was read in the current source of
the host repository at a named commit. Everything else is `BASELINE_NOT_VERIFIED`.

Path prefixes in this file: `minibase-cloudflare@9ab38d8` =
`Murkin1980/minibase-cloudflare@9ab38d832970b3956cf0f831f9b578f7b9fd9001`;
`mpe@ca16094` = `Murkin1980/murat-project-engineer@ca16094b373c1b5dccb4988edafe11fcbb525517`;
`OpenMuse@1ac68f3` = `CopilotKit/OpenMuse@1ac68f3909f2478ab6280883f1ab5ea65eb5719d`. In the tables below, an
unprefixed path is relative to the host named by that section: §B1/§B3/§B4/§B5 = `mpe@ca16094`,
§B2 = `minibase-cloudflare@9ab38d8`.

| Host | Pin actually read this session | Access | What was read |
| --- | --- | --- | --- |
| `Murkin1980/murat-project-engineer` (this repo) | `ca16094b373c1b5dccb4988edafe11fcbb525517` (base of the Arena session branch; `main` at fetch time) | yes | `AGENTS.md`, `docs/governance/SCOPE-CHANGE-CONTROL.md`, `docs/NEW_IDEA_FILTER_POLICY.md`, `docs/GLOBAL_MPE_ENFORCEMENT.md`, `docs/OPINIONATED_WORKSPACE_POLICY.md`, `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`, `docs/VALUE_UNIT_ECONOMICS.md`, `docs/architecture/RUNTIME_COORDINATION_PATTERNS.md`, `docs/architecture/MURAT_AI_ORCHESTRATOR_FUTURE_ARCHITECTURE.md`, `docs/evaluations/BROWSER_ACQUISITION_ROLE.md`, `contracts/RUNTIME_EVENT.schema.json`, `contracts/AGENT_RUNTIME_STATE.schema.json`, `contracts/RUN_REPORT.schema.json`, `contracts/HANDOFF.md`, `gates/registry.yaml`, `scripts/task_acceptance.py`, `scripts/runtime_coordination.py`, `experiments/exp-20/25/27` prior results, `wrangler.jsonc`, `package.json`, `dashboard/public/index.html` |
| `Murkin1980/minibase-cloudflare` | `9ab38d832970b3956cf0f831f9b578f7b9fd9001` (2026-09-23T19:34:10Z) — public | yes | `ARCHITECTURE.md`, `src/idempotency.ts`, `src/commands.ts`, `src/provision.ts`, `src/artifact-api.ts`, `src/file-reconciliation.ts`, `migrations/0001_control_plane.sql`, `migrations/0003_provisioning_recovery.sql` (read through the GitHub contents API at that SHA; the repository was **not** cloned into this workspace) |
| `Murkin1980/Murat-AI-Orchestrator` | — | **no** | `gh api repos/Murkin1980/Murat-AI-Orchestrator` → `403 {"message":"Resource not accessible by integration"}`; not in `users/Murkin1980/repos` (38 public repos enumerated). **`BASELINE_NOT_VERIFIED`.** No claim about orchestrator internals is made anywhere in CP-01. |
| `Murkin1980/business-discovery` | — | **no** | same `403`. **`BASELINE_NOT_VERIFIED`.** |
| MPE Control Center | — | **no repository located** | `gh api repos/Murkin1980/mpe-control-center` → `404`; the name appears only as a portfolio convention in `mpe@ca16094:docs/OPERATING_MODEL.md:30`. **`BASELINE_NOT_VERIFIED`** — the only verifiable MPE UI today is the portfolio dashboard in this repo (see below). |

---

## B1 — Verifiable MPE baseline: durable/interactive state today

| Aspect | Verified current state | Citation |
| --- | --- | --- |
| Execution authority | MPE is a bounded coordinator: "does not provide a daemon, scheduler, generic workflow engine, persistent agent runtime, memory service, credentials, MCP server, or Router modification" | `mpe@ca16094:README.md:7` |
| Coordination contract | Ephemeral, file-backed; `RUNTIME_EVENT` vocabulary is `spawn｜handoff｜gate｜terminal｜claim｜block｜resume`; explicitly "**no** broker, socket, poller, retry worker, or daemon"; JSONL is *supporting evidence*, one named writer, rejected if a different writer appends | `mpe@ca16094:docs/architecture/RUNTIME_COORDINATION_PATTERNS.md:23,27`; `mpe@ca16094:contracts/RUNTIME_EVENT.schema.json:13` |
| State vocabulary | `AGENT_RUNTIME_STATE.state` enum is `CREATED｜READY｜WORKING｜BLOCKED｜WAITING｜REVIEWING｜DONE｜FAILED｜CANCELLED` — **no** lease, attempt-count, checkpoint or evidence fields; worktree data is descriptive only | `mpe@ca16094:contracts/AGENT_RUNTIME_STATE.schema.json:12,15-27` |
| Handoff | `contracts/HANDOFF.md` v1 has 14 fields (assumptions, unresolved risks, checks already run, required next checks) — narrative, **no** content hash, **no** expiry, **no** idempotency key | `mpe@ca16094:contracts/HANDOFF.md:3-16` |
| Approval | `enforce_execution(acceptance_result, executor, approval_recorded: bool = False)` — a single boolean gate: `EXECUTE_WITH_APPROVAL` + `approval_recorded=True` → execute | `mpe@ca16094:scripts/task_acceptance.py:123-139` |
| Approval evidence | `RUN_REPORT.approvals` is `array of string` (free text, unvalidated content) | `mpe@ca16094:contracts/RUN_REPORT.schema.json:56` |
| Idempotent append | `deliver_atomic` = validate → exclusive lock (`O_CREAT｜O_EXCL`, mode `0600`) → write+fsync temp → atomic rename; duplicate message ids fail deterministically | `mpe@ca16094:scripts/runtime_coordination.py:82-116` |
| Prior experiment verdict on leases | EXP-27 CP-03 already produced a file-backed single-host lease proof (3 race rounds × 8 processes → exactly 1 winner, 21 explicit `LEASE_CONFLICT`, 0 duplicate executions) | `mpe@ca16094:experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md:51-68` |
| Prior experiment verdict on idempotent evidence | EXP-20 P1 already produced "crash-tolerant, idempotent, resumable event evidence" (`DUPLICATE_REPLAYED` / `DuplicateEventConflict`, duplicate records 1 → 0) | `experiments/exp-20-dify-openhands-component-extraction/RESULTS.md:122-133` (header `:122`, measured row `:133`) |

**Consequence for duplication risk:** OpenMuse's lease + CAS + replay-protection *mechanism
family* is **already covered inside Murat** by EXP-20/EXP-27 at pattern level, and MPE policy
prohibits turning it into a runtime. Any OpenMuse-derived value must therefore be an
*increment over those two results*, not a re-derivation of them.

## B2 — Verifiable MiniBase baseline (candidate storage/host)

| Aspect | Verified current state | Citation |
| --- | --- | --- |
| Scope guardrail | "deliberately **not** a Supabase clone, an ORM, a workflow engine, a queue, or an identity platform. It provides reusable primitives and nothing else." | `minibase-cloudflare@9ab38d8:ARCHITECTURE.md:3-5` |
| Idempotency primitive exists | `parseIdempotencyKey` (≤100 chars) + `fingerprintRequest` (`sha256(JSON.stringify(value))`) + `decideIdempotentReplay → execute｜replay｜conflict`; "MiniBase never trusts the key alone: it always compares fingerprints" | `minibase-cloudflare@9ab38d8:src/idempotency.ts:14,17,32,44-50` |
| Idempotency is already consumed twice | provisioning (`provisioningFingerprint`, conflict → `idempotency_key_reused_with_different_request`) and the single closed CP-05 command (`RECORDS_UPSERT_MANY_COMMAND_TYPE`, "intentionally not a command DSL") | `minibase-cloudflare@9ab38d8:src/provision.ts:19-27,43-50`; `minibase-cloudflare@9ab38d8:src/commands.ts:7-17,281` |
| Recovery state exists as SQL columns | `provisioning_jobs` gained `request_hash`, `d1_database_id`, `rollback_status IN ('not_required','completed','failed')`, `attempt_count > 0` and a remote-id index | `minibase-cloudflare@9ab38d8:migrations/0003_provisioning_recovery.sql:3-9` |
| Atomicity ceiling | `queryProjectD1` posts a single `{sql, params}` per call; multi-record atomicity only via **one** SQLite statement + a static trigger; one HTTPS round trip per query | `minibase-cloudflare@9ab38d8:ARCHITECTURE.md:50-53` |
| Artifact reconciliation exists | `compareFileInventories` / `compareArtifactInventories` (orphaned/missing/size/etag mismatch), immutable originals with exact D1/R2 round-trip accounting | `minibase-cloudflare@9ab38d8:src/file-reconciliation.ts:5-45`; `minibase-cloudflare@9ab38d8:src/artifact-api.ts:1-16` |

**Consequence:** a second idempotency/replay/conflict mechanism would duplicate
`src/idempotency.ts`, and a lease/heartbeat/queue inside MiniBase would violate its own
documented scope line. OpenMuse's durable engine is therefore **not** a MiniBase adoption
target; at most, `attempt_count`-style columns and "one statement + trigger" atomicity are
already the local answer.

## B3 — Verifiable MPE browser role baseline

| Aspect | Verified current state | Citation |
| --- | --- | --- |
| Browser role is policy-only, replaceable, read-only | `Disposition: REUSE_COMPONENT`; flow `raw evidence -> validate -> normalize -> deduplicate`; `Actions: READ, NAVIGATE, EXTRACT`; "Prohibited: private authentication, customer data, write/message/purchase/financial/destructive actions, access-control or CAPTCHA bypass"; conceptual interface only (`BrowserAcquisitionAdapter.acquire`) | `mpe@ca16094:docs/evaluations/BROWSER_ACQUISITION_ROLE.md:3,11,17-19,25-26` |

There is **no persistent browser session, no takeover state, no egress allowlist and no
per-session lock** in the verified Murat material — that whole surface is absent, not weaker.

## B4 — Verifiable MPE UI baseline (approval / rich-surface candidate)

`dashboard/public/index.html` is a single-line static document with **0** `<script>` tags,
**0** `fetch(`, `0` `addEventListener`, `0` `onclick`, and the strings
`approval` / `checkpoint` / `resume` / `browser` do not occur in it (1 verified by counting in
the working tree; 11,082 bytes). `wrangler.jsonc` declares **no Worker script, no bindings, no
secrets** — only static assets (`murat-project-engineer@ca16094:wrangler.jsonc:5-14`).
So today there is no interactive approval or rich-result surface in the verifiable MPE host to
"upgrade", and no rendering path that could accept a streamed/AG-UI message at all.
Any claim that MPE Control Center or Business Discovery already does interactive rendering is
**`BASELINE_NOT_VERIFIED`** (repos unreachable this session), so no such claim is made.

## B5 — Adjacent prior dispositions that constrain this experiment

| Prior finding | Effect on CP-01 ranking |
| --- | --- |
| EXP-20: "OpenHands sandbox/executor boundary → `REJECT` / `DEEP_CHANGE_REQUIRED`" (`mpe@ca16094:experiments/exp-20-dify-openhands-component-extraction/RESULTS.md:82`) and "Dify workflow representation → `REJECT`" for the generic DAG engine (`mpe@ca16094:experiments/exp-20-dify-openhands-component-extraction/RESULTS.md:91`) | Parallel runtime/workflow abstraction is out of bounds for MPE by precedent |
| EXP-20: OpenHands FIFO/resource locks were judged to "overlap" the already-adopted EXP-27 single-host lease (`mpe@ca16094:experiments/exp-20-dify-openhands-component-extraction/RESULTS.md:189`) | Re-admitting a lease pattern needs an explicit increment over both, stated per candidate |
| EXP-27: budget/runaway guard → `ADOPT_IN_MPE`; approval/governance gate → `REJECT` donor mechanism, "keep the existing MPE gate unchanged" (`RESULTS.md:119-122`) | Candidate C must not silently replace `enforce_execution`; it may only *enrich the record that authorizes it* |
| EXP-25: "one object → one identity → many representations" is the binding Minibase fit rule (`mpe@ca16094:experiments/exp-25-atomic-crm-component-extraction/MINIBASE_FIT.md:7`); `docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md` is preferred over a parallel pipeline (`AGENTS.md:113-118`) | Any state/evidence field must extend existing contracts, not create a store |
