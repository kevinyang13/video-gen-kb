# Headless CLI Pipeline — running this project without clicking a UI

**Summary**: Whether the whole pipeline — text-to-image with reference ("Moodboard") images, image-to-video, upscale, edit — can run from the command line with no GUI. Short answer: **yes, and the best CLI is Draw Things' own** (`draw-things-cli`, GPL-v3, same engine and same model files as the app, video output and repeatable `--image` references included). ComfyUI can be driven headlessly over HTTP but its Mac video story is bad; MLX tools cover stills only.

**Sources**: [drawthingsai/draw-things-community](https://github.com/drawthingsai/draw-things-community) source read on 2026-09-22 (`Apps/DrawThingsCLI/DrawThingsCLI.swift`, `Libraries/Scripting/Sources/ScriptModels.swift`, `Libraries/Scripting/Sources/SharedScript.swift`, `Libraries/DataModels/Sources/config.fbs`); [draw-things-cli announcement](https://releases.drawthings.ai/p/draw-things-cli-local-media-generation) (2026-03-25); [draw-things-comfyui](https://github.com/drawthingsai/draw-things-comfyui); [ComfyUI FLUX.2 klein tutorial](https://docs.comfy.org/tutorials/flux/flux-2-klein); [ComfyUI-Flux2Klein-Conditioning-Toolkit](https://github.com/xmarre/ComfyUI-Flux2Klein-Conditioning-Toolkit); [MyAIForce multi-reference guide](https://myaiforce.com/improve-multi-reference-image-results-flux-2-klein/); [ComfyUI + Wan 2.2 on Apple Silicon](https://papayabytes.substack.com/p/guide-comfyui-and-wan-22-image-to); [LTX-2 vs Wan 2.2 on M1 Max](https://lilting.ch/en/articles/ltx2-wan22-mac-local-video-gen); [ltx-video-mac](https://github.com/james-see/ltx-video-mac); [mflux](https://github.com/mflux-community/mflux); ComfyUI API guides ([9elements](https://9elements.com/blog/hosting-a-comfyui-workflow-via-api/), [Runflow](https://www.runflow.io/blog/comfyui-api-developer-guide)). All as of 2026-09-22.

**Last updated**: 2026-09-22

---

## The question

Everything in [[lost-city-plan]] and [[dragon-epic-plan]] currently runs through the Draw Things **window**: pick a model, load a still, drag crops into the Moodboard, press Generate, press Save. That is why this project carries a pile of UI-automation gotchas ([[draw-things-setup]], memory `draw-things-automation`): synthetic drags don't register, a double-click on Generate means Stop, a screen lock freezes the whole batch. None of that is inherent to the models — it is inherent to driving an app.

So: can the same four stages run from a shell script?

| Stage | Needs | CLI available? |
|---|---|---|
| Still — FLUX.2 [klein] 9B + 1–3 reference crops at fixed weight | multi-reference conditioning | **yes** — `draw-things-cli generate` with repeated `--image` |
| Motion — LTX-2.3 22B distilled (or Wan 2.2 I2V pair) | first-frame image + frame count + video file out | **yes** — same command, `--frames` + `--output clip.mov` |
| Upscale — Real-ESRGAN ncnn | — | already CLI ([[scripts-reference]]) |
| Edit/music — ffmpeg | — | already CLI |

Only the first two were ever UI-bound, and both have a first-party CLI.

## 1. `draw-things-cli` — the direct answer

Draw Things' inference stack is open source (GPL-v3) and ships two command-line binaries built from the same tree as the app: **`draw-things-cli`** (local generation + LoRA training) and **`gRPCServerCLI`** (a headless inference server). The announcement calls it "the fastest image generation tool on macOS" (source: releases.drawthings.ai, 2026-03-25).

```bash
brew tap drawthingsai/draw-things
brew install drawthingsai/draw-things/draw-things-cli
```

*(Not installed here yet. Comments on the announcement report Swift-version mismatches when building from source — expect friction; marked **unverified on this Mac**.)*

**It reads the app's own models.** `--models-dir` defaults to Draw Things' container; ours already holds the exact checkpoints this project uses:

```
~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/
  flux_2_klein_9b_i8x.ckpt                     # the still model
  ltx_2.3_22b_distilled_1.1_q8p.ckpt           # the motion model
  ltx_2.3_audio_video_vae_f16.ckpt
  wan_v2.2_a14b_hne_i2v_i8x.ckpt               # Wan high-noise
  wan_v2.2_a14b_lne_i2v_i8x.ckpt               # Wan low-noise (refiner)
  wan_v2.2_a14b_hne_i2v_lightning_251022_lora_f16.ckpt
```

Same quantisations, same engine → no re-download, no re-tuning, and the numbers in [[lost-city-plan]] §3 should carry over. `--model` also accepts a human-readable name (`"FLUX.2 [klein] 9B (8-bit)"`) or a Hugging Face reference.

### Official examples (from the CLI's own help text)

```bash
# still, multiple reference images — this is the Moodboard equivalent
draw-things-cli generate --model flux_2_klein_4b_q6p.ckpt \
  --prompt "combine these references" --image first.png --image second.png

# video model, frame count, video file out
draw-things-cli generate --model ltx_2.3_22b_distilled_q6p.ckpt \
  --prompt "ocean waves at sunset" --frames 49 --output clip.mov
```

`--image` is an array: "The first image is the primary img2img or reference input; subsequent images are additional references in the supplied order. Each image is resized with aspect-preserving scale and center crop to match the requested output size." That last clause is the CLI version of the canvas-crop gotcha we hit in LTX renders.

### Flags that matter here

| Flag | Meaning | Our use |
|---|---|---|
| `--model` | ckpt filename, model name, or `hf://owner/repo` | klein for stills, LTX for motion |
| `--prompt` / `--prompt-file` | inline or from file (`-` = stdin) | our prompts are long — use `--prompt-file`, straight out of `projects.json` |
| `--image` (repeatable) | primary input then references | still crops; the first frame for I2V |
| `--frames` | frame count for video models | 249 for a 10 s LTX clip |
| `--steps` `--cfg` `--width` `--height` `--seed` `--strength` | the usual | 8 / 1.0 / 1024 / 576 |
| `--output` | `.png`, `.mov`, `.mp4` | omit and it previews inline in iTerm2/Ghostty |
| `--video-format` | `prores4444`, `prores422hq`, `h264`, `hevc` | `prores422hq` = what the app exports today |
| `--config-json` / `--config-file` | partial override in `JSGenerationConfiguration` format, **merged onto the model's recommended settings** | everything with no dedicated flag: shift, sampler, SSS, refiner, LoRAs |
| `--no-download-missing`, `--offline` | never touch the network | good default for reproducible batches |
| `--remote --remote-url … --remote-port 7859` | run on a `gRPCServerCLI` instead of locally | offload to another Mac |
| `--audio`, `--avc`, `--segment-frames`, `--cond-frames` | segmented audio-video continuation | LongCat-Video-Avatar 1.5 only — **not** LTX; long shots still have to be chained by hand |

**Configuration precedence** (from the help text): model's recommended settings → `--config-json`/`--config-file` → explicit flags. So "Try recommended settings", the thing we click in the app, is the CLI's *default*.

### Our settings as a config file

`JSGenerationConfiguration` keys (from `ScriptModels.swift`) cover every setting this project touches: `steps`, `guidanceScale`, `shift`, `sampler`, `strength`, `numFrames`, `fps`, `stochasticSamplingGamma` (= Strategic Stochastic Sampling), `refinerModel`, `refinerStart`, `loras[]`, `hiresFix` + `hiresFixWidth/Height/Strength`, `stage2Steps/Guidance/Shift`, `controls[]`, `causalInference`, `teaCache*`, `upscaler`, `batchCount`.

`sampler` is an integer — the enum order in `config.fbs` is: `0 DPMPP2MKarras, 1 EulerA, 2 DDIM, 3 PLMS, 4 DPMPPSDEKarras, 5 UniPC, 6 LCM, 7 EulerASubstep, 8 DPMPPSDESubstep, 9 TCD, 10 EulerATrailing, 11 DPMPPSDETrailing, 12 DPMPP2MAYS, 13 EulerAAYS, 14 DPMPPSDEAYS, 15 DPMPP2MTrailing, 16 DDIMTrailing, 17 UniPCTrailing, 18 UniPCAYS, 19 TCDTrailing`. So **16 = DDIM Trailing** (our klein/Wan stills) and **19 = TCD Trailing** (our LTX clips).

Lost City's LTX config (§3c of [[lost-city-plan]]) as JSON:

```json
{ "steps": 8, "guidanceScale": 1.0, "sampler": 19, "shift": 5.0,
  "stochasticSamplingGamma": 0.3, "hiresFix": false,
  "width": 1024, "height": 576, "numFrames": 249, "fps": 25 }
```

and the klein still:

```json
{ "steps": 4, "guidanceScale": 1.0, "sampler": 16, "shift": 3.0,
  "width": 1280, "height": 768 }
```

**Unverified until we run it**: (a) that `--image still.png --frames 249` is treated as LTX *image-to-video* rather than img2img on frame 1; (b) whether reference images land in the Moodboard channel with equal weight for klein (the app lets us set per-image weight — `setMoodboardImageWeight` exists in the scripting API, no CLI flag seen); (c) that `stochasticSamplingGamma` is 0…1 and not 0…100. One test render each settles all three.

## 2. `gRPCServerCLI` — headless server, thin clients

```bash
gRPCServerCLI-macOS ~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models \
  --no-response-compression --model-browser      # listens on :7859
```

Same binary family, no window at all. Clients: `draw-things-cli --remote`, the official [ComfyUI extension](https://github.com/drawthingsai/draw-things-comfyui), or your own gRPC client. Useful later if rendering moves to a second machine while this one edits; not needed for a single-Mac batch.

## 3. The two half-measures (app must be running)

- **HTTP API** — Settings → Advanced → API Server, HTTP, port 7860. Automatic1111-compatible: `GET /` returns the current config, `POST /sdapi/v1/txt2img` runs a prompt with whatever is loaded in the UI, images come back base64. Fine for stills; the A1111 surface has no vocabulary for Moodboard or video, so **not** a route for this project (*unverified whether newer builds extend it*).
- **JS scripts** — the app's scripting layer exposes exactly the calls the UI clicks do: `pipeline.run(args)`, `loadImage(file)`, `addToMoodboardFromFiles()`, `addToMoodboardFromSrc(srcContent)`, `setMoodboardImageWeight(weight, index)`, `clearMoodboard()`, `removeFromMoodboardAt(index)` (`SharedScript.swift`). That is the one route that can set **Moodboard weights** programmatically — worth remembering if the CLI turns out not to expose them — but a script still has to be launched from inside the app.

## 4. Without Draw Things at all

| Route | Stills + references | Motion | Verdict on a Mac |
|---|---|---|---|
| **ComfyUI headless** — `python main.py`, `POST /prompt` with API-format workflow JSON, poll `/history/{id}`, fetch `/view`; workflows exported with "Save (API format)" | **Yes.** FLUX.2 klein is supported, multi-reference works by VAE-encoding each reference and feeding a *Multi* `ReferenceLatent` into the sampler; community node packs (`ComfyUI-Flux2Klein-Conditioning-Toolkit`, ref-grid nodes) fix the stock behaviour of only editing `reference_latents[0]` | **Painful.** Metal has no `Float8_e4m3fn`, so every FP8 checkpoint fails and you live on GGUF. Measured on an M1 Max 64 GB: Wan 2.2 GGUF Q4_K_S at 832×480 × 33 f (2 s) = **82 min**; LTX-2 FP8 won't load at all and its GGUF fallback gave "essentially a still image". Another guide on an M2 Max 64 GB starts at **320×320** to avoid `PYTORCH_MPS_HIGH_WATERMARK_RATIO` OOM. LTX-**2.3** is reported to run on MPS (~2.5× slower than a 4090 on an M4 Max/128 GB) — *unverified here* | 
| **mflux** (MLX) — `uv tool install mflux`, `mflux-generate-flux2 --model … --steps 4 …` | Yes for FLUX.2 klein 4B/9B (4-bit MLX weights on the Hub; ~9 s for 512² × 4 steps). Reference-image flags **not documented** | **None** — image models only, no Wan, no LTX | Good fallback for stills, useless for motion |
| **`mlx-video-with-audio`** (the engine behind the SwiftUI app [ltx-video-mac](https://github.com/james-see/ltx-video-mac)) | first/last frame and multi-image keyframes on LTX paths | LTX-2 / 2.3 / 2.5 with synchronised audio, MLX-native, 32 GB minimum | The only non-DT MLX route to LTX video. The app is a GUI, but it exposes a local REST API on `127.0.0.1:8420` and the Python package underneath is scriptable — **untested**, no published timings |
| **diffusers on MPS** (`LTXImageToVideoPipeline`, `WanImageToVideoPipeline`) | yes, in Python | yes, in principle | Same MPS wall as ComfyUI: the official two-stage LTX pipeline produces NaN/Inf at VAE decode on MPS. Not worth the debugging |

The pattern is consistent with [[apple-silicon-inference]]: the models are portable, the *runtime* is not. Draw Things ships hand-written Metal kernels and its own quant formats, which is why a 10 s LTX clip costs ~20 min here instead of the 82-min-per-2-second that ComfyUI+GGUF measured on comparable hardware.

## 5. Recommendation

1. **Install `draw-things-cli` and re-shoot one known clip** — s10 (drinking, the most stable result we have). Compare wall time and output against `s10_ltx_v1.mov`. That single test answers the three unverified items in §1.
2. If it matches, add `scripts/dt_render.sh` next to the existing scripts: read a scene id out of `projects.json`, write `--prompt-file`, pick the config JSON, call the CLI, then chain straight into `upscale_4k.sh`. The whole "render 5 scenes overnight" job becomes a `for` loop with no screen lock, no drag, no crash-from-cloned-project, and no `app_*` calls at all.
3. Keep the app for **looking** at results and for anything that needs Moodboard weights until §1(b) is settled.
4. Do not migrate to ComfyUI for motion on this Mac. Revisit only if an NVIDIA box enters the picture, where it becomes the better harness.

## Related pages
- [[scripts-reference]] — the CLI half of the pipeline that already exists
- [[draw-things-setup]] · [[runbook-living-painting]] — the UI workflow this would replace
- [[apple-silicon-inference]] — why Metal, FP8 and MPS decide all of this
- [[lost-city-plan]] — the settings that would go into the config JSON
- [[image-to-video-models]] — Wan vs LTX trade-off, unchanged by the harness
