#!/usr/bin/env python3
"""EXP-24 Phase 2 — CP-09 timeline builder.

storyboard + media manifest (+ voice manifest once CP-08 has run) -> src/generated/timeline.json

Timing derives from the script and is extended only when narration does not fit.
The brief's forbidden-claims screen runs over every spoken and on-screen word first.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMO = HERE.parent
EXP = PROMO.parent
OUT = PROMO / "src" / "generated" / "timeline.json"
BREATH_PAD = 0.8
MAX_LINE = 44
MAX_LINES = 2

CLAIMS = [
    (r"\b\d{2,}[\s-]?лет\b", "years on the market"), (r"\bгаранти", "warranty"),
    (r"\bсертифиц", "certification"), (r"\bсрок[аи]?\s+доставки\b", "delivery time"),
    (r"\bбесплатн", "free-of-charge promise"), (r"\bскидк", "discount"),
    (r"\+?\d[\d\s\-()]{7,}\d", "phone-like number"), (r"\bлучш(ий|ая|ее|ие)\b", "superlative"),
    (r"\b\d+[\s-]?(клиент|проект|заказчик|сотрудник)", "client/staff count"),
    (r"\bмлн\b|\bтыс(яч)?\b", "volume claim"), (r"[\w.+-]+@[\w-]+\.[\w.]+", "e-mail"),
    (r"\bwww\.|\.kz\b|\.com\b", "site/social handle"),
]


def wrap(text: str) -> list[str]:
    """Captions: at most two short lines; rebalanced at a word boundary when needed."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= MAX_LINE or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) <= MAX_LINES:
        return lines
    half = len(words) // 2
    return [" ".join(words[:half]), " ".join(words[half:])]


def screen_claims(beats: list[dict]) -> None:
    """The brief's forbidden-claims screen, applied to every spoken and on-screen word."""
    problems = [f"{beat['id']}: {label} → {hit.group(0)!r}"
                for beat in beats
                for pattern, label in CLAIMS
                for hit in [re.search(pattern, " ".join(
                    [beat["narration_part"] or ""] +
                    [v for v in beat["overlay_text"].values() if v]), re.IGNORECASE)]
                if hit]
    if problems:
        for problem in problems:
            print(f"  ERROR forbidden claim — {problem}", file=sys.stderr)
        raise SystemExit("timeline aborted: the film text contains claims the brief forbids")


def main() -> int:
    board = json.loads((EXP / "EDITORIAL_STORYBOARD.json").read_text(encoding="utf-8"))
    media_path = EXP / "MEDIA_MANIFEST.json"
    media = json.loads(media_path.read_text(encoding="utf-8")) if media_path.exists() else {"assets": []}
    voice_path = EXP / "VOICE_MANIFEST.json"
    voice = json.loads(voice_path.read_text(encoding="utf-8")) if voice_path.exists() else {}
    music_path = EXP / "MUSIC_MANIFEST.json"
    music = json.loads(music_path.read_text(encoding="utf-8")) if music_path.exists() else {}

    beats = sorted(board["beats"], key=lambda b: b["order"])
    screen_claims(beats)

    asset_by_beat = {a["scene_id"]: a for a in media.get("assets", [])}
    clip_by_beat = {c["scene_id"]: c for c in voice.get("clips", [])}
    fps = board["format"]["fps"]

    scenes, cursor = [], 0.0
    for beat in beats:
        intent = float(beat["target_duration_seconds"])
        clip = clip_by_beat.get(beat["id"])
        measured = float(clip["duration_seconds"]) if clip else None
        if measured is not None:
            seconds = max(intent, measured + BREATH_PAD)
            source = (f"voice {measured:.2f}s + {BREATH_PAD}s breath"
                      if seconds > intent else f"script timing {intent:.1f}s (voice + breath fits)")
        else:
            seconds = intent
            source = f"script timing {intent:.1f}s; voice not generated yet"
        asset = asset_by_beat.get(beat["id"])
        start_frame = round(cursor * fps)
        duration_frames = max(1, round(seconds * fps))
        scenes.append({
            "id": beat["id"],
            "order": beat["order"],
            "scriptScene": beat["script_scene"],
            "scriptTimecode": beat["script_timecode"],
            "startFrame": start_frame,
            "durationFrames": duration_frames,
            "narrationPart": beat["narration_part"],
            "captionLines": wrap(beat["narration_part"] or "") if beat["narration_part"] else [],
            "title": beat["overlay_text"]["title"],
            "subtitle": beat["overlay_text"]["subtitle"],
            "label": beat["overlay_text"]["label"],
            "motion": beat["motion"],
            "ownerDirected": beat["owner_directed"],
            "audio": clip.get("path") if clip else None,
            "durationSource": source,
            "asset": None if asset is None else {
                "file": asset.get("file"),
                "query": asset["all_queries"][0],
                "status": asset["asset_status"],
                "provider": asset["provider"],
            },
        })
        cursor = (start_frame + duration_frames) / fps

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "version": 4,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fps": fps,
        "width": board["format"]["width"],
        "height": board["format"]["height"],
        "totalSeconds": round(cursor, 3),
        "totalFrames": sum(s["durationFrames"] for s in scenes),
        "audioMix": voice.get("mix_path"),
        "musicGainDb": music.get("gain_db", -21.0),
        "scenes": scenes,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"timeline: {len(scenes)} beats, {round(cursor, 2)}s, "
          f"{sum(s['durationFrames'] for s in scenes)} frames @ {fps}fps → {OUT.relative_to(PROMO)}")
    unresolved = [s["id"] for s in scenes if s["asset"] and s["asset"]["status"] != "RESOLVED"]
    if unresolved:
        print(f"  {len(unresolved)} beat(s) still on neutral slates: {', '.join(unresolved)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
