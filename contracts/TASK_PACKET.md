# Task Packet v1

A Task Packet is the immutable execution brief for one bounded MPE run. Create it **after** the New Idea Filter and Value / Scope / Deep-change gates, and before a writer or subagent starts work. It is not a queue, scheduler, or persistent workflow record.

- packet_id:
- run_id:
- project:
- source_task:
- idea_disposition: EXTEND_EXISTING | REUSE_COMPONENT | MERGE | EXPERIMENT | HOLD | NEW_REPOSITORY | REJECT | NOT_APPLICABLE
- idea_disposition_evidence:
- measurable_value:
- scope_in:
- scope_out:
- target_files_or_components: JSON runs use a non-empty list of repository-relative files, directories, or glob patterns
- applicable_project_rules:
- risk_tier: FAST | VERIFIED | DEEP-CHANGE
- deep_change_assessment:
- required_user_approval:
- acceptance_criteria:
- verification_plan:
- browser_evidence_required: YES | NO | NOT_APPLICABLE
- skillization_gate:
- delegation_plan:
- single_writer_owner:
- allowed_external_effects:
- rollback:
- stop_conditions:

## Rules

1. `scope_in`, `scope_out`, acceptance criteria, and stop conditions must be specific enough to review a Git diff against them.
2. `DEEP-CHANGE`, an unresolved architecture conflict, or `required_user_approval: YES` stops implementation until explicit approval is recorded.
3. A delegated packet may narrow the parent packet but cannot widen scope, grant new authority, alter approvals, or authorize an external side effect.
4. `single_writer_owner` is mandatory when any delegate can edit. All other delegates are read-only unless isolated worktrees and an explicit merge owner are named.
5. The Task Packet is complete before execution only when the Skillization Gate and delegation plan have an explicit decision.
6. An executable final Git-diff checkpoint uses a JSON Task Packet and treats `target_files_or_components` as the allowed changed-path scope. Any changed path outside that list is `UNVERIFIED`.
