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

Ivy is family — an adult — and consent is settled, the same standing as [[kyle-is-kevins-son]]
and Lindsey. Two practical rules follow:

- `projects/ivy_lora/*/raw/` is **git-ignored**. Consent to train on a face is not consent to
  publish the source photographs; this repository is public and they are personal photographs.
- Conversion to PNG drops the EXIF block, so **GPS coordinates do not travel with the dataset**.
  `scripts/photo_dataset.sh` does this as a side effect of resizing; it is not incidental.

## 2. The dataset

| | |
|---|---|
| Count | **22** — 16 supplied photographs plus 6 reframes cropped from their own full-resolution originals |
| Split | 11 close-up, 8 medium, 3 full body |
| Sources | Hawaii, Tahiti, Paris, Venice, Rome; indoor restaurant, cafe, boat, beach, night canal |
| Lighting | warm indoor, flat overcast, hard midday, golden hour, open shade, night flash, hazy backlight |
| Trigger | `ivy_kx`, always followed by the class word `woman` |
| Known gap | **every frame is frontal or three-quarter.** No profile, no back of head — the supplied set has none, and B0 established klein cannot invent them from a reference |

```
scripts/photo_dataset.sh raw projects/ivy_lora/v1-photo-dataset/seed/dataset 1024 ivy_kx
```

The six reframes were cropped from the 2048 px originals with ffmpeg, not upscaled from the
1024 px working copies, so they carry real detail rather than interpolated pixels. A crop of a
photograph is genuine data — a different framing of a real moment — where a klein re-render of
the same photograph would be a second-hand copy of it.

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

## 6. Result

Trained 2026-09-26: 2,000 steps in **2 h 35 m**, five checkpoints, 402 MB each. Loss 0.83 → 0.55.

**It works, at half weight.** `ivy_lora_2000_lora_f32.ckpt` at **weight 0.5** is the recommended
setting. Identity carries into scenes the dataset never contained — a red coat in deep snow, a
night market under lanterns — and the no-LoRA control renders a different person every time.

**Weight is not a volume knob here, it is a trade against angle.** The sweep says so plainly:

| Weight | Identity | Profile | Back of head |
|---|---|---|---|
| 0.3 | not her | clean | clean |
| **0.5** | **her, sharp** | **clean, though it renders three-quarter rather than a true 90°** | **clean** |
| 0.7 | her, softer | ghosting, a second face forming | blurred blob |
| 1.0 | her, flattest | badly doubled | shapeless dark mass |

The cause is the dataset gap recorded in §2 before training: all 22 frames are frontal or
three-quarter. Past ~0.5 the LoRA is strong enough to impose frontality on a sample that was
asked to turn away, and the two intentions collide into a ghosted double-face. This is the
clearest evidence yet for the B0 finding — **a LoRA cannot generalise to an angle no frame in
its dataset contains**; it actively damages it.

Checkpoint choice barely mattered next to weight. 400 through 2000 all read as her at the
studio prompt; the failure mode is identical at every checkpoint, because it comes from the data,
not the training length.

## 7. Using it

```
draw-things-cli generate -m flux_2_klein_9b_i8x.ckpt \
  --prompt "ivy_kx woman, medium shot, three-quarter view, laughing, a linen shirt, a night market" \
  --width 512 --height 768 --steps 4 --cfg 1 \
  --config-json '{"shift":3.0,"sampler":16,"loras":[{"file":"ivy_lora_2000_lora_f32.ckpt","weight":0.5}]}'
```

- Trigger `ivy_kx`, always followed by `woman`.
- **Weight 0.5.** Raise it only for a frontal close-up, and look at the result.
- Do not ask for a true profile or a back view yet. Fix that by adding real photographs at those
  angles and retraining — nothing else will.

**A gotcha worth more than the rest of this page**: `draw-things-cli` **silently ignores a LoRA
file it cannot find**. No error, no warning, and the output is pixel-identical to no LoRA at all.
Verified by md5. A typo in the filename therefore looks exactly like a LoRA that did not learn
anything, which is why `lora_eval.sh` renders a control column.

## 7b. Weight scales with face size — and the LoRA pulls the framing in

Ten editorial shots (`seed/supermodel/`) exposed a second rule. At the recommended 0.5, every
**full-body** shot came back a stranger: at that distance the face is a handful of latent pixels
and the LoRA is not strong enough to claim it. Re-rendering the wide shots at **0.85** recovered
the rooftop, street and staircase frames outright.

The two settings answer different questions and do not conflict:

| Setting | Set by | Use |
|---|---|---|
| **0.5** | the ceiling imposed by *unseen angles* — profile and back of head ghost above it | close-ups, medium shots, anything turning away |
| **0.85** | the floor imposed by *small faces* in wide shots | full-body frontal framings |

Comparing checkpoints **at 0.85** (`seed/eval_ckpt_wide/`, the four wide prompts through 400,
1200 and 2000) settles the earlier open question: **2000 wins at every framing**, so there is no
earlier-checkpoint trade to exploit. The earlier note that "checkpoint barely mattered" was
measured at weight 1.0, where all of them failed the same way.

That grid also shows *why*: as the checkpoint advances, the subject is rendered **progressively
larger and closer** for an identical prompt and seed. The dataset is 19 close and medium frames
against 3 full body, so the LoRA has learned framing along with the face and biases composition
toward the distance it was trained on. A LoRA is not a pure identity token — it carries whatever
correlates with the trigger, and **framing correlates**.

Two shots still fail at any setting: a true full-length runway walk and a figure tiny against
dunes. Neither is fixable by weight; they need a tighter render plus a crop, or a face pass after
an upscale.

## 8. Next

- Add profile and back-of-head photographs, retrain, and re-run the same grid. That is the only
  open defect.
- Add full-body frames to the dataset: 3 of 22 is what causes both the small-face failure and the
  framing bias.
- The source photographs are Facebook-compressed JPEGs; the LoRA renders slightly soft at high
  weight, and re-exporting from originals may be worth testing.
- With identity in weights rather than reference tokens, a film of Ivy no longer needs a master
  portrait carried into every shot — which is the whole point of [[blueprint-v2-research]] B2.

## Related pages
- [[blueprint-v2-research]] — B0/B1/B8, the experiments this project applies
- [[nightelf-hunter-plan]] — §6, the synthetic-dataset version and what it could not do
- [[identity-conditioning]] — why trained weights beat reference tokens on unseen angles
- [[scripts-reference]] — `photo_dataset.sh`, `lora_eval.sh`, `train lora`
