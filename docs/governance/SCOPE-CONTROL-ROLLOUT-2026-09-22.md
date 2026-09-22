# Scope & Change Control rollout evidence

Date: 2026-09-22
Result: PASS

## Change

The MPE Scope & Change Control policy was established as the canonical cross-repository execution policy:

- canonical file: `docs/governance/SCOPE-CHANGE-CONTROL.md`
- canonical blob SHA: `ee8879b41b86f647cbb1889257bbb01561265095`
- mandatory first-read marker: `MPE:SCOPE-CHANGE-CONTROL:START`

For every active repository owned by `Murkin1980`:

1. A synchronized local copy was added at `docs/governance/SCOPE-CHANGE-CONTROL.md`.
2. The root `AGENTS.md` now requires that policy to be read before project-specific source-of-truth documents.
3. Existing project-specific rules were preserved rather than overwritten.
4. Repositories that had no `AGENTS.md` received a minimal project-local file that points to the policy and existing local source-of-truth documents without inventing project architecture.

## Portfolio verification

Repository inventory at rollout time:

- total repositories: 54
- active repositories: 42
- archived repositories: 12
- archived repositories modified: 0

Read-back verification across all 42 active repositories:

- local scope-policy file exists: 42/42
- local scope-policy content exactly matches canonical content: 42/42
- root `AGENTS.md` exists: 42/42
- mandatory first-read marker count is exactly one: 42/42

## AGENTS.md created where missing

Minimal root `AGENTS.md` files were created in:

- `Murkin1980/mebel-kalkulator2`
- `Murkin1980/1c-tutor-kz`
- `Murkin1980/mebelflow-asset-prep-sketchup`
- `Murkin1980/mebellayout-ai`
- `Murkin1980/MPE-core-`
- `Murkin1980/grand-mebel-document-control`
- `Murkin1980/threads-qaz`

## Business Discovery hierarchy

`Murkin1980/business-discovery/docs/agents/AGENTS.md` now explicitly declares itself subordinate to:

1. repository-root `AGENTS.md`
2. `docs/governance/SCOPE-CHANGE-CONTROL.md`

This removes ambiguity between the two agent-instruction layers without deleting Business Discovery-specific working rules.

## Archived repositories left unchanged

The following archived repositories were intentionally not migrated:

- `Murkin1980/kanban`
- `Murkin1980/LLMs-from-scratch-murkin-edition`
- `Murkin1980/Droid-claw-murkin`
- `Murkin1980/mebel-kalkulator`
- `Murkin1980/twenty`
- `Murkin1980/donutbrowser`
- `Murkin1980/Asyl-soft-landing-page`
- `Murkin1980/open-design`
- `Murkin1980/bek-mebel-v2`
- `Murkin1980/bek-mebel-3`
- `Murkin1980/LongLive`
- `Murkin1980/interactive-kp-import`

If one is reactivated, governance migration should be part of reactivation.

## Scope safety

No application runtime code, package dependencies, infrastructure configuration, production data, or deployment target was changed by this rollout.

No application test suite was run because the change is documentation/governance-only. Verification was performed by GitHub read-back of every active repository and exact content/marker checks.

## Result

**PASS**

All active repositories now use the same mandatory scope/change-control policy while retaining their project-specific constraints.
