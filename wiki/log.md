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
