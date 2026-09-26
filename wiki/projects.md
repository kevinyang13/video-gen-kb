# Projects Registry

**Summary**: Index of every video project so far, grouped by theme. The full record for each one — models, settings, prompts, seeds, music, files — lives on its theme page. Generated from `projects.json`; edit that file, not these pages.

**Sources**: projects.json; per-project notes from the session logs.

**Last updated**: 2026-09-25

---

**Project pages**: [[projects-anime|Anime projects]] (6) · [[projects-realistic|Photoreal projects]] (2) · [[projects-3d|3D-animated projects]] (4)

Each theme page holds the full records — settings, prompts, seeds, files. The tables below link straight to a project's record on its page.

## [[projects-anime|Anime projects]] (6)

Shinkai/Ghibli-styled living paintings: a still from FLUX or Wan T2V, ambient motion from Wan 2.2 I2V, looped 9:16 with music. Coastal wildflowers, Torrey Pines, Golden Gate, Mt. Rainier, a cyberpunk street, the FLL farm.

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Coastal wildflowers](projects-anime.html#coast) | 2026-09-20 | done | FLUX.2 [klein] 9B 1024x1792 | Wan 2.2 High Noise 15.5 min | Calm Ambient Dreamscape | `coast_v2_final.mp4` | [▶ watch](https://youtu.be/W8fy4bhGOEU) |
| 2 | [Torrey Pines, San Diego](projects-anime.html#torrey) | 2026-09-20 | done | FLUX.2 [klein] 9B 1024x1792 | Wan 2.2 High Noise 15 min | Calm Ambient Dreamscape | `torrey_final.mp4` | [▶ watch](https://youtu.be/nRU-Upd2E3o) |
| 3 | [Golden Gate, San Francisco](projects-anime.html#goldengate) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Calm Ambient Dreamscape | `goldengate_final.mp4` | [▶ watch](https://youtu.be/h8ic1_9Q9mI) |
| 4 | [Mt. Rainier from Paradise](projects-anime.html#rainier) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 15.5 min | Calm Ambient Dreamscape | `rainier_final.mp4` | [▶ watch](https://youtu.be/JJB154LbBi0) |
| 5 | [Cyberpunk city, rain, neon](projects-anime.html#cyberpunk) | 2026-09-20 | done | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Neon Synthwave Drive | `cyberpunk_final.mp4` | [▶ watch](https://youtu.be/GrNTNQCqKnk) |
| 6 | [FLL BOT Builders — Coastal Roots Farm, wide view](projects-anime.html#fll_farm) | 2026-09-20 | done (v2) | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise 16 min | Calm Ambient Dreamscape | `fll_farm_v2_final.mp4` | [▶ watch](https://youtu.be/-Mf2UThasCg) |

→ full records for all 6: [[projects-anime|Anime projects]]

## [[projects-realistic|Photoreal projects]] (2)

Cinematic photoreal shorts: FLUX.2 klein stills with Moodboard references, motion from LTX-2.3 or Wan 2.2, Real-ESRGAN to 4K, cut with crossfades. Dragon Epic, Lost City, the three-minute film.

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Dragon Epic — 1-minute photoreal short, family hero face](projects-realistic.html#dragon_epic) | 2026-09-21 | in progress — scene 1A posted | FLUX.2 [klein] 9B 1280x768 | Wan 2.2 High Noise 47 min | The Dragon's Breath | `—` | [▶ watch](https://youtu.be/Xzu-c5yX8uo) |
| 2 | [Lost City — hyper-real rider on a raptor-dragon entering jungle ruins](projects-realistic.html#lost_city) | 2026-09-21 | in progress — clips at 4K+music: s2, s3, s7, s8, s10, s14; s9 trimmed (4.6 s, drift after); s11 stills rejected (klein duplicates the creature); s12 not started; s15 rift coda done (3 clips assembled to 30 s 4K with music) | FLUX.2 [klein] 9B 1280x768 | LTX-2.3 22B [distilled] 1.1 (production engine — see ltx_10s) — Wan 2.2 High Noise I2V (8-bit S) + Low Noise refiner 10% for locked-camera shots at 768p 49 min | Mystical orchestral theme with ancient flute | `—` | [▶ watch](https://youtu.be/68sq_jZqu6c) |

→ full records for all 2: [[projects-realistic|Photoreal projects]]

## [[projects-3d|3D-animated projects]] (4)

Pixar-style 3D-animated shorts. Kyle's Antarctic Rescue, Lindsey: A Small Dream.

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Kyle's Antarctic Rescue — 1-minute 3D-animated vertical short from a 5-panel comic](projects-3d.html#kyle_rescue) | 2026-09-22 | delivered 2026-09-23 01:38 — 60.0 s, 1080x1920 + 2160x3840, rendered unattended overnight (see plan §0) | FLUX.2 [klein] 9B 576x1024 | LTX-2.3 22B [distilled] 1.1 via draw-things-cli ? min | Calm Ambient Dreamscape | `—` | [▶ watch](https://youtu.be/KscAwvCi6iQ) |
| 2 | [Lindsey: A Small Dream — 1-minute 3D-animated vertical short from Lindsey's 5-panel art comic](projects-3d.html#lindsey_art) | 2026-09-23 | delivered 2026-09-23 17:26 — 59.96 s, 1080x1920 + 2160x3840 + 720x1280 (see plan §0) | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | [▶ watch](https://youtu.be/lbU-_73MliI) |
| 3 | [BOT Builders (photo cut) — 12-shot 3D-animated short from the team's own photos](projects-3d.html#fll_champions) | 2026-09-23 | delivered 2026-09-25 03:00 — 59.08 s, 3840x2160 + 1920x1080, 11 shots (competition-floor wide dropped); see wiki/fll-champions-plan.md | FLUX.2 [klein] 9B 1024x576 | LTX-2.3 22B [distilled] 1.1 10 min | Light Adventure | `—` | — |
| 4 | [Bot Builders — 90-second 16:9 3D-animated FLL team film from a 3-page comic](projects-3d.html#fll_bot_builders) | 2026-09-23 | delivered 2026-09-24 04:11 — 63.5 s (planned 90; five-kid rule), 1920x1080 + 3840x2160 + 1280x720 (see plan §0) | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | — |

→ full records for all 4: [[projects-3d|3D-animated projects]]


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
