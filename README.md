# Murat Project Engineer v1.0

Minimal coordinator plugin for Murat AI Stack Option A+.

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

## Deterministic triage experiment

EXP-12 adds a bounded, stateless triage prototype and a 20-case retrospective backtest. See `docs/experiments/EXP-12_CLEARS_TRIAGE.md`. It recommends a risk tier and human gate from explicit structured inputs; it does not execute, approve or route work autonomously.

## Portfolio dashboard

Live project status map: https://murat-project-engineer.muriktl.workers.dev

## Disable or rollback

Stop invoking this plugin and remove its folder. Existing Codex projects, Router configuration, credentials and MASTER remain unchanged. Project changes use the target project's normal Git rollback.
