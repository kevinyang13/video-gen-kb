#!/usr/bin/env python3
"""Run a multi-shot film from its run-spec in projects/<id>/<version>/spec.json.

PROJECT is "<id>" (newest version), "<id>@<version>", or a path to a .json file
holding the run-spec (handy for tests).
  PROJECT is "<id>" (newest version) or "<id>@<version>", e.g. lost_city@v1-drawthings-ui
  scripts/film_run.py PROJECT check              validate the run-spec (paths, sizes, frame rules)
  scripts/film_run.py PROJECT status             one line per shot: still / candidates / clips / take / 4K
  scripts/film_run.py PROJECT masters [names]    seed candidates for each master -> seed/<name>_c<seed>.png
  scripts/film_run.py PROJECT stills [ids]       seed candidates for shots with no picked still -> seed/<id>_c<seed>.png
  scripts/film_run.py PROJECT sheet [ids]        label candidates -> seed/<id>_sheet.png (review before picking)
  scripts/film_run.py PROJECT pick ID SEED       candidate -> stills/<id>.png
  scripts/film_run.py PROJECT clips [ids] [--v N] [--seed S]   clips/<id>_v<N>.mov for shots with a still
  scripts/film_run.py PROJECT qc [ids] [--v N]   contact sheets seed/<id>_v<N>_qc.png (ref = master or still)
  scripts/film_run.py PROJECT finish [--force]   trim takes -> upscale -> assemble (+music) -> delivery copies
Global flags: --dry-run (print commands), --force (redo existing outputs).

Run-spec (all paths relative to run-spec.dir; every block optional except dir, size, shots):
  "run-spec": {
    "dir": "projects/<id>/<version>", "name": "<film file stem>", "size": [576, 1024],
    "still":   {"model": ..., "steps": 4, "cfg": 1, "config": {...}, "seeds": [1, 2, 3, 4, 5], "strength": 1.0},
    "clip":    {"model": ..., "frames": 249, "steps": 8, "cfg": 1, "config": {...}, "seed": 1, "video_format": "prores422hq"},
    "masters": {"kyle": "seed/kyle_front.png"},             # names usable as a shot's still.ref and qc_ref
    "upscale": {"model": "realesrgan-x4plus", "size": [2160, 3840], "fit": "crop", "bitrate": "40M"},
    "assemble":{"fps": 25, "xfade": 0.75, "clip_audio": false, "bitrate": "40M"},
    "music":   {"file": "projects/<id>/<version>/music/x.mp3", "start": "tail", "vol": 1.0, "fade_in": 1.5, "fade_out": 0},
    "deliver": [{"size": [1080, 1920], "bitrate": "12M"}, {"size": [720, 1280], "bitrate": "2.8M"}],
    "shots": [
      {"id": "s2",
       "still": {"ref": "kyle" | "seed/x.png" | "stills/s1.png" | null, "input": "seed/s2_in.png" | null,
                 "prompt": "<the still prompt text>",
                 "seeds": [...], "size": [w, h]},             # ref+input = diptych, input only = edit, neither = text
       "video_prompt": "<the motion prompt text>", "clip": {...overrides...},
       "qc_ref": "kyle", "take": "clips/s2_v2.mov", "trim": [0, 8]}
    ]}
music.file is relative to the repo root. Takes/trims are what `finish` cuts; set them after QC.
"""
import json
import os, re, shlex, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "scripts"
DEFAULT_STILL = {"model": "flux_2_klein_9b_i8x.ckpt", "steps": 4, "cfg": 1, "config": {"shift": 3.0, "sampler": 16},
                 "seeds": [1, 2, 3, 4, 5], "strength": 1.0}
DEFAULT_CLIP = {"model": "ltx_2.3_22b_distilled_1.1_q8p.ckpt", "seed": 1, "video_format": "prores422hq"}
DRY = "--dry-run" in sys.argv
FORCE = "--force" in sys.argv


def die(msg):
    sys.exit(f"film_run: {msg}")


