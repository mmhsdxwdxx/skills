# Contributing

## Add a skill

1. Choose a bucket under `skills/`.
2. Create `skills/<bucket>/<skill-name>/SKILL.md` and `agents/openai.yaml`.
3. Add only resources the skill actually uses: `scripts/`, `references/`, or `assets/`.
4. For a promoted bucket, add a human-facing page under `docs/<bucket>/` and update all indexes.
5. Run `python scripts/validate_skills.py`.
6. Add a Changeset with `npx changeset`.

Use lowercase letters, digits, and hyphens for skill names. Do not include secrets, personal data, real seals, proprietary fonts, generated PDFs, or copied third-party skill content without a compatible license and attribution.
