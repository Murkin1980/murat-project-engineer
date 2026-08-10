---
name: murat-project-engineer
description: Coordinate software and project work with Murat AI Stack risk tiers, bounded Expert roles, versioned Playbooks, deterministic Review Gates, typed handoffs, optional independent review, deep-change protection, and compact run reports. Use for implementing, reviewing, researching, or planning project changes where Codex must select FAST, VERIFIED, or DEEP-CHANGE execution without changing Router authority or creating persistent agents.
---

# Murat Project Engineer

Coordinate the current Codex environment; do not create a second orchestration runtime.

## Execution

1. Read the project context files referenced by `../../../context/project-context.md`.
2. Classify the request as `FAST`, `VERIFIED`, or `DEEP-CHANGE` using `references/risk-and-routing.md`.
3. Select the smallest sufficient Expert or temporary Expert Team from `../../../experts/` and `../../../teams/`.
4. Select a Playbook from `../../../playbooks/`.
5. Resolve a route profile from `references/route-profiles.md` to an explicit configured model slug. Never modify Router internals.
6. Execute the Playbook with explicit handoffs using `../../../contracts/HANDOFF.md`.
7. Run applicable hard deterministic gates from `../../../gates/registry.yaml` before semantic review.
8. Invoke an independent Reviewer only when required. The Reviewer must not edit the candidate in the same invocation.
9. Stop at `PASS`, `REWORK`, `BLOCKED`, or `HUMAN_REQUIRED` and complete `../../../contracts/RUN_REPORT.md`.

## Non-negotiable rules

- Prefer one Expert when sufficient.
- Treat Expert as a bounded role contract, never as a persistent process or fixed model.
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
