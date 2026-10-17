# Episode 1, the accuracy trap: idea

**State:** storyboarded 2026-10-16. `storyboard.md` is current, and where they differ it wins over this file (the numbers come from `_data/ledger.json`). The ledger, the images,
and Chris's words are in `../SERIES.md`.

## Preflight (phrase checked 10/16)

- **Question:** Why is my 99.5% accurate model useless?
- **Who is asking:** an engineer whose classifier looks great on accuracy
  and still misses the cases that matter.
- **Answer in one sentence:** when only 0.5% of cases are positive, a
  model that never says yes is 99.5% accurate, so accuracy mostly counts
  the easy negatives. Count the four boxes of the confusion matrix
  instead.
- **Search phrase (checked 10/16):** confusion matrix explained.
  "imbalanced dataset" also autocompletes, so use it in the title or
  description. "accuracy imbalanced" does not.

## Beats (sketch)

1. **Frame 0:** the score line already full: 9,950 teal user dots and 50
   attack dots. VO line 1 is the reframe: "This model is 99.5% accurate,
   and it has never caught a single attack."
2. "Never flag": no line on the axis, and every dot is called safe. A
   counter shows 99.5%.
3. Model A: the magenta threshold drops in, 100 dots flip to flagged, and
   the counter reads 99.3%. It's lower, and it catches 40 of 50.
4. The 2×2 box builds from the dots. Each group of dots flies into its
   cell, and the cells get named in Chris's words (TP, FP, FN, TN).
5. The TN cell swells to 9,890. That's where accuracy's number comes
   from.
6. Last line: the takeaway over the box ("With rare positives, look at
   the box, not the accuracy").

## Code (fits, PyTorch)

```python
y = torch.zeros(10_000); y[:50] = 1          # 50 attacks
pred = torch.zeros(10_000)                   # never flag
(pred == y).float().mean()                   # tensor(0.9950)
```

Payoff beat 2: the "model" is one line of zeros, and it scores 0.995.

## Open

- None blocking. Storyboard picks the engine (probably HyperFrames: dots
  and the box).
