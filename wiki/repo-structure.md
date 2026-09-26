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

**One folder per project**, named for its `projects.json` id:

```
projects/<id>/
  plan/    the project's page(s) — published with the wiki
  raw/     its source photos, comics, references (immutable)
  seed/    masters, crops, candidate renders, prompt inputs
  stills/  picked first frames + per-shot prompt files
  clips/   image-to-video exports (.mov)
  music/   the track(s) this film is cut to
  final/   trimmed, upscaled and assembled deliverables
  logs/    run logs
```

Not every project uses every folder: the early 9:16 loops ([[living-painting-loop]]) have only `clips/ final/ music/`, while a multi-shot film uses all eight.

**`seed/` is the one to understand.** It holds everything a render *starts from* that isn't a finished still: character and location masters, the face crops they were made from, rejected candidates, and any prepared input images. Masters are the valuable part — they're what makes shot 9 look like shot 2 (see [[character-consistency]]).

## Tracked vs generated

Only `plan/` and `raw/` are committed. Everything else is git-ignored:

```gitignore
projects/*/seed/  projects/*/stills/  projects/*/clips/
projects/*/final/ projects/*/music/   projects/*/logs/
projects/dragon_epic/raw/   # large
projects/lost_city/raw/     # large
```

The two ignored `raw/` folders are exceptions from before the move and stay ignored. Everything git-ignored is either re-derivable or a deliverable that belongs on YouTube rather than in git.

## How the pieces connect

**`projects.json` → a folder.** Each record's `run-spec.dir` is `projects/<id>`, and every path inside the spec — `seed/kyle.png`, `stills/s3.txt`, `clips/s3_v1.mov` — is relative to it. `scripts/film_run.py` resolves them, which is why the reorganisation needed no changes to any shell script: they all take paths as arguments.

**Plan pages publish with the wiki.** `scripts/build_site.py` collects `wiki/*.md` **and** `projects/*/plan/*.md` into one slug namespace, so `[[lost-city-plan]]` resolves from anywhere and the page lands at `docs/wiki/lost-city-plan.html` like any other. A project folder stays self-contained without splitting the knowledge base in two.

**`projects.json` → the registry pages.** `scripts/build_projects.py` renders it into [[projects]] (the hub) and one page per theme — [[projects-anime]], [[projects-realistic]], [[projects-3d]] — grouped by each record's `theme` field. A record with a missing or unknown theme is filed under the first theme with a warning rather than silently vanishing.

## Starting a new project

1. Pick an id (lowercase, underscores — it's the folder name and the registry key).
2. `mkdir -p projects/<id>/{plan,raw,seed,stills,clips,music,final,logs}` — or just the folders you need.
3. Put the source material in `projects/<id>/raw/`.
4. Add the record to `projects.json`: `id`, `title`, `date`, **`theme`**, `dt_project`, `status`, plus `still`/`i2v`/`post` blocks and, for a multi-shot film, a `run-spec`.
5. Write `projects/<id>/plan/<id>-plan.md` following the standard page format, and add a card for it to `wiki/index.md` under **Plans**.
6. Run `python3 scripts/build_site.py`, then follow [[idea-to-video-blueprint]].

## What is an intermediate

Safe to delete once a film is delivered:

| Category | Why it's disposable |
|---|---|
| `*_4k_frames/` | PNG dumps from the upscaler — by far the biggest thing on disk (23 GB across 13 projects) |
| `*_t.mov` in `final/` | trimmed ProRes, re-cut from the source clip in seconds |
| candidate and QC images in `seed/` (`*_c[0-9].png`, `*_qc.png`) | rejected seeds; the picks are already in `stills/` and `seed/` |
| `clips/*.mov` **that have a 4K counterpart** | the upscaled mp4 carries the shot |

**Always keep**: the finished films, the per-shot `*_4k.mp4` (they let a film be re-cut, re-ordered or re-scored without re-rendering), picked stills, masters, prompt files, music and `raw/`.

**The guard**: a `.mov` with no 4K counterpart is the *only* copy of that shot — deleting it means a ~10-minute re-render. Check before a sweep. On 2026-09-25 that rule spared lost_city's s9 pair and an old fll_farm drone test while 30 GB went.

## Related pages
- [[scripts-reference]] — what each script does and the flags that matter
- [[idea-to-video-blueprint]] — the process a project follows once its folder exists
- [[projects]] — the registry rendered from `projects.json`
- [[headless-cli-pipeline]] — the CLI that produces most of what lands in these folders
