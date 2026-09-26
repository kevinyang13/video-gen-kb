# Scripts Reference

**Summary**: What each script in `scripts/` does, which tools and APIs it calls, and the exact processing steps. Since 2026-09-23 the whole [[idea-to-video-blueprint]] runs on these scripts, driven by a **run-spec** (the `run-spec` block in `projects/<id>/<version>/spec.json`) through `film_run.py`: every size, model, frame count, upscaler, crossfade, music and delivery setting comes from the run-spec, not from the script. Covers the generation scripts (`dt_diptych.sh`, `dt_clip.sh`), QC (`qc_sheet.sh`), post (`upscale_4k.sh`, `assemble_film.sh`, `finish_clip.sh`), `preflight.sh`, the driver, and the site/registry builders.

**Sources**: the scripts themselves (`scripts/*.sh`, `scripts/*.py`); hands-on timings in [[log]] 2026-09-20/21; Real-ESRGAN ncnn README (`tools/realesrgan/README_macos.md`).

**Last updated**: 2026-09-23 (audit: every script parameterised and validated; new `dt_clip.sh`, `qc_sheet.sh`, `preflight.sh`, `film_run.py`)

---

## The toolchain (all local, all free)

| Tool | Version here | Role | Why this one |
|---|---|---|---|
| **ffmpeg / ffprobe** | 9.0 (Homebrew) | every decode, filter, encode, probe | one binary does frames-out, loops, crossfades, scaling, muxing; `hevc_videotoolbox` uses the Mac's hardware encoder |
| **Real-ESRGAN ncnn-vulkan** | `tools/realesrgan/realesrgan-ncnn-vulkan` (xinntao 0.2 build) | AI 4× upscaler, per frame | runs on Metal via Vulkan/MoltenVK, no Python, no PyTorch; ~4 s per 1280×768 frame |
| **Python 3** | system | `build_site.py`, `build_projects.py`, small arithmetic inside the shell scripts | `markdown` package for the site |
| **Draw Things** | App Store | produces the input `.mov` (ProRes, 16 or 25 fps) | see [[runbook-living-painting]] — not a script, but every script starts from its export |

No cloud APIs anywhere. The only network call in the whole workflow is `curl` for a Pixabay music file when a project needs music.

Draw Things exports are **ProRes 422 `.mov`** (video) — 8-bit 4:2:2, 16 fps for Wan 2.2 or 25 fps for LTX-2.3, plus a PCM audio track for LTX. Every script probes the input first; sizes to expect: 576×1024 / 576×1280 (loops), 1280×768 (Dragon Epic, Lost City), 1024×576 (LTX tests).

---

## Scripts by production phase (audit 2026-09-23)

| Phase ([[idea-to-video-blueprint]]) | Script | Decided by the run-spec | Validates |
|---|---|---|---|
| 3 Preflight | `preflight.sh [--fix] [models…]` | models to check | CLI, ffmpeg, Real-ESRGAN, models, AC, disk, app closed, caffeinate, no overlapping jobs |
| 4–5 Masters, stills | `dt_diptych.sh REF IN PROMPT OUT [seed] [W] [H]` | `film.still` (model, steps, cfg, config, strength, seeds), `film.size` or per-shot `still.size` | W/H ÷64, files exist, REF needs IN |
| 7 Clips | `dt_clip.sh STILL PROMPT OUT [seed] [W] [H] [FRAMES]` | `film.clip` (+ per-shot `clip` overrides): model family LTX / Wan, frames, steps, cfg, config, video format | W/H ÷64, LTX 8k+1 / Wan 4k+1 frames, LTX > 1024×576 warning, still ≠ render size note, skip if exists |
| 8 QC | `qc_sheet.sh CLIP OUT [REF] [N] [TILE_H]` | shot `qc_ref` (a master) or the shot's still | frame indices from the clip itself — any length/fps |
| 9 Upscale | `upscale_4k.sh IN [out] [model]` | `film.upscale` (model, size, fit, bitrate), `assemble.clip_audio` → `KEEP_AUDIO` | model/scale exists, even W/H, frame count out = in |
| 9 Assemble + music | `assemble_film.sh OUT clip…` | `film.assemble` (fps, xfade, clip_audio, bitrate), `film.music` (file, start / `tail`, vol, fades) | clips/music exist, letterbox landscape-only, music-too-short note, expected vs actual length |
| 9 Deliver | inside `film_run.py finish` | `film.deliver[]` sizes and bitrates | — |
| all | **`film_run.py PROJECT check·status·stills·pick·clips·qc·finish`** | the whole run-spec (or a standalone `.json` run-spec file) | run-spec sanity: sizes, frame rules, paths, refs, trims, planned length |
| loop posts | `finish_clip.sh IN [music] [out]` | env: W, H, LOOPS, SEAM, FPS, MUSIC_VOL | clip long enough for the seam |

