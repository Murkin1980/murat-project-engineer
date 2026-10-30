# Murat Project Engineer — Status

Updated: 2026-10-16 (core stabilization against main ca16094; EXP-12 prospective progress reconciled to 6/10; EXP-23/24/25/26/27/28/29 outcomes reflected; queued experiment-ID collisions must be renumbered before merge)

## CP-09 Recovery — verified merge (2026-10-30)

- **PR #115: MERGED** into `main`; approved head `34827c9dfc2e17e8454114f1d339c902e54f7c00`, merge commit `57a38b6277c155707aa6d935a54aac0196226ddb`.
- Acceptance before merge: full unittest 448 passed, 0 failed, 1 skipped; contract 12 OK; EXP-29 focused 47 OK; Dashboard/Reladraw 15 OK; package validator PASS; `npm run check` 52/52; EXP-29 proof PASS; EXP-29 and EXP-23 packets FRESH. These are pre-merge acceptance results, not a post-merge test rerun.
- GitHub post-merge verification: PR marked merged/closed and `main` was identical to merge commit at read-back.
- Schema: owner-approved additive `PARTIAL`/`RETIRED` statuses only. No production deploy authorized or performed in this task.
- **Next:** Harness² PR #113 / CP-SI-01 audit/design may be prepared after confirming canonical baseline and its separate gates. No agent self-modification execution, automatic merge or deploy authorized.
- Portfolio dashboard full-source synchronization remains **PENDING / NOT VERIFIED**; no claim of deployment or all-repository refresh.

## Current version

- Release: v1.0
- Stage 1: COMPLETE
- Stage 2: ACTIVE — 20-run evidence experiment
- Stage 2A: FIRST-FIVE EVIDENCE CAPTURED
- Runs 07–13: EVIDENCE CAPTURED — five PASS, one REWORK, one BLOCKED
- Portfolio dashboard: LIVE at https://murat-project-engineer.muriktl.workers.dev — deployed snapshot is 12.08.2026 (older design), stale relative to the 07.09.2026 snapshot on main. CI deploy steps are skipped on recent pushes because `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` are not configured in the repository; a successful workflow run is therefore not proof that the site was updated.

## Current architecture

Murat Project Engineer remains a bounded coordinator and policy layer for Murat AI Stack Option A+.

Implemented and available:

- coordinator skill
- bounded Expert roles: Architect, Coder, Reviewer, Researcher
- temporary Expert Teams
- FAST, VERIFIED, DEEP-CHANGE and Software Feature playbooks
- deterministic Review Gates
- typed handoffs
- compact Markdown Run Reports
- machine-readable Run Report schema/example
- Markdown Experiment Record template
- machine-readable Experiment Record schema/example
- progressive context map
- context-provider architecture documentation
- mandatory New Idea Filter Policy
- operating-model documentation connecting portfolio filtering to risk-tiered execution
- package validator and tests
- isolated software-feature PoC
- Stage 2 evidence for Runs 01–13
- bounded runtime-coordination contracts and stateless helpers from Run 11
- EXP-002 Machine Protocol (CLOSED, verdict PASS): external models correctly understood the frozen MPE IR (cross-model semantic portability supported); confirmed cross-executor execution is NOT demonstrated (INCONCLUSIVE — no real tool/repository access; self-reported execution claims remain UNVERIFIED). The evidence-trust boundary rule is promoted into `scripts/validate_package.py`
- EXP-12 deterministic triage prototype, contracts, retrospective backtest, and prospective cases P-001–P-006
- EXP-13 low-cost evaluation harness + pre-execution rework (frozen dataset v2, routes A/B/premium, thresholds, pricing snapshot, checks, and Pilot Batch 1 pre-registration). Telemetry state: usage evidence adapters exist in main for all routes (`scripts/usage_from_router_log.py` for A/B isolated metered Router windows; `scripts/usage_from_codex_rollout.py` for one explicit premium Codex turn with a complete per-call breakdown, fail-closed otherwise); no Pilot Batch 1 runs have been executed yet
- EXP-14 Laya / System One Decision Layer — **EXECUTED, CLOSED, verdict FAIL** (checkpoint `EXP-14-CP-01`, run 2026-09-30 → 2026-10-01, evidence `experiments/exp-14-laya/2026-09-30/`, pointer `experiments/exp-14-laya-system-one/EXECUTION_RECORD.md`). Frozen 43-case dataset (sha256 `aef7d8bf…3803b648`) + rule-derived oracle validated against 25 pre-existing frozen labels before any model call. Sequence A deterministic control: exact 0.8605, blocking safety gate PASS, routine coverage 12/12, 0.0095 ms median, $0.0. Sequence B Laya zero-shot (`laya==0.3.22`, `convaiinnovations/laya` @ `55cf4c4e…`, CPU, 3 reproducible passes): exact **7/43 = 0.1628**, routine coverage **0/12**, 0 protected false negatives and 0 unsafe FAST decisions but **5 protected escalation false negatives → blocking safety gate FAIL**, 3367.8 ms median → `B_MODEL_RESULT = FAIL`, `B_SAFETY_RESULT = FAIL`, classification `MODEL_FAIL`. Reference arm B2 (vendor fine-tuned `typed-decisions`, attempt 1 `INFRASTRUCTURE_BLOCKED` by a harness pin defect fixed minimally in `2acd481d`): exact 5/43 = 0.1163, routine coverage 1/12, gate PASS but 23 gate false positives → `B2_RESULT = FAIL`. `CONFIDENCE_SIGNAL = NOT_USEFUL` (`risk_tier` confidence AUC 0.5263 / 0.4878; best threshold cut is the trivial one, coverage 0.0 / 0.0833), so **calibration NOT_RUN / NOT_JUSTIFIED** and **fine-tuning NOT_RUN** (forbidden at this checkpoint). `PASS_FOR_NEXT_EXPERIMENT = NO`; `integration_authorized` remains false; 36/36 production and governing files digest-identical to `d2ec6453`; the temporary branch-scoped CI workflow used to reach the pinned checkpoint was deleted at close.
- EXP-23 Papermorph — PASS / REUSE_COMPONENT: reuse mark-based narration↔visual sync and quiz-data patterns; do not adopt the Papermorph engine
- EXP-24 agentic text→film pipeline — PASS / REUSE_COMPONENT: reuse the source→beats/work-units→marks/cues/timings→asset-slots→QA→minimal-diff revision contract; do not require HyperFrames or Papermorph
- EXP-25 Atomic CRM extraction — PASS / ADOPT_WITH_CHANGES at pattern level only; no parallel CRM or second source of truth
- EXP-26 TencentDB memory extraction — PARTIAL / ADOPT_WITH_CHANGES at pattern level only; no memory platform, database, vector store, autonomous write, or production integration
- EXP-27 Paperclip orchestration patterns — PASS / ADOPT_WITH_CHANGES at pattern level only; bounded ancestry, lease/resume, budget, and approval patterns only; no Paperclip control plane
- EXP-28 workflow retrospective — PASS / ADOPT_WITH_CHANGES as a manual evidence-gated pattern; no automatic post-run trigger
- EXP-29 Arena Bootstrap Harness — PASS / REUSE_COMPONENT: deterministic Git-derived bootstrap packets for context-heavy Arena tasks; Git remains canonical and packets must verify FRESH
- EXP-S2C-01 UI reconstruction feedback loop — PASS / REUSE_COMPONENT: 1 initial render + up to 3 targeted correction cycles with early stop
- portfolio dashboard (read-only static asset, Workers Static Assets, auto-deploy on configured main push)

