#!/usr/bin/env bash
# Clean up a raw voiceover recording: rumble cut, noise reduction, de-ess,
# compression, then loudness-normalize to -14 LUFS (YouTube's target).
#
# Usage:
#   tools/enhance_vo.sh vo.m4a [vo_clean.wav]
#
# Filters, in order:
#   highpass f=80        drop room rumble / mic handling below the voice
#   afftdn nf=-25        FFT noise reduction (room hiss, fan)
#   deesser              tame harsh "s" sounds
#   acompressor          even out loud vs quiet words (ratio 3:1)
#   loudnorm I=-14       EBU R128 loudness to -14 LUFS, true peak -1.5 dB
set -euo pipefail
in="$1"
out="${2:-${in%.*}_clean.wav}"
ffmpeg -y -loglevel error -i "$in" -af \
  "highpass=f=80,afftdn=nf=-25,deesser,acompressor=threshold=-18dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9" \
  -ar 48000 -ac 1 "$out"
echo "wrote $out"
ffmpeg -i "$out" -af "volumedetect" -f null - 2>&1 | grep -E "mean_volume|max_volume"
