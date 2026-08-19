# Bearded Diamond — KDE Plasma 6 Global Theme

A KDE Plasma 6 global theme generated from the [Bearded Theme](https://github.com/BeardedBear/bearded-theme)
"Black & Diamond" VS Code color theme and its companion "Bearded Icons" icon
pack: near-black backgrounds, a cyan accent, and gold highlight/cursor tones.

`vendor/bearded-theme` is a git submodule of the upstream theme source, used
to regenerate this repo's colors when upstream changes — see
[AGENTS.md](AGENTS.md) for how (any AI coding agent can follow it directly).
Clone with `git clone --recurse-submodules`, or run
`git submodule update --init` after a plain clone.

Includes:

- **Color scheme** (`color-schemes/BeardedDiamond.colors`) — the full KDE
  color palette (windows, views, buttons, selection, tooltips, WM decorations).
- **Icon theme** (`icons/BeardedIcons`) — folder icons plus ~90 file-type
  (mimetype) icons ported from the Bearded Icons VS Code extension, covering
  the most common languages and file formats. Inherits Breeze Dark for
  everything not explicitly themed (app icons, actions, devices, etc.).
- **Global theme package** (`look-and-feel/org.kde.beardeddiamond.desktop`) —
  ties the color scheme and icon theme together, using Breeze for the widget
  style, window decoration, and cursors, plus a custom Plasma splash screen
  (`contents/splash`) shown while a Plasma session starts.
- **Plymouth boot theme** (`plymouth/beardeddiamond`) — the system boot
  splash shown before login, styled to match. Installed separately since it
  requires root and a system boot component.
- **Chrome theme** (`chrome-theme`) — a matching browser theme (frame,
  toolbar, tabs, omnibox, and new-tab-page colors) for Chrome and
  Chromium-based browsers. Installed separately since it lives in the
  browser, not the desktop.

## Install

```sh
git clone <this-repo> BardedDiamond
cd BardedDiamond
./install.sh --apply
```

By default this installs into your user's XDG data directories
(`~/.local/share/...`) — no root required — and applies the theme immediately
with `--apply`.

Options:

| Flag               | Effect                                                                 |
|---------------------|-------------------------------------------------------------------------|
| `--apply`           | Apply the global theme immediately after installing                    |
| `--system`           | Install into `/usr/share/...` instead of `~/.local/share/...` (needs `sudo`) |
| `--with-plymouth`    | Also install the boot splash to `/usr/share/plymouth/themes` and rebuild your initramfs (needs `sudo`) |

Without `--apply`, apply the theme manually via *System Settings → Appearance
→ Global Themes → Bearded Diamond*.

The Plymouth boot theme is opt-in and separate from the rest because it's a
system-level, root-owned change that affects every boot and requires
rebuilding the initramfs — review `plymouth/beardeddiamond/beardeddiamond.plymouth`
before installing it.

## Chrome theme

`chrome-theme/` is an unpacked browser extension that themes Chrome (and
Chromium, Brave, Vivaldi, Edge, etc.). To install it:

1. Go to `chrome://extensions`.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked** and select the `chrome-theme` directory.

It applies immediately and can be removed like any other extension. There's
nothing to publish to the Chrome Web Store here — it's meant for local use.

## Building a distributable package

```sh
./package.sh [version]
```

Produces `dist/BeardedDiamond-<version>.tar.gz` containing everything needed
to install the theme (`install.sh`, `README.md`, `LICENSE`, and the theme
files) so others can download, extract, and run `./install.sh` without
cloning the repository.

## Uninstall

Remove the installed directories:

```sh
rm -f  ~/.local/share/color-schemes/BeardedDiamond.colors
rm -rf ~/.local/share/icons/BeardedIcons
rm -rf ~/.local/share/plasma/look-and-feel/org.kde.beardeddiamond.desktop
# if installed with --with-plymouth:
sudo rm -rf /usr/share/plymouth/themes/beardeddiamond
sudo plymouth-set-default-theme -R <previous-theme>
```

Then switch to a different global theme in System Settings.

## Credits

Colors and icons are ported from [Bearded Theme](https://github.com/BeardedBear/bearded-theme)
and [Bearded Icons](https://github.com/BeardedBear/bearded-icons) by BeardedBear,
both licensed GPL-3.0. This repository is licensed GPL-3.0 as well; see
[LICENSE](LICENSE).
