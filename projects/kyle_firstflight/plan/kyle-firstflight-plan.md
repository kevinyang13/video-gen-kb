# Kyle — First Flight

**Summary**: Sixth LoRA-driven film and the first written to a brief of "minimal face shots, happy": one face shot in eight, a story with a reversal in it, and every long take given to machinery, dust and sky.

**Sources**: no external source; story written for this film. Identity from `projects/kyle_lora` v2.

**Last updated**: 2026-10-05

---

## The film

A boy rebuilds a wrecked skiff in a desert salvage yard with his repair droid, gets it flying, loses
both engines over the dunes, and gets them back.

Eight shots, 59.95 s delivered at 3840×2160.

| shot | s | face | what |
|---|---|---|---|
| s1 | 9.9 | — | the salvage yard at dawn |
| s2 | 7.0 | — | the droid wakes |
| s3 | 9.9 | back | working on the skiff |
| s4 | 9.0 | — | the coil spins up |
| s5 | 6.0 | **yes** | it starts |
| s6 | 9.9 | — | lift off |
| s7 | 5.0 | — | the engines cut |
| s8 | 8.5 | — | it catches |

## One face shot

The brief asked for faces to be minimised, which suits what the previous films established: a frontal
face is the least reliable thing to put on screen for nine seconds, and backs, machinery and landscape
are the most reliable. s5 is the only one, and s3 is a back view with a containment clause so nothing
turns around. Everything else is wrecks, droid, coil, dust and sky — which is also where the long takes
belong, because those things move on their own.

## The story had no story

The first version was build it, fly it, fly into the sunset. Kevin's verdict was "lame", and he was
right: no obstacle, nothing at stake, eight pretty shots in a row. The fix cost two stills and no extra
running time — s7 and s8 became **the engines cut** and **it catches**, with the droid doing the saving,
which turns it from decoration into a character and pays off its two earlier shots.

Worth keeping as a rule: *happy* is not the same as *nothing goes wrong*. A film with no reversal has
nothing for the last twenty seconds to be about.

## What this film added

**An empty bright sky behind a subject invites invention.** Two separate failures, one cause.

- **s5** lost the face to bloom in two passes. I blamed the coil glow in front of him both times. The
  sharp candidate in each batch was the one with salvage wreckage behind him rather than open sky — a
  blown-out background plus shallow depth of field was hazing the subject. Putting a wall of rusted hull
  plating close behind his head fixed it outright. This is [[still-geometry-and-review]] §5 from the
  other direction: the thing destroying the face was *behind* it, not between it and the camera.
- **s2**, a droid against a plain sky, grew a swarm of winged insects from about frame 99 — manufactured
  out of the phrase "fine dust drifts past", which gave LTX a motion instruction with nothing in frame to
  attach it to. Moving the motion onto the droid itself helped; adding "nothing flying through the frame"
  did not, because negatives never bind. The second pass still carries distant birds and was accepted.

s1 is the control: the same drifting dust, in a frame full of wrecks for it to move against, invented
nothing.

## Process notes

Two operational failures, both mine, both worth recording:

**A phase-driven pipeline stalls if nothing wakes the agent.** Each phase was launched by a watcher that
re-invoked me on completion. One didn't fire, and the project sat idle for three hours with the GPU free.
The fix is a single script that runs masters → stills → pick → clips → QC → finish in one process, with
any review step given an automatic fallback — s5's pick is made by Laplacian variance over a centre crop
rather than by waiting for judgement.

**Archiving a bad take after the loop has passed it does not get it re-rendered.** s2's failed clip was
archived at 18:08; `film_run.py` had already moved to s3, so s2 was never regenerated, and `finish`
began building a film with a hole in it. Caught at the 4K stage. Re-render first, archive second.

## Related pages
- [[still-geometry-and-review]]
- [[lindsey-sparky-plan]]
- [[kyle-steamfield-plan]]
- [[kyle-lora-plan]]
- [[running-a-film-yourself]]
