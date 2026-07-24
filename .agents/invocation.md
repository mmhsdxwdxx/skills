# Invocation model

Every skill has exactly one invocation mode.

## Model-invoked

Use when the model can safely and usefully recognize the task by itself.

- Omit `disable-model-invocation` from `SKILL.md` frontmatter.
- Omit `policy.allow_implicit_invocation` from `agents/openai.yaml`.
- Write a rich `description` that explains what the skill does, when to use it, relevant file types, and distinctive trigger phrases.

## User-invoked

Use for orchestration, consequential actions, or flows the user should deliberately start.

- Add `disable-model-invocation: true` to `SKILL.md` frontmatter.
- Add this to `agents/openai.yaml`:

  ```yaml
  policy:
    allow_implicit_invocation: false
  ```

- Keep the description human-facing and concise.

## Dependencies

Refer to sibling skills by name in prose, for example `Run $skill-name`, instead of deep relative links into another skill's resources. A user-invoked skill may orchestrate model-invoked skills; do not make one user-invoked skill silently trigger another.
