# CLI-Anything × FreeCAD — harness-first experiment report

## Final disposition

- **New Idea Filter:** `EXPERIMENT`
- **Final terminal state:** `BLOCKED_HARNESS_REQUIRES_EXTERNAL_FREECAD`
- **Production MPE code:** unchanged.
- **Harness source:** audited and installed only from a temporary checkout.
- **Native JSON path:** passed the documented-command cabinet probe and a
  second semantic run.
- **Real FreeCAD geometry/artifact path:** blocked; no FreeCAD executable was
  available and the official Debian installation attempt could not install it.
- **Native `.FCStd`, STEP, or STL artifact:** none was created.
- **Bypass status:** `NO`.

The result is intentionally not reported as `PASS`: the harness's JSON model
state and analytic box calculations are useful intermediate state, but the
harness documentation and source make final FreeCAD geometry an external
runtime operation. Without that runtime there is no truthful native CAD file
to inspect.

## Phase 0 — MPE baseline and scope

Observed on **2026-09-07** in the user's Asia/Qyzylorda timezone:

| Item | Value |
|---|---|
| Repository | `Murkin1980/murat-project-engineer` |
| Branch | `arena/01a07d0d-murat-project-engineer` |
| MPE HEAD at report time | `3ebaf0938f88b0edd4143c4ffe46ff6da7a42cc0` |
| `origin/main` | `7962d91b0985c848b378ed319ef295e95365c973` |
| Working tree before this evidence update | clean |
| OS | Debian GNU/Linux 12 (bookworm) |
| Kernel / architecture | Linux 6.1.158+ / x86_64 |
| System Python | 3.11.2 |
| `AGENTS.md` | not present in or above the checkout |
| Existing MPE experiment rules read | root `README.md` and `experiments/cli-anything-libreoffice/` evidence files |

Existing LibreOffice experiment files and changes were preserved. This
experiment did not reset, switch branches, or modify production code.

## Phase 1 — temporary upstream checkout

CLI-Anything was cloned outside MPE:

```text
Temporary root: /tmp/cli-anything-freecad-ArOCYb/
Checkout:       /tmp/cli-anything-freecad-ArOCYb/CLI-Anything
CLI-Anything:   https://github.com/HKUDS/CLI-Anything.git
SHA:            810c18b0d1ab9b234bc996c9fd999318523a3ef0
Branch/status:  main, clean, tracking origin/main
```

The exact harness used was:

```text
/tmp/cli-anything-freecad-ArOCYb/CLI-Anything/freecad/agent-harness/
```

The temporary checkout and environment remain outside the MPE repository and
are not part of the evidence patch.

## Phase 2 — audit of the ready-made harness

### Files and documentation inspected

The audit covered the harness's:

- `FREECAD.md` standard operating procedure and dependency/architecture
  description;
- `cli_anything/freecad/README.md` prerequisites, installation, documented
  commands, export presets, preview commands, and test commands;
- `cli_anything/freecad/skills/SKILL.md` command inventory and examples;
- `setup.py`, generated egg metadata, package data, and console entrypoint;
- `cli_anything/freecad/freecad_cli.py` Click groups/options and dispatch;
- core modules under `cli_anything/freecad/core/`, including document, parts,
  measure, session, preview, motion, body, and export;
- `utils/freecad_backend.py`, `freecad_macro_gen.py`, and preview helpers;
- `tests/TEST.md`, `test_core.py`, and `test_full_e2e.py`;
- repository-wide FreeCAD-related fixture, bootstrap/install, and CI
  references.

The harness has no checked-in FreeCAD fixture directory or runtime bundle. The
upstream tests create temporary JSON projects with pytest `tmp_path`; they do
not provide a portable CAD engine. `setup.py` is the harness package's only
setup file. There is no FreeCAD-specific bootstrap/download script, Docker
runtime, AppImage, `.deb`, or CI workflow that installs FreeCAD. Generic
upstream installer scripts and unrelated issue/label fixtures were not treated
as FreeCAD runtime support.

The checked-in `tests/TEST.md` contains an older 67-test/Windows result and is
not the current execution result; the current checkout collected 112 tests.

### Packaging and entrypoint

`setup.py` reports:

