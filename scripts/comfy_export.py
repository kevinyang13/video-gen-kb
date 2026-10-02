#!/usr/bin/env python3
"""Export a project's spec.json as ComfyUI workflows you can open in the app.

    scripts/comfy_export.py PROJECT [-o OUT_DIR]

PROJECT is <id> (newest version) or <id>@<version>, same as film_run.py.

Writes three files into OUT_DIR (default projects/<id>/<version>/comfy/):
    <id>_still.json   FLUX.2 [klein] text-to-image + LoRA  -- open in ComfyUI
    <id>_i2v.json     LTX-Video image-to-video             -- open in ComfyUI
    <id>_shots.json   every shot's prompts, weights and trims as plain data

The two workflow files are ComfyUI UI-format graphs: Workflow > Open, or drag
the file onto the canvas. Each carries shot s1 loaded into its prompt boxes and
a Note node holding all eight shots, so switching shot is copy and paste.

Model filenames are what the loaders expect to find in ComfyUI's models/
folders. They will not match a fresh install -- see comfy/README.md.
"""
import json, sys, os, glob, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve(project):
    """<id> -> newest version dir; <id>@<version> -> that one."""
    if "@" in project:
        pid, ver = project.split("@", 1)
        return pid, os.path.join(ROOT, "projects", pid, ver)
    pid = project
    cands = sorted(glob.glob(os.path.join(ROOT, "projects", pid, "v*")))
    if not cands:
        sys.exit(f"no version dir under projects/{pid}")
    return pid, cands[-1]


# ---------------------------------------------------------------- graph building
class Graph:
    """Minimal ComfyUI UI-format graph builder.

    ComfyUI stores links twice -- once in a flat top-level list and once on the
    ports themselves -- and refuses to open a file where the two disagree, so
    both are written from the same call here rather than by hand.
    """

    def __init__(self):
        self.nodes, self.links, self._nid, self._lid = [], [], 0, 0

    def node(self, type_, pos, widgets=None, inputs=None, outputs=None, size=None,
             title=None, color=None):
        self._nid += 1
        n = {
            "id": self._nid,
            "type": type_,
            "pos": list(pos),
            "size": list(size or [340, 120]),
            "flags": {},
            "order": self._nid - 1,
            "mode": 0,
            "inputs": [{"name": i[0], "type": i[1], "link": None} for i in (inputs or [])],
            "outputs": [{"name": o[0], "type": o[1], "links": [], "slot_index": k}
                        for k, o in enumerate(outputs or [])],
            "properties": {"Node name for S&R": type_},
            "widgets_values": widgets or [],
        }
        if title:
            n["title"] = title
        if color:
            n["color"], n["bgcolor"] = color[0], color[1]
        self.nodes.append(n)
        return n

    def link(self, src, src_slot, dst, dst_slot):
        self._lid += 1
        t = src["outputs"][src_slot]["type"]
        self.links.append([self._lid, src["id"], src_slot, dst["id"], dst_slot, t])
        src["outputs"][src_slot]["links"].append(self._lid)
        dst["inputs"][dst_slot]["link"] = self._lid
        return self._lid

    def out(self, extra=None):
        return {
            "last_node_id": self._nid,
            "last_link_id": self._lid,
            "nodes": self.nodes,
            "links": self.links,
            "groups": [],
            "config": {},
            "extra": extra or {},
            "version": 0.4,
        }


def note(g, pos, text, size=(560, 420), title="Notes"):
    return g.node("Note", pos, widgets=[text], size=size, title=title,
                  color=["#432", "#653"])


