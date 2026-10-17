ENGINE: mixed

# ROC curve explained (series ep 3 of 5): storyboard (v1, pre-VO)

THE QUESTION: "What is an ROC curve?"
WHO IS ASKING: someone who has seen an ROC plot and doesn't know what a
point on it is.
THE ANSWER IN ONE SENTENCE: the model gives a score, and the threshold
turns it into a yes. Every threshold gives a different confusion matrix,
and the ROC curve plots all of them so you can pick your spot.
THE SEARCH PHRASE: roc curve explained (checked 10/16).

**One idea:** move the line, and the box changes. The curve is every box.

Series context: `../SERIES.md`. Beats 5–7 use Chris's sentences from the
vault journal. The rest is a draft.

## Ledger (from SERIES.md and `_data/ledger.json`)

- Model A scores from `_data/scores.npz`. The threshold stops, as
  (caught / 50, users blocked, FPR):
  **0.20 → 50, 5,055, 51%** · **0.40 → 46, 1,141, 11.5%** ·
  **0.55 → 44, 233, 2.3%** · **0.70 → 40, 60, 0.6% (the ledger box)** ·
  **0.85 → 21, 28, 0.3%**.
- TPR = recall = caught / 50. FPR = blocked users / 9,950.
- Model A ROC-AUC is 0.985. Not said here; it's ep 4's hook.
- Code: `pred = scores > 0.7     # move the line: no retraining`, with the
  0.7 ticking as the line moves.

## The look

The stage stacks three things: the **score line** on top (with the
magenta threshold), a **small box** in the middle that recounts live,
and **ROC axes** at the bottom (x: false positive rate 0 → 1, y: true
positive rate 0 → 1, with a dashed diagonal). Each threshold stop drops a
dot on the ROC axes, and the curve is drawn through all of the
`scores.npz` thresholds, not just the five stops. The threshold line,
the box, and the ROC dot move together. That link is the whole Short.

Engine: HyperFrames for the score line and box. The ROC plot can use
HyperFrames' 2D plane kit (`vec/` axes) if the curve reads well as a
polyline. Otherwise Manim axes for beats 5–7 only. Decide at build.

**Hero handoff:** the threshold line (beats 1–4), then the ROC dot and
curve (5–6), then the top-left corner (6).

## Beats

| # | Beat | ~s | Visual (9:16) | Hero | VO (draft; beats 5–7 Chris's words) |
|---|------|---:|---|---|---|
| 1 | Hook | 6 | Frame 0: all three panels up, with the threshold mid-slide, the box numbers flickering, and a dot moving along a half-drawn ROC curve. | the threshold | You can change what your classifier does without retraining it. Just move this line. That's what an ROC curve is about. |
| 2 | Score, not yes | 8 | Everything freezes at 0.70 (the ledger box). One dot gets a tag: "score 0.83 → flagged". The code card shows `pred = scores > 0.7`. | the line, then `> 0.7` | The model doesn't say yes or no. It gives every request a score. The threshold turns that score into a yes. |
| 3 | Slide left | 8 | The line slides to 0.20, and the code's number ticks to 0.2. The box recounts: caught 50/50, blocked 5,055. A huge spread of teal dots lights up. | the line | Slide it left, and we catch every attack. But we block half our users. |
| 4 | Slide right | 7 | The line slides to 0.85. Caught 21/50, blocked 28. Attack dots go dark left of the line. | the line | Slide it right, and almost nobody gets blocked. But half the attacks get through. |
| 5 | Every box is a point | 12 | The line glides back across all five stops. At each stop, the box's two numbers fly down and become a dot on the ROC axes (TPR up, FPR across). Then the full curve sweeps in through every threshold. | the ROC dots, then the curve | As you change the classification threshold, you change your predictions, and therefore your confusion matrix. Each one is a point: true positive rate up, false positive rate across. |
| 6 | Read it | 8 | The top-left corner glows. The dashed diagonal gets the label "coin flip". | the top-left corner | Top left is the sweet spot. It maxes the true positive rate and minimizes the false positive rate. The diagonal is a coin flip. |
| 7 | Takeaway | 6 | The line settles at 0.70, and its ROC dot pulses on the curve. Still frame. | the 0.70 dot | Where you stop depends on your goal: avoid false positives, or get all the positives. ROC is for picking thresholds. |

Total ≈ 55 s before tightening. If the take is long, beat 4's second
sentence goes first.

## Read-aloud script

You can change what your classifier does without retraining it. Just move
this line. That's what an ROC curve is about.

The model doesn't say yes or no. It gives every request a score. The
threshold turns that score into a yes.

Slide it left, and we catch every attack. But we block half our users.

Slide it right, and almost nobody gets blocked. *(if time:)* But half the
attacks get through.

As you change the classification threshold, you change your predictions,
and therefore your confusion matrix. Each one is a point: true positive
rate up, false positive rate across.

Top left is the sweet spot. It maxes the true positive rate and minimizes
the false positive rate. The diagonal is a coin flip.

Where you stop depends on your goal: avoid false positives, or get all the
positives. ROC is for picking thresholds.

## Not in this Short (on purpose)

AUC (ep 4). Precision on the curve (ep 4). "Specificity": your journal
said "recall vs specificity", but the axis is FPR = 1 − specificity, so
the VO only says "false positive rate". Put the specificity relationship
in the description.

## Title and description (draft)

- Title options: "ROC Curve Explained: Every Threshold at Once" · "ROC
  Curve Explained in 60 Seconds"
- Description: TPR = recall, FPR = FP / all negatives = 1 − specificity,
  and "Part 3 of 5. Next: ROC AUC vs PR AUC."
