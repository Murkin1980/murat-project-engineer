# Working Cleanly: Dependencies, Adjacent, Testing

## page 5

11. Dependencies
Add a dependency only when current capabilities are insufficient and the
dependency meaningfully reduces complexity or risk for the current task.
Before adding one, answer:
Why can this not be solved reasonably with the existing stack?
If there is no convincing answer, do not add it.
12. Adjacent problems
Fix a neighboring issue now only when it:
    blocks the current task;
    prevents correct verification;
    was directly caused by the current change.
Otherwise record it briefly for separate work and keep current scope closed.
13. Replaced implementations
Remove superseded code, dead branches, temporary files, commented-out
implementations, and debug artifacts created by the task.
Before deleting an older implementation, verify that it is not required for:
    public contract compatibility;
    backward compatibility;
    migration;
    an approved fallback;
    a supported interface/version.
14. Preserve system protections
Minimal change must not weaken necessary:
    input validation;
    error handling;
    security;
    project/tenant isolation;
    idempotency contracts;

## page 6

accessibility;
    required observability;
    runtime invariants.
15. When to ask
Continue implementation, verification, and correction inside already-approved
authority.
Do not repeatedly ask whether to continue, run required tests, or fix an
obvious implementation error.
Ask or stop before:
    substantial scope expansion;
    architecture/deep-change;
    a new repository;
    unapproved spending;
    irreversible action;
    additional permissions;
    materially different product interpretations.
If the task is analysis/review only, do not modify code.
16. Testing
After a change, verify the requested behavior and its consequences.
Order:
1. Existing relevant tests.
2. Mandatory project checks.
3. New tests only for real observable behavior or regression risk.
Test contracts and behavior, not implementation trivia.
Do not repeatedly rerun unchanged successful checks without a concrete reason.
Repeat when new edits, failures, merge/rebase effects, or a specific
unresolved doubt justify it.
17. Do not code to the test
Tests verify the contract; they are not the product.
