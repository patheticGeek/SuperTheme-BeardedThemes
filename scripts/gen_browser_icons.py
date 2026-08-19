"""
Regenerates the Chrome/Firefox extension icons: <theme>/chrome-theme/icons/
icon{16,48,128}.png and <theme>/firefox-theme/icons/icon{48,96}.png -- the
same accent-colored mark drawn for the Plymouth watermark and Plasma splash
logo, scaled down to icon sizes.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette  # noqa: E402

CHROME_SIZES = [16, 48, 128]
FIREFOX_SIZES = [48, 96]


def draw_mark(palette, size):
    from PIL import Image, ImageDraw

    S = size * 4  # supersample, then downscale for smooth edges at small sizes
    accent = palette["accent"]
    accent_light = palette["fg_button"]

    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S / 2, S / 2
    w, h = S * 0.6, S * 0.72
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

    return img.resize((size, size), Image.LANCZOS)


def generate(palette, spec):
    chrome_dir = os.path.join(spec.dir, "chrome-theme", "icons")
    firefox_dir = os.path.join(spec.dir, "firefox-theme", "icons")
    os.makedirs(chrome_dir, exist_ok=True)
    os.makedirs(firefox_dir, exist_ok=True)

    for size in CHROME_SIZES:
        path = os.path.join(chrome_dir, f"icon{size}.png")
        draw_mark(palette, size).save(path)
        print(f"wrote {path}")

    for size in FIREFOX_SIZES:
        path = os.path.join(firefox_dir, f"icon{size}.png")
        draw_mark(palette, size).save(path)
        print(f"wrote {path}")


if __name__ == "__main__":
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
