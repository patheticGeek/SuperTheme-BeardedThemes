"""
Regenerates the KDE global-theme picker mockup images:
<theme>/look-and-feel/<kde_lookandfeel_id>/contents/previews/{preview.png,fullscreenpreview.jpg}
-- a small fake desktop (titlebar, sidebar rows, one selected/accent row,
traffic-light dots, taskbar) drawn from the palette.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from palette import load_palette  # noqa: E402


def draw_mockup(palette, spec, size):
    from PIL import Image, ImageDraw

    W, H = size
    scale = W / 800

    def s(v):
        return int(v * scale)

    bg = palette["bg_main"]
    titlebar = palette["bg_titlebar"]
    sidebar_row = palette["fg_inactive"]
    accent = palette["accent"]
    positive = palette["positive"]
    neutral = palette["neutral"]
    negative = palette["negative"]

    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    # window chrome
    win = [s(120), s(60), W - s(120), H - s(70)]
    d.rectangle(win, fill=palette["bg_main"], outline=palette["border"], width=max(1, s(1)))

    tb_h = s(40)
    d.rectangle([win[0], win[1], win[2], win[1] + tb_h], fill=titlebar)
    d.text((win[0] + s(20), win[1] + s(10)), spec.display_name, fill=palette["fg_normal"])

    for i, color in enumerate((positive, neutral, negative)):
        cx = win[2] - s(20) - i * s(30)
        cy = win[1] + tb_h // 2
        r = s(8)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    # sidebar rows
    rows_x = win[0] + s(20)
    row_w = s(112)
    selected_row = 1
    for i in range(5):
        y = win[1] + tb_h + s(30) + i * s(35)
        dot_color = accent if i == selected_row else sidebar_row
        d.rectangle([rows_x, y, rows_x + s(8), y + s(8)], fill=dot_color)
        bar_color = accent if i == selected_row else sidebar_row
        d.rectangle([rows_x + s(20), y + s(2), rows_x + s(20) + row_w, y + s(10)], fill=bar_color)

    # content lines
    content_x = win[0] + s(170)
    content_w = win[2] - content_x - s(20)
    for i in range(6):
        y = win[1] + tb_h + s(25) + i * s(45)
        color = accent if i == 2 else sidebar_row
        w = content_w if i % 2 == 0 else int(content_w * 0.85)
        d.rectangle([content_x, y, content_x + w, y + s(10)], fill=color)

    # taskbar
    tb2_h = s(50)
    d.rectangle([0, H - tb2_h, W, H], fill=titlebar)
    r = s(15)
    cx, cy = s(35), H - tb2_h // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    d.rectangle(
        [s(85), cy - s(18), s(330), cy + s(18)], fill=palette["bg_main"]
    )
    d.rectangle([s(100), cy - s(9), s(120), cy + s(9)], fill=accent)

    for i, color in enumerate((positive, neutral, negative)):
        cx2 = W - s(150) + i * s(35)
        r2 = s(8)
        d.ellipse([cx2 - r2, cy - r2, cx2 + r2, cy + r2], fill=color)
    d.text((W - s(55), cy - s(8)), "12:30", fill=palette["fg_normal"])

    return img


def generate(palette, spec):
    lookandfeel_dir = os.path.join(spec.dir, "look-and-feel", spec.kde_lookandfeel_id)
    previews_dir = os.path.join(lookandfeel_dir, "contents", "previews")
    os.makedirs(previews_dir, exist_ok=True)

    preview_path = os.path.join(previews_dir, "preview.png")
    draw_mockup(palette, spec, (800, 600)).save(preview_path)
    print(f"wrote {preview_path}")

    fullscreen_path = os.path.join(previews_dir, "fullscreenpreview.jpg")
    draw_mockup(palette, spec, (1200, 900)).convert("RGB").save(fullscreen_path, quality=90)
    print(f"wrote {fullscreen_path}")


if __name__ == "__main__":
    from theme_spec import get

    generate(load_palette(sys.argv[1]), get(sys.argv[2]))
