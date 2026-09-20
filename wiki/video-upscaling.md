# Video Upscaling to 4K (Open Source)

**Summary**: Open-source tools that take 720p/1080p generated clips to 3840×2160, split into temporal restorers (SeedVR2, FlashVSR) and per-frame upscalers (Real-ESRGAN), with Apple Silicon notes.

**Sources**: 2026-09-19-local-4k-video-research.md

**Last updated**: 2026-09-19

---

## Two families

**Temporal / video-native** — look at neighboring frames, so textures do not flicker.
- **SeedVR2** (ByteDance) — strongest restoration quality in 2026 community tests. ComfyUI node `ComfyUI-SeedVR2_VideoUpscaler` (numz) has **full MPS support**. Weights auto-download on first run (multi-GB). Memory at 4K output on 48 GB unknown — may need tiling.
- **FlashVSR** — newer, faster than SeedVR2, slightly lower quality. Mac support unverified.

**Per-frame / image upscalers** — fast, simple, can shimmer on motion.
- **Real-ESRGAN** (ncnn-vulkan build) — runs on Apple Silicon via Metal/Vulkan; arm64 builds beat universal2. Good for slideshow-style motion, worse for AI-generated texture.
- **REAL Video Enhancer** — macOS GUI bundling Real-ESRGAN + RIFE with ncnn backend. Easiest all-in-one.

## Tricks from practice

- **Downscale-first restore**: if the generator output is muddy, downscale slightly, then let SeedVR2 restore + upscale — cleaner than upscaling mush directly.
- Upscale **before** frame interpolation ([[frame-interpolation]]) so RIFE sees clean edges.
- 720p → 4K is 3×; 1080p → 4K is 2×. Generating at 1080p when the model allows gives the upscaler less to invent.

## Encode target

3840×2160, HEVC or H.264, `hevc_videotoolbox` on Mac for hardware encode. See [[ffmpeg-pipeline]].

## Related pages
- [[local-open-source-4k-video-pipeline]]
- [[frame-interpolation]]
- [[image-to-video-models]]
