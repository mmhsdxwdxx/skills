#!/usr/bin/env python3
"""Generate standards-oriented Chinese Party/government official-document PDFs.

Input is UTF-8 JSON. This is a deterministic layout baseline for GB/T 9704-2012;
an issuing authority's valid template and supplied red-head/seal assets take priority.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PAGE_W, PAGE_H = A4
LEFT = 28 * mm
TOP = PAGE_H - 37 * mm
TYPE_W = 156 * mm
TYPE_H = 225 * mm
RIGHT = LEFT + TYPE_W
BOTTOM = TOP - TYPE_H
CELL = TYPE_W / 28.0
LINE = 29.0  # Engineering default; validate 22-line realization visually.
RED = colors.Color(0.92, 0.0, 0.0)
BLACK = colors.black
BODY_SIZE = 16.0
TITLE_SIZE = 22.0
RECORD_SIZE = 14.0
PAGE_NO_SIZE = 14.0

CLOSING_PUNCT = set("，。；：？！、）】》〉’”％‰℃…")
OPENING_PUNCT = set("（【《〈‘“")


def fullwidth_units(ch: str) -> float:
    if ch == "\t":
        return 2.0
    if ch.isspace():
        return 0.5
    return 1.0 if unicodedata.east_asian_width(ch) in {"W", "F", "A"} else 0.5


def normalize_text(value: Any) -> str:
    return str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def wrap_cells(text: str, capacity: float = 28.0, first_indent: float = 0.0) -> list[tuple[str, float]]:
    text = normalize_text(text).replace("\n", "")
    if not text:
        return []
    lines: list[tuple[str, float]] = []
    current = ""
    used = first_indent
    indent = first_indent
    for ch in text:
        width = fullwidth_units(ch)
        if current and used + width > capacity:
            lines.append((current, indent))
            current = ""
            used = 0.0
            indent = 0.0
        current += ch
        used += width
    if current:
        lines.append((current, indent))

    # Basic Chinese line-breaking cleanup without silently rewriting content.
    for i in range(1, len(lines)):
        txt, ind = lines[i]
        if txt and txt[0] in CLOSING_PUNCT:
            prev, prev_ind = lines[i - 1]
            lines[i - 1] = (prev + txt[0], prev_ind)
            lines[i] = (txt[1:], ind)
        prev, prev_ind = lines[i - 1]
        if prev and prev[-1] in OPENING_PUNCT and len(prev) > 1:
            lines[i - 1] = (prev[:-1], prev_ind)
            lines[i] = (prev[-1] + lines[i][0], lines[i][1])
    return [(t, i) for t, i in lines if t]


def split_title(text: str, font_name: str, size: float) -> list[str]:
    text = normalize_text(text).replace("\n", "")
    if not text:
        return []
    lines: list[str] = []
    current = ""
    for ch in text:
        candidate = current + ch
        if current and pdfmetrics.stringWidth(candidate, font_name, size) > TYPE_W:
            lines.append(current)
            current = ch
        else:
            current = candidate
    if current:
        lines.append(current)
    if len(lines) > 1 and len(lines[-1]) == 1:
        lines[-1] = lines[-2][-1] + lines[-1]
        lines[-2] = lines[-2][:-1]
    return [x for x in lines if x]


class FontBook:
    def __init__(self, overrides: dict[str, str] | None, strict: bool):
        self.overrides = overrides or {}
        self.strict = strict
        self.paths: dict[str, str] = {}
        self.warnings: list[str] = []
        self._register_all()

    def _pick(self, role: str, candidates: list[str], exact_title: bool = False) -> str:
        override = self.overrides.get(role)
        if override:
            path = Path(os.path.expandvars(os.path.expanduser(override))).resolve()
            if not path.is_file():
                raise FileNotFoundError(f"Font override for {role} not found: {path}")
            return str(path)
        for candidate in candidates:
            path = Path(os.path.expandvars(candidate))
            if path.is_file():
                if exact_title and "xbs" not in path.name.lower() and "小标宋" not in path.name:
                    message = f"No exact 小标宋 font found; draft fallback used for {role}: {path}"
                    if self.strict:
                        raise RuntimeError(message)
                    self.warnings.append(message)
                return str(path)
        raise FileNotFoundError(f"No usable font found for {role}; tried: {candidates}")

    def _register(self, role: str, pdf_name: str, candidates: list[str], exact_title: bool = False) -> None:
        path = self._pick(role, candidates, exact_title)
        try:
            pdfmetrics.registerFont(TTFont(pdf_name, path))
        except Exception as exc:
            raise RuntimeError(f"Unable to register {role} font {path}: {exc}") from exc
        self.paths[role] = path

    def _register_all(self) -> None:
        win = os.environ.get("WINDIR", r"C:\Windows")
        fonts = str(Path(win) / "Fonts")
        self._register("body", "CNBody", [f"{fonts}/simfang.ttf", f"{fonts}/STFANGSO.TTF"])
        self._register("hei", "CNHei", [f"{fonts}/simhei.ttf", f"{fonts}/HYZhongHeiTi-197.ttf"])
        self._register("kai", "CNKai", [f"{fonts}/simkai.ttf", f"{fonts}/STKAITI.TTF"])
        self._register("song", "CNSong", [f"{fonts}/STSONG.TTF", f"{fonts}/simsun.ttc"])
        self._register(
            "title",
            "CNTitle",
            [
                f"{fonts}/FZXBSJW.TTF",
                f"{fonts}/FZXBSJW_GBK.TTF",
                f"{fonts}/方正小标宋简体.ttf",
                f"{fonts}/STZHONGS.TTF",
                f"{fonts}/STSONG.TTF",
            ],
            exact_title=True,
        )


class OfficialPDF:
    def __init__(self, data: dict[str, Any], output: Path, strict_fonts: bool = False):
        self.data = data
        self.output = output
        self.format = str(data.get("format", "general")).lower()
        if self.format not in {"general", "upward", "letter", "order", "minutes"}:
            raise ValueError("format must be general, upward, letter, order, or minutes")
        self.fonts = FontBook(data.get("fonts"), strict_fonts)
        self.warnings = list(self.fonts.warnings)
        self.canvas = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
        self.canvas.setTitle(normalize_text(data.get("title")) or "党政机关公文")
        self.canvas.setAuthor(normalize_text(data.get("issuing_authority")) or "")
        self.page = 1
        self.y = TOP - BODY_SIZE
        self.suppress_page_numbers = {int(x) for x in data.get("suppress_page_numbers", [])}
        if self.format == "letter":
            self.suppress_page_numbers.add(1)
        self._page_open = True
        self._started_body = False

    def draw_text_cells(self, text: str, x: float, y: float, font: str, size: float, color=BLACK) -> None:
        self.canvas.setFillColor(color)
        self.canvas.setFont(font, size)
        cursor = x
        for ch in text:
            advance = CELL * fullwidth_units(ch)
            glyph_w = pdfmetrics.stringWidth(ch, font, size)
            self.canvas.drawString(cursor + max(0.0, (advance - glyph_w) / 2.0), y, ch)
            cursor += advance

    def draw_centered(self, text: str, y: float, font: str, size: float, color=BLACK) -> None:
        self.canvas.setFillColor(color)
        self.canvas.setFont(font, size)
        width = pdfmetrics.stringWidth(text, font, size)
        self.canvas.drawString(LEFT + (TYPE_W - width) / 2.0, y, text)

    def ensure_lines(self, count: int) -> None:
        if self.y - (count - 1) * LINE < BOTTOM + 4:
            self.finish_page()
            self.y = TOP - BODY_SIZE

    def finish_page(self, final: bool = False) -> None:
        if self.page not in self.suppress_page_numbers:
            self.draw_page_number()
        if final:
            self.canvas.save()
            self._page_open = False
        else:
            self.canvas.showPage()
            self.page += 1
            self._page_open = True

    def draw_page_number(self) -> None:
        number = str(self.page)
        self.canvas.setStrokeColor(BLACK)
        self.canvas.setFillColor(BLACK)
        self.canvas.setLineWidth(0.6)
        self.canvas.setFont("CNSong", PAGE_NO_SIZE)
        num_w = pdfmetrics.stringWidth(number, "CNSong", PAGE_NO_SIZE)
        dash_w = PAGE_NO_SIZE
        gap = 5.0
        total = dash_w * 2 + gap * 2 + num_w
        if self.page % 2:
            right_edge = RIGHT - CELL
            start = right_edge - total
        else:
            start = LEFT + CELL
        y = BOTTOM - 7 * mm - PAGE_NO_SIZE * 0.25
        self.canvas.line(start, y + 4.0, start + dash_w, y + 4.0)
        self.canvas.drawString(start + dash_w + gap, y, number)
        second = start + dash_w + gap + num_w + gap
        self.canvas.line(second, y + 4.0, second + dash_w, y + 4.0)

    def draw_header(self) -> None:
        if self.format == "letter":
            self._draw_letter_header()
            return

        if self.format == "order":
            mark = normalize_text(self.data.get("authority_mark")) or (
                normalize_text(self.data.get("issuing_authority")) + "令"
            )
            mark_top = TOP - 20 * mm
            self.draw_centered(mark, mark_top - 44, "CNTitle", 44, RED)
            number = normalize_text(self.data.get("order_number") or self.data.get("document_number"))
            number_y = mark_top - 44 - 2 * LINE
            if number:
                self.draw_centered(number, number_y, "CNBody", BODY_SIZE)
            else:
                self.warnings.append("Order format has no order_number/document_number.")
            self.y = number_y - 2 * LINE
            return

        copy_number = normalize_text(self.data.get("copy_number"))
        classification = normalize_text(self.data.get("classification"))
        urgency = normalize_text(self.data.get("urgency"))
        top_y = TOP - BODY_SIZE
        if copy_number:
            if not (copy_number.isdigit() and len(copy_number) == 6):
                self.warnings.append("copy_number should normally contain exactly six digits.")
            self.draw_text_cells(copy_number, LEFT, top_y, "CNBody", BODY_SIZE)
            top_y -= LINE
        if classification:
            self.draw_text_cells(classification, LEFT, top_y, "CNHei", BODY_SIZE)
            top_y -= LINE
        if urgency:
            self.draw_text_cells(urgency, LEFT, top_y, "CNHei", BODY_SIZE)

        mark = normalize_text(self.data.get("authority_mark"))
        if not mark:
            authority = normalize_text(self.data.get("issuing_authority"))
            mark = authority + ("文件" if authority and self.format != "minutes" else "")
        if self.format == "minutes" and mark and not mark.endswith("纪要"):
            mark += "纪要"
        if not mark:
            self.warnings.append("Missing issuing-authority mark.")
        mark_size = float(self.data.get("authority_mark_size_pt", 48))
        mark_size = min(mark_size, 62.0)
        mark_top = PAGE_H - 72 * mm
        mark_y = mark_top - mark_size * 0.82
        self.draw_centered(mark, mark_y, "CNTitle", mark_size, RED)

        number_y = mark_y - 2 * LINE
        number = normalize_text(self.data.get("document_number"))
        if self.format == "upward":
            if number:
                self.draw_text_cells(number, LEFT + CELL, number_y, "CNBody", BODY_SIZE)
            signers = self.data.get("signers") or []
            if isinstance(signers, str):
                signers = [signers]
            if signers:
                label = "签发人："
                names = "　".join(normalize_text(x) for x in signers)
                label_w = pdfmetrics.stringWidth(label, "CNBody", BODY_SIZE)
                names_w = pdfmetrics.stringWidth(names, "CNKai", BODY_SIZE)
                x = RIGHT - CELL - label_w - names_w
                self.canvas.setFont("CNBody", BODY_SIZE)
                self.canvas.setFillColor(BLACK)
                self.canvas.drawString(x, number_y, label)
                self.canvas.setFont("CNKai", BODY_SIZE)
                self.canvas.drawString(x + label_w, number_y, names)
            else:
                self.warnings.append("Upward format requires signer name(s).")
        elif number:
            self.draw_centered(number, number_y, "CNBody", BODY_SIZE)
        else:
            self.warnings.append("Missing document_number.")

        red_y = number_y - 4 * mm
        self.canvas.setStrokeColor(RED)
        self.canvas.setLineWidth(1.0)
        self.canvas.line(LEFT, red_y, RIGHT, red_y)
        self.y = red_y - 2 * LINE

    def _draw_letter_header(self) -> None:
        authority = normalize_text(self.data.get("authority_mark") or self.data.get("issuing_authority"))
        name_size = float(self.data.get("authority_mark_size_pt", 30))
        name_top = PAGE_H - 30 * mm
        name_y = name_top - name_size * 0.82
        self.draw_centered(authority, name_y, "CNTitle", name_size, RED)
        upper = name_y - 4 * mm
        x0 = (PAGE_W - 170 * mm) / 2.0
        x1 = x0 + 170 * mm
        self.canvas.setStrokeColor(RED)
        self.canvas.setLineWidth(1.0)
        self.canvas.line(x0, upper, x1, upper)
        self.canvas.setLineWidth(0.5)
        self.canvas.line(x0, upper - 2, x1, upper - 2)
        lower = 20 * mm
        self.canvas.setLineWidth(0.5)
        self.canvas.line(x0, lower + 2, x1, lower + 2)
        self.canvas.setLineWidth(1.0)
        self.canvas.line(x0, lower, x1, lower)
        number = normalize_text(self.data.get("document_number"))
        if number:
            self.canvas.setFillColor(BLACK)
            self.canvas.setFont("CNBody", BODY_SIZE)
            width = pdfmetrics.stringWidth(number, "CNBody", BODY_SIZE)
            self.canvas.drawString(RIGHT - width, upper - LINE, number)
        self.y = upper - 3 * LINE

    def draw_title_and_recipients(self) -> None:
        title = normalize_text(self.data.get("title"))
        if not title:
            self.warnings.append("Missing title.")
        title_lines = split_title(title, "CNTitle", TITLE_SIZE)
        for line in title_lines:
            self.ensure_lines(1)
            self.draw_centered(line, self.y, "CNTitle", TITLE_SIZE)
            self.y -= LINE
        if title_lines:
            self.y -= LINE  # title 下空一行 before recipient

        recipients = normalize_text(self.data.get("recipients"))
        if recipients:
            if not recipients.endswith("："):
                recipients += "："
            for line, indent in wrap_cells(recipients, 28, 0):
                self.ensure_lines(1)
                self.draw_text_cells(line, LEFT + indent * CELL, self.y, "CNBody", BODY_SIZE)
                self.y -= LINE
        self._started_body = True

    def draw_blocks(self, blocks: Any) -> None:
        if isinstance(blocks, str):
            blocks = [{"type": "paragraph", "text": p} for p in blocks.split("\n") if p.strip()]
        for raw in blocks or []:
            if isinstance(raw, str):
                raw = {"type": "paragraph", "text": raw}
            kind = str(raw.get("type", "paragraph")).lower()
            text = normalize_text(raw.get("text"))
            if not text:
                continue
            font = {"h1": "CNHei", "h2": "CNKai", "h3": "CNBody", "h4": "CNBody"}.get(kind, "CNBody")
            indent = float(raw.get("first_line_indent", 2.0))
            lines = wrap_cells(text, 28, indent)
            for line, line_indent in lines:
                self.ensure_lines(1)
                self.draw_text_cells(line, LEFT + line_indent * CELL, self.y, font, BODY_SIZE)
                self.y -= LINE

    def draw_attachment_description(self, attachments: list[Any]) -> None:
        if not attachments:
            return
        self.ensure_lines(2 + len(attachments))
        self.y -= LINE
        for index, item in enumerate(attachments, start=1):
            name = normalize_text(item.get("name")) if isinstance(item, dict) else normalize_text(item)
            prefix = "附件：" if len(attachments) == 1 else f"附件：{index}. "
            combined = prefix + name
            lines = wrap_cells(combined, 28, 2)
            for line, indent in lines:
                self.draw_text_cells(line, LEFT + indent * CELL, self.y, "CNBody", BODY_SIZE)
                self.y -= LINE

    def draw_signature(self) -> None:
        signature = normalize_text(self.data.get("signature"))
        date = normalize_text(self.data.get("date"))
        if not signature and not date:
            self.warnings.append("Missing signature and date.")
            return
        seal = self.data.get("seal_image")
        self.ensure_lines(4 if seal else 3)
        self.y -= LINE
        date_right = RIGHT - 4 * CELL
        date_w = pdfmetrics.stringWidth(date, "CNBody", BODY_SIZE)
        date_x = date_right - date_w
        sig_w = pdfmetrics.stringWidth(signature, "CNBody", BODY_SIZE)
        sig_x = date_x + (date_w - sig_w) / 2.0 if seal else RIGHT - 2 * CELL - sig_w
        self.canvas.setFillColor(BLACK)
        self.canvas.setFont("CNBody", BODY_SIZE)
        self.canvas.drawString(sig_x, self.y, signature)
        date_y = self.y - LINE
        if not seal:
            date_x = min(RIGHT - 2 * CELL - date_w, sig_x + 2 * CELL)
        self.canvas.drawString(date_x, date_y, date)

        if seal:
            seal_path = Path(os.path.expandvars(os.path.expanduser(str(seal)))).resolve()
            if not seal_path.is_file():
                raise FileNotFoundError(f"Authorized seal image not found: {seal_path}")
            seal_size = float(self.data.get("seal_size_mm", 42)) * mm
            cx = date_x + date_w / 2.0
            self.canvas.drawImage(
                str(seal_path), cx - seal_size / 2.0, date_y - seal_size * 0.28,
                width=seal_size, height=seal_size, mask="auto", preserveAspectRatio=True,
            )
        elif self.data.get("seal_required", True):
            self.warnings.append("No authorized seal image supplied; generated PDF is a draft/unsealed layout.")
        self.y = date_y - LINE

        note = normalize_text(self.data.get("note"))
        if note:
            if not (note.startswith("（") and note.endswith("）")):
                note = f"（{note}）"
            self.ensure_lines(1)
            self.draw_text_cells(note, LEFT + 2 * CELL, self.y, "CNBody", BODY_SIZE)
            self.y -= LINE

    def draw_attachment_bodies(self, attachments: list[Any]) -> None:
        for index, item in enumerate(attachments, start=1):
            if not isinstance(item, dict) or not item.get("body"):
                if not isinstance(item, dict):
                    self.warnings.append(f"Attachment {index} has a description but no body content in JSON.")
                continue
            self.finish_page()
            self.y = TOP - BODY_SIZE
            marker = "附件" if len(attachments) == 1 else f"附件{index}"
            self.draw_text_cells(marker, LEFT, self.y, "CNHei", BODY_SIZE)
            self.y -= 2 * LINE
            name = normalize_text(item.get("name"))
            for line in split_title(name, "CNTitle", TITLE_SIZE):
                self.draw_centered(line, self.y, "CNTitle", TITLE_SIZE)
                self.y -= LINE
            self.y -= LINE
            self.draw_blocks(item.get("body"))

    def draw_edition_record(self) -> None:
        copy_to = normalize_text(self.data.get("copy_to"))
        printing_authority = normalize_text(self.data.get("printing_authority"))
        printing_date = normalize_text(self.data.get("printing_date"))
        if not any([copy_to, printing_authority, printing_date]):
            return
        if self.format == "letter":
            if copy_to:
                y = 25 * mm
                self.canvas.setFont("CNBody", RECORD_SIZE)
                self.canvas.drawString(LEFT + CELL, y, "抄送：" + copy_to.rstrip("。") + "。")
            return
        needed = 3 if copy_to else 2
        if self.y < BOTTOM + needed * LINE + 6:
            self.finish_page()
            self.y = TOP - BODY_SIZE
            self.warnings.append("Edition record moved to a new final side because remaining space was insufficient.")
        last_y = BOTTOM
        print_y = last_y + LINE
        copy_y = print_y + LINE if copy_to else None
        first_y = (copy_y + LINE * 0.35) if copy_y is not None else (print_y + LINE * 0.35)
        self.canvas.setStrokeColor(BLACK)
        self.canvas.setLineWidth(1.0)
        self.canvas.line(LEFT, first_y, RIGHT, first_y)
        if copy_to:
            self.canvas.setFont("CNBody", RECORD_SIZE)
            self.canvas.setFillColor(BLACK)
            self.canvas.drawString(LEFT + CELL, copy_y, "抄送：" + copy_to.rstrip("。") + "。")
            self.canvas.setLineWidth(0.7)
            self.canvas.line(LEFT, print_y + LINE * 0.35, RIGHT, print_y + LINE * 0.35)
        self.canvas.setFont("CNBody", RECORD_SIZE)
        self.canvas.drawString(LEFT + CELL, print_y, printing_authority)
        right_text = (printing_date + "印发") if printing_date and not printing_date.endswith("印发") else printing_date
        right_w = pdfmetrics.stringWidth(right_text, "CNBody", RECORD_SIZE)
        self.canvas.drawString(RIGHT - CELL - right_w, print_y, right_text)
        self.canvas.setLineWidth(1.0)
        self.canvas.line(LEFT, last_y, RIGHT, last_y)

    def build(self) -> dict[str, Any]:
        self.draw_header()
        self.draw_title_and_recipients()
        self.draw_blocks(self.data.get("body"))
        attachments = self.data.get("attachments") or []
        if isinstance(attachments, (str, dict)):
            attachments = [attachments]
        self.draw_attachment_description(attachments)
        self.draw_signature()
        self.draw_attachment_bodies(attachments)
        self.draw_edition_record()
        self.finish_page(final=True)
        return {
            "standard": "GB/T 9704-2012 engineering baseline",
            "format": self.format,
            "page_count": self.page,
            "page_size_mm": [210, 297],
            "type_area_mm": {"left": 28, "top": 37, "width": 156, "height": 225},
            "line_grid": {"lines_per_side": 22, "cells_per_line": 28, "baseline_pitch_pt": LINE},
            "fonts": self.fonts.paths,
            "warnings": self.warnings,
            "created_utc": datetime.now(timezone.utc).isoformat(),
        }


def render_pdf(pdf: Path, render_dir: Path, warnings: list[str]) -> list[str]:
    render_dir.mkdir(parents=True, exist_ok=True)
    prefix = render_dir / pdf.stem
    executable = shutil.which("pdftoppm") or shutil.which("pdftoppm.exe")
    rendered: list[str] = []
    if executable:
        subprocess.run([executable, "-png", "-r", "180", str(pdf), str(prefix)], check=True)
        rendered = [str(p) for p in sorted(render_dir.glob(f"{pdf.stem}-*.png"))]
    else:
        try:
            import fitz  # type: ignore

            doc = fitz.open(pdf)
            matrix = fitz.Matrix(2.5, 2.5)
            for index, page in enumerate(doc, start=1):
                path = render_dir / f"{pdf.stem}-{index}.png"
                page.get_pixmap(matrix=matrix, alpha=False).save(path)
                rendered.append(str(path))
        except Exception as exc:
            warnings.append(f"PDF rendering unavailable (pdftoppm/PyMuPDF): {exc}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 JSON input")
    parser.add_argument("output", type=Path, help="Output PDF")
    parser.add_argument("--report", type=Path, help="Write JSON layout report")
    parser.add_argument("--render-dir", type=Path, help="Render every page to PNG")
    parser.add_argument("--strict-fonts", action="store_true", help="Fail if exact 小标宋 is unavailable")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = OfficialPDF(data, args.output, args.strict_fonts).build()
    if args.render_dir:
        report["rendered_pages"] = render_pdf(args.output, args.render_dir, report["warnings"])
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
