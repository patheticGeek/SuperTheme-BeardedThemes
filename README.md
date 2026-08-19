# Bearded Diamond — KDE Plasma 6 Global Theme

A KDE Plasma 6 global theme generated from the [Bearded Theme](https://github.com/BeardedBear/bearded-theme)
"Black & Diamond" VS Code color theme and its companion "Bearded Icons" icon
pack: near-black backgrounds, a cyan accent, and gold highlight/cursor tones.

`vendor/bearded-theme` and `vendor/bearded-icons` are git submodules of the
upstream sources. The color pipeline regenerates this repo's colors from
`vendor/bearded-theme` automatically — see [AGENTS.md](AGENTS.md) for how
(any AI coding agent can follow it directly). `vendor/bearded-icons` is
vendored for reference and version tracking; porting icon changes from it
is still a manual process (also documented in AGENTS.md). Clone with
`git clone --recurse-submodules`, or run `git submodule update --init`
after a plain clone.

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
- **Firefox theme** (`firefox-theme`) — the same palette mapped to Firefox's
  theme color keys (frame, tabs, toolbar, address bar, popups, sidebar,
  new-tab-page).
- **Ghostty theme** (`ghostty-theme/BeardedDiamond`) — a terminal color
  scheme (16-color ANSI palette, background/foreground, cursor, selection)
  for the [Ghostty](https://ghostty.org) terminal emulator.
- **zsh prompt theme** (`zsh-theme/beardeddiamond.zsh-theme`) — a
  lightweight prompt (user@host, cwd, git branch, background-job and
  exit-status indicators) using zsh's native truecolor escapes. Works
  standalone or as an oh-my-zsh custom theme.

## Install

```sh
git clone --recurse-submodules <this-repo> BeardedDiamond
cd BeardedDiamond
./install.sh --apply
```

By default this installs the color scheme, icon theme, KDE global theme,
Ghostty theme, and zsh theme into your user's config/XDG data directories
(`~/.local/share/...`, `~/.config/...`) — no root required — and applies the
KDE global theme immediately with `--apply`. The Chrome and Firefox themes
are browser extensions and are always installed manually (see below).

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

## Firefox theme

`firefox-theme/` is the same idea for Firefox. To install it:

1. Go to `about:debugging#/runtime/this-firefox`.
2. Click **Load Temporary Add-on…** and select `firefox-theme/manifest.json`.

Temporary add-ons are removed when Firefox restarts (Firefox only loads
unsigned themes this way outside of Nightly/Developer Edition). For a
permanent install, sign the theme via
[addons.mozilla.org](https://addons.mozilla.org) or run Firefox Developer
Edition/Nightly with `xpinstall.signatures.required` set to `false`.

## Ghostty theme

`install.sh` copies `ghostty-theme/BeardedDiamond` to
`~/.config/ghostty/themes/BeardedDiamond`. Enable it by adding to your
Ghostty config:

```
theme = BeardedDiamond
```

## zsh theme

`install.sh` installs `zsh-theme/beardeddiamond.zsh-theme` to your
oh-my-zsh custom themes directory (if oh-my-zsh is installed) or to
`~/.config/zsh/themes/` otherwise. Enable it with either:

```sh
# oh-my-zsh: in ~/.zshrc
ZSH_THEME="beardeddiamond"

# plain zsh: in ~/.zshrc
source ~/.config/zsh/themes/beardeddiamond.zsh-theme
```

## Building distributable packages

```sh
./package.sh [version]
```

Produces zip files in `dist/`:

- `SuperTheme-BeardedDiamond-<version>.zip` — everything bundled together
  (`install.sh`, `README.md`, `LICENSE`, and all the theme files), so others
  can download, extract, and run `./install.sh` without cloning the repo.
- `BeardedDiamond-<program>-<version>.zip` — one per program (`kde`,
  `chrome`, `firefox`, `ghostty`, `zsh`, `plymouth`) for anyone who only
  wants a single theme. Each contains just that program's files, `LICENSE`,
  and a short `INSTALL.txt` with manual install steps (no `install.sh`
  inside these, since it operates on the full set of directories).

Every push to `main` runs this automatically and publishes the resulting
zips as a GitHub Release (see `.github/workflows/release.yml`).

## Uninstall

Remove the installed directories:

```sh
rm -f  ~/.local/share/color-schemes/BeardedDiamond.colors
rm -rf ~/.local/share/icons/BeardedIcons
rm -rf ~/.local/share/plasma/look-and-feel/org.kde.beardeddiamond.desktop
rm -f  ~/.config/ghostty/themes/BeardedDiamond
rm -f  ~/.oh-my-zsh/custom/themes/beardeddiamond.zsh-theme  # or ~/.config/zsh/themes/...
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
