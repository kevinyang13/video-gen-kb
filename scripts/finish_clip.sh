#!/usr/bin/env bash
# Turn a short I2V export into a seamless looping post with optional music.
#   scripts/finish_clip.sh IN.mov [music.mp3] [outname]
# Works for any frame count / fps / size: the loop unit is the whole clip, with its last
# SEAM seconds crossfaded into its first SEAM seconds, repeated LOOPS+1 times.
# Env:
#   W=1080 H=1920   output size (landscape post: W=1920 H=1080); input is scaled to fill + centre-cropped
#   LOOPS=5         extra repeats (5 -> 6 units; a 5 s Wan clip gives ~27 s)
#   SEAM=0.5        crossfade seconds at the loop point
#   FPS=            output fps (default: the input's)
#   MUSIC_VOL=0.9   music level; 1 s fade in, 2 s fade out
# Output: <outname>_loop.mp4 (no audio) and, with music, <outname>_final.mp4.
set -euo pipefail

IN="${1:?input .mov/.mp4}"; MUSIC="${2:-}"; OUT="${3:-${IN%.*}}"
W="${W:-1080}"; H="${H:-1920}"; LOOPS="${LOOPS:-5}"; SEAM="${SEAM:-0.5}"; MUSIC_VOL="${MUSIC_VOL:-0.9}"
die() { echo "finish_clip: $*" >&2; exit 1; }
[ -f "$IN" ] || die "input not found: $IN"
[ -z "$MUSIC" ] || [ -f "$MUSIC" ] || die "music not found: $MUSIC"

IFPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$IN" | awk -F/ '{printf "%.4f", $1/$2}')
FPS="${FPS:-$IFPS}"
N=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 "$IN")
SF=$(python3 -c "print(max(1, round($SEAM * $FPS)))")          # seam length in frames
(( N > 3 * SF )) || die "clip too short ($N frames) for a ${SEAM}s seam"
TAIL=$(( N - SF ))

ffmpeg -nostdin -v error -y -i "$IN" -filter_complex "
  [0:v]fps=${FPS},scale=${W}:${H}:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}:${H},setsar=1[c];[c]split=3[c1][c2][c3];
  [c1]trim=start_frame=${SF}:end_frame=${TAIL},setpts=PTS-STARTPTS[body];
  [c2]trim=start_frame=${TAIL}:end_frame=${N},setpts=PTS-STARTPTS[tail];
  [c3]trim=start_frame=0:end_frame=${SF},setpts=PTS-STARTPTS[head];
  [tail][head]xfade=transition=fade:duration=${SEAM}:offset=0[seam];
  [body][seam]concat=n=2:v=1[unit];
  [unit]loop=loop=${LOOPS}:size=32767,setpts=N/FRAME_RATE/TB[out]" \
  -map "[out]" -r "$FPS" -c:v libx264 -pix_fmt yuv420p -crf 18 -an "${OUT}_loop.mp4"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${OUT}_loop.mp4")
echo "loop: ${OUT}_loop.mp4 (${DUR}s, ${W}x${H} @ ${FPS} fps)"

if [ -n "$MUSIC" ]; then
  FADE_OUT_START=$(python3 -c "print(max(0, float('$DUR') - 2))")
  ffmpeg -nostdin -v error -y -i "${OUT}_loop.mp4" -i "$MUSIC" -filter_complex \
    "[1:a]atrim=0:${DUR},afade=t=in:st=0:d=1,afade=t=out:st=${FADE_OUT_START}:d=2,volume=${MUSIC_VOL}[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "${OUT}_final.mp4"
  echo "final: ${OUT}_final.mp4"
fi
