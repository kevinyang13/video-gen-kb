# Dragon Epic — Project Plan

**Summary**: Plan for a 1-minute hyper-realistic short with a dragon and a hero carrying a real family member's face, built on the Mac Studio with Draw Things + ffmpeg. Covers the pipeline, the Draw Things configuration for every stage, the face-identity strategy, dragon consistency, the shot list, the time budget, and the experiments to run before committing render hours. Living document — update as experiments land.

**Sources**: 2026-09-19-local-4k-video-research.md; [[face-identity-workflows]]; [[runbook-living-painting]]; hands-on measurements 2026-09-20/21. Items marked *verify* have not been tested in Draw Things yet.

**Last updated**: 2026-09-21 (4K delivery added)

---

## 1. What we are making

| | |
|---|---|
| Length | 60 s = **12 shots × 5 s** (81 frames @ 16 fps each). Longer single shots cost more and drift more; 5 s is the sweet spot on this hardware. |
| Look | Photoreal cinematic, not anime. Anamorphic film feel, volumetric light, real skin. |
| Aspect / delivery | **16:9, delivered at 3840×2160 (4K UHD)**. No open model generates good 4K directly on this Mac (see [[image-to-video-models]]), so: generate at **1280×720**, AI-upscale 3× to 3840×2160. Stills are made at 1280×720 too so the I2V source matches. |
| Story | Three acts, four shots each: **Arrival** (hero rides into a burned valley) → **Encounter** (the dragon reveals itself, standoff) → **Bond** (hero and dragon fly together over the coast at dawn). No dialogue; music + SFX. |
| Hero | A family member's face (photo supplied by Kevin 2026-09-21, with her consent assumed as Kevin's household). One consistent character across ~8 of the 12 shots. |
| Dragon | One consistent design across ~7 shots. |

## 2. Pipeline

```
character sheet (hero, dragon)  ──►  per-shot still (FLUX.2 klein + face control)
                                            │
                                            ▼
                               Wan 2.2 I2V 5 s clip (photoreal motion prompt)
                                            │
                          (optional) FaceFusion pass on face-visible shots
                                            │
                                            ▼
                          AI upscale 1280×720 → 3840×2160 (§3e)
                                            │
                                            ▼
                    ffmpeg: xfade concat ×12 → music + SFX → title → 4K HEVC
```

Every stage exists already except the face control and the concat script. Nothing here needs ComfyUI.

## 3. Draw Things configuration per stage

### 3a. Stills — FLUX.2 [klein] 9B (8-bit S), photoreal

| Setting | Value | Notes |
|---|---|---|
| Model | FLUX.2 [klein] 9B (8-bit S) | proven on the farm photo test (2026-09-20) — photoreal kids, guide, pomegranate tree were convincing |
| Steps / CFG / Shift | 4 / 1.0 / 3 | klein defaults |
| Size | **1280×720** (16:9) | matches the I2V size below; FLUX klein is comfortable at 0.9 MP |
| Prompt style | camera + lens + light first, subject second | `Cinematic still, anamorphic 35mm, shallow depth of field, volumetric dawn light, …` No anime suffix |
| Negative | n/a at CFG 1 | fix the still, not the negative |
| Control | face adapter for hero shots (see §4) | *verify which adapters Draw Things lists for FLUX.2 klein* |

### 3b. Motion — Wan 2.2 I2V A14B (8-bit S) pair

Same as the living-painting runbook with three changes for photoreal:

| Setting | Value | Why |
|---|---|---|
| Model / Refiner | High Noise I2V (8-bit S) / Low Noise I2V (8-bit S) @ **10%** | mandatory pair; see the refiner trap in [[runbook-living-painting]]. Keep 10% with the Lightning LoRA — **50% produced noise** (v2, 2026-09-21): the distilled LoRA is trained for the 10% split; the low-noise expert needs ~3 of the 4 steps to clean up |
| LoRA | Lightning High-Noise 100%, 4 steps, CFG 1 | 16 min per clip. Try **8 steps** on one hero close-up to see if skin/face hold better (~30 min) — *experiment E3* |
| Size | **1280×720**, 81 frames @ 16 fps | 1.56× the pixels of 576×1024 → expect **~25 min per clip** (*measure in E6*). 1920×1080 native would be ~3.5× → 55 min/clip and 48 GB is tight; not worth it when the upscaler does the rest |
| Motion prompt | one camera move + one subject action, nothing else | `slow dolly in, the rider turns his head toward the ridge, cloak moving in the wind, embers drifting` — people may move here, but **one** action per shot, and never "walking toward camera" |
| Shift | 5 | |

