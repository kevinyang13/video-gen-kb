#!/usr/bin/env bash
# Prepare real photographs as a LoRA training set.
#   scripts/photo_dataset.sh SRC_DIR OUT_DIR [MAXPX=1024] [TRIGGER]
#   ROTATE=90 scripts/photo_dataset.sh …   rotate every image clockwise by 90/180/270
# Reads every jpg/jpeg/png/heic in SRC_DIR, writes OUT_DIR/NN.png + a caption stub
# OUT_DIR/NN.txt. Existing captions are never overwritten, so this is safe to re-run
# after adding photos.
#
# Uses `sips`, which is built into macOS: it applies EXIF orientation when the tag is
# present (ffmpeg silently does not for still JPEGs, so portraits come out sideways) and
# writing PNG drops the EXIF block, including GPS. That last part is the point for
# photographs of family.
#
# ALWAYS LOOK AT THE OUTPUT. Some iPhone HEICs carry **no** orientation tag at all — they
# store landscape pixels of a portrait photo and rely on the viewer — and sips cannot fix
# what is not recorded, so every frame lands on its side. `sips -g orientation FILE`
# printing `<nil>` is the tell. Pass ROTATE=90 (or 180/270) to correct a whole batch.
#
# Aspect ratio is preserved and only the long side is capped, because the trainer's
# --use-aspect-ratio buckets by shape; cropping everything square here would throw away
# exactly the framing variety that a real photo set has and a synthetic one does not.
#
# Captions are STUBS on purpose. Fill each by looking at the photo and naming only what
# VARIES — framing, angle, expression, clothing, background, light. Never name the face,
# the hair or anything permanent: captioned features stay steerable, uncaptioned ones bind
# to the trigger token. See wiki/blueprint-v2-research.md §2a-i.
set -euo pipefail
SRC="${1:?source directory of photographs}"; OUT="${2:?output dataset directory}"
MAXPX="${3:-1024}"; TRIGGER="${4:-${TRIGGER:-}}"; ROTATE="${ROTATE:-0}"
[ -d "$SRC" ] || { echo "photo_dataset: no such directory: $SRC" >&2; exit 1; }
mkdir -p "$OUT"

n=0; made=0; kept=0
while IFS= read -r f; do
  n=$((n+1)); id=$(printf "%02d" "$n")
  out="$OUT/$id.png"; cap="$OUT/$id.txt"
  if [ ! -f "$out" ]; then
    sips -Z "$MAXPX" -s format png "$f" --out "$out" >/dev/null 2>&1 || { echo "  ! skipped (unreadable): $f" >&2; continue; }
    if [ "$ROTATE" != 0 ]; then
      # sips -r only writes a rotation HINT into the PNG; the raster stays as it was, so the
      # file looks right in Preview and wrong to anything that reads pixels. Bake it with PIL.
      python3 - "$out" "$ROTATE" <<'ROT'
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB").rotate(-int(sys.argv[2]), expand=True)
out = Image.new("RGB", im.size); out.paste(im); out.save(sys.argv[1])
ROT
    fi
    made=$((made+1))
  fi
  if [ -f "$cap" ]; then kept=$((kept+1)); else
    printf "%s\n" "${TRIGGER}" > "$cap"
  fi
  printf "  %s  %s  %s\n" "$id" "$(sips -g pixelWidth -g pixelHeight "$out" | awk '/pixel/{printf "%s ", $2}')" "$(basename "$f")"
done < <(find "$SRC" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.heic" \) | sort)

echo "dataset: $OUT  ($n photos, $made converted, $kept captions left alone)"
echo "next: fill each $OUT/NN.txt — only what varies, never the face or hair"
