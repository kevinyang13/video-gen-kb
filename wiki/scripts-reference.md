# Scripts Reference

**Summary**: What each script in `scripts/` does, which tools and APIs it calls, and the exact processing steps — so the post-production side of the pipeline (Draw Things export → looped/upscaled/assembled deliverable) is reproducible without re-reading the code. Covers `finish_clip.sh`, `upscale_4k.sh`, `assemble_film.sh`, plus the site/registry builders.

**Sources**: the scripts themselves (`scripts/*.sh`, `scripts/*.py`); hands-on timings in [[log]] 2026-09-20/21; Real-ESRGAN ncnn README (`tools/realesrgan/README_macos.md`).

**Last updated**: 2026-09-22

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

## `scripts/finish_clip.sh` — 5 s I2V export → 27 s looping 9:16 post

```
scripts/finish_clip.sh raw/clips/NAME.mov [music.mp3] [outname]
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

**Gotchas**: expects exactly 81 frames — a 25-frame test export produces a 1-second "loop". Portrait only; for 16:9 use `assemble_film.sh` instead.

---

## `scripts/upscale_4k.sh` — any clip → 3840×2160 HEVC 10-bit

**Portrait (2026-09-23)**: `W=2160 H=3840 scripts/upscale_4k.sh …` — output size is now `W`/`H` env (default 3840×2160). Without it a 9:16 clip gets cropped to a landscape strip. Measured on 576×1024 LTX clips with x4plus: ~20 frames/min (6.8–11.1 min per 6–10 s clip).

```
scripts/upscale_4k.sh raw/clips/NAME.mov [outname] [model]
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

**Portrait (2026-09-23)**: same `W`/`H` env (`W=2160 H=3840`); `LETTERBOX` stays landscape-only. For a music-only film, assemble without `MUSIC` (mute clips get silence) and mux a pre-cut bed afterwards — `MUSIC` goes through `amix`, which halves its level.

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

## Site and registry scripts

| Script | What it does |
|---|---|
| `scripts/build_projects.py` | `projects.json` → `wiki/projects.md`. Fills each record from `defaults`, writes the summary table (with ▶ YouTube links) and one section per project, embeds the playlist and per-project YouTube iframes; orientation (16:9 vs 9:16) is inferred from the I2V size. Run by `build_site.py`. |
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
