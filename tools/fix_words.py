#!/usr/bin/env python3
"""Fix spellings and caption breaks in words.json, instead of ad hoc Python each Short.

Usage (from the video folder; ops run in this order: --join, --sub, --break-after):
    uv run --no-sync python ../../tools/fix_words.py words.json \
        --join "agent's MD," "AGENTS.md," \
        --sub harnesses "harness is" \
        --sub "error,@10.8" "error." \
        --break-after "error.@10.8"
    # writes words.json in place (or -o other.json) and prints the fixed text

Why: runbook step 5 fixes words.json's spellings against the Parakeet
transcript once, so the captions (step 7) and every beat's cues read the same
words. The recognizer merges and splits words ("harnesses" for "harness is",
"agent's MD," for "AGENTS.md,") and runs two sentences into one segment.

Ops (WORD is matched on the word with surrounding whitespace removed; add
@SECONDS to pick only the occurrence nearest that master time, otherwise
every occurrence):
  --join "W1 W2 ..." NEW   consecutive words -> one word: first start, last end
  --sub WORD NEW           replace the word's text (NEW may contain spaces)
  --break-after WORD       start a new caption segment after the word
Segment indexes are renumbered 0, 1, 2 ... in file order at the end.
"""
from __future__ import annotations

import argparse
import json
import sys


def _target(spec: str) -> tuple[str, float | None]:
    """'error,@10.8' -> ('error,', 10.8); 'error,' -> ('error,', None)."""
    word, sep, at = spec.rpartition("@")
    if sep and word:
        try:
            return word, float(at)
        except ValueError:
            pass
    return spec, None


def _pick(hits: list[int], words: list[dict], at: float | None) -> list[int]:
    if at is None or not hits:
        return hits
    return [min(hits, key=lambda i: abs(words[i]["t"] - at))]


def _keep_space(old: str, new: str) -> str:
    """Keep the original word's leading whitespace (recognizers emit ' word')."""
    return old[: len(old) - len(old.lstrip())] + new


def join(words: list[dict], spec: str, new: str) -> int:
    seq_spec, at = _target(spec)
    seq = seq_spec.split()
    n = len(seq)
    hits = [i for i in range(len(words) - n + 1)
            if [w["word"].strip() for w in words[i:i + n]] == seq]
    picked = set(_pick(hits, words, at))
    out, i, done = [], 0, 0
    while i < len(words):
        if i in picked:
            first, last = words[i], words[i + n - 1]
            merged = dict(first, word=_keep_space(first["word"], new), end=last.get("end", last["t"]))
            out.append(merged); i += n; done += 1
        else:
            out.append(words[i]); i += 1
    words[:] = out
    return done


def sub(words: list[dict], spec: str, new: str) -> int:
    word, at = _target(spec)
    hits = _pick([i for i, w in enumerate(words) if w["word"].strip() == word], words, at)
    for i in hits:
        words[i]["word"] = _keep_space(words[i]["word"], new)
    return len(hits)


def break_after(words: list[dict], spec: str) -> int:
    """Give every word after the target a fresh segment index until its segment ends."""
    word, at = _target(spec)
    hits = _pick([i for i, w in enumerate(words) if w["word"].strip() == word], words, at)
    fresh = max((w.get("seg", 0) for w in words), default=0) + 1
    for i in hits:
        seg = words[i].get("seg", 0)
        j = i + 1
        while j < len(words) and words[j].get("seg", 0) == seg:
            words[j]["seg"] = fresh; j += 1
        fresh += 1
    return len(hits)


def renumber(words: list[dict]) -> None:
    """Segment indexes 0, 1, 2 ... in file order (a new index wherever it changes)."""
    n, prev = -1, object()
    for w in words:
        if w.get("seg", 0) != prev:
            n += 1; prev = w.get("seg", 0)
        w["seg"] = n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words")
    ap.add_argument("-o", "--out", help="output path (default: overwrite the input)")
    ap.add_argument("--join", nargs=2, action="append", default=[], metavar=("WORDS", "NEW"))
    ap.add_argument("--sub", nargs=2, action="append", default=[], metavar=("WORD", "NEW"))
    ap.add_argument("--break-after", action="append", default=[], metavar="WORD")
    args = ap.parse_args(argv)
    words = json.load(open(args.words))
    missing = []
    for spec, new in args.join:
        if not join(words, spec, new): missing.append(f"--join {spec!r}")
    for spec, new in args.sub:
        if not sub(words, spec, new): missing.append(f"--sub {spec!r}")
    for spec in args.break_after:
        if not break_after(words, spec): missing.append(f"--break-after {spec!r}")
    renumber(words)
    with open(args.out or args.words, "w") as f:
        json.dump(words, f, indent=1)
    print(" ".join(w["word"].strip() for w in words))
    for m in missing:
        print(f"no match: {m}", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
