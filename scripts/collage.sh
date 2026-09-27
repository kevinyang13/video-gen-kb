#!/usr/bin/env bash
# Tile every image in a folder into one collage.
#   scripts/collage.sh SRC_DIR [OUT.png] [COLS]
# Env:
#   TILE_W TILE_H   cell size; default = the size of the first image (no resampling
#                   when every image already matches, which is the common case here)
#   PAD MARGIN      gutter and border in px, default 10
#   BG              background colour, default 0x141414
#   PREVIEW         set to a width (e.g. 2400) to also write OUT_preview.jpg
#
# Runs on the stock macOS bash 3.2, so no mapfile and no associative arrays.
#
# Mixed sizes and mixed orientations are fine: each image is fitted inside the cell
# and padded, never cropped, so nothing loses a head to a square crop.
set -euo pipefail
SRC="${1:?source directory}"; OUT="${2:-collage.png}"; COLS="${3:-0}"
PAD="${PAD:-10}"; MARGIN="${MARGIN:-10}"; BG="${BG:-0x141414}"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
FILES=()
while IFS= read -r line; do FILES+=("$line"); done < <(find "$SRC" -maxdepth 1 -type f \
  \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.webp" -o -iname "*.heic" \) | LC_ALL=C sort)
n=${#FILES[@]}
[ "$n" -gt 0 ] || { echo "collage: no images in $SRC" >&2; exit 1; }

# cell size defaults to the first image, so a uniform set is tiled without resampling
read -r W0 H0 < <(sips -g pixelWidth -g pixelHeight "${FILES[0]}" | awk '/pixelWidth/{w=$2}/pixelHeight/{h=$2}END{print w, h}')
TW="${TILE_W:-$W0}"; TH="${TILE_H:-$H0}"
[ "$COLS" -gt 0 ] || COLS=$(python3 -c "import math;print(math.ceil(math.sqrt($n)))")
ROWS=$(( (n + COLS - 1) / COLS ))

i=0
for f in "${FILES[@]}"; do
  i=$((i+1))
  ffmpeg -nostdin -v error -y -i "$f" \
    -vf "scale=${TW}:${TH}:force_original_aspect_ratio=decrease,pad=${TW}:${TH}:(ow-iw)/2:(oh-ih)/2:color=${BG}" \
    "$TMP/$(printf %04d $i).png"
done
# the last row is padded out with blanks, otherwise tile drops it
blank=$(( ROWS * COLS - n ))
for ((j=1;j<=blank;j++)); do
  ffmpeg -nostdin -v error -y -f lavfi -i "color=c=${BG}:s=${TW}x${TH}" -frames:v 1 "$TMP/$(printf %04d $((n+j))).png"
done

ffmpeg -nostdin -v error -y -start_number 1 -i "$TMP/%04d.png" \
  -filter_complex "tile=${COLS}x${ROWS}:padding=${PAD}:margin=${MARGIN}:color=${BG}" -frames:v 1 "$OUT"
echo "collage: $OUT  (${n} images, ${COLS}x${ROWS}, cell ${TW}x${TH})"

if [ -n "${PREVIEW:-}" ]; then
  prev="${OUT%.*}_preview.jpg"
  ffmpeg -nostdin -v error -y -i "$OUT" -vf "scale=${PREVIEW}:-2" -q:v 3 "$prev"
  echo "preview: $prev"
fi
