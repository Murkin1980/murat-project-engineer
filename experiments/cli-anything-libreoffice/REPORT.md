# CLI-Anything × LibreOffice — harness-first experiment report

## Final disposition

- New Idea Filter: `EXPERIMENT`
- Current terminal state: `BLOCKED_HARNESS_REQUIRES_EXTERNAL_LIBREOFFICE`
- Production MPE code was not changed.
- The existing evidence was preserved and this report was updated in place.
- No CLI-Anything source, virtualenv, LibreOffice binary, XLSX, or temporary
  harness artifact was added to the MPE repository.

This iteration deliberately audited and installed the ready-made harness before
re-checking the LibreOffice dependency. The dependency blocker is therefore a
harness-proven result, not an early `which libreoffice` stop.

## Phase 0 — MPE baseline

- Repository: `Murkin1980/murat-project-engineer`
- `AGENTS.md`: not present in or above the checkout.
- Read: `README.md` and all files in the existing
  `experiments/cli-anything-libreoffice/` evidence directory.
- Working tree before this report update: clean.
- Branch: `arena/01a07d0d-murat-project-engineer`
- MPE HEAD before this iteration's evidence update:
  `023aac1d705081ff5f2c13d89508b4de30949209`
- `origin/main`:
  `7962d91b0985c848b378ed319ef295e95365c973`

Environment observed on 2026-09-07:

- OS: Debian GNU/Linux 12 (bookworm)
- Kernel: `Linux e2b.local 6.1.158+ #1 SMP PREEMPT_DYNAMIC Mon May 11 18:48:24 UTC 2026 x86_64 GNU/Linux`
- Architecture: `x86_64`
- Python: `Python 3.11.2`
- At baseline: `libreoffice` and `soffice` were absent.

## Phase 1 — CLI-Anything checkout

CLI-Anything was cloned only into a temporary sandbox directory, not into MPE:

```bash
TMP_ROOT="$(mktemp -d)"
git clone https://github.com/HKUDS/CLI-Anything.git "$TMP_ROOT/CLI-Anything"
cd "$TMP_ROOT/CLI-Anything"
git rev-parse HEAD
```

Observed temporary checkout:

- Temporary root: `/tmp/cli-anything-harness-first-aIKMM9`
- CLI-Anything HEAD: `810c18b0d1ab9b234bc996c9fd999318523a3ef0`
- Branch: `main`
- Checkout status: clean and tracking `origin/main`

## Phase 2 — ready-made harness audit

### Structure inspected

```text
libreoffice/agent-harness/
├── LIBREOFFICE.md
├── setup.py
└── cli_anything/libreoffice/
    ├── README.md
    ├── __init__.py
    ├── __main__.py
    ├── libreoffice_cli.py
    ├── core/
    │   ├── calc.py
    │   ├── document.py
    │   ├── export.py
    │   ├── importer.py
    │   ├── impress.py
    │   ├── session.py
    │   ├── styles.py
    │   └── writer.py
    ├── skills/SKILL.md
    ├── tests/
    │   ├── TEST.md
    │   ├── test_core.py
    │   └── test_full_e2e.py
    └── utils/
        ├── lo_backend.py
        ├── odf_utils.py
        └── repl_skin.py
```

There are no `requirements.txt`, `pyproject.toml`, `setup.cfg`, shell
bootstrap scripts, download helpers, Docker/devcontainer files, or LibreOffice
binary/runtime bundles in this harness directory. `setup.py` is the only setup
file.

### Dependency model

`setup.py` version `1.0.1` installs Python dependencies only:

```text
click>=8.0.0
prompt-toolkit>=3.0.0
defusedxml>=0.7.1
```

The development extra adds `pytest` and `pytest-cov`. It does not install
LibreOffice.

The source documentation is consistent on the relevant point, despite a stale
count in `TEST.md` and the repository root README:

- ODF/HTML/text generation can run with Python code alone.
- Importing DOCX/XLSX/PPTX and exporting PDF/DOCX/XLSX/PPTX/CSV uses a real
  LibreOffice/`soffice` installation.
- `SKILL.md` states that LibreOffice must be installed on the system.
- `lo_backend.py` documents a system package requirement and only prints
  manual `apt`, `brew`, or `winget` suggestions on failure.
- No code downloads, installs, or bootstraps LibreOffice.

`LIBREOFFICE.md` contains an older module spelling (`cli.libreoffice_cli`) in
its examples; the actual installed package entrypoint is
`cli_anything.libreoffice.libreoffice_cli` and works as documented below.

### Actual execution path

For the requested XLSX producer, the audited path is:

```text
cli-anything-libreoffice
  → setup.py console_scripts
  → cli_anything.libreoffice.libreoffice_cli:main
  → core.export.export(..., preset="xlsx")
  → core.export._export_via_libreoffice()
  → odf_utils.write_odf(..., intermediate.ods)
  → utils.lo_backend.convert_odf_to()
  → utils.lo_backend.convert()
  → utils.lo_backend.find_libreoffice()
  → subprocess.run(
       [<libreoffice-or-soffice>, --headless, ..., --convert-to, xlsx, ...]
    )
```

