# ROC AUC vs PR AUC: the Precision-Recall Curve

`vo_raw.m4a`: 59.8 s, cut from `013-classifier metrics.m4a` at 197.50–257.25 s (episode announcement removed). Planned script: `../SCRIPTS.md`. Full take: `../TRANSCRIPT.md`.

## As recorded

This model's ROC area under the curve is 0.985, nearly perfect, but most of what it flags is wrong.

AUC is for comparing models. A coin flip is 0.5. You pick a random attack and a random user, and 98.5% of the time the attack scores higher. Now look at this point. False positive rate 2.3 percent. Sounds small. It's 233 real users blocked just to catch 44 attacks. So swap the false positive rate for precision. Precision doesn't use true negatives. Recall goes across, precision goes up, and the same model's curve drops. Now the good corner is top right. And the coin flip here isn't 0.5.

It's 0.005, the attack rate. This model's PR... This model's precision-recall area under the curve is 0.56. It's low looking, but over a hundred times better than chance. When positives are rare, we want to compare models on the precision-recall curve.

## Where the take leaves the script

- **Restart:** "This model's PR..." before the full line: cut the false start.
- "AUC is the area under the curve" not said; line 1 says "area under the curve" instead.
- 59.8 s raw: the random-pair line (if time) is the first cut if the tightened take runs long.
