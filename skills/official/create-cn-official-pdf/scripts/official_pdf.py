#!/usr/bin/env python3
"""Public entry point for the official-document PDF generator."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import _official_pdf_impl as impl


def render_pdf(pdf: Path, render_dir: Path, warnings: list[str]) -> list[str]:
    render_dir.mkdir(parents=True, exist_ok=True)
    prefix = render_dir / pdf.stem
    bundled = Path(sys.executable).resolve().parent.parent / "native" / "poppler" / "Library" / "bin" / "pdftoppm.exe"
    candidates = [str(bundled)] if bundled.is_file() else []
    on_path = shutil.which("pdftoppm") or shutil.which("pdftoppm.exe")
    if on_path and on_path not in candidates:
        candidates.append(on_path)
    for executable in candidates:
        try:
            subprocess.run([executable, "-png", "-r", "180", str(pdf), str(prefix)], check=True)
            rendered = [str(path) for path in sorted(render_dir.glob(f"{pdf.stem}-*.png"))]
            if rendered:
                return rendered
        except (OSError, subprocess.CalledProcessError) as exc:
            warnings.append(f"pdftoppm candidate failed ({executable}): {exc}")
    try:
        import fitz  # type: ignore

        document = fitz.open(pdf)
        matrix = fitz.Matrix(2.5, 2.5)
        rendered = []
        for index, page in enumerate(document, start=1):
            path = render_dir / f"{pdf.stem}-{index}.png"
            page.get_pixmap(matrix=matrix, alpha=False).save(path)
            rendered.append(str(path))
        return rendered
    except Exception as exc:
        warnings.append(f"PDF rendering unavailable (pdftoppm/PyMuPDF): {exc}")
        return []


def draw_edition_record(self: impl.OfficialPDF) -> None:
    copy_to = impl.normalize_text(self.data.get("copy_to"))
    printing_authority = impl.normalize_text(self.data.get("printing_authority"))
    printing_date = impl.normalize_text(self.data.get("printing_date"))
    if not any([copy_to, printing_authority, printing_date]):
        return
    if self.format == "letter":
        if copy_to:
            y = 25 * impl.mm
            self.canvas.setFont("CNBody", impl.RECORD_SIZE)
            self.canvas.drawString(impl.LEFT + impl.CELL, y, "抄送：" + copy_to.rstrip("。") + "。")
        return
    needed = 3 if copy_to else 2
    if self.y < impl.BOTTOM + needed * impl.LINE + 6:
        self.finish_page()
        self.y = impl.TOP - impl.BODY_SIZE
        self.warnings.append("Edition record moved to a new final side because remaining space was insufficient.")

    lower_rule = impl.BOTTOM
    print_top = lower_rule + impl.LINE
    copy_top = lower_rule + 2 * impl.LINE if copy_to else None
    text_lift = 7.5
    print_y = lower_rule + text_lift
    copy_y = print_top + text_lift if copy_to else None

    self.canvas.setStrokeColor(impl.BLACK)
    self.canvas.setFillColor(impl.BLACK)
    self.canvas.setLineWidth(1.0)
    self.canvas.line(impl.LEFT, copy_top or print_top, impl.RIGHT, copy_top or print_top)
    self.canvas.setFont("CNBody", impl.RECORD_SIZE)
    if copy_to and copy_y is not None:
        self.canvas.drawString(impl.LEFT + impl.CELL, copy_y, "抄送：" + copy_to.rstrip("。") + "。")
        self.canvas.setLineWidth(0.7)
        self.canvas.line(impl.LEFT, print_top, impl.RIGHT, print_top)
    self.canvas.drawString(impl.LEFT + impl.CELL, print_y, printing_authority)
    right_text = (printing_date + "印发") if printing_date and not printing_date.endswith("印发") else printing_date
    right_width = impl.pdfmetrics.stringWidth(right_text, "CNBody", impl.RECORD_SIZE)
    self.canvas.drawString(impl.RIGHT - impl.CELL - right_width, print_y, right_text)
    self.canvas.setLineWidth(1.0)
    self.canvas.line(impl.LEFT, lower_rule, impl.RIGHT, lower_rule)


impl.render_pdf = render_pdf
impl.OfficialPDF.draw_edition_record = draw_edition_record


if __name__ == "__main__":
    raise SystemExit(impl.main())
