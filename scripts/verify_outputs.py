#!/usr/bin/env python3
"""Verify image-first editable PPT workflow deliverables."""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SLIDE_PATTERN = re.compile(r"^ppt/slides/slide(\d+)\.xml$")
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}


def valid_png(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size <= len(PNG_SIGNATURE):
        return False
    with path.open("rb") as stream:
        return stream.read(len(PNG_SIGNATURE)) == PNG_SIGNATURE


def valid_office_package(path: Path, required_member: str) -> bool:
    if not path.is_file():
        return False
    try:
        with zipfile.ZipFile(path) as archive:
            return required_member in archive.namelist()
    except zipfile.BadZipFile:
        return False


def inspect_pptx(path: Path):
    slides = []
    with zipfile.ZipFile(path) as archive:
        names = sorted(
            (
                (int(match.group(1)), name)
                for name in archive.namelist()
                if (match := SLIDE_PATTERN.match(name))
            ),
            key=lambda item: item[0],
        )
        for slide_number, name in names:
            root = ElementTree.fromstring(archive.read(name))
            counts = {
                "slide": slide_number,
                "shapes": len(root.findall(".//p:sp", NS)),
                "pictures": len(root.findall(".//p:pic", NS)),
                "tables": len(root.findall(".//a:tbl", NS)),
                "charts": len(root.findall(".//c:chart", NS)),
                "formulas": len(root.findall(".//m:oMath", NS)),
            }
            counts["flattenedOnly"] = (
                counts["pictures"] == 1
                and counts["shapes"] == 0
                and counts["tables"] == 0
                and counts["charts"] == 0
                and counts["formulas"] == 0
            )
            slides.append(counts)
    return slides


def load_manifest(path: Path):
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outline-docx", required=True, type=Path)
    parser.add_argument("--reference-images-dir", required=True, type=Path)
    parser.add_argument("--assets-dir", required=True, type=Path)
    parser.add_argument("--pptx", required=True, type=Path)
    parser.add_argument("--images-dir", required=True, type=Path)
    parser.add_argument("--collage", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--expected-slides", required=True, type=int)
    args = parser.parse_args()

    issues = []
    if not valid_office_package(args.outline_docx, "word/document.xml"):
        issues.append(f"Missing or invalid outline DOCX: {args.outline_docx}")

    reference_images = (
        sorted(args.reference_images_dir.glob("*.png"))
        if args.reference_images_dir.is_dir()
        else []
    )
    final_images = (
        sorted(args.images_dir.glob("*.png")) if args.images_dir.is_dir() else []
    )
    invalid_reference_images = [
        str(path) for path in reference_images if not valid_png(path)
    ]
    invalid_final_images = [str(path) for path in final_images if not valid_png(path)]
    assets = sorted(args.assets_dir.rglob("*.png")) if args.assets_dir.is_dir() else []
    invalid_assets = [str(path) for path in assets if not valid_png(path)]
    if not args.assets_dir.is_dir():
        issues.append(f"Missing extracted-assets directory: {args.assets_dir}")
    if invalid_assets:
        issues.append(f"Invalid extracted PNG assets: {len(invalid_assets)}")

    ppt_slides = []
    if not valid_office_package(args.pptx, "ppt/presentation.xml"):
        issues.append(f"Missing or invalid PPTX: {args.pptx}")
    else:
        ppt_slides = inspect_pptx(args.pptx)

    manifest = load_manifest(args.manifest)
    manifest_slides = manifest.get("slides", []) if manifest else []
    manifest_count = manifest.get("slideCount") if manifest else None

    counts = {
        "canonicalImages": len(reference_images),
        "manifestSlides": len(manifest_slides) if isinstance(manifest_slides, list) else 0,
        "pptSlides": len(ppt_slides),
        "finalRenders": len(final_images),
    }
    for label, count in counts.items():
        if count != args.expected_slides:
            issues.append(f"{label} count is {count}; expected {args.expected_slides}")

    if manifest_count != args.expected_slides:
        issues.append(
            f"Manifest slideCount is {manifest_count}; expected {args.expected_slides}"
        )
    if invalid_reference_images:
        issues.append(f"Invalid canonical slide PNGs: {len(invalid_reference_images)}")
    if invalid_final_images:
        issues.append(f"Invalid final-render PNGs: {len(invalid_final_images)}")
    if not valid_png(args.collage):
        issues.append(f"Missing or invalid collage PNG: {args.collage}")

    flattened_slides = [slide["slide"] for slide in ppt_slides if slide["flattenedOnly"]]
    if flattened_slides:
        issues.append(
            "Slides delivered as one flattened full-slide image: "
            + ", ".join(map(str, flattened_slides))
        )

    if isinstance(manifest_slides, list):
        slide_numbers = [entry.get("slide") for entry in manifest_slides if isinstance(entry, dict)]
        expected_numbers = list(range(1, args.expected_slides + 1))
        if (
            not all(isinstance(number, int) for number in slide_numbers)
            or sorted(slide_numbers) != expected_numbers
        ):
            issues.append("Manifest slide numbers are missing, duplicated, or out of range")
        manifest_reference_paths = []
        manifest_final_paths = []
        for entry in manifest_slides:
            if not isinstance(entry, dict):
                issues.append("Manifest contains a non-object slide entry")
                continue
            if not entry.get("referenceImage") or not entry.get("finalRender"):
                issues.append(
                    f"Manifest slide {entry.get('slide')} lacks referenceImage or finalRender"
                )
            else:
                reference_path = args.manifest.parent / entry["referenceImage"]
                final_path = args.manifest.parent / entry["finalRender"]
                manifest_reference_paths.append(str(reference_path.resolve()))
                manifest_final_paths.append(str(final_path.resolve()))
                if not valid_png(reference_path):
                    issues.append(
                        f"Manifest slide {entry.get('slide')} references a missing canonical image"
                    )
                if not valid_png(final_path):
                    issues.append(
                        f"Manifest slide {entry.get('slide')} references a missing final render"
                    )
            if not isinstance(entry.get("elements"), list) or not entry.get("elements"):
                issues.append(f"Manifest slide {entry.get('slide')} has no element inventory")
                continue
            for element in entry["elements"]:
                if not isinstance(element, dict):
                    issues.append(
                        f"Manifest slide {entry.get('slide')} contains a non-object element"
                    )
                    continue
                element_type = element.get("type")
                editability = element.get("editability")
                if element_type not in {
                    "text",
                    "image",
                    "table",
                    "chart",
                    "formula",
                    "shape",
                    "connector",
                    "diagram",
                }:
                    issues.append(
                        f"Manifest slide {entry.get('slide')} has unsupported element type: {element_type}"
                    )
                if editability not in {"native", "editable-primitives", "raster-asset"}:
                    issues.append(
                        f"Manifest slide {entry.get('slide')} has unsupported editability: {editability}"
                    )
                if element_type in {"text", "table", "formula"} and editability == "raster-asset":
                    issues.append(
                        f"Manifest slide {entry.get('slide')} rasterizes editable {element_type}"
                    )
                if editability == "raster-asset":
                    asset = element.get("asset")
                    asset_path = args.manifest.parent / asset if asset else None
                    if not asset_path or not valid_png(asset_path):
                        issues.append(
                            f"Manifest slide {entry.get('slide')} has missing raster asset: {asset}"
                        )
        if len(set(manifest_reference_paths)) != len(manifest_reference_paths):
            issues.append("Multiple manifest slides reference the same canonical image")
        if len(set(manifest_final_paths)) != len(manifest_final_paths):
            issues.append("Multiple manifest slides reference the same final render")

    result = {
        "status": "pass" if not issues else "fail",
        "outlineDocx": str(args.outline_docx),
        "pptx": str(args.pptx),
        "assetsDir": str(args.assets_dir),
        "assetCount": len(assets),
        "expectedSlides": args.expected_slides,
        "counts": counts,
        "flattenedSlides": flattened_slides,
        "pptElementCounts": ppt_slides,
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
