# Index

**Summary**: Table of contents for the video generation knowledge base.

**Sources**: n/a

**Last updated**: 2026-09-19

---

## Overviews

- [[photo-to-4k-video-approaches]] — four candidate pipelines (Ken Burns, AI image-to-video, depth parallax, hybrid) with trade-offs and open questions
- [[local-open-source-4k-video-pipeline]] — the recommended all-local recipe on the M4 Max: I2V at 720p/1080p → upscale → interpolate → ffmpeg; runtime and model rankings, time budget, open questions

## Models & tools

- [[video-generation-landscape]] — the whole map: open and closed models, harnesses, apps, websites, launch dates, popularity; where this project sits

- [[image-to-video-models]] — Wan 2.2, LTX-2.5/2.3, HunyuanVideo 1.5, SkyReels: size, license, native output, Mac status
- [[video-upscaling]] — SeedVR2, FlashVSR, Real-ESRGAN; temporal vs per-frame; Mac support
- [[draw-things-setup]] — downloading Wan 2.1/2.2, LTX-2.3, Hunyuan, SkyReels inside Draw Things; LightX2V 4-step settings; I2V step-by-step; disk budget
- [[apple-silicon-inference]] — FP8 trap, MPS slowness, Draw Things and MLX runtimes, 48 GB memory planning

## Recipes

- [[living-painting-loop]] — TikTok-style animated painting: Wan 2.2 T2V still → I2V ambient motion → ffmpeg ping-pong loop; exact Draw Things settings and UI gotchas
- [[wan22-i2v-locked-image-settings]] — Draw Things settings to animate a photo while keeping it as the literal first frame; motion-only prompting
- [[face-identity-workflows]] — four ways to put a specific face into a prompt-generated video: two-stage still→I2V, reference-to-video models, FaceFusion swap, face LoRA

## Concepts

_(stubs referenced but not yet written: frame-interpolation, depth-parallax, ffmpeg-pipeline)_

## Log

- [[log]] — append-only record of all operations
