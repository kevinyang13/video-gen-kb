# Video Generation Landscape (2026)

**Summary**: One-page map of the AI video space as of 2026-09-19 — models (open and closed), the harnesses that run them, the apps and websites that sell access, launch dates, and a rough popularity read. Use it to place any new name you hear.

**Sources**: 2026-09-19-local-4k-video-research.md. Entries marked *needs verification* come from general knowledge, not a file in `raw/`.

**Last updated**: 2026-09-19

---

## How to read this page

Four layers. A **model** is weights. A **harness** loads weights and runs them. An **app** wraps a harness in a GUI. A **website/platform** rents closed or open models by the clip. Most confusion ("OpenArt vs Seedance") comes from comparing across layers.

Popularity is a qualitative read: ★★★ = dominant in its layer, ★★ = widely used, ★ = niche. Dates are first public release of the named version.

## Layer 1 — Models, open weights

| Model | Maker | Launched | Params | Native output | Audio | License | Mac | Popularity |
|---|---|---|---|---|---|---|---|---|
| **Wan 2.2** (I2V-A14B, T2V-A14B, TI2V-5B) | Alibaba | 2025-07 *(needs verification)* | 14B MoE / 5B | 720p, 16–24 fps, ~5 s | no | Apache 2.0 | Draw Things, mlx-video, GGUF | ★★★ open-source default |
| Wan 2.1 (1.3B, 14B) | Alibaba | 2025-02 *(needs verification)* | 1.3B / 14B | 480p / 720p, 81 f | no | Apache 2.0 | Draw Things, mlx-video | ★★ still common, CausVid LoRA |
| Wan 2.7 | Alibaba | 2026 *(needs verification)* | undisclosed | unconfirmed | unconfirmed | "open-weight line" per one source | unknown | ★ new; specs unconfirmed |
| **LTX-2.5** | Lightricks | 2026-08-11 | 22B | up to 4K HDR via 2-stage, auto duration, multi-shot | yes, native | free < $10M ARR | ltx-2-mlx | ★★ rising fast |
| **LTX-2.3** (dev, distilled, distilled-1.1) | Lightricks | 2026-03-05 | 22B | 480×704 default → 1080p; 4K via ×2 latent upscaler | yes, native | LTX-2 community | Draw Things, ltx-2-mlx | ★★ |
| LTX-2 | Lightricks | 2026-01 *(needs verification)* | 19B | 1080p→4K via upscaler | yes | LTX-2 community | ltx-2-mlx lineage | ★ superseded |
| LTX-Video 0.9.x | Lightricks | 2024-11 *(needs verification)* | 2B | 768×512, real-time class | no | Apache 2.0 | MPS | ★ superseded |
| **HunyuanVideo 1.5** | Tencent | 2025-11 *(needs verification)* | 8.3B DiT | 720p T2V/I2V | no | Tencent community | GGUF only | ★★ |
| HunyuanVideo (1.0) | Tencent | 2024-12 *(needs verification)* | 13B | 720p, up to 129 f, 14 camera presets | no | Tencent community | Draw Things | ★★ |
| SkyReels (V1/V2) | Skywork | 2025-02 *(needs verification)* | 13B (Hunyuan-derived) | 544p, human/face focus | no | open | Draw Things (T2V=100%) | ★ |
| CogVideoX 1.5 | Zhipu / THUDM | 2024-11 *(needs verification)* | 5B | 768×1360, 10 s | no | Apache 2.0 / custom | diffusers MPS | ★ superseded |
| Mochi 1 | Genmo | 2024-10 *(needs verification)* | 10B | 480p | no | Apache 2.0 | heavy | ★ superseded |
| MAGI-1 | Sand AI | 2025-04 *(needs verification)* | 24B / 4.5B autoregressive | 720p, chunked | no | Apache 2.0 | none | ★ |
| Stable Video Diffusion | Stability AI | 2023-11 *(needs verification)* | 1.5B | 576×1024, 25 f, I2V only | no | non-commercial | Draw Things | ★ obsolete |
| **SeedVR2** (upscaler) | ByteDance | 2025-06 *(needs verification)* | 3B / 7B | ×2–×4 temporal restore | — | Apache 2.0 | ComfyUI MPS | ★★ best open upscaler |
| FlashVSR (upscaler) | community | 2025 *(needs verification)* | — | fast temporal SR | — | open | unverified | ★ |
| Real-ESRGAN (upscaler) | Tencent ARC | 2021 *(needs verification)* | small | per-frame ×2–×4 | — | BSD | ncnn Metal | ★★★ ubiquitous |
| RIFE (interpolation) | hzwer | 2020 *(needs verification)* | small | frame interpolation | — | MIT | ncnn Metal | ★★★ ubiquitous |

