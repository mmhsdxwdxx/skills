---
"mmhsdxwdxx-skills": minor
---

Add `draft-cn-official-document` and separate content from format.

- New model-invoked skill `draft-cn-official-document`: chooses the document type, sets direction, drafts and preflights content, and emits JSON for `create-cn-official-pdf` to typeset. Ships with `scripts/check_draft.py` (deterministic content preflight) and `assets/templates.json` (starter structures per common type).
- Relocate `document-types-and-writing.md` from the renderer to the drafting skill—it is drafting knowledge—so each skill owns a single source of truth. The renderer now focuses on typesetting and points to the drafting skill for wording.
- Promote the new skill in README, bucket README, docs, and plugin manifest.
