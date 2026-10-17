ENGINE: hyperframes

# Confusion matrix explained: the accuracy trap (series ep 1 of 5): storyboard (v2, recorded VO)

THE QUESTION: "Why is my 99.5% accurate model useless?"
WHO IS ASKING: an engineer whose classifier looks great on accuracy and
still misses the cases that matter.
THE ANSWER IN ONE SENTENCE: when only 0.5% of cases are positive, a model
that never says yes is 99.5% accurate, so accuracy mostly counts the easy
negatives. Count the four boxes of the confusion matrix instead.
THE SEARCH PHRASE: confusion matrix explained (checked 10/16; "imbalanced
dataset" also autocompletes, so use it in the title or description).

**One idea:** accuracy is mostly true negatives. The box shows you what
it hides.

**Engine:** HyperFrames for every beat (`AGENTS.md` "Which engine"). The
score line is a 0 → 1 axis with dots, not plotted data on real axes, and
the box is a grid; nothing here needs Manim.

Series context: `../SERIES.md` (ledger, images, Chris's words). The VO is
`script.md` (what Chris said), not the planned script in `../SCRIPTS.md`.

## Ledger (copied from SERIES.md; every beat uses exactly these)

- A **prompt-injection detector** in front of an AI agent. **10,000
  requests: 50 attacks, 9,950 real users.**
- "Never flag": accuracy **99.5%**, catches **0 of 50**.
- **Model A** flags **100** requests, and **40** are attacks. Accuracy
  **99.3%** (9,930 / 10,000).
- Box: **TP 40 · FP 60 · FN 10 · TN 9,890.** Rows "flagged / not
  flagged", columns "attack / real user": TP top-left, FP top-right, FN
  bottom-left, TN bottom-right. The same layout in all five episodes.
- Correct = TP + TN = **9,930**, of which TN = **9,890**.
- Model A's threshold is **0.70** (`_data/ledger.json`, `model_a_box.t`).
  Dots come from `_data/scores.npz` (seed 13), model `a`.
- Frame-0 tag (SERIES.md "Context in every episode"): **prompt-injection
  detector · 10,000 requests · 50 attacks**.
- Code: `y = torch.zeros(10_000); y[:50] = 1` · `pred = torch.zeros(10_000)` ·
  `(pred == y).float().mean()  # tensor(0.9950)`.

## The look

**The score line** (the series image, built here and reused in eps 2–5).
A horizontal axis across the top-middle of the stage, labelled "attack
score" with ticks 0 and 1. The 9,950 user dots are a dense teal beeswarm
piled up on the left with a thin tail to the right, drawn on a canvas at
small dot size. The 50 attack dots are bigger, in **gold
(`CONTENT_GOLD`, `#E0B040`, the existing categorical token; no
`style.py` change)**, toward the right, 10 of them inside the teal tail.
**The threshold** is a vertical magenta line at 0.70, the series hero. In
ep 1 it first shows up in beat 3 and never moves. Flagged dots (right of
the line) get a bright ring; unflagged dots stay at rest.

**The tag** sits just above the axis, small `--dim` text, from frame 0 to
the end.

**The counter.** Big "accuracy 99.5%" in the middle of the stage, with
"attacks caught 0 / 50" under it.

**The box.** A 2×2 grid in the middle of the stage. Column headers
"attack" (gold) and "real user" (teal), row headers "flagged" and "not
flagged". Each cell holds its count and its two-letter tag. Dots fly from
the score line into their cells.

Layout (9:16, captions in the band y 1100–1536, which belongs to
`assemble.py`): tag + score line y ~260–560; counter, code card or box y
~620–1080. The code card shares the middle with the counter in beat 2
only.

Shared kit: `_kit/score.js` (score line, dots, threshold, box, counter)
linked into every beat as `kit/`, so every beat opens on its neighbour's
end state. `00_layout/` renders the canonical frame.

## Beats (VO from script.md; times are vo_clean seconds, finals after tightening)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook | This model is 99.5% accurate, but it's never caught a single attack. | Frame 0, already working: the full score line with all 10,000 dots, the tag above it, no threshold. The counter reads **99.5%**, "attacks caught 0 / 50" under it, the dots settling. On "never caught" the 0 / 50 pulses. | the counter |
| 2 | Never flag | It's a prompt injection detector. 10,000 requests come in, but only 50 are attacks. It never flags anything, and you're still right 99.5% of the time. | The tag brightens on "prompt injection detector". "10,000 requests": the teal pile pulses. "only 50": the 50 gold dots ring. The counter moves up and the code card fades in below it: the three lines, each highlighted as the VO reaches it ("never flags anything" → `pred = torch.zeros`), and `tensor(0.9950)` lands on "99.5%". | the counter, then the code card's output |
| 3 | Model A | Now, here's a real model. It flags 100 requests and catches 40 of the 50 attacks, but its accuracy goes down to 99.3%. | The code card leaves. On "real model" the magenta threshold drops onto the score line at 0.70. "flags 100": the 100 dots right of it ring (40 gold, 60 teal). "catches 40": the tag ticks to "attacks caught 40 / 50". "goes down": the counter ticks *down* to **99.3%**. Hold. | the threshold |
| 4 | The box, flags | So we look at the confusion matrix instead. A true positive is I said there was an attack, and it was genuinely an attack. A false positive is the model predicted attack, but it was a real user. | "confusion matrix": the counter dissolves into the empty 2×2 (headers in). TP: the 40 gold dots right of the line fly into the top-left cell, "TP 40" lands. FP: the 60 teal dots right of the line fly into the top-right, "FP 60". One cell lit at a time. | the cell being named |
| 5 | The box, misses | A false negative, I said user, but it was an attack. And a true negative, I said user, and it was a user. | FN: the 10 gold dots left of the line fly into bottom-left, "FN 10". TN: the teal pile streams into bottom-right, "TN 9,890". | the cell being named |
| 6 | Where accuracy comes from | Now look where the accuracy comes from. Almost all of it is true negatives. These are the easy ones. | "accuracy": "99.3% = 9,930 correct" above the box. "true negatives": the TN cell swells until it fills most of the grid, the other three shrink; "9,890 of 9,930" on TN. "easy ones": hold. | the TN cell |
| 7 | Takeaway | When positives are rare, we don't want to read the accuracy. We want to look at the confusion matrix. | "rare": the 50 gold dots on the score line pulse once. The box returns to its normal size, all four cells lit evenly, the score line above it. Still frame by the end. | none (rest) |

Cut candidates and per-beat lengths: see "Cut list" below. The final beat
table (master start, length, folder) is written after the cut is approved.

## Cut list (proposed, waiting on Chris)

Raw take 54.5 s. Pauses capped at 0.25 s (`--noise=-45dB`, so word tails
like "attacks" aren't clipped) → 49.6 s with no phrase cuts.

| # | Cut | vo_clean range | Saves | Why |
|---|---|---|---:|---|
| 1 | a 0.2 s breath/click inside the 2 s pause after line 1 | 4.80–6.60 | 0.5 s | not a word; the pause cap kept it as its own piece |
| 2 | "…a real user **in this case**." | 34.36–35.05 | 0.7 s | filler; script.md flags it |
| 3 | "…it was a user**, not an attack**." | 41.70–42.50 | 0.8 s | repeats "it was a user"; script.md flags it |

With all three: **48.8 s**. Trial-cut and re-transcribed: every join reads
clean. Beat lengths in the trial: 1 hook 5.2 · 2 never flag 8.1 · 3
Model A 7.5 · 4 box flags 10.5 · 5 box misses 6.5 · 6 accuracy 4.9 · 7
takeaway 6.2.

Kept on purpose:
- "It never flags anything": script.md flags a conflict with "here's a
  real model". It reads as the hook's model (the 99.5% one never flags),
  and "a real model" is the contrast, so it stays. The visual makes it
  explicit: no threshold until beat 3.
- "genuinely an attack" (one word, and it's Chris's voice).
- Both recognizers hear "here's **a** real model", not "your" as
  script.md has it. Captions follow the audio.

## Not in this Short (on purpose)

Precision and recall (ep 2). The threshold as a dial (ep 3): here it only
marks Model A's choice and never moves. The word "imbalanced" stays out
of the VO, since the 50 vs 9,950 shows it. It goes in the title and
description for search.
