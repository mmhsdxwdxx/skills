#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("${HOME}/.agents/skills" "${HOME}/.claude/skills")
BUCKETS=(official engineering productivity)

for DEST in "${DESTS[@]}"; do
  mkdir -p "$DEST"
  for BUCKET in "${BUCKETS[@]}"; do
    [ -d "$REPO/skills/$BUCKET" ] || continue
    while IFS= read -r -d '' SKILL_MD; do
      SRC="$(dirname "$SKILL_MD")"
      NAME="$(basename "$SRC")"
      TARGET="$DEST/$NAME"
      if [ -e "$TARGET" ] && [ ! -L "$TARGET" ]; then
        echo "warning: skipping real directory $TARGET" >&2
        continue
      fi
      ln -sfn "$SRC" "$TARGET"
      echo "linked $NAME -> $SRC ($DEST)"
    done < <(find "$REPO/skills/$BUCKET" -name SKILL.md -print0)
  done
done
