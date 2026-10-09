# Keeping a Subject Consistent Through Image-to-Video

**Summary**: The clip model sees only the still, so anything the motion reveals that the still does not contain gets invented — and invention is where identity dies. Six rules ranked by how much they actually bought, then a measured comparison of LTX-2.3 and Wan 2.2 on camera obedience and render cost. Wan is not a better model; it is better at one thing, and it costs 3.4–5.4× more per second of footage.

**Sources**: measured on this machine during `kyle_firstflight` v2/v3, `lindsey_orbit` v1/v2 and `tide` v1, 2026-10-07/09; render times from the projects' own logs. Refines the one-line verdict in [[image-to-video-models]] §Wan vs LTX, which is correct on speed and silent on camera obedience.

**Last updated**: 2026-10-09

---

## The principle everything follows from

**The clip model sees only the still.** Not the master sheet, not the turnaround, not the other shots. Whatever the motion brings into view that the still never showed has to be invented, and the invention is unconstrained.

That single fact explains every i2v failure recorded here, and it is why the rules below are all variations on *do not ask to see what is not there*.

## Six rules, ranked by what they bought

### 1. Never move the camera to a viewpoint the still does not contain

The biggest lever, and the only one measured in both directions on the same shot.

`kyle_firstflight` s7's video prompt opened **"The camera holds below the falling craft"** while its still was a locked side view. Over 249 frames the hull turned into a circular wheeled machine with two large lenses, and the boy disappeared. The same still with the camera locked off — *"the camera stays exactly where it is, locked off at the side, and does not move, orbit or change angle at any point"* — held for the full 249 frames.

When a move is unavoidable, keep it on the side the still already shows: a push in, a slow rise, a lateral drift. `tide` s3 drifts forward over water and holds; every other shot in that film is locked.

### 2. If the camera must arc, turn the subject with it

An orbit is the maximal version of rule 1 — it reveals every side. The mitigation is to keep the known side facing the lens: *"she turns slowly in place to follow the camera, so her face stays turned up toward the lens for the whole shot."* That is what made `lindsey_orbit` v1 work.

Where the shot needs the subject in profile looking away (`lindsey_orbit` v2-cliff), the arc must stay **in front** of them rather than circling round, because there is no turn available to hide the back of the head.

### 3. Describe camera and motion only — never the subject or the setting

This is Wan's documented rule ([[wan22-i2v-locked-image-settings]] §Prompting) and it generalises. Naming a thing invites the model to re-imagine it.

The LTX orbit prompt that failed described her dress, the meadow, the light and her expression. The Wan prompt that worked is three sentences of pure camera movement. Same still.

### 4. Give secondary subjects nothing to do

A secondary subject with the only active business in the shot gets promoted to the subject. `kyle_firstflight` s7 gave the droid *"its domed head spun hard around to the open engine panel with its amber lens blazing and status lights flashing red along its flank"* — the droid grew to pilot size and replaced the boy, and its red lights were painted across the hull. Made passive, it stayed a prop.

### 5. Hold expressions; do not change them

A held expression survives a full clip. A changing one drifts: `lindsey_sparky` s7's laugh aged her into a young woman, and the fix was to hold the smile rather than arrive at it. See [[still-geometry-and-review]] §8 for the controlled pair.

### 6. Keep clips short and cut

Drift compounds with length. Five seconds is materially safer than ten. Prefer more shots over longer takes, and re-anchor to a fresh still at the cut.

## LTX-2.3 vs Wan 2.2: measured

Both were given the same still of a girl in a meadow and a prompt asking for a locked-distance drone orbit. Subject size was measured as the fraction of frame occupied by her white dress, sampled across the clip.

| | LTX-2.3 distilled 1.1 | Wan 2.2 I2V 14B |
|---|---|---|
| Locked-distance orbit | **Failed.** 3.40 → 0.49 % — a **6.9×** shrink, on two different prompts | **Held.** 3.67 → 2.32 % — a **1.6×** change |
| Locked camera | Fine. Held every locked shot in `kyle_firstflight` v3 | Fine. Held all six `tide` shots |
| Render per 1 s of output | **~60 s** | **~205 s** at 81 frames; **~326 s** at 161 |
| Native clip | 249 frames @ 25 fps = 9.96 s | 81 frames @ 16 fps = 5.06 s |

Raw figures from the logs: LTX 249 frames in 592–638 s; Wan 81 frames in 1026–1119 s; Wan 161 frames in 3276 s. Note that Wan scales **worse than linearly** — doubling the frame count cost 3.2× the time, so a 10 s Wan clip is 5.4× the cost of a 10 s LTX clip.

### The decision rule

- **The camera moves → Wan.** LTX will not obey a distance or height constraint; it adds a pull-back regardless of prompting. Two attempts with completely different wording produced the same 6.9× recession, which makes it model behaviour rather than a prompt bug.
- **The camera is locked → LTX.** It held every locked shot tested, at roughly a fifth of the cost. `tide` used Wan throughout only because the project called for it; five of its six shots are locked and LTX would have produced them in a fifth of the time.

**Wan is not simply better.** It is better at one thing — honouring camera instructions — and pays for it with 3.4–5.4× the render time and half the native clip length.

## The limit of all of this

Every rule above is damage limitation inside a method that conditions on a single image. They reduce how often the model has to invent; they cannot stop it inventing when it does.

The structural fix is to condition the video on the subject rather than infer it from one frame. **Wan's VACE mode** takes reference images plus an optional control video, and is the only system whose documentation explicitly names *objects* rather than faces ([[consistency-by-control]] §8). No Apple Silicon benchmark for it exists anywhere, which makes it a genuine unknown and the single highest-value experiment still outstanding here.

## Related pages
- [[shot-locks]] — the reusable locks library, including the still-side version of rule 1
- [[consistency-by-control]] — why consistency comes from constraining rather than sampling; the VACE and ControlNet options
- [[wan22-i2v-locked-image-settings]] — the Wan settings these runs used, and the camera-and-motion-only prompting rule
- [[image-to-video-models]] — model catalogue; this page refines its Wan vs LTX one-liner
- [[still-geometry-and-review]] — §8 on held vs changing expressions, §11 on faces the motion may reveal
