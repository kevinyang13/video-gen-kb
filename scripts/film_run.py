#!/usr/bin/env python3
"""Run a multi-shot film from its run-spec in projects.json (the `run-spec` block of a project).

PROJECT is a projects.json id, or a path to a .json file holding the run-spec (handy for tests).
  scripts/film_run.py PROJECT check              validate the run-spec (paths, sizes, frame rules)
  scripts/film_run.py PROJECT status             one line per shot: still / candidates / clips / take / 4K
  scripts/film_run.py PROJECT stills [ids]       seed candidates for shots with no picked still -> work/<id>_c<seed>.png
  scripts/film_run.py PROJECT pick ID SEED       candidate -> stills/<id>.png
  scripts/film_run.py PROJECT clips [ids] [--v N] [--seed S]   clips/<id>_v<N>.mov for shots with a still
  scripts/film_run.py PROJECT qc [ids] [--v N]   contact sheets work/<id>_v<N>_qc.png (ref = master or still)
  scripts/film_run.py PROJECT finish [--force]   trim takes -> upscale -> assemble (+music) -> delivery copies
Global flags: --dry-run (print commands), --force (redo existing outputs).

Run-spec (all paths relative to run-spec.dir; every block optional except dir, size, shots):
  "run-spec": {
    "dir": "raw/clips/<project>", "name": "<film file stem>", "size": [576, 1024],
    "still":   {"model": ..., "steps": 4, "cfg": 1, "config": {...}, "seeds": [1, 2, 3], "strength": 1.0},
    "clip":    {"model": ..., "frames": 249, "steps": 8, "cfg": 1, "config": {...}, "seed": 1, "video_format": "prores422hq"},
    "masters": {"kyle": "masters/kyle_front.png"},          # names usable as a shot's still.ref and qc_ref
    "upscale": {"model": "realesrgan-x4plus", "size": [2160, 3840], "fit": "crop", "bitrate": "40M"},
    "assemble":{"fps": 25, "xfade": 0.75, "clip_audio": false, "bitrate": "40M"},
    "music":   {"file": "raw/clips/music/x.mp3", "start": "tail", "vol": 1.0, "fade_in": 1.5, "fade_out": 0},
    "deliver": [{"size": [1080, 1920], "bitrate": "12M"}, {"size": [720, 1280], "bitrate": "2.8M"}],
    "shots": [
      {"id": "s2",
       "still": {"ref": "kyle" | "stills/s1.png" | null, "input": "work/s2_in.png" | null, "prompt": "stills/s2.txt",
                 "seeds": [...], "size": [w, h]},             # ref+input = diptych, input only = edit, neither = text
       "video_prompt": "stills/s2_v.txt", "clip": {...overrides...},
       "qc_ref": "kyle", "take": "clips/s2_v2.mov", "trim": [0, 8]}
    ]}
music.file is relative to the repo root. Takes/trims are what `finish` cuts; set them after QC.
"""
import json, os, shlex, shutil, subprocess, sys
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
        data = json.loads((ROOT / "projects.json").read_text())
        p = next((x for x in data["projects"] if x["id"] == project), None)
        if not p:
            die(f"no project '{project}' in projects.json")
        f = p.get("run-spec") or die(f"project '{project}' has no 'run-spec' block")
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

def cmd_check(f, _):
    errs, warns = [], []
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
        for k in ("prompt",):
            if st and k in st and not d(f, st[k]).exists():
                errs.append(f"{i}: still.{k} missing: {st[k]}")
        if st.get("input") and not d(f, st["input"]).exists():
            warns.append(f"{i}: still.input not made yet: {st['input']}")
        ref = st.get("ref")
        if ref and ref not in f.get("masters", {}) and not ref.startswith(("stills/", "masters/", "work/")):
            errs.append(f"{i}: still.ref '{ref}' is neither a master name nor a path")
        if not s.get("video_prompt") or not d(f, s["video_prompt"]).exists():
            errs.append(f"{i}: video_prompt missing: {s.get('video_prompt')}")
        if "trim" in s:
            a, b = s["trim"]
            if not 0 <= a < b:
                errs.append(f"{i}: bad trim {s['trim']}")
        if s.get("take") and not d(f, s["take"]).exists():
            warns.append(f"{i}: take not rendered yet: {s['take']}")
    total = sum(s["trim"][1] - s["trim"][0] for s in f["shots"] if "trim" in s)
    if total:
        xf = f.get("assemble", {}).get("xfade", 0.5)
        n = sum(1 for s in f["shots"] if "trim" in s)
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
            out = d(f, f"work/{i}_c{seed}.png")
            if out.exists() and not FORCE:
                continue
            rc |= run([S / "dt_diptych.sh", ref or "-", inp or "-", d(f, st["prompt"]), out, seed, *c["size"]], env)
    return rc


def cmd_pick(f, args):
    pos = [a for a in args if not a.startswith("--")]
    if len(pos) != 2:
        die("usage: pick ID SEED")
    i, seed = pos
    src, dst = d(f, f"work/{i}_c{seed}.png"), d(f, f"stills/{i}.png")
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
        rc |= run([S / "dt_clip.sh", still, d(f, s["video_prompt"]), d(f, f"clips/{i}_v{v}.mov"), seed, w, h], env)
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
        rc |= run([S / "qc_sheet.sh", clip, d(f, f"work/{i}_v{v}_qc.png"), ref if ref.exists() else "-"])
    return rc


def cmd_finish(f, _):
    up = {"model": "realesrgan-x4plus", "size": [3840, 2160], "fit": "crop", "bitrate": "40M", **f.get("upscale", {})}
    asm = {"fps": 25, "xfade": 0.5, "clip_audio": True, "bitrate": up["bitrate"], **f.get("assemble", {})}
    shots = [s for s in f["shots"] if s.get("take") and s.get("trim")]
    missing = [s["id"] for s in f["shots"] if s not in shots]
    if missing:
        die(f"shots without take/trim: {', '.join(missing)} — set them after QC")
    fin = ROOT / f["dir"] / "final"
    fin.mkdir(parents=True, exist_ok=True)
    W, H = up["size"]
    outs = []
    for s in shots:
        i, (a, b) = s["id"], s["trim"]
        k4, stamp = fin / f"{i}_4k.mp4", fin / f"{i}_trim.txt"
        key = f"{s['take']} {a} {b} {up['model']} {W}x{H} {up['fit']}"
        if k4.exists() and stamp.exists() and stamp.read_text() == key and not FORCE:
            print(f"{i}: 4K up to date")
        else:
            t = fin / f"{i}_t.mov"
            rc = run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", d(f, s["take"]), "-vf",
                      f"trim=start={a}:end={b},setpts=PTS-STARTPTS", "-af", f"atrim=start={a}:end={b},asetpts=PTS-STARTPTS",
                      "-c:v", "prores_ks", "-profile:v", "3", "-c:a", "pcm_s16le", t])
            rc = rc or run([S / "upscale_4k.sh", t, fin / i, up["model"]],
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


CMDS = {"check": cmd_check, "status": cmd_status, "stills": cmd_stills, "pick": cmd_pick,
        "clips": cmd_clips, "qc": cmd_qc, "finish": cmd_finish}

if __name__ == "__main__":
    pos = [a for a in sys.argv[1:] if a not in ("--dry-run", "--force")]
    if len(pos) < 2 or pos[1] not in CMDS:
        print(__doc__)
        sys.exit(2)
    spec = load(pos[0])
    sys.exit(CMDS[pos[1]](spec, pos[2:]))
