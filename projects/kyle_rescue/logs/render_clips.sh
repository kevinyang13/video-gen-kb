#!/usr/bin/env bash
# LTX-2.3 I2V for every Kyle shot still (headless). Skips clips that already exist.
cd /Users/kevinyang/dev/video-gen-kb
K=raw/clips/kyle
for s in ${SHOTS:-s2 s3 s5 s7 s4 s1 s6 s8}; do
  out=$K/clips/${s}_ltx_v${V:-1}.mov; [ -f "$out" ] && continue
  t0=$(date +%s)
  draw-things-cli generate -m ltx_2.3_22b_distilled_1.1_q8p.ckpt \
    --prompt-file $K/stills/${s}_v.txt --image $K/stills/${s}.png \
    --width 576 --height 1024 --frames 249 --steps 8 --cfg 1 --seed ${SEED:-1} \
    --config-json '{"sampler":19,"shift":5.0,"stochasticSamplingGamma":0.3,"fps":25,"hiresFix":false}' \
    --offline --disable-preview --video-format prores422hq -o "$out" >/dev/null 2>&1
  echo "$s $? $(( $(date +%s)-t0 ))s $(date +%H:%M)" >> $K/render.log
done
echo "ALL DONE $(date +%H:%M)" >> $K/render.log
