#!/usr/bin/env python3
"""Step 1 of the gate: inventory every raw SKU folder before anything is generated.

Produces work/raws_inventory.csv and prints a flag summary.
This does NOT decide category or variant count -- that is a visual judgement made by
looking at the images. This script surfaces the facts and the risks so the visual audit
is fast and nothing is missed.

Usage:  python3 scripts/audit_raws.py raws/
"""
import csv
import hashlib
import sys
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".avif", ".heic"}
LOW_RES_PX = 800          # shorter side below this -> detail risk
TARGET_AR = 1080 / 1440   # 0.75


def phash(path: Path) -> str:
    """Structure + colour signature.

    Structure alone is not enough: two different colourways of the same print are DIFFERENT
    products (the 42954746 lesson), while a flat/low-variance image carries no structure at
    all and would collide with every other flat image. So: bail out on near-zero variance,
    and fold a coarse RGB signature into the hash.
    """
    try:
        im = Image.open(path)
        g = im.convert("L").resize((8, 8), Image.LANCZOS)
        c = im.convert("RGB").resize((2, 2), Image.LANCZOS)
    except Exception:
        return ""

    px = list(g.getdata())
    avg = sum(px) / len(px)
    var = sum((p - avg) ** 2 for p in px) / len(px)
    if var < 25:                       # essentially featureless -- not a fingerprint
        return ""

    bits = "".join("1" if p > avg else "0" for p in px)
    colour = "".join(f"{v >> 5:01x}" for rgb in c.getdata() for v in rgb)  # 3-bit per channel
    return f"{int(bits, 2):016x}-{colour}"


def dominant_hex(path: Path, k: int = 5) -> list[str]:
    """Top colours from a centre crop, ignoring near-white/near-grey studio background."""
    try:
        im = Image.open(path).convert("RGB")
    except Exception:
        return []
    w, h = im.size
    im = im.crop((int(w * 0.2), int(h * 0.2), int(w * 0.8), int(h * 0.8)))
    im = im.resize((80, 80), Image.LANCZOS)
    im = im.quantize(colors=16, method=Image.MEDIANCUT).convert("RGB")
    counts = Counter(im.getdata())
    out = []
    for (r, g, b), _ in counts.most_common():
        mx, mn = max(r, g, b), min(r, g, b)
        if mx > 235 and mx - mn < 18:      # blown-out white / paper background
            continue
        if mx < 32:                        # near black shadow
            continue
        out.append(f"#{r:02X}{g:02X}{b:02X}")
        if len(out) == k:
            break
    return out


def main(root: Path) -> None:
    rows = []
    hashes: dict[str, list[str]] = defaultdict(list)

    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        imgs = sorted(p for p in folder.iterdir() if p.suffix.lower() in IMG_EXT)
        if not imgs:
            rows.append({
                "sku": folder.name, "file": "", "width": "", "height": "",
                "aspect": "", "dominant_hex": "", "phash": "",
                "flags": "EMPTY_FOLDER",
            })
            continue

        for img in imgs:
            flags = []
            try:
                with Image.open(img) as im:
                    w, h = im.size
            except Exception as e:
                rows.append({
                    "sku": folder.name, "file": img.name, "width": "", "height": "",
                    "aspect": "", "dominant_hex": "", "phash": "",
                    "flags": f"UNREADABLE({type(e).__name__})",
                })
                continue

            if min(w, h) < LOW_RES_PX:
                flags.append("LOW_RES")
            ar = w / h
            if ar > 1.05:
                flags.append("LANDSCAPE_SRC")
            if abs(ar - TARGET_AR) > 0.25:
                flags.append("FAR_FROM_3:4")

            ph = phash(img)
            if ph:
                hashes[ph].append(f"{folder.name}/{img.name}")

            rows.append({
                "sku": folder.name,
                "file": img.name,
                "width": w,
                "height": h,
                "aspect": f"{ar:.3f}",
                "dominant_hex": " ".join(dominant_hex(img)),
                "phash": ph,
                "flags": ",".join(flags),
            })

    if not rows:
        print(f"No SKU folders found under {root}/. "
              "Drop one folder per SKU into raws/ (folder names exactly as received, "
              "images inside), then re-run.")
        return

    # duplicate-source pattern check (the 43326174 / 43326311 lesson)
    dupes = {h: v for h, v in hashes.items() if len(v) > 1}
    dupe_files = {f for v in dupes.values() for f in v}
    for r in rows:
        key = f"{r['sku']}/{r['file']}"
        if key in dupe_files:
            r["flags"] = ",".join(filter(None, [r["flags"], "DUPLICATE_SOURCE"]))

    out = Path("work"); out.mkdir(exist_ok=True)
    dest = out / "raws_inventory.csv"
    with dest.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)

    skus = {r["sku"] for r in rows}
    flagged = [r for r in rows if r["flags"]]
    print(f"{len(skus)} SKU folders, {len(rows)} images -> {dest}")
    print(f"{len(flagged)} flagged images")
    tally = Counter(f for r in flagged for f in r["flags"].split(",") if f)
    for name, n in tally.most_common():
        print(f"  {name}: {n}")
    if dupes:
        print("\nDuplicate source patterns (flag with user before generating):")
        for v in dupes.values():
            print("  " + "  ==  ".join(v))
    print("\nNEXT: open every folder visually. Decide category and count variants by eye. "
          "These flags are prompts for review, not verdicts.")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "raws"))
