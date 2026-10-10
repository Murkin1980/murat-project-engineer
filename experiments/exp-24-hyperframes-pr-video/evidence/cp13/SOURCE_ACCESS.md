# EXP-24 CP-13 — canonical source access check

Date: 2026-10-10 (UTC) · Executor: Arena Agent Mode (single agent, this session)
Branch: `arena/75c6ba59-murat-project-engineer` · Base: `main` @ `19dd6a096433edfe5742d667cfc70e8fda8d3434`

## Result

**SOURCE_ACCESS_BLOCKED**

The canonical fixture source `Murkin1980/AI-serial-v2` (file `TEASER_SCENE_SHEETS.md`, scene E01-S005 «Молодой продюсер открывает конверт») could not be read from this Arena session. No content was read, reconstructed, or invented. The production chain (scene contract, storyboard, media, Remotion preview, mobile QA, revisions) was **not started**.

## Attempts (all read-only, 2026-10-10 UTC)

| # | Check | Outcome |
|---|---|---|
| 1 | `gh repo view Murkin1980/AI-serial-v2` | Failed: `--json` field error (`visibility` unsupported by this gh version); no repository metadata returned. |
| 2 | `git clone --depth 1 https://github.com/Murkin1980/AI-serial-v2.git` | HTTP 403 — "Write access to repository not granted." Clone not created. |
| 3 | `gh api repos/Murkin1980/AI-serial-v2` | HTTP 403 — "Resource not accessible by integration". |
| 4 | `gh api repos/Murkin1980/AI-serial-v2/contents/TEASER_SCENE_SHEETS.md` | HTTP 403 (same). |
| 5 | `gh api repos/Murkin1980/AI-serial-v2/branches` | HTTP 403 (same). |
| 6 | `git ls-remote https://github.com/Murkin1980/AI-serial-v2.git` | HTTP 403 (same as #2). |
| 7 | `gh repo list Murkin1980` | `AI-serial-v2` not present in the visible repository list. |
| 8 | Connector check (`list_connector_tools` for GitHub) | `unsupported` — no additional GitHub connector is available to this session. |

`gh auth status` reports a valid login for `Murkin1980`; the token can read `murat-project-engineer` but not `AI-serial-v2`. This is an access-scope issue, the same class of blocker recorded for CP-02 in EXP-23 (`evidence/cp02-ai-serial-results.md`, §2).

Nothing was written to `AI-serial-v2`. No clone exists in the sandbox (`/tmp/ai-serial-v2` absent).

## Note on EXP-23 reference evidence

EXP-23 recorded a 20/20 action mapping, 0/0 omitted/added beats and 6/6 previs stills for E01-S005, but that verification was made in an earlier session against the source. In this run the source could not be re-read, so none of those counts are reproduced or re-verified here. They remain EXP-23 reference evidence only and must not be cited as CP-13 coverage.

## Required action to unblock

The owner must grant this Arena GitHub connection read access to `Murkin1980/AI-serial-v2` (or supply a read-only copy of `TEASER_SCENE_SHEETS.md` through an approved channel), then the CP-13 run can resume at Step 1 (scene contract freeze).
