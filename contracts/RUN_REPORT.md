# Compact Run Report v1

- run_id:
- project:
- task:
- start_timestamp:
- end_timestamp:
- risk_tier:
- playbook:
- experts_invoked:
- route_profiles:
- files_changed:
- commands_tools_used:
- deterministic_gate_results:
- judge_verdict:
- approvals:
- rework_count:
- outcome: PASS | REWORK | BLOCKED | HUMAN_REQUIRED
- unresolved_risks:
- rollback:
- approximate_usage_cost:
- task_packet_ref:
- skillization_gate_result:
- delegation_summary:
- browser_evidence_ref:
- verification_state_ref:
- final_git_diff_checkpoint:
- usage: (Run Usage Record — see USAGE_RECORD.md)
- compute_budget: (AI Compute Budget summary — see COMPUTE_BUDGET.md)

### Run Usage Record (inside `usage`)

- provider:
- model:
- input_tokens:
- cached_input_tokens:
- output_tokens:
- observed_cost:
- model_calls:
- tool_calls:
- retries:
- start_time:
- end_time:
- progress_checkpoints:
- measurement_source: provider_api | router_billing | usage_api | execution_log | price_reconstruction | operator_estimate | none
- measurement: observed | estimated | unobserved

### Compute Budget summary (inside `compute_budget`)

- planned_budget:
- hard_limit:
- spend:
- spend_measurement: observed | estimated | unobserved
- projected_total:
- projected_remaining:
- budget_status: GREEN | YELLOW | ORANGE | RED | UNOBSERVED
- burn_rate_status: OK | BURN_RATE_ANOMALY | UNOBSERVED
- measurement_quality: observed | estimated | unobserved
- forecast_confidence: low | medium | high
- provider_model_mix:
- recommended_stack:
- cost_per_progress_percent:

`approximate_usage_cost` stays compatible; it is treated as an *estimated* (never observed) spend when a number.

This report is the measurement source for the first 20 runs. Do not include private chain-of-thought or secret values.
