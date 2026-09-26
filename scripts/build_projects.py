#!/usr/bin/env python3
"""Render the registry pages from every projects/<id>/<version>/spec.json.

Each version's spec.json is the source of truth; projects/_shared.json holds the
defaults, themes and playlist. This assembles them, rewrites the root
projects.json as an aggregate, and renders the hub + one page per theme.
Edit a spec, then run this (build_site.py calls it automatically). A project's still/i2v/post dicts only need the keys
that differ from `defaults`; the rest is filled in here. Each project carries a
`theme` ("anime" / "realistic" / "3d"); the themes themselves — slug, title,
blurb — are defined in projects/_shared.json under `themes`, and each becomes its
own wiki page so no single page carries every record.
"""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "projects.json"          # generated aggregate, written by load()
SPECS = ROOT / "projects"             # source of truth: projects/<id>/spec.json + _shared.json
OUT = ROOT / "wiki" / "projects.md"
WIKI = ROOT / "wiki"

ORDER = {
    "still": ["model", "size", "steps", "cfg", "shift", "sampler", "lora", "refiner", "seed"],
    "i2v": ["model", "refiner", "lora", "size", "frames", "fps", "steps", "cfg", "shift", "sampler", "strength", "seed", "time_min"],
    "post": ["script", "loop", "upscale", "music"],
}
LABEL = {"cfg": "CFG", "time_min": "I2V time (min)", "fps": "FPS", "lora": "LoRA", "script": "Script"}


def merged(defaults, override):
    d = dict(defaults)
    d.update({k: v for k, v in (override or {}).items()})
    return d


def block(title, defaults, override, suffix):
    d = merged(defaults, override)
    lines = [f"**{title}**", "", "| Setting | Value |", "|---|---|"]
    for k in ORDER[title.split()[0].lower()]:
        if k in d and d[k] is not None:
            lines.append(f"| {LABEL.get(k, k.capitalize())} | {d[k]} |")
    if d.get("prompt"):
        p = d["prompt"].replace("{style_suffix}", suffix)
        lines += ["", f"Prompt: `{p}`"]
    return "\n".join(lines)


def summary_rows(projects, defs, link_page=None):
    """Table rows; link_page=None keeps the anchor local, else points at that page."""
    rows = []
    for i, p in enumerate(projects, 1):
        s = merged(defs["still"], p.get("still"))
        v = merged(defs["i2v"], p.get("i2v"))
        m = merged(defs["post"], p.get("post")).get("music") or "—"
        final = next((f for f in p.get("files", []) if f.endswith("_final.mp4")), "—")
        yt = f"[▶ watch](https://youtu.be/{p['youtube']})" if p.get("youtube") else "—"
        href = f"#{p['id']}" if link_page is None else f"{link_page}.html#{p['id']}"
        rows.append(
            f"| {i} | [{p['title']}]({href}) | {p['date']} | {p['status']} | "
            f"{s['model'].split(' (')[0]} {s['size'].split(' ')[0]} | "
            f"{v['model'].split(' Expert')[0]} {v.get('time_min', '?')} min | "
            f"{m.split(' —')[0].split(' (')[0]} | `{final}` | {yt} |")
    return rows


HEAD = ["| # | Project | Date | Status | Still | I2V | Music | Final file | YouTube |",
        "|--:|---|---|---|---|---|---|---|---|"]


def record(p, defs, suffix):
    ver = f" · **Version**: `{p['version']}`" if p.get("version") else ""
    out = [f"## {p['title']} {{#{p['id']}}}", "",
           f"- **Date**: {p['date']} · **Status**: {p['status']}{ver} · **Draw Things project**: `{p['dt_project']}`",]
    if p.get("variant"):
        out.append(f"- **This version**: {p['variant']}")
    if p.get("versions"):
        out += ["", "**Versions**", "", "| Version | What it is | Status | YouTube |", "|---|---|---|---|"]
        for v in p["versions"]:
            yt = f"[▶ watch](https://youtu.be/{v['youtube']})" if v.get("youtube") else "—"
            out.append(f"| `{v['version']}` | {v['variant']} | {v['status']} | {yt} |")
        out.append("")
    out += [
           (f"- **Files** (`projects/{p['id']}/{p['version']}/`): " if p.get("version")
            else "- **Files**: ") + ", ".join(f"`{f}`" for f in p.get("files", [])),
           f"- **Notes**: {p.get('notes', '')}", ""]
    if p.get("youtube"):
        note = f" *({p['youtube_note']})*" if p.get("youtube_note") else ""
        size = (p.get("i2v") or {}).get("size") or defs["i2v"].get("size", "576x1024")
        w, h = (int(x) for x in size.lower().split("x"))
        cls = "yt" if w > h else "yt yt-v"
        out += [f"- **YouTube**: [youtu.be/{p['youtube']}](https://youtu.be/{p['youtube']}){note}", "",
                f'<div class="{cls}"><iframe src="https://www.youtube.com/embed/{p["youtube"]}" title="{p["title"]}" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>', ""]
    out += [block("Still", defs["still"], p.get("still"), suffix), "",
            block("I2V", defs["i2v"], p.get("i2v"), suffix), "",
            block("Post", defs["post"], p.get("post"), suffix), ""]
    if p.get("scenes"):
        sc = p["scenes"]
        out += ["### Scene prompts", ""]
        if "locks" in sc:
            L = sc["locks"]
            out += ["**Locks** (paste verbatim into every prompt):", ""]
            for k in [k for k in L if k != "rules"]:
                if L.get(k): out += [f"- *{k.replace('_', ' ')}* — {L[k]}"]
            if L.get("rules"): out += ["", f"**Rules**: {L['rules']}", ""]
        for key in [k for k in sc if k != "locks"]:
            v = sc[key]
            out += ["", f"#### {key} — {v.get('title', '')}", ""]
            if v.get("engine"): out += [f"- **Engine**: {v['engine']}"]
            if v.get("files"): out += [f"- **Files**: {v['files']}"]
            if v.get("note"): out += [f"- **Note**: {v['note']}"]
            if v.get("still"): out += ["", "*Still prompt*", "", f"> {v['still']}"]
            for label, k in (("Video prompt", "video"), ("Video prompt (Wan)", "video_wan"), ("Video prompt (LTX)", "video_ltx")):
                if v.get(k): out += ["", f"*{label}*", "", f"> {v[k]}"]
            out += [""]
    return out


