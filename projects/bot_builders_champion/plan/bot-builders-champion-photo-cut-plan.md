# BOT Builders (photo cut) — 1-Minute Film from the Team's Own Photos

**Summary**: A 59-second 16:9 short about an FIRST LEGO League season — build, research at Coastal Roots Farm, the lacewing project, the competition, the win — made from the team's real photographs rather than a comic. Eleven shots, 3D-animated look, rendered entirely with `draw-things-cli`. Version 3 of the [[bot-builders-champion-comic-cut-plan|Bot Builders]] project: same five children as the comic cut, different source material and a different route to identity.

**Sources**: 13 photographs from Kevin (team coach) in `projects/bot_builders_champion/v3-photo-cut/raw/`, added 2026-09-23/24; [[idea-to-video-blueprint]] (the process); [[headless-cli-pipeline]] (CLI settings); [[lost-city-plan]] §3c (LTX motion rules); [[scripts-reference]] (run-spec, `film_run.py`).

**Last updated**: 2026-09-25 (delivered; §3b records the mixed-generation mistake)

---

## 0. Result

**Delivered** 2026-09-25 03:00: `projects/bot_builders_champion/v3-photo-cut/final/fll_champions_3840x2160.mp4` (59.08 s, 274 MB) and `fll_champions_1920x1080.mp4` (89 MB). Music "Light Adventure" (331music, Pixabay) under the LTX ambience; mean −18.8 dB, peak −5.5 dB.

**The cut** (11 shots, 0.75 s crossfades):

| # | Shot | Built from | Kept |
|---|---|---|---|
| 1 | Garage build night, five kids around the mission table | edit of the garage photo | 5.5 s |
| 2 | Cheryl and Lola building together | Cheryl's master, restaged | 7.0 s |
| 3 | Macro: the robot alone on the jungle mat | chained from shot 1 | 6.0 s |
| 4 | The team holding their emblem poster | edit of the living-room photo | 6.0 s |
| 5 | Walking in through the farm gate, backs to camera | edit of the farm photo | 6.0 s |
| 6 | On the logs with the farmer, taking notes | edit of the farm photo | 5.5 s |
| 7 | Lindsey presenting the lacewing board | Lindsey's master, restaged | 5.0 s |
| 8 | Kyle launching the robot at the competition table | Kyle's master, restaged | 7.0 s |
| 9 | Kei timing the run, stopwatch up | Kei's master, restaged | 6.0 s |
| 10 | The win — arms up, trophy, confetti | chained from shot 4 | 5.5 s |
| 11 | Closing portrait, medals in late light | chained from shot 10 | 7.0 s |

**Dropped**: the competition-floor wide. LTX invented a walking humanoid robot and marched a crowd into an empty gym (v2); a third pass fixed the crowd but left a stray toy robot wandering the court (v3). Applied the agreed failure rule — drop it, stretch the neighbours — since shots 8 and 9 already cover the competition.

## 1. What this project was for

The comic-derived film had already shipped. This one asks a different question: **can a film be built from a family's actual photographs**, where identity has to come from real faces rather than drawn panels? The answer is yes, but the master stage is where the work is.

## 2. Masters — the part that took the longest

Ten masters: five children, the mission table, three Coastal Roots Farm plates, the competition gym. Everything else in the film was chained off them or off an approved still.

**Three failed attempts before the recipe worked**:

