from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXPERT_FIELDS = {"expert_id", "role", "responsibility", "invoke_when", "do_not_invoke_when", "allowed_inputs", "expected_outputs", "required_skills", "capability_profile", "preferred_route_profile", "max_rework_cycles", "forbidden_actions", "handoff_contract"}
PLAYBOOK_FIELDS = {"playbook_id", "version", "supported_task_classes", "risk_tier", "roles", "sequence", "required_inputs", "deterministic_gates", "optional_semantic_review", "human_gate_conditions", "max_rework_cycles", "terminal_states", "run_report_fields"}
HANDOFF_FIELDS = {"run_id", "task_id", "producer_role", "consumer_role", "task_summary", "input_refs", "changed_files", "artifact_refs", "assumptions", "unresolved_risks", "checks_already_run", "required_next_checks", "acceptance_criteria", "do_not_change"}
RUN_REPORT_FIELDS = {"run_id", "project", "task", "start_timestamp", "end_timestamp", "risk_tier", "playbook", "experts_invoked", "route_profiles", "files_changed", "commands_tools_used", "deterministic_gate_results", "judge_verdict", "approvals", "rework_count", "outcome", "unresolved_risks", "rollback", "approximate_usage_cost"}
COMPUTE_BUDGET_FIELDS = {"compute_budget_currency", "compute_budget_planned_budget", "compute_budget_hard_limit", "preflight_input_tokens_min", "preflight_input_tokens_expected", "preflight_input_tokens_max", "preflight_output_tokens_min", "preflight_output_tokens_expected", "preflight_output_tokens_max", "preflight_estimated_cost_min", "preflight_estimated_cost_expected", "preflight_estimated_cost_max", "preflight_confidence", "usage_input_tokens", "usage_cached_input_tokens", "usage_output_tokens", "usage_estimated_cost", "usage_measurement", "forecast_estimated_total_cost_min", "forecast_estimated_total_cost_expected", "forecast_estimated_total_cost_max", "forecast_remaining_cost_expected", "forecast_confidence", "routing_recommended_stack", "routing_actual_provider_mix", "efficiency_project_progress_percent", "efficiency_budget_consumed_percent", "efficiency_cost_per_progress_percent", "status_budget_status", "status_burn_rate_status", "status_burn_rate_ratio"}
USAGE_RECORD_FIELDS = {"usage_provider", "usage_model", "usage_input_tokens", "usage_cached_input_tokens", "usage_output_tokens", "usage_observed_cost", "usage_model_calls", "usage_tool_calls", "usage_retries", "usage_start_time", "usage_end_time", "usage_progress_checkpoints", "usage_measurement_source", "usage_measurement"}
EXPERIMENT_FIELDS = {"run_id", "execution_mode", "task_class", "risk_tier", "expert_or_team", "run_duration", "resolved_model_slugs", "tool_calls_observable", "deterministic_gate_failures", "reviewer_findings", "reviewer_false_positives", "rework_count", "human_intervention", "defect_escaped_after_pass", "interruption_recovery_issue", "approximate_token_cost_overhead", "fan_out_fan_in_needed", "notes"}


# --- Canonical MPE evidence-trust boundary (integrated from EXP-002 Iteration 3) ---
# Reuses the existing Result Contract field ``evidence_ref``
# (RUN_REPORT.deterministic_gate_results). The invariant enforced here:
#   a claimed/required execution PASS must be backed by a trusted evidence source.
# Self-reported or unknown evidence is fail-closed (cannot yield PASS). Honest
# "understood but not executed" is represented as HUMAN_REQUIRED, never as PASS.
TRUSTED_EVIDENCE_REFS = {
    "git_status", "git_diff", "secrets_scan", "compileall",
    "test_runner", "terminal_command", "ci_result",
    "platform_tool_trace", "hash_linked_artifact",
}
UNTRUSTED_EVIDENCE_SENTINELS = {"self_reported", "executor_prose", "model_generated"}
REQUIRED_EXECUTION_CHECKS = ("clean_diff_scope", "secrets_scan", "build")


