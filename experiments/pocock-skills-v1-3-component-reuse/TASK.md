# EXP candidate — Matt Pocock Skills v1.3 component reuse

Date: 2026-10-08
Status: REGISTERED / NOT EXECUTED
Murat Project Engineer New Idea Filter: **REUSE_COMPONENT**
Source: https://github.com/mattpocock/skills (pin exact audited commit before any execution)
Host: existing Murat Project Engineer / Arena — no new repository, agent runtime, scheduler, memory DB or authority.

## Purpose and value

Extract only practical **patterns** from /retro, /pr, /implement-spec. Prioritize prevention of repeat Arena mistakes and more reviewable PR evidence. Existing MPE playbooks, review gates, run reports, source-of-truth repository docs, branch/worktree isolation and deep-change approvals remain authoritative.

## CP-01: upstream and overlap audit (read-only)

- Capture upstream commit, LICENSE, provenance, exact contents and versions of relevant skill files, including any installation scripts or hooks. No bulk installation or silent instructions acquisition.
- Compare each behavior against existing MPE review gates, retrospective/run reports, Arena execution plan, scripts and test coverage. Produce KEEP / BORROW / ADAPT / REJECT matrix and deduplication notes.
- Examine GLOSSARY.md convention versus current CONTEXT.md, project canon and glossary use. **Do not rename existing files**; only propose explicit compatibility mapping if gaps are shown.

## CP-02: /retro — priority 1 (bounded retrospective)

- Read one completed existing Arena session, initially EXP-24 HyperFrames PARTIAL, its RESULT/evidence and available terminal logs. No made-up historical traces.
- Produce a ranked, evidence-linked list: repeated searches/poor navigation; failures caught by static checks; unnecessary context or rules that change no behavior; missing preflight dependencies; tool friction and budget waste.
- For each proposal record severity, reproducibility, estimated effect, owner, smallest edit, test to verify and whether it crosses deep-change.
- Only generate recommendations; do not automatically edit instructions, install dependencies or reopen closed experiment.

## CP-03: /pr — priority 2 (reuse existing review gates)

- Build a **documentation-only** PR evidence checklist compatible with existing MPE PR format: problem, before/after, tests with precise counts, screenshots or artifacts when applicable, risk/blast radius, rollback, missing evidence, merge/deploy authorization.
- Pilot checklist against a recent existing PR (e.g. Grand Mebel Document Control) read-only, ensuring it does not create duplicate approvals or falsely call tests PASS.
- Keep current review authority and deep-change gate unchanged.

## CP-04: /implement-spec — priority 3 (isolation/duplication probe)

- First map current Arena scheduling/branch/worktree handling; **HOLD** adoption if existing components already meet needs.
- One small fixture spec with dependencies and 2 independent ready tasks: compare serial baseline to isolated worktree collaboration for conflicts, reproducibility, time, token use, human review, integration failures.
- Never enable autonomous merging, deploys, PR approvals, authority transfer, persistent queue or new orchestration infrastructure.

## CP-05: terminal acceptance

- Evidence: pinned upstream audit; component matrix; /retro report with severity-ranked actionable items; /pr checklist and one read-only trial; spec dependency graph and repeatable results if CP-04 feasible.
- Terminal result PASS / PARTIAL / FAIL / BLOCKED; separately mark each pattern ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT; no results before running.
- Recommended business targets (hypotheses only): measurable reduction of repeated Arena failures and review effort, no increase in regression/merge risk or token budget. Record pre/post numbers or UNOBSERVED explicitly.

## Guardrails

No production edits, merge, deploy, modification of core MPE architecture, change to deep-change gate, new repo, global skill install, mass rename of CONTEXT.md, hidden automation or self-modifying instructions. Any proposed structural/deep-change requires explicit owner consent. Arena task only after separate execution decision. This PR only registers the experiment, not its outcome.
