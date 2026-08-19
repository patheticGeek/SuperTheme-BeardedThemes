#!/usr/bin/env python3
"""
Regenerates every color-derived artifact for one theme variant from a built
Bearded Theme VS Code theme JSON.

Usage:
    python3 scripts/regenerate.py <path-to-theme.json> [slug]

slug defaults to the only entry currently in scripts/theme_spec.py's
REGISTRY ("black-and-diamond"); pass it explicitly once more variants are
registered there. This script only touches colors (color scheme, Chrome
theme, Firefox theme, Plymouth boot theme, Plasma splash + look-and-feel
metadata, Ghostty theme, zsh prompt theme) -- it does NOT touch
icons/BeardedIcons, which is ported from the separate 'bearded-icons' VS
Code extension and updated manually (shared across all variants).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette  # noqa: E402
from theme_spec import REGISTRY, get  # noqa: E402
import gen_colorscheme  # noqa: E402
import gen_chrome_theme  # noqa: E402
import gen_firefox_theme  # noqa: E402
import gen_plymouth  # noqa: E402
import gen_splash  # noqa: E402
import gen_lookandfeel_meta  # noqa: E402
import gen_ghostty  # noqa: E402
import gen_zsh_theme  # noqa: E402


def regenerate_one(theme_json_path, spec):
    palette = load_palette(theme_json_path, spec.options)

    gen_colorscheme.generate(palette, spec)
    gen_chrome_theme.generate(palette, spec)
    gen_firefox_theme.generate(palette, spec)
    gen_plymouth.generate(palette, spec)
    gen_splash.generate(palette, spec)
    gen_lookandfeel_meta.generate(palette, spec)
    gen_ghostty.generate(palette, spec)
    gen_zsh_theme.generate(palette, spec)


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        sys.exit(1)

    theme_json_path = sys.argv[1]
    spec = get(sys.argv[2]) if len(sys.argv) == 3 else REGISTRY[0]

    regenerate_one(theme_json_path, spec)

    print("\nDone. Review the diff (`git diff --stat`), then:")
    print("  - bump the version in your release notes")
    print("  - rebuild the distributable: ./package.sh <version>")
    print("  - commit")


if __name__ == "__main__":
    main()
