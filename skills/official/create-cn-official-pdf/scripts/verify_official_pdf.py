#!/usr/bin/env python3
"""Programmatic preflight for PDFs created by create-cn-official-pdf."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--require-no-warnings", action="store_true")
    args = parser.parse_args()

    result: dict[str, object] = {"pdf": str(args.pdf), "errors": [], "warnings": []}
    errors: list[str] = result["errors"]  # type: ignore[assignment]
    warnings: list[str] = result["warnings"]  # type: ignore[assignment]
    reader = PdfReader(str(args.pdf))
    result["page_count"] = len(reader.pages)
    if not reader.pages:
        errors.append("PDF has no pages.")
    expected_w, expected_h = 595.276, 841.890
    fonts: set[str] = set()
    text_chars = 0
    for index, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if abs(width - expected_w) > 0.75 or abs(height - expected_h) > 0.75:
            errors.append(f"Page {index} is not A4: {width:.3f} × {height:.3f} pt")
        text_chars += len((page.extract_text() or "").strip())
        resources = page.get("/Resources") or {}
        font_dict = resources.get("/Font") if hasattr(resources, "get") else None
        if font_dict:
            font_dict = font_dict.get_object()
            for ref in font_dict.values():
                obj = ref.get_object()
                name = obj.get("/BaseFont")
                if name:
                    fonts.add(str(name))
    result["font_resources"] = sorted(fonts)
    result["extracted_text_characters"] = text_chars
    if text_chars == 0:
        errors.append("No searchable text extracted.")

    if args.report:
        layout = json.loads(args.report.read_text(encoding="utf-8"))
        result["layout_report"] = str(args.report)
        if int(layout.get("page_count", -1)) != len(reader.pages):
            errors.append("Layout report page_count does not match PDF.")
        warnings.extend(str(x) for x in layout.get("warnings", []))
    if args.require_no_warnings and warnings:
        errors.append("Warnings remain and --require-no-warnings was requested.")

    result["status"] = "pass" if not errors else "fail"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
