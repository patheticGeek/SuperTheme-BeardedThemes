#!/usr/bin/env bash
# Installs the Bearded Diamond theme: KDE Plasma global theme, Ghostty
# terminal theme, and zsh prompt theme.
#
# By default installs into the current user's XDG data dirs (no root needed)
# and covers everything except the Plymouth boot splash, which lives outside
# the user session and requires root + an initramfs rebuild to take effect.
# The Chrome and Firefox themes are browser extensions, loaded manually --
# see README.md.
#
# Usage:
#   ./install.sh                 install color scheme, icons, global theme,
#                                 Ghostty theme, zsh theme (user-level)
#   ./install.sh --apply         also apply the KDE global theme immediately
#   ./install.sh --system        install user-level components system-wide instead (needs sudo)
#   ./install.sh --with-plymouth also install the Plymouth boot theme (needs sudo, rebuilds initramfs)
#   ./install.sh --help          show this text

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPLY=0
SYSTEM=0
WITH_PLYMOUTH=0

for arg in "$@"; do
    case "$arg" in
        --apply) APPLY=1 ;;
        --system) SYSTEM=1 ;;
        --with-plymouth) WITH_PLYMOUTH=1 ;;
        --help|-h)
            sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'
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

echo "==> Installing color scheme to $COLOR_SCHEME_DIR"
run mkdir -p "$COLOR_SCHEME_DIR"
run cp "$SCRIPT_DIR/color-schemes/BeardedDiamond.colors" "$COLOR_SCHEME_DIR/"

echo "==> Installing icon theme to $ICON_DIR/BeardedIcons"
run mkdir -p "$ICON_DIR"
run cp -r "$SCRIPT_DIR/icons/BeardedIcons" "$ICON_DIR/"
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    run gtk-update-icon-cache --force --ignore-theme-index "$ICON_DIR/BeardedIcons" || true
fi

echo "==> Installing global theme (colors, icons, Plasma splash) to $LOOKANDFEEL_DIR"
run mkdir -p "$LOOKANDFEEL_DIR"
run cp -r "$SCRIPT_DIR/look-and-feel/org.kde.beardeddiamond.desktop" "$LOOKANDFEEL_DIR/"

if command -v kbuildsycoca6 >/dev/null 2>&1; then
    kbuildsycoca6 >/dev/null 2>&1 || true
fi

echo "==> Installing Ghostty theme to \$XDG_CONFIG_HOME/ghostty/themes"
GHOSTTY_THEMES_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/themes"
mkdir -p "$GHOSTTY_THEMES_DIR"
cp "$SCRIPT_DIR/ghostty-theme/BeardedDiamond" "$GHOSTTY_THEMES_DIR/"
echo "    Set 'theme = BeardedDiamond' in your ghostty config to use it."

echo "==> Installing zsh prompt theme"
if [ -d "$HOME/.oh-my-zsh" ]; then
    ZSH_THEME_DIR="$HOME/.oh-my-zsh/custom/themes"
    mkdir -p "$ZSH_THEME_DIR"
    cp "$SCRIPT_DIR/zsh-theme/beardeddiamond.zsh-theme" "$ZSH_THEME_DIR/"
    echo "    Installed to $ZSH_THEME_DIR. Set ZSH_THEME=\"beardeddiamond\" in ~/.zshrc to use it."
else
    ZSH_THEME_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/zsh/themes"
    mkdir -p "$ZSH_THEME_DIR"
    cp "$SCRIPT_DIR/zsh-theme/beardeddiamond.zsh-theme" "$ZSH_THEME_DIR/"
    echo "    Installed to $ZSH_THEME_DIR. Add 'source $ZSH_THEME_DIR/beardeddiamond.zsh-theme' to ~/.zshrc to use it."
fi

if [ "$WITH_PLYMOUTH" -eq 1 ]; then
    echo "==> Installing Plymouth boot theme to /usr/share/plymouth/themes/beardeddiamond"
    echo "    (this requires root and will rebuild your initramfs)"
    sudo mkdir -p /usr/share/plymouth/themes/beardeddiamond
    sudo cp "$SCRIPT_DIR"/plymouth/beardeddiamond/* /usr/share/plymouth/themes/beardeddiamond/
    if command -v plymouth-set-default-theme >/dev/null 2>&1; then
        sudo plymouth-set-default-theme -R beardeddiamond
        echo "    Plymouth theme set as default and initramfs rebuilt."
    else
        echo "    plymouth-set-default-theme not found; install/enable Plymouth manually, then run:"
        echo "      sudo plymouth-set-default-theme -R beardeddiamond"
    fi
fi

if [ "$APPLY" -eq 1 ]; then
    echo "==> Applying the Bearded Diamond global theme"
    if command -v plasma-apply-lookandfeel >/dev/null 2>&1; then
        plasma-apply-lookandfeel -a org.kde.beardeddiamond.desktop
    else
        echo "    plasma-apply-lookandfeel not found; apply manually via System Settings > Appearance > Global Themes."
    fi
fi

echo "==> Done."
echo "    Global theme name: Bearded Diamond (org.kde.beardeddiamond.desktop)"
[ "$APPLY" -eq 0 ] && echo "    Apply it via System Settings > Appearance > Global Themes, or re-run with --apply."
[ "$WITH_PLYMOUTH" -eq 0 ] && echo "    Boot splash not installed; re-run with --with-plymouth to install it."
echo "    Chrome theme: chrome://extensions > Developer mode > Load unpacked > chrome-theme/"
echo "    Firefox theme: about:debugging > This Firefox > Load Temporary Add-on > firefox-theme/manifest.json"
