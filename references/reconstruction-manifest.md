# Reconstruction Manifest

Create `reconstruction-manifest.json` so every canonical image and reconstructed slide can be audited.

Minimum schema:

```json
{
  "slideCount": 2,
  "slides": [
    {
      "slide": 1,
      "referenceImage": "设计效果图/第01页.png",
      "finalRender": "PPT最终渲染图/第01页.png",
      "elements": [
        {
          "id": "title",
          "type": "text",
          "editability": "native",
          "content": "标题文字",
          "bounds": [120, 80, 900, 100],
          "zOrder": 5
        },
        {
          "id": "hero-image",
          "type": "image",
          "editability": "raster-asset",
          "asset": "assets/slide-01-hero.png",
          "bounds": [720, 180, 420, 360],
          "zOrder": 2
        }
      ],
      "exceptions": []
    }
  ]
}
```

Rules:

- `slideCount` must match the number of canonical images and PPT slides.
- Every slide number must appear exactly once.
- Every slide must reference its canonical image and final render.
- Every visible meaningful element must have an entry.
- `type` should be one of `text`, `image`, `table`, `chart`, `formula`, `shape`, `connector`, or `diagram`.
- `editability` should be `native`, `editable-primitives`, or `raster-asset`.
- Record formula source, chart data source, or asset path when applicable.
- Put unavoidable reconstruction limitations in `exceptions`.
