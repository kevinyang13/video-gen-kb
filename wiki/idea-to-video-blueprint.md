# Idea-to-Video Blueprint — Minimal-Touch Production

**Summary**: The end-to-end process for turning an idea (a sentence, a comic, a photo) into a finished short film on this Mac, arranged so that **all human input happens up front** — one intake questionnaire and one storyboard approval — and everything after "go" (masters, stills, clips, QC, retries, upscale, edit, music, report, push) runs unattended through `draw-things-cli`, with Claude as the judge. Proven end to end on [[kyle-antarctic-rescue-plan]] (60 s, 3 h 40 min, zero input after go).

**Sources**: [[kyle-antarctic-rescue-plan]] §0 (the unattended run, 2026-09-22/23 — every timing below is from it unless marked); [[lost-city-plan]] §3c prompt rules; [[headless-cli-pipeline]] §1b–1c; [[character-consistency]]; [[identity-conditioning]]; [[scripts-reference]].

**Last updated**: 2026-09-25 (Phase 4 rewritten as seeding — characters, locations and props — plus Phase 4b on feeding a seed into a shot)

---

## The shape of it

```
 HUMAN (≈15 min, before go)                 MACHINE (hours, no human)
 ┌──────────────────────────┐   ┌──────────────────────────────────────────────────────────────┐
 │ 0 Intake questionnaire   │   │ 4 Seeds → 5 Shot stills → 6 Motion prompts → 7 Clip batch    │
 │ 1 Story + storyboard  ✔  │ → │      ↑ Claude picks each      8 QC + redo queue ←──┘         │
 │ 2 Bible (locks, rules)   │ go│ 9 Trim → upscale → assemble → music → delivery copies        │
 │ 3 Preflight + permissions│   │ 10 Report to plan, spec.json, log → commit/push → notify     │
 └──────────────────────────┘   └──────────────────────────────────────────────────────────────┘
        ✔ = the only approval gate                     optional gate: master pick (step 4)
```

The rule that makes it work: **every decision the machine will face must have a rule written down before go** — which seed wins, what counts as a failed shot, what to do after N failures, what the film does if a shot can't be saved. Anything left open becomes a 2 a.m. stall.

---

## One command per phase

The intake answers become a **run-spec** (the `run-spec` block in `projects/<id>/<version>/spec.json`) (size, still/clip models, frames, upscaler and output size, crossfade, music, deliveries, and per shot: still recipe, prompts, take, trim). Every script reads its settings from there through the driver — nothing is hardcoded to Kyle's 9:16 LTX setup. The plan page keeps the story, decisions, rules and results; the run-spec keeps the exact settings and is the only thing the run reads. Run-spec schema and per-script options: [[scripts-reference]].

| Phase | Command |
|---|---|
| — set up the folder | see **Starting a new project** below |
| 3 Preflight | `scripts/preflight.sh --fix` |
| 2 → run-spec sanity | `scripts/film_run.py P check` |
| 4 Seeds (masters) | `dt_diptych.sh` per character / location / prop → pick → `seed/` |
| 5 Shot stills | `film_run.py P stills` → judge → `film_run.py P pick ID SEED` |
| 7 Clips | `film_run.py P clips` (redo: `clips ID --v 2 --seed 2`) |
| 8 QC | `film_run.py P qc` → judge sets `take` + `trim` in the run-spec |
| 9 Finish | `film_run.py P finish` |
| any time | `film_run.py P status` |

## Starting a new project

A project is one folder; a **version** inside it is one attempt at the film. Name the version for the method — `v1-drawthings-cli`, `v2-master-restage` — so the folder says how it was made. Full rules in [[repo-structure]].

```
projects/<id>/
  plan/<id>-plan.md        the story, decisions and results (this is §0 onward)
  <version>/
    spec.json              SOURCE OF TRUTH: settings, every prompt, shots, takes, trims
    raw/                   the source comic / photos, immutable
    seed/                  masters, crops, candidates, locks, qc_notes.txt
    stills/                sN.png — the picked first frames
    clips/                 sN_vK.mov, sN_t.mov, sN_4k.mp4, sN_trim.txt
    music/                 the track this version is cut to
    final/                 the film and its delivery copies
    logs/                  run logs and any hand-written run scripts
    .gen/                  prompts written out of spec.json at run time — generated
```

