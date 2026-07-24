---
"mmhsdxwdxx-skills": patch
---

Consolidate the PDF generator into a single implementation and tighten the skill prose.

- Merge the live `render_pdf` and `draw_edition_record` from the entry point into `_official_pdf_impl`; reduce `official_pdf.py` to a thin runner. Removes the monkey-patch that left a divergent, dead copy of both functions in the implementation module.
- Rewrite `SKILL.md` for precision: connect document direction to layout choice, spell out the per-level heading fonts, and name the five layout modes instead of "above".
- Standardize the human-facing doc headings and formalize the Chinese wording.
- Declare Python runtime dependencies in `requirements.txt` and mention them in the skill and docs.
