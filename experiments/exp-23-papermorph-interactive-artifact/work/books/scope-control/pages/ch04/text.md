# Scope Under Pressure: Growth, Parallel Systems, Merge Pressure

## page 7

If a test conflicts with newly approved behavior, verify the spec first, then
update the implementation and test to match the approved contract.
Do not add test-only production behavior.
18. If the plan grows
If work starts producing new layers, infrastructure, frameworks, broad
refactors, extra features, generalized systems, many new files, or repeated
checks, compare them with the original requirement.
Ask:
Is this necessary to complete the current task?
If not, remove it from the change.
19. No parallel systems by default
Before creating a new service, worker, API, storage layer, dashboard, adapter,
workflow, agent, utility, library, or repository, check whether an existing
system can be extended or reused.
A parallel system requires explicit justification and the New Idea Filter.
20. Evidence
After substantial work, leave enough evidence in the project's established
format for the next executor to continue without rediscovery.
As applicable, include:
    what changed;
    files/components affected;
    test/typecheck/build results;
    commit SHA / branch / PR;
    deploy status;
    known limitations;
    next authorized action.
Do not create duplicate evidence formats when the repository already defines
one.
21. Change-size and merge-pressure control

## page 8

Line count is a risk signal, not a productivity target and not a reason to
interrupt correct work mid-change.
Measure **meaningful changed lines** as additions + deletions on the current
branch/PR relative to its merge base with the default branch.
Exclude from the threshold when they are predominantly mechanical and
separately reviewable:
    lock files;
    generated code or generated artifacts;
    vendored third-party files;
    snapshots;
    large fixtures, captures, datasets, evidence payloads, or compiled/minified output;
    formatting-only bulk changes.
Do not split coherent code merely to stay below a number. Do not stop in the
middle of an atomic edit, migration, schema transition, repair, or
verification cycle.
Use these thresholds as merge pressure:
    **0-1,500 meaningful changed lines · NORMAL.** Continue inside the approved scope.
    **1,500-3,000 · WATCH.** Keep scope tight. Prefer finishing the current atomic task before taking adjacent work.
    **>=3,000 · MERGE CHECKPOINT.** Do not interrupt the current atomic task. At the next stable, testable bound
    **>=5,000 · STRONG MERGE PRESSURE.** Finish the already-started bounded task and verification, but do no
    **>=10,000 meaningful handwritten/semantic lines · EXCEPTION.** Continue only when the change is genuinely
These thresholds are **not hard stop signals for an external coder who is in
the middle of valid work**. The safe sequence is:
1. complete the current atomic operation to a coherent state;
2. make the state testable and resumable;
3. run the required verification;
4. record evidence/handoff;
5. then integrate, split, or request the required decision before expanding scope.
A checkpoint may be merged while its overall outcome is `BLOCKED` when the
completed implementation is coherent, tests/checks pass, unresolved blockers
are external or explicitly isolated, and merging does not weaken the default
branch.
Changed-file count is a secondary warning signal: around **25+ meaningful
files** should prompt the same scope/diff review, but it is not an automatic
