# Murat Project Engineer — repository rules

## Purpose

This repository develops the bounded coordination layer of Murat AI Stack. Preserve the architecture documented in `docs/MURAT_AI_STACK_V2_DECISION.md`.

## Mandatory boundaries

- Codex remains the execution/orchestration environment.
- Codex Router remains an inference/provider/protocol/credential gateway only.
- Expert is a bounded role contract, not a model or persistent process.
- Expert Team exists for one run only.
- Playbook is a human-readable procedure, not a workflow DSL or engine.
- Shared Memory references reviewed project source-of-truth files; do not create a memory service.
- Hard deterministic gates cannot be overridden by an LLM.
- Never store secrets, credentials, private chain-of-thought, or provider capability URLs.
- Do not bind an Expert permanently to one model.
- Do not promote temporary observations into durable rules automatically.

## Deep-change gate

Stop and emit `DEEP_CHANGE_REQUIRES_USER_APPROVAL` before implementing changes to:

- MASTER or core architecture;
- Router authority, credentials, or security boundaries;
- central runtime or daemon;
- persistent agents;
- fundamental plugin/skill boundaries;
- memory governance or automatic skill promotion.

Document a soft-compatible alternative and wait for explicit approval.

## Working rules

1. Read this file, applicable docs, and the relevant Playbook before editing.
2. Use a feature branch and a pull request; do not push directly to `main`.
3. Keep the diff scoped. Preserve unrelated changes.
4. Add or update tests for contract behavior.
5. Run the required validation commands before requesting review.
6. Report non-applicable checks explicitly; never hide failures.
7. Reviewer must be independent from the producer for meaningful semantic changes.

## Required checks

```powershell
python scripts/validate_package.py .
python -m unittest discover -s tests -v
python -m unittest discover -s examples/sample-software-project/tests -v
```

The official plugin/skill validators are also required when available in the Codex development environment.

## Pull-request evidence

Include changed files, decisions, validation output, deviations, unresolved risks, rollback, and confirmation that no deep-change boundary was crossed.