## Layer 1 — Models, closed / API only

| Model | Maker | Launched | Native output | Audio | Where to use | Mac local | Popularity |
|---|---|---|---|---|---|---|---|
| **Seedance 2.5** | ByteDance | 2026 | up to 4K, 30 s single, ~3 min extended, 50 refs | yes | Dreamina, CapCut, fal, OpenArt | no | ★★★ leaderboard top |
| Seedance 2.0 | ByteDance | 2026-02 | 2K → 4K upgrade, 9 img + 3 vid + 3 audio refs | yes | Dreamina, CapCut (2026-03), fal (2026-04), OpenArt | no | ★★★ |
| Veo 3.x | Google DeepMind | 2025-05 (Veo 3) *(needs verification)* | 1080p–4K, native audio | yes | Gemini app, Flow, Vertex AI | no | ★★★ |
| Sora 2 | OpenAI | 2025-09 *(needs verification)* | 1080p, audio, social app | yes | Sora app, ChatGPT | no | ★★★ consumer |
| Kling 2.x / 3 | Kuaishou | 2025–2026 *(needs verification)* | 1080p, 10 s+, strong I2V motion | partial | klingai.com, fal, OpenArt | no | ★★★ |
| Runway Gen-4 / 4.5 | Runway | 2025-03 *(needs verification)* | 1080p, references, Aleph editing | via separate tool | runwayml.com | no | ★★ pro/film |
| Luma Ray 3 | Luma AI | 2025-09 *(needs verification)* | 1080p HDR, 4K upscale | no | Dream Machine | no | ★★ |
| Hailuo 02 / MiniMax | MiniMax | 2025-06 *(needs verification)* | 1080p, physics | no | hailuoai.video, fal | no | ★★ |
| Pika 2.x | Pika | 2025 *(needs verification)* | 1080p, effects | no | pika.art | no | ★ consumer |
| Wan 2.5 / 2.6 | Alibaba | 2025-09 / 2026 *(needs verification)* | 1080p, audio | yes | Alibaba Cloud, fal | no — API only | ★★ |
| Vidu Q2 | Shengshu | 2025 *(needs verification)* | 1080p, reference-to-video | no | vidu.com | no | ★ |
| Midjourney Video | Midjourney | 2025-06 *(needs verification)* | 480p→1080p I2V of MJ images | no | midjourney.com | no | ★★ |

## Layer 2 — Harnesses (inference engines)

