---
name: create-cn-official-pdf
description: Create, typeset, inspect, or correct Chinese Party and government official-document PDFs under GB/T 9704—2012 and the Regulations on Handling Official Documents. Use for 通知、请示、报告、函、批复、纪要、决定、决议、命令（令）、公报、公告、通告、意见、议案、通报, 红头文件, 公文排版, 公文格式核验, or requests involving Chinese official-document fonts, font sizes, margins, line grids, indents, spacing, page numbers, seals, attachments, copy recipients, printing notes, PDF generation, or PDF preflight.
---

# Create Chinese Official-Document PDFs

Produce a print-ready PDF that meets the national format baseline—not text that merely resembles a government document. Treat GB/T 9704—2012 as the national baseline, and treat any superior rule, issuing-authority template, or supplied red-head/seal asset as an explicit override recorded before generation.

## Mandatory source loading

1. Read [references/format-standard.md](references/format-standard.md) in full before typesetting or auditing.
2. Read [references/document-types-and-writing.md](references/document-types-and-writing.md) when choosing a document type, drafting content, or reviewing wording.
3. When the user supplies an agency template or local rule, inspect it and record every deviation from the national baseline before generation.

## Workflow

1. From the request or source material, determine the document type, direction of communication, issuing authority, recipients, document number, signers, attachments, date, seal status, copy recipients, and printing authority/date.
2. Derive the layout from the direction and type: `general` by default; `upward` for a 请示 or 报告 addressed to a superior; `letter` (信函格式) when the competent office authorizes it; `order` (命令/令); `minutes` (纪要). Never invent an issuing authority, document number, signer, or seal.
3. Normalize the content into the JSON structure shown in [assets/example.json](assets/example.json). Preserve official names, dates, citations, punctuation, and attachment titles exactly.
4. Generate the PDF with the bundled runtime:

   ```powershell
   python scripts/official_pdf.py input.json output.pdf --report output.layout.json --render-dir rendered
   ```

5. Read the layout report. Treat a missing 小标宋, a substituted font, missing required metadata, overflow, and an omitted seal as surfaced warnings—never as silent fallbacks.
6. Inspect every rendered PNG. Verify red elements, title wrapping, first-page body presence, 22-line grid behavior, two-character indents, signatures, attachments, the edition record, odd/even page numbers, and the absence of clipping or stray blank pages.
7. After the final edit, run the verifier:

   ```powershell
   python scripts/verify_official_pdf.py output.pdf --report output.layout.json
   ```

8. Deliver the PDF with a concise compliance note listing any agency overrides or unresolved warnings.

## Non-negotiable rules

- Page: A4 with a 156 mm × 225 mm type area, a 37 mm ± 1 mm top white margin, and a 28 mm ± 1 mm binding-side margin, unless a special format explicitly overrides placement.
- Fonts by element: title in 2号小标宋; ordinary body in 3号仿宋; level-1 heading `一、` in 3号黑体, level-2 `（一）` in 3号楷体, level-3 `1.` and level-4 `（1）` in 3号仿宋; edition record in 4号仿宋; page numbers in 4号宋体.
- Body spacing: no paragraph-before or paragraph-after spacing. Express vertical gaps in whole “lines”; keep the body on the 22-line grid with each ordinary line holding 28 full-width cells.
- Indentation: every natural body paragraph starts two full-width cells in; wrapped lines return flush left. Titles and recipient lines are not indented.
- Seals: do not synthesize, trace, or imitate an official seal. Place only a user-supplied authorized seal image; otherwise reserve the space and flag the omission.
- Font substitutes: never claim a substitute is compliant. If 小标宋 is unavailable, use the closest readable Song-style face only for a draft and report it.
- Line spacing: there is no universal Word “fixed line spacing” value. The national standard defines a 22-line page and a standard line unit; values such as 28.8, 29, or 30 pt are implementation choices that may need calibration to the installed font.
- Digits and Latin letters: keep them in the surrounding prescribed font unless the user or an agency rule explicitly requires Times New Roman. Times New Roman is a common local convention, not a blanket GB/T 9704—2012 mandate.
- Output: keep PDF text searchable and embed fonts when licensing and the renderer permit it.

## Script behavior

The generator requires `reportlab` and the verifier requires `pypdf`; page rendering prefers `pdftoppm` and falls back to `PyMuPDF`. Pin them with [requirements.txt](requirements.txt).

`official_pdf.py` controls millimetre coordinates directly and does not rely on Word pagination. It supports the five layout modes—`general`, `upward`, `letter`, `order`, `minutes`—plus body paragraphs, four heading levels, attachments, signature/date blocks, optional authorized seal images, edition records, and odd/even page numbering. Pass `--strict-fonts` for final production when the exact required fonts are installed.

The generator is a standards-oriented baseline. For complex tables, landscape inserts, multi-authority seals, minority-language documents, or an agency-specific red-head asset, adapt the script or use an approved template, then visually verify every page.
