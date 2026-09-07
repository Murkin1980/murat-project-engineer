# CLI-Anything × FreeCAD experiment

This is an isolated MPE New Idea Filter experiment. It audits the existing
upstream CLI-Anything FreeCAD harness without changing MPE production code,
adding dependencies, creating a wrapper/executor, or creating permanent
infrastructure.

## Disposition

The harness installs and its pure-Python/native JSON command path works. The
real FreeCAD artifact path is **not available in this sandbox**: the harness
requires an external FreeCAD console executable (`freecadcmd`, `FreeCADCmd`, or
an equivalent discovered executable) to run generated FreeCAD macros and write
`.FCStd`, STEP, STL, and other final geometry files. No executable was present,
and the official Debian installation attempt could not obtain the package.

**Final terminal state:** `BLOCKED_HARNESS_REQUIRES_EXTERNAL_FREECAD`

The native JSON cabinet probe still ran twice through documented CLI commands.
It produced five correctly named box records with the requested dimensions and
placements, an exact `800 × 450 × 600 mm` analytic bounding box, positive
volumes, no positive-volume AABB collisions, and matching normalized state on a
fresh second run. This is intermediate harness state—not a native FreeCAD
`.FCStd` artifact and not evidence that the FreeCAD geometry kernel executed.

See:

- [`TASK.md`](TASK.md) — frozen task, dimensions, acceptance checks, and
  constraints.
- [`REPORT.md`](REPORT.md) — complete audit, installation and test counts,
  execution-path proof, native probes, dependency checks, cabinet verification,
  artifacts, determinism, bypass status, and recommendation.

No CLI-Anything source, virtualenv, FreeCAD binary, archive, or generated CAD
artifact was copied into this repository.
