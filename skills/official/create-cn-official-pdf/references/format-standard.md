# GB/T 9704—2012 implementation reference

## Contents

1. Authority and source hierarchy
2. Measurement model
3. Global page, type, and spacing rules
4. Complete element-by-element specification
5. Special formats
6. Printing, binding, and PDF requirements
7. National rule versus local convention
8. Preflight checklist
9. Sources

## 1. Authority and source hierarchy

Apply sources in this order: current national law/regulation/standard; an applicable superior or issuing authority's valid implementation rule; an authorized agency template or red-head asset; then the engineering defaults in this skill.

The national baseline is GB/T 9704—2012《党政机关公文格式》, released 2012-06-29, implemented 2012-07-01, and listed as current by the national standards platform as of 2026-07-24. The companion regulation is《党政机关公文处理工作条例》, especially Articles 9–12.

GB/T 9704 is recommended (`GB/T`), but Article 10 of the regulation directs Party and government official-document layout to follow that national standard. Agency-specific forms may add rules but should not be silently treated as national requirements.

Related national references include GB/T 148 for paper size, GB/T 15834 for punctuation, GB/T 15835 for numbers, and the GB/T 33476 series for electronic official-document structure and presentation.

## 2. Measurement model

- `一字`: the horizontal space occupied by one Chinese character.
- `一行`: one Chinese character height plus 7/8 of a 3号 Chinese-character height.
- PDF conversion used by this skill: 2号 = 22 pt, 3号 = 16 pt, 4号 = 14 pt. The standard specifies named Chinese sizes, not PDF points.
- At 156 mm/28 cells, one full-width cell is 5.5714 mm (about 15.79 pt).
- Practical PDF/Word implementations normally calibrate a baseline pitch around 28.8–30 pt to realize the 22-line type area. Do not state that one such point value is itself the national rule; verify actual pagination and type-area fill.

## 3. Global page, type, and spacing rules

### Paper and type area

- A4: 210 mm × 297 mm.
- Top white margin (`天头`): 37 mm ± 1 mm.
- Binding-side white margin (`订口`): 28 mm ± 1 mm.
- Type area: 156 mm × 225 mm, excluding page number.
- On left-bound portrait pages this implies a nominal right margin of 26 mm and bottom margin of 35 mm.
- Write horizontally from left to right. Use both sides for final printing.
- Text is black unless an element is explicitly red.

### Line and character grid

- Ordinary layout: 22 lines per side, 28 full-width Chinese-character cells per line, filling the type area.
- Body paragraphs: no extra paragraph-before or paragraph-after spacing.
- Natural paragraphs begin with a two-character first-line indent; wrapped lines return to the left edge.
- A specified blank line is a layout unit, not an empty paragraph with arbitrary Word spacing.
- Keep inseparable numbers, years, and number-unit groups on one line.
- Avoid a lone character on a line and a lone line at a page edge where practical; adjust character/line spacing only within controlled tolerance.

### Fonts

| Element | National baseline |
|---|---|
| Unspecified elements | 3号仿宋 |
| Main title | 2号小标宋 |
| Level-1 heading | 3号黑体 |
| Level-2 heading | 3号楷体 |
| Level-3 and level-4 headings | 3号仿宋 |
| Edition record | 4号仿宋 |
| Page number | 4号宋体, half-width Arabic numerals |

Do not automatically bold levels three and four. Some Party/local rules do; GB/T 9704 identifies the face but does not make bold a universal requirement.

## 4. Complete element-by-element specification

### 4.1 Copy number (`份号`)

- Required for classified documents; otherwise use only when the issuing process requires it.
- Six 3号 Arabic digits, zero-padded, e.g. `000017`.
- Flush at the first line in the upper-left of the type area.

### 4.2 Classification and confidentiality period

- Use `绝密`, `机密`, or `秘密`; add the period when required.
- Use 3号黑体, flush left.
- Separate classification and period with a solid star: `秘密★10年`.
- If copy number is present, place this on the next line.

### 4.3 Urgency

