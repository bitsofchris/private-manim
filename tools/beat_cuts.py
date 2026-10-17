#!/usr/bin/env python3
"""Place the beat cuts in the pauses and write beats.json plus the final beat table.

Usage (from the video folder, after words.json is fixed):
    uv run --no-sync python ../../tools/beat_cuts.py words.json vo_final.wav \
        01_hook 02_context=Context 03_tools=Tools 04_memory=Memory@14.6 ... \
        -o beats.json
    # Manim beats: --clip "media/videos/{name}/1920p30/{name}.mp4" (any {name} pattern)

Each beat after the first is NAME=WORD: the beat starts in the pause before
WORD (matched without surrounding whitespace or trailing punctuation, case-
insensitive; add @SECONDS to pick the occurrence nearest that master time).
The first beat starts at 0 and the last ends at the VO's length, so the
lengths sum to it (assemble.py's contract).

The cut sits at the middle of the pause before WORD, but at least MIN_LEAD
(80 ms) before the word starts, so a beat never opens mid-onset. Prints the
storyboard's "Final beats" table (start, length, folder, VO), ready to paste.
Writes beats.json as {"beats": [{"clip", "end"}]}, end = the beat's length.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import wave

MIN_LEAD = 0.08  # seconds between a cut and the next word's start


def norm(word: str) -> str:
    return re.sub(r"[^\w'.-]+$", "", word.strip()).rstrip(".").lower()


def find_word(words: list[dict], spec: str, after: float) -> int:
    """Index of the word a beat starts on: the first match after `after`, or the one nearest @T."""
    target, sep, at = spec.rpartition("@")
    if not sep:
        target, at = spec, None
    else:
        at = float(at)
    hits = [i for i, w in enumerate(words) if norm(w["word"]) == norm(target) and w["t"] > after]
    if not hits:
        raise SystemExit(f"beat_cuts: no word {target!r} after {after:.2f} s")
    return min(hits, key=lambda i: abs(words[i]["t"] - at)) if at is not None else hits[0]


def cut_before(words: list[dict], i: int) -> float:
    """Middle of the pause before word i, capped at MIN_LEAD before it."""
    start = words[i]["t"]
    prev_end = words[i - 1].get("end", words[i - 1]["t"]) if i > 0 else 0.0
    return round(min((prev_end + start) / 2, start - MIN_LEAD), 3)


def plan(words: list[dict], beats: list[str], total: float) -> list[dict]:
    """[{name, start, length, vo}] from 'NAME' / 'NAME=WORD[@T]' specs."""
    starts, names, after = [0.0], [beats[0].split("=")[0]], -1.0
    for b in beats[1:]:
        name, _, spec = b.partition("=")
        if not spec:
            raise SystemExit(f"beat_cuts: beat {name!r} needs =WORD (only the first beat starts at 0)")
        i = find_word(words, spec, after)
        starts.append(cut_before(words, i)); names.append(name); after = words[i]["t"]
    if any(b <= a for a, b in zip(starts, starts[1:])) or starts[-1] >= total:
        raise SystemExit(f"beat_cuts: cuts out of order: {starts} (VO {total:.3f} s)")
    ends = starts[1:] + [total]
    return [{"name": n, "start": s, "length": round(e - s, 3),
             "vo": " ".join(w["word"].strip() for w in words if s <= w["t"] < e)}
            for n, s, e in zip(names, starts, ends)]


def wav_seconds(path: str) -> float:
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def table(rows: list[dict]) -> str:
    out = ["| beat | start | length | folder | VO |", "|---|---|---|---|---|"]
    out += [f"| {k} | {r['start']:.3f} | {r['length']:.3f} | `{r['name']}` | {r['vo']} |" for k, r in enumerate(rows, 1)]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words")
    ap.add_argument("vo", help="vo_final.wav (its length is the last beat's end)")
    ap.add_argument("beats", nargs="+", help="NAME for the first beat, then NAME=WORD[@SECONDS]")
    ap.add_argument("-o", "--out", default="beats.json")
    ap.add_argument("--clip", default="media/hf/{name}.mp4", help="clip path pattern")
    args = ap.parse_args(argv)
    words = json.load(open(args.words))
    total = round(wav_seconds(args.vo), 3)
    rows = plan(words, args.beats, total)
    with open(args.out, "w") as f:
        json.dump({"beats": [{"clip": args.clip.format(name=r["name"]), "end": r["length"]} for r in rows]}, f, indent=1)
    print(f"VO {total:.3f} s, {len(rows)} beats -> {args.out}\n")
    print(table(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
