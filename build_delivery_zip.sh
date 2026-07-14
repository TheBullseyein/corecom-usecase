#!/usr/bin/env bash
# Downloads the 3 generated batch-2 sample fronts from Pixelbin, standardizes
# them to 1080x1440 .jpg (if Python + Pillow are present), and zips them.
# Run this on any machine with normal internet (this repo's container cannot
# reach cdn.pixelbin.io). Usage:  bash build_delivery_zip.sh
set -euo pipefail

BASE="https://cdn.pixelbin.io/v2/winter-mouse-5d2216/original/apparel-final/batch2"
OUT="delivery_batch2_samples"
rm -rf "$OUT" && mkdir -p "$OUT/41930178" "$OUT/41930171" "$OUT/41930182"

echo "Downloading 3 results..."
curl -fSs -o "$OUT/41930178/41930178_print01_1.png" "$BASE/result_0.png"
curl -fSs -o "$OUT/41930171/41930171_1.png"          "$BASE/41930171/result_0.png"
curl -fSs -o "$OUT/41930182/41930182_1.png"          "$BASE/41930182/result_0.png"

# Standardize to 1080x1440 .jpg if Pillow is available (uses scripts/postprocess.py if present).
if python3 -c "import PIL" 2>/dev/null; then
  echo "Standardizing to 1080x1440 .jpg..."
  if [ -f scripts/postprocess.py ]; then
    python3 scripts/postprocess.py "$OUT/"
  else
    python3 - "$OUT" <<'PY'
import sys, pathlib
from PIL import Image
W,H=1080,1440; AR=W/H
for p in pathlib.Path(sys.argv[1]).rglob("*.png"):
    im=Image.open(p).convert("RGB"); w,h=im.size; ar=w/h
    if ar>AR:
        nw=int(h*AR); l=(w-nw)//2; im=im.crop((l,0,l+nw,h))
    elif ar<AR:
        nh=int(w/AR); t=(h-nh)//2; im=im.crop((0,t,w,t+nh))
    im=im.resize((W,H), Image.LANCZOS)
    im.save(p.with_suffix(".jpg"),"JPEG",quality=95,subsampling=0); p.unlink()
    print(f"  {p.name} -> 1080x1440 .jpg")
PY
  fi
else
  echo "Pillow not found; leaving full-resolution PNGs (not resized)."
fi

echo "Zipping..."
( cd "$OUT" && zip -rq "../${OUT}.zip" . )
echo "Done -> ${OUT}.zip"
