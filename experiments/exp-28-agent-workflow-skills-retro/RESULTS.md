# EXP-28 — Results: evidence-gated Agent Workflow Skills retrospective

- **RESULT:** **PASS** (bounded decision experiment; see limitations)
- **ADOPTION:** **ADOPT_WITH_CHANGES** — keep a manual, evidence-gated retrospective pattern only
- **Donor disposition:** `/retro`, `/pr`, and instruction-review material are references, not installed skills
- **Run date:** 2026-10-09 (UTC)
- **Scope:** EXP-24 Phase 1 PARTIAL, EXP-25 PASS, EXP-27 PASS
- **Automation/integration:** none; no harness was necessary; no automatic post-run trigger

## Executive decision

A structured retrospective found concrete friction already present in the run records, separated verified causes from unknowns, and produced two bounded candidates. One immediate, experiment-local instruction improvement was applied to the still-authorized EXP-24 Phase 2 task. No production MPE code, core governance, review gate, or runtime changed.

The evidence supports **manual use after a run that was difficult or valuable to learn from**, not an automatic retrospective after every run. It does not support claiming that `/retro` itself saves time or improves engineering quality across all tasks. The strongest measured signal is the pre-existing EXP-27 no-packet vs. compact-context comparison; it measures context-retrieval overhead, not wall-clock time saved by this EXP-28 review.

## Reference extraction