Every script: `set -euo pipefail`, a clear `die` message, `ffmpeg -nostdin` everywhere (ffmpeg inside a `while read` loop eats the loop's input — the Kyle overnight bug), and `DRY_RUN=1` on the two CLI wrappers.

### The run-spec

Lives in `projects/<id>/<version>/spec.json → run-spec` (Kyle's is the reference). It is the machine-readable half of a project: the plan page says *what and why*, the run-spec says *exactly how*, and it is the only thing a run reads. Paths are relative to `run-spec.dir`, except `music.file` (repo root). Only `dir`, `size`, `shots` are required; everything else has the defaults used so far (klein 9B still, LTX-2.3 249 f clip, x4plus → 3840×2160, 0.5 s crossfades).

```json
"run-spec": {
  "dir": "projects/kyle_rescue/v1-drawthings-cli", "name": "kyle_rescue", "size": [576, 1024],
  "still":   {"model": "flux_2_klein_9b_i8x.ckpt", "steps": 4, "cfg": 1, "config": {"shift": 3.0, "sampler": 16}, "seeds": [1,2,3], "strength": 1.0},
  "clip":    {"model": "ltx_2.3_22b_distilled_1.1_q8p.ckpt", "frames": 249, "steps": 8, "cfg": 1,
              "config": {"sampler": 19, "shift": 5.0, "stochasticSamplingGamma": 0.3, "fps": 25, "hiresFix": false}, "seed": 1},
  "masters": {"kyle": "seed/kyle_front.png"},
  "upscale": {"model": "realesrgan-x4plus", "size": [2160, 3840], "fit": "crop", "bitrate": "40M"},
  "assemble":{"fps": 25, "xfade": 0.75, "clip_audio": false, "bitrate": "40M"},
  "music":   {"file": "projects/kyle_rescue/v1-drawthings-cli/music/best_adventure_ever.mp3", "start": "tail", "vol": 1.0, "fade_in": 1.5},
  "deliver": [{"size": [1080, 1920], "bitrate": "12M"}, {"size": [720, 1280], "bitrate": "2.8M"}],
  "shots": [
    {"id": "s2", "still": {"ref": "kyle", "input": "seed/s2_in.png", "prompt": "<the still prompt text>"},
     "video_prompt": "<the motion prompt text>", "qc_ref": "kyle", "take": "clips/s2_ltx_v2.mov", "trim": [0, 8]}
  ]}
```

Still mode per shot: `ref` + `input` = diptych; `input` only = single edit; neither = text-to-image. `ref` is a master name or a path (an approved shot = reference chaining). A shot can override `still.seeds/size/model…` and `clip.frames/model/seed…` — e.g. one Wan shot in an LTX film.

### `film_run.py` workflow

```bash
scripts/preflight.sh --fix
scripts/film_run.py kyle_rescue check          # run-spec sanity + planned length
scripts/film_run.py kyle_rescue stills         # 3 seeds per shot → seed/<id>_c<seed>.png   (skips shots with a picked still)
scripts/film_run.py kyle_rescue pick s2 4      # → stills/s2.png  (judge picks)
scripts/film_run.py kyle_rescue clips          # clips/<id>_v1.mov (skips existing);  --v 2 --seed 2 s2 for a redo
scripts/film_run.py kyle_rescue qc             # seed/<id>_v1_qc.png
#   judge sets take + trim per shot in the run-spec
scripts/film_run.py kyle_rescue finish         # trim → upscale → assemble + music → delivery copies
scripts/film_run.py kyle_rescue status         # where every shot is
```

`--dry-run` prints every command; `--force` redoes existing outputs. `finish` caches each shot's upscale against a stamp of *take, trim, model, size, fit*, so changing one trim re-upscales only that shot (a no-change re-run takes < 1 s). A standalone run-spec file works in place of the project id: `film_run.py path/to/run-spec.json …`.

**Tested 2026-09-23**: validation paths (bad sizes, 8k+1/4k+1 frames, unknown upscaler, portrait letterbox, missing IN); text / edit / landscape stills; LTX 33 f at 1024×576 (104 s); **Wan 2.2 I2V via the CLI with the low-noise refiner + Lightning LoRA in `CONFIG_JSON`** (9 f at 512² in 57 s — first CLI Wan run); upscale with `realesr-animevideov3` at 2× to 1080p with audio kept, and x4plus padded into 2160×3840; assembly single-clip, music tail + fades, landscape letterbox + clip audio; a 2-shot landscape film end to end through `film_run.py` (text still → chained edit → 2 clips → QC → finish → 720p copy). `assemble_film.sh` defaults reproduce the previous script's mix exactly (same length, −35.9 dB mean, −20.9 dB peak on the same inputs); `finish_clip.sh` reproduces the old 27.375 s coast loop.

### `scripts/dt_clip.sh` — any I2V clip

Model family from the name sets the defaults — **ltx**: 249 f, 8 steps, TCD Trailing (19), shift 5, SSS 0.3, 25 fps, hi-res fix off; **wan**: 81 f, 4 steps, UniPC Trailing (17), shift 5, 16 fps, `refinerModel` = the low-noise expert at `refinerStart` 0.1, Lightning LoRA at 1.0. Env `MODEL STEPS CFG CONFIG_JSON VIDEO_FORMAT NEGATIVE FORCE DRY_RUN` override any of it. W/H default to the still's size. Prints size, frame count and wall time.

### `scripts/seed_sheet.sh` — one master → a turnaround sheet, or a LoRA dataset

```
scripts/seed_sheet.sh MASTER.png OUT_PREFIX [SUBJECT] [SEED]
VIEWS="34 side back"  STYLE="…"  W=512 H=768  scripts/seed_sheet.sh …
```

**Purpose**: a frontal master cannot tell the model what the back of a head looks like, so every shot from behind is an invention ([[identity-conditioning]]: reference tokens copy what they can see). This renders the missing angles from the master and composes them into one sheet.

**Steps**: for each view in `VIEWS`, build a prompt from a keep-clause (*exactly the same face, hair, colours and clothing, no change to the features or the age*) plus a rotation clause, run `dt_diptych.sh - MASTER prompt out.png` (klein edit at strength 1.0), then `hstack` front + views into `OUT_PREFIX_sheet.png`.

Built-in views: `34`, `side`, `back`. Anything else in `VIEWS` is passed through as a prompt sentence, which is how you get a top-down, a head close-up or a clawed foot for a creature. `SUBJECT` is the noun used in the prompts ("boy", "creature"); `STYLE` overrides the look clause for non-3D projects.

**Cost**: ~25 s per view. **Gotcha**: klein amplifies a signature feature a little with each edit — Kyle's spiked fringe is taller on the sheet than on the master — so judge the sheet against the master, not against the previous view.

#### `--dataset` — 30 training images and their captions

```
KEEP="exactly the same face … the same pointed ears …" \
scripts/seed_sheet.sh --dataset MASTER.png OUT_DIR [SUBJECT] [TRIGGER]
ONLY="1 10 25"  CELLS="…"  WD=512 HD=768  DRY_RUN=1
```

**Purpose**: experiment **B0** in [[blueprint-v2-research]] — build the dataset a character LoRA would need. 30 cells over framing × angle × lighting × expression × wardrobe × background, 12 close / 12 medium / 6 wide, one klein seed per cell, written as `ds_NN.png` + `ds_NN.txt`.

**The two strings.** Each cell writes a **prompt** that names every feature to preserve (our reference-token practice — klein substitutes its own face otherwise) and a **caption** that names only what varies. Permanent features are absent from the caption on purpose, so they bind to the trigger token rather than to words a later prompt can contradict — the Isolation Rule, which is the exact inverse of how we write shot prompts. Captioned axes (wardrobe, lighting, framing) stay steerable after training.

Set `KEEP` per character; the default keep-clause is generic and will drift. `ONLY` renders a numbered subset — render two or three cells first and look at them before spending the full run. Captions are written even under `DRY_RUN`, so the text is reviewable before any pixels exist.

**Cost**: ~25–40 s per image, ~20 min for 30. Captions are tracked in git; the images are not.


## `scripts/qc_sheet.sh` — contact sheet

`qc_sheet.sh CLIP OUT [REF|-] [N=5] [TILE_H=384]` — reference + N frames spread evenly from first to last (indices computed from the clip, so a 33-frame test and a 249-frame shot both work).

### `scripts/preflight.sh`

Blocking failures (exit 1): CLI, ffmpeg, Real-ESRGAN or a model missing, disk < 20 GB. Warnings: battery, disk < 50 GB, Draw Things app open, no caffeinate, another CLI or Real-ESRGAN job running. `--fix` quits the app and starts `caffeinate -dis -t 50400`.

---

## `scripts/finish_clip.sh` — 5 s I2V export → 27 s looping 9:16 post

```
scripts/finish_clip.sh projects/<id>/<version>/clips/NAME.mov [music.mp3] [outname]
```

**Purpose**: turn one 81-frame Wan 2.2 clip into a TikTok/Shorts-ready 1080×1920 loop with music (the living-painting projects: coast, Torrey Pines, Golden Gate, Rainier, cyberpunk, FLL farm).

**Steps**

1. `ffprobe` the height. If it is 1280 (Draw Things sometimes exports 576×1280), centre-crop to 576×1024 with `crop=576:1024:0:128`.
2. Conform to 16 fps, `setsar=1`, then **split the stream three ways** (`split=3`) so ffmpeg can read the same frames as body, tail and head without re-decoding:
   - `body` = frames 8 … 72 (`trim=start_frame=8:end_frame=73`)
   - `tail` = frames 73 … 80 (last 8)
   - `head` = frames 0 … 7 (first 8)
3. **Seamless loop seam**: `[tail][head]xfade=transition=fade:duration=0.5:offset=0` dissolves the last 8 frames into the first 8. Then `concat` body + seam → one 73-frame unit whose last frame flows into its first. This is a *forward-only* loop — no ping-pong, so waves never run backwards (the reason ping-pong was rejected on 2026-09-20).
4. `loop=loop=5:size=32767` repeats the unit 6× (≈27.4 s), `setpts=N/FRAME_RATE/TB` rebuilds timestamps, `scale=1080:1920:flags=lanczos` upsizes 1.875×.
5. Encode `libx264 -crf 18 yuv420p`, no audio → `NAME_loop.mp4`.
6. If a music file was given: `atrim` to the loop length, `afade in 1 s`, `afade out 2 s` (start computed in Python from the probed duration), `volume=0.9`, mux with `-c:v copy -c:a aac 192k -shortest` → `NAME_final.mp4`.

**Knobs at the top of the script**: `LOOPS=5` (units − 1), `FADE_FRAMES=8` (seam length; 0.5 s at 16 fps). Music comes from Pixabay CC0 via the CDN URL grabbed from the page's `<audio>` element (see [[projects]] records for the URLs).

**Since 2026-09-23 generic**: frame count, fps and size come from the input; the seam is `SEAM` seconds (default 0.5 → 8 frames at 16 fps, identical to before); output size `W`/`H` (default 1080×1920, `W=1920 H=1080` for a landscape post); `LOOPS`, `FPS`, `MUSIC_VOL` env. It refuses clips shorter than 3 seams.

---

## `scripts/upscale_4k.sh` — any clip → 3840×2160 HEVC 10-bit

**Env (2026-09-23)**: `W`/`H` output size (default 3840×2160; portrait `W=2160 H=3840`), `FIT=crop|pad`, `BITRATE` (40M; 12M for 1080p), `KEEP_AUDIO=1` (copies the input's audio — no `-shortest`, which dropped a frame), `KEEP_FRAMES=0` (delete the PNG folder), `SCALE` (x4plus is always 4×; `realesr-animevideov3` also runs at 2×/3×, or name `-x2`/`-x3` — a 1080p target needs only 2×). Validates the model/scale file and that frames out = frames in; Real-ESRGAN's progress spam goes to a log shown only on failure. `-t 128 -j 1:1:1` are both required on Metal (segfault without). Measured on 576×1024 LTX clips with x4plus: ~20 frames/min.

```
scripts/upscale_4k.sh projects/<id>/<version>/clips/NAME.mov [outname] [model]
```

**Purpose**: the step that makes "4K" true. Wan/LTX generate 576p–768p; this adds detail with a learned upscaler instead of a blurry resize. Used for Dragon Epic scene 1A and every Lost City clip.

**Steps**

1. `ffprobe` the frame rate (`r_frame_rate`, e.g. `16/1` or `25/1`) so the output keeps the source cadence.
2. Resolve absolute paths — Real-ESRGAN resolves its `models/` folder relative to **cwd**, so the script `cd`s into `tools/realesrgan` and needs absolute in/out paths.
3. **Frames out**: `ffmpeg -i IN SRC/%04d.png` — one PNG per frame (8-bit; the 16-bit variant crashed the ncnn build).
4. **Upscale the whole directory in one process** (model loads once):
   `./realesrgan-ncnn-vulkan -i SRC -o DST -n MODEL -f png -s 4 -t 128 -j 1:1:1`
   - `-s 4`: 4× (1280×768 → 5120×3072; 1024×576 → 4096×2304)
   - `-t 128`: tile size — **auto/256 segfaults on Metal**; 128 is the largest stable value
   - `-j 1:1:1`: load/proc/save threads; more than one GPU thread also crashed
   - models present: `realesrgan-x4plus` (default, photoreal), `realesrgan-x4plus-anime`, `realesr-animevideov3-x2/x3/x4` (faster, flat shading — good for the anime loops)
5. **Encode**: `ffmpeg -framerate FPS -i DST/%04d.png -vf "scale=3840:2160:force_original_aspect_ratio=increase:flags=lanczos,crop=3840:2160"` — scale so the shorter side fits, then centre-crop to exactly UHD (1280×768 is 5:3, so ~4% is cropped top/bottom). Codec `hevc_videotoolbox -profile:v main10 -pix_fmt p010le -b:v 40M -tag:v hvc1` = hardware HEVC, 10-bit, 40 Mbps, Apple/YouTube-friendly tag. **`-an`: audio is dropped** — for LTX clips mux it back:
   `ffmpeg -i NAME_4k.mp4 -i NAME.mov -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest NAME_4k_audio.mp4`
6. Deletes the source PNGs, keeps `NAME_4k_frames/` (the 4× PNGs) for re-encodes without re-upscaling, prints an `ffprobe` line of the result.

**Timing (M4 Max)**: 81 frames @ 1280×768 → 5.6–6.3 min; 97 frames @ 1024×576 → ~7 min. Frames folder ≈ 1–1.5 GB per clip — delete when the clip is final.

**Alternatives considered** ([[video-upscaling]]): SeedVR2 (temporal, better but needs ComfyUI + MPS memory at 4K unverified), Draw Things' built-in upscaler (images only), Topaz (paid). Real-ESRGAN per-frame can shimmer on fine texture; so far no shimmer on foliage (Lost City L5).

---

## `scripts/assemble_film.sh` — N clips → one 4K film with crossfades

**Env (2026-09-23)**: `W`/`H`, `FPS`, `XFADE`, `BITRATE`, `LETTERBOX` (landscape only, bars computed for any width), `CLIP_AUDIO=0` (music-only film), `CLIP_VOL` (0.5), `MUSIC`, `MUSIC_VOL` (0.3), `MUSIC_START` (seconds or `tail` = the last film-length of the track, so the film ends on the song's ending), `MUSIC_FADE_IN/OUT`. The mix is `amix normalize=0` with explicit levels; the 0.5/0.3 defaults equal what the old normalised mix produced, so older projects sound the same. A single clip is allowed. Prints expected vs actual length and the music start.

```
scripts/assemble_film.sh OUT.mp4 clip1.mp4 clip2.mp4 [...]
XFADE=0.5 FPS=25 MUSIC=bed.mp3 LETTERBOX=1  scripts/assemble_film.sh ...
```

**Purpose**: the edit. Written 2026-09-21 for Lost City (s2 → s1); the same script is planned for Dragon Epic's 12 shots.

**Steps**

1. For each clip: `ffprobe` duration and whether it has an audio stream.
2. Per-clip video filter: scale-and-crop to 3840×2160 (same expression as `upscale_4k.sh`, so mixed sizes are safe), `fps=FPS` to conform 16- and 25-fps clips, `format=yuv420p10le`, `setsar=1`; optional `drawbox` bars for 2.39:1.
3. Per-clip audio: real track → `aformat` 48 kHz stereo + `apad`; no track → `anullsrc` silence of the same duration. A uniform audio graph is required or `acrossfade` fails.
4. **Crossfade chain**: for clip *i*, `xfade=transition=fade:duration=XFADE:offset=` (running total of durations minus one XFADE per join) and `acrossfade=d=XFADE`. With `XFADE=0` it uses `concat` (hard cuts).
5. Optional music: `volume=0.6` then `amix` under the clip audio.
6. Encode: same HEVC 10-bit 40 Mbps + AAC 192k, `-movflags +faststart`.

**Gotcha (2026-09-22, fixed)**: the per-clip audio used a bare `apad`, which pads silence *forever*. At 576p it went unnoticed; with three 4K 10-bit inputs the graph buffered until ffmpeg died with `Cannot allocate memory` after 11 minutes of encoding. It is now `apad=whole_dur=${dur}`. A 30 s 4K assembly takes ~8 min on the M4 Max.

**Level**: `amix` halves the perceived level, so finish with an audio-only pass — `ffmpeg -i film.mp4 -af volume=6dB -c:v copy -c:a aac -b:a 192k out.mp4` took s15 from mean −24 dB to −18.1 dB, max −3.4 dB.

**Limits**: xfade offsets are computed in Python from probed durations, so clips must have accurate container durations (Draw Things ProRes exports do). Title cards and SFX are not in yet — add them as extra "clips" (a 2 s still rendered with `ffmpeg -loop 1`).

---

## `scripts/dt_diptych.sh` — reference-locked klein edit, released CLI

`scripts/dt_diptych.sh REF.png IN.png PROMPT.txt OUT.png [seed] [W] [H]` — puts REF left and IN right (each fitted to W×H, default 576×1024), runs FLUX.2 klein 9B at `--strength 1.0` (edit mode) on the 2W×H pair, keeps the right half. REF `-` = plain single-image edit. The prompt must say "Two images side by side … re-render the right image … looking exactly like the left … keep the left image unchanged" and name the framing. ~55–60 s per diptych. The CLI's substitute for Moodboard references — see [[headless-cli-pipeline]] §1c and [[kyle-antarctic-rescue-plan]] §0.

## `scripts/dt_project.sh` — Draw Things projects from the shell

```
scripts/dt_project.sh list | newest | rename OLD NEW | rename-newest NEW | delete NAME
```

A Draw Things project is one SQLite file: `~/Library/Containers/com.liuliu.draw-things/Data/Documents/NAME.sqlite3` (plus `-shm`/`-wal` while open). The project name **is** the filename, so `mv` renames it and the Projects list updates live — verified 2026-09-21 (`Untitled-66452` → `junk-66452` appeared without a restart). Rules: never touch the currently open project (its WAL is live) — switch to another project first; `delete` moves the three files to `~/.Trash`. This replaces the in-app Rename dialog, which background automation cannot see.

New-project flow: **+** in Projects (creates and opens `Untitled-NNNNN`) → click any other project → `scripts/dt_project.sh rename-newest lostcity-s3` → click the renamed row.

## Where files live

Since 2026-09-25 every project owns one folder and every attempt a version inside it: `projects/<id>/<version>/` with `raw/ seed/ stills/ clips/ music/ final/ logs/`, and the plan at `projects/<id>/plan/`. Prompts are text inside `spec.json`; `film_run.py` writes them to `<version>/.gen/*.txt` at run time. Candidate renders and QC sheets go to `seed/`, picked frames to `stills/`, everything shot-scoped to `clips/`, the film to `final/`. Scripts take paths as arguments and `film_run.py` resolves everything relative to `run-spec.dir` (`projects/<id>`), so the reorganisation needed no changes to the shell scripts — only `build_site.py`, which now collects pages from `wiki/*.md` **and** `projects/*/plan/*.md` so a project's page is published with the rest of the wiki and `[[wiki-links]]` resolve from either place.

## Site and registry scripts

| Script | What it does |
|---|---|
| `scripts/build_projects.py` | every `projects/*/*/spec.json` + `projects/_shared.json` → the registry pages, and rewrites the root `projects.json` as an aggregate. Fills each record from `defaults`, writes the summary table (with ▶ YouTube links) and one section per project, embeds the playlist and per-project YouTube iframes; orientation (16:9 vs 9:16) is inferred from the I2V size. Run by `build_site.py`. |
| `scripts/build_site.py` | `wiki/*.md` → `docs/` static site with the `markdown` package: rewrites `[[wiki-links]]` to `.html`, copies `wiki/assets/`, generates the landing page cards from `wiki/index.md`. Run after any wiki edit; `./serve.sh` builds and serves on :8788. |
| `scripts/render_infographic.sh NAME` | headless Chrome screenshot of `scripts/infographics/NAME.html` at 2× → `cwebp` → `wiki/assets/NAME-3d.webp`. |

---

## End-to-end, per project type

```
living painting (9:16)   DT export .mov ─► finish_clip.sh (+music) ─► NAME_final.mp4 ─► YouTube
cinematic shot (16:9)    DT export .mov ─► upscale_4k.sh ─► NAME_4k.mp4 (+ audio remux for LTX)
film                     N × NAME_4k.mp4 ─► assemble_film.sh (XFADE, MUSIC) ─► film.mp4 ─► YouTube
```

Every run should end with an `ffprobe` check (size, frame count, fps, audio) and a line in [[log]] with the timing.

## Related pages
- [[runbook-living-painting]] — the Draw Things side, click by click
- [[video-upscaling]] — why Real-ESRGAN, what else exists
- [[lost-city-plan]] · [[dragon-epic-plan]] — where these scripts are used
- [[projects]] — per-project files and settings
