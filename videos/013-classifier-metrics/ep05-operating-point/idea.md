# Episode 5, F1 and choosing the threshold: idea

**State:** storyboarded 2026-10-16. `storyboard.md` is current, and where they differ it wins over this file (the numbers come from `_data/ledger.json`). The ledger, the images,
and Chris's words are in `../SERIES.md`. Reframed 10/16 to open on F1,
because nobody searches "how to choose a threshold" and people do search
"f1 score explained". The payoff is still choosing the threshold.

## Preflight

- **Question:** What is the F1 score, and should I maximize it?
- **Who is asking:** someone with a decent curve who now has to ship one
  number and was told to "use F1."
- **Answer in one sentence:** F1 is the harmonic mean of precision and
  recall, so it treats a blocked user and a missed attack as equally bad.
  Usually they aren't, so set the threshold by what each mistake costs.
- **Search phrase (checked 10/16):** f1 score explained. Also
  autocompleting: "f1 score vs accuracy", "precision recall tradeoff".
  "how to choose threshold" and "optimal threshold" return other fields
  (audio compressors, image processing), so keep them out of the title.

## Beats (sketch)

1. **Frame 0:** two bars, P 0.9 and R 0.1, with a dashed line at their
   average (0.5) and a magenta F1 line at 0.18. VO line 1: "The F1 score
   is precision and recall in one number, and it punishes whichever one
   is worse."
2. **Why harmonic:** the F1 line pulls down toward the short bar.
   Back on the ledger, Model A is P 40%, R 80%, F1 0.53.
3. **What F1 assumes:** a blocked user and a hijacked agent cost the same.
   Put the two mistakes side by side (an annoyed user and a support ticket,
   vs a hijacked agent) and the threshold on the score line slides right
   or left to match the cost. F-beta with β = 2 counts recall twice as
   much.
4. **The best AUC can lose:** two models' PR curves. Model B has the
   bigger area, but at the recall you need, Model A is higher. You ship a
   threshold, not an area.
5. **State a target:** "catch 80% of attacks, with at least 1 in 3 flags
   real" (recall at fixed precision), or "review the top 100 a day"
   (precision@k). **Trap (if time):** test at the real attack rate. On a
   50/50 test set, the same model's precision jumps from 29% to 99%.
6. Last line: "Decide what a mistake costs, then put the line there."

## Code (fits, PyTorch)

```python
ok = precision >= 1/3
t = thresholds[ok][recall[ok].argmax()]   # most recall at ≥1 in 3 real
```

A sweep over thresholds, then pick by the stated target. Drop it at
storyboard if it reads as noise.

## Open

- Beat 4 needs two synthetic score sets built so that the curves cross.
  Generate them once (seeded) and save them next to the ledger, so the
  beats agree. If beat 4 makes the Short too long, it goes first.
