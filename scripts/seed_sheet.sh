#!/usr/bin/env bash
# Turn one master portrait into a multi-angle seed sheet, or into a LoRA dataset.
#   scripts/seed_sheet.sh MASTER.png OUT_PREFIX [SUBJECT] [SEED]
#   scripts/seed_sheet.sh --dataset MASTER.png OUT_DIR [SUBJECT] [TRIGGER]
#
# SHEET MODE renders three more views by editing the master (klein strength 1.0), then
# composes front | three-quarter | profile | back into OUT_PREFIX_sheet.png.
#
# A 90-degree turn invites a Janus artifact: klein keeps the frontal face and adds a
# profile beside it, ear in the middle. The side prompt bans it explicitly; check the
# output anyway and re-roll the seed if two faces appear.
#
# A single frontal reference gives the model nothing to copy for a profile, so
# it invents one — see wiki/identity-conditioning.md. With a sheet you crop the
# angle a shot needs and hand that over as the reference instead.
#
#   SUBJECT   noun used in the prompts (or pass it as arg 3), default "character"
#   STYLE     one line describing the look; default matches our 3D-animated films
#   VIEWS     which views to render, default "34 side back"
#   W H       size of each view, default 512x768
#
# DATASET MODE (experiment B0, wiki/blueprint-v2-research.md) renders 30 training
# images over framing x angle x lighting x expression x wardrobe x background, and
# writes a caption .txt beside each one. Two different strings per image:
#   the PROMPT names every feature to preserve  (our reference-token practice)
#   the CAPTION names only what VARIES          (the LoRA Isolation Rule)
# Permanent features are deliberately absent from the caption so they bind to the
# trigger token instead of to words the prompt can later contradict.
#
#   TRIGGER   token every caption starts with (arg 5), default "sks_character"
#   KEEP      the preserve clause used in every prompt; set this per character
#   CELLS     override the cell list (one "framing angle light expr wardrobe bg" per line)
#   ONLY      render only these cell numbers, e.g. ONLY="1 2 30" — for a cheap preview
#   WD HD     portrait size, default 512x768
#   REF_<angle>  reference image to use for that angle instead of MASTER, e.g.
#                REF_back=seed/hunter_back.png REF_side=seed/hunter_side.png
#
# FRAMING FOLLOWS THE REFERENCE, NOT THE PROMPT. klein re-composes only as far as the
# output aspect forces it: a head-and-shoulders master asked for a medium shot comes back
# a head-and-shoulders shot. So framing sets the canvas — close = WD x HD portrait,
# medium = square, wide = HD x WD landscape — and that is what actually moves the camera back.
# The same rule kills "back of the head" and camera-height cells: give them a reference that
# already shows that angle (REF_back from a turnaround sheet) or they come back frontal.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------- dataset mode
if [ "${1:-}" = "--dataset" ]; then
  shift
  MASTER="${1:?master .png}"; OUTDIR="${2:?output dir}"
  SUBJ="${3:-${SUBJECT:-character}}"; TRIGGER="${4:-${TRIGGER:-sks_character}}"
  WD="${WD:-512}"; HD="${HD:-768}"
  KEEP="${KEEP:-exactly the same face and the same features, the same age, the same hair, no change to the identity}"
  mkdir -p "$OUTDIR"

  # caption phrase | prompt sentence, for each axis value
  cap () { case "$1" in
    close)   echo "close-up portrait" ;;
    medium)  echo "medium shot, waist up" ;;
    wide)    echo "full body wide shot, small in frame" ;;
    front)   echo "facing the camera" ;;
    34)      echo "three-quarter view" ;;
    side)    echo "side profile" ;;
    back)    echo "seen from behind" ;;
    shoulder) echo "looking back over one shoulder" ;;
    low)     echo "low camera angle looking up" ;;
    high)    echo "high camera angle looking down" ;;
    studio)  echo "soft even studio light" ;;
    overcast) echo "flat overcast daylight" ;;
    golden)  echo "warm low golden-hour sun" ;;
    noon)    echo "hard noon sunlight, strong shadows" ;;
    shade)   echo "cool blue open shade" ;;
    fire)    echo "orange firelight from below" ;;
    rim)     echo "backlit with a bright rim light" ;;
    window)  echo "soft directional window light" ;;
    storm)   echo "dim grey storm light" ;;
    moon)    echo "cold blue moonlight" ;;
    neutral) echo "neutral expression" ;;
    smile)   echo "a faint smile" ;;
    focused) echo "a focused, narrowed gaze" ;;
    alert)   echo "alert, eyes wide" ;;
    weary)   echo "weary and tired" ;;
    laugh)   echo "laughing" ;;
    frown)   echo "brow furrowed, frowning" ;;
    speak)   echo "mouth open mid-speech" ;;
    closed)  echo "eyes closed" ;;
    armour)  echo "wearing worn leather armour" ;;
    hoodup)  echo "the hood pulled up" ;;
    nocloak) echo "no cloak, undershirt only" ;;
    tunic)   echo "a plain linen tunic" ;;
    fur)     echo "a heavy fur cloak" ;;
    bare)    echo "bare shoulders with a single leather strap" ;;
    wet)     echo "a rain-soaked cloak" ;;
    grey)    echo "a plain grey studio backdrop" ;;
    grass)   echo "open sunlit grassland" ;;
    forest)  echo "a dense forest edge" ;;
    camp)    echo "a night camp beside a fire" ;;
    city)    echo "a stone city street" ;;
    river)   echo "a river bank" ;;
    hall)    echo "a dim stone hall" ;;
    *) echo "$1" ;;
  esac; }

  sent () { case "$1" in
    close)   echo "A close-up portrait, the head and shoulders filling the frame." ;;
    medium)  echo "A medium shot from the waist up, the upper body clearly visible." ;;
    wide)    echo "A full-length wide shot, the whole body visible from head to feet, standing small in a large scene." ;;
    front)   echo "Facing the camera straight on." ;;
    34)      echo "Turned to a three-quarter view, rotated about 45 degrees." ;;
    side)    echo "A true side profile seen from exactly 90 degrees, only ONE eye visible, exactly one face in the image, no second face on the other side of the head." ;;
    back)    echo "Seen from directly behind, the face not visible at all." ;;
    shoulder) echo "Turned away but looking back over one shoulder toward the camera." ;;
    low)     echo "Shot from a very low angle: the camera is down near the ground and tilted up, so the jaw and chin are seen from underneath and the sky fills the background behind the head." ;;
    high)    echo "Shot from a very high angle: the camera is well above the head and tilted down, so the top of the head and the shoulders are seen from above and the ground fills the background." ;;
    studio)  echo "Soft even studio lighting." ;;
    overcast) echo "Flat overcast daylight, soft shadowless light." ;;
    golden)  echo "Warm low golden-hour sun raking from one side." ;;
    noon)    echo "Hard overhead noon sunlight with strong contrasty shadows." ;;
    shade)   echo "Cool blue light of open shade." ;;
    fire)    echo "Orange firelight from below, deep shadows above." ;;
    rim)     echo "Backlit, a bright rim of light along the edge of the head and shoulders." ;;
    window)  echo "Soft directional light from a window on one side." ;;
    storm)   echo "Dim grey storm light, heavy clouds, no direct sun." ;;
    moon)    echo "Cold blue moonlight, very low key." ;;
    neutral) echo "A neutral expression." ;;
    smile)   echo "A faint smile." ;;
    focused) echo "A focused, narrowed gaze." ;;
    alert)   echo "Alert, eyes wide, head slightly raised." ;;
    weary)   echo "Weary and tired, shoulders low." ;;
    laugh)   echo "Laughing openly." ;;
    frown)   echo "Brow furrowed, frowning." ;;
    speak)   echo "Mouth open mid-speech." ;;
    closed)  echo "Eyes closed." ;;
    armour)  echo "Wearing the worn leather armour." ;;
    hoodup)  echo "The hood pulled up over the head." ;;
    nocloak) echo "No cloak and no shoulder armour, the undershirt only." ;;
    tunic)   echo "Wearing a plain undyed linen tunic instead of armour." ;;
    fur)     echo "Wearing a heavy fur cloak over the shoulders." ;;
    bare)    echo "Bare shoulders with a single leather strap across the chest." ;;
    wet)     echo "Wearing a rain-soaked cloak, wet hair and skin." ;;
    grey)    echo "Standing against a plain grey studio backdrop." ;;
    grass)   echo "In open sunlit grassland, tall grass around." ;;
    forest)  echo "At a dense forest edge, trees behind." ;;
    camp)    echo "At a night camp beside a fire." ;;
    city)    echo "In a stone city street." ;;
    river)   echo "On a river bank, water behind." ;;
    hall)    echo "In a dim stone hall." ;;
    *) echo "$1" ;;
  esac; }

  # 30 cells: 12 close, 12 medium, 6 wide (the 40/40/20 split in the source).
  # Identity is the only constant; every other axis moves.
  DEFAULT_CELLS="close front studio neutral armour grey
