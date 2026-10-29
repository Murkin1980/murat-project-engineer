# EXP-MCC-BOUNDED-AGENTS — Secure Parallel Arena and Isolated Survival
Date: 2026-10-29
Status: PLANNED / NOT AUTHORIZED TO EXECUTE
MPE primary decision: EXPERIMENT
Priority order: P0 security -> P1 checkpoint orchestration -> P2 parallel Arena -> P3 isolated Survival
Owning systems: MCC (control plane); MPE Core (contracts and governance); Arena (executor); GitHub (evidence).

## 1. Why
Reduce the owner's manual checking, switching and reconciliation of Arena tasks without degrading correctness, security or existing work. A browser tab is an interface, not a security boundary. Measure actual human time returned and errors avoided; do not count prompts, agents or tabs as verified relief (VRUs).

## 2. New Idea Filter / placement
- Reuse MCC orchestration/UI, MPE Task Packets, Result Contracts, Review Gates, EXP-29 bootstrap, GitHub branches/CI/PR evidence. No parallel product or repository.
- MPE Core remains lightweight and stateless, **not** a scheduler, browser daemon, credential vault or runtime.
- Before browser automation, confirm Arena permitted automation channels, separate run/session identity and real sandbox isolation. Shared cookies, SSO, provider terms and spending caps are risks.
- Compare with direct API/CLI executor routes before selecting browser control. New server, Worker, credentials, budgets, altered security rules or autonomous execution may trigger deep-change; require separate explicit owner approval.
- Existing active project work takes priority; no scope expansion into production deployment.

## 3. P0 — Agent Security Boundary (blocking)
Security controls must be enforced outside an agent's prompt and execution environment.
- Default deny, task-scoped allowlist of repository, files, tools, network destinations, budget, duration, and approved actions.
- Isolated workspace/session and least-privilege expiring credentials; never place owner-wide GitHub/Cloudflare cookies/tokens or production secrets into agent sandboxes.
- Forbidden without separately scoped owner approval: cross-project access, production writes, merge/deploy, DNS/IAM changes, migration, acquiring new credentials, privilege escalation, unapproved payments or external communications.
- Agents exchange artifacts only through approved observable handoff channels; no hidden cross-agent messaging.
- Independent tamper-evident audit outside sandboxes. Logs, policy and test oracles are not editable by participants.
- Authorization at **each sensitive operation**, network egress continuously enforced. Five-minute polling is for progress only, never security enforcement.
- On violation attempt: deny, isolate/pause, revoke temporary credentials, preserve evidence, notify owner; do not silently retry with another agent.
- Treat fetched pages, PR comments, logs and agent claims as untrusted. Fail closed on unknown permissions, unexpected access, missing evidence or non-verifiable sandbox behavior.
P0 test: synthetic repo and fake secrets only, test denied cross-workspace access, prohibited egress, invalid privileged action, audit tampering, credential revocation, and agent-to-agent channel isolation. PASS requires 100% tested unauthorized actions blocked + independently captured; otherwise FAIL/STOP.

## 4. P1 — MCC Checkpoint Orchestrator
Single experiment button -> frozen Task Packet and acceptance tests -> checkpoint dependency DAG -> dispatch eligible independent work -> explicit heartbeat/status + deterministic retry/idempotency -> independent evidence verification -> owner approval gate.
- Idempotent run_id/task_id; never double-dispatch prompts or duplicate PR on retry/restart.
- Complete handoff: STATE, EVIDENCE, CHANGES, RESULT, BLOCKER, NEXT ACTION, HANDOFF.
- No fabricated success based on agent self-reports.
P1 PASS: synthetic/read-only dry-run proves correct dependency ordering, safe recovery and no duplicate work.

