# Character Consistency Across Scenes

**Summary**: How to keep one character looking like the same person/creature across many shots in a generated video, ranked for the Mac Studio + Draw Things pipeline. The winning local recipe (as of 2026-09-21) is *reference-conditioned stills* — FLUX.2 klein with the character sheet in the Moodboard — feeding the existing Wan 2.2 I2V step, with a text "character lock" in every prompt and a cloud-trained LoRA as the upgrade path.

**Sources**: Web research 2026-09-21 (links inline); [[face-identity-workflows]] (face-specific subset); [[dragon-epic-plan]] §5 (first field notes). Everything marked *verify* has not been tested in Draw Things on this machine.

**Last updated**: 2026-09-21

---

## The problem in one line

Every clip is a fresh sample. Nothing carries over between shots unless you put it there — via **text**, **pixels** (a reference image in the first frame), **weights** (a LoRA), or a **model that accepts a separate identity input**. Real projects stack two or three of these. Mechanism per channel: [[identity-conditioning]].

## Layers, cheapest first

### 1. Text lock — the character bible (free, always on)

Write a 40–80 word paragraph per character: age, build, hair, eyes, skin, one signature feature, wardrobe (colour + material + one detail), props. Paste it **verbatim** into every still prompt; never paraphrase. Guides across the board call this the baseline and say to fix the reference structure before rewriting prompts when drift appears (source: [magichour](https://magichour.ai/blog/how-to-keep-characters-consistent-in-ai-video), [aimagicx](https://www.aimagicx.com/blog/long-form-ai-video-character-consistency-guide-2026)). Field note from the dragon project: text consistency is ~70% of the battle for non-human subjects ([[dragon-epic-plan]] §5).

Also lock what surrounds the character: lighting family, lens, time of day, colour palette. Characters "drift" most when the light changes.

### 2. Reference-conditioned stills (recommended core; zero installs)

Generate each shot's **first frame** with the character sheet as a reference, then animate with the proven [[wan22-i2v-locked-image-settings]] step. Identity lives in the still; I2V only has to hold it for 5 s.

Two in-app options, both already downloadable in Draw Things:

| Model | How in Draw Things | Notes |
|---|---|---|
| **FLUX.2 [klein] 9B** (already installed, used for all stills) | Base image or empty canvas + reference image(s) in **Control → Moodboard**; prompt refers to "the person in picture 2"; Strength 0.6–0.7 when editing an existing base, steps 4–8 | Draw Things demonstrates face swap this way (source: [Draw Things on X](https://x.com/drawthingsapp/status/2014756085438283811), [note.com guide](https://note.com/sane_weasel8589/n/ne8649e756cbe)). FLUX.2 accepts multiple references; community guides say 3–5 refs is the sweet spot, >7 muddies, keep lighting uniform and angle variance < 90° (source: [selfielab](https://selfielabstudio.com/blog/flux-2-multi-ref-character-consistency-guide-20260329) — written for FLUX.2 dev/pro CLI; *verify the same holds for klein 9B 8-bit in DT*) |
| **Qwen Image Edit 2509** | Base on canvas = Picture 1, refs on the moodboard = Picture 2, 3…; prompt like "the girl in Picture 2 is sitting on the sofa in Picture 1" | Draw Things added multi-image referencing for 2509 in Oct 2025; ControlNet (pose/depth) goes in Picture 1 (source: [DT wiki](https://wiki.drawthings.ai/wiki/Qwen_Image_Edit)). ~20 GB download; *verify* quality vs klein |

Workflow: make a **character sheet** first (front, three-quarter, profile, full body on a plain background — one FLUX still or 3–4 separate ones), then every shot still = scene prompt + character lock + sheet in the Moodboard. Iterate seeds; keep the one where the identity reads. Save sheets under `raw/characters/<name>/`.

Weakness: I2V softens identity over 5 s, most on faces (see [[face-identity-workflows]]). Keep face shots ≤ 5 s, one action, camera mostly still.

### 3. Character LoRA (weights; the upgrade when 2 drifts or the cast is large)

**For the still model (FLUX.2 klein):**
- Local training in Draw Things (PEFT tab) supports SDXL, Flux.1 dev, Kolors, SD3 — klein was added later but **crashes at step 0 on Apple Silicon** (MPS SwiGLU backward assertion, issue open since Aug 2026; source: [draw-things-community #114](https://github.com/drawthingsai/draw-things-community/issues/114), [DT wiki](https://wiki.drawthings.ai/wiki/LoRA_Training)). Re-check after each DT update.
- Cloud: ostris/ai-toolkit trains a klein LoRA in < 60 min on a 4090, ~$0.50 on RunPod; 15–40 images, non-word trigger token, caption content not style, pick a checkpoint around steps 750–1500 by eye. The official guide targets **klein-base-4B**; 9B "receives minimal discussion" (source: [HF blog](https://huggingface.co/blog/black-forest-labs/flux-2-klein-lora)). A 4B LoRA does not load into the 9B model — either train on 9B base or switch stills to klein 4B for that character. *verify* DT imports the resulting `.safetensors` as a klein LoRA.
- Dataset for a fictional character: 20–30 stills generated from the locked sheet (method 2), curated for identity, varied angle/expression/light.

**For the video model (Wan 2.2 I2V):** cloud trainers (RunComfy / ai-toolkit) train an I2V character LoRA in 30–60 min on a modern GPU; pays off past ~20 clips of the same character and is the fix for face drift *during* the clip rather than in the still (source: [RunComfy](https://www.runcomfy.com/trainer/ai-toolkit/wan-2-2-i2v-character-consistency-lora), [wan27.org guide](https://wan27.org/blog/wan-2-2-lora-training-guide)). Note T2V and I2V LoRAs are trained separately. Loads in DT as a plain LoRA alongside Lightning (*verify* stacking two LoRAs on the 8-bit S pair).

### 4. Reference-to-video models (identity as a separate input to the video model)

| Model | Identity input | Runs here? (as of 2026-09-21) |
|---|---|---|
| **Wan 2.1 VACE** in Draw Things | subject reference image(s) on white background in the Moodboard, plus T2V prompt; also first/last-frame control | **Yes, in-app** since DT 1.20250616.0, Wan 2.1 T2V base + CausVid/self-forcing LoRA (source: [Draw Things on X](https://x.com/drawthingsapp/status/1935515572911140882)). Wan 2.1 quality < Wan 2.2; *verify* whether DT's VACE also runs on the 2.2 experts |
| **Wan 2.2 Animate-14B** (Animate-2 weights released 2026-08-07) | character image + driving video → replaces the performer, copies motion/expression, relights | Open weights, but CUDA/ComfyUI only; no Mac port found. Cloud via Replicate/fal (source: [HF](https://huggingface.co/Wan-AI/Wan2.2-Animate-2-14B), [Replicate](https://replicate.com/wan-video/wan-2.2-animate-replace)) |
| **LTX-2.5** (22B, open) | native multi-shot in one pass (holds identity/voice across cuts, up to ~5 min claimed) + Multi-Subject Reference LoRA (≤ 5 refs) + reference-sheet IC-LoRA | Mac via `ltx-2-mlx` int8 ≈ 21 GB, unproven for these LoRAs (source: [ltx.io](https://ltx.io/model/capabilities/multi-shot-video-generation), [LTX blog](https://ltx.io/blog/how-to-use-ic-lora-in-ltx-2), [HF](https://huggingface.co/Lightricks/LTX-2.5)). Experiment track, see [[image-to-video-models]] |
| Wan 2.6 / 2.7 reference-to-video, multi-shot | up to several refs, 15 s clips | **API only** — no weights published for 2.5/2.6/2.7 (source: [Runpod](https://www.runpod.io/articles/guides/wan-2-7-runpod)) |
| Kling Elements, Veo Ingredients, Seedance refs, Sora cameo | 1–9 reference images | closed, per-clip cost; strongest results. See [[video-generation-landscape]] |

### 5. Post-process (faces only)

FaceFusion swap after I2V, before upscale — re-locks a *real* face; useless for creatures or stylised characters. Details in [[face-identity-workflows]] C.

### 6. Continuity tricks that cost nothing

- **Shot staging**: most shots do not need the full face. Over-shoulder, silhouette, wide, hands/props read as "the same character" for free; spend the reference budget on 25–30% of shots.
- **Wardrobe as identity**: a distinctive jacket/cloak/hat survives I2V far better than a face. Give every character one.
- **Chained shots**: for a continuous move longer than 5 s, use the last frame of clip N as the first frame of clip N+1 (I2V from that frame). Identity carries because pixels carry.
- **Same seed does nothing** across different prompts — do not rely on it.
- **Fewer, longer-held faces**: face at frame 81 drifts most when the head turns; keep head motion small, camera static or slow push.

## Decision table

| Situation | Stack |
|---|---|
| Fictional character, ~30 shots, local only | **1 + 2 (klein Moodboard) + 6**; if 5 test shots drift → add 3 (cloud klein LoRA, ~$1) |
| Real person's face | 1 + 2 + FaceFusion on close-ups; LoRA if many projects |
| Many characters in one frame | 2 with Qwen Image Edit 2509 (Picture 1/2/3 addressing) *verify*; or LTX-2.5 multi-subject LoRA |
| Need the character to *perform* (dialogue, dance) | Wan 2.2 Animate on cloud, or closed models |
| Money OK, best quality | Kling Elements / Veo Ingredients / Seedance for hero shots, local for the rest |

## Related pages
- [[identity-conditioning]]
- [[face-identity-workflows]]
- [[dragon-epic-plan]]
- [[wan22-i2v-locked-image-settings]]
- [[image-to-video-models]]
- [[video-generation-landscape]]
- [[draw-things-setup]]