Camera moves that Wan 2.2 does well at 4 steps: slow dolly/push, slow pan, orbit ≤ 30°, handheld drift. Avoid: whip pans, fast tracking, anything that reveals new geometry.

### 3c. Face pass — FaceFusion (post, optional per shot)

For shots where the hero's face is larger than ~120 px tall, run FaceFusion on the 5 s clip with one reference photo of Kevin, face-enhancer on. It re-locks identity that I2V softened. Runs on Apple Silicon via CoreML *(verify install: `pip install facefusion` or the standalone app)*. Do it **before** upscaling.

### 3d. Upscale to 4K — the step that makes "4K" true

1280×720 → 3840×2160 is exactly **3×**. Lanczos would just be a blurry 4K container; a learned upscaler adds the detail. Candidates, in order to test (*E8*):

| Upscaler | Type | Mac path | Expected |
|---|---|---|---|
| **SeedVR2** | temporal video restorer | ComfyUI node with MPS support (the one ComfyUI use in this project) | best quality, no flicker; memory at 4K unknown → may need tiling |
| **Real-ESRGAN x4plus / RealESRGAN_x4plus_anime** via ncnn | per-frame | `realesrgan-ncnn-vulkan` binary or **REAL Video Enhancer** app | fast, sharp, can shimmer on motion; run at 4× then downscale to 3840 |
| **Draw Things built-in Upscaler** (Settings → Upscaler: Real-ESRGAN / UltraSharp) | per-frame, in-app | applies to generated *images*; whether it upscales all 81 video frames on export is *unverified* | zero setup if it works |
| Topaz Video AI | commercial | Metal-native | reference quality; paid — fallback only |

Order of operations: **FaceFusion → upscale → assemble**. Never upscale before the face pass (3× the pixels to swap) and never assemble first (upscaling the crossfades is wasted work).

Details and Mac notes: [[video-upscaling]].

### 3e. Assembly — ffmpeg

- `xfade` crossfades (0.5 s) or hard cuts between the 12 upscaled clips; no loops
- optional 2.39:1 letterbox bars (3840×1608 picture inside 3840×2160)
- music bed + 3–5 SFX (wing beats, roar, wind, hooves) from Pixabay; `-shortest`
- 2 s title card at the end (FLUX still at 1280×720, upscaled the same way)
- encode **HEVC 10-bit, `hevc_videotoolbox`, ~40 Mbps** for YouTube 4K; keep a ProRes master
- **HDR**: the generators emit 8-bit SDR, so true HDR is not possible. The script gets an `--hdr` flag that produces an **HLG BT.2020** variant via inverse tone-mapping (`zscale` + `tonemap`) for A/B on an HDR TV; if it looks better, upload that, otherwise the SDR master. Default = SDR.

`scripts/assemble_film.sh` — to write when the first 3 clips exist.

## 4. Face identity — the hard part

Ranked for this project. Start at the top; fall through only if it fails the test in §7.

| # | Method | How | Cost | Expected identity hold |
|--:|---|---|---|---|
| 1 | **Face adapter in Draw Things at the still stage** | Control → IP-Adapter FaceID / PuLID / Flux Kontext-style reference *(verify names for FLUX.2 klein; Draw Things ships PuLID for FLUX.1 dev — klein support unknown)* + 1 frontal photo, strength 0.7–0.9 | free, in-app | good on the still; I2V softens it over 5 s |
| 2 | **Face LoRA for FLUX** | 15–30 photos → train. Draw Things has a **PEFT** tab (local LoRA training) *(verify it supports FLUX.2 klein and how long on M4 Max)*; fallback fal.ai trainer ~$5–10 | 1–3 h once | best on stills, reusable across all shots and future projects |
| 3 | **FaceFusion post-swap** (§3c) | swap after I2V | free, ~1 min/clip | re-locks identity; can look pasted on profile angles |
| 4 | **Face LoRA for Wan 2.2** | cloud trainer only | ~$10–20, hours | identity survives motion; most work |

