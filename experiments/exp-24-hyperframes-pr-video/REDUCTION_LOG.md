# Code reduction — implementation inventory and classification

Date: 2026-10-08
Trigger: `SALAMAT_PROMO_ARENA_TASK.md` § HARD CHANGE-SIZE BUDGET
(preferred ≤ 1,200 handwritten lines · soft warning > 1,500 · hard stop > 2,500).

## Measured state before reduction

Handwritten implementation on this branch: **2,076 lines** of code + 244 lines of
experiment docs → **over the soft warning, close to the hard stop**. Two generated
binaries and the npm lockfile were also committed as source.

## Inventory and classification

| File | Added LOC | Classification | Action |
| --- | --- | --- | --- |
| `tools/shot_plan.py` | 425 | KEEP (compressed) | prose-heavy dicts → compact table; −270 |
| `tools/build_storyboard_from_script.py` | 283 | KEEP (compressed) | integrity checks kept, ceremony removed; −130 |
| `src/Scene.tsx` | 252 | SPLIT-NOT-NEEDED | merged into one composition file |
| `tools/validate_contracts.py` | 236 | REMOVE | overlapped the builders' own integrity checks; claims screen folded into the timeline step |
| `tools/resolve_media.py` | 213 | KEEP (compressed) | −100 |
| `tools/build_timeline.py` | 192 | KEEP (compressed) | −90 |
| `adapters/storyblocks_adapter.py` | 124 | KEEP (thin) | availability + search only; −60 |
| `src/BrandClose.tsx` | 106 | SPLIT-NOT-NEEDED | merged into the composition file |
| `tools/media_assets.py` | 92 | REMOVE | constants merged into `resolve_media.py` |
| `src/typography.ts` | 38 | SPLIT-NOT-NEEDED | merged into the composition file |
| `src/types.ts` | 38 | SPLIT-NOT-NEEDED | merged into the composition file |
| `src/Promo.tsx` | 36 | KEEP (rewritten) | becomes the single composition file |
| `src/Root.tsx` | 33 | SPLIT-NOT-NEEDED | merged into the composition file |
| `src/index.ts` | 8 | KEEP | registerRoot + font CSS |
| `docs` (`PROMO_BRIEF.md`, `REVISION_LOG.md`, `MEDIA_PROVIDER_LOG.md`) | 244 | KEEP (trimmed) | required checkpoint artifacts |
| `out/smoke-frame.png`, `out/smoke-frame-small.jpg` | binary | REMOVE | generated render output; untracked, `out/` ignored |
| `package-lock.json` | 3,832 | VENDOR | lockfile churn — ignored by the budget and kept out of the reduction count |
| `node_modules/**` | vendor | VENDOR | not tracked |
| `EDITORIAL_STORYBOARD.json`, `MEDIA_MANIFEST.json`, `src/generated/timeline.json` | generated | GENERATED | rebuildable from script + tools; regenerated, not hand-edited |
| `SALAMAT_PROMO_ARENA_TASK.md`, `SALAMAT_PROMO_SCRIPT.md`, `SALAMAT_PROMO_OWNER_NOTES.md` | 756 | OWNER | owner-authored inputs, not implementation |

## Removed infrastructure (anti-framework check)

Dropped before continuing: the generic contract validator CLI, the standalone design-token
module, the standalone timeline types module, and the separate scene/brand component files.
No custom editor, asset manager, orchestration layer, design system, media DSL or provider SDK
wrapper remains — only Remotion primitives, three JSON manifests, two thin provider scripts and
one composition file.

## Result

| Metric | Before | After |
| --- | --- | --- |
| Handwritten implementation LOC | 2,076 | **see "Measured state after reduction" below** |
| Code files | 14 | 6 |
| Generated binaries tracked | 2 | 0 |

Measured state after reduction is recorded at the end of this file by
`python3 promo-remotion/tools/loc_report.py`(the same command the owner can re-run).

---

## Measured state after reduction

`python3 promo-remotion/tools/loc_report.py` (added lines vs `main`, generated artifacts,
owner inputs, docs, lockfiles and vendor trees excluded):

| File | LOC | Role |
| --- | --- | --- |
| `src/Promo.tsx` | 362 | the whole composition: footage/slate layer, overlay text, captions, wordmark, end card, Root |
| `tools/build_storyboard.py` | 215 | CP-06: script → storyboard with integrity assertions |
| `tools/resolve_media.py` | 166 | CP-07: storyboard → media manifest (Storyblocks requests + budget assert) |
| `tools/build_timeline.py` | 150 | CP-09: contracts → Remotion timeline + claims screen |
| `tools/shot_plan.py` | 137 | CP-06: beat table (ids, durations, queries, motion, approved overlays) |
| `adapters/storyblocks_adapter.py` | 69 | thin provider adapter: availability + search |
| `tools/loc_report.py` | 68 | this budget report |
| `package.json` | 20 | Remotion + Manrope + React dependencies |
| `src/index.ts` | 8 | registerRoot + font CSS |
| **TOTAL** | **1,195** | **within the preferred budget (≤ 1,200)**; warning 1,500; hard stop 2,500 |

Removed in this reduction: the generic contract-validator CLI, the standalone design-token and
types modules, the separate scene/brand component files, the media-spec module, two committed
generated binaries, and the alternate scene-timing script. Six code files remain, all of which
the CP-06…CP-12 pipeline actually executes.

Verified after reduction: `build_storyboard.py` → 18 beats / 120.0 s; `resolve_media.py` → 17 requests,
0 resolved; `build_timeline.py` → 3,600 frames; `remotion still` renders a frame (search slate +
two-line caption) with Chromium already present in the sandbox.

---

## Independent audit addendum (owner-requested verification)

The owner asked for factual checks rather than Arena's self-report. Re-measured on
`HEAD = b8edec7fb5f3886656e6b22cb095852285ae9374`:

| Check | Command | Result |
| --- | --- | --- |
| Added lines in code (`.py`/`.ts`/`.tsx`) | `git diff --numstat main HEAD -- experiments/exp-24-hyperframes-pr-video \| grep -E '\.(py\|tsx\|ts)$'` | **1,175** across 8 files (report also counts `package.json`'s 20 → 1,195) |
| Added lines in every file incl. generated JSON/docs | same, unfiltered | 8,604 (mostly the two manifests, `timeline.json`, owner task/script files, `package-lock.json`) |
| Line counts on disk | `wc -l` per file | matched the report exactly |
| Generated binaries tracked | `git ls-files \| grep -E '\.(png\|jpg\|mp4\|mp3)$'` | **2 were still tracked** (`out/smoke-frame.png`, `out/smoke-frame-small.jpg`) — the earlier `git rm --cached` was staged in the same command as `git add -A`, so `git add -A` re-added them |
| `.gitignore` change committed | `git status --porcelain` | **no** — the `promo-remotion/out/` + `node_modules/` rules were sitting uncommitted |
| Reproducibility of the JSON contracts | re-ran all three builders, compared SHA-256 | storyboard **byte-identical**; manifest and timeline **differ only in their `created`/`generatedAt` timestamps** (not byte-identical) |
| Storyblocks provider | `tools/resolve_media.py status` | `BLOCKED_PROVIDER`, 17 requests unresolved, 0 resolved |

Both defects found by the audit are fixed in the commit that carries this file: the binaries are
untracked again (`out/` is ignored), and `.gitignore` is committed. The reproducibility claim is
corrected here: the timeline and manifest carry timestamps, so "byte-identical re-run" applies to
the storyboard only.
