# EXP-33 / CP-02 — isolated read-only test

**Target:** no external target contacted.  
**Fixture:** environment package-readiness probe only.  
**Reason:** target permission is not enough to override the no-install and no-configuration boundary; there is no locally available browser or permitted local web-app artifact.

## Command

```bash
npx --no-install rea-agents --help
```

The command was run from an otherwise empty scratch directory. `--no-install` prevents package download and does not perform setup, registration, or global installation.

## Actual result

- Exit code: **1**
- npm reported that `rea-agents@6.8.0` was missing and cancelled because installation was disallowed.
- No REA command was found on PATH before the probe.
- No Chromium, Google Chrome, or Playwright executable was found on PATH.
- No request was made to PrivetMaket or any other external target.
- No files in the MPE worktree, client configuration, or persistent infrastructure were modified by the test.

## Interpretation

This is a real negative readiness test, not a functional REA capture. It proves only that REA cannot be executed in this environment under the approved non-install boundary. It does **not** prove or disprove REA's browser-capture behavior.

**CP-02 result: BLOCKED.**
