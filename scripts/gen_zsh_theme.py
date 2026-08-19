"""
Regenerates zsh-theme/beardeddiamond.zsh-theme from the palette, using
zsh's native `%F{#rrggbb}` truecolor prompt escapes.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import hex_str, load_palette  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(REPO_ROOT, "zsh-theme", "beardeddiamond.zsh-theme")

TEMPLATE = """\
# Bearded Diamond zsh prompt theme
# Generated to match the 'Bearded Theme Black & Diamond' VS Code theme.
#
# Usage:
#   Plain zsh:    source /path/to/beardeddiamond.zsh-theme   (in ~/.zshrc)
#   oh-my-zsh:    cp into ~/.oh-my-zsh/custom/themes/, then
#                 ZSH_THEME="beardeddiamond" in ~/.zshrc
#
# Regenerate this file with: python3 scripts/gen_zsh_theme.py <theme.json>
# Do not hand-edit the colors -- see AGENTS.md.

autoload -Uz vcs_info
setopt PROMPT_SUBST

zstyle ':vcs_info:git:*' formats " {gold}(%b){reset}"
zstyle ':vcs_info:git:*' actionformats " {gold}(%b|%a){reset}"

precmd() {{ vcs_info }}

PROMPT='{muted}%n@%m{reset} {accent}%1~{reset}${{vcs_info_msg_0_}} %(?.{accent}.{negative})❯{reset} '
RPROMPT='%(1j.{muted}[%j]{reset}.)'
"""


def generate(palette):
    accent = hex_str(palette, "accent")
    muted = hex_str(palette, "fg_inactive")
    gold = hex_str(palette, "fg_cursor_gold")
    negative = hex_str(palette, "negative")

    content = TEMPLATE.format(
        accent=f"%F{{{accent}}}",
        muted=f"%F{{{muted}}}",
        gold=f"%F{{{gold}}}",
        negative=f"%F{{{negative}}}",
        reset="%f",
    )

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        f.write(content)
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    generate(load_palette(sys.argv[1]))