def classify_evidence_ref(ref) -> str:
    """Classify an ``evidence_ref`` as TRUSTED / UNTRUSTED / UNKNOWN.

    UNKNOWN covers prose or unrecognized sources and must fail-closed.
    """
    if ref in TRUSTED_EVIDENCE_REFS:
        return "TRUSTED"
    if ref in UNTRUSTED_EVIDENCE_SENTINELS:
        return "UNTRUSTED"
    return "UNKNOWN"


def derive_execution_outcome(gate_results, required_checks=REQUIRED_EXECUTION_CHECKS) -> str:
    """Canonical MPE execution-outcome derivation from gate evidence (deterministic).

    - untrusted/unknown PASS claim for a required check -> REWORK (never PASS)
    - every required check PASS via trusted evidence        -> PASS
    - no verified execution evidence                        -> HUMAN_REQUIRED
    """
    passed_trusted = [
        g for g in gate_results
        if g.get("gate_id") in required_checks and g.get("result") == "PASS"
        and classify_evidence_ref(g.get("evidence_ref")) == "TRUSTED"
    ]
    fabricated = [
        g for g in gate_results
        if g.get("gate_id") in required_checks and g.get("result") == "PASS"
        and classify_evidence_ref(g.get("evidence_ref")) != "TRUSTED"
    ]
    if fabricated:
        return "REWORK"
    if len(passed_trusted) == len(required_checks):
        return "PASS"
    return "HUMAN_REQUIRED"


def validate_gate_results(gate_results) -> list:
    """Return violations: any PASS claim lacking trusted ``evidence_ref``."""
    violations = []
    for g in gate_results:
        if g.get("result") == "PASS" and classify_evidence_ref(g.get("evidence_ref")) != "TRUSTED":
            violations.append(
                f"gate {g.get('gate_id')!r} claims PASS with non-trusted evidence_ref {g.get('evidence_ref')!r}"
            )
    return violations


