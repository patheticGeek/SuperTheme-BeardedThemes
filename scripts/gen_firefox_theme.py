"""Regenerates the colors block in firefox-theme/manifest.json from the palette."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import hex_str, load_palette  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(REPO_ROOT, "firefox-theme", "manifest.json")

COLOR_MAP = {
    "frame": "bg_titlebar",
    "frame_inactive": "bg_button",
    "tab_background_text": "fg_inactive",
    "tab_selected": "bg_main",
    "tab_text": "fg_normal",
    "tab_line": "accent",
    "tab_loading": "accent",
    "toolbar": "bg_main",
    "toolbar_text": "fg_normal",
    "toolbar_field": "bg_alt",
    "toolbar_field_text": "fg_normal",
    "toolbar_field_border": "border",
    "toolbar_field_focus": "bg_alt",
    "toolbar_field_text_focus": "fg_normal",
    "toolbar_field_highlight": "accent",
    "toolbar_field_highlight_text": "bg_titlebar",
    "toolbar_top_separator": "bg_titlebar",
    "toolbar_bottom_separator": "bg_titlebar",
    "toolbar_vertical_separator": "border",
    "icons": "fg_button",
    "button_background_hover": "bg_alt",
    "button_background_active": "bg_button",
    "popup": "bg_alt",
    "popup_text": "fg_normal",
    "popup_border": "border",
    "popup_highlight": "accent",
    "popup_highlight_text": "bg_titlebar",
    "sidebar": "bg_button",
    "sidebar_text": "fg_normal",
    "sidebar_border": "border",
    "sidebar_highlight": "accent",
    "sidebar_highlight_text": "bg_titlebar",
    "ntp_background": "bg_main",
    "ntp_text": "fg_normal",
}


def generate(palette):
    with open(OUT_PATH) as f:
        manifest = json.load(f)

    manifest["theme"]["colors"] = {
        key: hex_str(palette, name) for key, name in COLOR_MAP.items()
    }

    with open(OUT_PATH, "w") as f:
        json.dump(manifest, f, indent=4)
        f.write("\n")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    generate(load_palette(sys.argv[1]))
