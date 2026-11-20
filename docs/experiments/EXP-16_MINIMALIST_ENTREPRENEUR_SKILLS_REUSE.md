# EXP-16 — MINIMALIST ENTREPRENEUR SKILLS REUSE
## Reuse selected Sahil Lavingia / Minimalist Entrepreneur decision patterns inside MPE and Business Discovery

**Date:** 2026-09-15  
**Primary governing repository:** `Murkin1980/murat-project-engineer`  
**Applicable repository:** `Murkin1980/business-discovery`  
**Murat Project Engineer New Idea Filter decision:** `REUSE_COMPONENT`  
**Experiment status:** `QUEUED / NOT STARTED`  
**New repository:** `NO`  
**Fork of `slavingia/skills`:** `NO`  
**Production integration:** `NO`  
**Deep change:** `NOT AUTHORIZED`

---

# 0. EXECUTIVE DIRECTIVE

Reuse a small subset of decision patterns from Sahil Lavingia's *The Minimalist Entrepreneur* skills as bounded decision-support components inside the existing Murat Project Engineer and Business Discovery workflows.

Do not create another agent, product, repository, workflow engine, database, memory layer, or source of truth.

The experiment must answer one practical question:

> Does adding a lightweight Minimalist Review to existing MPE decisions produce measurably better simplification and business-value decisions than the current Murat Project Engineer New Idea Filter alone?

The goal is not to adopt the full external skill pack. The goal is to test whether five selected patterns improve decisions we already make.

---

# 1. SOURCE REFERENCES

Reference article:

- https://pimenov.ai/articles/sahil-lavingiya-kniga-v-navyki-ii

Original skill repository:

- https://github.com/slavingia/skills

External material is a reference source only. It is not authoritative for MPE architecture, governance, project status, evidence, security, or execution.

---

# 2. MURAT PROJECT ENGINEER NEW IDEA FILTER

```text
MURAT_PROJECT_ENGINEER_NEW_IDEA_FILTER

Idea:
Reuse selected Minimalist Entrepreneur decision patterns inside existing MPE and Business Discovery workflows.

Decision:
REUSE_COMPONENT

Why:
- MPE already owns project-level decision governance and new-idea filtering.
- Business Discovery already owns problem validation, intake, interview, ontology and scoring.
- The external skills overlap strongly with existing responsibilities.
- A new repository or fork would duplicate logic and maintenance.
- The useful value can be tested as a small decision layer with no runtime dependency.
- The experiment is reversible and can be removed without affecting existing workflows.
- No deep architecture change is required.

Do not:
- fork slavingia/skills for production use;
- create a new agent dedicated to minimalist review;
- add a new database or persistent service;
- make the external repository a runtime dependency;
- copy all ten skills by default;
- change MPE source-of-truth rules;
- change Business Discovery architecture before experiment evidence exists.
```

---

# 3. SELECTED COMPONENTS TO REUSE

Only five patterns are in scope.

## 3.1 `validate-idea`

Purpose:
- verify that a real user problem exists;
- seek evidence of willingness to pay, commit, switch, or spend effort;
- distinguish interest from demand.

Primary home:
- `business-discovery`

MPE use:
- evidence input for `EXPERIMENT`, `HOLD`, `REJECT`, or `EXTEND_EXISTING` decisions.

## 3.2 `mvp`

Purpose:
- identify the smallest test that can prove or disprove value;
- remove features that are not required for the learning objective.

Primary home:
- `murat-project-engineer`

Required question:

> What is the smallest experiment that would earn the right to invest further?

## 3.3 `processize`

Purpose:
- prefer a manual or simple repeatable process before automating it;
- automate only after the process has demonstrated value and stable structure.

Primary home:
- shared principle across MPE and Business Discovery.

Default rule:

```text
MANUAL PROOF -> REPEATABLE PROCESS -> AUTOMATION
```

Automation must not be used as evidence that the underlying business process is valuable.

## 3.4 `pricing`

Purpose:
- test whether pricing, unit economics, willingness to pay, margin, and value capture support the idea.

Primary home:
- `business-discovery`

This component is especially relevant to business experiments, productized services, furniture product experiments, paid automation and commercial SaaS decisions.

## 3.5 `minimalist-review`

Purpose:
- act as a final simplification pass after the normal MPE New Idea Filter;
- challenge infrastructure, scope and implementation assumptions.

Primary home:
- `murat-project-engineer`

Canonical three questions:

1. Does a real user need the result?
2. Can the same value be proven in a simpler way?
3. What is the minimum experiment that earns the right to invest further?

Optional fourth question when automation or infrastructure is proposed:

4. Has the underlying process already been proven manually or with a simpler tool?

---

# 4. ARCHITECTURAL BOUNDARY

```text
MPE = PROJECT / CHANGE DECISION GOVERNANCE
Business Discovery = PROBLEM / DEMAND / BUSINESS VALIDATION
Minimalist patterns = BOUNDED REVIEW COMPONENTS
External skill repository = REFERENCE ONLY
```

The reused patterns must not become:

- a parallel governance framework;
- a second New Idea Filter;
- an execution engine;
- an agent runtime;
- an approval authority;
- a source of truth;
- a mandatory external dependency.

MPE remains authoritative for project-level change disposition.

Business Discovery remains authoritative for its own discovery contracts, intake, interview, ontology and scoring.

---

# 5. MINIMALIST REVIEW — PROPOSED BOUNDED FORM

