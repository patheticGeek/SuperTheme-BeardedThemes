#!/usr/bin/env python3
"""
Regenerates every color-derived artifact in this repo from a built
'Black & Diamond' VS Code theme JSON.

Usage:
    python3 scripts/regenerate.py <path-to-theme.json>

Typically invoked via scripts/update-from-upstream.sh, which builds that
JSON from the vendor/bearded-theme submodule first. This script only
touches colors (color scheme, Chrome theme, Plymouth boot theme, Plasma
splash) -- it does NOT touch icons/BeardedIcons, which is ported from the
separate 'bearded-icons' VS Code extension and updated manually.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette  # noqa: E402
import gen_colorscheme  # noqa: E402
import gen_chrome_theme  # noqa: E402
import gen_plymouth  # noqa: E402
import gen_splash  # noqa: E402


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    theme_json_path = sys.argv[1]
    palette = load_palette(theme_json_path)

    gen_colorscheme.generate(palette)
    gen_chrome_theme.generate(palette)
    gen_plymouth.generate(palette)
    gen_splash.generate(palette)

    print("\nDone. Review the diff (`git diff --stat`), then:")
    print("  - bump the version in package.sh's default / your release notes")
    print("  - rebuild the distributable: ./package.sh <version>")
    print("  - commit")


if __name__ == "__main__":
    main()
