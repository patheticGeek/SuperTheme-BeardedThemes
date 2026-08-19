#!/usr/bin/env bash
# Builds a redistributable archive of the Bearded Diamond theme that others
# can download, extract, and install via install.sh.
#
# Usage: ./package.sh [version]
#   version defaults to the short git commit hash, or "dev" outside a repo.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAME="BeardedDiamond"

VERSION="${1:-}"
if [ -z "$VERSION" ]; then
    if git -C "$SCRIPT_DIR" rev-parse --short HEAD >/dev/null 2>&1; then
        VERSION="$(git -C "$SCRIPT_DIR" rev-parse --short HEAD)"
    else
        VERSION="dev"
    fi
fi

OUT_DIR="$SCRIPT_DIR/dist"
STAGE_DIR="$(mktemp -d)"
PKG_NAME="${NAME}-${VERSION}"
PKG_DIR="$STAGE_DIR/$PKG_NAME"

mkdir -p "$PKG_DIR"
cp -r "$SCRIPT_DIR"/color-schemes "$SCRIPT_DIR"/icons "$SCRIPT_DIR"/look-and-feel "$SCRIPT_DIR"/plymouth \
      "$SCRIPT_DIR"/install.sh "$SCRIPT_DIR"/README.md "$SCRIPT_DIR"/LICENSE \
      "$PKG_DIR/"
chmod +x "$PKG_DIR/install.sh"

mkdir -p "$OUT_DIR"
ARCHIVE="$OUT_DIR/${PKG_NAME}.tar.gz"
tar -C "$STAGE_DIR" -czf "$ARCHIVE" "$PKG_NAME"
rm -rf "$STAGE_DIR"

echo "Built $ARCHIVE"
echo "Install with:"
echo "  tar xzf $(basename "$ARCHIVE")"
echo "  cd $PKG_NAME && ./install.sh --apply"
