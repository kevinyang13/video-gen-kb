# Lindsey — The Palace Pavilion

**Summary**: A one-minute 16:9 photoreal short: a nine-year-old girl in an emerald silk royal gown alone in a palace pavilion above domes and waterfalls. Seven shots. The first film in this repo where **identity comes from a trained LoRA rather than a reference photograph** — no source image is touched at render time, and the LoRA weight is set per shot rather than globally.

**Sources**: [[lindsey-lora-plan]] (the trained identity), [[blueprint-v2-research]] §B1/B8 (weight-per-shot), [[idea-to-video-blueprint]] Phase 4/4b, [[headless-cli-pipeline]].

**Last updated**: 2026-09-28

---

## 1. The brief

One prompt, supplied whole:

> a 9-year-old girl in an ornate palace pavilion overlooking domed architecture and waterfalls. She wears a
> high-fashion, Naboo-inspired royal gown in rich emerald green silk with gold lace trim, high structured collar,
> and intricate embroidery along the bodice. Soft ambient sunlight with subtle rim light highlighting natural
> flyaway hair, razor-sharp focus on facial detail and silk texture, Leica S3 quality.

One minute long, using `lindsey_lora`. No evaluation grid first — by request.

## 2. What is different about this film

Every previous photoreal project carried a face by **reference image**: a photo in the left half of a diptych,
or a seed master re-edited shot to shot. That works, and it is also the thing that limits framing — the face
only survives where the reference can reach.

Here the face is in the weights. Consequences, all of which shape the shot list:

- **The stills are text-to-image plus an environment reference.** The `--image` input is the *pavilion* or the
  *wardrobe master*, never a photograph of Lindsey. Identity rides on the token `lindsey_kx girl`.
- **Weight is a per-shot dial**, not a project setting. This is the operative result out of `ivy_lora` and
  `kyle_lora`: at 1.0 a character LoRA holds a face hard and starts taking prompt grip away from wardrobe;
  below ~0.6 it stops being the same child.
- **No LoRA at the video stage.** LTX never sees it. Whatever identity is in the still is all the identity the
  clip will ever have, which is an argument for spending the still budget on the close shots.

## 3. Shot list and the weight table

| # | Shot | Input master | LoRA weight | Why that weight |
|---|---|---|---|---|
| s1 | Extreme wide: she is small at the balustrade, seen from behind | pavilion | 0.85 | face is a few pixels; the gown and the valley need the prompt |
| s2 | Medium three-quarter at the balustrade, looking out | lindsey | 1.0 | face readable, identity matters |
| s3 | Tight close-up portrait, rim light on flyaway hair — the hero shot | lindsey | 1.0 | maximum identity, wardrobe is only the collar |
| s4 | Macro insert: silk, gold lace, embroidery, hands on the stone rail | lindsey | 0.6 | **no face in frame**; all grip goes to fabric |
| s5 | True profile, backlit, she turns toward camera | lindsey | 0.85 | profile is the angle the dataset covers but the one that punished Ivy |
| s6 | Wide full body from behind, walking the colonnade | pavilion | 0.85 | full body at distance — the framing that failed for Ivy and Kyle |
| s7 | Close-up frontal, the faint smile, hold | lindsey | 1.0 | the closing beat |

Seven takes trimmed to 9.25 s, six 0.75 s crossfades: **60.25 s**.

s5 and s6 are the interesting ones. Lindsey's dataset is the only one of the three that carries both true
profiles and thirteen full-body frames, so the prediction from [[lindsey-lora-plan]] is that these hold where
Ivy's and Kyle's would not. This film tests that in motion instead of in a grid.

## 4. Locks

Four strings reused verbatim across all seven prompts, so the shots cannot drift apart:

- **subject** — `lindsey_kx girl`, a nine-year-old girl, this exact face, long dark hair with natural flyaway strands
- **gown** — emerald green silk, gold lace trim, high structured collar, intricate gold embroidery on the bodice
- **place** — pale carved stone pavilion, tall slender arches, carved balustrade, a valley of golden domes and tall waterfalls in rising mist
- **style** — Leica S3 medium format, 120mm, soft ambient sunlight with a subtle rim light, razor-sharp focus, shallow depth of field, fine grain

The trigger token leads every still prompt. The class word `girl` follows it immediately, as in training.

## 5. Settings

