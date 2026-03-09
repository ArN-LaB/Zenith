#!/usr/bin/env python3
"""
Generate Zenith app icon — clean 5-pointed star (star.fill style).
White star on dark indigo, matching the SF Symbol used throughout the app.
"""

import math
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

SIZE = 1024
CENTER = SIZE // 2

BG_TOP = (18, 18, 42)      # dark indigo top
BG_BOT = (8,  8, 22)       # near-black bottom
STAR_COLOR = (255, 255, 255, 255)  # pure white


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_background(img):
    """Dark indigo vertical gradient."""
    draw = ImageDraw.Draw(img)
    for y in range(SIZE):
        c = lerp_color(BG_TOP, BG_BOT, y / SIZE)
        draw.line([(0, y), (SIZE, y)], fill=c)


def draw_star(img):
    """5-pointed star matching SF Symbols star.fill (inner/outer ratio = 0.382)."""
    outer_r = int(SIZE * 0.360)
    inner_r = int(outer_r * 0.382)
    pts = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((CENTER + r * math.cos(angle), CENTER + r * math.sin(angle)))
    overlay = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(overlay).polygon(pts, fill=STAR_COLOR)
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay))


def apply_squircle_mask(img):
    """macOS continuous-corner (squircle) mask, ~22% radius."""
    mask = Image.new('L', (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, SIZE - 1, SIZE - 1],
        radius=int(SIZE * 0.2237), fill=255
    )
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    result = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    result.paste(img, mask=mask)
    return result


def generate_icon():
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw_background(img)
    draw_star(img)
    return apply_squircle_mask(img)


def export_sizes(master, out_dir):
    sizes = [
        ("icon_16x16.png",     16),
        ("icon_16x16@2x.png",  32),
        ("icon_32x32.png",     32),
        ("icon_32x32@2x.png",  64),
        ("icon_64x64.png",     64),
        ("icon_128x128.png",   128),
        ("icon_128x128@2x.png",256),
        ("icon_256x256.png",   256),
        ("icon_256x256@2x.png",512),
        ("icon_512x512.png",   512),
        ("icon_512x512@2x.png",1024),
    ]
    for filename, px in sizes:
        resized = master.resize((px, px), Image.LANCZOS)
        (out_dir / filename).write_bytes(b"")  # ensure path exists
        resized.save(str(out_dir / filename), 'PNG')
        print(f"  ✓ {filename} ({px}×{px})")


def create_icns(icon_dir, icns_path):
    iconset = icon_dir.parent / "Zenith.iconset"
    iconset.mkdir(exist_ok=True)
    names = [
        "icon_16x16.png", "icon_16x16@2x.png",
        "icon_32x32.png",  "icon_32x32@2x.png",
        "icon_128x128.png","icon_128x128@2x.png",
        "icon_256x256.png","icon_256x256@2x.png",
        "icon_512x512.png","icon_512x512@2x.png",
    ]
    for name in names:
        src = icon_dir / name
        if src.exists():
            shutil.copy2(str(src), str(iconset / name))
    result = subprocess.run(
        ["iconutil", "--convert", "icns", "--output", str(icns_path), str(iconset)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  ✓ {icns_path.name}")
    else:
        print(f"  ✗ iconutil: {result.stderr}")
    shutil.rmtree(str(iconset), ignore_errors=True)


def main():
    script_dir = Path(__file__).parent.parent   # scripts/ → repo root
    icon_dir = script_dir / "Sources" / "Zenith" / "Assets.xcassets" / "AppIcon.appiconset"
    icns_path = script_dir / "Resources" / "Zenith.icns"

    print("==> Generating Zenith icon (star.fill style)")
    master = generate_icon()

    master_path = icon_dir / "icon_master_1024.png"
    master.save(str(master_path), 'PNG')
    print(f"  ✓ Master: {master_path.name}")

    print("==> Exporting sizes...")
    export_sizes(master, icon_dir)

    print("==> Creating .icns...")
    create_icns(icon_dir, icns_path)
    print("==> Done!")


if __name__ == "__main__":
    main()

