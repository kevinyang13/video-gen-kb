# Kyle's Antarctic Rescue — 1-Minute Headless Plan

**Summary**: Plan for a 60-second illustrated short made from a 5-panel comic: Kyle, a boy on an Antarctic expedition, sees a UFO attacking the ice, rescues the animals with a freeze-ray gadget and ends hugging a penguin chick. Rendered **entirely with `draw-things-cli`**: comic panels become cleaned first frames through klein img2img, LTX-2.3 animates each one, and the existing scripts handle the 4K upscale and the final cut. No Draw Things window, no Moodboard.

**Sources**: `raw/kyle/comic_source.webp` (the 5-panel comic, 1024×1536, added 2026-09-22); [[headless-cli-pipeline]] §1b (CLI flags and timings measured 2026-09-22); [[lost-city-plan]] §3c, §7b (LTX production settings and motion rules); [[character-consistency]]; [[scripts-reference]]. Timings below are estimates built from the Lost City measurements, **not yet measured on this project**.

**Last updated**: 2026-09-22 (plan written, nothing rendered)

---

## 1. What the source gives us

| Panel | Story beat | Kyle in frame? | Text to remove |
|---|---|---|---|
| 1 "A brave boy with a big dream" | Kyle on the ice, expedition ship behind, thumbs up | face, frontal close-up | title box, thought bubble, caption box |
| 2 "A mysterious UFO appears" | night, Kyle seen from behind looking up at a saucer firing purple beams at the ice | back of head only | title, "Wow! A UFO?!", caption |
| 3 "Animals in danger" | penguins, seal, orca, whale; beams lifting ice blocks | no | title, "Help!", caption |
| 4 "Kyle to the rescue!" | Kyle flying, freeze-ray with a snowflake glow, penguin sidekick | face, ¾ | title, bubble, 4 starbursts, caption |
| 5 "A happy ending" | sunrise, Kyle hugging a chick among penguins, seal, whale, orca, wooden sign | face, frontal | title, caption, slogan (sign is part of the scene) |

The comic already fixes the character design, the palette and every composition. That is the main asset: instead of generating Kyle from text and hoping he stays the same, **each Kyle shot starts from a panel that already shows him.** Identity comes in as pixels, which is the strongest channel in [[identity-conditioning]].

Style: keep the look — hand-painted comic illustration, bold ink lines, vivid saturated colour. Not photoreal. Illustration hides the small face drift that I2V causes over 10 s, and it matches the source.

> Kyle looks like a real child. Use a real child's likeness only with the parent's consent, and keep the film private unless they decide otherwise.

## 2. Why the CLI changes the plan

From [[headless-cli-pipeline]] §1b, measured on this Mac:

- the released CLI (`1.20260430.0`) takes **one** `--image`. With `--strength < 1` it is img2img on a still model, and with `--frames` on LTX it is true image-to-video (frame 0 = the image, pixel for pixel);
- **no Moodboard** — multi-reference `--image` exists only on `main`;
- LTX 249 frames (10 s) takes **9 min 41 s**, about 2× faster than the app; a klein still takes 27–35 s.

So consistency can't come from reference images the way it did on Lost City. It comes from three things the CLI *can* do:

1. **Panel → img2img.** The cropped panel is the `--image`, at strength 0.45–0.6. Klein keeps the layout, the face and the parka, repaints the parts under the removed text and adds detail at 1024×576.
2. **A text lock** pasted verbatim into every prompt (§4).
3. **Chaining.** For the non-panel shots next to Kyle shots, the last frame of the previous clip becomes the next `--image` (see [[character-consistency]] §6).

Fallback if img2img loses Kyle's face: build the CLI from `main` (`brew install --HEAD`, Swift-version friction reported) to get multi-`--image`, or do only the 3 Kyle stills in the app's Moodboard and everything else from the CLI.

## 3. Pipeline

```
comic_source.webp
  │ ffmpeg crop per panel → delogo over bubbles/captions → 2× lanczos        (§5 step 1–2)
  ▼
panel_N_clean.png ──draw-things-cli klein img2img, strength 0.45–0.6────────┐
text-only shots  ──draw-things-cli klein txt2img (style lock, no Kyle close-up)┤ 1024×576 still, 3 seeds
                                                                             ▼
                    draw-things-cli LTX-2.3 --image still --frames 249 → sN_ltx_v1.mov (ProRes + audio)
                                                                             ▼
                    ffmpeg trim → upscale_4k.sh (realesr-animevideov3-x4) → remux audio
                                                                             ▼
                    assemble_film.sh XFADE=0.75 MUSIC=… → kyle_rescue_4k.mp4 (+ drawtext captions)
```

## 4. Locks (paste verbatim, never paraphrase)

