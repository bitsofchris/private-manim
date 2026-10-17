# Publish: Confusion matrix explained (Classifier Metrics, part 1 of 5)

Search phrase: **confusion matrix explained** (SERIES.md "Search phrases";
"imbalanced dataset" also autocompletes, so it's in the title and tags;
"accuracy imbalanced" is dead and stays out). Before publishing, glance at
YouTube's results for it to check they're about ML.

Final cut: `media/short.mp4`, 34.1 s.

## Title (pick one; first is recommended)

1. Confusion Matrix Explained (Imbalanced Dataset)
2. Confusion Matrix Explained: Why Accuracy Lies
3. Confusion Matrix Explained in 30 Seconds

The house form, "Confusion Matrix Explained Made Simple (Beginner
Friendly)", is 59 characters, over the 50 limit. (1) is 47 and carries
the second phrase that autocompletes.

## Description

Confusion matrix explained: when attacks are rare, accuracy is mostly true negatives.

A prompt-injection detector sees 10,000 requests, and only 50 are attacks. A real model catches 40 of the 50, and its accuracy goes down, from 99.5% to 99.3%.
The confusion matrix counts four boxes instead: true positives 40, false positives 60 (real users blocked), false negatives 10 (attacks that got through), true negatives 9,890.
9,890 of the 9,930 correct answers are true negatives, the easy ones. With rare positives, read the box, not the accuracy.

Part 1 of 5 on classifier metrics. Next: precision vs recall.
[POST LINK]

Level up human.

#machinelearning #confusionmatrix #imbalanceddataset #datascience #Shorts

## Checked against the final cut

Every on-screen claim above is in the Short: 10,000 requests and 50
attacks (the frame-0 tag), the counter at 99.5% ticking down to 99.3%,
"attacks caught 40 / 50", the box TP 40 · FP 60 · FN 10 · TN 9,890 with
rows flagged / not flagged and columns attack / real user, and "of 9,930"
under the swollen TN cell. "Real users blocked" and "attacks that got
through" are SERIES.md's meanings of FP and FN; the VO says them as "it
was a real user" and "I said user, but it was an attack".