## Stage 2 run status

- Run 01 — Murat Project Engineer documentation/status hygiene — FAST baseline — PASS
- Run 02 — Furniture Configurator parametric/UI/pricing feature — VERIFIED baseline — PASS
- Run 03 — MebelDocs AI order→invoice→PDF vertical slice — VERIFIED baseline — PASS
- Run 04 — MebelLegal unified order workflow/domain-boundary change — DEEP-CHANGE baseline — PASS
- Run 05 — Murat Project Engineer Stage 2A resume/evidence readiness — VERIFIED coordinator — BLOCKED
- Run 06 — Murat Project Engineer operating-model/status synchronization — FAST coordinator — PASS
- Run 07 — Strix/FreeBuff controlled evaluation — VERIFIED coordinator — PASS (evaluation completed; Strix NOT_EXECUTED/HOLD)
- Run 08 — BrowserAct public-web acquisition evaluation — VERIFIED coordinator — PASS
- Run 09 — Personalized Assessment Engine v0 — VERIFIED coordinator — REWORK
- Run 10 — Munder Difflin controlled pilot — VERIFIED coordinator — BLOCKED
- Run 11 — bounded runtime-coordination patterns — VERIFIED coordinator — PASS
- Run 12 — CLEARS deterministic triage/executability backtest — VERIFIED coordinator — PASS (retrospective mechanics only)
- Run 13 — MPE navigation-test fix and status synchronization (this stabilization) — FAST coordinator — PASS

Run 05 remains historically BLOCKED because repository-local package validator and unit tests were not executable through the GitHub connector execution surface during that run. No PASS is retroactively claimed.

Run 06 is a separate FAST documentation/policy synchronization run. It does not replace or rewrite Run 05.

Run 07 PASS applies only to completion of the controlled evaluation. Strix execution is NOT_EXECUTED and its decision remains HOLD. FreeBuff execution is REJECT; selected Codebuff patterns are REUSE_COMPONENT.

Run 09 remains REWORK until its unresolved production-rule, external-LLM, Git-boundary, and source-of-truth findings are addressed. Run 10 remains historically BLOCKED. Run 11 remains inside Option A+ only while its mailbox, JSONL, and lifecycle elements stay bounded, stateless, conditional helpers rather than runtime authority.

Run 12 PASS validates deterministic execution and retrospective fixture consistency. Prospective P-001–P-006 are complete. P-003 is the first external product case (`mebeldocs-ai@987c13e`), P-004 is the first FAST dashboard UI case, P-005 covers Murat House editorial work, and P-006 covers dashboard reconciliation. All six completed prospective cases preserve human/engine/observed agreement. Progress is 6/10, still insufficient for operational reliance.