**Recommended stack:** 2 (or 1 if 2 is unavailable) for the still **+ 3 on the 3–4 close-up shots**. That is two independent locks on identity, both free.

**Face reference on disk** (`raw/face/`, git-ignored): `hero_face_head.jpg` (560×700 head crop) and `hero_face_tight.jpg` (1024 px tight face), cropped from `source_beach_selfie.jpg`. One frontal, evenly lit photo — enough for PuLID / IP-Adapter / FaceFusion. A LoRA (method 2, E7) wants 15–30 more with varied angles and expressions.

**Consent/ethics:** own face or a consenting family member only; the hero photo is from Kevin's own family album. Same as [[face-identity-workflows]].

## 5. Dragon consistency

No dragon LoRA exists for these models. Strategy:

1. **Design sheet first.** One FLUX still, 3 views on one canvas: `character design sheet, same dragon from front, side and three-quarter view, …`. Iterate until it is *the* dragon. Save as `raw/dragon/design.png`.
2. **Lock the description.** Write a 40-word dragon paragraph (color, horn shape, wing membrane, scale texture, eye color, size relative to a horse) and paste it verbatim into every dragon shot prompt. Text consistency is 70% of the battle.
3. **Reference control** if available: IP-Adapter (non-face) with the design sheet at ~0.5 strength on every dragon still *(verify)*.
4. **Stage the shots** so the dragon is far, backlit, or partially framed in most of them — silhouette is consistent for free; only 2 shots need the full close design.
5. If it still drifts: train a small dragon LoRA on 20 generated stills of the locked design (same PEFT path as the face).

## 5b. Scene 1 — locked (2026-09-21)

**Reference**: `raw/dragon/ref_scene1_flyby.webp` — reference for the **dragon** (reddish-brown, confirmed). Environment is ours: **setting sun**, not the ref's grey haze.

**Action**: a rider on a dragon high above open sea; a second dragon further back; the camera pushes in on the rider as the dragon flies past.

A 5 s push from "rider is 40 px tall" to "face fills the frame" is a 10× scale change — Wan will warp it. Split into two shots that cut together as one move:

| Shot | Frame | Camera (Wan prompt) | Face |
|---|---|---|---|
| **1A** | Wide, dragon enters frame left, crosses; second dragon small in the haze behind; sea far below | `slow push in, the dragon glides across frame from left to right, wings beating slowly, the distant dragon drifts behind, sea haze, camera slowly tightening` | rider tiny, no face |
| **1B** | Medium, three-quarter from behind-side, rider's upper body + dragon's neck, sea and second dragon beyond | `slow push in toward the rider, wind pulling at cloak and long dark hair, the rider turns to look back over her shoulder, dragon neck rising and falling with wing beats` | **yes** — ends on the face; FaceFusion pass |

Cut 1A → 1B on the wing downbeat. Optional 1C (2 s): tight on the face, eyes narrowing, if E3 shows the face holds.

**Dragon description lock (draft — edit)**: *massive dark reddish-brown dragon, matte ridged scales, long tapered neck, bat-like wing membranes with visible bone struts and torn trailing edges, a row of curved horns sweeping back from the skull, amber eyes, wingspan four times its body length.*

**Still prompt 1A (FLUX.2 klein, 1280×720)**:
`Cinematic film still, anamorphic 35mm, high above an open ocean at sunset, the sun low on the horizon and half-sunk, sky in orange, magenta and deep violet, backlit. A [dragon lock] flies left to right across the frame, wings spread wide, a small armored rider seated at the base of its neck. Far behind it a second dragon, smaller and soft in the sea haze. A long path of sun glitter on the water below, thin streaked clouds lit from beneath, volumetric warm light, photorealistic, highly detailed, shallow depth of field on the distant dragon.`

**Still prompt 1B**: `Cinematic film still, anamorphic 50mm, three-quarter view from behind and beside a rider on the neck of a [dragon lock], sea and haze far below, a second dragon distant in the background. The rider wears dark weathered leather armor with a deep-red cloak streaming behind her, hands on the dragon's neck ridge, looking back over her shoulder toward the camera. Sunset backlight, orange rim light on the rider's shoulder and hair, violet sky, photorealistic, highly detailed.` + face control (E1/E2).

