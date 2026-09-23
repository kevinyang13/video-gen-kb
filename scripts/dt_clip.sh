#!/usr/bin/env bash
# Image-to-video clip with the released draw-things-cli: the still is frame 0, pixel for pixel.
#   scripts/dt_clip.sh STILL.png PROMPT.txt OUT.mov [seed] [W] [H] [FRAMES]
# The model family is detected from MODEL and sets the defaults; every default can be overridden.
#   ltx (default)  MODEL=ltx_2.3_22b_distilled_1.1_q8p.ckpt   576x1024 portrait / 1024x576 landscape,
#                  FRAMES=249 (8k+1, ~10 s @25 fps), STEPS=8, CFG=1,
#                  CONFIG_JSON={"sampler":19,"shift":5.0,"stochasticSamplingGamma":0.3,"fps":25,"hiresFix":false}
#   wan            MODEL=wan_v2.2_a14b_hne_i2v_i8x.ckpt  + low-noise refiner at 10% + Lightning LoRA,
#                  FRAMES=81 (4k+1, ~5 s @16 fps), STEPS=4, CFG=1, UniPC Trailing, shift 5
#                  (Wan via the CLI is untested here — check the first run against the app).
# Env: MODEL STEPS CFG CONFIG_JSON VIDEO_FORMAT(prores422hq|prores4444|h264|hevc) NEGATIVE
#      DRY_RUN=1 prints the command.  FORCE=1 re-renders even if OUT exists.
# W, H default to the still's own size. Both must be multiples of 64.
set -euo pipefail

STILL="${1:?still .png}"; PROMPT="${2:?prompt .txt}"; OUT="${3:?out .mov}"; SEED="${4:-1}"
die() { echo "dt_clip: $*" >&2; exit 1; }
[ -f "$STILL" ] || die "still not found: $STILL"
[ -f "$PROMPT" ] || die "prompt file not found: $PROMPT"
IFS=, read -r SW SH < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$STILL")
W="${5:-$SW}"; H="${6:-$SH}"

MODEL="${MODEL:-ltx_2.3_22b_distilled_1.1_q8p.ckpt}"
case "$MODEL" in
  *ltx*) FAMILY=ltx; dF=249; dSTEPS=8; dCFG=1
         dCONF='{"sampler":19,"shift":5.0,"stochasticSamplingGamma":0.3,"fps":25,"hiresFix":false}' ;;
  *wan*) FAMILY=wan; dF=81; dSTEPS=4; dCFG=1
         dCONF='{"sampler":17,"shift":5.0,"fps":16,"refinerModel":"wan_v2.2_a14b_lne_i2v_i8x.ckpt","refinerStart":0.1,"loras":[{"file":"wan_v2.2_a14b_hne_i2v_lightning_251022_lora_f16.ckpt","weight":1.0}]}' ;;
  *) die "unknown model family for $MODEL (expected ltx or wan in the name); set STEPS/CFG/CONFIG_JSON/FRAMES explicitly and FAMILY=other"; ;;
esac
FRAMES="${7:-${FRAMES:-$dF}}"; STEPS="${STEPS:-$dSTEPS}"; CFG="${CFG:-$dCFG}"; CONFIG_JSON="${CONFIG_JSON:-$dCONF}"
VIDEO_FORMAT="${VIDEO_FORMAT:-prores422hq}"

(( W % 64 == 0 && H % 64 == 0 )) || die "W and H must be multiples of 64 (got ${W}x${H})"
[ "$FAMILY" = ltx ] && (( (FRAMES - 1) % 8 != 0 )) && die "LTX frames must be 8k+1 (got $FRAMES; use 249 or 97)"
[ "$FAMILY" = wan ] && (( (FRAMES - 1) % 4 != 0 )) && die "Wan frames must be 4k+1 (got $FRAMES; use 81)"
[ "$FAMILY" = ltx ] && (( W * H > 1024 * 576 )) && echo "dt_clip: warning — ${W}x${H} is above 1024x576; LTX may swap badly on 48 GB" >&2
[ "$SW" = "$W" ] && [ "$SH" = "$H" ] || echo "dt_clip: note — still is ${SW}x${SH}, render is ${W}x${H}; the CLI centre-crops it" >&2
case "$OUT" in *.mov|*.mp4) ;; *) die "OUT must be .mov or .mp4";; esac
if [ -e "$OUT" ] && [ -z "${FORCE:-}" ] && [ -z "${DRY_RUN:-}" ]; then echo "dt_clip: exists, skipping: $OUT" >&2; echo "$OUT"; exit 0; fi

args=(generate -m "$MODEL" --prompt-file "$PROMPT" --image "$STILL" --width "$W" --height "$H"
      --frames "$FRAMES" --steps "$STEPS" --cfg "$CFG" --seed "$SEED" --config-json "$CONFIG_JSON"
      --offline --disable-preview --video-format "$VIDEO_FORMAT" -o "$OUT")
[ -n "${NEGATIVE:-}" ] && args+=(--negative-prompt "$NEGATIVE")

if [ -n "${DRY_RUN:-}" ]; then echo "[$FAMILY] draw-things-cli ${args[*]}"; exit 0; fi
mkdir -p "$(dirname "$OUT")"
t0=$(date +%s)
draw-things-cli "${args[@]}" >/dev/null || die "draw-things-cli failed ($MODEL, seed $SEED)"
n=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 "$OUT" 2>/dev/null || echo "?")
echo "dt_clip: $OUT  ${W}x${H}  $n frames  $(( $(date +%s) - t0 ))s" >&2
echo "$OUT"
