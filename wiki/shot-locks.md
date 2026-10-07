# Shot Locks — the reusable ones

**Summary**: The lock paragraphs that have been written, failed, fixed and proven across the films here, kept in one place so a new project starts from them instead of rediscovering them.

**Sources**: `kyle_saltflats` v1, `kyle_firstflight`, `lindsey_sparky`, `kyle_steamfield`.

**Last updated**: 2026-10-06

---

## Why this page exists

`kyle_saltflats` v1 shipped pilots who looked like grown men. The fix was a lock stating the age, the
trigger token, the wardrobe and a scale referent, and it worked. That lock then stayed inside that
project's `spec.json`, so `kyle_firstflight` started from a blank page and shipped **"a small figure low
in the open cockpit"** — the identical failure, two films later.

Locks are the part of a spec most worth carrying forward and the part least likely to be, because each
project writes its own `scenes.locks` from scratch. Copy from here.

## A child in or on a vehicle

The hardest case: the figure is small in frame, the machine is the subject, and every one of these
renders as an adult without all four parts.

```
In the open cockpit sits kyle_kx boy, a small nine-year-old boy with child proportions, this exact
face, wearing <wardrobe>. He is unmistakably a small child in a machine built for someone far bigger:
his head and shoulders barely clear the <cowling/fairing>, the seat rises well above him, his arms are
short against the controls, and his small frame leaves the cockpit looking half empty around him.
```

Four parts, all load-bearing:

1. **The trigger token** — `kyle_kx` / `lindsey_kx` / `ivy_kx`. Without it the LoRA binds to nothing.
2. **The stated age** — "a small nine-year-old boy with child proportions".
3. **A scale referent in frame** — the machine itself, said out loud as too big for him.
4. **The wardrobe**, so he is the same person between shots.

Add for any shot where the face is small or turned away:

```
He is seen small at this distance and his face is not readable.
```

## A child at full-body distance

```
<trigger> boy, a nine-year-old boy with child proportions, this exact face, <hair>, wearing <wardrobe>,
<action>. The <door / stair tread / hull / doorway> beside him gives the unmistakable scale of a small
child against something built for adults.
```

## Faceless shots — the containment clause

A still with no face in it cannot survive a motion that reveals one; see
[[still-geometry-and-review]] §11. Phrase as what stays, never as what must not happen.

| the still shows | the clause |
|---|---|
| her back | "She stays turned away from the camera, her back to us for the whole shot, and does not turn around." |
| a person seated, from behind | "She stays seated in the chair the whole time, her back against the chair back." |
| hands only | "The shot stays on her hands and the desk the whole time; the camera does not tilt up and no face comes into frame." |
| a prop or an empty room | "No person enters the frame at any point." |
| a pilot too small to read | "The pilot stays low in the cockpit and his face never turns toward the camera; nobody else enters the frame." |

## A face that has to hold

A static expression survives about eight seconds; a changing one costs most of that
([[still-geometry-and-review]] §8). Put the peak in the first second and then hold it.

```
His <expression> reaches its full width in the first second and then holds steady for the rest of the
shot without changing. His head stays level and still and his chin does not lift.
```

And light it against something dark — a blown-out sky behind a face hazes it at shallow depth of field:

```
Close behind him stands <a wall of rusted hull plating / dark wreckage> in deep shade, dark and softly
out of focus, filling the frame behind his head so there is no bright sky anywhere in shot. Nothing
glowing or bright stands between the camera and his face and the air in front of him is clear.
```

## A hovering vehicle

State what holds it up, or the model will fill the gap with wheels:

```
The whole machine hovers a clear metre above the ground with a clean unbroken band of open air beneath
it from end to end, a hot blue repulsor glow washing down onto the ground, and its hard shadow falling
directly below it. It has no wheels, no tyres, no axles and no landing legs: nothing touches the ground
anywhere.
```

Put the same guarantee in the motion prompt, or it settles over nine seconds:

