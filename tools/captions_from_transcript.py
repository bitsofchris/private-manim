#!/usr/bin/env python3
"""Turn a MacWhisper timestamped transcript into captions.json for assemble.py.

Usage:
    tools/captions_from_transcript.py words.json captions.json [--max-words 3] [--max-chars 15]
    # or MacWhisper's transcript_final.json, or a .txt transcript

Input format (MacWhisper `--format txt --timestamps --end-timestamps --milliseconds`):

    00:01.730-00:03.490
    A neural network is just a function

    ...

Or words.json from tools/word_times.py (the usual input since 2026-10-11:
word-timed, spellings already fixed). Or MacWhisper's JSON (`--format json`, Pro), whose segments may carry a
`words` array with per-word times (WhisperKit and Parakeet engines do;
whisper.cpp does not):

    {"segments": [{"start": 580, "end": 3400, "text": "...",
                   "words": [{"start": 580, "end": 900, "text": "A"}, ...]}]}

Each segment's words are chunked into groups of at most --max-words. With
word times, chunks never cross a sentence end (. ? !), and a chunk runs from its first word's start to the next chunk's
start (minus a small gap). Without them, the segment's span is divided among
the chunks in proportion to their character length (a decent proxy for
spoken duration). A small gap is left between chunks so they visibly change.

A chunk longer than --max-chars is split again at its most balanced word
break: a longer caption wraps to two lines, and with `assemble.py
--captions-anchor bottom` the second line climbs into the stage (013: ep01
"predicted attack, but" over the box at 21 characters, "confusion matrix."
at 17; ep02 and ep05 settled on 15 by hand). Captions shorter than
FLASH seconds are listed on stderr: two fast words can be an unreadable
flash ("Here's a", 80 ms, 013 ep01); merge them by hand in captions.json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

GAP = 0.06  # seconds between consecutive captions
MAX_CHARS = 15  # one line at the caption size, with margin
FLASH = 0.15    # a caption shorter than this is reported


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


def parse_mw_json(text: str) -> list[dict]:
    """Segments from MacWhisper JSON: [{start, end, text, words: [(t0, t1, word)] or []}], seconds."""
    out = []
    for seg in json.loads(text).get("segments", []):
        words = [(w["start"] / 1000, w["end"] / 1000, w["text"].strip()) for w in (seg.get("words") or []) if w["text"].strip()]
        out.append({"start": seg["start"] / 1000, "end": seg["end"] / 1000, "text": seg["text"].strip(), "words": words})
    return out


def segments_from_words(words: list[dict]) -> list[dict]:
    """words.json (tools/word_times.py) back into word-timed segments: each run of
    consecutive words with the same "seg" index is one segment, in file order (the
    index only marks where one segment ends, so a hand-edited or out-of-order index
    never moves words)."""
    out, prev = [], object()
    for w in words:
        k = w.get("seg", 0)
        if k != prev:
            out.append({"words": []}); prev = k
        out[-1]["words"].append((w["t"], w.get("end") or w["t"], w["word"]))
    for seg in out:
        ws = seg["words"]
        seg.update(start=ws[0][0], end=ws[-1][1], text=" ".join(w for _, _, w in ws))
    return out


def load_segments(path: str) -> list[dict]:
    """Segments from words.json, a MacWhisper .json, or a .txt transcript, in one shape."""
    text = open(path).read()
    if path.endswith(".json"):
        data = json.loads(text)
        if isinstance(data, list):
            return segments_from_words(data)
        return parse_mw_json(text)
    return [{"start": s, "end": e, "text": t, "words": []} for s, e, t in parse_transcript(text)]


SENTENCE_END = re.compile(r"[.?!][\"')\]]*$")


def sentences(words: list[tuple[float, float, str]]) -> list[list[tuple[float, float, str]]]:
    """Split word-timed words after each word that ends a sentence (. ? !), so no
    caption spans two sentences when the recognizer put them in one segment
    ("last error. Tools are", 012 ep01). "AGENTS.md," and "0.70" don't end one."""
    out, cur = [], []
    for w in words:
        cur.append(w)
        if SENTENCE_END.search(w[2]):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def captions_for_words(words: list[tuple[float, float, str]], max_words: int, max_chars: int = MAX_CHARS) -> list[dict]:
    """Chunks timed by their words: start at the first word, end at the next chunk's start (minus GAP).
    Chunks never cross a sentence end."""
    chunks = []
    for sent in sentences(words):
        i = 0
        for size in [len(c) for c in chunk_words([w for _, _, w in sent], max_words, max_chars)]:
            chunks.append(sent[i:i + size]); i += size
    out = []
    for k, c in enumerate(chunks):
        end = chunks[k + 1][0][0] - GAP if k + 1 < len(chunks) else c[-1][1]
        out.append({"start": round(c[0][0], 3), "end": round(max(end, c[0][0] + GAP), 3), "text": " ".join(w for _, _, w in c)})
    return out


