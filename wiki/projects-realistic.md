# Photoreal projects

**Summary**: Cinematic photoreal shorts: FLUX.2 klein stills with Moodboard references, motion from LTX-2.3 or Wan 2.2, Real-ESRGAN to 4K, cut with crossfades. Dragon Epic, Lost City, the three-minute film. Full record per project: models, settings, prompts, seeds, music and output files. Generated from each version's `spec.json`.

**Sources**: projects/*/*/spec.json; per-project notes from the session logs.

**Last updated**: 2026-10-09

---

Index of every project: [[projects]]. Other themes: [[projects-anime]] · [[projects-3d]].

## Summary

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Dragon Epic — 1-minute photoreal short, family hero face](#dragon_epic) | 2026-09-21 | in progress — scene 1A posted | FLUX.2 [klein] 9B 1280x768 | Wan 2.2 High Noise 47 min | The Dragon's Breath | `—` | [▶ watch](https://youtu.be/Xzu-c5yX8uo) |
| 2 | [Lost City — hyper-real rider on a raptor-dragon entering jungle ruins](#lost_city) | 2026-09-21 | in progress — 4K with music: s3, s4, s5, s8, s9; s1 and s2 at 4K without music; s6 trimmed to 4.6 s and never upscaled; **s7 (escape run) not rendered**; no film assembled yet | FLUX.2 [klein] 9B 1280x768 | LTX-2.3 22B [distilled] 1.1 (production engine — see ltx_10s) — Wan 2.2 High Noise I2V (8-bit S) + Low Noise refiner 10% for locked-camera shots at 768p 49 min | Mystical orchestral theme with ancient flute | `—` | [▶ watch](https://youtu.be/68sq_jZqu6c) |
| 3 | [Night Elf Hunter — a boy and his bear crossing the grassland](#nightelf_hunter) | 2026-09-26 | research — B0 partial pass 2026-09-26: 30 images, identity 30/30, angles skewed (back 1/3, over-shoulder 0/2); v1 remains the delivered film | FLUX.2 [klein] 9B 512x768 | Wan 2.2 High Noise ? min | none | `—` | — |
| 4 | [Ivy — character LoRA](#ivy_lora) | 2026-09-26 | delivered 2026-09-26 — ivy_lora_2000_lora_f32.ckpt at weight 0.5; identity holds in unseen scenes, profile and back-of-head degrade (dataset has neither) | FLUX.2 [klein] 9B aspect-bucketed, | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | — |
| 5 | [Lindsey — character LoRA](#lindsey_lora) | 2026-09-27 | trained 2026-09-27 — 2000 steps in 2 h 26 m, five checkpoints; evaluation pending | FLUX.2 [klein] 9B aspect-bucketed, | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | — |
| 6 | [Lindsey — the palace pavilion](#lindsey_palace) | 2026-09-28 | delivered 2026-09-28 22:07 — 61.08 s, 3840x2160 (293 MB) + 1920x1080 (91 MB), 8 shots, none dropped; mean -21.1 dB, peak -5.4 dB | FLUX.2 [klein] 9B 1024x576 | LTX-2.3 22B [distilled] 1.1 10 min | Emotional Children Piano | `—` | — |
| 7 | [Kyle — five minutes to showtime](#kyle_debut) | 2026-09-28 | delivered 2026-09-29 01:20 — 60.76 s, 3840x2160 (279 MB) + 1920x1080 (79 MB), 8 shots, none dropped; mean -21.7 dB, peak -5.5 dB | FLUX.2 [klein] 9B 1024x576 | LTX-2.3 22B [distilled] 1.1 11 min | Emotional Children Piano | `—` | — |
| 8 | [Kyle: First Flight (v3, no droid)](#kyle_firstflight) | 2026-10-07 | stopped | flux_2_klein_9b_i8x.ckpt 1024x576 | ltx_2.3_22b_distilled_1.1_q8p.ckpt ? min | Calm Ambient Dreamscape | `—` | — |
| 9 | [Kyle — The Boonta Flats](#kyle_saltflats) | 2026-10-04 | clips QC'd 2026-10-04 — 59.85 s planned | none — supplied 1024x576 | ltx_2.3_22b_distilled_1.1_q8p.ckpt 10 min | best_adventure_ever.mp3 | `—` | — |
| 10 | [Lindsey — above the cloud sea](#lindsey_summit) | 2026-09-29 | delivered 2026-09-29 10:42 — 59.88 s, 3840x2160 (280 MB) + 1920x1080 (87 MB), 8 shots, none dropped; mean -18.7 dB, peak -5.3 dB. Planned length 59.75 s, delivered 59.88 s. | FLUX.2 [klein] 9B 1024x576 | LTX-2.3 22B [distilled] 1.1 11 min | Adventure Journey | `—` | — |
| 11 | [Kyle — the signal fire](#kyle_lighthouse) | 2026-09-29 | stopped 2026-09-29 — abandoned at Kevin's call after s6 could not be made to work. Seven of eight shots are rendered, graded and upscaled to 4K; s6 went through five designs (interior stairwell from below, side-on interior spiral, exterior stair on the tower, and two versions of the entrance door) and none was accepted. No final cut was produced from the current shot set. | FLUX.2 [klein] 9B 1024x576 | LTX-2.3 22B [distilled] 1.1 11 min | Best Adventure Ever | `—` | — |
| 12 | [Lindsey: Clifftop Orbit](#lindsey_orbit) | 2026-10-08 | rendering | flux_2_klein_9b_i8x.ckpt 1024x576 | wan_v2.2_a14b_hne_i2v_i8x.ckpt ? min | Calm Ambient Dreamscape | `—` | — |
| 13 | [Kyle — character LoRA v2](#kyle_lora) | 2026-09-29 | dataset built 2026-09-29 — 55 pairs; training | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | — |
| 14 | [Tide](#tide) | 2026-10-08 | rendering | flux_2_klein_9b_i8x.ckpt 1024x576 | wan_v2.2_a14b_hne_i2v_i8x.ckpt ? min | Calm Ambient Dreamscape | `—` | — |
| 15 | [Yang family — one LoRA, three subjects](#yang_family_lora) | 2026-09-30 | delivered 2026-09-30 — yang_family_lora_4000_lora_f32.ckpt, 9 h 22 m, 5 checkpoints at 843 MB each | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | — |
| 16 | [Yang family LoRA — made to work in ComfyUI](#yang_family_lora_comfy) | 2026-10-02 | in progress — source analysed and the mapping derived; converter not yet written | FLUX.2 [klein] 9B 576x1024 | Wan 2.2 High Noise ? min | Calm Ambient Dreamscape | `—` | — |
| 17 | [Kyle — where the ground breathes](#kyle_steamfield) | 2026-10-03 | clips QC’d 2026-10-03 — 60.41 s planned, finishing | FLUX.2 [klein] 9B 1024x576 | LTX-2.3 22B [distilled] 1.1 11 min | light_adventure.mp3 under the LTX ambience at 0.45, 1.5 s in, 2 s out. NOTE: music belongs at run-spec.music, NOT run-spec.assemble.music | `—` | — |
| 18 | [Lindsey — the eighth try](#lindsey_sparky) | 2026-10-03 | delivered | FLUX.2 [klein] 9B 1024x576 | LTX-2.3 22B [distilled] 1.1 11 min | emotional_children_piano.mp3 at 0.45 under the clip audio. NOTE: music belongs at run-spec.music, NOT run-spec.assemble.music | `—` | — |

## Dragon Epic — 1-minute photoreal short, family hero face {#dragon_epic}

- **Date**: 2026-09-21 · **Status**: in progress — scene 1A posted · **Version**: `v1-drawthings-ui` · **Draw Things project**: `dragon-1a (scene 1A I2V), dragon-1b (scene 1B stills, Kevin, 5 refs), dragon-1b-tests (1B v1/v2)`
- **This version**: Rendered by driving the Draw Things app window (accessibility automation).
- **Files** (`projects/dragon_epic/v1-drawthings-ui/`): `dragon/scene1a_v3.mov`, `dragon/scene1a_v3_4k.mp4`, `dragon/scene1a_v3_4k_music.mp4 (with music)`, `music/dragons_breath.mp3`, `dragon/scene1a.mov (v1, ghosting)`, `dragon/scene1a_4k.mp4 (v1)`
- **Notes**: Plan page: wiki/dragon-epic-plan.md. Experiments E1–E7 must pass before rendering the shot list. Needs face photos in projects/dragon_epic/v1-drawthings-ui/raw/face/. Delivery is 4K UHD. Scene 1A: v1 ghosted (push-in + translation), v2 noise (refiner 50%), v3 clean (10%, articulation-only prompt).

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

## Lost City — hyper-real rider on a raptor-dragon entering jungle ruins {#lost_city}

- **Date**: 2026-09-21 · **Status**: in progress — 4K with music: s3, s4, s5, s8, s9; s1 and s2 at 4K without music; s6 trimmed to 4.6 s and never upscaled; **s7 (escape run) not rendered**; no film assembled yet · **Version**: `v2-drawthings-cli` · **Draw Things project**: `lostcity-s1, s2, s3, s7 (named); s8, s9 (cloned — clone crashes on video save); s10 and s11 in fresh Untitled projects; s14 rendered with draw-things-cli (no project file)`
- **This version**: Rendered headless with draw-things-cli; the shots the app version never finished.

**Versions**

| Version | What it is | Status | YouTube |
|---|---|---|---|
| `v1-drawthings-ui` | Rendered by driving the Draw Things app window (accessibility automation). | in progress — 4K with music: s3, s4, s5, s8, s9; s1 and s2 at 4K without music; s6 trimmed to 4.6 s and never upscaled; **s7 (escape run) not rendered**; no film assembled yet | [▶ watch](https://youtu.be/68sq_jZqu6c) |
| `v2-drawthings-cli` | Rendered headless with draw-things-cli; the shots the app version never finished. | in progress — 4K with music: s3, s4, s5, s8, s9; s1 and s2 at 4K without music; s6 trimmed to 4.6 s and never upscaled; **s7 (escape run) not rendered**; no film assembled yet | [▶ watch](https://youtu.be/68sq_jZqu6c) |

- **Files** (`projects/lost_city/v2-drawthings-cli/`): `lostcity/ref_openart_rider_ruins.webp (reference, raw/)`, `lostcity/crop_creature_rider.png, crop_spires.png, crop_foreground.png (Moodboard refs, raw/)`, `lostcity/s1_still_v1.png (shot 1 still, klein)`, `lostcity/s1_ltx_v1.mov (LTX-2.3 test, 1024x576x97 @25fps + audio)`, `lostcity/s2_still_v1.png (shot 2 still, klein, refs: our s1 skyline + spires crop, seed 1)`, `lostcity/s5_still_v2.png (shot 7 still, wingless; s5_still_v1_winged.png = rejected v1)`, `lostcity/s2_wan_v1.mov (shot 2 I2V, Wan 2.2, 1280x768x81)`, `lostcity/s2_wan_v1_4k.mp4 (3840x2160 HEVC 10-bit)`, `lostcity/s2_ltx_v1.mov (shot 2 via LTX-2.3, 1024x576x97 @25fps + audio)`, `lostcity/s2_ltx_v1_4k_audio.mp4 (LTX shot 2 at 3840x2160 + audio)`, `lostcity/s4_still_v1.png (shot 3 still, ref = crop of our s1 creature body)`, `music/mystical_flute.mp3`, `lostcity/s4_ltx_v2.mov (shot 3 LTX v2, hold-position prompt)`, `lostcity/s4_ltx_v2_4k_music.mp4 (4K + ambience + music bed)`, `lostcity/s4_ltx_v1_walkout.mov (v1, rejected: walk-out + phantom rider)`, `lostcity/s5_still_v1.png (side profile, anatomy OK)`, `lostcity/s5_ltx_v1.mov (LTX 1024x576x249 @25fps)`, `lostcity/s5_ltx_v1_4k_music.mp4`, `lostcity/s8_still_v1.png (gallop)`, `lostcity/s8_ltx_v1.mov + s8_ltx_v1_4k_music.mp4 (gallop, 10 s)`, `lostcity/s6_still_v1.png, s6_ltx_v1.mov (jump; drifts after ~4.6 s), s6_ltx_v1_trim.mov (clean 116 f)`, `lostcity/s3_still_v1.png, s3_ltx_v1.mov, s3_ltx_v1_4k_music.mp4 (drinking, 10.3 s, holds design)`, `lostcity/s9_still_v1.png (seed 2; s1/s4 variants kept)`, `lostcity/s9_ltx_v1.mov (ProRes 422 HQ, 249 f @ 25 fps + PCM audio)`, `lostcity/s9_ltx_v1_4k_music.mp4`
- **Notes**: Plan: wiki/lost-city-plan.md. Reference is an OpenArt render (closed model, unknown); we re-generate our own frame. 8 shots × 5 s first. Experiments L0–L6 gate rendering; L1 = first LTX-2.3 test on this Mac. Shots renumbered 2026-09-25 to the cut order (old→new: s10→s3, s3→s4, s7→s5, s9→s6, s13→s7, s14→s9; s1, s2, s8 and s15a-c unchanged). The dismount/mount-up beat (old s11, s12) was dropped: klein rendered two creatures for every phrasing tried, and the story reads without it. The s15 rift coda (a crack opens in the sky, winged reptiles pour out and circle the ruins) was cut from the project on 2026-09-25; its three clips and the assembled 30 s film were deleted.

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
| Loop | none — xfade concat; s15 assembled with scripts/assemble_film.sh (XFADE=0.5, MUSIC=mystical_flute.mp3) then +6 dB |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus → 3840x2160 HEVC 10-bit |
| Music | Mystical orchestral theme with ancient flute — DesiFreeMusic, Pixabay (cdn.pixabay.com/audio/2025/07/12/audio_fb278af2ae.mp3), 4:00, steady −15 dB from 0 s, dips at 80 s and 200 s |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *style head* — Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain.
- *style tail* — Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.
- *creature* — a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs
- *rider* — a lone rider, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots

**Rules**: Never write 'dragon' (grows wings) or 'two-legged' (breaks legs). Quadruped wording only. Side/three-quarter framing — rear-view low angles fail. Moodboard refs must be crops, never a full wide frame. Destruction shots: name the subject and its stillness first, then confine the falling verbs to the distance in one clause — LTX bleeds collapse motion onto anything small or mentioned after it (s14 v1: the creature's head fell off like a spire). Keep the subject at least a third of the frame wide in any shot where other things break apart.


#### s1 — Side view, rider + creature walk toward the city (reference frame)

- **Engine**: LTX-2.3 1024x576 x97
- **Files**: s1_still_v1.png, s1_ltx_v1.mov, s1_ltx_v1_4k_audio.mp4

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A lost city of tall eroded sandstone spires and ziggurat towers swallowed by jungle rises in the distance through morning haze, a stone arch bridge and a white waterfall between them, soft volumetric god rays breaking through thin cloud. Mossy stone blocks and palms in the middle distance, ferns and tall grass in the foreground. In the centre, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking left to right on a dirt path on two heavy hind legs and two smaller forelegs. On its back a lone rider seen from behind, dark cropped hair, grey-green hooded cloak thrown back, brown leather jerkin, tan trousers, tall boots, hands on the reins. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature walks slowly from left to right with a heavy four-legged gait, its head bobbing and tail swaying, while the camera tracks alongside at the same pace so the rider stays centred in frame. The rider sways gently in the saddle, the cloak lifting in a light breeze. Behind them the waterfall pours steadily and thin mist drifts through the shafts of light; two birds glide across the distant spires. Heavy footsteps on damp earth, the far roar of the waterfall, faint jungle birdsong, no music.


#### s2 — Extreme wide from a ledge, tiny rider on the path

- **Engine**: both — Wan 2.2 1280x768 x81 and LTX 1024x576 x97
- **Files**: s2_still_v1.png, s2_wan_v1_4k.mp4, s2_ltx_v1_4k_audio.mp4

*Still prompt*

> Cinematic film still, anamorphic 35mm, extreme wide establishing shot from a high mossy ledge, muted colours, low contrast, subtle film grain. Below and beyond, a lost city of tall eroded sandstone spires and ziggurat towers swallowed by jungle stretches to the horizon through layered morning haze, a stone arch bridge and a white waterfall between the towers, soft volumetric god rays breaking through thin cloud. A narrow dirt path winds down from the ledge toward the city; on it, very small in the frame, a lone hooded rider on a large wingless quadrupedal raptor-like dragon walks toward the city, seen from behind. Ferns and a broken stone column in the foreground on the ledge, palms and mossy blocks in the middle distance, birds tiny in the sky. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt (Wan)*

> very slow push in, the camera drifting gently forward toward the city, mist drifting slowly through the god rays, the waterfall flowing steadily, thin clouds moving very slowly, ferns and palm fronds swaying in a light breeze, tiny birds gliding across the distant sky, the small rider and creature walking slowly along the path away from the camera, subtle motion, smooth, cinematic, photorealistic

*Video prompt (LTX)*

> The camera pushes in very slowly and steadily toward the distant city, the mossy columns in the foreground drifting past the edges of the frame. The small rider and creature walk slowly down the dirt path away from the camera toward the city. Mist drifts through the shafts of light, the waterfall pours steadily under the stone arch, ferns and palm fronds sway in a light breeze, and tiny birds glide across the sky above the spires. Wind through jungle leaves, the distant hush of the waterfall, faint birdsong, no music. Photorealistic, cinematic, smooth motion.


#### s3 — Drinking at a jungle pool

- **Engine**: LTX 1024x576 x257 (10.3 s)
- **Files**: s3_still_v1.png, s3_ltx_v1_4k_music.mp4
- **Note**: Best of the batch — design holds the full clip.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A still jungle pool below a small waterfall at the edge of the lost city, mossy carved blocks and ferns around the water, eroded sandstone spires in the haze behind, god rays through the canopy. At the water's edge in side profile, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs with its neck lowered and its muzzle touching the water, ripples spreading across the surface, its reflection in the pool. On its back a lone rider, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots, sitting relaxed in the saddle looking around. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> Fixed camera on the pool. The creature stands in place at the water's edge and drinks, lowering its muzzle to the surface and lifting its head slowly with water dripping from its jaw, then lowering it again, its throat working as it swallows, tail swaying gently. The rider sits relaxed in the saddle and turns his head to look around at the ruins. Ripples spread across the pool and settle, the waterfall pours steadily behind, mist drifts, ferns move in a light breeze. Water lapping and dripping, the hush of the waterfall, leather creaking, faint birdsong, no music.


#### s4 — Low angle, creature's feet on wet flagstones

- **Engine**: LTX 1024x576 x97
- **Files**: s4_still_v1.png, s4_ltx_v2_4k_music.mp4
- **Note**: v1 asked for one step forward — it walked out of frame and hallucinated a second rider. Close-ups need hold-position wording.

*Still prompt*

> Cinematic film still, anamorphic 35mm, very low camera angle at ground level on a wet jungle path, muted colours, low contrast, subtle film grain. Filling the frame, the heavy clawed feet and thick scaled legs of a large saddled raptor-like reptile mount, a wingless two-legged theropod with slate-grey ridged hide, planted on wet mossy flagstones, water pooled between the stones, ferns and tall grass in the near foreground, the rider's boot in a stirrup and a hanging brown satchel visible above. Behind, out of focus, mossy carved blocks and the haze of a lost city with soft god rays. Shallow depth of field, layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> Fixed camera, low on the wet stone path. The creature stands still in place and does not walk; it only shifts its weight from one foot to the other, the claws flexing on the wet flagstones, small ripples spreading in the pooled water, the thick scaled legs tensing, the tail swaying slowly. The rider's boot rocks gently in the stirrup and the satchel sways. Ferns and grass in the foreground move in a light breeze, mist drifts through the god rays behind. The path behind stays empty. Water dripping, leather creaking, wind in the leaves, faint birdsong, no music. Photorealistic, cinematic, subtle smooth motion.


#### s5 — Canyon, side profile walking through the spires

- **Engine**: LTX 1024x576 x249 (10 s)
- **Files**: s5_still_v1.png, s5_ltx_v1_4k_music.mp4
- **Note**: Six rear-view attempts failed on anatomy before switching to this side framing.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. Inside a narrow canyon between colossal eroded sandstone spires and ziggurat towers of a lost city, soft volumetric god rays pouring down through morning haze, dust drifting in the light, vines and moss hanging from the carved stone walls. In the centre, walking left to right along a dirt path, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs. On its back a lone rider seen from the side, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots, hands on the reins, looking up at the towers. Ferns and broken carved blocks in the foreground, tiny birds high in the sky. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The camera holds a steady low side view as the creature walks slowly from left to right through the canyon with a heavy four-legged gait, its head bobbing gently and tail swaying, staying in the centre of the frame while the carved stone walls drift past behind it. The rider sways in the saddle, cloak lifting in a light breeze, looking up at the towers. Dust and pollen drift through the shafts of light, mist rolls slowly along the ground, ferns sway, tiny birds cross the sky. Heavy footsteps on packed earth, leather creaking, wind in the vines, faint jungle birdsong, no music.


#### s6 — Jumping — leap over a fallen pillar

- **Engine**: LTX 1024x576 x249
- **Files**: s6_still_v1.png, s6_ltx_v1.mov, s6_ltx_v1_trim.mov
- **Note**: Creature morphs toward a horse after ~frame 115 (4.6 s) — trimmed there.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A jungle path beside the lost city, spires and ziggurat towers in the haze behind, god rays through morning mist. In the centre, caught mid-leap in side profile over a fallen mossy stone pillar lying across the path, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs, its heavy hind legs extended behind from the push-off and its smaller forelegs tucked up, body arched in the air above the pillar. On its back a lone rider crouched low in the saddle gripping the reins, grey-green hooded cloak flaring, brown leather jerkin, tan trousers, tall boots. Ferns and broken carved blocks in the foreground, tiny birds high in the sky. Motion, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature completes its leap over the fallen stone pillar, forelegs reaching down and hind legs swinging under it, lands on the far side with a puff of dust and runs on a few strides before slowing to a walk, while the camera tracks alongside at the same pace keeping the creature and rider centred in frame. The rider absorbs the landing, rising and settling in the saddle, cloak snapping. Dust bursts at the landing, ferns shake, birds scatter. A heavy thudding landing, pounding footfalls, leather creaking, distant birdsong, no music.


#### s7 — Escape — running as the spires collapse

- **Engine**: LTX 1024x576 x249 — plan for drift: keep the creature large in frame and cut by ~5 s if the design softens
- **Note**: Fast locomotion, so expect drift after ~4-5 s (see s8/s6). Mitigation: subject fills the lower half, camera locked alongside, and trim on the first soft frame.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A wide dirt avenue between the colossal eroded sandstone spires and ziggurat towers of the lost city, the air thick with dust and falling debris, shafts of hard sunlight cutting through the dust clouds, cracks running up the carved stone walls. In the centre foreground, galloping left to right in side profile and filling the lower half of the frame, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, all four legs in a running gallop with the heavy hind legs driving and the smaller forelegs reaching forward, dust exploding from its feet. On its back a lone rider leaning low over the neck gripping the reins, grey-green hooded cloak streaming straight back, brown leather jerkin, tan trousers, tall boots, glancing back over his shoulder. Behind and above them a spire is breaking apart mid-collapse, huge carved blocks tumbling through the air and a wall of dust rolling down the avenue. Ferns and rubble in the foreground. Motion, danger, energy, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature gallops at full speed from left to right down the avenue with a powerful four-legged running gait, dust bursting from each stride, while the camera tracks alongside at the same speed keeping the creature and rider centred in frame as the collapsing city rushes past behind. The rider stays low over the neck, cloak whipping back, and glances over his shoulder. Behind them a spire shears and falls, carved blocks tumbling and smashing into the avenue, a wall of dust rolling forward and swallowing the towers, smaller stones bouncing across the ground. Deep grinding stone, crashing masonry, pounding footfalls, rushing wind, no music.


#### s8 — Running — full gallop across a clearing

- **Engine**: LTX 1024x576 x249
- **Files**: s8_still_v1.png, s8_ltx_v1_4k_music.mp4

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. An open jungle clearing beside the lost city, eroded sandstone spires and ziggurat towers soft in the haze behind, god rays through thin cloud. In the centre, galloping left to right at full stride in side profile, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, all four legs in a running gallop with the heavy hind legs driving and the smaller forelegs reaching forward, dust kicked up behind it, on two heavy hind legs and two smaller forelegs. On its back a lone rider leaning low over the neck holding the reins, grey-green hooded cloak streaming straight back, brown leather jerkin, tan trousers, tall boots. Ferns and tall grass in the foreground, tiny birds high in the sky. Motion, energy, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature gallops at full speed from left to right across the clearing with a powerful four-legged running gait, hind legs driving and forelegs reaching, dust bursting up behind each stride, while the camera tracks alongside at the same speed keeping the creature and rider centred in the frame as the ruins and jungle rush past behind. The rider stays low over the neck, cloak whipping straight back. Grass and ferns blur past in the foreground, birds scatter from the trees. Pounding heavy footfalls, rushing wind, leather creaking, distant birds, no music.


#### s9 — Escape — final shot: the whole skyline falls, creature watching

- **Engine**: LTX 1024x576 x249 (9.96 s) — rendered headless with draw-things-cli, 9 min 41 s
- **Note**: v1 failed: LTX applied the collapse to the creature — its head sheared off and fell like a spire. Two causes, both fixed here. (1) Scale: the creature was a sixth of the frame, so its head was ~30 px in the 32x32 LTX latent and got re-synthesised as debris; it now fills the left third close to camera. (2) Prompt order and verbs: the falling verbs came before the subject and bled onto it. Subject first with positive rigidity words (solid, still, intact, head held level and attached, only the ribs move), then one sentence that pins the destruction to the horizon ('all of the destruction is far away on the horizon and nowhere near them'). Pace so the last tower falls by ~8 s and the final second is an empty dust skyline — the film's last frame. v2 rendered 2026-09-22 and works: creature solid the whole clip, spires fall through the shot, skyline empty by the last second. Both still and clip came from draw-things-cli with no UI (seed 2 of 3 stills, text-only — no Moodboard refs, which the released CLI cannot do yet); see [[headless-cli-pipeline]].

*Still prompt*

> Cinematic film still, anamorphic 35mm, wide landscape view from a high grassy ridge, muted colours, low contrast, subtle film grain. Standing on the ridge in the left foreground, close to the camera, in clear side profile and filling the left third of the frame from the ground to two thirds of the height, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck held up and steady with the head sharply in focus, a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, standing squarely on two heavy hind legs and two smaller forelegs. On its back a lone rider sitting upright and turned to look back, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots. Grass and ferns around its feet. Beyond the ridge the land drops away into a vast hazy valley of dark jungle canopy, and far away on the horizon the whole lost city of colossal eroded sandstone spires and ziggurat towers is coming down, towers leaning and breaking apart, immense dust plumes rising and merging into a low grey wall spreading across the valley floor, shafts of hard sunlight through the dust. Huge sense of scale, sharp intact animal in the foreground against a distant collapsing skyline, deep depth of field, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> Fixed camera, wide landscape. In the foreground the creature stands solid and completely still on the ridge, its whole body intact and upright, the long neck steady and the head held level and attached, only its ribs moving with deep slow breaths and its tail swaying gently; the rider sits upright in the saddle and watches, cloak moving in the wind; grass and ferns bend around their feet. All of the destruction is far away on the horizon and nowhere near them: out there in the distance the city finishes falling, spire after spire leaning, buckling and dropping in slow heavy arcs, the tallest towers going last, each collapse throwing up a fresh dust plume until the plumes merge into one grey wall rolling outward, and by the end nothing is left standing on the skyline, only a flat bank of dust over rubble. Distant thunderous collapse, grinding stone, rising wind, heavy animal breathing, no music.

## Night Elf Hunter — a boy and his bear crossing the grassland {#nightelf_hunter}

- **Date**: 2026-09-26 · **Status**: research — B0 partial pass 2026-09-26: 30 images, identity 30/30, angles skewed (back 1/3, over-shoulder 0/2); v1 remains the delivered film · **Version**: `v2-lora-identity` · **Draw Things project**: `none — draw-things-cli via scripts/seed_sheet.sh --dataset`
- **This version**: Research version: carry the same character with trained LoRA weights instead of reference tokens. Phase 1 (experiment B0) builds the training dataset; no film is rendered from this version yet.

**Versions**

| Version | What it is | Status | YouTube |
|---|---|---|---|
| `v1-drawthings-cli` | First version: photoreal live-action fantasy, half-elf treatment (Kyle's face, elf ears and markings), rendered headless with draw-things-cli. | delivered 2026-09-26 05:16 — 57.64 s, 3840x2160 + 1920x1080, 8 shots, none dropped (see plan §0) | — |
| `v2-lora-identity` | Research version: carry the same character with trained LoRA weights instead of reference tokens. Phase 1 (experiment B0) builds the training dataset; no film is rendered from this version yet. | research — B0 partial pass 2026-09-26: 30 images, identity 30/30, angles skewed (back 1/3, over-shoulder 0/2); v1 remains the delivered film | — |

- **Files** (`projects/nightelf_hunter/v2-lora-identity/`): `seed/dataset/ds_01..ds_30.png (images, git-ignored)`, `seed/dataset/ds_01..ds_30.txt (captions, tracked)`, `seed/dataset_contact.png (QC contact sheet, generated)`
- **Notes**: This version exists to answer the B-series experiments in wiki/blueprint-v2-research.md, not to make a second film. v1 stays the delivered cut. The dataset deliberately breaks v1's practice in one place: v1 prompts name every feature to preserve, while these CAPTIONS name only what varies, so the permanent features bind to the trigger token nelf_kyle (the Isolation Rule). The generation prompts still name everything — two different strings per image, one to make the pixels and one to train on.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 512x768 portrait, 768x512 for the six wides |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |

Prompt: `generated per cell by scripts/seed_sheet.sh --dataset`

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
| Upscale | none — training images stay at native size |
| Music | none |

## Ivy — character LoRA {#ivy_lora}

- **Date**: 2026-09-26 · **Status**: delivered 2026-09-26 — ivy_lora_2000_lora_f32.ckpt at weight 0.5; identity holds in unseen scenes, profile and back-of-head degrade (dataset has neither) · **Version**: `v1-photo-dataset` · **Draw Things project**: `none — draw-things-cli train lora`
- **This version**: Character LoRA trained on real photographs. The output is a reusable identity asset, not a film: any later project loads it with a trigger token instead of carrying a master into every shot.
- **Files** (`projects/ivy_lora/v1-photo-dataset/`): `raw/ (source photographs, git-ignored)`, `seed/dataset/NN.png + NN.txt (training pairs; captions tracked)`, `logs/train.log`
- **Notes**: Ivy is family, an adult; consent settled, same standing as Kyle and Lindsey. Real photos are the better dataset: B0 proved klein will not synthesize back views or true camera-height variation from a frontal master, because the reference image overrides the prompt. Photographs have those angles already — except that this particular set does not: all 22 frames are frontal or three-quarter. raw/ is git-ignored because consent to train on a face is not consent to publish the source photographs to a public repo.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | aspect-bucketed, 512 base |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
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

## Lindsey — character LoRA {#lindsey_lora}

- **Date**: 2026-09-27 · **Status**: trained 2026-09-27 — 2000 steps in 2 h 26 m, five checkpoints; evaluation pending · **Version**: `v1-photo-dataset` · **Draw Things project**: `none — draw-things-cli train lora`
- **This version**: Character LoRA for Lindsey from a 32-frame turnaround that covers full body as well as head angles. Third in the series after ivy_lora and kyle_lora, and the one that tests whether full-body identity is a dataset gap or a latent-resolution limit.
- **Files** (`projects/lindsey_lora/v1-photo-dataset/`): `raw/ (32 source photographs, git-ignored)`, `seed/dataset/NN.png + NN.txt (training pairs; captions tracked)`, `seed/dataset_contact.png`, `logs/train.log`
- **Notes**: Lindsey is Kevin's daughter; consent settled. The dataset is the most complete of the three: head angles (frontal, both profiles, back, three-quarters) AND thirteen full-body frames from front, both sides and behind, across two rooms. Ivy and Kyle both lost identity at full-body distance regardless of weight, which was read as a latent-resolution limit — too few pixels on the face. This set can distinguish the two explanations, because it contains the framing that was missing.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | aspect-bucketed, 512 base |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
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

## Lindsey — the palace pavilion {#lindsey_palace}

- **Date**: 2026-09-28 · **Status**: delivered 2026-09-28 22:07 — 61.08 s, 3840x2160 (293 MB) + 1920x1080 (91 MB), 8 shots, none dropped; mean -21.1 dB, peak -5.4 dB · **Version**: `v1-lora-cli` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: First film driven by a character LoRA rather than reference photographs: lindsey_lora_2000 carries the face, so every still is text-to-image plus an environment reference, with the LoRA weight set per shot.
- **Files** (`projects/lindsey_palace/v1-lora-cli/`): `stills/s1.png … s7.png`, `clips/s1_v1.mov … s7_v1.mov`, `final/lindsey_palace_3840x2160.mp4`, `final/lindsey_palace_1920x1080.mp4`, `music/emotional_children_piano.mp3`
- **Notes**: Lindsey is Kevin's daughter; consent settled. One minute, seven shots trimmed to ~8.5 s each. Weight is set per shot, which is the operative result from ivy_lora and kyle_lora: 1.0 on the close portraits (s3, s7, s2) where identity has to hold and the wardrobe is a small part of frame, 0.85 on the wides and the profile (s1, s5, s6) where 1.0 would start to fight the prompt for the gown, and 0.6 on the macro insert (s4), which has no face and needs all of its prompt grip on silk and embroidery. Lindsey's dataset is the only one of the three with profile, back and full-body coverage, so those framings are expected to hold — s5 and s6 are where that gets tested in a film rather than a grid. No evaluation grid was run first, by request. Cut order is s1 s2 s3 s4 s8 s5 s7 s6 — the walk away from camera closes the film, and the valley insert (s8) sits where the film needs a breath and where nothing can drift.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |
| LoRA | lindsey_lora_2000_lora_f32.ckpt @ per-shot weight (0.6 / 0.85 / 1.0) |

Prompt: `per shot — see scenes`

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

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none — xfade 0.75 |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus -> 3840x2160 |
| Music | Emotional Children Piano — Music_For_Videos, Pixabay (cdn.pixabay.com/download/audio/2023/09/03/audio_2c0ed5a272.mp3), 1:55; first 60 s under the LTX ambience at 0.5, 2 s fade out. Reused from lindsey_art — the same track, the same child, and its first minute builds to ~50 s and resolves at 60 s, which is this film's exact length. |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *subject* — lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair with natural flyaway strands catching the light
- *gown* — a high-fashion Naboo-inspired royal gown in rich emerald green silk with gold lace trim, a high structured collar and intricate gold embroidery along the bodice
- *place* — an ornate palace pavilion of pale carved stone, tall slender arches and a carved stone balustrade, overlooking a valley of great golden domed architecture and tall waterfalls falling into rising mist
- *style* — Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

#### s1 — Establishing — she is small at the balustrade, seen from behind

- **Note**: LoRA weight 0.85; edit-mode input seed/pavilion.png

*Still prompt*

> Extreme wide establishing shot. an ornate palace pavilion of pale carved stone, tall slender arches and a carved stone balustrade, overlooking a valley of great golden domed architecture and tall waterfalls falling into rising mist, early morning light, thin mist over the water. Small in the lower third of frame and seen from behind, lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair with natural flyaway strands catching the light, wearing a high-fashion Naboo-inspired royal gown in rich emerald green silk with gold lace trim, a high structured collar and intricate gold embroidery along the bodice, standing alone at the balustrade looking out over the valley. Enormous sense of scale, deep depth of field, layered atmospheric perspective. Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The waterfalls fall steadily, mist drifting upward and across the valley, the hem of the green silk gown stirring in a slow breeze, a few birds crossing far below. The girl stands still. Distant falling water, wind, no music.


#### s2 — Three-quarter front at the balustrade, turned toward camera

- **Note**: LoRA weight 1.0; edit-mode input seed/lindsey.png

*Still prompt*

> Medium shot, three-quarter front view. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair with natural flyaway strands catching the light, wearing a high-fashion Naboo-inspired royal gown in rich emerald green silk with gold lace trim, a high structured collar and intricate gold embroidery along the bodice, turned away from the carved stone balustrade toward the camera, one hand still resting on the stone, her face clearly visible and lit. Standing in an ornate palace pavilion of pale carved stone, tall slender arches and a carved stone balustrade, overlooking a valley of great golden domed architecture and tall waterfalls falling into rising mist. Warm ambient light through the open arches, a bright rim light along her cheek and the flyaway strands of her hair. Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no push in, no zoom. She stays facing the camera three-quarters on the whole time and never turns her head away. The breeze lifts loose strands of her hair across her cheek and moves the silk at her shoulder; she blinks once and breathes. Wind, no music.


#### s3 — Tight close-up portrait, rim light on the flyaway hair — the hero shot

- **Note**: LoRA weight 1.0; edit-mode input seed/lindsey.png

*Still prompt*

> Tight close-up portrait, head and shoulders. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair with natural flyaway strands catching the light, wearing a high-fashion Naboo-inspired royal gown in rich emerald green silk with gold lace trim, a high structured collar and intricate gold embroidery along the bodice with the high structured collar framing her jaw, facing the camera three-quarters on, eyes calm. Soft ambient sunlight from the left, a distinct rim light on the right edge of her face lighting every flyaway hair, the domes and waterfalls of an ornate palace pavilion of pale carved stone, tall slender arches and a carved stone balustrade, overlooking a valley of great golden domed architecture and tall waterfalls falling into rising mist thrown far out of focus behind her. Razor-sharp focus on the eyes, skin texture, individual eyelashes. Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera, almost no movement. She blinks slowly, her eyes shift a fraction toward the light, loose hairs move in the breeze, the collar of the gown catches the light as she breathes. Faint wind, no music.


#### s4 — Macro insert — silk, gold lace, embroidery, hands on the stone rail

- **Note**: LoRA weight 0.6; edit-mode input seed/lindsey.png

*Still prompt*

> Extreme close-up detail insert, no face in frame. The bodice and sleeve of a high-fashion Naboo-inspired royal gown in rich emerald green silk with gold lace trim, a high structured collar and intricate gold embroidery along the bodice — rich emerald green silk catching the light, gold lace trim, dense gold embroidery, small hands resting on a weathered carved stone balustrade. Every thread and the weave of the silk visible. Macro clarity, very shallow depth of field. Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked macro camera. Only the faintest movement: the silk shifts a few millimetres as she breathes, light creeps slowly across the gold embroidery, her fingers relax on the warm stone. The sleeve stays flat against her arm — nothing lifts, flaps or folds over. Faint wind, distant water, no music.


#### s8 — The valley itself — what she is looking at

- **Note**: no LoRA at all; no face in frame, so nothing can drift

*Still prompt*

> Extreme wide landscape, no people in frame, shot from inside the shade of the pavilion looking out between two tall carved stone columns. A valley of great golden domed architecture and tall waterfalls falling into rising mist, morning sun burning through the haze, birds turning far below, terraces of green between the falls. Enormous sense of scale, deep depth of field, layered atmospheric perspective. Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The waterfalls fall steadily, mist rolling upward and drifting across the valley, sunlight shifting slowly through the haze, birds turning far below. Falling water, wind, no music.


#### s5 — True profile, backlit, she turns toward camera

- **Note**: LoRA weight 0.85; edit-mode input seed/lindsey.png

*Still prompt*

> Medium shot, true profile. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair with natural flyaway strands catching the light, wearing a high-fashion Naboo-inspired royal gown in rich emerald green silk with gold lace trim, a high structured collar and intricate gold embroidery along the bodice, standing in profile against the bright open arch of an ornate palace pavilion of pale carved stone, tall slender arches and a carved stone balustrade, overlooking a valley of great golden domed architecture and tall waterfalls falling into rising mist, backlit so the rim light traces her profile and the flyaway hair around her head, her face still readable in the soft fill light bouncing off the pale stone. Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera. She holds her profile, looking out over the valley, and never turns her head. The wind lifts her hair and stirs the silk collar, she blinks once. Wind, no music.


#### s7 — Close-up frontal, the faint smile, hold

- **Note**: LoRA weight 1.0; edit-mode input seed/lindsey.png

*Still prompt*

> Close-up portrait, frontal, slightly low angle. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair with natural flyaway strands catching the light, wearing a high-fashion Naboo-inspired royal gown in rich emerald green silk with gold lace trim, a high structured collar and intricate gold embroidery along the bodice, looking just past the camera toward the light with the faintest beginning of a smile. Golden ambient sunlight, strong rim light along her hair and the high collar, an ornate palace pavilion of pale carved stone, tall slender arches and a carved stone balustrade, overlooking a valley of great golden domed architecture and tall waterfalls falling into rising mist soft and luminous far behind her. Razor-sharp focus on the eyes and skin. Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera. She lifts her chin a fraction, the small smile settles, she blinks once and holds her gaze on the light; hair and silk move gently in the breeze. Wind, distant water, no music.


#### s6 — Wide full body from behind, walking the colonnade

- **Note**: LoRA weight 0.85; text-to-image, no environment plate

*Still prompt*

> Wide full-body shot from behind at a low angle, looking straight down a long colonnade. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair with natural flyaway strands catching the light, wearing a high-fashion Naboo-inspired royal gown in rich emerald green silk with gold lace trim, a high structured collar and intricate gold embroidery along the bodice, the long emerald skirt trailing on polished pale stone, walking away from the camera mid-stride down a deep receding row of tall carved stone columns, hard bars of sunlight falling across the floor between the columns, golden domes and tall waterfalls in rising mist glimpsed through the arches to her left. Strong one-point perspective down the colonnade. Cinematic film still, Leica S3 medium format, 120mm lens, photoreal skin and fabric, soft ambient sunlight with a subtle rim light, razor-sharp focus on facial detail and silk texture, shallow depth of field, fine film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera. She walks slowly away down the colonnade, the silk skirt trailing and swaying behind her, bars of sunlight passing over her as she goes, mist rising beyond the arches. Footsteps on stone, water, no music.

## Kyle — five minutes to showtime {#kyle_debut}

- **Date**: 2026-09-28 · **Status**: delivered 2026-09-29 01:20 — 60.76 s, 3840x2160 (279 MB) + 1920x1080 (79 MB), 8 shots, none dropped; mean -21.7 dB, peak -5.5 dB · **Version**: `v1-lora-cli` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: Second LoRA-driven film, and the first written to the rule that came out of lindsey_palace: no shot may rotate or occlude the face, because the video model never sees the LoRA.
- **Files** (`projects/kyle_debut/v1-lora-cli/`): `stills/s1.png … s8.png`, `clips/s1_v1.mov … s8_v1.mov`, `final/kyle_debut_3840x2160.mp4`, `final/kyle_debut_1920x1080.mp4`, `music/emotional_children_piano.mp3`
- **Notes**: Kyle is Kevin's son; consent settled. One minute, eight shots. The story is the five minutes before a nine-year-old walks out to lead a symphony: composure, the waiting piano, a collar straightened, the doors opening, the walk toward the stage.

Written around two known limits. First, **the video model never sees the LoRA**, so identity is fixed at the still and any motion that rotates or occludes the face lets LTX recast the subject (lindsey_palace s5 came back as an adult). Every face shot here is therefore locked frontal with motion limited to breathing, blinking and hands; the story's one turn — 'turns smoothly on his heel' — is rendered as a still already facing away, with motion only continuing the walk. Second, **Kyle's dataset is 16 turnaround frames and only one full-body frame**, so identity is dependable close and at angle but not at full-body distance; the wides (s1, s8) sit at 0.85 and are composed so the face is small or turned away, and the three shots with no person in them (s5, s7) carry no LoRA at all.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |
| LoRA | kyle_lora_2000_lora_f32.ckpt @ per-shot weight (none / 0.6 / 0.85 / 1.0) |

Prompt: `per shot — see scenes`

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
| I2V time (min) | 11 |

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none — xfade 0.75 |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus -> 3840x2160 (~10 min per clip) |
| Music | Emotional Children Piano — Music_For_Videos, Pixabay (cdn.pixabay.com/download/audio/2023/09/03/audio_2c0ed5a272.mp3), 1:55; first 60 s under the LTX room tone at 0.5, 2 s fade out. Solo piano is the one instrument this story requires, and its first minute builds to ~50 s and resolves at 60 s. |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *subject* — kyle_kx boy, an elegant nine-year-old boy, this exact face, neat dark hair
- *wardrobe* — a bespoke navy velvet double-breasted blazer with satin lapels, a fine silk pocket square and a crisp white tailored collar shirt
- *place* — a grand neoclassical foyer of the royal conservatory, polished marble columns, a checkerboard marble floor, crystal chandeliers glowing warm overhead, heavy double oak doors at the far end
- *style* — High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

#### s1 — Establishing — the foyer, he stands alone at its centre

- **Note**: LoRA weight 0.85; edit-mode input seed/foyer.png

*Still prompt*

> Extreme wide establishing shot. a grand neoclassical foyer of the royal conservatory, polished marble columns, a checkerboard marble floor, crystal chandeliers glowing warm overhead, heavy double oak doors at the far end, empty and hushed, late afternoon light and chandelier glow mixing on the marble, long reflections on the polished floor. Small at the exact centre of frame, kyle_kx boy, an elegant nine-year-old boy, this exact face, neat dark hair, wearing a bespoke navy velvet double-breasted blazer with satin lapels, a fine silk pocket square and a crisp white tailored collar shirt, standing perfectly composed and facing the camera. Enormous sense of scale, deep depth of field, symmetrical composition. High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The chandelier light flickers almost imperceptibly, fine dust drifting through the light shafts, faint reflections shifting on the polished marble. The boy stands perfectly still. Room tone, a distant murmur of a crowd behind the doors, no music.


#### s2 — Medium — composed, hands at his sides, looking into the lens

- **Note**: LoRA weight 1.0; edit-mode input seed/kyle.png

*Still prompt*

> Medium shot, waist up, straight on. kyle_kx boy, an elegant nine-year-old boy, this exact face, neat dark hair, wearing a bespoke navy velvet double-breasted blazer with satin lapels, a fine silk pocket square and a crisp white tailored collar shirt, standing squarely facing the camera with his hands at his sides, a calm composed expression looking directly into the lens. Behind him a grand neoclassical foyer of the royal conservatory, polished marble columns, a checkerboard marble floor, crystal chandeliers glowing warm overhead, heavy double oak doors at the far end falls into soft focus, the chandeliers reduced to warm circles of light. High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera, no push in. He stands still and holds the camera's gaze; he breathes, blinks once, the velvet of the blazer catching the light as his chest rises. He does not turn his head or look away. Room tone, no music.


#### s3 — Hero close-up — the calm unflinching gaze

- **Note**: LoRA weight 1.0; edit-mode input seed/kyle.png

*Still prompt*

> Tight close-up portrait, head and shoulders, straight on. kyle_kx boy, an elegant nine-year-old boy, this exact face, neat dark hair, wearing a bespoke navy velvet double-breasted blazer with satin lapels, a fine silk pocket square and a crisp white tailored collar shirt with the white collar crisp at his throat, looking directly into the lens, calm and unflinching. Soft diffused chandelier light from above and slightly to the left, a warm rim light along his jaw, a grand neoclassical foyer of the royal conservatory, polished marble columns, a checkerboard marble floor, crystal chandeliers glowing warm overhead, heavy double oak doors at the far end thrown far out of focus behind him. Razor-sharp focus on the eyes, skin texture and individual eyelashes. High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera, almost no movement. He holds the camera's gaze, blinks slowly, breathes; the warm light shifts a fraction across his face. He does not turn his head. Room tone, no music.


#### s4 — Detail — satin lapels, the silk pocket square, the white collar

- **Note**: LoRA weight 0.6; edit-mode input seed/kyle.png

*Still prompt*

> Extreme close-up detail insert, no face in frame. The chest and shoulder of a bespoke navy velvet double-breasted blazer with satin lapels, a fine silk pocket square and a crisp white tailored collar shirt — deep navy velvet with the light raking across the pile, smooth satin lapels, a fine silk pocket square folded at the breast, the crisp white collar edge. Every fibre of the velvet and the weave of the silk visible. Macro clarity, very shallow depth of field, warm marble reflections behind. High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked macro camera. Only the faintest movement: the velvet shifts a few millimetres as he breathes, warm light creeping slowly across the satin lapel and the silk pocket square. The fabric stays flat — nothing lifts, flaps or folds over. Room tone, no music.


#### s5 — The piano waiting — the months of practice, and what comes next

- **Note**: no LoRA — no face in frame; edit-mode input seed/piano.png

*Still prompt*

> Wide interior, no people in frame. A polished black concert grand piano standing alone in a warm side hall of a grand neoclassical foyer of the royal conservatory, polished marble columns, a checkerboard marble floor, crystal chandeliers glowing warm overhead, heavy double oak doors at the far end, its lid raised, the keyboard lid open, chandelier light pooling on the lacquer and reflecting the marble columns. Sheet music open on the stand. Deep depth of field, still and reverent. High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. Nothing moves but the light: the chandelier glow shifting slowly across the black lacquer, fine dust drifting through the beam, a faint reflection wavering on the floor. Room tone, a distant murmur, no music.


#### s6 — He adjusts his collar and takes a slow breath

- **Note**: LoRA weight 1.0; edit-mode input seed/kyle.png

*Still prompt*

> Medium close-up, chest up, straight on. kyle_kx boy, an elegant nine-year-old boy, this exact face, neat dark hair, wearing a bespoke navy velvet double-breasted blazer with satin lapels, a fine silk pocket square and a crisp white tailored collar shirt, both hands raised to adjust the crisp white collar of his shirt, chin slightly lifted, eyes lowered in concentration. Warm chandelier light from above, a grand neoclassical foyer of the royal conservatory, polished marble columns, a checkerboard marble floor, crystal chandeliers glowing warm overhead, heavy double oak doors at the far end soft behind him. High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera. His hands settle the collar and come back down; his chest rises with a slow deep breath and his eyes come up to the lens. He stays facing the camera throughout and never turns his head. Room tone, no music.


#### s7 — The oak doors open and stage light floods the marble

- **Note**: no LoRA — no face in frame; edit-mode input seed/doors.png

*Still prompt*

> Wide shot, no people in frame, looking straight down a grand neoclassical foyer of the royal conservatory, polished marble columns, a checkerboard marble floor, crystal chandeliers glowing warm overhead, heavy double oak doors at the far end at the heavy double oak doors at the far end, standing open onto brilliant golden stage light that floods across the polished marble floor in a long blazing wedge, the chandeliers pale against it. Strong one-point perspective, dramatic contrast between the cool foyer and the hot golden doorway. High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The golden light from the doorway strengthens and spreads slowly across the marble, dust turning in the beam, the chandeliers steady overhead. Room tone, a swell of distant applause, no music.


#### s8 — He walks toward the stage

- **Note**: LoRA weight 0.85; edit-mode input seed/foyer.png

*Still prompt*

> Wide full-body shot from behind and slightly low, strong one-point perspective. kyle_kx boy, an elegant nine-year-old boy, this exact face, neat dark hair, wearing a bespoke navy velvet double-breasted blazer with satin lapels, a fine silk pocket square and a crisp white tailored collar shirt, seen from behind mid-stride walking away from the camera down the length of a grand neoclassical foyer of the royal conservatory, polished marble columns, a checkerboard marble floor, crystal chandeliers glowing warm overhead, heavy double oak doors at the far end toward the open oak doors and the brilliant golden stage light beyond, his silhouette rimmed by it, his long reflection on the polished marble. High-fashion indoor editorial photograph, Hasselblad medium format, soft diffused architectural chandelier lighting, ultra-realistic skin texture, sharp focus, rich warm wood and marble reflections, shallow depth of field, fine film grain, Vogue Kids indoor catalog style. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera. He walks steadily away from the camera toward the golden doorway, his reflection travelling with him on the marble, the light growing as he nears the doors. He never turns back. Room tone, applause rising, no music.

## Kyle: First Flight (v3, no droid) {#kyle_firstflight}

- **Date**: 2026-10-07 · **Status**: stopped · **Version**: `v3-nodroid` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: v3-nodroid

**Versions**

| Version | What it is | Status | YouTube |
|---|---|---|---|
| `v1-lora-cli` | lora-cli | clips QC'd 2026-10-05 — 59.95 s planned | — |
| `v2-sheets` | lora-cli | delivered | — |
| `v3-nodroid` | v3-nodroid | stopped | — |

- **Files** (`projects/kyle_firstflight/v3-nodroid/`): 
- **Notes**: Kyle and the skiff only. Built on v2's masters. The style lock no longer mandates haze, shallow depth of field or a huge pale sky -- that global clause was measured as the sole cause of v2 s5's nine failed candidates (bg 77 -> 9 from removing it alone, same seed, same input). Atmosphere and sky are now placed per shot. Every scene shot is a single-image edit off a combo master, never a diptych. Stopped partway through the 4K pass (5 of 8 shots upscaled); the 8 stills and 8 clips are on disk at 1080p.

**Still**

| Setting | Value |
|---|---|
| Model | flux_2_klein_9b_i8x.ckpt |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1 |
| Shift | 3.0 |
| Sampler | 16 |
| LoRA | kyle_lora_v2_2500_lora_f32.ckpt |

Prompt: `see scenes`

**I2V**

| Setting | Value |
|---|---|
| Model | ltx_2.3_22b_distilled_1.1_q8p.ckpt |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 576x1024 |
| Frames | 249 |
| FPS | 25 |
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
| Upscale | Real-ESRGAN 4K |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *subject* — kyle_kx boy, a nine-year-old boy with child proportions, this exact face, short dark hair, wearing a sun-bleached sand-coloured tunic with the sleeves pushed up, a wide utility belt and cracked leather work gloves
- *skiff* — the same slender riveted boat hull, the same open cockpit with its low curved windscreen, the same stubby swept fins at the stern and the same two thruster nacelles slung underneath, with every patched salvaged panel the colour it already is
- *style* — Cinematic film still from a live-action science-fiction adventure, anamorphic 35mm on film stock, photoreal skin and scuffed painted metal, visible film grain, sand and rust palette. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.
## Kyle — The Boonta Flats {#kyle_saltflats}

- **Date**: 2026-10-04 · **Status**: clips QC'd 2026-10-04 — 59.85 s planned · **Version**: `v3-stills-supplied` · **Draw Things project**: `kyle-saltflats-v3`
- **This version**: supplied-stills

**Versions**

| Version | What it is | Status | YouTube |
|---|---|---|---|
| `v1-lora-cli` | lora-cli | stopped | — |
| `v2-reference-led` | lora-cli | planned — 61.25 s across 8 shots | — |
| `v3-stills-supplied` | supplied-stills | clips QC'd 2026-10-04 — 59.85 s planned | — |

- **Files** (`projects/kyle_saltflats/v3-stills-supplied/`): 
- **Notes**: Third version and a different kind of run: Kevin supplied five finished images and asked for them to be used as the final stills, so there is no still stage at all -- no masters, no candidates, no picks, nothing generated. The film is motion prompts over fixed first frames. Two images carry two shots each with different camera moves, placed non-adjacent, which is what gets the running time to a minute from five images. Every motion prompt holds the machines hovering and keeps faces away from camera, since no still here contains a readable face to propagate. QC trims: s2's push-in overshoots into a blur of metal past frame 170; s6 and s7 both carry LTX's end-of-clip fade (frames 164 and 190), caught by qc_sheet.sh. An eighth clip was added from the arena image with a locked camera to make the minute, placed between the two canyon shots and the finish.

**Still**

| Setting | Value |
|---|---|
| Model | none — supplied |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3.0 |
| Sampler | DDIM Trailing |

**I2V**

| Setting | Value |
|---|---|
| Model | ltx_2.3_22b_distilled_1.1_q8p.ckpt |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 1024x576 |
| Frames | 249 |
| FPS | 25 |
| Steps | 8 |
| CFG | 1 |
| Shift | 5.0 |
| Sampler | 19 |
| Strength | 100% |
| I2V time (min) | 10 |

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none |
| Upscale | Real-ESRGAN x4plus -> 3840x2160 |
| Music | best_adventure_ever.mp3 |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *pace* — Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping.

#### s1 — Start line on the flats

- **Note**: first frame = raw/supplied_18.jpg, supplied unmodified; kept 9.9 s

*Still prompt*

> supplied image raw/supplied_18.jpg

*Video prompt*

> Locked camera low beside the line. The whole row of machines holds station hovering just above the pale ground, their exhaust glow pulsing and heat haze rippling off the metal, fine dust drifting steadily across the ground between them and the distant crowd shifting on the terraces behind. The machines stay where they are and do not move off. The pilots stay low in their cockpits and no face turns toward the camera; nobody else enters the frame at any point. Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping. Engines idling and a distant crowd, no music.


#### s2 — The arena, moments before the start

- **Note**: first frame = raw/supplied_14.jpg, supplied unmodified; kept 9.9 s

*Still prompt*

> supplied image raw/supplied_14.jpg

*Video prompt*

> Very slow push in along the line of waiting machines. Exhaust flares flicker at the rear nozzles, heat haze pours off the engines, loose dust streams low across the stone, the tall banners lift and fall in the wind and the packed crowd moves continuously on the terraces above. The machines hold their position hovering and do not move off. The pilots stay seated low and no face turns toward the camera; nobody else enters the frame. Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping. Engines idling and a roaring crowd, no music.


#### s3 — The ignition panel

- **Note**: first frame = raw/supplied_17.jpg, supplied unmodified; kept 6.0 s

*Still prompt*

> supplied image raw/supplied_17.jpg

*Video prompt*

> Locked camera. The four gauge needles sweep steadily up across their dials and settle, the red ignition button lights and glows, and heat shimmer rises off the scorched metal plate throughout. The brass lever and the panel stay exactly where they are. No person enters the frame at any point. Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping. Switches and turbines rising behind, no music.


#### s4 — Into the canyon

- **Note**: first frame = raw/supplied_16.jpg, supplied unmodified; kept 9.9 s

*Still prompt*

> supplied image raw/supplied_16.jpg

*Video prompt*

> The camera travels with the two machines as they run together down the narrow canyon, the rock walls streaking past on both sides. Blue underglow washes along the stone beneath them, red exhaust streams backwards, and dust boils up continuously behind. Both machines stay level and hold their line, neither turning toward the camera. The pilots stay low in their cockpits and no face turns toward the camera. Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping. Engines echoing off rock, no music.


#### s5 — Down the line

- **Note**: first frame = raw/supplied_18.jpg, supplied unmodified; kept 9.0 s

*Still prompt*

> supplied image raw/supplied_18.jpg

*Video prompt*

> The camera drifts steadily sideways along the row of machines, the near engines sliding past frame while the crowd terraces track behind. Exhaust glow pulses, heat haze ripples and dust streams low across the ground. The machines hold station hovering and do not move off. No face turns toward the camera and nobody enters the frame. Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping. Engines idling, no music.


#### s6 — Flat out between the walls

- **Note**: first frame = raw/supplied_16.jpg, supplied unmodified; kept 9.0 s

*Still prompt*

> supplied image raw/supplied_16.jpg

*Video prompt*

> Locked camera low on the canyon floor as both machines come straight on and past, growing fast in frame and then gone, the rock walls rushing by behind them. Red exhaust streams back, blue underglow sweeps across the stone and a dense wall of dust boils up behind. The pilots stay low and no face turns toward the camera. Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping. Engines at full power, no music.


#### s7 — Across the line

- **Note**: first frame = raw/supplied_15.jpg, supplied unmodified; kept 9.9 s

*Still prompt*

> supplied image raw/supplied_15.jpg

*Video prompt*

> Slow rise and push in from high above the arena as the machine runs the length of the course below, its long flame and dust wake spreading and drifting behind it across the ground. The packed crowd on both sets of terraces moves continuously with arms raised and the banners lift in the wind. The camera stays high and no face comes into frame at any point. Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping. A roaring crowd and engines, no music.


#### s8 — The line holds

- **Note**: first frame = raw/supplied_14.jpg, supplied unmodified; kept 9.9 s

*Still prompt*

> supplied image raw/supplied_14.jpg

*Video prompt*

> Locked camera low beside the waiting line, no camera movement. The machines hold station hovering just above the stone, exhaust flares flickering at the rear nozzles and heat haze pouring off the metal, while loose dust streams low across the ground and the tall banners lift and fall in the wind. The packed crowd moves continuously on the terraces above. The machines do not move off. The pilots stay seated low and no face turns toward the camera; nobody else enters the frame. Everything moves at natural real-time speed, the full speed of a race, with no slow motion and no speed ramping. Engines idling and a roaring crowd, no music.

## Lindsey — above the cloud sea {#lindsey_summit}

- **Date**: 2026-09-29 · **Status**: delivered 2026-09-29 10:42 — 59.88 s, 3840x2160 (280 MB) + 1920x1080 (87 MB), 8 shots, none dropped; mean -18.7 dB, peak -5.3 dB. Planned length 59.75 s, delivered 59.88 s. · **Version**: `v1-lora-cli` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: Third LoRA-driven film and the first built entirely to the shot grammar the previous two produced: face shots locked frontal and cut at ~7 s, the long takes given to backs, macro and landscape.
- **Files** (`projects/lindsey_summit/v1-lora-cli/`): `stills/s1.png … s8.png`, `clips/s1_v1.mov … s8_v1.mov (s3 uses v2)`, `final/lindsey_summit_3840x2160.mp4`, `final/lindsey_summit_1920x1080.mp4`, `music/adventure_journey.mp3`
- **Notes**: Lindsey is Kevin's daughter; consent settled. Story written for this film: a child walks a pine forest at dawn, reads a compass, finds an old stone stair, climbs it, and comes out on a ruined watchtower above a sea of cloud.

Every structural decision here is inherited rather than guessed. Face shots (s2, s4, s7) are locked frontal at weight 1.0 and budgeted at 7.0-7.5 s, because on both previous films every frontal face clip drifted at around eight seconds no matter what the video prompt said. The long takes go to the three things that held their full length before: walking away from camera (s1, s6), a macro insert with no face (s3), and pure landscape (s5, s8). s4 is the one shot asking for real movement from a person, and it is hand movement in front of a stationary head — the pattern that survived 9.9 s on kyle_debut s6. Every motion prompt says 'the light stays constant', because LTX reads 'the light shifts' as the lights going down.

Palette deliberately opposite to lindsey_palace: cold blue mist and wool instead of warm gold and silk, outdoors instead of interiors.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |
| LoRA | lindsey_lora_2000_lora_f32.ckpt @ per-shot weight (none / 0.6 / 0.85 / 1.0) |

Prompt: `per shot — see scenes`

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
| I2V time (min) | 11 |

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none — xfade 0.75 |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus -> 3840x2160 |
| Music | Adventure Journey — The_Mountain, Pixabay (cdn.pixabay.com/download/audio/2025/03/23/audio_51e1fddfd9.mp3), 2:07; first 60 s under the LTX ambience at 0.45, 2 s fade out. Reused from nightelf_hunter for its rising arc — -18.5 dB at the start climbing to -10 dB by 60 s, which is the shape of a climb that ends in a reveal. |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *subject* — lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair loose with natural flyaway strands
- *wardrobe* — a weathered waxed-canvas explorer's jacket in deep forest green over a cream cable-knit wool sweater, a worn leather satchel on a strap across her body and a small brass compass on a cord at her chest
- *forest* — an ancient pine forest on a steep mountainside at dawn, tall straight trunks receding into cold blue mist, deep moss and fern over granite boulders, shafts of early light coming through the canopy
- *summit* — a ruined stone watchtower on a high clifftop, weathered blocks and a broken arch, standing above an endless sea of cloud with distant blue peaks breaking through it, lit by a low gold sunrise
- *style* — Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

#### s1 — Establishing — the forest at dawn, she is small on the trail

- **Note**: LoRA weight 0.85; input seed/forest.png; kept 9.5 s

*Still prompt*

> Extreme wide establishing shot. an ancient pine forest on a steep mountainside at dawn, tall straight trunks receding into cold blue mist, deep moss and fern over granite boulders, shafts of early light coming through the canopy, cold and silent, mist lying between the trunks. Small in the lower third of frame and seen from behind, lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair loose with natural flyaway strands, wearing a weathered waxed-canvas explorer's jacket in deep forest green over a cream cable-knit wool sweater, a worn leather satchel on a strap across her body and a small brass compass on a cord at her chest, walking away from camera up a narrow root-crossed trail. Enormous sense of scale, deep depth of field, layered atmospheric perspective. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The mist drifts slowly between the trunks, ferns stirring in a cold breeze, light shafts holding steady through the canopy. She walks slowly away up the trail and never turns back. Wind in pines, distant birds, no music.


#### s2 — Close-up — her breath in the cold, eyes on the way ahead

- **Note**: LoRA weight 1.0; input seed/lindsey.png; kept 7.0 s

*Still prompt*

> Tight close-up portrait, head and shoulders, straight on. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair loose with natural flyaway strands, wearing a weathered waxed-canvas explorer's jacket in deep forest green over a cream cable-knit wool sweater, a worn leather satchel on a strap across her body and a small brass compass on a cord at her chest with the cream wool collar high at her throat, facing the camera, cheeks and nose flushed with cold, her breath faintly visible in the air. an ancient pine forest on a steep mountainside at dawn, tall straight trunks receding into cold blue mist, deep moss and fern over granite boulders, shafts of early light coming through the canopy thrown far out of focus behind her, cold blue light with a warm rim from a low shaft of sun. Razor-sharp focus on the eyes, skin texture and individual eyelashes. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera, no push in. She faces the camera the whole time and does not turn her head. Her breath clouds faintly and fades, loose strands of hair move in the cold air, she blinks once. The light stays constant. Wind in pines, no music.


#### s3 — Macro — a brass compass and a folded map, no face in frame

- **Note**: LoRA weight 0.6; input seed/lindsey.png; kept 8.0 s

*Still prompt*

> Extreme close-up detail insert, no face in frame. Two small hands holding an old brass compass open above a folded linen map marked in faded ink, resting on the sleeve of a weathered waxed-canvas explorer's jacket in deep forest green over a cream cable-knit wool sweater, a worn leather satchel on a strap across her body and a small brass compass on a cord at her chest. The compass glass catching the cold dawn light, the needle settling, fine scratches on the brass, the weave of the linen and the wool visible. Macro clarity, very shallow depth of field. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked macro camera. The compass stays resting flat on the map the whole time and never lifts, floats or leaves the frame. Only the needle swings and settles under the glass, the map shifts a few millimetres under her thumb, her fingers relax. The fabric stays flat — nothing lifts, flaps or folds over. The light stays constant. Wind, no music.


#### s4 — Medium — she holds a branch aside and looks up at what she has found

- **Note**: LoRA weight 1.0; input seed/lindsey.png; kept 7.5 s

*Still prompt*

> Medium shot, waist up, straight on. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair loose with natural flyaway strands, wearing a weathered waxed-canvas explorer's jacket in deep forest green over a cream cable-knit wool sweater, a worn leather satchel on a strap across her body and a small brass compass on a cord at her chest, one hand raised holding a pine branch aside in front of her, chin lifted and eyes raised toward something above and past the camera, an expression of dawning recognition. an ancient pine forest on a steep mountainside at dawn, tall straight trunks receding into cold blue mist, deep moss and fern over granite boulders, shafts of early light coming through the canopy close behind her, cold light on her face. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera. Her raised hand lowers the branch and comes down; her chin lifts a fraction further and her eyes widen slightly as she looks up. She stays facing the camera throughout and never turns her head. The light stays constant. Wind in pines, no music.


#### s5 — The old stone stair climbing into the mist

- **Note**: no LoRA — no face in frame; input seed/stair.png; kept 8.0 s

*Still prompt*

> Wide shot, no people in frame. An ancient stone stair cut into the mountainside, worn treads under deep moss and pine roots, climbing steeply and disappearing into cold blue mist above, an ancient pine forest on a steep mountainside at dawn, tall straight trunks receding into cold blue mist, deep moss and fern over granite boulders, shafts of early light coming through the canopy crowding in on both sides, one shaft of dawn light falling across the lower steps. Strong upward perspective. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. Mist rolls slowly down over the upper steps, ferns and moss stirring in the draught, the shaft of light holding steady on the stone. The light stays constant. Wind, no music.


#### s6 — She climbs, seen from behind and below

- **Note**: LoRA weight 0.85; input seed/stair.png; kept 9.5 s

*Still prompt*

> Wide full-body shot from behind and below, looking up the stair. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair loose with natural flyaway strands, wearing a weathered waxed-canvas explorer's jacket in deep forest green over a cream cable-knit wool sweater, a worn leather satchel on a strap across her body and a small brass compass on a cord at her chest, seen from behind mid-stride climbing the mossy stone steps away from the camera toward the mist above, the satchel swinging at her hip, one hand on the rock wall. Strong upward perspective. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera. She climbs steadily away from the camera up the steps, the satchel swinging with her stride, mist rolling down past her. She never turns back. The light stays constant. Wind, footfalls on stone, no music.


#### s7 — The top — sunrise on her face

- **Note**: LoRA weight 1.0; input seed/lindsey.png; kept 7.5 s

*Still prompt*

> Close-up portrait, frontal, slightly low angle. lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair loose with natural flyaway strands, wearing a weathered waxed-canvas explorer's jacket in deep forest green over a cream cable-knit wool sweater, a worn leather satchel on a strap across her body and a small brass compass on a cord at her chest, facing the camera with a low gold sunrise full on her face, wind lifting her hair, lips slightly parted in astonishment, eyes bright. Behind her a ruined stone watchtower on a high clifftop, weathered blocks and a broken arch, standing above an endless sea of cloud with distant blue peaks breaking through it, lit by a low gold sunrise soft and luminous and far out of focus. Razor-sharp focus on the eyes and skin. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera. Her expression settles from astonishment into a slow smile; she blinks once, wind lifting her hair across her face and away again. She faces the camera throughout and never turns her head. The light stays constant. Wind, no music.


#### s8 — What she climbed for — small at the edge above a sea of cloud

- **Note**: LoRA weight 0.85; input seed/summit.png; kept 8.0 s

*Still prompt*

> Extreme wide final shot. a ruined stone watchtower on a high clifftop, weathered blocks and a broken arch, standing above an endless sea of cloud with distant blue peaks breaking through it, lit by a low gold sunrise. Very small at the cliff edge beside the broken arch and seen from behind, lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair loose with natural flyaway strands, wearing a weathered waxed-canvas explorer's jacket in deep forest green over a cream cable-knit wool sweater, a worn leather satchel on a strap across her body and a small brass compass on a cord at her chest, standing still and looking out over the cloud sea. Enormous sense of scale, deep depth of field, layered atmospheric perspective, the sun just clearing the far peaks. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wool and weathered canvas, natural dawn light, shallow depth of field, subtle film grain, muted natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The cloud sea moves slowly below, pouring over the far ridges, the light climbing steadily as the sun clears the peaks. Her hair and the hem of her jacket move in the wind. She stands still and never turns back. Wind, no music.

## Kyle — the signal fire {#kyle_lighthouse}

- **Date**: 2026-09-29 · **Status**: stopped 2026-09-29 — abandoned at Kevin's call after s6 could not be made to work. Seven of eight shots are rendered, graded and upscaled to 4K; s6 went through five designs (interior stairwell from below, side-on interior spiral, exterior stair on the tower, and two versions of the entrance door) and none was accepted. No final cut was produced from the current shot set. · **Version**: `v1-lora-cli` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: Fourth LoRA-driven film, and the first chosen for a subject whose motion animates itself — fire, surf and spray — so the long takes need nothing from the model that it can get wrong.
- **Files** (`projects/kyle_lighthouse/v1-lora-cli/`): `stills/s1.png … s8.png`, `clips/s1_v1.mov … s8_v1.mov (s2 uses v2)`, `final/kyle_lighthouse_3840x2160.mp4`, `final/kyle_lighthouse_1920x1080.mp4`, `music/best_adventure_ever.mp3`
- **Notes**: Kyle is Kevin's son; consent settled. Story written for this film: a boy carries a lantern out along a storm causeway to a dead lighthouse, climbs the tower, strikes a match and relights the lamp.

Subject chosen for the constraint, which is the new move here. Three films in, the rule is that LTX responds to what a shot is *of* and not to instructions about what not to do, so this film is built of things whose natural motion is already the motion wanted: a flame, a swinging lantern, surf, spray, a sweeping beam. That fixes the failure from lindsey_summit, where a held compass floated out of frame twice — s3 here hangs its object on a hook, so swinging *is* the intended behaviour.

The rest is inherited. Face shots (s2, s7) budgeted at 7.0-7.5 s. No shot asks for a head turn. s4 is the one shot with real human movement and it is hands cupped around a match in front of a stationary head, the pattern that has now held 9.5 s twice. Kyle's dataset is close-heavy with one full-body frame, so the wides (s1, s6) sit at 0.85 with the face small or turned away, and the two shots with no person (s5, s8) carry no LoRA. Cut order is s1 s2 s3 s6 s5 s4 s7 s8: the shot ids were written in story-beat order but the climb has to precede the lamp room, so the sequence was corrected before rendering the clips. s6 was replaced entirely. Three attempts at a staircase — looking up an interior stairwell, side-on to an interior spiral, and an exterior stair bolted to the tower — all failed on geometry: klein renders a stairwell as an ambiguous tapering wedge and LTX turns any climb on it into a figure drifting up a wall. Rather than keep fighting it the beat was changed to the boy stepping through the door at the foot of the tower, which is a back view walking away from camera into a dark opening: the one figure motion that has held its full length in every film so far. It also reads better in sequence, since the next shot is inside.

Stopped before delivery. What is on disk: stills and 1024x576 clips for all eight shots, 4K upscales for s1-s5, s7 and s8, and an earlier 59.76 s assembly that contains a rejected s6. If this is ever picked up again, the open problem is s6 alone.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |
| LoRA | kyle_lora_2000_lora_f32.ckpt @ per-shot weight (none / 0.6 / 0.85 / 1.0) |

Prompt: `per shot — see scenes`

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
| I2V time (min) | 11 |

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none — xfade 0.75 |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus -> 3840x2160 |
| Music | Best Adventure Ever — geoffharvey, Pixabay (cdn.pixabay.com/download/audio/2022/10/13/audio_f917a5a4fc.mp3), 2:33; tail-aligned so the track's climax lands on the lamp catching and the beam going out. Reused from kyle_rescue. |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *subject* — kyle_kx boy, a nine-year-old boy, this exact face, neat dark hair wet with spray
- *wardrobe* — a heavy oiled canvas coat in dark slate over a thick cream fisherman's wool sweater, a coil of rope over one shoulder and a battered brass storm lantern in his hand
- *coast* — a storm-battered granite headland at dusk, black wet rock and white surf exploding against it, a narrow stone causeway running out to a ruined lighthouse of weathered pale stone, low iron-grey cloud and spray hanging in the air
- *lamproom* — the lamp room at the top of a ruined lighthouse, a great cracked fresnel lens on its brass carriage, salt-clouded glass panes, rusted iron railings and a spiral stair coming up through the floor
- *style* — Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

#### s1 — Establishing — the causeway, the lighthouse, and how small he is

- **Note**: LoRA weight 0.85; input seed/coast.png; kept 9.0 s

*Still prompt*

> Extreme wide establishing shot. a storm-battered granite headland at dusk, black wet rock and white surf exploding against it, a narrow stone causeway running out to a ruined lighthouse of weathered pale stone, low iron-grey cloud and spray hanging in the air, the sea heaving and breaking white over the rocks. Very small in the lower third of frame and seen from behind, kyle_kx boy, a nine-year-old boy, this exact face, neat dark hair wet with spray, wearing a heavy oiled canvas coat in dark slate over a thick cream fisherman's wool sweater, a coil of rope over one shoulder and a battered brass storm lantern in his hand, walking away from camera out along the stone causeway toward the dark lighthouse. Enormous sense of scale, deep depth of field, layered atmospheric perspective. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. Heavy surf rolls in and bursts white against the causeway, spray blowing across in the wind, low cloud moving over the headland. He walks steadily away along the causeway. The light stays constant. Surf, wind, no music.


#### s2 — Close-up — salt spray on his face, the lighthouse ahead

- **Note**: LoRA weight 1.0; input seed/kyle.png; kept 7.0 s

*Still prompt*

> Tight close-up portrait, head and shoulders, straight on. kyle_kx boy, a nine-year-old boy, this exact face, neat dark hair wet with spray, wearing a heavy oiled canvas coat in dark slate over a thick cream fisherman's wool sweater, a coil of rope over one shoulder and a battered brass storm lantern in his hand with the wool collar turned up at his throat, facing the camera, skin damp with fine sea spray, an even natural skin tone, jaw set. a storm-battered granite headland at dusk, black wet rock and white surf exploding against it, a narrow stone causeway running out to a ruined lighthouse of weathered pale stone, low iron-grey cloud and spray hanging in the air thrown far out of focus behind him, cool even grey light with a faint warm glow from the lantern below frame. Razor-sharp focus on the eyes, damp skin texture and individual eyelashes. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera, no push in. He faces the camera, breathing hard, blinking against the spray; wind drags at his wet hair and the collar of his coat. The light stays constant. Surf, wind, no music.


#### s3 — Macro — the storm lantern swinging on its hook

- **Note**: LoRA weight 0.6; input seed/kyle.png; kept 7.0 s

*Still prompt*

> Extreme close-up detail insert, no face in frame. A battered brass storm lantern hanging from a rusted iron hook, its small flame burning steadily behind sooted glass, swinging gently, salt crust and old dents on the brass, rain beading and running down the panes, the dark wet wool of a heavy oiled canvas coat in dark slate over a thick cream fisherman's wool sweater, a coil of rope over one shoulder and a battered brass storm lantern in his hand just visible behind it. Macro clarity, very shallow depth of field, warm flame against cold grey. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked macro camera. The hanging lantern swings slowly on its hook, the flame leaning and steadying inside the glass, rain beading and running down the panes. The light stays constant. Wind, surf, no music.


#### s6 — He goes in — the door at the foot of the tower

- **Note**: LoRA weight 0.85; input seed/coast.png; the shoulder rope is dropped in this shot only — LTX kept elaborating it into a cable across the frame

*Still prompt*

> Medium-wide shot from behind and slightly low, looking at the foot of the ruined lighthouse. A heavy weathered timber door banded with rusted iron is set into the base of the pale stone tower and stands half open onto darkness inside, a worn stone step in front of it, wet black rock and puddles around it, salt-bleached stone and peeling paint. Nothing stands between the camera and the tower; the foreground is clear open wet rock. kyle_kx boy, a small nine-year-old boy with child proportions, this exact face, neat dark hair wet with spray, wearing only a heavy oiled canvas coat in dark slate over a thick cream fisherman's wool sweater, empty-handed except for a lit battered brass storm lantern in one hand, seen from behind, standing on the step with his other hand on the edge of the open door, about to step through into the dark interior, the lantern throwing warm light into the doorway and back onto the wet stone. Behind and around him the storm: iron-grey sky, low fast cloud, spray in the air, white surf on the rocks. Unmistakable scale of a small child against a tall heavy door. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The boy pushes the heavy door wide open and walks forward through the doorway into the dark interior of the tower, going away from the camera the whole time with his back to it, getting smaller as he recedes into the darkness, the warm glow of his lantern shrinking away inside the tower until only the doorway is lit. His coat and the rope drag in the wind, spray blows across the frame behind him, surf bursts white on the rocks, cloud tears past overhead. Wind, surf, the door scraping on stone, no music.


#### s5 — The dark lamp room and the great cracked lens

- **Note**: no LoRA — no face in frame; input seed/lamproom.png; kept 8.0 s

*Still prompt*

> Wide interior, no people in frame. the lamp room at the top of a ruined lighthouse, a great cracked fresnel lens on its brass carriage, salt-clouded glass panes, rusted iron railings and a spiral stair coming up through the floor, unlit and cold, the last grey daylight coming through the salt-clouded panes and breaking into rings inside the great fresnel lens, rust and old paint, the dark sea visible beyond the glass. Deep depth of field, still and derelict. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The grey sea heaves and rolls far below beyond the clear glass, fine dust drifting slowly through the still air of the room, faint reflections turning inside the cracked lens. The panes are dry. The light stays constant. Muffled surf, wind, no music.


#### s4 — He strikes a match and shields the flame in both hands

- **Note**: LoRA weight 1.0; input seed/kyle.png; kept 9.5 s

*Still prompt*

> Medium close-up, chest up, straight on. kyle_kx boy, a nine-year-old boy, this exact face, neat dark hair wet with spray, wearing a heavy oiled canvas coat in dark slate over a thick cream fisherman's wool sweater, a coil of rope over one shoulder and a battered brass storm lantern in his hand, both hands raised and cupped in front of his chest around a freshly struck match, the small flame lighting his face warm from below, eyes down on the flame in concentration. the lamp room at the top of a ruined lighthouse, a great cracked fresnel lens on its brass carriage, salt-clouded glass panes, rusted iron railings and a spiral stair coming up through the floor dark around him. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera. His cupped hands close a little tighter around the match flame, which leans and steadies and throws moving warm light up across his face; his eyes stay down on it and then lift to the lens. He stays facing the camera throughout. Surf muffled through glass, wind, no music.


#### s7 — The lamp catches — warm light floods his face

- **Note**: LoRA weight 1.0; input seed/kyle.png; kept 7.5 s

*Still prompt*

> Close-up portrait, frontal, slightly low angle. kyle_kx boy, a nine-year-old boy, this exact face, neat dark hair wet with spray, wearing a heavy oiled canvas coat in dark slate over a thick cream fisherman's wool sweater, a coil of rope over one shoulder and a battered brass storm lantern in his hand, facing the camera with the newly lit lighthouse lamp blazing warm gold from just off frame, the light full on his face, eyes bright and reflecting the flame, the beginning of a smile. the lamp room at the top of a ruined lighthouse, a great cracked fresnel lens on its brass carriage, salt-clouded glass panes, rusted iron railings and a spiral stair coming up through the floor warm and luminous behind him. Razor-sharp focus on the eyes and skin. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Locked camera. The warm light on his face strengthens and steadies; his eyes widen a fraction and the small smile settles, he blinks once. He faces the camera throughout. Muffled surf, no music.


#### s8 — The beam goes out across the water

- **Note**: no LoRA — no face in frame; input seed/coast.png; kept 8.5 s

*Still prompt*

> Extreme wide final shot, no people in frame, from far out on the dark water looking back. a storm-battered granite headland at dusk, black wet rock and white surf exploding against it, a narrow stone causeway running out to a ruined lighthouse of weathered pale stone, low iron-grey cloud and spray hanging in the air at last light, the ruined lighthouse standing black against the storm sky with its lamp lit — a single hot gold beam reaching out across the heaving sea and through the spray, surf still bursting white on the rocks below. Enormous sense of scale, deep depth of field. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, wet wool and oiled canvas, natural storm light at dusk, shallow depth of field, subtle film grain, cold desaturated colour with warm firelight. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark, no extra people beyond those described.

*Video prompt*

> Fixed camera, no camera movement. The lighthouse lamp rotates steadily like a real lighthouse: the shaft of the beam swings around through the spray, passes across the camera, sweeps on out over the water and comes around again, over and over. Beneath the camera a heavy swell rolls and heaves, big waves surging in and bursting white against the black rocks, spray blowing across the causeway, storm cloud moving fast overhead. Surf, wind, no music.

## Lindsey: Clifftop Orbit {#lindsey_orbit}

- **Date**: 2026-10-08 · **Status**: rendering · **Version**: `v2-cliff` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: v2-cliff

**Versions**

| Version | What it is | Status | YouTube |
|---|---|---|---|
| `v1-drone` | v1-drone | rendering | — |
| `v2-cliff` | v2-cliff | rendering | — |

- **Files** (`projects/lindsey_orbit/v2-cliff/`): 
- **Notes**: v1 established that LTX-2.3 cannot hold a locked-distance orbit -- it pulled back 6.9x on two different prompts -- while Wan 2.2 held the subject to a 1.6x change. v2 uses Wan at 161 frames (4k+1) for the full 10 s at 16 fps. The motion prompt describes camera and motion only, per wan22-i2v-locked-image-settings.

**Still**

| Setting | Value |
|---|---|
| Model | flux_2_klein_9b_i8x.ckpt |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1 |
| Shift | 3.0 |
| Sampler | 16 |
| LoRA | lindsey_lora_2000_lora_f32.ckpt |

**I2V**

| Setting | Value |
|---|---|
| Model | wan_v2.2_a14b_hne_i2v_i8x.ckpt |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S) @ 10% |
| LoRA | Wan 2.2 A14B Lightning High-Noise T2V v2.0 @ 100% |
| Size | 576x1024 |
| Frames | 161 |
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
| Upscale | Real-ESRGAN 4K |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *subject* — lindsey_kx girl, a nine-year-old girl, this exact face, long dark hair loose with natural flyaway strands, wearing a simple pale sun-faded cotton dress
- *style* — Cinematic aerial film still, photoreal skin and natural fabric, late golden-hour sunlight, visible film grain. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.
## Kyle — character LoRA v2 {#kyle_lora}

- **Date**: 2026-09-29 · **Status**: dataset built 2026-09-29 — 55 pairs; training · **Version**: `v2-photo-dataset` · **Draw Things project**: `none — draw-things-cli train lora`
- **This version**: Second Kyle dataset, built to break the close-up/white-wall/blue-t-shirt correlation that caps v1 at close framing.

**Versions**

| Version | What it is | Status | YouTube |
|---|---|---|---|
| `v1-photo-dataset` | Character LoRA for Kyle trained on real photographs, following the Ivy route. The output is a reusable identity asset: kyle_rescue, bot_builders_champion and nightelf_hunter all carried his face by reference tokens and a master portrait, which this replaces with a trigger token. | delivered 2026-09-26 — kyle_lora_2000_lora_f32.ckpt, usable at weight 1.0 including true profile and back of head | — |
| `v2-photo-dataset` | Second Kyle dataset, built to break the close-up/white-wall/blue-t-shirt correlation that caps v1 at close framing. | dataset built 2026-09-29 — 55 pairs; training | — |

- **Files** (`projects/kyle_lora/v2-photo-dataset/`): `raw/ (git-ignored)`, `seed/dataset/NN.png + NN.txt`, `logs/train.log`
- **Notes**: Kyle is Kevin's son; consent settled. v1 delivered a LoRA that holds identity at close range and at every head angle including true profile and back, and that is genuinely good. What it cannot do is hold a child's face and proportions at medium or full-body distance — confirmed on kyle_debut and again on kyle_lighthouse, where wide shots had to be composed with the face small or turned away.

The cause is visible in v1's own captions. Sixteen of its twenty frames are close-ups, and they are the *same* sixteen that are on a white textured wall in a pale blue t-shirt under flat indoor light. Framing, background, wardrobe and lighting are therefore all correlated with each other and with the trigger, so the model has one dominant mode to fall back on and nothing to generalise from at distance.

v2 keeps all twenty v1 frames — the close-range identity they give is the part that works — and adds frames chosen so that **every new frame differs from that block in at least two of framing, background, lighting and wardrobe**. Breaking the correlation matters as much as adding full-body coverage; adding twenty more full-body frames on the same white wall would just move the problem.

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

## Tide {#tide}

- **Date**: 2026-10-08 · **Status**: rendering · **Version**: `v1-wan` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: v1-wan
- **Files** (`projects/tide/v1-wan/`): 
- **Notes**: Deliberately has no recurring character or object. Every consistency failure in this repo has come from holding a subject across cuts; a landscape film removes that axis entirely, so each still stands alone and only the grade has to carry continuity. Wan 2.2 I2V throughout -- LTX is not used, having been measured adding a 6.9x pull-back on a locked-camera shot. 6 x 81 frames at 16 fps, hard cuts, 30.0 s.

**Still**

| Setting | Value |
|---|---|
| Model | flux_2_klein_9b_i8x.ckpt |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1 |
| Shift | 3.0 |
| Sampler | 16 |

**I2V**

| Setting | Value |
|---|---|
| Model | wan_v2.2_a14b_hne_i2v_i8x.ckpt |
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
| Upscale | Real-ESRGAN 4K |
| Music | Calm Ambient Dreamscape — morgan-ambient, Pixabay, 1 s fade in / 2 s fade out, vol 0.9 |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *style* — Cinematic film still, anamorphic 35mm on film stock, photoreal water and wet rock, visible film grain. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.
## Yang family — one LoRA, three subjects {#yang_family_lora}

- **Date**: 2026-09-30 · **Status**: delivered 2026-09-30 — yang_family_lora_4000_lora_f32.ckpt, 9 h 22 m, 5 checkpoints at 843 MB each · **Version**: `v1-multi-subject` · **Draw Things project**: `none — draw-things-cli train lora`
- **This version**: First multi-subject LoRA: three people in one adapter, each behind its own trigger and class word.
- **Files** (`projects/yang_family_lora/v1-multi-subject/`): `seed/dataset/NNN.png + NNN.txt (87 pairs)`, `logs/train.log`
- **Notes**: Kyle, Lindsey and Ivy are Kevin's family; consent settled for all three. The point of a single adapter is that it can put two of them in one frame, which three separate LoRAs cannot do — Draw Things can load more than one LoRA, but two character adapters fight for the same face.

The setup is unusually favourable: all three datasets already lead every caption with a distinct trigger AND a distinct class word — kyle_kx boy, lindsey_kx girl, ivy_kx woman. That gives the model two independent axes to separate the subjects on, which is the main defence against the failure mode here, identity bleed.

Kyle was capped at 33 of his 55 v2 frames so that no subject dominates: 33 / 32 / 22 rather than 55 / 32 / 22. His full-body coverage was kept whole because that is what v2 was built for, the medium band was mostly kept, and the close-ups were thinned, since he had the most and close identity is the easiest thing for a LoRA to learn. kyle_lora v2 stays on disk for Kyle-only work, so nothing is lost by the cap.

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

## Yang family LoRA — made to work in ComfyUI {#yang_family_lora_comfy}

- **Date**: 2026-10-02 · **Status**: in progress — source analysed and the mapping derived; converter not yet written · **Version**: `v1-ckpt-convert` · **Draw Things project**: `none — offline conversion`
- **This version**: Convert the trained Draw Things family LoRA to safetensors rather than retrain it, because FLUX.2 klein LoRA training does not work on Apple Silicon.
- **Files** (`projects/yang_family_lora_comfy/v1-ckpt-convert/`): `seed/yang_family_lora_4000.safetensors (output, git-ignored)`, `logs/convert.log`
- **Notes**: Kyle, Lindsey and Ivy are Kevin's family; consent settled. No raw photographs are involved at any point here — the input is the trained adapter, not the dataset, which is one more reason to prefer conversion over retraining on a rented machine.

Training the equivalent LoRA natively for ComfyUI is blocked, checked 2026-10-02: Fizgig supports klein 9B but is Windows/Linux with NVIDIA or AMD only; ai-toolkit's Apple Silicon issue is closed as not planned after six non-converging configurations (NaN loss with cached text embeddings, OOM on fp16 despite gradient checkpointing, loss oscillating 0.45-0.56); musubi-tuner has an open klein 9B error. Converting the existing adapter reuses the 9 h 22 m already spent and runs entirely locally.

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

## Kyle — where the ground breathes {#kyle_steamfield}

- **Date**: 2026-10-03 · **Status**: clips QC’d 2026-10-03 — 60.41 s planned, finishing · **Version**: `v1-lora-cli` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: Fourth LoRA-driven film, built to the same shot grammar as lindsey_summit but on the standalone kyle_lora v2.
- **Files** (`projects/kyle_steamfield/v1-lora-cli/`): `seed/*.png (masters)`, `stills/<id>.png`, `clips/<id>.mp4`, `final/`
- **Notes**: Kyle is Kevin's son; consent settled. Story written for this film: a boy crosses a black volcanic plain at first light, finds a hot spring in the lava, climbs a ridge of broken basalt and comes out above a whole valley full of steam at sunrise.

Every structural choice is inherited from the three films before it rather than guessed. Face shots (s2, s4, s7) are locked frontal at weight 1.0 and budgeted at 7.0-7.5 s, because frontal face clips drift at about eight seconds whatever the motion prompt says. The long takes go to the three things that have held their full length every time: walking away from camera (s1, s6), a macro insert with no face (s3), and pure landscape (s5). s4 is the one shot asking a person for real movement, and it is hand movement in front of a stationary head — the pattern that survived 9.9 s on kyle_debut.

The setting is chosen for the same reason: steam is natural, continuous motion, so the long takes get their movement from the environment rather than from the subject. Palette is deliberately opposite to lindsey_summit — black basalt, white steam and sulfur yellow instead of blue pine and gold.

The wardrobe carries no strap, cord or satchel on purpose. On kyle_lighthouse a shoulder rope invented in the wardrobe lock was elaborated by LTX into a cable across the frame, and the project was stopped over it.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |
| LoRA | kyle_lora_v2_2500_lora_f32.ckpt @ per-shot weight (none / 0.6 / 0.85 / 1.0) |

Prompt: `per shot — see scenes`

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
| I2V time (min) | 11 |

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none — xfade 0.75 |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus -> 3840x2160 |
| Music | light_adventure.mp3 under the LTX ambience at 0.45, 1.5 s in, 2 s out. NOTE: music belongs at run-spec.music, NOT run-spec.assemble.music — film_run.py reads the top-level key and silently ignores a nested one, producing a film with clip audio only and no error. |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *subject* — kyle_kx boy, a nine-year-old boy with child proportions, this exact face, short dark hair
- *wardrobe* — a weathered burnt-orange hooded shell jacket over a charcoal fleece, dark trousers and scuffed hiking boots
- *plain* — a vast black volcanic plain at first light, broken basalt and old lava flows under a thin dusting of frost, columns of white steam rising from fissures in the ground, distant snow ridges on the horizon, a huge pale sky going from deep blue to cold gold
- *spring* — a hot spring pool of impossibly clear blue-green water set in black lava rock, its rim crusted in bright sulfur yellow and rust orange, heavy white steam pouring off the surface
- *valley* — a vast steaming valley seen from a high black ridge, dozens of steam columns rising from the floor and leaning together in the wind, a river of meltwater threading between them, low gold sunrise breaking across the whole basin
- *style* — Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

#### s1 — Establishing — the steaming plain at first light, he is small on it

- **Note**: LoRA weight 0.85; input seed/plain.png; kept 9.5 s

*Still prompt*

> Extreme wide establishing shot. a vast black volcanic plain at first light, broken basalt and old lava flows under a thin dusting of frost, columns of white steam rising from fissures in the ground, distant snow ridges on the horizon, a huge pale sky going from deep blue to cold gold. Small in the lower third of frame and seen from behind, one person alone in the frame: kyle_kx boy, a nine-year-old boy with child proportions, this exact face, short dark hair, wearing a weathered burnt-orange hooded shell jacket over a charcoal fleece, dark trousers and scuffed hiking boots, walking away from camera along a faint track between the steam columns. Enormous sense of scale, deep depth of field, layered atmospheric perspective. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. The steam columns drift and lean slowly in the wind, thin ground mist moving across the basalt. He walks steadily away and never turns back. The light stays constant. Wind over open ground, no music.


#### s2 — Close-up — cold morning air, eyes on the way ahead

- **Note**: LoRA weight 1.0; input seed/kyle.png; kept 7.0 s

*Still prompt*

> Tight close-up portrait, head and shoulders, straight on, one person alone in the frame. kyle_kx boy, a nine-year-old boy with child proportions, this exact face, short dark hair, wearing a weathered burnt-orange hooded shell jacket over a charcoal fleece, dark trousers and scuffed hiking boots with the hood down and the fleece collar high at his throat, facing the camera, an even natural skin tone, his breath faintly visible in the cold air. a vast black volcanic plain at first light, broken basalt and old lava flows under a thin dusting of frost, columns of white steam rising from fissures in the ground, distant snow ridges on the horizon, a huge pale sky going from deep blue to cold gold thrown far out of focus behind him, cold blue light with a warm rim from the low sun. The face is well exposed and clearly visible. Razor-sharp focus on the eyes and skin texture. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Locked camera, no push in. He faces the camera the whole time and his head stays still. His breath clouds faintly and fades, a few strands of hair move in the cold air, he blinks once. The light stays constant. Wind, no music.


#### s3 — Macro — a piece of obsidian turned in two hands, no face in frame

- **Note**: LoRA weight 0.6; input seed/kyle.png; kept 8.0 s

*Still prompt*

> Extreme close-up detail insert, no face in frame. Two small child's hands holding a shard of black volcanic glass up against the cold morning light, its edges catching the sun, resting over the cuff of a weathered burnt-orange hooded shell jacket over a charcoal fleece, dark trousers and scuffed hiking boots. Fine dust on the skin, the conchoidal ripples in the glass, a wisp of steam crossing behind. Macro clarity, very shallow depth of field. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Locked macro camera. The shard stays held in his hands the whole time and never lifts, floats or leaves the frame. His thumb turns it a few degrees and settles, the fingers relax. A thin wisp of steam drifts across behind. The light stays constant. Wind, no music.


#### s4 — Travelling — full body in profile, walking the plain

- **Note**: LoRA weight 0.85; input seed/plain.png; kept 7.5 s

*Still prompt*

> Full-body shot from the side, one person alone in the frame, filling about half the frame height. kyle_kx boy, a nine-year-old boy with child proportions, this exact face, short dark hair, wearing a weathered burnt-orange hooded shell jacket over a charcoal fleece, dark trousers and scuffed hiking boots, seen in profile walking steadily from left to right across the frame, mid-stride with one boot lifted, arms swinging naturally at his sides, looking ahead along his path. He walks across bare black basalt and the ground in front of him is clear and open. Tall columns of white steam rise well behind him and out to both sides, bright against the sky. a vast black volcanic plain at first light, broken basalt and old lava flows under a thin dusting of frost, columns of white steam rising from fissures in the ground, distant snow ridges on the horizon, a huge pale sky going from deep blue to cold gold behind him, distant snow ridges on the horizon. Clean dry air between the camera and the boy. Strong side-on composition, the whole body visible from boots to head. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. He walks steadily in profile from left to right across the frame at a constant pace, boots landing on the black rock, arms swinging, looking ahead the whole time. The steam columns behind him rise and lean slowly in the wind. The air between the camera and the boy stays clear. The light stays constant. Wind over open ground, boots on stone, no music.


#### s5 — The hot spring — blue-green water in a sulfur rim, no people in frame

- **Note**: no LoRA — no face in frame; input seed/spring.png; kept 8.0 s

*Still prompt*

> Wide shot, no people in frame. a hot spring pool of impossibly clear blue-green water set in black lava rock, its rim crusted in bright sulfur yellow and rust orange, heavy white steam pouring off the surface, the black rock wet and shining around it, a few frost-rimed tufts of moss at the edge, the pool so clear the ledges are visible far down into it. Strong colour contrast between the yellow rim, the blue water and the black rock. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. Heavy steam pours continuously off the surface of the pool and rolls away low across the rock, the water turning slowly with faint convection rings. The light stays constant. Water and wind, no music.


#### s6 — He climbs the black ridge, seen from behind and below

- **Note**: LoRA weight 0.85; input seed/plain.png; kept 9.5 s

*Still prompt*

> Wide full-body shot from behind and below, looking up a slope of broken black lava rock. One person alone in the frame: kyle_kx boy, a nine-year-old boy with child proportions, this exact face, short dark hair, wearing a weathered burnt-orange hooded shell jacket over a charcoal fleece, dark trousers and scuffed hiking boots, seen from behind mid-stride climbing the loose dark boulders away from the camera toward a bank of steam above, one hand down on the rock for balance. The foreground rock is clear and unobstructed. Strong upward perspective. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera. He climbs steadily away from the camera over the rock, steam rolling down past him from above. He never turns back. The light stays constant. Wind, boots on loose stone, no music.


#### s7 — The top — sunrise full on his face

- **Note**: LoRA weight 1.0; input seed/kyle.png; kept 7.5 s

*Still prompt*

> Close-up portrait, frontal, slightly low angle, one person alone in the frame. kyle_kx boy, a nine-year-old boy with child proportions, this exact face, short dark hair, wearing a weathered burnt-orange hooded shell jacket over a charcoal fleece, dark trousers and scuffed hiking boots, facing the camera with a low gold sunrise full on his face lighting it clearly and brightly, wind lifting his hair, lips slightly parted in astonishment, eyes bright. Behind him a vast steaming valley seen from a high black ridge, dozens of steam columns rising from the floor and leaning together in the wind, a river of meltwater threading between them, low gold sunrise breaking across the whole basin, soft and luminous and far out of focus. The face is well exposed and clearly visible. Razor-sharp focus on the eyes and skin texture. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Locked camera. His expression settles from astonishment into a slow smile; he blinks once, wind lifting his hair across his face and away again. He faces the camera throughout and his head stays still. Steam drifts far behind him. The light stays constant. Wind, no music.


#### s8 — What he climbed for — small on the ridge above a valley full of steam

- **Note**: LoRA weight 0.85; input seed/valley.png; kept 8.0 s

*Still prompt*

> Extreme wide final shot. a vast steaming valley seen from a high black ridge, dozens of steam columns rising from the floor and leaning together in the wind, a river of meltwater threading between them, low gold sunrise breaking across the whole basin. Very small at the ridge edge and seen from behind, one person alone in the frame: kyle_kx boy, a nine-year-old boy with child proportions, this exact face, short dark hair, wearing a weathered burnt-orange hooded shell jacket over a charcoal fleece, dark trousers and scuffed hiking boots, standing still and looking out over the steaming basin. Enormous sense of scale, deep depth of field, layered atmospheric perspective. Cinematic film still from a live-action adventure film, anamorphic 35mm, photoreal skin, technical fabric and wet volcanic rock, natural dawn light, shallow depth of field, subtle film grain, cool natural colour with warm sunrise accents. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. The steam columns rise and lean steadily across the whole valley, the meltwater river catching the light, the sunrise climbing visibly brighter as the sun clears the far ridge. His hair and the hem of his jacket move in the wind. He stands still and never turns back. Wind, no music.

## Lindsey — the eighth try {#lindsey_sparky}

- **Date**: 2026-10-03 · **Status**: delivered · **Version**: `v1-lora-cli` · **Draw Things project**: `none — draw-things-cli via scripts/film_run.py`
- **This version**: First interior film, and the first written against a supplied story. Also the first where every motion prompt forbids slow motion explicitly.
- **Files** (`projects/lindsey_sparky/v1-lora-cli/`): `final/lindsey_sparky_3840x2160.mp4`, `final/lindsey_sparky_1920x1080.mp4`, `spec.json`, `../plan/lindsey-sparky-plan.md`
- **Notes**: Lindsey is Kevin's daughter; consent settled. Story supplied: an eight-year-old inventor's homemade robot fails for the seventh time, she finds a reversed connection in her own wiring diagram, and the eighth attempt works.

This is the first interior, which removes the thing the last four films leaned on. Pine mist, surf, firelight and steam all gave the long takes continuous natural motion for free. A bedroom gives none, so the motion has to come from the subject and the robot. Three shots are built around things that move on their own anyway — smoke from the failed shoulder joint (s3), the robot's own mechanism (s2, s8) — and the long takes are given to those rather than to the face.

Face shots (s4, s7) are locked frontal at 7.0-7.5 s as always. s6 is the hands-in-front-of-a-stationary-head pattern that has held 9 s or more on every film it has been used in.

Every motion prompt ends with an explicit real-time instruction, because 'slowly' appeared four times in kyle_steamfield's motion prompts and the result read as slow motion. The word does not appear anywhere in this spec. Delivered 60.56 s (planned 60.45). Mean −21.9 dB, peak −4.9 dB, music continuous across the minute. Four of eight clips needed a second take; s5 never held and was cut to 3.4 s, with the seconds taken from the five shots that hold all 249 frames. Kept as-is: Sparky's visor cycles blue–green during s6, which reads as a display flickering while the joint is worked on.

**Still**

| Setting | Value |
|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) |
| Size | 1024x576 |
| Steps | 4 |
| CFG | 1.0 |
| Shift | 3 |
| Sampler | DDIM Trailing |
| LoRA | lindsey_lora_2000_lora_f32.ckpt @ per-shot weight (none / 0.6 / 0.85 / 1.0) |

Prompt: `per shot — see scenes`

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
| I2V time (min) | 11 |

**Post**

| Setting | Value |
|---|---|
| Script | scripts/finish_clip.sh |
| Loop | none — xfade 0.75 |
| Upscale | scripts/upscale_4k.sh — Real-ESRGAN x4plus -> 3840x2160 |
| Music | emotional_children_piano.mp3 at 0.45 under the clip audio. NOTE: music belongs at run-spec.music, NOT run-spec.assemble.music — film_run.py reads the top-level key and silently ignores a nested one. |

### Scene prompts

**Locks** (paste verbatim into every prompt):

- *subject* — lindsey_kx girl, an eight-year-old girl with child proportions, this exact face, long dark hair loose with natural flyaway strands
- *wardrobe* — a mustard-yellow hoodie over a white t-shirt, sleeves pushed up to the elbows, and a pair of clear safety goggles pushed up on top of her head
- *room* — a child inventor's bedroom at night, hand-drawn blueprints taped across the walls, loose wires and brass gears over a scarred wooden desk, jars of screws and bolts, a bright articulated desk lamp throwing a warm pool of light across the desk and leaving the rest of the room in soft blue shadow
- *robot* — Sparky, a foot-tall homemade robot built from recycled aluminium cans and salvaged toy motors, visible rivets and mismatched panels, a wide LED visor across its face, two simple jointed arms and small rubber treads
- *style* — Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.
- *pace* — Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping.

#### s1 — Establishing — the workshop bedroom, her back to us at the desk

- **Note**: LoRA weight 0.85; input seed/room.png; kept 9.0 s. picked c4.

*Still prompt*

> Wide establishing shot. a child inventor's bedroom at night, hand-drawn blueprints taped across the walls, loose wires and brass gears over a scarred wooden desk, jars of screws and bolts, a bright articulated desk lamp throwing a warm pool of light across the desk and leaving the rest of the room in soft blue shadow. Seen from behind and slightly above, one person alone in the frame: lindsey_kx girl, an eight-year-old girl with child proportions, this exact face, long dark hair loose with natural flyaway strands, wearing a mustard-yellow hoodie over a white t-shirt, sleeves pushed up to the elbows, and a pair of clear safety goggles pushed up on top of her head, sitting at the desk on a wooden chair with her shoulders hunched over her work. On the desk in front of her stands Sparky, a foot-tall homemade robot built from recycled aluminium cans and salvaged toy motors, visible rivets and mismatched panels, a wide LED visor across its face, two simple jointed arms and small rubber treads. The foreground is clear. Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. She stays seated in the chair the whole time, her back against the chair back and her weight settled. Only her right hand moves: it reaches a few inches across the desk, turns a small brass part over, and comes to rest again. Her head stays level and her shoulders stay where they are. The lamp light stays constant and the room behind her is still. Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping. Room tone, no music.


#### s2 — Macro — Sparky's visor comes up, no people in frame

- **Note**: no LoRA — no face in frame; input seed/bot.png; kept 7.0 s. picked c1.

*Still prompt*

> Extreme close-up detail insert, no people in frame. Sparky, a foot-tall homemade robot built from recycled aluminium cans and salvaged toy motors, visible rivets and mismatched panels, a wide LED visor across its face, two simple jointed arms and small rubber treads, framed tight on its head and shoulders, the LED visor lit a hard bright blue, a small fan spinning behind a grille in its chest, brass gears and exposed wiring at the shoulder joint. Warm lamp light raking across the scratched aluminium. Macro clarity, very shallow depth of field. Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Locked macro camera. The visor brightens to a steady blue and the small chest fan spins up to full speed, the shoulder gears turning a quarter turn and stopping. The robot stays where it is on the desk the whole time. Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping. A motor whirring, no music.


#### s3 — The seventh failure — smoke and scattered bolts, no people in frame

- **Note**: no LoRA — no face in frame; input seed/bot.png; kept 9.0 s. picked c5.

*Still prompt*

> Medium close shot of the desktop, no people in frame. Sparky, a foot-tall homemade robot built from recycled aluminium cans and salvaged toy motors, visible rivets and mismatched panels, a wide LED visor across its face, two simple jointed arms and small rubber treads slumped forward onto the scarred wooden desk with one arm folded under it, a thin plume of grey smoke rising from its left shoulder joint, bolts and a small spring scattered across the wood around it. The desk lamp throws a hard warm pool of light over the wreck. Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. The plume of smoke rises from the shoulder joint and curls away through the lamp light, thinning as it goes. One loose bolt rocks to a stop on the desk. The robot stays slumped where it is. The lamp light stays constant. Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping. A faint hiss, no music.


#### s4 — Close-up — the seventh failure on her face

- **Note**: LoRA weight 1.0; input seed/lindsey.png; kept 7.0 s. picked c5.

*Still prompt*

> Tight close-up portrait, head and shoulders, straight on, one person alone in the frame. lindsey_kx girl, an eight-year-old girl with child proportions, this exact face, long dark hair loose with natural flyaway strands, wearing a mustard-yellow hoodie over a white t-shirt, sleeves pushed up to the elbows, and a pair of clear safety goggles pushed up on top of her head, facing the camera with her chin low and her mouth set, an even natural skin tone, warm lamp light from one side and cool blue shadow on the other. a child inventor's bedroom at night, hand-drawn blueprints taped across the walls, loose wires and brass gears over a scarred wooden desk, jars of screws and bolts, a bright articulated desk lamp throwing a warm pool of light across the desk and leaving the rest of the room in soft blue shadow thrown far out of focus behind her. Clean clear air between the camera and her face. The face is well exposed and clearly visible. Razor-sharp focus on the eyes and skin texture. Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Locked camera, no push in. She faces the camera the whole time and her head stays still. She breathes out hard, blinks twice, and her jaw tightens. A few strands of hair settle. The light stays constant. Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping. Room tone, no music.


#### s5 — Macro — her finger traces the wiring diagram and finds the mistake, no face in frame

- **Note**: LoRA weight 0.6; input seed/desk.png; kept 8.0 s. picked c4.

*Still prompt*

> Extreme close-up detail insert, no face in frame. One small child's hand with a pencil held loosely, the index finger resting on a hand-drawn wiring diagram in an open spiral notebook, the paper covered in pencil lines and crossings-out. Beside the notebook on the desk corner is a strip of masking tape. Warm lamp light across the paper, the grain of the wood beyond. Macro clarity, very shallow depth of field. Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. Her wrist is bare and the hoodie sleeve stays pushed up above it. The pencil tip moves slowly along one drawn line on the page and stops. The hand stays a small child's hand, resting on the paper, and does not leave the frame. The paper and the desk stay still. Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping. Pencil on paper, no music.


#### s6 — Medium — hands working, the repair

- **Note**: LoRA weight 1.0; input seed/lindsey.png; kept 9.0 s. v2: v1 failed all five seeds -- hands merged into the robot because the prompt required the screwdriver to go INTO the shoulder joint. v2 holds the tool in open air and puts Sparky lower and clear of the hand. picked c3.

*Still prompt*

> Medium shot, chest up, straight on, one person alone in the frame. lindsey_kx girl, an eight-year-old girl with child proportions, this exact face, long dark hair loose with natural flyaway strands, wearing a mustard-yellow hoodie over a white t-shirt, sleeves pushed up to the elbows, and a pair of clear safety goggles pushed up on top of her head, leaning in over the desk. Her head is level and steady, her chin slightly down, her eyes lowered to the desk in front of her. She holds a small screwdriver in her right hand, raised just above the desk, the tool held in open air with clear space all around it. Her fingers are fully visible, closed around the handle, and do not touch or overlap anything else. Her left forearm rests flat along the near edge of the desk. Standing on the desk in the lower right of frame, well below her hand and separate from it, is Sparky, a foot-tall homemade robot built from recycled aluminium cans, a plain upright can-shaped silver body, a single wide LED visor lit blue across the front of his head, two simple jointed arms down at his sides and small rubber treads below. Sparky is whole and undamaged, his panels flat and unbent, his silhouette clean and unbroken against the desk. Nothing overlaps him. Behind her, a child inventor's bedroom at night, hand-drawn blueprints taped across the wall, jars of screws and bolts and loose brass gears along the far side of the desk, a bright articulated desk lamp off to one side throwing a warm pool of light, the rest of the room in soft blue shadow, all thrown well out of focus. The desk immediately in front of her is clear bare wood. Warm lamp light full on her face and her raised hand. Clean clear air between the camera and her. The face is well exposed and clearly visible. Razor-sharp focus on the eyes and skin texture. Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. The desk beside Sparky stays bare wood with nothing else on it. Sparky stands still and the blue light of his visor brightens and dims slowly and steadily throughout. She holds the screwdriver up in her right hand and turns it a few times in place, her left forearm flat on the desk. Her head stays level and her eyes stay down on the work. Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping. A screwdriver on metal, no music.


#### s7 — Close-up — it works, and it lands on her face

- **Note**: LoRA weight 1.0; input seed/lindsey.png; kept 7.5 s. picked c4. v2: v1's open laugh aged her into a young woman by frame 40 (1.6 s); the expression now peaks in the first second and then holds.

*Still prompt*

> Close-up portrait, frontal, slightly low angle, one person alone in the frame. lindsey_kx girl, an eight-year-old girl with child proportions, this exact face, long dark hair loose with natural flyaway strands, wearing a mustard-yellow hoodie over a white t-shirt, sleeves pushed up to the elbows, and a pair of clear safety goggles pushed up on top of her head with the goggles pushed up on her head, facing the camera with her eyes wide and her mouth beginning to open in delight, a hard blue LED glow from below and in front lighting her face brightly along with the warm lamp. a child inventor's bedroom at night, hand-drawn blueprints taped across the walls, loose wires and brass gears over a scarred wooden desk, jars of screws and bolts, a bright articulated desk lamp throwing a warm pool of light across the desk and leaving the rest of the room in soft blue shadow soft and far out of focus behind her. Clean clear air between the camera and her face. The face is well exposed and clearly visible. Razor-sharp focus on the eyes and skin texture. Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. Her eyes widen and her mouth opens into a small smile over the first second, and then the smile settles and holds steady for the rest of the shot without growing. Her head stays level and still and her chin does not lift. Her face stays the same face throughout. The blue glow on her face and the warm lamp both stay constant. Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping. Room tone, no music.


#### s8 — Sparky works — rolling forward and picking up the washer, no people in frame

- **Note**: no LoRA — no face in frame; input seed/bot.png; kept 9.0 s. picked c3.

*Still prompt*

> Medium close shot along the desktop at desk height, no people in frame. Sparky, a foot-tall homemade robot built from recycled aluminium cans and salvaged toy motors, visible rivets and mismatched panels, a wide LED visor across its face, two simple jointed arms and small rubber treads upright and square on the wood with its visor lit a solid bright blue, one jointed arm extended forward and down toward a small steel washer lying on the desk a few inches in front of it. The desk surface ahead of the robot is clear and open. Warm lamp light along the wood, the room soft and blue behind. Cinematic film still from a live-action family film, anamorphic 35mm, photoreal skin, cotton and scuffed metal, practical warm lamp light against cool blue shadow, shallow depth of field, subtle film grain, natural colour. Photorealistic, no cartoon or illustration styling, no text, no lettering, no logos, no watermark.

*Video prompt*

> Fixed camera, no camera movement. The robot's treads turn and it rolls forward a few inches across the desk, stops square, and its extended arm lowers and closes on the steel washer, lifting it clear of the wood. The visor stays lit a steady blue. Everything moves at natural real-time speed, the normal pace of someone working, with no slow motion and no speed ramping. Small motors, no music.

## Related pages
- [[projects]]
- [[runbook-living-painting]]
- [[draw-things-setup]]
