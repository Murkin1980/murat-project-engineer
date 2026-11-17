# EXP-30 candidate — OpenViking context component evaluation

Status: PROPOSED / NOT EXECUTED (not registered as an active experiment)
Primary New Idea Filter decision: **REUSE_COMPONENT**
Date: 2026-10-22
Owner: Murat Project Engineer
Upstream: https://github.com/volcengine/OpenViking

## Goal
Evaluate whether **selective context retrieval** from OpenViking improves real MPE/Arena task continuation beyond existing Git-derived bootstrap and handoff patterns. This is a comparative evaluation of a reusable component, **not permission to create a memory platform**.

## Existing assets and duplication gate
- EXP-15: MPE Project Memory Layer (prior memory evaluation).
- EXP-26: TencentDB Agent Memory component extraction.
- EXP-27/28: context packet, evidence-driven retrospectives.
- EXP-29: deterministic Git-derived Arena Bootstrap Harness; baseline and source-of-truth boundary.
- Canonical registry: `experiments/EXPERIMENT_REGISTRY.json`; do not create a second registry.

**Default hypothesis:** EXP-29 is sufficient. OpenViking is rejected if it does not show a clear measurable improvement without duplicate storage/authority.

## Proposed bounded checkpoints (not automatically authorized for execution)
1. **CP-00 / audit:** compare capabilities against EXP-15/26/27/29, inspect upstream license/dependencies/security and deployment footprint; log overlap and exact reusable subcomponent.
2. **CP-01 / frozen fixture:** choose one already-completed context-heavy task; freeze the same canonical Git snapshot, prompts, acceptance tests and retrieval budget for both arms.
3. **CP-02 / isolated A/B:** Arm A = EXP-29 current bootstrap; Arm B = same bootstrap + read-only, ephemeral OpenViking retrieval index over the *same* Git snapshot. No indexing of private credentials or external personal data. Both agents have identical model, tasks and budget.
4. **CP-03 / adversarial tests:** mutated source digest, stale state, conflicting instructions, missing evidence, prompt-injection text and retrieval failure. OpenViking output must be treated as non-authoritative and fail closed.
5. **CP-04 / disposition:** compare measurements and recommend REUSE_COMPONENT / HOLD / REJECT, with a verifiable report and cleanup of temporary resources.

## Measurement
- Input/output tokens **from actual model usage** (not estimated from bytes).
- Retrieval bytes, tool calls, elapsed time, relevant-answer accuracy, task completion and additional operational cost.
- Provenance: exact canonical path, git SHA and content hash for each retrieved item.
- Target, not claimed result: **>=20% lower combined token use** without reduced correctness or violation of governance. Record inconclusive results as UNVERIFIED, never PASS.

## Deep-change / stop gates
- No production integration, persistent vector store, memory database, daemon, network service, scheduler, data migration, new repository, autonomous rule promotion or change of Git source-of-truth.
- No new paid infrastructure or credential access. No write access to working repositories from evaluation component.
- If upstream cannot run ephemerally without prohibited infrastructure, finish only CP-00; mark BLOCKED/HOLD and ask owner before any deep change.
- Do not alter EXP-29 or its existing derived artifacts. Do not amend global governance or Router.
- Experimental implementation requires a separate bounded execution checkpoint; this document only registers the candidate proposal.
- Any registry mutation must follow existing dashboard-regeneration and evidence procedures; this proposal intentionally does **not** modify the canonical registry.

## Acceptance for planning stage
This file is a reviewable candidate proposal only. No OpenViking dependency installed; no benchmark run or savings claimed. Follow the MPE scope-control policy and do not start CP-01 until the relevant gate is cleared.
