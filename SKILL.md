---
name: ppt-template-collage-builder
description: Create a Word presentation outline from caller requirements and source files using a caller-specified PowerPoint template and slide count, generate one canonical slide-design image per requested slide, decompose every design image into editable PowerPoint elements and reusable PNG assets, reconstruct each image as one editable PPT slide, and verify visual fidelity by comparing final slide renders with the canonical images. Use when the user requests an image-first PPT workflow, editable reconstruction from slide images, template-guided report decks, or delivery of both slide images and a fully editable PPTX.
---

# Image-First Editable PPT Builder

Build a presentation through an image-first design and editable-reconstruction workflow. The canonical design images define the intended appearance; the final PPTX must reconstruct them with editable elements wherever technically possible.

## Required Caller Inputs

Confirm these inputs before starting:

- Source requirements and source files or folders
- Caller-specified PPT/PPTX template
- Caller-specified exact target slide count

Do not use a built-in template or default slide count. If the caller supplies reference slide images for reconstruction, one original image must map to exactly one final PPT slide. The final slide count must equal the number of original images. Ask before proceeding when the caller-specified slide count conflicts with the image count.

## Required Deliverables

Produce all of these unless the caller explicitly narrows the request:

- A Word `.docx` presentation outline
- One canonical design PNG for every slide
- One contact-sheet collage of the canonical design images
- A folder of extracted and reusable PNG visual assets
- A reconstruction manifest describing every slide and element
- One fully editable `.pptx`
- One final rendered PNG for every reconstructed PPT slide
- A fidelity and package QA report

## Editability Contract

Reconstruct elements according to their semantic type:

- Text, titles, labels, captions, and numbers: native editable text boxes
- Tables: native editable PowerPoint tables
- Charts: native editable charts when practical; otherwise editable shapes and text
- Diagrams, cards, lines, connectors, and backgrounds: native editable shapes
- Mathematical formulas: native editable Office equations when supported; otherwise editable text/shapes with the formula source recorded in the manifest. Do not silently rasterize a formula.
- Photos, screenshots, paintings, textures, and complex illustrations: extracted PNG image objects that remain movable, replaceable, resizable, and croppable

Never satisfy the editable-PPT requirement by placing one flattened full-slide image on each slide. A complex raster asset may remain a picture, but surrounding text, tables, shapes, formulas, and layout structure must be reconstructed separately.

Read [references/editability-and-fidelity.md](references/editability-and-fidelity.md) before decomposition and reconstruction.

## Workflow

### 1. Inspect Requirements and Sources

- Inventory all supplied files recursively.
- Extract and inspect source text, tables, images, formulas, and citations.
- When a template is supplied, render and inspect it; record its dimensions, fonts, colors, margins, decorations, image treatment, and layout families.
- Record unresolved source gaps and do not invent unsupported facts.

Use the bundled Documents skill for DOCX creation and the bundled Presentations skill for PPTX creation, rendering, template handling, and visual QA.

### 2. Create the Word Outline

Create a polished `.docx` outline before designing slide images. The outline must include:

- Audience, objective, requested slide count, and visual direction
- Overall narrative and section structure
- One entry per planned slide
- For each slide: slide number, claim/title, purpose, key content, source, visual composition, and planned editable element types

Render the DOCX to page images, inspect every page, and revise until clean. The outline is a production specification for the design and reconstruction stages.

Read [references/content-and-layout.md](references/content-and-layout.md) for outline and slide-planning rules.

### 3. Generate Canonical Slide Images

- Generate exactly one canonical high-resolution PNG per planned slide.
- Follow the caller's style requirements and supplied template.
- Preserve known text separately in the outline or manifest; do not rely only on OCR to recover generated text.
- Keep visual assets sufficiently separated and clear to support later extraction.
- Assemble the canonical images into a contact sheet and inspect the full deck rhythm.
- Fix design issues before reconstruction. Treat approved canonical images as immutable visual references unless a later correction is documented.
- Present the canonical images to the caller as a user-facing stage deliverable. If the caller requested a review checkpoint, wait for approval before reconstruction; otherwise continue the end-to-end workflow after internal visual review.

Canonical images may be produced through reference-image generation, layout rendering, or a draft visual composition. They are design specifications, not the final editable deck.

### 4. Decompose Every Canonical Image

For each canonical image, create a slide-level element inventory:

- Identify text boxes, tables, charts, formulas, shapes, backgrounds, and raster visual assets.
- Transcribe text and formulas from the known content source; use OCR only as a secondary check.
- Extract photos, screenshots, illustrations, textures, and other raster-only visuals as separate transparent or cropped PNG assets.
- Record element type, content/source, bounds, z-order, editability mode, and reconstruction notes in `reconstruction-manifest.json`.
- Record any element that cannot be made natively editable and explain why.

One canonical image must always map to one manifest slide entry and one final PPT slide.

Read [references/reconstruction-manifest.md](references/reconstruction-manifest.md) for the manifest schema.

### 5. Reconstruct the Editable PPT

- Create one PPT slide for each canonical image, in the same order.
- Use the supplied template as the editable starting point when one exists.
- Rebuild text, tables, charts, formulas, shapes, and connectors as editable PowerPoint objects.
- Place extracted PNG assets back at the correct position, size, crop, rotation, and z-order.
- Match the canonical image's canvas, spacing, typography, colors, line breaks, geometry, and visual hierarchy.
- Keep all meaningful objects separate and human-editable.
- Name or otherwise identify elements consistently when the authoring surface supports it.

### 6. Render, Compare, and Iterate

- Render every reconstructed PPT slide to PNG.
- Compare each final render with its corresponding canonical image.
- Inspect every pair at full size, not only the contact sheet.
- Correct differences in text, font, line breaks, bounds, crop, color, alignment, z-order, and spacing.
- Continue until the final render visually restores the canonical image, allowing only minor renderer or anti-aliasing differences.
- Run `scripts/compare_renders.py` for measurable comparison and record accepted differences.

Read [references/qa-checklist.md](references/qa-checklist.md) before delivery.

### 7. Validate and Deliver

Run:

```powershell
$expectedSlides = [int](Read-Host "Enter the caller-specified target slide count")
python scripts/verify_outputs.py `
  --outline-docx "output/汇报大纲.docx" `
  --reference-images-dir "output/设计效果图" `
  --assets-dir "output/提取素材" `
  --pptx "output/可编辑汇报.pptx" `
  --images-dir "output/PPT最终渲染图" `
  --collage "output/设计效果图_拼图.png" `
  --manifest "output/reconstruction-manifest.json" `
  --expected-slides $expectedSlides
```

Confirm:

- Outline DOCX is valid and visually reviewed
- Canonical image count, manifest slide count, PPT slide count, and final-render count all match
- Extracted raster assets exist and match manifest entries
- No slide is delivered as one flattened full-slide picture
- Each canonical image maps to exactly one editable PPT slide
- Visual differences have been reviewed and documented

## Blocking Failures

Do not deliver when any of these remain:

- Word outline is missing or was not rendered and reviewed
- Canonical image count does not match final PPT slide count
- A final slide is only a flattened screenshot of the canonical image
- Text is rasterized when it could be an editable text box
- A table is rasterized when it could be a native table
- A formula is rasterized without explicit caller approval
- Extracted PNG assets are missing, distorted, incorrectly cropped, or misplaced
- Final render visibly differs from the canonical image in structure, content, or layout
- Text is clipped, overflowing, incorrectly transcribed, or layered incorrectly
