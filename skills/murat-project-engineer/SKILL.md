---
name: murat-project-engineer
description: Coordinate software and project work with Murat AI Stack risk tiers, bounded Expert roles, versioned Playbooks, deterministic Review Gates, typed handoffs, optional independent review, deep-change protection, Opinionated Workspace defaults, and compact run reports. Use for implementing, reviewing, researching, or planning project changes where Codex must select FAST, VERIFIED, or DEEP-CHANGE execution without changing Router authority or creating persistent agents.
---

# Murat Project Engineer

Coordinate the current Codex environment; do not create a second orchestration runtime.

## Execution

1. Read the project context files referenced by `../../../context/project-context.md`.
2. Resolve the project's current Opinionated Workspace defaults from its source-of-truth files and `../../../docs/OPINIONATED_WORKSPACE_POLICY.md`. Prefer existing runtime, deployment, integration, verification, rollback, and cost defaults; do not invent parallel infrastructure because a tool is available.
3. Classify the request as `FAST`, `VERIFIED`, or `DEEP-CHANGE` using `references/risk-and-routing.md`.
4. Select the smallest sufficient Expert or temporary Expert Team from `../../../experts/` and `../../../teams/`.
5. Select a Playbook from `../../../playbooks/`.
6. Resolve a route profile from `references/route-profiles.md` to an explicit configured model slug. Never modify Router internals.
7. Execute the Playbook with explicit handoffs using `../../../contracts/HANDOFF.md`.
8. Run applicable hard deterministic gates from `../../../gates/registry.yaml` before semantic review.
9. Invoke an independent Reviewer only when required. The Reviewer must not edit the candidate in the same invocation.
10. Record any deviation from the resolved Opinionated Workspace default with a concrete reason and expected measurable benefit.
11. Stop at `PASS`, `REWORK`, `BLOCKED`, or `HUMAN_REQUIRED` and complete `../../../contracts/RUN_REPORT.md`.

## Non-negotiable rules

- Prefer one Expert when sufficient.
- Treat Expert as a bounded role contract, never as a persistent process or fixed model.
- Prefer existing project workspace defaults over reopening settled infrastructure choices.
- Never silently add a second hosting platform, storage layer, auth layer, workflow engine, AI gateway, deployment path, or verification path when the current project default satisfies the task.
- Treat absence of a formal workspace profile as a reason to inspect existing project architecture, not as permission to invent infrastructure.
- Record evidence-backed deviations from workspace defaults; apply the deep-change gate when a deviation changes protected architecture, runtime, credentials/security, persistent-agent, memory-governance, or Router-authority boundaries.
- Never let an LLM overrule a failed hard deterministic gate.
- Treat malformed Judge output as `INCONCLUSIVE`.
- Treat budget exhaustion as `BLOCKED`, never `PASS`.
- Never promote session observations into durable project memory automatically.
- Never expose or own provider credentials.
- Never bypass Codex permissions or applicable `AGENTS.md`/`FOUNDATION.md`.
- If the request changes MASTER, Router authority, security, credentials, persistent-agent governance, core plugin boundaries, memory governance, or the central runtime, emit `DEEP_CHANGE_REQUIRES_USER_APPROVAL`, offer a soft-compatible alternative, and stop implementation.

## Software feature flow

Use `../../../playbooks/software-feature.md` for meaningful software changes:

```text
resolve workspace -> classify -> Architect -> HANDOFF -> Coder -> deterministic gates
                  -> optional independent Reviewer -> final gates -> RUN_REPORT
```

Allow one normal rework cycle. Require new user approval for any deep change discovered during execution.

## Validation

From the plugin root run:

```powershell
python scripts/validate_package.py .
python -m unittest discover -s tests -v
```
