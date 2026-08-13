# Contributing

Murat Project Engineer is developed through small, reviewable pull requests.

## Setup

Requirements: Git and Python 3.11+; the package itself has no runtime third-party dependency.

```powershell
git clone https://github.com/Murkin1980/murat-project-engineer.git
cd murat-project-engineer
python scripts/validate_package.py .
python -m unittest discover -s tests -v
```

The repository is private. Ask the owner for collaborator access before cloning.

## Branches and commits

- Branch from current `main`.
- Use `feature/<short-name>`, `fix/<short-name>`, or `docs/<short-name>`.
- Keep one primary outcome per pull request.
- Write concise imperative commit messages.
- Never commit credentials, local Router state, generated caches, or unrelated project data.

## Development flow

1. Read `AGENTS.md` and relevant decision documents.
2. Classify the change as FAST, VERIFIED, or DEEP-CHANGE.
3. Implement the smallest compatible change.
4. Run validation and tests.
5. Open a draft PR with evidence.
6. Resolve review findings without expanding scope silently.

## Pull-request acceptance

A PR is ready when:

- package validation passes;
- contract tests pass;
- sample tests pass when relevant;
- new behavior has observable acceptance criteria;
- documentation matches implementation;
- rollback is described;
- no hard gate is bypassed;
- deep changes have explicit owner approval.

## Out of scope without a separate approved RFC

- generic Workflow Engine or scheduler;
- Prime Agent runtime integration;
- persistent runtime agents;
- adaptive model routing;
- autonomous memory/skill promotion;
- Router or credential-boundary changes.
