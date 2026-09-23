#!/usr/bin/env bash
# Reference-locked edit with the released draw-things-cli (single --image, no Moodboard):
# put a reference image beside the input, let FLUX.2 klein edit the pair at strength 1.0,
# and keep only the right half. klein treats the whole --image as an edit reference at
# strength 1.0, so the left half carries identity (face, costume, prop) into the right half.
#   scripts/dt_diptych.sh REF.png IN.png PROMPT.txt OUT.png [seed] [W] [H]
# W x H = size of ONE half (default 576x1024). Both images are scaled/cropped to it.
# Without REF (pass "-"), it is a plain single-image klein edit at W x H.
set -euo pipefail

REF="${1:?ref.png or -}"; IN="${2:?in.png}"; PROMPT="${3:?prompt.txt}"; OUT="${4:?out.png}"
SEED="${5:-1}"; W="${6:-576}"; H="${7:-1024}"
MODEL="${MODEL:-flux_2_klein_9b_i8x.ckpt}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fit="scale=${W}:${H}:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}:${H}"

if [ "$REF" = "-" ]; then
  ffmpeg -v error -y -i "$IN" -vf "$fit" "$TMP/pair.png"; OW=$W
else
  ffmpeg -v error -y -i "$REF" -i "$IN" -filter_complex "[0]${fit}[l];[1]${fit}[r];[l][r]hstack=2" "$TMP/pair.png"; OW=$((W*2))
fi

draw-things-cli generate -m "$MODEL" --prompt-file "$PROMPT" --image "$TMP/pair.png" --strength 1.0 \
  --width "$OW" --height "$H" --steps 4 --cfg 1 --seed "$SEED" \
  --config-json '{"shift":3.0,"sampler":16}' --offline --disable-preview -o "$TMP/out.png" >/dev/null

if [ "$REF" = "-" ]; then cp "$TMP/out.png" "$OUT"
else ffmpeg -v error -y -i "$TMP/out.png" -vf "crop=${W}:${H}:${W}:0" "$OUT"; fi
echo "$OUT"
