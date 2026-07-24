---
name: draft-cn-official-document
description: Draft, structure, and preflight the CONTENT of a Chinese Party/government official document—choose the document type (通知、请示、报告、函、批复、纪要、决定、决议、命令（令）、公报、公告、通告、意见、议案、通报), set direction, organize structure, control wording, and emit JSON. Use for 起草, 拟稿, 写公文, 拟一份通知/请示/报告/函, 公文写作, 公文内容, 措辞, or structuring official-document content. Produces content for $create-cn-official-pdf to typeset; do not use this skill when the user only needs PDF typesetting of already-final content.
---

# Draft Chinese Official-Document Content

Produce the content of a compliant official document: document type chosen correctly, direction set, structure ordered, wording controlled, and every factual claim grounded. Emit a JSON object that `$create-cn-official-pdf` can typeset directly. This skill owns words and structure; it does not render or preflight PDF layout.

## Mandatory source loading

1. Read [references/document-types-and-writing.md](references/document-types-and-writing.md) in full before choosing a document type, setting direction, or drafting.

## Workflow

1. From the request, determine the sender's intent, the recipient relationship (superior / subordinate / non-subordinate / public / meeting), the matter, any policy or legal basis, attachments, and the desired outcome (inform, request approval, reply, report, negotiate, record).
2. Choose the document type from the fifteen in [references/document-types-and-writing.md](references/document-types-and-writing.md) §1, using the purpose defined by the《党政机关公文处理工作条例》—never by template resemblance. Set direction and routing per §2.
3. Resolve every factual basis before drafting: confirm policy citations, approval status, consultation results, names, dates, and numbers. If a fact cannot be verified, flag it to the user rather than inventing it.
4. Draft under the controls in §3 and the language/notation rules in §4: correct document type and format, concise and rigorous wording, full-width Chinese punctuation, `〔〕` for the document number, and numerals per GB/T 15835.
5. Run the content preflight:

   ```powershell
   python scripts/check_draft.py draft.json
   ```

   The script checks structure deterministically (schema, brackets, direction rules, date format, heading order); then walk the §5 checklist for what code cannot judge (jurisdiction, policy currency, consultation completeness). Treat every warning as something to resolve or explicitly justify—never a silent pass.
6. Emit a JSON object using the structures in [assets/templates.json](assets/templates.json), compatible with `$create-cn-official-pdf`. Preserve official names, dates, citations, and attachment titles exactly.
7. When the user wants a PDF, hand the finalized JSON to `$create-cn-official-pdf`; do not duplicate its typesetting rules here.

## Non-negotiable rules

- One request, one matter: a 请示 holds one matter and one principal recipient; do not copy a request to a subordinate.
- A 报告 must not embed a request for approval. If approval is needed, use a 请示 instead.
- Direction must match authority: do not issue a command beyond statutory powers; do not address an official personally unless the rules allow it.
- Do not fabricate policy bases, approval status, consultations, meeting decisions, issuing authority, signers, or effective dates.
- Punctuation: full-width Chinese punctuation in prose; hexagonal brackets `〔〕` for the document number—never `[]`, `【】`, or parentheses.
- Numerals: follow GB/T 15835; do not impose “all Arabic” without context. Dates use full Arabic year/month/day without zero-padding (e.g. `2026年7月24日`).
- Headings keep their sequence and typefaces: `一、` → `（一）` → `1.` → `（1）`; a standalone heading has no terminal punctuation.
- Cite laws, rules, and named documents in book-title marks `《》` where grammatically appropriate; verify every title.

## Handoff

The emitted JSON is the contract with `$create-cn-official-pdf`. Include `format` (`general` | `upward` | `letter` | `order` | `minutes`) and, for `upward`, the signer name(s). Leave `seal_image` null unless the user supplies an authorized asset. This skill does not decide fonts, margins, or page geometry—those belong to the renderer.