`find_libreoffice()` checks `PATH` for `libreoffice` and `soffice`, then
Windows candidates and the macOS application bundle. It raises
`RuntimeError` if none is found. The conversion code uses an isolated temporary
LibreOffice profile/runtime/config/cache and verifies that the output file was
actually produced.

The Calc command stores formulas in the harness project model via
`calc set-cell --formula`; the actual XLSX conversion and formula calculation
are delegated to the external LibreOffice process. Native `ods` export is a
separate Python ODF-writing path and is not the requested XLSX execution path.

### Bootstrap result

- Harness-provided LibreOffice bootstrap: **NO**
- Bundled/portable/AppImage/build runtime: **NO**
- Install helper that can be invoked: **NO**
- CI workflow that installs LibreOffice for this harness: **NO specific
  LibreOffice workflow reference found**

The only installation-related behavior in the audited harness is the error
message from `find_libreoffice()`:

```text
apt install libreoffice
brew install --cask libreoffice
winget install TheDocumentFoundation.LibreOffice
```

Those are instructions, not an installer executed by CLI-Anything.

## Phase 3 — harness installation and entrypoints

The first upstream command was attempted exactly as requested:

```bash
cd libreoffice/agent-harness
python3 -m pip install -e .
```

The Debian Python environment rejected system installation under PEP 668 with
`externally-managed-environment`. This was a Python packaging restriction, not
a harness failure. The official local workaround was an isolated temporary
virtualenv outside MPE:

```bash
python3 -m venv /tmp/cli-anything-harness-first-aIKMM9/venv
/tmp/cli-anything-harness-first-aIKMM9/venv/bin/python -m pip install -e .
/tmp/cli-anything-harness-first-aIKMM9/venv/bin/python -m pip install -e '.[dev]'
```

Result: **Harness installed: YES** in the temporary virtualenv. No virtualenv
was committed.

Working entrypoints:

```text
/tmp/cli-anything-harness-first-aIKMM9/venv/bin/cli-anything-libreoffice
python -m cli_anything.libreoffice
```

Both produced the Click help output with the `document`, `calc`, `export`,
`writer`, `impress`, `style`, `session`, and `repl` command groups.

## Phase 4 — upstream tests before manual LibreOffice installation

Test collection from the checked-out source produced **180 tests**, which is
more current than the checked-in `TEST.md` claim of 172 and the root README
claim of 158.

### Unit / synthetic / mocked coverage

Command:

```bash
python -m pytest cli_anything/libreoffice/tests/test_core.py -v -s
```

Result:

```text
107 passed in 0.11s
0 failed
0 skipped
```

The unit suite includes the monkeypatched conversion test
`TestImport::test_import_docx_uses_libreoffice_conversion`; it passes without a
real LibreOffice process. There is no separate pytest marker/category for
mocked tests.

### Full E2E suite before LibreOffice

Command:

```bash
python -m pytest cli_anything/libreoffice/tests/test_full_e2e.py -v -s
```

Result:

```text
55 passed
18 failed
0 skipped
73 collected
```

The 55 passing tests cover native ODF/HTML/text generation, ODF validation,
project/session behavior, and CLI subprocess flows that do not invoke an Office
conversion. All 18 failures are installed-software cases: the backend lookup,
PDF/DOCX/XLSX/PPTX/CSV conversion, Office import, and CLI subprocess workflows
that depend on external LibreOffice. They fail with the harness's explicit
`LibreOffice is not installed` runtime error, not with an unverified artifact.

Test category summary:

| Category | Passed | Failed | Skipped | Classification |
|---|---:|---:|---:|---|
| Unit / synthetic / mocked | 107 | 0 | 0 | PASS |
| Native/full E2E without external LO | 55 | 0 | 0 | PASS |
| Installed-software/full E2E | 0 | 18 | 0 | blocked by missing external LO |
| Total collected | 162 | 18 | 0 | 180 total |

## Phase 5–7 — dependency proof and binary search

The harness was installed, its documentation and code were audited, its tests
were run, and its real conversion path was identified before checking the
sandbox for LibreOffice.

Commands:

```bash
which libreoffice || true
which soffice || true
find / -type f \( -name libreoffice -o -name soffice \) 2>/dev/null | head -50
```

Results:

- `libreoffice`: not found
- `soffice`: not found
- filesystem search: no matching executable
- `/usr/bin/`: no matching executable
- `/usr/lib/libreoffice/`: directory absent
- `/opt/`, `/app/`, `/workspace/`, `/home/`: no matching executable

A real harness producer-path probe was then run with the installed CLI. It
created a Calc project, renamed the sheet to `Order`, populated the requested
cells and formula fields, and attempted:

```bash
cli-anything-libreoffice --json --project order.json \
  export render mpe-cli-anything-test.xlsx --preset xlsx --overwrite
```

The harness returned exit code 1:

