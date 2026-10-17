"""Re-cut a re-cleaned take with the existing timemap.json, so every beat keeps its timing.

Used 2026-10-17 when Chris chose a lighter cleaning chain after the beats were
built (the minimal chain: highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=9):

    ffmpeg -i vo_raw.m4a -af "highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=9" -ar 48000 -ac 1 vo_clean.wav
    uv run --no-sync python recut_vo.py vo_clean.wav timemap.json vo_cut.wav 48.801
    ffmpeg -i vo_cut.wav -af "volume=2.7dB,alimiter=limit=0.83:attack=1:release=50:level=disabled" vo_final.wav   # -14 LUFS, peaks -1.5

Matches tools/tighten_vo.py's placement to within 1 ms.
"""
import json, subprocess, sys
import numpy as np
src, tmap, out, total = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
SR = 48000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32)
y = np.zeros(int(round(total * SR)), np.float32)
fade = int(0.008 * SR)
for p in json.load(open(tmap)):
    a, b, n = int(p["old_start"] * SR), int(p["old_end"] * SR), int(p["new_start"] * SR)
    seg = x[a:b].copy()
    r = np.linspace(0, 1, fade, dtype=np.float32)
    seg[:fade] *= r; seg[-fade:] *= r[::-1]
    m = min(len(seg), len(y) - n)
    y[n:n + m] += seg[:m]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", out], input=y.tobytes(), check=True)
