"""
Derives the Bearded Diamond palette from a built 'Black & Diamond' VS Code
theme JSON (as produced by vendor/bearded-theme's `npm run build:vscode`,
at dist/vscode/themes/bearded-theme-black-&-diamond.json).

This is the single source of truth other generator scripts read from, so
that regenerating the theme after an upstream update only requires editing
this file if the upstream color *structure* changes (new keys, renamed
fields) -- not the individual downstream artifacts.
"""

import json


def _hex_to_rgb(h):
    h = h.lstrip("#")[:6]
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def load_palette(theme_json_path):
    with open(theme_json_path) as f:
        theme = json.load(f)
    c = theme["colors"]

    hexes = {
        "bg_main": c["editor.background"],
        "bg_alt": c["input.background"],
        "bg_button": c["activityBar.background"],
        "bg_titlebar": c["titleBar.activeBackground"],
        "bg_terminal": c["terminal.background"],
        "fg_normal": c["editor.foreground"],
        "fg_inactive": c["sideBar.foreground"][:7],
        "fg_button": c["button.foreground"],
        "fg_cursor_gold": c["editorCursor.foreground"],
        "accent": c["terminal.ansiBlue"],
        "positive": c["terminal.ansiGreen"],
        "negative": c["terminal.ansiRed"],
        "neutral": c["terminal.ansiYellow"],
        "visited": c["terminal.ansiMagenta"],
        "link": c["terminal.ansiCyan"],
        "border": c["focusBorder"],
        "term_bg": c["terminal.background"],
        "term_fg": c["terminal.foreground"],
        "term_cursor": c["terminalCursor.foreground"],
        "ansi_black": c["terminal.ansiBlack"],
        "ansi_red": c["terminal.ansiRed"],
        "ansi_green": c["terminal.ansiGreen"],
        "ansi_yellow": c["terminal.ansiYellow"],
        "ansi_blue": c["terminal.ansiBlue"],
        "ansi_magenta": c["terminal.ansiMagenta"],
        "ansi_cyan": c["terminal.ansiCyan"],
        "ansi_white": c["terminal.ansiWhite"],
        "ansi_bright_black": c["terminal.ansiBrightBlack"],
        "ansi_bright_red": c["terminal.ansiBrightRed"],
        "ansi_bright_green": c["terminal.ansiBrightGreen"],
        "ansi_bright_yellow": c["terminal.ansiBrightYellow"],
        "ansi_bright_blue": c["terminal.ansiBrightBlue"],
        "ansi_bright_magenta": c["terminal.ansiBrightMagenta"],
        "ansi_bright_cyan": c["terminal.ansiBrightCyan"],
        "ansi_bright_white": c["terminal.ansiBrightWhite"],
    }

    palette = {name: _hex_to_rgb(h) for name, h in hexes.items()}
    palette["_hex"] = hexes
    return palette


def rgb_csv(palette, name):
    """e.g. '17,20,24' -- the format KDE .colors files use."""
    r, g, b = palette[name]
    return f"{r},{g},{b}"


def hex_str(palette, name):
    """e.g. '#11b7d4'"""
    r, g, b = palette[name]
    return f"#{r:02x}{g:02x}{b:02x}"


def plymouth_hex(palette, name):
    """e.g. '0x11b7d4' -- the format .plymouth files use."""
    r, g, b = palette[name]
    return f"0x{r:02x}{g:02x}{b:02x}"


if __name__ == "__main__":
    import sys

    p = load_palette(sys.argv[1])
    for name, rgb in p.items():
        if name == "_hex":
            continue
        print(f"{name:16s} {rgb}")
