# Projects Registry

**Summary**: Every video project so far — one record each with the exact models, settings, prompts, seeds, music and output files. Generated from `projects.json`; edit that file, not this page.

**Sources**: projects.json; per-project notes from the session logs.

**Last updated**: 2026-09-22

---

## Summary

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Coastal wildflowers (v1)](#coast) | 2026-09-20 | superseded by coast_v2 | Wan 2.2 High Noise Expert T2V A14B 576x1280 | Wan 2.2 High Noise 24 min | — | `—` | — |
| 2 | [Coastal wildflowers (v2)](#coast_v2) | 2026-09-20 | done | FLUX.2 [klein] 9B 1024x1792 | Wan 2.2 High Noise 15.5 min | Calm Ambient Dreamscape | `coast_v2_final.mp4` | [▶ watch](https://youtu.be/W8fy4bhGOEU) |
| 3 | [Torrey Pines, San Diego](#torrey) | 2026-09-20 | done | FLUX.2 [klein] 9B 1024x1792 | Wan 2.2 High Noise 15 min | Calm Ambient Dreamscape | `torrey_final.mp4` | [▶ watch](https://youtu.be/nRU-Upd2E3o) |
| 4 | [Golden Gate, San Francisco](#goldengate) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Calm Ambient Dreamscape | `goldengate_final.mp4` | [▶ watch](https://youtu.be/h8ic1_9Q9mI) |
| 5 | [Mt. Rainier from Paradise](#rainier) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 15.5 min | Calm Ambient Dreamscape | `rainier_final.mp4` | [▶ watch](https://youtu.be/JJB154LbBi0) |
| 6 | [Cyberpunk city, rain, neon](#cyberpunk) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Neon Synthwave Drive | `cyberpunk_final.mp4` | [▶ watch](https://youtu.be/GrNTNQCqKnk) |
| 7 | [FLL BOT Builders — Coastal Roots Farm, wide view](#fll_farm) | 2026-09-20 | done (v2) | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Calm Ambient Dreamscape | `fll_farm_v2_final.mp4` | [▶ watch](https://youtu.be/-Mf2UThasCg) |
| 8 | [Dragon Epic — 1-minute photoreal short, family hero face](#dragon_epic) | 2026-09-21 | in progress — scene 1A posted | FLUX.2 [klein] 9B 1280x768 | Wan 2.2 High Noise 47 min | The Dragon's Breath | `—` | [▶ watch](https://youtu.be/Xzu-c5yX8uo) |
| 9 | [Three-minute film — recurring characters (subject TBD)](#film3min) | 2026-09-21 | planning | FLUX.2 [klein] 9B 1024x576 | Wan 2.2 High Noise 15 min | TBD | `—` | — |
| 10 | [Lost City — hyper-real rider on a raptor-dragon entering jungle ruins](#lost_city) | 2026-09-21 | in progress — clips at 4K+music: s2, s3, s7, s8, s10, s14; s9 trimmed (4.6 s, drift after); s11 stills rejected (klein duplicates the creature); s12 not started | FLUX.2 [klein] 9B 1280x768 | LTX-2.3 22B [distilled] 1.1 (production engine — see ltx_10s) — Wan 2.2 High Noise I2V (8-bit S) + Low Noise refiner 10% for locked-camera shots at 768p 49 min | Mystical orchestral theme with ancient flute | `—` | [▶ watch](https://youtu.be/68sq_jZqu6c) |

## YouTube playlist — [AI-Vids](https://www.youtube.com/playlist?list=PLJx49Sf61wKQ)

<div class="yt"><iframe src="https://www.youtube.com/embed/videoseries?list=PLJx49Sf61wKQ" title="AI-Vids" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>


## Defaults (apply unless a record overrides)

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

Style suffix appended to every still prompt: `Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.`

## Coastal wildflowers (v1) {#coast}

- **Date**: 2026-09-20 · **Status**: superseded by coast_v2 · **Draw Things project**: `Untitled-35903`
- **Files** (`raw/clips/`): `coast.mov`, `coast_loop.mp4`
- **Notes**: First end-to-end run. Still too soft — Wan-T2V at native res. Led to FLUX for stills.

**Still**

| Setting | Value |
|---|---|
| Model | Wan 2.2 High Noise Expert T2V A14B (q8) @ 1 frame |
| Size | 576x1280 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 5 |
| Sampler | UniPC Trailing |
| LoRA | Lightning High-Noise 100% |

Prompt: `anime painting of a coastal hillside at golden hour, wildflowers in the foreground, tall grass, ocean waves below a cliff, towering orange and pink cumulus clouds, warm sunset light, birds in the sky, Makoto Shinkai style, highly detailed, soft painterly light`

**I2V**

| Setting | Value |
|---|---|
| Model | Wan 2.2 High Noise Expert I2V A14B (8-bit S) |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 576x1280 |
| Frames | 81 |
| FPS | 16 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 5 |
| Sampler | UniPC Trailing |
| Strength | 100% |
| I2V time (min) | 24 |

Prompt: `static camera, gentle ocean waves rolling onto the shore, grass and wildflowers swaying in a soft breeze, birds drifting slowly across the sky, clouds moving slowly, subtle motion, minimal movement`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | ping-pong x3 (rejected: reverses motion), then forward crossfade |
| Upscale | lanczos 1080x1920 |

## Coastal wildflowers (v2) {#coast_v2}

- **Date**: 2026-09-20 · **Status**: done · **Draw Things project**: `Untitled-35903`
- **Files** (`raw/clips/`): `coast_flux_1024x1792.png`, `coast_flux_576x1024.png`, `coast_v2.mov`, `coast_v2_loop.mp4`, `coast_v2_final.mp4`
- **Notes**: First run with wrong refiner (6-bit, not downloaded) produced washed-out noise; re-run with 8-bit S.

- **YouTube**: [youtu.be/W8fy4bhGOEU](https://youtu.be/W8fy4bhGOEU)

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/W8fy4bhGOEU" title="Coastal wildflowers (v2)" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x1792 then lanczos crop/downscale to 576x1024 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |
| Seed | 20104302 |

Prompt: `A breathtaking anime background painting of a coastal hillside at golden hour. Foreground: dense wildflowers in white, pink, yellow and blue with tall swaying grass, every petal crisply painted. Middle ground: lush green cliffs dropping to a turquoise bay with rolling white surf on a sandy cove. Sky: enormous towering cumulus clouds lit orange and pink by the setting sun, a few tiny birds in silhouette. Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.`

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
| Shift | 5 |
| Sampler | UniPC Trailing |
| Strength | 100% |
| Seed | 1180755429 |
| I2V time (min) | 15.5 |

Prompt: `static camera, gentle ocean waves rolling onto the shore, grass and wildflowers swaying in a soft breeze, birds drifting slowly across the sky, clouds moving slowly, subtle motion, minimal movement`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | forward, 8-frame tail->head crossfade, x6 = 27.4 s |
| Upscale | lanczos 1080x1920 |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

## Torrey Pines, San Diego {#torrey}

- **Date**: 2026-09-20 · **Status**: done · **Draw Things project**: `Untitled-91451`
- **Files** (`raw/clips/`): `torrey_flux_1024x1792.png`, `torrey_flux_576x1024.png`, `torrey.mov`, `torrey_loop.mp4`, `torrey_final.mp4`
- **Notes**: Second run of the runbook; refiner trap caught by checklist.

- **YouTube**: [youtu.be/nRU-Upd2E3o](https://youtu.be/nRU-Upd2E3o)

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/nRU-Upd2E3o" title="Torrey Pines, San Diego" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x1792 then downscale to 576x1024 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |
| Seed | 1190544862 |

Prompt: `A breathtaking anime background painting of Torrey Pines State Reserve in San Diego at golden hour. Foreground: a windswept Torrey pine tree with twisted branches and long needles, golden coastal sage and yellow wildflowers on a sandy bluff. Middle ground: dramatic eroded golden sandstone cliffs with deep gullies dropping to a wide sandy beach and the Pacific Ocean, small white surf lines. Sky: enormous towering cumulus clouds lit orange and pink by the setting sun over the ocean, a few tiny seagulls in silhouette. Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.`

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
| Shift | 5 |
| Sampler | UniPC Trailing |
| Strength | 100% |
| Seed | 284526412 |
| I2V time (min) | 15 |

Prompt: `static camera, gentle ocean waves rolling onto the beach below the cliffs, pine needles and coastal grass swaying in a soft breeze, seagulls drifting slowly across the sky, clouds moving slowly, subtle motion, minimal movement`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | forward, 8-frame tail->head crossfade, x6 = 27.4 s |
| Upscale | lanczos 1080x1920 |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

## Golden Gate, San Francisco {#goldengate}

- **Date**: 2026-09-20 · **Status**: done · **Draw Things project**: `Untitled-82025`
- **Files** (`raw/clips/`): `goldengate.mov`, `goldengate_loop.mp4`, `goldengate_final.mp4`
- **Notes**: Proved native 576x1024 still is good enough; runbook switched to it. Mac was locked 2.5 h with Save sheet open — render survived.

- **YouTube**: [youtu.be/h8ic1_9Q9mI](https://youtu.be/h8ic1_9Q9mI)

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/h8ic1_9Q9mI" title="Golden Gate, San Francisco" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 576x1024 (first native-res run, no downscale) |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |

Prompt: `A breathtaking anime background painting of the Golden Gate Bridge in San Francisco at golden hour, viewed from the Marin Headlands. Foreground: golden coastal grass and orange California poppies on a rocky bluff, a windswept cypress tree. Middle ground: the International Orange suspension bridge spanning the bay, its towers rising out of a low bank of fog, small sailboats on the water. Background: the San Francisco skyline glowing in warm light, Alcatraz in the distance. Sky: enormous towering cumulus clouds lit orange and pink by the setting sun, a few tiny seagulls in silhouette. Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.`

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
| Seed | 601904108 |
| I2V time (min) | 16 |

Prompt: `static camera, fog slowly drifting under the bridge, gentle waves on the bay, sailboats gliding slowly, grass and poppies swaying in a soft breeze, seagulls drifting slowly across the sky, clouds moving slowly, subtle motion, minimal movement`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | forward, 8-frame tail->head crossfade, x6 = 27.4 s |
| Upscale | lanczos 1080x1920 |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

## Mt. Rainier from Paradise {#rainier}

- **Date**: 2026-09-20 · **Status**: done · **Draw Things project**: `Untitled-70762`
- **Files** (`raw/clips/`): `rainier.mov`, `rainier_loop.mp4`, `rainier_final.mp4`
- **Notes**: First zero-click run — export Save button pressed by automation.

- **YouTube**: [youtu.be/JJB154LbBi0](https://youtu.be/JJB154LbBi0)

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/JJB154LbBi0" title="Mt. Rainier from Paradise" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 576x1024 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |

Prompt: `A breathtaking anime background painting of Mount Rainier from the Paradise meadows near Seattle at golden hour. Foreground: subalpine meadow dense with purple lupine, magenta paintbrush and white avalanche lilies, a few dark pointed fir trees. Middle ground: rolling green slopes and a small glacial stream catching the light. Background: the massive glaciated volcano filling the sky, its snow and ice lit pink and orange by the setting sun. Sky: enormous towering cumulus clouds lit orange and pink, a few tiny birds in silhouette. Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.`

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
| I2V time (min) | 15.5 |

Prompt: `static camera, wildflowers and meadow grass swaying in a soft breeze, the stream flowing gently, birds drifting slowly across the sky, clouds moving slowly over the mountain, subtle motion, minimal movement`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | forward, 8-frame tail->head crossfade, x6 = 27.4 s |
| Upscale | lanczos 1080x1920 |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

## Cyberpunk city, rain, neon {#cyberpunk}

- **Date**: 2026-09-20 · **Status**: done · **Draw Things project**: `Untitled-76300`
- **Files** (`raw/clips/`): `cyberpunk.mov`, `cyberpunk_loop.mp4`, `cyberpunk_final.mp4`
- **Notes**: Night scene works with the same style suffix. Music swapped from the calm-ambient default to synthwave on 2026-09-20.

- **YouTube**: [youtu.be/GrNTNQCqKnk](https://youtu.be/GrNTNQCqKnk)

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/GrNTNQCqKnk" title="Cyberpunk city, rain, neon" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 576x1024 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |

Prompt: `A breathtaking anime background painting of a rain-soaked cyberpunk city street at night. Foreground: wet asphalt reflecting neon, a noodle stall with steam rising, stacked crates, a puddle mirroring the signs. Middle ground: narrow street canyon lined with holographic billboards in magenta, cyan and orange, tangled cables, kanji and katakana neon signs, a few silhouetted pedestrians with umbrellas. Background: towering megastructures fading into purple haze, flying vehicles with red tail lights, a giant glowing advertisement screen. Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.`

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
| I2V time (min) | 16 |

Prompt: `static camera, rain falling steadily, neon signs flickering and glowing, steam rising from the noodle stall, puddle reflections rippling, pedestrians walking slowly with umbrellas, flying vehicles drifting across the sky, subtle motion, minimal movement`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | forward, 8-frame tail->head crossfade, x6 = 27.4 s |
| Upscale | lanczos 1080x1920 |
| Music | Neon Synthwave Drive — alex-morgan, Pixabay (cdn.pixabay.com/audio/2026/06/04/audio_ae113c6d69.mp3), 2:48; 1 s fade in / 2 s fade out, vol 0.9 |

## FLL BOT Builders — Coastal Roots Farm, wide view {#fll_farm}

- **Date**: 2026-09-20 · **Status**: done (v2) · **Draw Things project**: `Untitled-91574`
- **Files** (`raw/clips/`): `fll_farm_v2.mov`, `fll_farm_v2_loop.mp4`, `fll_farm_v2_final.mp4`, `fll_farm.mov (v1, rejected)`, `fll_farm_final.mp4 (v1, rejected)`, `fll/team_entrance.webp (reference only)`, `fll/chickens.webp (reference only)`, `fll/crop_rows.webp (reference only)`, `fll/logo.webp`
- **Notes**: Kids must be distant, no faces, no close-ups (Kevin's rule). Real photos used only as reference for farm features; a photoreal attempt and a real-photo I2V attempt were both abandoned. Farm details from FLL-kb: berms/swales, elderberry+pomegranate alleys with rotating chickens, sunflower mural shed, trellis netting. v1 (6 kids + adult, 'walking' prompt) had figures teleporting and merging; v2 regenerated with exactly 5+1 standing still and a wind-only motion prompt.

- **YouTube**: [youtu.be/-Mf2UThasCg](https://youtu.be/-Mf2UThasCg)

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/-Mf2UThasCg" title="FLL BOT Builders — Coastal Roots Farm, wide view" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 576x1024 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |

Prompt: `A breathtaking anime background painting, wide view from a low hill looking down over Coastal Roots Farm in Encinitas at golden hour. Foreground: rows of orchard trees on raised earth berms with shallow swales between them, alleys of elderberry and pomegranate trees where a flock of chickens pecks inside a white portable net fence, a small red barn-style chicken coop on wheels. Middle ground: long rows of squash and vegetables under white trellis netting, a shed painted with a bright sunflower mural, a corrugated-metal welcome-sign shelter, wooden fences. On the dirt path, exactly six people standing still in a tight group: one adult farm guide in a sun hat and five small children in matching black t-shirts, all facing the crops and listening, tiny distant figures, faces not visible. Background: tall coastal eucalyptus and a weeping willow, distant hills. Sky: enormous towering cumulus clouds lit orange and pink by the setting sun, a few tiny birds in silhouette. Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.`

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
| I2V time (min) | 16 |

Prompt: `static camera, the six people stand completely still in place, tree branches and leaves swaying in a steady wind, willow fronds swinging, vegetable rows and netting rippling in the breeze, chickens pecking slowly at the ground, birds drifting across the sky, clouds moving slowly, subtle motion`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | forward, 8-frame tail->head crossfade, x6 = 27.4 s |
| Upscale | lanczos 1080x1920 |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

## Dragon Epic — 1-minute photoreal short, family hero face {#dragon_epic}

- **Date**: 2026-09-21 · **Status**: in progress — scene 1A posted · **Draw Things project**: `dragon-1a (scene 1A I2V), dragon-1b (scene 1B stills, Kevin, 5 refs), dragon-1b-tests (1B v1/v2)`
- **Files** (`raw/clips/`): `dragon/scene1a_v3.mov`, `dragon/scene1a_v3_4k.mp4`, `dragon/scene1a_v3_4k_music.mp4 (with music)`, `music/dragons_breath.mp3`, `dragon/scene1a.mov (v1, ghosting)`, `dragon/scene1a_4k.mp4 (v1)`
- **Notes**: Plan page: wiki/dragon-epic-plan.md. Experiments E1–E7 must pass before rendering the shot list. Needs face photos in raw/face/. Delivery is 4K UHD. Scene 1A: v1 ghosted (push-in + translation), v2 noise (refiner 50%), v3 clean (10%, articulation-only prompt).

- **YouTube**: [youtu.be/Xzu-c5yX8uo](https://youtu.be/Xzu-c5yX8uo)

<div class="yt"><iframe src="https://www.youtube.com/embed/Xzu-c5yX8uo" title="Dragon Epic — 1-minute photoreal short, family hero face" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1280x768 (grid is 64px; 720 not reachable) |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |

Prompt: `per shot — see wiki/dragon-epic-plan.md §6`

**I2V**

| Setting | Value |
|---|---|
| Model | Wan 2.2 High Noise Expert I2V A14B (8-bit S) |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 1280x768 |
| Frames | 81 |
| FPS | 16 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 5.0 |
| Sampler | UniPC Trailing |
| Strength | 100% |
| I2V time (min) | 47 |

Prompt: `per shot — one camera move + one subject action`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/assemble_film.sh (to write) |
| Loop | none — 12 clips xfade-concatenated |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus ncnn, tile 128, → 3840x2160 HEVC 10-bit 40 Mbps (5.6 min/clip) |
| Music | The Dragon's Breath — ONECinematicStudio, Pixabay (cdn.pixabay.com/audio/2026/05/04/audio_505690c98b.mp3), 2:40; scene 1A preview uses peak section from 135 s, 0.3 s fade in / 1 s fade out, vol 0.9. Final film: full track + SFX (TBD) |

## Three-minute film — recurring characters (subject TBD) {#film3min}

- **Date**: 2026-09-21 · **Status**: planning · **Draw Things project**: `None`
- **Files** (`raw/clips/`): 
- **Notes**: Plan: wiki/three-minute-film-plan.md. Consistency stack: wiki/character-consistency.md. Waiting on story/style/characters from Kevin; experiments X1–X7 before rendering.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |

Prompt: `per shot — [camera/light lock] [scene] [character lock verbatim] [action]; see wiki/three-minute-film-plan.md`

**I2V**

| Setting | Value |
|---|---|
| Model | Wan 2.2 High Noise Expert I2V A14B (8-bit S) |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 1024x576 |
| Frames | 81 |
| FPS | 16 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 4.95 |
| Sampler | DDIM Trailing |
| Strength | 100% |
| I2V time (min) | 15 |

Prompt: `per shot — one camera move + one subject action`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Upscale | Real-ESRGAN ncnn 4x -> 3840x2160 (scripts/upscale_4k.sh) |
| Music | TBD |

## Lost City — hyper-real rider on a raptor-dragon entering jungle ruins {#lost_city}

- **Date**: 2026-09-21 · **Status**: in progress — clips at 4K+music: s2, s3, s7, s8, s10, s14; s9 trimmed (4.6 s, drift after); s11 stills rejected (klein duplicates the creature); s12 not started · **Draw Things project**: `lostcity-s1, s2, s3, s7 (named); s8, s9 (cloned — clone crashes on video save); s10 and s11 in fresh Untitled projects; s14 rendered with draw-things-cli (no project file)`
- **Files** (`raw/clips/`): `lostcity/ref_openart_rider_ruins.webp (reference, raw/)`, `lostcity/crop_creature_rider.png, crop_spires.png, crop_foreground.png (Moodboard refs, raw/)`, `lostcity/s1_still_v1.png (shot 1 still, klein)`, `lostcity/s1_ltx_v1.mov (LTX-2.3 test, 1024x576x97 @25fps + audio)`, `lostcity/s2_still_v1.png (shot 2 still, klein, refs: our s1 skyline + spires crop, seed 1)`, `lostcity/s7_still_v2.png (shot 7 still, wingless; s7_still_v1_winged.png = rejected v1)`, `lostcity/s2_wan_v1.mov (shot 2 I2V, Wan 2.2, 1280x768x81)`, `lostcity/s2_wan_v1_4k.mp4 (3840x2160 HEVC 10-bit)`, `lostcity/s2_ltx_v1.mov (shot 2 via LTX-2.3, 1024x576x97 @25fps + audio)`, `lostcity/s2_ltx_v1_4k_audio.mp4 (LTX shot 2 at 3840x2160 + audio)`, `lostcity/s3_still_v1.png (shot 3 still, ref = crop of our s1 creature body)`, `music/mystical_flute.mp3`, `lostcity/s3_ltx_v2.mov (shot 3 LTX v2, hold-position prompt)`, `lostcity/s3_ltx_v2_4k_music.mp4 (4K + ambience + music bed)`, `lostcity/s3_ltx_v1_walkout.mov (v1, rejected: walk-out + phantom rider)`, `lostcity/s7_still_v1.png (side profile, anatomy OK)`, `lostcity/s7_ltx_v1.mov (LTX 1024x576x249 @25fps)`, `lostcity/s7_ltx_v1_4k_music.mp4`, `lostcity/s8_still_v1.png (gallop)`, `lostcity/s8_ltx_v1.mov + s8_ltx_v1_4k_music.mp4 (gallop, 10 s)`, `lostcity/s9_still_v1.png, s9_ltx_v1.mov (jump; drifts after ~4.6 s), s9_ltx_v1_trim.mov (clean 116 f)`, `lostcity/s10_still_v1.png, s10_ltx_v1.mov, s10_ltx_v1_4k_music.mp4 (drinking, 10.3 s, holds design)`, `lostcity/s14_still_v1.png (seed 2; s1/s3 variants kept)`, `lostcity/s14_ltx_v1.mov (ProRes 422 HQ, 249 f @ 25 fps + PCM audio)`, `lostcity/s14_ltx_v1_4k_music.mp4`
- **Notes**: Plan: wiki/lost-city-plan.md. Reference is an OpenArt render (closed model, unknown); we re-generate our own frame. 8 shots × 5 s first. Experiments L0–L6 gate rendering; L1 = first LTX-2.3 test on this Mac.

- **YouTube**: [youtu.be/68sq_jZqu6c](https://youtu.be/68sq_jZqu6c) *(latest cut (replaces 9YlHr5mehaA))*

<div class="yt"><iframe src="https://www.youtube.com/embed/68sq_jZqu6c" title="Lost City — hyper-real rider on a raptor-dragon entering jungle ruins" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1280x768 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |

Prompt: `per scene — see the scenes table (locks + still/video prompt for every shot)`

**I2V**

| Setting | Value |
|---|---|
| Model | LTX-2.3 22B [distilled] 1.1 (production engine — see ltx_10s) — Wan 2.2 High Noise I2V (8-bit S) + Low Noise refiner 10% for locked-camera shots at 768p |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise 100% |
| Size | 1280x768 |
| Frames | 81 |
| FPS | 16 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 5.0 |
| Sampler | DDIM Trailing |
| Strength | 100% |
| I2V time (min) | 49 |

Prompt: `per scene — see the scenes table`

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none — xfade concat |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus → 3840x2160 HEVC 10-bit |
| Music | Mystical orchestral theme with ancient flute — DesiFreeMusic, Pixabay (cdn.pixabay.com/audio/2025/07/12/audio_fb278af2ae.mp3), 4:00, steady −15 dB from 0 s, dips at 80 s and 200 s |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *style head* — Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain.
- *creature* — a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs
- *rider* — a lone rider, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots
- *style tail* — Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

**Rules**: Never write 'dragon' (grows wings) or 'two-legged' (breaks legs). Quadruped wording only. Side/three-quarter framing — rear-view low angles fail. Moodboard refs must be crops, never a full wide frame. Destruction shots: name the subject and its stillness first, then confine the falling verbs to the distance in one clause — LTX bleeds collapse motion onto anything small or mentioned after it (s14 v1: the creature's head fell off like a spire). Keep the subject at least a third of the frame wide in any shot where other things break apart.


#### s1 — Side view, rider + creature walk toward the city (reference frame)

- **Engine**: LTX-2.3 1024x576 x97
- **Files** (`raw/clips/lostcity/`): s1_still_v1.png, s1_ltx_v1.mov, s1_ltx_v1_4k_audio.mp4

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A lost city of tall eroded sandstone spires and ziggurat towers swallowed by jungle rises in the distance through morning haze, a stone arch bridge and a white waterfall between them, soft volumetric god rays breaking through thin cloud. Mossy stone blocks and palms in the middle distance, ferns and tall grass in the foreground. In the centre, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking left to right on a dirt path on two heavy hind legs and two smaller forelegs. On its back a lone rider seen from behind, dark cropped hair, grey-green hooded cloak thrown back, brown leather jerkin, tan trousers, tall boots, hands on the reins. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature walks slowly from left to right with a heavy four-legged gait, its head bobbing and tail swaying, while the camera tracks alongside at the same pace so the rider stays centred in frame. The rider sways gently in the saddle, the cloak lifting in a light breeze. Behind them the waterfall pours steadily and thin mist drifts through the shafts of light; two birds glide across the distant spires. Heavy footsteps on damp earth, the far roar of the waterfall, faint jungle birdsong, no music.


#### s2 — Extreme wide from a ledge, tiny rider on the path

- **Engine**: both — Wan 2.2 1280x768 x81 and LTX 1024x576 x97
- **Files** (`raw/clips/lostcity/`): s2_still_v1.png, s2_wan_v1_4k.mp4, s2_ltx_v1_4k_audio.mp4

*Still prompt*

> Cinematic film still, anamorphic 35mm, extreme wide establishing shot from a high mossy ledge, muted colours, low contrast, subtle film grain. Below and beyond, a lost city of tall eroded sandstone spires and ziggurat towers swallowed by jungle stretches to the horizon through layered morning haze, a stone arch bridge and a white waterfall between the towers, soft volumetric god rays breaking through thin cloud. A narrow dirt path winds down from the ledge toward the city; on it, very small in the frame, a lone hooded rider on a large wingless quadrupedal raptor-like dragon walks toward the city, seen from behind. Ferns and a broken stone column in the foreground on the ledge, palms and mossy blocks in the middle distance, birds tiny in the sky. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt (Wan)*

> very slow push in, the camera drifting gently forward toward the city, mist drifting slowly through the god rays, the waterfall flowing steadily, thin clouds moving very slowly, ferns and palm fronds swaying in a light breeze, tiny birds gliding across the distant sky, the small rider and creature walking slowly along the path away from the camera, subtle motion, smooth, cinematic, photorealistic

*Video prompt (LTX)*

> The camera pushes in very slowly and steadily toward the distant city, the mossy columns in the foreground drifting past the edges of the frame. The small rider and creature walk slowly down the dirt path away from the camera toward the city. Mist drifts through the shafts of light, the waterfall pours steadily under the stone arch, ferns and palm fronds sway in a light breeze, and tiny birds glide across the sky above the spires. Wind through jungle leaves, the distant hush of the waterfall, faint birdsong, no music. Photorealistic, cinematic, smooth motion.


#### s3 — Low angle, creature's feet on wet flagstones

- **Engine**: LTX 1024x576 x97
- **Files** (`raw/clips/lostcity/`): s3_still_v1.png, s3_ltx_v2_4k_music.mp4
- **Note**: v1 asked for one step forward — it walked out of frame and hallucinated a second rider. Close-ups need hold-position wording.

*Still prompt*

> Cinematic film still, anamorphic 35mm, very low camera angle at ground level on a wet jungle path, muted colours, low contrast, subtle film grain. Filling the frame, the heavy clawed feet and thick scaled legs of a large saddled raptor-like reptile mount, a wingless two-legged theropod with slate-grey ridged hide, planted on wet mossy flagstones, water pooled between the stones, ferns and tall grass in the near foreground, the rider's boot in a stirrup and a hanging brown satchel visible above. Behind, out of focus, mossy carved blocks and the haze of a lost city with soft god rays. Shallow depth of field, layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> Fixed camera, low on the wet stone path. The creature stands still in place and does not walk; it only shifts its weight from one foot to the other, the claws flexing on the wet flagstones, small ripples spreading in the pooled water, the thick scaled legs tensing, the tail swaying slowly. The rider's boot rocks gently in the stirrup and the satchel sways. Ferns and grass in the foreground move in a light breeze, mist drifts through the god rays behind. The path behind stays empty. Water dripping, leather creaking, wind in the leaves, faint birdsong, no music. Photorealistic, cinematic, subtle smooth motion.


#### s7 — Canyon, side profile walking through the spires

- **Engine**: LTX 1024x576 x249 (10 s)
- **Files** (`raw/clips/lostcity/`): s7_still_v1.png, s7_ltx_v1_4k_music.mp4
- **Note**: Six rear-view attempts failed on anatomy before switching to this side framing.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. Inside a narrow canyon between colossal eroded sandstone spires and ziggurat towers of a lost city, soft volumetric god rays pouring down through morning haze, dust drifting in the light, vines and moss hanging from the carved stone walls. In the centre, walking left to right along a dirt path, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs. On its back a lone rider seen from the side, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots, hands on the reins, looking up at the towers. Ferns and broken carved blocks in the foreground, tiny birds high in the sky. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The camera holds a steady low side view as the creature walks slowly from left to right through the canyon with a heavy four-legged gait, its head bobbing gently and tail swaying, staying in the centre of the frame while the carved stone walls drift past behind it. The rider sways in the saddle, cloak lifting in a light breeze, looking up at the towers. Dust and pollen drift through the shafts of light, mist rolls slowly along the ground, ferns sway, tiny birds cross the sky. Heavy footsteps on packed earth, leather creaking, wind in the vines, faint jungle birdsong, no music.


#### s8 — Running — full gallop across a clearing

- **Engine**: LTX 1024x576 x249
- **Files** (`raw/clips/lostcity/`): s8_still_v1.png, s8_ltx_v1_4k_music.mp4

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. An open jungle clearing beside the lost city, eroded sandstone spires and ziggurat towers soft in the haze behind, god rays through thin cloud. In the centre, galloping left to right at full stride in side profile, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, all four legs in a running gallop with the heavy hind legs driving and the smaller forelegs reaching forward, dust kicked up behind it, on two heavy hind legs and two smaller forelegs. On its back a lone rider leaning low over the neck holding the reins, grey-green hooded cloak streaming straight back, brown leather jerkin, tan trousers, tall boots. Ferns and tall grass in the foreground, tiny birds high in the sky. Motion, energy, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature gallops at full speed from left to right across the clearing with a powerful four-legged running gait, hind legs driving and forelegs reaching, dust bursting up behind each stride, while the camera tracks alongside at the same speed keeping the creature and rider centred in the frame as the ruins and jungle rush past behind. The rider stays low over the neck, cloak whipping straight back. Grass and ferns blur past in the foreground, birds scatter from the trees. Pounding heavy footfalls, rushing wind, leather creaking, distant birds, no music.


#### s9 — Jumping — leap over a fallen pillar

- **Engine**: LTX 1024x576 x249
- **Files** (`raw/clips/lostcity/`): s9_still_v1.png, s9_ltx_v1.mov, s9_ltx_v1_trim.mov
- **Note**: Creature morphs toward a horse after ~frame 115 (4.6 s) — trimmed there.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A jungle path beside the lost city, spires and ziggurat towers in the haze behind, god rays through morning mist. In the centre, caught mid-leap in side profile over a fallen mossy stone pillar lying across the path, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs, its heavy hind legs extended behind from the push-off and its smaller forelegs tucked up, body arched in the air above the pillar. On its back a lone rider crouched low in the saddle gripping the reins, grey-green hooded cloak flaring, brown leather jerkin, tan trousers, tall boots. Ferns and broken carved blocks in the foreground, tiny birds high in the sky. Motion, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature completes its leap over the fallen stone pillar, forelegs reaching down and hind legs swinging under it, lands on the far side with a puff of dust and runs on a few strides before slowing to a walk, while the camera tracks alongside at the same pace keeping the creature and rider centred in frame. The rider absorbs the landing, rising and settling in the saddle, cloak snapping. Dust bursts at the landing, ferns shake, birds scatter. A heavy thudding landing, pounding footfalls, leather creaking, distant birdsong, no music.


#### s10 — Drinking at a jungle pool

- **Engine**: LTX 1024x576 x257 (10.3 s)
- **Files** (`raw/clips/lostcity/`): s10_still_v1.png, s10_ltx_v1_4k_music.mp4
- **Note**: Best of the batch — design holds the full clip.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A still jungle pool below a small waterfall at the edge of the lost city, mossy carved blocks and ferns around the water, eroded sandstone spires in the haze behind, god rays through the canopy. At the water's edge in side profile, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs with its neck lowered and its muzzle touching the water, ripples spreading across the surface, its reflection in the pool. On its back a lone rider, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots, sitting relaxed in the saddle looking around. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> Fixed camera on the pool. The creature stands in place at the water's edge and drinks, lowering its muzzle to the surface and lifting its head slowly with water dripping from its jaw, then lowering it again, its throat working as it swallows, tail swaying gently. The rider sits relaxed in the saddle and turns his head to look around at the ruins. Ripples spread across the pool and settle, the waterfall pours steadily behind, mist drifts, ferns move in a light breeze. Water lapping and dripping, the hush of the waterfall, leather creaking, faint birdsong, no music.


#### s11 — Dismount (blocked)

- **Engine**: not rendered

*Still prompt*

> Three variants tried, all rendered two creatures; see plan §7b. Latest: 'Solo portrait of one animal: a single large quadrupedal raptor-like reptile mount standing still in full side profile ... A man stands on the ground in front of its shoulder with his back to the camera, reaching up to the saddle strap ... No other animals, no second creature, empty path behind.'

*Video prompt*

> planned: The rider swings the leg over and steps down to the ground beside the creature, landing on both feet and patting its flank; the creature stands still, head turning to look at the rider.


#### s12 — Mount up (not started)

- **Engine**: not rendered

*Still prompt*

> planned: rider standing beside the creature with one boot in the stirrup and both hands on the saddle, about to swing up.

*Video prompt*

> planned: The rider pushes up from the stirrup, swings the leg over and settles into the saddle, gathering the reins; the creature shifts its weight and raises its head.


#### s13 — Escape — running as the spires collapse

- **Engine**: LTX 1024x576 x249 — plan for drift: keep the creature large in frame and cut by ~5 s if the design softens
- **Note**: Fast locomotion, so expect drift after ~4-5 s (see s8/s9). Mitigation: subject fills the lower half, camera locked alongside, and trim on the first soft frame.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A wide dirt avenue between the colossal eroded sandstone spires and ziggurat towers of the lost city, the air thick with dust and falling debris, shafts of hard sunlight cutting through the dust clouds, cracks running up the carved stone walls. In the centre foreground, galloping left to right in side profile and filling the lower half of the frame, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, all four legs in a running gallop with the heavy hind legs driving and the smaller forelegs reaching forward, dust exploding from its feet. On its back a lone rider leaning low over the neck gripping the reins, grey-green hooded cloak streaming straight back, brown leather jerkin, tan trousers, tall boots, glancing back over his shoulder. Behind and above them a spire is breaking apart mid-collapse, huge carved blocks tumbling through the air and a wall of dust rolling down the avenue. Ferns and rubble in the foreground. Motion, danger, energy, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature gallops at full speed from left to right down the avenue with a powerful four-legged running gait, dust bursting from each stride, while the camera tracks alongside at the same speed keeping the creature and rider centred in frame as the collapsing city rushes past behind. The rider stays low over the neck, cloak whipping back, and glances over his shoulder. Behind them a spire shears and falls, carved blocks tumbling and smashing into the avenue, a wall of dust rolling forward and swallowing the towers, smaller stones bouncing across the ground. Deep grinding stone, crashing masonry, pounding footfalls, rushing wind, no music.


#### s14 — Escape — final shot: the whole skyline falls, creature watching from the ridge

- **Engine**: LTX 1024x576 x249 (9.96 s) — rendered headless with draw-things-cli, 9 min 41 s
- **Note**: v1 failed: LTX applied the collapse to the creature — its head sheared off and fell like a spire. Two causes, both fixed here. (1) Scale: the creature was a sixth of the frame, so its head was ~30 px in the 32x32 LTX latent and got re-synthesised as debris; it now fills the left third close to camera. (2) Prompt order and verbs: the falling verbs came before the subject and bled onto it. Subject first with positive rigidity words (solid, still, intact, head held level and attached, only the ribs move), then one sentence that pins the destruction to the horizon ('all of the destruction is far away on the horizon and nowhere near them'). Pace so the last tower falls by ~8 s and the final second is an empty dust skyline — the film's last frame. v2 rendered 2026-09-22 and works: creature solid the whole clip, spires fall through the shot, skyline empty by the last second. Both still and clip came from draw-things-cli with no UI (seed 2 of 3 stills, text-only — no Moodboard refs, which the released CLI cannot do yet); see [[headless-cli-pipeline]].

*Still prompt*

> Cinematic film still, anamorphic 35mm, wide landscape view from a high grassy ridge, muted colours, low contrast, subtle film grain. Standing on the ridge in the left foreground, close to the camera, in clear side profile and filling the left third of the frame from the ground to two thirds of the height, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck held up and steady with the head sharply in focus, a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, standing squarely on two heavy hind legs and two smaller forelegs. On its back a lone rider sitting upright and turned to look back, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots. Grass and ferns around its feet. Beyond the ridge the land drops away into a vast hazy valley of dark jungle canopy, and far away on the horizon the whole lost city of colossal eroded sandstone spires and ziggurat towers is coming down, towers leaning and breaking apart, immense dust plumes rising and merging into a low grey wall spreading across the valley floor, shafts of hard sunlight through the dust. Huge sense of scale, sharp intact animal in the foreground against a distant collapsing skyline, deep depth of field, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> Fixed camera, wide landscape. In the foreground the creature stands solid and completely still on the ridge, its whole body intact and upright, the long neck steady and the head held level and attached, only its ribs moving with deep slow breaths and its tail swaying gently; the rider sits upright in the saddle and watches, cloak moving in the wind; grass and ferns bend around their feet. All of the destruction is far away on the horizon and nowhere near them: out there in the distance the city finishes falling, spire after spire leaning, buckling and dropping in slow heavy arcs, the tallest towers going last, each collapse throwing up a fresh dust plume until the plumes merge into one grey wall rolling outward, and by the end nothing is left standing on the skyline, only a flat bank of dust over rubble. Distant thunderous collapse, grinding stone, rising wind, heavy animal breathing, no music.

## Related pages
- [[runbook-living-painting]]
- [[living-painting-loop]]
- [[draw-things-setup]]
