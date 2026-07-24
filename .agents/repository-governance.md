# Repository governance

## Promotion lifecycle

1. Develop under `skills/in-progress/<name>`.
2. Validate on realistic requests and inspect emitted artifacts.
3. Promote to `official`, `engineering`, or `productivity`.
4. Add the skill to the root README, bucket README, docs tree, and plugin manifest in the same change.
5. Add a Changeset and let the release workflow create the version PR/tag.
6. Move obsolete skills to `deprecated`; do not delete history unless it contains unsafe material.

## Single sources of truth

- Agent behavior: `SKILL.md`.
- Detailed domain knowledge: the owning skill's `references/`.
- Deterministic automation: the owning skill's `scripts/`.
- Human selection guidance: `docs/`.
- Distribution set: `.claude-plugin/plugin.json` plus the promoted bucket rules.

## Security boundary

Treat every skill as executable supply-chain content. Review scripts, shell commands, dependencies, URLs, and bundled assets. Reject secrets, credentials, private documents, real seals, unlicensed fonts, opaque binaries, and unexplained network calls.
