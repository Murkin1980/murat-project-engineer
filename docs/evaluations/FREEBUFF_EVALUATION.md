# FreeBuff Execution Evaluation

Date: 2026-08-14  
Selected scope: `Murkin1980/murat-project-engineer`  
Baseline commit: `408f94915f997bf9e9ec87e53987a15e5d09b6af` (`main`)  
Decision: `REJECT`

## Environment and privacy gate

```yaml
freebuff_environment:
  version: 0.0.149
  mode: CLI
  local_or_remote: remote_model_processing
  repository_data_class: PUBLIC
  isolated_workspace: not_created_execution_not_started
  git_branch: main_no_experiment_changes
  credentials_required: no_api_key_cli_may_require_login
  external_model_processing_known: true
  privacy_review_status: REVIEWED_2026-08-14
```

The official CLI package was installed with `npm install -g freebuff`. The Windows launcher downloaded the official binary and reported version `0.0.149`. Supported documented options were `login`, `--continue`, `--cwd`, `--version`, and `--help`; no non-interactive prompt/headless interface was exposed.

FreeBuff's privacy policy effective 2026-07-23 states that prompts, code, files, and repository data may be processed by FreeBuff systems and model providers. Prompt/project data may be used to personalize advertising; AI training applies only when the selected model or feature is labelled accordingly. Retention is purpose-dependent and may include backups and deidentified/evaluation data.

Therefore:

```text
mebeldocs-ai classification: RESTRICTED
FREEBUFF_CLOUD = BLOCKED_FOR_SENSITIVE_REPOS
murat-project-engineer classification: PUBLIC
privacy status for selected scope: SAFE_FOR_SELECTED_SCOPE
```

## Proposed bounded pilot

```yaml
task:
  repository: Murkin1980/murat-project-engineer
  commit: 408f94915f997bf9e9ec87e53987a15e5d09b6af
  goal: add a deterministic test proving experiment records preserve external-capability decision metadata without adding a new store
  acceptance_criteria: existing validator and tests pass; one focused test; no schema/runtime/Router changes
  allowed_files: [tests/test_contracts.py, contracts/EXPERIMENT_RECORD.md]
  forbidden_files: [router configuration, credentials, dashboard, target application repositories]
  max_scope: two files
  tests_required: true
  build_required: false
  deep_change_allowed: false
```

MPE baseline validation passed: package validator PASS and unit tests 5/5 PASS.

## Controlled comparison

The current Terms of Service effective 2026-07-23 prohibit bots, scripts, headless browsers, autonomous agents, or similar automation from operating FreeBuff. They require a human to initiate each session and remain actively present; only automation performed by FreeBuff after that human start is allowed.

Murat initiated and remained present for the interactive FreeBuff session. Two isolated worktrees used the same starting commit. Codex used the Router `coding` route `opencode-go/kimi-k2.7-code`; final independent review used `gpt-5.6-sol`.

| Metric | Codex | FreeBuff |
|---|---:|---:|
| Changed files | 2 | 1 |
| Added lines | 23 | 72 |
| Human rework | 0 | 1 |
| Validator | PASS | PASS |
| Unit tests | 6/6 PASS | 6/6 PASS |
| Acceptance criteria | PASS | FAIL |
| Unexpected dependency attempt | 0 | 1 (`jsonschema`, removed after rework) |

FreeBuff's final test still used `decision: ADOPT`, outside the mandatory MPE decision vocabulary. It populated most required record fields with `None`, did not validate a schema-conforming Experiment Record, and mostly proved Python JSON serialization rather than the contract. The initial attempt was 136 lines and failed to import because it introduced an undeclared `jsonschema` dependency. One human rework reduced the final diff to 72 lines and removed the dependency, but did not fix semantic acceptance.

```text
FREEBUFF_EXECUTION_VALUE = FAIL
FREEBUFF_EXECUTION_DECISION = REJECT
acceptance_criteria = FAIL
comparison = WORSE
```

Main measurable advantage: one final changed file versus two, but this did not compensate for semantic failure or rework.  
Main limitation: unreliable scope/contract judgment, required human correction, interactive-only operation, and remote data processing.  
Operational overhead: MEDIUM (global package plus 47.8 MB launcher download; first start required external local state).  
Windows compatibility: launcher works through `freebuff.cmd`; PowerShell script invocation is blocked by the machine execution policy.

## Removal

After the terminal `FAIL/REJECT`, the global `freebuff@0.0.149` package and `C:\Users\Мурат\.config\manicode` runtime/config/history directory were removed. No repository dependency or integration was added. FreeBuff is not approved as an Optional Execution Worker. Re-evaluation requires a materially more mature version and a new bounded experiment.
