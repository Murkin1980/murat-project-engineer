# Human-Centered Value Delivery Principles

Status: ACTIVE / MANDATORY CORE PRODUCT PRINCIPLE
Decision: EXTEND_EXISTING
Owner: Murat Project Engineer Core
Date: 2026-09-17

## Purpose

This policy defines a shared product and automation philosophy for Murat Project Engineer and human-facing projects governed by MPE.

The goal is not to maximize AI activity, automation count, prompts, agent runs, or user engagement for its own sake. The goal is to reduce unnecessary human effort, preserve trust, prove real value through completed outcomes, and leave work in a resumable state whenever execution cannot continue.

## Core rule

Human involvement should be rewarded with visible relief.

A user who gives the system attention, context, confirmation, or access should receive a measurable reduction in work, uncertainty, errors, waiting, or cognitive load whenever technically and safely possible.

Canonical value loop:

```text
ENGAGEMENT
  -> UNDERSTANDING
  -> IMPROVEMENT
  -> VISIBLE RELIEF
  -> TRUST
  -> OPTIONAL DEEPER ENGAGEMENT
```

Do not use engagement mechanics that create work without returning useful value.

## 1. Observe real work, not only reported work

People frequently omit routine actions because those actions have become habitual, invisible, inconvenient to describe, or difficult to remember accurately.

Therefore human-facing discovery and automation systems should not depend exclusively on interviews, forms, or self-reporting.

When appropriate and consented, use the minimum necessary combination of:

- system events and logs;
- workflow and application transitions;
- artifacts and file histories;
- process/task evidence;
- structured communication events;
- observed exceptions and handoffs;
- short targeted human confirmations.

Preferred interaction pattern:

```text
OBSERVE -> DETECT PATTERN -> ASK SMALL QUESTION -> VALIDATE -> IMPROVE
```

Do not require a user to reconstruct an entire process from memory when evidence can establish most of it first.

## 2. Interview is evidence, not truth

Human explanation remains important, but it is one evidence source among others.

Systems should preserve disagreement between:

- declared process;
- documented process;
- system process;
- observed process;
- exception process.

Do not silently convert a person's description into the canonical process model without reconciliation where evidence exists.

## 3. Find friction before choosing technology

Start with human effort and process friction, not with a preferred technology.

Useful recurring patterns include:

- copying and repeated data entry;
- searching and retrieval;
- checking and validation;
- waiting and chasing;
- routing and classification;
- reformatting and transformation;
- remembering and follow-up;
- reconciliation across systems;
- summarizing and transcription;
- repeated correction;
- manual approval handoffs;
- hidden exception handling.

A detected pattern should be classified into an intervention type before selecting AI, RPA, integrations, agents, or other implementation technology.

Candidate intervention types:

- REMOVE
- AUTOMATE
- ASSIST
- STANDARDIZE
- INTEGRATE
- VALIDATE
- MONITOR
- LEAVE_HUMAN

Automation is one possible intervention, not the default answer.

## 4. Gamification must represent real relief

Gamification may be used to reduce resistance and make discovery/automation understandable, but it must not become manipulation, surveillance theater, or an artificial points economy.

Preferred rewards are real outcomes:

- minutes or hours returned;
- manual actions removed;
- errors prevented;
- handoffs removed;
- repeated checks eliminated;
- processes simplified;
- completed improvements.

Preferred product metric names include `Time Returned`, `Work Removed`, `Manual Steps Removed`, and `Errors Prevented`.

Avoid rewarding users merely for filling forms, generating prompts, clicking repeatedly, or increasing time spent in the product.

Visual agents or assistant characters may be used to make system activity legible. Each visual agent should correspond to a real role or state such as observing, mapping, validating, improving, or monitoring. Decorative animation must not imply work that did not occur.

## 5. Proof before pay

For first-time onboarding and discovery-led products, prove value before asking the user to pay for continuation whenever technically, legally, and operationally safe.

Preferred sequence:

```text
DISCOVER
  -> EXPLAIN
  -> COMPLETE ONE SAFE IMPROVEMENT
  -> MEASURE
  -> SHOW RESULT
  -> OFFER NEXT VALUE
```