1. **"Convert this photo into a 3D animated character"** → klein substituted its own default face. Recognisable as children, not as *these* children.
2. **Photoreal** (Kevin's call after seeing attempt 1) → sharper, but the drift became obvious rather than hidden: faces came back westernised, eyes rounder and larger, hair lightened, children aged up. Photoreal exposes a likeness gap that stylisation forgives.
3. **Pixar again, with the identity clauses kept** → worked.

**The recipe** (now in `projects.json` → `scenes.locks.rules`):

- **Name what to keep**: ethnicity and skin tone, hair colour, texture, length, cut and hairline, eye colour, eye shape, eyelid shape and spacing, eyebrows, nose, mouth, ears, jawline, age.
- **Ban the drifts explicitly**: do not westernise, do not enlarge or round the eyes, do not lighten hair or eyes, do not make the child look older, do not idealise or beautify.
- **Frame it as "stylise the rendering, not the identity"**, never "convert into a character".
- **Force dark hair**: klein warms black hair toward brown on *every* pass. "Pure black hair — not brown, not chestnut, no warm highlights."
- **Neutralise the source photo's light**: a sunset backlight baked orange into the hair and skin until the prompt said to remove it.
- **Name a signature feature or lose it**: Kyle's spiked fringe was combed flat until described, then over-spiked into anime; the mildest of three seeds was the keeper.

**Source photos matter as much as prompts.** The first masters came from crops of group photos and were the weakest. Solo shots — Kyle on a ship deck, Lindsey indoors, the two girls in the kitchen — produced masters good enough to carry the film.

## 3. Restaging beats a diptych when the layout is empty

Four character beats were first attempted as diptychs (master left, venue plate right). Two came back **with no child in them at all** and one with three girls instead of two: with no person in the layout image, klein renders the room and ignores the instruction to add someone.

What worked: **master as the input image, scene from the prompt** — "Keep this exact character … and place them in a new scene. Medium close-up … he stands at the edge of a robotics competition table …". Identity comes from the portrait's pixels, staging from text. All four beats landed on the first pass after the switch.

Two smaller rules from the same stage:
- Team shirts rendered with garbled lettering until the prompt said **"plain black t-shirt with no printing, no graphics and no letters"**.
- "No text anywhere" has to name clothing, boards and signs explicitly, or it applies only to the background.

## 3b. The mistake: two generations of stills in one cut

**The film mixes stills from two different pipelines, and it shows.** Shots 1, 3, 4, 5, 6, 10 and 11 were rendered on 2026-09-23 — old style head, no masters yet, identity coming straight from a klein edit of the source photograph. Shots 2, 7, 8 and 9 were rendered on 2026-09-25 from the rebuilt Pixar masters after three rounds of recipe changes. Their clips were still valid in the narrow sense (each still matched its own clip), so they were carried forward instead of re-rendered.

The result is a cut where the same five children are drawn by two different recipes: the older shots have the softer, more generic faces that drove the master rework in the first place, the newer ones have the corrected ones. Face shape, hair colour and the degree of stylisation all shift across cuts.

**Rule**: *when the look or the master recipe changes, every still is stale — re-render all of them, not just the new shots.* A still is only reusable if it was made with the same style head, the same masters and the same prompt generation as everything it will be cut against. The cost of re-rendering a still is about a minute; the cost of a mismatched film is the film.

**How to avoid it next time**: stamp each still with the generation that produced it (a `gen` field per shot in the run-spec, bumped whenever the style head or a master changes), and have `film_run.py check` refuse to finish while shots carry different stamps.

## 4. Settings

Unchanged from [[headless-cli-pipeline]]: klein 9B at 4 steps / CFG 1 / shift 3 / DDIM Trailing for stills (512×768 masters, 1024×576 shots, `--strength 1.0` edit mode); LTX-2.3 distilled at 8 steps / CFG 1 / TCD Trailing / SSS 0.3 / shift 5, 249 frames at 1024×576, ~9.5 min per clip; Real-ESRGAN x4plus to 3840×2160; `assemble_film.sh` at 0.75 s crossfades.

Timings: masters ~25 s each, shot stills ~55 s each, clips ~9.5 min each, upscales ~6.5 min each, whole finish pass 1 h 15 m.

## 5. Consent

Kevin is the team's coach and confirmed consent for all five children on 2026-09-23. The film shows no text, no team name and no school. Background people in the competition shots are distant, out of focus and have no recognisable faces.

## Related pages
- [[idea-to-video-blueprint]] — the process this follows
- [[headless-cli-pipeline]] — the CLI that rendered it
- [[projects]] · [[projects-3d]] — the registry and the comic-derived companion film
- [[character-consistency]] · [[identity-conditioning]] — why masters work
