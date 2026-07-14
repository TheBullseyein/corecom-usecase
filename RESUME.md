# Pipeline resume state — apparel model image generation

Last updated: 2026-07-14. Provider: Pixelbin MCP, model `nanoBananaPro.generate`.
Pixelbin cloud: `winter-mouse-5d2216`. Org: 16958166.

## Why this file exists — environment egress blocker

This remote session's egress policy **blocks all Pixelbin hosts**
(`delivery.pixelbin.io`, `cdn.pixelbin.io`, `api.pixelbin.io` → CONNECT 403).
`storage.googleapis.com` is reachable, but Pixelbin result objects there require
auth. The Pixelbin **MCP tools still work** (they run server-side), so generation
and save-to-storage succeed — but this container **cannot download result bytes**,
which blocks the local back half of the pipeline here: visual QC, `postprocess`
→ 1080x1440, `contact_sheet`, `final_check`, ZIP.

**To finish:** start a NEW session on an environment whose allowed-domains include
`delivery.pixelbin.io` and `cdn.pixelbin.io`, then follow "Resume steps" below.

## Credit ledger

- Spent so far: **12 credits** (3 sample images × 4 credits actual).
- NOTE: `estimate-prediction-cost` reported 2 cr/image, but real `consumedCredits`
  was **4 cr/image**. Trust 4/image for planning. Full batch-2 (12 images) ≈ 48 cr.

## Batch 2 — 5 dupatta SKUs (manifest: work/manifest.csv)

| SKU | product | variants | status |
|---|---|---|---|
| 41930178 | green/purple/orange sheer floral net-lace dupatta | 3 (print01/02/03) | print01 front generated |
| 41930171 | rani-red bandhani + gold gota border | 1 | front generated |
| 41930180 | magenta bandhani + gold gota border | 1 | not started |
| 41930182 | plain beige chiffon stole + picot edge | 1 | front generated |
| 41930166 | 5 rolled bandhani colourways | 5 | **HELD** (rolled-only, hidden layout; needs opened refs or product-only-inference approval) |

## Generated so far — 3 sample fronts (PENDING VISUAL QC)

Raw output is 1792x2400 PNG, aspect 3:4. Standardize to 1080x1440 .jpg via
`scripts/postprocess.py` once downloadable.

| SKU / view | prediction_id | permanent URL |
|---|---|---|
| 41930178_print01_1 (green net-lace, front) | nanoBananaPro--generate--019f61c3-a7b2-700e-958c-2ded327b3caf | https://cdn.pixelbin.io/v2/winter-mouse-5d2216/original/apparel-final/batch2/result_0.png |
| 41930171_1 (red bandhani, front) | nanoBananaPro--generate--019f61c3-ed67-744d-a7d1-24f166349db5 | https://cdn.pixelbin.io/v2/winter-mouse-5d2216/original/apparel-final/batch2/41930171/result_0.png |
| 41930182_1 (beige stole, front) | nanoBananaPro--generate--019f61c4-11d5-700e-958c-70e02eff6ad7 | https://cdn.pixelbin.io/v2/winter-mouse-5d2216/original/apparel-final/batch2/41930182/result_0.png |

30-day delivery URLs (same images): `https://delivery.pixelbin.io/predictions/outputs/30d/nanoBananaPro/generate/<prediction_id-tail>/result_0.png`

## Uploaded references already on Pixelbin (reusable)

Base: `https://cdn.pixelbin.io/v2/winter-mouse-5d2216/original/apparel-refs/`
- 41930178_image_3.jpeg (green worn front), 41930178_image_4.jpeg (green worn back)
- 41930171_image_1.jpeg (drape), 41930171_image_4.jpeg (border detail)
- 41930182_image_1.jpeg (drape), 41930182_image_4.jpeg (edge detail)

Still to upload for remaining images: `_2` side-view refs and refs for 41930180,
plus 41930178 purple/orange colourway refs (image_1 group + image_2 closeup).

## Resume steps (in an unblocked session)

1. Re-extract raws (private, gitignored): unzip the two drive downloads into `raws/`.
2. Download the 3 generated samples (permanent URLs above) → `outputs/<SKU>/<name>.png`.
3. `python3 scripts/postprocess.py outputs/` → 1080x1440 .jpg.
4. Visual QC each against its raw (colour/hex, category=dupatta, drape, sheerness,
   border zone, no prop/watermark leakage, framing). Fix or accept.
5. On pass: generate remaining batch-2 images — 41930178 print01 `_2` (back, ref
   image_4), print02 + print03 (purple/orange, both views), 41930171 `_2`,
   41930180 `_1`+`_2`, 41930182 `_2`. estimate → generate → download → postprocess.
6. `python3 scripts/contact_sheet.py raws/ outputs/ work/qc/` and QC.
7. `python3 scripts/final_check.py outputs/ work/manifest.csv --zip delivery_batch2.zip`.

## Still fully pending

- **Batch 1** (10 saree-blouse SKUs) — awaiting decisions: duplicate pair
  39830649≡39832934; combos 39830685 & 39830689 (1 vs 2 variants).
- **41930166** hold decision.