- Documents: `特急` or `加急`; telegrams: `特提`, `特急`, `加急`, or `平急`.
- Use 3号黑体, flush left.
- Stack in this order: copy number, classification/period, urgency.

### 4.4 Issuing-authority mark (`发文机关标志`)

- Form: full or normalized short authority name plus `文件`, or the authority name alone for an authorized specific form.
- Use red 小标宋, centered.
- Choose the size for dignity and fit; each character may not exceed 22 mm high × 15 mm wide.
- General form: mark upper edge 35 mm below the upper edge of the type area, nominally 72 mm from sheet top.
- Joint issue: principal authority first; `文件` to the right and vertically centered. Ensure page 1 still has body text.
- Prefer an approved vector/red-head asset supplied by the office over reconstructing the mark with a substitute font.

### 4.5 Document number (`发文字号`)

- Authority code + full year in `〔〕` + sequence + `号`; no `第`, no zero-padded sequence. Example: `国办发〔2026〕1号`.
- Use 3号仿宋.
- Ordinary: center below the mark after two blank lines.
- Upward: left with one-character inset, aligned to the final signer.
- Red separator: full 156 mm type width, 4 mm below the number/signers.

### 4.6 Signer (`签发人`)

- Required for upward documents.
- `签发人：姓名`, full-width colon.
- Label: 3号仿宋; name: 3号楷体.
- Right with one-character inset, sharing the document-number band.
- Multiple signers follow authority order left-to-right then top-to-bottom, normally two names per line; the last signer shares the document-number line.

### 4.7 Main title

- Normally issuing authority + subject + document type.
- 2号小标宋, black, centered.
- Start two blank lines below the red separator.
- Multi-line title: preserve phrases, symmetry, suitable lengths, and even spacing; prefer trapezoid or diamond, not an hourglass.
- Normally omit punctuation except necessary book-title marks for named laws, rules, or documents.

### 4.8 Primary recipient (`主送机关`)

- Full name, normalized short name, or collective name.
- 3号仿宋.
- Start one blank line below title, flush left; wraps remain flush left.
- End the final recipient with a full-width colon.
- If recipients prevent body text on page 1, move them to the edition record as `主送：`.

### 4.9 Body

- Start on the line immediately after recipient.
- 3号仿宋; first line of each natural paragraph inset two characters; continuation flush left; zero paragraph spacing.
- Normally no more than four levels:

  1. `一、` — 3号黑体
  2. `（一）` — 3号楷体
  3. `1.` — 3号仿宋
  4. `（1）` — 3号仿宋

- Use Chinese full-width parentheses at levels two/four and a full stop after the Arabic numeral at level three.
- A standalone heading normally has no terminal punctuation.

### 4.10 Attachment description (`附件说明`)

- One blank line after body; two-character inset; 3号仿宋.
- `附件：名称`; multiple: `附件：1. 名称`.
- No terminal punctuation after the name.
- Wrapped names align with the first character of the name.

### 4.11 Signature, date, and seal

- Signature: full or normalized authority name.
- Date: complete year/month/day in Arabic digits; do not zero-pad month/day, e.g. `2026年7月24日`.
- Seal is red and must correspond to the signature. Never create or imitate a seal; use only an authorized user-supplied asset.

One authority with seal:

- Signature above date, centered relative to date; date normally right-inset four characters.
- Center the seal over signature and date so both sit in its lower half.
- Seal top stays within one line of preceding body/attachment text.

Multiple authorities with seals:

- Arrange signatures in issuance order and seals neatly without touching/overlap; stay within the type area. The last seal also presses the final signature/date.

No seal:

- One blank line after body/attachment text; signature right-inset two characters.
- Date on next line; its first character normally two characters right of signature's first. If date is longer, right-inset date two characters and adjust signature.

Leader signature seal for an order:

- Two lines after body/attachment text; signature seal right-inset four characters.
- Full leader title two characters to the left, vertically centered; date one line below, right-inset four characters.

If the remaining page cannot contain the block, carefully adjust spacing to keep it with preceding text. Never add `此页无正文`.

