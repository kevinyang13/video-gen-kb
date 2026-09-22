#!/usr/bin/env bash
# Render scripts/infographics/<name>.html -> wiki/assets/<name>-3d.webp
# using headless Chrome at 2x (3200x2200). Usage: scripts/render_infographic.sh video-generation-landscape
set -euo pipefail
name="${1:?usage: render_infographic.sh <name>}"
root="$(cd "$(dirname "$0")/.." && pwd)"
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
tmp="$(mktemp -d)/shot.png"
"$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1600,1100 --screenshot="$tmp" "file://$root/scripts/infographics/$name.html" 2>/dev/null
mkdir -p "$root/wiki/assets"
cwebp -quiet -q 88 -m 6 "$tmp" -o "$root/wiki/assets/$name-3d.webp"
echo "wrote wiki/assets/$name-3d.webp ($(du -h "$root/wiki/assets/$name-3d.webp" | cut -f1))"
