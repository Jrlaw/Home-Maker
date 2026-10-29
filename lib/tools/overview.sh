#!/usr/bin/env bash
# Labeled overview sheet of a room's standard views (2 columns), e.g. renders/latest/overview_day.jpg.
# Usage: lib/tools/overview.sh <renders dir> <title> <out.jpg> camera:"Label" [camera:"Label" ...]
set -euo pipefail
dir=$1; title=$2; out=$3; shift 3
args=()
for pair in "$@"; do
  cam=${pair%%:*}; label=${pair#*:}
  args+=(-label "$label" "$dir/$cam.jpg")
done
magick montage "${args[@]}" -tile 2x -geometry 900x675+8+8 -pointsize 22 -background "#f4f1ea" \
  -title "$title" "$out"
echo "$out"