def frontmatter_keys(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not match:
        raise ValueError(f"missing frontmatter: {path}")
    return {m.group(1) for m in re.finditer(r"^([a-z_]+):", match.group(1), re.M)}


def template_fields(path: Path) -> set[str]:
    return {m.group(1) for m in re.finditer(r"^- ([a-z_]+):", path.read_text(encoding="utf-8"), re.M)}


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        if data.get("name") != root.name:
            errors.append("plugin name must match root folder")
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(data.get("version", ""))):
            errors.append("plugin version must be strict semver")
    except Exception as exc:
        errors.append(f"invalid plugin manifest: {exc}")

    experts = sorted((root / "experts").glob("*.md"))
    playbooks = sorted((root / "playbooks").glob("*.md"))
    teams = sorted((root / "teams").glob("*.md"))
    if len(experts) != 4:
        errors.append("exactly four Expert definitions are required")
    if len(teams) != 3:
        errors.append("exactly three Team definitions are required")
    if len(playbooks) != 4:
        errors.append("exactly four Playbooks are required")
    for path in experts:
        missing = EXPERT_FIELDS - frontmatter_keys(path)
        if missing:
            errors.append(f"{path.name} missing expert fields: {sorted(missing)}")
    for path in playbooks:
        missing = PLAYBOOK_FIELDS - frontmatter_keys(path)
        if missing:
            errors.append(f"{path.name} missing playbook fields: {sorted(missing)}")

    missing = HANDOFF_FIELDS - template_fields(root / "contracts" / "HANDOFF.md")
    if missing:
        errors.append(f"HANDOFF missing fields: {sorted(missing)}")
    missing = RUN_REPORT_FIELDS - template_fields(root / "contracts" / "RUN_REPORT.md")
    if missing:
        errors.append(f"RUN_REPORT missing fields: {sorted(missing)}")
    missing = EXPERIMENT_FIELDS - template_fields(root / "contracts" / "EXPERIMENT_RECORD.md")
    if missing:
        errors.append(f"EXPERIMENT_RECORD missing fields: {sorted(missing)}")
    missing = COMPUTE_BUDGET_FIELDS - template_fields(root / "contracts" / "COMPUTE_BUDGET.md")
    if missing:
        errors.append(f"COMPUTE_BUDGET missing fields: {sorted(missing)}")

    try:
        budget_example = json.loads((root / "contracts" / "COMPUTE_BUDGET.example.json").read_text(encoding="utf-8"))
        budget_schema = json.loads((root / "contracts" / "COMPUTE_BUDGET.schema.json").read_text(encoding="utf-8"))
        for block in ("compute_budget", "preflight", "usage", "forecast", "routing", "efficiency"):
            if block not in budget_example or block not in budget_schema["properties"]:
                errors.append(f"COMPUTE_BUDGET schema/example block mismatch: {block}")
    except Exception as exc:
        errors.append(f"invalid COMPUTE_BUDGET schema or example: {exc}")

    missing = USAGE_RECORD_FIELDS - template_fields(root / "contracts" / "USAGE_RECORD.md")
    if missing:
        errors.append(f"USAGE_RECORD missing fields: {sorted(missing)}")
    try:
        usage_example = json.loads((root / "contracts" / "USAGE_RECORD.example.json").read_text(encoding="utf-8"))
        usage_schema = json.loads((root / "contracts" / "USAGE_RECORD.schema.json").read_text(encoding="utf-8"))
        if set(usage_example) != set(usage_schema["required"]):
            errors.append("USAGE_RECORD example keys must match schema required fields")
    except Exception as exc:
        errors.append(f"invalid USAGE_RECORD schema or example: {exc}")

    required_gates = {"clean_diff_scope", "secrets_scan", "build", "typecheck", "lint", "unit_tests", "integration_tests", "acceptance_tests", "artifact_exists", "artifact_hash", "rollback_available", "deep_change_check", "mailbox_schema_valid", "handoff_traceable", "event_log_valid", "worktree_collision_check", "terminal_state_valid"}
    registry = (root / "gates" / "registry.yaml").read_text(encoding="utf-8")
    present = set(re.findall(r"gate_id:\s*([a-z_]+)", registry))
    if required_gates - present:
        errors.append(f"gate registry missing: {sorted(required_gates - present)}")

    # Evidence-trust integration: enforce the canonical rule on canonical RUN_REPORT
    # gate results (structured JSON). The legacy ``evidence/`` directory used prose
    # provenance and is intentionally excluded (backward-compat; no bulk-migration).
    for path in root.rglob("*.json"):
        if "evidence" in path.parts:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        gates = data.get("deterministic_gate_results") if isinstance(data, dict) else None
        if isinstance(gates, list):
            for v in validate_gate_results(gates):
                errors.append(f"{path.relative_to(root)}: evidence-trust violation: {v}")

    route_text = (root / "skills" / "murat-project-engineer" / "references" / "route-profiles.md").read_text(encoding="utf-8")
    for slug in ("gpt-5.6-sol", "opencode-go/deepseek-v4-flash", "opencode-go/kimi-k2.7-code"):
        if slug not in route_text:
            errors.append(f"route profile missing explicit slug: {slug}")

    sample_report = (root / "examples" / "sample-software-project" / "RUN_REPORT_COMPLETED.md").read_text(encoding="utf-8")
    for required in ("resolved_slug", "evidence/", "review_invocation_id", "git_commit"):
        if required not in sample_report:
            errors.append(f"sample report missing operational evidence marker: {required}")
    if "rework_count: `1`" not in sample_report:
        errors.append("sample report must record the remediation cycle")
    final_verdict = root / "examples" / "sample-software-project" / "REVIEWER_VERDICT_FINAL.md"
    if final_verdict.exists():
        verdict_text = final_verdict.read_text(encoding="utf-8")
        if "decision: PASS" not in verdict_text:
            errors.append("final reviewer artifact exists without PASS")
        if "outcome: PASS" not in sample_report:
            errors.append("final PASS reviewer artifact requires report outcome PASS")
    elif "outcome: PASS" in sample_report:
        errors.append("sample report cannot claim PASS without final reviewer artifact")

    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml"}:
            if "[TODO:" in path.read_text(encoding="utf-8"):
                errors.append(f"placeholder remains: {path.relative_to(root)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    root = Path(parser.parse_args().root).resolve()
    errors = validate(root)
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALIDATION PASSED")
    gate_count = len(set(re.findall(r"gate_id:\s*([a-z_]+)", (root / "gates" / "registry.yaml").read_text(encoding="utf-8"))))
    print(f"4 experts, 3 teams, 4 playbooks, contracts, and {gate_count} gates present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
