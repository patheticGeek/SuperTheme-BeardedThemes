"""
Regenerates <theme>/plymouth/<id_lower>/: the .plymouth color config plus
the watermark, throbber animation, and password-dialog images.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette, plymouth_hex  # noqa: E402

TEMPLATE = """\
[Plymouth Theme]
Name={display_name}
Description=Boot splash generated to match the 'Bearded Theme {upstream_name}' VS Code theme.
ModuleName=two-step

[two-step]
ImageDir=/usr/share/plymouth/themes/{id_lower}
DialogHorizontalAlignment=.5
DialogVerticalAlignment=.62
TitleHorizontalAlignment=.5
TitleVerticalAlignment=.62
HorizontalAlignment=.5
VerticalAlignment=.62
WatermarkHorizontalAlignment=.5
WatermarkVerticalAlignment=.5
Transition=none
TransitionDuration=0.0
BackgroundStartColor={bg_main}
BackgroundEndColor={bg_button}
ProgressBarBackgroundColor={border}
ProgressBarForegroundColor={accent}
MessageBelowAnimation=true

[boot-up]
UseEndAnimation=false

[shutdown]
UseEndAnimation=false

[reboot]
UseEndAnimation=false

[updates]
SuppressMessages=true
ProgressBarShowPercentComplete=true
UseProgressBar=true
Title=Installing Updates...
SubTitle=Do not turn off your computer

[system-upgrade]
SuppressMessages=true
ProgressBarShowPercentComplete=true
UseProgressBar=true
Title=Upgrading System...
SubTitle=Do not turn off your computer

[system-reset]
SuppressMessages=true
ProgressBarShowPercentComplete=true
UseProgressBar=true
Title=Resetting System...
SubTitle=Do not turn off your computer
"""


def update_plymouth_file(palette, spec, plymouth_file):
    text = TEMPLATE.format(
        display_name=spec.display_name,
        upstream_name=spec.upstream_name,
        id_lower=spec.id_lower,
        bg_main=plymouth_hex(palette, "bg_main"),
        bg_button=plymouth_hex(palette, "bg_button"),
        border=plymouth_hex(palette, "border"),
        accent=plymouth_hex(palette, "accent"),
    )
    os.makedirs(os.path.dirname(plymouth_file), exist_ok=True)
    with open(plymouth_file, "w") as f:
        f.write(text)
    print(f"wrote {plymouth_file}")


def regenerate_images(palette, theme_dir):
    from PIL import Image, ImageDraw

    accent = palette["accent"]
    accent_light = palette["fg_button"]
    dim = palette["border"]

    # watermark: diamond logo, transparent bg
    S = 400
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S / 2, S / 2
    w, h = 150, 185
    top = (cx, cy - h / 2)
    bottom = (cx, cy + h / 2)
    left = (cx - w / 2, cy - h / 6)
    right = (cx + w / 2, cy - h / 6)
    midleft = (cx - w / 3, cy + h / 10)
    midright = (cx + w / 3, cy + h / 10)
    d.polygon([left, top, right], fill=accent_light)
    d.polygon([left, midleft, bottom], fill=accent)
    d.polygon([right, midright, bottom], fill=tuple(max(0, c - 4) for c in accent))
    d.polygon([midleft, midright, bottom], fill=accent)
    outline = palette["bg_titlebar"]
    for a, b in [(left, right), (left, top), (right, top), (left, bottom), (right, bottom)]:
        d.line([a, b], fill=outline, width=3)
    img.save(os.path.join(theme_dir, "watermark.png"))

    # throbber animation frames: rotating dashed ring
    N = 30
    size = 128
    for i in range(N):
        frame = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        fd = ImageDraw.Draw(frame)
        angle0 = (360 / N) * i
        bbox = [10, 10, size - 10, size - 10]
        fd.arc(bbox, 0, 360, fill=dim, width=8)
        fd.arc(bbox, angle0, angle0 + 90, fill=accent, width=8)
        fd.arc(bbox, angle0, angle0 + 18, fill=accent_light, width=8)
        frame.save(os.path.join(theme_dir, f"throbber-{i + 1:04d}.png"))

    # password entry box, bullet, lock icon
    ew, eh = 300, 50
    entry = Image.new("RGBA", (ew, eh), (0, 0, 0, 0))
    ed = ImageDraw.Draw(entry)
    ed.rounded_rectangle(
        [0, 0, ew - 1, eh - 1], radius=10, fill=palette["bg_alt"] + (235,), outline=dim, width=2
    )
    entry.save(os.path.join(theme_dir, "entry.png"))

    bullet = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bullet)
    bd.ellipse([2, 2, 14, 14], fill=accent_light)
    bullet.save(os.path.join(theme_dir, "bullet.png"))

    lock = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lock)
    ld.rounded_rectangle([12, 20, 36, 44], radius=4, fill=accent)
    ld.arc([16, 4, 32, 28], 180, 360, fill=accent, width=5)
    lock.save(os.path.join(theme_dir, "lock.png"))

    print(f"wrote images to {theme_dir}")


def generate(palette, spec):
    theme_dir = os.path.join(spec.dir, "plymouth", spec.id_lower)
    os.makedirs(theme_dir, exist_ok=True)
    plymouth_file = os.path.join(theme_dir, f"{spec.id_lower}.plymouth")
    update_plymouth_file(palette, spec, plymouth_file)
    regenerate_images(palette, theme_dir)


if __name__ == "__main__":
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
