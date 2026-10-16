# Experiment inventory — post-cleanup reconciliation (2026-10-16)

**Decision:** EXTEND_EXISTING. **Source of truth:** `experiments/EXPERIMENT_REGISTRY.json` in this branch. This is a snapshot/review aid, not a replacement registry.

## Current registered inventory (30)

Status counts: PLANNED 3; PASS 15; HOLD 6; READY_TO_TEST 1; FAIL 1; RETIRED 3; PARTIAL 1.

| ID | Registered status | Experiment |
|---|---|---|
| EXP-ALEXANDRIA | PLANNED | Firecrawl Alexandria source discovery |
| EXP-RANKCONTROL | PLANNED | RankControl AI visibility |
| EXP-002 | PASS | Machine Protocol |
| EXP-07 | PASS | Strix / FreeBuff evaluation |
| EXP-08 | PASS | BrowserAct public-web acquisition |
| EXP-09 | HOLD | Personalized Assessment Engine v0 |
| EXP-10 | HOLD | Munder Difflin controlled pilot |
| EXP-12 | PASS | CLEARS triage backtest |
| EXP-13 | READY_TO_TEST | Low-cost evaluation harness |
| EXP-14 | FAIL | Laya / System One Decision Layer |
| EXP-15 | PASS | MPE Project Memory Layer |
| EXP-S2C-01 | PASS | Screenshot-to-Code Visual Workflow |
| EXP-COMPUTE-BUDGET | HOLD | Compute Budget Gate |
| EXP-QOOPIA-MEMORY | RETIRED | Qoopia cross-session memory |
| EXP-UX-UI-SKILLS | RETIRED | UX/UI Agent Skills |
| EXP-16 | RETIRED | Minimalist Entrepreneur Skills Reuse |
| EXP-STAGE3-SYNTHETIC | HOLD | Synthetic Stakeholder Evaluation |
| EXP-17 | HOLD | PrivetMaket backend recon |
| EXP-18 | PASS | Pirate Face model resilience |
| EXP-19 | PASS | Shir-man trend intake and agent-readable surface |
| EXP-20 | PASS | Dify/OpenHands component extraction |
| EXP-21 | PLANNED | EasyKitchen / SketchUp production backend |
| EXP-22 | HOLD | Colibri local inference / Brio routing |
| EXP-23 | PASS | Papermorph document → interactive artifact |
| EXP-24 | PASS | Agentic text → film pipeline (HyperFrames/Remotion) |
| EXP-25 | PASS | Atomic CRM component extraction |
| EXP-26 | PARTIAL | TencentDB Agent Memory component extraction |
| EXP-27 | PASS | Paperclip orchestration patterns |
| EXP-28 | PASS | Agent workflow skills retrospective (/retro) |
| EXP-29 | PASS | Arena Bootstrap Harness |

## Reconciliation after cleanup

- **Preserved** all 30 existing records, IDs, and past PASS/FAIL/HOLD/RETIRED decisions; no deleted experiments were resurrected.
- **EXP-12:** P-001–P-006 completed (6/10); P-006 EXECUTED/EVALUATED, human–engine–observed VERIFIED/no-approval agreement. Next step is P-007 pre-registration, not rerunning P-006. Canonical evidence: `evidence/exp-12/prospective/P-006_EXECUTION.json` and `P-006_EVALUATION.json`.
- **EXP-29:** corrected *next action* to owner-directed CP-08 and appended the reported 2026-10-16 stale-packet/test evidence. Historical PASS was not silently downgraded, because a later stale artifact does not erase a prior bounded experiment result. Full state repair remains unexecuted; see draft PR #108.
- **Unregistered candidate queue (NOT imported into canonical registry without repository checkpoint/evidence):** WaveSpeed LUT Generator series, OpenMuse, HtmlVR, RustGIS, Barid, REA, Web Scraping MCP connector, and any other October intake items. These are **reconciliation candidates only**, not claimed as approved/implemented experiments; verify their owning project, checkpoint files, duplication and IDs before adding. WaveSpeed may already be tracked in an EXP-29-adjacent task/branch; do not infer a new number.
- **Cleanup/stabilization caution:** an existing file or a prior chat discussion is not proof that a proposed experiment survived cleanup. Do not recreate removed experiment folders or superseded infrastructure just to increase inventory counts.
- **Verification needed:** compare canonical Git history and merged PRs with each registered record before mass status changes. The full test suite reportedly had pre-existing failures; do not claim it is green. In particular, review CP-07/CP-08 Bootstrap source freshness before generating a handoff packet.

## Safe next action

Arena / Codex should audit the current canonical registry and surviving experiment directories; for each October candidate classify `REGISTERED`, `MISSING_AFTER_CLEANUP`, `DUPLICATE`, or `HOLD_NO_EVIDENCE`. Propose minimal corrections in a separate PR. No new repository, service, automatic execution, deployment, or merge. Deep-change requires owner approval.