Setup, in order:

1. `mkdir -p projects/<id>/plan projects/<id>/v1-<how>/{raw,seed,stills,clips,music,final,logs}`
2. Source material into `<version>/raw/`.
3. Write `<version>/spec.json`: `id`, `version`, `variant`, `title`, `date`, `theme`, `status`, then `still` / `i2v` / `post` blocks and a `run-spec` whose `dir` is `projects/<id>/<version>`. Copy the shape from a delivered film — `bot_builders_champion/v3-photo-cut` for 16:9, `kyle_rescue/v1-drawthings-cli` for 9:16 — and **delete what you are not reusing** rather than leaving stale settings in place.
4. Plan page at `projects/<id>/plan/<id>-plan.md` in the standard page format, and a card for it in `wiki/index.md` under **Projects**.
5. `python3 scripts/build_site.py` — regenerates the root `projects.json` aggregate and the registry pages.
6. `scripts/film_run.py <id> check` — must pass before Phase 3.

Prompts go **in the spec**, not in files: each shot's `still.prompt` and `video_prompt` as text, plus `run-spec.prompts` for recipes no shot owns. `film_run.py` writes them to `.gen/` when it runs.

## Phase 0 — Intake (human, ~5 min)

Ask these once, all together, and record the answers in the plan page's "Decisions" table and in the version's `spec.json`. Defaults in **bold** are what Kyle used.

| # | Question | Options | Why it matters downstream |
|---|---|---|---|
| 1 | Source | idea text · comic/storyboard image · photo(s) · reference video frame | a visual source becomes the layout for every shot (pixels beat text for identity) |
| 2 | Look | 2D illustrated · **3D animated feature film** · photoreal live-action | sets the style lock; photoreal needs a real face photo (Q6) and tighter QC |
| 3 | Aspect / delivery | **9:16 phone (576×1024 → 2160×3840 + 1080×1920)** · 16:9 (1024×576 → 3840×2160) | render size, crops, `W`/`H` for the scripts |
| 4 | Length | 30 s · **60 s** · 3 min | shot count ≈ length ÷ 7.5 s (see Phase 1) |
| 5 | Sound | **music only** · music + model audio (LTX ambience) · narration | narration needs a TTS tool (none installed yet) |
| 6 | Characters | names, who they are, **consent** for real people, real face photo yes/no | a real person needs consent; no photo → face comes from the source drawing |
| 7 | On-screen text | **none** · captions · title/end card | text is always added with ffmpeg, never by the model |
| 8 | Music | pick now, or "find one" (Claude searches Pixabay, ranks by tags + loudness curve, human picks) | music must be chosen before go — the edit is cut to it |
| 9 | Who picks overnight | **Claude judges** (session stays open) · fully scripted (seed 1, fixed trims) | scripted finishes regardless of quality |
| 10 | If a hero shot keeps failing | **restage** (from behind/wide) · keep best attempt · drop and stretch neighbours | the one failure rule that must exist |
| 11 | Permissions | **quit Draw Things app · caffeinate · edit scripts · build tools** | each is otherwise a stop-and-ask |
| 12 | Morning deliverable | **film + wiki report, committed, pushed, notification** · same, no push | |

## Phase 1 — Story and storyboard (Claude drafts, human approves ✔)

