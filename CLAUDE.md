# LLM Wiki

A personal knowledge base maintained by Claude Code.
Based on Andrej Karpathy's LLM Wiki pattern.

## Purpose
This wiki is a structured, interlinked knowledge base for the AI video generation domain — turning still photos into 4K video, image-to-video models, upscaling, interpolation, and ffmpeg pipelines.
Claude maintains the wiki. The human curates sources, asks questions, and guides the analysis.

## Folder structure

Shared across every project:
```
wiki/         -- concept, recipe and reference pages maintained by Claude
wiki/index.md -- table of contents for the entire wiki
wiki/log.md   -- append-only record of all operations
docs/         -- generated static site (do not edit by hand)
raw/          -- cross-project source documents (immutable -- never modify)
scripts/      -- the pipeline (see wiki/scripts-reference.md)
tools/        -- realesrgan and other binaries
projects.json -- registry of every video project; scripts/build_projects.py renders it
```

One folder per project, named for its `projects.json` id:
```
projects/<id>/
  plan/    -- the project's wiki page(s); rendered into the site alongside wiki/
  raw/     -- that project's source photos, comics, references (immutable)
  seed/    -- character and location masters, crops, candidate renders, prompt inputs
  stills/  -- picked first frames + per-shot prompt files
  clips/   -- I2V exports (.mov)
  music/   -- the track(s) that project is cut to
  final/   -- trimmed, upscaled and assembled deliverables
  logs/    -- run logs
```
Only `plan/` and `raw/` are tracked; the rest is generated and git-ignored (see `.gitignore`;
`dragon_epic/raw/` and `lost_city/raw/` are ignored too, being large or personal).
A project's `run-spec.dir` in `projects.json` is `projects/<id>`, and every path inside it is
relative to that.

Key scripts:
```
scripts/build_site.py   -- wiki/*.md + projects/*/plan/*.md -> docs/
scripts/build_projects.py -- projects.json -> wiki/projects*.md (run by build_site.py)
scripts/film_run.py     -- runs a film from its run-spec: check/status/stills/pick/clips/qc/finish
scripts/dt_diptych.sh   -- klein still: diptych / single edit / text-to-image
scripts/dt_clip.sh      -- I2V clip (LTX or Wan presets)
scripts/qc_sheet.sh     -- contact sheet: reference + N frames
scripts/upscale_4k.sh   -- clip -> 3840x2160 (W/H configurable) via Real-ESRGAN
scripts/assemble_film.sh -- N clips -> one film with crossfades (+ music)
scripts/finish_clip.sh  -- 5 s I2V export -> looped 1080x1920 mp4 (+ music)
scripts/preflight.sh    -- pre-run checks (--fix quits Draw Things, starts caffeinate)
scripts/dt_project.sh   -- list/rename/delete Draw Things projects on disk
serve.sh                -- rebuild + serve docs/ on http://localhost:8788
```

## Producing a video
For a multi-shot film, follow `wiki/idea-to-video-blueprint.md` (intake questions up front, then unattended CLI run). For a single looping painting, follow `wiki/runbook-living-painting.md` step by step. When a project starts, add its record to `projects.json` (prompts, seeds, any non-default settings, files, notes) and keep it updated as it renders; `wiki/projects.md` is generated from it. After each session, record timings and any new gotcha on the relevant recipe page and in `wiki/log.md`.

## Site
`docs/` is a static site rendered from `wiki/`. After any wiki change, run
`python3 scripts/build_site.py` (or `./serve.sh` to build and preview).
The landing page is generated from `wiki/index.md` — keep index entries in the
form `- [[slug]] — one-line description` under `## Section` headings so they
become cards. Never edit `docs/` directly.

## Ingest workflow
When the user adds a new source to `raw/` and asks you to ingest it:
1. Read the full source document
2. Discuss key takeaways with the user before writing anything
3. Create a summary page in `wiki/` named after the source
4. Create or update concept pages for each major idea or entity
5. Add wiki-links ([[page-name]]) to connect related pages
6. Update `wiki/index.md` with new pages and one-line descriptions
7. Append an entry to `wiki/log.md` with the date, source name, and what changed

A single source may touch 10-15 wiki pages. That is normal.

## Page format
Every wiki page should follow this structure:

```markdown
# Page Title

**Summary**: One to two sentences describing this page.

**Sources**: List of raw source files this page draws from.

**Last updated**: Date of most recent update.

---

Main content goes here. Use clear headings and short paragraphs.

Link to related concepts using [[wiki-links]] throughout the text.

## Related pages
- [[related-concept-1]]
- [[related-concept-2]]
```

## Citation rules
- Every factual claim should reference its source file
- Use the format (source: filename.pdf) after the claim
- If two sources disagree, note the contradiction explicitly
- If a claim has no source, mark it as needing verification
- Model capabilities, pricing, and output resolutions change fast — always date such claims and mark them as "as of YYYY-MM-DD"

## Question answering
When the user asks a question:

1. Read `wiki/index.md` first to find relevant pages
2. Read those pages and synthesize an answer
3. Cite specific wiki pages in your response
4. If the answer is not in the wiki, say so clearly
5. If the answer is valuable, offer to save it as a new wiki page

Good answers should be filed back into the wiki so they compound over time.

## Lint

When the user asks you to lint or audit the wiki:
- Check for contradictions between pages
- Find orphan pages (no inbound links from other pages)
- Identify concepts mentioned in pages that lack their own page
- Flag claims that may be outdated based on newer sources
- Check that all pages follow the page format above
- Report findings as a numbered list with suggested fixes

## Rules
- Never modify anything in the `raw/` folder
- Always update `wiki/index.md` and `wiki/log.md` after changes
- Keep page names lowercase with hyphens (e.g. `image-to-video.md`)
- Write in clear, plain language
- When uncertain about how to categorize something, ask the user
