# Publish: Precision vs recall (Classifier Metrics, part 2 of 5)

Search phrase: **precision vs recall** (SERIES.md "Search phrases";
"precision and recall explained" also autocompletes; no dead phrases for
this one). Before publishing, glance at YouTube's results for it to check
they're about ML.

Final cut: `media/short.mp4`, 35.6 s.

## Title (pick one; first is recommended)

1. Precision vs Recall Made Simple
2. Precision vs Recall: Same 40, Two Denominators
3. Precision vs Recall, Explained in One Picture

The house form, "Precision vs Recall Made Simple (Beginner Friendly)", is
51 characters, one over the 50 limit, so (1) drops the suffix.

## Description

Precision vs recall: recall is how many attacks you caught; precision, how many flags were attacks.

A prompt-injection detector sees 10,000 requests, and 50 are attacks. It flags 100, and 40 of those are real attacks.
Recall = 40 / 50 = 80%: the attack column of the confusion matrix. Recall is about what you missed, the 10 attacks that got through. (Also called sensitivity, or the true positive rate.)
Precision = 40 / 100 = 40%: the flagged row. Precision is about what you wasted, the 60 real users you blocked.
Neither formula uses the 9,890 true negatives, which is why both still work when attacks are rare.

Part 2 of 5 on classifier metrics. Previous: confusion matrix explained. Next: ROC curve explained.
[POST LINK]

Level up human.

#machinelearning #precisionrecall #confusionmatrix #datascience #Shorts

## Checked against the final cut

Every on-screen claim above is in the Short: 10,000 requests and 50
attacks (the tag), the box TP 40 · FP 60 · FN 10 · TN 9,890, "recall 40 /
50 80%" and "precision 40 / 100 40%" (the fraction rows), FN renamed
"missed" and FP renamed "wasted", and the TN cell struck through. The VO
says "almost 10,000" true negatives; the description gives the ledger
value, 9,890.
