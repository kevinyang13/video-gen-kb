#!/usr/bin/env bash
# A production-style model sheet from one master: turnaround + head + expressions + detail,
# composed on a plain backdrop.
#   scripts/model_sheet.sh MASTER.png OUT_PREFIX "SUBJECT DESCRIPTION" [SEED]
#
# Why a sheet and not one image. A shot's `still.ref` can only carry what the reference shows: a frontal
# master gives the model nothing to copy for a profile or a back, so it invents one, and the craft or the
# face changes between shots. With a sheet you hand each shot the view that matches its framing.
#
# Two things the view order fixes:
#   * JANUS. A 90-degree turn straight from a frontal reference makes klein keep the front face and add a
#     profile beside it, ear in the middle. Rendering side from the THREE-QUARTER view instead of the
#     front halves the rotation at each step and largely avoids it.
#   * BACK VIEWS COME BACK FRONTAL unless the reference already shows that angle, so back is rendered
#     from side, not from front.
#
# Framing follows the reference and the canvas, not the prompt: body views use a tall canvas, head views
# a square one. Asking a head-and-shoulders reference for a "full body shot" returns head and shoulders.
#
#   BACKDROP  the backdrop clause, default a plain pale studio sweep. Keep a master on a plain backdrop:
#             a master shot in a location drags that location into every shot that references it.
#   VIEWS     body views, default "front 34 side back"
#   EXPR      expression heads, default "neutral alert worried"
#   DETAIL    optional extra view, e.g. "the hands holding the tool, close"
#   W H       body view size, default 512x768;  HW head size, default 640x640
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MASTER="${1:?master .png}"; OUT="${2:?output prefix}"; SUBJ="${3:-the same character}"; SEED="${4:-1}"
BACKDROP="${BACKDROP:-standing against a plain pale grey studio backdrop, soft even studio lighting from the front, no scenery and no props beyond those described}"
# A full rotation, not four cardinal angles. Rendered OUTWARD FROM THE FRONT IN BOTH DIRECTIONS rather
# than as one chain: each view references the previous one, so a single chain of eight accumulates eight
# steps of drift by the time it reaches the back. Going both ways makes the longest chain four.
VIEWS="${VIEWS:-front 45 90 135 180}"; VIEWS_CCW="${VIEWS_CCW:-315 270 225}"
EXPR="${EXPR-neutral alert worried}"
W="${W:-512}"; H="${H:-768}"; HW="${HW:-640}"
KEEP="exactly the same face, the same hair, the same colours and the same clothing, the same age, the same build, no change to the identity"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$(dirname "$OUT")"

