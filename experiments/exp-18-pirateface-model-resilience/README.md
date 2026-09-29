# EXP-18 — Pirate Face Model Resilience

## Decision
**EXPERIMENT**

This experiment extends the existing Murat Project Engineer experiment system. It does not create a new repository, service, runtime, or production dependency.

## Question
Can Pirate Face provide a useful, verifiable fallback distribution path for a pinned open-weight AI model artifact when the primary Hugging Face source is unavailable?

## Business value
The experiment is only valuable if it improves reproducibility or resilience for projects that depend on a specific open-weight model artifact, without creating a parallel model registry or ongoing infrastructure burden.

## Scope
Use one small model with a permissive license (for example MIT or Apache-2.0) that is already available on Hugging Face and discoverable through Pirate Face.

Record:
- Hugging Face repository and exact revision/commit.
- Expected files.
- SHA-256 checksums.
- Pirate Face / magnet reference used for retrieval.
- Retrieval result.
- Integrity comparison.
- Behavior when the normal Hugging Face retrieval path is intentionally unavailable for the test.

## Minimal experiment
1. Select one small permissively licensed model.
2. Pin the Hugging Face revision.
3. Download or otherwise establish the canonical artifact and compute SHA-256.
4. Obtain the Pirate Face distribution reference for the same model.
5. Retrieve the artifact through the Pirate Face path.
6. Compare file set and hashes against the pinned canonical artifact.
7. Simulate loss of the primary Hugging Face retrieval path without altering production systems.
8. Record whether the exact pinned artifact can still be recovered.

## PASS
PASS only if all of the following are true:
- the same pinned model artifact can be retrieved through Pirate Face;
- integrity is verifiable against recorded checksums;
- the test demonstrates a practical recovery path when the primary source is unavailable;
- no production architecture change or parallel registry is required;
- operational burden is low enough to justify keeping the method as an optional resilience tool.

## FAIL
FAIL if any of the following materially prevents useful recovery:
- the artifact cannot be retrieved reliably;
- checksums or revision identity cannot be verified;
- availability depends on assumptions that cannot be demonstrated in the bounded test;
- ongoing seeding/infrastructure cost outweighs the resilience benefit;
- the method requires a new production dependency or duplicate model-management system.

## Guardrails
- No production integration during EXP-18.
- No new repository.
- No replacement of Hugging Face as the current primary source.
- No model redistribution unless its license permits it.
- No assumption that a magnet link alone proves durable availability.
- Do not treat planned/announced Pirate Face features as implemented evidence.
- Any later fallback integration requires a separate Murat Project Engineer New Idea Filter decision.

## Evidence
Store only bounded experiment evidence here or in a dedicated evidence subdirectory. Record observed facts separately from assumptions.

## Current status
**PLANNED** — registered on 2026-09-29. No execution evidence exists yet.
