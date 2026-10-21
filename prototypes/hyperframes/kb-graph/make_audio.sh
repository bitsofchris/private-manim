#!/bin/bash
# Mix the Short's sound: Chris's voiceover placed at its beats, the music bed
# ducked under it, then muxed onto the HyperFrames render.
#   ./make_audio.sh            -> out/vo_final.wav, out/mix.wav, out/augicraft-diamond-short-sound.mp4
# Takes are cut from the raw recording by their times in it (found with an RMS
# envelope); PLACE moves each to its video time. Edit PLACE to retime a line.
set -euo pipefail
cd "$(dirname "$0")"
SRC=/Users/chris/Creating/augicraft-diamond-run
VO_RAW="$SRC/minecraft-diamond-run.m4a"
MUSIC="$SRC/Track.mp3"
VIDEO=out/augicraft-diamond-short.mp4
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")

# Video time of a moment in the run, through the edit's clock map (footage/edit.js),
# so lines and the music dip stay on their beats when the edit changes.
vt() { node -e '
const src = require("fs").readFileSync("footage/edit.js", "utf8");
const m = JSON.parse(src.slice(src.indexOf("{"), src.lastIndexOf("}") + 1)).map;
const c = s => s.split(":").map(Number).reduce((a, x) => a * 60 + x);
const k = c(process.argv[1]); let v = m[m.length - 1][1];
for (let i = 1; i < m.length; i++) if (k <= c(m[i][0])) { const a = c(m[i - 1][0]), b = c(m[i][0]); v = m[i - 1][1] + (m[i][1] - m[i - 1][1]) * (k - a) / (b - a); break; }
console.log((v + Number(process.argv[2] || 0)).toFixed(3));' "$1" "${2:-0}"; }

# take start, take end, video start, text   (take times in the raw recording)
#   line 3: "drowned" (0.79 s into the take) lands as the drowned chip shows (09:11:06)
#   line 4: "diamonds" (2.4 s in) lands as Chris's fifth diamond arrives (09:21:34.5)
PLACE=(
  "3.00 6.99 0.25 This is an AI agent playing Minecraft. I just asked it for five diamonds."
  "8.32 14.56 4.60 It's not an AI that knows how to play Minecraft, but it's an AI that writes its own skills, taking notes as it plays to learn from its mistakes."
  "23.53 26.18 $(vt 09:11:06 -0.92) And it just drowned. So it wrote a safer way to dig."
  "36.00 38.92 $(vt 09:21:34.5 -2.23) 40 minutes and nine skills later, it gives me those five diamonds."
)

mkdir -p out
# House VO chain (tools/enhance_vo.sh): high-pass, then -14 LUFS.
ffmpeg -v error -y -i "$VO_RAW" -af "highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=9" -ar 48000 -ac 1 out/vo_clean.wav

# Each line is levelled to the same speech RMS (the take got louder line by line).
rms() { ffmpeg -v error -ss "$1" -t "$(python3 -c "print($2 - $1)")" -i out/vo_clean.wav -ac 1 -ar 16000 -f s16le - | python3 -c "
import sys, struct, math
d = sys.stdin.buffer.read(); s = struct.unpack('<%dh' % (len(d) // 2), d)
w = 160; fr = [math.sqrt(sum(x * x for x in s[i:i + w]) / w) for i in range(0, len(s) - w, w)]
top = max(fr); sp = [f for f in fr if f > top / 30]                  # frames within 30 dB of the peak: speech
print(20 * math.log10(math.sqrt(sum(f * f for f in sp) / len(sp)) / 32768))"; }
TARGET=-18
inputs=(); chains=(); labels=""; txt=""
for i in "${!PLACE[@]}"; do
  read -r a b v text <<<"${PLACE[$i]}"
  len=$(python3 -c "print(round($b - $a, 3))")
  gain=$(python3 -c "print(round($TARGET - $(rms "$a" "$b"), 2))")
  ms=$(python3 -c "print(int(round($v * 1000)))")
  inputs+=(-i out/vo_clean.wav)
  chains+=("[$i:a]atrim=$a:$b,asetpts=PTS-STARTPTS,volume=${gain}dB,afade=t=in:d=0.02,afade=t=out:st=$(python3 -c "print(round($len - 0.04, 3))"):d=0.04,adelay=$ms[v$i]")
  labels+="[v$i]"; echo "line $((i + 1)): ${gain} dB"
  txt+=$(python3 -c "
v, l = $v, $len
f = lambda s: f'{int(s // 60):02d}:{s % 60:06.3f}'
print(f'{f(v)}-{f(v + l)}')")$'\n'"$text"$'\n\n'
done
n=${#PLACE[@]}
graph=$(IFS=';'; echo "${chains[*]}");
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$graph;${labels}amix=inputs=$n:normalize=0,apad,atrim=0:$DUR[out]" -map "[out]" -ar 48000 -ac 1 out/vo_final.wav
printf '%s' "$txt" > out/vo_final.txt     # MacWhisper txt format, video times: feeds tools/word_times.py

# Music: level it well under the voice, fade in and out, dip during the drowning
# (from hitting water, 09:09:22, to the drowned shot, 09:11:04), then duck it under the voice.
DIP_A=$(vt 09:09:22 -0.2); DIP_B=$(vt 09:11:04 0.1)
ffmpeg -v error -y -i "$MUSIC" -i out/vo_final.wav -filter_complex "
  [0:a]atrim=0:$DUR,asetpts=PTS-STARTPTS,loudnorm=I=-24:TP=-3,aresample=48000,
       afade=t=in:d=0.4,afade=t=out:st=$(python3 -c "print(round($DUR - 1.6, 2))"):d=1.5,
       volume='1-0.45*clip((t-$DIP_A)/0.4,0,1)*clip(($DIP_B-t)/0.4,0,1)':eval=frame[m];
  [1:a]asplit=2[vo][key];
  [m][key]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=450:makeup=1[duck];
  [vo]pan=stereo|c0=c0|c1=c0[vos];
  [duck][vos]amix=inputs=2:normalize=0,apad,atrim=0:$DUR[out]" \
  -map "[out]" -ar 48000 -ac 2 out/mix_raw.wav
# Two-pass loudnorm to -14 LUFS (one pass lands about 1 dB low on a clip this short).
stats=$(ffmpeg -hide_banner -i out/mix_raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { python3 -c "import json,sys; print(json.loads(sys.argv[1])['$1'])" "$stats"; }
ffmpeg -v error -y -i out/mix_raw.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true" -ar 48000 -ac 2 out/mix.wav
ffmpeg -v error -y -i "$VIDEO" -i out/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out/augicraft-diamond-short-sound.mp4
echo "wrote out/augicraft-diamond-short-sound.mp4"
ffmpeg -hide_banner -i out/mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|True peak|Peak):' | head -3
