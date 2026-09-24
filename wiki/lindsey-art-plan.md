# Lindsey: A Small Dream — 1-Minute Plan

**Summary**: A 60-second vertical 3D-animated short made from Lindsey's 5-panel comic. She draws at the kitchen table, practises every day, finds her own style, holds her first art exhibition, and ends hugging her favourite animals at sunrise. It's the second film through the [[idea-to-video-blueprint]], the first run entirely by `scripts/film_run.py` from a run-spec, unattended after "go".

**Sources**: `raw/lindsey/comic_source.jpg` (5-panel comic, 1374×1145, added 2026-09-23); [[idea-to-video-blueprint]]; [[kyle-antarctic-rescue-plan]] §0 (method and rules this reuses); [[scripts-reference]] (run-spec format).

**Last updated**: 2026-09-23 (**delivered** — §0 results; 5 redos, 2 caught by Kevin)

---

## 0. Results — 2026-09-23 12:50 → 17:26

**Delivered**: `raw/clips/lindsey/final/lindsey_art_1080x1920.mp4` (59.96 s, HEVC, 95 MB), `lindsey_art_2160x3840.mp4` master (301 MB), `lindsey_art_720x1280.mp4` phone preview (23 MB). Music from 0 s with a 2 s fade out; mean −15.8 dB, peak −0.8 dB. Everything ran through `scripts/film_run.py` from the run-spec.

![Final film, one frame every 5 s](assets/lindsey-final-strip.jpg)

![Master + S1–S8 first frames (final)](assets/lindsey-stills-sheet.jpg)

### Takes

| Shot | Still | Take | Kept | Notes |
|---|---|---|---|---|
| S1 | edit of S2, seed 1 | v1 | 0–5.4 s | camera drifts and the cat shrinks to a tail after ~f140 |
| S2 | diptych, seed 3 | **v3** | 0–6.5 s | v1: grey tabby → black-and-white cat (f124). v2: second cat head + pan (f140). v3: one cat, looks up and smiles |
| S3 | **restaged**: no hands, pencil lying flat | **v3** | 0–9 s | v1 + v2 stills/clips had two hands on the pencil — see below |
| S4 | diptych, seed 2 | v1 | 0–9.96 s | clean for the full clip |
| S5 | diptych, seed 1 | v1 | 0–9.96 s | push-in ends on the turtle canvas |
| S6 | diptych with S7, **new still** seed 2 | **v2** | 0–8.5 s | v1: people walked through dark signboards |
| S7 | diptych, seed 3 | v1 | 0–6.5 s | end fade from f169 (auto-detected) |
| S8 | diptych, seed 2 | **v2** | 0–9.3 s | v1: she sank out of frame with the horizon fixed |

13 LTX renders for 8 shots (9 min 20 s – 9 min 29 s each), 24 + 12 still candidates, 8 upscales in 73 min.

### What went wrong — and who caught it

![Rejected frames: S2 v1 cat swap · S3 v2 second hand · S6 v1 people through signboards · S8 v1 girl sinking](assets/lindsey-rejects.jpg)

- **Kevin caught two errors I had passed.** Both were visible only at full size; I had judged 216-px thumbnails.
  - **S3:** two hands on one pencil.
  - **S6:** the comic's chalkboard became dark standing boards that people walked through.
- **Once I re-checked at full size, I found a third: S8 v1.** She slid down out of frame while the horizon stayed put, so "the camera rises" had become "the girl sinks".
- **S3 needed a restage.**
  - "Exactly one hand" in the still prompt gave two hands in 2 of 3 seeds, and a stray sleeve in the third. A follow-up edit removed the sleeve.
  - The clip then grew a second hand anyway (v2, from f80).
  - LTX keeps inventing the other hand on a hand close-up, so S3 became the sketches alone with a pencil lying on them. A candidate with the pencil balanced on its tip was rejected.
- **S6's new still** banned signboards, easels and stands, and put about 8 people well apart on an open floor. The motion prompt also says "never passes through another person, the walls, the frames or the flower pots".

![Still fixes: S6 before/after, S3 before/after](assets/lindsey-still-fixes.jpg)

### New rules (added to [[idea-to-video-blueprint]])

1. **Judge at full size.** Count hands per person; look for bodies passing through props. Thumbnails hide both.
2. **Hand close-ups on LTX grow a second hand**; restage as hands-free or keep the hand small.
3. **Standing props in crowd shots** (signboards, easels) invite intersections; prompt them out.
4. **A small or partly hidden animal gets re-invented**; pin it ("exactly one cat, the same grey tabby stays curled up asleep in the same place").
5. **"Camera rises" can become "subject sinks"**: check that the horizon moves. For endings, "camera holds completely still" or an eye-level pull-back is safer.
6. `qc_sheet.sh` now **auto-detects the end-of-clip fade** (S6 f222, S7 f169, S8 v2 f238).

