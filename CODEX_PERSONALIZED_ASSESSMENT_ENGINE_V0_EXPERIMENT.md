# CODEX INSTRUCTION — PERSONALIZED ASSESSMENT ENGINE v0 EXPERIMENT
## Outcome-pattern reuse inside existing Murat projects

**Date:** 2026-08-15
**Primary governing repository:** `Murkin1980/murat-project-engineer`
**Primary decision:** `EXPERIMENT`
**New repository:** `NO`
**Deep change:** `NOT AUTHORIZED`

---

# 0. EXECUTIVE DIRECTIVE

Evaluate and prototype a reusable **Personalized Assessment Engine v0** inspired by the public product pattern observed in Outcome.

Do NOT clone Outcome as a SaaS.

Do NOT copy proprietary UI, code, private APIs, internal implementation details, branding, text, or protected assets.

The experiment is limited to reproducing the **general product pattern**:

```text
Ask
→ Understand
→ Calculate
→ Diagnose
→ Explain
→ Recommend
→ Convert
```

The first consumer should be an existing Kitchen / furniture lead-flow or configurator project if repository evidence shows that this is the smallest viable extension.

The engine must remain domain-aware and architecture-light.

---

# 1. MURAT PROJECT ENGINEER NEW IDEA FILTER

Record this before implementation:

```text
MURAT_PROJECT_ENGINEER_NEW_IDEA_FILTER

Idea:
Reusable Personalized Assessment Engine based on the public Outcome product pattern.

Decision:
EXPERIMENT

Why:
- Existing projects already contain intake, calculation, lead-flow, evidence, or recommendation components.
- The hypothesis can be tested without a new repository.
- The first value test is measurable.
- Outcome should be treated as reference architecture, not a dependency.
- The experiment can reuse deterministic rules plus AI explanation.
- No deep architecture change is needed for v0.
```

Do NOT create a new repository.

If existing repository boundaries clearly make a new repository unavoidable:

```text
NEW_REPOSITORY_REQUIRES_USER_APPROVAL
```

Stop and report.

---

# 2. SOURCE OF TRUTH

Before coding, inspect:

1. `Murkin1980/murat-project-engineer`
2. current Kitchen Configurator / kitchen lead-flow repository
3. `Murkin1980/business-discovery`
4. any existing shared calculation / lead / recommendation components referenced by those projects

Use current GitHub/repository reality.

Do not assume old filenames.

For each candidate repository identify:

```yaml
repo:
  active:
  purpose:
  current_architecture:
  intake_components:
  calculator_components:
  rules_engine:
  ai_components:
  result_page_components:
  crm_or_lead_components:
  shared_types:
  reusable_components:
  duplication_risk:
  integration_cost:
```

---

# 3. FIRST REQUIRED DECISION AFTER REPOSITORY AUDIT

Choose exactly one:

```text
EXTEND_EXISTING
REUSE_COMPONENT
MERGE
HOLD
REJECT
```

for the **implementation target**.

Expected preference:

```text
EXTEND_EXISTING
```

if a suitable Kitchen Configurator / Salamat lead-flow repo already exists.

Do not implement until this repository-level decision is written into the experiment report.

---

# 4. PRODUCT HYPOTHESIS

Test this hypothesis:

> A short structured furniture intake, combined with deterministic business rules and AI explanation, can produce a useful personalized kitchen assessment that is more actionable than a normal quote form while remaining reproducible and safe.

The experiment does NOT test:

- real customer conversion;
- production sales performance;
- paid traffic performance;
- CRM automation;
- WhatsApp automation;
- full Kitchen Configurator;
- Business Discovery integration;
- SaaS multi-tenancy;
- billing;
- marketplace behavior.

---

# 5. FIRST MVP USE CASE

Create one narrow experience:

# "Kitchen Project Assessment"

User answers approximately 7–10 questions.

Suggested topics:

