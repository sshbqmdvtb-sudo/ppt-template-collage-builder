#!/usr/bin/env python3
"""Verify a PPTX, its per-slide PNG exports, and a collage image."""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SLIDE_PATTERN = re.compile(r"^ppt/slides/slide\d+\.xml$")


def count_pptx_slides(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return sum(1 for name in archive.namelist() if SLIDE_PATTERN.match(name))


def valid_png(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size <= len(PNG_SIGNATURE):
        return False
    with path.open("rb") as stream:
        return stream.read(len(PNG_SIGNATURE)) == PNG_SIGNATURE


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pptx", required=True, type=Path)
    parser.add_argument("--images-dir", required=True, type=Path)
    parser.add_argument("--collage", required=True, type=Path)
    parser.add_argument("--expected-slides", required=True, type=int)
    args = parser.parse_args()

    issues = []
    slide_count = 0
    if not args.pptx.is_file():
        issues.append(f"Missing PPTX: {args.pptx}")
    else:
        try:
            slide_count = count_pptx_slides(args.pptx)
        except zipfile.BadZipFile:
            issues.append(f"Invalid PPTX archive: {args.pptx}")

    images = sorted(args.images_dir.glob("*.png")) if args.images_dir.is_dir() else []
    invalid_images = [str(path) for path in images if not valid_png(path)]

    if slide_count != args.expected_slides:
        issues.append(f"PPTX has {slide_count} slides; expected {args.expected_slides}")
    if len(images) != args.expected_slides:
        issues.append(f"Found {len(images)} slide PNGs; expected {args.expected_slides}")
    if invalid_images:
        issues.append(f"Invalid slide PNGs: {len(invalid_images)}")
    if not valid_png(args.collage):
        issues.append(f"Missing or invalid collage PNG: {args.collage}")

    result = {
        "status": "pass" if not issues else "fail",
        "pptx": str(args.pptx),
        "slideCount": slide_count,
        "imageCount": len(images),
        "invalidImageCount": len(invalid_images),
        "collage": str(args.collage),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
