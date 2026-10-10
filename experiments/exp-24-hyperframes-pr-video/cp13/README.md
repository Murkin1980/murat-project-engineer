# EXP-24 CP-13 — reproduction notes (single-agent bounded proof)

Order of truth: `SCENE_CONTRACT.json` (frozen) → `EDITORIAL_STORYBOARD.json` (timing, captions, marks, cues) → `MEDIA_MANIFEST.json` (slot → file, provenance) → Remotion composition (`../remotion`).

Checks (stdlib Python, run from `experiments/exp-24-hyperframes-pr-video`):

    python3 tools/check_cp13.py                       # coverage, IDs, marks/cues, manifest hashes
    python3 tools/semantic_diff.py OLD.json NEW.json  # field-level minimal diff
    python3 tools/frame_compare.py A.mp4 B.mp4 "label:start:end" ...   # decoded-frame hashes (needs imageio-ffmpeg)

Render (from `remotion/`, after `npm install`; Chromium supplied by the sandbox):

    LD_LIBRARY_PATH=<unpacked al2023 libs> npx remotion render src/index.ts E01S005 out/preview.mp4 --browser-executable=<chromium>

Revision snapshots: `revisions/v1` (before A), `rev-A-after.json`, `rev-B-after-manifest.json`, `rev-C-after.json`; diffs in `REV-*.diff.txt` and `REV-B.*.diff.txt`. Render hashes: `revisions/render_sha256.txt` (MP4s live outside Git).
Generation log: 6 test visuals (B01–B06 v1) + 2 B04 attempts (v2 rejected, v3 used).
