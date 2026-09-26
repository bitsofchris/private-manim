#!/usr/bin/env python3
"""Tighten a voiceover: drop flubbed ranges, shorten pauses, keep a time map.

Usage:
    tools/tighten_vo.py vo_clean.wav --out vo_tight.wav \
        [--remove 46.0-51.0 --remove 93.6-94.5] [--max-gap 0.4] \
        [--noise -35dB] [--min-silence 0.45] [--map timemap.json]

How it works:
    1. ffmpeg silencedetect finds pauses; speech = the gaps between them.
    2. Speech intervals inside a --remove range are dropped (partial overlaps
       are clipped).
    3. Each kept interval gets a small pad so consonants are not clipped, and
       the pause between kept intervals is shortened to --max-gap.
    4. ffmpeg trims + concatenates the kept pieces with tiny fades to avoid
       clicks. A JSON time map (old -> new seconds) is written so transcript
       timestamps can be re-timed with `remap(t)`.

Pure logic (plan_cuts, remap) is unit-tested in tests/test_tighten_vo.py.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict

PAD = 0.08        # seconds kept around each speech interval
FADE = 0.008      # seconds of fade at each cut to avoid clicks
LEAD_IN = 0.30    # silence before the first word
TAIL = 0.50       # silence after the last word


@dataclass
class Piece:
    old_start: float
    old_end: float
    new_start: float

    @property
    def new_end(self) -> float:
        return self.new_start + (self.old_end - self.old_start)


def detect_silences(path: str, noise: str, min_silence: float) -> list[tuple[float, float]]:
    cmd = ["ffmpeg", "-i", path, "-af", f"silencedetect=noise={noise}:d={min_silence}", "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True).stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([0-9.]+)", out)]
    ends = [float(m) for m in re.findall(r"silence_end: ([0-9.]+)", out)]
    return list(zip(starts, ends))


def duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(out.strip())


def speech_intervals(silences: list[tuple[float, float]], total: float) -> list[tuple[float, float]]:
    """Complement of the silence list within [0, total]."""
    out, cursor = [], 0.0
    for s, e in sorted(silences):
        if s > cursor:
            out.append((cursor, s))
        cursor = max(cursor, e)
    if cursor < total:
        out.append((cursor, total))
    return [(a, b) for a, b in out if b - a > 0.02]


def apply_removals(speech: list[tuple[float, float]], removes: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Drop the parts of speech intervals that fall inside any remove range."""
    out = []
    for a, b in speech:
        segs = [(a, b)]
        for r0, r1 in removes:
            nxt = []
            for s, e in segs:
                if e <= r0 or s >= r1:
                    nxt.append((s, e))
                else:
                    if s < r0:
                        nxt.append((s, r0))
                    if e > r1:
                        nxt.append((r1, e))
            segs = nxt
        out.extend((s, e) for s, e in segs if e - s > 0.05)
    return out


def plan_cuts(
    speech: list[tuple[float, float]],
    max_gap: float,
    total: float,
    pauses: dict[float, float] | None = None,
) -> list[Piece]:
    """Pad each interval, cap the pause between them, and lay them out on a new timeline.

    `pauses` maps an old-timeline instant to a pause length: the gap that
    contains that instant gets exactly that pause instead of the cap. Use it
    for beat boundaries, where the read should breathe.
    """
    pieces: list[Piece] = []
    cursor = LEAD_IN
    prev_end = None
    for a, b in speech:
        a_p = max(0.0, a - PAD)
        b_p = min(total, b + PAD)
        if prev_end is not None:
            a_p = max(a_p, prev_end)  # never overlap the previous piece
            gap = min(a_p - prev_end, max_gap)
            for t, d in (pauses or {}).items():
                if prev_end <= t <= a_p:
                    gap = d
            cursor += gap
        pieces.append(Piece(a_p, b_p, round(cursor, 3)))
        cursor += b_p - a_p
        prev_end = b_p
    return pieces


def remap(t: float, pieces: list[Piece]) -> float | None:
    """Old timestamp -> new timestamp. None if t was cut. Gaps snap to the next piece."""
    for p in pieces:
        if p.old_start <= t <= p.old_end:
            return round(p.new_start + (t - p.old_start), 3)
    nxt = [p for p in pieces if p.old_start > t]
    prv = [p for p in pieces if p.old_end < t]
    if nxt and prv:
        return round(nxt[0].new_start, 3)  # inside a shortened pause
    return None


def build_ffmpeg(src: str, pieces: list[Piece], out: str) -> list[str]:
    parts, labels = [], []
    for i, p in enumerate(pieces):
        d = p.old_end - p.old_start
        parts.append(
            f"[0:a]atrim=start={p.old_start:.3f}:end={p.old_end:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d={FADE},afade=t=out:st={max(0.0, d - FADE):.3f}:d={FADE}[s{i}]"
        )
        labels.append(f"[s{i}]")
    # silence between pieces is generated by padding each piece's end
    chain = []
    for i, p in enumerate(pieces):
        nxt_gap = (pieces[i + 1].new_start - p.new_end) if i + 1 < len(pieces) else TAIL
        chain.append(f"[s{i}]apad=pad_dur={max(0.0, nxt_gap):.3f}[p{i}]")
    concat = "".join(f"[p{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1[out]"
    lead = f"aevalsrc=0:d={LEAD_IN}:s=48000:c=mono[lead]"
    graph = ";".join(parts + chain + [lead, concat, "[lead][out]concat=n=2:v=0:a=1[final]"])
    return ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", graph,
            "-map", "[final]", "-ar", "48000", "-ac", "1", out]


def parse_range(s: str) -> tuple[float, float]:
    a, b = s.split("-")
    return float(a), float(b)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("--out", required=True)
    ap.add_argument("--remove", action="append", default=[], help="old-time range a-b to drop (repeatable)")
    ap.add_argument("--max-gap", type=float, default=0.4)
    ap.add_argument("--pause", action="append", default=[],
                    help="OLD_TIME=SECONDS: the gap containing OLD_TIME gets this pause (repeatable)")
    ap.add_argument("--noise", default="-35dB")
    ap.add_argument("--min-silence", type=float, default=0.45)
    ap.add_argument("--map", default=None, help="write old->new time map JSON here")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    total = duration(args.src)
    silences = detect_silences(args.src, args.noise, args.min_silence)
    speech = apply_removals(speech_intervals(silences, total), [parse_range(r) for r in args.remove])
    pauses = {float(k): float(v) for k, v in (x.split("=") for x in args.pause)}
    pieces = plan_cuts(speech, args.max_gap, total, pauses)
    cmd = build_ffmpeg(args.src, pieces, args.out)
    new_total = pieces[-1].new_end + TAIL if pieces else 0.0
    print(f"{len(pieces)} pieces, {total:.1f}s -> {new_total:.1f}s", file=sys.stderr)
    if args.map:
        with open(args.map, "w") as f:
            json.dump([asdict(p) for p in pieces], f, indent=1)
    if args.dry_run:
        print(" ".join(cmd))
        return 0
    subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
