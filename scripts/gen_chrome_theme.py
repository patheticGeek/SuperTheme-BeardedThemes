"""Regenerates the colors block in chrome-theme/manifest.json from the palette."""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(REPO_ROOT, "chrome-theme", "manifest.json")


def generate(palette):
    with open(OUT_PATH) as f:
        manifest = json.load(f)

    p = lambda name: list(palette[name])  # noqa: E731

    manifest["theme"]["colors"] = {
        "frame": p("bg_titlebar"),
        "frame_inactive": p("bg_button"),
        "toolbar": p("bg_main"),
        "toolbar_text": p("fg_normal"),
        "tab_text": p("fg_normal"),
        "tab_background_text": p("fg_inactive"),
        "tab_selected": p("bg_main"),
        "toolbar_button_icon": p("accent"),
        "button_background": p("bg_button"),
        "bookmark_text": p("fg_normal"),
        "ntp_background": p("bg_main"),
        "ntp_text": p("fg_normal"),
        "ntp_link": p("accent"),
        "ntp_header": p("bg_alt"),
        "omnibox_background": p("bg_alt"),
        "omnibox_text": p("fg_normal"),
        "toolbar_top_separator": p("bg_titlebar"),
        "toolbar_bottom_separator": p("bg_titlebar"),
        "toolbar_vertical_separator": p("border"),
    }

    text = json.dumps(manifest, indent=4)
    # collapse [n,\n n,\n n\n] RGB triples back onto one line for readable diffs
    text = re.sub(
        r"\[\s*(\d+),\s*(\d+),\s*(\d+)\s*\]",
        lambda m: f"[{m.group(1)}, {m.group(2)}, {m.group(3)}]",
        text,
    )
    with open(OUT_PATH, "w") as f:
        f.write(text + "\n")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    generate(load_palette(sys.argv[1]))
