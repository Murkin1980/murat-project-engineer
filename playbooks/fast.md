---
playbook_id: fast
version: 1.0.0
supported_task_classes: [trivial, narrow-code, narrow-document]
risk_tier: FAST
roles: [single-suitable-expert]
sequence: [classify, execute, deterministic-checks, report]
required_inputs: [task, project_context, acceptance_criteria]
deterministic_gates: [clean_diff_scope, secrets_scan, artifact_exists]
optional_semantic_review: false
human_gate_conditions: [deep_change_detected, irreversible_external_effect]
max_rework_cycles: 0
terminal_states: [PASS, BLOCKED, HUMAN_REQUIRED]
run_report_fields: contracts/RUN_REPORT.md
---

Use only when the change is narrow and reversible.
