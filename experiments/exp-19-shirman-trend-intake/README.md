# EXP-19 — Shir-man Trend Intake and Agent-Readable Surface

## Decision
**EXTEND_EXISTING**

This experiment extends Murat Project Engineer. It does not create a new repository, service, feed platform, crawler, or parallel governance system.

## Priority
**NEXT**

This is the first candidate among the newly registered experiments to execute.

## Goal
Test whether patterns observed on shir-man.com can improve two existing workflows:

1. discovery and intake of useful technology signals into MPE experiments;
2. agent-readable publishing and reusable workflow handoff, without duplicating MPE playbooks or Murat House content systems.

## Hypotheses

### H1 — Trend intake
A small, curated multi-source trend view can surface higher-value experiment candidates faster than ad-hoc manual discovery.

### H2 — Agent-readable public surface
Simple public machine-readable surfaces such as API catalogs, `llms.txt`, skills indexes, or equivalent structured pages can improve how agents understand an existing project without creating another source of truth.

### H3 — Reusable workflow presets
A portable preset or prompt representation may improve Arena/Codex handoff for existing MPE playbooks, but only if it reuses current instructions rather than creating a second instruction system.

## Minimal experiment — CP-01

### Dataset
Use a fixed small batch of recent candidate signals from shir-man.com. Do not build a scraper first.

Target: 10–15 candidate items maximum.

### Baseline
Use the current workflow:
- user/manual discovery;
- ad-hoc link review;
- MPE New Idea Filter;
- manual experiment registration when useful.

### Candidate workflow
For the same bounded period:
- review the fixed shir-man.com signal batch;
- classify each signal;
- run promising candidates through the existing New Idea Filter;
- record which candidates would become EXPERIMENT / HOLD / REJECT / EXTEND_EXISTING / REUSE_COMPONENT.

### Measure
Record:
- time to produce the first 5 viable candidates;
- number of duplicate or irrelevant signals;
- number of candidates that map to an existing project;
- number of genuinely actionable experiments;
- whether any candidate would have been missed by the baseline;
- operator effort and ambiguity.

## PASS
PASS if the bounded workflow demonstrates at least one meaningful improvement without new infrastructure, for example:
- materially faster discovery of useful candidates;
- fewer low-value links reaching full analysis;
- clearer mapping to existing projects/components;
- one or more valuable candidates not found through the baseline;
- reusable agent-readable or preset patterns that reduce handoff friction without duplicating authority.

## FAIL
FAIL if:
- the signal quality is mostly noise or duplicates;
- manual review effort is not reduced;
- trend intake encourages unnecessary experiments;
- machine-readable surfaces add no measurable agent benefit;
- presets duplicate MPE playbooks or create competing instructions;
- useful operation requires a new crawler/service before value is proven.

## Guardrails
- No new repository.
- No crawler, scheduled aggregator, or database in CP-01.
- No production integration.
- No automated experiment creation.
- Every candidate still passes the Murat Project Engineer New Idea Filter.
- Existing project docs/playbooks remain canonical.
- Murat House remains the public publishing project; this experiment may only recommend extensions to it after evidence.
- Any automation or recurring ingestion requires a new decision after PASS.

## Execution order
1. Run trend-intake comparison first.
2. Only if trend intake shows useful signal, test a tiny agent-readable surface pattern.
3. Only if that shows value, compare one existing MPE playbook against a portable preset representation.

Do not execute all three tracks in parallel.

## Current status
**READY_TO_TEST — PRIORITY: NEXT**

Registered on 2026-09-29. No execution evidence exists yet.
