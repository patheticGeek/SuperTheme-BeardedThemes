#!/usr/bin/env bash
# Builds redistributable zip archives of the Bearded Diamond theme:
#
#   - one "SuperTheme" zip with everything (install.sh, README, all themes)
#   - one zip per individual program theme (kde, chrome, firefox, ghostty,
#     zsh, plymouth), each with a short INSTALL.txt of its own
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

### 1. SuperTheme -- everything bundled together ###############################

SUPER_NAME="SuperTheme-BeardedDiamond-${VERSION}"
SUPER_DIR="$STAGE_DIR/$SUPER_NAME"
mkdir -p "$SUPER_DIR"
cp -r "$SCRIPT_DIR"/color-schemes "$SCRIPT_DIR"/icons "$SCRIPT_DIR"/look-and-feel "$SCRIPT_DIR"/plymouth \
      "$SCRIPT_DIR"/chrome-theme "$SCRIPT_DIR"/firefox-theme "$SCRIPT_DIR"/ghostty-theme "$SCRIPT_DIR"/zsh-theme \
      "$SCRIPT_DIR"/install.sh "$SCRIPT_DIR"/README.md "$SCRIPT_DIR"/LICENSE \
      "$SUPER_DIR/"
chmod +x "$SUPER_DIR/install.sh"
zip_dir "$SUPER_DIR" "$OUT_DIR/${SUPER_NAME}.zip"
echo "Built $OUT_DIR/${SUPER_NAME}.zip"

### 2. Per-program zips ##########################################################

make_component() {
    # make_component <component-name> <install-instructions> <src-dir>...
    local component="$1" instructions="$2"
    shift 2
    local pkg_name="${NAME}-${component}-${VERSION}"
    local pkg_dir="$STAGE_DIR/$pkg_name"
    mkdir -p "$pkg_dir"
    for src in "$@"; do
        cp -r "$src" "$pkg_dir/"
    done
    cp "$SCRIPT_DIR/LICENSE" "$pkg_dir/"
    printf '%s\n' "$instructions" > "$pkg_dir/INSTALL.txt"
    zip_dir "$pkg_dir" "$OUT_DIR/${pkg_name}.zip"
    echo "Built $OUT_DIR/${pkg_name}.zip"
}

make_component "kde" "\
Bearded Diamond -- KDE Plasma 6 global theme
=============================================

User install (no root):
  mkdir -p ~/.local/share/color-schemes ~/.local/share/icons ~/.local/share/plasma/look-and-feel
  cp color-schemes/BeardedDiamond.colors ~/.local/share/color-schemes/
  cp -r icons/BeardedIcons ~/.local/share/icons/
  cp -r look-and-feel/org.kde.beardeddiamond.desktop ~/.local/share/plasma/look-and-feel/

Then apply it via System Settings > Appearance > Global Themes > Bearded Diamond,
or run: plasma-apply-lookandfeel -a org.kde.beardeddiamond.desktop

For a system-wide install, use /usr/share/... instead of ~/.local/share/... (needs sudo)." \
    "$SCRIPT_DIR/color-schemes" "$SCRIPT_DIR/icons" "$SCRIPT_DIR/look-and-feel"

make_component "chrome" "\
Bearded Diamond -- Chrome theme
================================

1. Go to chrome://extensions
2. Enable Developer mode (top right)
3. Click \"Load unpacked\" and select this folder

Works in Chromium-based browsers too (Brave, Vivaldi, Edge, ...)." \
    "$SCRIPT_DIR/chrome-theme"

make_component "firefox" "\
Bearded Diamond -- Firefox theme
=================================

1. Go to about:debugging#/runtime/this-firefox
2. Click \"Load Temporary Add-on...\" and select manifest.json

Temporary add-ons are removed when Firefox restarts. For a permanent
install, sign the theme via addons.mozilla.org, or run Firefox Developer
Edition/Nightly with xpinstall.signatures.required set to false." \
    "$SCRIPT_DIR/firefox-theme"

make_component "ghostty" "\
Bearded Diamond -- Ghostty terminal theme
==========================================

mkdir -p ~/.config/ghostty/themes
cp BeardedDiamond ~/.config/ghostty/themes/

Then add to your Ghostty config:
  theme = BeardedDiamond" \
    "$SCRIPT_DIR/ghostty-theme"

make_component "zsh" "\
Bearded Diamond -- zsh prompt theme
=====================================

oh-my-zsh:
  mkdir -p ~/.oh-my-zsh/custom/themes
  cp beardeddiamond.zsh-theme ~/.oh-my-zsh/custom/themes/
  # then in ~/.zshrc: ZSH_THEME=\"beardeddiamond\"

plain zsh:
  mkdir -p ~/.config/zsh/themes
  cp beardeddiamond.zsh-theme ~/.config/zsh/themes/
  # then in ~/.zshrc: source ~/.config/zsh/themes/beardeddiamond.zsh-theme" \
    "$SCRIPT_DIR/zsh-theme"

make_component "plymouth" "\
Bearded Diamond -- Plymouth boot splash
=========================================

This is a system-level, root-owned change that affects every boot and
requires rebuilding your initramfs. Review beardeddiamond.plymouth before
installing.

  sudo mkdir -p /usr/share/plymouth/themes/beardeddiamond
  sudo cp * /usr/share/plymouth/themes/beardeddiamond/
  sudo plymouth-set-default-theme -R beardeddiamond" \
    "$SCRIPT_DIR/plymouth/beardeddiamond/."

rm -rf "$STAGE_DIR"

echo
echo "All packages built in $OUT_DIR:"
ls -1 "$OUT_DIR"
