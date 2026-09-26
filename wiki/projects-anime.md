# Anime projects

**Summary**: Shinkai/Ghibli-styled living paintings: a still from FLUX or Wan T2V, ambient motion from Wan 2.2 I2V, looped 9:16 with music. Coastal wildflowers, Torrey Pines, Golden Gate, Mt. Rainier, a cyberpunk street, the FLL farm. Full record per project: models, settings, prompts, seeds, music and output files. Generated from each version's `spec.json`.

**Sources**: projects/*/*/spec.json; per-project notes from the session logs.

**Last updated**: 2026-09-25

---

Index of every project: [[projects]]. Other themes: [[projects-realistic]] · [[projects-3d]].

## Summary

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Coastal wildflowers](#coast) | 2026-09-20 | done | FLUX.2 [klein] 9B 1024x1792 | Wan 2.2 High Noise 15.5 min | Calm Ambient Dreamscape | `coast_v2_final.mp4` | [▶ watch](https://youtu.be/W8fy4bhGOEU) |
| 2 | [Torrey Pines, San Diego](#torrey) | 2026-09-20 | done | FLUX.2 [klein] 9B 1024x1792 | Wan 2.2 High Noise 15 min | Calm Ambient Dreamscape | `torrey_final.mp4` | [▶ watch](https://youtu.be/nRU-Upd2E3o) |
| 3 | [Golden Gate, San Francisco](#goldengate) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Calm Ambient Dreamscape | `goldengate_final.mp4` | [▶ watch](https://youtu.be/h8ic1_9Q9mI) |
| 4 | [Mt. Rainier from Paradise](#rainier) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 15.5 min | Calm Ambient Dreamscape | `rainier_final.mp4` | [▶ watch](https://youtu.be/JJB154LbBi0) |
| 5 | [Cyberpunk city, rain, neon](#cyberpunk) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Neon Synthwave Drive | `cyberpunk_final.mp4` | [▶ watch](https://youtu.be/GrNTNQCqKnk) |

## Coastal wildflowers {#coast}

- **Date**: 2026-09-20 · **Status**: done · **Version**: `v2-klein-still` · **Draw Things project**: `Untitled-35903`
- **This version**: Still generated with FLUX.2 klein at 1024x1792 then cropped to 576x1024; the detail this added is what closed the gap with the reference.

**Versions**

| Version | What it is | Status | YouTube |
|---|---|---|---|
| `v1-wan-t2v-still` | Still generated with Wan 2.2 T2V at 576x1280, then Wan I2V; superseded because the still lacked detail. | superseded by v2-klein-still — kept as the record of the Wan-still attempt | — |
| `v2-klein-still` | Still generated with FLUX.2 klein at 1024x1792 then cropped to 576x1024; the detail this added is what closed the gap with the reference. | done | [▶ watch](https://youtu.be/W8fy4bhGOEU) |

- **Files** (`projects/coast/v2-klein-still/`): `coast_flux_1024x1792.png`, `coast_flux_576x1024.png`, `coast_v2.mov`, `coast_v2_loop.mp4`, `coast_v2_final.mp4`
- **Notes**: First run with wrong refiner (6-bit, not downloaded) produced washed-out noise; re-run with 8-bit S. Merged with the former coast_v2 project on 2026-09-25: the two were one film made twice, so they are now v1 and v2 of a single project.

- **YouTube**: [youtu.be/W8fy4bhGOEU](https://youtu.be/W8fy4bhGOEU)

<div class="yt yt-v"><iframe src="https://www.youtube.com/embed/W8fy4bhGOEU" title="Coastal wildflowers" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

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

- **Date**: 2026-09-20 · **Status**: done · **Version**: `v1-drawthings-ui` · **Draw Things project**: `Untitled-91451`
- **This version**: Rendered by driving the Draw Things app window (accessibility automation).
- **Files** (`projects/torrey/v1-drawthings-ui/`): `torrey_flux_1024x1792.png`, `torrey_flux_576x1024.png`, `torrey.mov`, `torrey_loop.mp4`, `torrey_final.mp4`
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

- **Date**: 2026-09-20 · **Status**: done · **Version**: `v1-drawthings-ui` · **Draw Things project**: `Untitled-82025`
- **This version**: Rendered by driving the Draw Things app window (accessibility automation).
- **Files** (`projects/goldengate/v1-drawthings-ui/`): `goldengate.mov`, `goldengate_loop.mp4`, `goldengate_final.mp4`
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

- **Date**: 2026-09-20 · **Status**: done · **Version**: `v1-drawthings-ui` · **Draw Things project**: `Untitled-70762`
- **This version**: Rendered by driving the Draw Things app window (accessibility automation).
- **Files** (`projects/rainier/v1-drawthings-ui/`): `rainier.mov`, `rainier_loop.mp4`, `rainier_final.mp4`
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

- **Date**: 2026-09-20 · **Status**: done · **Version**: `v1-drawthings-ui` · **Draw Things project**: `Untitled-76300`
- **This version**: Rendered by driving the Draw Things app window (accessibility automation).
- **Files** (`projects/cyberpunk/v1-drawthings-ui/`): `cyberpunk.mov`, `cyberpunk_loop.mp4`, `cyberpunk_final.mp4`
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

## Related pages
- [[projects]]
- [[runbook-living-painting]]
- [[draw-things-setup]]
