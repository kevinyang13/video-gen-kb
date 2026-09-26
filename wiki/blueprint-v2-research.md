# Blueprint v2 — Research Notes for a Different Pipeline Strategy

**Summary**: Research toward a second production pipeline built on a different strategy from [[idea-to-video-blueprint]]: identity from **trained weights** rather than reference images, motion from **pose and depth control** rather than prose, and a real **edit, grade and dialogue** stage instead of a scripted ffmpeg assembly. Records what the standard industry route does, what each piece would cost on this hardware, what is unknown, and the experiments that would decide whether to adopt it. Nothing here is implemented — the current blueprint is unchanged and still the production route.

**Sources**: `raw/2026-09-26-ai-film-production-pipeline.md` , `raw/2026-09-26-ai-film-orchestration-options.md` and `raw/2026-09-26-character-lora-training.md` (all pasted 2026-09-26, origin unattributed; the three orchestrator repos were verified to exist on 2026-09-26, their capabilities were not tested); our measured results in [[idea-to-video-blueprint]], [[headless-cli-pipeline]], [[character-consistency]], [[identity-conditioning]], [[apple-silicon-inference]], [[nightelf-hunter-plan]], [[bot-builders-champion-photo-cut-plan]]. Capability claims about tools we have not installed are marked *needs verification*.

**Last updated**: 2026-09-26 (LoRA dataset and hyperparameters; orchestration options; experiments B0–B10)

---

## 1. Why look for a different strategy

The current pipeline is fast, local, free and reliable, and it has delivered six films. Its limits are structural rather than incidental, and they all trace to the same choice — identity carried by **reference-image tokens** instead of trained weights ([[identity-conditioning]] channels 2 and 4):

| Limit | Where it bit | Root cause |
|---|---|---|
| A character only survives angles the reference shows | night-elf ears vanish under hair at distance; turnaround sheets exist precisely to patch this | reference tokens copy visible pixels; they do not generalise |
| Faces drift after ~5 s of motion, so shots are trimmed short and face shots rationed to ⅓ of a film | every film so far | first-frame latent conditioning decays with motion |
| The camera does what the model wants | "LTX obeys the action, not the staging" | no pose/depth control channel |
| No dialogue at all | every film is wordless | no TTS or lip-sync installed |
| Colour drifts between shots | the two city shots in [[nightelf-hunter-plan]] | no grade; colour is prompted, not corrected |
| Editing is a script | fine at 60 s; no J-cuts, ramps or trimming to music | ffmpeg assembly by design |

A v2 worth building is one that removes several of these at once, not one that swaps a tool.

## 2. The strategy being researched

Four substitutions, each independently testable:

| | Current | v2 candidate |
|---|---|---|
| **Identity** | seed sheet + klein edit per shot | **character LoRA** trained on 25–40 images, used in every still |
| **Motion** | prose motion prompt | **pose / depth control** (OpenPose, depth maps) driving the clip |
| **Dialogue** | none | **TTS + lip-sync** on a talking shot |
| **Finish** | ffmpeg crossfades | **NLE cut + LUT grade**, ffmpeg only for encode |

### 2a. Identity from a LoRA

The source route trains a character LoRA on 25–40 images with a trigger word, 1,500–3,000 steps, then validates across extreme angles.

What makes this newly plausible for us: **we can now generate the dataset ourselves.** `scripts/seed_sheet.sh` turns one photo into consistent views; extending it to 25–40 images across angles, expressions and lighting is a loop, not new science. The dataset problem that normally blocks a LoRA is already half-solved by the seeding phase.

Open questions:
- **Where to train.** Local LoRA training is impractical on Apple Silicon ([[character-consistency]]); cloud is quoted around \$1 per character *(needs verification of current pricing and of which services accept FLUX.2 klein)*.
- **Whether klein can consume a LoRA at all in our runtime.** `draw-things-cli` accepts `loras[]` in its config JSON with a `version` field, so the plumbing exists — but whether a klein-compatible character LoRA can be trained and loaded is **unverified** and is experiment B1.
- **Whether it actually beats a sheet.** A LoRA should generalise to unseen angles; our sheets cover four. The honest test is a profile and a three-quarter-back shot neither approach was given directly.