**Hero look (fixed 2026-09-21)**: young woman, long dark hair, dark weathered leather armor, deep-red cloak, no helmet (face must be visible). Same words in every hero prompt; the face itself comes from the adapter/LoRA, never from the prompt.

**Sea/sunset palette** is the same family as the coastal loops — reuse those learnings for the motion prompt (waves, haze drift).

## 6. Shot list (v0 — edit freely)

| # | Act | Shot | Hero face? | Dragon? | Camera | Notes |
|--:|---|---|:-:|:-:|---|---|
| 1A | Open | Wide: dragon + rider fly by high over open sea, second dragon in haze | tiny | **full** | slow push | **locked — see §5b** |
| 1B | Open | Medium: rider on the dragon's neck, turns to camera | **yes** | partial | slow push | **locked — see §5b**; FaceFusion |
| 2 | Arrival | Medium: hero on horseback, cloak, looks up | **yes** | — | slow dolly in | first identity shot |
| 3 | Arrival | Insert: hoof through ash, embers | — | — | static, low | cheap, no faces |
| 4 | Arrival | Wide: ruined village, giant claw marks on a wall | — | trace | slow pan | dragon implied |
| 5 | Encounter | Wide: cliff, a shadow passes over the hero | small | silhouette | static | wing shadow |
| 6 | Encounter | Dragon lands, dust, framed by rocks | — | **full** | slow pull back | design-sheet shot 1 |
| 7 | Encounter | Close: hero's face, wind, ash on cheek | **yes** | — | static, shallow DoF | hero close-up; FaceFusion pass |
| 8 | Encounter | Close: dragon's eye opens, pupil contracts | — | **full** | slow push | design-sheet shot 2 |
| 9 | Bond | Medium: hero reaches out, dragon lowers its head | **yes** | yes | slow orbit | hardest shot — two subjects |
| 10 | Bond | Wide: takeoff, wings blast the dust | small | yes | crane up | |
| 11 | Bond | Aerial: flying over the coast, dawn | small | yes | tracking | reuse coastal palette from earlier projects |
| 12 | Bond | Hero on dragon's back, looks at camera, smiles | **yes** | partial | static | final identity shot; FaceFusion pass |

4 face shots, 7 dragon shots. Shots 3, 4, 5 are cheap; render them first to build the assembly early.

## 7. Experiments before committing (in order)

| # | Question | Test | Pass criterion | Time |
|--:|---|---|---|---|
| E1 | What face controls does Draw Things offer for FLUX.2 klein? | open Control dropdown with klein selected; also check with FLUX.1 dev if klein has none | a face/reference adapter exists | 5 min |
| E2 | Does the adapter hold Kevin's identity on a cinematic still? | shot 7 prompt + adapter, 4 seeds | 3 of 4 recognisably Kevin | 10 min |
| E3 | Does identity survive I2V? 4 vs 8 steps | shot 7 still → I2V at 4 steps and at 8 steps | face at frame 81 still reads as Kevin | 16 + 30 min |
| E4 | FaceFusion on Apple Silicon | install, run on E3 output | runs; result better than E3 | 30 min |
| E5 | Dragon design sheet + description lock | 2 dragon stills from the locked paragraph, different scenes | same dragon | 10 min |
| E6 | Photoreal I2V motion at 1024×576 | shot 1 (no faces) | no warping, camera move reads | 16 min |
| E7 | PEFT tab: can Draw Things train a FLUX LoRA locally? | check tab, start a 20-image run | finishes in < 3 h | *verify* |
| E8 | Which upscaler gets 1280×720 → 4K looking real? | run the E6 clip through SeedVR2, Real-ESRGAN ncnn, and Draw Things' upscaler; compare a still frame at 100% | skin and scales gain detail, no flicker across 10 frames | 1 h |

E1–E2 decide the face strategy. E5–E6 decide whether the dragon look is achievable. Do all seven before rendering the shot list.

## 7b. Experiment results

