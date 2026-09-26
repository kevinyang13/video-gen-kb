# Step-by-Step AI Film Production Pipeline — the standard route, and ours

**Summary**: An eight-step industry-practice pipeline for AI short films (shot list → character turnarounds → **train a LoRA** → frame-0 anchors → I2V per shot → NLE edit with TTS dialogue → Topaz upscale and grade → master). Recorded here in full, then compared step by step with what this project actually does on a Mac Studio, where three of its eight steps are unavailable, unnecessary or were tried and rejected.

**Sources**: `raw/2026-09-26-ai-film-production-pipeline.md` (pasted 2026-09-26, origin unattributed — general industry practice, *not independently verified*); our own results in [[idea-to-video-blueprint]], [[character-consistency]], [[headless-cli-pipeline]], [[video-upscaling]], [[apple-silicon-inference]].

**Last updated**: 2026-09-26

---

## The two pipelines side by side

| # | Standard route (source) | What we do | Why |
|---|---|---|---|
| 1 | Script, scene breakdown, formal shot list; identify recurring assets | Same — intake questionnaire, then a shot table with camera, motion and consistency need per shot | [[idea-to-video-blueprint]] Phases 0–1 |
| 2 | **25–40** character images across angles, lighting, expressions; environment concept art | **4-view turnaround sheet** per character, plus a plate per location and prop | We don't need a training set, only reference pixels — §"Why no LoRA" below |
| 3 | **Train a character LoRA**, 1,500–3,000 steps, validate in ComfyUI | **Skipped entirely** | LoRA training is broken on Apple Silicon locally; klein takes reference images directly |
| 4 | Generate a still anchor per shot using the LoRA | Generate a still per shot by **editing the seed** (diptych or restage), 3 seeds, judge, pick | [[idea-to-video-blueprint]] Phase 4b |
| 5 | I2V per shot with the LoRA; ControlNet OpenPose/Depth for motion | I2V per shot from the picked still; **no ControlNet** — motion comes from the prompt | No klein-compatible ControlNet; LTX obeys action, not staging |
| 6 | NLE (Resolve/Premiere), TTS dialogue, lip-sync, sound design | `assemble_film.sh` — ffmpeg crossfades, LTX ambience, one music bed. **No dialogue** | Every film so far is wordless; TTS/lip-sync not installed |
| 7 | Topaz Video AI or ComfyUI upscaler; frame interpolation; unified LUT | Real-ESRGAN x4plus per frame → 3840×2160; **no interpolation, no LUT** | Free, local, ~6 min/clip ([[video-upscaling]]) |
| 8 | QC pass, export ProRes or H.264/H.265 | QC sheets per clip, level check, HEVC 10-bit 40 Mbps + delivery copies | Same intent, scripted |

## Where the routes genuinely diverge

### Why no LoRA (step 3)

The standard route spends its identity budget on **training**: 25–40 images, a captioned dataset, a trigger word, 1,500–3,000 steps. That is the strongest identity channel there is — LoRA weights generalise to angles the reference never showed ([[identity-conditioning]] channel 4).

We use **channel 2 instead — reference-image tokens.** FLUX.2 klein takes a reference image directly: its latent is concatenated into the transformer's token sequence and the target attends to it. No training, no dataset, no trigger word. One good photo becomes a usable character in about 25 seconds.

The trade is real and worth stating plainly:

| | LoRA | Reference tokens (ours) |
|---|---|---|
| Setup | hours, needs a training rig | ~25 s per seed |
| Novel angles | generalises | copies only what the reference shows — hence the turnaround sheet |
| Local on Apple Silicon | training effectively unavailable | works |
| Cost of a new character | a full dataset and training run | one photo |

Local LoRA training on this Mac is not practical ([[character-consistency]]); cloud training is ~$1 per character but adds a dependency and a round trip. With sheets covering front, three-quarter, profile and back, reference tokens have been sufficient for six delivered films.

### Why no ComfyUI (steps 3, 5, 7)

The source assumes ComfyUI as the harness. On this Mac it is the wrong one: Metal has no `Float8_e4m3fn`, so FP8 checkpoints fail outright, and a field test measured **82 minutes for a 2-second Wan clip** in ComfyUI+GGUF on an M1 Max — against ~10 minutes for a 10-second LTX clip through `draw-things-cli` here ([[headless-cli-pipeline]] §4). The models are portable; the runtime is not.

### Why no ControlNet (step 5)

No ControlNet, IP-Adapter or PuLID is compatible with klein ([[character-consistency]]). Motion is specified in the LTX prompt instead, which brings its own rule: **LTX obeys the action, not the staging** — it picks its own camera at CFG 1, so you write the action you want and accept the blocking, or shoot that frame on Wan ([[lost-city-plan]] §3c).

### Why no Topaz (step 7)

Real-ESRGAN x4plus ncnn runs on Metal, costs nothing, and takes ~6 minutes per 81-frame clip. Frame interpolation is unnecessary because LTX renders natively at 25 fps. A unified LUT would help — shots do drift in colour between plates — and is the one part of step 7 we should adopt.

### What the source has that we lack

Honestly assessed, three things:

1. **Dialogue and lip-sync.** Every film here is wordless. TTS plus a lip-sync model would open a whole category of story, and nothing about the Mac prevents it — it simply isn't installed.
2. **A colour grade.** We match colour by prompt wording alone. A single LUT across the assembly would fix the continuity drift visible between, say, the two city shots in [[nightelf-hunter-plan]].
3. **An NLE.** ffmpeg assembly is reproducible and scriptable, but it cannot do a J-cut, a speed ramp, or trim by eye against music. For anything longer than a minute this will start to hurt.

## Related pages
- [[idea-to-video-blueprint]] — our version of steps 1–8, with the intake and approval gates
- [[character-consistency]] · [[identity-conditioning]] — the LoRA-versus-reference-tokens decision in depth
- [[headless-cli-pipeline]] — why `draw-things-cli` rather than ComfyUI on this hardware
- [[video-upscaling]] — Real-ESRGAN versus Topaz and SeedVR2
- [[scripts-reference]] — the scripts that implement our steps 4–8
