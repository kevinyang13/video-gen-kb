# Kyle — Five Minutes to Showtime

**Summary**: A one-minute 16:9 photoreal short: the five minutes before a nine-year-old walks out to lead a symphony. Eight shots in a neoclassical conservatory foyer — composure, the waiting piano, a collar straightened, the oak doors opening, the walk toward the stage. The second LoRA-driven film, and the first written from the start to the rule that came out of [[lindsey-palace-plan]].

**Sources**: [[kyle-lora-plan]] (the trained identity), [[lindsey-palace-plan]] §6 (the occlusion rule), [[blueprint-v2-research]], [[headless-cli-pipeline]].

**Last updated**: 2026-09-28

---

## 1. The brief

A supplied portrait prompt — navy velvet double-breasted blazer with satin lapels, silk pocket square, crisp
white collar, marble columns and crystal chandeliers, Hasselblad, Vogue Kids catalog style — plus a storyline:
Leo, the youngest pianist ever to lead the city's symphony, waiting out the last five minutes in the foyer while
the hall fills behind the doors. A chime. He straightens his collar and breathes. The doors open, golden stage
light floods the marble, and he walks toward it.

## 2. Two limits this film was written around

**The video model never sees the LoRA.** Identity is fixed at the still; LTX then has 249 frames in which nothing
renews it. On [[lindsey-palace-plan]] a shot that turned the head through profile came back as a different,
adult person — twice, including once with an explicit instruction not to turn. So here **every face shot is
locked frontal**, and motion is restricted to breathing, blinking, and hands. The storyline's one turn — *"turns
smoothly on his heel"* — is not animated as a turn at all: s8 is rendered as a still that already faces away,
and the motion only continues the walk. Walking away from camera was one of the two things that held for a full
ten seconds last time.

**Kyle's dataset is close-heavy.** Sixteen turnaround frames and exactly one full-body photograph, so identity is
dependable in close-up and at angle but not at full-body distance — the failure Ivy and Kyle shared. The two
wides (s1, s8) therefore sit at 0.85 and are composed so the face is either small or turned away, and they carry
the story rather than the likeness.

## 3. Shot list and the weight table

| # | Shot | Input master | LoRA weight | Motion allowed |
|---|---|---|---|---|
| s1 | Establishing: the empty foyer, he stands small at its centre | foyer | 0.85 | light and dust only; he is still |
| s2 | Medium, hands at his sides, holding the lens | kyle | 1.0 | breathe, blink |
| s3 | Hero close-up: the calm unflinching gaze | kyle | 1.0 | breathe, blink |
| s4 | Detail: satin lapels, silk pocket square, white collar | kyle | 0.6 | fabric settles; nothing lifts |
| s5 | The piano waiting, alone in a side hall | piano | **none** | light and dust only |
| s6 | He adjusts his collar and takes a slow breath | kyle | 1.0 | hands, breath, eyes up — no head turn |
| s7 | The oak doors open, stage light floods the marble | doors | **none** | light spreads, dust turns |
| s8 | From behind, walking toward the stage | foyer | 0.85 | walking away; he never turns back |

Eight takes trimmed to 8.3 s, seven 0.75 s crossfades: **61.15 s**.

Three of the eight shots have no face in them at all (s4 has no head, s5 and s7 have no person). That is
deliberate, not filler — those are the shots that cannot drift, and last time they were the only ones usable for
their full length.

## 4. Locks

- **subject** — `kyle_kx boy`, an elegant nine-year-old boy, this exact face, neat dark hair
- **wardrobe** — bespoke navy velvet double-breasted blazer, satin lapels, fine silk pocket square, crisp white tailored collar shirt
- **place** — grand neoclassical conservatory foyer, polished marble columns, checkerboard marble floor, crystal chandeliers, heavy double oak doors at the far end
- **style** — Hasselblad medium format, soft diffused chandelier light, ultra-realistic skin texture, sharp focus, warm wood and marble reflections, Vogue Kids catalog

## 5. Settings

| Stage | Setting |
|---|---|
| Still | FLUX.2 [klein] 9B (8-bit S), 1024×576, 4 steps, CFG 1, shift 3, DDIM Trailing (sampler 16), edit mode strength 1.0 |
| LoRA | `kyle_lora_2000_lora_f32.ckpt` @ none / 0.6 / 0.85 / 1.0 per the table |
| Clip | LTX-2.3 22B [distilled] 1.1, 1024×576, 249 frames @ 25 fps, 8 steps, CFG 1, shift 5, TCD Trailing (sampler 19), SSS 0.3 — ~11 min each |
| Upscale | Real-ESRGAN x4plus → 3840×2160, crop fit, 40M — ~10 min per clip |
| Assemble | 0.75 s crossfades, clip audio kept, 1920×1080 delivery copy |

## 6. What the clips did with the rule

The rule held where it was followed, and the one thing it did **not** buy was immunity from the drift — only a
shorter useful take.

**Writing "he does not turn his head or look away" does not stop it.** s2 and s3 both turned away in the final
second anyway, exactly as lindsey_palace s5 did with the same instruction. The instruction is not a control
surface; the only reliable protection is the cut. Every frontal face shot here goes soft at roughly the
eight-second mark, so **7.0–7.5 s is the real ceiling for a face shot**, not the 9.9 s the clip length offers.

**Hands and breath are safe; that part worked.** s6 — both hands up to the collar, settling it, coming down,
eyes up to the lens — held all 9.9 s with no identity drift at all. That is the most movement any face shot in
either film has survived, and it confirms the distinction: articulated motion in front of a stationary head is
fine, rotation of the head is not.

**The shots with no face still win.** s4 (macro velvet and pocket square) held its full length, as the equivalent
shot did last time.

**A new one: LTX reads "the light shifts" as "the lights go down."** s5 (the waiting piano) and s7 (the open
doors) both dimmed steadily toward black — s5 is nearly unusable past five seconds. It suits the story, since a
hall does dim before a performance, so both are cut at the point where the dimming reads as intent rather than
as an error. Worth writing the next light-motion prompt as "the light stays constant" if a constant is what is
wanted.

## 7. The cut

| # | Shot | Kept | Why trimmed there |
|---|---|---|---|
| s1 | Establishing, he stands small at the centre | 9.9 s | clean throughout; LTX added a slow push in, which suits it |
| s2 | Medium, hands at his sides | 7.0 s | turns away in the last second |
| s3 | Hero close-up | 7.5 s | a smile arrives at ~5 s, then he turns away |
| s4 | Detail: lapels, pocket square, collar | 9.9 s | stable throughout — no face to lose |
| s5 | The piano waiting | 5.2 s | the light dims toward black past ~5 s |
| s6 | He adjusts his collar and breathes | 9.9 s | **held the full length** — hands and breath, no rotation |
| s7 | The doors open, light floods the marble | 7.5 s | dims at the end like s5 |
| s8 | Walking toward the stage | 9.0 s | he walks away and shrinks; last second goes dark |

65.9 s kept − 7 × 0.75 s crossfades = **60.65 s**.

Music is the same Pixabay solo piano used on `lindsey_art` and `lindsey_palace`. Reused deliberately here: solo
piano is the one instrument this particular story requires, and its first minute builds to ~50 s and resolves
at 60 s.

## 8. Log

- **2026-09-28** — spec written. All four masters (kyle, foyer, piano, doors) came out right on one seed each,
  same as lindsey_palace: with identity in the weights, the first pass is usable. Still candidates rendering.

## Related pages
- [[kyle-lora-plan]]
- [[lindsey-palace-plan]]
- [[blueprint-v2-research]]
- [[nightelf-hunter-plan]]
