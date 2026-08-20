#!/usr/bin/env python3
"""
Rebuilds icons/BeardedIcons from the vendor/bearded-icons submodule.

Every SVG in the icon theme is an unmodified copy of an upstream file; the port
is purely a rename to freedesktop icon names, recorded in icon_map.py. This
script replays that rename and writes index.theme, so the whole directory is
generated output rather than something to hand-maintain.

Unlike the gen_* scripts driven by regenerate.py, this one is NOT per-variant:
the icon theme carries no accent color and is shared by every theme under
themes/.

Usage:
    python3 scripts/gen_icons.py
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from icon_map import CONTEXTS, UPSTREAM_ICON_DIR  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR_DIR = os.path.join(REPO_ROOT, "vendor", "bearded-icons")
OUT_DIR = os.path.join(REPO_ROOT, "icons", "BeardedIcons")

THEME_NAME = "Bearded Icons"
COMMENT = (
    "Ported from the 'Bearded Icons' VS Code icon theme; overrides folder and "
    "common file-type icons, inherits Breeze Dark for everything else"
)
INHERITS = "breeze-dark,breeze,hicolor"

# freedesktop Context= names for the directories icon_map.CONTEXTS produces.
CONTEXT_NAMES = {"mimetypes": "MimeTypes", "places": "Places"}


def index_theme(subdirs):
    lines = [
        "[Icon Theme]",
        f"Name={THEME_NAME}",
        f"Comment={COMMENT}",
        f"Inherits={INHERITS}",
        "Example=folder",
        "",
        "Directories=" + ",".join(subdirs),
    ]
    for subdir in subdirs:
        lines += [
            "",
            f"[{subdir}]",
            "Size=48",
            "MinSize=8",
            "MaxSize=512",
            "Type=Scalable",
            f"Context={CONTEXT_NAMES[subdir.split('/')[0]]}",
        ]
    return "\n".join(lines) + "\n"


def generate():
    src_dir = os.path.join(VENDOR_DIR, UPSTREAM_ICON_DIR)
    if not os.path.isdir(src_dir):
        raise SystemExit(
            f"error: {src_dir} not found -- run `git submodule update --init` first"
        )

    # Rebuilt from scratch so a row removed from icon_map.py actually disappears.
    if os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)

    subdirs = []
    missing = []
    count = 0
    for context, mapping in CONTEXTS.items():
        subdir = f"{context}/scalable"
        subdirs.append(subdir)
        dest_dir = os.path.join(OUT_DIR, context, "scalable")
        os.makedirs(dest_dir)
        for name, upstream in sorted(mapping.items()):
            src = os.path.join(src_dir, f"{upstream}.svg")
            if not os.path.isfile(src):
                missing.append((name, upstream))
                continue
            shutil.copyfile(src, os.path.join(dest_dir, f"{name}.svg"))
            count += 1

    if missing:
        # An upstream rename or removal -- fix the value in icon_map.py.
        for name, upstream in missing:
            print(f"error: {upstream}.svg not found upstream (mapped to {name})", file=sys.stderr)
        raise SystemExit(f"{len(missing)} mapped icon(s) missing from {src_dir}")

    with open(os.path.join(OUT_DIR, "index.theme"), "w") as f:
        f.write(index_theme(subdirs))

    print(f"wrote {OUT_DIR} ({count} icons)")


if __name__ == "__main__":
    generate()
