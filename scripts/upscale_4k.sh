#!/usr/bin/env bash
# Upscale a Draw Things I2V export to 3840x2160 with Real-ESRGAN (ncnn/Vulkan, Apple Silicon).
#   scripts/upscale_4k.sh raw/clips/scene1a.mov [outname] [model]
# model: realesrgan-x4plus (default, photoreal) | realesr-animevideov3-x4 (anime, faster)
# Output: <outname>_4k.mp4 (HEVC 10-bit via videotoolbox, 16 fps, no audio) + <outname>_4k_frames/ kept for reuse.
set -euo pipefail

IN="${1:?input .mov/.mp4}"
OUT="${2:-${IN%.*}}"
MODEL="${3:-realesrgan-x4plus}"
ESR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/realesrgan"   # binary resolves models relative to cwd
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$IN" | awk -F/ '{printf "%.4f", $1/$2}')

IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"; OUT="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
SRC="${OUT}_src_frames"; DST="${OUT}_4k_frames"
rm -rf "$SRC" "$DST"; mkdir -p "$SRC" "$DST"

# 1. frames out (16-bit PNG keeps the ProRes precision)
ffmpeg -v error -i "$IN" "$SRC/%04d.png"

# 2. 4x upscale, whole directory in one process (model load once)
( cd "$ESR_DIR" && ./realesrgan-ncnn-vulkan -i "$SRC" -o "$DST" -n "$MODEL" -f png -s 4 -t 128 -j 1:1:1 >/dev/null )   # -t 128: auto/256 tile segfaults on Metal

# 3. downscale 4x result to exactly 3840x2160 (input aspect may not be 16:9: crop to fit), encode
ffmpeg -v error -y -framerate "$FPS" -i "$DST/%04d.png" \
  -vf "scale=3840:2160:force_original_aspect_ratio=increase:flags=lanczos,crop=3840:2160" \
  -c:v hevc_videotoolbox -profile:v main10 -pix_fmt p010le -b:v 40M -tag:v hvc1 -an "${OUT}_4k.mp4"

rm -rf "$SRC"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames,codec_name,pix_fmt -of csv=p=0 "${OUT}_4k.mp4"
echo "4k: ${OUT}_4k.mp4   (frames kept in $DST)"
