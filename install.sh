#!/usr/bin/env bash
# Installs Bearded Diamond theme variant(s): KDE Plasma global theme,
# Ghostty terminal theme, and zsh prompt theme.
#
# By default installs every variant under themes/ into the current user's
# XDG data dirs (no root needed) and covers everything except the Plymouth
# boot splash, which lives outside the user session and requires root + an
# initramfs rebuild to take effect. The Chrome and Firefox themes are
# browser extensions, loaded manually -- see README.md.
#
# Usage:
#   ./install.sh                 install color scheme, icons, global theme,
#                                 Ghostty theme, zsh theme (user-level) for
#                                 every variant under themes/
#   ./install.sh --theme=<slug>  only install the named variant (see
#                                 themes/ for available slugs)
#   ./install.sh --apply         also apply the KDE global theme immediately
#                                 (only valid with a single variant, explicit
#                                 or the only one present)
#   ./install.sh --system        install user-level components system-wide instead (needs sudo)
#   ./install.sh --with-plymouth also install the Plymouth boot theme (needs sudo, rebuilds initramfs)
#   ./install.sh --help          show this text

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPLY=0
SYSTEM=0
WITH_PLYMOUTH=0
ONLY_THEME=""

for arg in "$@"; do
    case "$arg" in
        --apply) APPLY=1 ;;
        --system) SYSTEM=1 ;;
        --with-plymouth) WITH_PLYMOUTH=1 ;;
        --theme=*) ONLY_THEME="${arg#--theme=}" ;;
        --help|-h)
            sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            echo "Unknown option: $arg" >&2
            exit 1
            ;;
    esac
done

if [ "$SYSTEM" -eq 1 ]; then
    COLOR_SCHEME_DIR="/usr/share/color-schemes"
    ICON_DIR="/usr/share/icons"
    LOOKANDFEEL_DIR="/usr/share/plasma/look-and-feel"
    NEED_SUDO=1
else
    COLOR_SCHEME_DIR="$HOME/.local/share/color-schemes"
    ICON_DIR="$HOME/.local/share/icons"
    LOOKANDFEEL_DIR="$HOME/.local/share/plasma/look-and-feel"
    NEED_SUDO=0
fi

run() {
    if [ "$NEED_SUDO" -eq 1 ]; then
        sudo "$@"
    else
        "$@"
    fi
}

echo "==> Installing icon theme to $ICON_DIR/BeardedIcons"
run mkdir -p "$ICON_DIR"
run cp -r "$SCRIPT_DIR/icons/BeardedIcons" "$ICON_DIR/"
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    run gtk-update-icon-cache --force --ignore-theme-index "$ICON_DIR/BeardedIcons" || true
fi

THEME_DIRS=()
if [ -n "$ONLY_THEME" ]; then
    if [ ! -d "$SCRIPT_DIR/themes/$ONLY_THEME" ]; then
        echo "error: no theme variant '$ONLY_THEME' under themes/" >&2
        exit 1
    fi
    THEME_DIRS=("$SCRIPT_DIR/themes/$ONLY_THEME")
