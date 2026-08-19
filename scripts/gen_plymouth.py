"""
Regenerates plymouth/beardeddiamond/: the .plymouth color config plus the
watermark, throbber animation, and password-dialog images.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette, plymouth_hex  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME_DIR = os.path.join(REPO_ROOT, "plymouth", "beardeddiamond")
PLYMOUTH_FILE = os.path.join(THEME_DIR, "beardeddiamond.plymouth")

COLOR_KEYS = {
    "BackgroundStartColor": "bg_main",
    "BackgroundEndColor": "bg_button",
    "ProgressBarBackgroundColor": "border",
    "ProgressBarForegroundColor": "accent",
}


def update_plymouth_file(palette):
    with open(PLYMOUTH_FILE) as f:
        text = f.read()
    for key, palette_name in COLOR_KEYS.items():
        text = re.sub(
            rf"^{key}=.*$",
            f"{key}={plymouth_hex(palette, palette_name)}",
            text,
            flags=re.MULTILINE,
        )
    with open(PLYMOUTH_FILE, "w") as f:
        f.write(text)
    print(f"wrote {PLYMOUTH_FILE}")


def regenerate_images(palette):
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
    img.save(os.path.join(THEME_DIR, "watermark.png"))

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
        frame.save(os.path.join(THEME_DIR, f"throbber-{i + 1:04d}.png"))

    # password entry box, bullet, lock icon
    ew, eh = 300, 50
    entry = Image.new("RGBA", (ew, eh), (0, 0, 0, 0))
    ed = ImageDraw.Draw(entry)
    ed.rounded_rectangle(
        [0, 0, ew - 1, eh - 1], radius=10, fill=palette["bg_alt"] + (235,), outline=dim, width=2
    )
    entry.save(os.path.join(THEME_DIR, "entry.png"))

    bullet = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bullet)
    bd.ellipse([2, 2, 14, 14], fill=accent_light)
    bullet.save(os.path.join(THEME_DIR, "bullet.png"))

    lock = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lock)
    ld.rounded_rectangle([12, 20, 36, 44], radius=4, fill=accent)
    ld.arc([16, 4, 32, 28], 180, 360, fill=accent, width=5)
    lock.save(os.path.join(THEME_DIR, "lock.png"))

    print(f"wrote images to {THEME_DIR}")


def generate(palette):
    update_plymouth_file(palette)
    regenerate_images(palette)


if __name__ == "__main__":
    generate(load_palette(sys.argv[1]))
