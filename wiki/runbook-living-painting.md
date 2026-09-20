# Runbook: Living-Painting Video (next time, start here)

**Summary**: The exact click-by-click sequence to produce a 27 s TikTok-style animated painting on this Mac, with every gotcha hit on 2026-09-20 baked in as a checklist item. Narrative and measurements live on [[living-painting-loop]]; this page is only the steps.

**Sources**: 2026-09-19-local-4k-video-research.md; hands-on sessions 2026-09-20.

**Last updated**: 2026-09-20

---

## Budget

| Stage | Time | Tool |
|---|---|---|
| Still | ~1 min per seed | Draw Things, FLUX.2 klein 9B |
| Downscale | seconds | ffmpeg |
| I2V | **~15 min** at 576×1024 × 81 f | Draw Things, Wan 2.2 I2V |
| Loop + music | seconds | `scripts/finish_clip.sh` |

Iterate on the still. Commit to I2V once.

## 0. One-time prerequisites (already done on this Mac)

- Draw Things (App Store) with these local checkpoints: FLUX.2 [klein] 9B (8-bit S) + Qwen3-8B encoder, Wan 2.2 High Noise Expert **I2V** A14B (8-bit S), Wan 2.2 Low Noise Expert **I2V** A14B (8-bit S), Wan 2.2 A14B Lightning High-Noise LoRA.
- `brew install ffmpeg` (9.0.2 present).
- Project `Untitled-35903` in Draw Things holds the working settings; create a new project per video if you want a clean history (Projects → + button top-left).

## 1. Still (Draw Things)

1. Version History → click **Cleared canvas** (canvas must be empty, otherwise Draw Things runs inpainting for 24 min).
2. Settings → Basic → Model → search `FLUX` → **FLUX.2 [klein] 9B (8-bit S)**. Accept "Try recommended settings" (steps 4, CFG 1, shift 3, DDIM Trailing).
3. LoRA → Disabled. Strength 100%.
4. All → Image Size → width **1024**, height **1792**. Height slider: drag thumb from ~153 px to ~205 px (→1600), then to ~233 px (→1792). Presets (9:16 / Small / Normal) register only sometimes; check the label.
5. Prompt: long natural-language scene description ending with `Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.` Describe foreground / middle / sky explicitly.
6. Generate. Repeat with new seeds until the composition is right (~1 min each).
7. Export: toolbar **4th icon** (folder with down-arrow) → Save → lands in `~/Documents/<prompt>_<seed>.png`. Move to `raw/clips/<name>_1024x1792.png`.

## 2. Downscale (terminal)

```bash
cd ~/dev/video-gen-kb/raw/clips
ffmpeg -i NAME_1024x1792.png -vf "crop=1008:1792:8:0,scale=576:1024:flags=lanczos" NAME_576x1024.png
```

## 3. Animate (Draw Things)

1. Version History → **Cleared canvas**. All → Image Size → 576×1024: try 9:16 + Small/Normal first; if it lands on 1:1 or 1024×1792, set the sliders (width click at ~117 px, height click at ~162 px, then nudge-drag each).
2. Click **Drag or paste an image** on the canvas → file picker → pick `NAME_576x1024.png`. It must fill the canvas.
3. Model → search `Wan` → **Wan 2.2 High Noise Expert I2V A14B (8-bit S)**. Accept recommended settings.
4. **Verify, in All settings, every one of these** (recommended settings reset them):
   - Strength tab shows **Image to Video**, 100%
   - Image Size **576×1024**
   - Steps **4** (click slider near left, then label-click to step up; label click = +1)
   - Number of Frames **81**
   - Text Guidance **1.0** (label click = +0.1)
   - Shift 5, Sampler UniPC Trailing
   - **Refiner Model = Wan 2.2 Low Noise Expert I2V A14B (8-bit S)** — recommended settings pick the *6-bit* one **every single time** (confirmed on 3 of 3 model switches); it is not downloaded and the refiner is then silently skipped → washed-out noise. Open the refiner dropdown and pick the Local entry ending in `(8-bit S)`.
   - Refiner Start 10%
   - LoRA → Wan 2.2 A14B Lightning High-Noise, 100%
5. Prompt (motion only, never describe the subject):
   `static camera, gentle ocean waves rolling onto the shore, grass and wildflowers swaying in a soft breeze, birds drifting slowly across the sky, clouds moving slowly, subtle motion, minimal movement`
6. Generate. The overlay must list the Refiner line. ~15 min. Preview at step 2 already shows whether it is working.
7. Export: same toolbar icon → Save → `~/Documents/<prompt>_<seed>.mov` (ProRes, 576×1024, 16 fps, 81 f). Move to `raw/clips/NAME.mov`.

## 4. Loop + music (terminal)

```bash
cd ~/dev/video-gen-kb
scripts/finish_clip.sh raw/clips/NAME.mov raw/clips/calm_ambient_dreamscape.mp3
```

Produces `NAME_loop.mp4` (1080×1920, 27.4 s, silent) and `NAME_final.mp4` (with music, fades). Forward-only loop with an 8-frame crossfade at the seam — never ping-pong (reverses waves and birds).

Other tracks: Pixabay → press play on a track page → `document.querySelector('audio').currentSrc` gives the CDN mp3 URL (the Download button wants a login).

## 5. File in the wiki

Append to `wiki/log.md`, note anything new on [[living-painting-loop]], `python3 scripts/build_site.py`, commit, push. Clips stay out of git (`raw/clips/` is ignored).

## Failure signatures

| Symptom | Cause | Fix |
|---|---|---|
| Overlay says "Image to Image + Inpainting", 24 min estimate | canvas not empty / smaller than generation area | Cleared canvas, regenerate |
| Washed-out, noisy, pastel video | refiner variant not downloaded | set refiner to the **8-bit S** Low Noise expert |
| No "Image to Video" tab | a T2V model is selected | pick the **I2V** High Noise expert |
| Birds fly backwards in the loop | ping-pong loop | use `finish_clip.sh` (forward + crossfade) |
| Still looks flat / plasticky | Wan T2V used for the still | FLUX.2 klein at 1024×1792, downscale |
| Slider label won't take the value | AX click moves thumb without commit | drag the thumb a few px, or use label clicks |

## Related pages
- [[living-painting-loop]]
- [[draw-things-setup]]
- [[wan22-i2v-locked-image-settings]]
- [[apple-silicon-inference]]
