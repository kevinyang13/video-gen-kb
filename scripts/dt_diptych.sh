#!/usr/bin/env bash
# Still images with the released draw-things-cli (single --image, no Moodboard).
#   scripts/dt_diptych.sh REF IN PROMPT.txt OUT.png [seed] [W] [H]
# Three modes, picked by which inputs are "-":
#   REF=file IN=file  diptych: REF left, IN right, edit the pair, keep the right half.
#                     FLUX.2 klein at strength 1.0 treats the whole --image as an edit
#                     reference, so the left half carries identity into the right half.
#   REF=-    IN=file  single-image edit (restyle / re-frame IN).
#   REF=-    IN=-     text-to-image.
# W x H = size of the OUTPUT (and of each half); default 576x1024. Multiples of 64.
# Env overrides (defaults = the klein 9B settings used on every project so far):
#   MODEL=flux_2_klein_9b_i8x.ckpt  STEPS=4  CFG=1  STRENGTH=1.0
#   CONFIG_JSON='{"shift":3.0,"sampler":16}'   (merged onto the model's recommended settings)
#   NEGATIVE=""   DRY_RUN=1 prints the command instead of running it.
# Inputs are fitted to W x H by scale-to-fill + centre crop, so hand over images at the target aspect.
set -euo pipefail

REF="${1:?REF image or -}"; IN="${2:?IN image or -}"; PROMPT="${3:?prompt .txt}"; OUT="${4:?out .png}"
SEED="${5:-1}"; W="${6:-576}"; H="${7:-1024}"
MODEL="${MODEL:-flux_2_klein_9b_i8x.ckpt}"; STEPS="${STEPS:-4}"; CFG="${CFG:-1}"; STRENGTH="${STRENGTH:-1.0}"
DEFAULT_CONFIG='{"shift":3.0,"sampler":16}'; CONFIG_JSON="${CONFIG_JSON:-$DEFAULT_CONFIG}"

die() { echo "dt_diptych: $*" >&2; exit 1; }
[ -f "$PROMPT" ] || die "prompt file not found: $PROMPT"
[ "$REF" = "-" ] || [ -f "$REF" ] || die "REF not found: $REF"
[ "$IN" = "-" ] || [ -f "$IN" ] || die "IN not found: $IN"
[ "$REF" != "-" ] && [ "$IN" = "-" ] && die "a diptych needs an IN image (REF without IN makes no sense)"
(( W % 64 == 0 && H % 64 == 0 )) || die "W and H must be multiples of 64 (got ${W}x${H})"
mkdir -p "$(dirname "$OUT")"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fit="scale=${W}:${H}:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}:${H}"
args=(generate -m "$MODEL" --prompt-file "$PROMPT" --height "$H" --steps "$STEPS" --cfg "$CFG" --seed "$SEED"
      --config-json "$CONFIG_JSON" --offline --disable-preview -o "$TMP/out.png")
[ -n "${NEGATIVE:-}" ] && args+=(--negative-prompt "$NEGATIVE")

if [ "$REF" != "-" ]; then
  mode=diptych
  ffmpeg -nostdin -v error -y -i "$REF" -i "$IN" -filter_complex "[0]${fit}[l];[1]${fit}[r];[l][r]hstack=2" "$TMP/pair.png"
  args+=(--image "$TMP/pair.png" --strength "$STRENGTH" --width $((W*2)))
elif [ "$IN" != "-" ]; then
  mode=edit
  ffmpeg -nostdin -v error -y -i "$IN" -vf "$fit" "$TMP/in.png"
  args+=(--image "$TMP/in.png" --strength "$STRENGTH" --width "$W")
else
  mode=text
  args+=(--width "$W")
fi

if [ -n "${DRY_RUN:-}" ]; then echo "[$mode] draw-things-cli ${args[*]}"; exit 0; fi
draw-things-cli "${args[@]}" >/dev/null || die "draw-things-cli failed ($mode, seed $SEED)"
[ -s "$TMP/out.png" ] || die "no output written"

if [ "$mode" = diptych ]; then ffmpeg -nostdin -v error -y -i "$TMP/out.png" -vf "crop=${W}:${H}:${W}:0" "$OUT"
else cp "$TMP/out.png" "$OUT"; fi
echo "$OUT"
