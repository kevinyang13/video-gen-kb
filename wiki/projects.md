# Projects Registry

**Summary**: Index of every video project so far, grouped by theme. The full record for each one — models, settings, prompts, seeds, music, files — lives on its theme page. Generated from `projects.json`; edit that file, not these pages.

**Sources**: projects.json; per-project notes from the session logs.

**Last updated**: 2026-09-23

---

## [[projects-anime|Anime projects]] (7)

Shinkai/Ghibli-styled living paintings: a still from FLUX or Wan T2V, ambient motion from Wan 2.2 I2V, looped 9:16 with music. Coastal wildflowers, Torrey Pines, Golden Gate, Mt. Rainier, a cyberpunk street, the FLL farm.

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Coastal wildflowers (v1)](projects-anime.html#coast) | 2026-09-20 | superseded by coast_v2 | Wan 2.2 High Noise Expert T2V A14B 576x1280 | Wan 2.2 High Noise 24 min | — | `—` | — |
| 2 | [Coastal wildflowers (v2)](projects-anime.html#coast_v2) | 2026-09-20 | done | FLUX.2 [klein] 9B 1024x1792 | Wan 2.2 High Noise 15.5 min | Calm Ambient Dreamscape | `coast_v2_final.mp4` | [▶ watch](https://youtu.be/W8fy4bhGOEU) |
| 3 | [Torrey Pines, San Diego](projects-anime.html#torrey) | 2026-09-20 | done | FLUX.2 [klein] 9B 1024x1792 | Wan 2.2 High Noise 15 min | Calm Ambient Dreamscape | `torrey_final.mp4` | [▶ watch](https://youtu.be/nRU-Upd2E3o) |
| 4 | [Golden Gate, San Francisco](projects-anime.html#goldengate) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Calm Ambient Dreamscape | `goldengate_final.mp4` | [▶ watch](https://youtu.be/h8ic1_9Q9mI) |
| 5 | [Mt. Rainier from Paradise](projects-anime.html#rainier) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 15.5 min | Calm Ambient Dreamscape | `rainier_final.mp4` | [▶ watch](https://youtu.be/JJB154LbBi0) |
| 6 | [Cyberpunk city, rain, neon](projects-anime.html#cyberpunk) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Neon Synthwave Drive | `cyberpunk_final.mp4` | [▶ watch](https://youtu.be/GrNTNQCqKnk) |
| 7 | [FLL BOT Builders — Coastal Roots Farm, wide view](projects-anime.html#fll_farm) | 2026-09-20 | done (v2) | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Calm Ambient Dreamscape | `fll_farm_v2_final.mp4` | [▶ watch](https://youtu.be/-Mf2UThasCg) |

## [[projects-realistic|Photoreal projects]] (3)

Cinematic photoreal shorts: FLUX.2 klein stills with Moodboard references, motion from LTX-2.3 or Wan 2.2, Real-ESRGAN to 4K, cut with crossfades. Dragon Epic, Lost City, the three-minute film.

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Dragon Epic — 1-minute photoreal short, family hero face](projects-realistic.html#dragon_epic) | 2026-09-21 | in progress — scene 1A posted | FLUX.2 [klein] 9B 1280x768 | Wan 2.2 High Noise 47 min | The Dragon's Breath | `—` | [▶ watch](https://youtu.be/Xzu-c5yX8uo) |
| 2 | [Three-minute film — recurring characters (subject TBD)](projects-realistic.html#film3min) | 2026-09-21 | planning | FLUX.2 [klein] 9B 1024x576 | Wan 2.2 High Noise 15 min | TBD | `—` | — |
| 3 | [Lost City — hyper-real rider on a raptor-dragon entering jungle ruins](projects-realistic.html#lost_city) | 2026-09-21 | in progress — clips at 4K+music: s2, s3, s7, s8, s10, s14; s9 trimmed (4.6 s, drift after); s11 stills rejected (klein duplicates the creature); s12 not started; s15 rift coda done (3 clips assembled to 30 s 4K with music) | FLUX.2 [klein] 9B 1280x768 | LTX-2.3 22B [distilled] 1.1 (production engine — see ltx_10s) — Wan 2.2 High Noise I2V (8-bit S) + Low Noise refiner 10% for locked-camera shots at 768p 49 min | Mystical orchestral theme with ancient flute | `—` | [▶ watch](https://youtu.be/68sq_jZqu6c) |

## [[projects-3d|3D-animated projects]] (1)

Pixar-style 3D-animated shorts. Kyle's Antarctic Rescue.

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Kyle's Antarctic Rescue — 1-minute 3D-animated vertical short from a 5-panel comic](projects-3d.html#kyle_rescue) | 2026-09-22 | delivered 2026-09-23 01:38 — 60.0 s, 1080x1920 + 2160x3840, rendered unattended overnight (see plan §0) | FLUX.2 [klein] 9B 576x1024 | LTX-2.3 22B [distilled] 1.1 via draw-things-cli ? min | Calm Ambient Dreamscape | `—` | — |


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

## Related pages
- [[projects-anime]] · [[projects-realistic]] · [[projects-3d]]
- [[runbook-living-painting]]
- [[living-painting-loop]]
- [[draw-things-setup]]
