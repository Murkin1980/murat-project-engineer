# Reusable Derived-Artifact Production Pattern

Status: ACTIVE / REUSE_COMPONENT  
Source evidence: EXP-23 Papermorph + EXP-24 CP-13 single-agent proof  
Validated: 2026-10-10

## Purpose

Provide a default reusable contract for MPE-governed work that transforms an authoritative source into visual, media, interactive, training, presentation, or other derived artifacts.

This is a pattern, not a platform. It does not authorize a new runtime, service, database, queue, renderer, media generator, or publishing system.

## Default contract

For applicable work, prefer:

```text
authoritative source
→ stable scene/section/object identity
→ ordered beats / work units
→ optional marks
→ cues / presentation timings
→ per-beat asset slots
→ derived artifact assembly
→ acceptance checks
→ natural-language revision
→ minimal-diff verification
```

The source remains authoritative. Storyboards, timings, images, audio, video, previews, simulations, and interactive views are derived representations unless the owning project's governance explicitly promotes them.

## Required properties

1. **Stable identity**  
   Preserve stable IDs for source object, scene/section and beats/work units where applicable.

2. **Coverage ledger**  
   Material source facts/actions must map to beats/work units. Record omissions/additions explicitly. Never silently invent scope.

3. **Presentation metadata stays derived**  
   Timing, captions, visual treatment, asset choices and renderer-specific data must not silently mutate source canon/business truth.

4. **Per-unit replaceability**  
   One beat/asset/section should be replaceable without forcing unrelated approved units to change.

5. **Natural-language revision with minimal diff**  
   Translate bounded user requests into bounded changes. Preserve unaffected approved assets/fields whenever possible.

6. **Traceable provenance**  
   Record source refs and asset provenance sufficient for review and reproduction.

7. **Acceptance at the consumption surface**  
   Test the actual intended surface when material: e.g. 360 px mobile readability for video, learner interaction for training, or document correctness for generated business artifacts.

8. **No parallel platform by default**  
   Reuse existing project runtime/render/storage/verification paths unless evidence shows a real gap and the New Idea Filter authorizes a larger change.

## Proven evidence

### EXP-23

- 20/20 source actions mapped in the AI-serial fixture;
- 0 omitted / 0 added;
- 6/6 bounded previs stills;
- useful mark-based narration/visual sync contract;
- Papermorph engine itself not adopted.

### EXP-24 CP-13

Single Arena agent completed:

```text
sanitized canonical fixture
→ 20/20 action coverage
→ 6 stable beats
→ storyboard + media manifest
→ 6 test assets
→ Remotion preview
→ 360 px QA
→ three natural-language revisions
→ minimal-diff verification
```

All three bounded revision classes passed:
- timing-only change;
- single-asset replacement;
- final-beat timing/text change.

AI-serial canon remained unchanged.

## Applicability

Use this as a default reuse candidate for:
- AI-serial storyboard/previs/video production;
- MPE video/report artifacts;
- Murat House explanatory media;
- training/interactive content;
- document-to-presentation flows;
- similar source→derived-artifact workflows.

Do not force it onto unrelated CRUD, accounting, infrastructure, database, or backend work where beats/timings/assets add no value.

## Executor rule

Before designing a new media/visual/interactive transformation pipeline, Arena/Codex should first check whether this pattern can satisfy the task by extension.

Primary New Idea Filter preference when it fits:
**REUSE_COMPONENT** or **EXTEND_EXISTING**.

A new parallel pipeline requires evidence that this contract is insufficient.

## Boundaries

This pattern does not:
- choose a mandatory image/video model;
- mandate Remotion;
- mandate Papermorph;
- mandate TTS;
- create a media platform;
- authorize automatic publishing;
- change source-of-truth rules;
- authorize canon mutation.

Renderers and media generators remain replaceable adapters/tools around the stable source/beat/revision contract.
