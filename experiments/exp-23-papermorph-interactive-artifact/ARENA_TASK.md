# Arena task — EXP-23 Papermorph

## Bootstrap preflight — first real post-CP-07 run

This experiment is the next real bootstrap validation after EXP-29 CP-07.

Before normal experiment work:

1. Start from fresh `main`.
2. Generate an EXP-29 Arena Bootstrap packet for **EXP-23 / CP-01** using:
   `experiments/exp-29-arena-bootstrap-harness/harness/bootstrap_builder.py`.
3. Verify the packet.
4. Continue only if verdict = `FRESH`.
5. Use the packet as startup context, but keep canonical Git files authoritative.
6. If verdict is `STALE` or `REJECTED`, stop EXP-23 execution and report the exact bootstrap defect/conflict first.
7. Do not modify the EXP-29 harness inside EXP-23. Any harness defect is a separate finding/checkpoint.

Record bootstrap-start evidence under:
`experiments/exp-23-papermorph-interactive-artifact/evidence/bootstrap/`

Capture at minimum:
- packet bytes;
- source-ref count;
- files read before first useful EXP-23 action;
- bytes read before first useful action;
- tool operations before first useful action;
- whether EXP-23 status, priority, checkpoint chain, stop rules, and next action were understood correctly from the packet;
- any rediscovery the packet failed to prevent;
- whether any stale or contradictory state was detected.

The purpose is to test whether a **fresh Arena session** can begin the next experiment from Git + bootstrap without relying on prior sandbox/session memory.

Do not start until EXP-22 Colibri has finished or Murat explicitly reprioritizes this experiment.

Read first:
1. `experiments/exp-23-papermorph-interactive-artifact/README.md`
2. `experiments/EXPERIMENT_REGISTRY.json`
3. repository governance/instructions applicable to experiments

Goal: evaluate Papermorph as a reusable document/script → structured interactive artifact pipeline, not as a new product.

Execute only the bounded checkpoints in README:
- CP-01: one short technical/business document fixture;
- CP-02: one bounded AI-serial script fixture;
- CP-03: map reusable components to existing projects.

Required behavior:
- use upstream Papermorph as close to stock as possible first;
- pin upstream commit/revision and record license;
- preserve source facts and measure manual corrections;
- do not modify production projects;
- do not alter AI-serial canon;
- do not create a new repository;
- do not build background infrastructure;
- stop on any deep-change requirement.

Return:
- READY / WARNING / BLOCKED per checkpoint;
- concise evidence under this experiment directory;
- exact manual correction count and major failure modes;
- exactly one final recommendation: REUSE_COMPONENT, HOLD, or REJECT.

No merge, production integration, deployment, or publication is authorized by this task.
