# Recipe: Living-Painting Loop (TikTok "calm vibes" video)

**Summary**: Reproduce the 9:16 "animated painting" genre — one AI-painted landscape with ambient motion (waves, grass, birds, clouds), looped to ~30 s over calm music. All in Draw Things on the M4 Max, then ffmpeg.

**Sources**: 2026-09-19-local-4k-video-research.md; reference clip frames captured 2026-09-19 (TikTok, 576×1024, 28.5 s, static camera, frames at 1 s and 24 s near-identical = looped 5 s clip).

**Last updated**: 2026-09-20

---

## What the reference actually is

- One still, Shinkai/Ghibli-style coastal sunset, 576×1024 (9:16)
- Static camera; only ambient motion
- ~5 s I2V clip ping-pong looped 5–6× to 28 s, music, hashtag spam
- No faces → no drift risk. Easiest genre to reproduce.

## Step 1 — the still (done 2026-09-20)

No Flux/SDXL on this Mac, so the still came from **Wan 2.2 T2V at 1 frame** — Wan makes strong painterly stills and was already on disk.

| Setting | Value |
|---|---|
| Model | Wan 2.2 High Noise Expert T2V A14B (q8) |
| LoRA | Wan 2.2 A14B Lightning High-Noise 100% |
| Refiner | Disabled |
| Steps / CFG / Shift | 4 / 1.0 / 5 |
| Sampler | UniPC Trailing |
| Size | 576×1280 (9:20 — 9:16 preset would not stick; crop later) |
| Frames | 1 |
| Prompt | `anime painting of a coastal hillside at golden hour, wildflowers in the foreground, tall grass, ocean waves below a cliff, towering orange and pink cumulus clouds, warm sunset light, birds in the sky, Makoto Shinkai style, highly detailed, soft painterly light` |

Result: usable on first seed — sunset, cliffs, waves, flowers, birds. ~1 min wall time (est. shown 1:07).

## Step 2 — animate (I2V)

| Setting | Value |
|---|---|
| Model | Wan 2.2 High Noise Expert **I2V** A14B (8-bit S) — `wan_v2.2_a14b_hne_i2v_i8x.ckpt`, 13.7 GB |
| Refiner | Wan 2.2 Low Noise Expert I2V A14B (8-bit S), start 10% |
| Mode | Image to Video (appears only when an I2V model is selected) |
| Strength | 100% |
| LoRA | Lightning High-Noise (T2V LoRA; works on I2V per community, 100%) |
| Steps / CFG / Shift | 4 / 1.0 / 5 |
| Frames | 81 (5 s @ 16 fps) |
| Prompt | `static camera, gentle waves rolling onto the shore, grass and wildflowers swaying in a soft breeze, birds drifting slowly across the sky, clouds moving slowly, subtle motion, minimal movement` |
| Negative | `camera movement, zoom, morphing, flicker, distortion, text, watermark` |

**Result (2026-09-20)**: success on first run. Birds drift across the sky, waves roll, clouds creep, foreground flowers stay put. Painting itself unchanged frame 1 → 81.

**Measured**: **24 min** wall time for 81 frames at 576×1280 (4 steps ≈ 6 min each, plus ~2.5 min model load). The M4 Max is ~3× slower than the earlier guess on [[local-open-source-4k-video-pipeline]]. Speed levers: 832×480 (≈2.5× fewer pixels), 49 frames, or the Wan 2.2 5B model.

## Step 3 — export + loop (done 2026-09-20)

**Export from Draw Things**: toolbar icon 4 (folder with down-arrow, right of the share icon) → Save. Writes a **ProRes `.mov`** to `~/Documents`, named after the *first* prompt in the project plus a seed. The share icon (↑) only offers AirDrop/Mail/Notes/Photos — no file save. Exported clip: 576×1280, 16 fps, 81 frames, 5.06 s, 57 MB.

**Loop** — forward only. Ping-pong was tried first and rejected: reversing makes waves recede and birds fly backwards. Instead, crossfade the last 8 frames into the first 8 so the cut is invisible and physics stays forward:

```bash
ffmpeg -i coast.mov -filter_complex \
  "[0:v]crop=576:1024:0:128,setsar=1,fps=16[c];[c]split=3[c1][c2][c3];
   [c1]trim=start_frame=8:end_frame=73,setpts=PTS-STARTPTS[body];
   [c2]trim=start_frame=73:end_frame=81,setpts=PTS-STARTPTS[tail];
   [c3]trim=start_frame=0:end_frame=8,setpts=PTS-STARTPTS[head];
   [tail][head]xfade=transition=fade:duration=0.5:offset=0[seam];
   [body][seam]concat=n=2:v=1[unit];
   [unit]loop=loop=5:size=32767,setpts=N/FRAME_RATE/TB[out]" \
  -map "[out]" -r 16 -c:v libx264 -pix_fmt yuv420p -crf 18 -an coast_loop.mp4
```

One unit = frames 8–72 + (73–80 faded into 0–7) = 73 frames; ×6 = 438 frames, 27.4 s. Moving objects (birds) can ghost during the 0.5 s fade; shorten to 4 frames or prompt "birds exit the frame" on the next generation if it shows.

**Music** (when a track is chosen):

```bash
ffmpeg -i coast_loop.mp4 -i music.mp3 -c:v copy -c:a aac -b:a 192k -shortest coast_final.mp4
```

**Upscale** to 1080×1920 for posting: Real-ESRGAN ncnn, or quick `-vf scale=1080:1920:flags=lanczos`. 4K is unnecessary for TikTok.

## Draw Things UI notes (learned driving it via accessibility)

- **No I2V button.** I2V = I2V model selected + image on Canvas + Frames > 1. With a T2V model the Strength tab reads "Text to Video / Video to Video"; with an I2V model it reads "Image to Video / Video to Video".
- Wan 2.2 = **two checkpoints**. High Noise goes in Model, Low Noise in **Refiner Model** (All settings tab, ~10% start). Draw Things downloads a refiner lazily — picking it shows a "Data Usage" confirm, then a modal download sheet.
- "Try recommended settings" on a Wan 2.2 card resets LoRAs, sets 832×448, shift 5, and pre-fills the refiner slot.
- Slider value labels are **step buttons**: click = +1 step (frames +4, CFG +0.1). Dragging the thumb commits; a bare accessibility click moves the thumb without committing until the next drag.
- Models dir: `~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models`. In-progress downloads are `*.ckpt.partial` (pre-allocated to full size, so watch for the rename, not the byte count).
- Local checkpoints on 2026-09-20: `wan_v2.2_a14b_hne_t2v_q8p` (14.8 GB), `hne_i2v_i8x` (14.4 GB), `lne_i2v_i8x` (downloading), Lightning LoRAs high+low (615 MB each), `wan_v2.1_video_vae_f16`, LTX-2.3 22B distilled 1.1, `gemma_3_12b_it_qat_q8p` (LTX text encoder).

## Related pages
- [[wan22-i2v-locked-image-settings]]
- [[draw-things-setup]]
- [[ffmpeg-pipeline]]
- [[video-upscaling]]
