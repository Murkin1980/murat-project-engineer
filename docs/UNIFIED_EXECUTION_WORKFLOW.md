# Unified MPE Execution Workflow

Status: ACTIVE / MANDATORY
Architecture: Option A+ boundaries unchanged

This is one bounded, evidence-first execution process. It connects portfolio choice, task scoping, safe delegation, verification, and the final checkpoint. It does not add a queue, scheduler, persistent agent, autonomous workflow engine, or new authority.

## 1. Decide where the work belongs

1. Apply the New Idea Filter whenever the request is a new substantial idea. Record exactly one disposition.
2. Apply the **Value Gate**: name a measurable business or user outcome and the smallest worthwhile outcome.
3. Apply the **Scope Gate**: name the target project, in-scope and out-of-scope components, allowed effects, and rollback.
4. Apply the **Deep-change Gate** against the project foundation and MPE boundaries. A detected deep change, architectural conflict, or missing required approval ends this run as `HUMAN_REQUIRED`; do not start implementation.

For an already-approved bounded task, record `idea_disposition: NOT_APPLICABLE` and the source task instead of repeating the portfolio decision.

## 2. Freeze the Task Packet

Create `contracts/TASK_PACKET.md` before any writer begins. The packet is the shared contract for the main executor, reviewers, and delegates. It binds value, scope, acceptance criteria, verification, skills, authority, rollback, and stop conditions.

An implementation may not silently broaden the packet. New scope returns to Scope Gate; a newly discovered deep change returns to the user-approval stop.

## 3. Pass the Skillization Gate and choose execution

Before acting, determine whether an available skill, project skill, or explicit user-named skill applies.

- If applicable, read and follow it before the task action; record the skill and version/reference in the packet.
- If none applies, record `NO_APPLICABLE_SKILL` with the search/reason. Do not create a new skill merely to pass the gate.
- If the task could repeat across projects and a reusable skill would materially reduce risk or effort, record `SKILL_CANDIDATE` as a follow-up decision after the current run. Skill creation itself remains a new idea subject to the New Idea Filter.

Choose the existing FAST, VERIFIED, or DEEP-CHANGE playbook only after this gate. One bounded Expert remains the default.

## 4. Execute or delegate safely

Delegation is a bounded handoff, not autonomous project ownership.

- Each delegate receives a narrowed Task Packet or typed Handoff with the goal, allowed inputs, allowed files, acceptance evidence, stop conditions, and explicit `do_not_change` list.
- One writer owns a worktree at a time. Concurrent writers require isolated worktrees, an explicit merge owner, and `worktree_collision_check`; otherwise delegates are read-only and report evidence.
- Delegates cannot create repositories, alter architecture/foundation, modify approvals, access or disclose credentials, deploy/publish, contact third parties, or trigger irreversible external effects unless those actions are explicitly authorized in the parent packet and the relevant human gate has passed.
- A delegate that finds new scope, a deep change, a security concern, or insufficient evidence must stop and return `BLOCKED` / `HUMAN_REQUIRED`; it must not improvise a workaround.
- The coordinator verifies returned artifacts and retains only observable handoffs, never hidden reasoning or durable agent state.

## 5. Prove the change

Run applicable deterministic technical checks first: scope, secret scan, build/typecheck/lint/tests, acceptance mapping, rollback, and project-specific checks. A hard-gate failure cannot be overridden by a reviewer.

Then collect `contracts/BROWSER_EVIDENCE.md` for every browser-observable acceptance criterion. If none exists, record `NOT_APPLICABLE` with a reason. Required browser evidence that cannot be collected is `BLOCKED`, not PASS.

After the evidence is collected, capture the exact verified files with:

```bash
python scripts/verification_state.py capture --state evidence/verification-state.json --file path/to/file
python scripts/verification_state.py check --state evidence/verification-state.json
```

The state is deterministic and file-scoped. A changed, removed, or altered verified file changes the state from `VERIFIED` to `UNVERIFIED` (exit code `3`). That automatically invalidates the previous technical, browser, and reviewer evidence for every affected criterion. Re-run the affected checks, refresh Browser Evidence, capture a new state, and then continue. This mechanism does not track unrelated files; the final Git diff gate still protects the declared scope.

## 6. Final Git-diff checkpoint and terminal state

Only after `verification_state.py check` returns `VERIFIED`:

1. inspect `git diff` and `git status` against the Task Packet's scope;
2. confirm the changed-file list, no unintended artifacts, and rollback reference;
3. record all gate results, Browser Evidence, verification-state artifact, reviewer verdict (when used), and final commit/rollback in the Run Report;
4. emit `PASS` only when every applicable gate passes.

Any mutation after this checkpoint resets the checkpoint to `UNVERIFIED` and returns the run to step 5. `PASS` is therefore a final state of a specific diff and evidence set, not a sticky label for a moving worktree.

## Terminal outcomes

- `PASS`: all applicable gates, Browser Evidence, verification state, and final Git diff pass.
- `REWORK`: a correctable technical, evidence, or scope issue remains within the approved packet.
- `BLOCKED`: required access/evidence/tooling is unavailable, or a hard blocker cannot be resolved safely.
- `HUMAN_REQUIRED`: a deep change, approval, irreversible effect, or architectural conflict needs an explicit user decision.
