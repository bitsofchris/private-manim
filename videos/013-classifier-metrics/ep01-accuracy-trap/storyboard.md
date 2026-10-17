ENGINE: hyperframes

# Confusion matrix explained: the accuracy trap (series ep 1 of 5): storyboard (v1, pre-VO)

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

Series context: `../SERIES.md` (ledger, images, Chris's words). The four
definitions in the VO are Chris's, word for word from the vault journal.
The connecting lines are a draft, so put them in your own words before
recording. About 140 words.

## Ledger (copied from SERIES.md; every beat uses exactly these)

- A **prompt-injection detector** in front of an AI agent. **10,000
  requests: 50 attacks, 9,950 real users.**
- "Never flag": accuracy **99.5%**, catches **0 of 50**.
- **Model A** flags **100** requests, and **40** are attacks. Accuracy
  **99.3%**.
- Box: **TP 40 · FP 60 · FN 10 · TN 9,890.** Rows are "flagged / not
  flagged", and columns are "attack / real user". The same layout is used
  in all five episodes.
- Code: `y = torch.zeros(10_000); y[:50] = 1` · `pred = torch.zeros(10_000)` ·
  `(pred == y).float().mean()  # tensor(0.9950)`.

## The look

**The score line** (the series image, built here and reused in eps 2–5).
A horizontal axis across the middle of the stage, labelled "attack score"
from 0 to 1. The 9,950 user dots are a dense teal beeswarm piled up on
the left with a thin tail to the right, drawn on a canvas at small dot
size. The 50 attack dots are bigger, in their own color, clustered toward
the right, and about 10 of them sit inside the teal tail. **Attack color:**
add one category token to `style.py` before building (e.g. `ATTACK`, a
warm amber/gold, far from teal and magenta, checked for contrast). It is
not magenta, which belongs to the threshold. **The threshold** is a vertical
magenta line, and it's the series hero. In ep 1 it only shows up in beat 3.

**The box.** A 2×2 grid. Column headers "attack" and "real user", row
headers "flagged" and "not flagged". Each cell holds its count and its
two-letter tag. In beat 4, the dots fly from the score line into their
cells.

Layout (9:16, captions in the bottom band, which belongs to
`assemble.py`): the score line takes the top-middle third, the counter or
box goes in the middle, and the code card sits below the middle in beat 2
only.

## Beats

| # | Beat | ~s | Visual (9:16) | Hero | VO (draft; definitions are Chris's words) |
|---|------|---:|---|---|---|
| 1 | Hook | 6 | Frame 0, already working: the full score line with all 10,000 dots. A big accuracy counter above it reads **99.5%**, and under it a small tag reads "attacks caught: 0 / 50". No threshold line. | the counter | This model is 99.5% accurate, and it has never caught a single attack. The confusion matrix shows why. |
| 2 | Never flag | 11 | The dots pulse once, and the 50 attack dots ring briefly on "only fifty". The code card fades in below the middle: three lines, highlighted one at a time as the VO reaches them. The third line's output `tensor(0.9950)` lands as the counter re-ticks to 99.5%. | the counter, then the code card's output | It's a prompt-injection detector. Ten thousand requests come in, and only fifty are attacks. So a model that never flags anything is right 99.5% of the time. |
| 3 | Model A | 11 | The code card leaves. The magenta threshold drops onto the score line. The 100 dots to its right light up: 40 attack dots and 60 teal dots. The tag ticks to "attacks caught: 40 / 50" while the counter ticks *down* to **99.3%**. Hold on the two numbers. | the threshold | Here's a real model. It flags a hundred requests, and forty of them are attacks. It catches forty out of fifty, and its accuracy goes down. 99.3%. Worse than doing nothing. |
| 4 | The box | 16 | The counter dissolves into the empty 2×2. On each definition, that group of dots flies from the score line into its cell and the count lands: TP 40 (attack dots right of the line), TN 9,890 (teal left), FP 60 (teal right), FN 10 (attack dots left). One cell lit at a time. | the cell being named | So count four boxes instead. True positive: what I correctly said is positive. True negative: what I correctly said is negative. False positive: I wrongly predicted positive. False negative: I wrongly said this was negative, but it was positive. |
| 5 | Where accuracy comes from | 8 | The TN cell swells until it fills most of the grid, and the other three shrink to slivers. The tag "9,890 of 9,930 correct" appears on the TN cell. | the TN cell | Look where the accuracy comes from. Almost all of it is true negatives, the easy ones. |
| 6 | Takeaway | 4 | The box returns to its normal size, all four cells lit evenly, and the score line rests above it. Still frame. | none (rest) | With rare positives, don't read the accuracy. Read the box. |

Total ≈ 56 s before tightening. The "if time" cut is beat 3's last
sentence ("Worse than doing nothing."). No closing hook, no call to
action.

## Read-aloud script

This model is 99.5% accurate, and it has never caught a single attack.
The confusion matrix shows why.

It's a prompt-injection detector. Ten thousand requests come in, and only
fifty are attacks. So a model that never flags anything is right 99.5% of
the time.

Here's a real model. It flags a hundred requests, and forty of them are
attacks. It catches forty out of fifty, and its accuracy goes down.
99.3%. *(if time:)* Worse than doing nothing.

So count four boxes instead. True positive: what I correctly said is
positive. True negative: what I correctly said is negative. False
positive: I wrongly predicted positive. False negative: I wrongly said
this was negative, but it was positive.

Look where the accuracy comes from. Almost all of it is true negatives,
the easy ones.

With rare positives, don't read the accuracy. Read the box.

## Not in this Short (on purpose)

Precision and recall (ep 2). The threshold as a dial (ep 3): here it only
marks Model A's choice and never moves. The word "imbalanced" stays out
of the VO, since the 50 vs 9,950 shows it. It goes in the title and
description for search.

## Title and description (draft, finalize at publish)

- Title options: "Confusion Matrix Explained: Why 99.5% Accuracy Is
  Useless" · "Confusion Matrix Explained (Imbalanced Dataset)"
- Description: one line on the 10,000 / 50 setup, the four definitions,
  and "Part 1 of 5: next, precision vs recall."
