#!/usr/bin/env python3
"""EXP-24 Phase 2 — CP-06 storyboard builder.

script (source of truth) + tools/shot_plan.py  ->  EDITORIAL_STORYBOARD.json

Aborts unless: narration slices rejoin verbatim; beat durations sum to the script
timecodes; every overlay comes from the script's approved on-screen text; every beat
traces to a script scene.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMO = HERE.parent
EXP = PROMO.parent
SCRIPT = EXP / "SALAMAT_PROMO_SCRIPT.md"
OUT = EXP / "EDITORIAL_STORYBOARD.json"
BLOCKS = {1: "A", 2: "B", 3: "B", 4: "C", 5: "C", 6: "D", 7: "E", 8: "E", 9: "F"}
ACCEPTED_RANGE = (110, 125)

sys.path.insert(0, str(HERE))
from shot_plan import GENERATIVE_ALLOWLIST, PLAN, beats_of  # noqa: E402


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def parse_script() -> list[dict]:
    """Scene number, timecode, video direction, approved on-screen text and narration."""
    body = SCRIPT.read_text(encoding="utf-8").split("---", 1)[1]
    pattern = re.compile(
        r"^## Scene (?P<number>\d+) — (?P<title>.+?)\n"
        r"\*\*(?P<start>\d+:\d+)–(?P<end>\d+:\d+)\*\*\n(?P<rest>.*?)(?=^## Scene |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    scenes = []
    for match in pattern.finditer(body):
        rest = match.group("rest")

        def section(name: str) -> str:
            found = re.search(rf"^### {name}\n(?P<body>.*?)(?=^### |^---\s*$|^## |\Z)",
                              rest, re.MULTILINE | re.DOTALL)
            return found.group("body").strip() if found else ""

        start, end = match.group("start"), match.group("end")
        scenes.append({
            "number": int(match.group("number")),
            "title": match.group("title").strip(),
            "start": int(start.split(":")[0]) * 60 + float(start.split(":")[1]),
            "end": int(end.split(":")[0]) * 60 + float(end.split(":")[1]),
            "video": section("Video"),
            "on_screen_text": [l.strip() for l in section("On-screen text").splitlines() if l.strip()],
            "narration": norm(section("Narration")),
        })
    if not scenes:
        raise SystemExit("no scenes parsed from the owner script")
    return scenes


def build() -> dict:
    script = parse_script()
    errors: list[str] = []
    beats: list[dict] = []
    order = 0

    for scene in script:
        plan = beats_of(scene["number"])
        if not plan:
            errors.append(f"script scene {scene['number']} has no beats planned")
            continue

        joined = norm(" ".join(b["narration"] for b in plan))
        if joined != scene["narration"]:
            errors.append(f"scene {scene['number']}: beats do not reproduce the script narration\n"
                          f"    script: {scene['narration']!r}\n    beats : {joined!r}")

        span = round(scene["end"] - scene["start"], 3)
        planned = round(sum(b["seconds"] for b in plan), 3)
        if abs(span - planned) > 0.001:
            errors.append(f"scene {scene['number']}: beats total {planned}s, script span {span}s")

        approved = set(scene["on_screen_text"])
        cursor = scene["start"]
        for beat in plan:
            title, subtitle = beat["title"], beat["subtitle"]
            for value in (title, subtitle):
                if value and value not in approved:
                    errors.append(f"scene {scene['number']}/{beat['id']}: overlay {value!r} is not in "
                                  f"the script's approved on-screen text {sorted(approved)}")
            order += 1
            queries = [q for q in (beat["query"],) if q]
            fallbacks = [q for q in (beat["fallback"],) if q]
            beats.append({
                "id": beat["id"],
                "order": order,
                "script_scene": scene["number"],
                "script_timecode": f"{int(scene['start']) // 60}:{int(scene['start']) % 60:02d}"
                                   f"–{int(scene['end']) // 60}:{int(scene['end']) % 60:02d}",
                "start_seconds": round(cursor, 3),
                "target_duration_seconds": float(beat["seconds"]),
                "block": BLOCKS[scene["number"]],
                "narration_part": beat["narration"],
                "overlay_text": {"title": title, "label": None, "subtitle": subtitle},
                "visual_intent": beat["intent"],
                "visual_source_preference": "GENERATIVE" if not queries else "REAL_FOOTAGE",
                "media_authority": "generative — allowlisted branded graphic" if not queries
                                   else "REAL LICENSED VIDEO — Storyblocks first",
                "generative_allowance": (GENERATIVE_ALLOWLIST.get(scene["number"], "none")
                                         if not queries else "none"),
                "footage_queries": queries,
                "fallback_queries": fallbacks,
                "motion": beat["motion"],
                "owner_directed": beat["owner_directed"],
                "source_grounding": [f"SALAMAT_PROMO_SCRIPT.md#scene-{scene['number']}"],
            })
            cursor = round(cursor + beat["seconds"], 3)

    if errors:
        for error in errors:
            print(f"  ERROR {error}", file=sys.stderr)
        raise SystemExit(f"storyboard aborted — {len(errors)} integrity problem(s)")

    total = round(sum(b["target_duration_seconds"] for b in beats), 3)
    return {
        "contract": "EDITORIAL_STORYBOARD",
        "version": 3,
        "experiment": "EXP-24 Phase 2",
        "fixture": "Salamat Mebel 2-minute promo",
        "created": "2026-10-08",
        "narrative_source_of_truth": {
            "file": "SALAMAT_PROMO_SCRIPT.md",
            "status": "OWNER-APPROVED BASELINE SCRIPT",
            "rule": "Scene meaning, narration wording and the mandatory tactile countertop shot are "
                    "preserved; only shot decomposition, footage queries and timing detail are added.",
            "enforced_by": "tools/build_storyboard.py (verbatim narration, script timecodes, "
                           "approved-only overlay text)",
        },
        "mode": "REAL_FOOTAGE",
        "language": "ru",
        "format": {
            "width": 1920, "height": 1080, "aspect": "16:9", "fps": 30,
            "target_duration_seconds": total, "accepted_duration_range_seconds": list(ACCEPTED_RANGE),
            "hard_cap_seconds": 130, "timecode_source": "sum of the script's own scene timecodes",
        },
        "media_source_authority": [
            "REAL LICENSED VIDEO FOOTAGE — Storyblocks first",
            "other explicitly approved licensed real footage",
            "existing owner/project media",
            "bounded neutral placeholder (pipeline testing only)",
            "generative media, allowlist only (max 3 before owner review)"],
        "generative_media_policy": {
            "budget_before_owner_review": 3,
            "allowlist": ["logo reveal", "abstract branded transition", "simple diagram/graphic",
                          "branded end card", "visual bridge with no reasonable real source"],
            "used": [b["id"] for b in beats if b["visual_source_preference"] == "GENERATIVE"],
            "forbidden_categories_never_generated": [
                "furniture production", "CNC/cutting/edgebanding", "workers or craftspeople",
                "client consultation", "installation", "kitchens", "wardrobes", "finished furniture",
                "interiors", "hands touching furniture/materials", "countertop tactile shot",
                "hardware/detail footage"],
            "generated_imagery_count": 0, "generated_video_count": 0},
        "delivery_mix_target": {
            "REAL_FOOTAGE_percent": [75, 80],
            "GENERATIVE_percent": [20, 25],
            "note": "Task-level design target. The authoritative script allows generative media only in "
                    "scenes 1 (wordmark) and 9 (end card), so this edit's achievable generative share is "
                    "~7 % once real footage is licensed.",
        },
        "claims_policy": {
            "forbidden": ["certifications", "production volumes or capacity", "warranty terms",
                          "delivery times", "addresses, phone numbers, e-mail", "awards",
                          "client counts", "years on the market", "price levels and superlatives",
                          "named partners, suppliers or compliance claims"],
            "cta": "Salamat Mebel — Мебель, созданная под ваше пространство",
            "enforced_by": "tools/build_timeline.py (screen_claims)"},
        "script_scenes": [{
            "number": s["number"], "title": s["title"],
            "timecode": f"{int(s['start']) // 60}:{int(s['start']) % 60:02d}"
                        f"–{int(s['end']) // 60}:{int(s['end']) % 60:02d}",
            "duration_seconds": round(s["end"] - s["start"], 3),
            "video_direction": s["video"], "on_screen_text": s["on_screen_text"],
            "narration": s["narration"],
            "beats": [b["id"] for b in beats if b["script_scene"] == s["number"]],
        } for s in script],
        "beats": beats,
        # kept under the historical key name so downstream readers stay compatible
        "scenes": beats,
    }


def main() -> int:
    storyboard = build()
    OUT.write_text(json.dumps(storyboard, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = storyboard["format"]["target_duration_seconds"]
    print(f"storyboard: {len(storyboard['beats'])} beats, {total}s, "
          f"{len(storyboard['script_scenes'])} script scenes → {OUT.name}")
    for beat in storyboard["beats"]:
        print(f"  {beat['order']:>2}. {beat['id']:<22} {beat['start_seconds']:>6.1f}s "
              f"+{beat['target_duration_seconds']:>4}s [{beat['script_timecode']}] "
              f"{beat['narration_part'][:52]}")
    low, high = storyboard["format"]["accepted_duration_range_seconds"]
    if not low <= total <= high:
        print(f"WARNING: {total}s outside {low}–{high}s")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
