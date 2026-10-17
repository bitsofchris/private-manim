"""Rebuild captions.json from words.json so no caption wraps to two lines.

Ep02's fraction rows sit just above the caption band (stage to y 1330), and a
two-line caption climbs into the precision row; one line clears it. Chunks are
greedy: at most 3 words and MAX_CHARS characters, broken after a sentence end.
Each caption runs from its first word to just before the next caption (or its
last word's end at a pause), so a fast word is never a flash.

Run from this folder (replaces captions_from_transcript.py for ep02):
    python3 split_captions.py words.json captions.json
"""
import json, sys

MAX_CHARS, MAX_WORDS, GAP, PAUSE, MIN_HOLD = 15, 3, 0.06, 0.45, 0.5
words = json.load(open(sys.argv[1]))
chunks, cur = [], []
for w in words:
    if cur and (len(" ".join(x["word"] for x in cur + [w])) > MAX_CHARS or len(cur) == MAX_WORDS):
        chunks.append(cur); cur = []
    cur.append(w)
    if w["word"][-1] in ".?":
        chunks.append(cur); cur = []
if cur:
    chunks.append(cur)
caps = []
for i, c in enumerate(chunks):
    start, end = c[0]["t"], c[-1]["end"]
    if i + 1 < len(chunks):
        nxt = chunks[i + 1][0]["t"]
        if nxt - end < PAUSE:            # no real pause: hold until the next caption
            end = nxt - GAP
        end = max(end, min(start + MIN_HOLD, nxt - GAP))   # a last word before a pause stays readable
    else:
        end = max(end, start + MIN_HOLD)
    caps.append({"start": round(start, 3), "end": round(end, 3), "text": " ".join(x["word"] for x in c)})
json.dump(caps, open(sys.argv[2], "w"), indent=1)
print(f"{len(caps)} captions; shortest {min(c['end'] - c['start'] for c in caps):.2f} s")
