#!/usr/bin/env python3
"""BEP-15 UDP tracker announce for the pinned infohash (observation only).

Confirms from the test host what the public BitTorrent tracker reports for the
torrent: seeder count, leecher count and reachable peer addresses (masked).
No download happens here; this is pure swarm observation.

Usage: tracker_announce.py <infohash_hex> <out.json> [tracker_host] [port]
"""
from __future__ import annotations

import json
import os
import random
import socket
import struct
import sys
import time

PROTOCOL_ID = 0x41727101980
ACTION_ANNOUNCE = 1


def mask(ip: str) -> str:
    parts = ip.split(".")
    return f"{parts[0]}.{parts[1]}.x.x" if len(parts) == 4 else "ipv6-masked"


def announce(infohash_hex: str, host: str, port: int, timeout: float = 10.0) -> dict:
    ih = bytes.fromhex(infohash_hex)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    tx = random.randrange(0, 1 << 31)
    sock.sendto(struct.pack(">QII", PROTOCOL_ID, 0, tx), (host, port))
    data, _ = sock.recvfrom(4096)
    action, _rtx, conn_id = struct.unpack(">IIQ", data[:16])
    if action != 0:
        return {"ok": False, "error": f"connect action={action}"}
    tx2 = random.randrange(0, 1 << 31)
    req = struct.pack(
        ">QII20s20sQQQIIIiH",
        conn_id,
        ACTION_ANNOUNCE,
        tx2,
        ih,
        os.urandom(20),
        0,
        0,
        0,
        2,
        0,
        random.randrange(0, 1 << 31),
        -1,
        port,
    )
    sock.sendto(req, (host, port))
    data, _ = sock.recvfrom(4096)
    action, _rtx, interval, leechers, seeders = struct.unpack(">IIIII", data[:20])
    if action != ACTION_ANNOUNCE:
        return {"ok": False, "error": f"announce action={action}"}
    peers = []
    rest = data[20:]
    for i in range(0, len(rest) - 5, 6):
        peers.append(f"{rest[i]}.{rest[i+1]}.{rest[i+2]}.{rest[i+3]}:{struct.unpack('>H', rest[i+4:i+6])[0]}")
    return {
        "ok": True,
        "interval_seconds": interval,
        "seeders": seeders,
        "leechers": leechers,
        "peers_returned": len(peers),
        "peer_networks": sorted({mask(p.split(":")[0]) for p in peers}),
    }


def main() -> int:
    infohash, out = sys.argv[1], sys.argv[2]
    host = sys.argv[3] if len(sys.argv) > 3 else "tracker.pirateface.co"
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 6969
    result = {
        "tracker": f"udp://{host}:{port}/announce",
        "infohash": infohash,
        "observed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        addr = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_DGRAM)[0][4]
        result["resolved_ip"] = addr[0]
        t0 = time.time()
        result["announce"] = announce(infohash, addr[0], port)
        result["elapsed_seconds"] = round(time.time() - t0, 2)
    except Exception as exc:  # noqa: BLE001
        result["announce"] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"tracker announce: {json.dumps(result['announce'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
