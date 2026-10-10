#!/usr/bin/env python3
"""Write a deterministic silent CBR MP3 of a target duration (EXP-23 CP-01 fallback).

Used only for the three beats whose TTS clips hit Arena's per-turn synthesis
limit: the engine plays the silent clip on its normal clock (captions carry the
text); files are replaced by real synthesized audio when the remaining clips
are generated. MPEG-1 Layer III, 128 kbps, 44.1 kHz, stereo: 417-byte frames
(4-byte header + 413 zeroed payload bytes), 1152 samples/frame.

Usage: python3 silent_mp3.py out.mp3 <seconds>
"""
import struct
import sys
from pathlib import Path

FRAME = bytes([0xFF, 0xFB, 0x90, 0x00]) + b"\x00" * 413  # 417 B, 26.122 ms each
SAMPLES = 1152
RATE = 44100


def main():
    out, seconds = Path(sys.argv[1]), float(sys.argv[2])
    n = max(1, round(seconds * RATE / SAMPLES))
    out.write_bytes(FRAME * n)
    dur = n * SAMPLES / RATE
    print(f"{out}: {n} frames, {out.stat().st_size} bytes, {dur:.3f}s (silent placeholder)")


if __name__ == "__main__":
    main()
