#!/usr/bin/env python3
"""Estimate when each word starts, from the phrase-level transcript and the audio.

Usage (from the video folder):
    uv run --no-sync python ../../tools/word_times.py transcript_final.txt vo_final.wav -o words.json
    # prints "  1.302  records" lines too; words.json is [{"t": 1.302, "word": "records"}, ...]

Why: MacWhisper's CLI (v15, Pro included) gives timestamps per phrase only,
and a beat lands each change on the word that names it. Beat agents used to
find each word by transcribing half-second sub-clips; this gives every word
once, in step 4, so the storyboard can list them.

How (per phrase, stdlib + numpy, no model):
  1. A 10 ms RMS envelope of the phrase's span; speech runs from the first to
     the last frame above the floor (peak − 30 dB).
  2. Each word gets a share of that span by its estimated syllables (vowel
     groups) + a constant, so "collapsing" gets more time than "a".
  3. The boundaries between words are then chosen together among the dips
     of the smoothed envelope (words are separated by small dips): distinct,
     in order, each near its guess, quiet dips preferred (`place`, a small
     dynamic program).
Accuracy on ep03 against 15 cues the beat agents measured by hand: see
tests/test_word_times.py for the logic and the runbook (step 4) for the
expected error. Treat the times as starting points; check a cue that matters
on the envelope.

Pure logic (syllable weights, the split, the dips, the placement) is unit-tested in
tests/test_word_times.py.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from captions_from_transcript import parse_transcript  # noqa: E402

HOP = 0.01      # envelope frame, s
SNAP = 0.25     # how far a boundary may move from its first guess to find a dip, s
MIN_WORD = 0.06 # the shortest word, s
PER_DB = 0.02   # seconds of distance worth one dB of quiet when choosing a dip
FLOOR_DB = 30   # speech is within this many dB of the phrase's peak


def syllables(word: str) -> int:
    """Vowel groups in the word, at least one ("e1" counts its letter and digit)."""
    w = re.sub(r"[^a-z0-9]", "", word.lower())
    groups = len(re.findall(r"[aeiouy]+", w)) + len(re.findall(r"\d", w))
    if w.endswith("e") and groups > 1 and not w.endswith(("le", "ee")):
        groups -= 1
    return max(1, groups)


def split_span(words: list[str], t0: float, t1: float) -> list[float]:
    """First guess at each word's start: the span shared by syllables + a constant."""
    weights = [syllables(w) + 0.5 for w in words]
    total, out, t = sum(weights), [], t0
    for wgt in weights:
        out.append(t)
        t += (t1 - t0) * wgt / total
    return out


def dips(env: list[float]) -> list[int]:
    """Frames that are local minima of the envelope (candidate gaps between words)."""
    return [i for i in range(1, len(env) - 1) if env[i] <= env[i - 1] and env[i] <= env[i + 1]]


def place(starts: list[float], env: list[float], t0: float, hop: float = HOP,
          reach: float = SNAP, min_word: float = MIN_WORD, per_db: float = PER_DB) -> list[float]:
    """Choose every start but the first among the envelope's dips, all at once.

    Each boundary j takes a distinct dip, in order, at least min_word after
    the previous one, within ±reach of its first guess. The cost of a choice
    is its loudness (dB above the quietest dip) plus the distance from the
    guess, at per_db seconds per dB, so a dip 10 dB quieter is worth moving
    10 * per_db further. Dynamic programming over boundaries x dips. A
    boundary with no dip in reach keeps its guess.
    """
    if len(starts) < 2:
        return list(starts)
    cand = dips(env)
    floor = min((env[i] for i in cand), default=0.0)
    tc = [t0 + i * hop for i in cand]
    INF = float("inf")
    n = len(starts) - 1                       # boundaries to place
    # options per boundary: indices into cand, or None (keep the guess)
    opts = []
    for j in range(n):
        g = starts[j + 1]
        near = [k for k, t in enumerate(tc) if abs(t - g) <= reach]
        opts.append(near + [None])
    def time(j, k):
        return starts[j + 1] if k is None else tc[k]
    def cost(j, k):
        if k is None:
            return 10.0                        # as bad as a dip 10 dB above the floor, at the guess
        return (env[cand[k]] - floor) + abs(tc[k] - starts[j + 1]) / per_db
    # best[j][k] = (total cost, previous option) for boundary j taking option k
    best = [dict() for _ in range(n)]
    for k in opts[0]:
        if time(0, k) - starts[0] >= min_word:
            best[0][k] = (cost(0, k), None)
    for j in range(1, n):
        for k in opts[j]:
            tk = time(j, k)
            prev = [(c + cost(j, k), pk) for pk, (c, _) in best[j - 1].items() if tk - time(j - 1, pk) >= min_word]
            if prev:
                best[j][k] = min(prev, key=lambda x: x[0])
    if not best[-1]:                            # nothing consistent: keep the guesses
        return list(starts)
    k = min(best[-1], key=lambda kk: best[-1][kk][0])
    chosen = []
    for j in range(n - 1, -1, -1):
        chosen.append(time(j, k))
        k = best[j][k][1]
    return [starts[0]] + chosen[::-1]


def read_mono(path: Path):
    import numpy as np
    with wave.open(str(path)) as w:
        n, ch, sw, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        raw = w.readframes(n)
    dt = {2: np.int16, 4: np.int32}[sw]
    x = np.frombuffer(raw, dtype=dt).astype(np.float64).reshape(-1, ch).mean(axis=1)
    return x / float(np.iinfo(dt).max), sr


def envelope(x, sr: int, t0: float, t1: float):
    """10 ms RMS in dB over [t0, t1), smoothed over 3 frames."""
    import numpy as np
    hop = int(sr * HOP)
    seg = x[int(t0 * sr):int(t1 * sr)]
    n = len(seg) // hop
    rms = np.sqrt((seg[: n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    return np.convolve(db, np.ones(3) / 3, mode="same")


def word_times(segments, x, sr) -> list[dict]:
    out = []
    for s, e, text in segments:
        words = text.split()
        if not words:
            continue
        env = envelope(x, sr, s, e)
        if len(env) == 0:
            continue
        loud = [i for i, v in enumerate(env) if v > env.max() - FLOOR_DB]
        a, b = s + loud[0] * HOP, s + (loud[-1] + 1) * HOP
        starts = place(split_span(words, a, b), list(env), s)
        out.extend({"t": round(t, 3), "word": w} for t, w in zip(starts, words))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("transcript")
    ap.add_argument("wav")
    ap.add_argument("-o", "--out", default="words.json")
    args = ap.parse_args(argv)
    segs = parse_transcript(Path(args.transcript).read_text())
    x, sr = read_mono(Path(args.wav))
    words = word_times(segs, x, sr)
    Path(args.out).write_text(json.dumps(words, indent=1) + "\n")
    for w in words:
        print(f"{w['t']:7.3f}  {w['word']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
