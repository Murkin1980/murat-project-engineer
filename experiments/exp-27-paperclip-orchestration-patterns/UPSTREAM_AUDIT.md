# EXP-27 CP-01 — Upstream audit: `paperclipai/paperclip`

Status: COMPLETE
Audit date: 2026-10-06 (UTC)
Auditor: Arena (MPE experiment executor)
Decision: **REUSE_COMPONENT** — Paperclip is a donor/reference only.

## 1. Donor identity and pinning

| Field | Value |
|---|---|
| Repository | `https://github.com/paperclipai/paperclip` |
| Default branch | `master` |
| Audited commit (HEAD at audit time) | `d9f600043f13cf19172da1373d1336a0db31664b` (2026-10-06T11:43:16-07:00, "Capture project archive and restore lifecycle events (#15371)") |
| Nearest release tag | `v2026.1005.0` → commit `467125fafb47a8520856504fecc48d6e32055db1` (published 2026-10-06T16:40:49Z) |
| License | MIT (`LICENSE`, blob `a63594a5150d0ae00c3ddc36b61fa8f708c3ca8c`, "Copyright (c) 2025 Paperclip AI") |
| Size signal at audit | ~98.0k stars, 16.6k forks, 4,822 commits, 8,565 tracked files, TypeScript monorepo (`server/`, `ui/`, `packages/`, `cli/`) |

Verification commands (no code was copied into this repository):

```bash
git ls-remote https://github.com/paperclipai/paperclip refs/heads/master
git clone --depth 1 --filter=blob:none --no-checkout https://github.com/paperclipai/paperclip /tmp/pc
git -C /tmp/pc ls-tree -r --name-only HEAD | wc -l     # 8565
git -C /tmp/pc show HEAD:LICENSE
curl -s https://api.github.com/repos/paperclipai/paperclip | grep -E '"license"|"spdx_id"'
```

### Freshness reconciliation (audit vs. release tag)

Every path cited below was hashed at `master` HEAD and at `v2026.1005.0`:

- identical at both: `LICENSE`, `doc/plans/2026-09-21-task-context-ownership.md`,
  `packages/db/src/schema/execution_workspace_runtime_leases.ts`, `packages/db/src/schema/goals.ts`,
  `packages/db/src/schema/issues.ts`, `docs/guides/board-operator/costs-and-budgets.md`,
  `docs/guides/agent-developer/handling-approvals.md`, `docs/guides/agent-developer/heartbeat-protocol.md`,
  `doc/AGENT-ARTIFACTS.md`, `doc/GOAL.md`;
- differs between the two: `server/src/services/budgets.ts` (blob `8938cb4b…` on master vs `e281dcb5…` at the tag;
  the `hard_stop` threshold function cited below is present in both revisions);
- absent at the release tag: `feature-map/*.md` (the feature-map layer is newer than `v2026.1005.0`).

Arena did **not** execute, install, deploy, or dependency-import Paperclip during this audit. All findings are
file-level readings of the pinned revision.

## 2. Mechanism inventory (donor, as read)

### 2.1 Goal / context model

- `packages/db/src/schema/goals.ts` — `goals(id, company_id, title, level, status, parent_id, owner_agent_id)`;
  `level` exists precisely to express a hierarchy (the product description states
  *company → team → agent → task*, `doc/GOAL.md`).
- `packages/db/src/schema/issues.ts` — every issue carries `project_id`, `goal_id`, and self-referencing `parent_id`,
  so a task can always be walked up to its goal/project ancestry.
- `doc/plans/2026-09-21-task-context-ownership.md` — the strongest donor idea found:
  `paperclipTurnContext` v1 records the **owner** of each prompt section and a
  `revision = sha256(trimmed source)` per source (`task_markdown`, `wake_prompt`), plus `objectiveSource`
  on compact continuation. Explicitly: *"A revision is evidence for the exact source body used … it is not an
  authorization token."* Rollback/compat rules keep v5/v3 readers while v4/v2 sessions remain live.

### 2.2 Task ownership / checkout / lease

- `packages/db/src/schema/execution_workspace_runtime_leases.ts` — one durable exclusivity row per execution
  workspace; the comment states the design: *"The unique constraint on execution_workspace_id is the atomicity
  anchor: concurrent claims from different server processes serialize on it instead of on per-process state."*
  Fields: `owner_key` (`issue:<uuid>` | `run:<uuid>`), `owner_issue_id`, `owner_run_id`, `owner_agent_id`,
  `last_action`, `claimed_at`, `renewed_at`, `expires_at`.
- `packages/db/src/schema/issues.ts` — `assignee_agent_id`, `checkout_run_id`, `status_version`,
  `last_status_decision_id` (assignment + checkout ownership on the task row).
- `docs/guides/agent-developer/heartbeat-protocol.md` Step 5 — `POST /api/issues/{id}/checkout` with
  `X-Paperclip-Run-Id`; *"If another agent owns it: 409 Conflict — stop and pick a different task.
  **Never retry a 409.**"*
