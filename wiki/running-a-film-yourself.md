# Running a Film Yourself

**Summary**: The seven commands that take a film from `spec.json` to a 4K master with no LLM in the loop, what you have to judge between them, and the four traps that fail silently.

**Sources**: measured on this machine across `lindsey_summit`, `kyle_steamfield` and `lindsey_sparky`, 2026-10-01 to 2026-10-04.

**Last updated**: 2026-10-04

---

## What actually needs a human, and what does not

Nothing in the render path needs an LLM. `scripts/film_run.py` reads a project's `spec.json` and shells
out to `draw-things-cli`, Real-ESRGAN and ffmpeg. Three things need judgement:

1. **Writing the prompts** in `spec.json`.
2. **Picking one still per shot** from five candidates.
3. **Deciding where each clip stops** being usable.

Everything else is `film_run.py PROJECT <phase>`, and every phase is resumable — it skips outputs that
already exist, so an interrupted run is restarted by running the same command again. `--force` redoes
work, `--dry-run` prints the commands without running them.

## Before anything

```bash
cd ~/dev/video-gen-kb && ls "/Volumes/KExtreme SSD/DrawThingsModels" >/dev/null && scripts/preflight.sh --fix
```

The external drive must be mounted; see [[model-storage-locations]]. `--fix` quits the Draw Things app,
which holds GPU memory and roughly halves CLI speed, and starts `caffeinate` for 14 h.

## The seven commands

```bash
python3 scripts/film_run.py PROJECT check     # paths, sizes, frame rules, planned length
python3 scripts/film_run.py PROJECT stills    # 5 candidates per shot -> seed/<id>_c<seed>.png
python3 scripts/film_run.py PROJECT sheet     # labelled contact sheet -> seed/<id>_sheet.png
python3 scripts/film_run.py PROJECT pick s1 4 # candidate -> stills/s1.png   (once per shot)
python3 scripts/film_run.py PROJECT clips     # 249-frame takes -> clips/<id>_v1.mov
python3 scripts/film_run.py PROJECT qc        # reference + 6 frames -> seed/<id>_v1_qc.png
python3 scripts/film_run.py PROJECT finish    # trim -> 4K upscale -> crossfade + music -> final/
```

`PROJECT` is the folder name under `projects/`, or `<id>@<version>` to target an older version.
`status` prints one line per shot at any time.

Put `caffeinate -dimsu` in front of `stills`, `clips` and `finish`, and run them from a terminal you
leave open. A render launched from an agent's shell does not survive; see [[log]] 2026-10-03.

## The three judgement calls

**Prompts.** `projects/<id>/<version>/spec.json`. Copy a delivered film's spec and replace the text —
`projects/lindsey_sparky` is the most current. `scenes.locks` holds the subject, wardrobe, room and style
paragraphs that get pasted into every shot, so each is written once. Read
[[still-geometry-and-review]] before writing shot prompts; it is the accumulated list of what breaks.

**Picking stills.** `seed/<id>_sheet.png` tiles five candidates and captions each with its seed number,
so you pick by number rather than position. **Open the shortlist at full size before deciding** — the
failures that matter (a sixth finger, a second person, structure that does not resolve) are invisible at
tile size. Then `pick <id> <seed>`.

**Trimming clips.** `seed/<id>_v1_qc.png` shows the reference plus six frames across the take. Find where
it stops being usable and write `trim` into the shot. Faces drift, props appear, people stand up. Then
run `finish`.

## Measured timings

M4 Max 48 GB, 8 shots, 1024×576 stills and 249-frame clips, models on the external SSD:

| phase | what | time |
|---|---|---|
| masters | 4 reference images | 2 min |
| `stills` | 40 candidates | **21 min** |
| `clips` | 8 × 249 frames | **80 min** (~10 min each) |
| `finish` | trim, 4K upscale, assemble, 1080p copy | **75 min** |
| | | **~3 h** plus review |

Add 10 minutes per clip you re-render. `lindsey_sparky` needed four second takes and one third take,
which is normal rather than unlucky — budget for it.

## The four traps that fail silently

- **An unmounted drive.** No error. Models simply do not resolve, or ComfyUI shows empty dropdowns.
  `preflight.sh` catches it; nothing downstream does.
- **Music under the wrong key.** It belongs at `run-spec.music`, not `run-spec.assemble.music`. The wrong
  key produces a finished film with no music, no warning, and a passing `check`. This happened to
  `kyle_steamfield` and cost a full re-assembly.
- **Real-ESRGAN running while LTX renders.** 48 GB will not hold both. Never overlap `finish` with
  `clips`.
- **A sleeping Mac.** Without `caffeinate` a long run dies partway with no message.

## When something fails

| symptom | cause |
|---|---|
| every model `DOWNLOADED: no` | drive unmounted, or the four `custom*.json` manifests missing — [[model-storage-locations]] |
| face becomes someone else mid-clip | expression changed, or the still had no face — [[still-geometry-and-review]] §8, §11 |
| a cord, watch or animal appears | nothing in frame was moving — §9, §10 |
| hands merge into an object | the still asked for hand and object to overlap — §6 |
| clip ends darker than it starts | LTX's end-of-clip fade; `qc_sheet.sh` prints where it begins, trim before it |

## Related pages
- [[idea-to-video-blueprint]]
- [[still-geometry-and-review]]
- [[scripts-reference]]
- [[model-storage-locations]]
- [[headless-cli-pipeline]]
