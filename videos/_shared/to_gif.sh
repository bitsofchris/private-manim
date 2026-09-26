#!/usr/bin/env bash
# Convert a rendered Manim mp4 into a small, email-safe looping GIF.
#
# Usage:
#   videos/_shared/to_gif.sh <input.mp4> <output.gif> [width] [fps]
# Defaults: width=640, fps=15. Uses two-pass palettegen for quality at small size.
set -euo pipefail
in="$1"; out="$2"; w="${3:-640}"; fps="${4:-15}"
ffmpeg -y -loglevel error -i "$in" \
  -vf "fps=${fps},scale=${w}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  -loop 0 "$out"
ls -la "$out"
