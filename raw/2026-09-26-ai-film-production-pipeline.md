# Step-by-Step AI Film Production Pipeline

*Pasted by Kevin on 2026-09-26. Origin unattributed — treat as a general industry-practice summary, not a verified source. Verbatim below.*

Step 1: Pre-Production (Script & Shot List)

* Write & Structure: Generate your narrative, breakdown scenes, and build a formal shot list (defining shot types: Close-Up, Medium, Wide, Tracking).
* Define Key Assets: Identify recurring characters, unique costumes, and key locations that require visual consistency.

Step 2: Character & Concept Asset Generation

* Generate Character Turnarounds: Use an image generator (like FLUX or Midjourney) to create 25–40 images of your character across varied angles, lighting, and expressions against neutral backgrounds.
* Generate Environment Anchor Images: Create baseline concept art for primary locations to establish color palettes and architectural style.

Step 3: Model Fine-Tuning (Train LoRA)

* Process Dataset: Crop images to standard resolutions, clean backgrounds, and draft precise text captions with a unique trigger word (e.g., `sks_alex_man`).
* Train & Validate: Train a character LoRA on your dataset (1,500–3,000 steps). Test in ComfyUI across extreme angles to verify identity locking before moving to production.

Step 4: Storyboard & Shot Image Generation (Frame 0 Anchors)

* Generate Still Anchors: Using your custom LoRA, generate a still image for each shot on your shot list.
* Select First Frames: Pick the best still image for each scene cut. These serve as visual anchors for your video models.

Step 5: Shot-by-Shot Video Generation

* Animate Frames: Feed your still anchor images and character LoRA into your video diffusion engine (Wan 2.2 / LTX / Seedance).
* Inject Motion & Poses: Use ControlNet (OpenPose/Depth maps) for complex actions or dynamic camera pans. Generate multiple iterations per shot to catch natural motion.

Step 6: Editing, Audio Design & Dialogue

* Assembly Cut: Import generated video clips into a non-linear editor (NLE) like DaVinci Resolve or Premiere Pro, trimming shots to match pacing.
* Generate Voiceovers & Lip-Sync: Produce dialogue tracks via TTS (ElevenLabs) and align character lip movement using lip-sync models.
* Sound Design & Score: Add background music (Foley, ambient noise, sound effects) and sound design across scene transitions.

Step 7: Post-Processing, Color & Upscaling

* Video Upscaling & Frame Interpolation: Pass low-resolution video renders through a specialized video upscaler (like Topaz Video AI or local Real-CUGAN/ComfyUI upscaling workflows) to achieve clean 4K output at 24/30 FPS.
* Color Grading: Apply a unified LUT or color grade to match contrast, grain, and lighting across all disparate shots.

Step 8: Mastering & Final Export

* Final QC: Perform a master pass to check audio levels, frame sync, and continuity errors.
* Export: Render the final short film in high-bitrate ProRes or H.264/H.265.
