# Research notes: local open-source 4K video from photos (2026-09-19)

Web research compiled by Claude Code. Target hardware: Mac Studio, Apple M4 Max, 48 GB unified memory, no CUDA.

## Sources consulted

- https://www.thundercompute.com/blog/best-open-source-ai-video-generation-models — Wan 2.2 (Apache 2.0, runs from 8GB VRAM on 5B GGUF), LTX-2.3 (native audio, 4K@50fps claim), HunyuanVideo 1.5 (8.3B, ~14GB VRAM FP8)
- https://www.hyperstack.cloud/blog/case-study/best-open-source-video-generation-models — model roundup Sept 2026
- https://www.thundercompute.com/blog/ltx-2-3-comfyui — LTX-2.3 official min 32GB VRAM BF16; FP8 ~16-24GB; direct 4K@50fps impractical on 24GB, recommend 1080p then upscale
- https://ltxworkflow.com/resources/community/ltx-23-vram-requirements-12gb-16gb-24gb — VRAM tiers
- https://comfyui-wiki.com/en/news/2026-08-11-ltx-2-5-open-weights-release — LTX-2.5 released 2026-08-11, 22B, native 4K HDR, I2V, distilled variant, free under $10M ARR
- https://huggingface.co/Lightricks/LTX-2.5
- https://lilting.ch/en/articles/ltx2-wan22-mac-local-video-gen — M1 Max 64GB tests: FP8 fails on Metal (`Undefined type Float8_e4m3fn`); Wan 2.2 GGUF Q4_K_S 832x480 33f = 82 min; LTX-2 GGUF I2V 768x512 33f = 13m42s, poor quality; official LTX 2-stage pipeline NaNs on MPS
- https://github.com/dgrauet/ltx-2-mlx — pure MLX LTX-2.3/2.5; bf16 42GB / int8 21GB / int4 12GB; `--image` I2V; frames = 8k+1; 480x704 default up to 1080p/1920p with tiling on 64-128GB; MIT
- https://github.com/Blaizzy/mlx-video — MLX inference for LTX-2, Wan2.1, Wan2.2 (T2V-14B, TI2V-5B, I2V-14B); MIT; `python -m mlx_video.wan_2.generate --image start.png --num-frames 81`
- https://github.com/james-see/ltx-video-mac — native macOS app, LTX-2/2.3/2.5
- https://wiki.drawthings.ai/wiki/Video_Generation_Basics — Draw Things supports LTX-2.3, Wan 2.1/2.2, Hunyuan, SkyReels, SVD; Wan 2.2 14B 6-bit ~20GB at 1024x576 81f; CausVid LoRA 4-12 steps; TeaCache, tiled decode
- https://releases.drawthings.ai/p/metal-flashattention-v25-w-neural — Metal FlashAttention v2.5; 5s 480p Wan 2.2 A14B on M5 iPad 16GB
- https://huggingface.co/lightx2v/Wan2.2-Distill-Loras — LightX2V 4-step distill LoRAs for Wan 2.2 (2 high + 2 low)
- https://blog.comfy.org/p/comfyui-wan22-fun-inp-support — ComfyUI LightX2V template integration
- https://localaimaster.com/blog/wan-video-generation-guide — Wan 2.2 720p 24fps, ~9 min/5s clip on RTX 4090
- https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler — SeedVR2 ComfyUI node, full MPS support
- https://artokun.mintlify.app/blog/video-upscale-comfyui — 2026 practice: SeedVR2 (quality) / FlashVSR (speed) temporal restorers, RIFE interpolation, downscale-first-restore trick
- https://medium.com/@ronregev/optimized-ai-image-video-upscaling-on-macs-with-apple-silicon-m1-m2-m3-m4-a248e128cdc6 — Real-ESRGAN ncnn on Apple Silicon
- https://www.free-codecs.com/download/real-video-enhancer.htm — REAL Video Enhancer: RIFE + Real-ESRGAN, macOS supported
- https://github.com/Comfy-Org/ComfyUI/issues/9255 — Wan 2.2 template broken on Apple Silicon (FP8)