# A person and an object need different view language. "Full-length from head to feet, arms relaxed at
# the sides" applied to a craft made klein supply a person to own the head and feet: the skiff turnaround
# came back as a man holding a model aeroplane. KIND=object drops every anatomical word and states that
# the frame holds no people.
# No default. A silent fallback to person language is what turned the skiff turnaround into a man
# holding a model aeroplane: every view rendered, nothing errored, and the fault was only visible after
# eight renders. Callers must say which template applies.
: "${KIND:?KIND must be set to person or object}"
case "$KIND" in person|object) ;; *) echo "model_sheet: KIND must be person or object, got '$KIND'" >&2; exit 2 ;; esac
obj_prompt () {
  local shot="$1"
  echo "$SUBJ, $KEEP. $shot The whole object is inside the frame from end to end with clear space around it, resting level, shown on its own with no people in frame and nobody holding it or standing beside it. $BACKDROP."
}
body_prompt () {
 if [ "$KIND" = "object" ]; then
  case "$1" in
    front) obj_prompt "A view of the front of the object, square to the camera." ;;
    45)    obj_prompt "A view rotated 45 degrees from the front." ;;
    90)    obj_prompt "A true side view seen from exactly 90 degrees, the full profile against the backdrop." ;;
    135)   obj_prompt "A view rotated 135 degrees, from behind and to one side." ;;
    180|back) obj_prompt "A view of the rear of the object, rotated a full 180 degrees from the front." ;;
    225)   obj_prompt "A view rotated 225 degrees, from behind and to the other side." ;;
    270)   obj_prompt "A true side view from exactly 90 degrees on the opposite side from the 90-degree view." ;;
    315)   obj_prompt "A view rotated 315 degrees, from the front and to the other side." ;;
    34)    obj_prompt "A three-quarter view from the front." ;;
    side)  obj_prompt "A true side view seen from exactly 90 degrees." ;;
    *)     obj_prompt "$1" ;;
  esac
  return
 fi
 case "$1" in
  front) echo "$SUBJ, $KEEP. A full-length view from head to feet, standing square to the camera and facing forward, arms relaxed at the sides, the whole body inside the frame with clear space above the head and below the feet. $BACKDROP." ;;
  34)    echo "$SUBJ, $KEEP. A full-length view from head to feet, the body rotated about 45 degrees to a three-quarter view, still looking toward the camera, the whole body inside the frame. $BACKDROP." ;;
  side)  echo "$SUBJ, $KEEP. A full-length true side profile seen from exactly 90 degrees, the body in line with the camera, the nose, lips and chin forming the outline against the backdrop, only ONE eye visible and the far side of the face hidden behind the near side. Exactly one face in the image. $BACKDROP." ;;
  back|180) echo "$SUBJ, $KEEP. A full-length view from directly behind, rotated a full 180 degrees, the back of the head, shoulders and legs toward the camera, the face turned fully away and not visible. $BACKDROP." ;;
  45)   echo "$SUBJ, $KEEP. A full-length view rotated 45 degrees to the left of front, a three-quarter front view, the whole body inside the frame. $BACKDROP." ;;
  90)   echo "$SUBJ, $KEEP. A full-length true side profile seen from exactly 90 degrees to the left, the body in line with the camera, the outline clean against the backdrop, only ONE eye visible and the far side hidden behind the near side. Exactly one face in the image. $BACKDROP." ;;
  135)  echo "$SUBJ, $KEEP. A full-length view rotated 135 degrees, a three-quarter view from behind and to the left, mostly the back with a sliver of the near cheek visible. $BACKDROP." ;;
  225)  echo "$SUBJ, $KEEP. A full-length view rotated 225 degrees, a three-quarter view from behind and to the right, mostly the back with a sliver of the near cheek visible. $BACKDROP." ;;
  270)  echo "$SUBJ, $KEEP. A full-length true side profile seen from exactly 90 degrees to the right, the opposite side from the 90-degree view, only ONE eye visible. Exactly one face in the image. $BACKDROP." ;;
  315)  echo "$SUBJ, $KEEP. A full-length view rotated 315 degrees, a three-quarter front view from the right, the whole body inside the frame. $BACKDROP." ;;
  *)     echo "$SUBJ, $KEEP. $1 $BACKDROP." ;;
esac; }

expr_prompt () { case "$1" in
  neutral) echo "$SUBJ, $KEEP. A head-and-shoulders portrait facing the camera with a level neutral expression, the mouth closed. $BACKDROP." ;;
  alert)   echo "$SUBJ, $KEEP. A head-and-shoulders portrait facing the camera, the eyes wide and alert, the brow raised. $BACKDROP." ;;
  worried) echo "$SUBJ, $KEEP. A head-and-shoulders portrait facing the camera, the brow drawn together and the mouth slightly open, worried. $BACKDROP." ;;
  smile)   echo "$SUBJ, $KEEP. A head-and-shoulders portrait facing the camera with an open delighted smile held steady. $BACKDROP." ;;
  *)       echo "$SUBJ, $KEEP. A head-and-shoulders portrait facing the camera, $1. $BACKDROP." ;;
esac; }

render () { # prompt_text out_path ref_image w h
  printf '%s' "$1" > "$TMP/p.txt"
  "$DIR/dt_diptych.sh" - "$3" "$TMP/p.txt" "$2" "$SEED" "$4" "$5" >/dev/null
}

