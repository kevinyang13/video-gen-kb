#!/usr/bin/env python3
"""Render projects.json -> wiki/projects.md (summary table + one record per project).

projects.json is the source of truth. Edit it, then run this (build_site.py
calls it automatically). A project's still/i2v/post dicts only need the keys
that differ from `defaults`; the rest is filled in here.
"""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "projects.json"
OUT = ROOT / "wiki" / "projects.md"

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


def main():
    data = json.loads(SRC.read_text())
    defs, suffix = data["defaults"], data["defaults"]["style_suffix"]
    projects = data["projects"]

    out = [
        "# Projects Registry",
        "",
        "**Summary**: Every video project so far — one record each with the exact models, settings, prompts, seeds, music and output files. Generated from `projects.json`; edit that file, not this page.",
        "",
        "**Sources**: projects.json; per-project notes from the session logs.",
        "",
        f"**Last updated**: {date.today().isoformat()}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| # | Project | Date | Status | Still | I2V | Music | Final file |",
        "|--:|---|---|---|---|---|---|---|",
    ]
    for i, p in enumerate(projects, 1):
        s = merged(defs["still"], p.get("still"))
        v = merged(defs["i2v"], p.get("i2v"))
        m = merged(defs["post"], p.get("post")).get("music") or "—"
        final = next((f for f in p.get("files", []) if f.endswith("_final.mp4")), "—")
        out.append(f"| {i} | [{p['title']}](#{p['id']}) | {p['date']} | {p['status']} | {s['model'].split(' (')[0]} {s['size'].split(' ')[0]} | {v['model'].split(' Expert')[0]} {v.get('time_min', '?')} min | {m.split(' —')[0].split(' (')[0]} | `{final}` |")

    out += ["", "## Defaults (apply unless a record overrides)", "",
            block("Still", defs["still"], None, suffix), "",
            block("I2V", defs["i2v"], None, suffix), "",
            block("Post", defs["post"], None, suffix), "",
            f"Style suffix appended to every still prompt: `{suffix}`", ""]

    for p in projects:
        out += [f"## {p['title']} {{#{p['id']}}}", "",
                f"- **Date**: {p['date']} · **Status**: {p['status']} · **Draw Things project**: `{p['dt_project']}`",
                f"- **Files** (`raw/clips/`): " + ", ".join(f"`{f}`" for f in p.get("files", [])),
                f"- **Notes**: {p.get('notes', '')}", "",
                block("Still", defs["still"], p.get("still"), suffix), "",
                block("I2V", defs["i2v"], p.get("i2v"), suffix), "",
                block("Post", defs["post"], p.get("post"), suffix), ""]

    out += ["## Related pages", "- [[runbook-living-painting]]", "- [[living-painting-loop]]", "- [[draw-things-setup]]", ""]
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(projects)} projects)")


if __name__ == "__main__":
    main()
