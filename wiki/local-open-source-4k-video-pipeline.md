# Local Open-Source 4K Video from Photos (Apple Silicon)

**Summary**: How to turn photos into 4K video entirely on the Mac Studio (M4 Max, 48 GB) with open-weight models — which models run, what fails, realistic speeds, and the recommended pipeline: generate at 720p–1080p, then upscale + interpolate to 4K.

**Sources**: 2026-09-19-local-4k-video-research.md

**Last updated**: 2026-09-19

---

## The one-line answer

No open model generates *good* 4K directly on a Mac in reasonable time. The working recipe as of 2026-09-19 is:

**photo → I2V model at 720p/1080p (5s clip) → SeedVR2 or Real-ESRGAN upscale to 3840×2160 → RIFE to 60fps → ffmpeg stitch**

See [[image-to-video-models]], [[video-upscaling]], [[frame-interpolation]], [[ffmpeg-pipeline]].

## Hardware reality: M4 Max, 48 GB, no CUDA

Nearly every guide assumes NVIDIA. Three things break on Apple Silicon:

1. **FP8 checkpoints do not run.** Metal has no `Float8_e4m3fn`; official FP8 releases of Wan 2.2 and LTX-2 fail with `RuntimeError: Undefined type Float8_e4m3fn` (source: 2026-09-19-local-4k-video-research.md, lilting.ch). Use GGUF, MLX-quantized, or Draw Things' own quantized weights instead.
2. **ComfyUI on MPS is slow and fragile.** Wan 2.2 GGUF Q4 on an M1 Max took 82 min for a 2-second 480p clip; LTX-2's official two-stage pipeline produced NaNs in VAE decode (source: lilting.ch). M4 Max is faster than M1 Max but not 10×.
3. **Unified memory is the upside.** 48 GB means int8 LTX-2.3 (~21 GB) and Wan 2.2 14B 6-bit (~20 GB) fit without offloading (sources: dgrauet/ltx-2-mlx README, Draw Things wiki).

## Runtime options, ranked for this Mac

| Runtime | Models | Why / why not |
|---|---|---|
| **Draw Things** (Mac App Store, free) | Wan 2.1/2.2, LTX-2.3, Hunyuan, SkyReels | Native Metal + FlashAttention, quantized weights built in, CausVid/LightX2V 4-step LoRAs, TeaCache, tiled decode. Least friction. Start here. |
| **mlx-video** (Blaizzy) | LTX-2, Wan 2.1, Wan 2.2 (TI2V-5B, I2V-14B) | Pure MLX, CLI, scriptable — good for batch pipelines. `python -m mlx_video.wan_2.generate --image photo.png --num-frames 81`. No published Mac benchmarks. |
| **ltx-2-mlx** (dgrauet) | LTX-2.3, LTX-2.5 | Pure MLX. int8 ≈ 21 GB fits 48 GB comfortably. `--image` for I2V, frames must be 8k+1 (97 = 4 s @ 24 fps). Up to 1080p with tiling. MIT. |
| ComfyUI + GGUF | anything | Most workflows, worst Mac experience. Use only when a node exists nowhere else (e.g. SeedVR2 upscaler, which does have MPS support). |

## Model choice for photos → motion

| Model | Params | License | Mac verdict |
|---|---|---|---|
| **Wan 2.2 I2V-A14B** | 14B MoE (high/low noise pair) | Apache 2.0 | Best motion quality of the open set; needs LightX2V 4-step LoRA to be tolerable on Mac. Draw Things 6-bit ≈ 20 GB at 1024×576×81f. |
| **Wan 2.2 TI2V-5B** | 5B | Apache 2.0 | Native 720p@24fps, smallest — fastest realistic Mac option. Lower fidelity than 14B. |
| **LTX-2.5** | 22B | Open weights, free < $10M ARR | Released 2026-08-11. Native 4K HDR *on NVIDIA*; distilled variant is few-step. MLX port exists (ltx-2-mlx). Unverified how 4K behaves on MPS — treat as experiment, not plan. |
| **LTX-2.3 distilled 1.1** | 22B | same | 8-step distill, audio+video. 46 GB bf16 → must run quantized (Draw Things, ltx-2-mlx int8). 4K = 1080p + bundled ×2 latent upscaler. Best LTX pick on Mac; unmeasured. |
| HunyuanVideo 1.5 | 8.3B | Tencent community license | ~14 GB FP8 on NVIDIA; FP8 dead on Mac, so needs GGUF. Not the first pick here. |

Details per model: [[image-to-video-models]].

## Recommended pipeline (v1)

1. **Prep photos**: export from Photos at full resolution as PNG/JPEG into `raw/photos/`. Crop to 16:9 first — I2V models inpaint if the image does not fill the canvas (source: Draw Things wiki).
2. **Generate clips** in Draw Things: Wan 2.2 I2V 14B, LightX2V LoRA, 4 steps, 1280×720, 81 frames (5 s @ 16 fps) or 121 frames @ 24 fps. Short camera-move prompts ("slow push in", "gentle pan left"). Test at 25 frames before full renders.
3. **Upscale** each clip 3× to 3840×2160 with SeedVR2 (ComfyUI, MPS) or Real-ESRGAN ncnn (fast, per-frame, may flicker). See [[video-upscaling]].
4. **Interpolate** to 48/60 fps with RIFE (REAL Video Enhancer on macOS, or `rife-ncnn-vulkan`). See [[frame-interpolation]].
5. **Assemble**: `ffmpeg` concat with `xfade` crossfades, add music, encode HEVC 4K (`-c:v hevc_videotoolbox` uses the M4 media engine). See [[ffmpeg-pipeline]].

## Realistic time budget (needs verification on this machine)

- M1 Max, Wan 2.2 Q4 GGUF, ComfyUI, 20 steps: 82 min / 2 s clip (measured, lilting.ch).
- **M4 Max, Draw Things, Wan 2.2 I2V 14B 8-bit pair + Lightning 4-step, 576×1280 × 81 frames: 24 min (measured 2026-09-20)** — ~6 min per step, ~2.5 min model load. Roughly 720p-equivalent pixel count, so budget ~25 min per 5 s 720p clip.
- M4 Max, Wan 2.2 T2V 14B q8 + Lightning, 576×1280 × 1 frame (a still): ~1 min (measured 2026-09-20).
- Upscale + RIFE: roughly real-time to 5× real-time per clip on Metal, depending on model.

## Not installed yet on this Mac

`ffmpeg`, ComfyUI, Draw Things. Python 3 exists (anaconda). Install order: `brew install ffmpeg`, Draw Things from App Store, then `uv` + mlx-video if scripting is wanted.

## Open questions

- Actual M4 Max timings for Wan 2.2 14B + LightX2V in Draw Things
- Does ltx-2-mlx int8 run LTX-2.5 I2V at 1080p on 48 GB, and how long?
- SeedVR2 on MPS: memory at 4K output, need for tiling?
- Face fidelity: which model keeps family faces closest to the photo?

## Related pages
- [[photo-to-4k-video-approaches]]
- [[image-to-video-models]]
- [[video-upscaling]]
- [[frame-interpolation]]
- [[ffmpeg-pipeline]]
- [[apple-silicon-inference]]
