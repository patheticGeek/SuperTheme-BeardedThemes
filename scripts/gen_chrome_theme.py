"""Regenerates the colors block in <theme>/chrome-theme/manifest.json."""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette  # noqa: E402


def generate(palette, spec):
    out_path = os.path.join(spec.dir, "chrome-theme", "manifest.json")
    with open(out_path) as f:
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
    manifest["name"] = spec.display_name
    manifest["short_name"] = spec.display_name
    manifest["description"] = (
        f"A Chrome theme generated to match the 'Bearded Theme {spec.upstream_name}' VS Code theme."
    )

    text = json.dumps(manifest, indent=4)
    # collapse [n,\n n,\n n\n] RGB triples back onto one line for readable diffs
    text = re.sub(
        r"\[\s*(\d+),\s*(\d+),\s*(\d+)\s*\]",
        lambda m: f"[{m.group(1)}, {m.group(2)}, {m.group(3)}]",
        text,
    )
    with open(out_path, "w") as f:
        f.write(text + "\n")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
