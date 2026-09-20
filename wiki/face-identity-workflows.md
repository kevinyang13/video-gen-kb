# Face Identity Workflows — Your Face in a Generated Scene

**Summary**: Four ways to generate a video from a text prompt while keeping a specific real face, ranked for the Mac Studio + Draw Things setup. Wan 2.2 I2V alone cannot do this; it anchors to a whole image, not a face.

**Sources**: 2026-09-19-local-4k-video-research.md for model facts; workflow details are general knowledge and *need verification* in the app.

**Last updated**: 2026-09-19

---

## Why plain I2V fails here

I2V locks the entire first frame. To put a face into a *new* scene you need either a first frame that already contains the face, a model that takes a separate identity reference, or a post-process swap.

## A. Two-stage: still with face → I2V (recommended, all in Draw Things)

**Stage 1 — make the first frame**
- Model: an image model (Flux.1 dev or SDXL) in Draw Things.
- Face control: **IP-Adapter FaceID** or **PuLID** style adapter — Draw Things exposes these under Controls for image models; confirm exact name in-app *(needs verification)*.
- Reference: one sharp, frontal, evenly lit photo of the face. Strength 0.7–0.9.
- Canvas 1280×720. Prompt describes **scene, lighting, wardrobe, camera** — not the face; the adapter supplies the face.
- Iterate seeds until identity reads correctly. Export PNG.

**Stage 2 — animate**
- Follow [[wan22-i2v-locked-image-settings]] exactly: Wan 2.2 I2V, Strength 100%, motion-only prompt, 81 frames.

Pros: no new installs, deterministic. Cons: face can soften over long clips; keep motion subtle, keep clips ≤ 5 s.

## B. Reference-to-video models (identity as a separate input)

Models that take a subject reference image plus a text prompt and hold identity across the shot:

- **Wan 2.1 VACE** — open weights, unified edit/reference framework; ComfyUI workflows are common. Draw Things support: check Manage for "VACE" *(needs verification)*.
- **Phantom** (Wan-based subject-to-video) — open weights; ComfyUI *(needs verification)*.
- Closed: **Seedance 2.0** (up to 9 image refs), **Kling Elements**, **Veo Ingredients** — strongest results, cloud only, per-clip cost via fal.ai / OpenArt. See [[video-generation-landscape]].

Pros: real T2V freedom with identity. Cons: open options need ComfyUI-on-MPS (slow) or cloud.

## C. Post-process face swap

Generate any T2V clip (Wan 2.2 T2V, any prompt), then swap the face per frame.

- **FaceFusion** — open source, runs on Apple Silicon via CoreML/ONNX providers *(needs verification of current Mac build)*. Input: clip + one face photo. Output: swapped clip. Has face enhancer pass built in.
- Older equivalents: roop, ReActor (ComfyUI node).

Pros: most reliable identity, works on any clip. Cons: "pasted" look on profile angles and occlusion; run before [[video-upscaling]] so the upscaler smooths the seam.

## D. Train a face LoRA for Wan 2.2

- 15–30 varied photos, captioned with a trigger word.
- Train on cloud (fal.ai Wan 2.2 LoRA trainer, Replicate) — roughly 1–2 h *(needs verification)*; local Mac training not practical.
- Import the LoRA in Draw Things (Manage → Import → LoRA), use trigger word in any T2V or I2V prompt.

Pros: best fidelity and full freedom, reusable forever. Cons: most effort, cloud cost, tuning.

## Decision

| Need | Pick |
|---|---|
| Try tonight, no installs | **A** |
| A drifts on faces | **A + C** (swap after) |
| Many clips of the same person over months | **D** |
| Best possible single clip, budget OK | Seedance 2.0 via fal.ai (**B**, closed) |

## Ethics note

Own face or explicit consent only. Same tools swap anyone's face; keep it to yourself and family who agree.

## Related pages
- [[wan22-i2v-locked-image-settings]]
- [[draw-things-setup]]
- [[image-to-video-models]]
- [[video-generation-landscape]]
- [[video-upscaling]]
