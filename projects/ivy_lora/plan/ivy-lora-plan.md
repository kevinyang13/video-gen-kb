# Ivy — a Character LoRA from Real Photographs

**Summary**: Train a reusable identity LoRA for Ivy from real photographs, so any later film loads a trigger token instead of carrying a master portrait into every shot. The output of this project is not a video — it is an asset other projects use.

**Sources**: photographs of Ivy in `raw/` (git-ignored); method from [[blueprint-v2-research]] §2a-i and experiments B0/B1/B8; training settings measured on [[nightelf-hunter-plan]] §6.

**Last updated**: 2026-09-26

---

## 0. Why photographs, not a synthetic master

The night-elf dataset (experiment B0) was built by editing one approved master 30 ways. It
worked for identity and failed for angle: klein returned back views 1 time in 3 and
over-shoulder 0 times in 2, **even when seeded from a turnaround sheet's back panel**. The
reason turned out to be mechanical — klein will not hide a face it can see in the reference
image, and the reference overrides the prompt for anything that needs the camera recomposed.

Photographs do not have that problem. A real photo set already contains profiles, backs of
heads, tilted cameras, mixed lighting and real expressions, which is precisely the share the
synthetic route could not manufacture. So this project starts where the night elf could not.

## 1. Consent

Ivy is family and consent is settled, the same standing as [[kyle-is-kevins-son]] and Lindsey.
Two practical rules follow:

- `projects/ivy_lora/*/raw/` is **git-ignored**. A public repository is the wrong home for a
  few dozen photographs of a child, whatever the consent position is.
- Conversion to PNG drops the EXIF block, so **GPS coordinates do not travel with the dataset**.
  `scripts/photo_dataset.sh` does this as a side effect of resizing; it is not incidental.

## 2. The dataset

| | |
|---|---|
| Count | 25–50 photographs |
| Split | ~40% close-up, ~40% medium, ~20% wide |
| Variety that matters | angle, distance, lighting, expression, clothing, background |
| Variety that hurts | other people in frame, heavy filters, motion blur, sunglasses, near-duplicate frames from a burst |
| Trigger | `ivy_kx` |

```
scripts/photo_dataset.sh <source folder> projects/ivy_lora/v1-photo-dataset/seed/dataset 1024 ivy_kx
```

Long side capped at 1024, aspect preserved — the trainer's `--use-aspect-ratio` buckets by
shape, so cropping to square here would discard the framing variety that justified using photos.

## 3. Captioning — the rule that inverts our practice

Every shot prompt we write names each feature to **preserve**, because klein substitutes its own
face otherwise. A LoRA caption does the opposite: it names only what **varies**, so everything
left uncaptioned binds to the trigger token.

```
WRONG  ivy_kx, a girl with long dark hair and brown eyes, smiling, in a garden
RIGHT  ivy_kx, close-up portrait, three-quarter view, smiling, a striped t-shirt, a sunlit garden, soft afternoon light
```

Naming the hair in a caption teaches the model that `ivy_kx` is steerable on hair — the one thing
it must never be. Captions are written **by hand, after looking at each photo**; an auto-caption
that mentions a permanent feature silently un-binds it.

## 4. Training

Settings carried over from the night-elf run, which passed its criterion at 500 steps and was
best at 2,000 with no sign of overfitting:

```
draw-things-cli train lora --model flux_2_klein_9b_i8x.ckpt \
  --dataset projects/ivy_lora/v1-photo-dataset/seed/dataset \
  --steps 2000 --rank 32 --learning-rate 1e-4 --seed 1 \
  --use-aspect-ratio --save-every 500 -o ivy_lora --name "Ivy (ivy_kx)" --offline
```

≈ 2 h 30 m on this Mac, 402 MB per checkpoint, no cloud. Checkpoints land in the Draw Things
`Models/` directory and appear in the app's LoRA list as well as to the CLI.

## 5. Evaluation

```
scripts/lora_eval.sh <out dir> "ivy_lora_500_lora_f32.ckpt,…,ivy_lora_2000_lora_f32.ckpt,-" 1.0 7
```

The `-` column is the **no-LoRA control**, and it is not optional: a LoRA that fails to load and
a LoRA that does nothing produce the same grid without it. Judge on the out-of-distribution rows
— an unseen scene and an unseen angle — never on the studio portrait, which always looks fine.

## 6. Status

Scaffolded. Waiting on the photographs.

## Related pages
- [[blueprint-v2-research]] — B0/B1/B8, the experiments this project applies
- [[nightelf-hunter-plan]] — §6, the synthetic-dataset version and what it could not do
- [[identity-conditioning]] — why trained weights beat reference tokens on unseen angles
- [[scripts-reference]] — `photo_dataset.sh`, `lora_eval.sh`, `train lora`
