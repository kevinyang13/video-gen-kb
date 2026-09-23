#!/usr/bin/env python3
"""Render wiki/*.md into docs/ as a static site.

- docs/wiki/<slug>.html   one page per wiki markdown file
- docs/wiki/assets/       copy of wiki/assets/ (images referenced as assets/<file>)
- docs/index.html         landing page generated from wiki/index.md

The wiki lives at the repo root (CLAUDE.md requires it); docs/ is what gets
served or published. Run after editing any wiki page:

    python3 scripts/build_site.py
"""

import re
import shutil
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
DOCS = ROOT / "docs"
OUT = DOCS / "wiki"

SITE = "video-gen-kb"
TAGLINE = "Photos to 4K video, locally, with open weights"

CSS = """
:root{--bg:#0B0D12;--panel:#141822;--panel-2:#1B2130;--stroke:#2A3245;--text:#E6E9F0;
--muted:#8B94A7;--accent:#F5B84B;--accent-2:#4BC9F5;--on-accent:#12131A;
--rule:rgba(139,148,167,.22);--code:#F5B84B}
@media(prefers-color-scheme:light){:root:not([data-theme=dark]){--bg:#F4F1EA;--panel:#fff;
--panel-2:#FAF8F3;--stroke:#D9D3C6;--text:#16181F;--muted:#5D6473;--accent:#B8781A;
--accent-2:#1E86B0;--rule:rgba(22,24,31,.14);--code:#8A5A0E}}
:root[data-theme=light]{--bg:#F4F1EA;--panel:#fff;--panel-2:#FAF8F3;--stroke:#D9D3C6;
--text:#16181F;--muted:#5D6473;--accent:#B8781A;--accent-2:#1E86B0;--rule:rgba(22,24,31,.14);--code:#8A5A0E}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);
line-height:1.65;padding:0 1rem 4rem}
.shell{max-width:840px;margin:0 auto}
a{color:var(--accent);text-decoration:none;font-weight:600}
a:hover{text-decoration:underline}
a:focus-visible{outline:3px solid var(--accent-2);outline-offset:3px;border-radius:4px}
.bar{display:flex;align-items:center;gap:.75rem;flex-wrap:wrap;padding:1.1rem 0;margin-bottom:1.5rem;
border-bottom:1px solid var(--stroke)}
.crumb{font-size:.76rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.spacer{flex:1}
.pill{border:1px solid var(--stroke);background:var(--panel);border-radius:999px;padding:.28rem .8rem;
font-size:.75rem;font-weight:700;color:var(--text);cursor:pointer;font-family:inherit}
.pill:hover{background:var(--accent);color:var(--on-accent);border-color:var(--accent)}
h1{font-size:clamp(1.7rem,5vw,2.5rem);margin:.2rem 0 1rem;line-height:1.1;letter-spacing:-.015em;text-wrap:balance}
h2{font-size:1.25rem;margin:2.2rem 0 .7rem;padding-bottom:.35rem;border-bottom:1px solid var(--rule);text-wrap:balance}
h3{font-size:1.02rem;margin:1.5rem 0 .5rem;color:var(--accent)}
p{margin:.7rem 0}
ul,ol{margin:.7rem 0 .7rem 1.3rem}
li{margin:.28rem 0}
li::marker{color:var(--accent)}
em{color:var(--muted)}
hr{border:none;border-top:1px solid var(--stroke);margin:2rem 0}
blockquote{border-left:3px solid var(--accent);background:var(--panel);border-radius:0 10px 10px 0;
padding:.8rem 1.1rem;margin:1.1rem 0;color:var(--muted);font-size:.92rem}
code{background:var(--panel);border:1px solid var(--stroke);border-radius:5px;padding:.1rem .35rem;
font-size:.85em;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--code)}
img{max-width:100%;height:auto;display:block;border-radius:12px;border:1px solid var(--stroke);margin:1.1rem 0}
pre{background:var(--panel);border:1px solid var(--stroke);border-radius:12px;padding:1rem;overflow-x:auto;margin:1.1rem 0}
pre code{background:none;border:none;padding:0;color:var(--text);font-size:.83rem;line-height:1.55}
.tw{overflow-x:auto;border:1px solid var(--stroke);border-radius:12px;background:var(--panel);margin:1.1rem 0}
table{width:100%;border-collapse:collapse;font-size:.85rem;min-width:min(100%,460px)}
th{background:var(--panel-2);color:var(--accent);text-align:left;padding:.55rem .8rem;font-size:.68rem;
letter-spacing:.09em;text-transform:uppercase;white-space:nowrap;border-bottom:1px solid var(--stroke)}
td{padding:.5rem .8rem;border-bottom:1px solid var(--rule);color:var(--muted);vertical-align:top}
tr:last-child td{border-bottom:none}
td strong{color:var(--text)}
.meta{display:flex;flex-wrap:wrap;gap:.4rem .9rem;font-size:.78rem;color:var(--muted);margin:-.4rem 0 1.2rem}
.meta b{color:var(--text);font-weight:600}
.missing{color:var(--muted);border-bottom:1px dashed var(--muted);cursor:help}
.related{margin-top:2.5rem;padding-top:1.2rem;border-top:1px solid var(--stroke)}
.related h2{border:none;margin:0 0 .7rem;font-size:.95rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;margin:0}
.chips li{margin:0}
.chips a,.chips .missing{display:inline-block;border:1px solid var(--stroke);background:var(--panel);
border-radius:999px;padding:.28rem .8rem;font-size:.8rem}
.chips a:hover{background:var(--accent);color:var(--on-accent);text-decoration:none;border-color:var(--accent)}
footer{max-width:840px;margin:2.5rem auto 0;padding-top:1.2rem;border-top:1px solid var(--stroke);
font-size:.75rem;color:var(--muted);text-align:center}
/* landing */
.hero{padding:2.4rem 0 1.6rem}
.kicker{font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-2)}
.hero h1{font-size:clamp(2rem,6vw,3.2rem);margin:.35rem 0 .5rem}
.hero p{color:var(--muted);font-size:1.05rem;max-width:56ch}
.hw{display:inline-flex;gap:.5rem;align-items:center;margin-top:1rem;border:1px solid var(--stroke);
background:var(--panel);border-radius:999px;padding:.3rem .9rem;font-size:.78rem;color:var(--muted)}
.hw .dot{width:8px;height:8px;border-radius:50%;background:var(--accent)}
.sec{margin-top:2.2rem}
.sec h2{border:none;padding:0;margin:0 0 .8rem;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:.9rem}
.card{display:block;border:1px solid var(--stroke);background:var(--panel);border-radius:14px;padding:1rem 1.1rem;
color:var(--text);font-weight:400;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--accent);transform:translateY(-2px);text-decoration:none}
.card b{display:block;color:var(--accent);font-size:1rem;margin-bottom:.3rem}
.card span{font-size:.85rem;color:var(--muted);line-height:1.5}
.stubs{font-size:.82rem;color:var(--muted);margin-top:.6rem}
.yt{position:relative;width:100%;aspect-ratio:16/9;border:1px solid var(--stroke);border-radius:12px;overflow:hidden;background:#000;margin:1rem 0}
.yt.yt-v{aspect-ratio:9/16;max-width:360px}
.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {site}</title>
<style>{css}</style>
</head>
<body>
<div class="shell">
  <nav class="bar">
    <span class="crumb"><a href="../">{site}</a> / <a href="index.html">Wiki</a></span>
    <span class="spacer"></span>
    <button class="pill" onclick="tt()">◐ Theme</button>
  </nav>
  {body}
  {related}
</div>
<footer>{site} · built {today} · <a href="../">Home</a> · <a href="index.html">Wiki index</a> · <a href="log.html">Log</a></footer>
<script>{js}</script>
</body>
</html>
"""

