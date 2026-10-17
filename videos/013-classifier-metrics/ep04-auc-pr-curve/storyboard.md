ENGINE: mixed

# ROC AUC vs PR AUC: the precision-recall curve (series ep 4 of 5): storyboard (v1, pre-VO)

THE QUESTION: "ROC AUC or PR AUC for imbalanced data?"
WHO IS ASKING: someone whose model has a great AUC but whose flags are
mostly wrong.
THE ANSWER IN ONE SENTENCE: AUC turns the curve into one number for
comparing models, but when positives are rare a tiny false positive rate
can still be hundreds of blocked users, and only the precision-recall
curve shows that.
THE SEARCH PHRASE: precision recall curve explained (checked 10/16).
"pr auc vs roc auc" also autocompletes exactly, so put it in the title.

**One idea:** the false positive rate divides by 9,950, so it hides the
blocked users. Precision doesn't.

Series context: `../SERIES.md`. Beats 2 and 5–6 use Chris's sentences.
This is the densest episode, so cut hard at step 5.

## Ledger (from SERIES.md and `_data/ledger.json`)

- Model A: **ROC-AUC 0.985**, **PR-AUC (average precision) 0.556**.
- The zoom point is threshold **0.55: FPR 2.3%, 44 of 50 caught, 233
  users blocked, precision 16%** (44 / 277).
- Coin flip: ROC **0.5**. PR **0.005** (the attack rate). 0.556 / 0.005 ≈
  **111×**, said as "over a hundred times better than chance".
- The AUC reading: the chance a random attack scores above a random user.
  For Model A that's **98.5%**.
- Code (sklearn, beat 6): `roc_auc_score(y, scores)  # 0.985` ·
  `average_precision_score(y, scores)  # 0.556`

## The look

Starts on ep 3's ROC plot of Model A, full width. Beat 2 shades the
area. Beat 3 zooms into the 0.55 point, with a small box inset showing
its counts. Beat 5 **morphs the plot**: the x axis label changes from
"false positive rate" to "recall", the y axis becomes "precision", and
every point slides to its new (recall, precision) position. Each point
keeps its identity (Transform, not a fade-swap) so the viewer sees it's
the same model. The good corner moves from top left to top right. Plots
are Manim if the morph needs real axes, and HyperFrames for the inset box
and code card.

**Hero handoff:** the shaded area (1–2), the 0.55 point (3–4), the PR
curve (5), the 0.005 baseline (6).

## Beats

| # | Beat | ~s | Visual (9:16) | Hero | VO (draft; beats 2, 5–6 Chris's words) |
|---|------|---:|---|---|---|
| 1 | Hook | 6 | Frame 0: Model A's ROC curve hugging the top left, area shaded, "ROC AUC 0.985". | the shaded area | This model's ROC AUC is 0.985. Nearly perfect. And most of what it flags is wrong. |
| 2 | What AUC is | 10 | The area pulses. One attack dot and one user dot get pulled side by side, and the attack is higher. A counter: "98.5% of pairs". The diagonal: "0.5". | the area | AUC is the area under the curve. It's for comparing models. Pick a random attack and a random user, and 98.5% of the time the attack scores higher. A coin flip is 0.5. |
| 3 | Count the point | 9 | Zoom into the point at FPR 2.3%. An inset box: caught 44, blocked **233**. The 233 teal dots light up on a mini score line. | the 0.55 point | Now look at this point. False positive rate, 2.3 percent. Sounds small. It's 233 real users blocked, to catch 44 attacks. |
| 4 | Why it hides | 6 | The FPR fraction appears: 233 / **9,950**. The 9,950 is huge, and the fraction looks tiny. | the 9,950 | The false positive rate divides by every real user, so hundreds of mistakes still look tiny. |
| 5 | Swap the axis | 11 | Axis labels change: x becomes recall, y becomes precision. Every point slides to its new position, and the curve sags low. The 0.55 point lands at (0.88, 0.16). The top-right corner glows. | the PR curve | So swap it for precision. Precision doesn't use true negatives. Recall goes across, precision goes up, and the same model's curve drops. Now the good corner is top right. |
| 6 | Baseline and code | 10 | A flat dashed line at 0.005 hugs the bottom: "coin flip". The PR area shades: "PR AUC 0.556". The code card shows two lines with outputs 0.985 and 0.556. | the 0.005 line, then the code | And a coin flip here isn't 0.5. It's 0.005, the attack rate. This model's PR AUC is 0.56. Low-looking, but over a hundred times better than chance. |
| 7 | Takeaway | 5 | Both curves side by side, small: ROC (0.985) and PR (0.556). Still frame. | none | ROC AUC compares rankings. When positives are rare, read the precision-recall curve. |

Total ≈ 57 s before tightening. If the take is long, beat 4 goes first,
then "Low-looking, but…" in beat 6.

## Read-aloud script

This model's ROC AUC is 0.985. Nearly perfect. And most of what it flags
is wrong.

AUC is the area under the curve. It's for comparing models. Pick a random
attack and a random user, and 98.5% of the time the attack scores higher.
A coin flip is 0.5.

Now look at this point. False positive rate, 2.3 percent. Sounds small.
It's 233 real users blocked, to catch 44 attacks.

*(if time:)* The false positive rate divides by every real user, so
hundreds of mistakes still look tiny.

So swap it for precision. Precision doesn't use true negatives. Recall
goes across, precision goes up, and the same model's curve drops. Now the
good corner is top right.

And a coin flip here isn't 0.5. It's 0.005, the attack rate. This model's
PR AUC is 0.56. *(if time:)* Low-looking, but over a hundred times better
than chance.

ROC AUC compares rankings. When positives are rare, read the
precision-recall curve.

## Not in this Short (on purpose)

The McDermott et al. (2024) caveat goes in the description and a pinned
comment: PR-AUC isn't always better. It rewards the top of the list, while
ROC-AUC weights every ranking mistake the same, which is fairer across
groups with different base rates. Also left out: the step-wise vs
trapezoid AP detail, and Davis & Goadrich.

## Title and description (draft)

- Title options: "ROC AUC vs PR AUC: Why 0.985 Can Still Be Bad" ·
  "Precision Recall Curve Explained (PR AUC vs ROC AUC)"
- Description: the caveat above with links (Saito & Rehmsmeier 2015,
  McDermott et al. 2024), and "Part 4 of 5. Next: F1 and picking the
  threshold."
