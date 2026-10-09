# REA — Reverse Engineer Anything: experiment intake

Status: QUEUED / NOT RUN
Decision (Murat Project Engineer New Idea Filter): **EXPERIMENT**
Date: 2026-10-09
Upstream: https://github.com/morluto/rea
Target: existing MPE Arena experiments; first consumer: Privetmaket Recon CP-02
Experiment number: assign against the canonical register before execution (avoid collision).

## Problem / business value
Privetmaket Recon CP-02 is BLOCKED by unavailable DevTools HAR evidence. Assess whether REA can lawfully and safely collect **technical evidence** sufficient to understand a permitted web-app feature, reducing manual investigation time and enabling the existing furniture configurator research. This is an opportunity hypothesis, not a verified relief unit.

## New Idea Filter
- Active fit: Privetmaket Recon for the initial case; Murat Project Engineer / Arena owns the controlled experiment.
- Extension/reuse: compare existing browser/network capture and manual HAR procedures first; use REA only if it closes a specific evidence gap.
- Avoid duplication: no separate reverse-engineering platform, agent, hosted service, memory store, browser infrastructure, or project repository.
- Measurable outcome: capture reproducible, attributable observations of ONE permitted feature; compare analyst minutes, evidence quality, setup effort, and failure/retry rate against current approach.
- Smallest MVP: documentation/upstream audit + one bounded read-only capture on an authorized target, then evaluate.
- Priority: below current production incidents and P0 work; no automatic scheduling or deployment.
- Deep change: NOT APPROVED. Installation with elevated permissions, security-boundary changes, protected binaries, production integrations, or external data transfer requires separate review/approval.

## Execution boundary (Arena)
CP-00: read AGENTS.md, docs/governance/SCOPE-CHANGE-CONTROL.md, docs/NEW_IDEA_FILTER_POLICY.md, docs/GLOBAL_MPE_ENFORCEMENT.md, docs/OPINIONATED_WORKSPACE_POLICY.md and relevant Privetmaket Recon evidence. Verify upstream repository identity, current license, version, dependency chain, permissions and threat model; inspect current capture options.
CP-01: decide whether REA provides a measurable capability not already available through existing tools. Stop as DO_NOT_ADOPT if duplicated or unsafe.
CP-02: if approved/safe, capture a single minimal **read-only** feature trace on an authorized test target. Never bypass authentication, access controls, licensing, anti-bot protections, or inspect third-party private data. When target permission is unclear, use an owned/local fixture and record target as a blocker.
CP-03: write reproducible evidence, source/commit, commands, security limits, before/after effort, PASS/PARTIAL/FAIL, ADOPT/ADOPT_WITH_CHANGES/DO_NOT_ADOPT, and a short next-action handoff.

## Stop conditions
STOP before invasive reverse engineering, exploit development, copying proprietary implementation, unapproved network egress, downloading untrusted executable payloads without validation, adding persistent infrastructure, touching production repos, or exceeding this read-only experiment. No merge, deployment, external integration, or installation authority is implied.

## Acceptance
PASS: one reproducible, lawful evidence capture establishes extra value over existing capture methods with no new persistent infrastructure.
PARTIAL: audit feasible but environment/permission/capture blocked.
FAIL: not economically useful, unsafe or redundant.
VRU: 0 until a real workflow relief is implemented and independently verified.

## Next action
Arena: validate upstream and existing Privetmaket CP-02 evidence, assign canonical next experiment identifier, and propose the smallest safe audit. Do not start code or installs by default.