```text
1. kitchen layout
2. approximate length / dimensions
3. facade preference
4. countertop preference
5. hardware level
6. appliances / complexity
7. target budget
8. desired timeline
9. installation/location constraints
10. optional priority: lowest price / balance / premium
```

Do not add a question unless its answer changes:

```text
calculation
diagnosis
recommendation
routing
```

If a question changes none of those, remove it.

---

# 6. OUTPUT OF MVP

The result page should produce a structured assessment such as:

```text
Kitchen Project Assessment

Configuration:
...

Budget Fit:
78 / 100

Estimated verified range:
1,350,000–1,550,000 KZT

Main cost drivers:
1. MDF facades
2. Blum hardware
3. countertop choice

Budget gap:
150,000–350,000 KZT

Options:
A. Keep current configuration
B. Reduce hardware tier
C. Change countertop

Recommended next step:
Measurement / exact calculation
```

Important:

The AI must NOT invent the price range.

Price/rule data must come from deterministic logic or existing verified calculation rules.

---

# 7. CORE DESIGN PRINCIPLE

Use two layers:

```text
DETERMINISTIC ENGINE
+
AI OUTCOME ENGINE
```

## Deterministic engine owns:

- price;
- dimensions;
- allowed ranges;
- hard eligibility;
- required business rules;
- scoring formulas where exact;
- routing gates;
- critical classification.

## AI engine owns:

- explanation;
- prioritization;
- summary;
- recommendation wording;
- trade-off explanation;
- personalization;
- presentation.

Never allow:

```text
answers → LLM → authoritative price
```

Use:

```text
answers
→ validated inputs
→ deterministic calculation
→ structured facts
→ AI explanation
```

---

# 8. MINIMAL DATA MODEL

Reuse existing project types first.

Only introduce missing concepts.

Suggested logical entities:

```text
AssessmentDefinition
Question
Answer
AssessmentInput
DeterministicFacts
ScoreDimension
AssessmentRun
Recommendation
Outcome
CTA
```

Possible TypeScript shapes:

```ts
type AssessmentInput = {
  layout: string;
  lengthMm?: number;
  facadeTier?: string;
  countertopTier?: string;
  hardwareTier?: string;
  budgetKzt?: number;
  timelineDays?: number;
  priority?: "budget" | "balanced" | "premium";
};

type DeterministicFacts = {
  estimateMinKzt?: number;
  estimateMaxKzt?: number;
  budgetGapKzt?: number;
  budgetFitScore?: number;
  costDrivers: string[];
  constraints: string[];
  ruleVersion: string;
};

type PersonalizedOutcome = {
  summary: string;
  score?: number;
  diagnosis: string[];
  strengths: string[];
  gaps: string[];
  recommendations: Recommendation[];
  nextSteps: string[];
  cta: {
    type: string;
    label: string;
  };
};
```

Do not create a generic workflow framework unless current repo already has one.

---

# 9. WORKFLOW v0

Use the smallest possible pipeline:

```text
START
 ↓
INTAKE
 ↓
VALIDATE_INPUT
 ↓
CALCULATE
 ↓
CLASSIFY
 ↓
GENERATE_ANALYSIS
 ↓
GENERATE_RECOMMENDATIONS
 ↓
COMPOSE_RESULT
 ↓
CTA
 ↓
END
```

No agent graph.

No generic DAG.

No persistent worker.

No new runtime.

No scheduler.

No queue.

---

# 10. ASSESSMENT ENGINE CONTRACT

Prefer one deterministic function plus one AI-generation boundary.

Conceptually:

```ts
calculateAssessment(input)
→ DeterministicFacts
```

then:

```ts
generateOutcome({
  input,
  facts,
  knowledge,
  constraints
})
→ PersonalizedOutcome
```

The AI call must receive structured facts.

Do not make the model infer source-of-truth numbers from prose.

---

# 11. KNOWLEDGE GROUNDING

For v0, use only bounded project knowledge.

Possible sources:

- existing material tiers;
- existing price rules;
- furniture calculation formulas;
- hardware categories;
- kitchen-specific business rules;
- approved recommendations;
- existing FAQ / sales guidance.

