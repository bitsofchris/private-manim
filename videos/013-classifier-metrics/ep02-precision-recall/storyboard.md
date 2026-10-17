ENGINE: hyperframes

# Precision vs recall (series ep 2 of 5): storyboard (v1, pre-VO)

THE QUESTION: "What's the difference between precision and recall?"
WHO IS ASKING: someone who has seen both numbers on a report and mixes
them up.
THE ANSWER IN ONE SENTENCE: precision asks, of the ones I flagged, how
many were attacks; recall asks, of all the attacks, how many I caught.
Same numerator, different denominators.
THE SEARCH PHRASE: precision vs recall (checked 10/16, the top
suggestion).

**One idea:** the same 40 catches, divided by two different things.

Series context: `../SERIES.md`. The two definitions are Chris's, word for
word. The connecting lines are a draft, so put them in your own words.

## Ledger (from SERIES.md)

- Model A box: **TP 40 · FP 60 · FN 10 · TN 9,890**, same layout as ep 1
  (rows flagged / not flagged, columns attack / real user).
- Recall = 40 / 50 = **80%**. Precision = 40 / 100 = **40%**.
- FP = a real user blocked. FN = an attack that got through.
- Code (PyTorch, `pred` and `y` are bool tensors):
  `tp = (pred & y).sum()` · `precision = tp / pred.sum()  # of my flags` ·
  `recall = tp / y.sum()  # of the attacks`

## The look

Ep 1's end state is frame 0: the score line on top with the magenta
threshold at 0.70, and the box below. Ep 2 adds **fraction bars** under
the box, with the numerator on top and the denominator below. The
denominator is built by lifting a row or column out of the box, so the
viewer sees where each one comes from. The column (attack) is recall's
denominator, and the row (flagged) is precision's. Keep that geometry
the whole way through, since it's the memory aid.

## Beats

| # | Beat | ~s | Visual (9:16) | Hero | VO (draft; definitions are Chris's words) |
|---|------|---:|---|---|---|
| 1 | Hook | 6 | Frame 0: the score line and box from ep 1. The TP cell's "40" is already lifted out, sitting above two empty fraction bars that each have a "40" on top. | the 40 | Precision versus recall comes down to one thing: the same forty catches, divided by two different numbers. |
| 2 | Recall | 11 | On the score line, all 50 attack dots ring, on both sides of the line. In the box, the *attack column* (TP 40 + FN 10) lifts out and becomes the left bar's denominator: 40 / 50 → **80%**. The FN 10 dots blink on the left of the line. | the attack column | Recall: of all the positives, how many did I catch? There were fifty attacks. We caught forty. Recall is eighty percent. |
| 3 | Precision | 11 | The 100 dots right of the threshold ring (40 attack, 60 teal). The *flagged row* (TP 40 + FP 60) lifts out and becomes the right bar's denominator: 40 / 100 → **40%**. | the flagged row | Precision: of the ones I predicted positive, how many actually were? We flagged a hundred. Forty were attacks. Precision is forty percent. |
| 4 | Code | 8 | The code card slides in below the bars: three lines. `.sum()` on line 2 (`pred.sum()`) and line 3 (`y.sum()`) highlight in turn, matching the right and left bars. | the two denominators | In code, it's the same numerator, over two different sums. |
| 5 | What's missing | 8 | The code card leaves. The TN cell (9,890) dims to ghost opacity, and a thin strike runs through it. Neither bar touches it. | the ghosted TN cell | And notice what's missing. Nine thousand eight hundred ninety true negatives. Neither one uses them. That's why they still work when attacks are rare. |
| 6 | Memory hook | 9 | The FN cell lights: "10 attacks got through" under recall. The FP cell lights: "60 users blocked" under precision. | FN, then FP | Recall is about what you missed: attacks that got through. Precision is about what you wasted: real users you blocked. |
| 7 | Takeaway | 3 | Both bars, 80% and 40%, side by side. Still frame. | none | Two questions. Two denominators. You need both. |

Total ≈ 56 s before tightening. If the take is long, beat 4 goes first,
then the last sentence of beat 5.

## Read-aloud script

Precision versus recall comes down to one thing: the same forty catches,
divided by two different numbers.

Recall: of all the positives, how many did I catch? There were fifty
attacks. We caught forty. Recall is eighty percent.

Precision: of the ones I predicted positive, how many actually were? We
flagged a hundred. Forty were attacks. Precision is forty percent.

*(if time:)* In code, it's the same numerator, over two different sums.

And notice what's missing. Nine thousand eight hundred ninety true
negatives. Neither one uses them. *(if time:)* That's why they still work
when attacks are rare.

Recall is about what you missed: attacks that got through. Precision is
about what you wasted: real users you blocked.

Two questions. Two denominators. You need both.

## Not in this Short (on purpose)

Moving the threshold (ep 3). F1 (ep 5). "Sensitivity" as another name for
recall goes in the description, not the VO.

## Title and description (draft)

- Title options: "Precision vs Recall, Explained in One Picture" ·
  "Precision vs Recall: Same Numerator, Different Denominator"
- Description: the two formulas, "recall a.k.a. sensitivity / true
  positive rate", and "Part 2 of 5. Previous: confusion matrix. Next: ROC
  curve."
