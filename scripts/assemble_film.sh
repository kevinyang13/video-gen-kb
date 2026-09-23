#!/usr/bin/env bash
# Join shot clips with crossfades into one film, optionally with a music bed.
#   scripts/assemble_film.sh OUT.mp4 clip1.mp4 [clip2.mp4 ...]
# Options via env:
#   W=3840 H=2160   output size (portrait: W=2160 H=3840). Clips are scaled to fill and centre-cropped.
#   FPS=25          output frame rate (inputs are conformed to it)
#   XFADE=0.5       crossfade seconds (0 = hard cuts)
#   BITRATE=40M     HEVC 10-bit video bitrate (12M for 1080p)
#   LETTERBOX=0     1 = 2.39:1 black bars (landscape only)
#   CLIP_AUDIO=1    0 = ignore the clips' own audio (music-only film)
#   CLIP_VOL=0.5    level of the clips' audio in the mix
#   MUSIC=path      optional music bed
#   MUSIC_VOL=0.3   level of the bed (0.5/0.3 = the levels this script always used; music-only: CLIP_AUDIO=0 MUSIC_VOL=1)
#   MUSIC_START=0   seconds into the track, or "tail" = the last <film length> seconds (film ends on the song's ending)
#   MUSIC_FADE_IN=0 / MUSIC_FADE_OUT=0   seconds
# Clips with no audio track get silence so the audio graph stays uniform.
set -euo pipefail

OUT="${1:?output .mp4}"; shift
[ "$#" -ge 1 ] || { echo "assemble_film: need at least 1 clip" >&2; exit 1; }
W="${W:-3840}"; H="${H:-2160}"; FPS="${FPS:-25}"; XFADE="${XFADE:-0.5}"; BITRATE="${BITRATE:-40M}"
LETTERBOX="${LETTERBOX:-0}"; CLIP_AUDIO="${CLIP_AUDIO:-1}"; CLIP_VOL="${CLIP_VOL:-0.5}"
MUSIC="${MUSIC:-}"; MUSIC_VOL="${MUSIC_VOL:-0.3}"; MUSIC_START="${MUSIC_START:-0}"
MUSIC_FADE_IN="${MUSIC_FADE_IN:-0}"; MUSIC_FADE_OUT="${MUSIC_FADE_OUT:-0}"
die() { echo "assemble_film: $*" >&2; exit 1; }
(( W % 2 == 0 && H % 2 == 0 )) || die "W and H must be even"
[ -z "$MUSIC" ] || [ -f "$MUSIC" ] || die "music not found: $MUSIC"
calc() { python3 -c "print(round($1, 3))"; }

inputs=(); filt=""; n=0; durs=()
for c in "$@"; do
  [ -f "$c" ] || die "clip not found: $c"
  inputs+=(-i "$c")
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$c")
  has_a=$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$c" | head -1)
  vf="scale=${W}:${H}:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}:${H},fps=${FPS},format=yuv420p10le,setsar=1"
  if [ "$LETTERBOX" = "1" ]; then
    (( W > H )) || die "LETTERBOX=1 is for landscape frames only (got ${W}x${H})"; bar=$(( (H - W * 100 / 239) / 2 ))
    vf="$vf,drawbox=0:0:${W}:${bar}:black:fill,drawbox=0:$((H - bar)):${W}:${bar}:black:fill"
  fi
  filt+="[$n:v]${vf}[v$n];"
  # apad must be bounded: an unbounded apad buffers silence forever and the graph OOMs at 4K (2026-09-22)
  if [ -n "$has_a" ] && [ "$CLIP_AUDIO" = "1" ]; then filt+="[$n:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur=${dur}[a$n];"
  else filt+="anullsrc=r=48000:cl=stereo,atrim=0:${dur}[a$n];"; fi
  durs[$n]=$dur; n=$((n+1))
done

# chain xfades: v = xfade(v0,v1) ... ; a = acrossfade
if [ "$n" -gt 1 ] && [ "$(echo "$XFADE > 0" | bc)" = "1" ]; then
  prev_v="v0"; prev_a="a0"; offset=${durs[0]}
  for ((i=1;i<n;i++)); do
    offset=$(calc "$offset - $XFADE")
    filt+="[$prev_v][v$i]xfade=transition=fade:duration=${XFADE}:offset=${offset}[xv$i];"
    filt+="[$prev_a][a$i]acrossfade=d=${XFADE}[xa$i];"
    prev_v="xv$i"; prev_a="xa$i"
    offset=$(calc "$offset + ${durs[$i]}")
  done
  FILM=$offset
else
  for ((i=0;i<n;i++)); do filt+="[v$i][a$i]"; done
  filt+="concat=n=${n}:v=1:a=1[xv][xa];"; prev_v="xv"; prev_a="xa"
  FILM=$(calc "$(IFS=+; echo "${durs[*]}")")
fi

if [ -n "$MUSIC" ]; then
  mlen=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MUSIC")
  if [ "$MUSIC_START" = "tail" ]; then ss=$(calc "max(0, $mlen - $FILM)"); else ss=$MUSIC_START; fi
  [ "$(echo "$mlen - $ss < $FILM" | bc)" = "1" ] && echo "assemble_film: note — music runs out $(calc "$FILM - ($mlen - $ss)") s before the film ends" >&2
  inputs+=(-ss "$ss" -i "$MUSIC")
  mf="aformat=sample_rates=48000:channel_layouts=stereo,volume=${MUSIC_VOL}"
  [ "$(echo "$MUSIC_FADE_IN > 0" | bc)" = "1" ] && mf+=",afade=t=in:st=0:d=${MUSIC_FADE_IN}"
  [ "$(echo "$MUSIC_FADE_OUT > 0" | bc)" = "1" ] && mf+=",afade=t=out:st=$(calc "$FILM - $MUSIC_FADE_OUT"):d=${MUSIC_FADE_OUT}"
  filt+="[$n:a]${mf}[m];[$prev_a]volume=${CLIP_VOL}[c];[c][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
  aout="[aout]"
else
  filt+="[$prev_a]volume=$([ "$CLIP_AUDIO" = "1" ] && echo 1 || echo 0)[aout]"; aout="[aout]"
fi

mkdir -p "$(dirname "$OUT")"
ffmpeg -nostdin -v error -y "${inputs[@]}" -filter_complex "${filt%;}" \
  -map "[$prev_v]" -map "$aout" \
  -c:v hevc_videotoolbox -profile:v main10 -pix_fmt p010le -b:v "$BITRATE" -tag:v hvc1 \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "film: $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s, expected ${FILM}s$([ -n "$MUSIC" ] && echo ", music from ${ss}s"))"
