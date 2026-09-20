# Image-to-Video Models (Open Weights)

**Summary**: Catalog of open-weight image-to-video models as of 2026-09-19, with size, license, native output, and how each runs on Apple Silicon.

**Sources**: 2026-09-19-local-4k-video-research.md

**Last updated**: 2026-09-19

---

All capability and size claims are **as of 2026-09-19**; this space moves monthly.

## Wan 2.2 (Alibaba / Wan-AI)

- **Variants**: I2V-A14B (MoE, high-noise + low-noise expert pair), T2V-A14B, TI2V-5B (text+image, single model).
- **License**: Apache 2.0.
- **Native output**: 480p–720p, 16 or 24 fps, 81 frames typical (~5 s).
- **Speedups**: LightX2V distill LoRAs — 4-step (2 high + 2 low) instead of ~20–30 steps. CausVid LoRA for Wan 2.1.
- **NVIDIA reference**: 720p 5 s clip ≈ 9 min on RTX 4090 without distill.
- **Apple Silicon**: FP8 fails; GGUF (city96 / bullerwins) or Draw Things quantized weights work. ComfyUI GGUF Q4 on M1 Max = 82 min per 2 s clip. Draw Things 6-bit 14B ≈ 20 GB at 1024×576×81f. mlx-video supports TI2V-5B and I2V-14B natively.
- **Verdict**: default choice for photo animation. Use 14B + LightX2V in Draw Things; fall back to 5B for speed.

## LTX-2.5 (Lightricks)

- **Released**: 2026-08-11, open weights on Hugging Face.
- **Size**: 22B asymmetric dual-stream DiT.
- **License**: free for orgs under $10M ARR.
- **Native output**: claims native 4K HDR, auto clip duration, multi-shot, synchronized audio. Distilled variant does a 10 s I2V clip in ~7 s on NVIDIA superchips.
- **Apple Silicon**: ltx-2-mlx port supports 2.5; int8 ≈ 21 GB. 4K on MPS unverified. Like 2.3, "native 4K" is a 2-stage pipeline with a latent spatial upscaler — needs verification.
- **Verdict**: most promising for true-4K-without-upscale, but unproven on Mac. Experiment track.

## LTX-2.3 (Lightricks)

- **Released**: 2026-03-05. **22B** (LTX-2 was 19B). Audio + video in one pass.
- **Checkpoints** (HF `Lightricks/LTX-2.3`): `ltx-2.3-22b-dev`, `ltx-2.3-22b-distilled` (v1.0), **`ltx-2.3-22b-distilled-1.1`** (46.1 GB bf16, 8 steps, better audio/aesthetic), `distilled-lora-384-1.1` (7.6 GB LoRA that turns dev into 8-step), spatial upscalers ×2 and ×1.5, temporal upscaler. License: LTX-2 community license.
- **4K is two-stage**: generate ~1080p, then the bundled latent spatial upscaler ×2. Not single-pass native. Width/height divisible by 32; frames = 8k+1.
- **Distilled 1.1 on Mac**: bf16 exceeds 48 GB; needs Draw Things' quant or ltx-2-mlx int8 (~21 GB) / int4 (~12 GB). Distilled weights expect the official 2-stage sampler — ComfyUI KSampler shortcuts on MPS produced blobs; Draw Things / MLX ports implement it properly.
- **NVIDIA**: 32 GB VRAM BF16 minimum; FP8 ≈ 16–24 GB; direct 4K@50fps only short bursts on 24 GB — guides say generate 1080p then upscale.
- **Apple Silicon**: official 2-stage ComfyUI pipeline NaNs on MPS; GGUF + KSampler gives blobs. Use ltx-2-mlx (bf16 42 GB / int8 21 GB / int4 12 GB) or Draw Things.

## HunyuanVideo 1.5 (Tencent)

- 8.3B DiT, T2V + I2V, 720p cinematic, 14 camera-move presets in Draw Things.
- NVIDIA: ~14 GB with FP8 + offload. Mac: needs GGUF; less community support than Wan.

## Others

- **SkyReels**: human/face-focused, 544p. Worth a test for portrait photos.
- **Stable Video Diffusion**: I2V only, 25 frames. Obsolete but tiny.
- **MAGI-1**: autoregressive, listed in 2026 roundups; no Mac data. Needs verification.
- **Wan 2.5 / 2.6**: API-only from Alibaba as of last check; no open weights found. Needs verification.

## Choosing for family photos

Faces are the hard case. Priority: identity preservation > motion > resolution. Wan 2.2 14B with low motion prompts and 4-step LoRA is the baseline; compare SkyReels on portraits. Resolution comes from [[video-upscaling]], not the generator.

## Related pages
- [[local-open-source-4k-video-pipeline]]
- [[apple-silicon-inference]]
- [[video-upscaling]]
- [[photo-to-4k-video-approaches]]
