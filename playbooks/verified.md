---
playbook_id: verified
version: 1.0.0
supported_task_classes: [meaningful-code, meaningful-content, architecture-review]
risk_tier: VERIFIED
roles: [architect, coder, reviewer-when-semantic]
sequence: [classify, architect, handoff, coder, deterministic-gates, optional-reviewer, final-gates, report]
required_inputs: [task, project_context, acceptance_criteria, rollback]
deterministic_gates: [clean_diff_scope, secrets_scan, build, typecheck, lint, unit_tests, rollback_available]
optional_semantic_review: true
human_gate_conditions: [deep_change_detected, legal_or_accounting_approval, irreversible_external_effect]
max_rework_cycles: 1
terminal_states: [PASS, REWORK, BLOCKED, HUMAN_REQUIRED]
run_report_fields: contracts/RUN_REPORT.md
---

Skip non-applicable gates only with an explicit `NOT_APPLICABLE` reason in the Run Report.
