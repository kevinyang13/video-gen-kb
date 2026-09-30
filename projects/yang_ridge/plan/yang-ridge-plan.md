# Yang Family — Under the Meteor Sky

**Summary**: A one-minute 16:9 photoreal short: Kyle, Lindsey and Ivy hike a high desert ridge at dusk, build a fire, and watch a meteor shower. The first film from the multi-subject [[yang-family-lora-plan]], and the first here with more than one real person in a frame.

**Sources**: [[yang-family-lora-plan]], [[kyle-lighthouse-plan]], [[lindsey-summit-plan]], [[kyle-debut-plan]], [[still-geometry-and-review]].

**Last updated**: 2026-09-30

---

## 1. The story exists to justify the adapter

Three separate character LoRAs can render three people one at a time and cannot render two of them together —
two character adapters loaded at once fight over the same face. `yang_family_lora` was trained to fix that, so
this film has to actually use it:

- **s5** is a two-shot of Ivy and Lindsey at the fire. It is the reason the LoRA exists.
- **s1** and **s8** put all three in frame, at distance.

Everything else is the accumulated shot grammar from the four previous films.

## 2. Inherited grammar, applied without rediscovery

| Rule | Where it came from | Applied here |
|---|---|---|
| A frontal face clip drifts at ~8 s | every previous film | s3, s4, s5, s7 budgeted at **7.0 s** |
| Head rotation lets the video model recast the subject | [[lindsey-palace-plan]] | no shot asks anyone to turn |
| Backs walking away hold full length | all | s1 — three of them from behind |
| No face, no drift | all | s2 (macro fire), s6 (night sky) |
| Pick subjects whose motion animates itself | [[kyle-lighthouse-plan]] | fire, sparks, drifting cloud, a meteor carry every long take |
| "The light stays constant" — except where light **is** the subject | [[kyle-lighthouse-plan]] | used on s1; deliberately absent from the fire and meteor shots |
| Say the count positively | [[still-geometry-and-review]] | "two people alone in the frame", "three figures alone" |

## 3. The new risk: identity bleed

A multi-subject LoRA can leak one subject's features into another's prompt. Three defences, all at the
composition level rather than in the prompt wording, since motion prompts cannot forbid anything:

1. **Separate the faces in space.** s5 specifies "a clear gap of dark air between their heads so the two faces
   never overlap", and names each subject with its own trigger, class word **and position in frame** — Ivy on
   the left, Lindsey on the right.
2. **Keep multi-person shots short.** s5 is cut at 7.0 s like any face shot.
3. **Hide the faces when there are three.** s1 and s8 are from behind and at distance, so bleed cannot show
   even if it exists.

The seven masters are themselves the bleed test: three subjects rendered individually plus the two-shot. If
Ivy's master comes back with Lindsey's face, that is known before a single shot is rendered.

## 4. Shot list

| # | Shot | Master | Weight | Budget |
|---|---|---|---|---|
| s1 | Three of them on the ridge trail at dusk, from behind | ridge | 0.85 | 9.5 s |
| s2 | Macro: two pairs of hands feeding the new fire | fire | 0.5 | 9.0 s |
| s3 | Close-up — Kyle, firelit | kyle | 1.0 | 7.0 s |
| s4 | Close-up — Lindsey, firelit | lindsey | 1.0 | 7.0 s |
| s5 | **Ivy and Lindsey together at the fire** | pair | 1.0 | 7.0 s |
| s6 | The Milky Way and a meteor over the canyon | night | **none** | 9.5 s |
| s7 | Close-up — Ivy, watching the sky | ivy | 1.0 | 7.0 s |
| s8 | All three small under the sky, silhouettes | night | 0.85 | 9.5 s |

65.5 s kept − 7 × 0.75 s crossfades = **60.25 s**.

Palette: cold blue night against warm firelight — the fifth distinct look in five films, after the palace's
gold, the conservatory's marble, the summit's blue dawn and the lighthouse's storm grey.

## 5. Settings

| Stage | Setting |
|---|---|
| Still | FLUX.2 [klein] 9B (8-bit S), 1024×576, 4 steps, CFG 1, shift 3, DDIM Trailing, edit mode strength 1.0, **5 seeds** |
| LoRA | `yang_family_lora_4000_lora_f32.ckpt` @ none / 0.5 / 0.85 / 1.0 |
| Clip | LTX-2.3 22B [distilled] 1.1, 249 frames @ 25 fps, 8 steps, CFG 1, shift 5, TCD Trailing, SSS 0.3 |
| Upscale | Real-ESRGAN x4plus → 3840×2160 |
| Assemble | 0.75 s crossfades, clip audio kept, 1920×1080 delivery copy |

## 6. Log

- **2026-09-30** — spec and masters written; queued to render automatically when `yang_family_lora` finishes
  training.

## Related pages
- [[yang-family-lora-plan]]
- [[kyle-lighthouse-plan]]
- [[lindsey-summit-plan]]
- [[still-geometry-and-review]]
