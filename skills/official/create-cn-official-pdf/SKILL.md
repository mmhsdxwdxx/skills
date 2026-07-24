---
name: create-cn-official-pdf
description: Create, typeset, inspect, or correct Chinese Party and government official-document PDFs under GB/T 9704-2012 and the Regulations on Handling Official Documents. Use for 通知、请示、报告、函、批复、纪要、决定、决议、命令（令）、公报、公告、通告、意见、议案、通报, 红头文件, 公文排版, 公文格式核验, or requests involving Chinese official-document fonts, font sizes, margins, line grids, indents, spacing, page numbers, seals, attachments, copy recipients, printing notes, PDF generation, or PDF preflight.
---

# Create Chinese Official-Document PDFs

Produce a print-ready PDF, not merely text that resembles a government document. Treat GB/T 9704-2012 as the national format baseline and keep agency-specific rules as explicit overrides.

## Mandatory source loading

1. Read [references/format-standard.md](references/format-standard.md) completely before typesetting or auditing.
2. Read [references/document-types-and-writing.md](references/document-types-and-writing.md) when choosing a document type, drafting content, or reviewing wording.
3. If the user supplies an agency template or local rule, inspect it and record every deviation from the national baseline before generation.

## Workflow

1. Determine the document type, direction of communication, issuing authority, recipients, document number, signers, attachments, date, seal status, copy recipients, and printing authority/date from the request or source material.
2. Use `general` unless the content clearly requires `upward`, `letter`, `order`, or `minutes`. Never infer a fake issuing authority, document number, signer, or seal.
3. Normalize content into the JSON structure demonstrated by [assets/example.json](assets/example.json). Preserve official names, dates, citations, punctuation, and attachment titles exactly.
4. Generate the PDF with the bundled runtime:

   ```powershell
   python scripts/official_pdf.py input.json output.pdf --report output.layout.json --render-dir rendered
   ```

5. Review the layout report. Treat missing 小标宋, substituted fonts, absent required metadata, overflow, and omitted seal as visible warnings, not silent fallbacks.
6. Inspect every rendered PNG. Verify red elements, title wrapping, first-page body presence, 22-line grid behavior, two-character indents, signatures, attachments, edition record, odd/even page numbers, and absence of clipping or blank extra pages.
7. Run the verifier after the last edit:

   ```powershell
   python scripts/verify_official_pdf.py output.pdf --report output.layout.json
   ```

8. Deliver the PDF together with a concise compliance note listing any agency overrides or unresolved warnings.

## Non-negotiable rules

- Use A4, a 156 mm × 225 mm type area, 37 mm ± 1 mm top white margin, and 28 mm ± 1 mm binding-side margin unless a special format explicitly overrides placement.
- Use 2号小标宋 for the title; 3号仿宋 for ordinary body; 3号黑体 / 楷体 / 仿宋 for levels one through four; 4号仿宋 for the edition record; and 4号宋体 for page numbers.
- Use no paragraph-before or paragraph-after spacing in body text. Express vertical gaps in standard “lines”; keep the body on the 22-line grid and each ordinary line at 28 full-width character cells.
- Indent every natural body paragraph by two full-width character cells; wrap subsequent lines at the left edge. Do not indent titles or recipient lines.
- Do not synthesize, trace, or imitate an official seal. Only place a user-supplied authorized seal image; otherwise reserve the correct space and flag the omission.
- Do not claim that a font substitute is compliant. If 小标宋 is unavailable, use the closest readable Song-style fallback only for a draft and report it.
- Do not invent a universal Word “fixed line spacing” value. The national standard defines a 22-line page and a standard line unit; point values such as 28.8, 29, or 30 pt are implementation choices and may require calibration to the installed font.
- Keep digits and Latin letters in the surrounding prescribed font unless the user or agency rule explicitly requires Times New Roman. Times New Roman is a common local convention, not a blanket GB/T 9704-2012 mandate.
- Keep the PDF text searchable and embed fonts when licensing and the renderer permit it.

## Script behavior

`official_pdf.py` directly controls millimetre coordinates and does not depend on Word pagination. It supports the five layout modes above, body paragraphs and four heading levels, attachments, signature/date blocks, optional authorized seal images, edition records, and odd/even page numbering. Use `--strict-fonts` for final production when exact required fonts are installed.

The generator is a standards-oriented baseline. For complex tables, landscape inserts, multi-authority seals, minority-language documents, or an agency-specific red-head asset, adapt the script or use an approved template, then visually verify every page.
