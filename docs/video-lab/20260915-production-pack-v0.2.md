# BILA VIDEO LAB — Production Pack v0.2

Date: 2026-09-15
Status: execution-ready / actual video generation pending generator access

## Goal

Use sellable showcase videos to attract SMEs, local businesses, ecommerce brands and marketing teams. Public flow: case → service → brief → order → review → revision → balance → delivery. Public site, client view and BILA System OS should share one order record rather than create a parallel CRM.

## First 12 showcase cases

1. C01 NOIR COFFEE — premium coffee / new beverage
2. C02 MORI SKIN — skincare serum / product image
3. C03 DAYDAY DESSERT — dessert / restaurant Reel
4. C04 FORM STUDIO — fitness / local-business lead generation
5. C05 LUME HAIR — salon / service transformation
6. C06 NOMA HOME — home / lifestyle product
7. C07 KASA TEA — tea / beverage
8. C08 ARC SPEAKER — tech / product launch
9. C09 MOMO PET — pet / product lifestyle
10. C10 OPENING NIGHT — opening / campaign
11. C11 SUMMER DROP — seasonal retail / campaign
12. C12 CITY STAY — hospitality / local business

MVP production order: C01 → C02 → C03 → C04.

All showcase brands are fictional until explicitly replaced by approved client material.

---

# C01 — NOIR COFFEE

## Deliverable

- 15-second vertical master, 9:16
- Four short clips assembled in post to protect product and liquid consistency
- No baked-in logo or subtitles during generation; BILA typography added in post
- Audience: coffee shops, beverage brands, restaurant new-product campaigns

## Art direction

- Palette: deep espresso brown / warm amber / graphite / soft cream
- Lens feel: 50–85mm commercial macro
- Lighting: warm side morning light + soft cream bounce
- Surface: dark graphite stone
- Product: clear minimalist tumbler, realistic condensation
- Physics: realistic espresso, ice and cream; no impossible floating objects
- Typography safe area: upper third

## 15s edit map

### Clip A — Beans / 0–3s
Macro roasted coffee beans, controlled dolly-in, light grazing bean texture.

### Clip B — Espresso / 3–7s
Clear tumbler on graphite stone. Espresso pours in a continuous physically plausible stream. Condensation and reflections remain stable.

### Clip C — Ice + swirl / 7–11s
Two or three ice cubes drop into dark coffee. One restrained cream ribbon creates a natural marble swirl.

### Clip D — Hero / 11–15s
Locked hero shot, slow 3–5% push-in, warm highlight, negative space above.

Post text suggestion:

NOIR COFFEE  
SLOW DOWN. WAKE UP.

## Generator prompts

### A / Beans
Cinematic macro commercial shot of freshly roasted coffee beans on a dark graphite surface, warm amber morning light grazing the beans, rich texture and natural oils, 85mm macro lens feel, shallow depth of field, controlled slow dolly-in, premium beverage advertising, photoreal, no text, no people, physically realistic, vertical 9:16.

### B / Espresso
Premium commercial beverage shot, a clear minimalist tumbler centered on dark graphite stone, deep espresso pouring smoothly into the glass, realistic condensation, realistic refraction and reflections, warm amber side light, 50–85mm lens feel, shallow depth of field, slow controlled camera push, physically plausible liquid, no warped glass, no extra objects, no readable text, vertical 9:16.

### C / Ice + Cream
High-end iced coffee commercial macro shot, clear tumbler with dark espresso, two or three realistic ice cubes dropping into the drink followed by a single subtle ribbon of cream creating a natural marble swirl, realistic splash scale, stable glass geometry, warm amber side light, graphite background, slow motion, premium food advertising, photoreal, no text, no hands, vertical 9:16.

### D / Hero
Luxury iced coffee hero shot on dark graphite stone, clear tumbler filled with deep iced espresso, crisp condensation droplets, a few roasted beans near the base, warm morning light from upper left, controlled reflections, shallow depth of field, very slow push-in, clean negative space in upper third for typography, premium commercial photography, photoreal, no logo, no text, no people, vertical 9:16.

## Negative guidance

warped glass, duplicated ice, impossible splash, floating beans, excessive milk, melting cup, text artifacts, hands, people, logos, labels, random letters, camera shake, fisheye, surreal object morphing

## Post checklist

- Select best four clips
- Match exposure and white balance
- Add 15s music bed
- Preserve sensory SFX if usable
- Add BILA typography in post
- Output 1080×1920 H.264 master
- After master approval: thumbnail + 1:1 cover + 6s cutdown

---

# System OS mapping

Public layer:
- case_id
- category
- use_case
- hero_video
- thumbnail
- short_pitch
- CTA / 我要做這種

Order layer:
- order_id
- source_case_id
- customer_id
- offer_snapshot
- deposit_status
- brief
- approved_storyboard
- versions[]
- revision_rounds
- final_approval
- balance_status
- invoice_status
- delivery_assets[]

Internal OS:
- capacity
- production_stage
- assigned_executor
- generation_cost
- external_cost
- due_date
- payment_reconciliation
- invoice_action
- event_log

## Current blocker

Attempted Magnific generation on 2026-09-15. Account balance could not resolve the wallet, and image generation then failed. The next production step is to restore a callable generator (Magnific wallet/credits or another connected generator such as TapNow). Once available, C01 can go straight into A→D generation without redoing strategy or storyboard.
