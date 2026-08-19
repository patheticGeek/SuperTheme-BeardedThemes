"""
Regenerates the Plasma (ksplash) splash screen images and inline QML colors
under <theme>/look-and-feel/<kde_lookandfeel_id>/contents/splash/.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import hex_str, load_palette  # noqa: E402


def regenerate_images(palette, images_dir, preview_file):
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
    img.save(os.path.join(images_dir, "logo.png"))

    size = 256
    spinner = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spinner)
    bbox = [16, 16, size - 16, size - 16]
    sd.arc(bbox, 0, 360, fill=dim + (180,), width=14)
    sd.arc(bbox, 0, 90, fill=accent, width=14)
    sd.arc(bbox, 0, 20, fill=accent_light, width=14)
    spinner.save(os.path.join(images_dir, "spinner.png"))

    bg = Image.new("RGB", (800, 600), palette["bg_main"])
    lw, lh = 220, 220
    logo_resized = img.resize((lw, lh), Image.LANCZOS)
    bg.paste(logo_resized, ((800 - lw) // 2, (600 - lh) // 2 - 20), logo_resized)
    bg.save(preview_file)

    print(f"wrote images to {images_dir} and {preview_file}")


def update_qml_colors(palette, spec, qml_file):
    with open(qml_file) as f:
        text = f.read()
    text = re.sub(r'color: "#[0-9a-fA-F]{6}"', f'color: "{hex_str(palette, "bg_main")}"', text, count=1)
    text = re.sub(
        r'color: "#[0-9a-fA-F]{6}"\n\s*text: "[^"]*"',
        f'color: "{hex_str(palette, "fg_normal")}"\n            text: "{spec.display_name}"',
        text,
    )
    with open(qml_file, "w") as f:
        f.write(text)
    print(f"wrote {qml_file}")


def generate(palette, spec):
    lookandfeel_dir = os.path.join(spec.dir, "look-and-feel", spec.kde_lookandfeel_id)
    splash_dir = os.path.join(lookandfeel_dir, "contents", "splash")
    images_dir = os.path.join(splash_dir, "images")
    qml_file = os.path.join(splash_dir, "Splash.qml")
    preview_file = os.path.join(lookandfeel_dir, "contents", "previews", "splash.png")

    os.makedirs(images_dir, exist_ok=True)
    regenerate_images(palette, images_dir, preview_file)
    update_qml_colors(palette, spec, qml_file)


if __name__ == "__main__":
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