## Local machine check
- `system_profiler`: Mac Studio, Apple M4 Max, 48 GB
- Not installed: ffmpeg, ComfyUI. python3 via anaconda at /opt/homebrew/anaconda3.

## Draw Things setup research (added 2026-09-19, later session)

- https://wiki.drawthings.ai/wiki/Install_a_Model_or_LoRA — Settings tab (left) → Model dropdown → Manage → Official / Community sections → cloud icon downloads. Import Model → Select from Files, or Enter URL… (less reliable). Pick category Model vs LoRA.
- https://wiki.drawthings.ai/wiki/Video_Generation_Basics — in-app names: "Wan 2.1 1.3B [T2V/I2V]", "(8-bit)", "Wan 2.1 14B [T2V/I2V]", "(6-bit, SVDQuant)", "Wan 2.1 [Fun Inpainting]"; Wan 2.2 High/Low Noise Expert 14B + 5B with SVDQuant; LTX-2.3; Hunyuan Video (up to 129 frames); SkyReels (needs T2V=100% in Settings); SVD. I2V: put image on Canvas, must cover canvas or it inpaints. CausVid LoRAs in-app or HF, 4–12 steps.
- https://civitai.com/articles/17918/my-swarmui-fast-wan-22-image2video-with-lightx2v-setup-experimental — with LightX2V LoRA: guidance 1, shift 5, Wan 2.1 lightx2v LoRA at ~1.5 strength works on Wan 2.2; use low-noise-compatible LoRAs only.
- https://docs.drawthings.ai/documentation/documentation/2.models/ — model dir: `~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models`; files in ~/Downloads importable after permission prompt.
- https://github.com/drawthingsai/community-models — community model index.
- https://huggingface.co/lightx2v/Wan2.2-Distill-Loras — 4-step distill LoRAs.

Local check: Draw Things installed at /Applications; Models dir 4.7 GB (SD 2.1 era); Data volume 21 GB free of 926 GB (98% full).

## LTX-2.3 distilled 1.1 (added 2026-09-19)
- https://huggingface.co/Lightricks/LTX-2.3 — 22B (not 19B); files: dev, distilled v1.0, distilled-1.1 (46.1 GB bf16, 8 steps, "different aesthetic, improved audio"), distilled-lora-384-1.1 (7.61 GB), spatial upscalers x2/x1.5, temporal upscaler; w/h % 32, frames 8k+1; LTX-2 community license; codebase wants CUDA >12.7.
- https://huggingface.co/Lightricks/LTX-2.3-fp8 — fp8 variant (unusable on Metal).

## Seedance / OpenArt / Wan 2.7 (added 2026-09-19)
- https://en.wikipedia.org/wiki/Seedance_2.0 — ByteDance, Feb 2026, unified multimodal (text+image+video+audio in), native audio; 2K then native 4K upgrade; closed
- https://techcrunch.com/2026/03/26/bytedances-new-ai-video-generation-model-dreamina-seedance-2-0-comes-to-capcut/ — Seedance 2.0 in CapCut 2026-03-26
- https://fal.ai/seedance-2.0 — API live on fal April 2026
- https://seedancetips.com/guides/seedance-2-0-open-source/ — no weights published, API only
- https://openart.ai/ai-model/seedance-2-0/ and https://openart.ai/ai-model/seedance-2-5/ — OpenArt hosts Seedance; 2.0 Teams/Enterprise first; 2.5 = 30 s 1080p with audio (OpenArt page) / up to 4K (orcarouter)
- https://www.orcarouter.ai/blog/seedance-2-5-vs-alibaba-wan-2-7 — Seedance 2.5: up to 4K, 30 s single, ~3 min extended, 50 refs, Maya/Blender plugins. Wan 2.7: "open-weight line", specs unconfirmed.
