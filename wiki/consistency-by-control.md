# Consistency by Control, Not by Sampling

**Summary**: Professional pipelines do not get consistency by generating candidates and picking the best one — they move the decision out of the sampler. Composition comes from a camera in a 3D scene, geometry from a depth map, identity from trained weights, and the sampler is left to render surface. This page records the research behind that shift, the Apple Silicon boundary it has to live inside, and the one correction that makes it possible here: `draw-things-cli` has had ControlNet all along, through `--config-json`.

**Sources**: `reports/AI video character consistency pipelines.md` (deep research, 2026-10-07) and its notes in `research_notes/AI video character consistency pipelines/`; links inline. Measured timings are from this machine via [[headless-cli-pipeline]] and [[draw-things-setup]]. Failures referenced are our own, recorded in [[shot-locks]] and [[still-geometry-and-review]].

**Last updated**: 2026-10-07

---

## 1. The correction: ControlNet was never missing

`draw-things-cli` exposes 23 flags and none of them is `--controlnet`, which led this project to conclude that structural conditioning was unavailable on a Mac. That conclusion was wrong, and **our own wiki already said so**: [[headless-cli-pipeline]] §1 lists `controls[]` among the `JSGenerationConfiguration` keys accepted by `--config-json`, alongside `loras[]`, `refinerModel`, `hiresFix*` and `upscaler` (source: [draw-things-community](https://github.com/drawthingsai/draw-things-community), `ScriptModels.swift`).

Configuration precedence is model-recommended settings → `--config-json`/`--config-file` → explicit flags. Anything the GUI exposes, the JSON layer accepts.

**What this unlocks**: per-shot geometry becomes an *input* rather than an outcome. A depth or canny map rendered from a camera you chose can be handed to the same klein render that currently receives only a prompt and a reference image — so hull proportions, nacelle placement, ground contact, subject scale and framing stop being re-rolled per seed. The two worst failures in [[shot-locks]] — the "flat delta-wing" that replaced the skiff whenever the model had to invent a yard around it, and the "angular cardboard shape" in `kyle_firstflight` s7 — are both the signature of layout being decided by noise in the first few sampling steps with nothing holding it.

**Four firm limits**:

- ControlNet is the **structural half only**. It carries no identity; it is normally paired with a LoRA or an adapter.
- **Per-reference Moodboard weights are not reachable headlessly.** `setMoodboardImageWeight(weight, index)` lives in the in-app JS scripting layer and needs the app running.
- **Repeatable multi-`--image` exists only in `main`**, not the shipped binary. Building `main` here failed compiling `ccv_nnc_mfa` Metal kernels at step 524/1254. Re-check against the Homebrew formula before designing around the diptych workaround — a newer release would remove the need for it.
- The A1111-compatible HTTP API on port 7860 has **no vocabulary for Moodboard or video**.

## 2. The frame shift

The current pipeline treats generation as a *search*: produce candidates, score them, pick. Every improvement inside that frame is an improvement to the scorer. The professional pattern is not a better scorer — it is removing the search.

This reframes a result we already measured. The `align` stage's discovery that lowest palette distance selects the *emptiest* frame was not a bug in the metric. **No appearance metric over whole frames can distinguish a correct render from a confident wrong one**, and the fix is to stop asking one to.

## 3. The Apple Silicon boundary

Stop considering these:

| Ruled out | Evidence class |
|---|---|
| FP8 checkpoints (`Float8_e4m3fn` on Metal) | Proven; issue still open April 2026 |
| Triton, SageAttention, xformers, flash-attention, `torch.compile` | Proven |
| Nunchaku | Absence of evidence, not a published refusal |
| ai-toolkit FLUX LoRA training on MPS | Closed "not planned"; no convergence |
| **IP-Adapter, InstantID, PuLID** | **No confirmed working MPS report in either direction** |

The identity half of the conditioning stack does not survive on Metal; the structural half does. And for this project the adapters are moot regardless: IP-Adapter FaceID, InstantID and PuLID are built on InsightFace/ArcFace **face-recognition** embeddings, which structurally cannot represent a skiff or a droid. Only plain IP-Adapter/Plus (SD-era), FLUX Redux, and multi-reference instruction-edit models are subject-agnostic — and Redux is a *variation* adapter that no source benchmarks for identity preservation.

Note also that the DiT transition (FLUX/Qwen/Wan) broke exactly the SD-era techniques that monkey-patch attention: **Reference-Only ControlNet and Attention Couple / regional prompting do not exist for FLUX, Qwen or Wan.** Adapters, ControlNets and reference latents do. That rule is predictive for any new DiT base.

## 4. Determinism is a schedule, not a weight

The mechanism is *when* conditioning applies, not how hard:

- **Structure front-loaded** at `start_percent 0` — shape is decided in the first steps.
- **Identity released** at `end ≈ 0.65–0.8`.
- **Last ~20% free**, or the output goes rigid and overcooked.

Published per-mode strengths, from the Shakker-Labs [FLUX.1-dev-ControlNet-Union-Pro-2.0](https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro-2.0) model card (scale / guidance_end):

| Mode | Scale | Guidance end |
|---|---|---|
| Canny | 0.7 | 0.8 |
| Soft edge | 0.7 | 0.8 |
| Depth | 0.8 | 0.8 |
| Pose | 0.9 | 0.65 |
| Gray | 0.9 | 0.8 |

Pose needs the highest strength but the **earliest** release.

**Node defaults are wrong.** FLUX union nodes default to strength 1.0 on a 0–10 range; Wan VACE defaults to 1.0 on a 0–1000 range — against recommendations of 0.15–0.8. Set them explicitly.

Two cautions: BFL's own page now marks **FLUX.1 Depth and Canny deprecated**, with HF weights "for reference only", so FLUX structural control means community unions. And a 2026 RL paper names a **collapse mode** where edit models inflate consistency scores by copying the reference scene — "preserved identity" can mean stasis rather than control.

## 5. Silhouettes survive; markings do not

The only rigorous object-fidelity benchmark found is [Photoroom's](https://photoroom.com/blog/top-editing-image-models-maintain-product-details-only-28-of-the-time): 850 products, 10 annotators, 3+ reviews each, fail-if-any-flag.

| Model | Clean passes |
|---|---|
| Nano Banana 2 | 29.0% |
| Nano Banana Pro | 28.2% |
| GPT Image 2 Medium | 27.2% |
| **FLUX.2 Klein 9B** | **16.8%** (plus 28% outright invalid) |

**Klein 9B — this project's still model — is last.**

The failure breakdown matters more than the ranking, and it inverts the intuition:

| Failure | Rate |
|---|---|
| Logo / text distortion | 20.1% |
| Missing or changed elements | 12.5% |
| **Shape / cut / fit change** | **1.5%** |

The silhouette is the *safest* thing in the frame. The danger is concentrated in markings, lettering and small parts. **Design rule: keep the skiff's surface deliberately plain, give it one asymmetric marking for orientation, and composite insignia back in rather than asking the sampler to reproduce them.**

## 6. One reference per visible side

A made-up object needs a reference for every side that appears on screen, or the model invents the hidden geometry. Runware's test: a front-only reference produced a plain denim back; adding a back reference brought through an embroidered design the prompt never mentioned.

This validates the turnarounds `seed_sheet.sh` already produces — but changes how they are used. The 8 views are **production inputs to be selected per shot**, not just a consistency check at the master stage.

Reference budgets differ by an order of magnitude, and by design: Gemini 14 total in *typed* slots (10 object + 4 character) > FLUX 3 Image 10 positional with bounding boxes > FLUX.2 8 API / 6 dev / **4 klein** > Seedream 6 > Qwen-Image-Edit ~3.

BFL publishes a role taxonomy worth adopting — **Subject / Product / Setting / Style**, where *Product* is "an object whose shape, color, or label should stay the same" — with the template: *"Put the ceramic mug from image 2 on the shelf in image 1, keeping the mug's glaze and the room unchanged."* Bounding boxes are documented as "a strong hint, not a hard constraint."

**Prompt form is not portable across families.** BFL documents *imperative* instructions; Qwen's own examples are *spatial scene descriptions* ("The magician bear is on the left..."). Keep per-model templates. Our instruction-form edit prompts match BFL's pattern and should stay.

## 7. The 3D proxy: real, but not standard practice

The premise "model the hero asset in 3D, render exact angles, style with depth ControlNet" is **overstated as professional practice**. It is the highest-effort end of a spectrum, and practitioners who document the whole spectrum recommend cheaper options for most shots — Flick's own table marks render-passes-plus-ControlNet "High effort, Very high control" and recommends motion reference for the bulk of narrative work. No journalist-verified brand commercial or music video breakdown credits this pipeline. Autodesk has shipped 3D-as-direction-layer tooling (Flow Studio), and the framing there is that *the 3D scene does not necessarily produce the final pixels* — it sets staging, composition and camera.

The documented recipe, when you do use it:

- **Untextured, silhouette-accurate proxy.** Texture is irrelevant.
- **Camera placed first**, before anything else.
- **Export depth + clay.** Clay is called the single most useful pass; derive **Canny from the clay** rather than rendering Freestyle.
- **Normalise depth with a fixed near/far across the whole shot**, or the geometry breathes.
- **Cryptomatte masks** per asset for region-locked regeneration.
- **Render at the generator's resolution**, divisible by 64 — not 4K.

Two findings make this cheaper than it sounds. **Coarse proxies suffice** — LooseControl and 3DProxyImg both show a rough structural carrier is enough, and the known image-to-3D failure modes (hair, joints, decals, back-side geometry) do not matter for a depth proxy of a hull. And **the child figure should not be hand-modelled**: toyxyz's Blender rig emits depth, normal, canny, OpenPose and segmentation from one posed rig in a single render.

For the fictional craft: TRELLIS.2 (MIT, local) or Rodin Gen-2.5 (hosted, aimed at hard-surface props). Blender on an M4 Max benchmarks around an RTX 4070 / 3080 Ti, so the 3D half is free here. The maintained bridge is [ComfyUI-Blender](https://github.com/alexisrolland/ComfyUI-Blender) (v4.5.1, 2026-07); AIGODLIKE's BlenderAI-node looks stale.

**Lighting continuity is explicitly unsolved** by the 3D layer — the generated clip supplies its own lighting. That is recovered in post (§10).

## 8. Video: what actually accepts a reference

- **VACE** is the only system whose docs explicitly name *objects* ("inject people or objects of your choice"), and the only one where reference stills + masks + control video + keyframes + a custom LoRA can be stacked. **No Mac benchmark for it exists anywhere.**
- **Wan 3.0 is API-only**; no weights on HF/GitHub/ModelScope. **Wan 2.2 remains the current open generation.**
- **LTX-2.5** has native keyframe conditioning (documented token mechanism) but **no reference-identity conditioning** in the base model — there is an open feature request, filled meanwhile by community LoRA/prefix-injection nodes.
- **Reference and keyframes are often mutually exclusive.** Seedance 2.5's API *rejects* reference fields on first/last-frame requests; MiniMax H3 cannot combine them; Kling 2.6 cannot do start-frame + element reference (gated to 3.0). Veo 3.1, Kling 3.0 and Luma Ray3 allow both. Some APIs silently ignore the field and still bill.
- Reference ceilings: Seedance 30, Vidu 15, Wan 3.0 10, MiniMax/Seedance-2 9, Kling 4/element, **Veo only 3** — too few for a four-view vehicle turnaround.

The practitioner product tests show a **stability/motion tradeoff, not a consistency ranking**: the models that "hold" a product best are often the ones barely moving the camera.

## 9. What a LoRA actually buys

**A LoRA locks the look, not the geometry.** Part-count failure is a documented *base-model* weakness — diffusion models cannot count. The recommended architecture is **LoRA for appearance + ControlNet canny/depth for structure**, plus a programmatic checker.

Consensus hyperparameters for an object LoRA: rank 16–32, alpha ≤ rank, LR 1e-4 (5e-5 if unstable), batch 2 with grad-accum 2, 1,000–3,000 steps, 10–50 images. Caption with **trigger + the object's own class noun** (`skslume lamp`), cover *defining* features — seams, openings, controls, material response — rather than a mechanical turnaround, and **vary framing hard**, because FLUX learns composition as part of the subject.

**The format trap**: a `.safetensors` LoRA passed to `draw-things-cli` **runs without error and silently has no effect**. Draw Things needs its own `<name>_lora_f16.ckpt` registered in `custom_lora.json`; the app converts on UI import, the CLI does not. Conversion *out* of Draw Things is effectively broken for quantised tensors.

One number is genuinely missing: **no measured LoRA-training wall-clock for FLUX-class models on any M4 Max exists in any source.** Whether local training is an afternoon or a week is unknown. Note this contradicts nothing in [[character-consistency]] §LoRA, which records klein local training crashing at step 0 — that remains the open issue to re-check.

## 10. The evidence gap, and the benchmark we could run

**There is no published side-by-side test of a made-up mechanical object held across multiple shots.** Every identity benchmark found is face-only; every practitioner product test uses a real consumer good — a mug, a serum bottle, headphones — with one or two generations per model.

The VideoMemory paper publishes a reusable prop-consistency metric that adapts directly to a vehicle: **Grounded SAM to localise the object, then DINOv2 features compared against the reference.** This repo already has the apparatus — turnarounds, contact sheets, fixed seeds, a pairwise-views evaluator with a published calibration. Swapping `film_run.py`'s palette histogram for masked DINOv2 is roughly an afternoon, and would produce the benchmark that does not publicly exist.

## 11. Keep, replace, and the order to do it in

**Keep — these already match professional practice:**

- Model-sheet master turnarounds (Kling's element system independently converged on 1 main + 3 supplementary references with named angles).
- Combo / composed-group masters on a plain backdrop — the correct answer to "preserve a group *and* invent a landscape is two jobs, and the hull loses".
- Instruction-form edit prompts at `--strength 1.0`, matching BFL's imperative template.
- The **edit-off-combo rule** — once a group is a picture, it is edited, not re-composed. This has no published equivalent; it is the best piece of local craft in the repo.
- Locked-camera video prompts stated positively.

**Replace:**

- Candidate generation as the mechanism for getting composition right.
- Palette distance as the identity metric.
- Text-only invention of the skiff's geometry in any shot where it must match.
- Any plan that waits for an identity adapter on Apple Silicon.

**Adoption order, biggest gain first:**

1. **Prove `controls[]` works headlessly** — depth map of the existing skiff master, one shot, depth 0.8 / start 0 / end 0.8. One evening; it either unlocks everything downstream or it does not.
2. **Swap `eval`'s palette metric for masked DINOv2.** Cheapest change in the list, and every later decision depends on being able to measure drift.
3. **Blockout and pass-render the shots that already failed** — `kyle_firstflight` s3, s6, s7 are documented failures with known-good comparisons, so they are a ready-made A/B.
4. **Train a skiff LoRA** at rank 32 / alpha 16 from turnaround plus proxy renders — accepting that it locks the look while ControlNet locks the geometry.
5. Only then consider the droid's own adapter or cloud GPU work.

**48 GB is not the binding constraint; time is.** Largest confirmed single load is ~24 GB. Planning rates measured here: klein 9B still 1280×768 = **27–35 s**; klein diptych = **45–60 s**; LTX-2.3 10 s clip @1024×576 = **9 min 41 s**; Wan 2.2 I2V 81 f @576×1280 = **24 min**. For contrast, ComfyUI + Wan 2.2 GGUF on an M1 Max took **1 h 22 min for 2 seconds**.

## Related pages
- [[headless-cli-pipeline]] — where `controls[]` was already documented, and the measured CLI timings
- [[shot-locks]] — the reusable locks library; the failures this page explains structurally
- [[still-geometry-and-review]] — the review rules these findings extend
- [[character-consistency]] — the character-focused predecessor (2026-09-21), still correct on faces
- [[identity-conditioning]] — the mechanism behind every consistency tool
- [[apple-silicon-inference]] — the FP8 trap and memory planning
- [[running-a-film-yourself]] — the command sequence this would change
