#!/usr/bin/env bash
# Manage Draw Things projects from the shell. A project is just
#   ~/Library/Containers/com.liuliu.draw-things/Data/Documents/NAME.sqlite3 (+ -shm/-wal)
# so renaming the files renames the project; the Projects list picks it up live.
#
#   scripts/dt_project.sh list                 # names, sizes, mtimes
#   scripts/dt_project.sh rename OLD NEW       # OLD must not be the open project
#   scripts/dt_project.sh newest               # most recently modified project (the one just created)
#   scripts/dt_project.sh rename-newest NEW    # rename the newest Untitled-* -> NEW
#   scripts/dt_project.sh delete NAME          # moves the files to ~/.Trash
set -euo pipefail
D="$HOME/Library/Containers/com.liuliu.draw-things/Data/Documents"
cmd="${1:-list}"

names() { ls "$D" | grep -E '\.sqlite3$' | sed 's/\.sqlite3$//'; }
files() { for e in sqlite3 sqlite3-shm sqlite3-wal; do [ -e "$D/$1.$e" ] && echo "$D/$1.$e"; done; return 0; }

case "$cmd" in
  list)
    for n in $(names); do printf "%-24s %8s  %s\n" "$n" "$(du -h "$D/$n.sqlite3" | cut -f1)" "$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$D/$n.sqlite3")"; done | sort -k3 ;;
  newest)
    ls -t "$D"/*.sqlite3 | head -1 | xargs basename | sed 's/\.sqlite3$//' ;;
  rename)
    old="${2:?old name}"; new="${3:?new name}"
    [ -e "$D/$old.sqlite3" ] || { echo "no project '$old'" >&2; exit 1; }
    [ -e "$D/$new.sqlite3" ] && { echo "'$new' already exists" >&2; exit 1; }
    for f in $(files "$old"); do mv "$f" "${f/$old./$new.}"; done
    echo "renamed $old -> $new" ;;
  rename-newest)
    new="${2:?new name}"; old="$("$0" newest)"
    case "$old" in Untitled-*) "$0" rename "$old" "$new" ;; *) echo "newest project is '$old', not Untitled-* — refusing" >&2; exit 1 ;; esac ;;
  delete)
    n="${2:?name}"; for f in $(files "$n"); do mv "$f" ~/.Trash/; done; echo "trashed $n" ;;
  *) echo "usage: $0 list|newest|rename OLD NEW|rename-newest NEW|delete NAME" >&2; exit 1 ;;
esac
