#!/usr/bin/env bash
# Contact sheet of evenly spaced frames at phone-ish size, for layout review.
#
# Usage:
#   tools/review_frames.sh <video.mp4|anim.gif> [cols] [frames] [out.png]
# Defaults: cols=4, frames=2*cols, each tile 360 px wide (a phone held at
# arm's length), out=$REVIEW_DIR or $TMPDIR/manim-review/<name>_sheet.png.
# The first tile is frame 0 (what the viewer sees before deciding to swipe).
# Prints the sheet path and the timestamp of each tile, left-to-right, top-down.
set -euo pipefail
in="${1:?usage: review_frames.sh <video> [cols] [frames] [out.png]}"
cols="${2:-4}"
frames="${3:-$((cols * 2))}"
name="$(basename "${in%.*}")"
dir="${REVIEW_DIR:-${TMPDIR:-/tmp}/manim-review}"
out="${4:-$dir/${name}_sheet.png}"
mkdir -p "$(dirname "$out")"

dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")"
rows=$(( (frames + cols - 1) / cols ))
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# Seek to each timestamp exactly (the fps filter drifts by up to half a step).
times=()
for ((i = 0; i < frames; i++)); do
  t="$(awk -v i="$i" -v n="$frames" -v d="$dur" 'BEGIN { printf "%.3f", i * d / n }')"
  times+=("${t}s")
  ffmpeg -y -loglevel error -ss "$t" -i "$in" -frames:v 1 \
    -vf "scale=360:-2:flags=lanczos" "$tmp/$(printf '%03d' "$i").png"
done
ffmpeg -y -loglevel error -framerate 1 -i "$tmp/%03d.png" \
  -vf "tile=${cols}x${rows}:padding=6:color=white" -frames:v 1 -update 1 "$out"

echo "$out"
echo "tiles at: ${times[*]}"