Do not introduce vector DB or RAG infrastructure unless already present and trivially reusable.

For MVP, a bounded structured object or markdown source is acceptable.

Example:

```yaml
knowledge:
  facade_tiers:
  hardware_tiers:
  countertop_tiers:
  recommendation_rules:
  wording_constraints:
```

---

# 12. SCORING

Use deterministic scoring where possible.

Example:

```text
Budget Fit Score
0–100
```

Possible basis:

```text
estimated_midpoint
vs
declared_budget
```

Do not let LLM assign arbitrary numeric scores without a rule.

If no meaningful score can be defined, omit the number.

A qualitative result is better than a fake metric.

---

# 13. RECOMMENDATION RULES

Recommendations must be traceable.

Example:

```text
IF budget < estimate_min
AND hardware = premium
THEN recommendation candidate:
downgrade hardware tier
```

Then AI may explain:

> Replacing premium hardware with the standard tier is likely to reduce cost without changing the facade appearance.

The AI may improve wording.

It may not invent the rule.

---

# 14. RESULT COMPOSITION

Result page should use structured blocks:

```text
1. Project summary
2. Budget fit
3. Cost drivers
4. Gaps / conflicts
5. Options
6. Recommendations
7. Next step
```

Do NOT build a generic visual page builder.

Do NOT build custom drag-and-drop blocks.

One result page is enough.

---

# 15. UX RULES BORROWED FROM THE OUTCOME PATTERN

Use these product principles:

## Rule A
Sell the result, not the form.

Bad:

```text
Fill out our questionnaire
```

Better:

```text
Get a preliminary assessment of your kitchen project
```

## Rule B
Ask only questions that change the outcome.

## Rule C
Give value before sales CTA.

## Rule D
Show the user a concrete gap or trade-off.

## Rule E
CTA must follow naturally from the diagnosis.

Example:

```text
To confirm the exact price,
the next required step is measurement.
```

---

# 16. TEST SCENARIOS

Do not use real customers yet.

Create at least 12 synthetic scenarios.

Minimum groups:

## A. Budget fit

```text
simple kitchen
low-cost materials
adequate budget
```

Expected:
GOOD_FIT

## B. Premium configuration with adequate budget

Expected:
PREMIUM_FIT

## C. Budget conflict

```text
MDF
premium hardware
stone countertop
low budget
```

Expected:
BUDGET_GAP

## D. Missing data

Expected:
PARTIAL / REQUEST_MORE_INFO

## E. Unrealistic timeline

Expected:
TIMELINE_RISK

## F. Contradictory preferences

Example:

```text
priority = lowest price
hardware = premium
countertop = premium
```

Expected:
TRADEOFF_REQUIRED

Run multiple variants per group.

---

# 17. ACCEPTANCE CRITERIA

The MVP passes only if all are true:

```text
1. Same deterministic input produces same deterministic facts.
2. AI never changes authoritative numbers.
3. Different input profiles produce materially different outcomes.
4. Recommendations are traceable to rules/facts.
5. No hallucinated product/material facts are accepted.
6. Missing inputs do not produce fabricated certainty.
7. At least 10/12 synthetic scenarios meet expected classification.
8. Existing repo tests remain passing.
9. No architecture boundary is crossed.
10. No new repository is created.
```

---

# 18. QUALITY EVALUATION

For each scenario score:

```yaml
scenario:
  deterministic_correctness: PASS | FAIL
  classification_correctness: PASS | FAIL
  recommendation_relevance: 1-5
  explanation_quality: 1-5
  hallucination: YES | NO
  unsupported_claims: YES | NO
  useful_to_customer: 1-5
  useful_to_manager: 1-5
```

Compute:

```text
classification_pass_rate
hallucination_rate
average_recommendation_relevance
average_customer_usefulness
```

---

# 19. REQUIRED COMPARISON

Compare MVP against a plain form.