def load():
    """Assemble the registry from projects/*/spec.json + projects/_shared.json.

    Each project owns its record so its folder is self-contained and re-runnable;
    projects.json is regenerated from them for anything that wants one file.
    """
    data = json.loads((SPECS / "_shared.json").read_text())
    data.pop("_note", None)
    # one spec per project VERSION; the registry shows the newest version of each
    # project and lists the older ones alongside it
    by_id = {}
    for f in SPECS.glob("*/*/spec.json"):
        r = json.loads(f.read_text())
        by_id.setdefault(r["id"], []).append(r)
    recs = []
    for pid, versions in by_id.items():
        versions.sort(key=lambda r: r.get("version", ""))
        newest = dict(versions[-1])
        if len(versions) > 1:
            newest["versions"] = [{"version": v["version"], "variant": v.get("variant", ""),
                                   "status": v.get("status", ""), "youtube": v.get("youtube")}
                                  for v in versions]
        recs.append(newest)
    recs.sort(key=lambda r: (r.get("order", 999), r["id"]))
    data["projects"] = [{k: v for k, v in r.items() if k != "order"} for r in recs]
    SRC.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return data


def main():
    data = load()
    defs, suffix = data["defaults"], data["defaults"]["style_suffix"]
    projects = data["projects"]
    themes = data["themes"]
    today = date.today().isoformat()

    # a project with no theme (or an unknown one) would otherwise vanish from every
    # page — put it in the first theme and say so loudly
    fallback = next(iter(themes))
    for p in projects:
        if p.get("theme") not in themes:
            print(f"  ! {p['id']}: theme {p.get('theme')!r} unknown — filed under {fallback!r}")
            p["theme"] = fallback

    # ---- hub page: every project in one table, grouped by theme, records live elsewhere
    out = [
        "# Projects Registry",
        "",
        "**Summary**: Index of every video project so far, grouped by theme. The full record for each one — models, settings, prompts, seeds, music, files — lives on its theme page. Generated from each version's `spec.json`; edit those, not this page.",
        "",
        "**Sources**: projects/*/*/spec.json; per-project notes from the session logs.",
        "",
        f"**Last updated**: {today}",
        "",
        "---",
        "",
        "**Project pages**: " + " · ".join(
            f"[[{t['slug']}|{t['title']}]] ({sum(1 for p in projects if p.get('theme') == key)})"
            for key, t in themes.items()
            if any(p.get("theme") == key for p in projects)),
        "",
        "Each theme page holds the full records — settings, prompts, seeds, files. The tables below link straight to a project's record on its page.",
        "",
    ]
    for key, t in themes.items():
        group = [p for p in projects if p.get("theme") == key]
        if not group:
            continue
        out += [f"## [[{t['slug']}|{t['title']}]] ({len(group)})", "", t["blurb"], ""] + HEAD
        out += summary_rows(group, defs, link_page=t["slug"])
        out += ["", f"→ full records for all {len(group)}: [[{t['slug']}|{t['title']}]]", ""]

    pl = data.get("playlist")
    if pl:
        out += ["", f"## YouTube playlist — [{pl['title']}]({pl['url']})", "",
                f'<div class="yt"><iframe src="https://www.youtube.com/embed/videoseries?list={pl["id"]}" title="{pl["title"]}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>', ""]

    out += ["", "## Defaults (apply unless a record overrides)", "",
            block("Still", defs["still"], None, suffix), "",
            block("I2V", defs["i2v"], None, suffix), "",
            block("Post", defs["post"], None, suffix), "",
            f"Style suffix appended to every still prompt: `{suffix}`", "",
            "## Related pages",
            "- " + " · ".join(f"[[{t['slug']}]]" for t in themes.values()),
            "- [[runbook-living-painting]]", "- [[living-painting-loop]]", "- [[draw-things-setup]]", ""]
    OUT.write_text("\n".join(out), encoding="utf-8")

    # ---- one page per theme with the full records
    wrote = [(OUT.name, len(projects))]
    for key, t in themes.items():
        group = [p for p in projects if p.get("theme") == key]
        if not group:
            continue
        others = " · ".join(f"[[{o['slug']}]]" for k, o in themes.items() if k != key)
        page = [f"# {t['title']}", "",
                f"**Summary**: {t['blurb']} Full record per project: models, settings, prompts, seeds, music and output files. Generated from each version's `spec.json`.",
                "", "**Sources**: projects/*/*/spec.json; per-project notes from the session logs.",
                "", f"**Last updated**: {today}", "", "---", "",
                f"Index of every project: [[projects]]. Other themes: {others}.", "",
                "## Summary", ""] + HEAD + summary_rows(group, defs) + [""]
        for p in group:
            page += record(p, defs, suffix)
        page += ["## Related pages", "- [[projects]]", "- [[runbook-living-painting]]", "- [[draw-things-setup]]", ""]
        path = WIKI / f"{t['slug']}.md"
        path.write_text("\n".join(page), encoding="utf-8")
        wrote.append((path.name, len(group)))
    print("wrote " + ", ".join(f"{n} ({c})" for n, c in wrote))


if __name__ == "__main__":
    main()
