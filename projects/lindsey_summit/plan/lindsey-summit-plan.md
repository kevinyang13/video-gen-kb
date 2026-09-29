# Lindsey — Above the Cloud Sea

**Summary**: A one-minute 16:9 photoreal adventure short: a child walks a pine forest at dawn, reads a compass, finds an old stone stair, climbs it, and comes out on a ruined watchtower above a sea of cloud. The third LoRA-driven film, and the first whose whole shot list was derived from the failures of the previous two rather than discovered during it.

**Sources**: [[lindsey-lora-plan]] (the trained identity), [[lindsey-palace-plan]] §6, [[kyle-debut-plan]] §6, [[headless-cli-pipeline]].

**Last updated**: 2026-09-29

---

## 1. The brief

One minute, Lindsey's LoRA, an original adventure story, 4K — and every judgement call mine. So the story was
written to the constraints rather than the other way round, which is the first time that has happened here.

## 2. The grammar this film is built from

Two films' worth of findings, applied as rules rather than rediscovered:

| Finding | Where it came from | What it does to this shot list |
|---|---|---|
| A frontal face clip drifts at ~8 s no matter what the prompt says | [[lindsey-palace-plan]] s5, [[kyle-debut-plan]] s2/s3 | face shots (s2, s4, s7) are **budgeted at 7.0–7.5 s** before anything is rendered |
| Head rotation lets LTX recast the subject entirely | lindsey_palace s5 came back an adult | **no shot turns a head.** The camera never asks for a turn |
| Hands moving in front of a stationary head is safe | kyle_debut s6 held 9.9 s | s4 is the one shot with real human movement, and it is a hand lowering a branch |
| Walking away from camera holds full length | both films | the two longest takes (s1, s6) are backs walking away |
| No face, no drift | macro and landscape shots in both films | s3 (compass macro), s5 (the stair) carry the runtime the face shots cannot |
| LTX reads "the light shifts" as *the lights go down* | kyle_debut s5/s7 dimmed to black | **every** motion prompt here says "the light stays constant" |

The story exists to give those shapes something to be. A climb is the ideal structure for it: it is mostly backs
and landscape by nature, and it earns exactly three face beats — setting out, finding the way, and arriving.

## 3. Shot list

| # | Shot | Input master | LoRA weight | Budget |
|---|---|---|---|---|
| s1 | Establishing: the forest at dawn, she is small on the trail, from behind | forest | 0.85 | 9.5 s |
| s2 | Close-up: her breath in the cold, eyes on the way ahead | lindsey | 1.0 | 7.0 s |
| s3 | Macro: a brass compass settling over a linen map — no face | lindsey | 0.6 | 8.0 s |
| s4 | Medium: she holds a branch aside and looks up | lindsey | 1.0 | 7.5 s |
| s5 | The old stone stair climbing into mist — no person | stair | **none** | 8.0 s |
| s6 | She climbs, from behind and below | stair | 0.85 | 9.5 s |
| s7 | The top — sunrise full on her face | lindsey | 1.0 | 7.5 s |
| s8 | Small at the cliff edge above the cloud sea | summit | 0.85 | 8.0 s |

65.0 s kept − 7 × 0.75 s crossfades = **59.75 s**.

Palette is deliberately the inverse of [[lindsey-palace-plan]]: cold blue mist, wool and waxed canvas, outdoors,
dawn — instead of warm gold, silk and interiors.

## 4. Locks

- **subject** — `lindsey_kx girl`, a nine-year-old girl, this exact face, long dark hair with natural flyaways
- **wardrobe** — weathered deep-green waxed-canvas jacket, cream cable-knit wool sweater, leather satchel across the body, small brass compass on a cord
- **forest** — ancient pines on a steep mountainside at dawn, cold blue mist, moss and fern over granite, light shafts through the canopy
- **summit** — a ruined stone watchtower on a clifftop above an endless cloud sea, distant peaks breaking through, low gold sunrise
- **style** — anamorphic 35mm live-action adventure, photoreal skin and wool, natural dawn light, shallow depth of field, muted colour

## 5. Settings

| Stage | Setting |
|---|---|
| Still | FLUX.2 [klein] 9B (8-bit S), 1024×576, 4 steps, CFG 1, shift 3, DDIM Trailing (sampler 16), edit mode strength 1.0 |
| LoRA | `lindsey_lora_2000_lora_f32.ckpt` @ none / 0.6 / 0.85 / 1.0 per the table |
| Clip | LTX-2.3 22B [distilled] 1.1, 1024×576, 249 frames @ 25 fps, 8 steps, CFG 1, shift 5, TCD Trailing (sampler 19), SSS 0.3 — ~11 min each |
| Upscale | Real-ESRGAN x4plus → 3840×2160, crop fit, 40M — ~10 min per clip |
| Assemble | 0.75 s crossfades, clip audio kept, 1920×1080 delivery copy |

## 6. Log

- **2026-09-29** — spec written, story written for the constraints. All four masters right on one seed each
  (seed 9), now the third film running for which that is true.

## Related pages
- [[lindsey-lora-plan]]
- [[lindsey-palace-plan]]
- [[kyle-debut-plan]]
- [[blueprint-v2-research]]
