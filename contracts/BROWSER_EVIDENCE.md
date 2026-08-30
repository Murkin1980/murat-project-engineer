# Browser Evidence v1

Use this evidence for every browser-observable acceptance criterion: a user-facing UI, rendered document, deployed route, form, interaction, responsive state, or public configuration result. It is recorded after applicable technical checks and before the final Git-diff checkpoint.

- run_id:
- packet_id:
- applicability: REQUIRED | NOT_APPLICABLE
- reason_if_not_applicable:
- environment: local | preview | production
- exact_url_or_entrypoint:
- browser_or_runtime:
- timestamp:
- prerequisite_state:
- steps:
- expected_results:
- observed_results:
- artifact_refs: (screenshots, recording, DOM/accessibility capture, or explicitly stated observation)
- defects_or_limitations:
- verifier:
- verdict: PASS | REWORK | BLOCKED

## Rules

1. A link alone is not Browser Evidence. Record the performed steps and observed result.
2. Evidence must identify the exact environment and URL/entry point. A production claim requires production evidence.
3. If browser access is unavailable for a required criterion, the criterion is `BLOCKED`; do not substitute a guessed result or claim `PASS`.
4. `NOT_APPLICABLE` is allowed only when no acceptance criterion is browser-observable, with the reason recorded.
5. Any later change to a verified file or browser-observable configuration invalidates the evidence and requires fresh applicable technical checks and Browser Evidence.
