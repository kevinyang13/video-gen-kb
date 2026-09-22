# Three-Minute Film — Project Plan

**Summary**: Plan for a ~3-minute narrative video (≈ 36–40 clips of 5 s) with one or more recurring characters, built on the Mac Studio with Draw Things + ffmpeg. Covers structure, the character-consistency stack, the per-shot workflow, gating experiments, machine-time budget, and the questions Kevin still has to answer. Living document — story, characters and style are placeholders until decided.

**Sources**: [[character-consistency]] (research 2026-09-21); [[dragon-epic-plan]] and [[runbook-living-painting]] for measured timings; `projects.json` for per-clip numbers. *verify* = untested here.

**Last updated**: 2026-09-21

---

## 1. What we are making

| | |
|---|---|
| Length | **180 s ≈ 36 hard-cut clips or ~39 clips with 0.5 s crossfades**, each 81 frames @ 16 fps (5.06 s). Same 5 s unit as every previous project — it is the sweet spot for Wan 2.2 on this hardware. |
| Cast | 1 hero (recurring in ~40% of shots) + up to 2 supporting characters (~15% each). Every extra recurring character multiplies the consistency work; keep it to three. |
| Look | **TBD** (anime/painterly like the loops, or photoreal like the dragon). Decide before the character sheets — the sheet must be in the final style. |
| Aspect / delivery | **TBD**; default 16:9 at 1024×576 generation → 4K upscale like the dragon project. 9:16 possible for a vertical cut, but a 3-minute story reads better wide. |
| Audio | Music bed + SFX (Pixabay). No dialogue in v1 — lip-sync is a separate problem. |
| Structure | 3 acts × ~12 shots. Act 1 sets character + place, Act 2 complication, Act 3 payoff. |

## 2. Pipeline

```
character bible (text) + character sheets (FLUX stills, plain bg)   raw/characters/<name>/
        │
        ▼
per-shot still: FLUX.2 klein 9B, scene prompt + character lock, sheet in Moodboard
        │           (Qwen Image Edit 2509 fallback for multi-character frames)
        ▼
Wan 2.2 I2V 81 f, one camera move + one action              (~15 min at 1024×576)
        │
        ├─ chained shots: last frame of clip N → first frame of clip N+1
        ├─ (real face only) FaceFusion on close-ups
        ▼
Real-ESRGAN ncnn 4× → 3840×2160                                (scripts/upscale_4k.sh)
        │
        ▼
ffmpeg assemble: cuts / 0.5 s xfade × 36–40 → music + SFX → title → HEVC 10-bit
```

Only new pieces vs the dragon project: Moodboard references at the still stage, the chained-shot trick, and an assembly script for N clips. No ComfyUI, nothing outside Draw Things + ffmpeg.

## 3. Character consistency stack (decided; details in [[character-consistency]])

1. **Character bible** — per character, 40–80 words, pasted verbatim into every still prompt. Also a lighting/lens/palette lock per act.
2. **Character sheet** — FLUX.2 klein still(s): front, three-quarter, profile, full-body, plain background, final style. Iterate until it is *the* character; freeze it. 3–5 images per character in `raw/characters/<name>/`.
3. **Moodboard reference on every character shot** — Control → Moodboard → sheet images; prompt refers to "the person in picture 2". Strength 0.6–0.7 if editing a base image, 100% on an empty canvas *(verify which the DT face-swap demo used)*.
4. **Wardrobe as identity** — one distinctive garment/prop per character, named in the bible.
5. **Staging** — ≥ 60% of shots without a readable face (wide, over-shoulder, silhouette, hands, inserts). Face shots: static or slow push, small head motion, ≤ 5 s.
6. **Upgrade path if the 5-shot test (X1) drifts**: cloud-train a FLUX.2 klein LoRA on 20–30 curated sheet-derived stills (ai-toolkit, ~$1, < 1 h), import into Draw Things. Wan I2V LoRA only if drift happens *inside* clips rather than between them.

## 4. Draw Things configuration

Unchanged from [[dragon-epic-plan]] §3 and the runbook, except:

