# Runbook: Living-Painting Video (next time, start here)

**Summary**: The exact click-by-click sequence to produce a 27 s TikTok-style animated painting on this Mac, with every gotcha hit on 2026-09-20 baked in as a checklist item. Narrative and measurements live on [[living-painting-loop]]; this page is only the steps.

**Sources**: 2026-09-19-local-4k-video-research.md; hands-on sessions 2026-09-20.

**Last updated**: 2026-09-20

---

## Budget

| Stage | Time | Tool |
|---|---|---|
| Still | ~40 s per seed | Draw Things, FLUX.2 klein 9B at 576×1024 |
| Downscale | seconds | ffmpeg |
| I2V | **~15 min** at 576×1024 × 81 f | Draw Things, Wan 2.2 I2V |
| Loop + music | seconds | `scripts/finish_clip.sh` |

Iterate on the still. Commit to I2V once. Human clicks needed per video: **one** (Save the .mov).

## 0. One-time prerequisites (already done on this Mac)

- Draw Things (App Store) with these local checkpoints: FLUX.2 [klein] 9B (8-bit S) + Qwen3-8B encoder, Wan 2.2 High Noise Expert **I2V** A14B (8-bit S), Wan 2.2 Low Noise Expert **I2V** A14B (8-bit S), Wan 2.2 A14B Lightning High-Noise LoRA.
- `brew install ffmpeg` (9.0.2 present).
- Project `Untitled-35903` in Draw Things holds the working settings; create a new project per video if you want a clean history (Projects → + button top-left).

## 1. Still (Draw Things) — generate at the video size

Tested 2026-09-20 (Golden Gate): FLUX.2 klein at native **576×1024** is visually as good as 1024×1792 + lanczos downscale for this use, and it removes two file dialogs. Use the 1024×1792 path only if a scene needs extra micro-detail.

1. Projects → **+** (new project) — canvas is empty.
2. Settings → Basic → Model → search `FLUX` → **FLUX.2 [klein] 9B (8-bit S)**. Accept "Try recommended settings" (steps 4, CFG 1, shift 3, DDIM Trailing).
3. LoRA → Disabled. Strength tab shows Text to Image, 100%.
4. All → Image Size → **576×1024**: click **9:16** then **Small**; if it lands elsewhere, width slider click at ~117 px (→576), height at ~162 px (→1024), nudge-drag each.
5. Prompt: long natural-language scene description ending with `Makoto Shinkai and Studio Ghibli background art style, ultra detailed, rich painterly brushwork, soft volumetric light, vibrant saturated colors, masterpiece.` Describe foreground / middle / sky explicitly.
6. Generate (~40 s). Repeat with new seeds until the composition is right. Note the seed.

*(Optional hi-res asset: export via the 4th toolbar icon → Save into `raw/clips/NAME_576x1024.png`. Not needed for the video.)*

## 2. Animate (I2V) — straight from the canvas

The generated still is already on the canvas and already fills 576×1024. No export, no reload.

1. Model → search `Wan` → **Wan 2.2 High Noise Expert I2V A14B (8-bit S)** (Local list). Pick **Not this time** on the Change Model Type dialog (recommended settings would reset the size to 832×448 and trigger inpainting).
2. **Verify, in All settings** (the model switch resets some of these):
   - Image Size **576×1024** — it drops to 384×704; click **Normal** under 9:16.
   - Strength tab shows **Image to Video**, 100%
   - Steps **4** (survives), Text Guidance **1.0** (survives)
   - Number of Frames **81** (resets to 14: click slider at ~188 px → 77, label-click ×1 → 81)
   - Shift **5** (resets to 3: click slider at ~150 px, nudge-drag → 4.95 is fine)
   - Sampler: DDIM Trailing works; UniPC Trailing is the Wan default but the menu does not take automation clicks — leave it
   - **Refiner Model = Wan 2.2 Low Noise Expert I2V A14B (8-bit S)** — resets to Disabled on this path (to the not-downloaded 6-bit variant on the recommended path). Pick the Local entry ending `(8-bit S)`.
   - **Refiner Start 10%** (defaults to 85% when set fresh: click slider at ~91 px)
   - LoRA → Wan 2.2 A14B Lightning High-Noise, 100% (resets to Disabled)
3. Prompt (motion only, never describe the subject):
   `static camera, gentle ocean waves rolling onto the shore, grass and wildflowers swaying in a soft breeze, birds drifting slowly across the sky, clouds moving slowly, subtle motion, minimal movement`
4. Generate. The overlay must list the Refiner line. ~15 min. Preview at step 2 already shows whether it is working.
5. Export: 4th toolbar icon → Save → navigate to `~/dev/video-gen-kb/raw/clips/` and save as `NAME.mov`. `ffprobe` it: expect 576×1024, 81 frames.

## 3. (removed — downscale/reload no longer needed)

## 4. Loop + music (terminal)

```bash
cd ~/dev/video-gen-kb
scripts/finish_clip.sh raw/clips/NAME.mov raw/clips/calm_ambient_dreamscape.mp3
```

Produces `NAME_loop.mp4` (1080×1920, 27.4 s, silent) and `NAME_final.mp4` (with music, fades). Forward-only loop with an 8-frame crossfade at the seam — never ping-pong (reverses waves and birds).

Other tracks: Pixabay → press play on a track page → `document.querySelector('audio').currentSrc` gives the CDN mp3 URL (the Download button wants a login).

## Done so far

| Date | Scene | Still seed | I2V seed | Files |
|---|---|---|---|---|
| 2026-09-20 | Coastal wildflowers (v2) | 20104302 | 1180755429 | `coast_v2_*` |
| 2026-09-20 | Torrey Pines, San Diego | 1190544862 | 284526412 | `torrey_*` |
| 2026-09-20 | Golden Gate, San Francisco (first native-576×1024 run) | — | 601904108 | `goldengate_*` |

## 5. File in the wiki

Append to `wiki/log.md`, note anything new on [[living-painting-loop]], `python3 scripts/build_site.py`, commit, push. Clips stay out of git (`raw/clips/` is ignored).

## When the Mac is locked

macOS blocks all Accessibility input while the screen is locked, so nothing in Draw Things can be clicked or typed — only screenshots work. A render already running continues fine; the Save dialog will wait. The automation watches `ioreg -n Root -d1 -a | grep -A1 CGSSessionScreenIsLocked` and resumes on unlock. Long-term fix: Draw Things HTTP API server (Settings → API Server) so generation and saving need no screen.

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