```text
name:           cli-anything-freecad
version:        1.0.0
python_requires >=3.10
install_requires: click>=8.0.0, prompt-toolkit>=3.0.0
console_scripts: cli-anything-freecad=cli_anything.freecad.freecad_cli:main
```

FreeCAD is not a Python package dependency. It is documented as a system
prerequisite. The console command accepts `--json`, `-p/--project`, and the
document/part/sketch/body/export/measure/preview/motion command groups.

### Execution-path finding

The audited path for final geometry/export is:

```text
Documented CLI command
  -> Click main in freecad_cli.py
  -> pure-Python Session/project dictionary loaded from JSON
  -> core.export.export_project()
  -> freecad_macro_gen.generate_macro()
  -> freecad_backend.export_headless()
  -> freecad_backend.run_macro_content()
  -> freecad_backend.run_macro()
  -> find_freecad()
  -> subprocess.run([discovered FreeCAD executable, temporary macro.py])
  -> generated macro imports FreeCAD and Part
  -> FreeCAD document/object creation, recompute, saveAs/export
  -> output existence and format-header validation
```

`freecad_backend.find_freecad()` searches `FREECAD_PATH`, then
`freecadcmd`, `FreeCADCmd`, `freecad`, and `FreeCAD` on `PATH`, followed by
platform-specific standard locations. `run_macro()` invokes the discovered
executable with a generated Python script using `subprocess.run`; it does not
import the FreeCAD Python module into the harness process.

`freecad_macro_gen.py` generates code using the real FreeCAD Python API, for
example `FreeCAD.newDocument`, `doc.addObject('Part::Box', ...)`, placements,
`doc.recompute()`, and `doc.saveAs(...)`. `core.parts`, `core.measure`, and the
session code used by the native probe are instead pure-Python JSON-state and
analytic-primitive code. There is no pure-Python fallback that writes a real
`.FCStd` or exchange file.

Therefore the harness is a **Python CLI front end plus external FreeCAD
subprocess**, not a standalone Python CAD kernel. The native JSON state path
must not be conflated with FreeCAD geometry execution.

## Phase 3 — isolated harness installation

The harness was installed editable only in:

```text
/tmp/cli-anything-freecad-ArOCYb/venv/
```

The system-wide editable installation was not used because Debian's PEP 668
`externally-managed-environment` policy rejects it. The isolated install
succeeded:

```bash
python3 -m venv /tmp/cli-anything-freecad-ArOCYb/venv
/tmp/cli-anything-freecad-ArOCYb/venv/bin/python -m pip install -e \
  /tmp/cli-anything-freecad-ArOCYb/CLI-Anything/freecad/agent-harness
```

The test-only environment also installed `pytest` and `Pillow`; Pillow was
needed because `test_full_e2e.py` imports it, but it is not declared by the
harness runtime package. The installed console was verified:

```bash
/tmp/cli-anything-freecad-ArOCYb/venv/bin/cli-anything-freecad --help
```

Observed package versions included `click 8.5.0`, `prompt-toolkit 3.0.53`,
`pytest 9.1.1`, and `Pillow 12.3.0`.

## Phase 4 — upstream tests

All available upstream categories were run from the harness checkout. The
final subprocess run used the installed console, not a fallback module path:

```bash
PATH="/tmp/cli-anything-freecad-ArOCYb/venv/bin:$PATH" \
CLI_ANYTHING_FORCE_INSTALLED=1 \
/tmp/cli-anything-freecad-ArOCYb/venv/bin/python -m pytest \
  cli_anything/freecad/tests/ -v -s
```

Captured logs are outside MPE at `/tmp/cli-anything-freecad-ArOCYb/`.

| Category / command | Collected | Passed | Failed | Skipped | Result |
|---|---:|---:|---:|---:|---|
| `test_core.py` | 88 | 88 | 0 | 0 | PASS |
| `test_full_e2e.py` without FreeCAD | 24 | 13 | 0 | 11 | PASS for available paths |
| Correct installed-console combined run | 112 | 101 | 0 | 11 | PASS for available paths |

