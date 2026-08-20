# AGENTS.md — Updating Bearded Diamond from upstream

This repo is a set of KDE Plasma 6 global themes, Chrome/Firefox/Ghostty/zsh
themes, and boot splashes, each derived from one variant of the **Bearded
Theme** VS Code theme family (vendored as a git submodule at
`vendor/bearded-theme`, upstream:
<https://github.com/BeardedBear/bearded-theme>) and its companion
**Bearded Icons** icon pack (vendored at `vendor/bearded-icons`, upstream:
<https://github.com/BeardedBear/bearded-icons>, shared by every variant).
Each variant lives under `themes/<slug>/` — generated output, gitignored
(not committed; rebuild it with `./scripts/build-all.sh` after cloning, or
per-variant with `./scripts/regenerate.py`/`update-from-upstream.sh` below).
Currently registered:
`black-and-diamond` (from upstream's "Black & Diamond"), `black-and-gold`
(from "Black & Gold"), and `black-and-emerald` (from "Black & Emerald") --
see "Adding a new theme variant" below for wiring in more of the ~66
upstream variants.

If you are an AI coding agent asked to "update this theme", "sync with
upstream", "refresh the colors", "add a new Bearded Theme variant", or
similar — this file is your task spec. Follow it directly; don't re-derive
the color-extraction logic from scratch, it's already implemented in
`scripts/`.

## When to run this

- The user asks to update/sync/refresh a theme variant, or add a new one.
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

## How to update an existing variant

Run the one script that does everything:

```sh
./scripts/update-from-upstream.sh [slug]
```

`slug` defaults to `black-and-diamond`; pass another registered slug (see
`scripts/theme_spec.py`'s `REGISTRY`) to update a different variant. This:

1. Fast-forwards the `vendor/bearded-theme` submodule to its latest
   upstream commit (`git submodule update --remote --merge`).
2. `npm install && npm run build:vscode` inside the submodule to produce
   fresh theme JSON for every upstream variant.
3. Runs `scripts/regenerate.py <json> <slug>`, which regenerates every
   artifact under `themes/<slug>/` from scratch (safe to run on a slug with
   no existing directory -- everything is created, not patched):
   - `color-schemes/<Ident>.colors`
   - `chrome-theme/manifest.json` and `chrome-theme/icons/icon{16,48,128}.png`
   - `firefox-theme/manifest.json` and `firefox-theme/icons/icon{48,96}.png`
   - `plymouth/<id_lower>/<id_lower>.plymouth` + its images (watermark,
     throbber frames, entry/bullet/lock)
   - `look-and-feel/<kde_lookandfeel_id>/` (`metadata.json`, `contents/
     defaults`, `contents/splash/Splash.qml`, `images/logo.png`,
     `images/spinner.png`, `previews/splash.png`,
     `previews/{preview.png,fullscreenpreview.jpg}` -- the theme-picker
     mockup)
   - `ghostty-theme/<Ident>` (16-color ANSI palette + UI colors)
   - `zsh-theme/<id_lower>.zsh-theme` (prompt colors)
4. Prints a diff summary.

Nothing is committed automatically. `themes/` itself is gitignored, so
there's nothing to commit there -- but `vendor/bearded-theme` was just
fast-forwarded to a new upstream commit, which IS tracked (as a submodule
pointer). After it runs:

```sh
git diff --stat                 # review the submodule pointer bump etc.
./package.sh <new-version>      # rebuild the distributable SuperTheme zip
git add -A
git commit -m "Sync colors with upstream bearded-theme <short-sha>"
```

## Adding a new theme variant

Upstream Bearded Theme ships ~66 variants total (see
`vendor/bearded-theme/src/shared/theme-registry.ts` for the full list of
`{name, slug, options}` entries, and `src/variations/*.ts` for the color
definitions themselves). To add one of them here:

1. Pick the entry from `theme-registry.ts` (e.g. `{ name: "Black & Gold",
   options: {}, slug: "black-&-gold" }`).
2. Add a matching `ThemeSpec` to `REGISTRY` in `scripts/theme_spec.py`:
   `slug` is our own directory-safe name (e.g. `black-and-gold`),
   `upstream_slug` is the registry's `slug` verbatim, `display_name` is
   what to show in UI, `ident` is a PascalCase identifier for filenames
   (`BeardedGold`), `id_lower` is its lowercase form (`beardedgold`), and
   `options` should mirror the upstream entry's `options` (light/hc/
   desaturateInputs) -- this matters for `ThemeSpec.kde_plasma_theme`
   picking `breeze-light` vs `breeze-dark`.
3. Run `./scripts/update-from-upstream.sh <your-new-slug>` -- this creates
   `themes/<your-new-slug>/` from scratch with every color-derived artifact
   (the generators create their output directories as needed).
4. Icons are NOT per-variant -- `icons/BeardedIcons` is shared by every
   theme in `themes/`, so there's nothing to do for icons.
5. Review the diff, especially for light/hc variants (contrast, readability
   of the splash/Plymouth text) since those have had the least testing.

## What this does NOT cover

- **`icons/BeardedIcons`** — ported from `vendor/bearded-icons` (the
  submodule), but *not* automatically: there's no generator script for it
  yet, only the manual mapping that was done once (VS Code icon-theme
  `iconDefinitions`/`fileExtensions`/`languageIds` -> freedesktop mimetype
  icon names -> `icons/BeardedIcons/{mimetypes,places}/scalable/*.svg`, see
  git history for the exact mapping table). If `vendor/bearded-icons` has
  upstream changes worth porting (new file-type icons, redrawn existing
  ones), that's a manual diff-and-reapply of that mapping -- there's
  nothing to run.
- Icon pack version reporting *is* automatic: `release.yml` reads
  `vendor/bearded-icons/CHANGELOG.md`'s top `## X.Y.Z` heading (that repo
  has no `version` field in `package.json`) the same way it reads
  `vendor/bearded-theme/package.json`'s `version` for the theme. This
  reflects whatever commit the submodule is pinned to, not necessarily
  what `icons/BeardedIcons` was actually last ported from -- keep the
  submodule pinned to (or update it to) the commit you actually ported
  from when you do a manual re-port.
- Anything structural: if upstream renames/removes the VS Code color keys
  `scripts/palette.py` reads (e.g. `editor.background`,
  `terminal.ansiBlue`, `focusBorder` — see that file for the full list),
  the script will raise a `KeyError`. Fix the key mapping in
  `scripts/palette.py`, not the generator scripts.
- If upstream renames or removes a registered variant's slug entirely,
  update that entry's `upstream_slug` in `scripts/theme_spec.py`'s
  `REGISTRY` accordingly.

## Manual regeneration (without touching the submodule)

If you already have a theme JSON (e.g. from a locally installed VS Code
extension) and just want to test the generators:

```sh
python3 scripts/regenerate.py /path/to/bearded-theme-black-&-diamond.json black-and-diamond
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
