# The Gates: Filter, Deep-Change, Minimal Diff

## page 3

Allowed primary decisions:
`EXTEND_EXISTING`
`REUSE_COMPONENT`
`MERGE`
`EXPERIMENT`
`HOLD`
`NEW_REPOSITORY`
`REJECT`
Default preference: strengthen existing systems before creating parallel ones.
The filter is required for substantial new ideas, not for every routine bug
fix.
6. Deep-change gate
Do not execute a substantial change without explicit approval when it:
    changes fundamental architecture;
    breaks an approved invariant;
    changes a public contract;
    requires data migration;
    changes the source of truth;
    introduces a new infrastructure platform;
    creates a new repository;
    materially changes security boundaries;
    creates unapproved recurring cost;
    is difficult to reverse;
    exceeds the approved checkpoint boundary.
Stop only the deep-change portion. Continue safe work that remains inside the
already approved scope.
7. Implementation order
Before adding new code, check in this order:
1. Existing code and established project patterns.
2. Standard library / built-in platform capability.
3. Already-installed dependencies.
4. Existing internal reusable components.

## page 4

5. Only then add new code or a new dependency.
Do not create a new abstraction when the existing mechanism solves the task
sufficiently.
8. Minimal diff
For a small task, prefer a targeted edit.
Avoid unless required:
    unrelated refactors;
    large renames;
    file moves;
    rewriting working modules;
    extra architecture layers;
    new configuration systems;
    generic frameworks for one use case;
    speculative future-proofing.
Every changed line should have a clear relationship to the current task.
9. Fix the root cause
Do not hide a problem behind extra checks, fallback layers, or workarounds
when the source can be corrected safely.
Root-cause work is not permission for a broad refactor.
Choose the smallest change that genuinely fixes the cause.
10. Do not design hypothetical future needs
Do not add:
    extensibility without a real consumer;
    a generic API without a second concrete use case;
    unused settings;
    compatibility layers without a current requirement;
    adapter/interface/factory layers only for possible future work;
    infrastructure for an unapproved feature.
Future opportunity is separate scope.
