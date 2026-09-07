# CLI-Anything × LibreOffice experiment report

## Decision and scope

- Decision: `EXPERIMENT`
- Scope: isolated technical experiment only.
- Production MPE files were not changed.
- No backend, database, SaaS, permanent infrastructure, new repository,
  executor, Task Packet change, governance change, Spreadsheet Runner change,
  or production dependency was added.
- The experiment stopped as required when the mandatory LibreOffice dependency
  could not be installed. CLI-Anything was not cloned into the MPE repository.

## Phase 0 — repository audit

- Repository: `Murkin1980/murat-project-engineer`
- `AGENTS.md`: not present in or above the checkout.
- Read: `README.md`.
- Read experiment/harness documentation: `docs/experiments/EXP-13_LOW_COST_EVALUATION_HARNESS.md`, `docs/experiments/EXP13_PRE_EXECUTION_REWORK.md`, `docs/experiments/EXPERIMENT_REPORT_TEMPLATE.md`, and `experiments/exp-002-machine-protocol/README.md` plus its results.
- Initial working tree: clean.
- Branch: `arena/01a07d0d-murat-project-engineer`
- MPE HEAD: `7962d91b0985c848b378ed319ef295e95365c973`
- `origin/main`: `7962d91b0985c848b378ed319ef295e95365c973`

## Phase 1 — environment

Observed on 2026-09-07 UTC:

- OS: Debian GNU/Linux 12 (bookworm)
- Kernel: `Linux e2b.local 6.1.158+ #1 SMP PREEMPT_DYNAMIC Mon May 11 18:48:24 UTC 2026 x86_64 GNU/Linux`
- Architecture: `x86_64`
- Python: `Python 3.11.2`
- `libreoffice`: absent (`which libreoffice` returned no path)
- `soffice`: absent (`which soffice` returned no path)
- `libreoffice --version`: command not found

## Phase 2 — dependency installation attempt

LibreOffice was not installed, so the permitted Debian package-manager path was
attempted first:

```bash
sudo -n apt-get update && sudo -n apt-get install -y libreoffice
```

Observed result:

```text
Connection failed [IP: 151.101.66.132 80]
Connection failed [IP: 151.101.194.132 80]
Connection failed [IP: 151.101.66.132 80]
E: Unable to locate package libreoffice
```

A non-interactive privilege check also returned:

```text
sudo: a password is required
```

The official LibreOffice download page was reachable through the page-fetch
facility and identified the official Linux x86-64 Debian package, but direct
sandbox retrieval was not possible. Direct requests to the official download
host and Debian package host failed with `SSL_ERROR_SYSCALL` / empty replies.
No mirror, unofficial binary, container, simulated LibreOffice, or prebuilt
artifact was used.

Because a real LibreOffice installation is a hard prerequisite and the sandbox
cannot install or retrieve it through the permitted paths, the experiment
stopped here. This is not an upstream harness failure.

## Later phases

| Phase | Result |
|---|---|
| 3. Obtain CLI-Anything | Not run; stopped before dependency was available |
| 4. Inspect LibreOffice harness | Not run |
| 5. Install harness | Not run |
| 6. Upstream harness tests | Not run; passed/failed/skipped: N/A |
| 7. E2E run 1 | Not run; no XLSX artifact |
| 8. Independent verification | Not run; no artifact to hash or read |
| 9. Determinism / E2E run 2 | Not run |

CLI-Anything upstream SHA: `N/A — Phase 3 not reached`.

## PASS criteria evaluation

Not evaluated to PASS. Criteria requiring a real LibreOffice process,
`cli-anything-libreoffice`, a produced XLSX, formulas, independent verification,
round-trip processing, and a second semantic run could not be exercised.

- Artifact path: not created
- Artifact SHA-256: `N/A`
- Calculated grand total: `N/A` (expected `218500`)
- Prohibited bypasses used: `NO`
- Production MPE files changed: `NO`

## Terminal state

`BLOCKED_SANDBOX_DEPENDENCY_INSTALL`

Reason: LibreOffice was absent; non-interactive package installation could not
retrieve Debian package indexes and required privilege was not available for a
fallback install, while direct official package retrieval was unavailable from
this sandbox. The experiment was not simulated and was not converted into
`PASS`.

## Continuation

Re-run this isolated experiment in a sandbox that has real LibreOffice available
or permits installation from the official Debian package manager / official
LibreOffice download. Start again at Phase 1, then clone CLI-Anything only into
a temporary directory, inspect the upstream harness before using it, and record
all later evidence in this directory. No production integration follows from
this blocked run.
