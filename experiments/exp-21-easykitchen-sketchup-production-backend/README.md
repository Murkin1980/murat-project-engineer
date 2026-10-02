# EXP-EASYKITCHEN-01 — MebelFlow → SketchUp/EasyKitchen production backend

Status: PLANNED

## Decision

Primary MPE disposition: EXPERIMENT.

Extend the existing MebelFlow/Talk-to-Design research; do not create a new repository, do not build a parallel furniture CAD, and do not replace the current MebelFlow source-of-truth architecture.

## Trigger

Fresh EasyKitchen 6 material indicates a broader production workflow inside the SketchUp ecosystem, including furniture modeling plus drilling/boring (присадка), nesting, and production documentation. The relevant video supplied for this experiment:

- YouTube: https://youtu.be/kBSAglftevM

The video itself must be treated as an evidence source to inspect during execution; claims below are hypotheses until verified from the product, documentation, API behavior, licensing, and controlled tests.

## Hypothesis

MebelFlow should remain the semantic/control layer while SketchUp + EasyKitchen may serve as the production execution layer.

Target architecture:

MebelFlow AI
→ Intent Parser
→ strict Furniture Command Schema
→ MebelFlow Project State (source of truth)
→ SketchUp/EasyKitchen adapter
→ EasyKitchen production functions
→ manufacturing documentation / nesting / drilling data

AI must describe furniture intent and allowed domain commands. AI must not generate or execute arbitrary SketchUp Ruby/Python code.

## Why this experiment matters

If EasyKitchen already provides production-grade furniture geometry and downstream manufacturing functions, implementing those algorithms ourselves would duplicate a mature capability.

The experiment therefore tests the integration boundary, not whether we should build another CAD.

Potential measurable value:

- reduce custom CAD/geometry scope;
- reuse EasyKitchen production logic;
- preserve MebelFlow as the stable conversational/domain layer;
- move from AI-generated geometry toward deterministic domain commands;
- potentially shorten the path from customer conversation to production-ready documentation.

## What must be investigated

### 1. SketchUp integration surface

Determine:

- SketchUp Ruby API capabilities relevant to furniture objects;
- creation/update/deletion of model entities;
- component/group/material/attribute handling;
- persistent identifiers and metadata;
- units and precision;
- event hooks;
- headless/automated execution feasibility;
- licensing and automation constraints.

### 2. EasyKitchen integration surface

Determine, with evidence:

- whether EasyKitchen exposes a public/documented API;
- whether its objects can be created or modified through SketchUp Ruby;
- whether kitchen/cabinet parameters are accessible;
- module/catalog semantics;
- material/thickness/edge-band/fitting parameters;
- drilling/boring configuration;
- nesting configuration;
- production-document generation;
- BOM/parts-list export;
- supported import/export formats;
- batch/recalculation behavior;
- whether changes made externally trigger the same production recalculation as UI changes.

Do not infer an API merely because SketchUp itself has a Ruby API.

### 3. Data-contract mapping

Map existing MebelFlow concepts to EasyKitchen concepts:

| MebelFlow | Target integration question |
|---|---|
| Project State | What SketchUp/EasyKitchen project representation corresponds to it? |
| Furniture Node | Cabinet/module/component representation |
| module catalog | EasyKitchen catalog/component definition |
| dimensions in mm | SketchUp/EasyKitchen units and precision |
| materials | material/catalog mapping |
| edge banding | production parameter mapping |
| hardware | fitting/library mapping |
| command schema | deterministic adapter operations |
| warnings | validation/recalculation feedback |
| project version | model/version identity |
| BOM | EasyKitchen output |
| production docs | EasyKitchen output |

### 4. Command bridge

Reuse the already-proven MebelFlow command architecture.

Initial candidate commands:

- SET_WALL_WIDTH
- ADD_MODULE
- INSERT_AFTER
- CHANGE_WIDTH
- REMOVE_MODULE
- UNDO

Do not expand the command vocabulary until the first adapter proof requires it.

The adapter should translate validated MebelFlow commands into deterministic SketchUp/EasyKitchen operations.

