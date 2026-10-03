# Still Geometry, Anatomy and Candidate Review

**Summary**: The prompt patterns that stop klein producing broken architecture and wrong-age bodies, and the review gate that stops a broken candidate being picked. Written after `kyle_lighthouse` was abandoned over a single shot that failed five times on geometry.

**Sources**: [[kyle-lighthouse-plan]] (the failure), [[lindsey-summit-plan]], [[kyle-debut-plan]], [[lindsey-palace-plan]], [[idea-to-video-blueprint]] Phase 5 and the pick rubric.

**Last updated**: 2026-10-03

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
| **Atmosphere** | steam, mist, spray or smoke crossing the face, or any part of the subject the shot depends on |
| Identity, costume, physics, framing, cleanliness, style | as in the blueprint's pick rubric |

Then one forward-looking question, which is the one that would have saved `kyle_lighthouse`:

> **What is the video model most likely to invent here?** Anything ambiguous in the still is what it will
> elaborate. If the answer is "I am not sure what that structure is", so is the model — reject the candidate
> rather than hoping the motion prompt will hold it together, because [[lindsey-summit-plan]] establishes that
> motion prompts cannot forbid anything.

## 5. Atmosphere placed between the camera and the subject will cross the face

Weather and atmosphere — steam, mist, spray, smoke, falling snow, rain — are the most useful things to put in
a shot, because they are continuous natural motion and the video model does not have to invent it. They are
also the fastest way to destroy a face, and the failure is in the still, not the clip.

`kyle_steamfield` hit this four times in one film:

| where | prompt said | what came back |
|---|---|---|
| Kyle master | background lock contained "columns of white steam rising from fissures" | the face smeared, eyes melted — steam rendered *across* it |
| s2 candidates | the same background behind a close-up | 4 of 5 had steam over the mouth or were lost in it |
| s4 v1 | "one hand raised ... **parting a curtain of white steam**" | 4 of 5 with the face buried; the clip only cleared around frame 170 |
| s4 v2 | steam moved "behind him and out to both sides" | better, but the shot was abandoned for an unrelated reason |

The v1 phrasing could not have worked. **A curtain you part is between you and the camera by construction** —
the prompt asked for the face to be occluded and for the face to be clearly visible in the same sentence, and
the model is not able to prefer the second.

Two fixes, both positive statements rather than prohibitions:

- **Say where the atmosphere is.** "Tall columns of white steam rise well behind him and out to both sides of
  frame" places it. "Steam everywhere" or an unplaced background lock does not, and unplaced atmosphere lands
  on the subject because that is where the composition's attention is.
- **Say the intervening air is clear.** The exact phrase that fixed the master and every shot after it:

  > **clean dry air between the camera and his face**

  Not "no steam over the face" — that is a negative and negatives do not bind, as [[lindsey-summit-plan]]
  establishes.

A background lock written for landscapes will contain atmosphere, and it will follow the subject into every
close-up that inherits it. Either strip the atmosphere out of the lock for face shots, or place it explicitly.

## 6. When a face shot keeps failing, stop making it a face shot

`kyle_steamfield` s4 went through three versions. v1 and v2 both tried to hold a readable face inside a scene
whose whole point was steam. v3 abandoned the premise: full body, side-on, walking across frame. It came back
clean on the first attempt and held all 249 frames without drifting.

That is not a consolation prize. It is the better shot for a reason already established three films running:
**a frontal face drifts at around eight seconds and nothing in the motion prompt prevents it, while walking
across or away from camera holds full length every time.** A film needs its identity carried somewhere, but
it does not need every shot to carry it. `kyle_steamfield` keeps identity in two close-ups, s2 and s7, and
gives everything else to backs, profiles, macro and landscape.

The rule of thumb: if two attempts at a face shot have failed for composition reasons, the third attempt
should change what the shot *is*, not reword it.

## 7. The video model still invents cords

`kyle_lighthouse` was stopped over a shoulder rope that LTX elaborated into a cable across frame. The wardrobe
lock in `kyle_steamfield` was written with **no strap, cord or satchel** specifically to avoid that, and the
film still grew one: s3, a macro insert of two hands holding obsidian, sprouts a dark cord at the top of frame
from about frame 160 (6.4 s), and the right hand's fingers merge shortly after.

Nothing in the prompt or the still suggested a cord. The shot was trimmed to 6.0 s, which is clean.

The lesson is not "write better wardrobe locks" — that was already done. It is that **a macro shot of hands has
a short safe window**, and it should be QC'd frame by frame near the intended cut rather than trusted because
the still was good. The cost of finding this at QC is a 2-second trim; the cost of finding it after the 4K pass
is an hour.

## Related pages
- [[idea-to-video-blueprint]]
- [[kyle-lighthouse-plan]]
- [[lindsey-summit-plan]]
- [[kyle-steamfield-plan]]
- [[scripts-reference]]
