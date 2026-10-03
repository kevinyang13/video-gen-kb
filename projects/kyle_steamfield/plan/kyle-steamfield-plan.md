# Kyle — Where the Ground Breathes

**Summary**: Fourth LoRA-driven film, built to the shot grammar the previous three produced and set somewhere whose natural motion does the work: a boy crosses a steaming volcanic plain at first light.

**Sources**: no external source; story written for this film. Identity from `projects/kyle_lora` v2.

**Last updated**: 2026-10-03

---

## The film

A boy walks a black volcanic plain at first light, finds a hot spring in the lava, climbs a ridge of
broken basalt, and comes out above a whole valley full of steam at sunrise.

Eight shots, 60.15 s delivered at 3840×2160.

| shot | s | LoRA | what |
|---|---|---|---|
| s1 | 9.9 | 0.85 | wide establishing, small, from behind |
| s2 | 7.0 | 1.0 | tight close-up, frontal |
| s3 | 6.0 | 0.6 | macro, obsidian in two hands, no face |
| s4 | 7.5 | 0.85 | full body in profile, walking |
| s5 | 9.0 | — | the hot spring, no people |
| s6 | 9.5 | 0.85 | climbing the ridge, from behind |
| s7 | 7.5 | 1.0 | close-up, sunrise on his face |
| s8 | 9.0 | 0.85 | extreme wide final, tiny above the valley |

## Why the setting was chosen

Not for looks. **Steam is continuous natural motion**, so the long takes get their movement from the
environment rather than from the subject — which is the pattern [[lindsey-summit-plan]] established and
this film is the fourth confirmation of. Fire, surf, spray, mist and steam all work the same way: the
video model does not have to invent the motion, so it does not invent anything else either.

Palette is deliberately opposite to `lindsey_summit`: black basalt, white steam and sulfur yellow instead
of blue pine and gold.

## What was inherited rather than guessed

- **Face shots locked frontal at 7.0–7.5 s.** Frontal faces drift at around eight seconds whatever the
  motion prompt says.
- **Long takes go to backs, macro and landscape.** The three things that have held full length every time.
- **No strap, cord or satchel in the wardrobe**, written that way because `kyle_lighthouse` was stopped
  over a shoulder rope the video model elaborated into a cable across frame.

## What this film added

Three findings, all now in [[still-geometry-and-review]]:

**Atmosphere between the camera and the subject crosses the face.** Four instances in one film. The worst
was s4 v1, which asked for a hand "parting a curtain of white steam" *and* a clearly visible face — a
curtain you part is between you and the camera by construction. The fix, used everywhere afterwards, is the
positive phrase **"clean dry air between the camera and his face"**, plus saying explicitly where the
atmosphere is.

**When a face shot keeps failing, change what the shot is.** s4 took three versions. v1 and v2 reworded;
v3 made it a full-body side-on walking shot and it came back clean on the first attempt, holding all 249
frames. Identity does not have to live in every shot — here it lives in s2 and s7.

**The video model still invents cords.** s3 grew a dark cord at the top of frame from about frame 160,
despite a wardrobe lock written specifically to prevent it. Trimmed to 6.0 s, which is clean. A macro shot
of hands has a short safe window and needs frame-by-frame QC near the intended cut.

## Process notes

Five seeds per shot and a labelled sheet, per [[still-geometry-and-review]]. The review caught every
problem above before the 4K pass — which is the point of the gate, and is what `yang_ridge` did not get.

One operational finding worth keeping: **long renders launched from the agent's shell do not survive.**
The stills run died at 36 of 40 and the clips run died after one clip, both silently, despite `nohup` and
`disown`. Run from the user's own terminal, the same command completed seven clips without interruption.
Harness-tracked background tasks cap at 30 minutes, which is not enough for a 90-minute GPU job.

## Related pages
- [[still-geometry-and-review]]
- [[lindsey-summit-plan]]
- [[kyle-lora-plan]]
- [[idea-to-video-blueprint]]
