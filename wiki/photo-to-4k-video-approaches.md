# Photo to 4K Video — Approaches

**Summary**: Four candidate pipelines for turning still photos into 4K video, with trade-offs. Starting point for choosing a workflow.

**Sources**: Brainstorm in chat, 2026-09-19. No raw sources yet — claims about specific model output resolutions need verification.

**Last updated**: 2026-09-19

---

## 1. Ken Burns (ffmpeg `zoompan`)

Pan/zoom over stills, crossfade between them, add music. Deterministic and free. Native 4K if source photos are at least 3840×2160; roughly 6000px wide gives headroom for zoom. Renders in minutes. Visually plain.

See [[ffmpeg-pipeline]].

## 2. AI image-to-video

Feed a photo to an image-to-video model and get a 5–10s motion clip. Candidates as of 2026-09-19: Kling 2.x, Runway Gen-4, Veo 3, Luma, Wan 2.x (local). Output is mostly 1080p, so a [[video-upscaling]] step (Topaz Video AI, SeedVR, Real-ESRGAN) is needed to reach 4K. Costs per clip; may hallucinate details, especially faces. Highest "wow" factor.

See [[image-to-video-models]].

## 3. Depth parallax (2.5D)

Estimate a depth map (Depth Anything v3), then move a virtual camera through the layered image (Blender, After Effects, Immersity AI). Photo pixels stay exact — no hallucination — but gain dimensional motion. Native 4K.

See [[depth-parallax]].

## 4. Hybrid pipeline

AI clip per photo → frame interpolation (RIFE, 24→60fps) → 4K upscale → ffmpeg stitch with transitions and audio. Best result, most steps. Good candidate for a scripted pipeline.

See [[ffmpeg-pipeline]], [[frame-interpolation]], [[video-upscaling]].

## Open questions

- Source photo resolution and count?
- Style target: slideshow, cinematic motion, or faces that must stay exact?
- Local GPU available, or cloud API budget?

## Related pages
- [[image-to-video-models]]
- [[video-upscaling]]
- [[frame-interpolation]]
- [[depth-parallax]]
- [[ffmpeg-pipeline]]
