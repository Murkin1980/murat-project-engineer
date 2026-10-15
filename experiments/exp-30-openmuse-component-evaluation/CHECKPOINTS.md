# EXP-30 — Checkpoint plan
Status: PLANNED | 2026-10-16
Primary disposition: REUSE_COMPONENT
Owning repository: Murkin1980/murat-project-engineer
Source of truth: this file + CP-01.md + MPE governance. Later checkpoints are proposals, not authority to execute.

## Gates
CP-01 → CP-02/03/04 (only if evidence justifies) → CP-05. No automatic transition; owner authorizes each execution checkpoint. Stop on DEEP-CHANGE. No production integrations, new repository, new infrastructure, new provider spending, live credentials, or external account actions.

| Checkpoint | Title | Scope and evidence | Exit |
| --- | --- | --- | --- |
| CP-01 | Upstream audit and reuse map | Pin exact upstream SHA; inspect license, maintenance, browser lifecycle, state/resume, AG-UI, packages, security model. Compare existing projects using verifiable citations to specific files/commits. Document capability matrix, risks, candidate rankings, no running new services. | PASS when factual report, evidence links and 1–3 prioritized reusable candidates exist; PARTIAL if source cannot be verified; BLOCKED if required access missing. |
| CP-02 | Browser handoff isolated probe | If CP-01 supports it: local/synthetic test of observe/pause/manual takeover/session recovery in an isolated test page, comparing baseline. No real account/session, credentials, or remote persistent browser. | PASS if explicit human control and isolation demonstrable with repeatable steps; otherwise PARTIAL/FAIL. |
| CP-03 | Durable task recovery isolated probe | Test one cancellable/restartable synthetic multi-step workflow. Compare replay, checkpoint integrity, idempotence, recovery time and failure reporting with orchestrator baseline. | PASS only with logs proving safe bounded recovery, no duplicate side effects. |
| CP-04 | AG-UI / Rich Messages probe | Render one synthetic interactive result using existing UI/tool patterns where possible; test approval boundary, mobile usability, keyboard access and safe untrusted content. No new UI framework by default. | PASS only with usable rendering and no weakened authorization or XSS trust boundary. |
| CP-05 | Adoption decision and closure | Compare CP-02–04 evidence (or blockers), maintenance/licensing, cost, architecture fit and rollback; classify each component ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT. Recommend owning existing project and minimal next action. | CLOSED only with traceable evidence and explicit no-deep-change declaration or owner approval request. |

## Value test and prioritization
Prioritize measurable reduction of manual tool switching, recovery after interruptions and completion of interactive tasks. Record before/after steps, recovery correctness and integration effort; do not invent verified value. The project currently prefers strengthening murat-ai-orchestrator, MPE Control Center, business-discovery and existing minibase-cloudflare patterns instead of a parallel platform.

## General acceptance
Each checkpoint yields STATE / EVIDENCE / CHANGES / RESULT / BLOCKER / NEXT ACTION / HANDOFF, pinned versions, exact commands/test outputs where relevant, and minimal diffs. No checkpoint expands another checkpoint's scope. Only CP-01 is ready to assign; all others are conditional.
