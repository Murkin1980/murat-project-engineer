# Model Artifact Resilience Practice

Status: ACTIVE / REUSE_COMPONENT  
Origin: EXP-18 — Pirate Face model resilience  
Adopted: 2026-10-16

## Rule

When a permissively licensed model artifact is pinned and an independent fallback distribution path is genuinely useful:

1. Record the exact model revision/commit.
2. Record license and gating/private status.
3. Record the fallback reference when available.
4. Preserve a canonical per-file SHA-256 manifest from the primary artifact.
5. After fallback retrieval, compare expected payload paths and SHA-256 values exactly.
6. Treat integrity as verified only after deterministic hash comparison.
7. State separately when repository-only metadata is omitted; do not call a partial repository snapshot exact.
8. Treat third-party availability as operationally uncertain.
9. Keep fallback retrieval optional. Do not create production routing, a permanent downloader, model registry, or seeding infrastructure without a separate MPE decision.

## Evidence

Preserve the canonical manifest, fallback reference, retrieval logs, per-file comparison result, deviations, and failed harness attempts that materially affect reproducibility.

## Boundary

This practice is provenance and recovery guidance only. It does not authorize a new runtime, routing layer, service, registry, background downloader, credentials, or infrastructure.
