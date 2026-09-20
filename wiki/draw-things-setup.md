# Draw Things Setup for Video Models

**Summary**: How to get Wan 2.1/2.2, LTX-2.3, Hunyuan Video, and SkyReels into Draw Things on the Mac Studio and run image-to-video, including the starting settings that make Wan 2.2 tolerable on Apple Silicon.

**Sources**: 2026-09-19-local-4k-video-research.md

**Last updated**: 2026-09-19

---

## Before anything: disk

The Data volume was at **21 GB free of 926 GB** on 2026-09-19. Video model budget:

| Model (Draw Things quantized) | Approx download |
|---|---|
| Wan 2.2 14B I2V, high + low noise experts (6-bit SVDQuant) | ~18–20 GB + umT5 text encoder ~5 GB |
| Wan 2.2 5B TI2V | ~6–8 GB |
| Wan 2.1 14B (6-bit) | ~10 GB + encoder |
| LTX-2.3 (quantized) | ~12–20 GB + Gemma encoder |
| Hunyuan Video | ~13 GB + encoders |
| SkyReels | ~13 GB (Hunyuan-based) |

Free at least 100 GB first. Sizes are estimates from NVIDIA-side file sizes; Draw Things' own quantizations vary. Mark as needing verification once downloaded.

## Where models live

`~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models` (source: docs.drawthings.ai). Existing content is 4.7 GB of SD 2.1-era files — `sd_v2.1_768_v_f16.ckpt`, `open_clip_vit_h14_f16.ckpt`, `vae_ft_mse_840000_f16.ckpt`, `moondream1_q6p.ckpt`, `siglip_384_q8p.ckpt`, one Ghibli LoRA. Safe to delete from inside the app (Manage → trash icon) if space is tight.

## Downloading models (in-app — no manual Hugging Face needed)

1. Open Draw Things → **Settings** tab in left sidebar.
2. **Model** dropdown → **Manage**.
3. Browse **Official** (and **Community**) sections. Video models appear by name (source: Draw Things wiki):
   - `Wan 2.1 1.3B [T2V/I2V]` and `(8-bit)` — tiny, test the pipeline with this first
   - `Wan 2.1 14B [T2V/I2V]` and `(6-bit, SVDQuant)`
   - `Wan 2.1 [Fun Inpainting]`
   - Wan 2.2 **High Noise Expert** and **Low Noise Expert**, 14B and 5B, SVDQuant variants — for 14B I2V you need **both** experts
   - `LTX-2.3`
   - `Hunyuan Video` (up to 129 frames)
   - `SkyReels`
   - `Stable Video Diffusion` (I2V only, 25 frames)
4. Click the **cloud icon** next to each. The app pulls the model plus required text encoder / VAE automatically.

Manual import (LoRAs from Hugging Face or Civitai): Manage → **Import Model** → **Select from Files**, choose category **LoRA** vs **Model**. `Enter URL…` exists but is less reliable — download the file to `~/Downloads` and import from there (source: Install a Model or LoRA wiki page).

## Speed LoRAs — mandatory on Mac

Without a distill LoRA, Wan 2.2 14B runs ~20–30 steps; on M1 Max that was 82 min per 2 s (ComfyUI). With a 4-step LoRA the same job is ~5–7× shorter.

- **LightX2V Wan 2.2 distill LoRAs** — `huggingface.co/lightx2v/Wan2.2-Distill-Loras`. Download the I2V LoRA(s), import as LoRA. Standard config: 2 steps high-noise + 2 steps low-noise (4 total).
- **CausVid** — Wan 2.1 equivalent, 4–12 steps. Also listed in-app under LoRAs.
- Community rule of thumb (source: civitai lightx2v article): with a distill LoRA set **guidance (CFG) = 1**, **shift = 5**; the Wan 2.1 lightx2v LoRA at ~1.5 strength also works on Wan 2.2; use low-noise-compatible LoRAs, not high-noise-only ones.

## Image-to-video, step by step (Wan 2.2 14B)

1. **Canvas**: set size to 1280×720 (or 960×544 for tests). Drop the photo onto the Canvas and make sure it **fills the whole canvas** — uncovered area gets inpainted with hallucinated content (source: Draw Things wiki).
2. **Model**: Wan 2.2 14B I2V. In Draw Things the high/low expert pair is selected as the model with the second expert in the refiner/expert slot — check the model card text in Manage for the exact pairing UI.
3. **LoRA**: add LightX2V I2V distill LoRA, weight ~1.0 (try 1.5 if motion is dead).
4. **Steps** 4, **Guidance** 1, **Shift** 5, **Frames** 25 for a test, then 81 (5 s @ 16 fps) or 121 (5 s @ 24 fps).
5. **Prompt**: short, camera-centric — "slow push in, subject still, soft natural light". Negative prompt: "blurry, distorted face, extra limbs, text".
6. Enable **TeaCache** and **Tiled Decode** in Settings if memory pressure shows (source: Draw Things wiki).
7. Generate. Time the first full render and record it on [[local-open-source-4k-video-pipeline]].

Output is saved via the export/share button as MP4; feed it to [[video-upscaling]].

## Per-model notes

- **Wan 2.1 1.3B** — 480p, seconds per frame. Use only to validate the workflow.
- **Wan 2.1 14B** — 720p, up to 81 frames. Still competitive; single model, simpler than 2.2's pair.
- **Wan 2.2 5B TI2V** — single model, native 720p@24fps. The speed pick if 14B is too slow.
- **LTX-2.3** — audio + video. Prefer the **22B distilled 1.1** listing if offered: 8 steps instead of 30–50. Draw Things ships its own quantization, so the FP8-on-Metal problem does not apply. Default resolution 480×704 up to 1080p; width/height divisible by 32; frames must be 8k+1. For 4K, look for the LTX spatial upscaler ×2 stage in-app; otherwise use [[video-upscaling]].
- **Hunyuan Video** — 720p cinematic, 14 camera-move presets, frames 1+4n up to 129.
- **SkyReels** — Hunyuan derivative for humans/faces, 544p. Set **T2V = 100%** in Settings for it to run (source: Draw Things wiki). Worth an A/B against Wan 2.2 on family portraits.

## Open questions

- Wan 2.2 I2V 8-bit S pair: `wan_v2.2_a14b_hne_i2v_i8x.ckpt` + `wan_v2.2_a14b_lne_i2v_i8x.ckpt`, 13.7 GB each, ~27 min download each
- Whether LightX2V LoRA import works as a plain LoRA or needs the Community listing
- ~~Measured seconds per 81-frame 720p clip on M4 Max~~ → 24 min at 576×1280, see [[living-painting-loop]]

## Related pages
- [[local-open-source-4k-video-pipeline]]
- [[image-to-video-models]]
- [[apple-silicon-inference]]
- [[video-upscaling]]
