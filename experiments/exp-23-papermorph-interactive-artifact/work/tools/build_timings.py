#!/usr/bin/env python3
"""Build site audio timings.js for the scope-control book (EXP-23 CP-01 TTS fallback).

The stock pipeline (tts.py + Edge TTS) is network-blocked in this sandbox
(verified: speech.platform.bing.com unreachable). Beats are synthesized per-clip
with the Arena TTS tool; long beats are split into two clips at a sentence
boundary so mark times are exact at the clip join. This script derives
timings.js (stock schema: {beat: {dur, marks, cues}}) from the resulting MP3s:

- clip durations are measured exactly (mutagen);
- a mark's time is linear within its clip, anchored exactly at clip joins;
- cues are one per sentence, with the same sentence split as stock tts.py.

Usage:
  python3 build_timings.py --narration content/scope-control/ch01/narration.en.json \
      --audio site/scope-control/ch01/audio/en \
      --splits site/scope-control/ch01/splits.json \
      --out site/scope-control/ch01/audio/en/timings.js [--placeholder]

splits.json: {"beat": "sentence-ending. "} — split after that substring (first occurrence).
--placeholder: no MP3s yet; estimate durations at 0.32 s/word + 0.4 s (page-boot only).
"""
import argparse
import json
import re
from pathlib import Path

MARK = re.compile(r"\[\[(\w+)\]\]")
SENT = re.compile(r"[.?!]\s+")


def split_marks(raw):
    marks, clean, pos = {}, [], 0
    for i, part in enumerate(MARK.split(raw)):
        if i % 2:
            if part in marks:
                raise SystemExit(f"duplicate mark {part!r} in one beat")
            marks[part] = pos
        else:
            clean.append(part)
            pos += len(part)
    return "".join(clean), marks


def clip_duration(path):
    if not path.exists() or path.stat().st_size == 0:
        return None
    try:
        from mutagen.mp3 import MP3
        return round(MP3(path).info.length, 3)
    except Exception:
        return None


def split_raw(raw, after):
    i = raw.find(after)
    if i < 0:
        raise SystemExit(f"split point {after!r} not found")
    j = i + len(after)
    return raw[:j].strip(), raw[j:].strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narration", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--splits", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--placeholder", action="store_true")
    a = ap.parse_args()

    spec = json.loads(Path(a.narration).read_text())
    splits = json.loads(Path(a.splits).read_text())
    out_dir = Path(a.audio)
    timings = {}
    for beat, raw in spec["beats"].items():
        parts = [raw]
        if beat in splits:
            parts = list(reversed(split_raw(raw, splits[beat])))
        clips = []
        for k, part in enumerate(parts):
            clean, marks = split_marks(part)
            name = f"{beat}.mp3" if len(parts) == 1 else f"{beat}{'AB'[k]}.mp3"
            dur = clip_duration(out_dir / name)
            if a.placeholder:
                dur = round(0.32 * len(clean.split()) + 0.4, 3)
            elif dur is None:
                raise SystemExit(f"missing/empty audio for {beat}: {name}")
            clips.append({"clean": clean, "marks": marks, "dur": dur, "chars": len(clean)})
        total = sum(c["dur"] for c in clips)
        # char offset of each clip's start in the full beat text
        offs = []
        s = 0
        for c in clips:
            offs.append(s)
            s += c["chars"]
        # full beat clean text for the sentence cues
        full_clean = "".join(c["clean"] for c in clips)

        def time_at(pos):
            acc = 0
            for idx, c in enumerate(clips):
                off = offs[idx]
                if pos <= off + c["chars"]:
                    frac = (pos - off) / max(1, c["chars"])
                    return round(acc + frac * c["dur"], 3)
                acc += c["dur"]
            raise SystemExit("mark beyond clip text")

        mout = {}
        for c, off in zip(clips, offs):
            for name, p in c["marks"].items():
                mout[name] = time_at(off + p)
        cues = []
        start = 0
        for m in list(SENT.finditer(full_clean)) + [None]:
            end = m.end() if m else len(full_clean)
            text = full_clean[start:end].strip()
            if text:
                cues.append([time_at(start), text])
            start = end
        timings[beat] = {"dur": round(total, 3), "marks": mout, "cues": cues}
    out = "window.TIMINGS = " + json.dumps(timings, indent=1) + ";\n"
    Path(a.out).write_text(out, encoding="utf-8")
    total = sum(t["dur"] for t in timings.values())
    print(f"{len(timings)} beats, {total:.1f}s total -> {a.out}")


if __name__ == "__main__":
    main()
