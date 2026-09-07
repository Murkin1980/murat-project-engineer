# Frozen task — CLI-Anything × FreeCAD

Run the existing upstream FreeCAD harness from CLI-Anything in an isolated,
harness-first experiment. Do not integrate it into MPE production code and do
not create a replacement harness, wrapper, executor, or permanent
infrastructure.

## Required model

If the harness provides a usable geometry path, create a five-panel cabinet
with these five named parts:

| Part | Length × Width × Height (mm) |
|---|---:|
| `LeftSide` | `18 × 450 × 600` |
| `RightSide` | `18 × 450 × 600` |
| `Top` | `764 × 450 × 18` |
| `Bottom` | `764 × 450 × 18` |
| `Shelf` | `764 × 430 × 18` |

The assembly bounding box must be `800 × 450 × 600 mm`, with a tolerance of
±0.1 mm. The exact native-state probe used these placements (x, y, z in mm):

| Part | Position |
|---|---:|
| `LeftSide` | `(0, 0, 0)` |
| `RightSide` | `(782, 0, 0)` |
| `Top` | `(18, 0, 582)` |
| `Bottom` | `(18, 0, 0)` |
| `Shelf` | `(18, 0, 291)` |

The shelf is centered in height and is 20 mm shallower in y than the cabinet
body. The top and bottom span between the side panels.

## Acceptance checks

1. Locate and record the existing upstream FreeCAD harness and exact
   CLI-Anything SHA.
2. Inspect its README, SKILL, packaging, entrypoint, core/backend/exporter and
   macro-generation code, fixtures, tests, bootstrap/install scripts, and CI
   references.
3. Install the existing harness only in a temporary isolated environment and
   run all available upstream test categories, recording passed/failed/skipped
   counts.
4. Establish whether the model state is pure Python/native JSON, and whether
   real geometry/export uses the FreeCAD Python API, `FreeCADCmd`, or an
   external subprocess.
5. Probe documented native commands before searching for or installing
   FreeCAD. Probe document creation, primitive creation, listing/get/info,
   bounds/measurements, placement changes, and the documented scale/dimension
   operation. Do not hand-edit project JSON as a producer.
6. After the native probes, search for an external FreeCAD executable and make
   the official dependency-install attempt if the runtime is absent.
7. If the runtime works, create and save a native `.FCStd` (and optionally
   STEP/STL) through the harness. Independently verify object count, names,
   dimensions, placement, bounding box, volume, collisions, artifact format,
   and a fresh second run.
8. If a working native-state geometry path exists while FreeCAD is unavailable,
   run the five-panel test through documented CLI commands and clearly label
   its JSON result as an intermediate harness state, not a FreeCAD artifact.
9. Stop after these three evidence files. Do not begin production integration.

## Standing constraints

- Work only in the existing MPE checkout. Preserve existing changes; do not
  reset or switch branches.
- The fixed branch is `arena/01a07d0d-murat-project-engineer`.
- Clone CLI-Anything only into a temporary sandbox; never vendor it into MPE.
- Use only documented upstream CLI commands for harness-produced geometry.
- Python is allowed only for independent verification after a harness artifact
  exists. Python/CadQuery/OpenCascade/Blender/trimesh/OpenSCAD/manual
  STEP/STL/custom geometry producers are forbidden.
- Do not install or search for FreeCAD before the audit, installation, tests,
  native probes, and dependency-path proof are complete.
- Allowed terminal states are only: `PASS`, `FAIL_HARNESS`,
  `FAIL_UPSTREAM_TESTS`, `FAIL_GEOMETRY`, `FAIL_ARTIFACT`, `FAIL_VERIFICATION`,
  `FAIL_NONDETERMINISTIC`, `BLOCKED_HARNESS_REQUIRES_EXTERNAL_FREECAD`,
  `BLOCKED_SANDBOX_DEPENDENCY_INSTALL`, `BLOCKED_NETWORK`, and
  `BLOCKED_OTHER`.
- Do not commit CLI-Anything source, virtualenvs, FreeCAD binaries, AppImages,
  `.deb` archives, or large generated dependencies.

## Evidence scope

Only these files may be created or updated in this experiment directory:

- `README.md`
- `TASK.md`
- `REPORT.md`
