#!/usr/bin/env python3
"""Sample an aria2 JSON-RPC endpoint while a torrent is downloading.

Records, over time: completed length, download speed, connection count, seeder
count and the peer set. Peer addresses are stored only as masked /16 networks so
third-party seeder IPs are not published in the evidence.

The sampler is also the component that stops aria2c: aria2c started with
``--enable-rpc`` keeps its RPC server alive after the transfer ends, so the
sampler issues ``aria2.shutdown`` as soon as the download reports *complete*,
*error*, or disappears from the active list (stopped by ``--bt-stop-timeout`` or
finished). Without that, a stage would only end when the wrapper ``timeout``
kills aria2c.

Usage: peer_sample.py <rpc_port> <out.json> [max_seconds]
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request

RPC = "http://127.0.0.1:{port}/jsonrpc"
IDLE_POLLS_BEFORE_STOP = 20  # consecutive polls with no active download


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
    return "shutdown-failed"


def main() -> int:
    port, out = int(sys.argv[1]), sys.argv[2]
    max_seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 900
    started = time.time()
    samples, seen_peers, max_seeders, max_connections, max_speed = [], {}, 0, 0, 0
    gid = None
    idle_polls = 0
    stop_reason, stop_detail = "max_seconds_elapsed", None

    # Wait for aria2c's RPC server before giving up; aria2c may still be starting.
    for _ in range(20):
        try:
            call(port, "aria2.getVersion")
            break
        except Exception:
            if time.time() - started >= max_seconds:
                stop_reason = "rpc_never_available"
                raise SystemExit(f"peer sample: RPC on port {port} never became available")
            time.sleep(1)

    while time.time() - started < max_seconds:
        try:
            if gid is None:
                active = call(port, "aria2.tellActive")
                if not active:
                    idle_polls += 1
                    if idle_polls >= IDLE_POLLS_BEFORE_STOP:
                        stop_reason = "no_active_download"
                        stop_detail = f"tellActive empty for {idle_polls} consecutive polls"
                        break
                    time.sleep(1)
                    continue
                gid = active[0]["gid"]
                idle_polls = 0
            status = call(port, "aria2.tellStatus", [gid])
            peers = call(port, "aria2.getPeers", [gid])
        except Exception as exc:  # download dropped out of the queue, or RPC gone
            idle_polls += 1
            if idle_polls >= IDLE_POLLS_BEFORE_STOP:
                stop_reason = "status_unavailable"
                stop_detail = f"{type(exc).__name__}: {exc}"
                break
            time.sleep(1)
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
        state = status.get("status")
        error_message = status.get("errorMessage")
        if state == "complete":
            stop_reason = "download_complete"
            stop_detail = "aria2 reported status=complete"
            stop_method = shutdown(port)
            stop_detail += f"; aria2c stopped via {stop_method}"
            break
        if state in ("error", "removed") or error_message:
            stop_reason = f"download_{state or 'error'}"
            stop_detail = error_message or f"aria2 status={state}"
            stop_method = shutdown(port)
            stop_detail += f"; aria2c stopped via {stop_method}"
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
        f"info_hash={result['info_hash']} stop_reason={stop_reason}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
