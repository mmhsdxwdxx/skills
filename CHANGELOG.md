# Changelog

## 0.2.0

### Minor Changes

- [#2](https://github.com/mmhsdxwdxx/skills/pull/2) [`716a024`](https://github.com/mmhsdxwdxx/skills/commit/716a0242b85c9785aa136e2c3a0459c33b4e1797) Thanks [@mmhsdxwdxx](https://github.com/mmhsdxwdxx)! - Add `draft-cn-official-document` and separate content from format.

  - New model-invoked skill `draft-cn-official-document`: chooses the document type, sets direction, drafts and preflights content, and emits JSON for `create-cn-official-pdf` to typeset. Ships with `scripts/check_draft.py` (deterministic content preflight) and `assets/templates.json` (starter structures per common type).
  - Relocate `document-types-and-writing.md` from the renderer to the drafting skill—it is drafting knowledge—so each skill owns a single source of truth. The renderer now focuses on typesetting and points to the drafting skill for wording.
  - Promote the new skill in README, bucket README, docs, and plugin manifest.

### Patch Changes

- [#1](https://github.com/mmhsdxwdxx/skills/pull/1) [`6461aa9`](https://github.com/mmhsdxwdxx/skills/commit/6461aa91a4df49407c4353fcb2ea50729dd79478) Thanks [@mmhsdxwdxx](https://github.com/mmhsdxwdxx)! - Consolidate the PDF generator into a single implementation and tighten the skill prose.

  - Merge the live `render_pdf` and `draw_edition_record` from the entry point into `_official_pdf_impl`; reduce `official_pdf.py` to a thin runner. Removes the monkey-patch that left a divergent, dead copy of both functions in the implementation module.
  - Rewrite `SKILL.md` for precision: connect document direction to layout choice, spell out the per-level heading fonts, and name the five layout modes instead of "above".
  - Standardize the human-facing doc headings and formalize the Chinese wording.
  - Declare Python runtime dependencies in `requirements.txt` and mention them in the skill and docs.

## 0.1.0

- Establish the personal skills collection and repository governance.
- Add `create-cn-official-pdf` as the first promoted skill.