```
The machine stays hovering clear above the ground throughout with open air beneath it the whole time
and never touches down.
```

## Pacing

```
Everything moves at natural real-time speed, with no slow motion and no speed ramping.
```

## Masters are model sheets, not single images

A shot's `still.ref` can only carry what the reference shows. A single frontal master gives the model
nothing to copy for a profile or a back, so it invents one — which is why the skiff in
`kyle_firstflight` is a different craft in every shot that was not handed `skiff.png`.

```bash
scripts/film_run.py PROJECT masters        # 3 candidates per master
scripts/film_run.py PROJECT pick kyle 3    # choose the hero view
scripts/film_run.py PROJECT views          # -> turnaround + expressions model sheet
```

`views` produces `seed/<name>_front.png`, `_34.png`, `_side.png`, `_back.png`, optional expression heads,
and a composed `seed/<name>_model.png` for review. A shot then references **the view that matches its
framing** — `_side` for a profile shot, `_back` for a back view, `_expr_smile` for the face shot — rather
than a frontal master for everything.

Three things the generator does that a naive turnaround does not:

**Each view references the previous one, not the master.** Side is rendered from the three-quarter, and
back from the side, which halves the rotation at each step. A 90-degree turn straight from a frontal
reference produces a Janus artifact: klein keeps the front face and adds a profile beside it with an ear
in the middle.

**Framing comes from the canvas, not the prompt.** Body views use a tall canvas and head views a square
one, because asking a head-and-shoulders reference for a "full body shot" returns head and shoulders.

**The backdrop is plain, and that is the point.** A master shot in a location drags that location into
every shot that references it. Keep masters on a pale studio sweep with no scenery.

For a prop, a vehicle or anything without a face, pass `EXPR=""`. An object asked for a "worried
portrait" grows a face to be worried with — the droid came back with a human face inside its dome.

### A master is a person or an object, and the spec must say which

The two need different view language. A person's turnaround asks for "a full-length view from head to
feet, standing square to the camera, arms relaxed at the sides". Applied to a craft, klein supplies a
person to own the head and feet: the `kyle_firstflight` skiff turnaround came back as **a man holding a
model aeroplane**, in all eight views, with nothing erroring.

```json
"master_views": {
  "kyle":  {"kind": "person", "expr": "neutral alert smile"},
  "skiff": {"kind": "object", "expr": ""},
  "yard":  {"skip": true}
}
```

`kind` is **required** and is never guessed at render time. Deriving it by word-counting the lock was
tried and is not reliable enough to act on — `dunes` reads as a person because the lock says "dune
*faces*", and a character whose description lives under `subject` rather than its own master name reads
as nothing at all. The heuristic survives only inside the error message, as a suggestion to the author.

The general rule this came from: **a default that silently selects the wrong template is worse than no
default.** Eight renders completed, nothing failed, and the fault was visible only in the picture.
`check` and `lint` both refuse to proceed without a declared kind.

## Turning a negation into something that binds

Across 114 shot prompts in this repo there is about **one authored negation each**, and the most common
ones are a list of this project's documented failures:

| written | what came back |
|---|---|
| "no tow cables and no trailing lines" | a cable across frame |
| "no wheels, no tyres, no axles, no landing legs" | wheels and landing legs |
| "no flame at the front" | flame out of the forward intakes |
| "no extra people beyond those described" | a second person, twice |
| "nothing flying through the frame at any point" | an insect swarm, then birds |

A negation names a thing and leaves the space it occupied undescribed, and undescribed space next to a
subject gets filled. The fix is always the same shape — **say what is there**:

| instead of | write |
|---|---|
| no wheels | "a clean unbroken band of open air beneath it from end to end, a blue repulsor glow washing down onto the ground, its hard shadow directly below" |
| no flame at the front | "the forward intakes are wide dark open throats with a cone hub at the centre, drawing air in" |
| no steam over his face | "clean dry air between the camera and his face" |
| no extra people | "a single figure alone in the frame" |
| nothing flying through the frame | "the sky behind it stays completely empty and clear" *(this one still failed — prefer putting the motion on the subject instead)* |
| no cords or straps | carry no prop the story does not need; a prop that is not in the wardrobe cannot grow |

