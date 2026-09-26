# Repo Structure — where everything lives

**Summary**: How this repository is laid out since the 2026-09-25 reorganisation: shared infrastructure at the root, one self-contained folder per video project, and the rules for what is tracked, what is generated, and what is safe to delete. Read this before starting a project or moving files.

**Sources**: the repository itself; `CLAUDE.md`; [[scripts-reference]]; [[log]] 2026-09-25.

**Last updated**: 2026-09-25

---

## The two halves

**Shared, at the root** — used by every project:

```
wiki/          concept, recipe and reference pages (this page lives here)
wiki/index.md  table of contents; entries become cards on the landing page
wiki/log.md    append-only record of every operation
docs/          the generated static site — never edit by hand
raw/           cross-project source documents (immutable)
scripts/       the whole pipeline
tools/         realesrgan and other binaries
projects.json  the registry: one record per project
```

**One folder per project**, named for its `projects.json` id, with **one folder per version** inside it:

```
projects/<id>/
  plan/          the project's page(s) — one story across all versions
  <version>/     e.g. v1-drawthings-ui, v2-drawthings-cli, v2-master-restage
    spec.json    this version's record: settings, prompts, run-spec, music, status
    raw/         its source photos, comics, references
    seed/        masters, crops, candidate renders, prompt inputs
    stills/      picked first frames + per-shot prompt files
    clips/       shot-scoped output: I2V exports, trims, per-shot 4K
    music/       the track(s) this version is cut to
    final/       the film itself — assembled master and delivery copies
    logs/        run logs and the scripts a run used
```

