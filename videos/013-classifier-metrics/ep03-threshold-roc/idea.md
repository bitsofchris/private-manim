# Episode 3, the threshold and the ROC curve: idea

**State:** storyboarded 2026-10-16. `storyboard.md` is current, and where they differ it wins over this file (the numbers come from `_data/ledger.json`). The ledger, the images,
and Chris's words are in `../SERIES.md`.

## Preflight (phrase checked 10/16)

- **Question:** What is an ROC curve?
- **Who is asking:** someone who has seen an ROC plot and doesn't know
  what a point on it is.
- **Answer in one sentence:** the model gives a score, and the threshold
  turns it into a yes. Every threshold gives a different confusion
  matrix, and the ROC curve plots all of them so you can pick your spot.
- **Search phrase (checked 10/16):** roc curve explained (it also
  suggests "... machine learning"). "classification threshold" gets no
  suggestion, so leave it out of the title.

## Beats (sketch)

1. **Frame 0:** the score line, the box, and an empty TPR-vs-FPR plot
   side by side, with the line mid-slide. VO line 1: "You can change what
   your classifier does without retraining it. Just move this line."
2. Slide the line left. More gets flagged, recall climbs toward 50 / 50,
   and blocked users pile up. The box recounts.
3. Slide right. Fewer users get blocked, and attacks slip through.
4. Each stop drops a point at (FPR, TPR). FPR = blocked users / all 9,950
   users, and TPR is recall. The points trace the ROC curve. "As you
   change the classification threshold you change your predictions and
   therefore your confusion matrix."
5. The top-left corner glows: "maxes the true positive rate, minimizes the
   false positive rate." The diagonal is a coin flip. Where you stop
   "depends on your goal: avoid false positives or get all the
   positives."
6. Last line: "There's no single precision for a model, only precision at
   a threshold. ROC shows you every threshold at once."

## Code (fits, PyTorch)

```python
pred = scores > 0.7     # move the line: no retraining
```

One line, and it's the whole idea. Put it on screen during the slide,
with the number ticking.

## Open

- Engine for the plot: HyperFrames' 2D plane kit (`vec/`) or Manim axes.
  Decide at storyboard.
