# Kyle — a Character LoRA from a Turnaround Session

**Summary**: A reusable identity LoRA for Kyle, trained on a purpose-shot turnaround (frontal, both profiles, back of head) plus four photographs from other settings. The output is an asset, not a film: `kyle_rescue`, `bot_builders_champion` and `nightelf_hunter` all carried his face by reference tokens and a master portrait, and this replaces that with a trigger token.

**Sources**: 16 HEIC turnaround frames shot for this purpose, in `raw/` (git-ignored); 4 photographs from `nightelf_hunter` and `bot_builders_champion`. Method from [[blueprint-v2-research]] B0/B1/B8 and [[ivy-lora-plan]].

**Last updated**: 2026-09-26

---

## 0. What makes this dataset different

[[ivy-lora-plan]] ended with a named defect: every frame was frontal or three-quarter, so the
LoRA *damaged* profiles and back views above weight 0.5 rather than merely failing at them.

This set was shot to fix exactly that. Kyle's 16 frames are a deliberate turnaround against one
wall: frontal, both true 90° profiles, the back of the head, and two back three-quarters, with
expressions ranging from neutral to open-mouthed to a full smile. That is the coverage the
synthetic route (B0) could not manufacture and the Ivy photo set happened not to contain.

The cost of a controlled session is the opposite bias: **one t-shirt, one wall, one light, one
distance**. Left alone, the trigger would absorb "pale blue tee on a white wall" as part of
Kyle. Two mitigations:

1. Four photographs from other settings — a warship deck, a hotel breakfast, a red parka at full
   length, a garage with a LEGO model — break the single-context lock and add the only full-body
   and outdoor frames.
2. Every caption names the shirt, the wall and the light **even though they never vary**.
   Captioning a constant is not the Isolation Rule's usual advice, but the rule's purpose is to
   decide what binds: naming a feature gives a later prompt a handle to override it. For a
   one-outfit session that handle is the difference between a character and a uniform.

| | |
|---|---|
| Count | 20 — 16 turnaround frames + 4 context photographs |
| Angles | 9 frontal, 2 true profile, 2 three-quarter, 3 back or back three-quarter, 4 varied |
| Framing | 16 close-up, 2 medium, 2 full body |
| Trigger | `kyle_kx`, always followed by the class word `boy` |
| Known bias | close framing dominates; expect the framing pull seen on Ivy |

## 1. Consent

Kyle is Kevin's son and consent is settled ([[kyle-is-kevins-son]]). `projects/kyle_lora/*/raw/`
is git-ignored: consent to train on a face is not consent to publish the source photographs to a
public repository. PNG conversion also drops the EXIF block including GPS.

## 2. The rotation trap that cost two passes

The iPhone HEICs carry **no orientation tag** — `sips -g orientation` prints `<nil>` — and store
landscape pixels of a portrait photo. Worse, the obvious fix is a lie:

> **`sips -r 90` does not rotate a PNG. It writes a rotation hint.**

The raster is untouched, so Preview, Finder and `sips -g pixelHeight` all report a corrected
portrait image while every pixel-level consumer still sees it on its side. `ffmpeg -map_metadata -1`
did not strip the hint either. The first training run got 67 steps into a sideways dataset before
Kevin spotted it in the contact sheet.

`scripts/photo_dataset.sh ROTATE=90` now bakes the rotation through PIL, which ignores the hint
and writes a clean raster. **Verify the way the consumer reads it**, never the way Preview shows
it:

```
ffmpeg -v error -y -i NN.png -vf "scale=300:-1" /tmp/check.png
```

## 3. Training

```
draw-things-cli train lora --model flux_2_klein_9b_i8x.ckpt \
  --dataset projects/kyle_lora/v1-photo-dataset/seed/dataset \
  --steps 2000 --rank 32 --learning-rate 1e-4 --seed 1 \
  --use-aspect-ratio --save-every 400 -o kyle_lora --name "Kyle (kyle_kx)" --offline
```

