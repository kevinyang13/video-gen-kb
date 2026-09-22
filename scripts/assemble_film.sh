#!/usr/bin/env bash
# Concatenate 4K shot clips with crossfades into one film.
#   scripts/assemble_film.sh OUT.mp4 clip1.mp4 clip2.mp4 [clip3.mp4 ...]
# Options via env:
#   XFADE=0.5   crossfade seconds (0 = hard cuts)
#   FPS=25      output frame rate (inputs are conformed to it)
#   MUSIC=path  optional music bed mixed under the clips' own audio
#   LETTERBOX=1 2.39:1 bars (3840x1608 picture inside 3840x2160)
# Clips with no audio track get silence so the audio graph stays uniform.
# Output: 3840x2160 HEVC 10-bit (videotoolbox) ~40 Mbps + AAC 192k.
set -euo pipefail

OUT="${1:?output .mp4}"; shift
[ "$#" -ge 2 ] || { echo "need at least 2 clips" >&2; exit 1; }
XFADE="${XFADE:-0.5}"; FPS="${FPS:-25}"; MUSIC="${MUSIC:-}"; LETTERBOX="${LETTERBOX:-0}"

inputs=(); filt=""; n=0; offset=0
for c in "$@"; do
  inputs+=(-i "$c")
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$c")
  has_a=$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$c" | head -1)
  vf="scale=3840:2160:force_original_aspect_ratio=increase:flags=lanczos,crop=3840:2160,fps=${FPS},format=yuv420p10le,setsar=1"
  [ "$LETTERBOX" = "1" ] && vf="$vf,drawbox=0:0:3840:276:black:fill,drawbox=0:1884:3840:276:black:fill"
  filt+="[$n:v]${vf}[v$n];"
  if [ -n "$has_a" ]; then filt+="[$n:a]aformat=sample_rates=48000:channel_layouts=stereo,apad[a$n];"
  else filt+="anullsrc=r=48000:cl=stereo,atrim=0:${dur}[a$n];"; fi
  durs[$n]=$dur; n=$((n+1))
done

# chain xfades: v = xfade(v0,v1) ... ; a = acrossfade
if [ "$(echo "$XFADE > 0" | bc)" = "1" ]; then
  prev_v="v0"; prev_a="a0"; offset=${durs[0]}
  for ((i=1;i<n;i++)); do
    offset=$(python3 -c "print(round($offset - $XFADE, 3))")
    filt+="[$prev_v][v$i]xfade=transition=fade:duration=${XFADE}:offset=${offset}[xv$i];"
    filt+="[$prev_a][a$i]acrossfade=d=${XFADE}[xa$i];"
    prev_v="xv$i"; prev_a="xa$i"
    offset=$(python3 -c "print(round($offset + ${durs[$i]}, 3))")
  done
else
  for ((i=0;i<n;i++)); do filt+="[v$i][a$i]"; done
  filt+="concat=n=${n}:v=1:a=1[xv][xa];"; prev_v="xv"; prev_a="xa"
fi

if [ -n "$MUSIC" ]; then
  inputs+=(-i "$MUSIC")
  filt+="[$n:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.6[m];[$prev_a][m]amix=inputs=2:duration=first:dropout_transition=2[aout]"
  aout="[aout]"
else
  aout="[$prev_a]"
fi

ffmpeg -v error -y "${inputs[@]}" -filter_complex "${filt%;}" \
  -map "[$prev_v]" -map "$aout" \
  -c:v hevc_videotoolbox -profile:v main10 -pix_fmt p010le -b:v 40M -tag:v hvc1 \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "film: $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s)"
