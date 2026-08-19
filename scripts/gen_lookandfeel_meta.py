"""
Regenerates <theme>/look-and-feel/<kde_lookandfeel_id>/metadata.json and
contents/defaults from the theme's identity (name/id) and light/dark option
-- no palette colors involved, just wiring the right widget style, plasma
theme, and package id for the variant.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette  # noqa: E402


def generate(palette, spec):
    lookandfeel_dir = os.path.join(spec.dir, "look-and-feel", spec.kde_lookandfeel_id)
    contents_dir = os.path.join(lookandfeel_dir, "contents")
    os.makedirs(contents_dir, exist_ok=True)

    metadata_path = os.path.join(lookandfeel_dir, "metadata.json")
    metadata = {
        "KPackageStructure": "Plasma/LookAndFeel",
        "KPlugin": {
            "Authors": [{"Name": f"Generated from Bearded Theme {spec.upstream_name} (VS Code)"}],
            "Category": "",
            "Description": (
                f"A KDE Plasma 6 global theme generated to match the "
                f"'Bearded Theme {spec.upstream_name}' VS Code color theme. "
                f"Uses the 'Bearded Icons' icon theme ported from the matching VS Code icon pack."
            ),
            "Id": spec.kde_lookandfeel_id,
            "License": "GPL-2.0-or-later",
            "Name": spec.display_name,
            "Version": "1.0",
        },
    }
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)
        f.write("\n")
    print(f"wrote {metadata_path}")

    defaults_path = os.path.join(contents_dir, "defaults")
    defaults = f"""[kdeglobals][KDE]
widgetStyle=Breeze

[kdeglobals][General]
ColorScheme={spec.ident}

[kdeglobals][Icons]
Theme=BeardedIcons

[plasmarc][Theme]
name={spec.kde_plasma_theme}

[Wallpaper]
Image=Next

[kcminputrc][Mouse]
cursorTheme=breeze_cursors

[kwinrc][org.kde.kdecoration2]
library=org.kde.breeze
theme=Breeze

[ksplashrc][KSplash]
Theme={spec.kde_lookandfeel_id}
"""
    with open(defaults_path, "w") as f:
        f.write(defaults)
    print(f"wrote {defaults_path}")


if __name__ == "__main__":
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
