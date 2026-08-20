#!/usr/bin/env bash
# Builds the two generated trees -- icons/BeardedIcons (shared) and
# themes/<slug>/ for every variant in scripts/theme_spec.py's REGISTRY -- from
# the currently-vendored submodules.
#
# Both are gitignored, so run this after a fresh clone (or whenever a vendor/
# submodule changes) before using ./install-dev.sh or ./package.sh. It rebuilds
# the icon theme from vendor/bearded-icons, builds vendor/bearded-theme's VS
# Code output if it isn't already built, then regenerates every registered
# variant's color-derived artifacts from it.
#
# Usage: ./scripts/build-all.sh
#
# Requires: node+npm (to build the upstream theme), python3 with Pillow.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
VENDOR_DIR="$REPO_ROOT/vendor/bearded-theme"

echo "==> Rebuilding icons/BeardedIcons from vendor/bearded-icons"
python3 "$SCRIPT_DIR/gen_icons.py"

if [ ! -d "$VENDOR_DIR/dist/vscode/themes" ] || [ -z "$(ls -A "$VENDOR_DIR/dist/vscode/themes" 2>/dev/null)" ]; then
    echo "==> Building upstream VS Code themes"
    ( cd "$VENDOR_DIR" && npm install --no-audit --no-fund && npm run build:vscode )
fi

SLUGS="$(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from theme_spec import REGISTRY
for spec in REGISTRY:
    print(spec.slug)
")"

while IFS= read -r SLUG; do
    [ -z "$SLUG" ] && continue
    UPSTREAM_SLUG="$(python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from theme_spec import get; print(get('$SLUG').upstream_slug)")"
    THEME_JSON="$VENDOR_DIR/dist/vscode/themes/bearded-theme-$UPSTREAM_SLUG.json"
    if [ ! -f "$THEME_JSON" ]; then
        echo "error: expected theme output not found at $THEME_JSON" >&2
        exit 1
    fi
    echo "==> Regenerating '$SLUG' from $THEME_JSON"
    python3 "$SCRIPT_DIR/regenerate.py" "$THEME_JSON" "$SLUG"
done <<< "$SLUGS"

echo
echo "Icon theme built at $REPO_ROOT/icons/BeardedIcons"
echo "All registered variants built under $REPO_ROOT/themes/"
