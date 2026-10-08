#!/usr/bin/env python3
"""EXP-24 Phase 2 — CP-09 timeline builder.

Frozen contracts in, Remotion timeline out:

  EDITORIAL_STORYBOARD.json  (scene intent, overlay text, narration)
  MEDIA_MANIFEST.json        (resolved asset per scene)
  VOICE_MANIFEST.json        (measured narration segment per scene, if present)
  MUSIC_MANIFEST.json        (music bed, if present)
        ↓
  src/generated/timeline.json   (consumed by the Remotion composition)

Timing is **derived**, never hardcoded:
  duration = max(storyboard intent, narration segment + breath pad)
the whole film is then held inside the accepted 110–125 s window and every
scene records where its duration came from (`duration_source`).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMO = HERE.parent
EXP = PROMO.parent
OUT = PROMO / "src" / "generated" / "timeline.json"

STORYBOARD = EXP / "EDITORIAL_STORYBOARD.json"
MEDIA = EXP / "MEDIA_MANIFEST.json"
VOICE = EXP / "VOICE_MANIFEST.json"
MUSIC = EXP / "MUSIC_MANIFEST.json"

BREATH_PAD_S = 0.8          # silence kept after the last word of a scene
MAX_LINES = 2
MAX_CHARS_PER_LINE = 44
MOTION_BY_ORDER = ["push-in", "drift-right", "drift-left", "push-out", "push-in", "drift-right"]


def caption_lines(text: str) -> list[str]:
    """Greedy wrap into <=2 short lines, then rebalance so the second line is not tiny."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= MAX_CHARS_PER_LINE or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) <= MAX_LINES:
        return lines
    # Too long for two lines: rebalance the whole text into two halves at word boundaries.
    half = len(words) // 2
    first = " ".join(words[:half])
    second = " ".join(words[half:])
    return [first, second]


def load(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def main() -> int:
    storyboard = json.loads(STORYBOARD.read_text(encoding="utf-8"))
    media = load(MEDIA)
    voice = load(VOICE)
    music = load(MUSIC)

    fps = storyboard["format"]["fps"]
    width = storyboard["format"]["width"]
    height = storyboard["format"]["height"]
    low, high = storyboard["format"]["accepted_duration_range_seconds"]

    assets_by_scene: dict[str, list[dict]] = {}
    for asset in (media or {}).get("assets", []):
        assets_by_scene.setdefault(asset["scene_id"], []).append(asset)

    clips_by_scene = {c["scene_id"]: c for c in (voice or {}).get("clips", [])}

    scenes = []
    for scene in sorted(storyboard["scenes"], key=lambda s: s["order"]):
        intent = float(scene["target_duration_seconds"])
        clip = clips_by_scene.get(scene["id"])
        measured = float(clip["duration_seconds"]) if clip else None
        if measured is not None:
            duration = max(intent, measured + BREATH_PAD_S)
            source = f"voice({measured:.2f}s)+{BREATH_PAD_S}s pad" if measured + BREATH_PAD_S > intent \
                else f"storyboard intent ({intent:.0f}s) > voice+pad ({measured + BREATH_PAD_S:.2f}s)"
        else:
            duration = intent
            source = f"storyboard intent ({intent:.0f}s); no voice yet"
        assets = assets_by_scene.get(scene["id"], [])
        primary = assets[0] if assets else None
        overlay = scene.get("overlay_text") or {}
        scenes.append({
            "id": scene["id"],
            "order": scene["order"],
            "block": scene["block"],
            "durationSeconds": round(duration, 3),
            "title": overlay.get("title"),
            "subtitle": overlay.get("subtitle"),
            "label": overlay.get("label"),
            "captionLines": caption_lines(scene.get("narration") or ""),
            "narration": scene.get("narration"),
            "audio": clip.get("path") if clip else None,
            "audioOffset": clip.get("offset_in_scene_seconds") if clip else None,
            "motion": MOTION_BY_ORDER[scene["order"] % len(MOTION_BY_ORDER)],
            "asset": None if not primary else {
                "file": primary.get("file"),
                "kind": primary.get("kind"),
                "provider": primary.get("provider"),
                "providerKind": primary.get("provider_kind"),
                "status": primary.get("asset_status"),
                "focalPoint": primary.get("focal_point", [0.5, 0.5]),
            },
            "brand": scene["id"] == "brand-close",
            "durationSource": source,
        })

    # Hold the film inside the accepted window without touching approved narration.
    total = sum(s["durationSeconds"] for s in scenes)
    if total > high:
        # Trim breath from the longest held scenes first (never below storyboard intent).
        over = total - high
        for s in sorted(scenes, key=lambda s: -s["durationSeconds"]):
            if over <= 0.01:
                break
            floor = next(x["target_duration_seconds"] for x in storyboard["scenes"] if x["id"] == s["id"])
            reducible = max(0.0, s["durationSeconds"] - float(floor))
            take = min(reducible, over)
            s["durationSeconds"] = round(s["durationSeconds"] - take, 3)
            s["durationSource"] += f"; trimmed {take:.2f}s to respect the {high}s cap"
            over -= take
    elif total < low:
        # Extend the quietest shots (brand close and result) with additional hold time.
        need = low - total
        for s in scenes:
            if need <= 0.01:
                break
            if s["id"] in {"result", "brand-close", "hook-reveal"}:
                add = min(1.5, need)
                s["durationSeconds"] = round(s["durationSeconds"] + add, 3)
                s["durationSource"] += f"; +{add:.2f}s hold to reach the {low}s minimum"
                need -= add

    cursor = 0.0
    for s in scenes:
        s["startSeconds"] = round(cursor, 3)
        s["startFrame"] = int(round(cursor * fps))
        s["durationFrames"] = max(1, int(round(s["durationSeconds"] * fps)))
        s["startSeconds"] = round(s["startFrame"] / fps, 3)
        cursor = s["startSeconds"] + s["durationFrames"] / fps

    timeline = {
        "version": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fps": fps,
        "width": width,
        "height": height,
        "totalSeconds": round(cursor, 3),
        "totalFrames": sum(s["durationFrames"] for s in scenes),
        "audioMix": (voice or {}).get("mix_path"),
        "musicGainDb": (music or {}).get("gain_db", -21.0),
        "sourceContracts": {
            "storyboard": STORYBOARD.name,
            "media": MEDIA.name if media else None,
            "voice": VOICE.name if voice else None,
            "music": MUSIC.name if music else None,
        },
        "scenes": scenes,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"timeline: {len(scenes)} scenes, {timeline['totalSeconds']}s, "
          f"{timeline['totalFrames']} frames @ {fps}fps -> {OUT.relative_to(PROMO)}")
    for s in scenes:
        print(f"  {s['order']:>2}. {s['id']:<18} {s['startSeconds']:>7.2f}s "
              f"+{s['durationSeconds']:>5.2f}s  {s['durationSource']}")
    if not (low <= timeline["totalSeconds"] <= high):
        print(f"WARNING: total {timeline['totalSeconds']}s outside {low}–{high}s")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
