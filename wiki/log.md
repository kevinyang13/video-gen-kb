# Log

**Summary**: Append-only record of every operation performed on this wiki.

**Sources**: n/a

**Last updated**: 2026-09-22

---

## 2026-09-26 — Orchestration options added to the v2 research

Second pasted source (`raw/2026-09-26-ai-film-orchestration-options.md`): Claude-Code-driven skills over ComfyUI/Kohya, and three open-source orchestrators. Verified all three repos exist before recording them — `OpenX-Inc/flow` and `juspay/director` are real and single-source; **OpenMontage appears under a dozen near-identical forks**, so its provenance is unclear and the page says so.

The honest framing added to [[blueprint-v2-research]]: **we already are that orchestrator** — `film_run.py` plus `spec.json` is the shots-manifest-then-render pattern the source recommends building. What the projects have that we lack is narrower and more interesting: Director's **critic that rejects a keyframe before animating it** (we judge by eye; it would have caught the empty-room Bot Builders shots and the child-in-adult-armour night-elf stills for free), and OpenX Flow's **serverless bursting**, which is the actual lever that makes LoRA training and control models possible on a Mac — and which breaks the local-and-free premise, so it is a decision rather than a detail. Also noted that `musubi-tuner` and `kohya_ss` are CUDA-centric, so local training is gated on an unverified question.

Three experiments added: B8 (does a LoRA train on MPS at all), B9 (cost per film of bursting), B10 (automate the judge).

## 2026-09-26 — Blueprint v2 research page

Kevin's framing for the pasted pipeline: it is **research for a new blueprint with a different strategy**, not a benchmark for the current one. Added [[blueprint-v2-research]] and left every existing page alone.

The page proposes four substitutions, each independently testable: identity from a **trained LoRA** instead of reference-image tokens, motion from **pose/depth control** instead of prose, **TTS and lip-sync** for dialogue, and an **NLE cut with a LUT grade** instead of scripted crossfades. Seven experiments (B1–B7) with pass criteria, ordered so the cheapest kill comes first.

Two findings worth keeping from writing it: the **seeding phase is strategy-independent** — a turnaround sheet is both a good reference set and a good LoRA training set, so step 2 survives either way and the dataset problem that usually blocks LoRA work is already half-solved. And **B7 (one LUT across an assembly) is worth doing regardless** — an afternoon, no new models, and it would fix the colour drift between the two city shots in [[nightelf-hunter-plan]].

The bar for switching is stated on the page: a LoRA must visibly beat a sheet on angles the sheet does not cover, pose control or dialogue must actually work, and any cloud dependency has to be recorded as the change of character it is.

## 2026-09-26 — Ingested a standard AI film pipeline, compared against ours

**Source**: `raw/2026-09-26-ai-film-production-pipeline.md` — an eight-step industry-practice pipeline Kevin pasted; origin unattributed, so treated as general practice rather than a verified source.

**Created**: [[ai-film-production-pipeline]] — the eight steps recorded in full beside what we actually do, because three of them do not apply here and the reasons are worth keeping next to the advice. No LoRA (training is impractical on Apple Silicon; klein takes reference images directly, which is [[identity-conditioning]] channel 2 rather than channel 4 — 25 seconds per seed against hours, at the cost of only copying angles the reference shows, which is why seeds are turnaround sheets). No ComfyUI (Metal has no FP8; 82 min for a 2 s Wan clip in a field test against ~10 min for a 10 s LTX clip here). No ControlNet (nothing klein-compatible exists). No Topaz (Real-ESRGAN is free, local and fast enough).

**What the source has that we lack**, stated plainly on the page: dialogue and lip-sync, a unified colour grade, and a real NLE. The grade is the cheapest to adopt and would fix the colour drift between plates visible in [[nightelf-hunter-plan]].

**Updated**: `wiki/index.md`.

## 2026-09-26 — Night Elf Hunter delivered (57.6 s, photoreal, seeded cast)

New project, rendered unattended overnight: a half-elf hunter with Kyle's face and a brown bear walking the grassland toward a distant city. Eight shots, `final/nightelf_hunter_3840x2160.mp4` (57.64 s) plus a 1920×1080 copy, music "Adventure Journey" picked for its rising arc (−18.5 dB climbing to −10 across the first minute, matching grassland → city revealed → crest). Nothing dropped; every trim is a drift point, not taste.

**First project built the new way** — [[idea-to-video-blueprint]] Phase 4/4b in anger. Four seeds before any shot: a hunter turnaround sheet from one photo, a bear, a grassland plate and a city plate. s6 is seeded from the sheet's **back** panel rather than the front portrait, which is the whole reason a sheet exists.

**The mistake worth keeping**: the first still batch returned a ten-year-old boy in adult armour in seven of eight shots. The master had been aged up on request, but the character lock embedded in every shot prompt still said *"a young half-elf hunter boy of about ten"* — and klein follows the text. **Changing a master does not propagate**: the lock, every prompt embedding it, and the run-spec must all change together. Same family as the Bot Builders mixed-generation failure — a stale ingredient that passes every per-shot check because nothing compares a shot against its own seed. 24 candidates and 25 minutes wasted.

Also fixed in the tooling: `seed_sheet.sh` produced a **Janus profile** (frontal face kept, profile added beside it, ear between), so its side prompt now demands one visible eye and forbids a second face. And two zsh traps cost a restart: `set -- $var` and `for x in $list` do not word-split in zsh, so a pick loop silently failed eight times while the clip batch started against zero picked stills — pick loops now run under `bash -c`.

Report: [[nightelf-hunter-plan]].

## 2026-09-25 — Seeds become turnaround sheets

Kevin showed what a seed should look like: a proper model sheet — front, three-quarter, profile, back, plus detail insets (eye, mouth, clawed foot, saddle) and gait thumbnails — not the single frontal portrait we had been making. He is right, and [[identity-conditioning]] already said why: reference tokens copy what they can *see*, so a frontal-only seed leaves the model inventing the side and back of a head, and the character changes the moment they turn.

Tested whether klein can orbit a master before writing any of it down: editing `seed/kyle.png` at strength 1.0 with "the same boy … turn to a three-quarter view / full side profile / seen from directly behind" held the face, hair, lighting and background across all four views. Same on Lindsey.

**New `scripts/seed_sheet.sh`** — master in, `_34 / _side / _back` plus a composed `_sheet.png` out, ~25 s per view. `VIEWS` takes the three built-ins or any free-text instruction separated by `|`, which is how a creature gets a top-down, a head close-up or a foot inset. `SUBJECT` sets the noun, `STYLE` the look clause for non-3D projects.

