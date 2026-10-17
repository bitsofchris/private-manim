"""Cut whole ranges out of an already-tightened VO, leaving everything else sample-identical.

Used 2026-10-17 for Chris's second cut (lines 2 and 4 out, line 5 trimmed) after the
beats were built: cutting vo_final.wav directly keeps beats 4-7 exactly as they were,
shifted by a constant. Each cut is (start, end, silence): drop [start, end) and put
`silence` seconds of digital silence in its place; 8 ms fades at each join.

    uv run --no-sync python cut_vo.py IN.wav OUT.wav 5.12:7.06:0.12 9.60:13.63:0.15 14.50:15.645:0
"""
import subprocess
import sys

import numpy as np

SR = 48000
FADE = int(0.008 * SR)


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def main():
    src, out, cuts = sys.argv[1], sys.argv[2], [tuple(map(float, c.split(":"))) for c in sys.argv[3:]]
    x = load(src)
    parts, pos, removed = [], 0, 0.0
    r = np.linspace(0, 1, FADE, dtype=np.float32)
    for a, b, sil in sorted(cuts):
        ia, ib = int(round(a * SR)), int(round(b * SR))
        keep = x[pos:ia].copy(); keep[-FADE:] *= r[::-1]
        parts += [keep, np.zeros(int(round(sil * SR)), np.float32)]
        x[ib:ib + FADE] *= r
        pos = ib
        removed += (b - a) - sil
        print(f"cut {a:.3f}-{b:.3f} (+{sil:.2f} s silence): after {b:.3f} everything moves {-removed:.3f} s")
    parts.append(x[pos:])
    y = np.concatenate(parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", out],
                   input=y.tobytes(), check=True)
    print(f"{len(x) / SR:.3f} s -> {len(y) / SR:.3f} s")


if __name__ == "__main__":
    main()
