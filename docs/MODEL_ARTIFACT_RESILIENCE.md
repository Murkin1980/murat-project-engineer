# Model Artifact Resilience Practice

Status: **ADOPTED**  
Origin: **EXP-18 — Pirate Face model resilience**  
Adopted: **2026-09-30**

## Rule

When a permissively licensed model is pinned for an MPE experiment or project, preserve enough provenance to reproduce and verify the artifact independently of its primary distribution service.

For each model pin, when a fallback distribution path is relevant:

1. Record the exact model revision/commit.
2. Record the license and gating/private status.
3. Record the fallback magnet/info hash, when available.
4. Store a canonical per-file SHA-256 manifest produced from the primary artifact.
5. After any fallback retrieval, compare the expected payload path set and SHA-256 values exactly.
6. Treat integrity as **verified only after deterministic hash comparison**.
7. Treat omitted repository metadata files separately; do not call a partial repository snapshot an exact snapshot.
8. Treat third-party swarm availability as an operational uncertainty, especially for low-demand models.
9. Keep fallback distribution as an optional last-resort recovery path. Do not turn it into production routing, a permanent downloader, a model registry, or seeding infrastructure without a separate MPE decision.

## Evidence standard

A successful fallback test should preserve:

- canonical manifest;
- fallback reference/magnet;
- retrieval logs;
- source-loss conditions, when tested;
- per-file comparison result;
- notable deviations;
- failed harness attempts when they reveal reproducibility or measurement defects.

A model payload can be considered byte-identical even when repository-only metadata differs, but the evidence must state the distinction explicitly.

## EXP-18-derived result

EXP-18 demonstrated this pattern for:

- sentence-transformers/all-MiniLM-L6-v2
- revision 1110a243fdf4706b3f48f1d95db1a4f5529b4d41
- Apache-2.0
- model.safetensors SHA-256: 53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db
- 29/29 payload files matched across the tested retrievals.
- .gitattributes was omitted by the torrent and therefore the full repository snapshot was not identical.
- Recovery remained dependent on third-party peers; low-demand models were not tested.

## Non-goals

This practice does **not** authorize:

- production Pirate Face integration;
- automatic model fallback routing;
- background torrent downloading;
- permanent seeding;
- credentials or external-service dependencies;
- replacing the existing model/source of truth.

## Application trigger

Apply this practice when a new model is pinned and an independent fallback distribution path is reasonably useful. Do not add fallback machinery merely because this document exists.
