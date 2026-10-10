# Authority, Done, Report

## page 9

stop when the files are mechanically related.
Never optimize for a smaller line count by hiding complexity, compressing
code, reducing tests, weakening evidence, or combining unrelated concerns.
22. Merge and deploy authority
Successful implementation does not automatically grant merge/deploy authority.
Merge or deploy automatically only when that authority is already granted by
the owner or project workflow.
If authority exists, do not ask again after every technical check.
If not, stop at the permitted boundary and preserve evidence.
23. Definition of done
The task is done when:
    requested behavior works;
    the root cause is addressed;
    scope remains within the approved boundary;
    mandatory verification passes;
    necessary tests are updated;
    temporary artifacts are removed;
    superseded unnecessary code is removed safely;
    no known blocker remains inside current scope;
    required evidence is recorded.
Do not stop at a plan, partial implementation, or the first green test.
24. Final report
Report briefly:
    **RESULT:** PASS / BLOCKED / PARTIAL
    **Changed:** what actually changed.
    **Verified:** checks and results.
    **Remaining:** only real unresolved items.
If complete, do not invent the next checkpoint.
Short form

## page 10

**Read scope rules first -> respect the checkpoint -> reuse before building ->
make the smallest correct change -> fix the root cause -> verify real behavior
-> leave evidence -> stop at the approved boundary.**