def load(project):
    if project.endswith(".json"):                       # a standalone run-spec file: {"run-spec": {...}} or the block itself
        j = json.loads(Path(project).read_text())
        f = j.get("run-spec", j)
    else:
        # "<id>" uses the newest version folder; "<id>@<version>" pins one
        pid, _, want = project.partition("@")
        vers = sorted((ROOT / "projects" / pid).glob("*/spec.json"))
        if want:
            vers = [v for v in vers if v.parent.name == want] or die(
                f"no version '{want}' in projects/{pid}")
        spec = vers[-1] if vers else ROOT / "projects" / pid / "spec.json"
        if spec.exists():                               # the project's own record
            p = json.loads(spec.read_text())
        else:                                           # fall back to the aggregate
            data = json.loads((ROOT / "projects.json").read_text())
            p = next((x for x in data["projects"] if x["id"] == project), None)
        if not p:
            die(f"no project '{project}': expected projects/{pid}/<version>/spec.json")
        f = p.get("run-spec") or die(f"project '{project}' has no 'run-spec' block")
        f["_scenes"] = p.get("scenes")          # locks, for the identity and reference checks
    for k in ("dir", "size", "shots"):
        if k not in f:
            die(f"run-spec.{k} missing")
    return f


def flag(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1]
    return default


def ids_arg(f, args):
    ids = [a for a in args if not a.startswith("--") and a not in (flag("--v"), flag("--seed"))]
    known = [s["id"] for s in f["shots"]]
    for i in ids:
        if i not in known:
            die(f"unknown shot '{i}' (have {', '.join(known)})")
    return [s for s in f["shots"] if not ids or s["id"] in ids]


def run(cmd, env=None):
    e = {k: str(v) for k, v in (env or {}).items()}
    shown = " ".join(f"{k}={shlex.quote(v)}" for k, v in e.items()) + (" " if e else "") + " ".join(map(shlex.quote, map(str, cmd)))
    if DRY:
        print(shown)
        return 0
    print(f"$ {shown}", flush=True)
    r = subprocess.run(list(map(str, cmd)), cwd=ROOT, env={**os.environ, **e})
    return r.returncode


def d(f, rel):
    return ROOT / f["dir"] / rel


def resolve_ref(f, ref):
    if not ref:
        return None
    return d(f, f.get("masters", {}).get(ref, ref))


def still_cfg(f, shot):
    c = {**DEFAULT_STILL, **f.get("still", {}), **{k: v for k, v in shot.get("still", {}).items()
                                                   if k in ("seeds", "model", "steps", "cfg", "config", "strength")}}
    c["size"] = shot.get("still", {}).get("size", f["size"])
    return c


def clip_cfg(f, shot):
    return {**DEFAULT_CLIP, **f.get("clip", {}), **shot.get("clip", {})}


# ---------- commands ----------

def prompt_path(f, name, value):
    """Prompts live as text in spec.json; the shell scripts want a file.

    Writes the text to .gen/<name>.txt and returns that path. A value
    that is still a path to an existing .txt (older specs) is used as-is.
    """
    if not isinstance(value, str) or not value.strip():
        die(f"{name}: no prompt in the spec")
    if value.endswith(".txt") and "\n" not in value and d(f, value).exists():
        return d(f, value)
    out = d(f, ".gen") / f"{name}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not DRY:
        out.write_text(value.strip() + "\n", encoding="utf-8")
    return out


# A still that contains a PERSON whose face is not visible gives the I2V stage nothing to propagate:
# whatever the motion reveals is invented from the prompt text, and what it invents is a stranger in
# different clothes rather than a drifted version of the subject. lindsey_sparky s1 turned an
# eight-year-old into an adult woman in a blazer this way. See wiki/still-geometry-and-review.md §11.
# Shots with no person at all are deliberately not flagged -- the risk there is a person wandering in,
# which is real but has never actually happened here.
FACELESS = ("from behind", "back to us", "back to the camera", "her back", "his back",
            "seen from behind", "no face in frame", "over her shoulder", "over his shoulder")
# Phrasings that keep it that way for the whole take. Negatives do not bind on their own, so these are
# the positive forms; "does not turn" is accepted because it only ever appears beside a positive clause.
CONTAINED = ("stays turned away", "stays facing away", "back stays to", "back to us for the whole",
             "back against the chair", "stays seated", "stays on her hands", "stays on his hands",
             "no face comes into frame", "no person enters the frame", "does not turn around",
             "does not tilt up")