Baseline:

```text
Form
→ Thank-you page
```

Experiment:

```text
Form
→ Personalized Assessment
```

Since no real customers are used, compare qualitatively using synthetic scenarios.

Questions:

```text
Does the assessment:
- expose conflicts?
- explain cost drivers?
- give useful next steps?
- help a manager understand the lead faster?
- provide more value than a plain form?
```

---

# 20. NO REAL CUSTOMER TEST YET

Do NOT expose publicly in this stage.

Do NOT:

- send to customers;
- run Google Ads;
- connect production WhatsApp;
- connect live CRM;
- collect personal data;
- store customer phone numbers;
- publish as production feature.

Use local/preview-only testing.

Public customer testing requires a separate approval after v0 passes.

---

# 21. BUSINESS DISCOVERY REUSE CHECK

Do NOT integrate Business Discovery now.

Only answer:

```text
Could the same engine later support:

Business Intake
→ deterministic scoring
→ diagnosis
→ recommendations
→ action plan
```

Classify:

```text
YES
PARTIAL
NO
```

Identify reusable parts:

```text
AssessmentDefinition
Question
Rule
ScoreDimension
AssessmentRun
Recommendation
Outcome
```

Do not modify Business Discovery core model during this experiment.

---

# 22. MEBELLEGAL / MEBELDOCS REUSE CHECK

Documentation only.

Evaluate whether engine pattern could later support:

```text
MebelLegal:
legal readiness assessment

MebelDocs:
document workflow readiness assessment
```

Do not implement either integration.

---

# 23. COMPONENT REUSE AUDIT

Before adding files, search existing repositories for:

```text
questionnaire
form schema
calculator
price rules
lead
score
assessment
recommendation
result
wizard
stepper
intake
```

For each candidate component classify:

```text
REUSE_AS_IS
EXTEND
ADAPT
DO_NOT_REUSE
```

Do not duplicate working components.

---

# 24. DEEP-CHANGE GATE

Stop if implementation requires:

- new generic workflow runtime;
- new agent framework;
- vector database;
- new persistence service;
- multi-tenant architecture;
- billing;
- new repo;
- domain-model rewrite;
- Router authority change;
- persistent agents;
- scheduler;
- queue;
- external SaaS dependency;
- production data flow change.

Return:

```text
DEEP_CHANGE_REQUIRES_USER_APPROVAL
```

Do not continue that change.

---

# 25. EXPECTED FILES

Prefer extending an existing Kitchen project.

Possible additions:

```text
src/assessment/
  types.ts
  calculateAssessment.ts
  generateOutcome.ts
  rules.ts

src/components/
  KitchenAssessmentForm.*
  KitchenAssessmentResult.*

tests/
  kitchen-assessment.*
```

Adapt to actual repository structure.

Do NOT force these exact paths.

---

# 26. EXPERIMENT REPORT

Inside `murat-project-engineer`, create/update a canonical evaluation report.

Suggested path:

```text
docs/evaluations/PERSONALIZED_ASSESSMENT_ENGINE_V0.md
```

If equivalent file exists, update it.

Include:

```text
- repository selected
- reuse audit
- architecture decision
- deterministic rules
- AI boundary
- test scenarios
- metrics
- failures
- screenshots/preview reference if available
- reuse potential
- final decision
```

---

# 27. RUN REPORT

Record as a normal MPE run.

Suggested ID:

```text
RUN-09
```

Suggested task:

```text
Controlled Personalized Assessment Engine v0 experiment using a kitchen project assessment with synthetic scenarios.
```

Suggested risk tier:

```text
VERIFIED
```

Use actual current Run Report schema.

Do not invent unsupported fields.

---

# 28. TERMINAL DECISION

After experiment choose exactly one:

```text
PERSONALIZED_ASSESSMENT_ENGINE_DECISION:

REUSE_COMPONENT
HOLD
REJECT
```

## REUSE_COMPONENT

Only if:

