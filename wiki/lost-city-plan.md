# Lost City — Project Plan (hyper-real sci-fantasy rider)

**Summary**: Plan for a hyper-realistic short in the style of the OpenArt reference (`raw/lostcity/ref_openart_rider_ruins.webp`): a hooded rider on a saddled raptor-dragon walks into an overgrown city of stone spires, god rays, waterfall. Covers what makes the reference look real, the local pipeline, Draw Things settings per stage (FLUX.2 klein stills; Wan 2.2 vs **LTX-2.3** for motion), creature/hero/environment consistency, shot list, experiments, budget. Living document.

**Sources**: `raw/lostcity/ref_openart_rider_ruins.webp` (reference, OpenArt watermark — generator unknown, probably a closed model such as Kling/Veo/Seedance; *unverified*); Wan 2.2 prompting guides ([MimicPC](https://www.mimicpc.com/learn/how-to-craft-wan22-ai-video-prompts), [InstaSD](https://www.instasd.com/post/wan2-2-whats-new-and-how-to-write-killer-prompts), [WhatLab](https://whatlab.ai/guides/wan2-2-prompting-guide)); LTX docs ([I2V guide](https://docs.ltx.io/open-source-model/usage-guides/image-to-video), [Draw Things LTX-2 wiki](https://wiki.drawthings.ai/wiki/LTX-2), [HF LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3)); hands-on results from [[dragon-epic-plan]] §7b (2026-09-21). All as of 2026-09-21.

**Last updated**: 2026-09-22 (LTX production settings in §3c; escape ending, shot 14 restaged as a landscape total collapse, creature enlarged after a motion-bleed failure; per-scene prompts in [[projects]])

---

## 1. What the reference does — and what we copy

| Element in the reference | Why it reads as real | How we get it locally |
|---|---|---|
| Rider seen **from behind**, hood + grey-green cloak, satchel, boots in stirrups | no face to judge → no uncanny valley; wardrobe is period-plausible | hero always ¾-back or profile; face optional (one hero-turn shot at most) — see §4 |
| Creature = **quadruped raptor-dragon**, no wings, saddle, reins, saddlebag, horn crest | grounded animal anatomy, tack that obeys gravity; scale ≈ horse+ | creature design sheet in the Moodboard (§4); "no wings" in every prompt |
| **God rays** through haze, cool overcast + warm sun, muted greens, soft shadows | atmospheric perspective: 4–5 depth planes, each hazier | prompt words: *volumetric god rays, layered haze, atmospheric perspective, natural overcast with sun breaks, muted desaturated greens* |
| Layered set: foreground fern/grass → creature → mossy blocks → waterfall/bridge → spire skyline | parallax gives motion something to reveal | describe the planes in order in the still prompt |
| Waterfall, birds, dust in the light | secondary motion sells the frame in video | motion prompt: waterfall + birds + drifting dust, always |
| Anamorphic 2.0:1 frame, 35–50 mm, slight film grain, no HDR glow | cinema camera, not a phone | `anamorphic 35mm, subtle film grain`; export 2.39:1 letterbox optional |
| Camera: slow **side tracking** with the walking rider | subject stays centred → no ghosting from translation | "tracking shot, camera moves with the rider, keeping them centred" (§3b/3c) |

Colour: **do not** saturate. Reference is low-contrast, sand/olive/slate palette; the sky is near-white. Add `muted colours, low contrast, natural` to every still prompt.

## 2. Pipeline

```
design sheets (creature, hero, city)  ──►  per-shot still (FLUX.2 klein + Moodboard refs, 1280×768)
                                                 │
                                                 ▼
                       5 s clip — Wan 2.2 I2V (proven) **or** LTX-2.3 distilled (untested, 25 fps + audio)
                                                 │
                                                 ▼
                          Real-ESRGAN ×4 → 3840×2160 HEVC 10-bit (scripts/upscale_4k.sh)
                                                 │
                                                 ▼
                       ffmpeg: xfade concat → music/ambience → letterbox → title → 4K master
```

Same skeleton as [[dragon-epic-plan]] §2. New: the LTX-2.3 branch (experiment L1 decides) and no face pass by default.

## 3. Draw Things configuration per stage

### 3a. Stills — FLUX.2 [klein] 9B (8-bit S)

| Setting | Value | Notes |
|---|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) | *Try recommended settings* → steps 4, CFG 1, shift 3, DDIM Trailing. New projects inherit the last model (Wan) — re-pick klein every time |
| Size | **1280×768** | 1280×720 not reachable (64-px grid). Same size as the I2V so no rescale |
| LoRA | Disabled | auto-clears when switching from Wan |
| Control Inputs → **Moodboard** | 1–3 reference images, equal weight | klein's reference channel; **no** ControlNet/IP-Adapter/PuLID is compatible with klein (Dragon Epic E1). Learned 2026-09-21: an uncropped scene reference at equal weight **imposes its composition** — crop references to the element you want copied (creature head/neck, cloak, a spire cluster), never a full wide frame |
| Prompt order | camera + lens + light → planes far to near → creature → rider → palette | see §5 prompt |
| Negative | n/a at CFG 1 | fix the prompt, not the negative |

Time: ~1 min per still with 3 refs (measured 2026-09-21 on Dragon Epic 1B v2).

### 3b. Motion A — Wan 2.2 I2V A14B (8-bit S) pair — the proven path

| Setting | Value |
|---|---|
| Model / Refiner | High Noise I2V (8-bit S) / Low Noise I2V (8-bit S) @ **10%** (never 50% with Lightning) |
| LoRA | Wan 2.2 A14B Lightning High-Noise 100% |
| Steps / CFG / Shift / Sampler | 4 / 1.0 / 5 / UniPC Trailing |
| Size / frames | 1280×768, 81 f @ 16 fps (5.06 s) |
| Time | **~45 min per clip** at this size (measured) |

**Motion prompt rules** (from guides + our ghosting fix):
- I2V formula = *subject motion + camera motion*, nothing about appearance (the image already has it). 80–120 words max; one camera move, one subject action, secondary ambience.
- **Walking creature**: the rider must not slide across the frame at 4 steps. Phrase it as a **tracking shot** so the subject stays put and the *background* moves: `tracking shot, the camera moves alongside the rider at walking pace, keeping the rider and creature centred in frame; the creature walks with a slow heavy four-legged gait, head bobbing gently, tail swaying; the rider sways with the saddle, cloak moving in a light breeze; the waterfall flows, mist drifts through the god rays, two birds cross the sky far away; smooth motion, cinematic, photorealistic`. Test = **L2**.
- Camera vocabulary Wan 2.2 obeys: *pushes in / pulls back / tilts up / tracking shot / fixed lens / handheld*. Speed word every time (*slowly*). Avoid whip pans and anything that reveals geometry not in the still.
- Full-frame creature shot (head fills frame): articulation only, no camera move (Dragon Epic rule).

### 3c. Motion B — LTX-2.3 22B [distilled] 1.1 — **the production engine** (validated 2026-09-22)

Every Lost City clip since shot 2 is LTX: s2, s3, s7, s8, s9, s10. What you get: native **25 fps**, a **PCM audio track** (footsteps, waterfall, birds), and real locomotion Wan cannot do at 4 steps. What you pay: a coarse latent (32×32 spatial, 8× temporal) that re-synthesizes fine detail and invents geometry, 576p instead of 768p, and **loose camera staging at CFG 1** — LTX obeys the *action*, picks its own *blocking*.

**Draw Things settings — all measured on the M4 Max 48 GB**

| Setting | Value | Why / gotcha |
|---|---|---|
| Model | LTX-2.3 22B [distilled] 1.1 (Local list, DT quant) | UI overlay says "Text to Image Generation" but the canvas image **is** the first frame; the Strength tab reads *Text to Video 100%* |
| Steps / CFG | **8 / 1.0** | distilled model. The DT wiki's 20–25 steps / CFG 6–7 are for the *dev* variant — wrong here |
| Sampler | **TCD Trailing** | from *Try recommended settings* |
| Strategic Stochastic Sampling | **30%** | ditto; leave on |
| Shift | **5** | |
| Size | **1024×576** | the only size that fits 48 GB in one stage. Sizes must be ÷32 (1280×768 is legal but see hi-res fix) |
| Frames | **249** = the slider max ≈ 9.96 s; **257** (8k+1) also accepted | frames must be 8k+1. 249 f costs the same wall clock as 97 f → always max out |
| High Resolution Fix | **off** (DT auto-disables it at 576p) | at 1280×768 DT turns it on (stage 1 at 640×384, stage 2 at 70% strength) and **stage 2 stalls in swap** — 27–48 GB, step counter frozen |
| Strength / first frame | **100%** | a canvas larger than the generation area is **centre-cropped, not scaled** — render or crop the still at 1024×576 or expect to lose the edges |
| LoRA / Refiner | none | |
| Time | **~20 min per 10 s clip** | the in-app compute timer reads ~3 min — the rest is paging. Quit other apps; **never run Real-ESRGAN while LTX renders** (48 GB can't hold both) |
| Export | ProRes 422 `.mov`, 25 fps + PCM audio ≈ −33 dB | `upscale_4k.sh` drops audio (`-an`) → remux, then mix the flute bed under it (recipe in §3e) |

**Prompt rules (learned the hard way)**

- One chronological paragraph, 4–8 sentences, < 200 words: **motion → camera → audio**. Name the sounds explicitly ("heavy footsteps on wet stone, distant waterfall roar, birdsong, no music") — they end up on the track.
- **Action, not staging.** "left to right, camera tracks alongside" was ignored on s1; the same wording worked on s2 and s7. Write the action you want, accept the camera you get, or shoot that frame on Wan.
- **Close-ups: hold position.** Asking a close-up for locomotion (s3 v1) produced a full walk cycle that left the frame by 2 s *and* hallucinated a second rider behind. Use "stands still… only shifts its weight" and say the path behind **stays empty**.
- **Motion-stability rule**: slow in-place actions (walk, drink, weight shift, breathing) hold the creature design for the full 10 s; fast locomotion (gallop, jump) drifts toward a horse after ~4–5 s → trim on the first soft frame (s9 → 116 f).
- **Motion bleeds onto small subjects.** In a shot where something else is destroyed, LTX applies those verbs to the subject too: s14 v1 sheared the creature's *head* off and dropped it like a falling spire. Fixes, in order of effect: make the subject large (≥ a third of the frame — a head that is ~30 px in the 32×32 latent gets re-synthesised as debris), name the subject and its stillness **before** any falling verb, use positive rigidity words (*solid, still, intact, head held level and attached, only the ribs move*), and add one clause pinning the destruction to the distance. Last resort: render the destruction as a plate with no creature in it.
- Wide shots tolerate invented foreground geometry (s2 gained palm fronds sweeping the lens — more cinematic); hero shots do not.

**Headless alternative (faster)** — since 2026-09-22 the same render runs from the shell with no window, at roughly half the wall clock (9 min 41 s for 249 frames vs ~20 min in the app), because nothing else holds memory:

```bash
draw-things-cli generate -m ltx_2.3_22b_distilled_1.1_q8p.ckpt \
  --prompt-file scene.txt --image still.png \
  --width 1024 --height 576 --frames 249 --steps 8 --cfg 1 \
  --config-json '{"sampler":19,"shift":5.0,"stochasticSamplingGamma":0.3,"fps":25,"hiresFix":false}' \
  --offline --disable-preview --video-format prores422hq -o clip.mov
```

`sampler: 19` is TCD Trailing (16 = DDIM Trailing), `stochasticSamplingGamma` is the 0…1 form of SSS 30%, and `--image` really is the first frame. The catch: the released CLI takes only one `--image`, so **Moodboard shots still need the app**. Full detail in [[headless-cli-pipeline]]. Shot 14 was shot this way.

**Per-clip workflow (Draw Things)**

1. **Fresh project** per clip (Projects → + → `dt_project.sh rename-newest lostcity-sN`). Never a `dt_project.sh clone` — saving a *video* into a cloned project asserts in `ImageHistoryManager.pushHistory` and **kills the app, wiping that project's history** (two crashes, 2026-09-22). Clone is fine for stills.
2. Load the still from disk with the import icon (the Open panel takes a full path via ⇧⌘G). Moodboard drag from Finder cannot be automated.
3. Pick the LTX model **after** loading the image — a new project inherits the last model, and pressing Stop rolls the settings back to the previous model.
4. Click **Generate once**. A second click is Stop.
5. Export, verify the file landed (`find raw/clips -mmin -2`) — the Save sheet needs two presses, the first only commits the filename.
6. Then, and only then, `scripts/upscale_4k.sh`.

L1 (below) is the experiment that produced these numbers; Wan 2.2 (§3b) stays for locked-camera, static-subject shots at 768p — see [[image-to-video-models]] for the decision rule.

### 3d. Upscale to 4K

`scripts/upscale_4k.sh clip.mov` — Real-ESRGAN x4plus ncnn, tile 128, → 3840×2160 HEVC 10-bit 40 Mbps, ~6 min per 81-frame clip (121 frames → ~9 min). Before upscaling, check the clip has no shimmer on the fern foreground; if it does, try `realesr-general-x4v3` (denoise) *(verify model present in tools/realesrgan/models)*.

### 3e. Assembly

`scripts/assemble_film.sh` (to write, shared with Dragon Epic): xfade 0.5 s, optional 2.39:1 letterbox (3840×1608 in 3840×2160), music + ambience, title, HEVC 10-bit. Music genre here: **ambient orchestral / ethereal choir**, quieter than Dragon Epic; pick from Pixabay when shot 1 exists.

## 4. Consistency — creature, hero, city

Same toolkit as [[character-consistency]]; three locks.

**Creature lock (text, verbatim in every prompt)**: *a large saddled raptor-like reptile mount, a wingless two-legged theropod with a long neck,* — **never the word "dragon"**: shot 7 v1 (2026-09-21) grew bat wings from "raptor-like dragon, no wings" when no creature crop was in the Moodboard; klein at CFG 1 weighs the noun over the negation. Old wording for reference: *a large quadrupedal raptor-like dragon, no wings, slate-grey ridged hide, long neck with a bony horn crest, small amber eyes, leather saddle with reins and a brown satchel, walking on two heavy hind legs and two smaller forelegs*.
**Creature sheet (Moodboard)**: first-shot still, **cropped to head+neck** and a second crop of saddle+flank. Never the full frame.

**Hero lock**: *a lone rider seen from behind, dark cropped hair, grey-green hooded cloak thrown back, brown leather jerkin, tan trousers, tall boots, hands on the reins*. No face by default. If a face shot is added later → Dragon Epic face path (Moodboard ×2 face crops; FaceFusion post).
**Hero sheet**: crop of the rider from the first still.

**City lock**: *a lost city of tall eroded sandstone spires and ziggurat towers swallowed by jungle, a stone arch bridge and a waterfall between them, soft god rays through morning haze*. Plus one crop of a spire cluster in the Moodboard for the wide shots.

Moodboard cap: **3 images** per still (klein guides say 3–5, >7 muddies; at 1280×768 three refs cost ~1 min).

## 5. Scene 1 — locked to the reference

Shot 1 = the reference frame, re-generated by us (we do not animate the OpenArt image itself — different creature, and it is someone else's render).

**Still prompt 1**:
`Cinematic film still, anamorphic 35mm, eye-level side view, muted colours, low contrast, subtle film grain. A lost city of tall eroded sandstone spires and ziggurat towers swallowed by jungle rises in the distance through morning haze, a stone arch bridge and a white waterfall between them, soft volumetric god rays breaking through thin cloud. Mossy stone blocks and palms in the middle distance, ferns and tall grass in the foreground. In the centre, [creature lock] walks left to right on a dirt path. On its back [hero lock]. Layered atmospheric perspective, photorealistic, highly detailed, natural overcast light with warm sun breaks.`

**Motion prompt 1 (Wan)**: see §3b tracking-shot prompt.
**Motion prompt 1 (LTX)**: `The creature walks slowly from left to right with a heavy four-legged gait, its head bobbing and tail swaying, while the camera tracks alongside at the same pace so the rider stays centred. The rider sways gently in the saddle, the cloak lifting in a light breeze. Behind them the waterfall pours steadily and thin mist drifts through the shafts of light; two birds glide across the distant spires. Heavy footsteps on damp earth, the far roar of the waterfall, faint jungle birdsong, no music.`

## 6. Shot list (v2 — 10 s clips; 1–3 and 7–10 shot, 13–14 written)

| # | Shot | Camera | Subject motion | Consistency need |
|---|---|---|---|---|
| 1 | **Reference frame**: side, rider + creature walk toward the city | slow side tracking | walk, cloak, waterfall, birds | creature + hero + city |
| 2 | Extreme wide from a ledge: city skyline, tiny rider on the path | very slow push in | mist drift, birds, waterfall | city |
| 3 | Low angle, creature's feet and forelegs on wet stone, ferns | fixed lens | feet plant, dust puffs, grass sway | creature (legs) |
| 4 | ¾-back medium on the rider's shoulders, spires beyond | slow push in | rider's head turns slightly, cloak, hair | hero |
| 5 | Creature head in profile, amber eye, horn crest, haze behind | fixed lens | slow blink, nostril flare, head turn ≤ 10° — **articulation only** | creature (head) |
| 6 | Through the stone arch: rider crosses the bridge, waterfall to the side | tracking from behind | walk, spray, mist | city + creature |
| 7 | Reverse wide: rider entering the spire canyon, god rays overhead | slow tilt up | dust in the light, birds | city |
| 8 | Ending: rider dismounted, silhouette before the tallest tower, hood up | slow pull back | cloak, mist | hero (silhouette) |
| 9 | **Running** — full gallop across a clearing | tracking alongside | gallop, dust, cloak streaming | creature (drifts after ~5 s) |
| 10 | **Jumping** — leap over a fallen pillar | tracking alongside | leap, landing, dust | creature (drifts after ~5 s) |
| 11 | **Drinking** — muzzle in a jungle pool below a waterfall | fixed | head lowers/lifts, ripples, rider looks around | creature (stable, full 10 s) |
| 12 | Dismount / mount up beside the creature | fixed | rider steps down / swings up | **blocked** — klein renders two creatures |
| 13 | **Escape** — gallop down the avenue as a spire shears and falls behind | tracking alongside at speed | gallop, tumbling blocks, rolling dust wall | creature large in frame; trim on first soft frame |
| 14 ✅ | **Escape / final shot** — wide landscape from a ridge: every spire falls until the skyline is empty | fixed, wide | creature solid and still in the near foreground (left third), rider looks back; the whole city comes down on the horizon, last tower by ~8 s, ends on a dust skyline | creature **must be large** — at a sixth of the frame its head collapsed with the spires (v1) |

Cheap shots first: 2, 3, 5, 7 have no hero face and simple motion — render them to test the look before the tracking shots.

**Story (v2, 2026-09-22)**: arrival and exploration (1–3, 7), life with the creature (9–11), then the city comes down and the rider escapes (13–14). Shot 14 is the last frame of the film: a distant landscape view where every spire collapses until nothing is left standing. The collapse gives the film an ending that needs no dialogue and no face.

## 7. Experiments (in order)

| # | Question | Test | Pass | Cost |
|---|---|---|---|---|
| L0 | Does klein reproduce the reference **look** (palette, god rays, layering) without copying it? | still prompt 1, Moodboard = 3 crops of the reference (spires, creature, foreground); 3 seeds | 2 of 3 read as film stills, not renders | 5 min |
| L1 | **LTX-2.3 distilled 1.1 on the M4 Max**: loads? time? quality? audio? | same still → LTX at 1024×576, 97 f, 8 steps, CFG 1, motion prompt 1 (LTX); then 1280×736 × 121 f | ≤ 60 min/clip, no blobs, walk cycle plausible | 1–2 h — **done, see 7b** |
| L2 | Walking creature without ghosting on Wan 2.2 (tracking-shot phrasing) | still 1 → Wan, §3b prompt | legs cycle, rider stays centred, no double edges | 45 min |
| L3 | Creature consistency via cropped sheet across two shots (1 → 5) | shot 5 still with the head crop in Moodboard | same crest/eye/hide | 5 min |
| L4 | Hero consistency from behind (1 → 4) | shot 4 still with the rider crop | same cloak/jerkin/hair | 5 min |
| L5 | Real-ESRGAN on fern foreground: shimmer? | upscale L2 result, check 3 s loop | no crawling texture | 10 min |
| L6 | Music/ambience pick | Pixabay "ambient orchestral ruins" | Kevin approves | 10 min — **picked**: "Mystical orchestral theme with ancient flute" (DesiFreeMusic, 4:00), `raw/clips/music/mystical_flute.mp3` |

L1 decides the engine for the whole project; run L2 anyway as the fallback.

## 7b. Results

| Exp | Date | Result |
|---|---|---|
| s14 v2 (final shot) | 2026-09-22 | **Works, and it was the first headless render.** Still and clip both from `draw-things-cli` — no window, no clicks. 3 klein seeds at 27–35 s each (seed 2 kept: sheared spire tops, dust columns, creature intact and large), then LTX 249 f in **9 min 41 s**. The enlarged creature plus subject-first rigidity wording fixed the motion bleed: the creature stands solid for the full 10 s while the spires come down behind it, and the last second is an empty dust skyline. Frame 0 of the clip is the still pixel-for-pixel, so `--image` is true I2V. `s14_ltx_v1.mov`. |
| s14 v1 (final shot) | 2026-09-22 | **Motion bled onto the subject.** In the extreme-wide staging the creature was about a sixth of the frame; LTX applied the city's collapse verbs to it and its **head sheared off and fell like a spire**. Two causes: at that scale the head is ~30 px in the 32×32 LTX latent (nothing to hold onto), and the falling verbs were in the prompt before the subject. v2 brings the creature into the near foreground at a third of the frame width, leads with the subject and positive rigidity words, and pins the destruction to the horizon in one clause. General rule now in §3c. |
| L1 (result) | 2026-09-21 | **Works; slow; strong motion.** 1024×576 × 97 f @ 25 fps, 8 steps, CFG 1, TCD Trailing, SSS 30%, shift 5, single stage (DT auto-disables hi-res fix at this size). **~25 min wall clock** (compute timer said 3 min — the rest is swap). Output: ProRes .mov **with a PCM audio track** (mean −33 dB, quiet ambience). Motion: the creature turns ¾ and **walks away into the city with a real four-legged gait**, rider stays seated, birds cross, god rays hold; no ghosting, anatomy intact. It ignored "left to right" + "camera tracks alongside" and chose its own blocking (walk into the scene, camera static) — LTX follows the *action*, not the *staging*, at CFG 1. First frame = centre crop of the 1280×768 still (canvas larger than the generation area). Files: `raw/clips/lostcity/s1_ltx_v1.mov`, `_preview.mp4`, `_strip.png`. **Verdict**: LTX-2.3 is usable for shots that need real locomotion (Wan can't at 4 steps) but costs ~25 min at 576p and needs a memory-light session (quit other apps); Wan 2.2 stays the default for ambient/static-subject shots at 768p. |
| L1 (interim) | 2026-09-21 | LTX-2.3 22B distilled 1.1 **loads and runs** in Draw Things on the M4 Max, but is **memory-bound**. *Try recommended settings* gives steps 8, CFG 1.0, TCD Trailing, Strategic Stochastic Sampling 30%, shift 5, frames 121, and turns on **High Resolution Fix** = the official LTX two-stage pipeline (1st pass at half size 640×384, 2nd pass at full size, strength 70%). At 1280×768 × 121 f: stage 1 (8 steps @ 640×384) took ~3 min — fast — but stage 2 at 1280×768 stalled (swap 27–48 GB, step counter frozen for minutes) → stopped. At 1024×576 × 97 f DT auto-disables hi-res fix (single stage); the compute timer reads ~1 min per 10+ min wall clock — paging the 22B DiT + Gemma text encoder in and out of swap. Overlay says "Text to Image Generation" but the canvas still **is** used as first frame (preview shows creature + rider); the Strength tab reads *Text to Video 100%* for LTX I2V. Canvas larger than the generation area → centre crop, not scale. |
| s10 drinking | 2026-09-22 | **Best clip of the batch.** Fresh project (not a clone), still loaded from disk, LTX 1024×576 × 257 f. Creature design holds for the whole 10.3 s — head lowers and lifts, water drips, ripples settle, rider looks around. Confirms the rule: **slow, in-place actions are stable; fast locomotion drifts**. `s10_ltx_v1_4k_music.mp4`. |
| s11 dismount | 2026-09-22 | **Blocked on the still.** Three seeds, each with *two* creatures — klein reads "rider beside the mount / dismounting" as two animals, and "alone / only one creature / no second creature" does not fix it (negations are weak at CFG 1). Next idea: stage the person in front of the creature's head holding the reins, or crop a single-creature region and inpaint. |
| Scenes 8–12 batch | 2026-09-22 | s8 gallop and s9 jump stills first-seed keepers; both clips 10 s. **Two Draw Things crashes** (SIGTRAP): the crash log points at `ImageHistoryManager.pushHistory` → `SQLiteWorkspace` — saving a *video* into a project **cloned** with `dt_project.sh clone` asserts and kills the app, wiping that project's history. Clone is fine for stills, not for clips: use a fresh project (Projects → +) per clip and load the still from disk via the import icon (⇧⌘G in the Open panel takes a full path; the panel needs full-screen control). Second rule: never upscale while LTX renders — 48 GB can't hold both. s9's clip drifts after ~4.6 s (creature morphs toward a horse under fast motion) → trimmed to 116 frames. |
| Shot 7 | 2026-09-22 | Six failed rear-view attempts (wings, three legs, mismatched legs) → the fix was the **camera**, not the prompt: the side-profile framing and verbatim creature wording from shot 1 gave correct anatomy first try. Rules: (1) never say "two-legged" — the creature is a quadruped in every ref; (2) don't put a four-legged animal dead-behind at low angle; klein cannot resolve the legs. Then LTX at the slider max **249 f = 10 s** (1024×576, 8 steps, ~20 min): tracking side view holds the creature centred through the canyon, anatomy stable for the full 10 s. `s7_ltx_v1_4k_music.mp4`. |
| Shot 3 v2 (LTX) | 2026-09-21 | Hold-position prompt ("stands still… only shifts its weight… the path behind stays empty"): creature stays in frame, weight shift + claw flex + tail sway, ripples, no phantom figures; slight forward drift in the last second. ~20 min. 4K + LTX ambience mixed with the flute bed at 0.5 (`s3_ltx_v2_4k_music.mp4`). Music mix recipe: `[fx]` LTX track at 1.0, `[m]` bed atrim/afade 0.5 in 1 out at 0.5, `amix` then `volume=1.6` to recover amix's level drop. |
| Shot 3 v1 (LTX) | 2026-09-21 | Still: first seed keeper (claws on wet flagstones, boot + satchel, arch in haze; ref = crop of *our* s1 creature body). LTX 1024×576 × 97 f with "take one slow step forward": it produced a full walk cycle, the creature left the frame by 2 s, and it **hallucinated a second rider on horseback** on the path behind (visible from frame ~30). Real gait, unusable shot. Rule: on a **close-up**, never ask LTX for locomotion — hold position ("stands still… only shifts its weight") and say the background stays empty; save walking for wides. v2 rerun with that prompt. |
| Shot 2 via LTX | 2026-09-21 | Same still through LTX-2.3 (1024×576 × 97 f, 8 steps, CFG 1, TCD, SSS 30%), ~20 min. **Obeyed the camera this time**: a real push-in with parallax — it hallucinates foreground palm fronds and a column sweeping past the lens, rider walks the path, waterfall + birds live, audio track. More cinematic than Wan's drift; costs invented foreground geometry (fine on a wide, risky on a hero shot). Side-by-side: Wan = stable/subtle at 768p; LTX = dynamic at 576p + audio. `raw/clips/lostcity/s2_ltx_v1.mov`. |
| Shot 2 clip | 2026-09-21 | Wan 2.2 I2V on `s2_still_v1.png`, §3b settings (DDIM Trailing, refiner 11%), prompt: *very slow push in … mist … waterfall … ferns swaying … tiny birds … the small rider and creature walking slowly along the path away from the camera*. **49 min** at 1280×768 × 81 f. Clean: push-in reads on the foreground columns, rider walks the path (tiny subject → translation is fine), no ghosting, foliage no shimmer after Real-ESRGAN (L5 pass). 4K: `raw/clips/lostcity/s2_wan_v1_4k.mp4` (6:19 upscale). |
| L0 | 2026-09-21 | **Pass on seed 1.** klein + 3 cropped refs (creature+rider, spires, foreground) at 33% each, still prompt 1 verbatim. God rays, spire skyline, bridge + waterfall, saddled wingless creature, hooded rider from behind, muted palette — all present; composition is ours (not a copy). ~2 min render with 3 refs. Export via the toolbar Save sheet worked fully from automation. `raw/clips/lostcity/s1_still_v1.png`. |

## 8. Budget

| Stage | Time |
|---|---|
| Design sheets + L0 | 30 min |
| L1 | 1–2 h |
| 8 stills × ~3 seeds | 30 min |
| 8 clips × ~20 min (LTX 10 s) or 45 min (Wan 5 s) | 3–6 h (unattended) |
| 8 upscales × 6 min | 50 min |
| Assembly + music | 45 min |
| **Total** | **~10 h**, ~2.5 h attended |

## 9. Risks

- **Walk cycles**: 4-step Lightning Wan struggles with limb cycles (Dragon 1A ghosting). Tracking phrasing (L2) or LTX (L1) mitigate; fallback = creature standing, only head/tail/cloak moving, camera does the travel.
- **LTX-2.3 memory**: confirmed — the 22B quant + Gemma text encoder swap on 48 GB. Stay at 1024×576, single stage, nothing else running (§3c).
- **Reference drift**: klein may copy the OpenArt frame too closely (composition, creature). Crops only; different palette words if needed. We are not distributing their image.
- **Shimmer** on high-frequency foliage after Real-ESRGAN → L5; alternative SeedVR2 (see [[video-upscaling]]).
- **Saturation creep**: Wan tends to warm/saturate; keep "muted colours" in the still and grade in ffmpeg if needed (`eq=saturation=0.9`).

## 10. Open questions for Kevin

1. Length: 40 s (8 shots) first, or straight to 60 s?
2. Story beat at the end — dismount and look up (shot 8), or ride on into the city?
3. Hero face ever shown? (If yes → face refs like Dragon Epic.)
4. Sound: LTX-generated ambience if L1 works, or music only?

## Related pages
- [[dragon-epic-plan]] — sibling project; motion rules and 4K path reused here
- [[character-consistency]] · [[identity-conditioning]]
- [[image-to-video-models]] — LTX-2.3 facts · [[draw-things-setup]]
- [[video-upscaling]] · [[runbook-living-painting]] · [[projects]]
