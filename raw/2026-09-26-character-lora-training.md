# Deep-Dive: Training a Custom Character LoRA

*Pasted by Kevin on 2026-09-26. Origin unattributed; hyperparameters are the source's own and are not independently verified.*

Training a LoRA is the ultimate approach for maintaining character identity across 10+ disparate shots and camera angles.

Dataset Curation (25–50 Images)
* Distribution: 40% Close-ups (varied angles/expressions), 40% Medium shots (waist-up), 20% Wide/Full-body shots.
* Lighting: Include diverse environments to prevent the LoRA from locking a specific lighting style.

Captioning Strategy
1. Assign a unique trigger token (e.g., `sks_alex_man`).
2. The Isolation Rule: Caption the background, camera angle, wardrobe, and lighting, but do not caption permanent facial features.
3. Example Caption: `A close-up photo of sks_alex_man smiling in a sunlit park, wearing a black leather jacket, soft bokeh background.`

Training Hyperparameters (Musubi-Tuner / Kohya_ss / AI-Toolkit)
* Network Rank / Alpha: Rank `32` or `64` | Alpha `16` or `32`
* Learning Rate: `1e-4` to `2e-4` (AdamW / Prodigy)
* Precision: `bf16`
* Target Steps: `1,500` – `3,000` steps
