---
playbook_id: deep-change
version: 1.0.0
supported_task_classes: [core-architecture, router-authority, security, credentials, persistent-agents, memory-governance, central-runtime]
risk_tier: DEEP-CHANGE
roles: [architect]
sequence: [analyze, identify-conflict, propose-soft-alternative, stop-for-user]
required_inputs: [task, master_context, project_context]
deterministic_gates: [deep_change_check]
optional_semantic_review: true
human_gate_conditions: [always]
max_rework_cycles: 0
terminal_states: [HUMAN_REQUIRED, BLOCKED]
run_report_fields: contracts/RUN_REPORT.md
---

Emit `DEEP_CHANGE_REQUIRES_USER_APPROVAL`. Do not implement until explicit approval.
