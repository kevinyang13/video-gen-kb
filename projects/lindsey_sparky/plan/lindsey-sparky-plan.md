# Lindsey — Sparky

**Summary**: Fifth LoRA-driven film and the first set indoors, which removed the ambient motion the previous four leaned on and produced two new findings about what a video model does with a static room.

**Sources**: no external source; story supplied by Kevin. Identity from `projects/lindsey_lora` v2.

**Last updated**: 2026-10-03

---

## The film

An eight-year-old inventor fails to fix her homemade robot for the seventh time, finds the mistake in
her own wiring diagram, repairs it, and watches it work.

Eight shots, 60.45 s delivered at 3840×2160.

| shot | s | LoRA | what |
|---|---|---|---|
| s1 | 9.9 | 0.85 | wide establishing, her back to us at the desk |
| s2 | 9.0 | — | macro, Sparky's visor and chest fan, no people |
| s3 | 9.5 | — | the seventh failure, smoke from the shoulder joint |
| s4 | 7.0 | 1.0 | close-up, the failure on her face |
| s5 | 3.4 | 0.6 | macro, her hand and the wiring diagram |
| s6 | 9.5 | 1.0 | medium, the repair |
| s7 | 7.5 | 1.0 | close-up, it works |
| s8 | 9.9 | — | Sparky rolling forward for the washer |

Two constraints came from Kevin: **no slow motion**, and **approval on every still before any clip**.

## The first interior, and what it cost

The four previous films were outdoors and gave their long takes to steam, surf, mist and firelight —
continuous natural motion the video model does not have to invent. A bedroom at night has none of
that, and the first pass showed exactly what fills the gap. Four of eight shots failed:

| shot | allotted | usable | what it invented |
|---|---|---|---|
| s1 | 9.0 s | 3.0 s | she stands up, walks out of frame, reads as a teenager |
| s5 | 8.0 s | 3.2 s | a blue wristwatch; the hand turns adult |
| s6 | 9.0 s | 3.1 s | a kitten and a red bottle on the desk; Sparky's arms vanish |
| s7 | 7.5 s | 1.3 s | the laugh ages her into a young woman |

The safe takes summed to 42.6 s against a 60 s target, so the film could not be cut from that material.

## What this film added

Three findings, all now in [[still-geometry-and-review]].

**A held expression survives; a changing one does not.** s4 and s7 are a controlled pair — same LoRA,
same frontal framing, same lamp, same seed count. s4 holds 7 s with a near-static face. s7 v1 asked
for a laugh and was a different, older person by frame 40, about 1.6 s. The rule was previously
written as "frontal faces drift at around eight seconds"; this film shows the eight seconds belongs
to a *static* face, and a large expression change costs most of it. The fix is not a smaller emotion
but an earlier one: the smile reaches its peak in the first second and then holds, which puts the
remaining 6.5 s into the condition s4 already proved.

**Give an interior its own light source.** s6 invented a kitten when nothing in frame moved. Told
instead that Sparky's visor brightens and dims throughout, it held all 249 frames with a bare desk.
Interiors have no weather, but they have practicals, and a lamp or an LED is as good a motion source
as surf.

**A placement lock removes the named prop and the model substitutes another.** s5 v1 grew a
wristwatch. v2 said "her wrist is bare and the hoodie sleeve stays pushed up above it" — no watch,
and a grey knit cuff instead, at frame 90. Naming the absence is not enough; the lock has to say what
the space positively *is*.

## Prompt-side fixes that worked

- **"She stays seated in the chair the whole time, her back against the chair back."** s1 v1 said
  "shifts her weight in the chair and reaches forward", which is a standing-up instruction read
  literally, and LTX read it literally.
- **Hands clear of metal.** s6's still failed all five seeds because the prompt put a screwdriver
  *into* a joint; fingers and metal in the same pixels is where the count is lost. Holding the tool
  in open air fixed it on the next attempt.

## Where the seconds came from

s5 could not be made to hold and was not re-rendered a third time. s1, s2, s3, s6 and s8 all hold
their full 249 frames, so they absorbed the difference: 65.70 s raw against 60.45 s delivered. A
3.4 s macro insert is an ordinary cut length — it was only ever long because the budget said so.

## Related pages
- [[still-geometry-and-review]]
- [[kyle-steamfield-plan]]
- [[lindsey-summit-plan]]
- [[lindsey-lora-plan]]
- [[idea-to-video-blueprint]]
