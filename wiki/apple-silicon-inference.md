# Apple Silicon Inference Notes

**Summary**: What works and what breaks when running open video models on Mac (M-series, unified memory, Metal/MPS), and the runtimes that avoid the traps.

**Sources**: 2026-09-19-local-4k-video-research.md

**Last updated**: 2026-09-19

---

## This machine

Mac Studio, Apple M4 Max, 48 GB unified memory. No discrete GPU; GPU shares the 48 GB with the OS.

## Traps

1. **FP8 is unsupported on Metal.** Any `*_fp8_e4m3fn` checkpoint fails immediately. Choose GGUF, MLX-quantized (int4/int8), or app-native quantized weights.
2. **PyTorch MPS is slow for large DiTs.** Community ComfyUI-on-Mac numbers are 5–20× slower than a 4090. Some official workflows produce NaNs on MPS (LTX-2 two-stage decode).
3. **Vulkan/ncnn tools are fine** — Real-ESRGAN and RIFE ncnn builds run well on Apple Silicon.

## Runtimes that are Mac-first

- **Draw Things** — App Store, free. Metal FlashAttention v2.5, TeaCache, tiled VAE decode, quantized model library, LoRA support (CausVid / LightX2V). GUI + optional server offload / gRPC.
- **MLX ports** — `mlx-video` (Blaizzy; LTX-2, Wan 2.1, Wan 2.2), `ltx-2-mlx` (dgrauet; LTX-2.3/2.5, int4/int8/bf16), `ltx-video-mac` (native SwiftUI app). All MIT.

## Memory planning (48 GB)

| Load | Approx |
|---|---|
| LTX-2.3/2.5 int8 (ltx-2-mlx) | 21 GB |
| LTX-2.3 int4 | 12 GB |
| Wan 2.2 14B 6-bit (Draw Things), 1024×576×81f | 20 GB |
| Wan 2.2 14B Q4 GGUF pair + umT5 + VAE | ~24 GB |
| SeedVR2 at 4K output | unknown — measure |

Leave ~8 GB for macOS. Running generator and upscaler simultaneously is not advisable.

## Related pages
- [[local-open-source-4k-video-pipeline]]
- [[image-to-video-models]]
- [[video-upscaling]]
