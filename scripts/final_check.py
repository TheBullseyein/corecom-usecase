#!/usr/bin/env python3
"""Pre-delivery gate. Nothing ships until this passes.

Validates naming, pairing, dimensions, extension and folder names against the manifest,
then writes the delivery summary CSV. Builds the ZIP only with --zip and only on a clean run.

Usage:
  python3 scripts/final_check.py outputs/ work/manifest.csv
  python3 scripts/final_check.py outputs/ work/manifest.csv --zip delivery.zip
"""
import csv
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image

W, H = 1080, 1440
OUT_RE = re.compile(r"^(?P<sku>.+?)(?:_(?P<variant>print\d+))?_(?P<idx>[12])\.jpg$")


def main(outputs: Path, manifest: Path, zip_to: str | None) -> int:
    errors, warnings = [], []

    held = set()
    expected: set[tuple[str, str]] = set()
    if manifest.exists():
        with manifest.open() as fh:
            for row in csv.DictReader(fh):
                sku = row["sku"].strip()
                variant = row.get("variant_label", "").strip()
                if row.get("hold_reason", "").strip():
                    held.add((sku, variant))
                else:
                    expected.add((sku, variant))
    else:
        warnings.append(f"no manifest at {manifest} -- cannot verify nothing was missed")

    found: dict[tuple[str, str], dict[str, Path]] = defaultdict(dict)

    for f in sorted(outputs.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix != ".jpg":
            errors.append(f"{f}: extension must be lowercase .jpg")
            continue
        m = OUT_RE.match(f.name)
        if not m:
            errors.append(f"{f.name}: does not match SKU_N.jpg or SKU_printNN_N.jpg")
            continue
        sku, variant, idx = m["sku"], m["variant"] or "", m["idx"]

        if f.parent.name != sku:
            errors.append(f"{f}: sits in folder '{f.parent.name}' but names SKU '{sku}'")

        try:
            with Image.open(f) as im:
                if im.size != (W, H):
                    errors.append(f"{f.name}: {im.size[0]}x{im.size[1]}, must be {W}x{H}")
        except Exception as e:
            errors.append(f"{f.name}: unreadable ({type(e).__name__})")

        if idx in found[(sku, variant)]:
            errors.append(f"{f.name}: duplicate index _{idx}")
        found[(sku, variant)][idx] = f

    for key, imgs in sorted(found.items()):
        tag = f"{key[0]}{'/' + key[1] if key[1] else ''}"
        if set(imgs) != {"1", "2"}:
            errors.append(f"{tag}: has {sorted(imgs)}, needs exactly _1 and _2")

    for key in sorted(expected - set(found)):
        tag = f"{key[0]}{'/' + key[1] if key[1] else ''}"
        errors.append(f"{tag}: in manifest, not generated, and not marked held")
    for key in sorted(set(found) - expected - held):
        if expected:
            tag = f"{key[0]}{'/' + key[1] if key[1] else ''}"
            warnings.append(f"{tag}: generated but absent from manifest")

    summary = Path("work/delivery_summary.csv")
    summary.parent.mkdir(exist_ok=True)
    with summary.open("w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["sku", "variant_label", "view", "output_file", "dimensions"])
        for (sku, variant), imgs in sorted(found.items()):
            for idx, p in sorted(imgs.items()):
                wr.writerow([sku, variant or "single",
                             "front" if idx == "1" else "side_or_back",
                             p.name, f"{W}x{H}"])

    units = len(found)
    print(f"{units} unit(s), {sum(len(v) for v in found.values())} image(s)")
    print(f"{len(held)} held: " + (", ".join(f"{s}/{v}" if v else s for s, v in sorted(held)) or "none"))
    print(f"summary -> {summary}")

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")

    if errors:
        print(f"\n{len(errors)} error(s). Nothing ships. Fix these, then re-run.")
        return 1

    print("\nAll checks passed.")
    if zip_to:
        subprocess.run(["zip", "-rq", zip_to, "."], cwd=outputs, check=True)
        print(f"ZIP -> {outputs / zip_to}")
    else:
        print("Re-run with --zip delivery.zip once contact-sheet QC is signed off.")
    return 0


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    z = sys.argv[sys.argv.index("--zip") + 1] if "--zip" in sys.argv else None
    sys.exit(main(Path(a[0] if a else "outputs"),
                  Path(a[1] if len(a) > 1 else "work/manifest.csv"), z))
