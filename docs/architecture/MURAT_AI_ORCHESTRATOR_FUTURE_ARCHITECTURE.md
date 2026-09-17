# Murat AI Orchestrator — Future Architecture Hold

Status: HOLD / FUTURE TARGET ARCHITECTURE
Decision: HOLD
Owner: Murat Project Engineer

## Purpose

Preserve the intended future architecture of the Murat AI Orchestrator without expanding the current MVP scope.

The MVP remains Cloud-first and may use existing cloud storage/runtime patterns without mandatory Kazakhstan data residency. Kazakhstan-hosted client data infrastructure, legal-entity migration, compliance automation, and infrastructure auto-provisioning are deferred until the product proves value and is ready for commercial scaling.

This document is a target boundary map, not an implementation authorization.

## Current MVP rule

For the MVP and early private pilots:

- use the simplest Cloud-first architecture that validates product value;
- do not create Kazakhstan-specific tenant infrastructure unless a concrete pilot requirement forces it;
- do not create a separate Kazakhstan legal-entity architecture yet;
- do not build per-client VPS provisioning by default;
- do not add extra gateways, routers, or services unless they remove a demonstrated bottleneck;
- keep the path from product to model/provider short;
- preserve enough metadata and abstractions so later migration is possible without redesigning the product semantics.

## Future target architecture

The mature Orchestrator is expected to contain four major internal planes.

### 1. Execution Plane

Responsibilities:

- receive machine-readable work requests from Business Discovery and other products;
- classify task complexity and capability requirements;
- select the appropriate model/provider/tool;
- create DIRECT, SESSION, or DURABLE execution modes;
- manage retries, fallbacks, quality escalation, and handoff generation;
- persist final artifacts/results separately from temporary session memory;
- keep external gateways optional rather than mandatory hops.

Preferred normal path:

```text
Product
  -> Murat AI Orchestrator
  -> selected model/provider
  -> result/handoff
```

External gateways or aggregators may be used only as optional provider adapters or experiments.

### 2. Finance Plane / AI Treasury

Responsibilities:

- track provider budgets, balances, reserves, and burn rate;
- allocate spend by product, client/tenant, task family, and execution class;
- separate customer-delivery spend from platform operations, R&D, and reserve budgets;
- calculate cost per task, cost per verified relief unit, infrastructure cost, and contribution margin;
- allow routing decisions to consider budget while never allowing finance logic to redefine task meaning or quality requirements;
- support a self-funding model where product revenue replenishes the technical operating budget.

Illustrative budget classes:

```text
CUSTOMER_DELIVERY
PLATFORM_OPERATIONS
R_AND_D
RESERVE
```

Provider balances or virtual envelopes may include OpenAI, Anthropic, Gemini, DeepSeek, Workers AI, long-tail providers, and future specialised models.

### 3. Intelligence Plane

This plane must remain split into two distinct scopes.

#### Tenant / Client Intelligence

Private to the client/tenant:

- Business Operating Portrait;
- process evidence;
- Work Atoms and Relief Atoms;
- recommendations;
- intervention history;
- Verified Relief Units;
- client-specific outcomes and business metrics.

#### Platform Intelligence

Cross-client product learning must use anonymised/aggregated derived data rather than raw client data.

Examples of allowed future aggregate dimensions:

- industry;
- company-size band;
- process category;
- pattern type;
- intervention type;
- success/failure outcome;
- time-returned band;
- cost band;
- model family/performance class;
- product capability gaps.

Raw personally identifying or directly re-identifying client information must not flow into platform-wide analytics by default.

Platform Intelligence should help answer:

- which business types the platform handles well;
- which patterns are frequently discovered;
- which interventions produce measurable relief;
- which task classes unnecessarily consume strong models;
- where the product has technical or philosophical capability gaps.

### 4. Infrastructure Plane

Deferred for the MVP.

Future responsibilities:

- provision Kazakhstan-hosted tenant infrastructure;
- manage tenant isolation level;
- create/resize/suspend/restore/delete compute and storage resources;
- manage databases, object storage, backups, and lifecycle;
- expose provider adapters for Kazakhstan cloud providers;
- integrate infrastructure cost into Finance Plane;
- preserve governance gates for destructive, expensive, or deep infrastructure changes.

Target tenancy modes:

```text
SHARED_KZ
ISOLATED_KZ
DEDICATED_KZ
```

The Infrastructure Plane should eventually be provider-abstracted rather than hard-wired to one vendor.

Illustrative adapter contract:

```text
createTenant()
createVM()
resizeVM()
createDatabase()
createStorage()
backup()
restore()
destroy()
getUsage()
```

Potential providers may include Kazakhstan-region infrastructure from providers such as PS Cloud Services, Yandex Cloud Kazakhstan, or other suitable vendors, but provider selection is explicitly deferred.

## Legal and compliance migration trigger

Do not implement the full Kazakhstan-residency architecture during the MVP merely because it may be required later.

Revisit this architecture when Business Discovery or another product reaches commercial-product maturity and the team is preparing to:

- register a Kazakhstan legal entity (for example a future LLP/ТОО);
- sell broadly beyond controlled pilots;
- process material amounts of client personal/business-confidential data;
- formalise external LLM/API subprocessors;
- introduce contractual data-processing commitments;
- require Kazakhstan-resident storage, stronger tenant isolation, or enterprise controls;
- establish product-level accounting and taxation.

At that point a dedicated legal/compliance review becomes a required deep-change gate.

## Data-residency target principle

The future mature architecture should be able to keep raw tenant-private and legally sensitive data in a Kazakhstan-resident data plane, while sending only the minimum permitted work packet to external model providers.

Conceptually:

```text
KZ Tenant Data
  -> privacy/minimisation policy
  -> temporary work packet
  -> external model/provider
  -> result
  -> KZ tenant store
```

This target does not constrain the current MVP unless required by a specific pilot or legal review.

## Session lifecycle target

The future Orchestrator should support:

```text
session start
-> temporary working memory
-> model/tool execution
-> checkpoints
-> final handoff/artifact
-> durable result ownership returned to originating product
-> temporary memory expiry/deletion
```

Canonical continuation rule:

**No rediscovery required.**

A completed or interrupted session should leave enough structured state for the originating product to continue without repeating discovery already completed.

## Product boundary

Business Discovery and other end-user products must not expose model/provider accounting, routing mechanics, infrastructure provisioning, or provider credentials to the client.

The user buys the product outcome.

The Orchestrator owns technical execution choices within policy, budget, quality, and privacy constraints.

## Anti-bloat rule

Do not prematurely split Finance, Intelligence, Infrastructure, and Execution into separate repositories or network services.

Keep them as logical modules of one Orchestrator until measured scale, legal requirements, reliability, or team boundaries justify physical separation.

Every new network hop must demonstrate a clear benefit in reliability, isolation, compliance, cost, or operability before introduction.

## Revisit criteria

Re-open this HOLD when at least one of the following becomes true:

1. Business Discovery has proven product value on the owner's business plus multiple external pilot users.
2. A commercial launch is being prepared.
3. A Kazakhstan legal entity is being formed for the software business.
4. A client requires Kazakhstan-resident storage or isolated infrastructure.
5. Cloud-first MVP architecture creates a measured legal, cost, privacy, latency, or reliability limitation.
6. Infrastructure automation itself becomes a verified product requirement.

Until then: preserve this architecture, but do not build it.
