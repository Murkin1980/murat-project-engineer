# EXP-24 upstream audit — bounded local path

Audit date: 2026-10-06 (UTC)  
Upstream: [`heygen-com/hyperframes`](https://github.com/heygen-com/hyperframes)  
Observed upstream `main`: `b9998dd5a823f70c40fc6978b18c0b63546d967d`  
CLI attempt pin: `hyperframes@0.8.137` (upstream release marker `e7b69785ea1fb473eb4cc5dd22f9bc05942c4138`)

## Reuse boundary

The candidate reuse is the published HyperFrames CLI plus its HTML composition contract. No upstream source is vendored or copied; the experiment composition is a small, local HTML/CSS file.

## Findings from upstream documentation

- **License:** Apache-2.0 ([LICENSE](https://github.com/heygen-com/hyperframes/blob/main/LICENSE)).
- **Runtime:** Node.js 22+ and FFmpeg are the documented local requirements. The documented CLI entrypoints are `npx hyperframes init`, `npx hyperframes preview`, and `npx hyperframes render` ([README](https://github.com/heygen-com/hyperframes/blob/main/README.md), [CLI guide](https://github.com/heygen-com/hyperframes/tree/main/packages/cli)).
- **Composition model:** ordinary HTML/CSS; no React or build step is required. A root composition declares its id, dimensions, start, and duration. Timed visible elements use unique ids, `class="clip"`, `data-start`, `data-duration`, and `data-track-index` ([HTML schema](https://hyperframes.heygen.com/reference/html-schema)).
- **Animation and determinism:** the renderer seeks frames in headless Chrome and encodes through FFmpeg. Upstream describes the same input as producing the same frames/video. Animated compositions should use seekable timelines; this fixture deliberately has no animation, so it does not depend on wall-clock behavior. Repeatability of an MP4 remains unverified unless a render can complete.
- **Preview/render boundary:** preview is a local browser-based Studio; MP4 rendering uses the local headless-browser/FFmpeg path. This is distinct from the separately documented hosted/AWS routes, neither of which is in scope.
- **Media/audio:** HyperFrames supports media/audio compositions, but neither external media nor narration is required here; this storyboard is silent and self-contained.
- **Observed `init` side effect:** the single pinned `init` invocation succeeded, but its skill-freshness check reported unavailable and it fell back to cloning the upstream repository to discover and install ten agent skills. This was not requested and is outside the minimum composition path. The scratch scaffold was removed; the command was not repeated. No upstream source was built or vendored.
- **No manual checkout/build:** no deliberate monorepo clone/build or upstream test suite was used to test the documented minimal CLI boundary.

## Executor preflight

- Node.js: `v22.22.3` — meets the documented version floor.
- npm/npx: `10.9.8` — available.
- FFmpeg: `ffmpeg` was not found on `PATH` at preflight. No installation or system-library repair is in scope.
- Browser/system dependencies: not investigated beyond the single bounded preview/render attempts recorded in `RESULTS.md`.

## Sources

- Upstream repository and observed main revision: https://github.com/heygen-com/hyperframes
- CLI usage: https://github.com/heygen-com/hyperframes/tree/main/packages/cli
- HTML composition schema: https://hyperframes.heygen.com/reference/html-schema
- License: https://github.com/heygen-com/hyperframes/blob/main/LICENSE
- Release marker: https://github.com/heygen-com/hyperframes/commit/e7b69785ea1fb473eb4cc5dd22f9bc05942c4138