LANDING = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{site}</title>
<style>{css}</style>
</head>
<body>
<div class="shell">
  <nav class="bar">
    <span class="crumb">{site}</span>
    <span class="spacer"></span>
    <a class="pill" href="wiki/index.html">Wiki index</a>
    <a class="pill" href="wiki/log.html">Log</a>
    <button class="pill" onclick="tt()">◐ Theme</button>
  </nav>
  <section class="hero">
    <div class="kicker">Knowledge base</div>
    <h1>{tagline}</h1>
    <p>An LLM-maintained wiki on turning still photos into 4K video with open-weight models — what runs on Apple Silicon, what breaks, and the pipeline that works.</p>
    <div class="hw"><span class="dot"></span> Mac Studio · M4 Max · 48 GB unified</div>
  </section>
  {sections}
</div>
<footer>{site} · {count} pages · built {today}</footer>
<script>{js}</script>
</body>
</html>
"""

JS = """function tt(){var r=document.documentElement,
d=r.getAttribute('data-theme')==='dark'||(!r.hasAttribute('data-theme')&&
matchMedia('(prefers-color-scheme: dark)').matches);
r.setAttribute('data-theme',d?'light':'dark');}"""


def md_to_html(body, slugs):
    """Convert wiki markdown to HTML with [[links]] resolved."""

    def link(m):
        target = m.group(1).strip()
        label = None
        if "|" in target:                      # [[slug|display text]]
            target, label = (x.strip() for x in target.split("|", 1))
        label = label or target.replace("-", " ")
        if target in slugs:
            return f'<a href="{target}.html">{label}</a>'
        return f'<span class="missing" title="page not written yet">{label}</span>'

    body = re.sub(r"\[\[([^\]]+)\]\]", link, body)
    html = markdown.markdown(
        body, extensions=["tables", "fenced_code", "sane_lists", "attr_list"]
    )
    return html.replace("<table>", '<div class="tw"><table>').replace(
        "</table>", "</table></div>"
    )


def extract_meta(html):
    """Turn the leading Summary/Sources/Last updated paragraphs into a meta strip."""
    fields = {}
    for key in ("Summary", "Sources", "Last updated"):
        m = re.search(
            rf"<p><strong>{key}</strong>:\s*(.*?)</p>\n?", html, re.S
        )
        if m:
            fields[key] = m.group(1).strip()
            html = html[: m.start()] + html[m.end() :]
    if not fields:
        return html, ""
    parts = []
    if "Summary" in fields:
        parts.append(f'<p class="lede">{fields["Summary"]}</p>')
    bits = []
    if "Last updated" in fields:
        bits.append(f"<span><b>Updated</b> {fields['Last updated']}</span>")
    if "Sources" in fields:
        bits.append(f"<span><b>Sources</b> {fields['Sources']}</span>")
    if bits:
        parts.append('<div class="meta">' + "".join(bits) + "</div>")
    # drop the <hr> that follows the header block
    html = re.sub(r"^\s*<hr\s*/?>\s*", "", html, count=1)
    return html, "".join(parts)


def split_related(html):
    m = re.search(r"<h2>Related [Pp]ages</h2>\s*<ul>(.*?)</ul>", html, re.S)
    if not m:
        return html, ""
    items = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
    chips = "".join(f"<li>{i.strip()}</li>" for i in items)
    related = f'<div class="related"><h2>Related pages</h2><ul class="chips">{chips}</ul></div>'
    return html[: m.start()] + html[m.end() :], related


def build_landing(slugs, today):
    """Render wiki/index.md sections as card grids."""
    text = (WIKI / "index.md").read_text(encoding="utf-8")
    body = text.split("\n---\n", 1)[-1]
    sections = []
    for sec in re.split(r"^## ", body, flags=re.M)[1:]:
        title, _, rest = sec.partition("\n")
        title = title.strip()
        if title.lower() == "log":
            continue
        cards, stubs = [], ""
        for line in rest.splitlines():
            m = re.match(r"^- \[\[([^\]]+)\]\]\s*[—-]\s*(.*)$", line.strip())
            if m:
                slug, desc = m.group(1).strip(), m.group(2).strip()
                if slug in slugs:
                    cards.append(
                        f'<a class="card" href="wiki/{slug}.html"><b>{slug.replace("-", " ")}</b>'
                        f"<span>{desc}</span></a>"
                    )
            elif line.strip().startswith("_("):
                stubs = f'<p class="stubs">{line.strip().strip("_")}</p>'
        if cards or stubs:
            sections.append(
                f'<section class="sec"><h2>{title}</h2><div class="grid">{"".join(cards)}</div>{stubs}</section>'
            )
    (DOCS / "index.html").write_text(
        LANDING.format(
            site=SITE,
            tagline=TAGLINE,
            css=CSS,
            js=JS,
            sections="".join(sections),
            count=len(slugs),
            today=today,
        ),
        encoding="utf-8",
    )


def build():
    import subprocess, sys
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_projects.py')], check=True)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    if (WIKI / "assets").is_dir():
        shutil.copytree(WIKI / "assets", OUT / "assets")
    (DOCS / ".nojekyll").touch()
    today = date.today().isoformat()

    slugs = {p.stem for p in WIKI.glob("*.md")}
    for path in sorted(WIKI.glob("*.md")):
        slug = path.stem
        raw = path.read_text(encoding="utf-8")
        html = md_to_html(raw, slugs)
        m = re.search(r"<h1>(.*?)</h1>", html)
        title = re.sub(r"<[^>]+>", "", m.group(1)) if m else slug.replace("-", " ").title()
        html, meta = extract_meta(html)
        html = html.replace(f"<h1>{m.group(1)}</h1>", f"<h1>{m.group(1)}</h1>{meta}", 1) if m else meta + html
        html, related = split_related(html)
        (OUT / f"{slug}.html").write_text(
            PAGE.format(title=title, site=SITE, css=CSS, js=JS, body=html, related=related, today=today),
            encoding="utf-8",
        )

    build_landing(slugs, today)
    print(f"built {len(slugs)} wiki pages + landing -> {DOCS.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
