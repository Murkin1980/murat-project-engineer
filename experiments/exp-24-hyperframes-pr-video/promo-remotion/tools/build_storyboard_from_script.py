#!/usr/bin/env python3
"""EXP-24 Phase 2 — CP-06 storyboard builder.

`SALAMAT_PROMO_SCRIPT.md`  (owner-approved narrative source-of-truth)
        +  `tools/shot_plan.py` (shot decomposition, footage queries, overlays)
                ↓
        `EDITORIAL_STORYBOARD.json`

The builder does not invent narrative. It asserts:

  1. every shot's narration part, joined in order, reproduces the script narration
     **verbatim** (whitespace-normalised) — so wording cannot drift;
  2. shot durations sum to the script scene's own timecode span;
  3. overlay text is the script's "On-screen text" section, unmodified;
  4. totals stay inside the accepted duration window.

Any mismatch aborts the build.
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

sys.path.insert(0, str(HERE))
from shot_plan import SHOTS  # noqa: E402

FPS = 30
ACCEPTED_RANGE = (110, 125)
HARD_CAP = 130
GENERATIVE_BUDGET_BEFORE_REVIEW = 3


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def parse_timecode(value: str) -> float:
    minutes, seconds = value.split(":")
    return int(minutes) * 60 + float(seconds)


def parse_script(path: Path) -> list[dict]:
    """Split the owner script into scenes with timecodes, on-screen text and narration."""
    raw = path.read_text(encoding="utf-8")
    body = raw.split("---", 1)[1]
    pattern = re.compile(
        r"^## Scene (?P<number>\d+) — (?P<title>.+?)\n"
        r"\*\*(?P<start>\d+:\d+)–(?P<end>\d+:\d+)\*\*\n"
        r"(?P<rest>.*?)(?=^## Scene |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    scenes = []
    for match in pattern.finditer(body):
        rest = match.group("rest")

        def section(name: str) -> str:
            found = re.search(
                rf"^### {name}\n(?P<body>.*?)(?=^### |^---\s*$|^## |\Z)",
                rest,
                re.MULTILINE | re.DOTALL,
            )
            if not found:
                return ""
            body = found.group("body")
            # drop markdown bullets' markers but keep their text
            return body.strip()

        narration = normalise(section("Narration"))
        scenes.append({
            "number": int(match.group("number")),
            "title": match.group("title").strip(),
            "start": parse_timecode(match.group("start")),
            "end": parse_timecode(match.group("end")),
            "video": section("Video"),
            "on_screen_text": [
                line.strip() for line in section("On-screen text").splitlines() if line.strip()
            ],
            "narration": narration,
        })
    if not scenes:
        raise SystemExit("could not parse any scenes from the owner script")
    return scenes


def build() -> dict:
    script = parse_script(SCRIPT)
    script_by_number = {s["number"]: s for s in script}
    missing = sorted(set(SHOTS) - set(script_by_number))
    if missing:
        raise SystemExit(f"shot plan references script scenes that do not exist: {missing}")

    errors: list[str] = []
    scenes: list[dict] = []
    order = 0

    for number, script_scene in sorted(script_by_number.items()):
        shots = SHOTS.get(number, [])
        if not shots:
            errors.append(f"script scene {number} has no shots planned")
            continue

        # 1. narration integrity
        joined = normalise(" ".join(s["narration_part"] for s in shots if s.get("narration_part")))
        if joined != script_scene["narration"]:
            errors.append(
                f"scene {number}: shot narration does not reproduce the approved script.\n"
                f"    script : {script_scene['narration']!r}\n"
                f"    shots  : {joined!r}"
            )

        # 2. duration integrity
        span = round(script_scene["end"] - script_scene["start"], 3)
        planned = round(sum(s["duration"] for s in shots), 3)
        if abs(span - planned) > 0.001:
            errors.append(f"scene {number}: shots total {planned}s but script span is {span}s")

        # 3. overlay integrity — the film may only use the script's approved on-screen text
        approved = set(script_scene["on_screen_text"])
        for shot in shots:
            overlay = shot["overlay"]
            for value in overlay.values():
                if value and value not in approved:
                    errors.append(
                        f"scene {number}/{shot['id']}: overlay {value!r} is not in the script's "
                        f"approved on-screen text {sorted(approved)}"
                    )

        cursor = script_scene["start"]
        for shot in shots:
            order += 1
            scenes.append({
                "id": shot["id"],
                "order": order,
                "script_scene": number,
                "script_scene_title": script_scene["title"],
                "script_timecode": f"{int(script_scene['start']) // 60}:{int(script_scene['start']) % 60:02d}"
                                   f"–{int(script_scene['end']) // 60}:{int(script_scene['end']) % 60:02d}",
                "script_narration": script_scene["narration"],
                "narration": shot["narration_part"] or None,
                "start_seconds": round(cursor, 3),
                "target_duration_seconds": shot["duration"],
                "block": None,  # filled below
                "editorial_purpose": shot["visual_intent"],
                "visual_intent": shot["visual_intent"],
                "visual_source_preference": "GENERATIVE" if shot["id"] == "brand-close"
                                            else "REAL_FOOTAGE",
                "media_authority_rank": 5 if shot["id"] == "brand-close" else 1,
                "media_authority": "generative — allowlisted branded graphic" if shot["id"] == "brand-close"
                                   else "REAL LICENSED VIDEO — Storyblocks first",
                "generative_allowance": shot["generative_allowance"],
                "footage_queries": shot["footage_queries"],
                "fallback_queries": shot["fallback_queries"],
                "motion": shot["motion"],
                "in_out_intent": shot["in_out_intent"],
                "framing_note": shot["framing_note"],
                "overlay_text": shot["overlay"],
                "audio": "narration + low-profile music bed; footage audio muted",
                "source_grounding": [f"SALAMAT_PROMO_SCRIPT.md#scene-{number}"],
                "approval_notes": shot["framing_note"],
            })
            cursor = round(cursor + shot["duration"], 3)

    if errors:
        for error in errors:
            print(f"  ERROR {error}", file=sys.stderr)
        raise SystemExit(f"storyboard build aborted — {len(errors)} integrity problem(s)")

    # Blocks A–F from the original task map onto script scenes; kept as grouping metadata only.
    block_of = {1: "A", 2: "B", 3: "B", 4: "C", 5: "C", 6: "D", 7: "E", 8: "E", 9: "F"}
    for scene in scenes:
        scene["block"] = block_of[scene["script_scene"]]

    total = round(sum(s["target_duration_seconds"] for s in scenes), 3)
    generative_scenes = [s["id"] for s in scenes if s["visual_source_preference"] == "GENERATIVE"]

    storyboard = {
        "contract": "EDITORIAL_STORYBOARD",
        "version": 2,
        "experiment": "EXP-24 Phase 2",
        "fixture": "Salamat Mebel 2-minute promo",
        "created": "2026-10-08",
        "narrative_source_of_truth": {
            "file": "SALAMAT_PROMO_SCRIPT.md",
            "status": "OWNER-APPROVED BASELINE SCRIPT",
            "rule": "Scene meaning, narration wording and the mandatory tactile countertop shot are "
                    "preserved; only shot decomposition, footage queries and timing detail are added.",
            "adaptation_allowed_for": ["voice timing", "subtitle readability", "natural speech",
                                       "scene timing"],
        },
        "mode": "REAL_FOOTAGE",
        "language": "ru",
        "format": {
            "width": 1920,
            "height": 1080,
            "aspect": "16:9",
            "fps": FPS,
            "target_duration_seconds": total,
            "accepted_duration_range_seconds": list(ACCEPTED_RANGE),
            "hard_cap_seconds": HARD_CAP,
            "timecode_source": "sum of the script's own scene timecodes",
        },
        "media_source_authority": [
            "REAL LICENSED VIDEO FOOTAGE — Storyblocks first",
            "other explicitly approved licensed real footage",
            "existing owner/project media",
            "bounded neutral placeholder (pipeline testing only)",
            "generative media, allowlist only (max 3 before owner review)",
        ],
        "generative_media_policy": {
            "budget_before_owner_review": GENERATIVE_BUDGET_BEFORE_REVIEW,
            "allowlist": ["logo reveal", "abstract branded transition", "simple diagram/graphic",
                          "branded end card", "visual bridge with no reasonable real source"],
            "used": [s for s in generative_scenes],
            "forbidden_categories_never_generated": [
                "furniture production", "CNC/cutting/edgebanding", "workers or craftspeople",
                "client consultation", "installation", "kitchens", "wardrobes", "finished furniture",
                "interiors", "hands touching furniture/materials", "countertop tactile shot",
                "hardware/detail footage",
            ],
            "generated_imagery_count": 0,
            "generated_video_count": 0,
        },
        "delivery_mix_target": {
            "REAL_FOOTAGE_percent": [75, 80],
            "GENERATIVE_percent": [20, 25],
            "note": "Design target inherited from the task; the authoritative script allows generative "
                    "media only in scenes 1 (wordmark) and 9 (end card), so the achievable generative "
                    "share of this 120 s edit is ~7 % once real footage is licensed.",
        },
        "script_scenes": [
            {
                "number": s["number"],
                "title": s["title"],
                "timecode": f"{int(s['start']) // 60}:{int(s['start']) % 60:02d}"
                            f"–{int(s['end']) // 60}:{int(s['end']) % 60:02d}",
                "duration_seconds": round(s["end"] - s["start"], 3),
                "video_direction": s["video"],
                "on_screen_text": s["on_screen_text"],
                "narration": s["narration"],
                "storyboard_scene_ids": [x["id"] for x in scenes if x["script_scene"] == s["number"]],
            }
            for s in script
        ],
        "claims_policy": {
            "forbidden": ["certifications", "production volumes or capacity", "warranty terms",
                          "delivery times", "addresses, phone numbers, e-mail", "awards",
                          "client counts", "years on the market", "price levels and superlatives",
                          "named partners, suppliers or compliance claims"],
            "cta": "Salamat Mebel — Мебель, созданная под ваше пространство",
        },
        "scenes": scenes,
    }
    return storyboard


def main() -> int:
    storyboard = build()
    OUT.write_text(json.dumps(storyboard, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = storyboard["format"]["target_duration_seconds"]
    print(f"storyboard built from the owner script: {len(storyboard['scenes'])} scenes, {total}s, "
          f"{len(storyboard['script_scenes'])} script scenes → {OUT.name}")
    for scene in storyboard["scenes"]:
        narration = scene["narration"] or "—"
        print(f"  {scene['order']:>2}. {scene['id']:<22} {scene['start_seconds']:>6.1f}s "
              f"+{scene['target_duration_seconds']:>4}s  [{scene['script_timecode']}] {narration[:58]}")
    low, high = storyboard["format"]["accepted_duration_range_seconds"]
    if not (low <= total <= high):
        print(f"WARNING: {total}s outside the accepted {low}–{high}s window")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
