---
playbook_id: verified
version: 1.1.0
supported_task_classes: [meaningful-code, meaningful-content, architecture-review]
risk_tier: VERIFIED
roles: [architect, coder, reviewer-when-semantic]
sequence: [research-source-of-truth, produce-task-packet, handoff, execute-smallest-change, deterministic-gates, independent-semantic-review, final-gates, report]
required_inputs: [task, project_context, acceptance_criteria, rollback]
deterministic_gates: [clean_diff_scope, secrets_scan, build, typecheck, lint, unit_tests, rollback_available]
optional_semantic_review: true
human_gate_conditions: [deep_change_detected, legal_or_accounting_approval, irreversible_external_effect]
max_rework_cycles: 1
terminal_states: [PASS, REWORK, BLOCKED, HUMAN_REQUIRED]
run_report_fields: contracts/RUN_REPORT.md
---

## Six-Stage Execution Flow (Research → Execute → Review)

1. **Research source-of-truth and constraints:** Read nearest project context (`AGENTS.md`, `FOUNDATION.md`, `DESIGN.md`), verify constraints and active repository state.
2. **Produce a bounded implementation plan / Task Packet:** Architect defines objective, scope boundaries, acceptance criteria, test plan, and deep-change assessment.
3. **Execute the smallest sufficient change:** Coder implements only the bounded change needed to fulfill criteria.
4. **Run deterministic checks:** Run all applicable hard deterministic gates before semantic evaluation.
5. **Perform independent semantic review:** Independent Reviewer inspects diffs and gate results. **Agent claims are not evidence:** The reviewer must not rely solely on executor claims; unverified assertions remain UNKNOWN/UNVERIFIED.
6. **Emit one terminal state and Run Report:** Emit exactly one terminal state (`PASS`, `REWORK`, `BLOCKED`, `HUMAN_REQUIRED`) and document all evidence in `contracts/RUN_REPORT.md`.

Skip non-applicable gates only with an explicit `NOT_APPLICABLE` reason in the Run Report.