≈ 2 h 30 m, five checkpoints at 402 MB each, no cloud.

## 4. Evaluation

```
TRIGGER="kyle_kx boy" scripts/lora_eval.sh <out dir> "kyle_lora_400_lora_f32.ckpt,…,kyle_lora_2000_lora_f32.ckpt,-" 1.0 7
```

The `-` column is the no-LoRA control and is not optional. The prompt set must include a **true
profile and a back view**, because those are the angles this dataset was shot to cover and the
whole point of the exercise is whether that coverage shows up in the weights.

Starting weights from [[ivy-lora-plan]]: 1.0 frontal close-up, 0.85 three-quarter and full body,
0.5–0.7 turning, ≤ 0.5 profile or back. **The prediction to test is that Kyle's profile and back
ceiling is much higher than Ivy's 0.5**, because his dataset contains those angles and hers did
not. If it is not, the dataset explanation for Ivy's ceiling is wrong.

## 5. Result — the prediction held

Trained 2026-09-26, 2,000 steps in **2 h 27 m**, five checkpoints. Use
`kyle_lora_2000_lora_f32.ckpt`.

**There is no weight ceiling.** The prediction in §4 was that Kyle's profile and back views would
survive far past Ivy's 0.5 because his dataset contains those angles. They survive all the way to
**1.0**, with no ghosting, no second face and no collapse:

| Prompt | Ivy (no profile/back frames) | Kyle (2 profiles, 3 back frames) |
|---|---|---|
| true 90° profile | ghosted second face at 0.7, mush at 1.0 | **clean at every weight through 1.0** |
| back of head | blurred blob at 0.7, shapeless at 1.0 | **clean at every weight through 1.0** |
| frontal close-up | good at 1.0 | good at 1.0, strongest likeness |
| unseen scene (snow) | holds | holds |

This is as close to a controlled experiment as this project has managed: same model, same rank,
same learning rate, same step count, same captioning rule, two subjects, and the **only** material
difference is whether the dataset contained the angles being asked for. It did not merely help —
it moved the usable weight from 0.5 to 1.0 and removed the failure mode entirely.

So the rule from [[ivy-lora-plan]] generalises, and now with its cause named: **a LoRA's weight
ceiling is set by the angle coverage of its dataset, not by the trainer, the step count or the
subject.** When a LoRA damages an angle, the fix is photographs, not hyperparameters.

Checkpoint choice barely mattered — 400 already reads as Kyle at the studio prompt — but 2000 is
sharpest and has no downside here.

**Settings**: weight **0.85–1.0** for everything, 1.0 for the closest likeness. The one caveat
carried over from Ivy is unchanged and is about size, not angle: at full-body distance the face
is a handful of latent pixels and identity washes out regardless of weight.

```
draw-things-cli generate -m flux_2_klein_9b_i8x.ckpt \
  --prompt "kyle_kx boy, close-up portrait, a true side profile, a red hoodie, a school corridor" \
  --width 512 --height 768 --steps 4 --cfg 1 \
  --config-json '{"shift":3.0,"sampler":16,"loras":[{"file":"kyle_lora_2000_lora_f32.ckpt","weight":1.0}]}'
```

## 6. Next

- The blue-tee lock did not materialise: green t-shirt, red hoodie, yellow raincoat and a winter
  coat all rendered correctly. Captioning the constant wardrobe appears to have done its job,
  though that is one observation, not a controlled test.
- Full-body identity remains unsolved for both subjects. It needs a tighter render plus a crop,
  or a face pass after upscaling — not a weight change.
- A film with Kyle no longer needs a master portrait carried into every shot, which is the point
  of [[blueprint-v2-research]] B2.

## Related pages
- [[ivy-lora-plan]] — the same route on an adult, and the angle ceiling this set exists to test
- [[blueprint-v2-research]] — B0/B1/B8
- [[identity-conditioning]] · [[scripts-reference]]
