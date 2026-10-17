# Episode 2, precision and recall: idea

**State:** storyboarded 2026-10-16. `storyboard.md` is current, and where they differ it wins over this file (the numbers come from `_data/ledger.json`). The ledger, the images,
and Chris's words are in `../SERIES.md`.

## Preflight (phrase checked 10/16)

- **Question:** What's the difference between precision and recall?
- **Who is asking:** someone who has seen both numbers on a report and
  mixes them up.
- **Answer in one sentence:** precision asks, of the ones I flagged, how
  many were attacks; recall asks, of all the attacks, how many I caught.
  Same numerator, different denominators.
- **Search phrase (checked 10/16):** precision vs recall (the top
  suggestion). "precision and recall explained" also autocompletes.

## Beats (sketch)

1. **Frame 0:** the Model A box from ep 1, with the threshold on the
   score line. VO line 1: "Precision and recall are the same 40 catches
   divided by two different things."
2. **Recall:** the 50 attack dots get circled, wherever they sit. 40 are
   right of the line. 40 / 50 = 80%. "Of all the positives, how many did
   I catch?"
3. **Precision:** the 100 flagged dots right of the line get circled. 40
   are attacks and 60 are blocked users. 40 / 100 = 40%. "Of the ones I
   predicted positive, how many actually were?"
4. The TN cell (9,890) dims. Neither formula touches it, which is why
   they still work when positives are rare.
5. The memory hook: recall is what you *missed* (attacks through), and
   precision is what you *wasted* (users blocked).
6. Last line (if time): "Two questions, two denominators. Ask both."

## Code (fits, PyTorch)

```python
tp = (pred & y).sum()           # pred, y: bool tensors
precision = tp / pred.sum()     # of my flags
recall    = tp / y.sum()        # of the attacks
```

The two denominators sit on adjacent lines, so the code is the beat 2–3
contrast.

## Open

- None blocking.