close 34 golden smile armour grass
close side overcast focused hoodup forest
close 34 fire weary nocloak camp
close front window speak tunic hall
close high noon alert armour grass
close shoulder shade frown fur forest
close side rim laugh nocloak river
close low moon focused hoodup camp
close 34 storm alert wet forest
close front overcast closed bare grey
close back studio neutral armour grey
medium front studio neutral armour grey
medium 34 golden focused armour grass
medium side noon alert nocloak city
medium back overcast neutral fur forest
medium shoulder fire smile hoodup camp
medium 34 shade weary tunic river
medium front rim laugh nocloak grass
medium low storm frown wet forest
medium high window focused armour hall
medium side moon neutral hoodup camp
medium 34 overcast speak tunic city
medium front noon alert bare river
wide front golden neutral armour grass
wide 34 overcast focused fur forest
wide back noon neutral armour city
wide side shade weary tunic river
wide front fire alert hoodup camp
wide 34 storm focused wet grass"
  CELLS="${CELLS:-$DEFAULT_CELLS}"

  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  n=0; made=0
  while read -r framing angle light expr dress bg; do
    [ -n "${framing:-}" ] || continue
    n=$((n+1))
    if [ -n "${ONLY:-}" ] && ! grep -qw "$n" <<< "$ONLY"; then continue; fi
    id=$(printf "ds_%02d" "$n")
    case "$framing" in
      wide)   w="$HD"; h="$WD" ;;
      medium) w="$HD"; h="$HD" ;;
      *)      w="$WD"; h="$HD" ;;
    esac
    # a frontal master cannot show a back or a profile; use the matching sheet panel if given
    refvar="REF_${angle}"; ref="${!refvar:-$MASTER}"

    # PROMPT: name everything to preserve — klein substitutes its own face otherwise.
    { echo "The same $SUBJ, $KEEP."
      sent "$framing"; sent "$angle"; sent "$dress"; sent "$bg"; sent "$light"; sent "$expr"
      echo "Photorealistic, highly detailed, one person only, no text, no lettering, no logos."
    } | tr "\n" " " > "$TMP/p.txt"; echo >> "$TMP/p.txt"

    # CAPTION: only what varies. Face, ears, markings and hair are absent on purpose.
    printf "%s, %s, %s, %s, %s, %s, %s\n" "$TRIGGER" \
      "$(cap "$framing")" "$(cap "$angle")" "$(cap "$dress")" \
      "$(cap "$bg")" "$(cap "$light")" "$(cap "$expr")" > "$OUTDIR/$id.txt"

    echo "  $id  $framing/$angle/$light/$expr/$dress/$bg  ${w}x${h}"
    if [ -z "${DRY_RUN:-}" ]; then
      "$DIR/dt_diptych.sh" - "$ref" "$TMP/p.txt" "$OUTDIR/$id.png" "$n" "$w" "$h" >/dev/null
      made=$((made+1))
    else
      cat "$TMP/p.txt"
    fi
  done <<< "$CELLS"
  echo "dataset: $OUTDIR  ($made images, $n cells)"
  exit 0
fi

# ------------------------------------------------------------------ sheet mode
MASTER="${1:?master .png}"; OUT="${2:?output prefix}"; SUBJ="${3:-${SUBJECT:-character}}"; SEED="${4:-1}"
STYLE="${STYLE:-in the same style and the same soft studio lighting on the same plain grey background}"
VIEWS="${VIEWS:-34 side back}"
W="${W:-512}"; H="${H:-768}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

keep="exactly the same face, hair, colours and clothing, no change to the features, no change to the age"
case_prompt () {
  case "$1" in
    34)   echo "The same $SUBJ, $keep, $STYLE. Turn to a three-quarter view, rotated about 45 degrees so one side of the face and the jawline are visible, still looking toward the camera." ;;
    side) echo "The same $SUBJ, $keep, $STYLE. A true side profile seen from exactly 90 degrees: the head is turned so the nose, lips and chin form the outline against the background, only ONE eye is visible, and the far cheek is hidden behind the near one. Exactly one face in the image — do not draw a second face on the other side of the head, do not show both eyes, do not merge two views." ;;
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
