# EXP-30 — AI Process Discovery

Status: PLANNED | MPE disposition: EXPERIMENT | Date: 2026-10-29
Owner: Murat Project Engineer | Pilot: Grand Mebel Document Control

## Hypothesis
Mapping real operations before automation produces a more reliable, measurable roadmap than feature-first AI implementation.

## Scope
Read-only study of 10 real document bundles (invoice, waybill, optional AVR) with anonymized operational evidence. Interview actual operators. Measure human **touch time** and end-to-end **lead time** separately. Map each step atomically (one actor, system, action). Record exception types, frequency, rework, costs, and failure modes. Classify each step:
- BLUE / RULE: deterministic validation or automation;
- PURPLE / JUDGMENT: ambiguous inputs suitable for assisted AI with confidence and human approval;
- ORANGE / MONEY_OR_RELATIONSHIP: sensitive financial, legal and customer decisions retained by authorized humans.

For each candidate step, score observed frequency × minutes per occurrence × estimated error impact (declare units/normalization and never treat the product as currency without calibration). Compare baseline exception rate, eligible touchless rate, operator time, lead time, error and rework counts. Keep a distinct record of operations where human sign-off is legally or operationally mandatory.

## Sequence
1. Identify existing MPE/MCC/Grand Mebel components and current policies to avoid duplicates.
2. Observe and time 10 real workflows; record provenance, timestamps, and redaction.
3. Map atomic actions and log observed exceptions; do not extrapolate from a tiny sample without caveats.
4. Classify rule / AI-judgment / human-money steps; document approval and deep-change gates.
5. Rank low-risk candidates by measured value; propose a minimal human-approved draft-generation test only if justified.
6. Produce results, limitations, ROI ranges and next MPE disposition.

## Acceptance evidence
- 10 documented anonymized cases with touch/lead timing and an atomic step inventory.
- Exception register and classification rationale for all mapped steps.
- Reproducible baseline and calculations, with observed vs hypothetical numbers separated.
- Explicit keep-human gates for financial, tax, legal, customer and final-document approval actions.
- Owner review of any proposed downstream build; no implementation or deployment is authorized by this experiment registration.

## Constraints
No new repository, worker, database, agent, production integration, deployment, autonomous write, document approval or governance changes. No changes to Grand Mebel production. Any deep-change requires separate explicit owner consent.

Source: user-supplied narration, “How a $50K AI Project Actually Starts” (Harlow Industrial Supply example); conceptual method, not verified vendor performance data.
