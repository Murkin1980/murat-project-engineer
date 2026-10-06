# Arena Task — EXP-24 HyperFrames PR → Video

Decision: **EXPERIMENT**

Repository: `Murkin1980/murat-project-engineer`

Work only in this repository. Do not create a new repo, video service, database, queue, auth layer, or automatic publishing path.

Read `AGENTS.md`, mandatory governance, then:
- `experiments/exp-24-hyperframes-pr-video/README.md`

## Objective

Use `heygen-com/hyperframes` as a reusable component to test:

```text
one real completed Murat PR
→ evidence-backed summary
→ small structured storyboard
→ HyperFrames composition
→ preview
→ deterministic ~30–60s MP4
```

## Required execution

1. Audit HyperFrames upstream: license, runtime, render path, dependencies, determinism constraints.
2. Select one bounded completed Murat PR with clear evidence and no sensitive data.
3. Freeze the minimum PR evidence needed for a reproducible fixture.
4. Define a narrow PR-evidence → storyboard contract. Do not create a generic media DSL.
5. Build the smallest composition needed for that fixture.
6. Attempt preview + MP4 render twice from identical input.
7. Verify grounding, comprehension, mobile readability, repeatability, cost/complexity, and reuse.
8. Run repository-required validation.
9. Preserve experiment evidence and final handoff.

## Final output

Return:
- RESULT: PASS / PARTIAL / FAIL
- adoption: ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT
- selected PR
- changed files
- tests/checks
- render artifact/hash or precise render blocker
- remaining limitation

STOP after this bounded experiment. No production integration.
