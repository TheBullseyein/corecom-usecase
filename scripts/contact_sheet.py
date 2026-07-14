#!/usr/bin/env python3
"""Build QC contact sheets: raw references beside both outputs, one row per SKU/variant.

Every batch gets one of these before delivery. Visual QC is final -- this sheet exists so
category, colour, motif zones, variant isolation and pair angle can be judged by eye against
the raw, not against memory.

Usage:  python3 scripts/contact_sheet.py raws/ outputs/ work/qc/
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
CELL = 300
PAD = 12
LABEL_H = 34
ROWS_PER_SHEET = 8

# SKU_1.jpg | SKU_print01_2.jpg
OUT_RE = re.compile(r"^(?P<sku>.+?)(?:_(?P<variant>print\d+))?_(?P<idx>[12])\.jpg$", re.I)


def fit(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    im.thumbnail((CELL, CELL), Image.LANCZOS)
    canvas = Image.new("RGB", (CELL, CELL), (245, 245, 245))
    canvas.paste(im, ((CELL - im.width) // 2, (CELL - im.height) // 2))
    return canvas


def placeholder(text: str) -> Image.Image:
    canvas = Image.new("RGB", (CELL, CELL), (232, 232, 232))
    d = ImageDraw.Draw(canvas)
    d.text((CELL // 2 - 28, CELL // 2 - 6), text, fill=(120, 120, 120))
    return canvas


def main(raws: Path, outputs: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)

    units: dict[tuple[str, str], dict[str, Path]] = defaultdict(dict)
    for f in sorted(outputs.rglob("*.jpg")):
        m = OUT_RE.match(f.name)
        if not m:
            print(f"  !! unparseable output name: {f.name}")
            continue
        key = (m["sku"], m["variant"] or "")
        units[key][m["idx"]] = f

    raw_map = {p.name: sorted(q for q in p.iterdir() if q.suffix.lower() in IMG_EXT)
               for p in raws.iterdir() if p.is_dir()}

    keys = sorted(units)
    sheets = [keys[i:i + ROWS_PER_SHEET] for i in range(0, len(keys), ROWS_PER_SHEET)]

    for n, chunk in enumerate(sheets, 1):
        max_raw = max((len(raw_map.get(sku, [])) for sku, _ in chunk), default=1)
        max_raw = max(1, min(max_raw, 3))          # cap raw refs shown at 3
        cols = max_raw + 2
        sheet_w = cols * CELL + (cols + 1) * PAD
        row_h = CELL + LABEL_H + PAD
        sheet = Image.new("RGB", (sheet_w, len(chunk) * row_h + PAD), (255, 255, 255))
        draw = ImageDraw.Draw(sheet)

        for r, (sku, variant) in enumerate(chunk):
            y = PAD + r * row_h
            label = f"{sku}{'  [' + variant + ']' if variant else '  [single]'}"
            draw.text((PAD, y), label, fill=(20, 20, 20))
            draw.text((PAD + (max_raw) * (CELL + PAD) + PAD, y),
                      "OUT _1 (front)", fill=(20, 20, 20))
            draw.text((PAD + (max_raw + 1) * (CELL + PAD) + PAD, y),
                      "OUT _2 (side/back)", fill=(20, 20, 20))

            cells = []
            refs = raw_map.get(sku, [])[:max_raw]
            for i in range(max_raw):
                cells.append(fit(refs[i]) if i < len(refs) else placeholder("no raw"))
            for idx in ("1", "2"):
                p = units[(sku, variant)].get(idx)
                cells.append(fit(p) if p else placeholder("MISSING"))

            for c, cell in enumerate(cells):
                sheet.paste(cell, (PAD + c * (CELL + PAD), y + LABEL_H))

        out = dest / f"contact_sheet_{n:02d}.jpg"
        sheet.save(out, "JPEG", quality=92)
        print(f"wrote {out}  ({len(chunk)} units)")

    print(f"\n{len(units)} units across {len(sheets)} sheet(s).")
    print("Check each row: category / colour + hex / motif scale + zone placement / "
          "variant isolation / pair angle / background / crop / anatomy / prop leakage.")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(Path(a[0] if a else "raws"),
         Path(a[1] if len(a) > 1 else "outputs"),
         Path(a[2] if len(a) > 2 else "work/qc"))
