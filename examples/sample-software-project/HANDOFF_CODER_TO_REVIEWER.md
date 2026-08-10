# Typed Handoff v1

- run_id: `mpe-sample-001`
- task_id: `add-clamp-function`
- producer_role: `Coder`
- consumer_role: `Reviewer`
- task_summary: Review the implemented clamp function against the Architect contract.
- input_refs: `HANDOFF_ARCHITECT_TO_CODER.md`.
- changed_files: `calculator.py`, `tests/test_calculator.py`.
- artifact_refs: test and compile results in `RUN_REPORT_COMPLETED.md`.
- assumptions: inclusive bounds and standard comparable numeric inputs.
- unresolved_risks: NaN semantics not specified.
- checks_already_run: unit tests PASS; compile PASS; artifact exists PASS.
- required_next_checks: acceptance mapping and scope review.
- acceptance_criteria: criteria from Architect handoff.
- do_not_change: candidate files; Reviewer is read-only.
