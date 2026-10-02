# EXP-21 — Subtasks and execution plan

Status: PLANNED

## Execution model

EXP-21 is split between two environments:

- **Arena** — research, repository work, adapter design, deterministic tests, evidence consolidation.
- **Windows SketchUp/EasyKitchen bench** — real application/plugin validation that cannot be assumed to run inside Arena Agent Mode.

MPE remains the experiment authority and result registry.

## Phase 0 — Control

### EXP21-00 — Freeze scope
**Environment:** MPE/Arena  
**Goal:** Confirm experiment boundaries before implementation.

Deliverables:
- approved fixture definition;
- command list frozen to existing commands;
- explicit PASS/HOLD/FAIL criteria;
- no production MebelFlow changes.

Exit: scope frozen.

---

## Phase 1 — Evidence reconnaissance

### EXP21-01 — SketchUp automation surface
**Environment:** Arena

Investigate and document:
- Ruby API;
- model/entity manipulation;
- components/groups;
- attributes/metadata;
- units/precision;
- identifiers;
- events;
- automation/headless limitations;
- licensing constraints.

Deliverable:
- `evidence/sketchup-recon.md`

Exit: verified automation boundary or documented blocker.

### EXP21-02 — EasyKitchen integration surface
**Environment:** Arena + official EasyKitchen evidence

Investigate separately from SketchUp:
- public/documented API;
- catalog/module access;
- parameters;
- materials/thickness/edge banding;
- fittings;
- drilling;
- nesting;
- BOM;
- production documentation;
- import/export;
- recalculation;
- external-change behavior;
- licensing.

Rule: never infer an EasyKitchen API from the existence of SketchUp Ruby API.

Deliverable:
- `evidence/easy-kitchen-recon.md`

Exit: each capability marked `VERIFIED`, `UNVERIFIED`, or `BLOCKED`.

### EXP21-03 — Video/evidence extraction
**Environment:** Arena

Use the supplied EasyKitchen 6 material as evidence, but separate observed behavior from assumptions.

Deliverable:
- timestamped observations;
- evidence links;
- unresolved questions.

Exit: claims used by the experiment are traceable to evidence.

---

## Phase 2 — Contract and fixture

### EXP21-04 — MebelFlow → EasyKitchen mapping
**Environment:** Arena

Map:
- Project State;
- Furniture Node;
- module;
- dimensions;
- materials;
- edge banding;
- hardware;
- command schema;
- warnings;
- version identity;
- BOM;
- production documents.

Deliverable:
- `evidence/data-contract-mapping.md`

Exit: explicit mapping gaps documented.

### EXP21-05 — Freeze minimal kitchen fixture
**Environment:** Arena + Windows

Fixture:
- one wall;
- 3–5 base modules;
- one drawer module;
- one appliance module;
- one upper module;
- fixed materials/thicknesses.

Deliverables:
- canonical MebelFlow state;
- manual SketchUp/EasyKitchen reference model;
- expected dimensions and module list.

Exit: identical reference fixture exists on both sides.

---

## Phase 3 — Deterministic bridge

### EXP21-06 — Adapter boundary design
**Environment:** Arena

Reuse existing command architecture.

Initial commands only:
- SET_WALL_WIDTH
- ADD_MODULE
- INSERT_AFTER
- CHANGE_WIDTH
- REMOVE_MODULE
- UNDO

Deliverable:
- adapter interface;
- command translation table;
- validation/error model.

Exit: no arbitrary AI-generated SketchUp code is required.

### EXP21-07 — Offline adapter prototype
**Environment:** Arena

Implement/test only the deterministic translation/state logic that does not require SketchUp.

Tests:
- command validation;
- serialization;
- replay;
- idempotency where applicable;
- error handling;
- state consistency.

Deliverable:
- prototype + automated tests.

Exit: deterministic command layer passes offline tests.

### EXP21-08 — First real SketchUp command
**Environment:** Windows SketchUp

Run exactly one command through the real integration boundary.

Preferred first proof:
- SET_WALL_WIDTH, or
- ADD_MODULE.

Capture:
- before/after model;
- command trace;
- resulting dimensions;
- errors/manual steps.

Exit: one real deterministic mutation verified, or blocker documented.

---

## Phase 4 — EasyKitchen production proof

### EXP21-09 — EasyKitchen recalculation
**Environment:** Windows SketchUp/EasyKitchen

Verify whether an externally driven model change can be recalculated through the normal EasyKitchen workflow.

Deliverable:
- reproducible procedure;
- evidence;
- limitations.

Exit: recalculation behavior classified.

### EXP21-10 — Production-output proof
**Environment:** Windows SketchUp/EasyKitchen

Verify at least one:
- BOM/parts list;
- drilling/boring output;
- nesting output;
- production documentation.

Do not require every output for the first proof if one reliable production output establishes the boundary.

Deliverable:
- sample output;
- mapping to fixture;
- reproducibility notes.

Exit: at least one downstream production output is verified, or capability is proven inaccessible.

---

## Phase 5 — Round-trip and resilience

### EXP21-11 — Result/evidence return path
**Environment:** Arena + Windows

Test:

MebelFlow State → SketchUp/EasyKitchen → result/evidence → MPE

Determine what structured information can return without making SketchUp/EasyKitchen the source of truth.

Deliverable:
- return-data contract;
- unsupported fields;
- evidence examples.

### EXP21-12 — Repeatability test
**Environment:** Arena + Windows

Repeat the same fixture and command sequence.

Compare:
- geometry;
- dimensions;
- module identity;
- production output;
- warnings/errors.

Exit: deterministic repeatability measured.

---

## Phase 6 — Decision

### EXP21-13 — Cost/complexity comparison
**Environment:** Arena

Compare:
- custom implementation effort;
- adapter complexity;
- EasyKitchen capability reused;
- manual steps;
- fragility;
- licensing/cost;
- maintenance burden.

Do not score subjectively. Record measurable observations.

Deliverable:
- evidence-backed comparison.

### EXP21-14 — Final experiment report
**Environment:** Arena

Produce:
- PASS / HOLD / FAIL;
- verified integration boundary;
- blockers;
- evidence index;
- recommended next experiment, if justified;
- explicit statement of what must NOT be changed in MebelFlow.

Important: Arena must not declare a production architecture change.

### EXP21-15 — MPE registry update
**Environment:** Arena/MPE

Update:
- experiment status;
- result;
- evidence paths;
- next action.

Only after EXP21-14 is complete.

---

## Execution order

EXP21-00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15

### Parallelizable work

These can run in parallel after EXP21-00:

- EXP21-01
- EXP21-02
- EXP21-03

After EXP21-04:

- EXP21-06 and EXP21-05 can proceed in parallel.

After EXP21-07:

- Windows work begins with EXP21-08.

## Hard gates

Do not proceed to the next phase when:

1. the previous phase has an unresolved blocker that invalidates its assumptions;
2. EasyKitchen API behavior is being guessed rather than verified;
3. a step requires arbitrary AI-generated code execution;
4. the proposed adapter starts becoming a replacement CAD;
5. a production MebelFlow contract must change.

## Definition of done

EXP-21 is complete when:

- the real SketchUp/EasyKitchen automation boundary is known;
- at least one MebelFlow command has been tested against the real environment, or a concrete blocker is proven;
- at least one EasyKitchen production output is verified, or its programmatic inaccessibility is proven;
- repeatability has been tested;
- licensing and manual dependencies are documented;
- MPE has a final PASS/HOLD/FAIL result;
- no production MebelFlow architecture was changed without a separate approval.