### 4.12 Note (`附注`)

- 3号仿宋; line below date; left-inset two characters; enclosed in Chinese parentheses.

### 4.13 Attachment body

- Start each attachment on a new side before the edition record.
- First line upper-left: `附件` plus number in 3号黑体.
- Attachment title centered on third line; number/title must exactly match the description.
- Format body by general rules.
- If not bound with main document, top-left first line shows the main number followed by `附件` and its number.

### 4.14 Copy recipients (`抄送机关`)

- 4号仿宋 in edition record, above printing authority/date; one-character inset on both sides.
- `抄送：` + names; continuation aligns with first name; end with a full stop.
- If primary recipients moved here, place `主送：` above without a separator between.

### 4.15 Printing authority/date

- 4号仿宋 on line above final edition-record separator.
- Authority left-inset one character; printing date right-inset one character, full Arabic date without leading zeros, followed by `印发`.

### 4.16 Edition-record separators

- 156 mm width.
- First/last: recommended height 0.35 mm; intermediate: 0.25 mm.
- First sits above first item; last coincides with lower type-area edge.
- Edition record is on the final side.

### 4.17 Page numbers

- 4号宋体 half-width Arabic numerals below type area.
- Upper edge of each flanking one-em line is 7 mm below the lower type-area edge.
- Odd: outside right, one character in from right type edge. Even: outside left, one character in from left type edge.
- Render flanking dashes as vector one-em rules when a glyph is unreliable.
- A blank side before the edition-record side and that edition-record side carry no page number. Bound attachments continue numbering.
- General page 1 has a number; letter-format page 1 does not.

### 4.18 Spacing matrix

| Transition | Required gap |
|---|---|
| Mark → document number | two blank lines |
| Document number → red separator | 4 mm |
| Red separator → title | two blank lines |
| Title → recipient | one blank line |
| Recipient → body | next line, no blank line |
| Body → attachment description | one blank line |
| Body/attachment → unsealed signature | one blank line |
| Body/attachment → leader signature seal | two blank lines |
| Date → note | next line |
| Attachment marker → attachment title | title on third line |

## 5. Special formats

### Letter (`信函格式`)

- Authority name centered, red 小标宋, upper edge 30 mm from sheet top.
- A 170 mm red double rule 4 mm below name: upper thick, lower thin.
- A 170 mm red double rule 20 mm from sheet bottom: upper thin, lower thick.
- Document number upper-right beneath first double rule; classification/urgency upper-left when present.
- Center 28 characters per line.
- Edition record contains copy recipients only, without surrounding separator or printing authority/date.
- No page number on first side.
- This is a layout form, not synonymous with document type `函`.

### Command/order (`命令（令）格式`)

- Mark `发文机关名称+令`, centered red 小标宋, upper edge 20 mm below upper type-area edge.
- `第×号` centered two lines below; body two lines below number.
- Use authorized leader signature seal and title; date one line below.
- A supplied agency order template takes priority.

### Minutes (`纪要格式`)

- Mark `××××纪要`, centered red 小标宋, upper edge 35 mm below upper type-area edge.
- May be customized by issuing authority.
- Attendance lists after body/attachment text: one blank line, two-character inset; 3号黑体 for `出席：`, `请假：`, `列席：`; 3号仿宋 for units/names; continuations align to first name.

### Landscape tables

- Keep page-number position consistent with portrait pages.
- Odd side table head faces binding edge; even side faces cut edge.
- Maintain legibility and type-area discipline; agency templates may refine treatment.

### Minority-language documents

Apply the same paper, dimensions, layout, printing, and binding requirements; apply relevant language rules to remaining typography and writing details.

## 6. Printing, binding, and PDF requirements

### Paper

- 60–80 g/m² offset printing/copy paper; whiteness 80%–90%; cross-direction folding endurance ≥15; opacity ≥85%; pH 7.5–9.5.

### Printing and binding

