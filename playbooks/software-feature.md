---
playbook_id: software-feature
version: 1.1.0
supported_task_classes: [software-feature, bug-fix, bounded-refactor]
risk_tier: VERIFIED
roles: [architect, coder, reviewer-when-required]
sequence: [research-source-of-truth, produce-task-packet, architect-to-coder-handoff, execute-smallest-change, deterministic-gates, coder-to-reviewer-handoff, independent-semantic-review, rework-at-most-once, final-gates, run-report]
required_inputs: [task, repository_path, project_context, acceptance_criteria]
deterministic_gates: [deep_change_check, clean_diff_scope, secrets_scan, build, typecheck, lint, unit_tests, integration_tests, acceptance_tests, rollback_available]
optional_semantic_review: true
human_gate_conditions: [deep_change_detected, irreversible_external_effect, judge_human_required]
max_rework_cycles: 1
terminal_states: [PASS, REWORK, BLOCKED, HUMAN_REQUIRED]
run_report_fields: contracts/RUN_REPORT.md
---

## Substantial Implementation Flow: Research → Execute → Review

For all substantial implementation tasks, follow these six canonical stages:

1. **Research source-of-truth and constraints:** Read active project context (`AGENTS.md`, `FOUNDATION.md`, `DESIGN.md`, `STATUS.md`), identify dependencies, and check Opinionated Workspace defaults.
2. **Produce a bounded implementation plan / Task Packet:** Architect defines objective, affected components, explicit constraints, acceptance criteria, likely files, tests, rollback procedure, and deep-change assessment.
3. **Execute the smallest sufficient change:** Coder implements the minimal necessary diff strictly within approved scope. Reports changed files, tests run, deviations, and unresolved issues.
4. **Run deterministic checks:** Execute all applicable hard deterministic gates (`build`, `typecheck`, `lint`, `unit_tests`, `secrets_scan`, `clean_diff_scope`, `rollback_available`).
5. **Perform independent semantic review:** Independent Reviewer verifies candidate against acceptance criteria. **Agent claims are not evidence:** Reviewer must verify command exit statuses, diffs, and read-back evidence directly rather than relying on executor assertions.
6. **Emit one terminal state and Run Report:** Emit exactly one terminal state (`PASS`, `REWORK`, `BLOCKED`, or `HUMAN_REQUIRED`) and complete `contracts/RUN_REPORT.md`.

Reviewer returns:

```yaml
decision: PASS | REWORK | INCONCLUSIVE | HUMAN_REQUIRED
critical_findings: []
noncritical_findings: []
evidence: []
confidence: low | medium | high
```

Reviewer must not edit the candidate in the same invocation.