Pinned source: [`mattpocock/skills@b0618bc436ad893b3c5e84e55fba86586d34a404`](https://github.com/mattpocock/skills/tree/b0618bc436ad893b3c5e84e55fba86586d34a404), last commit observed 2026-10-08. Files read: [`/retro`](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/retro/SKILL.md), [retro rationale](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/docs/engineering/retro.md), [`/pr`](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/pr/SKILL.md), [PR rationale](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/docs/engineering/pr.md), [writing-for-agents](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/productivity/writing-for-agents/SKILL.md), [skill mechanics](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/productivity/writing-for-agents/SKILL-MECHANICS.md), and [code-review](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/code-review/SKILL.md). No source files were copied or installed.

| Reference | **KEEP** | **BORROW** | **ADAPT** | **REJECT** |
|---|---|---|---|---|
| `/retro` | User-invoked and proposal-only; inspect the session's own evidence. | Friction categories (navigation, checks, instructions, tools, information access) and map a proven issue to the smallest existing place that can prevent it. | Require MPE-specific evidence, root cause, minimal change, effect, false-improvement risk, and verification; use `NO_CHANGE` for isolated low-cost events. Keep Git/project records canonical. | Run after every session, auto-edit instructions, auto-install hooks, or convert one run's obstacle into a global rule. |
| `/pr` | The distinction between a PR body and the branch/PR workflow. | `Summary → Evidence → Merge Danger` as a concise reviewer-facing body. | Use the existing MPE task/result, test baseline, branch, and merge authority; open/manage the PR with the repository's existing Git/`gh` workflow. | Treat `/pr` as permission to push/open/merge, auto-merge, or replace local PR requirements. |
| Instruction review (`writing-for-agents` + `code-review`) | Existing source-of-truth priority and progressive disclosure. | Check pointers, relevance/no-ops, and whether a proposed instruction belongs at the level that consumes it; separate spec compliance from standards review. | First prefer a narrowly scoped existing task/run file; change global MPE instructions only when evidence shows a cross-task rule and local governance authorizes it. MPE's own mandatory `AGENTS.md` rules remain binding. | Copy the donor's opinions as universal MPE policy (for example, that `AGENTS.md` must contain navigation pointers only), add a new standards/governance layer, or keep rerunning judgement-based reviews until they report no findings. |

This is mechanism extraction, not a copy of the upstream skill. The adopted shape deliberately stays smaller than the donor's full `/retro` category list.

## Evidence and method

The reconstruction used the checked-in Arena task, result, audit, recovery, proof, and event files. Missing chat logs and unrecorded elapsed time are not inferred. The detailed procedure is in [`ARENA_TASK.md`](ARENA_TASK.md).

### EXP-24 HyperFrames, Phase 1 — PARTIAL

**Task.** Turn merged MPE PR #46 into a short, deterministic HyperFrames video.

**Executor actions.** The recovered run froze PR evidence, audited HyperFrames, wrote a four-scene storyboard and plain HTML/CSS composition, ran a bounded structural check, attempted one CLI initialization, one preview, and one render. A preceding Arena attempt had stalled without a terminal result or persisted artifacts; `RECOVERY.md` instructed cancellation and a fresh bounded run.

**Delays/errors in evidence.** The one `npx hyperframes@0.8.137 init` exited successfully, but its unavailable skills-freshness check fell back to cloning upstream and installing ten agent skills into `~/.claude/skills` and `~/.agents/skills`—an unrequested side effect. Preview started but reported 1 lint error and 6 warnings without identifying the rules. Render exited before capture because Chrome was missing; the browser download failed at TLS setup. FFmpeg was also absent. No MP4, screenshot, repeatability check, or phone review was produced. The result was correctly closed as PARTIAL.

**Root cause vs. unknown.** The renderer was incompatible with the available Arena environment (browser/codec prerequisites); the exact cause of the older hung run and the preview lint error is **unknown** from preserved artifacts. The CLI bootstrap's hidden skill-install fallback was a tool side effect not anticipated by the task instructions. Do not infer that a generic MPE rule caused or would have prevented the earlier hang.

**Prevention.** A renderer-specific, task-local preflight and an explicit boundary around HyperFrames initialization are justified for the still-authorized Phase 2 only if HyperFrames is selected. This is the only recommendation applied in this experiment; details are R2 below. No global environment policy is proposed.

Evidence: `experiments/exp-24-hyperframes-pr-video/RECOVERY.md` → Situation; `ARENA_TASK.md` → Phase 1 closure-first limits and Phase 2 constraints; `RESULTS.md` → Bounded attempts and exact blocker; `UPSTREAM_AUDIT.md` → Observed `init` side effect and executor preflight.

### EXP-25 Atomic CRM component extraction — PASS

**Task.** Map reusable Atomic CRM patterns onto the existing MiniBase contract and prove a bounded contact → deal → task → timeline slice plus a read-first tool surface.

**Executor actions.** The run audited Atomic and the MiniBase host read-only, mapped eight reusable patterns and three rejections, built a test-data-only harness, ran 25/25 proof checks and 26 tests, and compared the full test suite before and after. Optional Kanban was not built because MiniBase had no UI integration point. No production host or live data was changed.

**Delays/errors in evidence.** There are no recorded execution delays or proof failures. The full suite had 41 failures, 3 errors, and 1 skipped test both before and after (with the same failure set); the run classified these as pre-existing registry/dashboard drift and did not fold the neighboring cleanup into EXP-25. The proof itself passed, and the two recorded proof JSON runs were byte-identical. The experiment report also records 3,109 handwritten lines and notes that the change crossed MPE's merge-checkpoint threshold; the records do not show that this size caused avoidable rework, so line count alone is not treated as a failure.

**Root cause vs. unknown.** The full-suite failures were repository baseline problems, not regressions from the CRM proof: the dashboard snapshot lagged the registry and the registry schema did not permit some statuses in use. No evidence supports a claim that the run searched too long or took the wrong implementation path. The task's optionality worked as intended by rejecting Kanban without a consumer.

**Prevention.** `NO_CHANGE` for EXP-25. Preserve the before/after test comparison and avoid turning a bounded proof into a cleanup of unrelated failures. Do not create a policy to build UI or fix all pre-existing failures during component-extraction experiments.

Evidence: `experiments/exp-25-atomic-crm-component-extraction/RESULTS.md` → Checkpoint results, Checks run, pre-existing repository breakage, and changed files; `evidence/proof_run.json` and `evidence/proof_run.log`.

### EXP-27 Paperclip orchestration patterns — PASS

**Task.** Test five Paperclip-inspired patterns without installing Paperclip or adding a parallel control plane.

**Executor actions.** The run pinned/audited the donor, tested goal ancestry on EXP-25 and EXP-27 records, stress-tested a file-backed lease with 3 rounds × 8 concurrent processes, resumed a stopped workflow in a fresh interpreter, and checked retry/tool/time/budget limits plus the existing MPE approval path. It regenerated the documented dashboard views after adding the registry record; it did not change MPE governance or production paths.

**Verified friction and checks.** CP-02 measured manual/no-packet rediscovery at 3 files / 49,656 bytes for EXP-27 and 2 files / 43,429 bytes for EXP-25; the derived packets were 2,316 B and 2,013 B, preserved all eight genealogy answers, and required 0 rediscovery steps in the fresh process. CP-03 found a race defect in an initial lease proof: a second process could take over between lock creation and owner-record initialization. A bounded wait now reports `LEASE_INITIALIZING`; the final 3 × 8 concurrency evidence shows one winner per race and zero duplicate executions. CP-04 resumed with 21/21 handoff fields, zero rediscovery, and zero replayed steps.

**Source-record discrepancy.** `evidence/cp02.json`, `evidence/proof_run.json`, and the harness agree on the measurements above and a mean of 46,542.5 B scanned without a packet. `RESULTS.md` instead says 49,584 B, 43,357 B, and 46,470.5 B. Each case and the mean are 72 B lower in the prose. The prose also says both packets have three hashed source refs, while the machine evidence has three for EXP-27 and **two** for EXP-25. The exact reason is not recorded. The byte discrepancy is about 0.15% of the baseline and does not change the direction of the result, but the mismatch is real and a deterministic comparison can flag it. This retrospective uses the machine evidence and does not rewrite the closed EXP-27 result.

**Root cause vs. unknown.** The context search cause is the task genealogy being spread over the registry and per-experiment files, with no compact handoff packet in the no-packet arm. The lease defect's cause and successful fix are recorded. The CP-02 prose mismatch's underlying cause is unknown; manual transcription/staleness is plausible but not proven. The full test suite's baseline failures remained mostly pre-existing; the run's registry/dashboard refresh was the documented path, not avoidable scope creep.

**Prevention.** Use R1 only for context-heavy tasks; the lease defect already had a deterministic experiment-local concurrency test, so do not add a second general MPE check from that incident. For the small CP-02 reporting mismatch, `NO_CHANGE` to global governance or a new report-generation tool; keep the discrepancy recorded as evidence.

Evidence: `experiments/exp-27-paperclip-orchestration-patterns/RESULTS.md` → CP-02, CP-03, Checks run, and limitations; `evidence/cp02.json` and `evidence/proof_run.json`; `evidence/cp03.json`; `evidence/cp04.json`.

## Five required problem classes

| Class | Run evidence | Assessment and decision |
|---|---|---|
| Long search for file/context | EXP-27 CP-02, reproduced against EXP-25 and EXP-27 ancestry. | **Real and measured.** Root cause is split task ancestry; use a compact derived packet selectively (R1). This is a file/byte proxy, not measured human waiting time. |
| Wrong or unnecessary execution path | EXP-24 one-time `hyperframes init` fallback installed ten unrequested skills; one preview and one render were bounded by the task. EXP-25 avoided unneeded Kanban; EXP-27's registry refresh followed `dashboard/README.md`. | **One real tool-side-effect issue, not a repeated MPE rule failure.** Apply only the HyperFrames-specific guard in the pending Phase 2 task (R2). The other two paths were justified by their contracts. |
| Error a deterministic check could catch | EXP-27 CP-03 race found and fixed by its concurrency proof; EXP-27 CP-02 JSON/prose mismatch; EXP-24 lint reported an error without a rule/location. | **Real but differently resolved.** The race's existing experiment check caught it before PASS. The 72-byte reporting drift is small and one-off: record it, no new MPE-wide check. The lint finding is not actionable without its exact diagnostic. |
| Insufficient/excessive instruction | EXP-24 recovery records a prior hang but not its cause; closure-first limits were followed by the recovered run. The unrequested `init` side effect was not spelled out. EXP-25/27 followed bounded instructions and made their no-scope-expansion choices explicit. | **Only a local omission is evidenced.** Add the conditional Phase 2 note (R2). Do not rewrite `AGENTS.md`, add a coding-standards file, or infer a cause for the lost run. |
| Repeated environment/tooling problem | EXP-24's Chrome/TLS/FFmpeg blockage occurred in one run; no equivalent failure is recorded in EXP-25/27. The same registry-status schema drift appears in EXP-25 and EXP-27 suite baselines; current EXP-28 baseline also fails on that pre-existing mismatch and stale generated views. | **Mixed.** Renderer blockage is not proven recurrent. The repository test drift is recurrent and already visible to deterministic tests; it is outside this retrospective's scope. Refresh required generated registry views for this EXP-28 registry update, but do not modify the status contract or unrelated dashboard HTML here. |

## Recommendations with the required evidence contract

### R1 — Use the existing context-packet pattern for context-heavy handoffs (**recommended; immediately usable**)

- **Evidence:** EXP-27 `evidence/cp02.json`: EXP-27 no-packet arm 3 files / 49,656 B vs. a 2,316 B packet; EXP-25 no-packet arm 2 files / 43,429 B vs. a 2,013 B packet. Both preserved eight genealogy answers; fresh-process packet arm had 0 rediscovery steps. The EXP-25 machine record has two hashed source refs, although its result prose says three. The `RESULTS.md` prose is 72 B lower per case; these calculations use the machine JSON and disclose the mismatch above.
- **Root cause:** Context needed to resume (registry intent, checkpoint chain, task/stop conditions) is distributed among canonical files. A fresh executor has to rediscover it when no brief is handed over.
- **Minimal change:** For a task that actually spans several context files, place a short **derived** ancestry brief in the existing task/handoff: project, goal, checkpoint/task, stop conditions, and source paths + digests. Do not persist a competing source of truth, add a memory store, or add this brief to routine one-file tasks.
- **Expected effect:** On a comparable context-heavy handoff, reduce measured input retrieval from about 46.5 KB / 2.5 file reads to a roughly 2.2 KB packet and 0 rediscovery steps (the observed proxy is ~95.35% fewer bytes; not an elapsed-time or VRU claim).
- **Risk of false improvement:** Two synthetic/fixed cases are too small to show generality. A packet can become stale or add more context than it saves. It can also be mistaken for authority rather than a derived view.
- **Verification:** On the next comparable, separately authorized run, give a fresh isolated executor only the packet; require all eight genealogy answers to match the canonical files, verify each digest, count packet bytes/reads and rediscovery steps, and compare with a no-packet baseline. Skip the packet if the task is not context-heavy.

### R2 — Bound HyperFrames bootstrap side effects in the existing EXP-24 Phase 2 task (**applied task-locally**)

- **Evidence:** EXP-24 `UPSTREAM_AUDIT.md` and `RESULTS.md` record the `init` fallback installing ten agent skills outside the repository, Chrome download failure at TLS setup, and FFmpeg absent. Phase 2 already makes HyperFrames optional and Remotion preferred.
- **Root cause:** The Phase 1 task bounded the number of attempts but did not describe `init`'s skill-install side effect or require a chosen-renderer prerequisite/side-effect check before bootstrapping.
- **Minimal change:** Add a short conditional guard to `experiments/exp-24-hyperframes-pr-video/ARENA_TASK.md`: if HyperFrames is selected, reuse the existing local composition rather than rerunning broad `init` unless side effects have first been inspected and isolated; check only the chosen renderer's documented prerequisites before preview/render and stop at a concrete sandbox/network blocker. This edit was applied; no global MPE instruction changed.
- **Expected effect:** Avoid a repeat of the unrequested global skill install and surface a known browser/codec blocker before spending a render attempt or troubleshooting the general sandbox.
- **Risk of false improvement:** A prerequisite check can reject a valid renderer that provisions its browser locally. The guard is therefore conditional, allows an explicitly reviewed project-local setup, and does not replace the task's acceptance test.
- **Verification:** In the next authorized EXP-24 Phase 2 run, if HyperFrames is selected, record the exact preflight command and renderer version; verify no global agent-skill/config mutation and no second bootstrap after the first concrete blocker. If Remotion remains the selected baseline, do not apply HyperFrames-specific checks to it.

### R3 — Add an automatic retrospective hook and promote every finding to global instructions (**rejected**)

- **Evidence:** Only EXP-24 shows the renderer/initializer friction; EXP-25 and EXP-27 completed their bounded scopes, and the EXP-27 lease issue was already caught by its test. No common execution-friction root cause appears across all three. The existing MPE `AGENTS.md`, Scope & Change Control, context map, and experiment task boundaries already define governance and navigation.
- **Root cause of the proposed overreach:** Treating one-off session signals as cross-project policy would confuse observation with recurrence and duplicate controls already present in MPE.
- **Minimal change:** `NO_CHANGE`—do not add an after-every-run hook, global rule, new standards file, or automatic memory promotion.
- **Expected effect if rejected:** Avoid always-on context and review overhead, false rules, and a second governance path while retaining the two useful, local improvements above.
- **Risk of false improvement:** Some repeated issue might go unnoticed if all retrospectives are skipped. The user-invoked trigger remains available for difficult runs; use evidence across runs before promoting a broader rule.
- **Verification:** In any future promotion proposal, require recurrence or high, evidenced cost across independent runs, show it maps to an existing instruction/check location, and demonstrate that the change prevents a concrete regression without firing on valid work. No such evidence exists for an automatic hook now.

### `NO_CHANGE` for the remaining candidates

- Do not add a global environment check from one Arena-only Chrome/FFmpeg failure.
- Do not add another lease check: EXP-27 already had a deterministic concurrency check that found and fixed the race before its final PASS.
- Do not add a generic lint rule from EXP-24's diagnostic-free “1 error, 6 warnings” summary; the rule and location are unknown.
- Do not change EXP-27's closed historical report as part of EXP-28. The 72-byte CP-02 summary mismatch is recorded here against the machine evidence; a general numeric-reporting tool is not justified by one small discrepancy.
- Do not fix the repository's unrelated registry-status schema or dashboard HTML during this experiment. The current tests identify the existing mismatch; changing that source contract is a separate decision, not a retrospective side effect.

## Measured benefit and limits

The measurable comparator is EXP-27 CP-02's existing **manual/no-packet rediscovery arm** vs. its compact packet arm:

| Measure | No packet / manual rediscovery | Derived packet | Difference |
|---|---:|---:|---:|
| Mean bytes scanned / packet | 46,542.5 B | 2,164.5 B | 95.35% fewer bytes (~21.5× smaller) |
| Fresh-worker rediscovery steps | 2.5 on average (3 and 2 source-file reads) | 0 rediscovery steps once the packet is supplied | 2.5 fewer rediscovery steps |
| Genealogy answers | Independently derived from 2–3 source files | 8 of 8 preserved in each case | No loss in the two tested cases |

The no-packet row is computed from the machine evidence, not the inconsistent bytes/source-ref counts in EXP-27 `RESULTS.md`. This is a reproducible retrieval-cost proxy for the navigation recommendation. It does **not** measure elapsed human/agent minutes or prove that EXP-28's retrospective method itself saves time. Historical raw Arena event logs were not available for all runs, so run durations, total tool calls, and cost cannot be reconstructed. No VRU is claimed.

## Validation, scope, and boundary

- All three named runs were read; EXP-24 Phase 1, not Phase 2, was analyzed as the completed run.
- All five required problem classes are explicitly assessed. Unsupported causes are labeled unknown; low-cost one-off candidates default to `NO_CHANGE`.
- The applied EXP-24 instruction is conditional and task-local. No global instruction, gate, contract, runtime, source-of-truth hierarchy, production code, or automatic trigger changed.
- No prototype/harness was added: existing experiment evidence already supplied a deterministic comparator and actual failure/fix records. A new retrospective classifier would be underpowered and overfit to three selected runs.
- **Package validator:** `python3 scripts/validate_package.py .` — PASS.
- **Dashboard build/deploy checks:** `npm run check` — PASS, 43/43 checks; generated views are 355 px wide and test at 14 px text.
- **Registry/evidence validation:** registry parses as JSON; EXP-28 is a single `PASS` entry; all relative evidence links exist; `git diff --check` — PASS.
- **Generated registry views:** the documented Reladraw refresh was run; `tests.test_registry_to_reladraw` and all dashboard freshness/size/text checks pass.
- **Test baseline before EXP-28 edits:** `PYTHONHASHSEED=0 python3 -m unittest discover -s tests` — 369 tests, 13 failures, 1 skipped. Failures included existing unsupported `PARTIAL`/`RETIRED` registry statuses, missing mobile-status references in `dashboard/public/index.html`, and stale generated registry views/text.
- **Full suite after EXP-28 edits:** same command — 369 tests, **7 failures**, 1 skipped. The seven are the four pre-existing registry-status schema mismatches and three pre-existing mobile-status references missing from `dashboard/public/index.html`; the six stale generated-view/text failures from baseline are gone. No new failure was introduced; the new EXP-28 registry status is `PASS` (allowed by the schema).
- **Targeted dashboard tests:** `python3 -m unittest tests.test_dashboard_registry_views tests.test_registry_to_reladraw -v` — generated portfolio, current registry text, width, and freshness checks pass; 3 subtests remain failing because the existing `index.html` does not reference the `FAIL`, `PARTIAL`, and `RETIRED` mobile SVGs. This is the same known baseline defect, not fixed here.
- No deep-change boundary was encountered. The result does not authorize contract/schema changes, production integration, or automation.
- The PR is opened but must not be merged as part of EXP-28.
