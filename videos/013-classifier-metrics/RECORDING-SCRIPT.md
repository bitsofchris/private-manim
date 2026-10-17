# Recording script: all five episodes (v2, 2026-10-17)

Read each episode as its own take, with a pause of a few seconds between episodes. *(if time:)* lines are optional: read them, and they get cut at tighten if the take runs long. Save as `epNN-*/vo_raw.m4a` per episode, or as one file at the series root (`vo_raw_all.m4a`), and Claude will split it at the pauses.

---

## Confusion matrix explained: the accuracy trap (series ep 1 of 5)

*133 words, ~53s*

This model is 99.5% accurate, and it has never caught a single attack.
The confusion matrix shows why.

It's a prompt-injection detector. Ten thousand requests come in, and only
fifty are attacks. Never flag anything, and you're right 99.5% of the
time.

Here's a real model. It flags a hundred requests and catches forty of the
fifty attacks. Its accuracy goes down, to 99.3%.

So count four boxes instead. True positive: I said attack, and it was.
False positive: I said attack, and it was a real user. False negative: I
said user, and it was an attack. True negative: I said user, and it was.

Look where the accuracy comes from. Almost all of it is true negatives,
the easy ones.

With rare positives, don't read the accuracy. Read the four boxes.

---

## Precision vs recall (series ep 2 of 5)

*107 words, ~42s*

Precision versus recall comes down to one thing: the same forty catches,
divided by two different numbers.

Recall: of all the positives, how many did I catch? There were fifty
attacks. We caught forty. Recall is eighty percent.

Precision: of the ones I predicted positive, how many actually were? We
flagged a hundred. Forty were attacks. Precision is forty percent.

Recall is about what you missed: attacks that got through. Precision is
about what you wasted: real users you blocked.

Neither one uses the true negatives, almost ten thousand of them. That's
why they still work when attacks are rare.

Two questions. Two denominators. You need both.

---

## ROC curve explained (series ep 3 of 5)

*123 words, ~49s (117 without the if-time line)*

You can change what your classifier does without retraining it. Just move
this line. An ROC curve shows every place you could put it.

The model doesn't say yes or no. It gives every request a score. The
threshold turns that score into a yes.

Slide it left, and we catch every attack. But we block half our users.

Slide it right, and almost nobody gets blocked. *(if time:)* But half the
attacks get through.

Every threshold gives a new confusion matrix, and each one is a point:
true positive rate up, false positive rate across.

Top left is the sweet spot. The diagonal is a coin flip.

ROC is for picking thresholds: decide whether you'd rather avoid false
positives, or get all the positives.

---

## ROC AUC vs PR AUC: the precision-recall curve (series ep 4 of 5)

*139 words, ~55s*

This model's ROC AUC is 0.985. Nearly perfect. And most of what it flags
is wrong.

AUC is the area under the curve. It's for comparing models. Pick a random
attack and a random user, and 98.5% of the time the attack scores higher.
A coin flip is 0.5.

Now look at this point. False positive rate, 2.3 percent. Sounds small.
It's 233 real users blocked, to catch 44 attacks.

So swap the false positive rate for precision. Precision doesn't use true
negatives. Recall goes across, precision goes up, and the same model's
curve drops. Now the good corner is top right.

And a coin flip here isn't 0.5. It's 0.005, the attack rate. This model's
PR AUC is 0.56. Low-looking, but over a hundred times better than chance.

When positives are rare, compare models on the precision-recall curve.

---

## F1 score explained, and picking the threshold (series ep 5 of 5)

*149 words, ~59s (138 without the if-time line)*

The F1 score is precision and recall in one number, and it punishes
whichever one is worse.

Average 0.9 and 0.1, you get 0.5. F1 gives you 0.18. It's a harmonic
mean. Our model, 40 percent precision, 80 percent recall, scores 0.53.

But F1 treats both mistakes the same, and here they aren't. A false
positive blocks a real user, who can try again. A false negative lets an
attack hijack your agent and leak your data. *(if time:)* If misses cost
more, F-beta with beta two counts recall double.

So say we'll accept two blocked users for every attack we stop. That
means at least one flag in three has to be a real attack.

Now move the line down as far as that allows: forty-one of fifty attacks
caught.

You don't ship an F1 score. You ship a threshold. Decide what a mistake
costs, then put the line there.