## New Idea Filter

`docs/NEW_IDEA_FILTER_POLICY.md` is ACTIVE and MANDATORY.

Every new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea must be evaluated through Murat Project Engineer before implementation starts.

The primary disposition must be one of:

- `EXTEND_EXISTING`
- `REUSE_COMPONENT`
- `MERGE`
- `EXPERIMENT`
- `HOLD`
- `NEW_REPOSITORY`
- `REJECT`

`NEW_REPOSITORY` is the exception, not the default.

See `docs/OPERATING_MODEL.md` for how portfolio filtering connects to the existing FAST / VERIFIED / DEEP-CHANGE execution model.

## Boundaries still in force

Not part of the current implementation:

- daemon or scheduler
- generic workflow engine / DAG runtime
- persistent runtime agents
- independent memory service
- automatic memory promotion
- adaptive routing
- Router task/workflow orchestration
- Prime Agent runtime integration
- mandatory Docsalot dependency
- mandatory Context.dev dependency
- Workspace UI implementation

Codex remains the execution/orchestration environment. Codex Router remains the inference/protocol/credential gateway.

## Current objective

Continue the Stage 2 experiment defined in `STAGE2_EXPERIMENT_PLAN.md` toward 20 representative runs.

The experiment must measure quality, rework, reviewer value, interruption recovery, overhead, and genuine architecture pressure before any expansion is proposed.

## Next actions

**Nearest single action (as of 2026-10-29):** EXP-29 is closed at PASS / REUSE_COMPONENT (CP-08 accepted via PR #111, canonical closure at CP-09); continue fresh real Stage 2 / EXP-12 prospective cases. Do not run EXP-13 Pilot Batch 1 until credential, egress, and telemetry preconditions are genuinely satisfied.

1. Preserve the historical Run 05 and Run 10 BLOCKED outcomes; do not retroactively promote them.
2. Keep Run 09 in REWORK until the recorded findings are resolved or explicitly scoped out.
3. Continue Runs 14–20 with fresh real work; EXP-12 prospective progress is 6/10, so pre-register P-007 only when its real task is selected and reach 10/10 before operational reliance.
4. Ensure the 20-run set contains at least five baseline runs total; Runs 01–04 currently provide four historical baselines.
5. Use independent Reviewer on enough VERIFIED runs to measure reviewer usefulness and false positives.
6. Keep Run 11 helpers conditional and bounded. A poller, daemon, retry worker, router, scheduler, shared state, database, or generic messaging/runtime layer requires a new filter and DEEP-CHANGE review.
7. Add selected deterministic gates to GitHub CI only through a separate bounded change.
8. Maintain the portfolio dashboard snapshot as part of the weekly status ritual. Before merging any queued experiment registration, ensure its experiment ID is unique in canonical `experiments/EXPERIMENT_REGISTRY.json`; do not merge competing identities under the same EXP number.
9. EXP-13 Pilot Batch 1 has fail-closed usage paths for all routes: `scripts/usage_from_router_log.py` imports isolated metered A/B Router windows, while `scripts/usage_from_codex_rollout.py` can import one explicit premium Codex turn only when its rollout contains a complete token breakdown. Native Router events and opaque-total rollout events remain unusable; do not substitute synthetic telemetry. The three T-008 routes legally stop without usage. Run the 18-entry batch only after each proceeding run has a valid source record, then STOP and analyse.
10. EXP-14 checkpoint `EXP-14-CP-01` is closed with `RESULT = FAIL` and `PASS_FOR_NEXT_EXPERIMENT = NO`: Laya zero-shot closed 0 of 12 routine cases and tripped the blocking safety gate on 5 protected escalation false negatives, and the vendor fine-tuned reference arm closed 1 of 12. Do not integrate Laya and do not grant it any decision authority. Do not fine-tune on the 43-case evaluation dataset; any continuation needs a new pre-registration with a new, separately frozen dataset whose splits do not overlap those cases (`experiments/exp-14-laya/2026-09-30/FINE_TUNING.md`). Any proposal to integrate a learned System One model into the production decision path still requires a separate New Idea Filter decision and applicable DEEP-CHANGE approval. The cheapest improvement this checkpoint identified is not a model: the deterministic engine under-tiers five DEEP-CHANGE cases (credentials/security, destructive-without-rollback, source-of-truth changes) that MPE rule text already covers — fixing that in `scripts/triage_engine.py` is a production decision-path change and requires its own filter decision and, if it touches protected routing boundaries, DEEP-CHANGE approval.

## Evidence-format finding

Stage 2A showed that retrospective baselines need a distinction between zero and unknown. Machine-readable experiment metrics therefore keep required fields but permit `null` where a historical value is not observable.

This is evidence portability only; no database or workflow runtime was added.

## Deep-change rule

Any proposal to add a workflow runtime, persistence layer for orchestration state, persistent agents, autonomous memory promotion, Router authority changes, adaptive routing, Prime runtime integration, or core architecture redesign is a deep change and requires explicit approval before implementation.