Blueprint Phase 4 now ends with **"the seed is a sheet, not a portrait"** and says to hand a shot the *panel that matches its angle* rather than the front view. Documented in [[scripts-reference]] with the one gotcha found: klein amplifies a signature feature slightly with each edit (Kyle's spiked fringe grows), so judge each view against the master, not against the previous view.

## 2026-09-25 — Blueprint: seeding as its own phase

Phase 4 was "Masters (model sheets)" and covered recurring characters plus the odd hero prop. It now covers **everything that must stay the same** — characters, locations and props alike — under the name it deserves: a diffusion model keeps no memory, so anything recurring has to be rendered once and fed back in. Bot Builders needed five children *and* the mission table, the gym and three farm plates; a location you skip is one the model re-invents every shot.

The phase carries the full identity recipe (name what to keep, ban the drifts, force pure black hair, neutralise the source lighting, name signature features and then take the mildest seed) and a table of what to seed from what.

New **Phase 4b — Feeding a seed into a shot** names the three mechanisms and when each applies: diptych when the layout already contains a subject, restaging when it does not, chaining when a prop or place carries between shots. With the rule that broke two shots: a diptych pointed at an empty room renders the room and leaves the character out. Phase 5 was trimmed to what is actually about stills — three seeds, judge at full size, count the subjects in group frames, plain wardrobe.

## 2026-09-25 — Lost City: shots renumbered, rift coda cut

**Renumbered** to the order the film plays: old s10 (drinking) → s3, s3 (feet on flagstones) → s4, s7 (canyon) → s5, s9 (jumping) → s6, s13 (escape run) → s7, s14 (final collapse) → s9; s1, s2 and s8 unchanged. 26 files renamed, both specs and the plan rewritten, mapping recorded in each.

Two traps in doing it, both worth remembering for the next renumber: **chained renames double-apply** if you substitute rule by rule — s10→s3 then s3→s4 turns the drinking shot into s4 — and wrapping the replacement in placeholders does not help, because `@@s3@@` still matches the next rule. The fix is one regex pass with a lookup function so each id is visited exactly once. Files need the same care: rename through temporary names or s3→s4 clobbers the real s4. I got this wrong twice and restored from git rather than patching over it.

**Cut the s15 rift coda** — the crack in the sky, the flock pouring out, the circling over the dead city. Three clips and the assembled 30 s 4K film, deleted at Kevin's instruction (596 MB, roughly 50 minutes of GPU). It was a fine sequence but a different film from the one the plan tells: the rider's story ends with the escape, not with a monster arrival. The prompts and the rules it taught — never write "lightning" for a sky rift; a diptych needs a person in the layout image — stay in the plan and here.

Lost City now stands at nine shots, seven finished at 4K, **s7 (the escape run) the only one unrendered**, and no film assembled yet.

## 2026-09-25 — Script audit against the new structure

Audited all 13 scripts. The nine shell scripts take every path as an argument and needed no changes. The two Python drivers encoded the old layout:

- **A real bug in `film_run.py`**: `stills` wrote seed candidates to `work/<id>_c<seed>.png` and `qc` wrote sheets to `work/`, but `work/` was folded into `seed/` during the reorganisation — and because the new `.gitignore` lists the folders by name, a recreated `work/` was **not ignored**, so the next run would have committed a few hundred MB of candidate PNGs. Confirmed with `git check-ignore` before fixing. Candidates and QC sheets now go to `seed/`; `projects/*/*/work/**` is ignored as a safety net.
- `resolve_ref` still accepted `masters/` and `work/` prefixes for a shot's `ref`; now `seed/` and `stills/`.
- Docstrings in both drivers described `raw/clips/<project>`, `masters/`, prompt files and "projects.json is the source of truth". Rewritten for `projects/<id>/<version>/spec.json`.
- [[scripts-reference]] had the same stale paths in its run-spec example and its per-script usage lines; updated, including the note that prompts are text in the spec and materialised to `.gen/`.

Verified after: all four run-specs `check: PASS`, and a dry run shows candidates targeting `seed/` and prompts resolving through `.gen/`.

## 2026-09-25 — Blueprint brought up to the current structure

[[idea-to-video-blueprint]] still described the pre-reorganisation world: `raw/<project>/` for sources, `raw/clips/<project>/` with `masters/` and `work/`, prompts as `stills/sN.txt`, the run-spec inside the root `projects.json`, QC notes in `work/`, and hand-written `raw/clips/kyle/*.sh`. Eight places corrected, and the layout section replaced with the project/version tree plus a six-step **Starting a new project** checklist — now placed *before* Phase 0, since setting up the folder precedes the intake questions, with a row pointing at it from the phase table.

It now states that prompts live in `spec.json` (materialised to `.gen/` at run time), that a version is named for its method, and that Phase 10 must fix any shot whose staging changed mid-run.

## 2026-09-25 — Wrote down what belongs in the plan vs the spec

The split had been implicit and was drifting. Now stated in [[repo-structure]] with a table, and summarised in [[idea-to-video-blueprint]]: *if changing it changes the render it goes in `spec.json`; if it explains why, it goes in the plan.* Settings, prompts, shot list, takes and trims are spec; story, beats, rejected attempts and the rules they taught are plan.

Two rules attached to it, both learned the hard way this week: the spec must describe **what actually shipped** (v3-photo-cut's spec described the diptych staging that failed, so a re-run would have reproduced the bug), and the plan is **the only place a failure survives** — the spec keeps one prompt per shot, the one that worked, so everything rejected has to be written down elsewhere or it is lost.

## 2026-09-25 — Prompts moved into spec.json

Prompt text lived in two places depending on a project's age: `stills/*.txt` for the four CLI films, inline in `spec.json` for everything older — and kyle_rescue carried both, 8 scenes inline *and* 18 files, with nothing checking they agreed. Now every prompt is text inside its version's `spec.json`: each shot's `still.prompt` and `video_prompt`, plus a `run-spec.prompts` map for recipes no shot owns (master portraits, location plates, the dropped s6). 100 duplicate `.txt` files removed.

`film_run.py` materialises each prompt to `<version>/.gen/<shot>.txt` before calling the shell scripts, so they keep taking a file path; `.gen/` is generated and ignored. `check` now validates that a prompt is non-empty text rather than that a file exists.

Caught while doing it: the v3-photo-cut spec still described the **diptych** staging for the four character beats, which is the form that *failed* — the delivered film restaged them from the master portrait. A re-run from that spec would have reproduced the bug, not the film. Corrected, with the reason recorded in `run-spec.note`.

One tracked file per version now carries settings, shot list, prompts, takes and trims.

## 2026-09-25 — Wiki index reorganised around projects

The index had a separate **Plans** section listing project pages away from the registry, and its descriptions had gone stale (FLL farm under anime, the deleted three-minute film, only Kyle under 3D). Plans now sit inside **Projects**, under a line explaining that each project owns its folder and its plan lives in it, with the registry pages first and the six plan pages after, each labelled by project and version.

Landing-page cards also gained two fixes while the section was being rewritten: they now use each page's own `# H1` (trimmed at the subtitle dash, so "Lost City" rather than "lost city plan") and render inline `**bold**` and `` `code` `` instead of printing the asterisks. Both were long-standing, just more obvious with ten cards in one section.

## 2026-09-25 — All three FLL projects consolidated as bot_builders_champion

`fll_farm`, `fll_bot_builders` and `fll_champions` were one team filmed three ways, so they are now one project with three versions: `v1-anime-loop` (the Shinkai-style 9:16 loop of the Coastal Roots Farm visit, no faces, driven through the app), `v2-comic-cut` (63.5 s 16:9 film from the 3-page comic) and `v3-photo-cut` (59 s 16:9 film from the family's photographs). Both plan pages moved to `projects/bot_builders_champion/plan/` and were renamed to match; the registry is down to **10 projects**.

The registry now renders a **Versions table** per project — version, what it is, status and its own YouTube link — because a project's older versions can have their own uploads. Without it the anime loop's video would have vanished when the newest version took the summary row.

Two notes on the merge: the project's theme follows its newest version, so this one now sits under [[projects-3d]] and the anime loop no longer appears on [[projects-anime]]; and consent differs by version — v1 is a faceless wide of the farm, v2 and v3 show the children with all five families' consent.

## 2026-09-25 — coast and coast_v2 merged into one project

They were one film made twice — same scene, same music, different still model — so they are now `projects/coast/v1-wan-t2v-still` (Wan 2.2 T2V still, superseded) and `projects/coast/v2-klein-still` (FLUX.2 klein still at 1024×1792 cropped to 576×1024, the version on YouTube). The registry is down to 12 projects and shows coast once, newest version first, with both listed. Exactly the case the version scheme was for: the second attempt is a variant of the same project, not a separate one.

## 2026-09-25 — Versions inside each project

**Structure**: `projects/<id>/<version>/` where version is `v<n>-<short-description>` of the *variant* — how that attempt was made. 655 items moved. Existing work retrofitted by method: the seven loops and dragon_epic are `v1-drawthings-ui`; kyle_rescue, lindsey_art and fll_bot_builders are `v1-drawthings-cli`; lost_city splits into `v1-drawthings-ui` (shots 1–13, through the app) and `v2-drawthings-cli` (s14, s15); fll_champions is `v2-master-restage` (the Pixar rebuild that shipped).

Each version folder is self-contained — its own `raw/ seed/ stills/ clips/ music/ final/ logs/` and its own `spec.json`, stamped with `version` and a one-line `variant`. The plan page stays at project level and tells the story across versions. `film_run.py <id>` runs the newest version, `<id>@<version>` pins one. `build_projects.py` reads `projects/*/*/spec.json`, shows each project's newest version and lists the rest. Verified: four run-specs still PASS, and `lost_city@v1-drawthings-ui` correctly reports no run-spec because the app-driven version never had one.

## 2026-09-25 — final/ means the film, not the shots

**Convention fixed** (Kevin): `final/` holds only the assembled film and its delivery copies; everything shot-scoped — the `.mov` export, the trimmed ProRes, the per-shot `_4k.mp4` and its stamp — belongs in `clips/`. `film_run.py finish` now writes per-shot output to `clips/` and only the master plus deliveries to `final/`; 105 existing files were moved to match. lost_city's `final/` is down to the 30 s rift coda (an assembled sequence, so still a deliverable) and kyle_rescue's stray `music_bed.wav` went to `music/`. [[repo-structure]] and `CLAUDE.md` updated.

## 2026-09-25 — Structure written up as a page

**Created**: `wiki/repo-structure.md` — the shared-root vs per-project split, what each folder holds (`seed/` being the non-obvious one), tracked vs generated, how `run-spec.dir` ties the registry to a folder, how plan pages publish with the wiki, a checklist for starting a project, and the intermediate-deletion table with the sole-copy guard. `CLAUDE.md` now points at it instead of carrying a second copy of the tree. Indexed under Recipes.

## 2026-09-25 — Repo reorganised into one folder per project; film3min removed

**Reorganisation**: every project now owns `projects/<id>/` with `plan/ raw/ seed/ stills/ clips/ music/ final/ logs/`; 843 files moved out of the old split (sources in `raw/<project>/`, output in `raw/clips/<project>/` under four different layouts, seven projects loose in `raw/clips/`, music shared, plans in `wiki/`). Shared infrastructure — `wiki/`, `docs/`, `scripts/`, `tools/`, `raw/` for cross-project sources, `projects.json` — unchanged. `build_site.py` now collects pages from `wiki/*.md` **and** `projects/*/plan/*.md`, so project pages publish with the wiki and `[[links]]` resolve from either place. The shell scripts needed no edits because `film_run.py` resolves paths from `run-spec.dir`.

**Intermediates cleared** across all projects: 23 GB of `*_4k_frames`, 1.6 GB of trimmed ProRes, 5.8 GB of source clips that already have a 4K counterpart, 104 MB of rejected candidates — **35 GB → 5.5 GB**. Kept the films, the per-shot 4K mp4s (so any project can be re-cut without re-rendering), stills, masters, prompts and music. Three `.mov`s spared as sole copies: lost_city's s9 pair and an old fll_farm drone test.

**Removed**: the `film3min` project — three-minute narrative film, in planning since 2026-09-21, never given a story, characters or a single render. Its plan page, registry record and inbound links are gone; the work it informed lives on in [[character-consistency]] and [[identity-conditioning]]. Registry is now 13 projects.

## 2026-09-25 — BOT Builders photo cut delivered (59 s, from family photographs)

**Source**: 13 photographs from Kevin in `raw/fll_champions/`; rendered unattended overnight with `film_run.py` after he went to sleep.

**Delivered**: `raw/clips/fll/final/fll_champions_3840x2160.mp4` (59.08 s) and the 1920×1080 copy, music "Light Adventure", mean −18.8 dB / peak −5.5 dB. Eleven shots; the competition-floor wide was dropped after two failed passes and its neighbours stretched.

**Created**: `wiki/fll-champions-plan.md` with the full record.

**What this project taught** — all of it about getting a *real* child's likeness through klein:
- Asking to "convert this photo into a 3D animated character" makes klein substitute its own default face. Ask it to **stylise the rendering, not the identity**, and name every feature to keep (ethnicity, skin tone, hair colour/texture/cut, eye and eyelid shape, eyebrows, nose, mouth, jawline, age) plus the drifts to avoid (no westernising, no enlarged eyes, no lightened hair, no ageing up).
- **Photoreal made it worse, not better.** Tried at Kevin's request mid-project: the sharper the render, the more obvious the mismatch. Stylisation forgives what photorealism exposes. Reverted to Pixar.
- **klein warms black hair to brown on every pass** — say "pure black hair, not brown, not chestnut, no warm highlights".
- **It copies the source photo's lighting**, so a sunset backlight bakes orange into hair and skin unless the prompt neutralises it.
- **A diptych needs a person in the layout image.** Pointed at an empty venue plate, klein renders the room and leaves the child out entirely — two shots came back with nobody in them. Restaging from the master portrait (identity from pixels, scene from text) worked first time.
- Signature features vanish unless named (Kyle's spiked fringe), and then overshoot — take the mildest seed.
- Shirts print garbled text unless told "plain, no printing, no graphics, no letters"; "no text anywhere" must name clothing and props explicitly.

**The mistake worth keeping**: the delivered cut mixes two generations of stills — seven shots from 2026-09-23 (before masters existed, identity from raw photo edits) cut against four restaged from the rebuilt Pixar masters on 2026-09-25. Their clips were individually fine, so they were carried forward rather than re-rendered, and the film ends up drawing the same five children two ways. **When the look or the master recipe changes, every still is stale — re-render all of them.** A stale still is not broken and passes QC; the damage only appears in the cut. Filed as [[idea-to-video-blueprint]] Phase 5b and [[bot-builders-champion-photo-cut-plan]] §3b.

**Updated**: `projects.json` (delivered, files, music), `wiki/index.md`.

## 2026-09-24 — Two FLL films; the photo cut retired

**What happened**: an overnight run in another session delivered **`fll_bot_builders`** (Bot Builders, 63.5 s 16:9, 12 shots from a 3-page comic, 1920×1080 + 3840×2160 + 1280×720, music "Victory"). This session had separately taken the same team through the blueprint from the family's **photographs** — intake, consent, 8-shot storyboard, 5 character masters, 8 picked stills, 8 rendered clips — but stopped before QC. With the comic film shipped, `fll_champions` is marked **superseded**; its stills and clips stay in `raw/clips/fll/` (818 MB).

**Kept from it** — two klein-edit rules now in that project's `scenes.locks.rules`:
- **An edit inherits the source pose.** Chaining the calm closing portrait off the celebration still reproduced the jump in all three seeds. Fix: name the new pose positively *and* negatively — "both feet flat on the ground, arms relaxed at their sides… nobody jumping".
- **klein drops people from crowded groups.** Only 1 of 3 seeds of the celebration shot kept all five children. Group shots need 3 seeds and a headcount at pick time, not a glance at a thumbnail strip.

**Also fixed**: `fll_bot_builders` shipped without a `theme`, so the registry builder was filing it under *anime*; tagged `3d`.

## 2026-09-24 — Bot Builders delivered (63.5 s of a planned 90)

Third blueprint film, first with five recurring kids. Intake: separate project from fll_farm, faces OK (all families consent), **no extra kids**, 16:9, 90 s, full group close-ups, "Victory" (The_Mountain). New per-kid masters (Kyle's and Lindsey's re-dressed) + a **team master** used as the diptych reference for every shot. Stills: 4 of 12 failed the child count first time (comic panels with 6 figures are copied regardless of prompt → rebuilt S10 as an edit of the approved S5). Clips: in 7 of 12, LTX pulled back and invented extra children after 3–6 s; "no zoom, no pull-back, no one enters from any edge" held S8 but not S5/S7/S10. Every clip trimmed before the first wrong frame → 63.5 s, zero frames with six kids. Rules for group films added to [[idea-to-video-blueprint]] (frame groups wide, ~5 s usable per group clip, double the shot count). Report in [[bot-builders-champion-comic-cut-plan]] §0.

## 2026-09-23 — Kyle film on YouTube

Kevin uploaded the 2160×3840 master as a Short: https://youtube.com/shorts/KscAwvCi6iQ. Recorded in `projects.json` (`youtube`) and the plan's results; the projects page embeds it.

## 2026-09-23 — Lindsey film on YouTube

Kevin uploaded the 2160×3840 master as a Short: https://youtube.com/shorts/lbU-_73MliI. Recorded in `projects.json` (`youtube`) and the plan's results; the projects page embeds it.

## 2026-09-23 — Lindsey: A Small Dream delivered (second blueprint film)

Intake (2 batches of 4 questions), storyboard approval and a Pixabay music pick ("Emotional Children Piano", ranked by loudness curve), then the whole run through `scripts/film_run.py` from the `lindsey_art` run-spec: master (4 seeds, picked 3), 36 still candidates, 13 LTX renders for 8 shots, 73 min of upscale. Delivered 59.96 s at 1080×1920, 2160×3840 and 720×1280 (`raw/clips/lindsey/final/`).

**Kevin caught two errors I had passed on thumbnails**: S3 two hands on one pencil, S6 people walking through signboards. A full-size recheck then caught S8 v1 (girl sinking, horizon fixed). Fixes: S3 restaged hands-free (LTX re-grew a second hand even from a one-hand still), S6 new still with no standing props and separated people, S8 v2 camera still, S2 v3 cat pinned ("exactly one cat"). New rules → [[idea-to-video-blueprint]] failure playbook and rubric (judge at full size). `qc_sheet.sh` now detects the LTX end fade automatically. zsh gotcha: `for p in "s2 3"; do cmd $p` doesn't split in zsh — pass arguments explicitly.

## 2026-09-23 — "film spec" renamed to "run-spec"

Kevin's call. The `projects.json` block is now `run-spec` (was `film`); `film_run.py` reads `run-spec` from a project or from a standalone file (`{"run-spec": {...}}` or the bare block). Docs updated: [[scripts-reference]], [[idea-to-video-blueprint]], index, CLAUDE.md. The blueprint now states the split: the plan page holds story, decisions, rules and results; the run-spec holds the exact settings and is the only thing a run reads.

## 2026-09-23 — Script audit: every pipeline step driven by the film spec

Kevin asked for the list of scripts the blueprint needs, each able to handle whatever size/model the plan's spec decides. **Audit findings fixed**: `dt_diptych.sh` hardcoded klein steps/cfg/sampler (now env, + text-to-image mode, validation, DRY_RUN); `upscale_4k.sh` fixed 4× (now SCALE / anime 2×–3×), crop-only (FIT=pad), no audio (KEEP_AUDIO; dropped `-shortest`, which lost a frame), fixed bitrate, progress spam, no frame-count check; `assemble_film.sh` needed ≥2 clips, letterbox coordinates hardcoded to 3840×2160, no music offset/tail/level/fades (amix normalisation halved music — now explicit levels whose defaults reproduce the old mix exactly), no music-only mode; `finish_clip.sh` hardcoded 81 frames/16 fps/576×1024; an ffprobe `csv=s=' '` parse bug. **New**: `dt_clip.sh` (LTX/Wan presets, 8k+1/4k+1 frame checks), `qc_sheet.sh`, `preflight.sh`, `film_run.py` driver (check/status/stills/pick/clips/qc/finish; projects.json id or spec file; per-shot upscale cache). Kyle's run is encoded as the reference `film` spec in `projects.json`. **Tested**: every validation path, text/edit/landscape stills, LTX 33 f, the first **Wan 2.2 run via the CLI** (refiner + Lightning LoRA in config JSON, 9 f at 512² in 57 s), anime-2× and padded-portrait upscales, assembly variants, and a 2-shot landscape film end to end through `film_run.py`. Docs: [[scripts-reference]] (phase table, spec, workflow, tests), [[idea-to-video-blueprint]] (one command per phase), CLAUDE.md folder list.

## 2026-09-23 — Blueprint: idea to video with minimal human input

Kevin asked for an end-to-end blueprint. **Created** `wiki/idea-to-video-blueprint.md`, distilled from the unattended Kyle run: human input only in Phases 0–3 (12-question intake, storyboard approval, bible, preflight), then Phases 4–10 unattended (klein edit-mode masters, diptych/chained stills, motion prompt rules, LTX batch loop, QC contact sheets with a reject/redo ladder, finish script, report). Includes pick rubric, measured time budget (~0.6 h + 0.35 h per shot), folder layout, failure playbook, and what's not automated yet (a single `film_run.sh` driver, face-embedding scoring, TTS). Index and CLAUDE.md "Producing a video" now point to it.

## 2026-09-23 — Projects registry split by theme

**Source**: Kevin — the projects page had grown past 960 lines and every record loaded at once.

**Changed**: `projects.json` gains a `theme` per project (`anime` / `realistic` / `3d`) and a `themes` block holding each theme's slug, title and blurb. `scripts/build_projects.py` now writes four pages instead of one: `wiki/projects.md` is a hub with the summary table grouped by theme (rows link straight into the theme page), and `wiki/projects-anime.md` (7), `wiki/projects-realistic.md` (3), `wiki/projects-3d.md` (1) carry the full records. 961 lines became 93 + 386 + 385 + 189. Adding a theme means adding it to `themes` — no code change.

**Also**: `scripts/build_site.py` now understands `[[slug|display text]]` wiki-links.

**Updated**: `wiki/index.md` (one card per theme page).

## 2026-09-23 — Kyle's Antarctic Rescue rendered overnight, unattended

Kevin's go at ~22:00; film finished 01:38 with no human input (Claude judged every pick). Delivered `raw/clips/kyle/final/kyle_rescue_1080x1920.mp4` + 2160×3840 master, 60.0 s, music tail from 93.4 s.

**Key findings**: klein `--strength` 0.7–0.9 barely changes the input on the released CLI; **1.0 = edit mode** (reference + instruction) — that made the 3D Kyle master in one 30 s pass. **Diptych trick** (reference left, input right, crop right half) replaced Moodboard; `scripts/dt_diptych.sh` added. Building the CLI from `main` failed (compile error in `ccv_nnc_mfa`, step 524/1254) and wasn't needed. LTX-2.3 portrait 576×1024 × 249 f: 9:21–9:31 per clip. LTX fades to dark at the end of 4/10 clips. Two clips redone: S2 (hair restyled by "wind" wording, thumb dropped) and S4 (camera pull-back lost the chick). Upscale x4plus to 2160×3840 ~20 frames/min. Script bug: ffmpeg in a `while read` loop ate the shot list — fixed with `-nostdin` + fd 3.

**Changed**: `scripts/upscale_4k.sh`, `scripts/assemble_film.sh` (`W`/`H` portrait env, default landscape unchanged), new `scripts/dt_diptych.sh`; `wiki/kyle-antarctic-rescue-plan.md` §0 results with every pick/rejection and QC sheets; `wiki/headless-cli-pipeline.md` §1c; `wiki/scripts-reference.md`; `projects.json`.

## 2026-09-22 — Kyle plan restyled: 3D animated film

Kevin wants a "3D realistic world"; clarified as a **3D animated feature-film look** (stylised characters, physically real ice/snow/water), face from the comic (no photo). Consequence: 2D → 3D needs klein at ~0.75–0.9, which keeps layout but redraws the face, so the panel alone no longer locks identity. Plan rewritten around two stages: **Stage A** 3D model sheets (Kyle front and ¾, sidekick, chick, saucer) from comic crops, Kevin picks; **Stage B** every face shot locked to the masters via, in order, multi-`--image` from a `--HEAD` CLI build, a single-image diptych (master | panel), a two-pass face transplant, or the app Moodboard for failing stills only. Collages (S6, S8) now use 3D pieces so they only blend. Upscaler switched to x4plus. Experiments renumbered K0–K7; budget ~5–6 h. `projects.json` locks and shot methods updated.

## 2026-09-22 — Kyle plan: consistency strategy

Kevin asked how Kyle's face, the animals and the UFO stay consistent. Added §4b to the plan: (1) **pixel anchors** — every shot now starts from comic pixels; the three former text-only shots get a P1 ship crop (S1) or a **panel-cutout collage** blended by klein img2img (S6 saucer over ice, S8 animals + sky), which stands in for the Moodboard the CLI lacks; (2) a verbatim text lock per entity (UFO, penguins, chick, sidekick, seal, orca, whale, ship added; never write "UFO"/"alien"; say "one boy"); (3) drift limits inside clips (hold-position faces, slow foreground, S5 ≤ 6 s, little camera motion); (4) one look — same style/model/upscaler, optional shared colour pass; (5) a QC contact sheet per clip with explicit reject criteria; fallbacks: CLI from `main`, one Moodboard still in the app, or a cloud Kyle LoRA. K4 is now the collage test. `projects.json` locks updated.

## 2026-09-22 — Kyle plan: music chosen

Searched Pixabay (adventure kids / family orchestral / heroic kids) — ~20 candidates. Can't listen, so ranked by tags, play count and an in-browser loudness profile (WebAudio decode, 5 s RMS windows). Kevin picked **"Best Adventure Ever"** (geoffharvey, 2:33, 417k plays, Disney/quest tags) → `raw/clips/music/best_adventure_ever.mp3`. Runners-up recorded in chat: "Wonders of the Earth" (Grand_Project; best build-and-drop but epic and overused), "Magical Journey" (geoffharvey; 1:21, flat). Plan step 6: use the track's last 60 s — its dip, climb and ending line up with the UFO, freeze-ray and happy-ending beats; pre-cut the bed with ffmpeg since `assemble_film.sh` has no music offset. All open questions on the plan are now answered.

## 2026-09-22 — Kyle plan: Kevin's answers (9:16, music only)

Kevin answered the open questions: **9:16 for phones**, **pictures and music only**, **no narration**, and Kyle is his son (consent settled). Plan updated: stills/clips at 576×1024; each panel gets a 9:16 window by tight crop (panels 2, 5) or pad-and-repaint at higher klein strength (panels 1, 3, 4); LTX audio discarded, no remux, no captions or end card; master 2160×3840 plus a 1080×1920 phone copy. New prerequisite found: `upscale_4k.sh` and `assemble_film.sh` both hardcode 3840×2160 and would crop a portrait clip to a landscape strip — they need a `W`/`H` option (plan step 5a). New experiment K6 (portrait LTX). Music still open. `projects.json` `kyle_rescue` updated.

## 2026-09-22 — Plan: Kyle's Antarctic Rescue (1-minute, headless)

**Source**: `raw/kyle/comic_source.webp` — a 5-panel comic Kevin shared (Kyle on an Antarctic expedition; UFO attacks the ice; rescue with a freeze-ray; happy ending with the penguins). Added to `raw/`.

**Created**: `wiki/kyle-antarctic-rescue-plan.md` — how to make a 60 s film from it with `draw-things-cli` only. Key decision: the released CLI has no Moodboard, so Kyle's identity comes from the panels themselves (crop → `delogo` the bubbles → klein img2img at strength 0.45–0.6), plus a verbatim text lock and last-frame chaining. 8 shots (5 from panels, 3 text-only), LTX-2.3 at 249 f with the Lost City config JSON, Real-ESRGAN anime model for the illustrated look, `assemble_film.sh` with 0.75 s crossfades, captions via `drawtext`. Experiments K0–K5, ~4–5 h machine time. Nothing rendered yet.

**Updated**: `projects.json` (new `kyle_rescue` record, status planned, locks + all 8 scene prompts), `wiki/index.md`.

## 2026-09-22 — First headless render: Lost City shot 14 through `draw-things-cli`

**Source**: hands-on. `brew tap drawthingsai/draw-things && brew install draw-things-cli` (prebuilt binary, 178 MB, version `1.20260430.0`).

**Done**: rendered the film's final shot end to end with no Draw Things window — 3 klein stills at 27–35 s each (1280×768, 4 steps, `--config-json '{"shift":3.0,"sampler":16}'`), then LTX-2.3 at 249 frames in **9 min 41 s** (~2× faster than the same settings in the app), then `upscale_4k.sh`. Files: `s14_still_v1.png` (+ s1/s3 seed variants), `s14_ltx_v1.mov`, `s14_ltx_v1_4k*.mp4`.

**Verified**: the CLI resolves models from the app's own container (and pulled the Gemma 3 12B text encoder itself); `--image` + `--frames` is true image-to-video (frame 0 is the still pixel-for-pixel); the `config.fbs` sampler indices hold in practice (16 = DDIM Trailing, 19 = TCD Trailing); `stochasticSamplingGamma` is 0…1; output is ProRes 422 HQ + `pcm_f32le`, identical to the app's export.

**Limitation found**: the *released* binary takes a single `--image` (img2img). Repeatable multi-reference `--image`, `--remote` and `--avc` exist only in `main`. So Moodboard-conditioned stills still need the app. Also: the progress spinner is TTY-only, so a redirected log stays empty until exit.

**Story**: s14 v2 (enlarged creature, subject-first rigidity wording) fixed the motion bleed — the creature holds for the full 10 s while every spire comes down behind it, ending on an empty dust skyline.

**Updated**: `wiki/headless-cli-pipeline.md` (§1b measured, recommendation rewritten), `wiki/lost-city-plan.md` (§3c headless block, 7b row, shot 14 marked shot), `projects.json`.

## 2026-09-22 — Can this run without a UI? Yes: `draw-things-cli`

**Source**: Kevin's question ("can it be done via CLI"). Research: the `drawthingsai/draw-things-community` source (read directly — `Apps/DrawThingsCLI/DrawThingsCLI.swift`, `Libraries/Scripting/Sources/ScriptModels.swift`, `SharedScript.swift`, `Libraries/DataModels/Sources/config.fbs`), the draw-things-cli announcement (2026-03-25), ComfyUI FLUX.2 klein docs and multi-reference node packs, two Apple-Silicon field reports (Wan 2.2 GGUF on M1 Max, ComfyUI+Wan on M2 Max), mflux, ltx-video-mac.

**Created**:
- `wiki/headless-cli-pipeline.md` — the four stages vs what has a CLI; `draw-things-cli` flags (repeatable `--image` = Moodboard, `--frames` + `--output clip.mov` = video, `--config-json` in `JSGenerationConfiguration` format for shift/sampler/SSS/refiner/LoRA), the sampler enum (16 = DDIM Trailing, 19 = TCD Trailing), our Lost City settings as config JSON, `gRPCServerCLI`, the app's HTTP API and JS scripting API (the only place Moodboard *weights* are exposed), and the non-DT routes (ComfyUI headless, mflux, mlx-video-with-audio, diffusers on MPS).

**Findings that matter**: the CLI reads the app's own `Models/` directory, so our exact checkpoints (`flux_2_klein_9b_i8x.ckpt`, `ltx_2.3_22b_distilled_1.1_q8p.ckpt`, the Wan i2v pair) need no re-download; model *recommended settings* are the CLI's defaults, with `--config-json` merged on top. Against that, ComfyUI on Metal cannot load FP8 at all and a field test measured 82 min for a 2-second Wan 2.2 GGUF clip on an M1 Max — versus ~20 min for a 10-second LTX clip in Draw Things here. mflux is stills-only.

**Open**: three things need one test render each — whether `--image` + `--frames` is true image-to-video, whether klein reference images land in the Moodboard channel at equal weight, and the scale of `stochasticSamplingGamma`. Next step if it passes: `scripts/dt_render.sh` driving renders straight from `projects.json`.

**Updated**: `wiki/index.md` (new entry under Models & tools).

## 2026-09-19 — Wiki created; first brainstorm filed

**Source**: Chat brainstorm on making 4K video from personal photos. No files in `raw/` yet.

**Created**:
- `CLAUDE.md` — wiki rules, adapted from `garden-kb`
- `.obsidian/` — vault config copied from `garden-kb` (workspace.json excluded)
- `wiki/photo-to-4k-video-approaches.md` — overview of four pipelines
- `wiki/index.md` — table of contents
- `wiki/log.md` — this file

**Open items carried forward**: photo resolution/count, style target, local GPU vs cloud budget. Five concept pages are linked but not yet written.

## 2026-09-19 — Research: local open-source 4K video on Apple Silicon

**Source**: `raw/2026-09-19-local-4k-video-research.md` (web research notes, ~18 URLs, plus `system_profiler` hardware check: Mac Studio M4 Max 48 GB).

**Created**:
- `wiki/local-open-source-4k-video-pipeline.md` — main recommendation page
- `wiki/image-to-video-models.md` — model catalog (fills earlier stub)
- `wiki/video-upscaling.md` — upscaler catalog (fills earlier stub)
- `wiki/apple-silicon-inference.md` — Mac-specific traps and runtimes

**Updated**: `wiki/index.md`

**Key findings**: FP8 checkpoints do not run on Metal; ComfyUI-on-MPS is 5–20× slower than NVIDIA; Draw Things and MLX ports are the practical Mac runtimes; no open model does good direct 4K on Mac yet, so generate 720p–1080p and upscale with SeedVR2 (MPS supported). LTX-2.5 (2026-08-11) claims native 4K but unverified on Mac.

**Open items carried forward**: measure real M4 Max clip times; test ltx-2-mlx LTX-2.5 at 1080p; SeedVR2 memory at 4K; face fidelity comparison. Stubs still unwritten: frame-interpolation, depth-parallax, ffmpeg-pipeline.

## 2026-09-19 — Static site added

**Source**: pattern from `FLL-kb/scripts/build_site.py` and `yang-kb/serve.sh`.

**Created**:
- `scripts/build_site.py` — renders `wiki/*.md` → `docs/wiki/*.html`; landing `docs/index.html` generated from `wiki/index.md` sections as cards; `[[links]]` to unwritten pages render as dashed stubs
- `serve.sh` — rebuild + `http.server` on 8788
- `.claude/launch.json` — preview config
- `docs/` — built output

**Updated**: `CLAUDE.md` (Site section, folder structure).

## 2026-09-19 — Draw Things setup page

**Source**: appended Draw Things research to `raw/2026-09-19-local-4k-video-research.md`; local checks (Draw Things installed, Models dir 4.7 GB, disk 21 GB free).

**Created**: `wiki/draw-things-setup.md`. **Updated**: `wiki/index.md`.

**Open items**: disk space must be freed (~100 GB) before any video model download; measure first clip time.

## 2026-09-19 — LTX-2.3 correction

**Source**: HF `Lightricks/LTX-2.3` card. LTX-2.3 is 22B (wiki previously said 19B — that was LTX-2). Added distilled 1.1 details (46 GB bf16, 8 steps, LoRA variant, bundled spatial upscalers; 4K is two-stage). Updated `image-to-video-models`, `local-open-source-4k-video-pipeline`, `draw-things-setup`.

## 2026-09-19 — Landscape page

**Source**: research file (Seedance/OpenArt/Wan 2.7 section appended) plus general knowledge; unsourced entries are marked *needs verification* inline.

**Created**: `wiki/video-generation-landscape.md` — four-layer map (models open/closed, harnesses, apps, websites) with dates and popularity. **Updated**: `wiki/index.md`.

## 2026-09-19 — Recipe pages

**Source**: chat Q&A grounded in Draw Things wiki + LightX2V settings already in the research file; app-specific control names marked *needs verification*.

**Created**: `wiki/wan22-i2v-locked-image-settings.md`, `wiki/face-identity-workflows.md`. **Updated**: `wiki/index.md` (new Recipes section).

## 2026-09-20 — Living-painting recipe, first real Draw Things run

**Source**: hands-on session driving Draw Things; reference TikTok frames.

**Created**: `wiki/living-painting-loop.md`. **Updated**: `wiki/index.md`.

**Findings**: Wan 2.2 T2V at 1 frame + Lightning LoRA makes a good painterly still in ~1 min on M4 Max. I2V requires the separate I2V checkpoint pair (High in Model, Low in Refiner). Downloaded `hne_i2v_i8x` (13.7 GB, ~27 min); `lne_i2v_i8x` in progress. Draw Things has no I2V button — mode is implied by model + canvas image.

## 2026-09-20 — First I2V clip measured

Wan 2.2 I2V 14B 8-bit pair, Lightning 4-step, 576×1280 × 81 frames: 24 min on M4 Max. Result matches the TikTok reference. Updated `living-painting-loop`, `local-open-source-4k-video-pipeline` (time budget), `draw-things-setup` (open items).

## 2026-09-20 — Living-painting loop delivered

Exported ProRes from Draw Things (toolbar export icon → `~/Documents`), cropped 9:16, ping-pong looped ×3 with ffmpeg 9.0.2 → `raw/clips/coast_loop.mp4` (30 s). Pipeline validated end to end. Updated `living-painting-loop`.

## 2026-09-20 — Loop method corrected

Ping-pong rejected (reverses wave and bird motion). Replaced with forward-only loop using an 8-frame tail→head crossfade. Updated `living-painting-loop`.

## 2026-09-20 — FLUX.2 klein still

Quality gap vs reference diagnosed (video-model still, no supersampling, I2V softening). Downloaded FLUX.2 [klein] 9B (8-bit S) + Qwen3-8B encoder (~17.8 GB). 1024×1792 still in ~1 min, reference-grade. Downscaled 2× for I2V; second I2V run in progress. Updated `living-painting-loop`.

## 2026-09-20 — Refiner mismatch gotcha

Second I2V run produced washed-out noise: recommended settings had selected the 6-bit Low Noise refiner (not downloaded) instead of the local 8-bit S. Documented in `draw-things-setup`. Re-running with correct refiner.

## 2026-09-20 — v2 loop delivered

FLUX.2 klein still → Wan 2.2 I2V (correct 8-bit refiner, 15.5 min) → forward-loop + lanczos 1080×1920 → `raw/clips/coast_v2_loop.mp4`. Reference-quality achieved. Updated `living-painting-loop`.

## 2026-09-20 — Music added, deliverable complete

Pixabay CC0 ambient track muxed with fades → `raw/clips/coast_v2_final.mp4`. Living-painting recipe complete end to end. Updated `living-painting-loop`.

## 2026-09-20 — Runbook + finish script

**Created**: `wiki/runbook-living-painting.md` (checklist distilled from the day's two runs, with failure-signature table), `scripts/finish_clip.sh` (loop + music in one command). **Updated**: `wiki/index.md`, `CLAUDE.md` (Producing a video section).

## 2026-09-20 — Torrey Pines video (second run of the runbook)

New Draw Things project, same settings. Still (FLUX.2 klein, seed 1190544862) → I2V (seed 284526412, ~15 min) → `finish_clip.sh` → `raw/clips/torrey_final.mp4`. No wasted renders; refiner trap caught by the checklist. Runbook updated: save exports straight into `raw/clips/`, ffprobe before looping; added a "Done so far" table.

## 2026-09-20 — Golden Gate (native 576×1024 test) + lock-screen finding

Still generated directly at 576×1024 with FLUX.2 klein: quality indistinguishable from the supersampled path in the finished video. Runbook now uses this as the default (one human click per video). Mac was locked for ~2.5 h with the Save dialog open; render survived, saved on unlock → `raw/clips/goldengate_final.mp4`. Documented lock behaviour in the runbook.

## 2026-09-20 — Mt. Rainier, zero-click run

New project → FLUX still at 576×1024 → Wan I2V from canvas → export sheet Save button pressed by automation → `finish_clip.sh` → `raw/clips/rainier_final.mp4`. No human input at any step. Runbook updated (export step, done-so-far table).

## 2026-09-20 — Cyberpunk city

Fifth video, zero-click. Night/neon scene works with the same style suffix; the Wan motion prompt handled rain + steam + flickering neon. Music mismatch noted (calm ambient on a cyberpunk scene) — next time pick a genre-matched Pixabay track. `raw/clips/cyberpunk_final.mp4`.

## 2026-09-20 — Projects registry + FLL farm video

Added `projects.json` + `scripts/build_projects.py` → `wiki/projects.md` (summary table + per-project models/settings/prompts/seeds/music/files). FLL BOT Builders farm video delivered: wide anime view of Coastal Roots Farm with the team as distant figures, no faces — after a photoreal attempt and a real-photo I2V attempt were both stopped at Kevin's request. `raw/clips/fll_farm_final.mp4`.

## 2026-09-20 — Cyberpunk music swap

Replaced calm-ambient with "Neon Synthwave Drive" (Pixabay). Registry + runbook music note updated.

## 2026-09-20 — YouTube embeds on the projects page

Playlist "AI-Vids" (PLJx49Sf61wKQ, 6 videos) mapped to registry entries by title via oEmbed. `projects.json` gained `playlist` + per-project `youtube` id; generator emits a playlist iframe under the summary and a 9:16 player on each record. Plain iframes work on GitHub Pages. Note: the uploaded fll farm video is v1.

## 2026-09-20 — FLL farm v2

Regenerated still with exactly 5 children + 1 adult standing still; I2V prompt gave people zero motion and put the motion budget on wind/chickens/clouds. Frame check: figures hold position across all 81 frames. `raw/clips/fll_farm_v2_final.mp4`. Registry updated; YouTube upload still shows v1.

## 2026-09-21 — Kevin's own I2V attempt (project vid-916) debugged

Symptoms: mid-denoise noise output + 5–9-frame clips. Causes: refiner set to Low Noise **T2V** (not downloaded → skipped), Frames 9, CFG 2.1, "drone camera, people walking" prompt. Fixed via automation; also found that clicking a Version History entry restores that entry's settings. Runbook updated.

## 2026-09-21 — Dragon Epic plan

New project planned, not started: `wiki/dragon-epic-plan.md` (pipeline, per-stage Draw Things settings, face strategy ranked, dragon consistency, 12-shot list, 7 gating experiments, ~8 h budget, open questions). Registry entry added as `planning`.

## 2026-09-21 — Dragon Epic: 4K delivery

Plan updated: generate stills + I2V at 1280×720, AI-upscale 3× to 3840×2160 (SeedVR2 first, Real-ESRGAN ncnn fallback, Draw Things upscaler to verify), FaceFusion before upscale, HEVC 10-bit via videotoolbox. New experiment E8 (upscaler bake-off); budget ~12 h.

## 2026-09-21 — Dragon Epic: first 4K clip

Scene 1A end to end: FLUX.2 klein still at 1280×768 (first seed) → Wan 2.2 I2V 81 f (~43 min, GPU shared) → Real-ESRGAN ncnn 4× (5.6 min) → 3840×2160 HEVC 10-bit. Real-ESRGAN needs `-t 128`, `-j 1:1:1`, and cwd = its own directory. `scripts/upscale_4k.sh` added. Plan §7b + registry updated.

## 2026-09-21 — Scene 1A ghosting diagnosed

Double-exposure on the dragon from frame ~55. In the Wan output, not the upscale. Hypothesis: Refiner Start 10% → High-Noise expert underused on large motion. Plan and runbook updated; re-render pending (Draw Things not running, screen locked).

## 2026-09-21 — False alarm: "lost" render was still running

`pgrep -x "Draw Things"` reports the app absent even while it renders; v2 finished normally through a lock. Keep-awake kept as insurance; runbook corrected to say locks are safe.

## 2026-09-21 — Scene 1A v2 failed (refiner 50%)

Output was noise. Refiner Start 50% is incompatible with the 4-step Lightning LoRA (trained for 10%). Reverting to 10%; v3 attacks ghosting via the motion prompt instead. Plan + runbook corrected.

## 2026-09-21 — Character consistency research + 3-minute film plan

Web research on keeping one character consistent across shots (as of 2026-09-21). Key findings: FLUX.2 klein takes reference images via the Draw Things Moodboard (official face-swap demo); Qwen Image Edit 2509 does Picture 1/2/3 multi-reference in DT; local klein LoRA training crashes on Apple Silicon (draw-things-community #114, open), cloud training ~$1 / < 1 h; Wan 2.1 VACE subject reference is in DT, Wan 2.2 Animate is CUDA-only, Wan 2.5/2.6/2.7 have no weights; LTX-2.5 has native multi-shot + multi-subject LoRA but unproven on Mac. **Created**: `wiki/character-consistency.md` (methods ranked, decision table), `wiki/three-minute-film-plan.md` (36–40 clips, consistency stack, X1–X7 experiments, ~23 h budget, open questions). **Updated**: `index.md`, `face-identity-workflows.md`, `dragon-epic-plan.md` (links), `projects.json` (film3min, planning).

## 2026-09-21 — Identity conditioning concept page

Filed the Q&A on *why* consistency tools work: `wiki/identity-conditioning.md` (five conditioning channels — text, in-context reference tokens, ID adapters, LoRA, first-frame latent — and our stack mapped onto them). Linked from `character-consistency`, `index`.

## 2026-09-21 — 3D infographic for the landscape page

Built an isometric "four-layer stack" infographic of `video-generation-landscape` (models → harnesses → local apps → platforms, gold outlines = this project's path). Source is CSS-3D HTML in `scripts/infographics/video-generation-landscape.html`, rendered by `scripts/render_infographic.sh` (headless Chrome, 2×) to `wiki/assets/video-generation-landscape-3d.webp` (~390 KB). Not a generative-model image — content mirrors the page's tables. **Changed**: `build_site.py` now copies `wiki/assets/` → `docs/wiki/assets/` and styles `img`; page embeds the image above "How to read this page"; `CLAUDE.md` folder list.

## 2026-09-21 — Scene 1A v3 clean at 4K

Ghosting fixed by the prompt, not the refiner: full-frame subject articulates but does not translate. Rule added to plan §3b. `raw/clips/dragon/scene1a_v3_4k.mp4`.

## 2026-09-21 — Dragon Epic music chosen

"The Dragon's Breath" (ONECinematicStudio, Pixabay CC0) picked as the film's music bed; RMS profile shows the track peaks at 135–155 s, so scene 1A's preview uses that section. Muxed `raw/clips/dragon/scene1a_v3_4k_music.mp4`. Plan §3e + open question 4 + `projects.json` updated.

## 2026-09-21 — Dragon Epic scene 1A on YouTube

Added `Xzu-c5yX8uo` to the dragon_epic record. `build_projects.py` now picks the embed orientation from the I2V size (landscape `yt`, portrait `yt yt-v`) instead of hard-coding 9:16. Title corrected to "family hero face".

## 2026-09-21 — Lost City project plan

New project from an OpenArt reference (rider on a wingless raptor-dragon walking into overgrown spire ruins, god rays, waterfall). Research: Wan 2.2 prompt guides (subject+scene+movement; I2V = motion + camera only; 80–120 words; name the camera move and speed every time), LTX docs (I2V: describe what happens, not the image; 4–8 sentence paragraph; dialogue in quotes; defaults 768×512 × 97 f @ 24 fps, CFG 1 dual-CFG; sizes ÷32, frames 8k+1), Draw Things LTX-2 wiki (25 fps in DT; 20–25 steps / CFG 6–7 are dev-model numbers; ×2 / ×1.5 latent upscalers via High Resolution Fix). **Created** `wiki/lost-city-plan.md` — reference breakdown → local recipe, §3 Draw Things settings for klein stills (Moodboard crops only — full frames impose composition, learned on Dragon 1B v2), Wan 2.2 tracking-shot phrasing for a walking creature, first LTX-2.3 22B distilled 1.1 config (8 steps, CFG 1, 1280×736 × 121 f), creature/hero/city text locks, 8-shot list, L0–L6 experiments, ~10 h budget. **Updated**: `index.md`, `projects.json` (lost_city, planning), `.gitignore` (raw/lostcity/). Reference saved to `raw/lostcity/`.

## 2026-09-21 — Dragon Epic scene 1B stills v1/v2

E1 done (no klein-compatible face adapter → Moodboard). 1B v1: 1 face ref, medium shot, likeness partial, dragon anatomy wrong. v2: 3 refs (face head, face tight, 1A frame as dragon ref) — dragon now matches 1A and likeness improved, but the wide 1A frame pulled the composition wide. Fix for v3: dragon ref cropped to head/neck (`raw/dragon/ref_scene1a_dragon_head.png`). Both stills in DT project `Untitled-39715` Version History. Paused pending Kevin's pick.

## 2026-09-21 — Lost City L0 + L1: klein look test passes; first LTX-2.3 run on the Mac

Draw Things project `lostcity-s1` (renamed at creation — new rule: never leave Untitled). **L0**: FLUX.2 klein + 3 cropped refs from the OpenArt frame reproduces the look on seed 1 (`raw/clips/lostcity/s1_still_v1.png`). **L1**: LTX-2.3 22B distilled 1.1 runs in DT — recommended settings = 8 steps, CFG 1, TCD Trailing, SSS 30%, shift 5, 121 f, and High Resolution Fix on (the LTX two-stage: 640×384 → full size @70%). At 1280×768 stage 2 stalled in swap (27–48 GB); at 1024×576 × 97 f single-stage it finished in ~25 min wall (3 min compute + paging) with a PCM audio track. Motion is real locomotion (creature turns and walks into the city) but it ignored the tracking-shot staging. Verdict in plan §7b: LTX for locomotion shots, Wan 2.2 default otherwise. Also learned: the export Save sheet is AX-visible now (filename + Save from automation); rename dialog needs full-screen control. **Updated**: `lost-city-plan.md` §3c/§7/§7b, `projects.json`, memory notes.

## 2026-09-21 — Lost City stills for shots 2 and 7

`lostcity-s2` project: shot 2 (extreme wide, tiny rider) and shot 7 (canyon reverse) both first-seed keepers with two Moodboard refs (our shot-1 skyline crop + the reference spires crop). Shot 7 v1 grew bat wings from "raptor-like dragon, no wings" — klein at CFG 1 obeys the noun, not the negation; rewritten creature lock without the word "dragon" fixed it (plan §4). Draw Things quit and relaunched between drags and lost the unsaved prompt (settings survived) — re-check the prompt after any restart. Finder→Moodboard drag cannot be automated (synthetic drags don't register); the import icon loads to the canvas, not the Moodboard. Files: `raw/clips/lostcity/s2_still_v1.png`, `s7_still_v1.png`.

## 2026-09-21 — Lost City shot 2 clip at 4K

First finished Lost City clip: shot 2 still → Wan 2.2 I2V (49 min at 1280×768 × 81 f, refiner 11%, Lightning 100%, DDIM Trailing, shift 5) → Real-ESRGAN 4K (6:19). Slow push-in + tiny walking rider, no artefacts; L5 (foliage shimmer) passes. Gotcha: the export Save sheet's filename field refused typing this time (AXGroup, not AXTextField) — saved under the stale default name and renamed on disk; always `find -mmin` the export folder after Save. Files in `raw/clips/lostcity/`.

## 2026-09-21 — Shot 2 A/B: Wan 2.2 vs LTX-2.3

Same shot-2 still through both engines. Wan (768p, 49 min): subtle stable push, rider walks. LTX (576p, ~20 min, audio): real push-in with foreground parallax (invents palm fronds/column passing the lens), obeyed the camera prompt this time — an action-first paragraph with an explicit "camera pushes in … columns drifting past the edges" phrasing. Both clean. Recorded in plan §7b. Draw Things gotcha: clicking the export icon on a video saves straight to the last folder with the prompt-derived name (no sheet if the folder is remembered) — a second click makes a duplicate.

## 2026-09-21 — Wan vs LTX comparison filed

Kevin's questions (why LTX faster; which has better quality; T2V vs I2V) answered and filed as a section in `image-to-video-models.md` (latent-token math, fidelity vs motion, both runs were I2V). LTX shot 2 upscaled to 4K with audio re-muxed (`s2_ltx_v1_4k_audio.mp4`; `upscale_4k.sh` strips audio — mux back from the .mov).

## 2026-09-21 — Scripts reference page; assemble_film.sh

Kevin asked for a page explaining the key scripts. **Created** `wiki/scripts-reference.md`: toolchain table (ffmpeg 9, Real-ESRGAN ncnn-vulkan, python), then per script — purpose, invocation, numbered steps with the actual filter chains, the Metal-specific flags (`-t 128 -j 1:1:1`, cwd), timings, gotchas (audio dropped by the upscaler → remux command), plus the site/registry builders and an end-to-end map per project type. **Added** `scripts/assemble_film.sh` (xfade/acrossfade chain, silence padding for mute clips, optional music and 2.39:1 bars, HEVC 10-bit). Index + CLAUDE.md updated.

## 2026-09-21 — Draw Things project rename without screen control

Kevin asked for a rename path that doesn't need desktop takeover. Found: projects are `NAME.sqlite3` files in the app container; renaming the files renames the project and the list refreshes live (tested on a junk project). Added `scripts/dt_project.sh` (list/newest/rename/rename-newest/delete), documented in `scripts-reference.md`, CLAUDE.md and memory; the in-app Rename dialog is now a fallback only.

## 2026-09-21 — Lost City shot 3 (LTX) and the close-up rule

`lostcity-s3` (renamed on disk with `dt_project.sh` — no screen control; gotcha: the stale list row re-creates an Untitled if clicked, so refresh the panel and click the new name). Still first-seed keeper. LTX v1 with "one slow step" walked the creature out of frame and hallucinated a second rider — close-ups must use hold-position prompts; v2 clean. Music bed chosen (L6): "Mystical orchestral theme with ancient flute", mixed under LTX ambience. Files in `raw/clips/lostcity/`.

## 2026-09-22 — Lost City overnight batch: shot 7 done, s8–s12 queued

Shot 7 rear-view anatomy failures solved by switching to the side-profile framing that worked on shot 1 (rules in plan §7b). LTX frame slider maxes at 249 (10 s) — rendered in ~20 min, same as 97 f, so 10 s is now the default clip length. New `dt_project.sh clone` copies a closed project's DB (history + Moodboard refs) so new scenes need no drag; the app must be restarted after cloning or it treats the copy as empty. s8 (gallop) still keeper on seed 1, LTX running; s9 jump, s10 drink, s11 dismount, s12 mount queued.

## 2026-09-22 — Lost City batch: s8, s9, s10 done; s11 blocked

s8 gallop and s10 drinking finished at 4K with music; s9 jump trimmed to its clean 4.6 s. Two crashes traced to `ImageHistoryManager.pushHistory` when saving a video into a **cloned** project — fresh projects fixed it. New rules in the plan: slow in-place actions hold the creature design for a full 10 s clip, fast locomotion drifts after ~4–5 s; never upscale while LTX renders; the screen lock blocks all automation (disable auto-lock for unattended batches). s11 dismount blocked: klein renders two creatures for any "rider beside the mount" phrasing, negations don't help.

## 2026-09-22 — Lost City: escape ending, and every prompt in one place

Kevin added a story turn: the lost city collapses and the rider escapes. Wrote two scenes for it — **s13** (gallop down the avenue while a spire shears and falls, dust wall rolling after them) and **s14** (out on the plain, creature still and breathing while the whole skyline comes down behind). s14 deliberately uses the s10 pattern — slow foreground, violent background — because that is what holds the creature design for a full 10 s clip.

Also consolidated prompts: `projects.json` now has a `scenes` block per project (shared locks + still and video prompt for every shot), and `build_projects.py` renders it as a "Scene prompts" section on the projects page. Previously the prompts were scattered across `still.shot2_prompt`, `i2v.shot3_ltx_prompt` and similar keys, and several were never recorded. Shot list in the plan updated to v2 (10 s clips, shots 9–14 added).