| Harness | Type | Backend | Runs on Mac | Best for | Popularity |
|---|---|---|---|---|---|
| **ComfyUI** | node graph | PyTorch CUDA / MPS | yes, slow + fragile on MPS; FP8 dead | every model, every workflow, upscalers (SeedVR2 node) | ★★★ standard |
| **Draw Things engine** | app-native | Metal + Metal FlashAttention v2.5 | yes, native | Wan, LTX, Hunyuan, SkyReels, LoRAs | ★★ Mac default |
| **MLX** ports: mlx-video, ltx-2-mlx, ltx-video-swift-mlx | CLI / lib | Apple MLX | yes, native | scripting, LTX-2.5, batch | ★ growing |
| diffusers | Python lib | PyTorch | MPS partial | research, custom pipelines | ★★★ dev |
| WanGP / Wan2GP | low-VRAM wrapper | PyTorch CUDA | no *(needs verification)* | Wan + Hunyuan on small GPUs | ★★ |
| SwarmUI | GUI over ComfyUI | PyTorch | limited | one-click Wan/LTX workflows | ★ |
| LightX2V | inference framework + distill LoRAs | CUDA | no; LoRAs usable anywhere | 4-step Wan | ★★ |
| GGUF (city96 / bullerwins quants) | format, not engine | ComfyUI-GGUF node | yes | fitting 14B models in less memory | ★★ |
| TensorRT / NVIDIA RTX pipeline | accel | CUDA | no | LTX-2 4K on RTX | ★ |

## Layer 3 — Local apps

| App | Platform | Engine | Models | Cost | Popularity |
|---|---|---|---|---|---|
| **Draw Things** | macOS / iOS / iPadOS | own Metal engine | Wan 2.1/2.2, LTX-2.3, Hunyuan, SkyReels, SVD + image models | free (App Store), optional cloud compute | ★★ Mac default |
| ltx-video-mac | macOS | MLX | LTX-2 / 2.3 / 2.5, MiniMax H3 | free, MIT | ★ |
| REAL Video Enhancer | macOS / Win / Linux | ncnn | RIFE + Real-ESRGAN | free | ★ |
| Topaz Video AI | macOS / Win | proprietary (Metal on Mac) | own upscale/interp models | paid | ★★★ pro upscaling |
| ComfyUI Desktop | macOS / Win | ComfyUI | anything | free | ★★ |
| Pinokio | macOS / Win / Linux | script launcher | one-click installs of open tools | free | ★ |
| Final Cut / DaVinci Resolve | macOS | NLE | assembly, color, encode — not generation | paid / free tier | ★★★ editing |

## Layer 4 — Websites / platforms (rent by the clip)

| Site | Model | What it is | Models offered | Notes |
|---|---|---|---|---|
| **fal.ai** | API + playground, per-second billing | Seedance 2.0, Kling, Wan 2.5/2.6, LTX, Veo, Hunyuan, many open models | cheapest way to try a closed model once |
| **OpenArt** | subscription creative suite | Seedance 2.0/2.5 (Teams/Enterprise first), Kling, Veo, Wan, Runway… | aggregator; "OpenArt vs Seedance" is platform vs model |
| Dreamina / CapCut | ByteDance's own front end | Seedance 2.0, 2.5 | first-party home of Seedance |
| Replicate | API marketplace | Wan, LTX, Hunyuan, SeedVR2, upscalers | open models as APIs |
| Runway | first-party | Gen-4 / 4.5, Aleph | film/pro tooling |
| Google Flow / Gemini | first-party | Veo 3.x | Google account |
| Sora app | first-party | Sora 2 | social feed |
| Kling AI | first-party | Kling 2.x / 3 | credit packs |
| Luma Dream Machine | first-party | Ray 3 | HDR |
| Hailuo | first-party | Hailuo 02 | |
| Civitai | community hub | LoRAs, workflows for Wan/LTX/Hunyuan | source for speed LoRAs |
| Hugging Face | weights host | every open model above | canonical download location |
| Artificial Analysis Video Arena | leaderboard | all | popularity / quality ranking source |

## Where this project sits

Local, open, Mac: **Layer 1 open** (Wan 2.2, LTX-2.3 distilled 1.1) × **Layer 2** (Draw Things engine, optionally MLX) × **Layer 3** (Draw Things, REAL Video Enhancer, ffmpeg). Closed models are a quality ceiling and a per-clip fallback via fal.ai for hero shots. See [[local-open-source-4k-video-pipeline]].

## Related pages
- [[image-to-video-models]]
- [[video-upscaling]]
- [[apple-silicon-inference]]
- [[draw-things-setup]]
- [[local-open-source-4k-video-pipeline]]
