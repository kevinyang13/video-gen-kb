# Lindsey — a Character LoRA That Also Covers Full Body

**Summary**: The third character LoRA in the series, trained on 32 photographs that cover head angles *and* thirteen full-body frames. It exists to settle the one defect [[ivy-lora-plan]] and [[kyle-lora-plan]] both share: identity washing out when the subject is small in frame.

**Sources**: 32 photographs shot for this project, in `raw/` (git-ignored). Method from [[blueprint-v2-research]] B0/B1/B8.

**Last updated**: 2026-09-27

---

## 0. The question this set answers

Three runs, each fixing the previous one's defect:

| Project | Dataset | What it proved |
|---|---|---|
| [[ivy-lora-plan]] | 22 frames, all frontal or three-quarter | above weight 0.5 the LoRA **damaged** profiles and back views |
| [[kyle-lora-plan]] | 20 frames including profiles and backs | those angles then held at weight 1.0 — **the ceiling is set by dataset angle coverage** |
| this one | 32 frames including thirteen full-body | ? |

Ivy and Kyle both lost identity at full-body distance, at any weight. I read that as a
resolution limit — at that scale the face occupies a handful of latent pixels and there is
nothing for the weights to assert. But neither dataset contained a full-body frame, so the
competing explanation was never ruled out: the LoRA may simply never have been shown what this
person looks like from ten feet away.

**This dataset contains that framing.** If full-body identity now holds, the small-face failure
was a dataset gap and is fixable by photography. If it still washes out with thirteen full-body
frames in training, it is a genuine latent-resolution limit and no dataset will fix it — the
answer is a tighter render plus a crop, or a face pass after upscaling.

Either result is worth having, which is what makes it worth running.

## 1. The dataset

| | |
|---|---|
| Count | 32 |
| Framing | 19 close-up or chest-up, **13 full body** |
| Head angles | frontal, both true 90° profiles, back of head, back three-quarters |
| Body angles | full body from the front, both sides and behind, plus one mid-stride |
| Backgrounds | white textured wall (head frames); a room with wooden floor, framed artwork and a piano (full-body frames) |
| Wardrobe | one pink teddy-bear t-shirt throughout; light blue shorts in the full-body frames |
| Trigger | `lindsey_kx`, always followed by the class word `girl` |

Captions name the shirt, the wall and the light in every frame even though they never vary — the
approach that worked on Kyle, where a single-outfit session nonetheless rendered correctly in a
green t-shirt, a red hoodie and a yellow raincoat. Naming a constant does not bind it; it gives a
later prompt a handle to override it.

The two backgrounds are a small bonus: they are perfectly correlated with framing (wall = head,
room = full body), so if the LoRA has absorbed background along with framing, asking for a
full-body shot somewhere else will show it.

## 2. Consent and handling

Lindsey is Kevin's daughter and consent is settled ([[lindsey-is-kevins-daughter]]).
`projects/lindsey_lora/*/raw/` is git-ignored: consent to train on a face is not consent to
publish the source photographs to a public repository.

The JPEGs are natively portrait and carry no orientation tag, and orientation was verified
**through ffmpeg rather than Preview** — the trap from [[kyle-lora-plan]] §2, where `sips -r`
wrote a rotation hint that made a sideways dataset look correct in every Apple tool.

## 3. Training

```
draw-things-cli train lora --model flux_2_klein_9b_i8x.ckpt \
  --dataset projects/lindsey_lora/v1-photo-dataset/seed/dataset \
  --steps 2000 --rank 32 --learning-rate 1e-4 --seed 1 \
  --use-aspect-ratio --save-every 400 -o lindsey_lora --name "Lindsey (lindsey_kx)" --offline
```

Started 2026-09-27 11:00. ≈ 2 h 30 m, five checkpoints at 402 MB each.

## 4. Evaluation

The grid must include a **full-body shot in a scene the dataset never contained**, because that is
the whole question. Plus the standard rows — frontal close-up, true profile, back of head — and a
no-LoRA control column, since `draw-things-cli` silently ignores a LoRA file it cannot find.

## 5. Status

Training.

## Related pages
- [[kyle-lora-plan]] — the angle-coverage result this builds on
- [[ivy-lora-plan]] — the first run and the weight ceiling it exposed
- [[blueprint-v2-research]] · [[identity-conditioning]] · [[scripts-reference]]
