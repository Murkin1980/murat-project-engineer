# Value Unit Economics

Status: ACTIVE / CANONICAL MPE CORE ECONOMIC MODEL
Decision: EXTEND_EXISTING
Owner: Murat Project Engineer Core
Date: 2026-09-17

## Purpose

This document defines a common unit model for measuring useful automation and process improvement across MPE-governed projects.

The model exists because different projects create value in very different forms: cleaning spreadsheets, fixing geometry in furniture workflows, validating documents, removing duplicate entry, reducing retries, simplifying approvals, or eliminating repeated human checks. A common economic model must therefore measure relieved human work rather than count AI calls, agent runs, prompts, features, or raw automation steps.

## Core hierarchy

```text
PROCESS
  -> TASK
  -> STEP
  -> ACTION
  -> WORK ATOM
  -> RELIEF ATOM
  -> VERIFIED RELIEF UNIT (VRU)
  -> PROCESS RELIEF
  -> PRODUCT VALUE
  -> PORTFOLIO ECONOMICS
```

## 1. Work Atom

A `Work Atom` is the smallest independently observable human action that can be detected, measured, changed, removed, assisted, standardized, validated, or automated.

Typical categories include:

- COPY
- SEARCH
- CHECK
- DECIDE
- TRANSFORM
- ENTER
- WAIT
- APPROVE
- CORRECT
- CALCULATE
- GENERATE
- COMPARE
- MOVE
- ROUTE
- RECONCILE
- REMEMBER
- RETRY

A Work Atom should be decomposed until further splitting would stop producing a useful separately measurable human action.

## 2. Relief Atom

A `Relief Atom` exists when one Work Atom has been measurably reduced, removed, assisted, or made materially safer/easier by an implemented intervention.

A Relief Atom is not created by a recommendation alone.

Examples:

- repeated copy/paste removed by integration;
- manual spreadsheet cleanup replaced by validated cleanup logic;
- repeated geometry correction eliminated by a reliable inference step;
- repeated document check replaced by deterministic validation;
- reminder burden removed by reliable follow-up automation.

## 3. Verified Relief Unit (VRU)

A `Verified Relief Unit` is the primary cross-project economic unit.

A VRU is a completed, user-relevant piece of work made measurably easier and verified on a real workflow, artifact, or production-like case.

A VRU should only be counted when:

1. the friction or failure mode was identified;
2. relevant Work Atoms were decomposed;
3. an intervention was implemented or a bounded working artifact was delivered;
4. the target outcome remained usable/correct;
5. before/after or equivalent evidence confirms real relief;
6. the result is attributable with sufficient confidence.

Canonical rule:

> A theoretical automation opportunity is not a VRU.

## 4. VRU evidence fields

A VRU record should capture, where measurable:

- `name`
- `process`
- `work_atoms_before`
- `work_atoms_removed_or_assisted`
- `time_returned`
- `frequency`
- `errors_prevented`
- `rework_avoided`
- `context_switches_removed`
- `human_judgement_removed_or_assisted`
- `business_criticality`
- `unlock_value`
- `reuse_multiplier`
- `confidence`
- `evidence_refs`
- `implementation_cost`
- `operating_cost`
- `status`

Recommended `status` values:

- HYPOTHESIS
- OBSERVED
- IMPLEMENTED
- VERIFIED
- RETIRED

Only `VERIFIED` units count as completed VRUs.

## 5. Unlock Value

`Unlock Value` measures how strongly one relieved atom or VRU enables downstream work that was otherwise blocked, unreliable, or excessively expensive.

This is essential because a technically small intervention can have disproportionately large economic importance.

Example:

```text
correct corner geometry
  -> valid FRAME
  -> materials can be applied
  -> render becomes reliable
  -> costing becomes reliable
  -> proposal can be produced
```

A geometry fix may therefore have higher value than many low-impact click removals.

Unlock Value should be tracked separately from time savings to avoid understating bottleneck-breaking work.

## 6. Reuse Multiplier

`Reuse Multiplier` measures how broadly the relieved atom or implementation can be reused across tasks, workflows, products, or projects.

Examples:

- a reliable corner-orientation primitive reused in L-kitchens, U-kitchens, wardrobes, room planning, and bathroom cabinetry;
- a document-normalization primitive reused across invoices, waybills, and contracts;
- a spreadsheet-cleanup primitive reused across several automation skills.

High-reuse Work Atoms deserve stronger priority because one implementation can create multiple downstream VRUs.

## 7. Value dimensions

VRU value should be evaluated across multiple dimensions rather than forced immediately into one monetary number.

Recommended dimensions:

