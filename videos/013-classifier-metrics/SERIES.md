# Classifier Metrics: the series

**Name:** classifier-metrics-series
**Description:** Home base for five Shorts on how to score a classifier
when positives are rare: the accuracy trap and the confusion matrix,
precision and recall, the threshold and the ROC curve, AUC and the PR
curve, and choosing the operating point. Each episode adds one intuition
to the same 10,000 requests.
**When to use:** at the start of any session on this series. Take the
next unchecked episode, open its `epNN-slug/idea.md`, and run
`agents/runbook.md` from step 0 in that folder. Update the checklist in
the same pass as the work.
**How it works:** one contrived example, one confusion matrix, one
threshold line. No episode starts from scratch. Each one changes how you
read the same dots or what you do with them. Status: **scoped,
2026-10-16.** Agreed (Chris, 10/16):
- Five episodes, in this order. No merge.
- The story is a prompt-injection detector. It's contrived, purely for
  teaching, with no work angle and no "I hit this at work."
- Code on screen only where it really belongs. Prefer PyTorch, then
  sklearn. Don't force it.
- No learn-first step. Chris learns by explaining over the visuals, so
  recording is the learning pass.
- Recording is in series order, audio first (runbook).

**Vault pointer:** the scope and Chris's own definitions are in
`[[Classifier Metrics Series - Confusion Matrix, ROC]]`
(`~/Documents/ZK Home/OpenAugi/Plans/`). Its 2026-10-16 journal block is
Chris's words from StatQuest and a ChatGPT thread, so it can be cut into
VO.

## Who it is for

Engineers doing AI work, and anyone who now uses a classification model
(a guardrail, a filter, an eval judge) and wants the basics of scoring
one. They can read a little PyTorch. They have heard "precision",
"recall", and "AUC", but couldn't say which one to trust when positives
are rare.

## The promise

**When almost everything is negative, accuracy tells you nothing. Here's
what to count instead, which curve to use for picking a threshold and
which number for comparing models, and how to set the line by what a
mistake costs.**

## Ledger (identical in every episode; agents copy from here)

- **The story:** a **prompt-injection detector** in front of an AI agent.
  It scores every incoming request, and a high score means "this looks
  like an attack."
- **10,000 requests. 50 are injection attempts (0.5%). 9,950 are real
  users.**
- **Model A** flags 100 requests, and 40 of them are real attacks:

|  | Actually an attack | Actually a real user |
|---|---|---|
| **Flagged** | TP = 40 | FP = 60 |
| **Not flagged** | FN = 10 | TN = 9,890 |

- Accuracy 99.3% (9,930 / 10,000). "Never flag" gets **99.5%** and
  catches 0 of 50.
- Precision 40 / 100 = **40%**. Recall 40 / 50 = **80%**. FPR 60 / 9,950
  = **0.6%**. F1 = **0.53**.
- What each mistake means: **false positive = a real user gets blocked.
  False negative = an attack gets through and the agent is hijacked.**
- **Generated data:** `_data/make_scores.py` (seed 13) writes
  `scores.npz` and `ledger.json`. Every curve, point, and AUC comes from
  there. Never invent a number in a beat.
- **Threshold stops for Model A** (ep 3): 0.20 → caught 50/50, blocked
  5,055 users (FPR 51%) · 0.40 → 46/50, 1,141 (11.5%) · 0.55 → 44/50,
  233 (2.3%) · **0.70 → 40/50, 60 (0.6%), the ledger box** · 0.85 →
  21/50, 28 (0.3%).
- **AUCs** (eps 4–5): Model A ROC-AUC **0.985**, PR-AUC (average
  precision) **0.556**. Model B ROC-AUC 0.906, PR-AUC **0.689**. Coin
  flip: ROC 0.5, PR **0.005** (the attack rate).
- **Ep 4 point:** at threshold 0.55, FPR is **2.3%**, which means **233
  blocked users to catch 44 attacks**, so precision is **16%**.
- **Ep 5:** to catch 40 attacks, Model A flags **100** and Model B flags
  **896**. The threshold pick (most recall with at least 1 in 3 flags
  real) gives **0.66 → 41 of 50 caught, 123 flags**. The F1 example is P
  0.9, R 0.1 → average 0.5, **F1 0.18**. Model A's F1 is **0.53**.
- Trap (ep 5 description only): on a 50/50 test set, Model A's precision
  at its threshold goes from **40% to about 99%**.

### Chris's words (use in VO; cut and reorder, never reword)

From the vault journal, 2026-10-16:
- "True positive: what I correctly said is positive." "False positive: I
  wrongly predicted positive." "False negative: I wrongly said this was
  negative but it was positive."
- Precision: "of the ones I predicted positive, how many actually were?"
- Recall: "of all the positives, how many did I catch?"
- "As you change the classification threshold you change your
  classification predictions and therefore your confusion matrix."
- "ROC helps us identify the sweet spot threshold." "Top left: maxes the
  true positive rate, minimizes the false positive rate." "Depends on
  your goal: avoid false positives or get all the positives."
- "ROC for picking thresholds." "AUC: area under curve for comparing
  models."
