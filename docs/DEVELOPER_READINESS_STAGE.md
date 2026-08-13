# Developer readiness stage

Date: 2026-08-13  
Status: bounded repository-governance change

## Goal

Allow external collaborators to update Murat Project Engineer through reproducible pull requests without changing Murat AI Stack architecture.

## Included

- repository operating rules;
- contribution and security guidance;
- GitHub Actions validation;
- pull-request and experiment-run templates;
- current project status and roadmap;
- README navigation for developers;
- recommended protection of `main` after CI is available.

## Not included

- product/runtime feature changes;
- Workflow Engine, daemon or scheduler;
- Prime Agent integration;
- persistent agents;
- adaptive routing;
- marketplace/global installation;
- production infrastructure.

## Acceptance criteria

1. A new collaborator can locate architecture rules, setup steps and required checks from the repository root.
2. Pull requests run package validation, contract tests, sample tests and Python compilation on supported Python versions.
3. PR authors must disclose risk tier, evidence, rollback and architecture-boundary compliance.
4. Stage 1 experiment runs have a structured GitHub issue template.
5. Existing validation and tests continue to pass.
6. No Router, MASTER, credential or runtime authority changes occur.

## Developer report format

- changed files;
- requirements completed;
- commands and results;
- deviations and non-applicable checks;
- unresolved risks;
- rollback;
- confirmation that no prohibited architectural expansion occurred.

## Stop rule

If a contribution requires a deep change, stop the affected work and mark `DEEP_CHANGE_REQUIRES_USER_APPROVAL`.
