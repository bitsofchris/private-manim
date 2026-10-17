#!/usr/bin/env python3
"""Check every cut of a HyperFrames Short: beat N's last frame against beat N+1's first.

Usage (from the video folder, the one holding beats.json):
    uv run --no-sync python ../../tools/seam_check.py beats.json [--out media/seams] [--beat 03_x ...]

For each pair of neighbouring beats whose clip is `media/hf/<beat>.mp4` and
whose folder `<beat>/index.html` exists, it takes a `hyperframes snapshot`
of the end of beat N and of t = 0 of beat N+1, pixel-diffs them, and writes
a side-by-side PNG per cut. `--beat NAME` limits it to the cuts into and
out of that beat, so a beat agent checks its own cuts as soon as a
neighbour's folder exists, without snapshotting the whole Short. Snapshots, not mp4 frames: h264 noise around
text reads as differences up to ~60/255 where there are none (ep03).
Manim beats are skipped. Snapshots run with `--describe false`, so no frame
is ever sent to a vision API.

A cut passes when no pixel differs by more than --tol (default 8/255). The
exit code is the number of failing cuts. Pure logic (pairing, duration
parsing, the verdict) is unit-tested in tests/test_seam_check.py.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HF = ["npx", "--yes", "--prefer-offline", "hyperframes@0.8.115", "snapshot"]
DURATION = re.compile(r'data-duration="([0-9.]+)"')


def hf_pairs(beats: dict, base: Path) -> list[tuple[str, str]]:
    """Neighbouring HyperFrames beats, by folder name, from beats.json."""
    names = []
    for b in beats["beats"]:
        clip = Path(b["clip"])
        is_hf = clip.parent.as_posix().endswith("media/hf") and (base / clip.stem / "index.html").exists()
        names.append(clip.stem if is_hf else None)
    return [(a, b) for a, b in zip(names, names[1:]) if a and b]


def touching(pairs: list[tuple[str, str]], beats: list[str]) -> list[tuple[str, str]]:
    """Only the cuts into or out of the named beats (all cuts when none are named)."""
    return [p for p in pairs if not beats or p[0] in beats or p[1] in beats]


def duration(html: str) -> float:
    """The composition's length, from the root's data-duration."""
    m = DURATION.search(html)
    if not m:
        raise ValueError("no data-duration in index.html")
    return float(m.group(1))


def verdict(max_diff: int, tol: int) -> str:
    return "ok" if max_diff <= tol else "DIFF"


def snapshot(folder: Path, t: float, out: Path) -> Path:
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", HYPERFRAMES_NO_UPDATE_CHECK="1")
    subprocess.run(HF + ["--at", f"{t:.3f}", "--no-end", "--describe", "false", "-o", str(out), "."],
                   cwd=folder, env=env, check=True, capture_output=True)
    return sorted(out.glob("frame-*.png"))[0]


def main(argv: list[str] | None = None) -> int:
    from PIL import Image, ImageChops

    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("beats")
    ap.add_argument("--out", default="media/seams")
    ap.add_argument("--tol", type=int, default=8, help="largest allowed per-pixel difference (0-255)")
    ap.add_argument("--beat", action="append", default=[],
                    help="check only the cuts into and out of this beat folder (repeatable)")
    args = ap.parse_args(argv)
    path = Path(args.beats).resolve()
    base, out = path.parent, (path.parent / args.out)
    pairs = touching(hf_pairs(json.loads(path.read_text()), base), args.beat)
    fails = 0
    for a, b in pairs:
        end = duration((base / a / "index.html").read_text()) - 0.02
        pa = snapshot(base / a, end, out / f"{a}_end")
        pb = snapshot(base / b, 0.0, out / f"{b}_start")
        ia, ib = Image.open(pa).convert("RGB"), Image.open(pb).convert("RGB")
        hist = ImageChops.difference(ia, ib).convert("L").histogram()
        mx = max(i for i, n in enumerate(hist) if n)
        side = Image.new("RGB", (720, 640))
        side.paste(ia.resize((360, 640)), (0, 0)); side.paste(ib.resize((360, 640)), (360, 0))
        side.save(out / f"cut_{a}__{b}.png")
        v = verdict(mx, args.tol)
        fails += v != "ok"
        print(f"{a} -> {b}: {v}  max diff {mx}/255, {sum(hist[args.tol + 1:])} px over {args.tol}")
    if not pairs:
        print("no HyperFrames cuts found")
    return fails


if __name__ == "__main__":
    sys.exit(main())
