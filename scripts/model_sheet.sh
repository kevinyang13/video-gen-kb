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
VIEWS="${VIEWS:-front 34 side back}"; EXPR="${EXPR-neutral alert worried}"
W="${W:-512}"; H="${H:-768}"; HW="${HW:-640}"
KEEP="exactly the same face, the same hair, the same colours and the same clothing, the same age, the same build, no change to the identity"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$(dirname "$OUT")"

body_prompt () { case "$1" in
  front) echo "$SUBJ, $KEEP. A full-length view from head to feet, standing square to the camera and facing forward, arms relaxed at the sides, the whole body inside the frame with clear space above the head and below the feet. $BACKDROP." ;;
  34)    echo "$SUBJ, $KEEP. A full-length view from head to feet, the body rotated about 45 degrees to a three-quarter view, still looking toward the camera, the whole body inside the frame. $BACKDROP." ;;
  side)  echo "$SUBJ, $KEEP. A full-length true side profile seen from exactly 90 degrees, the body in line with the camera, the nose, lips and chin forming the outline against the backdrop, only ONE eye visible and the far side of the face hidden behind the near side. Exactly one face in the image. $BACKDROP." ;;
  back)  echo "$SUBJ, $KEEP. A full-length view from directly behind, the back of the head, shoulders and legs toward the camera, the face turned fully away and not visible. $BACKDROP." ;;
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

ref="$MASTER"; made=()
for v in $VIEWS; do
  out="${OUT}_${v}.png"
  echo "  view ${v} (ref $(basename "$ref")) …"
  render "$(body_prompt "$v")" "$out" "$ref" "$W" "$H"
  made+=("$out")
  ref="$out"                      # each view references the previous one: half the rotation per step
done
# Expression heads only apply to a subject with a face. An object asked for a "worried" portrait grows
# one: the droid came back with a human face inside its dome. Pass EXPR="" for props and vehicles.
for e in $EXPR; do
  out="${OUT}_expr_${e}.png"
  echo "  expression ${e} …"
  render "$(expr_prompt "$e")" "$out" "$MASTER" "$HW" "$HW"
  made+=("$out")
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
bodies = [f for f in files if "_expr_" not in f and "_detail" not in f]
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
    lab = os.path.basename(f).replace(".png", "").split("_expr_")[-1].split("_")[-1]
    d.rectangle([x, y, x + 150, y + 26], fill=(0, 0, 0))
    d.text((x + 7, y + 3), lab, fill=(255, 255, 255), font=font)
    x += im.width + PAD
sheet.save(f"{out}_model.png")
print(f"model sheet: {out}_model.png  ({len(files)} views)")
PY
