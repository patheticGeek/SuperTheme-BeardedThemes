"""Regenerates <theme>/ghostty-theme/<Ident> from the palette."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import hex_str, load_palette  # noqa: E402

ANSI_ORDER = [
    "ansi_black",
    "ansi_red",
    "ansi_green",
    "ansi_yellow",
    "ansi_blue",
    "ansi_magenta",
    "ansi_cyan",
    "ansi_white",
    "ansi_bright_black",
    "ansi_bright_red",
    "ansi_bright_green",
    "ansi_bright_yellow",
    "ansi_bright_blue",
    "ansi_bright_magenta",
    "ansi_bright_cyan",
    "ansi_bright_white",
]


def generate(palette, spec):
    h = lambda name: hex_str(palette, name)  # noqa: E731

    lines = [f"palette = {i}={h(name)}" for i, name in enumerate(ANSI_ORDER)]
    lines += [
        f"background = {h('term_bg')}",
        f"foreground = {h('term_fg')}",
        f"cursor-color = {h('term_cursor')}",
        f"cursor-text = {h('bg_main')}",
        f"selection-background = {h('accent')}",
        f"selection-foreground = {h('bg_titlebar')}",
    ]

    out_path = os.path.join(spec.dir, "ghostty-theme", spec.ident)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