# ---------------------------------------------------------------- still workflow
def still_workflow(pid, spec, shots):
    """FLUX.2 [klein]: UNET + CLIP + VAE loaders -> LoRA -> sampler -> save.

    CFG is 1.0 because klein is distilled, so the negative branch is a
    ConditioningZeroOut rather than a second prompt -- at CFG 1 the sampler
    never evaluates it, and a real negative prompt there would be dead weight
    that reads as if it were doing something.
    """
    st = spec.get("still", {})
    s1 = shots[0]
    g = Graph()

    # weight_dtype MUST stay "default" on Apple Silicon. MPS has no float8 kernel,
    # so fp8_e4m3fn raises "Trying to convert Float8_e4m3fn to the MPS backend"
    # the moment the sampler touches a weight -- it loads fine and dies at step 0.
    unet = g.node("UNETLoader", [40, 40], ["flux2-klein-9b.safetensors", "default"],
                  outputs=[("MODEL", "MODEL")], size=[340, 82],
                  title="FLUX.2 [klein] 9B  (dtype: default -- MPS has no fp8)")
    clip = g.node("CLIPLoader", [40, 170], ["mistral3_flux2_text_encoder.safetensors", "flux2", "default"],
                  outputs=[("CLIP", "CLIP")], size=[340, 106],
                  title="FLUX.2 text encoder")
    vae = g.node("VAELoader", [40, 320], ["flux2-vae.safetensors"],
                 outputs=[("VAE", "VAE")], size=[340, 58], title="FLUX.2 VAE")

    lora = g.node("LoraLoaderModelOnly", [420, 40],
                  [spec_lora_name(st), s1["lora_weight"]],
                  inputs=[("model", "MODEL")], outputs=[("MODEL", "MODEL")],
                  size=[340, 82], title="LoRA  (see README -- needs conversion)")

    shift = g.node("ModelSamplingSD3", [420, 170], [float(st.get("shift", 3))],
                   inputs=[("model", "MODEL")], outputs=[("MODEL", "MODEL")],
                   size=[340, 58], title=f"shift {st.get('shift', 3)}")

    pos = g.node("CLIPTextEncode", [420, 270], [s1["still"]],
                 inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")],
                 size=[520, 300], title=f"{s1['id']} -- still prompt",
                 color=["#232", "#353"])
    neg = g.node("ConditioningZeroOut", [420, 600], [],
                 inputs=[("conditioning", "CONDITIONING")],
                 outputs=[("CONDITIONING", "CONDITIONING")], size=[340, 30],
                 title="negative (unused at CFG 1)")

    w, h = [int(x) for x in st.get("size", "1024x576").split("x")]
    lat = g.node("EmptySD3LatentImage", [420, 680], [w, h, 1],
                 outputs=[("LATENT", "LATENT")], size=[340, 106],
                 title=f"{w}x{h}")

    ks = g.node("KSampler", [990, 270],
                [1, "fixed", int(st.get("steps", 4)), float(st.get("cfg", 1.0)),
                 "euler", "ddim_uniform", 1.0],
                inputs=[("model", "MODEL"), ("positive", "CONDITIONING"),
                        ("negative", "CONDITIONING"), ("latent_image", "LATENT")],
                outputs=[("LATENT", "LATENT")], size=[340, 262],
                title=f"{st.get('steps', 4)} steps / CFG {st.get('cfg', 1.0)}")

    dec = g.node("VAEDecode", [1370, 270], [],
                 inputs=[("samples", "LATENT"), ("vae", "VAE")],
                 outputs=[("IMAGE", "IMAGE")], size=[210, 46])
    sav = g.node("SaveImage", [1370, 360], [f"{pid}/{s1['id']}"],
                 inputs=[("images", "IMAGE")], size=[420, 450])

    g.link(unet, 0, lora, 0)
    g.link(lora, 0, shift, 0)
    g.link(shift, 0, ks, 0)
    g.link(clip, 0, pos, 0)
    g.link(pos, 0, neg, 0)
    g.link(pos, 0, ks, 1)
    g.link(neg, 0, ks, 2)
    g.link(lat, 0, ks, 3)
    g.link(ks, 0, dec, 0)
    g.link(vae, 0, dec, 1)
    g.link(dec, 0, sav, 0)

    note(g, [990, 620], still_note(spec, shots), size=(620, 760),
         title="All 8 shots -- paste into the prompt box")
    return g.out({"video_gen_kb": {"project": pid, "stage": "still"}})


def spec_lora_name(st):
    raw = st.get("lora", "")
    base = raw.split("@")[0].strip() or "lora.safetensors"
    return base.replace("_lora_f32.ckpt", ".safetensors").replace(".ckpt", ".safetensors")


def still_note(spec, shots):
    st = spec.get("still", {})
    out = [
        f"STILL STAGE -- {spec.get('title', '')}",
        f"model {st.get('model')} | {st.get('size')} | steps {st.get('steps')} | "
        f"CFG {st.get('cfg')} | shift {st.get('shift')} | sampler {st.get('sampler')}",
        "",
        "LoRA weight is PER SHOT. Set it on the LoraLoaderModelOnly node each time.",
        "Render 5 seeds per shot and pick -- one seed in five is often the only correct one.",
        "", "=" * 64, "",
    ]
    for s in shots:
        out += [f"--- {s['id']}  (LoRA {s['lora_weight']}) {s['title']}",
                "", s["still"], ""]
    return "\n".join(out)


