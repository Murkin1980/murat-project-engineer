#!/usr/bin/env python3
"""Torrent metainfo (bencode) inspection and identity check for EXP-18.

Extracts, from the .torrent captured by each retrieval:
  * infohash (SHA-1 over the bencoded info dictionary)
  * file list, total length, piece length/count, piece-table hash
  * announce list, url-list (BEP-19 web seeds), creator/creation date
and reports whether the "normal" and "swarm-only" retrievals used the same
torrent (same piece table + same file list + same infohash).

Minimal bencode reader, no external dependency.
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


def dec(value):
    """Make bencode output JSON-serialisable (decode bytes to str)."""
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    if isinstance(value, list):
        return [dec(item) for item in value]
    if isinstance(value, dict):
        return {dec(key): dec(val) for key, val in value.items()}
    return value


def find_torrents(directory: str) -> list[str]:
    found = []
    for dirpath, _dirnames, filenames in os.walk(directory):
        for name in filenames:
            if name.endswith(".torrent"):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def describe(path: str) -> dict:
    with open(path, "rb") as fh:
        raw = fh.read()
    meta, _ = bdecode(raw)
    info = meta[b"info"]
    key_pos = raw.index(b"4:info")
    info_start = key_pos + len(b"4:info")
    _value, info_end = bdecode(raw, info_start)

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

    url_list = dec(info.get(b"url-list") or meta.get(b"url-list"))
    return {
        "torrent_file": os.path.basename(path),
        "metainfo_sha256": hashlib.sha256(raw).hexdigest(),
        "metainfo_bytes": len(raw),
        "info_hash_sha1": hashlib.sha1(raw[info_start:info_end]).hexdigest(),
        "name": info[b"name"].decode("utf-8", "replace"),
        "piece_length": info[b"piece length"],
        "piece_count": len(info[b"pieces"]) // 20,
        "piece_table_sha1": hashlib.sha1(info[b"pieces"]).hexdigest(),
        "total_length": sum(entry["length"] for entry in files),
        "file_count": len(files),
        "files": files,
        "announce_list": dec(meta.get(b"announce-list")) or ([dec(meta[b"announce"])] if b"announce" in meta else None),
        "url_list_web_seeds": url_list,
        "has_web_seed_in_metainfo": bool(url_list),
        "creator": dec(meta.get(b"created by")),
        "creation_date_utc": (
            datetime.fromtimestamp(meta[b"creation date"], tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if b"creation date" in meta
            else None
        ),
        "comment": dec(meta.get(b"comment")),
        "is_private": bool(info.get(b"private", 0)),
    }


def main() -> int:
    if len(sys.argv) != 4:
        sys.exit("usage: torrent_identity.py <dir_normal> <dir_swarm_only> <out.json>")
    normal = describe(p) if (p := (find_torrents(sys.argv[1])[:1] or [None])[0]) else None
    swarm = describe(p) if (p := (find_torrents(sys.argv[2])[:1] or [None])[0]) else None
    same = bool(
        normal and swarm and normal["piece_table_sha1"] == swarm["piece_table_sha1"] and normal["files"] == swarm["files"]
    )
    result = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "normal_retrieval_metainfo": normal,
        "swarm_only_retrieval_metainfo": swarm,
        "same_piece_table_and_file_list": same,
        "same_info_hash": bool(normal and swarm and normal["info_hash_sha1"] == swarm["info_hash_sha1"]),
    }
    with open(sys.argv[3], "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(
        "torrent identity: same_piece_table_and_file_list="
        f"{same} info_hash={(normal or {}).get('info_hash_sha1', 'n/a')} "
        f"pieces={(normal or {}).get('piece_count', 'n/a')} files={(normal or {}).get('file_count', 'n/a')} "
        f"bytes={(normal or {}).get('total_length', 'n/a')} "
        f"metainfo_web_seed={(normal or {}).get('has_web_seed_in_metainfo', 'n/a')} "
        f"creator={(normal or {}).get('creator', 'n/a')!r}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
