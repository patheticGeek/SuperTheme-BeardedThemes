#!/usr/bin/env bash
# Pulls the latest vendor/bearded-theme, builds its VS Code theme JSON, and
# regenerates every color-derived artifact in this repo from it.
#
# This does NOT commit anything -- it leaves you with a working tree diff to
# review. It also does not touch icons/BeardedIcons (ported from the
# separate bearded-icons extension, updated manually).
#
# Requires: git, node+npm (to build the upstream theme), python3 with Pillow.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
VENDOR_DIR="$REPO_ROOT/vendor/bearded-theme"

echo "==> Updating vendor/bearded-theme submodule to latest upstream"
git -C "$REPO_ROOT" submodule update --remote --merge vendor/bearded-theme

echo "==> Installing upstream dependencies"
( cd "$VENDOR_DIR" && npm install --no-audit --no-fund )

echo "==> Building upstream VS Code themes"
( cd "$VENDOR_DIR" && npm run build:vscode )

THEME_JSON="$VENDOR_DIR/dist/vscode/themes/bearded-theme-black-&-diamond.json"
if [ ! -f "$THEME_JSON" ]; then
    echo "error: expected theme output not found at $THEME_JSON" >&2
    echo "The upstream build layout may have changed -- check vendor/bearded-theme/src/generators/vscode/index.ts" >&2
    exit 1
fi

echo "==> Regenerating derived artifacts from $THEME_JSON"
python3 "$SCRIPT_DIR/regenerate.py" "$THEME_JSON"

echo "==> Upstream commit now vendored:"
git -C "$VENDOR_DIR" log -1 --oneline

echo "==> Diff summary:"
git -C "$REPO_ROOT" diff --stat
