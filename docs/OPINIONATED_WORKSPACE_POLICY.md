# Opinionated Workspace Policy

Status: ACTIVE / MANDATORY

## Purpose

Murat Project Engineer should minimize repeated infrastructure and tooling decisions by using a versioned, project-specific default workspace profile before substantial implementation begins.

The workspace profile is policy and configuration guidance only. It does not create a daemon, scheduler, workflow engine, persistent agent, autonomous memory service, central runtime, or new authority layer.

## Core rule

After the New Idea Filter places work into an existing project or approved experiment, MPE must resolve the project's current default workspace before implementation.

The default workspace answers, where applicable:

- source-of-truth repository and governing project files;
- execution environment/runtime;
- deployment/hosting target;
- approved integrations and reusable components;
- evidence and verification method;
- permissions/authority boundaries;
- rollback/recovery path;
- cost or compute-budget constraints.

An agent should prefer these defaults instead of reopening the same technology or infrastructure choice on every task.

## Default-over-invention rule

If a project already defines an approved runtime, deployment target, verification method, integration, or reusable component, the agent must use it by default.

The agent must not silently introduce a parallel alternative such as a second hosting platform, another auth layer, duplicate storage, another workflow engine, a competing AI gateway, or an additional deployment path merely because it is technically possible.

A deviation is allowed only when at least one of the following is true:

1. the current default cannot satisfy a concrete requirement;
2. measurable evidence shows the alternative materially improves cost, reliability, speed, quality, security, or maintainability;
3. the existing default is unavailable or operationally blocked;
4. the change is an explicitly bounded experiment approved under the New Idea Filter.

The reason for deviation must be recorded in the task/run evidence.

## Workspace profile hierarchy

Defaults should resolve from broadest to most specific:

1. portfolio/MPE constitutional rules;
2. project foundation, architecture, AGENTS/instructions and source-of-truth files;
3. project workspace profile or established operational convention;
4. task-specific override justified by evidence.

A lower layer may specialize a higher layer but must not weaken deep-change, security, permission, evidence, or approval requirements.

## Required behavior when no profile exists

Absence of a formal workspace profile is not permission to invent infrastructure.

The agent must infer the smallest safe default from the project's existing source of truth and current deployed architecture, reuse existing components where practical, and record any genuinely unresolved infrastructure decision.

If the missing decision would change core architecture, central runtime, credentials/security boundaries, persistent-agent governance, memory governance, or Router authority, the deep-change gate applies.

## Change control

Changing a workspace default is a separate decision from using it.

Routine replacement of a tool or service can remain FAST or VERIFIED when it preserves existing authority, security, persistence, and architecture boundaries.

A proposed workspace change becomes DEEP-CHANGE when it changes any protected boundary defined by the MPE deep-change policy.

## Verification invariant

The workspace profile must include or reference how completion is proven.

For software and deployed UI work, this normally means the applicable combination of:

- deterministic technical checks;
- Git diff/scope evidence;
- browser or runtime evidence where user-visible behavior is involved;
- checkpoint/PASS rules;
- rollback information.

A convenient development environment is not a substitute for evidence.

## Business value

Opinionated Workspace exists to reduce:

- repeated tool-selection discussions;
- duplicated infrastructure;
- configuration drift;
- accidental vendor/tool proliferation;
- unnecessary setup work;
- deployment inconsistency;
- verification gaps.

Success should be measured through reduced setup/rework, fewer duplicate components, lower operating cost, faster validated delivery, or improved reliability — not by the number of tools standardized.

## Portability rule

Opinionated does not mean permanently vendor-locked.

Defaults are replaceable when evidence justifies the change. Model names, providers, hosting vendors, CI services, and similar implementation choices remain configuration unless a project foundation explicitly elevates them to a stronger architectural constraint.

## Current implementation scope

This policy extends the existing MPE operating model and coordinator skill only.

It does not introduce a new repository, runtime, workspace application, persistent state service, autonomous installer, or orchestration layer.
