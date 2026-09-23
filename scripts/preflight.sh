#!/usr/bin/env bash
# Pre-run checks for an unattended render. Exit 1 if anything blocking fails.
#   scripts/preflight.sh [--fix] [model.ckpt ...]
# --fix: quit the Draw Things app (it holds GPU memory and halves CLI speed) and start
#        caffeinate for 14 h so the Mac can't sleep (kill it when the run is done).
# Models: checked in the app's Models/ folder (DRAWTHINGS_MODELS_DIR overrides). Default:
#         the klein still model and the LTX clip model.
set -uo pipefail

FIX=0; [ "${1:-}" = "--fix" ] && { FIX=1; shift; }
MODELS=("$@"); [ ${#MODELS[@]} -gt 0 ] || MODELS=(flux_2_klein_9b_i8x.ckpt ltx_2.3_22b_distilled_1.1_q8p.ckpt)
MD="${DRAWTHINGS_MODELS_DIR:-$HOME/Library/Containers/com.liuliu.draw-things/Data/Documents/Models}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
bad=0
ok()   { printf "  ok    %s\n" "$*"; }
warn() { printf "  WARN  %s\n" "$*"; }
fail() { printf "  FAIL  %s\n" "$*"; bad=1; }

echo "preflight:"
command -v draw-things-cli >/dev/null && ok "draw-things-cli $(draw-things-cli --version 2>/dev/null | head -1)" || fail "draw-things-cli not installed (brew install drawthingsai/draw-things/draw-things-cli)"
command -v ffmpeg >/dev/null && ok "ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}')" || fail "ffmpeg missing"
[ -x "$ROOT/tools/realesrgan/realesrgan-ncnn-vulkan" ] && ok "Real-ESRGAN ncnn" || fail "tools/realesrgan/realesrgan-ncnn-vulkan missing"
for m in "${MODELS[@]}"; do [ -f "$MD/$m" ] && ok "model $m" || fail "model not found: $MD/$m"; done

pmset -g batt | grep -q "AC Power" && ok "on AC power" || warn "on battery — plug in for an overnight run"
free=$(df -g "$ROOT" | awk 'NR==2{print $4}')
(( free >= 50 )) && ok "disk ${free} GB free" || { (( free >= 20 )) && warn "disk only ${free} GB free (upscale frames need ~2 GB per clip)" || fail "disk ${free} GB free"; }

if pgrep -x DrawThings >/dev/null; then
  if [ "$FIX" = 1 ]; then osascript -e 'tell application "Draw Things" to quit' >/dev/null 2>&1; sleep 3
    pgrep -x DrawThings >/dev/null && fail "Draw Things app still running" || ok "Draw Things app quit"
  else warn "Draw Things app is open — quit it (holds GPU memory, CLI runs ~2x slower); --fix does it"; fi
else ok "Draw Things app closed"; fi

if pgrep -x caffeinate >/dev/null; then ok "caffeinate running"
elif [ "$FIX" = 1 ]; then nohup caffeinate -dis -t 50400 >/dev/null 2>&1 & ok "caffeinate started (pid $!, 14 h)"
else warn "caffeinate not running — the Mac may sleep; --fix starts it"; fi

pgrep -f "draw-things-cli generate" >/dev/null && warn "another draw-things-cli job is running"
pgrep -f realesrgan-ncnn >/dev/null && warn "Real-ESRGAN is running — never overlap it with LTX (memory)"

[ $bad = 0 ] && echo "preflight: PASS" || echo "preflight: FAIL"
exit $bad
