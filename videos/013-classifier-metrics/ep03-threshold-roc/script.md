# ROC Curve Explained

`vo_raw.m4a`: 45.3 s, cut from `013-classifier metrics.m4a` at 143.25–188.50 s (episode announcement removed). Planned script: `../SCRIPTS.md`. Full take: `../TRANSCRIPT.md`.

## As recorded

You can change what your classifier does without retraining it. You just move this line. An ROC curve shows every place that you could put it. The model doesn't say yes or no. It gives every request a score, and this threshold is what turns that score into a yes. You slide it to the left, and we can catch every attack, but we end up blocking most of our users. If you slide it to the right, almost nobody gets blocked, but half of the attacks get through. Every threshold gives a new confusion matrix, and each one is a point, the true positive rate up, false positive rate across.

Top left is the sweet spot.

Now ROC is for picking thresholds. You decide whether you'd rather avoid false positives or get all the false positives depending on the problem you're solving.

## Where the take leaves the script

- **Misspoken closer:** "get all the false positives" should be "get all the positives". Needs a cut (end on "…for picking thresholds") or a pickup line.
- "blocking most of our users": the ledger's left stop (0.20) blocks 51%, so the visual should show about half.
- "The diagonal is a coin flip" (if time) not said.
