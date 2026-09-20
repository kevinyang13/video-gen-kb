#!/usr/bin/env bash
# Rebuild the site from wiki/ and serve docs/ over http.
set -euo pipefail

PORT="${1:-8788}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$DIR/scripts/build_site.py"
echo "video-gen-kb → http://localhost:${PORT}/"
echo "Ctrl-C to stop."

exec python3 -m http.server "$PORT" --directory "$DIR/docs"
