ENGINE: hyperframes

# ROC AUC vs PR AUC: the precision-recall curve (series ep 4 of 5): storyboard (v2, recorded VO)

THE QUESTION: "ROC AUC or PR AUC for imbalanced data?"
WHO IS ASKING: someone whose model has a great AUC but whose flags are
mostly wrong.
THE ANSWER IN ONE SENTENCE: AUC turns the curve into one number for
comparing models, but when positives are rare a tiny false positive rate
can still be hundreds of blocked users, and only the precision-recall
curve shows that.
THE SEARCH PHRASE: precision recall curve explained (checked 10/16).
"pr auc vs roc auc" also autocompletes exactly, so put it in the title.

**One idea:** the false positive rate divides by 9,950, so it hides the
blocked users. Precision doesn't.

**Engine: HyperFrames for every beat** (`AGENTS.md` "Which engine"). v1
said mixed, with Manim for the plots. Every beat of this episode has the
plot on screen *and* the series score line above it, so mixed would mean
an engine seam at every cut or the ep01 score line rebuilt in Manim. The
plot is drawn on the canvas from the real curve (sklearn `roc_curve` /
`precision_recall_curve` on `_data/scores.npz`, model `a`), with real 0–1
axes and ticks, and the ROC → PR morph is per-point interpolation, so
every point keeps its identity. Same kit as ep01's score line, so the
look matches the series. Chris confirms at the `00_layout` check.

