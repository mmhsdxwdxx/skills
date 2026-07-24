#!/usr/bin/env python3
"""Validate repository invariants without third-party Python dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
PROMOTED = {"official", "engineering", "productivity"}
ALLOWED_FRONTMATTER = {"name", "description", "disable-model-invocation"}
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"(?:gho_|ghp_|github_pat_)[A-Za-z0-9_]{12,}"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "local user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.IGNORECASE),
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("missing closing YAML frontmatter delimiter")
    values: dict[str, str] = {}
    for raw in parts[1].splitlines():
        if not raw.strip() or raw.startswith((" ", "\t")):
            continue
        if ":" not in raw:
            raise ValueError(f"invalid frontmatter line: {raw!r}")
        key, value = raw.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def fail(errors: list[str], path: Path | str, message: str) -> None:
    errors.append(f"{path}: {message}")


def main() -> int:
    errors: list[str] = []
    skill_mds = sorted(SKILLS.glob("*/*/SKILL.md"))
    if not skill_mds:
        errors.append("No skills found under skills/<bucket>/<name>/SKILL.md")

    names: dict[str, Path] = {}
    promoted_paths: set[str] = set()
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    plugin_skills = set(plugin.get("skills", []))

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if package.get("version") != plugin.get("version"):
        fail(errors, "package.json", "version must match .claude-plugin/plugin.json")

    for skill_md in skill_mds:
        bucket = skill_md.parents[1].name
        skill_dir = skill_md.parent
        folder_name = skill_dir.name
        rel = skill_md.relative_to(ROOT).as_posix()
        try:
            frontmatter = parse_frontmatter(skill_md)
        except Exception as exc:
            fail(errors, rel, str(exc))
            continue

        unknown = set(frontmatter) - ALLOWED_FRONTMATTER
        if unknown:
            fail(errors, rel, f"unsupported frontmatter keys: {sorted(unknown)}")
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if name != folder_name:
            fail(errors, rel, f"frontmatter name {name!r} must match directory {folder_name!r}")
        if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
            fail(errors, rel, "name must use lowercase letters, digits, and hyphens")
        if not description:
            fail(errors, rel, "description is required")
        if name in names:
            fail(errors, rel, f"duplicate skill name also used by {names[name]}")
        names[name] = skill_md

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if not openai_yaml.is_file():
            fail(errors, rel, "agents/openai.yaml is required")
        else:
            ui_text = openai_yaml.read_text(encoding="utf-8")
            if "display_name:" not in ui_text or "short_description:" not in ui_text:
                fail(errors, openai_yaml.relative_to(ROOT), "display_name and short_description are required")
            if f"${name}" not in ui_text:
                fail(errors, openai_yaml.relative_to(ROOT), f"default_prompt must mention ${name}")
            user_invoked = frontmatter.get("disable-model-invocation", "").lower() == "true"
            implicit_disabled = bool(re.search(r"allow_implicit_invocation:\s*false", ui_text))
            if user_invoked != implicit_disabled:
                fail(errors, openai_yaml.relative_to(ROOT), "Claude and Codex invocation flags are out of sync")

        for json_file in skill_dir.rglob("*.json"):
            try:
                json.loads(json_file.read_text(encoding="utf-8"))
            except Exception as exc:
                fail(errors, json_file.relative_to(ROOT), f"invalid JSON: {exc}")
        for py_file in skill_dir.rglob("*.py"):
            try:
                compile(py_file.read_text(encoding="utf-8"), str(py_file), "exec")
            except Exception as exc:
                fail(errors, py_file.relative_to(ROOT), f"Python syntax error: {exc}")

        if bucket in PROMOTED:
            plugin_ref = f"./skills/{bucket}/{name}"
            promoted_paths.add(plugin_ref)
            root_ref = f"./skills/{bucket}/{name}/SKILL.md"
            if root_ref not in root_readme:
                fail(errors, "README.md", f"missing promoted skill link {root_ref}")
            bucket_readme = skill_dir.parents[0] / "README.md"
            if not bucket_readme.is_file() or f"./{name}/SKILL.md" not in bucket_readme.read_text(encoding="utf-8"):
                fail(errors, bucket_readme.relative_to(ROOT), f"missing link for {name}")
            docs = ROOT / "docs" / bucket / f"{name}.md"
            if not docs.is_file():
                fail(errors, docs.relative_to(ROOT), "promoted skill requires a human-facing docs page")

    if plugin_skills != promoted_paths:
        fail(
            errors,
            plugin_path.relative_to(ROOT),
            f"skills list differs from promoted set; expected {sorted(promoted_paths)}, got {sorted(plugin_skills)}",
        )

    forbidden_suffixes = {".pem", ".key", ".p12", ".pfx", ".pyc"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "node_modules" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        if path.suffix.lower() in forbidden_suffixes or "__pycache__" in path.parts:
            fail(errors, rel, "forbidden generated or secret-bearing file")
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".md", ".py", ".ps1", ".sh", ".json", ".yaml", ".yml", ".txt"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    fail(errors, rel, f"possible {label} detected")

    if errors:
        print("Skill repository validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validated {len(skill_mds)} skill(s); {len(promoted_paths)} promoted; no errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