| Stage | Setting |
|---|---|
| Still | FLUX.2 [klein] 9B (8-bit S), 1024×576, 4 steps, CFG 1, shift 3, DDIM Trailing (sampler 16), edit mode strength 1.0 |
| LoRA | `lindsey_lora_2000_lora_f32.ckpt` @ 0.6 / 0.85 / 1.0 per the table above |
| Clip | LTX-2.3 22B [distilled] 1.1, 1024×576, 249 frames @ 25 fps, 8 steps, CFG 1, shift 5, TCD Trailing (sampler 19), SSS 0.3 — ~10 min each |
| Upscale | Real-ESRGAN x4plus → 3840×2160, crop fit, 40M |
| Assemble | 0.75 s crossfades, clip audio kept, 1920×1080 delivery copy |

## 6. The finding: the LoRA stops at the still

The clips exposed something the stills could not, and it is the most useful thing this project produced.

**LTX never sees the LoRA.** Identity is baked into the still and nothing renews it for the next 249 frames. So
any motion that *hides the face and then shows it again* hands the video model a free choice, and it does not
choose Lindsey.

- **s5 — true profile, "she turns toward camera."** The head rotated through the back of the skull and the face
  that came back was **an adult woman**. Re-rendered with an explicit "she does not turn her head": it turned
  anyway, and recast her again. A profile still appears to be unstable input — LTX wants to resolve it to a
  frontal face, and it invents the frontal face it was never given.
- **s2 — three-quarter, "keeps looking out over the valley."** Same failure, slower: fine for six seconds, then
  she turns away and the back of an adult's dress fills frame.
- **s4 — the macro silk insert.** Not a face problem but the same shape: the sleeve inflated and folded into a
  wing by the eight-second mark. "The sleeve stays flat against her arm — nothing lifts, flaps or folds over"
  fixed it.

**The rule this gives us**: with a LoRA-carried face, write video prompts with no occlusion and no rotation.
Breathing, blinking, hair in wind, fabric settling, walking *away* — all stable. Turning, looking back over a
shoulder, anything that passes through profile — not stable, at any LoRA weight, because the weight is not in
the room by then.

Corollary in the cut: the shots that hold longest are the ones with no face to lose. s6 (walking away down the
colonnade) and s8 (the valley, no person at all) are the only two clips usable for their full 9.9 seconds.

## 7. What the cut ended up being

Order is **s1 s2 s3 s4 s8 s5 s7 s6** — the valley insert placed where the film needs a breath, the walk away
from camera moved to the end as the closer.

| # | Shot | Take | Kept | Why trimmed there |
|---|---|---|---|---|
| 1 | Establishing, she is small at the balustrade | s1_v1 | 9.9 s | clean throughout; LTX added a slow drift instead of the locked camera, which suits it |
| 2 | Three-quarter at the balustrade | s2_v2 | 6.5 s | she turns away after ~6.5 s and is recast |
| 3 | Close-up portrait — the hero shot | s3_v1 | 8.0 s | push-in creeps too close after 8 s |
| 4 | Macro: silk, lace, embroidery | s4_v2 | 8.5 s | v2 fixed the inflating sleeve; drifts to a hand at the end |
| 5 | The valley itself, no person | s8_v1 | 9.9 s | nothing can drift |
| 6 | True profile, backlit | s5_v2 | 3.6 s | **the head turn recasts her as an adult**; only the hold survives |
| 7 | Close-up frontal, the faint smile | s7_v1 | 9.9 s | carries the whole arc, identity holds to the last frame |
| 8 | Walking away down the colonnade | s6_v1 | 9.9 s | clean throughout; back of head, nothing to lose |

66.20 s kept − 7 × 0.75 s crossfades = **60.95 s**.

An eighth shot was added part-way through for exactly this reason: once s5 collapsed to 3.6 s the film was
around 52 s, and the cheapest way back to a minute was a shot with no face in it.

## 8. Log

- **2026-09-28** — spec written; both masters rendered first try (seeds 7 and 11). The wardrobe master came out
  with the face, the gown and the valley all correct in one pass, which is the LoRA doing the work a diptych
  used to do. Still candidates rendering.

## Related pages
- [[lindsey-lora-plan]]
- [[blueprint-v2-research]]
- [[idea-to-video-blueprint]]
- [[headless-cli-pipeline]]
- [[nightelf-hunter-plan]]
