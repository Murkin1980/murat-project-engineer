# Arena Task — EXP-24 HyperFrames PR → Video

Decision: **EXPERIMENT**

Repository: `Murkin1980/murat-project-engineer`

## Closure-first override — 2026-10-06

The purpose is to close the experiment, not to make Arena's environment capable of running the full HyperFrames stack.

Do **not** clone/build the full HyperFrames monorepo unless the minimal CLI path proves impossible to evaluate otherwise.
Do **not** use Studio, AWS/Lambda, GCP, TTS, external paid APIs, audio generation, Git LFS fixtures, or upstream regression suites.
Do **not** spend time repairing generic browser/system infrastructure beyond the bounded attempts below.

HyperFrames' documented minimal path is:
- Node.js 22+
- FFmpeg
- `npx hyperframes init`
- plain HTML composition
- `npx hyperframes preview`
- `npx hyperframes render`

The experiment may finish **PARTIAL** when the render is blocked by Arena sandbox/browser/binary constraints. PARTIAL is a valid completed outcome.

## Objective

Test only this bounded chain:

```text
one completed Murat PR
→ frozen evidence summary
→ tiny storyboard
→ one plain-HTML HyperFrames composition
→ preview/render attempt
→ PASS / PARTIAL / FAIL
→ adoption recommendation
```

## Execution

### 1. Freeze evidence first
Select one completed, non-sensitive Murat PR. Preserve only:
- repository + PR number/title
- problem
- 2–4 meaningful changes
- verification/tests
- final result / remaining limitation
- source refs

Do not wait for video tooling before completing this evidence artifact.

### 2. Storyboard
Create 3–5 scenes, total target 30–45 seconds.
No generic media DSL.

### 3. Minimal composition
Use plain local HTML/CSS only.
No React requirement.
No external CDN dependency if avoidable.
No narration/audio required.
No custom animation framework unless already available.
Prefer simple opacity/transform motion or static timed scenes.

### 4. Bounded render attempts
Check Node and FFmpeg availability.

Then make at most:
1. one minimal CLI/install attempt;
2. one preview/snapshot attempt if supported;
3. one MP4 render attempt.

A second identical render is required only if the first render succeeds.

Do not keep troubleshooting browser binaries, package managers, system libraries, codecs, NSS, sandbox flags, GPU, or network after a concrete environment blocker is established.

### 5. Mandatory terminal classification

**PASS**
- MP4 rendered
- grounding checked
- materially equivalent rerender demonstrated
- useful on phone
- no persistent infrastructure

**PARTIAL**
- evidence → storyboard → valid HyperFrames composition is complete;
- render/preview is blocked specifically by Arena environment/runtime dependency;
- blocker is reproduced and recorded.

This is a **completed experiment**, not an invitation to continue environment repair.

**FAIL**
- HyperFrames itself is unsuitable/disproportionate for this use case, independent of Arena-specific environment constraints.

## Required files before stopping

Inside `experiments/exp-24-hyperframes-pr-video/` preserve:
- `UPSTREAM_AUDIT.md`
- `FIXTURE.json` or equivalent
- `STORYBOARD.json`
- minimal composition source
- `RESULTS.md`

`RESULTS.md` must contain:
- RESULT: PASS / PARTIAL / FAIL
- ADOPTION: ADOPT / ADOPT_WITH_CHANGES / DO_NOT_ADOPT
- selected PR
- successful steps
- exact blocker, if any
- commands attempted
- checks
- changed files
- next action

## Decision guidance

If PARTIAL because Arena lacks Chrome/FFmpeg/system capability but the composition contract is valid:
- default adoption recommendation: **ADOPT_WITH_CHANGES**
- next action: validate one render later in a suitable local/CI environment, not by expanding this experiment.

If the minimal CLI itself requires disproportionate engineering or unstable infrastructure:
- **FAIL / DO_NOT_ADOPT**

STOP after the terminal result is recorded.
No production integration.


---

# Phase 2 Arena Task — agentic text → film

Owner authorization: 2026-10-08  
Disposition: **MERGE into EXP-24**  
Phase 1 result remains historical: **PARTIAL / ADOPT_WITH_CHANGES**.

## Objective

Run CP-06…CP-12 from README.md. The critical path is no longer HyperFrames-specific.

Preferred baseline:

```text
bounded source
→ editorial storyboard JSON
→ media manifest
→ voice
→ Remotion preview
→ 360 px mobile QA
→ natural-language revision
→ final render
```

HyperFrames is optional and must not block Phase 2.

## Constraints

- No new repo.
- No persistent service, DB, queue or control plane.
- Do not rebuild a stock library, TTS platform or editor.
- Use provider adapters; do not hard-wire Storyblocks/ElevenLabs into the core contract.
- Keep licensed-media provenance.
- Preserve existing Phase 1 files/evidence.
- Do not auto-publish.
- Do not change AI-serial canon.
- Stop at any deep-change boundary.

### Conditional HyperFrames bootstrap guard — EXP-28 finding

If HyperFrames is selected, reuse the existing local composition. Do not rerun its broad `init` flow unless its side effects have first been inspected and isolated: the Phase 1 invocation unexpectedly installed ten agent skills outside the repository. Before preview/render, check only the selected renderer's documented prerequisites; if the browser or codec path is blocked by the executor, record the blocker and stop rather than repairing the general sandbox. Remotion remains the preferred Phase 2 baseline; this HyperFrames-specific guard does not apply to Remotion.

## CP-06
Freeze one source and generate `EDITORIAL_STORYBOARD.json`.

## CP-07
Generate `MEDIA_MANIFEST.json` with scene-to-asset mapping and provenance. Test assets/local assets are acceptable if provider authorization is unavailable.

## CP-08
Generate narration through a `VoiceProvider` adapter and preserve reproducibility metadata.

## CP-09
Create the smallest Remotion composition that consumes the frozen storyboard/media/voice contracts. Render a preview.

## CP-10
Run mobile acceptance at 360 px effective width. Preserve machine-readable checks plus representative frame evidence.

## CP-11
Apply at least three natural-language revision requests and prove minimal-diff behavior: approved voice/media should remain unchanged unless the request requires changing them.

## CP-12
Render the accepted final version. Publishing is evidence-only/planned unless separately authorized by the owner.

## Mandatory terminal report

Update RESULTS.md with a distinct **Phase 2 Result** section:
- RESULT
- ADOPTION
- source fixture
- provider/adapters used
- CP-06…CP-12 status
- mobile QA
- revision commands and resulting diffs
- render evidence
- cost/credits if observable
- blockers
- changed files
- next action

Do not overwrite the Phase 1 terminal record.