The 11 full-E2E skips are runtime-gated: seven FreeCAD backend/export/preview
cases and four CLI preview/motion cases. They require an external FreeCAD
runtime and, for the video case, preview/motion support. The initial forced
installed-console invocation omitted the temporary venv from `PATH` and caused
six `cli-anything-freecad not found` fixture errors; that invocation was
identified as an invocation mistake and was not counted. The corrected run
above produced `101 passed, 0 failed, 11 skipped`.

## Phase 5 — native capability probes before external lookup

The documented CLI was exercised before any deliberate FreeCAD binary search
or install attempt. Producer operations were all CLI commands; no project JSON
was hand-edited.

### Small native probe

The following documented operations were run against a temporary project:

```bash
cli-anything-freecad --json document new --name NativeProbe --units mm -o probe.json
cli-anything-freecad --json -p probe.json part add box --name ProbeBox \
  -P length=20 -P width=15 -P height=5
cli-anything-freecad --json -p probe.json part list
cli-anything-freecad --json -p probe.json part get 0
cli-anything-freecad --json -p probe.json part info 0
cli-anything-freecad --json -p probe.json part bounds 0
cli-anything-freecad --json -p probe.json measure bounding-box 0
cli-anything-freecad --json -p probe.json measure volume 0
cli-anything-freecad --json -p probe.json part transform 0 --position 10,20,30
cli-anything-freecad --json -p probe.json document info
cli-anything-freecad --json -p probe.json session status
cli-anything-freecad --json -p probe.json document save
```

Observed native results:

- document and JSON save succeeded;
- the box record retained `length=20`, `width=15`, `height=5`;
- volume was `1500.0 mm^3` and the initial box bounds were exactly
  `20 × 15 × 5`;
- `part transform` changed the world bounds to
  min `(10, 20, 30)`, max `(30, 35, 35)`;
- `document info`, `part list`, `part info`, `part bounds`, and session status
  all returned JSON without FreeCAD installed.

### Dimension/parameter mutation probe

The documented `part scale 0 2.0` command was also run. It recorded a
`ProbeBox_scaled` operation with `scale=[2.0, 2.0, 2.0]`, but the native analytic
inspection returned `null` bounds/volume and `deferred: true` measurements for
that derived `type=scale` record. `part --help` exposes no direct
`part set-params` or primitive-dimension-edit command. Thus the native path can
create parameterized primitive records and transform them, and can record a
scale operation, but it does not provide a fully evaluated mutable dimension
model for that derived operation. This limitation was recorded rather than
worked around by editing JSON.

The native probe proves a pure-Python model/state path; it does not prove that
FreeCAD or OpenCASCADE ran.

## Phase 6 — dependency proof and external runtime gate

After the native probes, a documented export command was used to make the
backend dependency observable:

```bash
cli-anything-freecad --json -p probe.json export render probe.step \
  --preset step --overwrite
```

It exited with code 1, produced no output file, and returned the harness's
explicit error:

```text
FreeCAD console executable (FreeCADCmd) not found.
Install FreeCAD and make sure FreeCADCmd is on your PATH...
```

This is consistent with the audited source chain: final exports are delegated
to an external FreeCAD console subprocess. The harness's own Python package
contains no `FreeCAD`/`Part` runtime module and no geometry-kernel fallback.

### Binary search after dependency proof

The following names were checked only after the audit, upstream tests, native
probes, and export-path proof:

```bash
which FreeCAD
which freecad
which FreeCADCmd
which freecadcmd
find /usr /opt /app /workspace /home -type f \
  \( -name FreeCAD -o -name FreeCADCmd -o -name freecad -o -name freecadcmd \) \
  2>/dev/null
```

Results:

- no command was found on `PATH`;
- no matching executable was found in the searched filesystem roots;
- all four version probes returned `command not found`;
- no `FREECAD_PATH` override was used.

### Official dependency-install attempt

The official Debian package path was attempted only after the above proof:

```bash
sudo -n DEBIAN_FRONTEND=noninteractive apt-get update
sudo -n DEBIAN_FRONTEND=noninteractive apt-get install -y freecad
```

`apt-get update` could not fetch the Debian `bookworm`, `bookworm-updates`,
and `bookworm-security` `InRelease` files because the sandbox connection to
`deb.debian.org` failed; the command retained/used stale package lists. The
install then exited with code 100 and `E: Unable to locate package freecad`.
A direct non-sudo attempt also failed on apt/dpkg lock permissions. No FreeCAD
binary, AppImage, `.deb`, archive, or website download was fetched. Post-attempt
`FreeCAD`, `freecad`, `FreeCADCmd`, and `freecadcmd` probes remained absent.

