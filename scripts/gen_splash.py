"""
Regenerates the Plasma (ksplash) splash screen images and inline QML colors
under look-and-feel/org.kde.beardeddiamond.desktop/contents/splash/.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import hex_str, load_palette  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPLASH_DIR = os.path.join(
    REPO_ROOT, "look-and-feel", "org.kde.beardeddiamond.desktop", "contents", "splash"
)
IMAGES_DIR = os.path.join(SPLASH_DIR, "images")
QML_FILE = os.path.join(SPLASH_DIR, "Splash.qml")
PREVIEW_FILE = os.path.join(
    REPO_ROOT, "look-and-feel", "org.kde.beardeddiamond.desktop", "contents", "previews", "splash.png"
)


def regenerate_images(palette):
    from PIL import Image, ImageDraw

    accent = palette["accent"]
    accent_light = palette["fg_button"]
    dim = palette["border"]

    S = 512
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S / 2, S / 2
    w, h = 170, 210
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
        d.line([a, b], fill=outline, width=4)
    img.save(os.path.join(IMAGES_DIR, "logo.png"))

    size = 256
    spinner = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spinner)
    bbox = [16, 16, size - 16, size - 16]
    sd.arc(bbox, 0, 360, fill=dim + (180,), width=14)
    sd.arc(bbox, 0, 90, fill=accent, width=14)
    sd.arc(bbox, 0, 20, fill=accent_light, width=14)
    spinner.save(os.path.join(IMAGES_DIR, "spinner.png"))

    bg = Image.new("RGB", (800, 600), palette["bg_main"])
    lw, lh = 220, 220
    logo_resized = img.resize((lw, lh), Image.LANCZOS)
    bg.paste(logo_resized, ((800 - lw) // 2, (600 - lh) // 2 - 20), logo_resized)
    bg.save(PREVIEW_FILE)

    print(f"wrote images to {IMAGES_DIR} and {PREVIEW_FILE}")


def update_qml_colors(palette):
    with open(QML_FILE) as f:
        text = f.read()
    text = re.sub(r'color: "#[0-9a-fA-F]{6}"', f'color: "{hex_str(palette, "bg_main")}"', text, count=1)
    text = re.sub(
        r'color: "#[0-9a-fA-F]{6}"\n\s*text: "Bearded Diamond"',
        f'color: "{hex_str(palette, "fg_normal")}"\n            text: "Bearded Diamond"',
        text,
    )
    with open(QML_FILE, "w") as f:
        f.write(text)
    print(f"wrote {QML_FILE}")


def generate(palette):
    regenerate_images(palette)
    update_qml_colors(palette)


if __name__ == "__main__":
    generate(load_palette(sys.argv[1]))
