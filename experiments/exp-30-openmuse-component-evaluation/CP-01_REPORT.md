# EXP-30 / CP-01 — OpenMuse upstream audit and reuse map — REPORT

| Field | Value |
| --- | --- |
| Experiment / checkpoint | EXP-30 `openmuse-component-evaluation` / **CP-01 only** |
| Checkpoint outcome | **PASS** — read-only investigation; documentation output only |
| Run date | 2026-10-16 UTC (session start 2026-10-15 UTC) |
| Repository / branch | `Murkin1980/murat-project-engineer`, Arena session branch `arena/9196ade0-murat-project-engineer` (base `ca16094b373c1b5dccb4988edafe11fcbb525517`) |
| Owner-approved disposition under execution | `REUSE_COMPONENT` |
| Candidate audited | `CopilotKit/OpenMuse`, pinned at **`1ac68f3909f2478ab6280883f1ab5ea65eb5719d`** (`main`, 2026-10-06T22:39:29Z) |
| Method | `git clone --depth 1` (source only) outside the workspace + GitHub/npm API reads. No install, build, test, execution, deployment or upstream write |
| Authoritative instruction | `experiments/exp-30-openmuse-component-evaluation/CP-01.md` — exists on open draft **PR #104** (head `c4bbe94`, that file's blob `5160e5447a115c7c26091db339e27d22bb26c492`), **not merged to `main`**; its rules are restated in §2 rather than duplicated or edited |
| CP-02 / CP-03 / CP-04 / CP-05 | **NOT_AUTHORIZED** — proposals only, §7 |

