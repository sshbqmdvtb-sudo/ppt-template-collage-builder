#!/usr/bin/env python3
"""Compare canonical slide images with final PPT renders."""

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


def compare(reference: Path, final: Path):
    with Image.open(reference).convert("RGB") as ref, Image.open(final).convert("RGB") as out:
        if ref.size != out.size:
            return {"sizeMatch": False, "referenceSize": ref.size, "finalSize": out.size}
        diff = ImageChops.difference(ref, out)
        stat = ImageStat.Stat(diff)
        rmse = math.sqrt(sum(value * value for value in stat.rms) / len(stat.rms))
        bbox = diff.getbbox()
        return {
            "sizeMatch": True,
            "referenceSize": ref.size,
            "finalSize": out.size,
            "rmse": round(rmse, 4),
            "identical": bbox is None,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference-images-dir", required=True, type=Path)
    parser.add_argument("--final-images-dir", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    references = sorted(args.reference_images_dir.glob("*.png"))
    finals = sorted(args.final_images_dir.glob("*.png"))
    issues = []
    if len(references) != len(finals):
        issues.append(
            f"Image count mismatch: {len(references)} references vs {len(finals)} final renders"
        )

    comparisons = []
    for index, (reference, final) in enumerate(zip(references, finals), start=1):
        metrics = compare(reference, final)
        metrics.update({"slide": index, "reference": str(reference), "final": str(final)})
        if not metrics["sizeMatch"]:
            issues.append(f"Slide {index} dimensions do not match")
        comparisons.append(metrics)

    result = {
        "status": "pass" if not issues else "fail",
        "comparisons": comparisons,
        "issues": issues,
        "note": "RMSE is diagnostic only; every slide pair still requires full-size visual review.",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    print(text)
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