def fit_chars(group: list[str], max_chars: int) -> list[list[str]]:
    """Split one group at its most balanced word break until each part fits max_chars
    (a single word that is longer stays whole)."""
    if len(group) < 2 or len(" ".join(group)) <= max_chars:
        return [group]
    k = min(range(1, len(group)), key=lambda i: abs(len(" ".join(group[:i])) - len(" ".join(group[i:]))))
    return fit_chars(group[:k], max_chars) + fit_chars(group[k:], max_chars)


def _greedy(words: list[str], max_words: int, max_chars: int) -> list[list[str]]:
    """Fill each group while it fits both limits; then give a lone last word a partner."""
    out, cur = [], []
    for w in words:
        if cur and (len(cur) == max_words or len(" ".join(cur + [w])) > max_chars):
            out.append(cur); cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    if len(out) > 1 and len(out[-1]) == 1 and len(out[-2]) > 1 \
            and len(" ".join(out[-2][-1:] + out[-1])) <= max_chars:
        out[-1].insert(0, out[-2].pop())
    return out


def chunk_words(words: list[str], max_words: int, max_chars: int = MAX_CHARS) -> list[list[str]]:
    """Groups of <= max_words, balanced so the last group isn't a lone word. If any
    group would run over max_chars, the whole run is regrouped greedily by characters
    instead, which avoids splitting "When positives are rare," into a lone "When"."""
    balanced = _balanced(words, max_words)
    if all(len(" ".join(g)) <= max_chars for g in balanced):
        return balanced
    return [part for g in _greedy(words, max_words, max_chars) for part in fit_chars(g, max_chars)]


def _balanced(words: list[str], max_words: int) -> list[list[str]]:
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


def captions_for_segment(start: float, end: float, text: str, max_words: int, max_chars: int = MAX_CHARS) -> list[dict]:
    words = text.split()
    chunks = chunk_words(words, max_words, max_chars)
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


def build_captions(segments: list, max_words: int, max_chars: int = MAX_CHARS) -> list[dict]:
    """segments: (start, end, text) tuples, or load_segments() dicts (word-timed when they have words)."""
    caps = []
    for seg in segments:
        if isinstance(seg, dict):
            caps.extend(captions_for_words(seg["words"], max_words, max_chars) if seg["words"]
                        else captions_for_segment(seg["start"], seg["end"], seg["text"], max_words, max_chars))
        else:
            caps.extend(captions_for_segment(*seg, max_words, max_chars))
    # strip trailing punctuation that reads badly as a 2-word caption
    for c in caps:
        c["text"] = c["text"].strip(" ,;")
    return caps


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript")
    ap.add_argument("out")
    ap.add_argument("--max-words", type=int, default=3)
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    args = ap.parse_args(argv)
    segs = load_segments(args.transcript)
    caps = build_captions(segs, args.max_words, args.max_chars)
    for c in caps:
        if c["end"] - c["start"] < FLASH:
            print(f"flash: {c['text']!r} at {c['start']:.2f} lasts {c['end'] - c['start']:.2f} s", file=sys.stderr)
    with open(args.out, "w") as f:
        json.dump(caps, f, indent=1)
    print(f"{len(caps)} captions from {len(segs)} segments -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
