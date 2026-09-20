#!/usr/bin/env bash
# Turn a 5 s Draw Things I2V export into a posted-ready 27 s loop with music.
#   scripts/finish_clip.sh raw/clips/coast_v2.mov [music.mp3] [outname]
# Input: 576x1024 (or 576x1280 -> auto-cropped), 16 fps, 81 frames.
# Output: <outname>_loop.mp4 (1080x1920, no audio) and <outname>_final.mp4 (with music).
set -euo pipefail

IN="${1:?input .mov/.mp4}"
MUSIC="${2:-}"
OUT="${3:-${IN%.*}}"
FPS=16
LOOPS=5            # unit x6 = 27.4 s
FADE_FRAMES=8      # crossfade tail->head, 0.5 s at 16 fps

H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$IN")
CROP=""
[ "$H" -gt 1024 ] && CROP="crop=576:1024:0:$(( (H-1024)/2 )),"

ffmpeg -v error -y -i "$IN" -filter_complex "
  [0:v]${CROP}fps=${FPS},setsar=1[c];[c]split=3[c1][c2][c3];
  [c1]trim=start_frame=${FADE_FRAMES}:end_frame=73,setpts=PTS-STARTPTS[body];
  [c2]trim=start_frame=73:end_frame=81,setpts=PTS-STARTPTS[tail];
  [c3]trim=start_frame=0:end_frame=${FADE_FRAMES},setpts=PTS-STARTPTS[head];
  [tail][head]xfade=transition=fade:duration=0.5:offset=0[seam];
  [body][seam]concat=n=2:v=1[unit];
  [unit]loop=loop=${LOOPS}:size=32767,setpts=N/FRAME_RATE/TB,scale=1080:1920:flags=lanczos[out]" \
  -map "[out]" -r ${FPS} -c:v libx264 -pix_fmt yuv420p -crf 18 -an "${OUT}_loop.mp4"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${OUT}_loop.mp4")
echo "loop: ${OUT}_loop.mp4 (${DUR}s)"

if [ -n "$MUSIC" ]; then
  FADE_OUT_START=$(python3 -c "print(max(0, float('$DUR') - 2))")
  ffmpeg -v error -y -i "${OUT}_loop.mp4" -i "$MUSIC" -filter_complex \
    "[1:a]atrim=0:${DUR},afade=t=in:st=0:d=1,afade=t=out:st=${FADE_OUT_START}:d=2,volume=0.9[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "${OUT}_final.mp4"
  echo "final: ${OUT}_final.mp4"
fi
