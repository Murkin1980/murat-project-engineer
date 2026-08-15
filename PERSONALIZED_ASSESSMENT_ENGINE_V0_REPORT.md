# Personalized Assessment Engine v0 — pre-implementation decision

MURAT_PROJECT_ENGINEER_NEW_IDEA_FILTER

- Idea: reusable Personalized Assessment Engine based on the public Outcome product pattern.
- Primary decision: `EXPERIMENT`.
- New repository: `NO`.
- Deep change: `NOT AUTHORIZED`.

## Repository audit decision

- Implementation target: `C:\Projects\salamat-kitchen-configurator`.
- Repository decision: `EXTEND_EXISTING`.
- Why: the project already owns kitchen intake, deterministic millimetre geometry, module composition, future isolated pricing and result/lead flow. The experiment adds one local-only assessment path without persistence, external services, production pricing, CRM, analytics, or deployment.
- Price boundary: v0 uses an isolated, versioned synthetic experiment tariff and labels every range as preliminary/non-commercial. It does not claim approved Salamat production prices.
- AI boundary: a pure bounded outcome composer consumes deterministic facts and traceable rule candidates. It cannot change numbers. No external LLM is required for the reproducible v0 evaluation.

## Reuse audit

| Component | Source | Decision |
|---|---|---|
| React/Vite shell and mobile CSS | salamat-kitchen-configurator | EXTEND |
| Kitchen layout and millimetre conventions | configurator/geometry | REUSE_AS_IS |
| Module composition concepts | configurator/modules | ADAPT |
| Versioned deterministic scoring pattern | business-discovery/packages/scoring | ADAPT |
| Existing public Salamat lead form | salamat-mebel-kz | DO_NOT_REUSE (production flow excluded) |
| Production pricing | unavailable/unapproved | DO_NOT_REUSE |

This decision was recorded before implementation.

## Implemented v0

Target: `C:\Projects\salamat-kitchen-configurator`.

- Nine-field local intake and structured result page.
- Pure `calculateAssessment(input)` with rule version `kitchen-assessment-experiment-0.1.0`.
- Isolated synthetic preliminary KZT range; never presented as approved production pricing.
- Six classifications and traceable recommendation rule IDs.
- Bounded outcome composer that cannot calculate or mutate authoritative facts. No external LLM call was made, so hallucination safety is proven for the fallback composer only.
- Twelve synthetic scenarios defined before the assessment source was copied into the target project.
- No persistence, personal data, CRM, WhatsApp, analytics, public deployment, queue, agent graph, or new runtime.

## Scenario evaluation

| Group | Scenarios | Result |
|---|---:|---|
| GOOD_FIT | 2 | 2 PASS |
| PREMIUM_FIT | 2 | 2 PASS |
| BUDGET_GAP | 2 | 2 PASS |
| PARTIAL | 2 | 2 PASS |
| TIMELINE_RISK | 2 | 2 PASS |
| TRADEOFF_REQUIRED | 2 | 2 PASS |

Metrics:

- Classification pass rate: **100% (12/12)**.
- Hallucination rate: **0% for the deterministic/template v0**; an external LLM was not evaluated.
- Average recommendation relevance: **4.7/5** (manual synthetic review).
- Average customer usefulness: **4.5/5** (manual synthetic comparison with a thank-you page).
- Average manager usefulness: **4.8/5** (classification, drivers, gap and next action are visible).
- Different profiles: PASS.
- Missing-data certainty guard: PASS.
- Recommendation traceability: PASS.

Quality gate on 2026-08-15: `npm.cmd run check` — PASS. Typecheck PASS, lint PASS, 35/35 tests PASS, Vite build PASS.

## Plain-form comparison

The experiment exposes budget conflicts, cost drivers, rule-backed options and a next step before the CTA. A plain form followed by a thank-you page exposes none of these. The experiment is qualitatively more useful to both customer and manager in all complete synthetic scenarios.

## Reuse potential

- Business Discovery: `PARTIAL` — intake, deterministic score/facts, recommendation trace and outcome contract are reusable concepts; its evidence model and domain pack remain untouched.
- MebelLegal: `PARTIAL` — readiness rules and traceable gaps fit, but legal knowledge and review gates are domain-specific.
- MebelDocs: `PARTIAL` — workflow-readiness intake fits, but document truth and validation must remain deterministic and domain-specific.

## Failures and limitations

- Approved Salamat production prices are unavailable; synthetic tariff v0 cannot support customer release.
- No external AI generation was run; the fallback boundary is safe, but AI explanation quality/hallucination rate remain unverified.
- The target directory has no Git metadata, and its in-repo master instruction is still a placeholder pointing to the canonical file in `salamat-mebel-kz`.
- No real-customer or conversion evidence was collected, by design.

## Terminal decision

`PERSONALIZED_ASSESSMENT_ENGINE_DECISION: HOLD`

Reason: the small deterministic component works and produces useful differentiated outcomes, but `REUSE_COMPONENT` requires evidence for bounded AI output and mature price/rule data. Neither is available yet.

`FIRST_PRODUCTION_CANDIDATE: KITCHEN_CONFIGURATOR`

Recommended next experiment: obtain an owner-approved pilot tariff fixture, then evaluate a real bounded AI adapter against the same 12 locked scenarios and reject any output that changes numbers or introduces unsupported material claims. No production rollout is authorized.