**Citation convention.** Bare `path:line` references (`apps/…`, `packages/…`, `tests/…`,
`docs/…`, `README.md`, `SECURITY.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `render.yaml`,
`infra/compose.yaml`, `.github/workflows/ci.yml`) point at
`CopilotKit/OpenMuse@1ac68f3909f2478ab6280883f1ab5ea65eb5719d`. Murat references are always
prefixed with `repo@sha:` (e.g. `murat-project-engineer@ca16094:AGENTS.md`,
`minibase-cloudflare@9ab38d8:src/idempotency.ts`). Full citation forms are in
`evidence/SOURCE_EVIDENCE.md` and `evidence/HOST_BASELINE.md`.

---

## 1. Answer, before detail

OpenMuse at this pin is a **personal-agent application**, not a component library: one
always-on Node process, one generic JSONB table, a lease-polling task engine, a private
Playwright sidecar, an Expo client, and a startup that **refuses to run** without a hosted
CopilotKit Intelligence key (`apps/server/src/config.ts:152` + `apps/server/src/app.ts:35`).
Read from source rather than from its marketing, three mechanisms are genuinely real, tested and
worth Murat's attention:

1. **Fenced durable task execution** — CAS lease claim + lease-renewal heartbeat that
   **aborts the in-process run** the moment the fence is lost, plus a persisted per-operation
   memo so a resumed run replays results instead of re-firing side effects
   (`apps/server/src/engine/worker.ts:126-190`, `apps/server/src/engine/model.ts:34-46,77-88`).
2. **Uncertain-write quarantine** — an external write whose outcome is unknown is recorded as
   `outcome_unknown`, retry is refused until a human reconciles, and a cancelled task
   auto-denies its pending review; the rule is also enforced in SQL, not in UI
   (`apps/server/src/db.ts:116-133`, `apps/server/src/engine/service.ts:278-286,317-321`).
3. **Content-hash-bound, expiring, single-consumption approval** — the approval must present the
   SHA-256 of exactly what was reviewed (payload + account + target version) and is consumed by
   one atomic claim (`apps/server/src/actions.ts:39-207`).

Everything else that looks reusable is either (i) already owned by Murat at pattern level
(EXP-27 lease + expiry, EXP-20 idempotent append, MiniBase `decideIdempotentReplay` →
`execute` / `replay` / `conflict`), or (ii) a runtime/platform adoption that trips the deep-change gate
(Postgres/PGlite, persistent Chromium profiles, Docker/E2B computer, CopilotKit runtime +
telemetry default-on, Expo UI).

Verdict: **PASS** for CP-01; upstream-as-a-system **DO_NOT_ADOPT**; three narrow pattern probes
pre-registered (§7). No VRU is claimed — nothing here is implemented relief
(`murat-project-engineer@ca16094:docs/VALUE_UNIT_ECONOMICS.md`).

---

## 2. Governance and boundary compliance

Every path in this section (reading order and both tables) is local to this repository,
i.e. `murat-project-engineer@ca16094:…` — the citation convention above would otherwise read
bare paths as OpenMuse.

Read before any audit action, in this order: `murat-project-engineer@ca16094:docs/governance/SCOPE-CHANGE-CONTROL.md`;
`murat-project-engineer@ca16094:AGENTS.md`; `docs/NEW_IDEA_FILTER_POLICY.md`; `docs/GLOBAL_MPE_ENFORCEMENT.md`;
`murat-project-engineer@ca16094:docs/OPINIONATED_WORKSPACE_POLICY.md`; `docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md`;
`murat-project-engineer@ca16094:docs/VALUE_UNIT_ECONOMICS.md`; PR #104's `README.md` + `CHECKPOINTS.md` + `CP-01.md`; and the
verifiable host material listed in `evidence/HOST_BASELINE.md`.

Applied constraints, and how each was honoured:

| Rule | Honour in CP-01 |
| --- | --- |
| Checkpoint is the boundary (`SCOPE-CHANGE-CONTROL.md` §3) | only CP-01 executed; CP-02–CP-05 marked NOT_AUTHORIZED (§7) |
| Changes allowed in this experiment directory only | 5 new files, all under `experiments/exp-30-openmuse-component-evaluation/` (§9); registry, `README.md`, `CHECKPOINTS.md`, `CP-01.md` untouched |
| Do not duplicate PR #104 | verified #104 is unmerged (`git merge-base --is-ancestor FETCH_HEAD main` → false), so no registration file was re-created or edited |
| Analysis task → do not modify code (`SCOPE-CHANGE-CONTROL.md` §15) | zero code changes; upstream never built or run |
| No cloning/importing OpenMuse dependencies | no `pnpm install`, no `node_modules` (verified absent), only the source tree |
| No credential, cookie, API key, paid call, live account, deployment | none used; only public GitHub/npm/registry reads |
| License compatibility asserted only from read text | root `LICENSE` read (MIT, `Copyright (c) 2026 OpenMuse contributors`); per-package `license` fields checked on the npm registry for every direct dependency; transitive closure explicitly **not** audited |
| Deep-change gate (§6) | 6 boundaries identified and **stopped at**, not crossed (§6.5) |
| Host baseline honesty | every host claim carries `repo@SHA:path[:line]`; unreachable hosts are labelled `BASELINE_NOT_VERIFIED` |
| "Do not reveal private context to external services" (`murat-project-engineer@ca16094:context/CONTEXT_MAP.md:44`) | nothing from Murat repos was sent anywhere; only public upstream reads |

---

## 3. Verified upstream facts (pin, license, activity, toolchain)

Full table with commands: `evidence/UPSTREAM_PINS.md`.

| Fact | Verified value |
| --- | --- |
| Pin | `1ac68f3909f2478ab6280883f1ab5ea65eb5719d`; agreed by local `git rev-parse HEAD`, `gh api repos/CopilotKit/OpenMuse/branches/main`, and `git ls-remote` for `HEAD` + `refs/heads/main` |
| Commit date / subject | 2026-10-06T22:39:29Z · `perf(server): scope refreshIdeas status queries (#109)` |
| Tags / releases | **none** (`git tag` empty; API `tags` and `releases` both empty) → the SHA is the only possible pin |
| Declared version | `0.1.0`, `"private": true` (`package.json:3-4`); `CHANGELOG.md:3` "0.1.0-alpha — 2026-09-15" |
| License | **MIT**, root `LICENSE` only (sha256 `399a9cccf1b228c9…`, 21 lines); no `NOTICE`; sub-packages declare no own license |
| Not covered by that license | CopilotKit **Intelligence** service: "a separate service and is not included in this repository's MIT license" (`README.md:194`; `docs/RICH-THREADS.md:30`) |
| Activity | created 2026-09-15; 125 commits on `main`; 27 contributors (top 39/15/11 commits); 30 branches; 11 open issues + 41 open PRs; 5,075 stars / 704 forks; last push 2026-10-14 |
| CI | 1 workflow, 5 jobs (`quality`, `platform`, `browser`, `browser-container`, `computer-container`); last `main` push run **success** (2026-10-06T22:39:33Z); two recent `renovate/*` PR runs **failure** |
| Languages | TypeScript 1,380,481 B · Python 4,799 · JavaScript 3,089 · Dockerfile 834 (GitHub linguist) |
| Size | non-test TS/TSX: 99 files / **22,807** lines; tests: 60 files / 14,465 lines; 413 `test(` declarations in `tests/` (+32 mobile, +4 worker, +2 computer) |
| Package managers | `pnpm@11.19.0` at the root (workspace = `apps/mobile`, `apps/worker`; patched `metro@0.83.3`; `image-size` override) **and** an independent npm lockfile inside `apps/worker` (used by its Docker build) |
| Node | `engines.node: ">=22"` (`package.json:9`) vs README/CI/CONTRIBUTING "Node 24 LTS" → **documented mismatch** |
| Dependency graph | 18 runtime + 7 dev root deps; 22 runtime deps in `apps/mobile`; 1 (`playwright@1.62.1`) in `apps/worker`; `pnpm-lock.yaml` 14,137 lines |
| Direct-dependency licenses (verified on the pinned versions) | MIT: `@ag-ui/core`/`client` 0.0.59, `@copilotkit/runtime`/`react-native`/`aimock` 1.70.1/1.70.1/1.42.0, `hono`, `@hono/node-server`, `zod`, `pg`, `pdf-lib`, `parse5`, `@tanstack/ai*`, `@modelcontextprotocol/sdk`, `@e2b/desktop`, `@typesafe-ai/sdk`, `expo`; Apache-2.0: `@electric-sql/pglite`, `playwright`, `rxjs`, `typescript`, `@google/genai`; `@biomejs/biome` = `MIT OR Apache-2.0`. **No copyleft in this audited set**; transitive tree not walked |
| App / platform targets | Hono API on `@hono/node-server`; optional separate task worker (needs `DATABASE_URL`); Playwright/Chromium sidecar (Docker or local); optional nonroot Docker Linux computer **or** E2B desktop VM; Expo iOS/Android/web; Render Blueprint (`render.yaml`) |
| Cloudflare surface | **none** — case-insensitive greps over `*.ts/.tsx/.md/.json/.yaml/Dockerfile` (lockfile excluded) return **0** matches for `cloudflare`, `wrangler`, `\bD1\b`, `durable object`, `workers.dev` and `\bR2\b`; the only hits in an unanchored `d1` search are `thread1` identifiers in test fixtures |
| Telemetry | on by default: `process.env.COPILOTKIT_TELEMETRY_SAMPLE_RATE ??= "1"` (`apps/server/src/config.ts:28`), PostHog sink (`README.md:196-198`); upstream's own tests must disable it (`tests/setup.ts:2-4`) |
| Doc drift found | `docs/VERIFICATION.md:7` claims "154 tests pass" (dated 2026-09-16) against 445 `test(` declarations in the `pnpm test` scope at this pin |

**Marked unverified:** any claim about CopilotKit Intelligence pricing/limits, Parallel search
quotas, E2B behaviour, and everything in `OpenMuse@1ac68f3:docs/VERIFICATION.md`'s manual-acceptance rows
(device recordings) — none of it is checkable from source.

---

## 4. Capability audit — implemented / partial / stub / advertised

Full citation matrix (all `repo@SHA:path:line`) in `evidence/SOURCE_EVIDENCE.md`. Compact form:

| Required area | Status at the pin | Key evidence |
| --- | --- | --- |
| Browser lifecycle, manual takeover | **Implemented.** Per-session serial lane; ownership row persisted *before* the side-effect; thread→session association reserved before the call; 15 s health cache (worker answering ≠ worker ready); reopen with the same UUID after failure; profile restore + best-effort cookie persist on close; 3 active sessions / 20 profiles / 30-min idle | `apps/server/src/browser.ts:64-72,128-140,194-207`; `apps/worker/src/browser.ts:140-158,163-172,292-297` |
| Non-injectable read surface | **Implemented.** Read evaluation is fixed inside the worker ("callers cannot inject JavaScript"), 100 k visible-text cap with an explicit `truncated` flag; takeover input is a closed 4-verb vocabulary with bounded coordinates/key names; popups closed, dialogs dismissed | `apps/worker/src/browser.ts:307-331,333-368,237-242` |
| Takeover console | **Implemented**, deliberately dumb: a screenshot-only document (no remote page code), scaled click mapping, visibility-aware 2 s polling, retained text after a failure, `stale` class blocks input when disconnected | `apps/server/src/browser-console.ts:1-38` |
| Egress policy | **Implemented.** Public-unicast allowlist incl. IPv6 range tests; **all** DNS answers must be public; the proxy connects to the validated IP (no second resolution → DNS-rebind defence); CONNECT limited to :443; loopback-only worker host | `apps/worker/src/network.ts:8-41,46-95`; `apps/worker/src/proxy.ts:13,58-66`; `apps/worker/README.md:62` |
| Task state / checkpoints / restart | **Implemented.** 9-state enum; CAS claim with `leaseId`/`leaseUntil` (60 s) + `attempts++`; `guard()` before every effect; `checkpoint()` CAS that throws `LostLeaseError` if preempted; heartbeat renews the lease and **aborts** on a lost CAS; expired-lease reclaim = crash recovery; 3 in-flight cap; pending reviews don't starve the queue | `packages/domain/src/agent.ts:3-21`; `apps/server/src/engine/worker.ts:76-121,126-190,212-236` |
| Idempotence | **Implemented** at three layers: `id = sha256("task:"+key)` + `insertIfAbsent`; persisted tool-result memo `sha256(name+JSON(args))`; deterministic UUIDv5-shaped file id from `(owner, operationKey)` | `apps/server/src/engine/service.ts:192-196`; `apps/server/src/engine/model.ts:77-88`; `apps/server/src/files.ts:28-40` |
| Retry / backoff / alert storm control | **Implemented for watches only**: `min(60, 2**failures)` minutes, pause after 5 failures, streak-scoped notice keys, notification dedupe by hashed key + `insertIfAbsent`. A failed open-ended `agent` task is **not** auto-retried — a human must | `apps/server/src/engine/service.ts:826-870,719-729` |
| Uncertain external writes | **Implemented.** On boot, `executing` → `outcome_unknown` with a reconciliation instruction; `retry` is refused (409) while the linked action isn't `succeeded`; cancel auto-denies the pending proposal; `README.md:188` states the rule | `apps/server/src/db.ts:129-133`; `apps/server/src/engine/service.ts:278-286,317-321`; `apps/server/src/index.ts:9` |
| Agent-tool permissions | **Implemented** server-side, not model-side: model has **no** approve tool; writes go through a persisted, versioned proposal | `apps/server/src/engine/model.ts:331`; `apps/server/src/actions.ts:39-100` |
| Approval integrity | **Implemented.** `hash = sha256({input, connection, target, targetVersion})` must be presented to decide; 30-min expiry CAS; account/connection-change invalidation; single consumption in one `UPDATE … WHERE data->>'status'='awaiting_review' AND expiresAt>now AND task-liveness EXISTS` | `apps/server/src/actions.ts:77-88,112-149`; `apps/server/src/db.ts:116-127` |
| Model / provider config | **Implemented** narrowly: `MODEL=provider/model` for OpenAI/Anthropic/Google, gateway `OPENAI_BASE_URL` + Chat-Completions opt-in, `MODEL_MAX_RETRIES = 2` with per-provider retry semantics documented, and an explicit note that external writes never re-fire inside the model loop | `apps/server/src/engine/tanstack-agent.ts:18-64`; `apps/server/src/config.ts:96-104` |
| Persistence boundary | **Implemented.** One table `records(owner,kind,id,data jsonb,updated_at)`; concurrency = JSONB containment CAS; PGlite (single process) or pg; files in `DATA_DIR` 0700; browser profiles in the worker volume | `apps/server/src/db.ts:69-83,160-180` |
| Auth / secrets | **Implemented.** Shared access key (constant-time compare), opaque 24-h session tokens, HMAC 15-min signed URLs, AES-256-GCM versioned envelope for Google tokens, signing key written `0600` with a `wx`+`link` race-safe publish | `apps/server/src/auth.ts:14-67,68-90`; `packages/integrations/src/vault.ts:10-38` |
| Tests | **Implemented and adversarial.** ~451 test declarations; fault-injection helpers that force a lost CAS mid-write; restart/recovery, double-claim, cancellation-before-effect, stale-hash approval, DNS/private-destination rejection, container lifecycle | `tests/engine.test.ts:30,46,70`; `tests/monitor-recovery.test.ts:26-43` (20 tests); `tests/actions.test.ts:69,107,250,289`; `tests/browser.test.ts:488,541,670` |
| AG-UI rich interactive messages | **Implemented** as hand-emitted AG-UI events (`RUN_STARTED`/`TEXT_MESSAGE_*`/`TOOL_CALL_*`) whose `delegate_task` result carries the persisted task id; grounded `present_choices` panel refuses options whose label/detail/source title is not a **verbatim** excerpt of the page text read in that turn; candidate-set version + optimistic reserve CAS make a superseded panel non-actionable; `textOnlyToolResult` strips image parts before persistence so history never replays binaries | `apps/server/src/engine/conversation.ts:86-133`; `apps/server/src/jev/tools.ts:44-93`; `apps/server/src/jev/service.ts:55-88,291-330`; `apps/server/src/engine/tanstack-agent.ts:170-192` |
| Same area, **partial** | two message-shape fixes are version-pinned workarounds for `@copilotkit/runtime` 1.70.1 (self-labelled "ponytail: … remove this when …"), and the SSE body needs a string→bytes shim → coupling risk, not reusable code | `apps/server/src/engine/tanstack-agent.ts:220-241`; `apps/server/src/app.ts:337-349` |
| CopilotKit Rich Threads | **Stub-to-partial for us**: implemented, but every mode requires the hosted Intelligence key; CI runs against mocked boundaries | `apps/server/src/config.ts:152`; `docs/VERIFICATION.md:40`; `SECURITY.md:35` |
| OpenBot backend | **Stub.** Adapter is contract-tested against a pinned upstream ref and returns `{state:"disabled"}` unless enabled; server reports `openbotConfigured: false` | `packages/backends/src/openbot.ts:4,140`; `apps/server/src/workspace.ts:357,366` |
| AI-Mock demo model, `sample://` pages | **Stub by design** — scripted fixtures, explicitly labelled as not live-model reasoning | `apps/server/src/demo/model.ts:1-20`; `docs/DEMO.md` |
| Autonomous booking/checkout, graphical desktops, device push, OCR, multi-tenant auth, per-person VMs | **Advertised only** (roadmap) | `docs/FEATURES.md:5-21`; `ROADMAP.md:16-31` |
| E2B desktop provider | **Implemented but self-declared unsafe**: all VM ports publicly reachable, 8-char VNC password, unreviewed egress, passwordless sudo in-VM | `SECURITY.md:29` |

---

## 5. Capability and duplicate map vs existing Murat hosts

Legend for dispositions: `REUSE_PATTERN_ONLY` (adopt the idea/vocabulary, no code),
`KEEP_EXISTING` (Murat already covers it), `REJECT` (duplicate or conflicting),
`BASELINE_NOT_VERIFIED` (host unreadable this session — no claim made).

| # | OpenMuse part | Verified Murat baseline | Increment OpenMuse actually adds | Disposition |
| --- | --- | --- | --- | --- |
| 1 | Lease + CAS task claim (reclaim on expiry) | EXP-27 CP-03 already produced a working single-host lease proof: 3 rounds × 8 processes, 1 winner, 21 `LEASE_CONFLICT`, 0 duplicate executions (`murat-project-engineer@ca16094:experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md:51-68`) | only the **in-flight** half: heartbeat renewal + abort on lost CAS, and `guard()` before each effect (EXP-27 has expiry/reclaim but no mid-run fencing) | `REUSE_PATTERN_ONLY` for the fencing half; the lease itself `KEEP_EXISTING` |
| 2 | Idempotent append / replay / conflict | MiniBase `minibase-cloudflare@9ab38d8:src/idempotency.ts:44-50` `decideIdempotentReplay → execute｜replay｜conflict`, "never trusts the key alone: always compares fingerprints"; EXP-20 P1 proved duplicate-replay rejection in `murat-project-engineer@ca16094:scripts/runtime_coordination.py` | deterministic **id-as-hash-of-key** record identity (`apps/server/src/engine/service.ts:194`) and UUIDv5-shaped derived file ids (`apps/server/src/files.ts:31-40`) | `KEEP_EXISTING` + small `REUSE_PATTERN_ONLY` (derived-ID idea) |
| 3 | Uncertain-write quarantine (`outcome_unknown`) + retry refusal | MPE has an *evidence-trust* gate and a "no fabricated PASS" rule (`murat-project-engineer@ca16094:scripts/earned_autonomy.py:3-6`, `scripts/execution_runner.py:24-29` header) but no named *uncertain-effect* state in `murat-project-engineer@ca16094:contracts/RUNTIME_EVENT.schema.json` / `murat-project-engineer@ca16094:contracts/AGENT_RUNTIME_STATE.schema.json` | a fourth terminal-ish outcome distinct from FAIL, persisted, that blocks retry until reconciled | `REUSE_PATTERN_ONLY` — candidate C |
| 4 | Content-hash-bound, expiring, single-consumption approval | MPE approval today is a boolean: `enforce_execution(..., approval_recorded: bool)` (`murat-project-engineer@ca16094:scripts/task_acceptance.py:123-139`); `RUN_REPORT.approvals` is `array of string` (`murat-project-engineer@ca16094:contracts/RUN_REPORT.schema.json:56`); `murat-project-engineer@ca16094:gates/registry.yaml:80-86` has `deep_change_check` with `HUMAN_REQUIRED` | approval bound to *what was shown* (content hash), with expiry and one-shot consumption; also deny-on-cancel | `REUSE_PATTERN_ONLY` — candidate B; **not** an MPE gate replacement (EXP-27 already ruled "keep the existing MPE gate unchanged", `murat-project-engineer@ca16094:experiments/exp-27…/RESULTS.md:122`) |
| 5 | Durable task engine as a service (poller + DB) | `murat-project-engineer@ca16094:README.md:7` and `murat-project-engineer@ca16094:docs/architecture/RUNTIME_COORDINATION_PATTERNS.md:23,35` explicitly exclude scheduler/heartbeat/poller/daemon/queue; `murat-project-engineer@ca16094:STATUS.md:135` deep-change rule | nothing usable — adopting it *is* the forbidden parallel runtime | `REJECT` |
| 6 | JSONB/PGlite persistence layer | MiniBase is the portfolio's storage primitive and is "deliberately not a … workflow engine, a queue" (`minibase-cloudflare@9ab38d8:ARCHITECTURE.md:3-5`), with one D1 statement per round trip (`minibase-cloudflare@9ab38d8:ARCHITECTURE.md:50-53`) | nothing; a second store = second source of truth | `REJECT` |
| 7 | Persistent Chromium browser worker + profiles + takeover | `murat-project-engineer@ca16094:docs/evaluations/BROWSER_ACQUISITION_ROLE.md` defines a **conceptual, read-only, public-only** adapter: actions `READ/NAVIGATE/EXTRACT`; "Private authentication, customer data, write/message/purchase" prohibited; "no product runtime may depend on it without a new approved experiment" | the *policy* around such a worker (public-unicast allowlist with DNS-pinning, 4-verb input, screenshot-only console, session-recorded-before-call) — the worker itself is new infrastructure | worker `REJECT`; **hardening policy → `REUSE_PATTERN_ONLY`** — candidate A |
| 8 | Grounded option panels + optimistic candidate-set versioning | No verifiable implementation in MPE (`murat-project-engineer@ca16094:dashboard/public/index.html`: 11 kB, **0** `<script>`, 0 `fetch`/listener); business-discovery and Control Center → `BASELINE_NOT_VERIFIED` (403/404) | verbatim-source grounding rule + version-fencing of a human pick | `REUSE_PATTERN_ONLY` with `BASELINE_NOT_VERIFIED` explicitly attached |
| 9 | AG-UI / CopilotKit runtime, Expo UI, telemetry | MPE owns no agent runtime; Router owns provider credentials; dashboard is static assets with no Worker script (`murat-project-engineer@ca16094:wrangler.jsonc:5-8`) | nothing | `REJECT` (new runtime, new vendor service, new credential) |
| 10 | Docker/E2B Linux computer, Gmail/Calendar/PDF/finance connectors, Ideas/Goals/Monitors product surfaces | out of EXP-30's stated scope; would be parallel products | — | `REJECT` for this experiment (HOLD-worthy only as product ideas) |

Integration surface / build-runtime requirements / license constraint / security change /
estimated effort / rollback difficulty, per surviving candidate:

| Candidate | Integration surface | Build/runtime requirement | License constraint | Security change required | Adaptation effort (range) | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| **A — bounded takeover + egress policy for public-web acquisition** | `murat-project-engineer@ca16094:docs/evaluations/BROWSER_ACQUISITION_ROLE.md` policy text + adapter contract (`acquire(task)`), optionally a `murat-project-engineer@ca16094:gates/registry.yaml` deterministic check | none to adopt the *rules*; the rules are already implemented in this repo's Python/CI style (no Node, no Playwright) | none (policy text; if any `isPublicIp` code is transcribed → MIT attribution required) | **strengthening**: destination allowlist, DNS-answer-all check, IP pinning, closed input vocabulary, read caps | 0.5–1.5 dev-days (spec + one Python fixture table) | trivial: delete/revert the doc hunk; no runtime |
| **B — content-bound, expiring, single-consume approval record** | a new `APPROVAL_RECORD` contract shape next to `murat-project-engineer@ca16094:contracts/RUN_REPORT.schema.json`; `enforce_execution` keeps its boolean decision | pure Python, stdlib only | none (concept; no code copied) | adds replay/stale/expired refusal; no new authority | 1–3 dev-days for contract + validator + tests | revert the contract + helper; no data migration |
| **C — uncertain-effect outcome state (`OUTCOME_UNKNOWN`) + reconcile-before-retry** | `murat-project-engineer@ca16094:contracts/RUNTIME_EVENT.schema.json` / `murat-project-engineer@ca16094:contracts/RUN_REPORT.schema.json` vocabulary + `murat-project-engineer@ca16094:scripts/execution_runner.py:24-29` status handling | pure Python, deterministic | none | prevents duplicate side effects; no new permission | 0.5–2 dev-days | revert vocabulary addition; additive, no migration |

Deep-change scan for the three survivors: none introduces a repository, hosting platform,
storage engine, credential, source-of-truth change or irreversible action. Each touches a
**contract file** (`murat-project-engineer@ca16094:contracts/**`, `docs/evaluations/**`, `murat-project-engineer@ca16094:gates/registry.yaml`), which under
`murat-project-engineer@ca16094:docs/governance/SCOPE-CHANGE-CONTROL.md` §6 is a public-contract change → each requires explicit owner
approval at its own checkpoint, even though the change is small.

---

## 6. Security, licensing, cost, Cloudflare/workspace fit

### 6.1 Security — what is genuinely good, and what must not be copied

Adoptable *as policy* (evidence in `evidence/SOURCE_EVIDENCE.md` §1, §7): destination
allowlist that rejects any non-public DNS answer; connecting to the already-validated IP
instead of resolving twice; a closed 4-verb input vocabulary with bounded coordinates; a
read path where the caller cannot inject a selector or script; recording ownership *before*
the side-effect; single-consumption claims in SQL; a hash-bound, expiring approval;
`outcome_unknown` instead of blind retry; notice-keyed notifications to prevent alert storms;
rate-limit key derived from the socket rather than from caller-supplied credentials; a
screenshot-only console that never executes remote page code; sample mode pinned to loopback.

Must **not** be inherited: shared single-owner access key as an auth model (`SECURITY.md:9`);
Playwright's disabled Chromium sandbox treated as "good enough" (`SECURITY.md:13`); the E2B
desktop provider with publicly reachable VM ports and an 8-char VNC password (`SECURITY.md:29`);
default-on PostHog telemetry (`apps/server/src/config.ts:26-28`) — which alone would violate
`murat-project-engineer@ca16094:context/CONTEXT_MAP.md:44` if ever run inside Murat; a required third-party
search call that forwards conversation content (`README.md:154-160`).

### 6.2 Licensing

MIT, single root `LICENSE`, no `NOTICE` file, no per-package license fields, no contributor
license agreement (`CONTRIBUTING.md:54` "Contributions are accepted under the MIT license").
Practical consequences: patterns/vocabulary need no attribution; **copying** a file or a
substantial portion does (copyright + permission notice must be kept), so any future adoption
must ship a `NOTICE`-style attribution block. Apache-2.0 direct deps (`pglite`, `playwright`,
`rxjs`, `@google/genai`, `typescript`) would carry their own NOTICE obligations if vendored —
they will not be. CopilotKit's **Intelligence service is outside the license**, so any
"reuse" that needs it is really a vendor/service decision, not an OSS one. Nothing in Murat is
re-licensed by any of this.

### 6.3 Cost

CP-01: $0 (read-only clone + public API reads; no model calls). Any *runtime* adoption would
create standing cost: a ≥1 GB always-on host (512 MB OOM-kills before the port binds,
`render.yaml:5-6`), a browser worker container, a CopilotKit Intelligence project, and optional
Parallel search + model provider keys. All three surviving candidates are documentation +
stdlib-Python scale (≈0 marginal cost), consistent with the compute-budget posture used by
EXP-20/EXP-27 (`murat-project-engineer@ca16094:docs/COMPUTE_BUDGET_GATE.md`).

### 6.4 Cloudflare / opinionated-workspace fit

| Aspect | Murat default (verified) | OpenMuse requirement | Fit |
| --- | --- | --- | --- |
| Runtime | MPE = static assets on Workers (`murat-project-engineer@ca16094:wrangler.jsonc:5-8`, no Worker script, no bindings, no secrets); MiniBase = Workers + D1 + R2 | long-lived Node ≥22 process with `setInterval` polling ×4 (`apps/server/src/engine/worker.ts:50,174`; `apps/server/src/engine/service.ts:75`; `apps/worker/src/browser.ts:292`) | **incompatible** → REJECT as runtime; patterns are runtime-free |
| Storage | D1/R2 via MiniBase, one statement per round trip | PGlite/WASM Postgres or Postgres with `jsonb` containment CAS | **incompatible** (D1/SQLite has no `@>`; one statement per call) |
| Persistence authority | project stores stay the source of truth | app-local `.openmuse` directory, wiping the disk wipes data | would create a second source of truth → REJECT |
| Secrets | Router/owner-managed; no new credential | mandatory `CPK_INTELLIGENCE_API_KEY` + optional provider/Google/E2B keys | violates "no new credential" → REJECT |
| Auth | project-owned | shared access key, single owner | REJECT |
| Verification | deterministic scripts + CI + gates | 451 `node:test` cases (good practice to imitate, not to import) | pattern-only reuse |

### 6.5 DEEP-CHANGE boundaries flagged (stop points, not actions)

1. Deploying/using OpenMuse as a runtime → new persistent agent runtime + new hosting platform.
2. Introducing Postgres/PGlite (or any second store) → source-of-truth change.
3. Persistent browser cluster / logged-in profiles → new infrastructure + credential custody.
4. Docker or E2B "computer" → new execution authority boundary.
5. CopilotKit runtime/Intelligence → new vendor dependency, telemetry, and credential.
6. Editing `murat-project-engineer@ca16094:contracts/**` or `murat-project-engineer@ca16094:gates/registry.yaml` in production → public-contract change
   (flagged for each candidate in §5, requires explicit approval at that checkpoint).

---

## 7. Ranked follow-up probes (max 3) — pre-registered only, **NOT_AUTHORIZED**

Each probe below is written so that its numbers can be produced by a single experiment-local
harness with no credentials, no network and no new dependency. `CP-02` (browser handoff),
`CP-03` (durable recovery) and `CP-04` (AG-UI rendering) as scoped in `CHECKPOINTS.md` stay
unassigned until the owner authorizes them; probe P-1..P-3 map onto them but are **not** a grant.

| Rank | Probe | Maps to | Pre-registered hypothesis | Reproducible inputs | Baseline metric | Success threshold | Failure / stop |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **P-1** | Bounded public-web acquisition policy: closed input vocabulary + destination allowlist + record-before-call, expressed as rules for the existing `BrowserAcquisitionAdapter` role | CP-02 (re-scoped to policy, **no live browser**) | Stating these five rules removes the two unsafe gaps in today's role doc (`murat-project-engineer@ca16094:docs/evaluations/BROWSER_ACQUISITION_ROLE.md`) (unbounded caller-supplied selectors/scripts; no destination/DNS policy) with zero runtime change | the current `murat-project-engineer@ca16094:docs/evaluations/BROWSER_ACQUISITION_ROLE.md` (30 lines) + OpenMuse `apps/worker/src/network.ts:8-95`, `apps/worker/src/browser.ts:307-368`, `apps/server/src/browser.ts:64-72,128-140`; 12 adversarial URL fixtures (loopback, 169.254, CGNAT, IPv6 ULA, `*.local`, decimal-encoded IP, redirect-to-private, port 8080, credential URL, oversized text, script-injection selector, concurrent read) | role doc today blocks 0/12 (no policy stated; only an action list) | 12/12 classified correctly (8 blocked, 4 allowed), every rule traceable to an upstream `path:line`, doc diff ≤ +25 lines, no new file outside the experiment | any rule that requires a persistent browser, a proxy, or credentials → STOP + `DEEP_CHANGE_REQUIRED` |
| **P-2** | Approval record bound to content hash + expiry + single consumption + reconcile-before-retry (candidates B and C together) | new bounded probe (CP-03 sibling) | A pure `approval_id = sha256(payload‖account‖targetVersion‖run_id)` record with `expires_at` and one-shot claim removes replay/expiry/mismatch acceptance while leaving `enforce_execution` semantics intact | deterministic Python fixture set of 6 cases (approve-once, approve-twice, approve-after-mutation, approve-after-expiry, account-switch invalidation, cancel-denies-pending) run against a copy of the acceptance path | today's boolean path accepts 2 unsafe cases (replay and mutated-content) — `murat-project-engineer@ca16094:scripts/task_acceptance.py:123-139`, `contracts/RUN_REPORT.schema.json:56` | 6/6 verdicts correct, executor invoked exactly once for the whole suite, 0 new dependencies, `git diff --stat` limited to `experiments/**` | any proposal to replace `enforce_execution` or to move approval into a service → STOP (EXP-27 already rejected donor approval machinery, `murat-project-engineer@ca16094:experiments/exp-27…/RESULTS.md:122`) |
| **P-3** | Grounded-option validation + optimistic candidate-set versioning for derived interactive artifacts (source-excerpt requirement + stale-version refusal) | CP-04 (rendering-free half) | Requiring every displayed option label/detail to be a verbatim excerpt of the stored source text, and refusing a selection whose `candidateSetVersion` ≠ head, removes unsourced options and stale double-selection with no UI framework | `murat-project-engineer@ca16094:docs/REUSABLE_DERIVED_ARTIFACT_PATTERN.md` contract + EXP-23 artifact fixture; 8 cases (3 ungrounded, 2 exact-excerpt, 1 case-only change, 2 stale-version clicks) | EXP-23 measured 0 factual errors **by manual review** with 2 manual corrections (`murat-project-engineer@ca16094:experiments/exp-23-papermorph-interactive-artifact/FINDINGS.md:18-22`) — no automated grounding check exists | 3/3 ungrounded rejected, 2/2 stale clicks refused, 1/1 case-insensitive match accepted (normalization is explicit), 0 new deps, ≤150 lines in `harness/` | any need to import AG-UI/CopilotKit rendering, or to run a model → STOP; baseline of the real host stays labelled `BASELINE_NOT_VERIFIED` |

Pre-registration discipline: thresholds are fixed before execution; a probe that cannot produce
its numbers without a credential, a service or a new runtime **fails by construction** and must
be recorded as such rather than softened. All three inherit the no-new-credential constraint
from CP-01 and are `$0`-cost.

---

## 8. Limitations and unknowns (explicit)

1. **Two host baselines are unreadable here.** `Murkin1980/Murat-AI-Orchestrator` and
   `Murkin1980/business-discovery` → `403 Resource not accessible by integration`;
   no `mpe-control-center` repository (404). Every statement about them is
   `BASELINE_NOT_VERIFIED`; the experiment README's assumptions about orchestrator
   ("browser session ownership, resumable task execution, AG-UI interoperability") were **not**
   confirmed against code and are not treated as baselines.
2. **No execution evidence.** Nothing from OpenMuse was installed, built, or run (CP-01
   forbids it), so behaviour claims rest on source + upstream tests + upstream CI, not on
   observed runtime.
3. **Dependency audit is depth-1.** Direct packages and their registry `license` fields were
   verified; the 14,137-line lockfile's transitive closure and each package's own NOTICE/CLA
   text were not.
4. **Doc/code drift is real and unresolved.** "154 tests" vs 445 declarations;
   `engines.node >=22` vs "Node 24 LTS"; root pnpm vs a second npm lockfile. Cited, not fixed
   (not ours to fix).
5. **No released version exists** → everything here is valid for `1ac68f3…` only; a later
   checkpoint must re-pin and re-verify §4 rows before reuse.
6. **This repo's own suite is not green at the base commit** — 432 tests, 27 failures, 1 skip,
   all pre-existing and unrelated to EXP-30: 19 in `test_dashboard_registry_views`
   (16 rendered-text + 3 mobile-view), 4 in `test_contracts` (the `RETIRED` registry status of
   `EXP-QOOPIA-MEMORY`, `EXP-UX-UI-SKILLS`, `EXP-16`, `EXP-26` is outside the contract's
   allowed set), 2 in `test_registry_to_reladraw`, 2 in `test_exp29_bootstrap`. The result is
   identical before and after CP-01 (`evidence/READ_ONLY_LOG.md` §6). CP-01 neither caused nor attempted to fix them: repairing
   them means touching `experiments/EXPERIMENT_REGISTRY.json`, `tests/test_contracts.py`'s
   allowed-status set and the committed views — all outside this checkpoint's authorized files
   (and the registry half belongs to PR #104).

---

## 9. Changes, checks, and the handoff block

**STATE** — `CP-01_COMPLETE / OUTCOME: PASS`; CP-02–CP-05 `NOT_AUTHORIZED`. Read-only
checkpoint finished on the Arena session branch, delivered as a reviewable PR (no merge, no
deploy, no production change).

**EVIDENCE** — `evidence/UPSTREAM_PINS.md` (pin, license, activity, toolchain, dependency-license
checks, commands); `evidence/SOURCE_EVIDENCE.md` (~60 `OpenMuse@1ac68f3:path:line` citations with
implemented/partial/stub/advertised classification); `evidence/HOST_BASELINE.md` (verified MPE +
MiniBase baselines with `repo@SHA:path` citations and the `403`/`404` non-access records);
`evidence/READ_ONLY_LOG.md` (exact commands, digests, the "nothing installed/executed/written
elsewhere" attestation, repo test-suite baseline before and after).

**CHANGES** — new files only, all inside the experiment directory: `CP-01_REPORT.md`,
`evidence/UPSTREAM_PINS.md`, `evidence/SOURCE_EVIDENCE.md`, `evidence/HOST_BASELINE.md`,
`evidence/READ_ONLY_LOG.md`. Nothing else in the repository was touched: PR #104's registration
files, `experiments/EXPERIMENT_REGISTRY.json` and the committed `dashboard/public/registry/**`
views were deliberately left alone (no registry change → no Reladraw regeneration required).

**RESULT** — **PASS** by CP-01's own criteria: reproducible upstream evidence at a pinned SHA, a
genuine host comparison where the host was readable, clearly labelled unknowns where it was not,
and 3 evaluable pre-registered probes with fixed thresholds. Component dispositions:
A `REUSE_PATTERN_ONLY`, B `REUSE_PATTERN_ONLY`, C `REUSE_PATTERN_ONLY`, plus 8 explicit
`KEEP_EXISTING`/`REJECT` rows; **`DO_NOT_ADOPT` for OpenMuse as a system, runtime, store,
auth model, browser cluster or UI framework**. Adoption-as-code was rejected on evidence, not on
preference: §5/§6.4. No Verified Relief Unit is claimed — this checkpoint produced analysis,
and rule 10 of `murat-project-engineer@ca16094:AGENTS.md` forbids calling that relief.

**BLOCKER** — none for CP-01. Two access blockers constrain *later* comparisons: orchestrator and
business-discovery are `403`-inaccessible and Control Center has no repository, so their
baselines are unverifiable in this session; any candidate whose value depends on them (P-3's host
side, and any orchestrator-resumability claim) must first be given an accessible baseline commit.
Six deep-change boundaries (§6.5) are flagged as stop-points requiring explicit owner approval.

**NEXT ACTION** — owner: review PR #104 (registration + registry entry) and this CP-01 PR
separately; decide whether to assign **P-1** (cheapest, zero new capability, documentation +
one deterministic table) and/or **P-2** (contract-level, small, measurable) as a new bounded
checkpoint with its own instruction file. Do **not** treat §7 as authorization.

**HANDOFF** — everything needed to resume without rediscovery is in this directory: the pin is
`1ac68f3909f2478ab6280883f1ab5ea65eb5719d` (with file digests in `evidence/READ_ONLY_LOG.md`),
the method and commands are recorded there, the verified/unverified boundary is set in
`evidence/HOST_BASELINE.md`, and each surviving candidate already carries its integration
surface, effort range, rollback path and pre-registered probe thresholds (§5, §7). A fresh
session should read: `murat-project-engineer@ca16094:docs/governance/SCOPE-CHANGE-CONTROL.md` → PR #104's `CP-01.md` → this
report → the candidate's row in §5 and §7 → `evidence/SOURCE_EVIDENCE.md` for the exact code
lines. If the pin moves, re-run §3/§4 verification before reusing any conclusion.
