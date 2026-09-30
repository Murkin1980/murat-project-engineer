#!/usr/bin/env python3
"""Sample an aria2 JSON-RPC endpoint while a torrent is downloading.

Records, over time: completed length, download speed, connection count, seeder
count and the peer set. Peer addresses are stored only as masked /16 networks so
third-party seeder IPs are not published in the evidence.

Usage: peer_sample.py <rpc_port> <out.json> [max_seconds]
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

RPC = "http://127.0.0.1:{port}/jsonrpc"


def call(port: int, method: str, params=None):
    payload = json.dumps(
        {"jsonrpc": "2.0", "id": "exp18", "method": method, "params": params or []}
    ).encode()
    req = urllib.request.Request(RPC.format(port=port), data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=3) as resp:
        body = json.loads(resp.read().decode())
    if "error" in body:
        raise RuntimeError(body["error"])
    return body["result"]


def mask(ip: str) -> str:
    parts = ip.split(".")
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.x.x"
    return "ipv6-masked"


def main() -> int:
    port, out = int(sys.argv[1]), sys.argv[2]
    max_seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 900
    started = time.time()
    samples, seen_peers, max_seeders, max_connections, max_speed = [], {}, 0, 0, 0
    gid = None
    while time.time() - started < max_seconds:
        try:
            if gid is None:
                active = call(port, "aria2.tellActive")
                if not active:
                    time.sleep(1)
                    continue
                gid = active[0]["gid"]
            status = call(port, "aria2.tellStatus", [gid])
            peers = call(port, "aria2.getPeers", [gid])
        except Exception:
            # aria2 has exited (download finished) or RPC not up yet
            time.sleep(1)
            try:
                active = call(port, "aria2.tellActive")
            except Exception:
                break
            continue
        seeders = int(status.get("numSeeders", 0) or 0)
        conns = int(status.get("connections", 0) or 0)
        speed = int(status.get("downloadSpeed", 0) or 0)
        max_seeders, max_connections, max_speed = (
            max(max_seeders, seeders), max(max_connections, conns), max(max_speed, speed)
        )
        for peer in peers:
            key = mask(peer.get("ip", "?"))
            entry = seen_peers.setdefault(key, {"seen": 0, "seeder": False})
            entry["seen"] += 1
            if peer.get("seeder"):
                entry["seeder"] = True
        samples.append(
            {
                "t": round(time.time() - started, 1),
                "completed": int(status.get("completedLength", 0) or 0),
                "speed_bps": speed,
                "connections": conns,
                "num_seeders": seeders,
                "peers_listed": len(peers),
                "info_hash": status.get("infoHash"),
                "error": status.get("errorMessage") or status.get("status"),
            }
        )
        if status.get("status") == "complete":
            break
        time.sleep(1)

    result = {
        "samples": samples,
        "sample_count": len(samples),
        "max_seeders": max_seeders,
        "max_connections": max_connections,
        "max_download_speed_bps": max_speed,
        "distinct_peer_networks": seen_peers,
        "distinct_peer_network_count": len(seen_peers),
        "peer_networks_that_were_seeders": sorted(k for k, v in seen_peers.items() if v["seeder"]),
        "info_hash": (samples[0]["info_hash"] if samples else None),
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(
        f"peer sample: networks={result['distinct_peer_network_count']} "
        f"max_seeders={max_seeders} max_connections={max_connections} "
        f"max_speed={max_speed/1048576:.1f}MiB/s samples={len(samples)} info_hash={result['info_hash']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