- deterministic layer works;
- personalized outcomes are meaningfully different;
- AI output remains bounded;
- recommendations are useful;
- reuse across projects is plausible;
- implementation is small and clean.

## HOLD

If:

- concept is useful but rules/data are incomplete;
- AI quality is inconsistent;
- kitchen formulas are not mature enough;
- integration cost is unclear.

## REJECT

If:

- result adds little beyond normal calculator/form;
- AI output is too generic;
- hallucination risk is unacceptable;
- component requires excessive architecture.

---

# 29. SECONDARY DECISION

Also choose:

```text
FIRST_PRODUCTION_CANDIDATE:

KITCHEN_CONFIGURATOR
SALAMAT_LEAD_FLOW
BUSINESS_DISCOVERY
NONE
```

Do not productionize it during this task.

---

# 30. SUCCESS DEFINITION

The experiment is successful only if it answers:

> Can an existing Murat project produce a reliable, useful, personalized kitchen assessment using deterministic furniture rules plus bounded AI explanation, without creating a new system?

Not success:

```text
AI generated nice text
```

Success:

```text
correct facts
+
different outcomes for different scenarios
+
useful recommendations
+
traceable rules
+
small architecture footprint
```

---

# 31. IMPLEMENTATION ORDER

Execute exactly in this order:

```text
STEP 1
Read Murat Project Engineer source of truth.

STEP 2
Read current Kitchen / lead-flow repositories.

STEP 3
Run component reuse audit.

STEP 4
Choose implementation target:
EXTEND_EXISTING / REUSE_COMPONENT / MERGE / HOLD / REJECT.

STEP 5
Document minimal deterministic rule set.

STEP 6
Define 12 synthetic scenarios and expected outcomes BEFORE coding AI behavior.

STEP 7
Implement deterministic assessment core.

STEP 8
Add tests for deterministic facts and classifications.

STEP 9
Implement bounded AI outcome generation.

STEP 10
Add minimal intake + result UI in local/preview scope.

STEP 11
Run all synthetic scenarios.

STEP 12
Review hallucinations and unsupported claims.

STEP 13
Measure quality metrics.

STEP 14
Evaluate reuse for Business Discovery / MebelLegal / MebelDocs without integrating them.

STEP 15
Create/update MPE evaluation + RUN-09 evidence.

STEP 16
Choose:
REUSE_COMPONENT / HOLD / REJECT.

STEP 17
Return compact summary to Murat.

STEP 18
STOP.
No production rollout.
```

---

# 32. REQUIRED FINAL RESPONSE TO MURAT

Return exactly:

```text
PERSONALIZED ASSESSMENT ENGINE v0

Overall:
PASS / CONDITIONAL / FAIL

Implementation target:
...

Repository decision:
EXTEND_EXISTING / REUSE_COMPONENT / MERGE / HOLD / REJECT

New repository:
NO

Synthetic scenarios:
N

Classification pass rate:
X%

Hallucination rate:
X%

Average recommendation relevance:
X/5

Average customer usefulness:
X/5

Average manager usefulness:
X/5

Deterministic layer:
PASS / FAIL

AI boundary:
PASS / FAIL

Kitchen result:
USEFUL / PARTIAL / NOT_USEFUL

Business Discovery reuse:
YES / PARTIAL / NO

MebelLegal reuse:
YES / PARTIAL / NO

MebelDocs reuse:
YES / PARTIAL / NO

Deep change required:
YES / NO

Decision:
REUSE_COMPONENT / HOLD / REJECT

First production candidate:
KITCHEN_CONFIGURATOR / SALAMAT_LEAD_FLOW / BUSINESS_DISCOVERY / NONE

Recommended next action:
...
```

Then point Murat to the full report and preview.

---

# 33. FINAL ARCHITECTURE RULE

Do not build:

```text
Outcome clone
```

Build only enough to test:

```text
structured intake
+
deterministic rules
+
bounded AI explanation
+
personalized result
+
next best action
```

The engine earns reuse only through evidence.
