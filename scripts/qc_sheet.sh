#!/usr/bin/env bash
# QC contact sheet for a clip: [reference] + N frames spread evenly from first to last.
#   scripts/qc_sheet.sh CLIP.mov OUT.png [REF.png|-] [N=5] [TILE_H=384]
# Works for any size/aspect/frame count: frame indices come from the clip itself.
# Compare the reference (character master or the shot's still) against frame 0 … last:
# identity, costume, count, style, held gestures, end-of-clip fade.
set -euo pipefail

CLIP="${1:?clip}"; OUT="${2:?out .png}"; REF="${3:--}"; N="${4:-5}"; TH="${5:-384}"
[ -f "$CLIP" ] || { echo "qc_sheet: clip not found: $CLIP" >&2; exit 1; }
total=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 "$CLIP")
[ "$total" -ge 1 ] || { echo "qc_sheet: no frames in $CLIP" >&2; exit 1; }
sel=""; for i in $(seq 0 $((N-1))); do
  f=$(( N > 1 ? i * (total - 1) / (N - 1) : 0 ))
  sel+="eq(n\\,$f)+"; idx+="$f "
done
sel="${sel%+}"
mkdir -p "$(dirname "$OUT")"
if [ "$REF" != "-" ]; then
  ffmpeg -nostdin -v error -y -i "$REF" -i "$CLIP" -filter_complex \
    "[0]scale=-2:${TH}[m];[1]select='${sel}',scale=-2:${TH},tile=${N}x1[t];[m][t]hstack=2" -frames:v 1 "$OUT"
else
  ffmpeg -nostdin -v error -y -i "$CLIP" -vf "select='${sel}',scale=-2:${TH},tile=${N}x1" -frames:v 1 "$OUT"
fi
echo "$OUT  (frames: ${idx}of $total)"
