# Identity Conditioning — Why a Character Can Stay the Same

**Summary**: The mechanism behind every "consistent character" tool. A diffusion model samples each image or clip fresh from noise and remembers nothing; a character persists only if identity is injected as a *condition* the network attends to. Five mechanisms, weak to strong: text embeddings, reference-image tokens in context, identity-embedding adapters, LoRA weights, and first-frame latent conditioning inside a video clip.

**Sources**: General knowledge of diffusion-transformer architectures (FLUX.2, Qwen-Image-Edit, Wan 2.x, VACE, IP-Adapter/PuLID, LoRA); product behaviour cross-checked against the links in [[character-consistency]]. Architectural details of closed models (Kling, Veo, Seedance) are inferred and *need verification*.

**Last updated**: 2026-09-21

---

## The core concept: conditioning

A latent diffusion model starts from Gaussian noise and denoises toward whatever its conditioning inputs point at. There is no hidden state between generations — seed, prompt and conditioning are the *entire* input. So "same character across scenes" is not a memory problem; it is a question of **which channel carries the identity into each generation, and how much information that channel can hold**.

| Channel | Carries | Capacity | Used by |
|---|---|---|---|
| 1. Text embeddings | a description | low — a region of faces, not one face | every model |
| 2. Reference-image tokens (in-context) | actual latent pixels of the character | high — copies detail | FLUX.2 klein, Qwen Image Edit, Flux Kontext, VACE, Wan Animate, Kling Elements, Veo Ingredients |
| 3. Identity-embedding adapter | one compressed face vector | medium, faces only | IP-Adapter FaceID, PuLID, InstantID |
| 4. LoRA weights | the *concept* of the character | highest — generalises to unseen angles | any model with a trained LoRA |
| 5. First-frame latent (I2V) | one whole frame | high at frame 1, decays with motion | Wan 2.2 I2V, every I2V model |

## 1. Text conditioning

Prompt → text encoder (T5 / Qwen3 / Gemma) → sequence of embeddings → attended to by every transformer block. Words select a *distribution*: "young woman, long dark hair, red cloak" is satisfied by millions of faces. Same words with a new seed give a new person. Text locks wardrobe, silhouette, palette — the things that are categorical — and cannot lock a face. This is why the character bible in [[character-consistency]] helps a lot and is never enough.

## 2. Reference-image conditioning (in-context editing)

The mechanism behind the Moodboard in Draw Things and most 2025–26 consistency features.

1. Reference image → VAE encoder → latent → split into patch tokens, same as the target image.
2. Reference tokens are **concatenated into the transformer's token sequence** beside the noisy target tokens. Positional IDs are offset (a separate "picture 2" coordinate range) so the model can tell reference from canvas.
3. In joint self-attention, target tokens attend to reference tokens and copy features from them — colour, texture, geometry of the face — rather than reconstructing them from a description.
4. The model was fine-tuned on (reference, instruction, edited target) triples, so it learned the rule "preserve the identity in the reference, change what the instruction says".

Multi-reference = more token blocks with more positional offsets. Costs: sequence length grows and attention is quadratic in it; past ~5 references the model blurs which tokens to copy from (the "muddied fusion" failure in the guides).

Video models do the same thing along time: **VACE** and **Wan 2.2 Animate** append the reference image(s) as extra latent *frames* (plus a mask saying "these frames are given, do not denoise"); temporal attention then carries the identity into the generated frames. Closed models with "elements" / "ingredients" / "cameo" features almost certainly work this way at larger scale *(needs verification)*.

Limits: the model copies what it can see. A single frontal reference gives weak profiles; extreme lighting changes break the copy because the reference tokens encode lit pixels, not an albedo.

## 3. Identity-embedding adapters (IP-Adapter, PuLID, InstantID)

Older, face-specific approach for SD1.5 / SDXL / FLUX.1.

- A face recogniser (ArcFace) or CLIP image encoder turns the face into one or a few embedding vectors.
- Small adapter layers add an extra cross-attention path into the U-Net or DiT that reads these vectors.
- PuLID trains the adapter with an ID-loss so the output face scores as the same identity to a recogniser.

Compact and cheap, but one vector cannot hold a costume, a dragon, or a hairstyle. Draw Things ships these for FLUX.1 dev; klein support unknown ([[dragon-epic-plan]] E1).

## 4. LoRA — identity in the weights

Fine-tuning that adds low-rank matrices to the attention (and sometimes MLP) projections: `W' = W + A·B`, with A·B of rank 8–32, trained on 15–40 images of the character captioned with a trigger token. After training, the trigger token in any prompt steers the model into the character — from angles, lighting and outfits it never saw, because it learned the *concept*, not pixel copies.

- Strongest and most flexible channel; combinable with 2 for belt-and-braces.
- Cost: a training run (cloud ~$1 / < 1 h for FLUX.2 klein; local Draw Things training currently crashes on Apple Silicon — see [[character-consistency]] §3).
- Separate LoRAs per model: a klein LoRA does nothing for Wan; a Wan I2V LoRA teaches the *video* model to hold the face through motion.
- Failure modes: overfitting (character appears in every image regardless of prompt; only the training poses work) — pick an earlier checkpoint.

## 5. First-frame conditioning — why identity survives inside one clip

Wan 2.2 I2V (and every I2V model):

- The still → VAE → latent; it **replaces the first latent frame** of the video tensor, with an extra mask channel telling the model "frame 0 is given".
- Temporal self-attention lets later frames attend to frame 0's tokens, so its pixels propagate forward.
- Identity is perfect at frame 1 and decays as motion reveals pixels that were not in the still (the back of the head on a turn, an open mouth). The model must *invent* those from text + priors, and priors drift toward an average face.

Practical consequences (all observed on this Mac): keep faces still or on a slow push, ≤ 5 s per clip, one action; chain long moves by using the last frame of clip N as the still for clip N+1 so pixels keep carrying ([[wan22-i2v-locked-image-settings]]).

## Our stack, in these terms

```
character bible ── (1) text ──┐
character sheet ── (2) reference tokens (klein Moodboard) ──┤──► per-shot still
                                                            │
                                (5) first-frame latent ──► Wan 2.2 I2V clip
optional upgrade: (4) klein LoRA, then Wan I2V LoRA
```

All open-weight consistency tooling of 2025–26 is (2) or (4); the closed products are (2) at scale. (3) is legacy and face-only.

## Related pages
- [[character-consistency]] — which tools implement each mechanism and what runs here
- [[face-identity-workflows]]
- [[wan22-i2v-locked-image-settings]]
- [[image-to-video-models]]
