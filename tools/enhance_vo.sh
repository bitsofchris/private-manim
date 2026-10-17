#!/usr/bin/env bash
# Clean up a raw voiceover recording, then loudness-normalize to -14 LUFS
# (YouTube's target).
#
# Usage:
#   tools/enhance_vo.sh vo.m4a [vo_clean.wav]            # minimal chain (default)
#   tools/enhance_vo.sh --denoise vo.m4a [vo_clean.wav]  # + denoise and de-ess
#
# Default chain (Chris's pick by ear on 013 ep01, 2026-10-17):
#   highpass f=80        drop room rumble / mic handling below the voice
#   loudnorm I=-14       EBU R128 loudness to -14 LUFS, true peak -1.5 dB
#
# --denoise adds, before loudnorm, only when the room is audible:
#   afftdn nf=<floor>    FFT noise reduction, its floor set from the take's
#                        measured noise floor (tools/vo_floor.py). The old fixed
#                        nf=-25 sat ~30 dB above a quiet room and smeared the
#                        voice (013 ep01, floor -54 dB in the pauses).
#   deesser              tame harsh "s" sounds
# No compressor: the 3:1 one dulled the voice and loudnorm already evens it.
#
# Cutting pauses changes the integrated loudness, so level the cut take
# again: tools/tighten_vo.py --level -14 (runbook step 5).
set -euo pipefail
denoise=0
if [[ "${1:-}" == "--denoise" ]]; then denoise=1; shift; fi
in="$1"
out="${2:-${in%.*}_clean.wav}"
chain="highpass=f=80"
if [[ $denoise == 1 ]]; then
  here="$(cd "$(dirname "$0")" && pwd)"
  floor="$(uv run --no-sync python "$here/vo_floor.py" "$in")"
  nf="$(python3 -c "print(max(-80, min(-20, round($floor))))")"
  echo "noise floor $floor dB -> afftdn nf=$nf"
  chain="$chain,afftdn=nf=$nf,deesser"
fi
ffmpeg -y -loglevel error -i "$in" -af "$chain,loudnorm=I=-14:TP=-1.5:LRA=9" -ar 48000 -ac 1 "$out"
echo "wrote $out ($chain)"
ffmpeg -i "$out" -af "volumedetect" -f null - 2>&1 | grep -E "mean_volume|max_volume"
