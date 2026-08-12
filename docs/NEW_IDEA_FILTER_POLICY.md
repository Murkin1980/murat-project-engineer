# New Idea Filter Policy

Status: ACTIVE / MANDATORY

## Rule

Every new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea must be evaluated through Murat Project Engineer before implementation starts.

## Required filter

For each new idea, Murat Project Engineer must determine in this order:

1. Does an existing active project already solve the same problem fully or partially?
2. Can the idea be implemented as an extension of an existing project without violating its foundation, architecture, scope, or deep-change-gate?
3. Can an existing component, module, repository, skill, integration, or external pattern be reused instead of building a new system?
4. Does the idea create duplicate functionality, duplicated infrastructure, or a competing product inside the current portfolio?
5. What measurable user or business outcome justifies implementation now?
6. What is the smallest test or MVP that can validate the idea before deeper development?
7. Does the change trigger the deep-change-gate? If yes, explicit user approval is required before proceeding.

## Decision outcomes

Murat Project Engineer must return exactly one primary disposition:

- EXTEND_EXISTING — add the idea to an existing project.
- REUSE_COMPONENT — reuse an existing internal or external component/pattern.
- MERGE — consolidate the idea with an overlapping project.
- EXPERIMENT — run a bounded validation experiment before product development.
- HOLD — record the idea but do not develop it now.
- NEW_REPOSITORY — create a new repository only when the idea cannot reasonably live inside an existing active project and has a distinct product boundary.
- REJECT — do not pursue because it duplicates, conflicts with, or lacks sufficient value relative to the current portfolio.

## New repository gate

Creating a new repository is the exception, not the default.

Before NEW_REPOSITORY is allowed, the evaluation must show:

- no suitable existing active repository;
- a clearly different product or system boundary;
- a measurable outcome and validation path;
- no unnecessary duplication of data models, infrastructure, auth, AI gateways, UI systems, or agent orchestration;
- compatibility with current Murat AI Stack architecture and portfolio priorities.

## Portfolio priority rule

When a new idea competes for development capacity with an active P0 project, Murat Project Engineer must explicitly compare expected value, urgency, dependencies, and opportunity cost before recommending development.

## Current default

Until the portfolio is intentionally re-prioritized, new ideas should preferentially strengthen or validate the current core projects rather than create parallel products.

## Enforcement

No new implementation or repository should begin from an unfiltered idea. The idea must first pass this policy and receive a recorded Murat Project Engineer disposition.
