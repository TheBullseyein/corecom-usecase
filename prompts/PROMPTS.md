# Prompt Library

Assemble every prompt as: **Universal skeleton + the matching category lock + the SKU's
product lock (hex anchors + design zones) + the angle clause for image 1 or image 2.**

---

## Universal skeleton

```text
Create a standardized ecommerce catalogue model image from the attached product reference.

Output: {front-facing / side-angle / back-facing} {category} image for SKU {SKU}.

Product lock:
Preserve the exact product from the reference:
{base colour + hex anchors, motif/print/pattern, motif scale, border/edge placement,
pallu/end-panel, pleats, tassels/fringe, lace/net transparency, sheen, woven/embroidered
detail, blouse colour/style/sleeves/neck/back if visible}

Do not recolor, simplify, change motif scale, change border placement, change fabric texture,
invent embroidery, invent a missing back design, or replace the product with a generic garment.

Category lock:
{paste the category lock below}

Model:
Centered adult female ecommerce model, wheatish/fair skin tone, dark brown or black hair,
height appearance 5'6" or above, regular S-size build, pleasant subtle smile, slightly dynamic
natural catalogue pose.

Framing:
1080x1440 portrait ecommerce image. {head-to-hip / waist-to-feet / head-to-feet} framing.
Product/model centered. Tight clean crop with no unnecessary empty margins.

Background:
Plain premium studio ecommerce background in light grey or light beige only. Realistic
catalogue lighting and subtle floor/contact shadow. No props, decor, lifestyle room, busy
texture, text, logos, watermark, UI, price tag, or collage.

Consistency:
Keep the same model identity, outfit/styling, background, lighting, crop style, and product
handling across both images of this SKU/variant.

Angle:
{angle clause}
```

**Angle clause — image 1:** `Front/main catalogue view.`

**Angle clause — image 2:** `A clearly different 60-80 degree side or front-three-quarter
view. Torso, shoulders, hips and feet must rotate. Hand placement and drape arrangement must
differ from image 1. Do not repeat the front-facing pose.` — use a true back view only when a
back reference exists.

---

## Saree blouse / choli lock

Only when the raw clearly shows a stitched blouse: neckline, sleeve/armhole, back, closure or
garment construction visible.

```text
This product is an Indian saree blouse/choli, not Western topwear.
The model must wear it as a fitted cropped saree blouse/choli with authentic blouse
construction and proportions.
Preserve the exact sleeve length, sleeve shape, neckline, back style, edge piping, motif
placement, print density, embroidery, and fabric texture from the reference.
If sleeves are present, preserve sleeves. Do not make it sleeveless unless the source is
clearly sleeveless.
Do not turn it into a T-shirt, tank top, camisole, crop top, tunic, kurti, shirt, jacket,
vest, bodysuit, or sports top.
Do not hide the blouse under a pallu/dupatta. Use only minimal plain styling if needed so the
blouse remains primary.
Frame: head to hip.
```

---

## Saree lock

Only when the source is genuinely a saree, not a dupatta.

```text
This product is a saree. Drape it naturally as a saree on the model.
Preserve base colour, border width/placement, pallu design, pleats, motif scale,
transparency/sheen, woven details, edge colours, and blouse colour/style if visible.
Do not change border layout, simplify dense print, invent a blouse, or generate a generic saree.
If no back reference exists, do not invent a back design.
Frame: full body head to feet.
```

---

## Dupatta / stole / scarf lock

```text
This product is a dupatta/stole/scarf, not a saree.
Style it naturally over a plain ivory/off-white straight kurta with matching pants and simple
neutral footwear.
The dupatta must remain a long rectangular drape over shoulders, arms, neck, or one shoulder.
Do not create saree pleats, waist tuck, pallu styling, gown, kurta, dress, skirt, cape,
shawl-coat, or generic fabric garment.
Preserve exact source colour, transparency, motif, print density, border/edge, tassels/fringe,
lace/net openness, and end-panel details.
No jewellery/accessories that distract.
Frame: full body head to feet.
```

---

## Product-only dupatta inference lock

Only after explicit user approval — the hidden-layout risk is real.

```text
Approved product-only dupatta inference lock:
The reference is a product-only textile source, not a model-worn source. Use it only as the
exact textile design source and convert it into a natural model-worn dupatta over the ivory
outfit.
Preserve the complete visible textile design exactly: base colour, hue, saturation, brightness,
motif type, motif scale, spacing, density, borders, end panels, edge piping, tassels/fringe,
lace/net openness, transparency, sheen, and texture.
Do not reproduce source-photo composition, folded pile, rolled braid, hanger, hook, rack, hand,
mannequin, floor, dark cloth, white cloth, label text, SKU code, watermark, prop, or background.
No source-prop leakage: no ghosted flatlay/product photo, picture-in-picture textile panel,
source background patch, product shadow, staged prop, or collage element behind or beside the
model.
If the source is rolled/braided/folded/detail-only and does not show full layout, do not invent
hidden motifs, borders, or end panels. Keep the drape conservative and preserve visible
colour/texture cues only.
```

### Narrow rolled/braided trim addendum

```text
This is a narrow rolled/braided dupatta/scarf/trim-like textile source.
Keep it narrow and accessory-like when worn. Do not expand it into a full-width shawl, saree,
cape, blanket, or wide dupatta unless the opened source proves that width.
Preserve visible braid/crinkle/texture/tassel cues and exact colour only.
```

---

## Colour anchor clause — append whenever colour fidelity matters

```text
Colour anchors from selected crop: {#HEX}. Match this {plain-language colour} exactly.
Do not make it mustard, beige, pastel, cream, greyed, dull, muted, or hue-shifted.
Render it bright and saturated exactly as the reference.
```

## Multi-zone clause — append whenever the raw has more than one pattern zone

```text
This product has {N} distinct design zones: {zone 1 description and location},
{zone 2 description and location}. Reproduce each zone in its correct location with its
correct density and motif scale. Do not apply one uniform pattern across the whole product.
```
