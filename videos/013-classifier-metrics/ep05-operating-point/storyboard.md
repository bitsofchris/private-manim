ENGINE: mixed

# F1 score explained, and picking the threshold (series ep 5 of 5): storyboard (v1, pre-VO)

THE QUESTION: "What is the F1 score, and should I maximize it?"
WHO IS ASKING: someone with a decent curve who now has to ship one number
and was told to "use F1."
THE ANSWER IN ONE SENTENCE: F1 is the harmonic mean of precision and
recall, so it treats a blocked user and a missed attack as equally bad.
Usually they aren't, so write down what each mistake costs and set the
threshold there.
THE SEARCH PHRASE: f1 score explained (checked 10/16).

**One idea:** you don't ship a score, you ship a threshold, so choose it
by what a mistake costs.

Series context: `../SERIES.md`. The VO is a draft (the journal has no F1
lines), so put it in your own words.

## Ledger (from SERIES.md and `_data/ledger.json`)

- F1 example: **P 0.9, R 0.1 → average 0.5, F1 0.18.** Model A: **P 40%,
  R 80%, F1 0.53.**
- Costs: FP = **a real user blocked** (an annoyed user, a support ticket).
  FN = **an attack gets through** (a hijacked agent).
- Model B: **PR-AUC 0.689 vs Model A's 0.556.** To catch 40 attacks,
  **Model A flags 100, Model B flags 896.**
- Target: **at least 1 in 3 flags real, catching as many attacks as
  possible** → threshold **0.66**, **41 of 50 caught, 123 flags**.
- Code (sklearn, beat 6):
  `p, r, t = precision_recall_curve(y, scores)` ·
  `ok = p[:-1] >= 1/3` ·
  `t[ok][r[:-1][ok].argmax()]   # 0.66: 41 of 50 caught`

## The look

Opens on **two bars** (precision and recall) with two horizontal lines
across them: a dashed "average" and the magenta "F1". Beat 3 brings back
the score line with two **cost cards** above it, one per mistake, and the
threshold slides toward the side whose mistake is cheaper. Beat 4 is two
PR curves (A teal-outlined, B dim) with their areas and a vertical
"40 caught" marker, plus flag counts 100 and 896. Beat 6 is the code
card, with the line landing at 0.66 on the score line.

**Hero handoff:** the F1 line (1–2), the threshold (3), Model A's flag
count (4), the threshold at 0.66 (6).

## Beats

| # | Beat | ~s | Visual (9:16) | Hero | VO (draft) |
|---|------|---:|---|---|---|
| 1 | Hook | 6 | Frame 0: bars at 0.9 and 0.1. The dashed average sits at 0.5, and the magenta F1 line is already at 0.18. | the F1 line | The F1 score is precision and recall in one number, and it punishes whichever one is worse. |
| 2 | Why harmonic | 9 | The F1 line drops from 0.5 to 0.18 as the short bar pulses. The bars re-fill to Model A's 0.40 / 0.80, and F1 lands at 0.53. | the F1 line | Average 0.9 and 0.1, you get 0.5. F1 gives you 0.18. It's a harmonic mean, so it gets pulled toward the weaker one. Our model, 40 percent precision, 80 percent recall, scores 0.53. |
| 3 | What F1 assumes | 11 | The score line returns with the threshold at 0.70. Cost cards: "false positive: a user blocked" (small) and "false negative: an agent hijacked" (large). The threshold slides left, toward catching more. Small tag: "F-beta, β = 2: recall counts double". | the threshold | But F1 treats both mistakes the same. Here, a false positive blocks a real user. A false negative lets an attack hijack your agent. Those don't cost the same. *(if time:)* If misses cost more, F-beta with beta two counts recall double. |
| 4 | Best AUC can lose | 11 | Two PR curves. "PR AUC: A 0.56, B 0.69", and B's number glows. A vertical marker at "40 attacks caught": A shows **100 flags** and B shows **896 flags**. | A's 100 | Same with AUC. Model B has the bigger PR AUC. But to catch forty attacks, Model A flags a hundred. Model B flags eight hundred ninety-six. |
| 5 | Write the target | 7 | Text card: "≥ 1 in 3 flags real · catch as many as possible". | the target card | So write the target down: at least one in three flags real. |
| 6 | Code finds the line | 8 | The code card shows three lines. The output `0.66` lands, and the threshold on the score line glides to 0.66: "41 of 50 caught · 123 flags". | the threshold at 0.66 | Let the curve find the line: 0.66, forty-one of fifty caught. |
| 7 | Takeaway | 5 | The score line with the threshold at 0.66, and the cost cards at rest. Still frame. | none | You don't ship an AUC. You ship a threshold. Decide what a mistake costs, then put the line there. |

Total ≈ 57 s before tightening. If the take is long, the F-beta sentence
in beat 3 goes first.

## Read-aloud script

The F1 score is precision and recall in one number, and it punishes
whichever one is worse.

Average 0.9 and 0.1, you get 0.5. F1 gives you 0.18. It's a harmonic
mean, so it gets pulled toward the weaker one. Our model, 40 percent
precision, 80 percent recall, scores 0.53.

But F1 treats both mistakes the same. Here, a false positive blocks a real
user. A false negative lets an attack hijack your agent. Those don't cost
the same. *(if time:)* If misses cost more, F-beta with beta two counts
recall double.

Same with AUC. Model B has the bigger PR AUC. But to catch forty attacks,
Model A flags a hundred. Model B flags eight hundred ninety-six.

So write the target down: at least one in three flags real.

Let the curve find the line: 0.66, forty-one of fifty caught.

You don't ship an AUC. You ship a threshold. Decide what a mistake costs,
then put the line there.

## Not in this Short (on purpose)

These go in the description, not the VO. The trap: test at the real
attack rate. On a 50/50 test set, Model A's precision jumps from 40% to
about 99%. The noise point: with 50 positives, one case moves recall by 2
points, so report a bootstrap interval. Calibration (does 0.8 mean 80%?)
is a follow-up topic.

## Title and description (draft)

- Title options: "F1 Score Explained (and Why Not to Maximize It)" · "F1
  Score Explained: You Ship a Threshold, Not a Score"
- Description: the F1 and F-beta formulas, the test-at-real-prevalence
  trap, and "Part 5 of 5. The series: confusion matrix → precision vs
  recall → ROC curve → PR AUC vs ROC AUC → F1 and the threshold."