else
    for d in "$SCRIPT_DIR"/themes/*/; do
        THEME_DIRS+=("${d%/}")
    done
fi

APPLY_ID=""
for THEME_DIR in "${THEME_DIRS[@]}"; do
    SLUG="$(basename "$THEME_DIR")"
    echo "==> Installing theme variant: $SLUG"

    COLORS_FILE=$(find "$THEME_DIR/color-schemes" -maxdepth 1 -name '*.colors' | head -n1)
    echo "    color scheme -> $COLOR_SCHEME_DIR"
    run mkdir -p "$COLOR_SCHEME_DIR"
    run cp "$COLORS_FILE" "$COLOR_SCHEME_DIR/"

    LOOKANDFEEL_PKG=$(find "$THEME_DIR/look-and-feel" -maxdepth 1 -mindepth 1 -type d | head -n1)
    LOOKANDFEEL_ID="$(basename "$LOOKANDFEEL_PKG")"
    echo "    global theme -> $LOOKANDFEEL_DIR/$LOOKANDFEEL_ID"
    run mkdir -p "$LOOKANDFEEL_DIR"
    run cp -r "$LOOKANDFEEL_PKG" "$LOOKANDFEEL_DIR/"

    GHOSTTY_FILE=$(find "$THEME_DIR/ghostty-theme" -maxdepth 1 -type f | head -n1)
    GHOSTTY_THEMES_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/themes"
    echo "    Ghostty theme -> $GHOSTTY_THEMES_DIR"
    mkdir -p "$GHOSTTY_THEMES_DIR"
    cp "$GHOSTTY_FILE" "$GHOSTTY_THEMES_DIR/"

    ZSH_FILE=$(find "$THEME_DIR/zsh-theme" -maxdepth 1 -type f | head -n1)
    if [ -d "$HOME/.oh-my-zsh" ]; then
        ZSH_THEME_DIR="$HOME/.oh-my-zsh/custom/themes"
    else
        ZSH_THEME_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/zsh/themes"
    fi
    echo "    zsh theme -> $ZSH_THEME_DIR"
    mkdir -p "$ZSH_THEME_DIR"
    cp "$ZSH_FILE" "$ZSH_THEME_DIR/"

    if [ "$WITH_PLYMOUTH" -eq 1 ]; then
        PLYMOUTH_THEME_DIR=$(find "$THEME_DIR/plymouth" -maxdepth 1 -mindepth 1 -type d | head -n1)
        PLYMOUTH_ID="$(basename "$PLYMOUTH_THEME_DIR")"
        echo "    Plymouth boot theme -> /usr/share/plymouth/themes/$PLYMOUTH_ID (needs sudo, rebuilds initramfs)"
        sudo mkdir -p "/usr/share/plymouth/themes/$PLYMOUTH_ID"
        sudo cp "$PLYMOUTH_THEME_DIR"/* "/usr/share/plymouth/themes/$PLYMOUTH_ID/"
        if command -v plymouth-set-default-theme >/dev/null 2>&1; then
            sudo plymouth-set-default-theme -R "$PLYMOUTH_ID"
        else
            echo "    plymouth-set-default-theme not found; install/enable Plymouth manually, then run:"
            echo "      sudo plymouth-set-default-theme -R $PLYMOUTH_ID"
        fi
    fi

    APPLY_ID="$LOOKANDFEEL_ID"
    echo "    Chrome theme:  chrome://extensions > Developer mode > Load unpacked > $THEME_DIR/chrome-theme/"
    echo "    Firefox theme: about:debugging > This Firefox > Load Temporary Add-on > $THEME_DIR/firefox-theme/manifest.json"
done

if command -v kbuildsycoca6 >/dev/null 2>&1; then
    kbuildsycoca6 >/dev/null 2>&1 || true
fi

if [ "$APPLY" -eq 1 ]; then
    if [ "${#THEME_DIRS[@]}" -ne 1 ]; then
        echo "error: --apply requires exactly one theme variant -- pass --theme=<slug>" >&2
        exit 1
    fi
    echo "==> Applying the $APPLY_ID global theme"
    if command -v plasma-apply-lookandfeel >/dev/null 2>&1; then
        plasma-apply-lookandfeel -a "$APPLY_ID"
    else
        echo "    plasma-apply-lookandfeel not found; apply manually via System Settings > Appearance > Global Themes."
    fi
fi

echo "==> Done."
[ "$APPLY" -eq 0 ] && echo "    Apply a theme via System Settings > Appearance > Global Themes, or re-run with --theme=<slug> --apply."
[ "$WITH_PLYMOUTH" -eq 0 ] && echo "    Boot splash not installed; re-run with --with-plymouth to install it."