1. **Beats.** Reduce the idea to 4–6 story beats (Kyle: arrival → threat → danger → rescue → happy ending).
2. **Shot count.** 249-frame LTX clips are ~10 s; after trimming the end fade and drift, a shot keeps 6–10 s. **Group shots (3+ people) keep only ~5 s** before LTX pulls back and invents people — plan roughly twice as many shots for group-heavy films (Bot Builders: 12 planned shots gave 63 s, not 90). With 0.75 s crossfades: **60 s ≈ 8 shots, 30 s ≈ 4–5, 3 min ≈ 24**. Sum of kept lengths − (shots−1)×0.75 = film length.
3. **One line per shot**: what's in the still, what moves, how long it's kept, and whether it is a **face shot**. Keep face shots to ~⅓ of the film; the rest are from behind, wide, or without the character — identity is free there.
4. **Stage for the model, not just the story** (rules from [[lost-city-plan]] §3c and Kyle §0):
   - close-ups **hold position** — the character smiles, blinks, rocks; doesn't walk or turn away;
   - **slow foreground, busy background** — violence goes to the sky, beams, ice, never onto the hero;
   - fast action (flight, gallop, jump) is clean for ~4–6 s only — plan it short;
   - **camera mostly still** — a moving camera makes LTX invent picture at the edges, where extra characters appear and existing ones vanish.
5. **Approval gate ✔** — show the shot table (and, if the source is a comic, which panel feeds which shot). This is the last question to the human.

## Phase 2 — Bible: locks and rules (Claude)

- **One lock per entity** (character, creature, vehicle, place), 1–2 sentences, pasted verbatim into every prompt that shows it. Name the count: "one boy".
- **Style lock** (head of every still prompt) and **video tail** (end of every LTX prompt).
- **Word bans** collected so far: "UFO"/"alien" (invites aliens → write "flying saucer, no aliens visible"), "dragon" for a wingless mount (grows wings), "lightning" for a sky rift (renders a bolt), "wind in his hair" on a face shot (hair restyles over 10 s), negations with klein at CFG 1 (it obeys the noun). Add to this list after every project.
- Store everything in the version's `spec.json`: `scenes.locks` for the locks, each shot's `still.prompt` and `video_prompt` for the wording; the registry pages render it.

## Phase 3 — Preflight (Claude, 2 min, just before go)

| Check | Command / action |
|---|---|
| On AC power, disk > 50 GB free | `pmset -g batt`, `df -h /` |
| Draw Things app closed (holds GPU memory, halves CLI speed) | `osascript -e 'tell application "Draw Things" to quit'` |
| Mac won't sleep | `caffeinate -dis -t 50400 &` (kill it when done) |
| Models present | klein `flux_2_klein_9b_i8x.ckpt`, LTX `ltx_2.3_22b_distilled_1.1_q8p.ckpt` in the app's `Models/` |
| All of the above in one go | `scripts/preflight.sh --fix` (quits the app, starts caffeinate, checks models/disk/power) |
| Session stays open | the desktop app and this session must keep running; the screen may lock (the CLI needs no screen) |

## Phase 4 — Seeds: a master for everything that must stay the same

A diffusion model keeps no memory between generations ([[identity-conditioning]]). Anything that has to look the same in shot 9 as in shot 2 must be **seeded**: rendered once as a canonical image, then fed into every shot that contains it. Seeds live in `<version>/seed/` and are listed in the spec's `run-spec.masters`.

**Seed everything recurring, not just people.** On Bot Builders that meant five children *and* the LEGO mission table, the competition gym, and three Coastal Roots Farm plates. Lost City seeded the creature, the rider and the city. A location you skip is a location the model re-invents every shot — a different gym each time reads as a different tournament.

