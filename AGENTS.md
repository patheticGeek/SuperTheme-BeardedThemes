# AGENTS.md — Updating Bearded Diamond from upstream

This repo is a KDE Plasma 6 global theme, Chrome theme, and boot splash
derived from the **Bearded Theme "Black & Diamond"** VS Code theme
(vendored as a git submodule at `vendor/bearded-theme`, upstream:
<https://github.com/BeardedBear/bearded-theme>).

If you are an AI coding agent asked to "update this theme", "sync with
upstream", "refresh the colors", or similar — this file is your task spec.
Follow it directly; don't re-derive the color-extraction logic from scratch,
it's already implemented in `scripts/`.

## When to run this

- The user asks to update/sync/refresh the theme.
- `vendor/bearded-theme` has upstream commits not yet reflected in this
  repo's generated files (check with `git -C vendor/bearded-theme log
  HEAD..origin/main --oneline` after fetching).
- Periodically/on a schedule, if the user has set that up.

## What "the theme" is derived from

The single source of truth is the `blackAndDiamond` export in
`vendor/bearded-theme/src/variations/black.ts`:

```ts
const base = "#111418";
blue: "#11B7D4"   // accent
// ...
export const blackAndDiamond: Theme = {
  colors: blackColors,
  levels: blackLevels,
  ui: makeMainColorsDark({ base, primary: blackColors.blue }),
};
```

Upstream's build (`npm run build:vscode`, via `vite-node`) expands that into
a full VS Code theme JSON at
`vendor/bearded-theme/dist/vscode/themes/bearded-theme-black-&-diamond.json`
— the same shape as the file originally used to hand-derive this repo's
palette (see `scripts/palette.py` for the exact VS Code color keys read).

## How to update

Run the one script that does everything:

```sh
./scripts/update-from-upstream.sh
```

This:

1. Fast-forwards the `vendor/bearded-theme` submodule to its latest
   upstream commit (`git submodule update --remote --merge`).
2. `npm install && npm run build:vscode` inside the submodule to produce a
   fresh theme JSON.
3. Runs `scripts/regenerate.py` on that JSON, which regenerates every
   color-derived artifact in this repo:
   - `color-schemes/BeardedDiamond.colors`
   - `chrome-theme/manifest.json` (the `theme.colors` block only)
   - `firefox-theme/manifest.json` (the `theme.colors` block only)
   - `plymouth/beardeddiamond/beardeddiamond.plymouth` + its images
     (watermark, throbber frames, entry/bullet/lock)
   - `look-and-feel/org.kde.beardeddiamond.desktop/contents/splash/`
     (`Splash.qml` colors, `images/logo.png`, `images/spinner.png`,
     `previews/splash.png`)
   - `ghostty-theme/BeardedDiamond` (16-color ANSI palette + UI colors)
   - `zsh-theme/beardeddiamond.zsh-theme` (prompt colors)
4. Prints a diff summary.

Nothing is committed automatically. After it runs:

```sh
git diff --stat                 # review what changed
./package.sh <new-version>      # rebuild the distributable tarball
git add -A
git commit -m "Sync colors with upstream bearded-theme <short-sha>"
```

## What this does NOT cover

- **`icons/BeardedIcons`** — ported from the separate
  [bearded-icons](https://github.com/BeardedBear/bearded-icons) VS Code
  extension, which is not vendored here. If it needs updating, that's a
  manual re-port: diff the extension's `icons.json` / `icons/*.svg` against
  what's mapped in this repo (there's no script for this yet — the original
  mapping table lives only in this project's history, not in `scripts/`).
- Anything structural: if upstream renames/removes the VS Code color keys
  `scripts/palette.py` reads (e.g. `editor.background`,
  `terminal.ansiBlue`, `focusBorder` — see that file for the full list),
  the script will raise a `KeyError`. Fix the key mapping in
  `scripts/palette.py`, not the generator scripts.
- If upstream renames or removes the `blackAndDiamond` variant entirely,
  update the `THEME_JSON` path in `scripts/update-from-upstream.sh`
  accordingly.

## Manual regeneration (without touching the submodule)

If you already have a theme JSON (e.g. from a locally installed VS Code
extension) and just want to test the generators:

```sh
python3 scripts/regenerate.py /path/to/bearded-theme-black-&-diamond.json
```

Each generator can also be run individually — see `scripts/gen_*.py`.

## Conventions

- Don't hand-edit the generated files listed above; edit the generator
  scripts or `vendor/bearded-theme` instead, then regenerate. Hand-edits
  will just be overwritten on the next sync.
- Keep `scripts/palette.py`'s named colors (`bg_main`, `accent`, `border`,
  etc.) as the only place that maps upstream VS Code keys to this theme's
  semantic palette — every generator should read from that dict, never
  from a raw theme JSON directly.