### 2a-i. What training a character LoRA actually requires

From the third source (`raw/2026-09-26-character-lora-training.md`, *hyperparameters unverified*):

| | Recipe |
|---|---|
| Dataset | **25–50 images**: 40% close-ups at varied angles and expressions, 40% medium (waist-up), 20% wide / full body |
| Lighting | deliberately varied, so the LoRA does not bind to one lighting style |
| Trigger | a unique token, e.g. `sks_alex_man` |
| Captions | describe background, camera angle, wardrobe and lighting — **not** permanent facial features |
| Rank / alpha | 32 or 64 / 16 or 32 |
| Learning rate | 1e-4 to 2e-4 (AdamW or Prodigy) |
| Precision | bf16 |
| Steps | 1,500–3,000 |

**The Isolation Rule is the interesting part, because it inverts our practice.** For reference-token editing we *name* every feature to preserve — "same eye shape, same jawline, same hairline, pure black hair" — because the prompt has to stop klein substituting its own face. For LoRA training you deliberately *omit* those features from the caption: anything left uncaptioned gets absorbed into the trigger token, while anything captioned stays steerable. Caption the leather jacket and it becomes optional; caption the nose and the model learns the nose is a variable.

Same goal, opposite technique. Worth writing on the wall before anyone reuses our master prompts as training captions — they are precisely the wrong shape.

**Our seeding phase is two-thirds of the dataset work.** `seed_sheet.sh` already produces consistent views from one photo by editing the master; the source's distribution is a superset of what it does:

| Source wants | We have | Gap |
|---|---|---|
| 40% close-ups, varied angle + expression | 4 views, one expression | expressions, and more angles between the four |
| 40% medium, waist-up | none — masters are head-and-shoulders | a framing variant |
| 20% wide / full body | none | a full-body variant |
| varied lighting | none — all on the same grey studio background | a lighting variant, which is the real risk: a LoRA trained only on flat grey may refuse to sit in a landscape |

A `--dataset` mode for `seed_sheet.sh` — loop the existing edit over angle × framing × lighting × expression, then caption each by the Isolation Rule with a vision model — is maybe an afternoon, and it is the same afternoon whether training happens locally or in the cloud. That makes it the first thing to build if B8 says training is possible at all.

### 2b. Motion from pose and depth

No ControlNet is klein-compatible, so this cannot live in the still stage as the source describes. It would have to live in the **video** stage, where open options exist: **Wan 2.1 VACE** and **Wan 2.2 Animate** take reference frames plus control signals; both are *unverified* in Draw Things and may require ComfyUI ([[image-to-video-models]]).

The prize is specific: a shot where the character performs a named action (draws a bow, kneels, turns to camera on a beat) instead of whatever LTX decides. Every action shot in every film so far has been chosen from what the model offered.

### 2c. Dialogue

Two pieces, both absent: TTS and lip-sync. Local candidates exist — MLX-Audio for speech, and lip-sync models that may or may not run on MPS — all *unverified*. This is the single largest expansion of what the wiki can produce: every film to date is wordless because the tooling isn't here, not because the stories wanted silence.

### 2d. Finish

The cheapest win on this list. DaVinci Resolve is free and runs on Apple Silicon; a single LUT across an assembly would fix the colour drift we currently cannot address. Frame interpolation stays unnecessary — LTX is natively 25 fps.

## 3. What v2 would look like end to end

```
1  Intake + shot list                     unchanged
2  Seeds: turnaround sheets                unchanged, but extended to a 25-40 image dataset
3  TRAIN a character LoRA (cloud)          NEW — replaces per-shot reference editing
4  Shot stills with the LoRA               changed: prompt + trigger word, no diptych
5  Clips with pose/depth control           changed: named actions instead of prose motion
6  Dialogue: TTS + lip-sync                NEW
7  Upscale (Real-ESRGAN, unchanged)        + LUT grade in an NLE
8  Cut in an NLE, export, QC               changed: ffmpeg becomes the encoder, not the editor
```

