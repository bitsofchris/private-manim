#!/usr/bin/env bash
# Contact sheet of evenly spaced frames at phone-ish size, for layout review.
#
# Usage:
#   tools/review_frames.sh [--at T1,T2,...] <video.mp4|anim.gif> [cols] [frames] [out.png]
# Defaults: cols=4, frames=2*cols, each tile 360 px wide (a phone held at
# arm's length), out=$REVIEW_DIR or $TMPDIR/manim-review/<name>_sheet.png.
# The first tile is frame 0 (what the viewer sees before deciding to swipe);
# the last tile is always the final frame (the hold, and the next cut's match).
# --at adds tiles at those seconds (cue times: did the change land on its word?),
# in time order among the even ones.
# Prints the sheet path and the timestamp of each tile, left-to-right, top-down.
set -euo pipefail
at=""
if [[ "${1:-}" == "--at" ]]; then at="${2:?--at needs T1,T2,...}"; shift 2; fi
in="${1:?usage: review_frames.sh [--at T1,T2,...] <video> [cols] [frames] [out.png]}"
cols="${2:-4}"
frames="${3:-$((cols * 2))}"
name="$(basename "${in%.*}")"
dir="${REVIEW_DIR:-${TMPDIR:-/tmp}/manim-review}"
out="${4:-$dir/${name}_sheet.png}"
mkdir -p "$(dirname "$out")"

dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# Even tiles (frame 0 first), the final frame (a frame before the end, so the
# seek lands on a picture), and any --at times; sorted, duplicates dropped.
list="$(
  {
    awk -v n="$frames" -v d="$dur" 'BEGIN { m = (n > 1 ? n - 1 : 1); for (i = 0; i < n - 1; i++) printf "%.3f\n", i * d / m }'
    awk -v d="$dur" 'BEGIN { t = d - 0.04; if (t < 0) t = 0; printf "%.3f\n", t }'
    if [[ -n "$at" ]]; then tr ',' '\n' <<<"$at" | awk 'NF { printf "%.3f\n", $1 }'; fi
  } | sort -n -u
)"
times=()
i=0
while read -r t; do
  times+=("${t}s")
  # Seek to each timestamp exactly (the fps filter drifts by up to half a step).
  ffmpeg -y -loglevel error -ss "$t" -i "$in" -frames:v 1 \
    -vf "scale=360:-2:flags=lanczos" "$tmp/$(printf '%03d' "$i").png"
  i=$((i + 1))
done <<<"$list"
rows=$(( (i + cols - 1) / cols ))
ffmpeg -y -loglevel error -framerate 1 -i "$tmp/%03d.png" \
  -vf "tile=${cols}x${rows}:padding=6:color=white" -frames:v 1 -update 1 "$out"

echo "$out"
echo "tiles at: ${times[*]}"
