#!/usr/bin/env python3
"""Bencode-based identity check between the two retrieved torrent metainfo files.

If the metainfo (info dictionary: file list, piece length, piece hashes) is
identical between the Pirate Face "normal" retrieval and the swarm-only
retrieval, then both runs demonstrably describe the same pinned artifact.
Minimal bencode reader, no external dependency. Also computes the BitTorrent
info-hash (SHA-1 over the bencoded info dictionary) for cross-checks.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone


def bdecode(data: bytes, pos: int = 0):
    """Decode bencode; returns (value, end_position_of_value)."""

    def parse(pos: int):
        char = data[pos : pos + 1]
        if char == b"i":
            end = data.index(b"e", pos)
            return int(data[pos + 1 : end]), end + 1
        if char == b"l":
            pos += 1
            out = []
            while data[pos : pos + 1] != b"e":
                item, pos = parse(pos)
                out.append(item)
            return out, pos + 1
        if char == b"d":
            pos += 1
            out = {}
            while data[pos : pos + 1] != b"e":
                key, pos = parse(pos)
                value, pos = parse(pos)
                out[key] = value
            return out, pos + 1
        if char.isdigit():
            colon = data.index(b":", pos)
            length = int(data[pos:colon])
            start = colon + 1
            return data[start : start + length], start + length
        raise ValueError(f"invalid bencode at {pos}: {data[pos:pos+20]!r}")

    return parse(pos)


def find_torrent(directory: str) -> str | None:
    for dirpath, _dirnames, filenames in os.walk(directory):
        for name in filenames:
            if name.endswith(".torrent"):
                return os.path.join(dirpath, name)
    return None


def describe(path: str | None) -> dict | None:
    if not path:
        return None
    with open(path, "rb") as fh:
        raw = fh.read()
    meta, _ = bdecode(raw)
    info = meta[b"info"]
    # locate the exact bencoded info dictionary for a correct info-hash
    key_pos = raw.index(b"4:info")
    info_start = key_pos + len(b"4:info")
    _value, info_end = bdecode(raw, info_start)
    info_hash = hashlib.sha1(raw[info_start:info_end]).hexdigest()

    entries = info.get(b"files")
    files = []
    if entries:
        for entry in entries:
            files.append(
                {
                    "path": "/".join(part.decode("utf-8", "replace") for part in entry[b"path"]),
                    "length": entry[b"length"],
                }
            )
    else:
        files.append({"path": info[b"name"].decode("utf-8", "replace"), "length": info[b"length"]})
    files.sort(key=lambda entry: entry["path"])
    return {
        "torrent_file": os.path.basename(path),
        "metainfo_sha256": hashlib.sha256(raw).hexdigest(),
        "info_hash_sha1": info_hash,
        "name": info[b"name"].decode("utf-8", "replace"),
        "piece_length": info[b"piece length"],
        "piece_count": len(info[b"pieces"]) // 20,
        "piece_table_sha1": hashlib.sha1(info[b"pieces"]).hexdigest(),
        "total_length": sum(entry["length"] for entry in files),
        "files": files,
        "announce_list": meta.get(b"announce-list") if b"announce-list" in meta else None,
        "has_url_list": b"url-list" in info or b"url-list" in meta,
    }


def main() -> int:
    if len(sys.argv) != 4:
        sys.exit("usage: torrent_identity.py <dir_normal> <dir_swarm_only> <out.json>")
    a = describe(find_torrent(sys.argv[1]))
    b = describe(find_torrent(sys.argv[2]))
    same = bool(a and b and a["piece_table_sha1"] == b["piece_table_sha1"] and a["files"] == b["files"])
    result = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "normal_retrieval_metainfo": a,
        "swarm_only_retrieval_metainfo": b,
        "same_piece_table_and_file_list": same,
        "same_info_hash": bool(a and b and a["info_hash_sha1"] == b["info_hash_sha1"]),
    }
    with open(sys.argv[3], "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(
        "torrent identity: same_piece_table_and_file_list="
        f"{same} info_hash={(a or {}).get('info_hash_sha1', 'n/a')} "
        f"pieces={(a or {}).get('piece_count', 'n/a')} files={len(a['files']) if a else 'n/a'} "
        f"total_bytes={(a or {}).get('total_length', 'n/a')} "
        f"has_url_list={(a or {}).get('has_url_list', 'n/a')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
