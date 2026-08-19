#!/usr/bin/env bash
# Builds a single redistributable "SuperTheme" zip with everything:
# install.sh, README, LICENSE, the shared icon theme, and every theme
# variant under themes/.
#
# Usage: ./package.sh [version]
#   version defaults to the short git commit hash, or "dev" outside a repo.
#
# Uses Python's zipfile module rather than the `zip` CLI so it doesn't
# depend on `zip` being installed.

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
mkdir -p "$OUT_DIR"

zip_dir() {
    # zip_dir <staged-dir> <output.zip>
    # Zips <staged-dir> with its own basename as the top-level folder in
    # the archive, preserving unix file permissions (so install.sh stays
    # executable after extraction).
    python3 - "$1" "$2" <<'PY'
import os
import sys
import zipfile

src, out = sys.argv[1], sys.argv[2]
base = os.path.basename(src.rstrip("/"))
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(src):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(root, name)
            rel = os.path.join(base, os.path.relpath(full, src))
            zi = zipfile.ZipInfo(rel)
            zi.external_attr = (os.stat(full).st_mode & 0xFFFF) << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(full, "rb") as f:
                zf.writestr(zi, f.read())
PY
}

SUPER_NAME="SuperTheme-${NAME}-${VERSION}"
SUPER_DIR="$STAGE_DIR/$SUPER_NAME"
mkdir -p "$SUPER_DIR"
cp -r "$SCRIPT_DIR"/icons "$SCRIPT_DIR"/themes \
      "$SCRIPT_DIR"/install.sh "$SCRIPT_DIR"/README.md "$SCRIPT_DIR"/LICENSE \
      "$SUPER_DIR/"
chmod +x "$SUPER_DIR/install.sh"
zip_dir "$SUPER_DIR" "$OUT_DIR/${SUPER_NAME}.zip"
echo "Built $OUT_DIR/${SUPER_NAME}.zip"

rm -rf "$STAGE_DIR"

echo
echo "Package built in $OUT_DIR:"
ls -1 "$OUT_DIR"
