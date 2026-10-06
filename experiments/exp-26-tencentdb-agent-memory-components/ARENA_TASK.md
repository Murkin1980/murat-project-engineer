# Arena Task — EXP-26 TencentDB Agent Memory component extraction

Decision: **REUSE_COMPONENT**

Repository: `Murkin1980/murat-project-engineer`

Read mandatory governance, then:
- `experiments/exp-26-tencentdb-agent-memory-components/README.md`
- EXP-15 baseline files referenced there.

## Goal

Do NOT install/adopt TencentDB Agent Memory as a platform.

Test whether two donor mechanisms improve the existing EXP-15 memory baseline:

1. symbolic short-term compaction;
2. layered progressive-disclosure recall.

## Execute

1. Audit current `TencentCloud/TencentDB-Agent-Memory`; pin upstream commit/tag and license.
2. Map relevant components against EXP-15; reject duplicates.
3. Freeze a small EXP-15-compatible comparison set.
4. Compare:
   - A: EXP-15 baseline;
   - B: symbolic compaction;
   - C: layered recall.
5. Use the smallest local deterministic harness possible.
6. Measure recall correctness, provenance, context/tokens, reads/rediscovery, isolation, false positives, drill-down cost, and implementation complexity.
7. Preserve evidence under the EXP-26 folder.
8. Run repository-required checks.
9. Stop with:
   - PASS / PARTIAL / FAIL
   - ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT
   - exact reusable component(s), if any.

No new repo, service, database, vector store, autonomous writes, Router change, or production integration.
