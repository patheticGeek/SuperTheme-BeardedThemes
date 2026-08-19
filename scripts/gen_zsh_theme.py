"""
Regenerates <theme>/zsh-theme/<id_lower>.zsh-theme from the palette, using
zsh's native `%F{#rrggbb}` truecolor prompt escapes.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import hex_str, load_palette  # noqa: E402

TEMPLATE = """\
# {display_name} zsh prompt theme
# Generated to match the 'Bearded Theme {upstream_name}' VS Code theme.
#
# Usage:
#   Plain zsh:    source /path/to/{filename}   (in ~/.zshrc)
#   oh-my-zsh:    cp into ~/.oh-my-zsh/custom/themes/, then
#                 ZSH_THEME="{zsh_theme_name}" in ~/.zshrc
#
# Regenerate this file with: python3 scripts/regenerate.py <theme.json> {slug}
# Do not hand-edit the colors -- see AGENTS.md.

autoload -Uz vcs_info
setopt PROMPT_SUBST

zstyle ':vcs_info:git:*' formats " {gold}(%b){reset}"
zstyle ':vcs_info:git:*' actionformats " {gold}(%b|%a){reset}"

precmd() {{ vcs_info }}

PROMPT='{muted}%n@%m{reset} {accent}%1~{reset}${{vcs_info_msg_0_}} %(?.{accent}.{negative})❯{reset} '
RPROMPT='%(1j.{muted}[%j]{reset}.)'
"""


def generate(palette, spec):
    accent = hex_str(palette, "accent")
    muted = hex_str(palette, "fg_inactive")
    gold = hex_str(palette, "fg_cursor_gold")
    negative = hex_str(palette, "negative")

    filename = f"{spec.id_lower}.zsh-theme"

    content = TEMPLATE.format(
        display_name=spec.display_name,
        upstream_name=spec.upstream_name,
        filename=filename,
        zsh_theme_name=spec.id_lower,
        slug=spec.slug,
        accent=f"%F{{{accent}}}",
        muted=f"%F{{{muted}}}",
        gold=f"%F{{{gold}}}",
        negative=f"%F{{{negative}}}",
        reset="%f",
    )

    out_path = os.path.join(spec.dir, "zsh-theme", filename)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(content)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