**A version is a variant of the same film, not a revision of a file.** The name is `v<n>-<short-description>`: what changed about *how* it was made. Existing ones: `v1-drawthings-ui` (driven through the app window), `v1-drawthings-cli` (headless from the start), `v2-drawthings-cli` (lost_city's shots 14–15, after the CLI arrived), `v2-master-restage` (fll_champions, after the masters were rebuilt and the beats restaged).

Each version folder is **self-contained and independently re-runnable** — it carries its own sources, prompts and spec, at the cost of duplicating the source photos between versions of the same project. The plan page stays at project level and tells the whole story.

`scripts/film_run.py <id>` uses the newest version; `<id>@<version>` pins one, e.g. `film_run.py lost_city@v1-drawthings-ui status`. The registry shows each project's newest version and lists the others.

Not every version uses every folder: the early 9:16 loops ([[living-painting-loop]]) have only `clips/ final/ music/`, while a multi-shot film uses all eight.

**`final/` is the film, not the shots.** One folder, one question: *what do I hand over?* Every shot-scoped artefact — the `.mov` export, the trimmed ProRes, the per-shot `_4k.mp4` and its stamp — stays in `clips/` next to the clip it came from. Only the assembled master and its delivery copies (1920×1080, 720p, and so on) belong in `final/`. `film_run.py finish` writes to both accordingly. An assembled *sequence* that isn't the whole film still counts as a deliverable — lost_city's 30-second rift coda sits in `final/` even though the film around it isn't cut yet.

**`seed/` is the one to understand.** It holds everything a render *starts from* that isn't a finished still: character and location masters, the face crops they were made from, rejected candidates, and any prepared input images. Masters are the valuable part — they're what makes shot 9 look like shot 2 (see [[character-consistency]]).

## A project must be re-runnable from its own folder

`projects/<id>/<version>/spec.json` is the **source of truth** for that project: the same record that used to sit in the root `projects.json` — models, sizes, seeds, per-scene prompts, the run-spec, music, status, file list. `scripts/build_projects.py` reads every `projects/*/*/spec.json` plus `projects/_shared.json` (defaults, themes, playlist), regenerates the root `projects.json` as an aggregate, and renders the registry pages from it. `film_run.py <id>` reads the project's own spec first and falls back to the aggregate.

So: **edit `projects/<id>/<version>/spec.json`**, never the root `projects.json` — that one is generated and will be overwritten on the next build.

## Tracked vs generated

*Keep the recipe, drop the generated pixels.*

| In git | Ignored |
|---|---|
| `plan/*.md` — the project's page | everything under `seed/ stills/ clips/ final/ music/ logs/` … |
| `spec.json` — its full record | …except the `.txt` prompts and locks and the `.sh` run scripts inside them |
| `stills/*.txt`, `seed/*.txt` — prompts and locks | `clips/*_trim.txt` (upscale stamps: build cache) |
| `logs/*.sh` — the scripts a run used | every generated image, video and audio file |
| `raw/` — source photos, comics, references | `dragon_epic/raw/` (personal faces) and `lost_city/raw/` (someone else's render) |

Source material in `raw/` **is** tracked — it's an input, not an output, and it's small (12 MB for the largest project). Only the two noted exceptions stay out.

A fresh clone therefore carries every plan, spec, prompt, lock and source photo — enough to re-run any project from scratch — and not one generated frame.

Two traps, both hit in practice on 2026-09-25:
- A **trailing comment on a pattern line** is read as part of the pattern, so `foo/*.txt  # stamps` silently matches nothing. Comments go on their own line.
- **Ignoring media by extension repo-wide** also catches `raw/` inputs, and `git rm -r --cached` then quietly drops already-tracked sources from HEAD. Scope ignores to the generated folders instead.

## How the pieces connect

**`projects.json` → a folder.** Each record's `run-spec.dir` is `projects/<id>`, and every path inside the spec — `seed/kyle.png`, `stills/s3.txt`, `clips/s3_v1.mov` — is relative to it. `scripts/film_run.py` resolves them, which is why the reorganisation needed no changes to any shell script: they all take paths as arguments.

**Plan pages publish with the wiki.** `scripts/build_site.py` collects `wiki/*.md` **and** `projects/*/plan/*.md` into one slug namespace, so `[[lost-city-plan]]` resolves from anywhere and the page lands at `docs/wiki/lost-city-plan.html` like any other. A project folder stays self-contained without splitting the knowledge base in two.

**`projects.json` → the registry pages.** `scripts/build_projects.py` renders it into [[projects]] (the hub) and one page per theme — [[projects-anime]], [[projects-realistic]], [[projects-3d]] — grouped by each record's `theme` field. A record with a missing or unknown theme is filed under the first theme with a warning rather than silently vanishing.

## Starting a new project

1. Pick an id (lowercase, underscores — it's the folder name and the registry key).
2. `mkdir -p projects/<id>/plan projects/<id>/v1-<how>/{raw,seed,stills,clips,music,final,logs}` — or just the folders you need. Name the version for the method, e.g. `v1-drawthings-cli`.
3. Put the source material in `projects/<id>/v1-<how>/raw/`.
4. Write `projects/<id>/v1-<how>/spec.json`: `id`, `title`, `date`, **`theme`**, `dt_project`, `status`, `version`, `variant`, plus `still`/`i2v`/`post` blocks and, for a multi-shot film, a `run-spec` whose `dir` is `projects/<id>/<version>`.
5. Write `projects/<id>/plan/<id>-plan.md` following the standard page format, and add a card for it to `wiki/index.md` under **Plans**.
6. Run `python3 scripts/build_site.py`, then follow [[idea-to-video-blueprint]].

**Start a new version** when the method changes materially — a different engine, a rebuilt cast, a new look. Copy the sources across, write a fresh spec, and leave the old version untouched as the record of what was tried.

## What is an intermediate

Safe to delete once a film is delivered:

| Category | Why it's disposable |
|---|---|
| `*_4k_frames/` | PNG dumps from the upscaler — by far the biggest thing on disk (23 GB across 13 projects) |
| `*_t.mov` in `clips/` | trimmed ProRes, re-cut from the source clip in seconds |
| candidate and QC images in `seed/` (`*_c[0-9].png`, `*_qc.png`) | rejected seeds; the picks are already in `stills/` and `seed/` |
| `clips/*.mov` **that have a `_4k.mp4` beside them** | the upscaled mp4 carries the shot |

**Always keep**: the finished films in `final/`, the per-shot `clips/*_4k.mp4` (they let a film be re-cut, re-ordered or re-scored without re-rendering), picked stills, masters, prompt files, music and `raw/`.

**The guard**: a `.mov` with no 4K counterpart is the *only* copy of that shot — deleting it means a ~10-minute re-render. Check before a sweep. On 2026-09-25 that rule spared lost_city's s9 pair and an old fll_farm drone test while 30 GB went.

## Related pages
- [[scripts-reference]] — what each script does and the flags that matter
- [[idea-to-video-blueprint]] — the process a project follows once its folder exists
- [[projects]] — the registry rendered from `projects.json`
- [[headless-cli-pipeline]] — the CLI that produces most of what lands in these folders
