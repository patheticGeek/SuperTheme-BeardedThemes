"""Regenerates <theme>/color-schemes/<Ident>.colors from the palette."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import rgb_csv  # noqa: E402


def generate(palette, spec):
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
ColorScheme={spec.ident}
Name={spec.display_name}
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
    out_path = os.path.join(spec.dir, "color-schemes", f"{spec.ident}.colors")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(content)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    from palette import load_palette
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
