# EXP-12 — Recommended Next Prospective Case

Date: 2026-08-19  
Status: RECOMMENDATION  
Parent experiment: `docs/experiments/EXP-12_CLEARS_TRIAGE.md`

## Recommended project for P-004

**Furniture Configurator / Kitchen Configurator**

Use the next real, bounded task from the active Furniture Configurator / Kitchen Configurator work as the preferred candidate for EXP-12 prospective case `P-004`.

## Why this project

P-001 and P-002 were self-hosting MPE/tooling cases. P-003 was the first external product case and used MebelDocs AI. P-004 should deliberately move to a different product class so the prospective sample is not dominated by MPE/MebelDocs work.

Furniture Configurator is preferred because a real task can exercise a different combination of signals:

- UI / interaction change;
- business-rule or calculation logic;
- customer-facing behavior;
- regression risk;
- deterministic acceptance checks where available.

This gives EXP-12 a more representative prospective dataset than repeating another MPE or MebelDocs task immediately.

## Selection rule

Do not invent a hypothetical task only to fill the dataset. Select an actual task that would be implemented anyway, then pre-register it before execution according to the EXP-12 protocol.

If no suitable real Furniture Configurator task is available at registration time, use the next real task from the Stage 2 project mix, preferring a project not already represented in the prospective sample.

## Expected follow-up diversity

After P-004, distribute remaining prospective cases across other real project classes where practical, including MebelLegal, production/operational tooling, customer-facing sales workflow, and at least one genuine approval-required or DEEP-CHANGE case. The goal is diversity of risk classes and project contexts, not equal representation by repository.
