#!/usr/bin/env bash
# Install fe-agent-workflow into a business project.
#
# Usage:
#   ./tools/install.sh <pc|uniapp> <target-project-path> [--with-docs]
#   ./tools/install.sh <pc|uniapp> <target-project-path> --from-git <repo-url> [--ref <branch|tag>] [--with-docs]
#
# Remote install (no local fe-agent-workflow checkout required):
#   bash install.sh uniapp /path/to/project --from-git <repo-url> --with-docs
#
# --from-git supports:
#   - Standalone fe-agent-workflow repo (workflow at repo root) — recommended
#   - AI-Core / parent repo (workflow under fe-agent-workflow/)

set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  install.sh <pc|uniapp> <target-project-path> [options]

Options:
  --with-docs                Sync SDD docs template (constitution, features/_template, etc.)
  --from-git <repo-url>      Shallow-clone workflow from Git instead of local checkout
  --ref <branch|tag>         Git ref when using --from-git (default: remote default branch)

Examples:
  ./tools/install.sh uniapp /path/to/HiStore-mall-mobile
  ./tools/install.sh pc /path/to/HiStore-store-pc --with-docs
  ./tools/install.sh uniapp /path/to/project \
    --from-git https://github.com/TieZhuzhu/fe-agent-workflow.git \
    --with-docs
  ./tools/install.sh uniapp /path/to/project \
    --from-git https://github.com/TieZhuzhu/fe-agent-workflow.git --ref v1.3.3
EOF
  exit 1
}

# Resolve workflow root inside a cloned Git repo.
# Standalone fe-agent-workflow: {pc,uniapp}/.cursor at repo root
# AI-Core / parent: fe-agent-workflow/{pc,uniapp}/.cursor
resolve_workflow_root() {
  local clone_root="$1"
  local platform="$2"

  if [[ -d "$clone_root/$platform/.cursor" ]]; then
    echo "$clone_root"
    return 0
  fi

  if [[ -d "$clone_root/fe-agent-workflow/$platform/.cursor" ]]; then
    echo "$clone_root/fe-agent-workflow"
    return 0
  fi

  echo "Cannot find $platform workflow in cloned repo: $clone_root" >&2
  echo "  Tried: $clone_root/$platform/.cursor" >&2
  echo "  Tried: $clone_root/fe-agent-workflow/$platform/.cursor" >&2
  return 1
}

PLATFORM=""
TARGET=""
WITH_DOCS=false
FROM_GIT=""
GIT_REF=""
TEMP_CLONE=""
ROOT=""

cleanup() {
  if [[ -n "$TEMP_CLONE" && -d "$TEMP_CLONE" ]]; then
    rm -rf "$TEMP_CLONE"
  fi
}
trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-docs)
      WITH_DOCS=true
      shift
      ;;
    --from-git)
      [[ $# -ge 2 ]] || usage
      FROM_GIT="$2"
      shift 2
      ;;
    --ref)
      [[ $# -ge 2 ]] || usage
      GIT_REF="$2"
      shift 2
      ;;
    pc|uniapp)
      if [[ -n "$PLATFORM" ]]; then
        echo "Duplicate platform: $1" >&2
        usage
      fi
      PLATFORM="$1"
      shift
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      ;;
    *)
      if [[ -n "$TARGET" ]]; then
        echo "Unexpected argument: $1" >&2
        usage
      fi
      TARGET="$1"
      shift
      ;;
  esac
done

[[ -n "$PLATFORM" && -n "$TARGET" ]] || usage

if [[ "$PLATFORM" != "pc" && "$PLATFORM" != "uniapp" ]]; then
  echo "Platform must be pc or uniapp" >&2
  exit 1
fi

if [[ -n "$FROM_GIT" ]]; then
  if ! command -v git >/dev/null 2>&1; then
    echo "git is required for --from-git" >&2
    exit 1
  fi
  TEMP_CLONE="$(mktemp -d)"
  echo "Cloning $FROM_GIT (depth=1)..."
  CLONE_ARGS=(--depth 1)
  if [[ -n "$GIT_REF" ]]; then
    CLONE_ARGS+=(--branch "$GIT_REF")
  fi
  git clone "${CLONE_ARGS[@]}" "$FROM_GIT" "$TEMP_CLONE"
  ROOT="$(resolve_workflow_root "$TEMP_CLONE" "$PLATFORM")"
  echo "Resolved workflow root: $ROOT"
  if [[ -n "$GIT_REF" ]]; then
    echo "Using ref: $GIT_REF"
  fi
else
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

SRC_CURSOR="$ROOT/$PLATFORM/.cursor"
SRC_DOCS="$ROOT/$PLATFORM/docs"

if [[ ! -d "$TARGET" ]]; then
  mkdir -p "$TARGET"
fi

TARGET="$(cd "$TARGET" && pwd)"
DEST_CURSOR="$TARGET/.cursor"
DEST_DOCS="$TARGET/docs"

if [[ ! -d "$SRC_CURSOR" ]]; then
  echo "Missing $SRC_CURSOR" >&2
  exit 1
fi

mkdir -p "$DEST_CURSOR"

# Preserve per-project bootstrap output
CONVENTIONS_BACKUP=""
if [[ -f "$DEST_CURSOR/project-conventions.md" ]]; then
  CONVENTIONS_BACKUP="$(mktemp)"
  cp "$DEST_CURSOR/project-conventions.md" "$CONVENTIONS_BACKUP"
fi

rsync -a --delete \
  --exclude='project-conventions.md' \
  "$SRC_CURSOR/" "$DEST_CURSOR/"

if [[ -n "$CONVENTIONS_BACKUP" ]]; then
  cp "$CONVENTIONS_BACKUP" "$DEST_CURSOR/project-conventions.md"
  rm -f "$CONVENTIONS_BACKUP"
  echo "Kept existing project-conventions.md"
fi

echo "Installed .cursor → $DEST_CURSOR (platform: $PLATFORM)"

if $WITH_DOCS; then
  if [[ ! -d "$SRC_DOCS" ]]; then
    echo "No docs at $SRC_DOCS" >&2
    exit 1
  fi
  mkdir -p "$DEST_DOCS"
  rsync -a \
    --exclude='specs/_index.md' \
    --exclude='features/archive/*' \
    --exclude='features/project-refactor' \
    --exclude='features/vue3-migration' \
    "$SRC_DOCS/" "$DEST_DOCS/"
  echo "Synced docs → $DEST_DOCS (excluded generated _index.md)"
fi

echo "Done."
