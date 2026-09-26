#!/usr/bin/env bash
# Trim -> 4K portrait upscale -> assemble -> music tail. Logs to finish.log.
set -uo pipefail
cd /Users/kevinyang/dev/video-gen-kb
K=raw/clips/kyle; L=$K/finish.log
# shot  clip           start  end
spec="s1 s1_ltx_v1 0 6.5
s2 s2_ltx_v2 0 8
s3 s3_ltx_v1 0 9.96
s4 s4_ltx_v2 0 9.96
s5 s5_ltx_v1 0 6
s6 s6_ltx_v1 1.6 8.8
s7 s7_ltx_v1 0 8
s8 s8_ltx_v1 0 9.6"
list=()
while read -r s c a b <&3; do
  if [ -f $K/final/${s}_4k.mp4 ]; then list+=($K/final/${s}_4k.mp4); continue; fi
  t0=$(date +%s)
  ffmpeg -nostdin -v error -y -i $K/clips/$c.mov -vf "trim=start=$a:end=$b,setpts=PTS-STARTPTS" -an -c:v prores_ks -profile:v 3 $K/final/${s}_t.mov
  W=2160 H=3840 scripts/upscale_4k.sh $K/final/${s}_t.mov $K/final/$s realesrgan-x4plus </dev/null >/dev/null 2>&1
  rc=$?; rm -rf $K/final/${s}_4k_frames
  echo "$s upscale rc=$rc $(( $(date +%s)-t0 ))s $(date +%H:%M)" >> $L
  list+=($K/final/${s}_4k.mp4)
done 3<<< "$spec"
W=2160 H=3840 XFADE=0.75 scripts/assemble_film.sh $K/final/film_nomusic.mp4 "${list[@]}" >> $L 2>&1
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $K/final/film_nomusic.mp4)
SS=$(python3 -c "print(max(0,153.4-$D))")
ffmpeg -v error -y -ss $SS -i raw/clips/music/best_adventure_ever.mp3 -t $D -af "afade=t=in:d=1.5" $K/final/music_bed.wav
ffmpeg -v error -y -i $K/final/film_nomusic.mp4 -i $K/final/music_bed.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $K/final/kyle_rescue_2160x3840.mp4
ffmpeg -v error -y -i $K/final/kyle_rescue_2160x3840.mp4 -vf scale=1080:1920:flags=lanczos -c:v hevc_videotoolbox -b:v 12M -tag:v hvc1 -c:a copy -movflags +faststart $K/final/kyle_rescue_1080x1920.mp4
echo "FINISHED D=$D music_ss=$SS $(date +%H:%M)" >> $L
