# 3D-animated projects

**Summary**: Pixar-style 3D-animated shorts. Kyle's Antarctic Rescue, Lindsey: A Small Dream. Full record per project: models, settings, prompts, seeds, music and output files. Generated from `projects.json`.

**Sources**: projects.json; per-project notes from the session logs.

**Last updated**: 2026-09-23

---

Index of every project: [[projects]]. Other themes: [[projects-anime]] · [[projects-realistic]].

## Summary

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Kyle's Antarctic Rescue — 1-minute 3D-animated vertical short from a 5-panel comic](#kyle_rescue) | 2026-09-22 | delivered 2026-09-23 01:38 — 60.0 s, 1080x1920 + 2160x3840, rendered unattended overnight (see plan §0) | FLUX.2 [klein] 9B 576x1024 | LTX-2.3 22B [distilled] 1.1 via draw-things-cli ? min | Calm Ambient Dreamscape | `—` | — |
| 2 | [Lindsey: A Small Dream — 1-minute 3D-animated vertical short from Lindsey's 5-panel art comic](#lindsey_art) | 2026-09-23 | delivered 2026-09-23 17:26 — 59.96 s, 1080x1920 + 2160x3840 + 720x1280 (see plan §0) | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | — |

## Kyle's Antarctic Rescue — 1-minute 3D-animated vertical short from a 5-panel comic {#kyle_rescue}

- **Date**: 2026-09-22 · **Status**: delivered 2026-09-23 01:38 — 60.0 s, 1080x1920 + 2160x3840, rendered unattended overnight (see plan §0) · **Draw Things project**: `none — rendered with draw-things-cli (no project file)`
- **Files** (`raw/clips/`): `music/best_adventure_ever.mp3`, `kyle/masters/kyle_front.png`, `kyle/stills/s1..s8.png (+ *_v.txt video prompts)`, `kyle/clips/s1..s8_ltx_v1.mov, s2_ltx_v2.mov, s4_ltx_v2.mov`, `kyle/final/kyle_rescue_1080x1920.mp4`, `kyle/final/kyle_rescue_2160x3840.mp4`, `kyle/work/qc_notes.txt`
- **Notes**: Kyle is Kevin's son; consent confirmed 2026-09-22.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) via draw-things-cli |
| Size | 576x1024 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing (16) |

Prompt: `per scene — see scenes`

**I2V**

| Setting | Value |
|---|---|
| Model | LTX-2.3 22B [distilled] 1.1 via draw-things-cli |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 576x1024 |
| Frames | 249 |
| FPS | 25 |
| Steps | 8 |
| CFG | 1.0 |
| Shift | 5.0 |
| Sampler | TCD Trailing (19) |
| Strength | 100% |

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | forward, 8-frame tail->head crossfade, x6 = 27.4 s |
| Upscale | lanczos 1080x1920 |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *style head* — High-end 3D animated feature film still. Stylised characters in a realistic world: physically based lighting, real-looking ice, snow and ocean water, soft global illumination, subsurface scattering on skin, detailed fur and feathers, cinematic depth of field, rich natural colour.
- *kyle* — Kyle, one cheerful young East Asian boy with slightly stylised proportions, short spiky black hair, dark brown eyes and a wide smile, wearing a bright red and black insulated expedition parka with a round blue Antarctica patch on the left chest, black backpack straps over both shoulders, black gloves.
- *world* — Antarctica: turquoise icebergs, snowy white mountains, deep blue polar ocean.
- *video tail* — 3D animated feature film, smooth expressive character animation, soft cinematic lighting, consistent character, no text.
- *ufo* — a large silver-grey flying saucer with a glowing blue-violet dome on top and a ring of cyan and purple lights around its rim, crackling purple energy beams from its underside, no aliens visible.
- *penguins* — emperor penguins with black backs, white bellies and yellow-orange neck patches.
- *chick* — a fluffy grey emperor penguin chick with a white face and a black cap.
- *sidekick* — a small cheerful penguin wearing a little blue backpack.
- *seal* — a round silver-grey seal pup with big dark eyes.
- *orca* — an orca, glossy black with a white belly and a white eye patch.
- *whale* — a dark blue-grey humpback whale with long white-edged flippers.
- *ship* — an expedition icebreaker ship with a dark blue hull, a red band and a white superstructure.

**Rules**: Two stages: approved 3D masters first, then every shot locked to them. Paste only the locks for entities in the shot; say 'one boy'. Never write 'UFO' or 'alien'. No on-screen text. Face shots hold position; fast action ≤ 6 s; little camera motion. QC contact sheet vs the master before a shot counts. Hand the CLI a 9:16 image.


#### s1 — P1 ship crop (pad) → 3D at 0.8, keep 7 s

- **Engine**: LTX-2.3 via draw-things-cli

*Still prompt*

> Tall vertical frame: an expedition ship with a red and white hull small at the bottom on a turquoise sea, a towering iceberg and blue sky above, seagulls overhead.

*Video prompt*

> The camera tilts slowly down from the gliding seagulls to the ship as the sea swells gently around the icebergs.


#### s2 — P1 + kyle_front master (B1/B2/B3), keep 8 s

- **Engine**: LTX-2.3 via draw-things-cli

*Still prompt*

> Close-up of Kyle smiling and giving a thumbs up, the expedition ship and icebergs behind him.

*Video prompt*

> Kyle stays in place and smiles wider, his thumbs-up bobs once, his hair and parka stir in the wind; the camera holds still.


#### s3 — P2 → 3D at 0.8, saucer vs ufo master, keep 10 s

- **Engine**: LTX-2.3 via draw-things-cli

*Still prompt*

> Night: Kyle seen from behind looking up at a huge glowing flying saucer firing purple energy beams onto the ice.

*Video prompt*

> Kyle stays still at the bottom of the frame and turns his head slightly; above him the saucer hovers and pulses, purple beams crackle down onto the ice, which glows and cracks.


#### s4 — P3 → 3D at 0.8, keep 10 s

- **Engine**: LTX-2.3 via draw-things-cli

*Still prompt*

> Frightened penguins, a seal pup, an orca and a whale on breaking ice floes, purple beams lifting blocks of ice into the sky.

*Video prompt*

> Blocks of ice rise slowly into the beams as the floes split apart; the penguins huddle and flap, the seal looks up, the orca surfaces.


#### s5 — P4 + kyle_34 + sidekick masters (B1/B2), keep 6 s

- **Engine**: LTX-2.3 via draw-things-cli

*Still prompt*

> Kyle flying through the air aiming a glowing freeze-ray gadget, a small penguin with a backpack beside him.

*Video prompt*

> Kyle glides forward and the gadget fires a bright blue snowflake beam; frost spreads across the frame.


#### s6 — collage: ufo master over S4's 3D ice → klein 0.5, keep 6 s

- **Engine**: LTX-2.3 via draw-things-cli

*Still prompt*

> The flying saucer frozen inside a crust of blue ice above the icebergs, its beams gone.

*Video prompt*

> The ice crust cracks, the saucer shakes free and zips up into the stars, its light fading.


#### s7 — P5 + kyle_front + chick masters (B1/B2/B3), keep 10 s

- **Engine**: LTX-2.3 via draw-things-cli

*Still prompt*

> Sunrise: Kyle kneeling and hugging a fluffy penguin chick, happy penguins at the edges of the frame.

*Video prompt*

> Kyle hugs the chick and rocks gently, the chick nuzzles him, the penguins bob at the edges, the sun glints behind.


#### s8 — collage: S7's 3D animals + sunrise sky → klein 0.55, keep 8 s

- **Engine**: LTX-2.3 via draw-things-cli

*Still prompt*

> Tall sunrise frame: sky and sun above, a whale's tail and a line of penguins with a small boy far away on the ice below.

*Video prompt*

> The camera rises slowly into the glowing sky as the sun climbs.

## Lindsey: A Small Dream — 1-minute 3D-animated vertical short from Lindsey's 5-panel art comic {#lindsey_art}

- **Date**: 2026-09-23 · **Status**: delivered 2026-09-23 17:26 — 59.96 s, 1080x1920 + 2160x3840 + 720x1280 (see plan §0) · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **Files** (`raw/clips/`): `lindsey/masters/lindsey_front.png`, `lindsey/stills/s1..s8.png`, `lindsey/clips/s*_v*.mov`, `lindsey/final/lindsey_art_1080x1920.mp4`, `lindsey/final/lindsey_art_2160x3840.mp4`, `lindsey/final/lindsey_art_720x1280.mp4`, `lindsey/work/qc_notes.txt`, `music/emotional_children_piano.mp3`
- **Notes**: Lindsey is Kevin's daughter; consent confirmed 2026-09-23. Face from the comic, no photo.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 576x1024 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |

**I2V**

| Setting | Value |
|---|---|
| Model | Wan 2.2 High Noise Expert I2V A14B (8-bit S) |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 576x1024 |
| Frames | 81 |
| FPS | 16 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 4.95 |
| Sampler | DDIM Trailing |
| Strength | 100% |

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | forward, 8-frame tail->head crossfade, x6 = 27.4 s |
| Upscale | lanczos 1080x1920 |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

## Related pages
- [[projects]]
- [[runbook-living-painting]]
- [[draw-things-setup]]
