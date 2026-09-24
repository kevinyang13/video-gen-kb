# Photoreal projects

**Summary**: Cinematic photoreal shorts: FLUX.2 klein stills with Moodboard references, motion from LTX-2.3 or Wan 2.2, Real-ESRGAN to 4K, cut with crossfades. Dragon Epic, Lost City, the three-minute film. Full record per project: models, settings, prompts, seeds, music and output files. Generated from `projects.json`.

**Sources**: projects.json; per-project notes from the session logs.

**Last updated**: 2026-09-24

---

Index of every project: [[projects]]. Other themes: [[projects-anime]] · [[projects-3d]].

## Summary

| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |
|--:|---|---|---|---|---|---|---|---|
| 1 | [Dragon Epic — 1-minute photoreal short, family hero face](#dragon_epic) | 2026-09-21 | in progress — scene 1A posted | FLUX.2 [klein] 9B 1280x768 | Wan 2.2 High Noise 47 min | The Dragon's Breath | `—` | [▶ watch](https://youtu.be/Xzu-c5yX8uo) |
| 2 | [Three-minute film — recurring characters (subject TBD)](#film3min) | 2026-09-21 | planning | FLUX.2 [klein] 9B 1024x576 | Wan 2.2 High Noise 15 min | TBD | `—` | — |
| 3 | [Lost City — hyper-real rider on a raptor-dragon entering jungle ruins](#lost_city) | 2026-09-21 | in progress — clips at 4K+music: s2, s3, s7, s8, s10, s14; s9 trimmed (4.6 s, drift after); s11 stills rejected (klein duplicates the creature); s12 not started; s15 rift coda done (3 clips assembled to 30 s 4K with music) | FLUX.2 [klein] 9B 1280x768 | LTX-2.3 22B [distilled] 1.1 (production engine — see ltx_10s) — Wan 2.2 High Noise I2V (8-bit S) + Low Noise refiner 10% for locked-camera shots at 768p 49 min | Mystical orchestral theme with ancient flute | `—` | [▶ watch](https://youtu.be/68sq_jZqu6c) |

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

- **Date**: 2026-09-21 · **Status**: in progress — clips at 4K+music: s2, s3, s7, s8, s10, s14; s9 trimmed (4.6 s, drift after); s11 stills rejected (klein duplicates the creature); s12 not started; s15 rift coda done (3 clips assembled to 30 s 4K with music) · **Draw Things project**: `lostcity-s1, s2, s3, s7 (named); s8, s9 (cloned — clone crashes on video save); s10 and s11 in fresh Untitled projects; s14 rendered with draw-things-cli (no project file)`
- **Files** (`raw/clips/`): `lostcity/ref_openart_rider_ruins.webp (reference, raw/)`, `lostcity/crop_creature_rider.png, crop_spires.png, crop_foreground.png (Moodboard refs, raw/)`, `lostcity/s1_still_v1.png (shot 1 still, klein)`, `lostcity/s1_ltx_v1.mov (LTX-2.3 test, 1024x576x97 @25fps + audio)`, `lostcity/s2_still_v1.png (shot 2 still, klein, refs: our s1 skyline + spires crop, seed 1)`, `lostcity/s7_still_v2.png (shot 7 still, wingless; s7_still_v1_winged.png = rejected v1)`, `lostcity/s2_wan_v1.mov (shot 2 I2V, Wan 2.2, 1280x768x81)`, `lostcity/s2_wan_v1_4k.mp4 (3840x2160 HEVC 10-bit)`, `lostcity/s2_ltx_v1.mov (shot 2 via LTX-2.3, 1024x576x97 @25fps + audio)`, `lostcity/s2_ltx_v1_4k_audio.mp4 (LTX shot 2 at 3840x2160 + audio)`, `lostcity/s3_still_v1.png (shot 3 still, ref = crop of our s1 creature body)`, `music/mystical_flute.mp3`, `lostcity/s3_ltx_v2.mov (shot 3 LTX v2, hold-position prompt)`, `lostcity/s3_ltx_v2_4k_music.mp4 (4K + ambience + music bed)`, `lostcity/s3_ltx_v1_walkout.mov (v1, rejected: walk-out + phantom rider)`, `lostcity/s7_still_v1.png (side profile, anatomy OK)`, `lostcity/s7_ltx_v1.mov (LTX 1024x576x249 @25fps)`, `lostcity/s7_ltx_v1_4k_music.mp4`, `lostcity/s8_still_v1.png (gallop)`, `lostcity/s8_ltx_v1.mov + s8_ltx_v1_4k_music.mp4 (gallop, 10 s)`, `lostcity/s9_still_v1.png, s9_ltx_v1.mov (jump; drifts after ~4.6 s), s9_ltx_v1_trim.mov (clean 116 f)`, `lostcity/s10_still_v1.png, s10_ltx_v1.mov, s10_ltx_v1_4k_music.mp4 (drinking, 10.3 s, holds design)`, `lostcity/s14_still_v1.png (seed 2; s1/s3 variants kept)`, `lostcity/s14_ltx_v1.mov (ProRes 422 HQ, 249 f @ 25 fps + PCM audio)`, `lostcity/s14_ltx_v1_4k_music.mp4`, `lostcity/s15a|b|c_still_v1.png + _ltx_v1.mov + _4k_audio.mp4`, `lostcity/s15_rift_30s_4k_music.mp4 (the 30 s cut: 15a+15b+15c, xfade 0.5, flute bed, +6 dB)`
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


#### s3 — Low angle, creature's feet on wet flagstones

- **Engine**: LTX 1024x576 x97
- **Files**: s3_still_v1.png, s3_ltx_v2_4k_music.mp4
- **Note**: v1 asked for one step forward — it walked out of frame and hallucinated a second rider. Close-ups need hold-position wording.

*Still prompt*

> Cinematic film still, anamorphic 35mm, very low camera angle at ground level on a wet jungle path, muted colours, low contrast, subtle film grain. Filling the frame, the heavy clawed feet and thick scaled legs of a large saddled raptor-like reptile mount, a wingless two-legged theropod with slate-grey ridged hide, planted on wet mossy flagstones, water pooled between the stones, ferns and tall grass in the near foreground, the rider's boot in a stirrup and a hanging brown satchel visible above. Behind, out of focus, mossy carved blocks and the haze of a lost city with soft god rays. Shallow depth of field, layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> Fixed camera, low on the wet stone path. The creature stands still in place and does not walk; it only shifts its weight from one foot to the other, the claws flexing on the wet flagstones, small ripples spreading in the pooled water, the thick scaled legs tensing, the tail swaying slowly. The rider's boot rocks gently in the stirrup and the satchel sways. Ferns and grass in the foreground move in a light breeze, mist drifts through the god rays behind. The path behind stays empty. Water dripping, leather creaking, wind in the leaves, faint birdsong, no music. Photorealistic, cinematic, subtle smooth motion.


#### s7 — Canyon, side profile walking through the spires

- **Engine**: LTX 1024x576 x249 (10 s)
- **Files**: s7_still_v1.png, s7_ltx_v1_4k_music.mp4
- **Note**: Six rear-view attempts failed on anatomy before switching to this side framing.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. Inside a narrow canyon between colossal eroded sandstone spires and ziggurat towers of a lost city, soft volumetric god rays pouring down through morning haze, dust drifting in the light, vines and moss hanging from the carved stone walls. In the centre, walking left to right along a dirt path, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs. On its back a lone rider seen from the side, grey-green hooded cloak, brown leather jerkin, tan trousers, tall boots, hands on the reins, looking up at the towers. Ferns and broken carved blocks in the foreground, tiny birds high in the sky. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The camera holds a steady low side view as the creature walks slowly from left to right through the canyon with a heavy four-legged gait, its head bobbing gently and tail swaying, staying in the centre of the frame while the carved stone walls drift past behind it. The rider sways in the saddle, cloak lifting in a light breeze, looking up at the towers. Dust and pollen drift through the shafts of light, mist rolls slowly along the ground, ferns sway, tiny birds cross the sky. Heavy footsteps on packed earth, leather creaking, wind in the vines, faint jungle birdsong, no music.


#### s8 — Running — full gallop across a clearing

- **Engine**: LTX 1024x576 x249
- **Files**: s8_still_v1.png, s8_ltx_v1_4k_music.mp4

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. An open jungle clearing beside the lost city, eroded sandstone spires and ziggurat towers soft in the haze behind, god rays through thin cloud. In the centre, galloping left to right at full stride in side profile, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, all four legs in a running gallop with the heavy hind legs driving and the smaller forelegs reaching forward, dust kicked up behind it, on two heavy hind legs and two smaller forelegs. On its back a lone rider leaning low over the neck holding the reins, grey-green hooded cloak streaming straight back, brown leather jerkin, tan trousers, tall boots. Ferns and tall grass in the foreground, tiny birds high in the sky. Motion, energy, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature gallops at full speed from left to right across the clearing with a powerful four-legged running gait, hind legs driving and forelegs reaching, dust bursting up behind each stride, while the camera tracks alongside at the same speed keeping the creature and rider centred in the frame as the ruins and jungle rush past behind. The rider stays low over the neck, cloak whipping straight back. Grass and ferns blur past in the foreground, birds scatter from the trees. Pounding heavy footfalls, rushing wind, leather creaking, distant birds, no music.


#### s9 — Jumping — leap over a fallen pillar

- **Engine**: LTX 1024x576 x249
- **Files**: s9_still_v1.png, s9_ltx_v1.mov, s9_ltx_v1_trim.mov
- **Note**: Creature morphs toward a horse after ~frame 115 (4.6 s) — trimmed there.

*Still prompt*

> Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A jungle path beside the lost city, spires and ziggurat towers in the haze behind, god rays through morning mist. In the centre, caught mid-leap in side profile over a fallen mossy stone pillar lying across the path, a large quadrupedal raptor-like reptile mount, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs, its heavy hind legs extended behind from the push-off and its smaller forelegs tucked up, body arched in the air above the pillar. On its back a lone rider crouched low in the saddle gripping the reins, grey-green hooded cloak flaring, brown leather jerkin, tan trousers, tall boots. Ferns and broken carved blocks in the foreground, tiny birds high in the sky. Motion, Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.

*Video prompt*

> The creature completes its leap over the fallen stone pillar, forelegs reaching down and hind legs swinging under it, lands on the far side with a puff of dust and runs on a few strides before slowing to a walk, while the camera tracks alongside at the same pace keeping the creature and rider centred in frame. The rider absorbs the landing, rising and settling in the saddle, cloak snapping. Dust bursts at the landing, ferns shake, birds scatter. A heavy thudding landing, pounding footfalls, leather creaking, distant birdsong, no music.


#### s10 — Drinking at a jungle pool

- **Engine**: LTX 1024x576 x257 (10.3 s)
- **Files**: s10_still_v1.png, s10_ltx_v1_4k_music.mp4
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


#### s15a — The crack — a rift opens in the sky above the ruined city

- **Engine**: LTX 1024x576 x257 (10.28 s) — draw-things-cli — rendered in 9.7 min
- **Note**: No creature and no rider in this shot: the ground mount must never share a frame with winged animals or klein grows wings on it. City is already ruined here — this follows s14. Never write 'lightning' — klein renders a literal lightning bolt instead of a rift; say torn sky, broken glass, hard-edged crack. Rendered 2026-09-22: crack holds and widens, winged shapes multiply. Artefact: the rising dust reads as puffy cumulus blobs rather than dust — drop the dust clause if re-shot.

*Still prompt*

> Cinematic film still, anamorphic 35mm, muted colours, low contrast, subtle film grain. Low wide angle looking up across a ruined city. Broken sandstone spires and shattered ziggurat towers fill the lower third of the frame, rubble and snapped stone, thick dust still hanging in the air, jungle canopy pressing in at the edges. Above them the overcast sky is torn wide open by a long jagged crack that runs across the clouds like a sheet of glass broken from edge to edge, hard-edged and forked, blinding white light pouring through the gap from behind the sky, the torn edges sharp and glowing, the clouds curling and peeling back along them, pale light spilling down onto the ruins in hard shafts. Far away and tiny, a few small dark winged shapes are just slipping out of the crack. Huge sense of scale, deep depth of field, Layered atmospheric perspective, photorealistic, highly detailed, cold pale light spilling from the crack against a dull overcast sky.

*Video prompt*

> Fixed camera, very slow push in on the crack. The tear in the sky splits further open, its glowing edges flaring and shifting, the pale light pulsing brighter over the ruins; clouds peel back and drag in toward the opening, dust lifts from the rubble below and turns in the shafts of light. The small dark winged shapes grow larger as more of them slip out of the tear, one after another. Deep resonant hum from the torn sky, low rumbling air, distant falling stones, wind, no music.


#### s15b — Exodus — the flock pours out of the rift

- **Engine**: LTX 1024x576 x257 (10.28 s) — draw-things-cli, --image = last frame of s15a — rendered in 9.5 min
- **Note**: Chaining test: extract the last frame with ffmpeg and hand it to the CLI as --image. Flying animals are the subject here, so wings are wanted — never mention the ground creature. Chaining worked: `ffmpeg -sseof -0.08 -i a.mov -update 1 -frames:v 1 first.png` then pass it as --image. Continuous across the cut.

*Still prompt*

> none — chained: first frame is the last frame of s15a (keeps the rift shape and cloud spiral continuous)

*Video prompt*

> The torn crack holds open above the ruins as a dense stream of large leathery-winged flying reptiles pours out of it, long crested heads and beating wings, spilling downward and fanning apart across the sky; the camera tilts slowly down with them toward the broken spires. Their shadows sweep over the rubble, dust swirls up through the shafts of light, the torn edges of the sky keep flaring. Massed leathery wingbeats, harsh distant shrieks, deep rift hum, wind, no music.


#### s15c — The circling — the flock wheels above the dead city

- **Engine**: LTX 1024x576 x257 (10.28 s) — draw-things-cli — rendered in 9.6 min
- **Note**: Slow, in-place swarm motion — the stable pattern. Nothing large and detailed in the foreground to drift. Best of the three: the ring of animals holds for the full clip and the crack stays put.

*Still prompt*

> Cinematic film still, anamorphic 35mm, muted colours, low contrast, subtle film grain. Very wide high vantage looking down and across the ruined lost city, the broken spires and collapsed ziggurats small in a wide bowl of jungle, dust and haze lying over the rubble. Dozens of large leathery-winged flying reptiles wheel in one slow enormous circle above the ruins, silhouetted at different distances, some near and sharp with crested heads and outstretched wings, others tiny specks far away, their shadows crossing the stone below. Behind and above them the sky is still torn wide open by a long jagged crack like broken glass, white light pouring through the gap, its glow lighting the underside of the flock and the dust. Enormous sense of scale, deep depth of field, Layered atmospheric perspective, photorealistic, highly detailed, cold pale light spilling from the rift against a dull overcast sky.

*Video prompt*

> Fixed wide camera. Dozens of winged reptiles wheel slowly in one great circle above the ruined city, gliding and banking, wings beating now and then, the whole ring turning steadily and unbroken; nearer birds cross the frame and away, their shadows sliding over the rubble. Behind them the torn crack in the sky glows and flares, its edges shifting, clouds peeling back along it, dust drifting over the ruins below. Massed wingbeats, layered distant shrieks, deep rift hum, wind, no music.

## Related pages
- [[projects]]
- [[runbook-living-painting]]
- [[draw-things-setup]]