| Stage | Setting | Value |
|---|---|---|
| Still | Size | **1024×576** (16:9, same pixel count as the proven 576×1024 → same ~1 min) |
| Still | Control | Moodboard = character sheet images |
| Still | Prompt | `[camera/lens/light lock] [scene] [character lock verbatim] [action]` |
| I2V | Size / frames | 1024×576, 81 f — **~15 min per clip** (measured at 576×1024); 1280×768 would be ~35 min and triple the budget — not for 40 clips |
| I2V | Refiner / LoRA | 8-bit S pair, Refiner Start 10%, Lightning 100%, 4 steps, CFG 1 (50% refiner fails — dragon v2) |
| I2V | Prompt | one camera move + one subject action; no "across the frame" for full-frame subjects (dragon ghosting) |

## 5. Shot list

Template (fill per shot once the story exists):

| # | Act | Shot | Char face? | Which chars | Camera | Chained from | Notes |
|--:|---|---|:-:|---|---|---|---|
| 1 | 1 | establishing wide | — | — | slow push | — | render first, no consistency risk |
| … | | | | | | | |

Render order: (a) all no-character shots, (b) hero wide/back shots, (c) hero face shots last, once X1–X3 have set the reference recipe. Same as the dragon project: build the assembly early with the cheap shots so the edit is visible while the hard ones render.

## 6. Experiments before committing (in order)

| # | Question | Test | Pass | Time |
|--:|---|---|---|---|
| X1 | Does the klein Moodboard hold identity across scenes? | sheet + 3 different scene prompts × 4 seeds | ≥ 3/4 per scene read as the same character | 15 min |
| X2 | Does it survive I2V? | 2 X1 stills → 81 f; compare frame 1 vs 81 at 100% | still the character at f81, incl. one head turn | 30 min |
| X3 | Chained shots | clip A → last frame → clip B; view the seam | no identity/colour jump at the cut | 30 min |
| X4 | Multi-character frame | 2 sheets in Moodboard, one still | both identities hold; if not, Qwen Image Edit 2509 (Picture 1/2/3) | 15 min (+20 GB download for Qwen) |
| X5 | Wan 2.1 VACE subject reference in DT | one T2V clip from a sheet image on white | worth it only if quality ≈ Wan 2.2 I2V — expected no | 30 min |
| X6 | Cloud klein LoRA | only if X1/X2 fail | identity ≥ Moodboard at 3 seeds | 1–2 h + ~$1 |
| X7 | `draw-things-cli` batch (DT, Mar 2026) | run 2 stills + 1 I2V from the shell | works → 40 clips unattended without UI automation | 30 min *(verify it exists in the installed version)* |

X1–X3 decide the recipe. X7 decides how painful 40 clips are.

## 7. Budget (machine time)

| Item | Estimate |
|---|---|
| Character sheets, 3 chars × ~10 seeds | 30 min |
| Stills, 40 shots × ~5 seeds × ~1 min | ~3.5 h (with review) |
| I2V, 40 × 15 min | **10 h** unattended |
| Re-renders, assume 30% | +3 h |
| 4K upscale, 40 × ~4 min | ~2.7 h |
| Assembly, music, titles | 1 h |
| Experiments X1–X7 | ~3 h |
| **Total** | **≈ 23 h**, i.e. 5–6 sessions with overnight I2V batches |

At 1280×768 the I2V line alone becomes ~23 h; not worth it when the upscaler carries the resolution. Draw Things' Cloud Compute / Server Offload is the escape hatch if the calendar matters more than the cost *(verify pricing)*.

## 8. Risks

- **Drift between shots** — the whole point of §3; X1 is the gate. Fallback: LoRA (X6).
- **Drift inside a clip** — keep faces short and still; FaceFusion only helps real faces.
- **40 clips of UI automation** — every export needs a Save click unless X7 works; batch overnight and accept one human pass per session.
- **Story fatigue** — 3 minutes of 5 s ambient shots is long. Needs real story beats and ≥ 3 camera-move types; plan the edit before rendering.
- **Multi-character frames** — highest failure odds (same as dragon shot 9); stage them as over-shoulder or wide.

## 9. Open questions for Kevin

1. **Story / subject** — what is the film about? One paragraph is enough to derive the shot list.
2. **Style** — anime/painterly (loops) or photoreal (dragon)?
3. **Characters** — how many recur; is any a real person (face photo → FaceFusion path)?
4. **Delivery** — 16:9 4K for YouTube, or 9:16?
5. **Audio** — music only, or voice-over (recorded by you) on top?
6. **Deadline** — sets whether cloud offload is on the table.

## Related pages
- [[character-consistency]]
- [[dragon-epic-plan]]
- [[runbook-living-painting]]
- [[wan22-i2v-locked-image-settings]]
- [[video-upscaling]]
- [[projects]]
