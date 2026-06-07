# Editability and Fidelity Rules

## Editable Reconstruction Hierarchy

Use the highest feasible editability level:

1. Native PowerPoint object: text box, table, chart, shape, connector, or Office equation
2. Editable primitive reconstruction: grouped shapes, lines, and text labels
3. Separate PNG asset: photos, screenshots, textures, complex illustrations, or visuals that cannot be reliably reconstructed
4. Flattened full-slide image: forbidden

An image object is editable as an object: a human can move, resize, crop, replace, rotate, or delete it. The internal pixels of a photo or illustration are not expected to become individually editable.

## Element Rules

- Text: preserve exact wording, font hierarchy, line breaks, alignment, color, and bounds.
- Tables: reconstruct cells, values, borders, fills, merged regions, widths, and heights.
- Charts: preserve the data and labels; use a native chart or editable shape-based chart.
- Formulas: preserve editable formula source. Prefer Office equations. If unavailable, use editable text/shapes and record the source. Ask before using a raster formula.
- Diagrams: reconstruct nodes and connectors separately; preserve attachment and z-order.
- Raster visuals: extract at the highest available resolution and retain transparent backgrounds when appropriate.

## Visual Fidelity

The canonical slide image is the visual reference for the corresponding final slide.

Compare:

- Canvas size and aspect ratio
- Content and transcription
- Position, size, rotation, crop, and z-order
- Typography, line breaks, and alignment
- Colors, borders, shadows, and transparency
- Table geometry and chart labeling
- Image quality and background treatment

Minor renderer, font rasterization, and anti-aliasing differences are acceptable. Structural differences, missing elements, changed content, wrong crops, and obvious layout drift are not.

## Honest Limitations

Do not claim pixel-perfect semantic reconstruction of arbitrary raster artwork. When an element cannot be decomposed without damaging its appearance, preserve it as a separate PNG asset and document the limitation in the reconstruction manifest.