This satisfies the dependency-proof order and establishes the external
runtime blocker without treating a bare initial `which` result as sufficient.

## Phase 7 — five-panel cabinet native-state run

Because the documented native JSON path was usable, the required cabinet was
created twice from clean temporary projects with only documented CLI
commands. The producer commands were repeated for each run:

```bash
cli-anything-freecad --json document new --name Cabinet --units mm -o mpe-cabinet-test.json
cli-anything-freecad --json -p mpe-cabinet-test.json part add box --name LeftSide \
  --position 0,0,0 -P length=18 -P width=450 -P height=600
cli-anything-freecad --json -p mpe-cabinet-test.json part add box --name RightSide \
  --position 782,0,0 -P length=18 -P width=450 -P height=600
cli-anything-freecad --json -p mpe-cabinet-test.json part add box --name Top \
  --position 18,0,582 -P length=764 -P width=450 -P height=18
cli-anything-freecad --json -p mpe-cabinet-test.json part add box --name Bottom \
  --position 18,0,0 -P length=764 -P width=450 -P height=18
cli-anything-freecad --json -p mpe-cabinet-test.json part add box --name Shelf \
  --position 18,0,291 -P length=764 -P width=430 -P height=18
cli-anything-freecad --json -p mpe-cabinet-test.json document save
cli-anything-freecad --json -p mpe-cabinet-test.json part list
cli-anything-freecad --json -p mpe-cabinet-test.json part info 0
# ... part info/bounds for indexes 1 through 4 as well
```

### Independent verification results

Verification happened only after the harness-produced JSON existed, using
standard Python to read the records and calculate expected AABBs, volumes,
pairwise intersections, and run comparison. No CAD library or geometry
producer was used.

| Part | Dimensions (mm) | Position (mm) | World AABB min → max (mm) | Volume (mm³) |
|---|---:|---:|---:|---:|
| `LeftSide` | `18 × 450 × 600` | `(0, 0, 0)` | `(0,0,0)` → `(18,450,600)` | `4,860,000` |
| `RightSide` | `18 × 450 × 600` | `(782, 0, 0)` | `(782,0,0)` → `(800,450,600)` | `4,860,000` |
| `Top` | `764 × 450 × 18` | `(18, 0, 582)` | `(18,0,582)` → `(782,450,600)` | `6,188,400` |
| `Bottom` | `764 × 450 × 18` | `(18, 0, 0)` | `(18,0,0)` → `(782,450,18)` | `6,188,400` |
| `Shelf` | `764 × 430 × 18` | `(18, 0, 291)` | `(18,0,291)` → `(782,430,309)` | `5,913,360` |

The verification outcome was:

```text
object_count:              5
names:                     exact required five names
assembly bbox:             min=(0,0,0), max=(800,450,600)
assembly size:             800 × 450 × 600 mm
bbox tolerance:            PASS (exact, therefore within ±0.1 mm)
sum part volumes:          28,010,160 mm³ (positive and sane)
positive-volume collisions: 0 of 10 pairs
```

The parts meet only at intended panel faces/edges; the pairwise AABB
intersection volume was zero for every pair. The shelf remains inside the
cabinet x/y envelope and centered in z.

### Native JSON artifact evidence

These are temporary intermediate harness-state files, not FreeCAD documents:

```text
/tmp/cli-anything-freecad-ArOCYb/furniture/run1/mpe-cabinet-test.json
  size: 2534 bytes
  raw SHA-256: 2d09248bfa863239609a4da0a38b6d7ee19944e0138ee68df3793eb17be3748e
  normalized SHA-256 (timestamps removed): e572738c47db3fbf51afd1f03d9e2665ab09f1d75a04bd70deb6c2ddc6cd0f00

/tmp/cli-anything-freecad-ArOCYb/furniture/run2/mpe-cabinet-test.json
  size: 2534 bytes
  raw SHA-256: c117f371cd3ef9bbcfe221d46896bd7aa97b445874702a644b5f7430968cfc8b
  normalized SHA-256 (timestamps removed): e572738c47db3fbf51afd1f03d9e2665ab09f1d75a04bd70deb6c2ddc6cd0f00
```

