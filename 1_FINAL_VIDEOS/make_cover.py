"""Builds the X cover images from one frame of a close-up render.

Usage (needs Pillow and imageio; the jumper .venv has both):
    jumper\\.venv\\Scripts\\python.exe make_cover.py <close_up.mp4> <frame_index> <out_dir> [cx cy zoom]
cx, cy (pixels in the source frame) and zoom (e.g. 1.5) crop closer on the robot first.
Writes cover_thumbnail_1920x1080.png (video thumbnail) and x_header_1500x500.png (profile header).
Text claims only what is true: laptop CPU, no GPU, KingKong's open-source Jumper toolkit.
"""
import sys

import imageio.v3 as iio
from PIL import Image, ImageDraw, ImageFilter, ImageFont

video, index, out_dir = sys.argv[1], int(sys.argv[2]), sys.argv[3]
frame = Image.fromarray(iio.imread(video, index=index)).convert("RGB")
W, H = frame.size  # 1920 x 1080
if len(sys.argv) > 4:
    cx, cy, zoom = float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
    cw, ch = W / zoom, H / zoom
    left = min(max(cx - cw / 2, 0), W - cw)
    top0 = min(max(cy - ch / 2, 0), H - ch)
    frame = frame.crop((int(left), int(top0), int(left + cw), int(top0 + ch))).resize((W, H), Image.LANCZOS)

IMPACT = r"C:\Windows\Fonts\impact.ttf"
BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
PINK, CYAN, WHITE, VIOLET = (255, 60, 190), (40, 235, 255), (255, 255, 255), (120, 60, 255)


def glow_text(img, xy, text, font, fill, glow, spread=10):
    """Draws text with a soft neon glow behind it."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(xy, text, font=font, fill=glow + (255,))
    layer = layer.filter(ImageFilter.GaussianBlur(spread))
    img.alpha_composite(layer)
    d = ImageDraw.Draw(img)
    d.text(xy, text, font=font, fill=fill, stroke_width=3, stroke_fill=(10, 10, 25))


def darken_bottom(img, start, strength=215):
    """Fades the bottom of the picture to dark so the text reads on any tile colour."""
    grad = Image.new("L", (1, img.height))
    for y in range(img.height):
        t = max(0.0, (y - start) / (img.height - start))
        grad.putpixel((0, y), int(strength * t))
    mask = grad.resize(img.size)
    dark = Image.new("RGBA", img.size, (8, 6, 24, 255))
    dark.putalpha(mask)
    img.alpha_composite(dark)


# ---- 16:9 thumbnail ----
thumb = frame.convert("RGBA")
darken_bottom(thumb, int(H * 0.52))
title = ImageFont.truetype(IMPACT, 235)
sub = ImageFont.truetype(BOLD, 62)
tag = ImageFont.truetype(BOLD, 44)
# Left column, so the robot (placed on the right by the crop) is never covered.
glow_text(thumb, (70, H - 800), "CRAB", title, WHITE, PINK, spread=18)
glow_text(thumb, (70, H - 560), "RAVE", title, WHITE, PINK, spread=18)
glow_text(thumb, (78, H - 290), "Trained on a laptop CPU.", sub, CYAN, CYAN, spread=8)
glow_text(thumb, (78, H - 215), "No GPU.", sub, CYAN, CYAN, spread=8)
ImageDraw.Draw(thumb).text((78, H - 110), "KingKong Jumper  |  #CrabRobot",
                           font=tag, fill=WHITE, stroke_width=2, stroke_fill=(10, 10, 25))
thumb.convert("RGB").save(f"{out_dir}/cover_thumbnail_1920x1080.png")

# ---- 3:1 profile header (X recommends 1500x500) ----
hw, hh = 1500, 500
crop_h = int(W * hh / hw)               # 3:1 slice of the 16:9 frame
top = int((H - crop_h) * 0.62)          # keep the crab and the floor, lose most of the empty sky
head = frame.crop((0, top, W, top + crop_h)).resize((hw, hh), Image.LANCZOS).convert("RGBA")
darken_bottom(head, int(hh * 0.45), 200)
t2 = ImageFont.truetype(IMPACT, 130)
s2 = ImageFont.truetype(BOLD, 38)
glow_text(head, (40, hh - 225), "CRAB RAVE", t2, WHITE, PINK, spread=12)
glow_text(head, (46, hh - 75), "A Jumper dance. Trained on a laptop CPU.", s2, CYAN, CYAN, spread=6)
head.convert("RGB").save(f"{out_dir}/x_header_1500x500.png")
print("saved", out_dir)
