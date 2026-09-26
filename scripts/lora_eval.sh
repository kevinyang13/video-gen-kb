#!/usr/bin/env bash
# Render one prompt set through several LoRA checkpoints and tile the result.
#   scripts/lora_eval.sh OUT_DIR "ckpt_a.ckpt,ckpt_b.ckpt,…" [WEIGHT] [SEED]
# A "-" in the checkpoint list renders that column with NO LoRA, which is the control
# every identity claim needs: a LoRA that changes nothing and a LoRA that changes the
# wrong thing look the same without it.
#
# Prompts come from PROMPTS (one per line) or the built-in set, which is ordered from
# in-distribution to out-of-distribution on purpose — the interesting failure is not the
# studio portrait, it is the angle and the scene the dataset never showed.
#
#   WEIGHT  LoRA weight, default 1.0. Pass a comma list to sweep it against one checkpoint.
#   W H     size, default 512x768        MODEL  base model
#   TRIGGER prepended to every prompt, default nelf_kyle
set -euo pipefail
OUT="${1:?output dir}"; CKPTS="${2:?comma-separated checkpoints, - for none}"
WEIGHT="${3:-1.0}"; SEED="${4:-7}"
MODEL="${MODEL:-flux_2_klein_9b_i8x.ckpt}"; W="${W:-512}"; H="${H:-768}"
TRIGGER="${TRIGGER:-nelf_kyle}"
mkdir -p "$OUT"

DEFAULT_PROMPTS="close-up portrait, facing the camera, wearing worn leather armour, a plain grey studio backdrop, soft even studio light, neutral expression
close-up portrait, side profile, the hood pulled up, a dense forest edge, flat overcast daylight, a focused gaze
medium shot, seen from behind, the back of the head and shoulders, wearing worn leather armour, a stone city street, hard noon sunlight
full body wide shot, small in frame, facing the camera, a heavy fur cloak, deep snow and bare black trees, cold blue winter light
medium shot, three-quarter view, a plain linen tunic, a crowded market at dusk, warm lantern light, laughing"
PROMPTS="${PROMPTS:-$DEFAULT_PROMPTS}"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
IFS=',' read -r -a CK <<< "$CKPTS"
IFS=',' read -r -a WT <<< "$WEIGHT"
cols=0
for c in "${CK[@]}"; do for w in "${WT[@]}"; do cols=$((cols+1)); done; done

row=0
while IFS= read -r p; do
  [ -n "$p" ] || continue
  row=$((row+1)); col=0
  for c in "${CK[@]}"; do
    for w in "${WT[@]}"; do
      col=$((col+1))
      printf "%s, %s\n" "$TRIGGER" "$p" > "$TMP/p.txt"
      if [ "$c" = "-" ]; then cfg='{"shift":3.0,"sampler":16}'; tag="base"
      else cfg="{\"shift\":3.0,\"sampler\":16,\"loras\":[{\"file\":\"$c\",\"weight\":$w}]}"
           tag="$(basename "$c" .ckpt)@$w"; fi
      out="$OUT/r${row}_c${col}.png"
      echo "  row $row col $col  $tag"
      draw-things-cli generate -m "$MODEL" --prompt-file "$TMP/p.txt" --width "$W" --height "$H" \
        --steps 4 --cfg 1 --seed "$SEED" --config-json "$cfg" --offline --disable-preview -o "$out" >/dev/null
    done
  done
done <<< "$PROMPTS"

i=0
for f in $(ls "$OUT"/r*_c*.png | sort -t r -k2 -n); do
  i=$((i+1))
  ffmpeg -v error -y -i "$f" -vf "scale=320:480:force_original_aspect_ratio=decrease,pad=320:480:(ow-iw)/2:(oh-ih)/2:color=0x202020" "$TMP/$(printf %03d $i).png"
done
ffmpeg -v error -y -start_number 1 -i "$TMP/%03d.png" -filter_complex "tile=${cols}x${row}:padding=4:color=0x202020" -frames:v 1 "$OUT/grid.png"
echo "grid: $OUT/grid.png  (${cols} columns x ${row} prompts)"
