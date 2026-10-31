#!/usr/bin/env python3
"""Cut phrases out of a finished vo_final.wav after the beats are built.

Usage:
    tools/cut_vo.py vo_final.wav --out vo_final.wav --words words.json \
        --cut 5.12-7.06:0.12 --cut 9.60-13.63:0.15 --cut 14.50-15.645

When Chris watches the assembled Short and asks for a line to go (013 ep01:
"we spend too much time before the confusion matrix"), re-running
tighten_vo.py re-detects every pause and moves every beat. This cuts the
finished VO itself instead: each `--cut A-B[:S]` drops [A, B) in vo_final
seconds and puts S seconds of silence in its place (default 0), with 8 ms
fades at each join. Everything after the last cut is sample-identical,
shifted by a constant, so the beats after it only need a new start in
beats.json. To drop the opening, cut from 0 (`--cut 0-7.85`); to drop the
closing, cut to `end` (`--cut 39.57-end:0.6` leaves 0.6 s of silence as the
last beat's tail: 016 ep02 lost its closing line).

--words rewrites words.json in place: words inside a cut are dropped,
later words shift. A word whose recorded start falls a few ms inside a cut
is dropped too, so read the new words.json once (013 ep01 lost "catches",
whose WhisperKit start was 5 ms early). Then rebuild captions and
beats.json, and re-transcribe the result to check the joins (runbook step 5).

Put cut edges at the envelope dips around the words, not at word times:
"here's" lost its "h" when a cut ended 20 ms late.

Pure logic (shift, shift_words) is unit-tested in tests/test_cut_vo.py.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys

import numpy as np

SR = 48000
FADE = 0.008


def parse_cut(s: str) -> tuple[float, float, float]:
    """`A-B[:S]`; B may be `end` (math.inf until main clamps it to the file's length)."""
    rng, _, sil = s.partition(":")
    a, b = rng.split("-")
    return float(a), math.inf if b == "end" else float(b), float(sil or 0)


def shift(t: float, cuts: list[tuple[float, float, float]]) -> float | None:
    """New time of old time t, or None if t falls inside a cut."""
    d = 0.0
    for a, b, sil in sorted(cuts):
        if a <= t < b:
            return None
        if t >= b:
            d += (b - a) - sil
    return round(t - d, 3)


def shift_words(words: list[dict], cuts: list[tuple[float, float, float]]) -> list[dict]:
    out = []
    for w in words:
        t = shift(w["t"], cuts)
        if t is None:
            continue
        end = shift(w.get("end", w["t"]), cuts)
        out.append(dict(w, t=t, end=end if end is not None else t))
    return out


def cut_audio(x: np.ndarray, cuts: list[tuple[float, float, float]]) -> np.ndarray:
    x = x.copy()
    n = int(FADE * SR)
    ramp = np.linspace(0, 1, n, dtype=np.float32)
    parts, pos = [], 0
    for a, b, sil in sorted(cuts):
        ia, ib = int(round(a * SR)), int(round(b * SR))
        keep = x[pos:ia].copy()
        if len(keep) >= n:
            keep[-n:] *= ramp[::-1]
        parts += [keep, np.zeros(int(round(sil * SR)), np.float32)]
        x[ib:ib + n] *= ramp[: len(x[ib:ib + n])]
        pos = ib
    parts.append(x[pos:])
    return np.concatenate(parts)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cut", action="append", required=True, help="A-B[:SILENCE], vo_final seconds; B may be 'end' (repeatable)")
    ap.add_argument("--words", help="words.json to rewrite in place")
    args = ap.parse_args(argv)
    cuts = [parse_cut(c) for c in args.cut]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", args.src, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    cuts = [(a, min(b, len(x) / SR), sil) for a, b, sil in cuts]
    y = cut_audio(x, cuts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", args.out],
                   input=y.tobytes(), check=True)
    for a, b, sil in sorted(cuts):
        print(f"cut {a:.3f}-{b:.3f} (+{sil:.2f} s): after {b:.3f} -> {shift(b, cuts):.3f}", file=sys.stderr)
    print(f"{len(x) / SR:.3f} s -> {len(y) / SR:.3f} s", file=sys.stderr)
    if args.words:
        with open(args.words) as f:
            words = json.load(f)
        new = shift_words(words, cuts)
        with open(args.words, "w") as f:
            json.dump(new, f, indent=1)
        print(f"words: {len(words)} -> {len(new)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
