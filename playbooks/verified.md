---
playbook_id: verified
version: 1.1.0
supported_task_classes: [meaningful-code, meaningful-content, architecture-review]
risk_tier: VERIFIED
roles: [architect, coder, reviewer-when-semantic]
sequence: [idea-filter-when-needed, value-scope-deep-change-gates, task-packet, skillization-gate, bounded-execution-or-delegation, technical-gates, browser-evidence-when-required, verification-state-check, optional-reviewer, final-git-diff-checkpoint, report]
required_inputs: [task, project_context, acceptance_criteria, rollback, task_packet]
deterministic_gates: [deep_change_check, task_packet_complete, skillization_gate, clean_diff_scope, secrets_scan, build, typecheck, lint, unit_tests, browser_evidence, verification_state_current, final_git_diff_checkpoint, rollback_available]
optional_semantic_review: true
human_gate_conditions: [deep_change_detected, legal_or_accounting_approval, irreversible_external_effect]
max_rework_cycles: 1
terminal_states: [PASS, REWORK, BLOCKED, HUMAN_REQUIRED]
run_report_fields: contracts/RUN_REPORT.md
---

Skip non-applicable gates only with an explicit `NOT_APPLICABLE` reason in the Run Report.
