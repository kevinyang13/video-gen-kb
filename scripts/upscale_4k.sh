#!/usr/bin/env bash
# Upscale a clip with Real-ESRGAN (ncnn/Vulkan, Apple Silicon), then fit it to an exact output size.
#   scripts/upscale_4k.sh IN.mov [outname] [model]
# model: realesrgan-x4plus (default; 3D renders, photoreal — fur, snow, water)
#        realesr-animevideov3-x4 (flat 2D line art; faster) — also -x2 / -x3, or SCALE=2|3 with it
# Output: <outname>_4k.mp4 (HEVC 10-bit via videotoolbox, input fps).
# Env:
#   W=3840 H=2160   output size (portrait: W=2160 H=3840; 1080p: W=1920 H=1080)
#   FIT=crop        crop = fill the frame and centre-crop the overflow; pad = letter/pillar-box in black
#   BITRATE=40M     video bitrate (12M is plenty for 1080p)
#   KEEP_AUDIO=0    1 = copy the input's audio track into the output (AAC 192k)
#   SCALE=          model scale; x4plus is always 4, realesr-animevideov3 can be 2/3/4 (a 1080p target
#                   from 576p needs only 2x — faster). Default: from the model name, else 4.
#   KEEP_FRAMES=1   0 = delete the upscaled PNG folder after encoding (~1-2 GB per 10 s clip)
set -euo pipefail

IN="${1:?input .mov/.mp4}"
OUT="${2:-${IN%.*}}"
MODEL="${3:-realesrgan-x4plus}"; MODEL_ARG="$MODEL"
W="${W:-3840}"; H="${H:-2160}"; FIT="${FIT:-crop}"; BITRATE="${BITRATE:-40M}"
KEEP_AUDIO="${KEEP_AUDIO:-0}"; KEEP_FRAMES="${KEEP_FRAMES:-1}"
ESR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/realesrgan"   # binary resolves models relative to cwd

die() { echo "upscale_4k: $*" >&2; exit 1; }
[ -f "$IN" ] || die "input not found: $IN"
case "$MODEL" in
  realesrgan-x4plus*) SCALE=4 ;;
  *-x2) SCALE=2; MODEL="${MODEL%-x2}" ;; *-x3) SCALE=3; MODEL="${MODEL%-x3}" ;; *-x4) SCALE=4; MODEL="${MODEL%-x4}" ;;
  *) SCALE="${SCALE:-4}" ;;
esac
MF="$MODEL"; [[ "$MODEL" == realesr-animevideov3 ]] && MF="$MODEL-x$SCALE"
[ -f "$ESR_DIR/models/$MF.param" ] || die "unknown model '$MODEL_ARG' (scale $SCALE) (have: $(ls "$ESR_DIR/models" | sed -n 's/\.param$//p' | tr '\n' ' '))"
(( W % 2 == 0 && H % 2 == 0 )) || die "W and H must be even (got ${W}x${H})"
case "$FIT" in
  crop) VF="scale=${W}:${H}:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}:${H}" ;;
  pad)  VF="scale=${W}:${H}:force_original_aspect_ratio=decrease:flags=lanczos,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2:black" ;;
  *) die "FIT must be crop or pad" ;;
esac
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$IN" | awk -F/ '{printf "%.4f", $1/$2}')
IFS=, read -r IW IH < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$IN")
(( IW * SCALE < W || IH * SCALE < H )) && echo "upscale_4k: note — ${IW}x${IH} x${SCALE} is still smaller than ${W}x${H}; the last step upsamples" >&2
if (( IW * IH * SCALE * SCALE > W * H * 4 )); then echo "upscale_4k: note — ${IW}x${IH} x${SCALE} is far above ${W}x${H}; a plain lanczos scale may be enough" >&2; fi

IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"; mkdir -p "$(dirname "$OUT")"; OUT="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
SRC="${OUT}_src_frames"; DST="${OUT}_4k_frames"
rm -rf "$SRC" "$DST"; mkdir -p "$SRC" "$DST"

# 1. frames out (16-bit PNG keeps the ProRes precision)
ffmpeg -nostdin -v error -i "$IN" "$SRC/%04d.png"

# 2. SCALEx upscale, whole directory in one process (model load once)
LOG="${OUT}_esrgan.log"   # progress spam goes here; shown only on failure
( cd "$ESR_DIR" && ./realesrgan-ncnn-vulkan -i "$SRC" -o "$DST" -n "$MODEL" -f png -s "$SCALE" -t 128 -j 1:1:1 >"$LOG" 2>&1 ) \
  || { tail -5 "$LOG" >&2; die "Real-ESRGAN failed (log: $LOG)"; }   # -t 128 and -j 1:1:1: without them it segfaults on Metal
[ "$(ls "$DST" | wc -l)" -eq "$(ls "$SRC" | wc -l)" ] || die "Real-ESRGAN produced $(ls "$DST" | wc -l) of $(ls "$SRC" | wc -l) frames"

# 3. fit the upscaled result to exactly WxH, encode (+ optional audio from the input)
aud=(-map 0:v -an)
if [ "$KEEP_AUDIO" = "1" ] && ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | grep -q .; then
  aud=(-map 0:v -map 1:a -c:a aac -b:a 192k)   # no -shortest: it drops the last video frame
fi
ffmpeg -nostdin -v error -y -framerate "$FPS" -i "$DST/%04d.png" -i "$IN" -vf "$VF" \
  -c:v hevc_videotoolbox -profile:v main10 -pix_fmt p010le -b:v "$BITRATE" -tag:v hvc1 "${aud[@]}" "${OUT}_4k.mp4"

rm -rf "$SRC" "$LOG"; [ "$KEEP_FRAMES" = "1" ] || rm -rf "$DST"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames,codec_name,pix_fmt -of csv=p=0 "${OUT}_4k.mp4"
echo "4k: ${OUT}_4k.mp4$([ "$KEEP_FRAMES" = "1" ] && echo "   (frames kept in $DST)")"
