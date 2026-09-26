#!/usr/bin/env bash
# Turn one master portrait into a multi-angle seed sheet.
#   scripts/seed_sheet.sh MASTER.png OUT_PREFIX [SUBJECT] [SEED]
# Renders three more views by editing the master (klein strength 1.0), then
# composes front | three-quarter | profile | back into OUT_PREFIX_sheet.png.
#
# A single frontal reference gives the model nothing to copy for a profile, so
# it invents one — see wiki/identity-conditioning.md. With a sheet you crop the
# angle a shot needs and hand that over as the reference instead.
#
#   SUBJECT   noun used in the prompts (or pass it as arg 3), default "character"
#   STYLE     one line describing the look; default matches our 3D-animated films
#   VIEWS     which views to render, default "34 side back"
#   W H       size of each view, default 512x768
set -euo pipefail

MASTER="${1:?master .png}"; OUT="${2:?output prefix}"; SUBJ="${3:-${SUBJECT:-character}}"; SEED="${4:-1}"
STYLE="${STYLE:-in the same style and the same soft studio lighting on the same plain grey background}"
VIEWS="${VIEWS:-34 side back}"
W="${W:-512}"; H="${H:-768}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

keep="exactly the same face, hair, colours and clothing, no change to the features, no change to the age"
case_prompt () {
  case "$1" in
    34)   echo "The same $SUBJ, $keep, $STYLE. Turn to a three-quarter view, rotated about 45 degrees so one side of the face and the jawline are visible, still looking toward the camera." ;;
    side) echo "The same $SUBJ, $keep, $STYLE. Turn to a full side profile, exactly 90 degrees, so only the side is visible — the line of the nose, lips, chin and ear read as a silhouette against the background." ;;
    back) echo "The same $SUBJ, $keep, $STYLE. Seen from directly behind, the back of the head and shoulders filling the frame, the hairline and the back of the haircut clearly visible, the face not visible at all." ;;
    *)    echo "The same $SUBJ, $keep, $STYLE. $1" ;;
  esac
}

imgs=("$MASTER")
IFS="|" read -r -a VIEWLIST <<< "${VIEWS// /|}"
if [[ "$VIEWS" == *"|"* ]]; then IFS="|" read -r -a VIEWLIST <<< "$VIEWS"; fi
for v in "${VIEWLIST[@]}"; do
  [ -n "$v" ] || continue
  case_prompt "$v" > "$TMP/p.txt"
  slug=$(echo "$v" | tr -cd "[:alnum:] " | tr " " "_" | cut -c1-24)
  out="${OUT}_${slug}.png"
  echo "  ${slug} …"
  "$DIR/dt_diptych.sh" - "$MASTER" "$TMP/p.txt" "$out" "$SEED" "$W" "$H" >/dev/null
  imgs+=("$out")
done

# compose: front | 34 | side | back
args=(); filt=""; i=0
for f in "${imgs[@]}"; do args+=(-i "$f"); filt+="[$i]scale=${W}:${H}[v$i];"; i=$((i+1)); done
for ((j=0;j<i;j++)); do filt+="[v$j]"; done
filt+="hstack=$i"
ffmpeg -v error -y "${args[@]}" -filter_complex "$filt" "${OUT}_sheet.png"
echo "sheet: ${OUT}_sheet.png  (${i} views)"
