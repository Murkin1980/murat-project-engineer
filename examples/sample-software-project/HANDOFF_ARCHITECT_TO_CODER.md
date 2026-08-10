# Typed Handoff v1

- run_id: `mpe-sample-001`
- task_id: `add-clamp-function`
- producer_role: `Architect`
- consumer_role: `Coder`
- task_summary: Add a dependency-free numeric clamp function with explicit invalid-range behavior.
- input_refs: approved Stage 1 instruction and sample repository.
- changed_files: planned `calculator.py`, `tests/test_calculator.py`.
- artifact_refs: none before implementation.
- assumptions: inclusive bounds; numeric inputs; Python standard library only.
- unresolved_risks: floating-point NaN behavior is outside this bounded sample.
- checks_already_run: deep-change assessment = no.
- required_next_checks: unit tests, syntax compile, artifact existence, scope review.
- acceptance_criteria: inside values unchanged; outside values clamped; invalid range raises ValueError.
- do_not_change: plugin architecture, Router, MASTER, credentials, external systems.