made=()
turn () {                          # render a chain of views, each referencing the one before it
  local ref="$1"; shift
  for v in "$@"; do
    out="${OUT}_${v}.png"
    echo "  view ${v} (ref $(basename "$ref")) …"
    render "$(body_prompt "$v")" "$out" "$ref" "$W" "$H"
    made+=("$out")
    ref="$out"
  done
}
turn "$MASTER" $VIEWS                                   # front and clockwise to the back
[ -n "$VIEWS_CCW" ] && turn "${OUT}_front.png" $VIEWS_CCW   # anticlockwise from the front
# Expression heads only apply to a subject with a face. An object asked for a "worried" portrait grows
# one: the droid came back with a human face inside its dome. Pass EXPR="" for props and vehicles.
for e in $EXPR; do
  out="${OUT}_expr_${e}.png"
  echo "  expression ${e} …"
  render "$(expr_prompt "$e")" "$out" "$MASTER" "$HW" "$HW"
  made+=("$out")
done
# Already-rendered images to fold into this subject's sheet -- combined plates in which the subject
# appears with another locked thing (the boy in the craft, the boy with the droid). A subject's sheet is
# meant to be the one picture that shows every way it has to stay the same, including alongside others.
for x in ${EXTRA:-}; do
  [ -f "$x" ] && made+=("$x")
done

if [ -n "${DETAIL:-}" ]; then
  echo "  detail …"
  render "$SUBJ, $KEEP. $DETAIL $BACKDROP." "${OUT}_detail.png" "$MASTER" "$HW" "$HW"
  made+=("${OUT}_detail.png")
fi

python3 - "$OUT" "${made[@]}" <<'PY'
import sys, os
from PIL import Image, ImageDraw, ImageFont
out, files = sys.argv[1], sys.argv[2:]
try: font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
except OSError: font = ImageFont.load_default()
base = os.path.basename(out)
ORDER = ["front", "45", "90", "135", "180", "back", "225", "270", "315", "34", "side"]
def rank(f):
    tag = os.path.basename(f).replace(".png", "").split("_")[-1]
    return ORDER.index(tag) if tag in ORDER else 99
bodies = [f for f in files
          if "_expr_" not in f and "_detail" not in f and os.path.basename(f).startswith(base + "_")]
bodies = sorted(bodies, key=rank)
rest   = [f for f in files if f not in bodies]
PAD, BG = 14, (248, 248, 248)
bims = [Image.open(f).convert("RGB") for f in bodies]
rims = [Image.open(f).convert("RGB") for f in rest]
bh = max((i.height for i in bims), default=0)
bw = sum(i.width for i in bims) + PAD * (len(bims) + 1)
rh = max((i.height for i in rims), default=0)
rw = sum(i.width for i in rims) + PAD * (len(rims) + 1) if rims else 0
W = max(bw, rw); H = bh + (rh + PAD if rims else 0) + PAD * 2
sheet = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(sheet)
x = PAD
for f, im in zip(bodies, bims):
    sheet.paste(im, (x, PAD))
    d.rectangle([x, PAD, x + 150, PAD + 26], fill=(0, 0, 0))
    d.text((x + 7, PAD + 3), os.path.basename(f).rsplit("_", 1)[-1][:-4], fill=(255, 255, 255), font=font)
    x += im.width + PAD
x, y = PAD, bh + PAD * 2
for f, im in zip(rest, rims):
    sheet.paste(im, (x, y))
    n = os.path.basename(f).replace(".png", "")
    lab = n.split("_expr_")[-1] if "_expr_" in n else n
    d.rectangle([x, y, x + 150, y + 26], fill=(0, 0, 0))
    d.text((x + 7, y + 3), lab, fill=(255, 255, 255), font=font)
    x += im.width + PAD
sheet.save(f"{out}_model.png")
print(f"model sheet: {out}_model.png  ({len(files)} views)")
PY