def faceless_without_containment(shot):
    """True when a person is in the still but their face is not, and the motion prompt never says so."""
    still = (shot.get("still", {}).get("prompt") or "").lower()
    if not any(k in still for k in FACELESS):
        return False
    return not any(k in (shot.get("video_prompt") or "").lower() for k in CONTAINED)



# A person described generically renders as an adult, and a character LoRA with no trigger token in the
# prompt is inert -- it costs sampling time and binds to nothing. kyle_firstflight shipped with "a small
# figure low in the open cockpit" in s6, no figure at all in s7, and the LoRA applied at 0.6 to both.
# See wiki/still-geometry-and-review.md section 12.
PERSON = ("figure", "pilot", "boy", "girl", "child", "person", "rider", "driver", "kid")
AGE_CUES = ("child proportions", "nine-year-old", "eight-year-old", "year-old boy", "year-old girl",
            "small child's", "child's hand", "a small child")


def trigger_of(f):
    """The LoRA trigger token for this film, e.g. 'kyle_kx', taken from the subject lock."""
    for src in (f.get("subject_lock"), (f.get("_scenes") or {}).get("locks", {}).get("subject")):
        if src:
            m = re.search(r"\b(\w+_kx)\b", src)
            if m:
                return m.group(1)
    return None


# Shots that declare themselves empty of people, or faceless; the first kind has no person to identify,
# the second has a person whose face is not in frame, so a missing trigger is waste rather than a defect.
NO_PEOPLE = ("no people in frame", "no person in frame", "no people close to the camera")
NO_FACE = ("no face in frame", "no face readable", "no face is readable")


def person_problems(shot, trig, wants_child):
    """Identity faults in a shot that contains a person: missing trigger, missing age."""
    p = (shot.get("still", {}).get("prompt") or "").lower()
    if any(k in p for k in NO_PEOPLE):
        return []
    if not any(re.search(r"\b" + n + r"s?\b", p) for n in PERSON):
        return []
    out = []
    has_lora = bool((shot.get("still", {}).get("config") or {}).get("loras"))
    faceless = any(k in p for k in NO_FACE)
    if trig and trig not in p:
        if has_lora and not faceless:
            out.append(("ERR", f"describes a person but the trigger '{trig}' is absent while the LoRA "
                               f"is applied -- it binds to nothing"))
        elif has_lora:
            out.append(("WARN", f"no face in frame and no trigger '{trig}', but the LoRA is still "
                                f"applied -- it costs sampling time and binds to nothing"))
        else:
            out.append(("WARN", f"describes a person but the trigger '{trig}' is absent"))
    # The age cue is required even when the face is not readable: a distant or back-turned figure still
    # renders with adult proportions unless the age is stated, which is the defect kyle_firstflight
    # shipped with ("a small figure low in the open cockpit") and kyle_saltflats v1 before it.
    if wants_child and not any(c in p for c in AGE_CUES):
        out.append(("ERR", "describes a person but never states the age or child proportions "
                           "-- a generic figure renders as an adult at any distance"))
    return out


def object_without_reference(shot, locks, masters):
    """Objects the shot describes in full but was given no picture of."""
    p = (shot.get("still", {}).get("prompt") or "")
    ref = shot.get("still", {}).get("ref")
    inp = (shot.get("still", {}).get("input") or "")
    missing = []
    for name, text in (locks or {}).items():
        if name in ("subject", "wardrobe", "style", "pace", "pilot") or name not in (masters or {}):
            continue
        probe = text[:48]
        if probe and probe in p and ref != name and not inp.endswith(f"{name}.png"):
            missing.append(name)
    return missing