For any substantial new idea that already passed through the Murat Project Engineer New Idea Filter, the experiment may add this compact review:

```yaml
minimalist_review:
  real_user_need:
    evidence: ""
    confidence: LOW | MEDIUM | HIGH

  simpler_proof:
    exists: true | false
    description: ""

  minimum_experiment:
    hypothesis: ""
    smallest_test: ""
    measurable_success: ""
    stop_condition: ""

  process_maturity:
    manual_process_proven: true | false | not_applicable
    automation_justified: true | false | not_applicable

  complexity_removed:
    components_not_needed_now: []

  recommendation:
    KEEP_DECISION | SIMPLIFY | HOLD | REJECT
```

This review does not replace the primary MPE disposition. During EXP-16 it produces advisory evidence only.

---

# 6. BUSINESS DISCOVERY APPLICATION

Business Discovery should reuse the five patterns only where they strengthen existing discovery outputs.

## Intake / interview

Add emphasis on observable evidence:

- Who has the problem now?
- How is it solved today?
- What does the current workaround cost in money, time, risk or lost revenue?
- Has the user already tried to solve it?
- What action would demonstrate real commitment?

## Scoring

Where relevant, consider evidence for:

- urgency;
- willingness to pay;
- frequency of the problem;
- current workaround cost;
- reachable first customers;
- gross-margin or unit-economic plausibility;
- smallest viable manual test.

Do not expand the ontology or scoring model merely because these concepts exist. Any schema change requires separate evidence and the normal MPE filter.

## Output

A Business Discovery result may recommend a minimal experiment rather than software development.

Examples:

- sell manually before building checkout automation;
- create a single product offer before a catalog platform;
- run five customer interviews before building a configurator;
- price and deliver one paid pilot before implementing a scalable workflow.

---

# 7. EXP-16 TEST DESIGN

Run a retrospective comparison on five real decisions that are already sufficiently documented.

Candidate cases:

1. Qoopia cross-session memory experiment.
2. OpenObserve observability candidate.
3. Telegram Rich Messages experiment.
4. Furniture business experiment focused only on sliding-door wardrobes.
5. Salamat Projects Dashboard product-boundary decision.

For each case, produce two views:

### A. Baseline

Use the recorded MPE / project decision as it existed without EXP-16.

### B. Minimalist Review

Apply only the bounded questions in this document.

Record:

```yaml
case:
baseline_decision:
minimalist_recommendation:
decision_changed: true | false
simplification_found: true | false
simplification:
new_business_evidence_required:
complexity_removed:
would_have_saved_time_or_cost: true | false | unknown
notes:
```

Do not rewrite historical decisions to make the experiment look successful.

---

# 8. PASS / FAIL CRITERIA

## PASS

EXP-16 passes if all of the following are true:

- The added review does not create a second governance system.
- At least 2 of 5 cases produce a concrete, useful simplification, stronger validation requirement, or avoidable-cost finding.
- At least 4 of 5 cases preserve the original high-level MPE disposition OR any changed disposition is supported by clear evidence that the original decision would have been unnecessarily complex.
- The review can be completed from existing project evidence without installing the external skill pack.
- No new repository, service, database or runtime dependency is required.
- Business Discovery can reuse the relevant questions without mandatory schema expansion.

## FAIL

EXP-16 fails if any of the following are true:

- The review merely duplicates the existing New Idea Filter with no useful additional signal.
- It routinely changes decisions without stronger evidence.
- It adds bureaucracy but does not remove implementation scope, risk, time or cost.
- Adoption requires maintaining a fork of the external repository.
- It requires a new agent, runtime, service or source of truth.
- It creates conflicting authority between MPE and Business Discovery.

## Terminal states

```text
PASS
FAIL
HUMAN_REQUIRED
```

---

# 9. ADOPTION RULE AFTER EXPERIMENT

If EXP-16 = `PASS`:

- integrate the three-question Minimalist Review into the existing MPE New Idea Filter workflow as a small post-filter review;
- reuse `validate-idea`, `processize`, and `pricing` questions inside existing Business Discovery contracts where they naturally fit;
- keep the implementation local to existing repositories;
- do not copy the full external plugin pack.

If EXP-16 = `FAIL`:

- keep this document as evidence;
- do not add the review to canonical workflows;
- continue using the current MPE New Idea Filter and Business Discovery process unchanged.

If EXP-16 = `HUMAN_REQUIRED`:

- stop before any deep-change, governance change, scoring-model change, or external runtime integration;
- request explicit user approval.

---

# 10. REPOSITORY PLACEMENT

Canonical experiment copy:

```text
Murkin1980/murat-project-engineer
  docs/experiments/EXP-16_MINIMALIST_ENTREPRENEUR_SKILLS_REUSE.md
```

Applicable reference copy:

```text
Murkin1980/business-discovery
  docs/EXP-16_MINIMALIST_ENTREPRENEUR_SKILLS_REUSE.md
```

The content should remain identical while EXP-16 is active. MPE is the governing source for the experiment result.

No copy is required in other project repositories at this stage. Project-specific teams consume the rule through MPE; duplicating it across every repository would create maintenance drift.

---

# 11. CURRENT NEXT ACTION

Run the five-case retrospective only when EXP-16 reaches active experiment priority.

Until then:

```text
STATUS = QUEUED / NOT STARTED
NO PRODUCTION CHANGE
NO FORK
NO NEW REPOSITORY
NO NEW AGENT
NO NEW SERVICE
```
