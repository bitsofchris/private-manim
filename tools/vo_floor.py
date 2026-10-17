#!/usr/bin/env python3
"""Measure a voiceover's noise floor: the level of the room between words.

Usage:
    tools/vo_floor.py vo_raw.m4a          # prints e.g. -54.2

How it works: the take is decoded to mono 16 kHz, cut into 50 ms windows,
and each window's RMS level is taken in dB. Windows of digital silence
(below -90 dB, e.g. a hard-gated pause) are ignored. The floor is the 10th
percentile of the rest: low enough to be the room, not the voice, and robust
to a few clicks.

Used by tools/enhance_vo.sh --denoise (the denoiser's floor) and
tools/tighten_vo.py --noise auto (the pause threshold). Measured on 013 ep01
(2026-10-17): a QuickTime take at -54 dB, where the old fixed `afftdn nf=-25`
treated the quiet parts of the voice as noise.

Pure logic (noise_floor_db) is unit-tested in tests/test_vo_floor.py.
"""
from __future__ import annotations

import subprocess
import sys

import numpy as np

SR = 16000
WINDOW = 0.05       # seconds per RMS window
PERCENTILE = 10
DIGITAL_SILENCE = -90.0


def noise_floor_db(x: np.ndarray, sr: int = SR) -> float:
    """10th-percentile RMS level (dB) of 50 ms windows, ignoring digital silence."""
    n = int(WINDOW * sr)
    k = len(x) // n
    if k == 0:
        raise ValueError("clip shorter than one window")
    w = x[: k * n].reshape(k, n).astype(np.float64)
    db = 20 * np.log10(np.sqrt((w ** 2).mean(axis=1)) + 1e-12)
    db = db[db > DIGITAL_SILENCE]
    if db.size == 0:
        raise ValueError("no audio above digital silence")
    return float(np.percentile(db, PERCENTILE))


def load(path: str) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def measure(path: str) -> float:
    return noise_floor_db(load(path))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: vo_floor.py AUDIO")
    print(f"{measure(sys.argv[1]):.1f}")
