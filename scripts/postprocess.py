#!/usr/bin/env python3
"""Standardize generated images to 1080x1440 portrait JPG, lowercase .jpg.

Centre-crops to 3:4 before resizing so the product stays centred and tight. Never pads
with whitespace -- the rules ban dead margins.

Usage:  python3 scripts/postprocess.py outputs/
"""
import sys
from pathlib import Path

from PIL import Image

W, H = 1080, 1440
TARGET_AR = W / H
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def standardize(path: Path) -> str:
    with Image.open(path) as im:
        im = im.convert("RGB")
        w, h = im.size
        ar = w / h
        if ar > TARGET_AR:                      # too wide -> crop sides
            new_w = int(h * TARGET_AR)
            left = (w - new_w) // 2
            im = im.crop((left, 0, left + new_w, h))
        elif ar < TARGET_AR:                    # too tall -> crop top/bottom evenly
            new_h = int(w / TARGET_AR)
            top = (h - new_h) // 2
            im = im.crop((0, top, w, top + new_h))
        im = im.resize((W, H), Image.LANCZOS)
        dest = path.with_suffix(".jpg")
        im.save(dest, "JPEG", quality=95, optimize=True, subsampling=0)
    if dest != path:
        path.unlink()
    return f"{w}x{h} -> {W}x{H}"


def main(root: Path) -> None:
    n = 0
    for img in sorted(root.rglob("*")):
        if img.suffix.lower() not in IMG_EXT or not img.is_file():
            continue
        print(f"{img.relative_to(root)}: {standardize(img)}")
        n += 1
    print(f"\n{n} images standardized to {W}x{H} .jpg")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "outputs"))
