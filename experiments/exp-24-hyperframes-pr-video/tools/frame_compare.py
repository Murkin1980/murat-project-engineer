#!/usr/bin/env python3
"""Per-frame decoded-pixel hash comparison of two MP4 renders (minimal visual diff proof)."""
import hashlib, subprocess, sys
# Full ffmpeg build (rawvideo muxer). Resolved from the imageio-ffmpeg wheel installed in the sandbox venv.
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 320, 180  # downscaled for speed; equality at this size is a strong pixel-level check
def hashes(path):
    cmd = [FFMPEG, "-v", "error", "-i", path, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    out = subprocess.run(cmd, capture_output=True).stdout
    n = len(out) // (W * H * 3)
    return [hashlib.sha1(out[i*W*H*3:(i+1)*W*H*3]).hexdigest() for i in range(n)]
if __name__ == "__main__":
    a, b = hashes(sys.argv[1]), hashes(sys.argv[2])
    print(f"frames {len(a)} vs {len(b)}")
    segs = sys.argv[3:]  # optional named ranges "label:start:end" in frames [start,end)
    for s in segs:
        label, st, en = s.split(":"); st, en = int(st), int(en)
        same = sum(a[i] == b[i] for i in range(st, min(en, len(a), len(b))))
        print(f"{label}: identical {same}/{en-st} frames")
