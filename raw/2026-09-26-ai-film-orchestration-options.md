# Orchestration options for an AI film pipeline

*Pasted by Kevin on 2026-09-26. Origin unattributed. Repo names verified on 2026-09-26; capability claims are the source's own and are not independently tested.*

Several powerful Claude Skills, open-source orchestrators, and framework extensions automate and execute these steps.

Option 1: Claude Code Skills & Agents

1. Claude Film Pipeline Skill (Theoretically Media / Claude Cowork)
* Converts raw narrative scripts directly into scene-by-scene shot lists. Formats text prompts with negative safety filters, embeds tag bindings (`@Face1`, `@Body1`, `@Environment`), and outputs API payloads or JSON keyframes ready for video models.

2. Local ComfyUI & Kohya API Skills
* Dataset & Captioning: Python script where Claude uses a vision model (Qwen-VL, Gemini Flash) to caption 30 character images with a trigger token (`sks_alex_man`).
* Triggering LoRA Training: fire training jobs via CLI using `musubi-tuner` or `kohya_ss`, reading training loss logs in the terminal.
* ComfyUI API Execution: send JSON payloads to http://127.0.0.1:8188/prompt to auto-queue shot-by-shot runs in Wan 2.2 or LTX-2.5.

Option 2: Open-Source Autonomous Video Orchestrators

1. OpenX Flow (`OpenX-Inc/flow`) — fully local / cloud-mixed pipelines. Takes a topic, writes scene descriptions, triggers Wan 2.2 (local or serverless GPUs like Modal/RunPod), uses last-frame/first-frame conditioning for shot-to-shot coherence, stitches clips with narration and subtitles.
2. OpenMontage (`calesthio/OpenMontage`) — agentic multi-tool production. Integrates AI coding assistants (Claude Code, Cursor) with video tools; manages character stills, orchestrates I2V models, aligns audio, uses Remotion or FFmpeg to assemble cuts with transitions and music.
3. Director (`juspay/director`) — autonomous QC and multi-scene filmmaking. TypeScript framework; breaks scripts into shot plans, evaluates keyframes for character/brand consistency before animating, generates across multiple API adapters, runs self-critique cycles before mastering.

Recommended Hybrid Setup

```
1. Scripting & Visual Prompts  ► Claude Code / Film Skill
2. Captioning & Dataset Prep   ► Python + Vision LLM Script
3. LoRA Training (Local)       ► Musubi-Tuner / Kohya_ss
4. Shot Generation & Motion    ► OpenX Flow / ComfyUI API
5. Assembly & Upscaling        ► OpenMontage / FFmpeg / NLE
```

1. Use Claude Code to turn the story into a structured `shots.json` manifest.
2. Run LoRA training locally (Steps 2 & 3) using Kohya/Musubi-Tuner to lock character weights.
3. Pass `shots.json` and the `.safetensors` LoRA to OpenX Flow or OpenMontage to render, stitch, score and upscale the sequence autonomously.