### Fresh second run / determinism

The second clean CLI run reproduced the same object order, names, dimensions,
placements, analytic bounds, volumes, and collision result. The normalized
project states are equal. Raw file hashes differ only because the harness
writes fresh `metadata.created` and `metadata.modified` timestamps; this is
expected metadata nondeterminism, not geometry nondeterminism. No random or
order-dependent geometry behavior was observed.

### FreeCAD furniture E2E status

The native-state cabinet probe is `PASS` as a JSON/analytic intermediate
probe. The requested real FreeCAD furniture E2E is
`BLOCKED_HARNESS_REQUIRES_EXTERNAL_FREECAD`:

- no `.FCStd` was written;
- no STEP or STL was written;
- no FreeCAD document could be reopened independently;
- no FreeCAD-kernel volume or collision check could be performed;
- no native artifact format magic/header could be verified.

The documented export of this cabinet would follow the same missing external
`FreeCADCmd` path demonstrated by the small-box export failure.

## Phase 8 — acceptance matrix

| Acceptance item | Result | Evidence |
|---|---|---|
| Existing harness located | PASS | temporary checkout and harness path above |
| Exact CLI-Anything SHA recorded | PASS | `810c18b0d1ab9b234bc996c9fd999318523a3ef0` |
| Docs/package/entrypoint/core/backend/exporter audited | PASS | Phase 2 |
| Fixtures/bootstrap/CI references inspected | PASS | Phase 2; no runtime bundle/install workflow found |
| Isolated harness installation | PASS | temporary venv; console help succeeds |
| Upstream core tests | PASS | `88/0/0` |
| Upstream full E2E available subset | PASS | `13/0/11` |
| Correct installed-console total | PASS | `101/0/11` |
| Native JSON operations | PASS | Phase 5 |
| Documented dimension/scale limitation captured | PASS with limitation | scale is deferred; no direct dimension edit command |
| External dependency path proven | PASS | export failure plus source chain |
| FreeCAD executable discovery | BLOCKED | no binary in PATH/search roots |
| Official dependency install | BLOCKED | apt network/package availability failure |
| Five-panel native-state cabinet | PASS | exact dimensions, names, bounds, volumes, zero positive-volume collisions |
| Native `.FCStd`/STEP/STL artifact | BLOCKED | requires external FreeCAD |
| Independent FreeCAD artifact verification | BLOCKED | no artifact exists |
| Fresh second semantic run | PASS | normalized SHA equal; geometry results equal |
| Production integration | NOT STARTED | explicitly out of scope |

## Changed files and bypass audit

Only these requested evidence files were created in MPE:

```text
experiments/cli-anything-freecad/README.md
experiments/cli-anything-freecad/TASK.md
experiments/cli-anything-freecad/REPORT.md
```

No production source, tests, dependencies, MPE configuration, governance, or
existing experiment files were changed. The temporary upstream checkout,
virtualenv, test logs, native JSON probe, and verification scratch data remain
outside the repository. No CLI-Anything source was copied or vendored.

Forbidden bypasses used: **NO**. In particular, no Python/CadQuery/
OpenCascade/Blender/trimesh/OpenSCAD geometry producer, manual STEP/STL writer,
custom wrapper, replacement harness, or direct JSON producer mutation was used.
The only Python after harness artifacts existed was independent verification.

## Recommendation

Do not integrate this harness into MPE based on this run. It is a viable
command-line front end for a separately managed FreeCAD installation, and its
pure-Python JSON state path is useful for command/unit testing and intent
inspection. It is not a standalone CAD backend and cannot satisfy a real
`.FCStd`/STEP/STL artifact requirement without FreeCAD.

A future rerun should provide a genuine, version-pinned FreeCAD installation
with `FreeCADCmd` visible to the harness, then repeat the same documented
cabinet commands, export `fcstd` (preferably also STEP/STL), reopen/validate the
artifact independently, and compare a fresh second native-artifact run. Until
that dependency is available, the correct terminal state remains
`BLOCKED_HARNESS_REQUIRES_EXTERNAL_FREECAD`.
