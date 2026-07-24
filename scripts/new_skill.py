#!/usr/bin/env python3
"""Create a minimal skill scaffold; repository validation identifies required indexes."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--bucket", choices=["official", "engineering", "productivity", "in-progress"], default="in-progress")
    parser.add_argument("--description", required=True)
    parser.add_argument("--user-invoked", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9-]{1,64}", args.name):
        parser.error("name must use lowercase letters, digits, and hyphens")

    root = Path(__file__).resolve().parents[1]
    skill = root / "skills" / args.bucket / args.name
    if skill.exists():
        parser.error(f"already exists: {skill}")
    (skill / "agents").mkdir(parents=True)
    flag = "disable-model-invocation: true\n" if args.user_invoked else ""
    (skill / "SKILL.md").write_text(
        f"---\nname: {args.name}\ndescription: {args.description}\n{flag}---\n\n# {args.name}\n\n## Workflow\n\n1. Replace this scaffold with imperative instructions.\n",
        encoding="utf-8",
    )
    policy = "\npolicy:\n  allow_implicit_invocation: false\n" if args.user_invoked else "\n"
    (skill / "agents" / "openai.yaml").write_text(
        "interface:\n"
        f"  display_name: \"{args.name}\"\n"
        f"  short_description: \"{args.description[:64]}\"\n"
        f"  default_prompt: \"Use ${args.name} to complete this task.\"\n"
        + policy,
        encoding="utf-8",
    )
    print(skill)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
