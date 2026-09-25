---
name: mpe-logo-creation
version: 1.0.0
description: Create product logos for the Murat Project Engineer ecosystem through a repeatable meaning-first workflow: product meaning, associations, numbered visual elements, owner selection, visual story, core mark, pseudo-3D family language, simplification, small-scale testing, variants, and canonical asset storage.
---

# MPE Logo Creation

Create logos as explainable product symbols, not decorative marks.

This skill is for product logos inside the Murat Project Engineer ecosystem. It reuses the visual and decision pattern validated on MPE and Business Discovery.

## Trigger

Use this skill when the owner asks to:

- create a logo for an existing MPE product;
- redesign or refine an existing product logo;
- create favicon / compact / horizontal logo variants;
- derive a product mark from product meaning;
- build a coherent logo family across MPE products.

Do not create a new repository for logo work. Prefer the product's existing repository and its `assets` branch or established asset location.

## Core principle

Use this sequence:

```text
Product
→ Meanings
→ Associations
→ Numbered Elements
→ Owner Selection
→ Visual Story
→ Core Mark
→ Pseudo-3D Family Language
→ Simplify
→ Small-Scale Test
→ Variants
→ Assets
```

The logo must be explainable in plain language:

1. what the product is;
2. what each visible element means;
3. what result the product creates.

If an element has no clear semantic role, remove it.

## 1. Understand the product first

Before generating visuals, summarize the product in 1–3 short sentences.

Answer:

- What does the product do?
- For whom?
- What process does it perform?
- What result does the user receive?
- What is the strongest differentiator?

Do not start with initials, colors, or icon generation.

## 2. Extract key meanings

Choose 3–7 important meanings from the product description.

Examples:

- business;
- interview;
- analysis;
- discovery;
- change;
- result.

Prefer nouns and actions that can become recognizable visual metaphors.

## 3. Build associations

For every key meaning, generate concrete visual associations.

Example:

```text
Business
- office building
- structure
- blocks
- chart

Interview
- microphone
- dialogue
- speech wave

Analysis
- bar chart
- matrix
- data blocks

Discovery
- magnifier
- focus
- highlight
- found point
```

Avoid generic decorative elements unless they directly support meaning.

## 4. Produce a numbered element catalog

Combine all viable visual elements into one numbered list.

The owner must be able to answer using only numbers, for example:

```text
Use 1, 4, 7, 12.
```

Do not jump directly to many full logo concepts before this selection step.

The list should be broad enough to choose from, but concise enough to scan.

## 5. Wait for owner selection when material

When element choice materially changes the logo concept, present the numbered options and let the owner choose.

Do not silently pick a large semantic direction on the owner's behalf when multiple materially different directions remain.

Minor composition details can be resolved autonomously.

## 6. Convert elements into a visual story

Selected elements should form one understandable structure.

Preferred patterns:

### Process story

```text
input → action → analysis → discovery → result
```

Example for Business Discovery:

```text
company → interview → analysis → discovery → highlighted module
```

### Core + orbit

Use when the product has a strong central identity and a surrounding workflow.

### Problem → transformation → result

Use when change itself is the key product meaning.

Do not place unrelated icons around a logo only for decoration.

## 7. Define the core mark

Every product needs one recognizable core that can survive after all secondary detail is removed.

Possible cores:

- initials / monogram;
- one geometric symbol;
- one transformed object;
- letters integrated into the product metaphor.

Examples already validated:

- MPE: M, P and E each occupy one ascending pseudo-3D step.
- Business Discovery: BD is the central core; the process story lives around it.

The core mark must work independently from the full story composition.

## 8. Use the MPE family visual language

Default family language for core MPE products:

- pseudo-3D;
- simple geometric forms;
- light and dark compatibility;
- cool blue palette;
- restrained gradients;
- clean background;
- soft depth / shadow;
- high silhouette clarity;
- minimal decorative detail.

The products should feel related, but not identical.

Do not force pseudo-3D when it harms small-size recognition.

## 9. Simplify after the first strong concept

The first generated concept is a draft, not the final logo.

Run a simplification pass:

- remove non-semantic detail;
- enlarge important shapes;
- reduce tiny edges and facets;
- strengthen contrast;
- simplify shadows;
- simplify orbit/process elements;
- remove anything that disappears at favicon scale.

Priority:

```text
recognition > decoration
```

## 10. Run the small-scale test

Never approve only from a large presentation image.

Check at minimum:

- 16×16;
- 32×32;
- 48×48;
- browser tab / favicon context;
- mobile navigation context.

Questions:

- Is the core still recognizable?
- Do letters remain readable?
- Do secondary elements turn into noise?
- Does the light version disappear on white UI?
- Does the dark version lose internal contrast?

If the full logo fails, create a dedicated compact mark.

## 11. Create the minimum useful variant set

Create only variants that have a real use.

Preferred set:

### Primary Logo
Full composition.

### Compact Mark
Core mark without long text or secondary narrative.

### Favicon
Simplified small-scale source.

### Horizontal Lockup
Mark + product name.

### Light Version
For light surfaces.

### Dark Version
For dark surfaces.

Do not create unnecessary variants just to complete a template.

## 12. Preserve owner-approved meaning

Once the owner approves a concept, treat its meaning and composition as canonical.

For example, if the approved Business Discovery sequence is:

```text
office building
→ microphone
→ three-step analysis chart
→ magnifier
→ highlighted module
```

do not later replace the highlighted module with a gear because it looks attractive.

Meaning takes precedence over decorative novelty.

## 13. Save approved assets into the existing product repository

After approval, convert the concept from a chat image into usable product assets.

Preferred repository pattern:

```text
assets/<product>/
  <product>-mark-light.svg
  <product>-mark-dark.svg        # when needed
  <product>-logo-horizontal.svg  # when needed
  README.md
```

Use the product's existing repository.

Prefer a dedicated `assets` branch when that pattern already exists for the product.

The README should record:

- approved concept;
- meaning of each element;
- canonical sequence/composition;
- preferred background treatment;
- small-scale rules;
- prohibited semantic substitutions;
- intended use of each file.

Do not merge or deploy unless the owner or repository workflow already grants that authority.

## 14. Separate presentation art from production assets

Generated presentation images are useful for exploration and approval.

Production assets should be recreated or exported as clean scalable assets, preferably SVG where appropriate.

Do not treat a large generated PNG mockup as the only source of truth for a website logo.

## 15. Reference examples

### MPE

Meaning:

- project / engineering / growth;
- three ascending steps;
- one letter per step: M → P → E.

Rules:

- letters remain separate;
- pseudo-3D is simple;
- light compact version is preferred for browser/favicon use;
- no unnecessary graphic elements.

### Business Discovery

Meaning sequence:

1. office building = company/business;
2. microphone = interview;
3. three-step chart = analysis;
4. magnifier = discovery;
5. highlighted module = identified key point / result.

Core:

- central BD mark.

Rules:

- orbit/process elements must stay simplified;
- highlighted module is the canonical result element;
- do not substitute a gear without an explicit redesign decision.

## Completion

A logo task is complete when:

- product meaning is explicit;
- chosen visual elements are explicit;
- owner-approved composition is captured;
- small-scale usability is considered;
- required variants exist;
- canonical assets are stored in the product repository;
- the asset README records the meaning and usage rules.

Keep the final handoff concise: concept, files, branch, and any unresolved item.
