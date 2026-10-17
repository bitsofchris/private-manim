# Publish: ROC curve explained (series ep 3 of 5)

Search phrase: **roc curve explained** (SERIES.md "Search phrases";
"roc curve explained machine learning" also autocompletes). Dead phrase,
kept out: "classification threshold". "roc curve" alone pulls in
medical/USMLE results, so the title says machine learning.

## Title (pick one; first is recommended)

1. ROC Curve Explained (Machine Learning)
2. ROC Curve Explained Made Simple (Beginner Friendly)
3. ROC Curve Explained: Every Threshold at Once

## Description

ROC curve explained: every threshold gives a new confusion matrix, and the ROC curve plots them all.

A prompt-injection detector scores 10,000 requests, 50 of them attacks. The model doesn't say yes or no; the threshold turns its score into a yes, so you can change what it does without retraining (pred = scores > 0.70). Slide the line left to 0.20 and it catches all 50 attacks but blocks 5,055 real users. Slide it right to 0.85 and it blocks 28, but misses 29 attacks.

Each threshold is one point: true positive rate (recall, caught / 50) up, false positive rate (blocked users / all 9,950 users, which is 1 − specificity) across. Top left is the sweet spot. Where you stop depends on which mistake costs you more.

Part 3 of 5. Next: ROC AUC vs PR AUC.
[POST LINK]

Level up human.

#roccurve #machinelearning #classification #datascience #Shorts
