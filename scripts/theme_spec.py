"""
Identity of one generated theme variant: names/ids/paths that every gen_*.py
needs besides the color palette itself, plus the upstream registry options
(light/hc/desaturateInputs) that affect how a variant should be handled.

Add new variants to REGISTRY below -- that's the only place a new Bearded
Theme variation needs to be wired in to get colors, chrome/firefox/ghostty/
zsh/plymouth/KDE output. See AGENTS.md for the end-to-end steps.
"""

import os
from dataclasses import dataclass, field

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES_DIR = os.path.join(REPO_ROOT, "themes")


@dataclass(frozen=True)
class ThemeSpec:
    slug: str  # our directory slug, e.g. "black-and-diamond"
    upstream_slug: str  # vendor/bearded-theme's slug, e.g. "black-&-diamond"
    upstream_name: str  # vendor/bearded-theme's registry `name`, e.g. "Black & Diamond"
    display_name: str  # our product-facing name, e.g. "Bearded Diamond"
    ident: str  # PascalCase identifier, e.g. "BeardedDiamond" -- used for
    # ColorScheme=, .colors/ghostty/zsh-theme filenames
    id_lower: str  # lowercase identifier, e.g. "beardeddiamond" -- used for
    # the KDE look-and-feel package id and the Plymouth theme dir name
    options: dict = field(default_factory=dict)  # light / hc / desaturateInputs

    @property
    def dir(self):
        return os.path.join(THEMES_DIR, self.slug)

    @property
    def upstream_json_name(self):
        return f"bearded-theme-{self.upstream_slug}.json"

    @property
    def kde_lookandfeel_id(self):
        return f"org.kde.{self.id_lower}.desktop"

    @property
    def is_light(self):
        return bool(self.options.get("light"))

    @property
    def kde_plasma_theme(self):
        return "breeze-light" if self.is_light else "breeze-dark"


REGISTRY = [
    ThemeSpec(
        slug="black-and-diamond",
        upstream_slug="black-&-diamond",
        upstream_name="Black & Diamond",
        display_name="Bearded Diamond",
        ident="BeardedDiamond",
        id_lower="beardeddiamond",
        options={},
    ),
    ThemeSpec(
        slug="black-and-gold",
        upstream_slug="black-&-gold",
        upstream_name="Black & Gold",
        display_name="Bearded Gold",
        ident="BeardedGold",
        id_lower="beardedgold",
        options={},
    ),
]


def get(slug):
    for spec in REGISTRY:
        if spec.slug == slug:
            return spec
    raise KeyError(f"no theme registered with slug {slug!r}")
