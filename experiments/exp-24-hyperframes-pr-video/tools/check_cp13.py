#!/usr/bin/env python3
"""EXP-24 CP-13 deterministic contract checks (stdlib only, experiment-local).

Checks: 20/20 action coverage, ordered beat partition, <=6 beats, stable IDs,
marks/cues inside beat bounds, one manifest entry per beat, asset existence and
sha256, no timing in the scene contract. Exit 1 on any failure.
"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p): return json.load(open(os.path.join(ROOT, p), encoding="utf-8"))

contract = load("cp13/SCENE_CONTRACT.json")
story = load("cp13/EDITORIAL_STORYBOARD.json")
manifest = load("cp13/MEDIA_MANIFEST.json")
fails = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)

actions = [a["action_id"] for a in contract["source_actions"]]
check(len(actions) == 20 and len(set(actions)) == 20, "20 unique source actions in contract")
cov = contract["coverage_ledger"]["map"]
check(set(cov) == set(actions), "coverage ledger keys == A01..A20 (no omitted/added)")
beat_ids_contract = [b["beat_id"] for b in contract["beats"]]
flat = [a for b in contract["beats"] for a in b["action_ids"]]
check(flat == actions, "beats partition actions in source order (no split/reorder)")
check(all(cov[a] == b["beat_id"] for b in contract["beats"] for a in b["action_ids"]), "ledger agrees with beat membership")
check(len(contract["beats"]) <= 6, "<= 6 visual beats")

sb_beats = story["beats"]
check([b["beat_id"] for b in sb_beats] == beat_ids_contract, "storyboard beat IDs/order == contract")
check(all(sorted(b["source_grounding"]) == sorted(next(c for c in contract["beats"] if c["beat_id"] == b["beat_id"])["action_ids"]) for b in sb_beats), "storyboard grounding == contract membership")
for b in sb_beats:
    d = b["duration_s"]
    check(all(0 <= m["at_s"] < d for m in b["marks"]), f"{b['beat_id']} marks inside [0,duration)")
    check(all(0 <= c["at_s"] <= d for c in b["cues"]), f"{b['beat_id']} cues inside beat")
    kinds = [c["kind"] for c in b["cues"]]
    if b["caption"] is not None:
        check(kinds == ["caption_in", "caption_out"], f"{b['beat_id']} caption has in/out cues")
    else:
        check(kinds == [], f"{b['beat_id']} no caption -> no caption cues")
    check(set(a for m in b["marks"] for a in m["action_ids"]) == set(b["source_grounding"]), f"{b['beat_id']} marks cover its grounding actions")

check("timing" not in json.dumps(contract).lower() or "not part of" in json.dumps(contract), "timing kept out of scene contract")

entries = manifest["entries"]
check([e["beat_id"] for e in entries] == beat_ids_contract, "exactly one manifest entry per beat, in order")
check(all(e["asset_slot"] == next(b["asset_slot"] for b in sb_beats if b["beat_id"] == e["beat_id"]) for e in entries), "manifest slot == storyboard slot")
for e in entries:
    p = os.path.join(ROOT, "remotion/public", e["asset_path"])
    ok = os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == e["asset_sha256"]
    check(ok, f"{e['beat_id']} asset exists and sha256 matches manifest")

total = sum(b["duration_s"] for b in sb_beats)
print(f"INFO total_duration_s={total:.2f} beats={len(sb_beats)} assets={len(entries)}")
print("RESULT", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
