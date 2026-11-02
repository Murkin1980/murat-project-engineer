# Text-to-CAD — experiment candidate (2026-10-08)

Status: **QUEUED / NOT EXECUTED**  
Murat Project Engineer New Idea Filter: **EXPERIMENT**  
Upstream: https://www.texttocad.dev/  
Source: https://github.com/earthtojake/text-to-cad

## Purpose
Evaluate whether reusable text-to-CAD agent skills can reduce time and errors when preparing manufacturing CAD files for existing Murat projects. No new repository, CAD service, database, deployment, or autonomous manufacturing control.

## Existing projects / reuse
- **Murat Project Engineer / Arena:** experiment governance, reproducible checks and result recording.
- **Existing furniture configurator:** possible later reuse of geometry/export logic, only after accurate manufacturing output is established.
- **Furniture production:** technical drawings, cut parts and connectors; avoid duplicating established cutting/CAD workflows.
- **One-off Subaru flat-pack brazier:** concrete benchmark for sheet-metal plasma cutting, not a new product or infrastructure.

## Business hypothesis and minimum MVP
A reusable skill can produce a valid manufacturing-oriented DXF from a dimensioned brief with less manual cleanup than the present workflow. Record actual baseline and experimental time; do not assign fabricated savings.

One bounded test:
1. Freeze dimensions, material thickness, kerf/slot clearance assumptions, letterform/logo references and machine constraints for a flat-pack Subaru-themed brazier. Confirm brand art use is appropriate.
2. Audit upstream version, license, dependencies, network/telemetry behavior and skill install side effects before running anything.
3. Generate one CAD model and export DXF (STEP only if supported and useful). Record exact inputs and version.
4. Validate DXF as geometry: supported entities, closed planar contours, no self-intersections/duplicates, minimum web/feature widths, clear internal cutouts, practical part fit and sheet size. Visually inspect lettering and logo cutouts.
5. Review with the actual plasma-machine operator/CAM software. Distinguish DXF geometry from NC/G-code and machine-specific kerf, lead-in/lead-out, bridges and nesting. No production cut without explicit operator signoff.
6. Compare against manual baseline: minutes to usable drawing, number of manual corrections, file import success, dimension/fit errors. Save reproducible evidence and a terminal result.

## Gates
- **FAST/VERIFIED** for isolated source assessment and nonproduction generation; **DEEP-CHANGE** and explicit owner approval before changes to production configurator, machinery, production flows, architecture or mandatory tooling.
- Existing components first; do not introduce parallel geometry store, services, APIs, cloud infrastructure or a new repo.
- No automatic installation into global agent directories without review.
- Vendor capabilities (DXF, STEP, DFM, offline processing) are **claims to verify**, not proven facts.
- No merges/deploys/production actions as part of experiment intake.

## Outcome template
`RESULT: PASS | PARTIAL | FAIL | BLOCKED`  
`ADOPTION: ADOPT | ADOPT_WITH_CHANGES | HOLD | REJECT`  
Evidence: upstream pin; environment; commands; exported artifact hashes; CAD checks; CAM import proof; baseline comparison; blockers; follow-up owner decision.

**Priority:** high relative to speculative agent integrations, because there is a concrete plasma-cutting case. Reassess against currently active production fixes before execution.