Canonical principle:

> First-session value should include one completed improvement, not analysis alone, whenever a safe bounded improvement is possible.

If direct execution is not possible, deliver the closest useful completed artifact: a ready workflow, validated configuration, prepared script, corrected form, migration/import package, actionable template, or one-confirmation-ready change.

Do not create a paywall that intentionally leaves the user's current work in a worse or unusable state.

Monetization should be value-based and non-coercive: make the next paid step understandable in terms of additional work removed or value delivered, not merely tokens, agent runs, or artificial scarcity.

## 6. Proof of Relief

For human-facing automation, a successful proof should demonstrate at least one observable relief outcome:

- faster completion;
- fewer manual actions;
- fewer errors;
- less remembering or monitoring;
- fewer context switches;
- reduced waiting;
- reduced rework.

Record before/after evidence where practical.

A discovery result that merely says "this can be automated" is weaker than a bounded demonstration showing the user that one part of the work is already easier.

## 7. Never stop at an unusable state

When work cannot continue because of a usage limit, missing credential, unavailable integration, human approval, external dependency, budget boundary, model/context boundary, or other blocker, the system must perform a graceful handoff instead of abandoning execution mid-process.

Minimum handoff contract:

```text
STATE       what has been completed
EVIDENCE    what was learned or verified
CHANGES     what changed
RESULT      usable value already delivered
BLOCKER     why execution stopped
NEXT ACTION smallest next action required
HANDOFF     sufficient context/artifacts to resume without repeating work
```

Where code or files changed, include relevant diff/commit/artifact references according to the project's normal governance.

Canonical continuation rule:

> No rediscovery required.

A user should not have to repeat previously supplied context or re-explain a process solely because a session, quota, agent, or execution boundary was reached.

## 8. Preserve safe terminal states

Every substantial workflow should define safe terminal or pause states.

If an automation cannot complete fully, it should prefer a valid partially completed artifact plus explicit status over an opaque failure or half-written state.

Examples:

- save draft + validation state rather than discard work;
- commit or preserve bounded changes + handoff rather than leave untracked partial edits;
- preserve discovery evidence + confirmed pattern labels rather than restart observation;
- preserve process state + pending approval rather than reconstruct the case later.

## 9. Human-centered does not mean surveillance

Observe work patterns only to improve processes and reduce unnecessary effort.

Do not convert process-discovery signals into employee productivity scoring by default.

Prefer aggregated workflow/role/pattern evidence over individual ranking when individual identity is not required.

Collect the minimum content necessary. Prefer metadata or structural events when they are sufficient. Sensitive observation must be transparent, permissioned where required, and bounded by applicable privacy/security rules.

Canonical boundary:

```text
observe work patterns != evaluate human worth or employee performance
```

## 10. Trust-preserving interaction

Human confirmation requests should be small, contextual, and skippable whenever possible.

Prefer:

> "We observed X. Is this Y?"

instead of:

> "Describe your entire process."

Use progressive confirmation rather than long mandatory questionnaires when evidence already exists.

Never pretend an improvement occurred when only a recommendation was generated.

## 11. Cross-project application

These principles are mandatory design input for MPE-governed projects that include one or more of:

- human-facing automation;
- process discovery;
- onboarding;
- AI agents acting on a user's work;
- recommendations intended to change workflows;
- usage/plan limits that can interrupt substantial work;
- monetization tied to automation or productivity value.

Projects may adapt the UX, metrics, and implementation, but must not silently invert the core principles.

## 12. Development gate

Before substantial implementation of a human-facing workflow, the developer/agent should answer:

1. What real human friction is being reduced?
2. What evidence proves the friction exists?
3. What is the smallest completed relief we can safely deliver?
4. How will the user see the result?
5. What happens if execution stops halfway?
6. Can the workflow resume without rediscovery?
7. Does monetization follow demonstrated value rather than precede all value?
8. Are observation and gamification trust-preserving rather than manipulative?

If a proposed implementation conflicts materially with these principles, surface the conflict and apply the existing MPE deep-change/governance rules before proceeding.
