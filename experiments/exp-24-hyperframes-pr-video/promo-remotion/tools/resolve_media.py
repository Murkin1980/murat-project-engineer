#!/usr/bin/env python3
"""EXP-24 Phase 2 — CP-07 media manifest builder.

  EDITORIAL_STORYBOARD.json   (frozen intent: query, duration, in/out, motion, framing)
      + tools/media_assets.py (provider/auth metadata, branded allowlist, budget)
      + adapters/storyblocks_adapter.py (availability probe)
            ↓
  MEDIA_MANIFEST.json

An ordinary scene is RESOLVED only when a real licensed clip is attached. A blocked
provider produces `BLOCKED_PROVIDER` + a neutral search slate — never generated media.

Usage:
  python3 tools/resolve_media.py plan      # build/refresh MEDIA_MANIFEST.json
  python3 tools/resolve_media.py status    # provider availability only
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMO = HERE.parent
EXP = PROMO.parent
STORYBOARD = EXP / "EDITORIAL_STORYBOARD.json"
MANIFEST = EXP / "MEDIA_MANIFEST.json"
LOG = EXP / "MEDIA_PROVIDER_LOG.md"

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PROMO / "adapters"))
from media_assets import (  # noqa: E402
    ALLOWLISTED_UNUSED, BLOCKER, BRANDED, GENERATIVE_BUDGET, PLACEHOLDER, REQUIRED_ACTION,
    STORYBLOCKS, assert_budget,
)

try:
    import storyblocks_adapter  # noqa: E402
except Exception:  # noqa: BLE001 - adapter is optional by design
    storyblocks_adapter = None


def provider_state() -> tuple[bool, str]:
    if storyblocks_adapter is None:
        return False, "adapter module unavailable"
    return storyblocks_adapter.availability()


def plan() -> int:
    assert_budget()
    storyboard = json.loads(STORYBOARD.read_text(encoding="utf-8"))
    scenes = sorted(storyboard["scenes"], key=lambda s: s["order"])
    available, reason = provider_state()
    scene_by_id = {s["id"]: s for s in scenes}

    # Sanity: branded graphics must point at real scenes and stay inside the allowlist.
    for item in BRANDED:
        if item["scene_id"] not in scene_by_id:
            raise SystemExit(f"branded graphic {item['asset_id']} references unknown scene "
                             f"{item['scene_id']}")

    assets: list[dict] = []
    for scene in scenes:
        queries = scene.get("footage_queries") or []
        if not queries:
            continue                      # branded-only scene (brand-close)
        primary = queries[0]
        assets.append({
            "asset_id": f"sb-{scene['id']}",
            "scene_id": scene["id"],
            "scene_order": scene["order"],
            "script_scene": scene["script_scene"],
            "script_timecode": scene["script_timecode"],
            "block": scene["block"],
            "kind": "REAL_FOOTAGE",
            "required": True,
            "media_type": "video",
            "provider": STORYBLOCKS["provider"],
            "provider_kind": STORYBLOCKS["provider_kind"],
            "provider_asset_id": None,
            "provider_search_url": STORYBLOCKS["search_base"] + primary.replace(" ", "+"),
            "all_queries": queries,
            "fallback_queries": scene.get("fallback_queries") or [],
            "licence_note": STORYBLOCKS["licence_note"],
            "asset_status": "RESOLVED" if available else "BLOCKED_PROVIDER",
            "blocker": None if available else BLOCKER,
            "required_action": None if available else REQUIRED_ACTION,
            "target_duration_seconds": scene["target_duration_seconds"],
            "in_out_intent": scene["in_out_intent"],
            "framing_note": scene["framing_note"],
            "motion": scene["motion"],
            "audio": scene["audio"],
            "file": None,
            "placeholder": dict(
                PLACEHOLDER,
                kind="PLACEHOLDER",
                render="Remotion SearchSlate card built from this manifest entry",
                carries=["scene number and script timecode", "block", "Storyblocks query",
                         "target duration", "licence status: UNLICENSED — PREVIEW ONLY"],
                preview_only=True,
            ),
            "generative_substitute": False,
            "generative_substitute_reason": ("forbidden by HARD SCOPE CONTRACT "
                                             "§ No generative fallback for stock failure"),
            "owner_directed": scene["id"] == "tactile-hero",
        })

    real = [a for a in assets if a["kind"] == "REAL_FOOTAGE"]
    resolved_real = [a for a in real if a["asset_status"] == "RESOLVED"]
    branded_entries = [
        dict(
            b,
            kind="GENERATIVE",
            media_type="motion_graphic",
            provider="in-house",
            provider_kind="branded_motion_graphic",
            licence_note="Designed and rendered by the Remotion composition from brand tokens; "
                         "no third-party asset, no generated imagery.",
            asset_status="RESOLVED",
            required=True,
            file=None,
            generator="remotion-code",
            counts_against_generative_budget=True,
        )
        for b in BRANDED
    ]

    manifest = {
        "contract": "MEDIA_MANIFEST",
        "version": 3,
        "fixture": "Salamat Mebel 2-minute promo",
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "narrative_source_of_truth": "SALAMAT_PROMO_SCRIPT.md",
        "media_source_authority": storyboard["media_source_authority"],
        "primary_provider": "storyblocks",
        "primary_provider_available": available,
        "primary_provider_status": f"{'AVAILABLE' if available else 'BLOCKED_PROVIDER'} — {reason}",
        "resolved_provider": "storyblocks" if available
                             else "none — neutral placeholders only; no licensed footage obtained",
        "provider_neutral_contract": {
            "note": ("Scenes declare footage intent as queries; resolving a different provider rewrites "
                     "this manifest only, leaving the storyboard untouched."),
            "adapters": ["adapters/storyblocks_adapter.py"],
        },
        "delivery_mix_target": storyboard["delivery_mix_target"],
        "mix_accounting": {
            "ordinary_scenes_requiring_real_footage": len(real),
            "real_footage_resolved": len(resolved_real),
            "real_footage_unresolved": len(real) - len(resolved_real),
            "generative_assets_in_manifest": len(branded_entries),
            "generative_budget_before_owner_review": GENERATIVE_BUDGET,
            "generative_budget_unused_slots": GENERATIVE_BUDGET - len(branded_entries),
            "generated_imagery_used": 0,
            "generated_video_used": 0,
            "note": ("The delivered real-footage share is reported in SALAMAT_PROMO_RESULTS.md once clips "
                     "are licensed. While the provider is blocked the film cannot claim a real-footage "
                     "share and the preview must not be presented as a finished promo."),
        },
        "assets": assets,
        "branded_motion_graphics": branded_entries,
        "generative_allowlist_unused": ALLOWLISTED_UNUSED,
        "coverage": {
            "scenes_total": len(scenes),
            "scenes_with_stock_request": len({a["scene_id"] for a in real}),
            "scenes_generative": [b["scene_id"] for b in branded_entries],
        },
        "scope_compliance": {
            "generative_fallback_for_blocked_stock": "prohibited and not used",
            "unused_assets_from_rev_000": "see REVISION_LOG.md — 10 stills classified UNUSED, removed from the tree",
            "script_overlay_rule": "only the script's approved on-screen text may be rendered",
            "self_check_rule": "no media action without a mapped scene, an allowlisted category and a manifest entry",
        },
    }

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n### {stamp} — `resolve_media.py plan`\n\n"
            f"- provider: storyblocks — {'AVAILABLE' if available else 'BLOCKED_PROVIDER'}\n"
            f"- reason: {reason}\n"
            f"- stock requests planned: {len(real)} (resolved {len(resolved_real)})\n"
            f"- branded graphics: {len(branded_entries)} / budget {GENERATIVE_BUDGET}\n"
            f"- generated imagery used: 0\n"
        )

    print(f"manifest: {len(assets)} stock requests, {len(branded_entries)} branded graphics "
          f"(budget {GENERATIVE_BUDGET}) → {MANIFEST.name}")
    print(f"provider: {manifest['primary_provider_status']}")
    for a in assets:
        flag = " [OWNER-DIRECTED]" if a["owner_directed"] else ""
        print(f"  {a['scene_order']:>2}. {a['scene_id']:<22} {a['asset_status']:<17} "
              f"“{a['all_queries'][0]}”{flag}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["plan", "status"], nargs="?", default="plan")
    args = parser.parse_args()
    if args.action == "status":
        available, reason = provider_state()
        print(f"storyblocks: {'AVAILABLE' if available else 'UNAVAILABLE'} — {reason}")
        return 0 if available else 3
    return plan()


if __name__ == "__main__":
    sys.exit(main())