- Double-sided; page images aligned, typical two-side tolerance ≤2 mm.
- Clear, solid, even reproduction; no broken strokes, smears, folds, missing/duplicate pages, or unintended blanks.
- Left binding, flat and secure. Two outer staple holes 70 mm from upper/lower sheet edges, tolerance ±4 mm.
- Saddle stitches on fold; flat-stitch wire 3–5 mm from spine.
- Cut-size tolerance ±2 mm; 90° corners; no burrs/defects.

### PDF

- Exact A4 MediaBox: about 595.276 × 841.890 PDF points.
- Searchable text and embedded font subsets where permitted.
- Preserve vector text/lines; raster only for authorized seals, red-head images, scanned signatures, or unavoidable sources.
- Use PDF/A only if the archive workflow requires it; PDF/A does not itself prove GB/T 9704 compliance.
- Inspect every page rasterized at 150–200 dpi before delivery.

## 7. National rule versus local convention

| Common practice | Correct treatment |
|---|---|
| Fixed 28/28.8/29/30 pt line spacing | Engineering/local setting for the 22-line grid; calibrate to font/renderer. |
| All digits/Latin in Times New Roman | Agency/local convention unless explicitly required. |
| Level-3/4 headings bold | Agency/Party-office convention, not blanket GB/T rule. |
| `仿宋_GB2312` specifically | Common font choice; national wording is 仿宋体. Prefer GBK/Unicode support. |
| Margins 3.3/2.8/2.5/2.5 cm | Local setting, not national geometry. |
| Centered page numbers | Generally not compliant with national general format; use odd/even outside edges. |

## 8. Preflight checklist

- [ ] Correct document type/direction; required signer for upward document.
- [ ] A4, 156 × 225 mm type area, 37 mm top and 28 mm binding-side margins.
- [ ] Exact fonts installed or substitutions disclosed.
- [ ] 22-line × 28-cell grid; zero body paragraph spacing.
- [ ] Title 2号小标宋 and balanced wrapping.
- [ ] Correct gaps for title, recipient, body, attachments, signature/date.
- [ ] Paragraphs indent two characters; continuations flush left.
- [ ] Heading sequence, punctuation, and typefaces correct.
- [ ] Number uses `〔〕`, full year, no zero-padded sequence.
- [ ] Full-width punctuation and valid number/unit usage.
- [ ] Attachment description/pages agree exactly.
- [ ] Authorized real seal only; signature/date correct.
- [ ] Edition record and separators correct.
- [ ] Odd/even page numbers and blank-side exceptions correct.
- [ ] General page 1 contains body text.
- [ ] Every rendered page inspected for clipping, overlap, widows/orphans, accidental blanks, damaged glyphs.
- [ ] Printing/binding specs communicated when a paper original is required.

## 9. Sources

Government and standards sources, retrieved 2026-07-24:

- National standard status: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=F3CC9BEF482524C895FDA7A08BB4A70E&refer=outter
- National standards public service platform: https://std.samr.gov.cn/gb/search/gbDetailedCNF?id=71F772D7E77CD3A7E05397BE0A0AB82A
-《党政机关公文处理工作条例》: https://www.miit.gov.cn/xwdt/szyw/art/2020/art_6afb8ee6d07540dcacccbeb47dbc0fd4.html
- Xiamen GB/T 9704—2012 implementation details: https://www.siming.gov.cn/xxgk/zfgb/201208/qfbwj/201209/t20120924_656819.htm
- Ankang government transcription/samples: https://www.ankang.gov.cn/Content-2060365.html
- Tibet Culture Department printing/binding: https://wlt.xizang.gov.cn/xwzx_69/tzgg/202204/t20220427_296133.html
- Shaanxi Transport Department letter/minutes notes: https://jtyst.shaanxi.gov.cn/zfxxgk/fdzdgknr/lzyj/qtgw/qtwj/201507/t20150708_3442860.html
- Beijing Haidian implementation details: https://zyk.bjhd.gov.cn/jbdt/auto4559_51855/201810/t20181002_3166291_hd.shtml

Confirm standard status and the issuing authority's current template again when precision is material.
