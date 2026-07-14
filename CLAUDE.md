# Ecommerce Apparel Model Image Generation — Operating Rules

Provider: **Pixelbin MCP**. Model: **nanoBananaPro.generate (4 credits/image)**.
Mode: **normal multi-variant rules** (NOT the special pending/recovery one-variant rule).

Privacy: use only raws in `raws/`, this file, and artifacts in this project. Do not import
memory from other chats.

## The gate — never skip a step

Raw visual audit -> category decision -> variant count -> product lock (hex + design zones)
-> view plan -> preflight manifest -> credit estimate -> **user approval** -> 2-3 samples
-> batch -> contact-sheet QC -> post-process -> final check -> ZIP.

No prediction before a manifest row exists. No batch before samples pass visual QC.
No ZIP before final_check passes.

## Hard output rules

- 1080x1440 portrait JPG, lowercase `.jpg`.
- Folder name = original SKU folder name, exactly.
- Single-print SKU: `SKU_1.jpg`, `SKU_2.jpg`.
- Multi-variant: `SKU_print01_1.jpg`, `SKU_print01_2.jpg`, `SKU_print02_1.jpg`, ...
- `_1` = front/main. `_2` = side/front-three-quarter, or back **only if a back reference exists**.
- Exactly 2 images per SKU/variant unless explicitly held.
- Never invent a back view.
- Product centered, tight crop, no dead margins.

## Model + background

Adult female ecommerce model. Wheatish/fair skin, dark brown or black hair, 5'6"+ appearance,
regular S build. Pleasant subtle smile, slightly dynamic catalogue pose.
Same model identity, styling, crop, lighting, background across both images of a unit.
Background: plain light grey or light beige studio only, subtle contact shadow.
Banned: lifestyle room, decor, plants, furniture, props, text, logos, watermarks, UI, collage.

## Category lock — the #1 historical failure

Process each SKU as its **actual visible category**, never blouse-by-default.
- Saree blouse/choli must read as an Indian blouse/choli — not a T-shirt, tank, camisole,
  crop top, kurti. Preserve sleeves if the source has sleeves.
- Dupatta/stole/scarf must stay a dupatta over a plain ivory/off-white straight kurta with
  matching pants — never a saree, pallu, gown, cape, shawl-coat, skirt.
- Narrow rolled/braided trim stays narrow. Do not inflate into a shawl.
- Uncertain category -> **pause and ask**.

## Framing

Topwear: head to hip. Bottomwear: waist to feet. Saree/dupatta/full-length: head to feet.
Saree blouse/choli: head to hip; blouse stays primary and visible.

## Fidelity — hard rules

- Sample hex anchors from the raw before generating. Put them in the prompt. State saturation
  and brightness explicitly. "Same colour family" is a fail.
- Log **every** design zone (border, pallu/end-panel, dense vs sparse zone, net/lace body,
  contrast piping, tassels). A multi-zone raw must not become one uniform pattern.
- Count **every** visible variant before generating. Never render two variants in one image.
- Second image must be a real 60-80 degree rotation. Torso, shoulders, hips, feet rotate;
  hands and drape differ. If it could pass as another front shot, reject.
- No source-prop leakage: no flatlay/rolled/hanger/label/watermark/background patch in output.

## Credit safety

- `estimate-prediction-cost` before every `create-prediction`. Pass the `confirmation_token`
  verbatim. Trust the returned number over any expected number.
- Quote exact image count and credit count, get approval, then generate.
- Stop the moment an error pattern appears. Repair only failed images. If repairs fail twice,
  hold the SKU.
- Holding a SKU beats spending credits on a hallucinated product.

## Repair vs regenerate vs hold

Repair: colour close but off saturation/hue; isolated background inconsistency; small artifact
away from product/model boundary.
Regenerate: wrong category, saree/dupatta/blouse confusion, wrong motif or zone layout,
variants mixed, source pasted/flatlay in output, substantially wrong colour.
Hold: source doesn't show enough to infer design; no opened/model-worn ref and no approval;
hidden layout/border/end-panel; model keeps hallucinating after repairs.

## Source confidence

Model-worn = highest. Opened/spread = medium-high. Hanger = medium.
Rolled/braided/folded/detail-only = **low — colour and texture only, never layout**.
Mixed opened+rolled: use the opened ref for design, ignore the rolled one.

## Known lessons (do not repeat)

42954890 dupatta->saree. 42954746 variants merged into one frame. 43325492 duplicate pair
angle. 41904971 / 43325508 (#FBF96B) / 43326338 / 43326529 colour drift and muted output.
43279362 two pattern zones flattened to one. 43325666 / 43325719 six variants, five generated.
42955002_2 inpaint patch bled over the product. 43326174 / 43326311 duplicate source pattern
across SKUs — flag, don't silently accept.

## Final instruction

When in doubt, pause and ask. Do not guess category, hidden back design, hidden layout,
missing variants, or exact colour.
