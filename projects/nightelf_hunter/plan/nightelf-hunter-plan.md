# Night Elf Hunter — a Hunter and His Bear Crossing the Grassland

**Summary**: A 57-second 16:9 photoreal fantasy short: a half-elf hunter with Kevin's son's face walks the grassland toward a distant walled city, a brown bear at his side. Eight shots, rendered entirely with `draw-things-cli`. The project's real subject is **seeding** — a character turnaround sheet, an animal, and two location plates made before a single shot was rendered — and what happens when a seed and its prompts disagree.

**Sources**: `raw/kyle_ship.jpg`, `kyle_breakfast.jpg` (Kyle's face); [[idea-to-video-blueprint]] Phase 4/4b; [[identity-conditioning]]; [[headless-cli-pipeline]].

**Last updated**: 2026-09-26 (v2: experiment B0, the LoRA dataset)

---

## 0. Result

**Delivered** 2026-09-26 05:16: `final/nightelf_hunter_3840x2160.mp4` (57.64 s, 278 MB) and `nightelf_hunter_1920x1080.mp4` (85 MB). Music "Adventure Journey" (The_Mountain, Pixabay) under the LTX ambience; mean −18.8 dB, peak −5.9 dB.

| # | Shot | Seeded from | Kept |
|---|---|---|---|
| s1 | Establishing: the pair small in the grassland, city on the horizon | land plate | 9.5 s |
| s2 | Tracking alongside, hunter and bear walking | hunter master | 6.5 s |
| s3 | The bear's head pushing through the grass | bear plate | 9.9 s |
| s4 | He stops and looks toward the city — the one face shot | hunter master | 8.0 s |
| s5 | Low through the grass: boots and paws passing | land plate | 5.0 s |
| s6 | The bear stops, his hand on its shoulder | hunter **back** panel | 9.9 s |
| s7 | The city closer, towers catching the light | city plate | 6.0 s |
| s8 | Cresting the rise, the last look before the gates | land plate | 8.0 s |

No shot was dropped. Every trim is a drift point, not an aesthetic choice: s2 loses the hunter entirely after ~6 s and the bear walks on alone; s5 empties as both leave frame; s7 hits an LTX end-fade at 6.28 s; s8 loses the bear late. The two steadiest clips — s3 (bear close-up) and s6 (hand on the bear's shoulder) — held the full 10 s, which matches the motion-stability rule from [[lost-city-plan]]: slow, in-place action survives, travel does not.

## 1. Decisions

| Question | Answer |
|---|---|
| Look | photoreal live-action fantasy |
| Elf treatment | **half-elf** — Kyle's face and skin, long pointed ears, faint blue-green markings; no purple skin, no glowing eyes |
| Age | adult, about twenty-eight |
| Format | 16:9, 60 s target, 8 shots |
| Sound | LTX ambience + one music bed |
| Gate | seeds approved, then unattended to delivery |

Photoreal was chosen knowing it exposes likeness gaps that stylisation hides ([[bot-builders-champion-photo-cut-plan]] §2). The mitigation is staging: **one face shot out of eight**, everything else from behind, small in frame, or the animal alone.

## 2. Seeds

Four seeds carried the whole film:

- **Hunter** — Kyle's ship photo → klein edit at strength 1.0 adding ears, markings and leather armour → aged to an adult → a four-view turnaround (`seed_sheet.sh`).
- **Bear** — text-to-image plate, real grizzly build, leather harness, on all fours.
- **Grassland plate** and **city plate** — empty landscapes, "no people, no text".

Shots then used the panel that matched their angle: s6 is seeded from `hunter_back.png`, not the front portrait, which is the entire point of a sheet.

**Ageing took two passes.** "A grown man in his early thirties" produced a 45–55-year-old; adding *"about twenty-eight, in his athletic prime, clear taut skin, no deep wrinkles, no crow's feet, not middle-aged"* landed it.

**The profile came back with two faces** — a Janus artifact, the frontal face kept and a profile added beside it with the ear between them. Fixed in `seed_sheet.sh` itself: the side prompt now demands one visible eye and forbids a second face.

## 3. The mistake: a seed and its prompts disagreeing

The first full still batch came back with **a ten-year-old boy in adult armour** in seven of eight shots.

The master had been aged up on request, but the character lock embedded in every shot prompt still read *"a young half-elf hunter boy of about ten"*. klein follows the text. The seed was an adult; the prompts said child; the prompts won.

**Rule**: changing a master does not propagate. The lock and every prompt that embeds it must change with it, and the run-spec must be re-synced from the scenes afterwards. This is the same family as the mixed-generation failure on the Bot Builders photo cut — a stale ingredient that passes every per-shot check because nothing compares the shot against its own seed.

Cost: 24 wasted candidate renders, about 25 minutes.

## 4. Settings

klein 9B, 4 steps, CFG 1, shift 3, DDIM Trailing, 1024×576, edit mode at `--strength 1.0`. LTX-2.3 distilled, 8 steps, CFG 1, TCD Trailing, SSS 0.3, shift 5, 249 frames at 25 fps, ~10 min per clip. Real-ESRGAN x4plus to 3840×2160; crossfades 0.75 s.

Whole run: seeds ~15 min, stills 2 × 25 min (one wasted), clips 78 min, finish 72 min.

## 5. What to fix in a v2

- The city changes character between shots — a fairy-tale castle in s7, a denser skyline in s8. One city plate is not enough; seed the gate, the walls and the skyline separately, or chain s8 from the approved s7 still.
- The hunter's ears are hidden by hair in several shots; naming them in the prompt is not enough at small scale.
- s2's disappearing hunter is a tracking-shot failure — the same "subject slides out of frame" problem Lost City solved by phrasing the move as the camera keeping the subject centred.

## 6. v2 — the LoRA identity route (research, not a second film)

`projects/nightelf_hunter/v2-lora-identity/` exists to answer the B-series experiments in
[[blueprint-v2-research]]. v1 stays the delivered cut; v2 renders no shots. Phase 1 is
**experiment B0 — can we build a training dataset at all?**

**What B0 builds**: 30 images edited from v1's approved master (`seed/hunter.png`) across
six axes — framing (12 close / 12 medium / 6 wide), angle, lighting, expression, wardrobe
and background — one klein seed per cell, plus a caption `.txt` beside each image.

**The one thing that inverts our practice.** Every prompt on every project so far names
each feature to *preserve*, because klein substitutes its own face otherwise. A LoRA caption
does the opposite: it names only what **varies**, so that everything left uncaptioned binds
to the trigger token instead. So each cell carries two different strings:

```
PROMPT  (makes the pixels)  The same half-elf hunter, exactly the same face … the same long
                            slender pointed ears, the same faint pale blue-green markings …
CAPTION (trains the LoRA)   nelf_kyle, close-up portrait, three-quarter view, a rain-soaked
                            cloak, a dense forest edge, dim grey storm light, alert, eyes wide
```

Face, ears, markings, hair and age appear in the prompt and are **absent from the caption on
purpose**. Wardrobe *is* captioned and *is* varied, so the armour stays steerable rather than
being welded to the character.

**What it cost**: ~26 s per image — 13 min for the 30, plus a 10 min second pass over 17 cells. No new models, no cloud, 21 MB.

**Results**: the dataset builds, and identity is the part that works. All 30 images read as the
same man; no Janus double-face appeared in five profile cells; the pointed ears and the eye
markings survive rain, firelight, moonlight and a shaved-down tunic. One first-pass failure
(`ds_19`, hair lightened to brown under a rim light) cleared on a re-render.

What does **not** work is the variation, and it fails along one clean line:

| Axis | Honoured | Why |
|---|---|---|
| lighting | 10/10 | prompt-only, and klein repaints light freely |
| background | 7/7 | same |
| wardrobe | 7/7 | same |
| expression | 9/9 | same |
| framing | after the fix | **the canvas decides it**, not the prompt |
| angle — profile | 4/5 | the master shows enough of the head to rotate |
| angle — back | 1/3 | klein will not hide a face it can see in the reference |
| angle — over-shoulder | 0/2 | same |
| camera height | 2/4, weakly | same |

**The mechanism**: everything klein can *repaint* obeys the prompt; everything that requires
*recomposing the camera* obeys the reference image instead. A head-and-shoulders master asked
for a medium shot returns a head-and-shoulders shot. The fix that worked was to stop asking and
change the canvas — close cells stay 512×768, medium cells became 512×512, wides are 768×512 —
and the medium row visibly pulled back. The fix that did **not** work was pointing the back and
over-shoulder cells at v1's `hunter_back.png` panel: only one of three came back facing away.

**Why this matters for B1 and B2**: the dataset is skewed toward front and three-quarter faces —
precisely the angles reference tokens already handle well. Training on it would test the LoRA on
its weakest possible ground, and **B2 would measure dataset bias rather than method**. Before B1,
the back and profile cells need a source that is not a frontal portrait: real photos at those
angles, or frames lifted from v1's rendered clips, where the hunter is already turned away.

**What it does not answer**: whether any trainer runs on Apple Silicon (**B8**) — until that is
known, B1 cannot start locally, and the dataset is the only part of the LoRA route that is
identical whether training ends up local or rented.

## Related pages
- [[idea-to-video-blueprint]] — Phase 4 and 4b, seeding and how to feed a seed into a shot
- [[blueprint-v2-research]] — the B-series experiments v2 exists to answer
- [[identity-conditioning]] · [[character-consistency]]
- [[headless-cli-pipeline]] · [[scripts-reference]]