Steps 1, 2 and 7's upscale survive intact. That is the useful finding: **the seeding phase is strategy-independent** — a turnaround sheet is a good reference set *and* a good training set.

## 3b. Who drives it: orchestration options

A second question, separate from the four substitutions: **what runs the pipeline.** The source proposes Claude-Code-driven skills over local tools, or one of three open-source orchestrators (source: `raw/2026-09-26-ai-film-orchestration-options.md`; repo names verified 2026-09-26, capabilities not tested).

Worth stating first: **this project already is that orchestrator.** `scripts/film_run.py` + `spec.json` is the "turn a story into a `shots.json` manifest, then render it" pattern — a spec with per-shot prompts, takes and trims, driven from one command, with a model judging picks and QC. The interesting question is not whether to adopt an orchestrator but which parts of theirs we lack.

| Project | What it is | What it would add here |
|---|---|---|
| [`OpenX-Inc/flow`](https://github.com/OpenX-Inc/flow) | autonomous pipeline; topic → scenes → Wan 2.2 clips → stitched with narration and subtitles; last-frame conditioning for coherence; can burst to Modal/RunPod | **serverless GPU bursting** — the only credible route to LoRA training and to parallel clip renders. Its last-frame chaining we already do by hand (the rift coda, Lindsey) |
| [`juspay/director`](https://github.com/juspay/director) | TypeScript; shot planning, a **consistency critic that rejects off-brand keyframes before animating**, multi-judge scoring across weighted dimensions, self-critique before mastering | **automated QC.** Today I judge every still and clip by eye. A critic that rejects a still *before* 10 minutes of LTX time is the single highest-value idea in the whole source |
| OpenMontage | agentic production system for coding assistants; 12 pipelines, tool + skill layers, Remotion or ffmpeg assembly | a **skills/knowledge layering** pattern, and Remotion for titles and captions. Note: it exists under a dozen near-identical GitHub forks, so provenance is unclear — treat with care |
| Claude film skill / ComfyUI + Kohya API | Claude captions the dataset, fires `kohya_ss` / `musubi-tuner` training, queues ComfyUI jobs over HTTP | the **dataset-and-training half of a LoRA route**, which is exactly what B1 needs |

Three things follow:

1. **Automated pre-animation QC is worth stealing regardless of strategy.** Director's shape — critic rejects a keyframe before it becomes a clip — maps directly onto our `pick` step and would have caught the two Bot Builders shots with no child in them, and the seven night-elf stills showing a ten-year-old, without a human looking. That is experiment **B10**, and it is cheap.
2. **Serverless bursting is the lever that makes v2 possible**, not the orchestrator choice. LoRA training, ComfyUI-only control models and parallel renders all need GPU we do not have; Modal/RunPod is how the source's stack gets it. It also breaks the "everything local and free" premise, so it is a decision, not a detail.
3. **`musubi-tuner` and `kohya_ss` are CUDA-centric.** Whether either trains on Apple Silicon at all is *unverified* and is the gate on local LoRA — if the answer is no, B1 becomes a cloud experiment or nothing.

## 4. Experiments to run before adopting anything

Each is small, and each can kill the idea cheaply. Ordered by what would block the rest.

| # | Question | Test | Pass |
|---|---|---|---|
| **B0** ✅ **run 2026-09-26** | Can we build the dataset at all? | `seed_sheet.sh --dataset`: 30 images over angle × framing × lighting × expression, captioned by the Isolation Rule | 30 usable images of one character, consistent identity, varied everything else — **partial pass**, see below |
| **B1** | Can a character LoRA be trained and then used in our runtime at all? | B0's dataset, rank 32 / alpha 16, 1e-4, bf16, ~2,000 steps; load through `draw-things-cli --config-json loras[]` | it loads and the character is recognisable |
| **B2** | Does a LoRA beat a turnaround sheet? | same three shots — profile, three-quarter back, extreme wide — both ways, judged blind against the source photo | LoRA wins on the angles the sheet does not cover |
| **B3** | Can pose control reach the clip stage? | VACE or Wan Animate in Draw Things; if absent, ComfyUI on MPS with a GGUF build | a named action renders at all, at any speed |
| **B4** | Is ComfyUI usable here in 2026? | re-measure a single Wan clip; the 82 min/2 s figure is from an M1 Max and may be stale | under 15 min for a 5 s clip |
| **B5** | Local TTS quality and Mac support | MLX-Audio on a paragraph of dialogue | intelligible, no cloud dependency |
| **B6** | Lip-sync on MPS | drive an existing face clip with B5's audio | mouth tracks the audio without destroying the face |
| **B7** | Does a LUT fix inter-shot colour drift? | grade the night-elf film's eight shots to one LUT in Resolve | the two city shots stop disagreeing |
| **B8** | Can a LoRA be trained on this Mac at all? | `musubi-tuner` / `kohya_ss` on MPS with the night-elf dataset | it runs to completion; if not, B1 goes to cloud or dies |
| **B9** | What does serverless bursting cost per film? | price a LoRA train + 8 clips on Modal or RunPod | under a few dollars per film, and the local route stays the default |
| **B10** | Can the judge be automated? | a critic pass over existing candidates that scores identity, subject count and framing, run before `pick` | it rejects the known failures: the empty-room shots, the child-in-adult-armour stills |

B7 is worth doing first regardless of the rest: it is an afternoon, it needs no new models, and it improves films we have already delivered.

### B0 — result (2026-09-26, `nightelf_hunter@v2-lora-identity`)

Built with `scripts/seed_sheet.sh --dataset` from the night-elf film's approved master: 30 images,
13 min at ~26 s each, plus 10 min re-rendering 17 cells. Full audit in
[[nightelf-hunter-plan]] §6; the images are git-ignored, the 30 captions are tracked.

**Identity passed.** All 30 read as the same man, through rain, firelight, moonlight, a linen
tunic and bare shoulders. No Janus double-face in five profile cells — the ban wording from the
sheet mode holds in dataset mode too.

**Variation failed along one line**, and the line is informative: klein obeys the prompt for
anything it can **repaint** — light, background, wardrobe, expression, all 100 % — and obeys the
reference image for anything that requires **recomposing the camera**. Framing only moved once
the *canvas* changed (close 512×768, medium 512×512, wide 768×512); asking in words did nothing.
Back views came back 1 in 3 and over-shoulder 0 in 2, even when pointed at the turnaround sheet's
back panel: klein will not hide a face it can see in the reference.

**Consequence for B1 and B2.** The dataset skews toward front and three-quarter faces, which is
exactly what reference tokens already do well. Training on it would test the LoRA on its weakest
ground, so **B2 would be measuring dataset bias, not method**. B0 is therefore *not* finished by
30 images: the rear and profile share needs a non-frontal source — real photographs at those
angles, or frames pulled out of v1's rendered clips, where the hunter is already walking away.

This also sharpens **B8**: the gate on the LoRA route is now two questions, not one — can a
trainer run on this Mac at all, *and* can we source enough non-frontal images of a synthetic
character to train on.

## 5. What would make this worth switching to

Not "the industry does it this way". The bar is:

- **B2 must show a visible win on unseen angles.** If a sheet holds, the LoRA's hours and dollars buy nothing — reference tokens at 25 seconds per seed are the better trade.
- **B3 or B6 must succeed.** Pose control or dialogue would each open work the current pipeline cannot do at all. Identity alone is not a reason to rebuild.
- **Nothing may become cloud-dependent without saying so.** The whole wiki's premise is local and free; a cloud LoRA step is a real change of character for the project and should be recorded as one.

Until then the current blueprint stays the production route, and this page stays research.

## Related pages
- [[idea-to-video-blueprint]] — the current pipeline, unchanged
- [[ai-film-production-pipeline]] — the source route recorded step by step
- [[scripts-reference]] — `film_run.py`, the orchestrator we already have
- [[identity-conditioning]] — why trained weights and reference tokens differ
- [[character-consistency]] · [[image-to-video-models]] · [[apple-silicon-inference]]