- **style_head**: `Hand-painted comic book illustration, bold clean ink outlines, soft cel shading, vivid saturated colours, bright cheerful children's storybook style.`
- **kyle**: `Kyle, a cheerful young East Asian boy with short spiky black hair, dark brown eyes and a wide smile, wearing a bright red and black insulated expedition parka with a round blue Antarctica patch on the left chest, black backpack straps over both shoulders, black gloves.`
- **world**: `Antarctica: turquoise icebergs, snowy white mountains, deep blue polar ocean.`
- **video tail** (LTX): `Smooth gentle motion, consistent character, hand-painted animated illustration style, no text, no speech bubbles.`
- **rules**: never ask for readable text from the model — titles and captions are added with ffmpeg. Kyle's face shots use hold-position wording (Lost City close-up rule: a "step" walks the subject out of frame). Fast action drifts after ~4–5 s: trim.

## 5. Step-by-step

### Step 0 — project record
Add `kyle_rescue` to `projects.json` (done at plan time, status `planned`). Every still and clip lands in `raw/clips/kyle/`.

### Step 1 — crop the panels
Approximate panel boxes in the 1024×1536 source (measure and correct on the first run):

| Panel | ffmpeg crop (w:h:x:y) |
|---|---|
| 1 | `506:470:6:6` |
| 2 | `500:470:518:6` |
| 3 | `534:514:6:486` |
| 4 | `488:514:530:486` |
| 5 | `1012:520:6:1010` |

```bash
mkdir -p raw/clips/kyle
ffmpeg -i raw/kyle/comic_source.webp -vf "crop=506:470:6:6" raw/clips/kyle/p1_crop.png
```

These are whole-panel boxes. The CLI center-crops `--image` to the output aspect, so a near-square panel fed at 1024×576 silently loses its top and bottom strips. Cut the 16:9 window yourself instead (panel 1: `crop=506:285:6:100` skips the title box and most of the caption), so you choose what goes — title and caption boxes mostly sit in those strips anyway.

### Step 2 — remove the text
Speech bubbles and starbursts sit inside the 16:9 area. Cover each with ffmpeg `delogo` (it fills the box from the pixels around it), then 2× lanczos so klein gets a 1024-wide input:

```bash
ffmpeg -i raw/clips/kyle/p1_crop.png \
  -vf "delogo=x=290:y=0:w=210:h=150,scale=1024:-1:flags=lanczos" \
  raw/clips/kyle/p1_clean.png
```

The smear left by `delogo` doesn't matter: klein repaints it in step 3. Box coordinates are per panel — read them off the crop.

### Step 3 — stills with klein (CLI)

```bash
# panel shot: img2img from the cleaned panel
draw-things-cli generate -m flux_2_klein_9b_i8x.ckpt \
  --prompt-file raw/clips/kyle/s2_still.txt \
  --image raw/clips/kyle/p1_clean.png --strength 0.5 \
  --width 1024 --height 576 --steps 4 --cfg 1 --seed 1 \
  --config-json '{"shift":3.0,"sampler":16}' \
  --offline --disable-preview -o raw/clips/kyle/s2_still_v1.png

# text-only shot: same command without --image/--strength
```

Loop over `--seed 1 2 3` and keep the best. Strength guide: 0.4 ≈ panel redrawn cleaner; 0.6 ≈ more painterly detail with the pose kept; > 0.7 Kyle starts turning into a different boy (*to verify in K0*).

### Step 4 — motion with LTX-2.3 (CLI)

```bash
draw-things-cli generate -m ltx_2.3_22b_distilled_1.1_q8p.ckpt \
  --prompt-file raw/clips/kyle/s2_video.txt \
  --image raw/clips/kyle/s2_still_v1.png \
  --width 1024 --height 576 --frames 249 --steps 8 --cfg 1 --seed 1 \
  --config-json '{"sampler":19,"shift":5.0,"stochasticSamplingGamma":0.3,"fps":25,"hiresFix":false}' \
  --offline --disable-preview --video-format prores422hq \
  -o raw/clips/kyle/s2_ltx_v1.mov
```

Always render 249 frames: same cost per clip as a shorter one in practice (Lost City §7b), and the trim happens in the edit. Progress is a TTY spinner — a redirected log stays empty until the process exits.

### Step 5 — trim, upscale, remux

```bash
ffmpeg -i raw/clips/kyle/s2_ltx_v1.mov -t 8 -c copy raw/clips/kyle/s2_ltx_v1_t.mov
scripts/upscale_4k.sh raw/clips/kyle/s2_ltx_v1_t.mov s2 realesr-animevideov3-x4
ffmpeg -i s2_4k.mp4 -i raw/clips/kyle/s2_ltx_v1_t.mov -map 0:v -map 1:a -c:v copy -c:a aac s2_4k_audio.mp4
```

Use the **anime** Real-ESRGAN model: it is built for flat-shaded line art and runs faster than x4plus ([[scripts-reference]]). `upscale_4k.sh` drops audio — the remux line restores LTX's ambience. Never upscale while LTX is rendering.

### Step 6 — assemble

```bash
XFADE=0.75 MUSIC=raw/clips/music/<track>.mp3 \
  scripts/assemble_film.sh raw/clips/kyle/kyle_rescue_4k.mp4 s1_4k_audio.mp4 … s8_4k_audio.mp4
```

Then burn the title and the five story captions with `drawtext` (one lower-third per beat, 3–4 s each), and the end card "The End ♥".

