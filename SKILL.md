---
name: ppt-template-collage-builder
description: Analyze a folder of source documents, screenshots, and images using a caller-specified PowerPoint template and caller-specified slide count; then create a polished template-matched PPTX, export every slide as a PNG, assemble a contact-sheet collage, and verify visual and package quality. Use when the user asks to generate or remake a slide deck from uploaded materials, follow a supplied PPT/PPTX style, produce a specified page count, or deliver PPT images in collage form.
---

# PPT Template Collage Builder

Create a complete presentation package from source materials and a supplied template. Treat the template as the visual system, not merely inspiration.

## Required Caller Inputs

Require all three inputs before starting:

- Source material file or folder
- PowerPoint template `.ppt` or `.pptx`
- Exact target slide count

Do not use a built-in template or default slide count. If the template or slide count is missing, ask the caller for it before building the deck.

## Required Deliverables

Produce all of these unless the user explicitly narrows the request:

- One editable `.pptx`
- One PNG for every slide
- One contact-sheet collage containing all slides in reading order
- A short QA result covering slide count, empty images, rendering, and template fidelity

Use the caller's exact requested slide count.

## Workflow

### 1. Confirm and Inspect Inputs

- Confirm the source path, template path, and exact target slide count.
- Recursively inventory the supplied folder.
- Identify the main content sources, the presentation template, and reusable visual assets.
- Extract or inspect source text and images before drafting.
- Render the template to a contact sheet and inspect representative slides at full size.
- Record the template's canvas ratio, typography, color palette, recurring decorations, image treatment, and layout families.

Use the bundled Presentations skill for PPTX manipulation, rendering, and visual QA. Read its template-editing profile when a template is supplied.

### 2. Plan the Narrative

- Build a page-by-page outline before editing slides.
- Organize the deck into a clear progression: cover, agenda, sections, evidence/examples, synthesis, and closing.
- Assign one primary message to each slide.
- Keep content grounded in the supplied files. Clearly label any inference or supplemental knowledge.
- Select the closest template layout for each planned slide.

Read [references/content-and-layout.md](references/content-and-layout.md) when choosing layouts or compressing dense source material.

### 3. Build Template-First

- Clone and edit template slides whenever possible.
- Preserve the template's master, dimensions, fonts, colors, recurring shapes, margins, and footer behavior.
- Replace text and visuals while retaining the original layout hierarchy.
- Reuse multiple template layout families to avoid repetition.
- Keep titles concise and prevent orphaned lines, clipping, overflow, or accidental overlaps.
- Do not add a second visual style that competes with the supplied template.

When the source template has fewer slides than requested, duplicate the most suitable template slides and vary their use intentionally.

### 4. Render and Review

- Export every slide to PNG.
- Generate a contact sheet with slides ordered left-to-right, top-to-bottom.
- Inspect the full contact sheet for narrative rhythm and visual consistency.
- Inspect the cover, section slides, densest slides, chart slides, and closing slide at full size.
- Fix visible issues and rerender. Do not deliver the first render without review.

Read [references/qa-checklist.md](references/qa-checklist.md) before final delivery.

### 5. Validate and Deliver

- Run the Presentations skill's template-fidelity checker when using a supplied template.
- Run `scripts/verify_outputs.py` to verify package completeness.
- Confirm the final slide count, PNG count, nonempty images, readable collage, and openable PPTX.
- Place final artifacts together in a clearly named output directory.
- In the response, embed or link the collage first, then link the editable PPTX and per-slide image directory.

Example verification:

```powershell
python scripts/verify_outputs.py `
  --pptx "output/deck.pptx" `
  --images-dir "output/逐页图片" `
  --collage "output/deck_拼图.png" `
  --expected-slides 20
```

## Quality Bar

- Match the supplied template closely enough that every slide feels native to it.
- Favor legibility and message clarity over filling every available shape.
- Avoid raw source screenshots as final slide backgrounds unless the user requests that treatment.
- Avoid fabricated citations, statistics, or claims.
- Never omit the editable PPTX when the user asks for PPT images; provide both unless explicitly told otherwise.