### 5. Round-trip boundary

Test whether the integration can safely support:

MebelFlow Project State
→ SketchUp/EasyKitchen
→ generated production outputs

and, separately, whether any useful structured result can return:

EasyKitchen
→ adapter
→ validation/result
→ MebelFlow evidence/state metadata

MebelFlow remains the source of truth unless an explicit architecture decision changes this.

### 6. Production-output verification

For a frozen small kitchen fixture, compare:

- cabinet/module count;
- dimensions;
- parts list/BOM;
- drilling/boring data;
- nesting output;
- production documentation;
- materials and thicknesses;
- deterministic repeatability after recalculation.

Where outputs are not exposed programmatically, record the limitation rather than inventing an adapter.

## Minimal experiment

Use one frozen reference project with a small straight kitchen.

Suggested fixture:

- one wall;
- 3–5 base modules;
- at least one drawer module;
- one appliance module;
- one upper module;
- fixed material/thickness rules.

Run:

1. Create the reference state in MebelFlow.
2. Produce the equivalent model manually in SketchUp/EasyKitchen.
3. Identify the smallest deterministic automation surface.
4. Execute one MebelFlow command through the adapter.
5. Verify model state.
6. Trigger/recalculate EasyKitchen production outputs.
7. Compare outputs against the frozen reference.
8. Repeat the same operation to test deterministic behavior.
9. Record failures, inaccessible surfaces, licensing constraints, and manual steps.

## Success criteria

PASS requires all of the following:

1. A supported and repeatable integration path is identified.
2. At least one validated MebelFlow command changes the SketchUp/EasyKitchen model deterministically.
3. The resulting model preserves required furniture parameters.
4. At least one downstream EasyKitchen production output can be verified.
5. No arbitrary code execution is required from the AI layer.
6. MebelFlow Project State remains the source of truth.
7. The integration does not require building a parallel CAD.
8. Licensing/automation constraints are documented.
9. The measured benefit is concrete enough to justify a second bounded experiment.

## Failure / HOLD criteria

HOLD or FAIL if:

- EasyKitchen has no usable automation boundary;
- licensing prohibits the intended workflow;
- production outputs cannot be accessed or reliably verified;
- the integration requires fragile UI automation as the primary mechanism;
- MebelFlow would have to surrender source-of-truth ownership;
- the adapter becomes more complex than the capability it replaces;
- the workflow duplicates existing MebelFlow functionality without measurable value.

## Relationship to Blender experiment

Blender remains an isolated research environment for the Talk-to-Design command bridge.

This experiment does not delete or invalidate the Blender bridge.

The comparison question is:

- Blender: can we control a 3D environment using strict furniture commands?
- SketchUp + EasyKitchen: can the same command architecture reach a production-capable furniture workflow?

If EasyKitchen provides the required production surface, it should be evaluated as the preferred production backend rather than reproducing production algorithms in Blender.

## Relationship to MebelFlow

MebelFlow currently has an explicit rule prohibiting SketchUp/CAD integration in its approved MVP scope. This experiment therefore remains MPE research only.

No MebelFlow production code, public contract, source-of-truth rule, or roadmap stage is changed by this experiment.

Any actual SketchUp/EasyKitchen integration into MebelFlow requires a separate deep-change review and explicit owner approval.

## Evidence to collect

- video observations with timestamps;
- EasyKitchen official documentation;
- SketchUp Ruby API references;
- EasyKitchen licensing terms;
- screenshots or recordings of controlled operations;
- adapter source and command traces;
- before/after model evidence;
- BOM/production-document samples;
- nesting/drilling evidence;
- repeatability results;
- measured implementation effort;
- unresolved constraints.

## Next action

Perform a focused technical reconnaissance of SketchUp Ruby + EasyKitchen automation and licensing, then freeze the first minimal fixture before writing an adapter.

## Constraints

- No new repository.
- No production integration.
- No arbitrary AI-generated code execution.
- No replacement of MebelFlow Project State.
- No custom furniture CAD.
- No broad command-schema expansion.
- No paid dependency or recurring cost without explicit approval.
- Stop before any deep-change.