| # | Date | Result |
|--:|---|---|
| E6 | 2026-09-21 | Scene 1A still at 1280×768 (FLUX klein, first seed) matched the brief. I2V at 1280×768 × 81 f: **~43 min** with the upscaler test sharing the GPU for ~10 min; estimate **~35 min clean**. Twice the 576×1024 cost. |
| E6 follow-up | 2026-09-21 | **Ghosting** (translucent double dragon head/wing/rider) from ~frame 55 of scene 1A, once the dragon fills the frame. Present in the Wan output, not the upscale. Diagnosis: **Refiner Start 10%** gives the High-Noise expert (motion/layout) ~0.4 of 4 steps — fine for calm landscapes, fails on a large fast subject. Wan 2.2's documented split is 50/50. Fix to test: Refiner Start 50%, LoRA 0.8, gentler motion prompt. |
| E6 v2 | 2026-09-21 | Refiner 50% + LoRA 80% + gentle prompt → **washed-out noisy silhouette**. Wrong lever: the Lightning LoRA is trained for the 10% split, and at 50% the low-noise expert gets only 2 steps. **Refiner stays at 10%.** v3 plan: 10%, LoRA 100%, motion prompt with no camera move and no "across the frame" — the ghosting in v1 most likely came from asking a full-frame subject to translate a long distance in 5 s. |
| E8 (part) | 2026-09-21 | **Real-ESRGAN ncnn (x4plus)** works on Metal with `-t 128 -j 1:1:1`, run from its own directory (models path is cwd-relative); auto/256 tile segfaults. **81 frames at 1280×768 → 4K in 5.6 min** on a free GPU. 1:1 comparison vs lanczos: scale ridges and spine edges resolve, no ringing. Script: `scripts/upscale_4k.sh` → HEVC 10-bit 40 Mbps. **Good enough to ship**; SeedVR2 only if flicker shows up on motion. First 4K clip: `raw/clips/dragon/scene1a_4k.mp4`. |

## 8. Budget

| Item | Estimate |
|---|---|
| Stills, all shots incl. iteration (~5 seeds each) | 60 × 40 s ≈ **40 min** |
| I2V, 12 clips × ~25 min at 1280×720 | **5 h** unattended |
| Re-renders (assume 4 shots need a second pass) | +1.7 h |
| 4K upscale, 12 clips (SeedVR2 on MPS, est. 3–8 min each) | ~1 h |
| FaceFusion, 4 shots | 10 min |
| Assembly, music, titles | 30 min |
| Experiments E1–E8 | ~3.5 h |
| **Total** | **≈ 12 h machine time**, spread over 3–4 sessions |

Rendering is unattended and survives a screen lock; the session holds a keep-awake so the Mac cannot idle-sleep mid-render.

## 9. Risks

- **Face drift over 5 s** — mitigated by FaceFusion; if still bad, shorten face shots to 49 frames (3 s).
- **Dragon changes between shots** — mitigated by description lock + silhouette staging; LoRA as last resort.
- **Two-subject shot (9)** — highest failure odds; have a fallback framing (dragon head only, hero's hand in frame).
- **Photoreal humans at 4 steps** — hands and eyes. Keep hands out of frame or holding reins; no waving.
- **Hardware time** — 12 h is fine; 25 h is not. Cap re-renders at one per shot, then accept or cut the shot.
- **4K upscale memory** — SeedVR2 at 3840×2160 may exceed 48 GB unified; fall back to tiled mode or Real-ESRGAN. Test on one clip (E8) before the batch.
- **1280×720 I2V unmeasured** — if E6 shows > 35 min/clip, drop to 1024×576 and upscale 3.75× instead; the upscaler cost is the same.

## 10. Open questions for Kevin

1. Photos: ~~can you drop 15–30 face photos?~~ → one frontal reference supplied 2026-09-21; more only if E7 (LoRA) goes ahead.
2. Hero look: ~~armor / cloak / modern?~~ → weathered leather + red cloak, no helmet (settled 2026-09-21).
3. Dragon: ~~color~~ reddish-brown (settled 2026-09-21). Vibe still open: menacing-then-loyal, or noble throughout?
4. Music: orchestral epic, or ambient like the loops?
5. Deliverable: YouTube 16:9 at 4K UHD, SDR master + optional HLG variant — confirmed 2026-09-21.

## Related pages
- [[character-consistency]]
- [[face-identity-workflows]]
- [[runbook-living-painting]]
- [[projects]]
- [[wan22-i2v-locked-image-settings]]
- [[video-upscaling]]
