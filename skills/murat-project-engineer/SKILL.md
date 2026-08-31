---
name: murat-project-engineer
description: Coordinate software and project work with Murat AI Stack risk tiers, bounded Expert roles, versioned Playbooks, deterministic Review Gates, typed handoffs, optional independent review, deep-change protection, and compact run reports. Use for implementing, reviewing, researching, or planning project changes where Codex must select FAST, VERIFIED, or DEEP-CHANGE execution without changing Router authority or creating persistent agents.
---

# Murat Project Engineer

Coordinate the current Codex environment; do not create a second orchestration runtime.

## Execution

1. For a new substantial idea, apply `../../../docs/NEW_IDEA_FILTER_POLICY.md` and record exactly one disposition.
2. Read the project context files referenced by `../../../context/project-context.md`, then pass Value, Scope, and Deep-change gates from `../../../docs/UNIFIED_EXECUTION_WORKFLOW.md`.
3. Create a Task Packet using `../../../contracts/TASK_PACKET.md`; stop for explicit approval when deep-change or architecture conflict is detected.
4. Pass the Skillization Gate: read any applicable user-named, project, or available skill and record it, or record why none applies.
5. Classify the task as `FAST`, `VERIFIED`, or `DEEP-CHANGE` using `references/risk-and-routing.md`; select the smallest sufficient Expert or temporary Team and a Playbook.
6. Resolve a route profile from `references/route-profiles.md` to an explicit configured model slug. Never modify Router internals.
7. Execute the bounded Task Packet, using typed handoffs from `../../../contracts/HANDOFF.md` for delegates. Keep one writer per worktree unless explicitly isolated and merged by the named owner.
8. Run applicable hard technical gates, then collect `../../../contracts/BROWSER_EVIDENCE.md` where required.
9. Capture and check the Git-complete snapshot with `../../../scripts/verification_state.py`; any change-set, content, status, `HEAD`, or base movement returns `UNVERIFIED` and requires fresh affected evidence.
10. Invoke an independent Reviewer only when required. The Reviewer must not edit the candidate in the same invocation.
11. Run the executable final scope checkpoint against the Task Packet only after capture; complete `../../../contracts/RUN_REPORT.md` with one terminal state only when it returns `VERIFIED`.

## Non-negotiable rules

- Prefer one Expert when sufficient.
- Treat Expert as a bounded role contract, never as a persistent process or fixed model.
- Never let an LLM overrule a failed hard deterministic gate.
- Treat malformed Judge output as `INCONCLUSIVE`.
- Treat budget exhaustion as `BLOCKED`, never `PASS`.
- Never promote session observations into durable project memory automatically.
- Never expose or own provider credentials.
- Never bypass Codex permissions or applicable `AGENTS.md`/`FOUNDATION.md`.
- Do not delegate authority: delegates may only receive a narrowed packet and may not publish, deploy, contact third parties, access credentials, or widen scope without explicit parent authorization and any required human approval.
- A `PASS` is invalid after any post-verification Git snapshot change. The mandatory check returns `UNVERIFIED`; re-run affected checks and Browser Evidence, then repeat the final Git-diff checkpoint.
- If the request changes MASTER, Router authority, security, credentials, persistent-agent governance, core plugin boundaries, memory governance, or the central runtime, emit `DEEP_CHANGE_REQUIRES_USER_APPROVAL`, offer a soft-compatible alternative, and stop implementation.

## Software feature flow

Use `../../../playbooks/software-feature.md` for meaningful software changes:

```text
classify -> Architect -> HANDOFF -> Coder -> deterministic gates
         -> optional independent Reviewer -> final gates -> RUN_REPORT
```

Allow one normal rework cycle. Require new user approval for any deep change discovered during execution.

## Validation

From the plugin root run:

```powershell
python scripts/validate_package.py .
python -m unittest discover -s tests -v
```
