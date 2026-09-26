#!/usr/bin/env python3
"""Turn a MacWhisper timestamped transcript into captions.json for assemble.py.

Usage:
    tools/captions_from_transcript.py transcript_final.txt captions.json [--max-words 3]

Input format (MacWhisper `--format txt --timestamps --end-timestamps --milliseconds`):

    00:01.730-00:03.490
    A neural network is just a function

    ...

Whisper only gives segment-level times. Each segment's words are chunked into
groups of at most --max-words, and the segment's time span is divided among
the chunks in proportion to their character length (a decent proxy for
spoken duration). A small gap is left between chunks so they visibly change.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

GAP = 0.06  # seconds between consecutive captions


def parse_transcript(text: str) -> list[tuple[float, float, str]]:
    """[(start, end, text), ...] from the MacWhisper txt format."""
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        m = re.match(r"(\d+):(\d+\.\d+)-(\d+):(\d+\.\d+)", lines[0].strip())
        if not m:
            continue
        start = int(m[1]) * 60 + float(m[2])
        end = int(m[3]) * 60 + float(m[4])
        out.append((start, end, " ".join(lines[1:]).strip()))
    return out


def chunk_words(words: list[str], max_words: int) -> list[list[str]]:
    """Split into groups of <= max_words, balancing so the last group isn't a lone word."""
    n = len(words)
    if n == 0:
        return []
    groups = -(-n // max_words)  # ceil
    base, extra = divmod(n, groups)
    out, i = [], 0
    for g in range(groups):
        size = base + (1 if g < extra else 0)
        out.append(words[i:i + size])
        i += size
    return out


def captions_for_segment(start: float, end: float, text: str, max_words: int) -> list[dict]:
    words = text.split()
    chunks = chunk_words(words, max_words)
    if not chunks:
        return []
    weights = [sum(len(w) for w in c) + len(c) for c in chunks]  # chars + spaces
    total = sum(weights)
    span = end - start - GAP * (len(chunks) - 1)
    out, t = [], start
    for c, w in zip(chunks, weights):
        d = span * w / total
        out.append({"start": round(t, 3), "end": round(t + d, 3), "text": " ".join(c)})
        t += d + GAP
    return out


def build_captions(segments: list[tuple[float, float, str]], max_words: int) -> list[dict]:
    caps = []
    for s, e, text in segments:
        caps.extend(captions_for_segment(s, e, text, max_words))
    # strip trailing punctuation that reads badly as a 2-word caption
    for c in caps:
        c["text"] = c["text"].strip(" ,;")
    return caps


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript")
    ap.add_argument("out")
    ap.add_argument("--max-words", type=int, default=3)
    args = ap.parse_args(argv)
    with open(args.transcript) as f:
        segs = parse_transcript(f.read())
    caps = build_captions(segs, args.max_words)
    with open(args.out, "w") as f:
        json.dump(caps, f, indent=1)
    print(f"{len(caps)} captions from {len(segs)} segments -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
