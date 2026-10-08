#!/usr/bin/env python3
"""EXP-24 Phase 2 — contract validator (stdlib only).

Validates the frozen editorial/editorial-adjacent contracts before any expensive
media or render step. Fails loudly; never edits the contracts.

Usage:
  python3 tools/validate_contracts.py storyboard
  python3 tools/validate_contracts.py media
  python3 tools/validate_contracts.py voice
  python3 tools/validate_contracts.py music
  python3 tools/validate_contracts.py all
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMO_DIR = HERE.parent                       # .../promo-remotion
EXP_DIR = PROMO_DIR.parent                    # .../exp-24-hyperframes-pr-video

STORYBOARD = EXP_DIR / "EDITORIAL_STORYBOARD.json"
MEDIA = EXP_DIR / "MEDIA_MANIFEST.json"
VOICE = EXP_DIR / "VOICE_MANIFEST.json"
MUSIC = EXP_DIR / "MUSIC_MANIFEST.json"

REQUIRED_SCENE_FIELDS = [
    "id", "order", "block", "start_seconds", "target_duration_seconds",
    "narration", "editorial_purpose", "visual_intent",
    "visual_source_preference", "footage_queries", "fallback_queries",
    "overlay_text", "source_grounding", "approval_notes",
]

# Claims the owner forbade (PROMO_BRIEF.md §5). Kept narrow on purpose: they must
# never fire on approved wording.
FORBIDDEN_PATTERNS = [
    (r"\b\d{2,}[\s-]?лет\b", "years on the market"),
    (r"\bгаранти", "warranty"),
    (r"\bсертифиц", "certification"),
    (r"\bсрок[аи]?\s+доставки\b", "delivery time"),
    (r"\bбесплатн", "free-of-charge promise"),
    (r"\bскидк", "discount"),
    (r"\+?\d[\d\s\-()]{7,}\d", "phone-like number"),
    (r"\bлучш(ий|ая|ее|ие)\b", "superlative"),
    (r"№\s*1|номер\s+один", "number-one claim"),
    (r"\b\d+[\s-]?(клиент|проект|заказчик|сотрудник)", "client/staff count"),
    (r"\bмлн|\bтыс(яч)?\b", "volume claim"),
    (r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\b", "e-mail"),
    (r"\bwww\.|\.kz\b|\.com\b", "site/social handle"),
]

errors: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load(path: Path) -> dict:
    if not path.exists():
        fail(f"missing file: {path.relative_to(EXP_DIR.parent.parent)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        fail(f"{path.name}: not valid JSON: {exc}")
        return {}


def scene_text(scene: dict) -> str:
    overlay = scene.get("overlay_text") or {}
    parts = [scene.get("narration") or ""]
    parts += [str(v) for v in overlay.values() if v]
    return "\n".join(parts)


def check_claims(scene: dict) -> None:
    text = scene_text(scene)
    for pattern, label in FORBIDDEN_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            fail(f"scene {scene.get('id')}: forbidden claim ({label}): {m.group(0)!r}")


def validate_storyboard() -> tuple[dict, list[dict]]:
    sb = load(STORYBOARD)
    scenes = sb.get("scenes", [])
    if not scenes:
        fail("storyboard has no scenes")
        return sb, []

    fmt = sb.get("format", {})
    seen: set[str] = set()
    cursor = 0.0
    for index, scene in enumerate(scenes, start=1):
        sid = scene.get("id", f"<scene#{index}>")
        for field in REQUIRED_SCENE_FIELDS:
            if field not in scene:
                fail(f"scene {sid}: missing field {field}")
        if sid in seen:
            fail(f"scene {sid}: duplicate id")
        seen.add(sid)
        if scene.get("order") != index:
            fail(f"scene {sid}: order {scene.get('order')} != position {index}")
        start = float(scene.get("start_seconds", -1))
        if abs(start - cursor) > 1e-6:
            fail(f"scene {sid}: start {start} does not continue the timeline at {cursor}")
        dur = float(scene.get("target_duration_seconds", 0))
        if dur <= 0:
            fail(f"scene {sid}: non-positive duration")
        cursor = start + dur
        preference = scene.get("visual_source_preference")
        if preference not in {"REAL_FOOTAGE", "GENERATIVE"}:
            fail(f"scene {sid}: bad visual_source_preference {preference!r}")
        if preference == "REAL_FOOTAGE" and not scene.get("footage_queries"):
            fail(f"scene {sid}: REAL_FOOTAGE scene without footage_queries")
        if not scene.get("source_grounding"):
            fail(f"scene {sid}: no source_grounding")
        if not (scene.get("narration") or "").strip():
            warn(f"scene {sid}: empty narration")
        check_claims(scene)

    total = cursor
    low, high = fmt.get("accepted_duration_range_seconds", [110, 125])
    if not (low <= total <= high):
        fail(f"storyboard total {total}s outside accepted range {low}–{high}s")
    if fmt.get("target_duration_seconds") != total:
        warn(f"format.target_duration_seconds={fmt.get('target_duration_seconds')} "
             f"but scenes sum to {total}")

    scene_ids = [s["id"] for s in scenes]
    print(f"  scenes={len(scenes)} total={total}s range={low}–{high}s")
    print(f"  real_footage_scenes={sum(1 for s in scenes if s.get('visual_source_preference') == 'REAL_FOOTAGE')} "
          f"generative_scenes={sum(1 for s in scenes if s.get('visual_source_preference') == 'GENERATIVE')}")
    return sb, scenes


def validate_media(scenes: list[dict]) -> None:
    mm = load(MEDIA)
    if not mm:
        return
    entries = mm.get("assets", [])
    by_scene = {e.get("scene_id"): e for e in entries}
    if len(by_scene) != len(entries):
        warn("media manifest: duplicate scene_id entries (a scene may have >1 asset)")
    for scene in scenes:
        if scene["id"] not in by_scene:
            fail(f"media manifest: scene {scene['id']} has no asset mapping")
    for entry in entries:
        for field in ["scene_id", "kind", "provider", "license_note", "asset_status"]:
            if not entry.get(field):
                fail(f"media manifest: {entry.get('scene_id')} missing {field}")
        if entry.get("kind") not in {"REAL_FOOTAGE", "GENERATIVE"}:
            fail(f"media manifest: {entry.get('scene_id')} bad kind {entry.get('kind')!r}")
        if entry.get("asset_status") not in {"RESOLVED", "BLOCKED_PROVIDER", "PLANNED"}:
            fail(f"media manifest: {entry.get('scene_id')} bad asset_status {entry.get('asset_status')!r}")
    real = sum(1 for e in entries if e.get("kind") == "REAL_FOOTAGE")
    print(f"  assets={len(entries)} real_footage={real} generative={len(entries) - real}")


def validate_voice(scenes: list[dict]) -> None:
    vm = load(VOICE)
    if not vm:
        return
    clips = {c.get("scene_id"): c for c in vm.get("clips", [])}
    for scene in scenes:
        clip = clips.get(scene["id"])
        if clip is None:
            fail(f"voice manifest: no clip for scene {scene['id']}")
            continue
        if not clip.get("path"):
            fail(f"voice manifest: scene {scene['id']} has no path")
        if not (clip.get("duration_seconds") or 0) > 0:
            fail(f"voice manifest: scene {scene['id']} has no measured duration")
    for field in ["provider", "provider_kind", "model", "voice", "settings", "generated_at"]:
        if not vm.get(field):
            fail(f"voice manifest: missing {field}")
    audio_total = sum((c.get("duration_seconds") or 0) for c in vm.get("clips", []))
    print(f"  clips={len(clips)} measured_audio_total={audio_total:.2f}s")
    if vm.get("narration_total_seconds") and abs(float(vm["narration_total_seconds"]) - audio_total) > 0.05:
        fail("voice manifest: narration_total_seconds does not match summed clip durations")


def validate_music() -> None:
    mu = load(MUSIC)
    if not mu:
        return
    for field in ["provider", "provider_kind", "license_note", "path", "duration_seconds", "gain_db"]:
        if mu.get(field) in (None, ""):
            fail(f"music manifest: missing {field}")
    print(f"  music={mu.get('provider')} duration={mu.get('duration_seconds')}s gain={mu.get('gain_db')}dB")


def main() -> int:
    target = (sys.argv[1] if len(sys.argv) > 1 else "all").lower()
    print(f"validate: {target}")
    sb: dict = {}
    scenes: list[dict] = []
    if target in {"all", "storyboard"}:
        sb, scenes = validate_storyboard()
        if not scenes:
            return finish()
    elif STORYBOARD.exists():
        scenes = json.loads(STORYBOARD.read_text(encoding="utf-8")).get("scenes", [])
    if target in {"all", "media"}:
        validate_media(scenes)
    if target in {"all", "voice"}:
        validate_voice(scenes)
    if target in {"all", "music"}:
        validate_music()
    return finish()


def finish() -> int:
    for w in warnings:
        print(f"  WARN {w}")
    if errors:
        print(f"\nFAIL — {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nOK — contracts valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