- `server/src/routes/issues.ts` — stale-ownership adoption event `issue.checkout_lock_adopted` with
  `reason: "stale_checkout_run"`, and `409` for mutations locked by *"another active checkout or run"*.
- `server/src/__tests__/board-claim.test.ts`, `packages/db/src/migrations/0220_execution_workspace_runtime_leases.sql`.

### 2.3 Persistent run history / evidence

- `packages/db/src/schema/heartbeat_runs.ts`, `heartbeat_run_events.ts`, `packages/shared/src/types/artifact.ts`,
  `doc/AGENT-ARTIFACTS.md` — deliverables are registered with `contentRef`, exact `byteSize`, **SHA-256** and a
  stable `idempotencyKey`; the document is explicit that a local workspace path is not evidence for a reviewer.
- The audit trail is event-based (`heartbeat_run_events`), which is what makes resume/watchdog decisions possible.

### 2.4 Budget / runaway controls

- `packages/shared/src/types/budget.ts` — `BudgetPolicy(metric, windowKind, amount, warnPercent,
  hardStopEnabled, notifyEnabled)`, `BudgetPolicySummary(status: "ok" | "warning" | "hard_stop", paused,
  pauseReason)`, `BudgetIncident(thresholdType, amountLimit, amountObserved, approvalId, approvalStatus, resolvedAt)`.
- `server/src/services/budgets.ts` — `budgetStatusFromObserved`: `observedAmount >= amount → "hard_stop"`,
  `>= ceil(amount * warnPercent / 100) → "warning"`; `pauseScopeForBudget` pauses the agent/project/company scope.
- `docs/guides/board-operator/costs-and-budgets.md` — 80% soft alert, 100% hard stop (agent auto-paused,
  no more heartbeats), resume by raising the budget or waiting for the next calendar month.
- `feature-map/budgets-costs.md` — *"Hard stops pause or prevent eligible work until the governing incident is
  resolved"*, *"A successful retry must not bypass an unresolved budget hold"*, and the warning that overlapping
  company/project/agent gates may leave several incidents active.

### 2.5 Approvals / governance

- `docs/guides/agent-developer/handling-approvals.md` — approvals are reserved for governed actions (hires,
  strategy, spend, security-sensitive); ordinary plan sign-off uses `request_confirmation` bound to the latest
  plan revision with an idempotency key and `supersedeOnUserComment`. Resolved approvals wake the agent with
  `PAPERCLIP_APPROVAL_ID` / `PAPERCLIP_APPROVAL_STATUS`.
- `docs/api/approvals.md`, `feature-map/questions-and-approvals.md`, `doc/agent-permission-defaults.md`.

### 2.6 Secondary / reference-only mechanics

- Heartbeat + watchdog: `docs/guides/agent-developer/heartbeat-protocol.md`,
  `packages/db/src/schema/heartbeat_run_watchdog_decisions.ts`, `doc/architecture/durable-continuation-scheduler.md`.
- Routines/schedules: `packages/db/src/schema/routines.ts`, `packages/paperclip-runner/src/protocol-actions/*`.
- Runtime adapters: `doc/GOAL.md` (control plane does not run agents; adapters connect Claude Code / Codex /
  Gemini / OpenCode / Cursor / gateway runtimes), `adapter-plugin.md`, `packages/adapters/**`.
- Org/permissions model: `doc/plans/2026-02-21-humans-and-permissions.md`, `feature-map/app-permissions.md`.

## 3. What Paperclip is, in MPE terms

Paperclip is a **persistent multi-tenant control plane** (Postgres + server + web UI + runner) for fleets of
agents: goals, org chart, issue checkout, heartbeats, budgets, approvals, artifacts, routines. Its value comes
from being the system of record for that fleet.

That is exactly the shape MPE governance forbids here: a second source of truth, a persistent parallel control
plane, and 24/7 agent fleets are non-goals of EXP-27 and deep changes under
`docs/governance/SCOPE-CHANGE-CONTROL.md` §6. The audit therefore evaluated **mechanisms**, not the product.

## 4. Audit conclusion

At least one donor mechanism offers incremental value without requiring a parallel control plane:
**goal ancestry as a compact, revision-hashed context packet**, plus **explicit lease conflict/expiry semantics**,
**evidence records that a fresh executor can consume**, and **hard-stop budget semantics**. Section-by-section
mapping, overlap, incremental value, and required runtime are in `COMPONENT_MAP.md`; the measured bounded proof
is in `RESULTS.md`.

Adoption verdict for the donor as a system: **DO_NOT_ADOPT** (see `RESULTS.md`); adoption verdict for the
individual patterns: **ADOPT_WITH_CHANGES** at pattern level only.

## 5. Audit limitations

- File-level reading of the pinned revision; Paperclip was not executed, so runtime behaviour claims rest on the
  donor's own code, tests, and documentation rather than independent observation.
- The donor moves fast (4,822 commits, 1,766 tags); the pin above is what this experiment audited.
- No Paperclip code, schema, migration, or asset was vendored into this repository; MIT licensing is recorded
  only to document that reuse would be legally possible if a future approved checkpoint decided to reuse a file.
