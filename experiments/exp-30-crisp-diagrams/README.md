# EXP-30 — Crisp Diagrams

Status: PLANNED (registration only)
Date added: 2026-10-11
Owner: Murat Project Engineer
Disposition: EXPERIMENT

## Source
- Upstream: https://github.com/sandrinodm/skills
- Skill: `crisp-diagrams`
- Reference installation command (NOT executed): `pnpx skills add sandrinodm/skills --skill crisp-diagrams`

## Hypothesis
A small, reproducible, branded SVG architecture diagram can improve stakeholder and mobile comprehension compared to the existing diagram path without establishing a second diagram system.

## Portfolio fit / non-duplication
- MPE: architecture and component relationships, initially as a read-only documentation sample.
- Business Discovery: explain workflow to clients, later reuse only if evidence supports it.
- Murat House: editorial diagrams, later reuse only if approved.
- Compare against existing Mermaid/diagram options; do not replace them by default.
- Keep configuration in existing project documentation; no new repository, worker, storage, integration, or service.

## Bounded pilot (not authorized to run by registration alone)
1. Check upstream skill instructions, license, transitive execution and file-write behavior before installation.
2. Identify one *verified* MPE architecture flow from canonical project sources; never infer undocumented integrations.
3. Produce one SVG using Crisp Diagrams and one comparable baseline using existing tooling.
4. Inspect at smartphone viewport, normal desktop, and dark theme. Check contrast, text size, vector rendering, and PNG export.
5. Verify palette reuse from approved MPE branding, `STYLE.md` and retained source prompt; avoid overwriting any existing style file.
6. Compare authoring/update time, diagram fidelity, mobile legibility, output size, reproducibility, and dependency/security burden.
7. Record explicit evidence and a single outcome: ADOPT_WITH_CHANGES / REUSE_COMPONENT / HOLD / REJECT, subject to owner's decision.

## Acceptance
- One accurate, source-grounded, mobile-readable SVG.
- Reproducible style and retained prompt; no silent branding deviation.
- Meaningful improvement over the baseline on at least one measured axis without material regression elsewhere.
- No deep-change, production deploy, credentials, new infrastructure, or automatic adoption.

## Scope and gates
Registration is documentation only. Do not install, execute the skill, modify a production project, merge, or deploy under this registration. If the skill would introduce new dependencies, untrusted scripts, or a fundamental change, require separate MPE scope/security review and the applicable owner approval.
