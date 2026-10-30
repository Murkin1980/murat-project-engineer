# EXP-34 — Self-Improving Harness / Arena task

Status: EXP-34 ASSIGNED IN INTAKE BRANCH / NOT YET MERGED INTO MAIN
MPE New Idea Filter: EXPERIMENT
Priority proposal: P1 (subject to portfolio comparison)
Owner-authorized scope: one Arena session, isolated evaluation, 3 sequential improvement cycles.
This file assigns EXP-34 for the owner-approved experiment in this branch; canonical registry registration and merge into main remain separate controlled steps. It is NOT permission to alter core runtime.

## CP-00 — verify EXP-34 reservation, STOP if collision

1. Read `docs/governance/SCOPE-CHANGE-CONTROL.md` before anything else, then `AGENTS.md`, `docs/NEW_IDEA_FILTER_POLICY.md`, `docs/GLOBAL_MPE_ENFORCEMENT.md`, `docs/OPINIONATED_WORKSPACE_POLICY.md`, human-value / unit economics policies as applicable, and current registry/status.
2. Read `experiments/EXPERIMENT_REGISTRY.json` at the actual target `main` head. Inspect active/pending PRs, experiment directories, issues/queued drafts, and any documented experiment-ID reservation protocol; do not rely on largest number in main only.
3. Existing candidates already observed: EXP-30 collisions (OpenViking, AI Process Discovery, Crisp Diagrams, Nodecode Lisp), EXP-31 HtmlVR, EXP-32 OpenMuse, EXP-33 Seedance 2.5. These may be pending/unmerged. Revalidate their live state.
4. Owner-assigned candidate ID: EXP-34. Revalidate absence of conflicting reservations before canonical registry registration; if a conflict is discovered, STOP and report it rather than silently renumbering or editing other experiments. Do not self-assign EXP-30.
5. Inspect EXP-27 (lease/budget/approval), EXP-28 (evidence-gated retrospective), EXP-29 (Git-derived bootstrap) and any existing self-improvement work. Avoid a second agent framework or source of truth. Compare P1 priority and smallest useful value/ROI proxy.
6. Run focused baseline; label pre-existing failures, and do not silently fix unrelated failures.

## CP-01 — bounded design
After the identifier gate passes, define a frozen replayable, non-production MPE task plus an independent unseen holdout. Benchmark the unchanged harness (A), then three sequential candidate improvements (B, C, D) with identical task inputs and evaluation criteria. Specify measurable quality, completion, tool calls, context bytes, runtime, tokens/cost where available, retries, and permission outcomes. Label proxies as proxies. Maintain hashes/provenance and reproducible inputs.

## CP-02 — constrained iterative execution
Use only an isolated Arena sandbox and existing harness/test primitives. For each of three rounds, identify a real bottleneck, change only an explicitly allowlisted experiment-local harness/config candidate, execute tests and fresh holdout validation, and compare against the best prior candidate. Only accept improvements that preserve correctness and safety, are reproducible, and improve a meaningful metric without unacceptable regression. Roll back otherwise. Negative controls must show attempted override of governance, unauthorized writes, or benchmark shortcut fails closed. Any LLM-generated modification is untrusted until independently verified.

## CP-03 — evidence and handoff
Write experiment-local README, RESULTS, candidate diffs, test commands, machine-readable measurements and provenance, and comparative table. Use existing MPE evidence formats. Report PASS/PARTIAL/FAIL/INCONCLUSIVE separately from adoption disposition. Distinguish real gains from overfitting and unmeasured claims. If registry/dashboard/Reladraw changes are required, use established regeneration and validation contracts; never manufacture a FRESH derived packet.

## Hard boundaries / STOP
No new repository, service, worker, database, credentials, model-weight training, persistent self-modification, self-issued permissions, router/governance/source-of-truth changes, production access, autonomous merge or deploy, or unapproved spend. Never modify outside the approved experiment-local allowlist. Deep-change or collision => STOP for that action and request owner approval. Do not merge even if checks pass. Any PR must be review-only and only within session branch write permissions.

## Delivery
Return verified registry allocation status, exact selected ID if safely reserved, branch/head/PR (if authorized), baseline, all arms' evidence, accepted/rejected diffs, safety gates, validation results, blockers, and the smallest next owner decision. Preserve STATE / EVIDENCE / CHANGES / RESULT / BLOCKER / NEXT ACTION / HANDOFF.