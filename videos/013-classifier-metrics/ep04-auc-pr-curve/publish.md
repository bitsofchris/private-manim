# Publish: ROC AUC vs PR AUC, the precision-recall curve (series ep 4 of 5)

Search phrase: **precision recall curve explained** (SERIES.md "Search
phrases"; "pr auc vs roc auc" also autocompletes exactly, so it goes in
the title). Before publishing, glance at the results for the phrase to
check they're about ML.

## Title (pick one; first is recommended)

1. Precision Recall Curve Explained: PR AUC vs ROC AUC
2. Precision Recall Curve Explained (Beginner Friendly)

(1 is 51 characters; the search phrase is the first 32.)

## Description

Precision recall curve explained: a 0.985 ROC AUC can hide 233 blocked users. PR AUC shows them.

A prompt-injection detector sees 10,000 requests, and 50 are attacks. Its ROC AUC is 0.985: pick a random attack and a random user, and 98.5% of the time the attack scores higher. But at a 2.3% false positive rate it blocks 233 real users to catch 44 attacks, because the false positive rate divides by all 9,950 users. Precision doesn't use true negatives, so swap it in: recall across, precision up, and the same model's curve drops. On a PR plot a coin flip scores the attack rate (0.005), not 0.5, and this model's PR AUC is 0.556. In sklearn that's roc_auc_score vs average_precision_score.

One caveat: PR AUC isn't always the better number. It rewards getting the top of the list right, while ROC AUC weights every ranking mistake the same (McDermott et al., 2024). When positives are rare and false alarms are what you pay for, read the PR curve.

Part 4 of 5. Next: F1 and picking the threshold.

Sources:
Saito & Rehmsmeier (2015), The precision-recall plot is more informative than the ROC plot on imbalanced datasets: https://pmc.ncbi.nlm.nih.gov/articles/PMC4349800/
McDermott et al. (2024), A Closer Look at AUROC and AUPRC under Class Imbalance: https://arxiv.org/abs/2401.06091

Level up human.

#machinelearning #datascience #sklearn #classification #Shorts
