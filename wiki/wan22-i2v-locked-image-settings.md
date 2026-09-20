# Wan 2.2 I2V — Animate a Photo Without Changing It

**Summary**: Draw Things settings that keep the source photo as the literal first frame and let the prompt drive only motion. The "my photo, but moving" recipe.

**Sources**: 2026-09-19-local-4k-video-research.md (Draw Things wiki, LightX2V settings article). Timings on M4 Max still unmeasured.

**Last updated**: 2026-09-19

---

## Principle

Wan 2.2 **I2V** conditions every generated frame on the input image; **T2V** (and Draw Things' T2V/I2V slider at 100% T2V) treats the image as a loose reference. Draw Things has no "keep image" toggle — the lock comes from three things: the I2V model, Strength 100%, and a prompt that never describes the subject.

## Settings

| Setting | Value | Why |
|---|---|---|
| Model | **Wan 2.2 I2V 14B** — High Noise Expert + Low Noise Expert pair (6-bit SVDQuant) | Only the I2V checkpoint anchors to the image. TI2V-5B works but drifts more. |
| Canvas | Match photo aspect, e.g. 1280×720 or 960×544 for tests | Photo must cover 100% of canvas; uncovered pixels get inpainted with invented content. |
| Image | Drag photo onto **Canvas** (not Moodboard) | Moodboard is style reference, not first-frame conditioning. |
| Strength | **100%** | Below 100% the first frame is partially repainted. |
| Frames | 25 to test, then **81** (5 s @ 16 fps) | Drift compounds with length; shorter = more faithful. |
| LoRA | LightX2V Wan 2.2 I2V distill, weight 1.0 (try 1.5 if motion is dead) | 4 steps instead of 20–30. Mandatory on Mac. |
| Steps | **4** with LoRA (2 high + 2 low); 20 without | |
| Guidance (CFG) | **1** with LoRA; 3.5–5 without | Distilled LoRAs break above ~1.5. |
| Shift | **5** | Community default for LightX2V. |
| Seed | fixed integer | Same seed + prompt = reproducible; change only the prompt when iterating. |
| TeaCache / Tiled Decode | on | Memory safety on first runs. |

## Prompting

Describe **camera and motion only**. Never describe the subject, clothing, or setting — the model may re-imagine what it is told about.

Good:
- `slow push in, camera dolly forward, subject still, gentle wind in hair`
- `static camera, subject turns head slightly and smiles`
- `slow pan left, leaves moving softly, subtle motion, minimal movement`

Bad:
- `a woman in a red dress on a beach` — invites re-generation of the woman

Negative prompt: `morphing, deformed face, extra fingers, flicker, text, watermark`

## If the result drifts from the photo

1. Add `subtle motion, minimal movement` — less motion, less drift.
2. Cut Frames to 49.
3. Confirm the model name in Manage contains **I2V**; the T2V-A14B pair accepts an image but does not anchor to it.
4. Check the T2V/I2V slider if the model shows one — push it toward I2V.
5. Lower LoRA weight to 0.8; distill LoRAs can add motion at the expense of fidelity.

## Next step after a good clip

Export MP4 → [[video-upscaling]] → [[frame-interpolation]] → [[ffmpeg-pipeline]]. Record the wall time on [[local-open-source-4k-video-pipeline]].

## Related pages
- [[draw-things-setup]]
- [[face-identity-workflows]]
- [[image-to-video-models]]
- [[local-open-source-4k-video-pipeline]]
