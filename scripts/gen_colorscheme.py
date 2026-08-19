"""Regenerates color-schemes/BeardedDiamond.colors from the palette."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import rgb_csv  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(REPO_ROOT, "color-schemes", "BeardedDiamond.colors")


def generate(palette):
    p = lambda name: rgb_csv(palette, name)  # noqa: E731

    content = f"""[ColorEffects:Disabled]
Color=56,56,56
ColorAmount=0
ColorEffect=0
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color={p('fg_inactive')}
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={p('bg_alt')}
BackgroundNormal={p('bg_button')}
DecorationFocus={p('accent')}
DecorationHover={p('fg_button')}
ForegroundActive={p('accent')}
ForegroundInactive={p('fg_inactive')}
ForegroundLink={p('link')}
ForegroundNegative={p('negative')}
ForegroundNeutral={p('neutral')}
ForegroundNormal={p('fg_normal')}
ForegroundPositive={p('positive')}
ForegroundVisited={p('visited')}

[Colors:Selection]
BackgroundAlternate={p('accent')}
BackgroundNormal={p('accent')}
DecorationFocus={p('accent')}
DecorationHover={p('fg_button')}
ForegroundActive={p('bg_titlebar')}
ForegroundInactive={p('fg_normal')}
ForegroundLink={p('bg_titlebar')}
ForegroundNegative={p('negative')}
ForegroundNeutral={p('neutral')}
ForegroundNormal={p('bg_titlebar')}
ForegroundPositive={p('positive')}
ForegroundVisited={p('bg_titlebar')}

[Colors:Tooltip]
BackgroundAlternate={p('bg_alt')}
BackgroundNormal={p('bg_alt')}
DecorationFocus={p('accent')}
DecorationHover={p('fg_button')}
ForegroundActive={p('accent')}
ForegroundInactive={p('fg_inactive')}
ForegroundLink={p('link')}
ForegroundNegative={p('negative')}
ForegroundNeutral={p('neutral')}
ForegroundNormal={p('fg_normal')}
ForegroundPositive={p('positive')}
ForegroundVisited={p('visited')}

[Colors:View]
BackgroundAlternate={p('bg_terminal')}
BackgroundNormal={p('bg_main')}
DecorationFocus={p('accent')}
DecorationHover={p('fg_button')}
ForegroundActive={p('accent')}
ForegroundInactive={p('fg_inactive')}
ForegroundLink={p('link')}
ForegroundNegative={p('negative')}
ForegroundNeutral={p('neutral')}
ForegroundNormal={p('fg_normal')}
ForegroundPositive={p('positive')}
ForegroundVisited={p('visited')}

[Colors:Window]
BackgroundAlternate={p('bg_alt')}
BackgroundNormal={p('bg_main')}
DecorationFocus={p('accent')}
DecorationHover={p('fg_button')}
ForegroundActive={p('accent')}
ForegroundInactive={p('fg_inactive')}
ForegroundLink={p('link')}
ForegroundNegative={p('negative')}
ForegroundNeutral={p('neutral')}
ForegroundNormal={p('fg_normal')}
ForegroundPositive={p('positive')}
ForegroundVisited={p('visited')}

[Colors:Complementary]
BackgroundAlternate={p('bg_alt')}
BackgroundNormal={p('bg_button')}
DecorationFocus={p('accent')}
DecorationHover={p('fg_button')}
ForegroundActive={p('accent')}
ForegroundInactive={p('fg_inactive')}
ForegroundLink={p('link')}
ForegroundNegative={p('negative')}
ForegroundNeutral={p('neutral')}
ForegroundNormal={p('fg_normal')}
ForegroundPositive={p('positive')}
ForegroundVisited={p('visited')}

[Colors:Header]
BackgroundAlternate={p('bg_alt')}
BackgroundNormal={p('bg_main')}
ForegroundActive={p('accent')}
ForegroundInactive={p('fg_inactive')}
ForegroundNormal={p('fg_normal')}

[General]
ColorScheme=BeardedDiamond
Name=Bearded Diamond
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={p('bg_titlebar')}
activeBlend={p('fg_normal')}
activeForeground={p('fg_normal')}
inactiveBackground={p('bg_button')}
inactiveBlend={p('fg_inactive')}
inactiveForeground={p('fg_inactive')}
"""
    with open(OUT_PATH, "w") as f:
        f.write(content)
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    from palette import load_palette

    generate(load_palette(sys.argv[1]))