Series context: `../SERIES.md` (ledger, images, Chris's words). The VO is
`script.md` (what Chris said), not the planned script in `../SCRIPTS.md`.

## Ledger (copied from SERIES.md and `_data/ledger.json`; every beat uses exactly these)

- A **prompt-injection detector** in front of an AI agent. **10,000
  requests: 50 attacks, 9,950 real users.** Attack rate **0.005** (0.5%).
- Model A (dots from `_data/scores.npz`, seed 13, model `a`):
  **ROC-AUC 0.985**, **PR-AUC (average precision) 0.556**.
- The AUC reading: the chance a random attack scores above a random
  user. For Model A, **98.5%**. Coin flip: ROC **0.5**.
- Model A at its ledger threshold **0.70**: flags **100**, **40** are
  attacks, **60** are real users (precision 40%). "Most of what it flags
  is wrong" = 60 of 100.
- The point (ep 4): threshold **0.55**: **FPR 2.3%** (233 / 9,950),
  **44 of 50 caught** (recall 88%), **233 users blocked**, precision
  **16%** (44 / 277). On the PR plot it sits at (0.88, 0.16).
- PR coin flip: **0.005** (the attack rate), not 0.5. 0.556 / 0.005 ≈
  **111×**, said as "over a hundred times better than chance".
- Frame-0 tag (SERIES.md "Context in every episode"): **prompt-injection
  detector · 10,000 requests · 50 attacks**.
- Code (sklearn, beat 8): `roc_auc_score(y, s)` → `0.985` ·
  `average_precision_score(y, s)` → `0.556`.

## The look

Two stacked images, top and bottom of the stage (captions anchored
bottom, so the stage runs to y 1330):

- **Top, the score line** (ep01's series image, a little shorter): tag
  y 240–372, teal user pile above the axis, gold attack pile below it,
  "0 · attack score · 1" under it, down to y ~680. The magenta threshold
  sits at **0.70** in beat 1 and moves to **0.55** in beat 4. Flagged
  dots (right of the line) ring.
- **Bottom, the plot** y ~700–1320: a 0–1 by 0–1 box with ticks at 0 and
  1, the y-axis name above it on the left, the x-axis name below it.
  ROC: x **false positive rate**, y **true positive rate**. The ROC curve
  is teal at rest and hugs the top-left; its area fills on "area under the
  curve". The point for the current threshold is a dot on the curve, so
  the line on the score line and the point on the curve always agree.
- **The morph (beat 5):** each point slides from (FPR, TPR) to (recall,
  precision). The y label "true positive rate" becomes "recall" and slides
  to the x axis (TPR *is* recall); "false positive rate" becomes
  "precision" and slides to the y axis. The curve sags to the bottom; the
  good corner moves from top left to top right.
- **Numbers on the plot** (AUC readouts, the 233 / 44 count, the
  baselines) sit in the plot's empty corner: bottom right for ROC, top
  right for PR.
- **Code card (beat 8)** takes the score line's place at the top; the PR
  plot stays below it.

**Hero handoff (one magenta thing at a time):** the ROC area (1) → the
threshold (1, on "flags") → the area (3) → the threshold and its point
(4) → the PR curve (5) → the baseline (6) → the PR area (7) → the code
card's lit line (8).

## Beats (VO from script.md; times from the trial cut, finals after approval)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook | This model's ROC area under the curve is 0.985, nearly perfect, but most of what it flags is wrong. | Frame 0, already working: tag + score line on top (threshold at 0.70, its 100 flagged dots ringed), the ROC curve below with its area filled and **ROC AUC 0.985** in the bottom-right corner. "nearly perfect": the area glows. "most of what it flags": the 60 teal dots right of the line brighten, and "60 of 100 flags are real users" lands under the AUC. | the area, then the threshold |
| 2 | Context (spliced) | It's a prompt injection detector. | The tag brightens and settles. Nothing else moves. | none |
| 3 | What AUC is | AUC is for comparing models. A coin flip is 0.5. You pick a random attack and a random user, and 98.5% of the time the attack scores higher. | "comparing models": the AUC readout pulses. "coin flip": the dashed diagonal draws, its triangle labelled **0.5**. "random attack … random user": one gold dot and one teal dot on the score line ring, the gold one to the right. "98.5%": "98.5% of pairs" under the readout. | the area |
| 4 | Count the point | Now look at this point. False positive rate 2.3 percent. Sounds small. It's 233 real users blocked just to catch 44 attacks. | "this point": the threshold slides 0.70 → 0.55 (≥ 1 s) and the point runs down the curve with it, then rings. "2.3 percent": "FPR 2.3%" by the point. "233 real users": the 233 teal dots right of the line light; "233 blocked" in the corner. "44 attacks": "44 caught" under it. | the threshold and its point |
| 5 | Swap the axis | So swap the false positive rate for precision. Precision doesn't use true negatives. Recall goes across, precision goes up, and the same model's curve drops. Now the good corner is top right. | "swap": "false positive rate" turns into "precision". "doesn't use true negatives": the teal pile left of the line dims. "Recall goes across": the y label becomes "recall" and slides to the x axis. "precision goes up": "precision" slides to the y axis. "curve drops": every point slides to (recall, precision), ≥ 1.5 s; the 0.55 point lands at (0.88, 0.16). "top right": the corner glows. | the PR curve |
| 6 | The baseline | And the coin flip here isn't 0.5. It's 0.005, the attack rate. | "isn't 0.5": a dashed line at precision 0.5 labelled **0.5**. "0.005": it drops to the floor, labelled **0.005 = attack rate**. | the baseline |
| 7 | PR AUC | This model's precision-recall area under the curve is 0.56. It's low looking, but over a hundred times better than chance. | "area under the curve": the PR area fills (step-wise, as average precision is). "0.56": **PR AUC 0.556** in the top-right corner. "hundred times": "≈ 111× the coin flip" under it. | the PR area |
| 8 | Takeaway | When positives are rare, we want to compare models on the precision-recall curve. | "rare": the 50 gold dots pulse once. Then the score line gives way to the code card: `roc_auc_score(y, s)` → `0.985`, `average_precision_score(y, s)` → `0.556`, the second line lit. Still for the last ~1 s. | the code card's lit line |

## Not in this Short (on purpose)

The McDermott et al. (2024) caveat goes in the description: PR-AUC isn't
always better. It rewards the top of the list, while ROC-AUC weights
every ranking mistake the same, which is fairer across groups with
different base rates. Also left out: the step-wise vs trapezoid AP
detail, Davis & Goadrich, and Model B (ep 5).
