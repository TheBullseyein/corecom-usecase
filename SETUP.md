# Setup — Pixelbin apparel pipeline in Claude Desktop

## What you do (about 5 minutes)

1. Install **Claude Desktop** and open it.
2. Unzip this kit somewhere permanent, e.g. `~/apparel-pipeline/`.
3. Drop your raw SKU folders into `raws/` — one folder per SKU, **folder names exactly as
   received**, images inside. Nothing else in there.
4. Confirm the **Pixelbin connector** is enabled in Desktop (Settings → Connectors) on the
   account you verified.
5. Open the `apparel-pipeline` folder in Claude Code (Desktop → Code tab → open folder), and
   say: **"Read CLAUDE.md and start the raw audit."**

`CLAUDE.md` loads automatically as project instructions, so the operating rules, the credit
gate and every past-failure lesson are live from the first message. You don't have to re-explain
anything.

## Expected folder shape

```
apparel-pipeline/
  CLAUDE.md                 <- operating rules, auto-loaded
  SETUP.md                  <- this file
  prompts/PROMPTS.md        <- universal skeleton + category locks
  scripts/
    audit_raws.py           <- step 1: inventory + flags
    postprocess.py          <- 1080x1440 lowercase .jpg
    contact_sheet.py        <- QC sheets, raws beside outputs
    final_check.py          <- pre-delivery gate + summary CSV + ZIP
  work_manifest_template.csv
  raws/                     <- YOU put SKU folders here
  outputs/                  <- created during generation
  work/                     <- inventory, manifest, QC sheets, summary
```

## What I do, in order

1. **`audit_raws.py`** → inventory CSV: dimensions, dominant hex anchors, low-res flags,
   landscape sources, and cross-SKU duplicate-pattern detection (colour-aware, so two
   colourways of one print are *not* falsely merged).
2. **Visual audit.** I open every folder and look. Category call, variant count by eye,
   source type, design zones. The script's flags are prompts for review, never verdicts.
3. **Manifest** (`work/manifest.csv`, from the template): one row per SKU/variant with
   category, source type, product lock, hex anchors, design zones, view plan, output names,
   credit estimate, hold reason.
4. **`estimate-prediction-cost`** on Pixelbin → I quote you exact image count and credits and
   **wait for your approval**. The confirmation token is enforced server-side, so I cannot
   generate around this gate even by accident.
5. **2–3 samples first.** You look. Only then the batch.
6. **`contact_sheet.py`** → QC every row against the raw.
7. **`postprocess.py`** → standardize to 1080x1440.
8. **`final_check.py`** → naming, pairing, dimensions, folder names, held-SKU reconciliation
   against the manifest. Exits non-zero and refuses to ZIP if anything is off.

## The uploads

Pixelbin's `create-prediction` only takes public HTTPS URLs. In Desktop I have shell access, so
I mint a presigned URL per file (`request-upload-url`) and `curl` it up from your disk myself.
You never paste a URL by hand. That's the whole reason for moving to Desktop.

## Cost

Nano Banana Pro: **4 credits/image → 8 credits per SKU/variant** (2 images).
Multi-variant rules are active, so a 6-variant combo pack is 6 units = 48 credits, not 8.
I quote before every batch.
