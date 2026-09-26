# 3D-animated projects

**Summary**: Pixar-style 3D-animated shorts. Kyle's Antarctic Rescue, Lindsey: A Small Dream. Full record per project: models, settings, prompts, seeds, music and output files. Generated from each version's `spec.json`.

**Sources**: projects/*/*/spec.json; per-project notes from the session logs.

**Last updated**: 2026-09-26

---

Index of every project: [[projects]]. Other themes: [[projects-anime]] · [[projects-realistic]].

## Summary

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [BOT Builders Champion — the FLL team's films](#bot_builders_champion) | 2026-09-23 | delivered 2026-09-25 03:00 — 59.08 s, 3840x2160 + 1920x1080, 11 shots (competition-floor wide dropped); see wiki/fll-champions-plan.md | FLUX.2 [klein] 9B 1024x576 | LTX-2.3 22B [distilled] 1.1 10 min | Light Adventure | `—` | — |
| 2 | [Kyle's Antarctic Rescue — 1-minute 3D-animated vertical short from a 5-panel comic](#kyle_rescue) | 2026-09-22 | delivered 2026-09-23 01:38 — 60.0 s, 1080x1920 + 2160x3840, rendered unattended overnight (see plan §0) | FLUX.2 [klein] 9B 576x1024 | LTX-2.3 22B [distilled] 1.1 via draw-things-cli ? min | Calm Ambient Dreamscape | `—` | [▶ watch](https://youtu.be/KscAwvCi6iQ) |
| 3 | [Lindsey: A Small Dream — 1-minute 3D-animated vertical short from Lindsey's 5-panel art comic](#lindsey_art) | 2026-09-23 | delivered 2026-09-23 17:26 — 59.96 s, 1080x1920 + 2160x3840 + 720x1280 (see plan §0) | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | [▶ watch](https://youtu.be/lbU-_73MliI) |

## BOT Builders Champion — the FLL team's films {#bot_builders_champion}

- **Date**: 2026-09-23 · **Status**: delivered 2026-09-25 03:00 — 59.08 s, 3840x2160 + 1920x1080, 11 shots (competition-floor wide dropped); see wiki/fll-champions-plan.md · **Version**: `v3-photo-cut` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: 59 s 16:9 3D-animated film built from the family's photographs, with masters rebuilt per child; rendered headless with draw-things-cli.

**Versions**

| Version | What it is | Status | YouTube |
|---|---|---|---|
| `v1-anime-loop` | Shinkai-style 9:16 living-painting loop of the team's Coastal Roots Farm visit, wide view with no faces; Wan 2.2 I2V driven through the Draw Things window. | done (v2) | [▶ watch](https://youtu.be/-Mf2UThasCg) |
| `v2-comic-cut` | 63.5 s 16:9 3D-animated film built from the team's 3-page comic; rendered headless with draw-things-cli. | delivered 2026-09-24 04:11 — 63.5 s (planned 90; five-kid rule), 1920x1080 + 3840x2160 + 1280x720 (see plan §0) | — |
| `v3-photo-cut` | 59 s 16:9 3D-animated film built from the family's photographs, with masters rebuilt per child; rendered headless with draw-things-cli. | delivered 2026-09-25 03:00 — 59.08 s, 3840x2160 + 1920x1080, 11 shots (competition-floor wide dropped); see wiki/fll-champions-plan.md | — |

- **Files** (`projects/bot_builders_champion/v3-photo-cut/`): `fll_champions/*.jpg|webp|png (13 source photos)`, `fll/masters/{kei,kyle,lindsey,lola,cheryl,table,venue,farm_logs,farm_barn,farm_coop}.png`, `fll/stills/s1..s12.png + per-shot prompts`, `fll/clips/s*_v*.mov`, `fll/final/fll_champions_3840x2160.mp4`, `fll/final/fll_champions_1920x1080.mp4`
- **Notes**: Kevin is the team's coach; consent for all five children confirmed by him 2026-09-23. 3D-animated look chosen over photoreal precisely because five recurring child faces are the heaviest identity load attempted here — stylised faces hold through LTX motion. No on-screen text. Source photos are real: every shot still is a klein edit of a photo (identity from pixels), and the two invented shots (s6, s7) chain off approved stills. Companion to the comic-derived fll_bot_builders film, which covers the same team from drawn panels. This one differs in approach: every still here is a klein edit of a real photo at --strength 1.0 (the garage build table, the farm gate, the logs, the team portrait), where the comic film works from drawn panels. Two rules came out of it — see the run notes. Known flaw in the delivered cut: it mixes two generations of stills — seven shots rendered 2026-09-23 before the masters existed, four restaged 2026-09-25 from the rebuilt Pixar masters. The same children are drawn by two recipes and it is visible across cuts. Not re-done; recorded as the lesson (wiki/fll-champions-plan.md §3b).

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |

Prompt: `per shot — projects/bot_builders_champion/v3-photo-cut/stills/sN.txt`

**I2V**

| Setting | Value |
|---|---|
| Model | LTX-2.3 22B [distilled] 1.1 |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 1024x576 |
| Frames | 249 |
| FPS | 25 |
| Steps | 8 |
| CFG | 1.0 |
| Shift | 5.0 |
| Sampler | TCD Trailing |
| Strength | 100% |
| I2V time (min) | 10 |

Prompt: `per shot — projects/bot_builders_champion/v3-photo-cut/stills/sN_v.txt`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none — xfade 0.75 via scripts/assemble_film.sh |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus -> 3840x2160 HEVC 10-bit |
| Music | Light Adventure — 331music, Pixabay (cdn.pixabay.com/download/audio/2026/08/26/audio_f1cf54e839.mp3), 2:12; first 59 s under the LTX ambience at 0.45, 2 s fade out; final mean -18.8 dB, peak -5.5 dB |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *style head* — Re-render this photograph as a frame from a high-end 3D animated feature film — Pixar-style stylisation with photoreal skin, hair and fabric, soft cinematic lighting, shallow depth of field, warm colour grade. Keep every child recognisable: same ethnicity and skin tone, pure black hair, same haircut, same eye and eyelid shape, same face shape.
- *style tail* — Remove all text, lettering, logos and brand marks from clothing, signs and props. Photoreal materials, no outlines, cinematic 16:9 framing, no extra people beyond those described.
- *team* — five children, left to right in the team photo: **Kei** (boy, white t-shirt, straight dark fringe); **Kyle** (boy, orange t-shirt, short dark hair); **Lindsey** (girl, long straight black hair, dark sleeveless dress); **Lola** (girl, pink t-shirt, hair tied back); **Cheryl** (girl, white textured top, hair in braids)
- *video tail* — Smooth cinematic motion, 3D animated feature film look.
- *table* — the team's LEGO mission table: a wooden-framed table holding the printed jungle mission mat — winding blue river, sandy clearings, dense pale-green canopy — with the same brick models on it: a tall brown tree tower in the middle, lime-green ring structures, small grey machine buildings, and the team's little wheeled robot
- *farm* — Coastal Roots Farm: huge pale fallen logs crossing on wood-chip ground under a big sycamore; a red-brown timber barn with pale metal roof and blue trim above rows of vegetables and artichokes; a small brown wheeled chicken coop in a netted run of dry straw with brown and white hens
- *venue* — the tournament: a school gymnasium with pale timber floor and painted court lines, folded basketball hoops, rows of plain gold and cream banners with no lettering, tall windows, dark folded bleachers; black-framed competition tables holding printed jungle mission mats, low white net barriers, adult referees in black and white striped shirts, background crowd distant and out of focus with no recognisable faces

**Rules**: Every still is an edit of a real photo at --strength 1.0 (identity comes from pixels, never from text). No on-screen text anywhere — the model cannot spell, and the team emblem is described as 'a small round colourful emblem with no lettering'. Group shots must say 'their faces, hair and clothes stay exactly the same' or LTX restyles them. Camera holds still in every shot: a moving camera makes LTX invent people at the frame edge. Face shots (s5, s7, s8) are the only ones where all five are recognisable; s3 is backs, s4 is wide, s2 and s6 have no people. Learned 2026-09-23: (1) an edit inherits the SOURCE POSE — chaining the closing portrait off the celebration still reproduced the jump across three seeds; naming the new pose both ways fixed it ('both feet flat on the ground, arms relaxed at their sides… nobody jumping'). (2) klein drops people from a crowded group: only 1 of 3 seeds of the celebration shot kept all five children, so group shots need 3 seeds and a headcount at pick time. Names mapped 2026-09-24 (Kei, Kyle, Lindsey, Lola, Cheryl). Kyle and Lindsey also have masters in the kyle_rescue and lindsey_art films — those came from drawings, this project's come from photographs. A table master (masters/table.png) locks the mission mat and the brick models so every build/competition shot shows the same table. Look changed 2026-09-24 from 3D-animated to photoreal. Master recipe that preserves a real child: name the features to keep (ethnicity, skin tone, hair colour/texture/cut, eye and eyelid shape, eyebrows, nose, mouth, jawline, age) and ban the drifts (do not westernise, do not enlarge or round the eyes, do not lighten hair or eyes, do not make the child look older, do not idealise). Asking for '3D animated character' substitutes klein's default face. Also neutralise the source photo's light: a sunset backlight turned black hair brown until the prompt said so. klein warms dark hair toward brown on every pass — say 'pure black hair, not brown, not chestnut, no warm highlights' for the black-haired children. Master sources that worked: Kyle = ship-deck photo, Lindsey = indoor portrait, Kei = garage crop, Lola + Cheryl = kitchen photo. Style history: started 3D-animated, tried photoreal on 2026-09-24 (faces read as strangers), returned to Pixar. Open issues at pause: Kyle's spiked fringe is combed flat by the model and must be named explicitly; the five faces read similar under Pixar styling, so wardrobe and hair have to carry who-is-who in group shots. One generation per film: when the style head or any master changes, re-render every still, not just the new shots — a stale still still matches its own clip and passes QC, so the mismatch only shows up in the cut.

## Kyle's Antarctic Rescue — 1-minute 3D-animated vertical short from a 5-panel comic {#kyle_rescue}

- **Date**: 2026-09-22 · **Status**: delivered 2026-09-23 01:38 — 60.0 s, 1080x1920 + 2160x3840, rendered unattended overnight (see plan §0) · **Version**: `v1-drawthings-cli` · **Draw Things project**: `none — rendered with draw-things-cli (no project file)`
- **This version**: Rendered headless with draw-things-cli via scripts/film_run.py.
- **Files** (`projects/kyle_rescue/v1-drawthings-cli/`): `music/best_adventure_ever.mp3`, `kyle/masters/kyle_front.png`, `kyle/stills/s1..s8.png (+ *_v.txt video prompts)`, `kyle/clips/s1..s8_ltx_v1.mov, s2_ltx_v2.mov, s4_ltx_v2.mov`, `kyle/final/kyle_rescue_1080x1920.mp4`, `kyle/final/kyle_rescue_2160x3840.mp4`, `kyle/work/qc_notes.txt`
- **Notes**: Kyle is Kevin's son; consent confirmed 2026-09-22.

- **YouTube**: [youtu.be/KscAwvCi6iQ](https://youtu.be/KscAwvCi6iQ) *(YouTube Short, 2160x3840 master)*

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/KscAwvCi6iQ" title="Kyle's Antarctic Rescue — 1-minute 3D-animated vertical short from a 5-panel comic" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

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

- **Date**: 2026-09-23 · **Status**: delivered 2026-09-23 17:26 — 59.96 s, 1080x1920 + 2160x3840 + 720x1280 (see plan §0) · **Version**: `v1-drawthings-cli` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: Rendered headless with draw-things-cli via scripts/film_run.py.
- **Files** (`projects/lindsey_art/v1-drawthings-cli/`): `lindsey/masters/lindsey_front.png`, `lindsey/stills/s1..s8.png`, `lindsey/clips/s*_v*.mov`, `lindsey/final/lindsey_art_1080x1920.mp4`, `lindsey/final/lindsey_art_2160x3840.mp4`, `lindsey/final/lindsey_art_720x1280.mp4`, `lindsey/work/qc_notes.txt`, `music/emotional_children_piano.mp3`
- **Notes**: Lindsey is Kevin's daughter; consent confirmed 2026-09-23. Face from the comic, no photo.

- **YouTube**: [youtu.be/lbU-_73MliI](https://youtu.be/lbU-_73MliI) *(YouTube Short, 2160x3840 master)*

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/lbU-_73MliI" title="Lindsey: A Small Dream — 1-minute 3D-animated vertical short from Lindsey's 5-panel art comic" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

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
