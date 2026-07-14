#!/usr/bin/env bash
# One-shot install from remote fe-agent-workflow — no local checkout required.
#
# Usage:
#   bash remote-install.sh <pc|uniapp> <target-project-path> [--with-docs] [--ref <branch|tag>]
#
# Environment:
#   FE_AGENT_WORKFLOW_GIT_URL   Override default Git URL
#   AI_CORE_GIT_URL             Legacy alias (still supported)
#
# Example:
#   bash remote-install.sh uniapp /path/to/HiStore-mall-mobile --with-docs
#
# Curl one-liner (from GitHub raw):
#   curl -fsSL https://raw.githubusercontent.com/TieZhuzhu/fe-agent-workflow/master/tools/remote-install.sh \
#     | bash -s -- uniapp /path/to/project --with-docs

set -euo pipefail

DEFAULT_REPO="https://github.com/TieZhuzhu/fe-agent-workflow.git"
REPO_URL="${FE_AGENT_WORKFLOW_GIT_URL:-${AI_CORE_GIT_URL:-$DEFAULT_REPO}}"

usage() {
  cat >&2 <<'EOF'
Usage:
  remote-install.sh <pc|uniapp> <target-project-path> [options]

Options:
  --with-docs          Sync SDD docs template
  --ref <branch|tag>   Git ref to install (default: remote default branch)

Environment:
  FE_AGENT_WORKFLOW_GIT_URL   Workflow repository URL (optional)
  AI_CORE_GIT_URL             Legacy alias for the same override

Example:
  bash remote-install.sh uniapp /path/to/HiStore-mall-mobile --with-docs
EOF
  exit 1
}

# Resolve install.sh inside a cloned Git repo.
# Standalone fe-agent-workflow: tools/install.sh at repo root
# AI-Core: fe-agent-workflow/tools/install.sh
resolve_install_sh() {
  local clone_root="$1"

  if [[ -f "$clone_root/tools/install.sh" ]]; then
    echo "$clone_root/tools/install.sh"
    return 0
  fi

  if [[ -f "$clone_root/fe-agent-workflow/tools/install.sh" ]]; then
    echo "$clone_root/fe-agent-workflow/tools/install.sh"
    return 0
  fi

  echo "Cannot find tools/install.sh in cloned repo: $clone_root" >&2
  echo "  Tried: $clone_root/tools/install.sh" >&2
  echo "  Tried: $clone_root/fe-agent-workflow/tools/install.sh" >&2
  return 1
}

PLATFORM=""
TARGET=""
WITH_DOCS=false
GIT_REF=""
TEMP_CLONE=""

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
    --ref)
      [[ $# -ge 2 ]] || usage
      GIT_REF="$2"
      shift 2
      ;;
    pc|uniapp)
      [[ -z "$PLATFORM" ]] || usage
      PLATFORM="$1"
      shift
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      ;;
    *)
      [[ -z "$TARGET" ]] || usage
      TARGET="$1"
      shift
      ;;
  esac
done

[[ -n "$PLATFORM" && -n "$TARGET" ]] || usage

if ! command -v git >/dev/null 2>&1; then
  echo "git is required" >&2
  exit 1
fi

TEMP_CLONE="$(mktemp -d)"
echo "Cloning $REPO_URL (depth=1)..."
CLONE_ARGS=(--depth 1)
if [[ -n "$GIT_REF" ]]; then
  CLONE_ARGS+=(--branch "$GIT_REF")
fi
git clone "${CLONE_ARGS[@]}" "$REPO_URL" "$TEMP_CLONE"

INSTALL_SH="$(resolve_install_sh "$TEMP_CLONE")"

INSTALL_ARGS=("$PLATFORM" "$TARGET")
if $WITH_DOCS; then
  INSTALL_ARGS+=(--with-docs)
fi

bash "$INSTALL_SH" "${INSTALL_ARGS[@]}"
echo "Remote install complete. Temporary clone cleaned up."
