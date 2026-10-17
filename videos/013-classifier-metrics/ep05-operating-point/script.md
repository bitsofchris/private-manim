# F1 Score Explained, and Picking the Threshold

`vo_raw.m4a`: 44.9 s, cut from `013-classifier metrics.m4a` at 263.90–308.75 s (episode announcement removed). Planned script: `../SCRIPTS.md`. Full take: `../TRANSCRIPT.md`.

## As recorded

The F1 score is precision and recall in one number, and it punishes whichever is worse. Average 0.9 and 0.1 and you get 0.5. F1 will give you 0.18. It's a harmonic mean. Our model, 40 percent precision, 80 percent recall, scores 0.53.

But F1 treats both mistakes the same, and here they aren't. A false positive blocks a real user who can try again. A false negative would let an attack hijack your agent and leak your data.

So say we'll accept two blocked users for every attack we stop. That means at least one flag in three has to be a real attack. Now move the line down as far as that allows, 41 of 50 attacks caught. You don't ship an F1 score, you ship a threshold. Decide what a mistake costs and then put the line there.

## Where the take leaves the script

- The F-beta line (if time) not said.
- Clean take otherwise; at 44.9 s there is room to keep the 0.53 line.
