# Still Geometry, Anatomy and Candidate Review

**Summary**: The prompt patterns that stop klein producing broken architecture and wrong-age bodies, and the review gate that stops a broken candidate being picked. Written after `kyle_lighthouse` was abandoned over a single shot that failed five times on geometry.

**Sources**: [[kyle-lighthouse-plan]] (the failure), [[lindsey-summit-plan]], [[kyle-debut-plan]], [[lindsey-palace-plan]], [[idea-to-video-blueprint]] Phase 5 and the pick rubric.

**Last updated**: 2026-09-29

---

## Why this page exists

Four LoRA-driven films went out in two days. The fifth, `kyle_lighthouse`, was stopped with seven of eight shots
finished, because one shot — a boy climbing a lighthouse stair — could not be made to work in five attempts.
Every attempt failed the same way: **the still contained geometry the model had not actually resolved**, and the
video stage then amplified the ambiguity into something obviously wrong (a figure walking up a blank wall).

None of that was caught at the still stage, because the candidates were reviewed as small tiles in an unlabelled
grid. The three fixes below are prompt-side, count-side and review-side.

## 1. Prompt patterns that prevent broken geometry

**Put the camera beside a structure, not along its axis.** A spiral stair shot *up the stairwell* gives klein a
receding helix with no silhouette, and it returns a tapering wedge with no treads. The same stair shot from the
side, crossing frame as a diagonal, renders correctly. Same for corridors, ladders and towers: an oblique or
side-on camera gives the model a shape to draw.

**Name the structural members, not the object.** "A spiral staircase" is a label. "A central iron column, open
cast-iron treads winding around it, a curved handrail, slender balusters, the stringer visible from the side" is
a description the model can build. Anything load-bearing in the frame should be named as parts.

**Let structure leave the frame instead of resolving.** A stair that runs out of the top of frame is easier than
one that must terminate somewhere convincing. If it does terminate, the destination has to be *in* the shot — a
lit hatch, a landing, a doorway — or the movement reads as going nowhere.

**Say the foreground is clear.** LTX elaborates whatever is nearest the camera. A clear statement — "nothing
stands between the camera and the tower; the foreground is clear open wet rock" — is cheaper than fixing it
later.

**Prefer a subject whose motion animates itself** for any shot that must hold: surf, fire, spray, cloud, a lamp
hanging on a hook. See [[kyle-lighthouse-plan]] §1; this is the same rule from the other direction.

## 2. Prompt patterns that prevent anatomy and scale errors

**A child at full-body distance renders as an adult.** Every character LoRA here is close-heavy, and past
medium distance the body reverts to adult proportions in a long coat. Counters, in order of effect:

1. Frame closer. A medium beats an extreme wide whenever the age has to read.
2. Say the proportions: "a small nine-year-old boy **with child proportions**".
3. Give a scale referent of known size in frame — a full-height door, a stair tread, a column — and say the
   comparison out loud: "unmistakable scale of a small child against a tall heavy door".

**Ask for one figure positively.** The style lock's "no extra people beyond those described" is a negative and
does not hold: two separate shots grew a second person. "A single figure alone in the frame" works better.

**Describe skin, don't colour it.** "Cheeks reddened by cold wind" makes klein paint a blotchy red face. Weather
on skin comes from the environment; say "skin damp with fine sea spray, an even natural skin tone".

**Every prop in the wardrobe lock is a risk.** A coil of rope over the shoulder — invented by me, not asked for —
was repeatedly elaborated by LTX into a cable slashing across frame. Carry only props the story needs, and drop
a prop from a shot the moment it starts growing.

## 3. Five seeds, a labelled sheet, and a full-size look

**Five candidates per shot, not three.** `film_run.py` now defaults to `seeds: [1, 2, 3, 4, 5]`. Three was
enough when a still only had to look nice; it is not enough when one of the things being screened for is a
structural failure that appears in some seeds and not others.

**Review from a labelled sheet.** `film_run.py PROJECT sheet [ids]` tiles a shot's candidates and captions each
one with its own `c<seed>`:

```
scripts/film_run.py kyle_lighthouse sheet s6      # -> seed/s6_sheet.png, every tile labelled
```

Picking is then by seed number. Reading a grid by position is how the wrong still gets picked, and it happened.

**Look at the shortlist at full size before picking.** The wedge-shaped stair and both extra people were
invisible at tile size and obvious at full resolution. The sheet is for narrowing to two or three; the decision
is made on the full-size images.

## 4. The review checklist

Run this against each shortlisted candidate, at full size. Any hard fail rejects the candidate — this extends
the [[idea-to-video-blueprint]] pick rubric rather than replacing it.

| Check | Hard fail |
|---|---|
| **Structure** | load-bearing geometry that does not resolve: stairs without treads, a surface that is both floor and wall, a rail attached to nothing |
| **Destination** | the subject is moving, or about to, and there is nowhere in frame for them to go |
| **Age and scale** | the body reads adult when it should read child; no object of known size to judge scale against |
| **Count** | a second person; extra or missing limbs; count hands per person. For groups, count at full size on a tight crop — group counts read correctly at tile size and are wrong at full size |
| **Foreground** | a cable, rope, pole or branch across frame that the shot does not need |
| **Props** | a prop from the wardrobe lock that has grown, multiplied or moved somewhere it cannot be |
| **Skin** | blotching, plastic sheen, or colour that came from a weather adjective |
| Identity, costume, physics, framing, cleanliness, style | as in the blueprint's pick rubric |

Then one forward-looking question, which is the one that would have saved `kyle_lighthouse`:

> **What is the video model most likely to invent here?** Anything ambiguous in the still is what it will
> elaborate. If the answer is "I am not sure what that structure is", so is the model — reject the candidate
> rather than hoping the motion prompt will hold it together, because [[lindsey-summit-plan]] establishes that
> motion prompts cannot forbid anything.

## Related pages
- [[idea-to-video-blueprint]]
- [[kyle-lighthouse-plan]]
- [[lindsey-summit-plan]]
- [[scripts-reference]]