```json
{
  "error": "LibreOffice is not installed. Install it with:\n  apt install libreoffice          # Debian/Ubuntu\n  brew install --cask libreoffice   # macOS\n  winget install TheDocumentFoundation.LibreOffice  # Windows",
  "type": "RuntimeError"
}
```

Only the temporary project JSON remained. No XLSX was produced. The project
JSON contained the requested formulas (`=B2*C2`, `=B3*C3`, `=B4*C4`, and
`=SUM(D2:D4)`), but it is not an XLSX artifact and was not treated as a result.

## Phase 8 — official LibreOffice installation after dependency proof

Only after the harness audit, installation, upstream tests, execution-path
identification, and binary search, the official installation paths were tried.

### Debian package manager

```bash
sudo -n apt-get update
sudo -n apt-get install -y libreoffice
```

Observed:

```text
apt-get update: exit 0, but all Debian InRelease fetches failed with
Connection failed against deb.debian.org
apt-get install: exit 100
E: Unable to locate package libreoffice
```

### Official LibreOffice download host

The official page-fetch facility identified the official Linux x86-64 Debian
package URL for LibreOffice 26.8.0. Direct sandbox requests to the official
website and download host were then attempted without downloading or using a
binary:

```bash
curl -IL --max-time 20 https://www.libreoffice.org/download/download-libreoffice/
curl -IL --max-time 20 \
  https://download.documentfoundation.org/libreoffice/stable/26.8.0/deb/x86_64/LibreOffice_26.8.0_Linux_x86-64_deb.tar.gz
```

Both direct requests failed with exit 35 / `SSL_ERROR_SYSCALL`. No unofficial
mirror, random binary, container image, or simulated LibreOffice was used.

After the failed installation attempts, `libreoffice --version` and
`soffice --version` remained unavailable.

## Artifact and verification

- Real LibreOffice binary found: **NO**
- E2E XLSX executed: **NO**
- `mpe-cli-anything-test.xlsx`: not created
- `file`, `sha256sum`, OOXML validation: not applicable
- Grand total: `N/A` (expected `218500`)
- Independent verification: not applicable
- LibreOffice round-trip: not applicable
- Second semantic run: `N/A`
- Prohibited bypasses: **NO**

The unsuccessful XLSX producer-path probe does not count as an E2E run because
there was no physical XLSX artifact and no calculated business result.

## PASS criteria assessment

The harness itself is real and installed, and its native ODF path has passing
unit/native-E2E coverage. However, the requested real XLSX path cannot execute
in this sandbox because the upstream harness explicitly delegates XLSX creation
to an external LibreOffice process and provides no bootstrap for it.

Therefore this iteration cannot claim `PASS`, `FAIL_ARTIFACT`, or
`FAIL_VERIFICATION`: no artifact was produced. The 18 installed-mode test
failures are environment dependency failures after the harness was correctly
audited, not evidence that the harness silently generated a substitute file.

## Terminal state

`BLOCKED_HARNESS_REQUIRES_EXTERNAL_LIBREOFFICE`

This state is justified only because all required distinction checks were
completed:

1. ready-made CLI-Anything LibreOffice harness installed;
2. relevant code and documentation audited;
3. upstream unit and full E2E tests run;
4. actual `CLI → Python → subprocess → LibreOffice` path identified;
5. harness shown to require an external LibreOffice binary for XLSX;
6. binary absent from PATH and common/system locations;
7. official package-manager and official-download paths unavailable.

## Final harness-first summary

```text
CLI-ANYTHING × LIBREOFFICE — HARNESS-FIRST

MPE HEAD: 023aac1d705081ff5f2c13d89508b4de30949209
CLI-Anything HEAD: 810c18b0d1ab9b234bc996c9fd999318523a3ef0

Harness installed: YES
Harness entrypoint: cli-anything-libreoffice
  (/tmp/cli-anything-harness-first-aIKMM9/venv/bin/cli-anything-libreoffice)

Upstream tests:
  unit: 107 passed / 0 failed / 0 skipped
  integration/native E2E: 55 passed / 0 failed / 0 skipped
  installed-mode: 0 passed / 18 failed / 0 skipped

Does harness require external LibreOffice: YES
Evidence for dependency model:
  lo_backend.find_libreoffice() resolves an existing binary and
  lo_backend.convert() invokes it with subprocess.run(); xlsx is an
  explicit lo_convert export preset. Missing binary raises RuntimeError.

Harness-provided bootstrap exists: NO
Real LibreOffice binary found: NO
E2E executed: NO
Grand total: N/A (expected 218500)
Artifact valid: NO — artifact not created
Second run: N/A
Terminal State: BLOCKED_HARNESS_REQUIRES_EXTERNAL_LIBREOFFICE

Conclusion:
  The ready-made harness installs and works for native ODF operations, but it
  does not organize or provide a LibreOffice runtime. Real XLSX execution is
  blocked by the sandbox's missing external dependency. Keep experimental;
  do not integrate into MPE Core.
```

## Files changed in MPE

Only this existing evidence file was updated:

```text
experiments/cli-anything-libreoffice/REPORT.md
```

No production integration follows from this blocked harness-first run.
