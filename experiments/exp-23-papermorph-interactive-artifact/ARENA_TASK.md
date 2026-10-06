# Arena task — EXP-23 Papermorph

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
