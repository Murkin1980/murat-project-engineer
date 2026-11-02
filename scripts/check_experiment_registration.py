#!/usr/bin/env python3
"""Fail closed for simultaneous/competing canonical experiment registrations.

This check is advisory unless GitHub rulesets require the named status check
and disallow bypassing it. It does not issue numbers or write the registry.
"""
import base64
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

REGISTRY_PATH = "experiments/EXPERIMENT_REGISTRY.json"
ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"


def fail(message):
    print(f"BLOCKED: {message}", file=sys.stderr)
    sys.exit(1)


def api(path):
    token = os.environ.get("GH_TOKEN")
    if not token:
        fail("GH_TOKEN missing; cannot prove absence of in-flight claims")
    req = urllib.request.Request(
        API + path,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "mpe-experiment-registration-guard",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return json.load(res)
    except (urllib.error.URLError, ValueError) as exc:
        fail(f"GitHub evidence unavailable: {exc}")


def records(payload, label):
    if not isinstance(payload, dict) or not isinstance(payload.get("experiments"), list):
        fail(f"{label}: invalid registry structure")
    out = payload["experiments"]
    ids = [x.get("experiment_id") for x in out]
    names = [str(x.get("name", "")).strip().casefold() for x in out]
    if any(not isinstance(v, str) or not v for v in ids):
        fail(f"{label}: missing experiment ID")
    if len(ids) != len(set(ids)) or len(names) != len(set(names)):
        fail(f"{label}: duplicate ID or title")
    if "EXP-34" in ids:
        fail(f"{label}: reserved EXP-34 cannot be registered")
    return out


def get_registry(repo, ref):
    uri = urllib.parse.quote(REGISTRY_PATH, safe="/")
    ref = urllib.parse.quote(ref, safe="")
    data = api(f"/repos/{repo}/contents/{uri}?ref={ref}")
    if data.get("encoding") != "base64":
        fail("cannot read current registry from GitHub")
    try:
        return json.loads(base64.b64decode(data["content"]))
    except (ValueError, KeyError) as exc:
        fail(f"invalid GitHub registry payload: {exc}")


def added_identity(proposal, base):
    base_ids = {x["experiment_id"] for x in base}
    return {x["experiment_id"]: x for x in proposal if x["experiment_id"] not in base_ids}


def main():
    payload = json.loads((ROOT / REGISTRY_PATH).read_text(encoding="utf-8"))
    proposed = records(payload, "checkout")
    repo = os.environ.get("GH_REPOSITORY", "")
    event = os.environ.get("GH_EVENT_NAME", "")
    if not repo or "/" not in repo:
        fail("repository context missing")
    canonical = records(get_registry(repo, "main"), "current main")

    if event not in ("pull_request", "merge_group"):
        print("PASS: current registry integrity checked")
        return

    added = added_identity(proposed, canonical)
    # Existing canonical records are immutable in the absence of a separately approved migration.
    previous = {x["experiment_id"]: x for x in canonical}
    for entry in proposed:
        old = previous.get(entry["experiment_id"])
        if old is not None and old != entry:
            fail(f"existing canonical record changed: {entry['experiment_id']}")
    if not added:
        print("PASS: no new registration in this PR")
        return

    current_pr = os.environ.get("GH_PR_NUMBER", "")
    if event == "merge_group":
        # GitHub merge queue replays this check against a proposed merged tree.
        # Its required status check protects concurrent integrations in the queue.
        print("PASS: merge-group registry integrity; FIFO must be asserted at PR intake")
        return
    if not current_pr.isdigit():
        fail("PR identity unknown; cannot verify FIFO")

    prs = []
    for page in range(1, 11):
        batch = api(f"/repos/{repo}/pulls?state=open&per_page=100&page={page}")
        prs.extend(batch)
        if len(batch) < 100:
            break
    else:
        fail("open PR list truncated; cannot prove uniqueness")

    own = next((p for p in prs if p["number"] == int(current_pr)), None)
    if own is None:
        fail("own PR not in current GitHub PR list")

    for candidate in prs:
        if candidate["number"] == int(current_pr):
            continue
        # Compare the source PR's original creation timestamp, not commit time.
        if candidate["created_at"] > own["created_at"]:
            continue
        # Inspect other older PR heads only when they touch the canonical registry.
        files = []
        for page in range(1, 11):
            batch = api(f"/repos/{repo}/pulls/{candidate['number']}/files?per_page=100&page={page}")
            files.extend(batch)
            if len(batch) < 100:
                break
        else:
            fail(f"PR #{candidate['number']} files truncated")
        if not any(f["filename"] == REGISTRY_PATH for f in files):
            continue
        try:
            other = records(get_registry(repo, candidate["head"]["sha"]), f"PR #{candidate['number']}")
        except SystemExit:
            # Stale PR that cannot be read needs human reconciliation, not a silent PASS.
            raise
        older_claims = added_identity(other, canonical)
        overlap = set(added) & set(older_claims)
        same_names = {
            x["name"].strip().casefold() for x in added.values()
        } & {
            x["name"].strip().casefold() for x in older_claims.values()
        }
        if overlap or same_names:
            fail(
                f"earlier PR #{candidate['number']} has competing ID(s) "
                f"{sorted(overlap)} or name(s) {sorted(same_names)}; FIFO reconcile"
            )

    print(f"PASS: {len(added)} new IDs; no older competing registered claims")


if __name__ == "__main__":
    main()