The last row is the general case. The cheapest negation is the one you never have to write, because the
thing was never introduced.

## Three defects that are readable before rendering

`film_run.py PROJECT lint` reads every prompt and reports these without spending a GPU-second.

**A contradiction the model cannot resolve.** `kyle_steamfield` s4 asked for a hand "parting a curtain of
white steam" *and* a face "well exposed and clearly visible". A curtain you part is between you and the
camera by construction. Three versions were rendered before the prompt was read properly. `lint` fails on
an occluder and a visibility demand in one prompt.

**Motion with nothing in frame to attach to.** `kyle_firstflight` s2 said "fine dust drifts past" over a
droid against an empty sky. There was no dust in the still, so the video stage manufactured something to
carry the motion — insects, and on the retake, birds. `lint` warns when the motion prompt moves a noun
the still never mentions.

**A motion acting on more subjects than the still contains.** `kyle_saltflats` s7 described an overtake
between two machines over a still holding one. `lint` fails on this.

## What `check` enforces

`film_run.py PROJECT lint` fails on a contradiction, and on a motion acting on more subjects than the
still contains; it warns on every authored negation, on unplaced atmosphere in a shot that needs a
visible subject, and on motion with no anchor in the still.

`film_run.py PROJECT check` fails the run on:

- a shot describing a person with no trigger token while a LoRA is applied and the face is in frame;
- a shot describing a person with no age or child-proportions cue, at any distance.

and warns on:

- a shot describing a locked object whose master is neither its `still.ref` nor its `still.input`;
- a faceless still whose motion prompt carries no containment clause;
- a LoRA applied to a faceless shot with no trigger token — wasted sampling time.

## Related pages
- [[still-geometry-and-review]]
- [[idea-to-video-blueprint]]
- [[running-a-film-yourself]]
- [[character-consistency]]

## A diptych prompt is an edit instruction, or the subject is thrown away

`dt_diptych.sh` in diptych mode hstacks REF and IN into one canvas twice the output width, renders it,
and keeps the **right half**. The model only knows that canvas is two images if the prompt says so.
Given a plain scene description it lays the scene across the whole canvas, the subject lands wherever
the composition puts it, and the crop discards whatever fell in the left half.

Measured on `kyle_firstflight` v2 s4 — same seed, same scene-description prompt, only the reference
swapped:

| Run | Palette distance | Subject present? |
|---|---|---|
| REF = `skiff_90` (the right master) vs REF = `droid_front` (a deliberately wrong object) | **0.061** | neither |
| REF = `skiff_90` vs REF = none (single-image edit) | **0.333** | edit only |

Two readings, both bad. Swapping the reference for an unrelated object changed the result by less than
the drift *within* one master's own turnaround (droid: 0.026–0.076), so no identity was crossing over.
And neither diptych contained the thruster nacelle the prompt described, while the single-image edit
did — the nacelle had been composed into the half that gets cropped off.

So a reference is not "weakly used" in this mode. It is close to inert, and the mode actively costs you
the subject. This is the mechanism behind "the size, the shape, the identity of the aircraft doesn't look
the same at all across all the shots".

**Choose the mode by what the shot needs:**

- **One locked subject, no new environment** → single-image edit. Set `still.input` to the master and
  leave `still.ref` unset. The master *is* the image being re-rendered, so it cannot be cropped away.
- **A locked subject placed into a different environment** → diptych, `ref` = the subject, `input` =
  the environment plate, and the prompt written as an edit instruction naming both halves.

Setting `ref` and `input` to the same subject is always wrong: it spends half the canvas carrying in an
identity the input already has.

`film_run.py check` fails on a diptych whose prompt has no edit-instruction marker, and warns on a
self-diptych. See also [[still-geometry-and-review]] §12.