| What | Source | Recipe |
|---|---|---|
| **Character** | photo or drawing, face large in frame | crop head-and-shoulders, klein edit at `--strength 1.0`, plain grey background, neutral wardrobe, 3 seeds |
| **Location** | a photo of the real place | klein edit 1.0 of a 16:9 crop, **"no people anywhere, no text, no lettering"**, 2 seeds |
| **Hero prop** | photo, or a crop from an approved shot | same as a location; name the parts that matter (the mat's river, the tree tower, the robot) |
| **From text only** | nothing to photograph | klein text-to-image with the lock + "character portrait, plain background" |

**The recipe that preserves a real person** (learned across three failed attempts, [[bot-builders-champion-photo-cut-plan]] §2):

- Say **"stylise the rendering, not the identity"** — never "convert this into a 3D character", which makes klein substitute its own default face.
- **Name what to keep**: ethnicity and skin tone, hair colour, texture, length, cut and hairline, eye colour, eye and eyelid shape, eyebrows, nose, mouth, jawline, age.
- **Ban the drifts**: do not westernise, do not enlarge or round the eyes, do not lighten hair or eyes, do not make the subject look older, do not idealise.
- **Force dark hair** — klein warms black toward brown on every pass: "pure black hair, not brown, not chestnut, no warm highlights".
- **Neutralise the source lighting**, or a sunset photo bakes orange into hair and skin.
- **Name signature features** (a spiked fringe, a horn crest) or they get combed flat — then take the mildest seed, because naming them also invites overshoot.
- `--strength` 0.7–0.9 is a near no-op on the released CLI; only 1.0 is edit mode ([[headless-cli-pipeline]] §1c).

**Pick rule**: closest to the source on face shape, hair silhouette and signature details — judged at full size, not from a thumbnail strip. Optional human gate here when the subject is a real person.

### The seed is a sheet, not a portrait

A single frontal image gives the model nothing to copy when a shot needs a profile, so it invents one, and the character changes the moment they turn their head. Once a master is picked, expand it into a **turnaround sheet** — front, three-quarter, profile, back — by editing the master itself:

```bash
scripts/seed_sheet.sh seed/kyle.png seed/kyle boy 1
#   -> seed/kyle_34.png  seed/kyle_side.png  seed/kyle_back.png  seed/kyle_sheet.png
```

Each view is a klein edit at strength 1.0 that says *"the same character, exactly the same face, hair, colours and clothing … turn to a three-quarter view / full side profile / seen from directly behind"*, keeping the same lighting and grey background so the views read as one sheet. ~25 s per view.

For a creature, vehicle or location, add the views that matter with free text — `VIEWS` accepts a prompt sentence as well as the three built-ins:

```bash
VIEWS="34 side back" SUBJECT=creature scripts/seed_sheet.sh seed/mount.png seed/mount creature
VIEWS="seen from directly above, wings folded|a close-up of the head in profile|a close-up of one clawed foot" \
  scripts/seed_sheet.sh seed/mount.png seed/mount_detail creature
```

That is what a professional model sheet carries: the four orbit views plus detail insets (eye, mouth, foot, tack) and a few gait thumbnails. Render the insets the same way — each is just another edit of the master.

**Then use the right panel.** A shot that shows the character from behind should be seeded with `seed/kyle_back.png`, not the front portrait — hand the angle the shot needs as the reference and the model copies instead of inventing. The whole sheet is also useful as a single reference when the shot shows the character at an unusual angle.

Costs about 75 s per character on top of the master. On a film with a recurring cast it pays for itself the first time someone turns around.

## Phase 4b — Feeding a seed into a shot

Three mechanisms, and choosing wrong is the most common way a shot fails:

| Mechanism | Use when | Command |
|---|---|---|
| **Diptych** — seed left, layout right, edit the pair, keep the right half | the layout image **already contains a person or object to replace** | `dt_diptych.sh SEED LAYOUT prompt out.png` |
| **Restaging** — the seed *is* the input, the scene comes from the prompt | there is no layout image, or the layout is an empty place | `dt_diptych.sh - SEED prompt out.png` |
| **Chaining** — an approved shot becomes the reference for the next | props, places and light carrying between shots | `dt_diptych.sh stills/s3.png LAYOUT prompt out.png` |

**A diptych needs a subject in the layout image.** Pointed at an empty venue plate, klein renders the room and silently leaves the character out — two Bot Builders shots came back with nobody in them. Restaging from the seed portrait fixed all four on the first pass.

Prompt pattern for a diptych: *"Two images side by side. Left: … Right: … Re-render the right image as a frame from the same film, with the boy looking exactly like the boy on the left: same face, same hair, same costume. [framing]. [scene]. [style]. Keep the left image unchanged."*

Prompt pattern for restaging: *"Keep this exact character — same face, same hair, same age, same style — and place them in a new scene. [framing]. [scene]. Exactly one child in the frame."*

**Always state the framing** ("medium close-up: head and shoulders fill the frame") — without it klein zooms out to full body. And an edit **inherits the source pose**: chaining a calm portrait off a celebration still reproduced the jump across three seeds until the new pose was named both positively and negatively.

In the Draw Things app the equivalent channel is the **Moodboard** (up to 3 crops, equal weight); on the CLI the diptych is its substitute, since the released binary takes a single `--image`.

## Phase 5 — Shot stills (first frames)

Every shot's first frame must carry identity from **pixels**, never text alone — pick the mechanism from Phase 4b, then:

- Render **3 seeds per shot** (`film_run.py P stills`), judge **at full size** — never from a thumbnail strip — and `pick` the winner into `stills/`.
- **Count the subjects in every group frame.** klein drops people from crowded shots: only 1 of 3 seeds of the Bot Builders celebration kept all five children, and comic panels with six figures get copied six-figured regardless of the prompt.
- Typical rejects: subject dropped, an extra hand or doubled gesture, a different face, text left in, the wrong pose inherited from the input.
- Inputs are fitted to W×H by centre-crop, so hand over images already at the target aspect; pad near-square panels with a blurred copy of themselves.
- **Wardrobe**: say "plain black t-shirt with no printing, no graphics and no letters" or shirts come back with garbled lettering. "No text anywhere" must name clothing, boards and signs explicitly.

## Writing it down as you go

Two files, one rule: **if changing it changes the render it goes in `spec.json`; if it explains why, it goes in the plan** ([[repo-structure]] has the full table). Settings, prompts, shots, takes and trims are spec; the story, the rejected attempts and the rules they taught are plan. Fix the spec the moment a shot is rescued by a different method, or a re-run will reproduce the failure rather than the film.

## Phase 5b — One generation per film

Everything a film is cut from must come from the same generation: the same style head, the same masters, the same prompt wording. If any of those change mid-project — a different look, a rebuilt master, a corrected recipe — **every still is stale**, including the ones whose clips already rendered fine. Re-render them all.

This is easy to get wrong, because a stale still is not broken: it matches its own clip, and QC passes. The damage only appears in the cut, where the same character is drawn two ways (BOT Builders photo cut, 2026-09-25 — seven shots from the pre-master pipeline cut against four from the rebuilt masters). A still costs about a minute to re-render; a film with two faces for one child costs the film.

Practical guard: stamp each shot with the generation that produced its still, bump the stamp whenever the style head or a master changes, and refuse to assemble while stamps differ.

## Phase 6 — Motion prompts

One paragraph per shot, action first, ending with the video tail. Rules from Kyle and Lost City:
- describe **motion only** — the still already has the look;
- **hold wording** on face shots: "keeps holding his thumbs up the whole time", "his face and hair stay exactly the same", "hair stays neat";
- multi-subject shots: "all stay in place in the foreground … the camera holds completely still, same framing throughout";
- name the subject and its stillness **before** any destruction verb (motion bleeds onto small subjects);
- music-only films: skip sound sentences.

## Phase 7 — Clip batch (unattended)

`film_run.py P clips` runs this loop from the run-spec (one clip at a time, skipping clips that exist). What it does per shot, equivalent to Kyle's hand-written `logs/render_clips.sh`:

```bash
for s in $SHOTS; do
  out=clips/${s}_ltx_v$V.mov; [ -f "$out" ] && continue
  draw-things-cli generate -m ltx_2.3_22b_distilled_1.1_q8p.ckpt \
    --prompt-file .gen/${s}_v.txt --image stills/$s.png \
    --width 576 --height 1024 --frames 249 --steps 8 --cfg 1 --seed $SEED \
    --config-json '{"sampler":19,"shift":5.0,"stochasticSamplingGamma":0.3,"fps":25,"hiresFix":false}' \
    --offline --disable-preview --video-format prores422hq -o "$out"
  echo "$s $? $(date +%H:%M)" >> render.log
done
```

- Order the batch **hero shots first**, so their QC (and any redo) happens while the rest render.
- Watch `render.log` (one event per clip) and QC each clip as it lands.
- Never run Real-ESRGAN while LTX renders (memory).
- Always 249 frames: same cost as short clips; trim later.

## Phase 8 — QC and the redo queue (Claude as judge)

**Contact sheet per clip**: reference (master or still) + frames 0, 62, 124, 186, 248. `qc_sheet.sh` also prints where an end-of-clip fade starts. **Judge stills and sheets at full size** (open the candidate PNGs, not a 200-px strip): hand counts and intersections are invisible in thumbnails.

```bash
ffmpeg -i master.png -i clip.mov -filter_complex \
 "[0]scale=216:384[m];[1]select='eq(n\,0)+eq(n\,62)+eq(n\,124)+eq(n\,186)+eq(n\,248)',scale=216:384,tile=5x1[t];[m][t]hstack=2" \
 -frames:v 1 qc.png
```

**Reject / trim when**: face differs from the master (eyes, hair silhouette, smile) · costume loses a signature detail · count changes (extra or missing character, second prop) · animal changes species or markings · style slides (2D ↔ 3D ↔ photo) · a held gesture drops · camera pulls back and invents or loses subjects · **end-of-clip fade to dark** (4 of 10 Kyle clips — trim ~2–3 s before it).

**Decision ladder per shot**:
1. clean for ≥ the planned keep length → **pass**, note the trim;
2. clean for less → keep as fallback trim, **queue v2**: fix the prompt cause (drop the wind, add hold/still wording), new seed;
3. v2 fails → new still seed → v3;
4. still failing → apply the intake failure rule (restage / best attempt / drop).

Log every verdict to `<version>/seed/qc_notes.txt`; it becomes the report.

## Phase 9 — Finish (unattended)

`film_run.py P finish` does this from each shot's `take` + `trim` and the run-spec's upscale / assemble / music / deliver blocks, caching each shot's upscale so a changed trim only redoes that shot. The underlying commands (Kyle's hand-written `logs/finish.sh` did the same):

