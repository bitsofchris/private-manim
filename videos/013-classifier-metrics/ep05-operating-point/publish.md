# Publish: F1 score explained (Classifier Metrics, part 5 of 5)

Search phrase: **f1 score explained** (SERIES.md "Search phrases"; "f1
score vs accuracy" and "precision recall tradeoff" also autocomplete;
"how to choose threshold" and "optimal threshold" are dead and stay out).
Before publishing, glance at YouTube's results for it to check they're
about ML ("f1 score" alone pulls in the movie soundtrack).

Final cut: `media/short.mp4`, 44.1 s.

## Title (pick one; first is recommended)

1. F1 Score Explained Made Simple (Beginner Friendly)
2. F1 Score Explained: Ship a Threshold, Not a Score
3. F1 Score Explained (and Why Not to Maximize It)

(1) is the house form at exactly 50 characters. (2) is 49 and carries the
takeaway; (3) is 47 and answers "should I maximize it?".

## Description

F1 score explained: precision and recall in one number, and it punishes whichever is worse.

F1 = 2·P·R / (P + R), a harmonic mean. Precision 0.9 and recall 0.1 average to 0.5, but F1 is 0.18.
On a prompt-injection detector (10,000 requests, 50 attacks), our model has 40% precision and 80% recall: F1 0.53.
But F1 treats both mistakes the same. A false positive blocks a real user, who can try again. A false negative lets an attack hijack your agent.
So set a target from the costs: accept two blocked users per attack stopped, so at least 1 flag in 3 must be real. Move the threshold down as far as that allows (0.70 → 0.66): 41 of 50 attacks caught, 123 flags, 41 of them real.
If misses cost more than false alarms, F-beta with β = 2 counts recall twice as much as precision.
One trap: test at the real attack rate. On a 50/50 test set, the same model's precision at its threshold jumps from 40% to about 99%.

Part 5 of 5 on classifier metrics: confusion matrix explained → precision vs recall → ROC curve explained → precision recall curve explained → F1 score explained.
[POST LINK]

Level up human.

#machinelearning #f1score #precisionrecall #datascience #Shorts

## Checked against the final cut

On screen: the frame-0 tag (prompt-injection detector · 10,000 requests ·
50 attacks); bars precision 0.9 / recall 0.1 with "mean 0.5" and
"F1 0.18"; the formula F1 = 2·P·R / (P + R) and 2·0.9·0.1 / (0.9 + 0.1)
= 0.18 under "harmonic mean"; the bars at 40% / 80% and "F1 0.53"; the
cost cards (false positive: real user blocked, can try again; false
negative: agent hijacked, data leaked); "2 blocked : 1 stopped", "at
least 1 flag in 3 is a real attack"; the readout from "caught 40 / 50,
100 flags, 40 real" to "caught 41 / 50, 123 flags, 41 real" as the line
moves. Not on screen, and the description doesn't claim it is: the
threshold values 0.70 and 0.66 (the ledger's; the exact cut is scores ≥
0.656), F-beta, and the 50/50 trap (SERIES.md: ep 5 description only).
