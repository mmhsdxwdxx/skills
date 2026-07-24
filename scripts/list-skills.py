#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in sorted((root / "skills").glob("*/*/SKILL.md")):
    print(path.relative_to(root).as_posix())
