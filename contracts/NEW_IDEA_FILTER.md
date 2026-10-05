# New Idea Filter and Anti-Roadmap Contract v1

Canonical contract for evaluating new products, features, integrations, and architectural proposals prior to implementation.

```yaml
idea_id:
title:
submitted_date:
proposer:
target_domain:
checks:
  existing_active_project:
    status: OVERLAPPING | DISTINCT | NONE
    matched_project:
    details:
  extension_possibility:
    viable: true | false
    target_project:
    architectural_fit:
  reusable_component:
    identified: true | false
    reusable_refs: []
  duplicate_capability:
    detected: true | false
    duplicate_systems: []
  measurable_business_value:
    metric:
    expected_outcome:
    horizon:
  smallest_useful_experiment:
    hypothesis:
    method:
    sample_size:
    max_duration:
  portfolio_priority:
    competes_with_p0: true | false
    priority_verdict: PROCEED | DEFER | REJECT
  deep_change_impact:
    triggers_deep_change: true | false
    affected_boundaries: []
  anti_roadmap_constraints:
    violates_anti_roadmap: true | false
    violated_clauses: []
decision:
  terminal_disposition: EXTEND_EXISTING | REUSE_COMPONENT | MERGE | EXPERIMENT | HOLD | NEW_REPOSITORY | REJECT
  fail_closed_triggered: true | false
  rationale:
  next_action:
```

## Field reference (flat)

- idea_id: unique identifier (e.g. IDEA-2026-10-001)
- title: concise title of the idea
- submitted_date: date in YYYY-MM-DD format
- proposer: originator or source reference
- target_domain: system or product area
- check_existing_active_project: OVERLAPPING | DISTINCT | NONE
- check_extension_possibility: viable boolean and fit notes
- check_reusable_component: identified boolean and reusable references
- check_duplicate_capability: detected boolean and duplicate systems list
- check_measurable_business_value: metric, expected outcome, and horizon
- check_smallest_useful_experiment: hypothesis, method, and sample size
- check_portfolio_priority: competes_with_p0 flag and verdict
- check_deep_change_impact: triggers_deep_change flag and affected boundaries
- check_anti_roadmap_constraints: violates_anti_roadmap flag and violated clauses
- terminal_disposition: EXTEND_EXISTING | REUSE_COMPONENT | MERGE | EXPERIMENT | HOLD | NEW_REPOSITORY | REJECT
- fail_closed_triggered: boolean indicating fail-closed enforcement
- rationale: conclusive justification for disposition
- next_action: concrete immediate step

## Rules

- Every idea must be evaluated against all nine checks in order.
- `terminal_disposition` must be exactly one of the seven canonical states.
- If `violates_anti_roadmap` is `true`, `terminal_disposition` must be `REJECT` or `HOLD`.
- If `triggers_deep_change` is `true` without pre-existing human approval, the filter must fail closed to `HOLD` or `HUMAN_REQUIRED`.
- Anti-roadmap constraints and idea records must not contain private personal data.