# ---------------------------------------------------------------- i2v workflow
def i2v_workflow(pid, spec, shots):
    """LTX-Video image-to-video.

    Node class names here come from the ComfyUI-LTXVideo pack and have changed
    between releases of it; the README says what to swap if a node loads red.
    No LoRA is attached on purpose -- LTX never sees one, which is why identity
    is fixed entirely at the still.
    """
    iv = spec.get("i2v", {})
    s1 = shots[0]
    g = Graph()

    ck = g.node("CheckpointLoaderSimple", [40, 40], ["ltx-2.3-22b-distilled.safetensors"],
                outputs=[("MODEL", "MODEL"), ("CLIP", "CLIP"), ("VAE", "VAE")],
                size=[380, 98], title="LTX-2.3 22B [distilled]")
    clip = g.node("CLIPLoader", [40, 180], ["t5xxl_fp16.safetensors", "ltxv", "default"],
                  outputs=[("CLIP", "CLIP")], size=[380, 106],
                  title="T5 text encoder")
    img = g.node("LoadImage", [40, 330], [f"{s1['id']}.png", "image"],
                 outputs=[("IMAGE", "IMAGE"), ("MASK", "MASK")], size=[380, 390],
                 title="the picked still")

    pos = g.node("CLIPTextEncode", [460, 40], [s1["video"]],
                 inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")],
                 size=[500, 220], title=f"{s1['id']} -- motion prompt",
                 color=["#232", "#353"])
    neg = g.node("CLIPTextEncode", [460, 290],
                 ["worst quality, blurry, jittery, distorted, warping, morphing face"],
                 inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")],
                 size=[500, 140], title="negative", color=["#322", "#533"])

    w, h = [int(x) for x in iv.get("size", "1024x576").split("x")]
    i2v = g.node("LTXVImgToVideo", [460, 460],
                 [w, h, int(iv.get("frames", 249)), 1, 0.15],
                 inputs=[("positive", "CONDITIONING"), ("negative", "CONDITIONING"),
                         ("vae", "VAE"), ("image", "IMAGE")],
                 outputs=[("positive", "CONDITIONING"), ("negative", "CONDITIONING"),
                          ("latent", "LATENT")],
                 size=[380, 170], title=f"{iv.get('frames', 249)} frames")

    cond = g.node("LTXVConditioning", [880, 460], [float(iv.get("fps", 25))],
                  inputs=[("positive", "CONDITIONING"), ("negative", "CONDITIONING")],
                  outputs=[("positive", "CONDITIONING"), ("negative", "CONDITIONING")],
                  size=[300, 82], title=f"{iv.get('fps', 25)} fps")

    sch = g.node("LTXVScheduler", [880, 580],
                 [int(iv.get("steps", 8)), 2.05, 0.95, True, float(iv.get("shift", 5.0))],
                 inputs=[("latent", "LATENT")], outputs=[("SIGMAS", "SIGMAS")],
                 size=[300, 154], title=f"{iv.get('steps', 8)} steps / shift {iv.get('shift', 5.0)}")

    smp = g.node("KSamplerSelect", [880, 770], ["euler"],
                 outputs=[("SAMPLER", "SAMPLER")], size=[300, 58])
    guide = g.node("LTXVAddGuide", [1220, 40], [], size=[300, 58],
                   title="(optional) stronger first-frame hold")
    guide["mode"] = 4  # bypassed by default

    cs = g.node("SamplerCustom", [1240, 300],
                [True, 1, "fixed", float(iv.get("cfg", 1.0))],
                inputs=[("model", "MODEL"), ("positive", "CONDITIONING"),
                        ("negative", "CONDITIONING"), ("sampler", "SAMPLER"),
                        ("sigmas", "SIGMAS"), ("latent_image", "LATENT")],
                outputs=[("output", "LATENT"), ("denoised_output", "LATENT")],
                size=[320, 230], title=f"CFG {iv.get('cfg', 1.0)}")

    dec = g.node("VAEDecode", [1600, 300], [],
                 inputs=[("samples", "LATENT"), ("vae", "VAE")],
                 outputs=[("IMAGE", "IMAGE")], size=[210, 46])
    vid = g.node("SaveWEBM", [1600, 390],
                 [f"{pid}/{s1['id']}", "vp9", float(iv.get("fps", 25)), 10],
                 inputs=[("images", "IMAGE")], size=[380, 160],
                 title="save -- or swap for VHS_VideoCombine")

    g.link(ck, 0, cs, 0)
    g.link(ck, 2, i2v, 2)
    g.link(ck, 2, dec, 1)
    g.link(clip, 0, pos, 0)
    g.link(clip, 0, neg, 0)
    g.link(pos, 0, i2v, 0)
    g.link(neg, 0, i2v, 1)
    g.link(img, 0, i2v, 3)
    g.link(i2v, 0, cond, 0)
    g.link(i2v, 1, cond, 1)
    g.link(i2v, 2, sch, 0)
    g.link(i2v, 2, cs, 5)
    g.link(cond, 0, cs, 1)
    g.link(cond, 1, cs, 2)
    g.link(smp, 0, cs, 3)
    g.link(sch, 0, cs, 4)
    g.link(cs, 0, dec, 0)
    g.link(dec, 0, vid, 0)

    note(g, [1240, 580], i2v_note(spec, shots), size=(660, 780),
         title="All 8 motion prompts + trims")
    return g.out({"video_gen_kb": {"project": pid, "stage": "i2v"}})


