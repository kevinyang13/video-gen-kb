# Index

**Summary**: Table of contents for the video generation knowledge base.

**Sources**: n/a

**Last updated**: 2026-09-23

---

## Overviews

- [[photo-to-4k-video-approaches]] — four candidate pipelines (Ken Burns, AI image-to-video, depth parallax, hybrid) with trade-offs and open questions
- [[local-open-source-4k-video-pipeline]] — the recommended all-local recipe on the M4 Max: I2V at 720p/1080p → upscale → interpolate → ffmpeg; runtime and model rankings, time budget, open questions

## Models & tools

- [[video-generation-landscape]] — the whole map: open and closed models, harnesses, apps, websites, launch dates, popularity; where this project sits

- [[image-to-video-models]] — Wan 2.2, LTX-2.5/2.3, HunyuanVideo 1.5, SkyReels: size, license, native output, Mac status
- [[video-upscaling]] — SeedVR2, FlashVSR, Real-ESRGAN; temporal vs per-frame; Mac support
- [[draw-things-setup]] — downloading Wan 2.1/2.2, LTX-2.3, Hunyuan, SkyReels inside Draw Things; LightX2V 4-step settings; I2V step-by-step; disk budget
- [[apple-silicon-inference]] — FP8 trap, MPS slowness, Draw Things and MLX runtimes, 48 GB memory planning
- [[headless-cli-pipeline]] — running the whole pipeline without a UI: `draw-things-cli` (klein strength 1.0 = edit mode, diptych as Moodboard substitute, `--frames` video, config JSON), gRPCServerCLI, and why ComfyUI/MLX can't replace it on a Mac

## Projects

- [[projects]] — index of every video, grouped by theme; generated from `projects.json`
- [[projects-anime]] — Shinkai/Ghibli living-painting loops: coast, Torrey Pines, Golden Gate, Rainier, cyberpunk, FLL farm
- [[projects-realistic]] — photoreal shorts: Dragon Epic, Lost City, the three-minute film
- [[projects-3d]] — 3D-animated shorts: Kyle's Antarctic Rescue

## Plans

- [[dragon-epic-plan]] — 1-minute photoreal dragon short with a personal face: pipeline, Draw Things config per stage, face-identity and dragon-consistency strategy, 12-shot list, experiments, budget
- [[lost-city-plan]] — hyper-real sci-fantasy rider entering jungle ruins (OpenArt-style reference): what makes it look real, klein Moodboard stills, Wan 2.2 vs LTX-2.3 motion settings, creature/hero/city locks, 8-shot list, experiments L0–L6
- [[lindsey-art-plan]] — 1-minute vertical 3D-animated short from Lindsey's 5-panel art comic (drawing → practice → style → exhibition → brighter future); first run fully through `film_run.py`
- [[kyle-antarctic-rescue-plan]] — **delivered**: 1-minute vertical 3D-animated short from Kyle's 2D comic, rendered unattended overnight with `draw-things-cli` — klein edit-mode masters, diptych identity lock, LTX-2.3, every pick and rejection
- [[three-minute-film-plan]] — 3-minute narrative film (36–40 × 5 s clips) with recurring characters: structure, consistency stack, per-shot workflow, 7 gating experiments, ~23 h budget, open questions

## Recipes

- [[idea-to-video-blueprint]] — **start here for a new film**: idea → intake questionnaire → storyboard approval → unattended CLI run (masters, diptych stills, LTX batch, QC/redo, upscale, music, report); rules, rubric, time budget, failure playbook
- [[scripts-reference]] — every pipeline script by production phase, the run-spec that drives them, `film_run.py` (check/stills/pick/clips/qc/finish), options, validation, tests, timings
- [[runbook-living-painting]] — **start here next time**: click-by-click checklist, settings to verify after every model switch, failure signatures, `scripts/finish_clip.sh`
- [[living-painting-loop]] — TikTok-style animated painting: Wan 2.2 T2V still → I2V ambient motion → ffmpeg ping-pong loop; exact Draw Things settings and UI gotchas
- [[wan22-i2v-locked-image-settings]] — Draw Things settings to animate a photo while keeping it as the literal first frame; motion-only prompting
- [[character-consistency]] — keeping one character the same across many shots: text lock, Moodboard-referenced stills (FLUX.2 klein / Qwen Image Edit), LoRAs (local training broken on Apple Silicon, cloud ~$1), reference-to-video models, staging tricks; decision table
- [[face-identity-workflows]] — four ways to put a specific face into a prompt-generated video: two-stage still→I2V, reference-to-video models, FaceFusion swap, face LoRA

## Concepts

- [[identity-conditioning]] — why a character can stay the same: text embeddings vs reference-image tokens vs adapters vs LoRA weights vs first-frame latent; the mechanism behind every consistency tool

_(stubs referenced but not yet written: frame-interpolation, depth-parallax, ffmpeg-pipeline)_

## Log

- [[log]] — append-only record of all operations
