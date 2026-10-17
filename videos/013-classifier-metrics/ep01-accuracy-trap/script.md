# Confusion Matrix Explained: the Accuracy Trap

`vo_raw.m4a`: 54.6 s, cut from `013-classifier metrics.m4a` at 7.55–62.10 s (episode announcement removed). Planned script: `../SCRIPTS.md`. Full take: `../TRANSCRIPT.md`.

## As recorded

This model is 99.5% accurate, but it's never caught a single attack. It's a prompt injection detector. 10,000 requests come in, but only 50 are attacks. It never flags anything, and you're still right 99.5% of the time. Now, here's your real model. It flags 100 requests and catches 40 of the 50 attacks, but its accuracy goes down to 99.3%.

So we look at the confusion matrix instead. A true positive is I said there was an attack, and it was genuinely an attack. A false positive is the model predicted attack, but it was a real user in this case. A false negative, I said user, but it was an attack. And a true negative, I said user, and it was a user, not an attack.

Now look where the accuracy comes from. Almost all of it is true negatives. These are the easy ones. When positives are rare, we don't want to read the accuracy. We want to look at the confusion matrix.

## Where the take leaves the script

- "The confusion matrix shows why" (line 2) not said; the matrix is named at the box definitions instead.
- "It never flags anything": the planned line is "Never flag anything". The VO says the model never flags, which conflicts with "here's your real model" flagging 100; worth a look at tighten.
- Box definitions run longer than planned ("genuinely an attack", "in this case", "a user, not an attack"): candidates for trimming.
- Closer is "look at the confusion matrix", not "read the four boxes".
