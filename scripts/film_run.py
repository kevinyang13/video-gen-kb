#!/usr/bin/env python3
"""Run a multi-shot film from its run-spec in projects/<id>/<version>/spec.json.

PROJECT is "<id>" (newest version), "<id>@<version>", or a path to a .json file
holding the run-spec (handy for tests).
  PROJECT is "<id>" (newest version) or "<id>@<version>", e.g. lost_city@v1-drawthings-ui
  scripts/film_run.py PROJECT check              validate the run-spec (paths, sizes, frame rules)
  scripts/film_run.py PROJECT status             one line per shot: still / candidates / clips / take / 4K
  scripts/film_run.py PROJECT lint [ids]        prompt defects readable without rendering
  scripts/film_run.py PROJECT masters [names]    seed candidates for each master -> seed/<name>_c<seed>.png
  scripts/film_run.py PROJECT views [names]      picked master -> turnaround + expressions model sheet
  scripts/film_run.py PROJECT combos [names]     combined masters (character + vehicle / weapon / mount)
  scripts/film_run.py PROJECT eval [names]       consistency: views vs hero, stills vs their ref
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
    "still":   {"model": ..., "steps": 4, "cfg": 1, "config": {...}, "seeds": [1, 2, 3], "strength": 1.0},
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
                 "seeds": [1, 2, 3], "strength": 1.0}
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
    masters = f.get("masters", {})
    if ref in masters:
        return d(f, masters[ref])
    # a model-sheet view or a combo: "<master>_<view>" -> seed/<master>_<view>.png
    if "_" in ref and ref.split("_")[0] in masters or (f.get("combos") or {}).get(ref):
        return d(f, f"seed/{ref}.png")
    return d(f, ref)


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
# A pronoun names a person as surely as a noun does, and it is how the defect slipped through: s8 of
# kyle_firstflight read "He is seen small at this distance" and the age check never fired, so the final
# shot of the film had an adult in the cockpit. Matched with spaces so "the" and "there" do not trip it.
PERSON = ("figure", "pilot", "boy", "girl", "child", "person", "rider", "driver", "kid",
          " he ", " he's", " his ", " him ", " she ", " her ", " hers ")
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


def combo_parts(f, name, seen=None):
    """Every master a combo contains, following chains.

    `flight_crew` is built from `droid` and `kyle_in_skiff`, and that second one is itself built from
    `kyle` and `skiff` -- so a shot referencing flight_crew has been shown all three. Matching master
    names against the ref STRING missed this, because "flight_crew" spells out none of its ingredients.
    """
    seen = seen if seen is not None else set()
    combos = f.get("combos") or {}
    spec = combos.get(name)
    if not spec or name in seen:
        return set()
    seen.add(name)
    parts = set()
    for role in ("ref", "input"):
        src = spec.get(role)
        if not src:
            continue
        parts.add(src)
        parts |= combo_parts(f, src, seen)
    return parts


DIPTYCH_MARKERS = ("side by side", "left image", "right image", "image on the left")


def diptych_problems(shot):
    """A diptych whose prompt is a scene description throws the subject away.

    dt_diptych.sh hstacks REF and IN into one canvas twice the output width, renders it, and keeps the
    RIGHT half. The model only knows that canvas is two images if the prompt says so. Given a plain scene
    description it lays the scene across the whole canvas, the subject lands wherever the composition
    puts it, and the crop discards whatever fell in the left half.

    Measured on kyle_firstflight v2 s4, same seed, same prompt, only the reference swapped:
      REF = skiff_90 (right master)     vs  REF = droid_front (wrong subject)   palette distance 0.061
      REF = skiff_90                    vs  REF = none (single-image edit)      palette distance 0.333
    Swapping the reference for an unrelated object changed almost nothing, so no identity was crossing
    over; and neither diptych contained the thruster nacelle the prompt described, while the single-image
    edit did. See wiki/shot-locks.md.
    """
    st = shot.get("still") or {}
    ref, inp, p = st.get("ref"), st.get("input"), (st.get("prompt") or "").lower()
    out = []
    if ref and inp and not any(k in p for k in DIPTYCH_MARKERS):
        out.append(("ERR", "sets both still.ref and still.input, so it renders as a diptych, but the "
                           "prompt is a scene description -- it must be an edit instruction naming the "
                           "halves ('keep the left image unchanged, re-render the right image so that "
                           "...'), or drop still.ref to run a single-image edit"))
    if ref and inp:
        base = ref.split("_")[0]
        tail = inp.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        if base and (base == tail or base == inp):
            out.append(("WARN", f"still.ref and still.input are both '{base}' -- a diptych of one subject "
                                f"against itself spends half the canvas and carries nothing in; use a "
                                f"single-image edit instead"))
    return out


def object_without_reference(shot, locks, masters, f=None):
    """Objects the shot describes in full but was given no picture of."""
    p = (shot.get("still", {}).get("prompt") or "")
    ref = shot.get("still", {}).get("ref")
    inp = (shot.get("still", {}).get("input") or "")
    parts = combo_parts(f, ref) if (f and ref) else set()
    missing = []
    for name, text in (locks or {}).items():
        if name in ("subject", "wardrobe", "style", "pace", "pilot") or name not in (masters or {}):
            continue
        probe = text[:48]
        # a model-sheet view (skiff_side) or a combo (kyle_in_skiff) shows the object just as its master
        # does, so either satisfies the requirement; a combo also shows whatever it was built from, and
        # a combo built on another combo shows that one's ingredients too (flight_crew -> kyle, skiff, droid)
        # input may be a master NAME ("yard") or a path ("seed/yard.png"), and either shows the object
        shown = (ref == name or (ref or "").startswith(f"{name}_") or f"_{name}" in (ref or "")
                 or f"{name}_" in (ref or "") or name in parts
                 or inp == name or inp.startswith(f"{name}_") or inp.endswith(f"{name}.png"))
        if probe and probe in p and not shown:
            missing.append(name)
    return missing



# ---- prompt lint -------------------------------------------------------------------------------
# Candidates and a contact sheet improve picking, not prompting. Every failure this repo has
# recorded was visible in the prompt text before a GPU-second was spent: a negation that does not bind,
# a contradiction the model cannot resolve, a motion instruction with nothing in frame to attach to, or
# atmosphere with no stated position. See wiki/still-geometry-and-review.md and wiki/shot-locks.md.

NEG_RE = re.compile(r"\b(?:no|without|never|not)\s+([a-z]+(?:\s+[a-z]+)?)")
# phrases every style lock carries; they are conventions the model does honour, not authored negations
NEG_SKIP = ("cartoon", "text", "lettering", "logos", "logo", "watermark", "illustration")
OCCLUDE = ("curtain of", "across his face", "across her face", "in front of his face",
           "in front of her face", "obscuring", "veiling", "parting a")
VISIBLE = ("clearly visible", "well exposed", "razor-sharp focus", "face is well exposed")
ATMOS = ("steam", "mist", "smoke", "haze", "spray", "fog", "dust", "glow")
PLACED = ("behind", "to one side", "out of frame", "beyond", "far side", "in the background",
          "well behind", "either side", "under the hull", "beneath")
MOVERS = ("dust", "steam", "smoke", "sand", "crowd", "banner", "banners", "cable", "cables", "flame",
          "water", "surf", "snow", "rain", "leaves", "birds", "grass", "curtain", "needle", "needles")


def lint_shot(shot, style=""):
    """Prompt defects that are readable without rendering. Returns (level, message, suggestion)."""
    out = []
    still_raw = shot.get("still", {}).get("prompt") or ""
    still = still_raw.lower()
    if style:
        still = still.replace(style.lower(), "")
    video = (shot.get("video_prompt") or "").lower()

    negs = [m for m in NEG_RE.findall(still) if not any(s in m for s in NEG_SKIP)]
    for n in dict.fromkeys(negs):
        out.append(("WARN", f"negation 'no {n}' -- negatives do not bind",
                    f"say what occupies that space instead of what is absent from it"))

    if any(o in still for o in OCCLUDE) and any(v in still for v in VISIBLE):
        out.append(("ERR", "asks for the subject to be occluded and clearly visible in one prompt",
                    "move the occluder behind or beside the subject, or drop the visibility demand"))

    if any(v in still for v in VISIBLE):
        for a in ATMOS:
            if re.search(r"\b" + a + r"\b", still) and not any(pl in still for pl in PLACED):
                out.append(("WARN", f"'{a}' in a shot that demands a visible subject, with no position",
                            "place it: 'well behind him and out to both sides', plus 'clean clear air "
                            "between the camera and his face'"))
                break

    # A motion prompt that moves more subjects than the still contains: the video stage must invent the
    # extra one. kyle_saltflats s7 described an overtake between two machines over a still holding one.
    # "both nacelles" is two parts of one craft, not two subjects, so a part noun after the quantifier
    # does not count. Without this the rule fires on every twin-engined machine in the repo.
    PARTS = ("nacelle", "engine", "hand", "eye", "arm", "wing", "side", "leg", "foot", "feet", "thruster",
             "cable", "rail", "door", "sun", "light", "lamp", "shoulder", "ear")
    plural = re.search(r"\b(both|all four|two of them|each other)\b\s*(\w+)?", video)
    part_ref = bool(plural and plural.group(2) and any(p in plural.group(2) for p in PARTS))
    if re.search(r"\b(a single|one)\b", still) and plural and not part_ref:
        out.append(("ERR", "motion prompt acts on more subjects than the still contains",
                    "match the count: either put the second subject in the still or rewrite the motion "
                    "for one"))

    for mv in MOVERS:
        if re.search(r"\b" + mv + r"\b", video) and not re.search(r"\b" + mv + r"\b", still):
            out.append(("WARN", f"motion prompt moves '{mv}' but the still never mentions it",
                        "the video stage has nothing in frame to attach that motion to and will "
                        "invent something -- put it in the still or drop it from the motion"))
    return out


def cmd_lint(f, args):
    """Read every prompt and report what will fail before anything renders."""
    for name in (f.get("masters") or {}):
        mv = (f.get("master_views") or {}).get(name) or {}
        if mv.get("skip"):
            continue
        if master_kind(f, name) not in ("person", "object"):
            print(f'  ERR   master {name}: no declared kind -- object views would be rendered with '
                  f'anatomy words ("from head to feet, arms relaxed at the sides")\n'
                  f'        -> set master_views.{name}.kind to "person" or "object"')
    style = ((f.get("_scenes") or {}).get("locks") or {}).get("style", "")
    locks = (f.get("_scenes") or {}).get("locks") or {}
    trig, bad = trigger_of(f), 0
    wants_child = bool(re.search(r"\b(year-old|child proportions)\b", locks.get("subject", "")))
    ids = {s["id"] for s in ids_arg(f, args)}
    for s in f["shots"]:
        if s["id"] not in ids:
            continue
        rows = lint_shot(s, style)
        rows += [(lvl, msg, "see wiki/shot-locks.md") for lvl, msg in person_problems(s, trig, wants_child)]
        rows += [(lvl, msg, "see wiki/shot-locks.md") for lvl, msg in diptych_problems(s)]
        for name in object_without_reference(s, locks, f.get("masters"), f):
            rows.append(("WARN", f"describes '{name}' but was given no picture of it",
                         f"set still.ref to '{name}'"))
        for lvl, msg, fix in rows:
            bad += lvl == "ERR"
            print(f"  {lvl:4}  {s['id']}: {msg}\n        -> {fix}")
    print(f"lint: {'FAIL' if bad else 'PASS'}")
    return 1 if bad else 0


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
        mv = (f.get("master_views") or {}).get(name) or {}
        if not mv.get("skip") and master_kind(f, name) not in ("person", "object"):
            errs.append(f'master \'{name}\': master_views.{name}.kind must be "person" or "object" '
                        f'-- object views must not use anatomy words (looks like "{kind_guess(f, name)}")')
    seen = set()
    for s in f["shots"]:
        i = s["id"]
        if i in seen:
            errs.append(f"duplicate shot id {i}")
        seen.add(i)
        st = s.get("still", {})
        if st and not (isinstance(st.get("prompt"), str) and st["prompt"].strip()):
            errs.append(f"{i}: still.prompt is empty")
        for sev, msg in diptych_problems(s):
            (errs if sev == "ERR" else warns).append(f"{i}: {msg}")
        if st.get("input") and not resolve_ref(f, st["input"]).exists():
            warns.append(f"{i}: still.input not made yet: {st['input']}")
        ref = st.get("ref")
        if ref:
            known = (ref in f.get("masters", {}) or ref in (f.get("combos") or {})
                     or ref.startswith(("stills/", "seed/"))
                     or ref.split("_")[0] in f.get("masters", {}))
            if not known:
                errs.append(f"{i}: still.ref '{ref}' is not a master, a model-sheet view, a combo or a path")
            elif not resolve_ref(f, ref).exists():
                warns.append(f"{i}: still.ref '{ref}' not rendered yet ({resolve_ref(f, ref).name})")
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
        for name in object_without_reference(s, locks, f.get("masters"), f):
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
        inp = resolve_ref(f, st["input"]) if st.get("input") else None
        # A diptych carries identity in the left half, so its prompt names no trigger and the LoRA would
        # bind to nothing -- it would still cost sampling time on every seed. cmd_combos already drops it
        # in that case; shots did not, which is what made lint fail s3, s6 and s7.
        cfg = dict(c["config"])
        trig = trigger_of(f)
        if trig and trig not in (st.get("prompt") or "").lower():
            cfg.pop("loras", None)
        env = {"MODEL": c["model"], "STEPS": c["steps"], "CFG": c["cfg"], "STRENGTH": c["strength"],
               "CONFIG_JSON": json.dumps(cfg, separators=(",", ":"))}
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


def metric_label(m, best_sharp, plate=False):
    """A short caption, with a mark on the sharpest tile and a flag on a bright background."""
    if not m:
        return ""
    s = f"  sharp {m['sharp']:.0f}"
    if m["sharp"] >= best_sharp * 0.98:
        s += "*"
    if m["bg"] > 150 and not plate:
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




# A master is either a person or an object and the two need different view language. Deriving it from
# the lock text is reliable when the text actually describes a body, and silently guessing when it does
# not is how the skiff turnaround became a man holding a model aeroplane. So: derive when the evidence
# is clear, and refuse when it is not, rather than defaulting.
PERSON_WORDS = ("boy", "girl", "man", "woman", "child", "person", "face", "hair", "skin", "shoulders",
                "wearing", "eyes")
OBJECT_WORDS = ("hull", "machine", "craft", "engine", "vehicle", "droid", "robot", "metal", "panel",
                "riveted", "wheels", "chassis", "cockpit", "blade", "weapon", "sword", "mount")


def master_kind(f, name):
    """The declared kind. Only ever what the spec says -- never a guess."""
    return ((f.get("master_views") or {}).get(name) or {}).get("kind")


def kind_guess(f, name):
    """A suggestion for the error message only. Deliberately not used to render anything.

    Word-counting the lock is not reliable enough to act on: 'dune faces' reads as a person and a
    character lock that lives under `subject` rather than the master's own name reads as nothing. A
    suggestion that is wrong a fifth of the time is useful in a prompt to the author and unacceptable as
    a silent default -- which is exactly how the skiff turnaround became a man holding a model aeroplane.
    """
    locks = (f.get("_scenes") or {}).get("locks") or {}
    text = (locks.get(name) or locks.get("subject") or "").lower()
    p = sum(w in text for w in PERSON_WORDS)
    o = sum(w in text for w in OBJECT_WORDS)
    return "person" if p > o else "object" if o else "?"


def cmd_views(f, args):
    """Turn a picked master into a model sheet: turnaround, head, expressions, optional detail.

    A shot's still.ref can only carry what the reference shows. A frontal master gives the model nothing
    to copy for a profile or a back, so it invents one and the subject changes between shots. With a
    sheet, each shot references the view that matches its framing: seed/<name>_side.png for a profile
    shot, _back.png for a back view, _expr_smile.png for the face shot.
    """
    names = [a for a in args if not a.startswith("--")] or list(f.get("masters", {}))
    locks = (f.get("_scenes") or {}).get("locks") or {}
    rc = 0
    for name in names:
        spec_views = (f.get("master_views") or {}).get(name) or {}
        master = d(f, f.get("masters", {}).get(name, f"seed/{name}.png"))
        if not spec_views.get("skip") and not master.exists():
            print(f"{name}: no master yet -- run `masters` and `pick {name} <seed>` first")
            rc |= 1
            continue
        subject = locks.get(name) or locks.get("subject") or f"the same {name}"
        env = {"SUBJECT": subject, "SEED": "1"}
        if spec_views.get("skip"):
            # An environment has no turnaround: a location needs camera angles and times of day, not a
            # rotation. Rotating `yard` or `dunes` produces nonsense.
            print(f"{name}: skipped (environment -- no turnaround)")
            continue
        kind = master_kind(f, name)
        if kind not in ("person", "object"):
            print(f'{name}: master_views.{name}.kind is not set -- add "person" or "object" '
                  f'(looks like "{kind_guess(f, name)}", but this is not guessed at render time)')
            rc |= 1
            continue
        env["KIND"] = kind
        if kind == "object":
            env["EXPR"] = ""
        for k in ("VIEWS", "VIEWS_CCW", "EXPR", "DETAIL", "BACKDROP", "KIND"):
            if spec_views.get(k.lower()) is not None:
                env[k] = spec_views[k.lower()]
        # every combined plate this subject appears in joins its sheet, so one picture shows every way
        # the subject has to stay the same -- alone and alongside the other locked things
        extra = [str(d(f, f"seed/{cn}.png")) for cn, cs in (f.get("combos") or {}).items()
                 if name in (cs.get("ref"), cs.get("input")) or f"{name}_" in cn or f"_{name}" in cn]
        extra = [x for x in extra if Path(x).exists()]
        if extra:
            env["EXTRA"] = " ".join(extra)
        # an object has no expressions; a person does
        if "EXPR" not in env and name not in ("subject",) and not locks.get("subject", "").startswith(
                str(subject)[:20]):
            if name in ("kyle", "lindsey", "ivy") or "boy" in subject or "girl" in subject:
                env["EXPR"] = "neutral alert smile"
            else:
                env["EXPR"] = ""
        rc |= run([S / "model_sheet.sh", master, d(f, f"seed/{name}"), subject, "1"], env)
    return rc



def image_palette(path, bins=4):
    """A normalised 3-D RGB histogram: the subject's materials and colours, independent of pose.

    A turnaround legitimately changes silhouette between views, so shape cannot be compared across them.
    Palette can: the droid's rust, its blue and its white are the same from every angle, and a view that
    drifted off-design shows up as a palette that no longer matches the hero view.
    """
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        return None
    a = np.asarray(Image.open(path).convert("RGB").resize((160, 160)), dtype=float) / 255.0
    idx = np.clip((a * bins).astype(int), 0, bins - 1)
    flat = idx[..., 0] * bins * bins + idx[..., 1] * bins + idx[..., 2]
    h = np.bincount(flat.ravel(), minlength=bins ** 3).astype(float)
    return h / max(h.sum(), 1.0)


def palette_distance(p, q):
    """Chi-square distance between two palettes; 0 is identical, ~1 is unrelated."""
    import numpy as np
    p, q = np.asarray(p), np.asarray(q)
    d = ((p - q) ** 2 / (p + q + 1e-9)).sum()
    return float(min(d, 2.0) / 2.0)


def cmd_eval(f, args):
    """Score consistency: each master's views against its hero, and each picked still against its ref.

    Catches the failure that produced a different craft in every shot -- a view or a still whose palette
    has drifted away from the master it is supposed to match.
    """
    try:
        import numpy as np  # noqa: F401
    except ImportError:
        die("eval needs numpy (pip3 install numpy)")
    masters = f.get("masters", {})
    names = [a for a in args if not a.startswith("--")]
    # Calibrated on the kyle_firstflight droid: a consistent turnaround sits at 0.006-0.010, a different
    # object on the same backdrop at 0.216, an unrelated image at 0.753. 0.06 is well clear of noise.
    thresh = float(flag("--thresh", 0.06))
    worst = 0.0

    print("masters — views compared pairwise (outlier = the view that wandered):")
    for name, rel in masters.items():
        if names and name not in names:
            continue
        hero = d(f, rel)
        if not hero.exists():
            continue
        views = sorted(d(f, "seed").glob(f"{name}_*.png"))
        views = [v for v in views if not re.search(r"_(c\d+|sheet|model|expr_\w+)$", v.stem)]
        if len(views) < 2:
            print(f"  {name}: no views yet -- run `views {name}`")
            continue
        # Views are compared against EACH OTHER, not against the hero: the hero is often rendered in a
        # location while the views share a studio backdrop, and that background difference swamps any
        # real design drift. Pairwise among views holds the backdrop constant, so what is left is the
        # subject. The outlier is the view that wandered.
        pal = {v: image_palette(v) for v in views}
        means = {v: sum(palette_distance(pal[v], pal[w]) for w in views if w is not v) / (len(views) - 1)
                 for v in views}
        for v in views:
            worst = max(worst, means[v])
            mark = "  OUTLIER" if means[v] > thresh else ""
            print(f"  {name:10} {v.stem.replace(name + '_', ''):16} {means[v]:.3f}{mark}")

    # A still is a scene and its master is a studio plate, so part of any distance here is background
    # rather than drift. Treat it as a ranking, not a verdict: the shot furthest from its own reference
    # is the one to look at first.
    print("stills — each picked still against the master it references (ranking, not a verdict):")
    rows = []
    for s in f["shots"]:
        still = d(f, f"stills/{s['id']}.png")
        ref = s.get("still", {}).get("ref") or s.get("qc_ref")
        # Score against whatever the shot actually referenced -- a model-sheet view or a combo, not
        # only a plain master. Looking the ref up in the masters dict scored 1 shot in 8 on
        # kyle_firstflight v2 and silently skipped every view and combo, which are the references
        # that carry identity in the first place.
        if not still.exists() or not ref:
            continue
        rp = resolve_ref(f, ref)
        if not rp or not rp.exists():
            continue
        rows.append((palette_distance(image_palette(rp), image_palette(still)), s["id"], ref))
    for dist, sid, ref in sorted(rows, reverse=True):
        print(f"  {sid:10} vs {ref:12} {dist:.3f}")
    if rows:
        print(f"  (worst first. A scene is not a studio plate, so part of every number here is "
              f"background -- use it to choose what to look at, not to fail a shot.)")
    return 0


def cmd_combos(f, args):
    """Render combined masters: the character in the vehicle, holding the weapon, on the mount.

    A shot showing two locked things together has to keep both, and neither single master shows the
    pair. The diptych carries one reference on the left and the scene on the right, so a combo is
    rendered with the character as REF and the object as IN, then becomes a reference in its own right.

    Spec block:  "combos": {"kyle_in_skiff": {"ref": "kyle", "input": "skiff", "prompt": "..."}}
    """
    combos = f.get("combos") or {}
    if not combos:
        print("no run-spec.combos block")
        return 0
    names = [a for a in args if not a.startswith("--")] or list(combos)
    c = still_cfg(f, {})
    trig = trigger_of(f)
    rc = 0
    for name in names:
        spec = combos.get(name) or die(f"no combo '{name}'")
        a = resolve_ref(f, spec.get("ref"))
        b = resolve_ref(f, spec.get("input")) if spec.get("input") else None
        # Use dt_diptych's diptych mode as designed: REF on the left carries identity, IN on the right is
        # the thing being edited, and the right half is kept. The earlier attempt to compose the pair by
        # hand and run a single-image edit bypassed that and produced two subjects standing side by side.
        #
        # The prompt has to be an EDIT INSTRUCTION that names the halves, not a scene description. A
        # description asks the model to invent a composition from nothing; an instruction tells it what to
        # do with the pixels it already has. wiki/headless-cli-pipeline.md records the working form:
        # "Two images side by side ... re-render the right image ... keep the left image unchanged".
        ref = resolve_ref(f, spec.get("ref"))
        inp = resolve_ref(f, spec.get("input")) if spec.get("input") else None
        cfg = dict(c["config"])
        if trig and trig not in (spec.get("prompt") or "").lower():
            cfg.pop("loras", None)
        # Strength is the lever for a combo. At 1.0 klein regenerates both subjects from the text and
        # only the one with a LoRA survives -- the droid came back as a different machine every seed.
        # Below 1.0 the edit stays closer to the composed reference, so the subject with no adapter
        # keeps its design. Per-combo so a character-only combo can still run hot.
        env = {"MODEL": c["model"], "STEPS": c["steps"], "CFG": c["cfg"],
               "STRENGTH": spec.get("strength", c["strength"]),
               "CONFIG_JSON": json.dumps(cfg, separators=(",", ":"))}
        # A combo may chain off another combo (the crew shot edits the boy-in-skiff, not the bare skiff).
        # The parent has to be PICKED, not merely rendered, because resolve_ref points at seed/<name>.png
        # and only `pick` writes that file. Failing here names the missing step; rendering against a
        # non-existent reference silently produces a text-to-image guess instead.
        for role, path in (("ref", ref), ("input", inp)):
            src_name = spec.get(role)
            if path and not path.exists():
                hint = (f"run `pick {src_name} <seed>` first" if src_name in (f.get("combos") or {})
                        else f"render it first")
                die(f"combo '{name}': {role} '{src_name}' missing at {path.relative_to(ROOT)} -- {hint}")
        pf = prompt_path(f, f"combo_{name}", spec["prompt"])
        for seed in c["seeds"]:
            out = d(f, f"seed/{name}_c{seed}.png")
            if out.exists() and not FORCE:
                continue
            rc |= run([S / "dt_diptych.sh", ref or "-", inp or "-", pf, out, seed, *c["size"]], env)
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
    # a sheet tiles candidates for a shot, a master or a combo -- anything that produced seed/<x>_c<n>.png
    pos = [a for a in args if not a.startswith("--")]
    extra = [p for p in pos if p in (f.get("masters") or {}) or p in (f.get("combos") or {})]
    shots = [s["id"] for s in ids_arg(f, [a for a in args if a not in extra])] if not extra or \
        [a for a in pos if a not in extra] else []
    for i in (extra or shots) if extra else shots:
        cands = sorted(d(f, "seed").glob(f"{i}_c*.png"),
                       key=lambda q: int(re.sub(r"\D", "", q.stem.split("_c")[-1]) or 0))
        if not cands:
            print(f"{i}: no candidates")
            continue
        # A master is a studio plate: the pale backdrop that signals bloom risk in a scene is the point
        # here, so the flag is suppressed rather than fired on every master and trained into noise.
        is_plate = i in (f.get("masters") or {}) or i in (f.get("combos") or {})
        mets = {q: image_metrics(q) for q in cands}
        best = max((m["sharp"] for m in mets.values() if m), default=0.0)
        ims = []
        for q in cands:
            im = Image.open(q).convert("RGB")
            im = im.resize((tile_w, round(im.height * tile_w / im.width)), Image.LANCZOS)
            seed = q.stem.split("_c")[-1]
            cap = f"c{seed}" + metric_label(mets[q], best, plate=is_plate)
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
            bright = [] if is_plate else [q.stem.split("_c")[-1] for q in cands
                                          if mets[q] and mets[q]["bg"] > 150]
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
    # A combo is a master in every way that matters -- it is referenced by shots and by other combos --
    # but it lives at seed/<name>.png, which is where resolve_ref looks for it. Picking one into
    # stills/ put it somewhere nothing reads, and a chained combo then rendered against a missing parent.
    if i in masters:
        dst = d(f, masters[i])
    elif i in (f.get("combos") or {}):
        dst = d(f, f"seed/{i}.png")
    else:
        dst = d(f, f"stills/{i}.png")
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


CMDS = {"check": cmd_check, "status": cmd_status, "lint": cmd_lint, "masters": cmd_masters, "views": cmd_views, "combos": cmd_combos, "eval": cmd_eval, "stills": cmd_stills, "sheet": cmd_sheet, "pick": cmd_pick,
        "clips": cmd_clips, "qc": cmd_qc, "finish": cmd_finish}

if __name__ == "__main__":
    pos = [a for a in sys.argv[1:] if a not in ("--dry-run", "--force")]
    if len(pos) < 2 or pos[1] not in CMDS:
        print(__doc__)
        sys.exit(2)
    spec = load(pos[0])
    sys.exit(CMDS[pos[1]](spec, pos[2:]))
