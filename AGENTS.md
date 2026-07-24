# Repository instructions

This repository is a governed collection of Agent Skills.

## Source of truth

- `skills/**/SKILL.md` contains executable agent instructions.
- `agents/openai.yaml` beside each skill contains Codex UI and invocation metadata.
- `docs/<bucket>/<skill>.md` contains human-facing orientation for promoted skills.
- `README.md`, each promoted bucket README, and `.claude-plugin/plugin.json` are synchronized indexes.

## Buckets

- Promoted: `official`, `engineering`, `productivity`.
- Not promoted: `in-progress`, `deprecated`.
- Only promoted skills appear in the root README, bucket README, docs tree, and plugin manifest.
- Deprecated skills remain for history but are excluded from installers.

## Invocation

Read [.agents/invocation.md](./.agents/invocation.md) before adding or changing a skill.

- User-invoked skills set `disable-model-invocation: true` in `SKILL.md` frontmatter and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
- Model-invoked skills omit both flags and use a rich, model-facing trigger description.

## Adding or changing a skill

1. Keep frontmatter `name` identical to the skill directory name.
2. Keep `SKILL.md` concise; put detailed standards in `references/`, deterministic operations in `scripts/`, and reusable output material in `assets/`.
3. For promoted skills, update the root README, the bucket README, `docs/<bucket>/<name>.md`, and `.claude-plugin/plugin.json`.
4. Never commit credentials, tokens, private documents, personal information, real official seals, generated PDFs, or font files without redistribution rights.
5. Run `python scripts/validate_skills.py` and any skill-specific tests.
6. Add a Changeset when behavior, distribution, or public documentation changes.

## Quality bar

- Instructions are imperative and operational.
- Trigger descriptions name both intended use and boundaries.
- Scripts fail loudly and produce auditable reports.
- Examples are fictional and contain no sensitive data.
- Local paths are never embedded in committed outputs.