```bash
ffmpeg -nostdin -i clips/$c.mov -vf "trim=start=$a:end=$b,setpts=PTS-STARTPTS" -an -c:v prores_ks -profile:v 3 final/${s}_t.mov
W=2160 H=3840 scripts/upscale_4k.sh final/${s}_t.mov final/$s realesrgan-x4plus </dev/null
W=2160 H=3840 XFADE=0.75 scripts/assemble_film.sh final/film_nomusic.mp4 final/s*_4k.mp4
# music = the track's tail, so the film ends on the song's own ending
ffmpeg -ss $(python3 -c "print(max(0,TRACK_LEN-$D))") -i music.mp3 -t $D -af afade=t=in:d=1.5 bed.wav
ffmpeg -i film_nomusic.mp4 -i bed.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out_master.mp4
ffmpeg -i out_master.mp4 -vf scale=1080:1920 -c:v hevc_videotoolbox -b:v 12M -tag:v hvc1 -c:a copy out_1080.mp4
```

- **`-nostdin`** on every ffmpeg inside a `while read` loop (ffmpeg eats the loop's input — cost one restart on Kyle).
- `x4plus` for 3D/photo textures, `realesr-animevideov3-x4` for flat 2D line art.
- Music-only: assemble **without** `MUSIC` and mux the bed afterwards (`MUSIC` goes through `amix`, which halves it).
- For phones over a 30 MB share limit, also make a ~23 MB 720p preview.

## Phase 10 — Report and file back

- Project page §0 **Results**: deliverables, what differed from the plan, every pick and rejection with reasons, QC sheets, timings, new rules.
- the version's `spec.json`: status, seeds, trims, files — and fix any shot whose staging changed mid-run, or a re-run reproduces the failure. `wiki/log.md` entry. New gotchas onto the recipe pages ([[headless-cli-pipeline]], [[scripts-reference]], [[lost-city-plan]] rules).
- `python3 scripts/build_site.py`, commit, push (if the intake said so), notification, send the film (or preview) to the human.

---

## Pick rubric (stills and masters)

Score each candidate against the reference, reject on any hard fail:

| Check | Hard fail |
|---|---|
| Identity | different face shape, eyes, hair silhouette |
| Costume | signature colour split, patch, prop missing |
| Count | extra / missing character, doubled hand or gesture — **count hands per person** (two hands on one pencil passed thumbnail QC on Lindsey S3) |
| Physics | people or objects intersecting: a body passing through a sign, frame, wall or another person (Lindsey S6: the comic's chalkboard became dark boards the crowd walked through). Any standing prop in a crowd shot is a risk — prompt it out |
| Framing | not what the prompt named (zoomed out, subject cropped) |
| Cleanliness | leftover text, bubbles, borders, smears |
| Style | slides away from the style lock |

Among passes, prefer: closest to the master → most readable at phone size → most room for the planned motion.

## Time budget (M4 Max 48 GB, measured on Kyle, 576×1024)

| Stage | Unit | Time |
|---|---|---|
| klein edit / text still | per image | ~30 s |
| klein diptych | per image | 55–60 s |
| Masters + 8 shots × 3 seeds | per film | ~35 min |
| LTX-2.3, 249 f | per clip | 9 min 20–30 s |
| Redo rate | | 2 of 8 shots needed v2 |
| Real-ESRGAN x4plus → 2160×3840 | per clip (6–10 s) | 7–11 min (~20 f/min) |
| Assembly + music + delivery | per film | ~2 min |
| **60 s film, go → pushed** | | **~3 h 40 min** |

Rule of thumb: **wall clock ≈ 0.6 h + 0.35 h per shot** (stills + LTX + 25% redos + upscale).

## Failure playbook

| Symptom | Cause | Fix |
|---|---|---|
| restyled still looks like the input | `--strength` < 1 with klein | strength 1.0 + instruction prompt |
| still zoomed out to full body | edit prompt didn't name framing / said "fill the frame" | name the framing explicitly |
| character missing from a busy still | too many subjects | another seed; put the character first in the prompt |
| hair / face restyles mid-clip | wind, turn, walk in a face shot | hold wording; "hair stays neat" |
| second hand appears in a hand close-up | LTX invents the other hand | restage without hands (pencil lying on the page) or keep the hand small in frame |
| a pet / small animal changes breed or doubles | partly hidden subject is re-invented | "exactly one cat: the same grey tabby stays … in the same place"; show it larger |
| people pass through a sign, frame or each other | standing props in a crowd still | prompt the props out; "each person solid and clearly separate, walks only on the floor" |
| an extra person appears at the frame edge mid-clip | tight group frame + LTX pull-back invents people in the new margin (Bot Builders S5: a 6th kid) | "the camera does not move at all: no zoom, no pull-back, no pan" + "no one enters from any edge"; check the last frames for head count |
| subject sinks out of frame | "camera rises" executed as subject motion (horizon stays put) | "camera holds completely still", or an eye-level pull-back |
| gesture drops mid-clip | not asked to persist | "keeps holding … the whole time" |
| animals vanish / morph, camera pulls back | no framing lock | "camera holds completely still, same framing throughout" |
| last 2–3 s go dark | LTX end fade | trim before it (or keep it as the film's ending) |
| subject destroyed with the scenery | motion bleed | subject large, still, named before the destruction |
| only the first shot processed in a loop | ffmpeg reading stdin | `-nostdin` / separate fd |
| portrait clip cropped to landscape | scripts at default size | `W=2160 H=3840` |
| LTX slow (~20 min instead of ~10) | Draw Things app open | quit the app |

## Not automated yet

- The judge steps (`pick`, setting `take`/`trim`) are decisions, not code — Claude reads the candidate and QC sheets; `film_run.py` stops cleanly at each of them.
- Programmatic identity scoring (face embeddings) — the judge is Claude reading contact sheets.
- Narration/TTS and captions.
- Chaining clips longer than 10 s (last frame → next first frame) — planned in [[character-consistency]] §6, not needed yet.

## Related pages
- [[kyle-antarctic-rescue-plan]] — the run this blueprint is distilled from
- [[headless-cli-pipeline]] — the CLI, strength-1.0 edit mode, the diptych
- [[lost-city-plan]] — LTX prompt and staging rules
- [[character-consistency]] · [[identity-conditioning]] — why pixels carry identity
- [[scripts-reference]] — `upscale_4k.sh`, `assemble_film.sh`, `dt_diptych.sh`
- [[projects]] — where every project's record lives
