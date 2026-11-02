#!/usr/bin/env python3
"""Fail closed for concurrent canonical MPE experiment registrations."""
import base64
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

REGISTRY_PATH = "experiments/EXPERIMENT_REGISTRY.json"
ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
NUMERIC_ID = re.compile(r"^EXP-(\d+)$")
REQUIRED_FIELDS = {"experiment_id", "name", "owning_project", "status", "why", "date_added", "next_action", "result_summary", "repo", "experiment_path", "evidence_links", "pr_or_issue_links", "updated_at"}
ALLOWED_STATUSES = {"IDEA", "PLANNED", "READY_TO_TEST", "RUNNING", "PASS", "PARTIAL", "FAIL", "HOLD", "RETIRED", "ADOPTED"}


def fail(message):
    print(f"BLOCKED: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalize(value):
    return " ".join(str(value).split()).casefold()


def api(path):
    token = os.environ.get("GH_TOKEN")
    if not token:
        fail("GH_TOKEN missing; cannot prove absence of in-flight claims")
    req = urllib.request.Request(API + path, headers={
        "Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "mpe-experiment-registration-guard",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return json.load(res)
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as exc:
        fail(f"GitHub evidence unavailable: {exc}")


def records(payload, label):
    if not isinstance(payload, dict) or not isinstance(payload.get("experiments"), list):
        fail(f"{label}: invalid registry structure")
    out = payload["experiments"]
    ids, names = [], []
    for record in out:
        if not isinstance(record, dict) or set(record) != REQUIRED_FIELDS:
            fail(f"{label}: registry record violates canonical contract")
        identifier = record.get("experiment_id")
        if not isinstance(identifier, str) or not identifier:
            fail(f"{label}: missing experiment ID")
        if record.get("status") not in ALLOWED_STATUSES or not normalize(record.get("name")):
            fail(f"{label}: invalid status or missing experiment title")
        ids.append(identifier)
        names.append(normalize(record["name"]))
    if len(ids) != len(set(ids)) or len(names) != len(set(names)):
        fail(f"{label}: duplicate ID or title")
    if "EXP-34" in ids:
        fail(f"{label}: reserved EXP-34 cannot be registered")
    return out


def get_registry(repo, ref):
    uri = urllib.parse.quote(REGISTRY_PATH, safe="/")
    data = api(f"/repos/{repo}/contents/{uri}?ref={urllib.parse.quote(ref, safe='')}")
    if data.get("encoding") != "base64":
        fail("cannot read current registry from GitHub")
    try:
        return json.loads(base64.b64decode(data["content"]))
    except (ValueError, KeyError) as exc:
        fail(f"invalid GitHub registry payload: {exc}")


def added_identity(proposal, base):
    base_ids = {x["experiment_id"] for x in base}
    return {x["experiment_id"]: x for x in proposal if x["experiment_id"] not in base_ids}


def next_free_numeric_id(records_):
    used = {int(match.group(1)) for item in records_ if (match := NUMERIC_ID.fullmatch(item["experiment_id"]))}
    # Historic aliases leave intentional gaps below the already allocated FIFO
    # range. New registrations continue after the highest numeric allocation.
    number = max(used, default=0) + 1
    while number in used or number == 34:
        number += 1
    return f"EXP-{number:02d}"


def validate_new_identities(added, canonical):
    canonical_names = {normalize(item["name"]) for item in canonical}
    canonical_whys = {normalize(item["why"]) for item in canonical}
    for identifier, item in added.items():
        if identifier == "EXP-34":
            fail("reserved EXP-34 cannot be registered")
        if not NUMERIC_ID.fullmatch(identifier):
            fail(f"new registration {identifier} is not a numeric canonical EXP ID")
        if normalize(item["name"]) in canonical_names:
            fail(f"new registration {identifier} duplicates a canonical title")
        if normalize(item["why"]) in canonical_whys:
            fail(f"new registration {identifier} duplicates a canonical hypothesis")


def assert_fifo(current_added, canonical, older_claims):
    if older_claims:
        oldest = min(older_claims, key=lambda item: (item["created_at"], item["number"]))
        fail(f"earlier registration claim PR #{oldest['number']} must reconcile first; FIFO blocks this PR")
    expected = next_free_numeric_id(canonical)
    actual = sorted(current_added, key=lambda item: int(NUMERIC_ID.fullmatch(item).group(1)))
    if actual != [expected]:
        fail(f"FIFO requires next free ID {expected}; proposed {actual}")


def open_prs(repo):
    result = []
    for page in range(1, 11):
        batch = api(f"/repos/{repo}/pulls?state=open&per_page=100&page={page}")
        result.extend(batch)
        if len(batch) < 100:
            return result
    fail("open PR list truncated; cannot prove uniqueness")


def pr_touches_registry(repo, number):
    files = []
    for page in range(1, 11):
        batch = api(f"/repos/{repo}/pulls/{number}/files?per_page=100&page={page}")
        files.extend(batch)
        if len(batch) < 100:
            return any(item["filename"] == REGISTRY_PATH for item in files)
    fail(f"PR #{number} files truncated")


def main():
    proposed = records(json.loads((ROOT / REGISTRY_PATH).read_text(encoding="utf-8")), "checkout")
    repo, event = os.environ.get("GH_REPOSITORY", ""), os.environ.get("GH_EVENT_NAME", "")
    if "/" not in repo:
        fail("repository context missing")
    canonical = records(get_registry(repo, "main"), "current main")
    added = added_identity(proposed, canonical)
    if not added:
        print("PASS: no new registration in this PR")
        return
    validate_new_identities(added, canonical)
    if event != "pull_request":
        fail("registration requires pull_request provenance; merge-group-only validation is insufficient")
    current_pr, base_sha = os.environ.get("GH_PR_NUMBER", ""), os.environ.get("GH_BASE_SHA", "")
    main_sha = api(f"/repos/{repo}/git/ref/heads/main").get("object", {}).get("sha")
    if not current_pr.isdigit() or not base_sha or not main_sha:
        fail("PR identity or current main evidence unavailable")
    if base_sha != main_sha:
        fail("PR is behind current main; update and rerun before registration can merge")
    prs = open_prs(repo)
    own = next((item for item in prs if item["number"] == int(current_pr)), None)
    if own is None:
        fail("own PR not in current GitHub PR list")
    older_claims = []
    for candidate in prs:
        if candidate["number"] == int(current_pr) or candidate["created_at"] > own["created_at"] or not pr_touches_registry(repo, candidate["number"]):
            continue
        claims = added_identity(records(get_registry(repo, candidate["head"]["sha"]), f"PR #{candidate['number']}"), canonical)
        if claims:
            older_claims.append(candidate)
            overlap = set(added) & set(claims)
            names = {normalize(x["name"]) for x in added.values()} & {normalize(x["name"]) for x in claims.values()}
            if overlap or names:
                fail(f"earlier PR #{candidate['number']} has competing IDs {sorted(overlap)} or titles {sorted(names)}")
    assert_fifo(added, canonical, older_claims)
    print(f"PASS: {len(added)} new ID; current main and FIFO order verified")


if __name__ == "__main__":
    main()
