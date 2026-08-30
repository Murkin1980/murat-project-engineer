# Murat Project Engineer v1.0

Minimal coordinator plugin for Murat AI Stack Option A+.

## Boundaries

This package defines bounded Experts, temporary Expert Teams, human-readable Playbooks, Review Gates, source-of-truth context references, typed handoffs and compact run reports. It does not provide a daemon, scheduler, generic workflow engine, persistent agent runtime, memory service, credentials, MCP server, or Router modification.

## Execution

1. Apply the New Idea Filter when the request is a new substantial idea.
2. Pass Value / Scope / Deep-change gates and freeze a Task Packet.
3. Pass the Skillization Gate, then classify `FAST`, `VERIFIED`, or `DEEP-CHANGE`.
4. Choose the smallest sufficient Expert or temporary Team and matching Playbook.
5. Execute with bounded handoffs and one writer per worktree.
6. Run hard technical gates, then Browser Evidence where the outcome is browser-observable.
7. Capture verification state; post-verification changes reset it to `UNVERIFIED`.
8. Inspect the final Git diff only after current verification, then emit one typed terminal state and complete the Run Report.

## Validation

```powershell
python scripts/validate_package.py .
python -m unittest discover -s tests -v
```

The sample project demonstrates an isolated `software-feature` run with completed handoffs and Run Report.

## Compute Budget Gate

The deterministic `AI Compute Budget` check is currently **experimental** and may be run as a preflight for substantial execution; it is not a mandatory gate or hard-stop. See `docs/COMPUTE_BUDGET_GATE.md` and `contracts/COMPUTE_BUDGET.md`. `scripts/compute_budget.py` is the single source of truth for the preflight estimate, budget health (GREEN/YELLOW/ORANGE/RED/UNOBSERVED), burn-rate anomaly, and evidence-based reforecast. `observed` / `estimated` / `unobserved` usage are distinct; missing usage renders `UNOBSERVED`, never fake zeros.

## Deterministic triage experiment

EXP-12 adds a bounded, stateless triage prototype and a 20-case retrospective backtest. See `docs/experiments/EXP-12_CLEARS_TRIAGE.md`. It recommends a risk tier and human gate from explicit structured inputs; it does not execute, approve or route work autonomously.

Prospective cases use immutable REGISTERED, EXECUTED and EVALUATED evidence with hashes. P-001–P-003 are complete; P-003 is the first product case. Progress is 3/10.

## Portfolio dashboard

Live project status map: https://murat-project-engineer.muriktl.workers.dev

## Disable or rollback

Stop invoking this plugin and remove its folder. Existing Codex projects, Router configuration, credentials and MASTER remain unchanged. Project changes use the target project's normal Git rollback.