def cmd_check(f, _):
    errs, warns = [], []
    locks = (f.get("_scenes") or {}).get("locks") or {}
    trig = trigger_of(f)
    wants_child = bool(re.search(r"\b(year-old|child proportions)\b", locks.get("subject", "")))
    w, h = f["size"]
    if w % 64 or h % 64:
        errs.append(f"run-spec.size {w}x{h} not multiples of 64")
    cc = {**DEFAULT_CLIP, **f.get("clip", {})}
    fr = cc.get("frames", 249 if "ltx" in cc["model"] else 81)
    if "ltx" in cc["model"] and (fr - 1) % 8:
        errs.append(f"LTX frames {fr} not 8k+1")
    if "wan" in cc["model"] and (fr - 1) % 4:
        errs.append(f"Wan frames {fr} not 4k+1")
    if "ltx" in cc["model"] and w * h > 1024 * 576:
        warns.append(f"LTX at {w}x{h} is above 1024x576 (48 GB swap risk)")
    m = f.get("music", {}).get("file")
    if m and not (ROOT / m).exists():
        errs.append(f"music not found: {m}")
    for name, path in f.get("masters", {}).items():
        if not d(f, path).exists():
            warns.append(f"master '{name}' not made yet: {path}")
    seen = set()
    for s in f["shots"]:
        i = s["id"]
        if i in seen:
            errs.append(f"duplicate shot id {i}")
        seen.add(i)
        st = s.get("still", {})
        if st and not (isinstance(st.get("prompt"), str) and st["prompt"].strip()):
            errs.append(f"{i}: still.prompt is empty")
        if st.get("input") and not d(f, st["input"]).exists():
            warns.append(f"{i}: still.input not made yet: {st['input']}")
        ref = st.get("ref")
        if ref and ref not in f.get("masters", {}) and not ref.startswith(("stills/", "seed/")):
            errs.append(f"{i}: still.ref '{ref}' is neither a master name nor a path")
        if not (isinstance(s.get("video_prompt"), str) and s["video_prompt"].strip()):
            errs.append(f"{i}: video_prompt is empty")
        if s.get("trim"):
            a, b = s["trim"]
            if not 0 <= a < b:
                errs.append(f"{i}: bad trim {s['trim']}")
        if s.get("take") and not d(f, s["take"]).exists():
            warns.append(f"{i}: take not rendered yet: {s['take']}")
        if faceless_without_containment(s):
            warns.append(f"{i}: still has no face and video_prompt never says it stays that way "
                         f"-- anything the motion reveals will be invented (see still-geometry §11)")
        for level, msg in person_problems(s, trig, wants_child):
            (errs if level == "ERR" else warns).append(f"{i}: {msg} (see still-geometry §12)")
        for name in object_without_reference(s, locks, f.get("masters")):
            warns.append(f"{i}: describes '{name}' in full but was given no picture of it "
                         f"-- set still.ref to '{name}' or use its master as still.input (§12)")
    total = sum(s["trim"][1] - s["trim"][0] for s in f["shots"] if s.get("trim"))
    if total:
        xf = f.get("assemble", {}).get("xfade", 0.5)
        n = sum(1 for s in f["shots"] if s.get("trim"))
        print(f"planned length: {total:.2f} s kept − {max(0, n - 1)}×{xf} fades = {total - max(0, n - 1) * xf:.2f} s")
    for x in warns:
        print("  WARN ", x)
    for x in errs:
        print("  FAIL ", x)
    print("check:", "FAIL" if errs else "PASS")
    return 1 if errs else 0


def cmd_status(f, _):
    for s in f["shots"]:
        i = s["id"]
        still = "still" if d(f, f"stills/{i}.png").exists() else "-"
        cands = sum(1 for p in (ROOT / f["dir"] / "work").glob(f"{i}_c*.png") if p.stem[len(i) + 2:].isdigit())
        clips = sorted(p.name for p in (ROOT / f["dir"] / "clips").glob(f"{i}_*.mov"))
        take = s.get("take", "-")
        k4 = "4K" if d(f, f"final/{i}_4k.mp4").exists() else "-"
        print(f"{i:5} {still:5} cand={cands:<2} clips={','.join(clips) or '-':30} take={take} trim={s.get('trim', '-')} {k4}")
    return 0


