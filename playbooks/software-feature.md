---
playbook_id: software-feature
version: 1.1.0
supported_task_classes: [software-feature, bug-fix, bounded-refactor]
risk_tier: VERIFIED
roles: [architect, coder, reviewer-when-required]
sequence: [idea-filter-when-needed, value-scope-deep-change-gates, task-packet, skillization-gate, architect, architect-to-coder-handoff, bounded-coder-or-delegate, technical-gates, browser-evidence-when-required, verification-state-check, coder-to-reviewer-handoff, reviewer-if-required, rework-at-most-once, final-git-diff-checkpoint, run-report]
required_inputs: [task, repository_path, project_context, acceptance_criteria, task_packet]
deterministic_gates: [deep_change_check, task_packet_complete, skillization_gate, clean_diff_scope, secrets_scan, build, typecheck, lint, unit_tests, integration_tests, acceptance_tests, browser_evidence, verification_state_current, final_git_diff_checkpoint, rollback_available]
optional_semantic_review: true
human_gate_conditions: [deep_change_detected, irreversible_external_effect, judge_human_required]
max_rework_cycles: 1
terminal_states: [PASS, REWORK, BLOCKED, HUMAN_REQUIRED]
run_report_fields: contracts/RUN_REPORT.md
---

Architect outputs objective, affected components, constraints, acceptance criteria, likely files, tests, rollback, and deep-change assessment.

Coder outputs implementation, changed files, tests, deviations, and unresolved issues.

Reviewer returns:

```yaml
decision: PASS | REWORK | INCONCLUSIVE | HUMAN_REQUIRED
critical_findings: []
noncritical_findings: []
evidence: []
confidence: low | medium | high
```

Reviewer must not edit the candidate in the same invocation.

If the Git-complete snapshot changes after technical checks, Browser Evidence, or reviewer evidence, the required check returns `UNVERIFIED`; repeat the affected verification before the executable final Git-diff checkpoint.