- Time Returned
- Work Removed
- Errors Prevented
- Rework Avoided
- Cognitive Load Reduced
- Context Switching Reduced
- Waiting Reduced
- Business Criticality
- Unlock Value
- Reuse Multiplier
- User Confidence / Trust Improvement when measurable

Monetary conversion may be added later when reliable local cost inputs exist.

## 8. Cost dimensions

Recommended VRU cost components:

- AI/model compute
- infrastructure
- external APIs
- human validation
- support/operations
- integration maintenance
- amortized development cost
- expected failure/recovery cost

A basic unit margin may be represented as:

```text
Unit Margin = Monetized VRU Value - VRU Cost
```

Do not fabricate monetary precision when value inputs are uncertain.

## 9. Relief Score for prioritization

MPE may use a normalized `Relief Score` for portfolio prioritization when direct monetary comparison is not yet reliable.

Recommended factors include:

- frequency;
- time returned;
- error/rework impact;
- business criticality;
- unlock value;
- reuse multiplier;
- implementation effort;
- confidence of evidence.

The score is a prioritization aid, not customer billing and not a claim of exact economic equivalence.

Do not interpret two scores as a literal money ratio unless a separate validated financial model supports that conclusion.

## 10. Decomposition rule

When analyzing a candidate process, decompose iteratively:

```text
PROCESS
  -> TASK
  -> STEP
  -> ACTION
  -> WORK ATOM
```

Stop when the smallest actionable source of friction is found.

The goal is to identify the minimum element whose relief materially changes the user outcome.

This prevents oversized solutions and enables reuse of solved primitives.

## 11. Example — spreadsheet cleanup

```text
VRU: Reliable Spreadsheet Cleanup

work_atoms_removed_or_assisted:
- detect empty rows
- remove empty rows
- normalize formats
- validate resulting structure

time_returned: measured per file
frequency: measured per period
errors_prevented: measured/estimated with evidence
unlock_value: low-to-medium unless cleanup blocks downstream processing
reuse_multiplier: potentially high across spreadsheet workflows
```

The VRU is only verified when a real file is processed correctly and the relieved work is demonstrated.

## 12. Example — furniture corner geometry

```text
VRU: Reliable Corner Kitchen Frame

friction:
repeated failure to infer/create correct corner geometry

relief:
reliable corner/orientation primitive produces a valid frame without repeated manual correction

possible value:
- retries avoided
- correction time removed
- downstream rendering unlocked
- costing/proposal flow unlocked
- reusable in other corner furniture workflows
```

This example demonstrates why Unlock Value and Reuse Multiplier must exist separately from simple time savings.

## 13. Relationship to Human Value Delivery

`docs/HUMAN_VALUE_DELIVERY_PRINCIPLES.md` defines the human-facing philosophy.

This document defines the measurable economic unit model underneath that philosophy.

Canonical relationship:

```text
Human involvement
  -> Visible Relief
  -> Relief Atom(s)
  -> Verified Relief Unit
  -> Measured Product Value
```

## 14. Relationship to Business Discovery

Business Discovery should identify candidate Work Atoms and friction patterns, but it should not count a VRU merely because a candidate was detected.

Business Discovery may produce:

- candidate Work Atoms;
- candidate Relief Atoms;
- expected Unlock Value;
- expected Reuse Multiplier;
- expected Relief Score.

A completed VRU requires implemented and verified relief.

## 15. MPE prioritization rule

When choosing among implementation candidates, MPE should prefer work that maximizes verified or strongly evidenced relief subject to current portfolio priority, risk, cost, and deep-change constraints.

Particular attention should be given to:

- high Unlock Value;
- high Reuse Multiplier;
- severe recurring friction;
- high error/rework reduction;
- strong evidence with bounded implementation scope.

## 16. Anti-metrics

Do not treat the following as primary value units:

- number of prompts;
- number of agent runs;
- number of model calls;
- number of generated files;
- number of automation steps;
- lines of code;
- feature count;
- time spent inside the product.

These may be operational metrics, but they do not prove user value.

## 17. Development gate

For substantial automation/value work, developers and coding agents should be able to answer:

1. What process is being decomposed?
2. What is the smallest relevant Work Atom?
3. What friction does it create?
4. What Relief Atom will the implementation create?
5. What evidence will convert the result into a Verified Relief Unit?
6. What is the Unlock Value?
7. What is the Reuse Multiplier?
8. What are the operating and implementation costs?
9. How will the result be visible to the user?
10. Is the unit verified, or still only a hypothesis?

Material deviations from this model should be documented rather than silently inventing incompatible value units inside individual projects.