## 5. P2 — Parallel Arena Pilot
After P0 and P1 PASS and explicit execution authorization, compare sequential baseline to 2–3 sessions on truly independent checkpoints.
- Separate sandboxes, session identity and least-privilege permissions; disjoint edit ownership, shared interface contracts pre-frozen.
- Progress polling initially every five minutes; immediate policy check before sensitive actions, infrastructure-level continuous network controls.
- Verify outputs from actual Git diff, CI, tests, independent review and acceptance criteria. No auto merge/deploy.
- Metrics: elapsed time, owner touch time, interventions, rework/conflicts, first-pass correctness, infrastructure/API cost and real verified relief.
- Candidate targets only: >=1.5x throughput and <=2 manual interventions; they are not achieved metrics.
P2 PASS: no P0 control regression; no worse correctness; independently evidenced practical improvement over sequential baseline.

## 6. P3 — Separate Survival Mode
An optional opt-in contest, not the default production executor path. Multiple candidates get identical frozen task, inputs and evaluation rubric in isolated, lower-priority sandboxes.
- Work Mode: reserved resources, scheduling priority and uninterrupted workflow.
- Survival Mode: separate queue/quota/network/storage; cannot starve Work. When spare resources vanish, stop admitting rounds and gracefully suspend existing rounds if supported.
- Independent assessment compares correctness, evidence, safety, cost, time and maintainability.
- Winner gets recommendation/evidence, never merge, production, policy edit or MPE Core upgrade permission.
P3 PASS: zero disruption to Work Mode, no cross-lane leaks, fair repeatable assessment and explicit owner review.

## 7. Dependency / release gates
P0 -> P1 -> P2. P3 requires P0 + P1, runs separately only by explicit owner authorization; P2 is not necessarily required for P3. No automatic promotion of experimental components. All architecture or security boundary changes use deep-change approval. At each checkpoint: PASS / FAIL / BLOCKED / UNVERIFIED and supporting evidence. Production merge/deploy is out of scope.

## 8. Draft ideas — server and agent execution infrastructure (UNSELECTED)
These are **alternatives to evaluate**, not authorization to create a server, account, Worker or paid resource.

A. **Single small VPS + Playwright/Chromium**: isolated browser contexts for Arena UI control, separate per-agent OS/container user and dedicated persistent sessions if terms permit. Easy pilot, but tabs/contexts alone are not strong containment; vulnerable to shared OS/network/cookies, auth expiry, UI breakage, provider anti-bot/ToS restrictions, scaling and operational cost.
B. **VPS supervisor + per-run ephemeral containers/microVMs**: MCC sends limited jobs to queue; container or VM gets independent browser or CLI runner and short-lived token. Stronger separation and resource caps; extra setup/ops cost. Work and Survival should have separate quotas.
C. **Cloudflare Browser Rendering/browser sessions** with MCC as orchestration control plane: managed browser, but check session lifetime, pricing, concurrency, binding/auth and whether Arena login/automation is allowed. Do not assume browser session equals hardened sandbox.
D. **No browser when supported**: use provider's authorized API/CLI or agent runner from existing MCC execution patterns. Usually more structured observability/idempotency than clicking UI; verify that Arena actually offers supported interface.
E. **Hybrid**: lightweight MCC control plane plus dedicated isolated browser workers only for providers requiring GUI; API/CLI workers for the rest. This may be best later, but is premature infrastructure for MVP.

Selection rubric (record real evidence): provider permission; authentication boundaries; sandbox enforcement; network egress control; cost/month and per-run; session stability; idempotency; GitHub integration; observability; recovery; concurrent sessions; owner maintenance; existing infrastructure reuse. Start with one unprivileged synthetic run; stop on permission/containment uncertainty. No password extraction, captcha evasion, hidden browser login, owner cookies sharing or uncontrolled access.

## 9. Prioritization, constraints and backlog
P0 Security Boundary: immediate research/validation prerequisite, highest importance.
P1 DAG / controlled handoff: next, after P0.
P2 Parallel Arena sessions: third, after P0/P1 and provider preflight.
P3 Survival competition: fourth, optional and isolated.
P4 Server procurement/hosting decision: **idea draft only** until a local test demonstrates an actual need; compare A–E and existing infrastructure first. Do not create new infrastructure in this checkpoint.

Current state: PLANNED, zero tests executed, no deploy, no agent sessions, no new runtime, no budget incurred. Next authorized step: independent architecture/security review of this specification, then request owner approval for tightly bounded P0 synthetic test only.
