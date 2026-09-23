# Kyle's Antarctic Rescue — 1-Minute Headless Plan

**Summary**: Plan for a 60-second **vertical (9:16)** illustrated short made from a 5-panel comic: Kyle, a boy on an Antarctic expedition, sees a UFO attacking the ice, rescues the animals with a freeze-ray gadget and ends hugging a penguin chick. Rendered **entirely with `draw-things-cli`**: comic panels become cleaned first frames through klein img2img, LTX-2.3 animates each one, and the existing scripts handle the 4K upscale and the final cut. Pictures and music only — no captions, no narration, no sound effects. No Draw Things window, no Moodboard.

**Sources**: `raw/kyle/comic_source.webp` (the 5-panel comic, 1024×1536, added 2026-09-22); [[headless-cli-pipeline]] §1b (CLI flags and timings measured 2026-09-22); [[lost-city-plan]] §3c, §7b (LTX production settings and motion rules); [[character-consistency]]; [[scripts-reference]]. Timings below are estimates built from the Lost City measurements, **not yet measured on this project**.

**Last updated**: 2026-09-22 (Kevin's answers folded in: 9:16, music only, no narration; nothing rendered yet)

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

> Kyle is Kevin's son; consent is Kevin's (confirmed 2026-09-22). Sharing is his call.

## 2. Why the CLI changes the plan

From [[headless-cli-pipeline]] §1b, measured on this Mac:

- the released CLI (`1.20260430.0`) takes **one** `--image`. With `--strength < 1` it is img2img on a still model, and with `--frames` on LTX it is true image-to-video (frame 0 = the image, pixel for pixel);
- **no Moodboard** — multi-reference `--image` exists only on `main`;
- LTX 249 frames (10 s) takes **9 min 41 s**, about 2× faster than the app; a klein still takes 27–35 s.

So consistency can't come from reference images the way it did on Lost City. It comes from three things the CLI *can* do:

1. **Panel → img2img.** The cropped panel is the `--image`, at strength 0.45–0.6. Klein keeps the layout, the face and the parka, repaints the parts under the removed text and adds detail at 576×1024.
2. **A text lock** pasted verbatim into every prompt (§4).
3. **Chaining.** For the non-panel shots next to Kyle shots, the last frame of the previous clip becomes the next `--image` (see [[character-consistency]] §6).

Fallback if img2img loses Kyle's face: build the CLI from `main` (`brew install --HEAD`, Swift-version friction reported) to get multi-`--image`, or do only the 3 Kyle stills in the app's Moodboard and everything else from the CLI.

## 2b. Decisions (Kevin, 2026-09-22)

| Question | Answer | What it changes |
|---|---|---|
| Aspect | **9:16 for phones** | stills and clips at **576×1024**; master 2160×3840, delivery copy 1080×1920; both scripts need a portrait option (step 5a); every panel crop changes (step 1) |
| Text on screen | **none** — pictures and music | no captions, no title, no end card; bubbles and caption boxes still have to be painted out |
| Narration | **none** | no TTS tool needed |
| Sound | music only | LTX's generated audio is discarded, so the remux step goes away; `assemble_film.sh` pads mute clips with silence under `MUSIC` |
| Consent | Kyle is Kevin's son | settled |
| Music | *still open* | on disk: `mystical_flute`, `dragons_breath`, `calm_ambient_dreamscape`, `neon_synthwave_drive` — none is bright and adventurous; pick one or add a new track |

## 3. Pipeline

```
comic_source.webp
  │ ffmpeg: 9:16 window per panel (tight crop, or pad-and-repaint) → delogo bubbles → scale to 576 wide   (§5 step 1–2)
  ▼
panel_N_clean.png ──draw-things-cli klein img2img, strength 0.45–0.7────────┐
text-only shots  ──draw-things-cli klein txt2img (style lock, no Kyle close-up)┤ 576×1024 still, 3 seeds
                                                                             ▼
                    draw-things-cli LTX-2.3 --image still --frames 249 → sN_ltx_v1.mov (audio ignored)
                                                                             ▼
                    ffmpeg trim → upscale_4k.sh W=2160 H=3840 (realesr-animevideov3-x4)
                                                                             ▼
                    assemble_film.sh W=2160 H=3840 XFADE=0.75 MUSIC=… → kyle_rescue_2160x3840.mp4
                                                                             ▼
                    ffmpeg scale 1080:1920 → kyle_rescue_1080x1920.mp4 (phone delivery)
```

## 4. Locks (paste verbatim, never paraphrase)

- **style_head**: `Hand-painted comic book illustration, bold clean ink outlines, soft cel shading, vivid saturated colours, bright cheerful children's storybook style.`
- **kyle**: `Kyle, a cheerful young East Asian boy with short spiky black hair, dark brown eyes and a wide smile, wearing a bright red and black insulated expedition parka with a round blue Antarctica patch on the left chest, black backpack straps over both shoulders, black gloves.`
- **world**: `Antarctica: turquoise icebergs, snowy white mountains, deep blue polar ocean.`
- **video tail** (LTX): `Smooth gentle motion, consistent character, hand-painted animated illustration style, no text, no speech bubbles.`
- **rules**: never ask for readable text from the model — the film has no on-screen text at all. Kyle's face shots use hold-position wording (Lost City close-up rule: a "step" walks the subject out of frame). Fast action drifts after ~4–5 s: trim.

## 5. Step-by-step

### Step 0 — project record
Add `kyle_rescue` to `projects.json` (done at plan time, status `planned`). Every still and clip lands in `raw/clips/kyle/`.

### Step 1 — cut a 9:16 window from each panel
Whole-panel boxes in the 1024×1536 source (approximate — measure on the first run):

| Panel | panel box (w:h:x:y) | 9:16 method | Why |
|---|---|---|---|
| 1 | `506:470:6:6` | **B pad** | a tight 264-wide window loses the thumbs-up |
| 2 | `500:470:518:6` | **A tight** `264:470:~560:6` | Kyle's head bottom, saucer top — already a vertical composition |
| 3 | `534:514:6:486` | **B pad** | the animals are spread across the panel |
| 4 | `488:514:530:486` | **B pad** | Kyle and the gadget run diagonally across the width |
| 5 | `1012:520:6:1010` | **A tight** `292:520:~270:1010` | Kyle hugging the chick fills a vertical window by itself |

The panels are near-square, so a 9:16 window is either narrow or needs new picture above and below.

- **A — tight crop.** Cut `h×9/16` wide around the subject. Only ~260–290 px wide, so klein at 576 wide is working from a 2× upscale: expect softer detail, fix it with strength 0.55–0.6.
- **B — pad and repaint.** Keep the full panel width, extend to 9:16 with a blurred, stretched copy of the panel behind it, and let klein paint real sky and ice into the padding at strength 0.65–0.7. Keeps the whole composition; the risk is Kyle changing at that strength (K0 measures it).

```bash
mkdir -p raw/clips/kyle
# A: tight
ffmpeg -i raw/kyle/comic_source.webp -vf "crop=292:520:270:1010" raw/clips/kyle/p5_crop.png
# B: pad (panel 1 → 506 wide × 900 tall, blurred copy behind, panel centred)
ffmpeg -i raw/kyle/comic_source.webp -filter_complex \
  "[0]crop=506:470:6:6,split[a][b];[a]scale=506:900,boxblur=30[bg];[bg][b]overlay=0:(H-h)/2" \
  raw/clips/kyle/p1_crop.png
```

Always hand the CLI an image that is already 9:16: it center-crops `--image` to the output aspect, and on a square panel that would silently throw away the sides.

### Step 2 — remove the text
Speech bubbles, starbursts and caption boxes inside the window get covered with ffmpeg `delogo` (it fills the box from the pixels around it), then scaled to 576 wide so klein gets the output size:

```bash
ffmpeg -i raw/clips/kyle/p1_crop.png \
  -vf "delogo=x=290:y=215:w=210:h=150,scale=576:1024:flags=lanczos" \
  raw/clips/kyle/p1_clean.png
```

The smear left by `delogo` doesn't matter: klein repaints it in step 3. Box coordinates are per panel — read them off the crop.

### Step 3 — stills with klein (CLI)

```bash
# panel shot: img2img from the cleaned panel
draw-things-cli generate -m flux_2_klein_9b_i8x.ckpt \
  --prompt-file raw/clips/kyle/s2_still.txt \
  --image raw/clips/kyle/p1_clean.png --strength 0.5 \
  --width 576 --height 1024 --steps 4 --cfg 1 --seed 1 \
  --config-json '{"shift":3.0,"sampler":16}' \
  --offline --disable-preview -o raw/clips/kyle/s2_still_v1.png

# text-only shot: same command without --image/--strength
```

Loop over `--seed 1 2 3` and keep the best. Strength guide: 0.4 ≈ panel redrawn cleaner; 0.6 ≈ more painterly detail with the pose kept; 0.65–0.7 needed to paint real picture into method-B padding; > 0.7 Kyle probably starts turning into a different boy (*to verify in K0*).

### Step 4 — motion with LTX-2.3 (CLI)

```bash
draw-things-cli generate -m ltx_2.3_22b_distilled_1.1_q8p.ckpt \
  --prompt-file raw/clips/kyle/s2_video.txt \
  --image raw/clips/kyle/s2_still_v1.png \
  --width 576 --height 1024 --frames 249 --steps 8 --cfg 1 --seed 1 \
  --config-json '{"sampler":19,"shift":5.0,"stochasticSamplingGamma":0.3,"fps":25,"hiresFix":false}' \
  --offline --disable-preview --video-format prores422hq \
  -o raw/clips/kyle/s2_ltx_v1.mov
```

Always render 249 frames: same cost per clip as a shorter one in practice (Lost City §7b), and the trim happens in the edit. 576×1024 is the same pixel count as Lost City's 1024×576, so expect the same ~10 min per clip (*portrait LTX not yet tested here*). The clip comes with LTX audio; it is simply not used. Progress is a TTY spinner — a redirected log stays empty until the process exits.

### Step 5a — prerequisite: portrait output in the two scripts
Both scripts hardcode landscape — `upscale_4k.sh` scales and crops to `3840:2160`, and `assemble_film.sh` conforms every clip to `3840:2160`. Fed a 576×1024 clip, both would crop it to a landscape strip. Before the batch, add `W`/`H` env vars (default 3840/2160) to both, and pass `W=2160 H=3840`. Also update [[scripts-reference]].

### Step 5 — trim and upscale

```bash
ffmpeg -i raw/clips/kyle/s2_ltx_v1.mov -t 8 -an -c:v copy raw/clips/kyle/s2_ltx_v1_t.mov
W=2160 H=3840 scripts/upscale_4k.sh raw/clips/kyle/s2_ltx_v1_t.mov s2 realesr-animevideov3-x4
```

Use the **anime** Real-ESRGAN model: it is built for flat-shaded line art and runs faster than x4plus ([[scripts-reference]]). No audio remux — music only. Never upscale while LTX is rendering.

### Step 6 — assemble and deliver

```bash
W=2160 H=3840 XFADE=0.75 MUSIC=raw/clips/music/<track>.mp3 \
  scripts/assemble_film.sh raw/clips/kyle/kyle_rescue_2160x3840.mp4 s1_4k.mp4 … s8_4k.mp4
ffmpeg -i raw/clips/kyle/kyle_rescue_2160x3840.mp4 -vf scale=1080:1920:flags=lanczos \
  -c:v hevc_videotoolbox -b:v 12M -tag:v hvc1 -c:a copy raw/clips/kyle/kyle_rescue_1080x1920.mp4
```

Fade the music out over the last 2 s. No text overlays.

### Step 7 — batch it
Once the per-shot commands work, write `scripts/dt_render.sh <project> <scene>` (proposed in [[headless-cli-pipeline]] §5): read the locks and the scene's prompts from `projects.json`, write the prompt files, run step 3 over 3 seeds and step 4 on the chosen still. Stills first (≈ 12 min, pick by eye), then one `for` loop renders all 8 clips overnight — no screen lock, no app.

## 6. Shot list (60 s)

8 clips, 7 crossfades of 0.75 s. Kept lengths add up to ~65 s, ~60 s after the fades.

| # | Keep | Source | Still | Motion (LTX prompt core) |
|---|---|---|---|---|
| S1 | 7 s | text-only | Tall frame: expedition ship small at the bottom on a turquoise sea, towering iceberg and sky above, seagulls | slow tilt down from the gulls to the ship, gentle swell |
| S2 | 8 s | panel 1 | Kyle close-up, ship behind, thumbs up (bubble removed) | Kyle holds his place, smiles wider, thumbs-up bobs once, hair and parka hood stir in the wind; camera still (method B keeps the thumb in frame) |
| S3 | 10 s | panel 2 | night, Kyle from behind, saucer overhead | foreground still (Kyle only turns his head a little), saucer hovers and pulses at the top of the frame, purple beams crackle down onto the ice, ice glows and cracks — suits 9:16: boy at the bottom, threat at the top |
| S4 | 10 s | panel 3 | penguins, seal, orca, whale on breaking ice | slow background violence: ice blocks rise into the beams, floes split, penguins huddle and flap, seal looks up; the s10/s14 Lost City pattern — slow foreground, violent background |
| S5 | 6 s | panel 4 | Kyle mid-air aiming the freeze-ray, penguin sidekick | Kyle glides forward, the gadget fires a bright blue snowflake beam, frost spreads across the frame; trim at the first sign of drift |
| S6 | 6 s | last frame of S5 → text-only fallback | the saucer frozen in blue ice, beams gone | ice crust cracks, saucer shakes free and zips away up into the stars, light fades |
| S7 | 10 s | panel 5 | sunrise, Kyle hugging the chick (tight vertical window) | slow and warm: Kyle hugs and rocks gently, chick nuzzles, penguins bob at the edges, sun glints behind |
| S8 | 8 s | text-only | Tall sunrise frame: sky and sun above, a whale's tail and a line of penguins with a small boy far away on the ice below | slow rise into the sky as the music ends |

S2, S5 and S7 are the only face shots; S3 shows Kyle from behind (identity from wardrobe, free).

## 7. Experiments (run before the batch)

| # | Question | Test | Pass |
|---|---|---|---|
| K0 | Does img2img keep Kyle — and which 9:16 method? | panel 1 via method B at strength 0.55 / 0.65 / 0.75, panel 5 via method A at 0.45 / 0.55 / 0.65, seed 1 | the boy reads as Kyle; padding becomes real sky/ice; bubble area painted over |
| K1 | Does LTX keep the illustrated style? | S2 clip | no drift to photoreal or 3D over 10 s; if it drifts, add "2D" and "flat colour" to the tail, or try Wan 2.2 via CLI with `refinerModel` |
| K2 | Face drift over 10 s | S2 and S7 | face and parka unchanged at frame 249; else trim to 5–6 s |
| K3 | Fast action | S5 | clean for ≥ 5 s |
| K4 | Chaining | last frame of S5 → S6 | saucer and frost carry over |
| K5 | Upscaler | anime vs x4plus on S2 | pick by eye; anime expected cleaner lines |
| K6 | Portrait LTX | S2 at 576×1024 | renders in ~10 min, motion as good as landscape |

## 8. Budget (estimate)

| Stage | Count | Each | Total |
|---|---|---|---|
| klein stills | 8 shots × 3 seeds + K0 sweep | ~30 s | ~15 min |
| LTX clips | 8 + ~50% retries | 9 min 41 s | ~2 h |
| Upscale (trimmed clips, ~65 s total ≈ 1 625 frames) | 8 | ~13 frames/min (81 f ≈ 6 min) | ~2 h |
| Script change (step 5a) | 1 | — | ~15 min, once |
| Assembly + delivery copy | 1 | — | ~10 min |

About **4–5 h of machine time**, mostly unattended, plus ~1 h of picking stills and trims.

## 9. Open questions for Kevin

1. **Music**: which track? The four on disk are all mood or synth; a bright, adventurous one would need adding.
2. ~~Aspect~~ 9:16 · ~~Captions~~ none · ~~Voice~~ none · ~~Consent~~ Kevin's son — answered 2026-09-22 (§2b).

## Related pages
- [[headless-cli-pipeline]] — the CLI, its flags, and the measured timings this plan relies on
- [[lost-city-plan]] — LTX production settings and motion rules
- [[character-consistency]] · [[identity-conditioning]] — why panel pixels beat text for identity
- [[face-identity-workflows]] — if the face drifts
- [[scripts-reference]] — `upscale_4k.sh`, `assemble_film.sh`
- [[projects]] — the `kyle_rescue` record
