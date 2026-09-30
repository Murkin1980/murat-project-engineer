#!/usr/bin/env python3
"""Sample an aria2 JSON-RPC endpoint while a torrent is downloading.

Records, over time: completed length, download speed, connection count, seeder
count and the peer set. Peer addresses are stored only as masked /16 networks so
third-party seeder IPs are not published in the evidence.

The sampler is also the component that stops aria2c. aria2c started with
``--enable-rpc`` keeps its RPC server alive after the transfer ends, so a stage
would otherwise wait for its wrapper timeout even though the payload is already
on disk. It issues ``aria2.shutdown`` only when no download is *active* any more
(verified over consecutive polls), because that is the one state that means the
transfer is over - succeeded, stopped by ``--bt-stop-timeout``, or failed.

Careful: a magnet download starts as a metadata-only job and is replaced by a
new job (new GID) once the metadata arrives; the old GID then answers
``400 Bad Request``. The sampler therefore never pins a GID - it re-reads the
active list every poll and only samples the downloads that are still active.

Usage: peer_sample.py <rpc_port> <out.json> [max_seconds]
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

RPC = "http://127.0.0.1:{port}/jsonrpc"
IDLE_POLLS_BEFORE_STOP = 20  # consecutive polls with nothing active before shutdown


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


def shutdown(port: int) -> str:
    for method in ("aria2.shutdown", "aria2.forceShutdown"):
        try:
            call(port, method)
            return method
        except Exception:
            continue
    return "shutdown-request-failed"


def main() -> int:
    port, out = int(sys.argv[1]), sys.argv[2]
    max_seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 900
    started = time.time()
    samples, seen_peers, max_seeders, max_connections, max_speed = [], {}, 0, 0, 0
    idle_polls = 0
    rpc_failures = 0
    seen_active = False
    stop_reason, stop_detail = "max_seconds_elapsed", None

    # Wait for aria2c's RPC server before giving up; aria2c may still be starting.
    rpc_up = False
    for _ in range(20):
        try:
            call(port, "aria2.getVersion")
            rpc_up = True
            break
        except Exception:
            if time.time() - started >= max_seconds:
                break
            time.sleep(1)
    if not rpc_up:
        stop_reason = "rpc_never_available"
        stop_detail = f"no JSON-RPC answer on port {port}"

    while rpc_up and time.time() - started < max_seconds:
        try:
            active = call(port, "aria2.tellActive")
            rpc_failures = 0
        except Exception as exc:  # aria2c gone, or RPC temporarily busy
            rpc_failures += 1
            if rpc_failures >= IDLE_POLLS_BEFORE_STOP:
                stop_reason = "rpc_unavailable"
                stop_detail = f"{type(exc).__name__}: {exc} (client gone; nothing to stop)"
                break
            time.sleep(1)
            continue

        # Only downloads still in state "active" count; a finished or
        # timeout-stopped job is removed from there (and its GID becomes invalid).
        running = []
        for entry in active:
            try:
                status = call(port, "aria2.tellStatus", [entry["gid"]])
            except Exception:
                continue
            if status.get("status") == "active":
                running.append(status)

        if not running:
            idle_polls += 1
            if seen_active and idle_polls >= IDLE_POLLS_BEFORE_STOP:
                stop_reason = "no_active_download"
                stop_detail = (
                    f"nothing active for {idle_polls} consecutive polls after the transfer started; "
                    f"aria2c stopped via {shutdown(port)}"
                )
                break
            time.sleep(1)
            continue

        seen_active = True
        idle_polls = 0
        for status in running:
            gid = status["gid"]
            try:
                peers = call(port, "aria2.getPeers", [gid])
            except Exception:
                peers = []
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
                    "gid": gid,
                    "completed": int(status.get("completedLength", 0) or 0),
                    "total": int(status.get("totalLength", 0) or 0),
                    "speed_bps": speed,
                    "connections": conns,
                    "num_seeders": seeders,
                    "peers_listed": len(peers),
                    "info_hash": status.get("infoHash"),
                    "bittorrent_mode": (status.get("bittorrent") or {}).get("mode"),
                    "error": status.get("errorMessage") or status.get("status"),
                }
            )
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
        "saw_active_download": seen_active,
        "last_completed_bytes": (samples[-1]["completed"] if samples else None),
        "last_total_bytes": (samples[-1]["total"] if samples else None),
        "stop_reason": stop_reason,
        "stop_detail": stop_detail,
        "elapsed_seconds": round(time.time() - started, 1),
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(
        f"peer sample: networks={result['distinct_peer_network_count']} "
        f"max_seeders={max_seeders} max_connections={max_connections} "
        f"max_speed={max_speed/1048576:.1f}MiB/s samples={len(samples)} "
        f"completed={result['last_completed_bytes']}/{result['last_total_bytes']} "
        f"info_hash={result['info_hash']} stop_reason={stop_reason}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
