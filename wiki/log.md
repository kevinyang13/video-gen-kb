# Log

**Summary**: Append-only record of every operation performed on this wiki.

**Sources**: n/a

**Last updated**: 2026-09-19

---

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
