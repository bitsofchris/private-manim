#!/usr/bin/env python3
"""Tighten a voiceover: drop flubbed ranges, shorten pauses, keep a time map.

Usage:
    tools/tighten_vo.py vo_clean.wav --out vo_final.wav \
        [--remove 46.0-51.0 --remove 93.6-94.5] [--max-gap 0.4] \
        [--noise auto] [--min-silence 0.45] [--map timemap.json] [--level -14]

    # re-clean a take after the beats are built, keeping every cut and pause:
    tools/tighten_vo.py vo_clean.wav --out vo_final.wav --map-in timemap.json --level -14

How it works:
    1. ffmpeg silencedetect finds pauses; speech = the gaps between them.
    2. Speech intervals inside a --remove range are dropped (partial overlaps
       are clipped).
    3. Each kept interval gets a small pad so consonants are not clipped (but
       never back into a --remove range: a mid-phrase cut stays cut), and
       the pause between kept intervals is shortened to --max-gap.
    4. ffmpeg trims + concatenates the kept pieces with tiny fades to avoid
       clicks. A JSON time map (old -> new seconds) is written so transcript
       timestamps can be re-timed with `remap(t)`.
    5. --level LUFS: cutting pauses changes the integrated loudness (013 ep01:
       -14 -> -15.9 LUFS), so the result is measured and brought to LUFS with
       a gain and a peak limiter at -1.5 dBTP.

--noise auto sets the pause threshold NOISE_MARGIN dB above the take's
measured noise floor (tools/vo_floor.py). A fixed -35dB clipped word tails
on 013 ep01 ("attacks" read as "attacked").

--map-in skips steps 1-3 and re-applies an existing time map to a new
source, so a re-cleaned take keeps every beat's timing to the sample.

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
NOISE_MARGIN = 12.0   # --noise auto: dB above the measured noise floor
PEAK_LIMIT = 0.84     # --level: limiter ceiling, linear (-1.5 dBFS)


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


def pad_limits(a: float, b: float, removes: list[tuple[float, float]]) -> tuple[float, float]:
    """How far interval (a, b) may be padded: never back into a removed range."""
    lo = max([r1 for r0, r1 in removes if r1 <= a + 1e-9] + [a - PAD])
    hi = min([r0 for r0, r1 in removes if r0 >= b - 1e-9] + [b + PAD])
    return min(lo, a), max(hi, b)


def plan_cuts(
    speech: list[tuple[float, float]],
    max_gap: float,
    total: float,
    pauses: dict[float, float] | None = None,
    removes: list[tuple[float, float]] | None = None,
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
        lo, hi = pad_limits(a, b, removes or [])
        a_p = max(0.0, lo)
        b_p = min(total, hi)
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


def level_gain(measured_lufs: float, target_lufs: float) -> float:
    """dB of gain that brings measured to target (the limiter then holds the peaks)."""
    return round(target_lufs - measured_lufs, 2)


def loudness(path: str) -> float:
    out = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", out)[-1])


def level(path: str, target: float, tol: float = 0.3, passes: int = 3) -> None:
    """Bring `path` to `target` LUFS in place: gain, then a peak limiter at -1.5 dBFS.

    The limiter takes back some of the gain on a peaky take (013 ep01: +2.0 dB
    gave -16.0 -> -14.7), so it repeats until within `tol` LU.
    """
    start = now = loudness(path)
    tmp = path + ".level.wav"
    for _ in range(passes):
        gain = level_gain(now, target)
        if abs(gain) <= tol:
            break
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-af",
                        f"volume={gain}dB,alimiter=limit={PEAK_LIMIT}:attack=1:release=50:level=disabled",
                        "-ar", "48000", "-ac", "1", tmp], check=True)
        subprocess.run(["mv", tmp, path], check=True)
        now = loudness(path)
    print(f"level: {start:.1f} -> {now:.1f} LUFS (limited at -1.5 dBFS)", file=sys.stderr)


def auto_noise(path: str) -> str:
    """--noise auto: NOISE_MARGIN dB above the take's measured floor."""
    from vo_floor import measure  # numpy; only needed here
    return f"{measure(path) + NOISE_MARGIN:.1f}dB"


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
    ap.add_argument("--noise", default="-35dB", help='silencedetect threshold, e.g. -45dB, or "auto"')
    ap.add_argument("--min-silence", type=float, default=0.45)
    ap.add_argument("--map", default=None, help="write old->new time map JSON here")
    ap.add_argument("--map-in", default=None, help="re-apply this time map instead of planning cuts")
    ap.add_argument("--level", type=float, default=None, help="level the result to this LUFS (e.g. -14)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    total = duration(args.src)
    if args.map_in:
        with open(args.map_in) as f:
            pieces = [Piece(**p) for p in json.load(f)]
    else:
        noise = auto_noise(args.src) if args.noise == "auto" else args.noise
        if args.noise == "auto":
            print(f"noise auto -> {noise}", file=sys.stderr)
        removes = [parse_range(r) for r in args.remove]
        silences = detect_silences(args.src, noise, args.min_silence)
        speech = apply_removals(speech_intervals(silences, total), removes)
        pauses = {float(k): float(v) for k, v in (x.split("=") for x in args.pause)}
        pieces = plan_cuts(speech, args.max_gap, total, pauses, removes)
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
    if args.level is not None:
        level(args.out, args.level)
    return 0


if __name__ == "__main__":
    sys.exit(main())
