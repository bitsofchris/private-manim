# Episode 4, AUC and the PR curve: idea

**State:** storyboarded 2026-10-16. `storyboard.md` is current, and where they differ it wins over this file (the numbers come from `_data/ledger.json`). The ledger, the images,
and Chris's words are in `../SERIES.md`. This is the densest episode, so
cut hard at step 5.

## Preflight (phrase checked 10/16)

- **Question:** ROC AUC or PR AUC for imbalanced data?
- **Who is asking:** someone whose model has a great AUC but whose flags
  are mostly wrong.
- **Answer in one sentence:** AUC turns the curve into one number for
  comparing models, but with rare positives a 1% false-positive rate is
  still 100 blocked users, and only the precision-recall curve shows
  that.
- **Search phrase (checked 10/16):** precision recall curve explained
  (the broader phrase). "pr auc vs roc auc" and "roc auc vs pr auc" both
  autocomplete exactly, so put one in the title.

## Beats (sketch)

1. **Frame 0:** the ROC curve from ep 3 with a point lit at FPR 1%, TPR
   80%, which looks excellent. VO line 1: "A 1% false positive rate sounds
   great, until you count the people."
2. **AUC:** shade the area. It's one number per model for comparing
   models. A literal reading: grab one attack dot and one user dot, and
   AUC is the chance the attack scores higher. Coin flip is 0.5.
3. **Count it:** 1% of 9,950 users is about **100 blocked**, next to 40
   caught. Precision is **29%**. FPR divides by 9,950, so it hides them.
4. **Swap the axis:** FPR becomes precision ("precision doesn't use true
   negatives"), and recall stays. Recall goes on x and precision on y. Same
   model, same slide, and the curve now sits low. The good corner moves to
   the top right.
5. The baseline line: a coin flip on the PR plot is **0.005** (the attack
   rate), not 0.5.
6. Last line: "ROC to compare rankings, PR when the positives are rare
   and false alarms are what you pay for."

## Code (optional, sklearn)

```python
roc_auc_score(y, scores)            # looks great
average_precision_score(y, scores)  # tells the truth here
```

Use it only if it lands as the payoff. Don't force it.

## Cut candidates if long

- The McDermott caveat (PR-AUC isn't always better: it rewards the top of
  the list, while AUROC treats every ranking error the same) goes to the
  description or a pinned comment, not the VO.
- The rebalanced-test-set trap moves to ep 5.