- PR graph: "for imbalanced sets." "Precision doesn't use true
  negatives." "Now thresholds are top right."

Two fixes to that journal, so the VO says them correctly: ROC is TPR
against **FPR** (= 1 − specificity), not specificity, and the PR plot
puts **recall on x and precision on y**.

## The two recurring images

1. **The score line.** Every request is a dot on a 0 → 1 score axis.
   Real users make a big teal pile on the left with a long tail. The 50
   attacks sit toward the right, and some are inside the tail. **The
   threshold is a vertical line (the magenta hero), and everything to its
   right is flagged.** This is the series image, and frame 0 of ep 1.
2. **The 2×2 box**, which recounts itself every time the line moves. One
   threshold gives one box. Slide the line and you get a curve (eps 3–4).

The attacks need a second accent color, and the user dots stay teal at
rest. The engine is decided per beat at storyboard time: HyperFrames by
default, Manim if the ROC/PR plots need real plotted axes.

## Context in every episode (Chris, 10/17)

Each Short is found on its own, so eps 2–5 say what the model is, the
same way ep 1 does:

- **VO:** splice ep 1's own line in right after VO line 1 (never before
  it; the answer comes first). Both clips are from the one take, so tone
  and level match:
  - `vo_context_short.m4a` (1.65 s): "It's a prompt injection detector."
    Eps 3–5.
  - `vo_context_long.m4a` (4.15 s): "…10,000 requests come in, but only
    50 are attacks." Ep 2, which opens on "50 attacks" with no setup.
  Ep 4's raw take is 59.8 s, so it pays for the splice with a cut (the
  random-pair line first).
- **On screen:** frame 0 of every episode labels the score line with a
  short tag, "prompt-injection detector · 10,000 requests · 50 attacks",
  so muted viewers have it too.


| # | Folder | Question (viewer's words) | The viewer leaves able to say |
|---|---|---|---|
| 1 | `ep01-accuracy-trap` | Why is my 99.5% accurate model useless? | "Never flag" scores 99.5% and catches zero attacks. When positives are rare, accuracy mostly counts true negatives. |
| 2 | `ep02-precision-recall` | What's the difference between precision and recall? | Precision: of my flags, how many were attacks? Recall: of the attacks, how many did I catch? Neither formula uses true negatives. |
| 3 | `ep03-threshold-roc` | What is an ROC curve? | The model outputs a score, and the threshold turns it into a yes. Every threshold is a new confusion matrix. ROC plots all of them so you can pick the spot. |
| 4 | `ep04-auc-pr-curve` | ROC AUC vs PR AUC, which one for imbalanced data? | AUC turns the curve into one number for comparing models. With rare positives, FPR hides the false alarms, and the PR curve shows them. |
| 5 | `ep05-operating-point` | What is the F1 score, and should I maximize it? | F1 treats a blocked user and a missed attack as equally bad. You ship one threshold, so set it by what each mistake costs. |

## Search phrases (checked in YouTube autocomplete, 2026-10-16)

| # | Phrase | Also autocompletes | Dead (keep out of titles) |
|---|---|---|---|
| 1 | confusion matrix explained | imbalanced dataset | accuracy imbalanced |
| 2 | precision vs recall | precision and recall explained | none |
| 3 | roc curve explained | roc curve explained machine learning | classification threshold |
| 4 | precision recall curve explained | pr auc vs roc auc, roc auc vs pr auc | none |
| 5 | f1 score explained | f1 score vs accuracy, precision recall tradeoff | how to choose threshold, optimal threshold |

Autocomplete shows that people type a phrase, not how many do. Before
publishing each one, glance at the search results to make sure they're
about ML ("roc curve" alone pulls in medical/USMLE, and "f1 score" alone
pulls in the movie soundtrack).

## Checklist

All five are storyboarded (v1, 10/16) and recorded in one take (10/17, `TRANSCRIPT.md`), split into each folder's `vo_raw.m4a` + `script.md`. Build each with `EPISODE_PROMPT.md`, one session per folder.

- [ ] ep01: storyboard v1 → recorded → build
- [ ] ep02: storyboard v1 → recorded → build
- [ ] ep03: storyboard v1 → recorded → build
- [ ] ep04: storyboard v1 → recorded → build
- [ ] ep05: storyboard v1 → recorded → build
- [ ] optional: stitch 1–5 into one 16:9 explainer after all five ship

## Sources

- Saito & Rehmsmeier (2015), [The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets](https://pmc.ncbi.nlm.nih.gov/articles/PMC4349800/), PLOS ONE. Ep 4. *(read: abstract and summary)*
- McDermott et al. (2024), [A Closer Look at AUROC and AUPRC under Class Imbalance](https://arxiv.org/abs/2401.06091), NeurIPS. The ep 4 caveat. *(read: abstract and summary)*
- Davis & Goadrich (2006), "The relationship between precision-recall and ROC curves," ICML. Ep 4. *(not re-read)*
- Hanley & McNeil (1982), AUC = the chance a random positive outranks a random negative. Ep 4. *(standard result)*
- scikit-learn docs: `roc_curve`, `roc_auc_score`, `precision_recall_curve`, `average_precision_score` (step-wise, not trapezoid).
