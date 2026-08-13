# Murat Project Engineer v1.0

Minimal coordinator plugin for Murat AI Stack Option A+.

> Status: Stage 1 validated. The project is collecting evidence before any Workflow Engine, persistent-agent, or Prime-runtime expansion.

## For developers

- Start with `AGENTS.md` and `CONTRIBUTING.md`.
- Read the decision record in `docs/MURAT_AI_STACK_V2_DECISION.md`.
- Check current scope in `PROJECT_STATUS.md` and `ROADMAP.md`.
- Use feature branches and pull requests; do not push directly to `main`.
- CI runs package validation, contract tests, sample tests and Python compilation.

## Boundaries

This package defines bounded Experts, temporary Expert Teams, human-readable Playbooks, Review Gates, source-of-truth context references, typed handoffs and compact run reports. It does not provide a daemon, scheduler, generic workflow engine, persistent agent runtime, memory service, credentials, MCP server, or Router modification.

## Execution

1. Invoke `$murat-project-engineer` with a project task.
2. Read project source-of-truth files.
3. Classify `FAST`, `VERIFIED`, or `DEEP-CHANGE`.
4. Choose the smallest sufficient Expert or temporary Team.
5. Use the matching Playbook and explicit route profile.
6. Preserve handoffs as observable artifacts.
7. Run hard deterministic gates before optional semantic review.
8. Emit one typed terminal state and complete the Run Report.

## Validation

```powershell
python scripts/validate_package.py .
python -m unittest discover -s tests -v
```

The sample project demonstrates an isolated `software-feature` run with completed handoffs and Run Report.

## Disable or rollback

Stop invoking this plugin and remove its folder. Existing Codex projects, Router configuration, credentials and MASTER remain unchanged. Project changes use the target project's normal Git rollback.
