# Final QA Checklist

## Outline

- Word outline exists, opens, and has been rendered to images.
- Every outline page was visually inspected.
- Outline slide entries match the requested slide count.
- Each slide entry records content, source, visual plan, and editable element plan.

## Package

- Canonical design PNG count matches the requested slide count.
- Reconstruction manifest slide count matches.
- Editable PPTX slide count matches.
- Final-render PNG count matches.
- No PNG is empty or corrupt.
- Canonical-image collage exists and preserves slide order.
- Extracted raster assets are present and reusable.

## Editability

- No slide consists only of one flattened full-slide image.
- Text is editable text, not baked into a background image.
- Tables are native editable tables when feasible.
- Charts and diagrams use native objects or editable primitives.
- Formulas remain editable or have an explicitly approved and documented exception.
- Photos and complex visuals are separate movable/croppable PNG objects.

## Per-Slide Fidelity

Compare every canonical image against its final PPT render:

- Same content and element count
- Same visual hierarchy and reading order
- Matching position, size, crop, rotation, and z-order
- Matching typography, line breaks, alignment, and color
- No clipping, overflow, overlaps, missing glyphs, or transcription errors
- No distorted, low-resolution, or incorrectly extracted images

## Template Review

When a template is supplied:

- Canvas size, fonts, colors, decorations, margins, and footer behavior match.
- Reconstructed slides feel native to the template.
- Added objects do not introduce a conflicting visual language.