def cmd_stills(f, args):
    rc = 0
    for s in ids_arg(f, args):
        i = s["id"]
        if d(f, f"stills/{i}.png").exists() and not FORCE:
            print(f"{i}: picked still exists, skipping (--force to regenerate candidates)")
            continue
        st = s.get("still") or die(f"{i}: no still recipe")
        c = still_cfg(f, s)
        ref = resolve_ref(f, st.get("ref"))
        inp = d(f, st["input"]) if st.get("input") else None
        env = {"MODEL": c["model"], "STEPS": c["steps"], "CFG": c["cfg"], "STRENGTH": c["strength"],
               "CONFIG_JSON": json.dumps(c["config"], separators=(",", ":"))}
        for seed in c["seeds"]:
            out = d(f, f"seed/{i}_c{seed}.png")
            if out.exists() and not FORCE:
                continue
            rc |= run([S / "dt_diptych.sh", ref or "-", inp or "-", prompt_path(f, i, st["prompt"]), out, seed, *c["size"]], env)
    return rc




def image_metrics(path):
    """Sharpness and blown-highlight fraction, the two numbers that caught this repo's still failures.

    Sharpness is the variance of a Laplacian over the centre crop, so a soft or bloomed subject scores
    low even when the corners are busy. Blown is the fraction of pixels at or near clipping -- a face
    against an overexposed sky reads high here, which is what hazed kyle_firstflight s5 twice before
    the cause was found.
    """
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        return None
    a = np.asarray(Image.open(path).convert("L"), dtype=float)
    h, w = a.shape
    c = a[h // 5:h * 4 // 5, w // 4:w * 3 // 4]
    lap = (-4 * c[1:-1, 1:-1] + c[:-2, 1:-1] + c[2:, 1:-1] + c[1:-1, :-2] + c[1:-1, 2:])
    # Background luminance over the top and side borders. A subject in front of a blown sky scores high
    # here, and that -- not clipping -- is what hazed kyle_firstflight s5 twice: shallow depth of field
    # against a bright background bleeds over the subject. Clipping alone never caught it (0% every time).
    bg = float(np.concatenate([a[:h // 6].ravel(), a[:, :w // 8].ravel(), a[:, -w // 8:].ravel()]).mean())
    return {"sharp": float(lap.var()), "bg": bg, "clip": float((a >= 245).mean())}


def metric_label(m, best_sharp):
    """A short caption, with a mark on the sharpest tile and a flag on a bright background."""
    if not m:
        return ""
    s = f"  sharp {m['sharp']:.0f}"
    if m["sharp"] >= best_sharp * 0.98:
        s += "*"
    if m["bg"] > 150:
        s += f"  bg {m['bg']:.0f}"
    return s



def master_prompt(f, name):
    """A master's prompt: from run-spec.master_prompts, else .gen/master_<name>.txt."""
    mp = (f.get("master_prompts") or {}).get(name)
    if mp:
        return prompt_path(f, f"master_{name}", mp)
    q = d(f, f".gen/master_{name}.txt")
    return q if q.exists() else None


def cmd_masters(f, args):
    """Render candidates for each master, the same way shots get candidates.

    Masters were made one seed at a time by hand, which is backwards: a master is the most load-bearing
    image in a film because every shot that references it inherits whatever it got on that single roll.
    The LoRA is applied only to a master whose prompt carries the trigger token, which is the same rule
    `check` enforces on shots.
    """
    names = [a for a in args if not a.startswith("--")] or list(f.get("masters", {}))
    trig = trigger_of(f)
    c = still_cfg(f, {})
    rc = 0
    for name in names:
        pf = master_prompt(f, name)
        if not pf:
            print(f"{name}: no prompt (run-spec.master_prompts or .gen/master_{name}.txt)")
            rc |= 1
            continue
        cfg = dict(c["config"])
        if trig and trig not in pf.read_text().lower():
            cfg.pop("loras", None)                       # a LoRA with no trigger in the prompt is inert
        env = {"MODEL": c["model"], "STEPS": c["steps"], "CFG": c["cfg"], "STRENGTH": c["strength"],
               "CONFIG_JSON": json.dumps(cfg, separators=(",", ":"))}
        for seed in c["seeds"]:
            out = d(f, f"seed/{name}_c{seed}.png")
            if out.exists() and not FORCE:
                continue
            rc |= run([S / "dt_diptych.sh", "-", "-", pf, out, seed, *c["size"]], env)
    return rc


def cmd_sheet(f, args):
    """Tile a shot's candidates into one labelled sheet, so a pick is by seed number, not by position.

    Every candidate is captioned with its own `c<seed>`, because reading a grid by
    position is how the wrong still gets picked.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        die("sheet needs Pillow (pip3 install Pillow)")
    cols = int(flag("--cols", 3))
    tile_w = int(flag("--width", 560))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except OSError:
        font = ImageFont.load_default()
    rc = 0
    for s in ids_arg(f, args):
        i = s["id"]
        cands = sorted(d(f, "seed").glob(f"{i}_c*.png"),
                       key=lambda q: int(re.sub(r"\D", "", q.stem.split("_c")[-1]) or 0))
        if not cands:
            print(f"{i}: no candidates")
            continue
        mets = {q: image_metrics(q) for q in cands}
        best = max((m["sharp"] for m in mets.values() if m), default=0.0)
        ims = []
        for q in cands:
            im = Image.open(q).convert("RGB")
            im = im.resize((tile_w, round(im.height * tile_w / im.width)), Image.LANCZOS)
            seed = q.stem.split("_c")[-1]
            cap = f"c{seed}" + metric_label(mets[q], best)
            dr = ImageDraw.Draw(im)
            dr.rectangle([0, 0, 24 + int(dr.textlength(cap, font=font)), 40], fill=(0, 0, 0))
            dr.text((8, 4), cap, fill=(255, 255, 255), font=font)
            ims.append(im)
        tw, th = ims[0].size
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * th), (16, 16, 16))
        for n, im in enumerate(ims):
            sheet.paste(im, ((n % cols) * tw, (n // cols) * th))
        out = d(f, f"seed/{i}_sheet.png")
        if not DRY:
            sheet.save(out)
        note = ""
        if best:
            sharpest = max(mets, key=lambda q: mets[q]["sharp"] if mets[q] else -1)
            bright = [q.stem.split("_c")[-1] for q in cands if mets[q] and mets[q]["bg"] > 150]
            note = f"  sharpest c{sharpest.stem.split('_c')[-1]}"
            if bright:
                note += f", bright background (bloom risk): {', '.join('c' + b for b in bright)}"
        print(f"{i}: {len(ims)} candidates -> {out.relative_to(ROOT)}{note}")
    return rc


def cmd_pick(f, args):
    pos = [a for a in args if not a.startswith("--")]
    if len(pos) != 2:
        die("usage: pick ID SEED")
    i, seed = pos
    src = d(f, f"seed/{i}_c{seed}.png")
    masters = f.get("masters", {})
    dst = d(f, masters[i]) if i in masters else d(f, f"stills/{i}.png")
    if not src.exists():
        die(f"no candidate {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not DRY:
        shutil.copy2(src, dst)
    print(f"{i}: picked seed {seed} -> {dst.relative_to(ROOT)}")
    return 0


def cmd_clips(f, args):
    v = flag("--v", "1")
    rc = 0
    for s in ids_arg(f, args):
        i = s["id"]
        still = d(f, f"stills/{i}.png")
        if not still.exists():
            print(f"{i}: no picked still, skipping")
            continue
        c = clip_cfg(f, s)
        seed = flag("--seed", c["seed"])
        env = {"MODEL": c["model"], "VIDEO_FORMAT": c["video_format"]}
        for k, e in (("steps", "STEPS"), ("cfg", "CFG"), ("frames", "FRAMES")):
            if k in c:
                env[e] = c[k]
        if "config" in c:
            env["CONFIG_JSON"] = json.dumps(c["config"], separators=(",", ":"))
        if FORCE:
            env["FORCE"] = 1
        w, h = s.get("size", f["size"])
        rc |= run([S / "dt_clip.sh", still, prompt_path(f, f"{i}_v", s["video_prompt"]), d(f, f"clips/{i}_v{v}.mov"), seed, w, h], env)
    return rc


def cmd_qc(f, args):
    v = flag("--v", "1")
    rc = 0
    for s in ids_arg(f, args):
        i = s["id"]
        clip = d(f, f"clips/{i}_v{v}.mov")
        if not clip.exists():
            continue
        ref = resolve_ref(f, s.get("qc_ref")) or d(f, f"stills/{i}.png")
        rc |= run([S / "qc_sheet.sh", clip, d(f, f"seed/{i}_v{v}_qc.png"), ref if ref.exists() else "-"])
    return rc


def cmd_finish(f, _):
    up = {"model": "realesrgan-x4plus", "size": [3840, 2160], "fit": "crop", "bitrate": "40M", **f.get("upscale", {})}
    asm = {"fps": 25, "xfade": 0.5, "clip_audio": True, "bitrate": up["bitrate"], **f.get("assemble", {})}
    shots = [s for s in f["shots"] if s.get("take") and s.get("trim")]
    missing = [s["id"] for s in f["shots"] if s not in shots]
    if missing:
        die(f"shots without take/trim: {', '.join(missing)} — set them after QC")
    # per-shot pieces (trims, per-shot 4K) live with the clips they came from;
    # final/ holds only the assembled film and its delivery copies
    cl = ROOT / f["dir"] / "clips"
    fin = ROOT / f["dir"] / "final"
    cl.mkdir(parents=True, exist_ok=True)
    fin.mkdir(parents=True, exist_ok=True)
    W, H = up["size"]
    outs = []
    for s in shots:
        i, (a, b) = s["id"], s["trim"]
        k4, stamp = cl / f"{i}_4k.mp4", cl / f"{i}_trim.txt"
        key = f"{s['take']} {a} {b} {up['model']} {W}x{H} {up['fit']}"
        if k4.exists() and stamp.exists() and stamp.read_text() == key and not FORCE:
            print(f"{i}: 4K up to date")
        else:
            t = cl / f"{i}_t.mov"
            rc = run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", d(f, s["take"]), "-vf",
                      f"trim=start={a}:end={b},setpts=PTS-STARTPTS", "-af", f"atrim=start={a}:end={b},asetpts=PTS-STARTPTS",
                      "-c:v", "prores_ks", "-profile:v", "3", "-c:a", "pcm_s16le", t])
            rc = rc or run([S / "upscale_4k.sh", t, cl / i, up["model"]],
                           {"W": W, "H": H, "FIT": up["fit"], "BITRATE": up["bitrate"], "KEEP_FRAMES": 0,
                            "KEEP_AUDIO": 1 if asm["clip_audio"] else 0})
            if rc:
                die(f"{i}: trim/upscale failed")
            if not DRY:
                stamp.write_text(key)
        outs.append(k4)
    name = f.get("name", Path(f["dir"]).name)
    master = fin / f"{name}_{W}x{H}.mp4"
    env = {"W": W, "H": H, "FPS": asm["fps"], "XFADE": asm["xfade"], "BITRATE": asm["bitrate"],
           "CLIP_AUDIO": 1 if asm["clip_audio"] else 0}
    m = f.get("music")
    if m:
        env.update({"MUSIC": ROOT / m["file"], "MUSIC_START": m.get("start", 0), "MUSIC_FADE_IN": m.get("fade_in", 0),
                    "MUSIC_FADE_OUT": m.get("fade_out", 0),
                    "MUSIC_VOL": m.get("vol", 0.3 if asm["clip_audio"] else 1.0),
                    "CLIP_VOL": m.get("clip_vol", 0.5 if asm["clip_audio"] else 0)})
    if run([S / "assemble_film.sh", master, *outs], env):
        die("assemble failed")
    for dl in f.get("deliver", []):
        w, h = dl["size"]
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", master, "-vf", f"scale={w}:{h}:flags=lanczos",
             "-c:v", "hevc_videotoolbox", "-b:v", dl.get("bitrate", "12M"), "-tag:v", "hvc1", "-c:a", "copy",
             "-movflags", "+faststart", fin / f"{name}_{w}x{h}.mp4"])
    print(f"finished: {master.relative_to(ROOT)}")
    return 0


CMDS = {"check": cmd_check, "status": cmd_status, "masters": cmd_masters, "stills": cmd_stills, "sheet": cmd_sheet, "pick": cmd_pick,
        "clips": cmd_clips, "qc": cmd_qc, "finish": cmd_finish}

if __name__ == "__main__":
    pos = [a for a in sys.argv[1:] if a not in ("--dry-run", "--force")]
    if len(pos) < 2 or pos[1] not in CMDS:
        print(__doc__)
        sys.exit(2)
    spec = load(pos[0])
    sys.exit(CMDS[pos[1]](spec, pos[2:]))
