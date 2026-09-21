# Projects Registry

**Summary**: Every video project so far — one record each with the exact models, settings, prompts, seeds, music and output files. Generated from `projects.json`; edit that file, not this page.

**Sources**: projects.json; per-project notes from the session logs.

**Last updated**: 2026-09-21

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

## Related pages
- [[runbook-living-painting]]
- [[living-painting-loop]]
- [[draw-things-setup]]