## 1. Decisions (Kevin, 2026-09-23 intake)

| Question | Answer |
|---|---|
| Who | Lindsey, Kevin's daughter. Consent is his, and her face comes from the comic (no photo) |
| Look | 3D animated feature film: stylised characters in a physically real world, same as Kyle's film |
| Format | 9:16, 60 s, rendered at 576×1024; 2160×3840 master plus 1080×1920 and 720×1280 copies |
| Her artworks | **stay flat 2D kid drawings** on paper and canvas inside the 3D world. The finale animals are plush toys, as drawn in panel 5 |
| On-screen text | none; pictures and music only |
| Music | **"Emotional Children Piano"**, Music_For_Videos (Pixabay, 1:55) → `raw/clips/music/emotional_children_piano.mp3`. First 60 s: rises from −23 dB to fullest near 50 s (the exhibition), and its section ends at 60 s. 2 s fade out |
| Overnight | Claude judges. A face shot that keeps failing gets restaged from behind or wide. Allowed to quit the app, run caffeinate and edit scripts. Deliver the film plus this report, commit, push and notify |

Runners-up for the music: "Inspirational Piano Arpeggios" (Music_For_Videos, 1:14, builds then dips), "Leva – Finder Dreams" (lemonmusicstudio, acoustic folk, bright but no build).

## 2. Storyboard (approved)

| # | Keep | From | First frame | Motion | Face |
|---|---|---|---|---|---|
| S1 | 6.5 s | P1 → S2 | sunlit table: her cat-and-cake drawing, cup of pencils, grey tabby asleep | slow push-in, sunlight flickers, tail flicks | — |
| S2 | 8 s | P1 | Lindsey (teal top) coloring the cat drawing, cat beside her | colors, looks up and smiles | ✔ |
| S3 | 7 s | P2 → S4 | looking down at sketches (fish, panda, gecko), her hand in the pink sleeve shading | hand shades, light drifts | — |
| S4 | 8 s | P2 | Lindsey (pink sweater) sketching a gecko | draws, pauses, smiles at the page | ✔ |
| S5 | 10 s | P3 | from behind (lavender hoodie) painting a sea turtle, her drawings on the wall | brush strokes, push-in to the canvas | back |
| S6 | 8 s | P4 → S7 | gallery wide: framed drawings, visitors walking in | visitors drift in | — |
| S7 | 8 s | P4 | Lindsey (navy dress, name tag) arms open, crowd from behind | laughs, arms stay open | ✔ |
| S8 | 9.6 s | P5 | sunrise by the sea, hugging plush cat, panda, gecko and fish | rocks gently, camera rises | ✔ |

65.1 s kept − 7 × 0.75 s crossfades ≈ 60 s. Her outfit changes by panel, which shows time passing; her face and hair are the identity, locked to the master.

## 3. How consistency is held

This is the Kyle method ([[kyle-antarctic-rescue-plan]] §0, [[headless-cli-pipeline]] §1c):

- **Master**: panel 1 face crop → klein edit at strength 1.0 ("re-render as a 3D animated film character, same face, same long dark brown hair with a side part …"). 4 seeds; **seed 3** was picked for its side part and closest face shape. File: `raw/clips/lindsey/masters/lindsey_front.png`.
- **Face shots** S2, S4, S5, S7, S8: diptych with the master on the left and the panel crop on the right.
- **Chained shots**: S1 = edit of the approved S2 ("the girl is gone"); S3 = diptych with S4 (same sleeve, sketches, light); S6 = diptych with S7 (same gallery, same framed drawings).
- **Art stays art**: every still prompt ends with "her drawings stay flat hand-drawn children's crayon and colored-pencil pictures on paper".
- **Motion rules**: face shots "stay in place … face and hair stay exactly the same, hair stays neat"; multi-person shots "camera holds completely still, same framing throughout"; trim before LTX's end-of-clip fade.

## 4. Run

The run-spec is `projects.json → lindsey_art["run-spec"]`. Commands, in order:

```bash
scripts/preflight.sh --fix
scripts/film_run.py lindsey_art stills s2 s4 s5 s7 s8   # then pick
scripts/film_run.py lindsey_art stills s1 s3 s6         # chained from the picks
scripts/film_run.py lindsey_art clips                   # 8 × ~9.5 min
scripts/film_run.py lindsey_art qc                      # judge sets take + trim, queues redos
scripts/film_run.py lindsey_art finish
```

## Related pages
- [[idea-to-video-blueprint]] — the process
- [[kyle-antarctic-rescue-plan]] — the first film, same method
- [[scripts-reference]] — run-spec and `film_run.py`
- [[projects]] — the `lindsey_art` record