### Step 7 — batch it
Once the per-shot commands work, write `scripts/dt_render.sh <project> <scene>` (proposed in [[headless-cli-pipeline]] §5): read the locks and the scene's prompts from `projects.json`, write the prompt files, run step 3 over 3 seeds and step 4 on the chosen still. Stills first (≈ 12 min, pick by eye), then one `for` loop renders all 8 clips overnight — no screen lock, no app.

## 6. Shot list (60 s)

8 clips, 7 crossfades of 0.75 s. Kept lengths add up to ~65 s, ~60 s after the fades.

| # | Keep | Source | Still | Motion (LTX prompt core) |
|---|---|---|---|---|
| S1 | 7 s | text-only | Expedition ship "Antarctica Expedition" on a turquoise sea between icebergs, seagulls, wide | slow push toward the ship, gulls glide, gentle swell, ice creaks; wind, gulls |
| S2 | 8 s | panel 1 | Kyle close-up, ship behind, thumbs up (bubble removed) | Kyle holds his place, smiles wider, thumbs-up bobs once, hair and parka hood stir in the wind; camera still |
| S3 | 10 s | panel 2 | night, Kyle from behind, saucer overhead | foreground still (Kyle only turns his head a little), saucer hovers and pulses, purple beams crackle onto the ice, ice glows and cracks; low hum, electric crackle |
| S4 | 10 s | panel 3 | penguins, seal, orca, whale on breaking ice | slow background violence: ice blocks rise into the beams, floes split, penguins huddle and flap, seal looks up; the s10/s14 Lost City pattern — slow foreground, violent background |
| S5 | 6 s | panel 4 | Kyle mid-air aiming the freeze-ray, penguin sidekick | Kyle glides forward, the gadget fires a bright blue snowflake beam, frost spreads across the frame; trim at the first sign of drift |
| S6 | 6 s | last frame of S5 → text-only fallback | the saucer frozen in blue ice, beams gone | ice crust cracks, saucer shakes free and zips away up into the stars, light fades |
| S7 | 10 s | panel 5 | sunrise, Kyle hugging the chick, animals around, whale breaching | slow and warm: Kyle hugs and rocks gently, chick nuzzles, penguins bob, whale arcs behind; soft wind, lapping waves, happy penguin calls |
| S8 | 8 s | text-only | Wide sunrise over the ice, the wooden "protect our ocean" sign in the foreground, small figure and penguins far away | slow pull-back and rise; end card text from ffmpeg over the last 4 s |

S2, S5 and S7 are the only face shots; S3 shows Kyle from behind (identity from wardrobe, free).

## 7. Experiments (run before the batch)

| # | Question | Test | Pass |
|---|---|---|---|
| K0 | Does img2img keep Kyle? | panel 1 at strength 0.4 / 0.5 / 0.6, seed 1 | the boy reads as the same kid; bubble area painted over |
| K1 | Does LTX keep the illustrated style? | S2 clip | no drift to photoreal or 3D over 10 s; if it drifts, add "2D" and "flat colour" to the tail, or try Wan 2.2 via CLI with `refinerModel` |
| K2 | Face drift over 10 s | S2 and S7 | face and parka unchanged at frame 249; else trim to 5–6 s |
| K3 | Fast action | S5 | clean for ≥ 5 s |
| K4 | Chaining | last frame of S5 → S6 | saucer and frost carry over |
| K5 | Upscaler | anime vs x4plus on S2 | pick by eye; anime expected cleaner lines |

## 8. Budget (estimate)

| Stage | Count | Each | Total |
|---|---|---|---|
| klein stills | 8 shots × 3 seeds + K0 sweep | ~30 s | ~15 min |
| LTX clips | 8 + ~50% retries | 9 min 41 s | ~2 h |
| Upscale (trimmed clips, ~65 s total ≈ 1 625 frames) | 8 | ~13 frames/min (81 f ≈ 6 min) | ~2 h |
| Assembly + captions | 1 | — | ~10 min |

About **4–5 h of machine time**, mostly unattended, plus ~1 h of picking stills and trims.

## 9. Open questions for Kevin

1. **Aspect**: 16:9 3840×2160 (YouTube, like Lost City), or 9:16 for phone? The comic panels are near-square, so either works; 9:16 would change every crop.
2. **Captions**: burn the comic's own caption lines as lower-thirds, or picture and music only?
3. **Voice**: narration of the captions? No local TTS is set up yet — would need a new tool.
4. **Music**: which bed from `raw/clips/music/` — something bright and adventurous rather than the orchestral Lost City theme.

## Related pages
- [[headless-cli-pipeline]] — the CLI, its flags, and the measured timings this plan relies on
- [[lost-city-plan]] — LTX production settings and motion rules
- [[character-consistency]] · [[identity-conditioning]] — why panel pixels beat text for identity
- [[face-identity-workflows]] — if the face drifts
- [[scripts-reference]] — `upscale_4k.sh`, `assemble_film.sh`
- [[projects]] — the `kyle_rescue` record