def i2v_note(spec, shots):
    iv = spec.get("i2v", {})
    out = [
        f"I2V STAGE -- {spec.get('title', '')}",
        f"model {iv.get('model')} | {iv.get('size')} | {iv.get('frames')} frames @ "
        f"{iv.get('fps')} fps | steps {iv.get('steps')} | CFG {iv.get('cfg')} | "
        f"shift {iv.get('shift')}",
        "",
        "NO LoRA at this stage. LTX never sees it -- identity is fixed at the still,",
        "and nothing renews it across the clip. That is why frontal face shots are",
        "cut at ~7 s: they drift at about eight seconds whatever the prompt says.",
        "",
        "Negative instructions do not work. 'She does not turn her head' failed twice.",
        "Only the still and the cut length control the result.",
        "", "=" * 64, "",
    ]
    for s in shots:
        out += [f"--- {s['id']}  (keep {s['trim']} s) {s['title']}", "", s["video"], ""]
    return "\n".join(out)


# ---------------------------------------------------------------- shot data
def parse_note(n):
    """Pull LoRA weight and kept length out of the free-text note field."""
    lw, trim = 1.0, None
    if "no LoRA" in n:
        lw = 0.0
    else:
        for tok in n.replace(";", " ").split():
            pass
    import re
    m = re.search(r"LoRA weight ([\d.]+)", n)
    if m:
        lw = float(m.group(1))
    elif "no LoRA" in n:
        lw = 0.0
    m = re.search(r"kept ([\d.]+) s", n)
    if m:
        trim = float(m.group(1))
    m = re.search(r"input (\S+\.png)", n)
    return lw, trim, (m.group(1) if m else None)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    project = args[0]
    out_dir = None
    if "-o" in args:
        out_dir = args[args.index("-o") + 1]

    pid, vdir = resolve(project)
    spec = json.load(open(os.path.join(vdir, "spec.json")))
    sc = spec["scenes"]

    shots = []
    for k in sorted([x for x in sc if x.startswith("s") and x[1:].isdigit()],
                    key=lambda x: int(x[1:])):
        v = sc[k]
        lw, trim, src = parse_note(v.get("note", ""))
        shots.append({"id": k, "title": v.get("title", ""), "still": v.get("still", ""),
                      "video": v.get("video", ""), "lora_weight": lw,
                      "trim": trim, "input": src, "note": v.get("note", "")})

    out_dir = out_dir or os.path.join(vdir, "comfy")
    os.makedirs(out_dir, exist_ok=True)

    w1 = os.path.join(out_dir, f"{pid}_still.json")
    w2 = os.path.join(out_dir, f"{pid}_i2v.json")
    w3 = os.path.join(out_dir, f"{pid}_shots.json")
    json.dump(still_workflow(pid, spec, shots), open(w1, "w"), indent=1)
    json.dump(i2v_workflow(pid, spec, shots), open(w2, "w"), indent=1)
    json.dump({"project": pid, "version": os.path.basename(vdir),
               "title": spec.get("title"), "still": spec.get("still"),
               "i2v": spec.get("i2v"), "post": spec.get("post"),
               "locks": sc.get("locks"), "shots": shots},
              open(w3, "w"), indent=1)
    for p in (w1, w2, w3):
        print(f"  wrote {os.path.relpath(p, ROOT)}")


if __name__ == "__main__":
    main()
