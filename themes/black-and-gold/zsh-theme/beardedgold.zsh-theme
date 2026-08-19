# Bearded Gold zsh prompt theme
# Generated to match the 'Bearded Theme Black & Gold' VS Code theme.
#
# Usage:
#   Plain zsh:    source /path/to/beardedgold.zsh-theme   (in ~/.zshrc)
#   oh-my-zsh:    cp into ~/.oh-my-zsh/custom/themes/, then
#                 ZSH_THEME="beardedgold" in ~/.zshrc
#
# Regenerate this file with: python3 scripts/regenerate.py <theme.json> black-and-gold
# Do not hand-edit the colors -- see AGENTS.md.

autoload -Uz vcs_info
setopt PROMPT_SUBST

zstyle ':vcs_info:git:*' formats " %F{#c7910c}(%b)%f"
zstyle ':vcs_info:git:*' actionformats " %F{#c7910c}(%b|%a)%f"

precmd() { vcs_info }

PROMPT='%F{#a0acbb}%n@%m%f %F{#c7910c}%1~%f${vcs_info_msg_0_} %(?.%F{#c7910c}.%F{#e35535})❯%f '
RPROMPT='%(1j.%F{#a0acbb}[%j]%f.)'
