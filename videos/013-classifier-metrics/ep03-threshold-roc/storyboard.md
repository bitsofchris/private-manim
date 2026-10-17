ENGINE: hyperframes

# ROC curve explained (series ep 3 of 5): storyboard (v2, recorded VO)

THE QUESTION: "What is an ROC curve?"
WHO IS ASKING: someone who has seen an ROC plot and doesn't know what a
point on it is.
THE ANSWER IN ONE SENTENCE: the model gives a score, and the threshold
turns it into a yes. Every threshold gives a different confusion matrix,
and the ROC curve plots all of them so you can pick your spot.
THE SEARCH PHRASE: roc curve explained (checked 10/16; "... machine
learning" also autocompletes; "classification threshold" is dead, keep it
out of the title).

**One idea:** move the line, and the box changes. The curve is every box.

**Engine:** HyperFrames for every beat (`AGENTS.md` "Which engine"). The
episode prompt says Manim for the ROC curve, and v1 left it open. The
reason for HyperFrames here: the threshold line, the box and the ROC dot
move together in almost every beat, and that link is the whole Short.
Split across engines, every frame would be two renders composited, and
seams would drift. The plot itself is two 0 → 1 axes, a dashed diagonal,
one polyline from `scores.npz` and a dot: no tick labels beyond 0 and 1,
no camera, nothing a canvas can't draw exactly. The canonical frame
(`00_layout/`) is where Chris checks that it reads as a real plot.

Series context: `../SERIES.md`. The VO is `script.md` (what Chris said),
not the planned script in `../SCRIPTS.md`.

## Ledger (copied from SERIES.md and `_data/ledger.json`; every beat uses exactly these)

- A **prompt-injection detector** in front of an AI agent. **10,000
  requests: 50 attacks, 9,950 real users.** Model A's scores, from
  `_data/scores.npz` (seed 13), model `a`.
- Frame-0 tag (SERIES.md "Context in every episode"): **prompt-injection
  detector · 10,000 requests · 50 attacks**.
- **Threshold stops for Model A** (caught / 50, users blocked, FPR):
  **0.20 → 50, 5,055, 51%** · **0.40 → 46, 1,141, 11.5%** ·
  **0.55 → 44, 233, 2.3%** · **0.70 → 40, 60, 0.6% (the ledger box:
  TP 40 · FP 60 · FN 10 · TN 9,890)** · **0.85 → 21, 28, 0.3%**.
  Full boxes (TP / FP / FN / TN): 0.20 → 50 / 5,055 / 0 / 4,895 ·
  0.40 → 46 / 1,141 / 4 / 8,809 · 0.55 → 44 / 233 / 6 / 9,717 ·
  0.70 → 40 / 60 / 10 / 9,890 · 0.85 → 21 / 28 / 29 / 9,922.
- Between stops the box counts come from the same dots (`s > t` on the
  scores in `_kit/dots.js`, which reproduce every stop exactly). Never a
  typed number.
- **TPR** = recall = caught / 50 (y, up). **FPR** = blocked users / 9,950
  (x, across). The ROC curve is every threshold of Model A's scores.
- "blocking most of our users" (VO) is the 0.20 stop: the visual shows
  **5,055** (51%), never a rounder number.
- "half of the attacks get through" (VO) is the 0.85 stop: **29 of 50**
  missed (FN 29).
- Box layout as in every episode: columns attack / user, rows flagged /
  not flagged; TP top-left, FP top-right, FN bottom-left, TN
  bottom-right.
- Code: `pred = scores > 0.70`, the number ticking with the line. One
  line, and it's the whole idea (move the line, no retraining).
- Model A ROC-AUC 0.985: not said and not shown (ep 4's hook).

## The look

Built on ep01's score-line kit, copied into `_kit/` (ep01's own kit is
still in use by its beats and is not touched).

- **Top, the score line**, exactly as ep01: the tag (y 240–372), the teal
  user pile above the axis and the gold attack dots below it (y 400–673),
  "0 · attack score · 1" (y 690–756). **The threshold** (magenta, the
  series hero) now *moves*: everything right of it is flagged and lit.
- **The code line** (beats 4–9), one 52 px monospace row under the axis
  labels: `pred = scores > 0.70`, the number following the line.
- **Bottom left, the box**: a compact 2×2 (headers "attack" / "user", the
  cell tags TP / FP / FN / TN, the counts), recounting live as the line
  moves.
- **Bottom right, the ROC plot**: square axes 0 → 1, "TPR" up and "FPR"
  across, a dashed diagonal (unlabelled; "coin flip" wasn't said), the
  curve in teal, and **the ROC dot** for the current threshold. The line
  and its dot are one hero group (magenta): move one, the other moves.

Hero handoff: the line + its dot (beats 1–2, 4–6, 9), the curve (3), the
five stop points (7), the top-left corner (8).

## Beats (VO from script.md, after the approved cuts; master times in `vo_final.wav`)

| # | Folder | Start | Length | VO (as recorded) | Visual (9:16) | Hero |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 3.00 | You can change what your classifier does without retraining it. | Frame 0, already working: every panel up, the line mid-slide (from ~0.55 toward 0.70), the box counts ticking, the ROC dot riding the curve. Lands on 0.70 by "retraining". | the line + dot |
| 2 | `02_move_line` | 3.00 | 2.06 | You just move this line. | "move this line": the line nudges (0.70 → ~0.62 → 0.70, ≥ 0.6 s each way), box and dot following. | the line + dot |
| 3 | `03_every_place` | 5.06 | 3.15 | An ROC curve shows every place that you could put it. | "ROC curve": the curve lights. "every place": the line sweeps right → left across the scores and back to 0.70, the dot tracing the whole curve. | the curve |
| 4 | `04_score` | 8.21 | 5.95 | The model doesn't say yes or no. It gives every request a score. And this threshold is what turns that score into a yes. | Line still at 0.70. "a score": one real attack dot right of the line gets a tag with its own score (2 dp, from `dots.js`). "this threshold": the line pulses. "into a yes": the code line fades in, `pred = scores > 0.70`, and the tagged dot rings as flagged. | the line, then `> 0.70` |
| 5 | `05_slide_left` | 14.16 | 4.55 | You slide it to the left and we can catch every attack. But we end up blocking most of our users. | "slide it to the left": the line slides to 0.20 (≥ 1 s), the code ticks to 0.20, the box recounts, the dot climbs to (0.51, 1). "every attack": TP 50 pulses. "most of our users": FP 5,055 pulses; the teal pile lights up to the line. | the line + dot |
| 6 | `06_slide_right` | 18.71 | 4.20 | If you slide it to the right, almost nobody gets blocked, but half of the attacks get through. | "slide it to the right": to 0.85 (≥ 1 s), code 0.85, box recounts, the dot drops to (0.003, 0.42). "nobody gets blocked": FP 28 pulses. "half of the attacks": FN 29 pulses, the unflagged gold dots left of the line ring. | the line + dot |
| 7 | `07_each_point` | 22.91 | 7.50 | Every threshold gives a new confusion matrix, and each one is a point. The true positive rate up, false positive rate across. | The curve dims. "Every threshold": the line steps through the five stops (0.20, 0.40, 0.55, 0.70, 0.85), the box recounting at each. "each one is a point": from there each stop leaves a magenta point on the plot. "true positive rate up": the TPR label and a vertical guide from the current point to the x-axis light. "false positive rate across": the FPR label. Then the curve comes back up through the points. | the stop points |
| 8 | `08_sweet_spot` | 30.41 | 1.90 | Top left is the sweet spot. | The points and the line go to rest; the top-left corner (0, 1) glows. | the corner |
| 9 | `09_takeaway` | 32.31 | 8.35 | Now ROC is for picking thresholds. You decide whether you'd rather avoid false positives or get all the positives depending on the problem you're solving. | Corner fades. "picking thresholds": the line and dot take the hero back. "avoid false positives": the line slides right toward 0.85 (FP falls). "get all the positives": left toward 0.20 (TP 50). "problem you're solving": it settles at 0.70, the ledger box. Still for the last ~1 s. | the line + dot |

Total 40.66 s (`vo_final.wav`). The contract for the beats; `BRIEF.md`'s table is the
pre-change version (beat 2 was 3.50 s with the context line; every later beat
starts 1.44 s earlier, its local cues unchanged).

## Cut list (approved by Chris, 10/17; applied)

Raw take 45.3 s → context line spliced in → 46.9 s → **42.1 s**.

| # | Edit | Range (vo_clean s) | Effect | Why |
|---|---|---|---:|---|
| 1 | Splice `../vo_context_short.m4a` ("It's a prompt injection detector.") after VO line 1 | at raw 2.78, in the pause after "retraining it." | +1.65 s | SERIES.md "Context in every episode". After sentence 1, not after "move this line": then "put it" in the next sentence still means the line |
| 2 | Pauses capped at 0.25 s (`--noise=-45dB`, as ep01) | whole take | −2.2 s | |
| 3 | The misspoken "false" in "get all the ~~false~~ positives" | 44.47–44.755, rejoined with a 30 ms gap | −0.3 s | script.md flags it. Cut at the dip before the f and inside the p's closure; Parakeet re-hears "get all the positives depending on…" |
| 4 | 1.4 s of room tone left as its own piece in the 3.6 s pause after "sweet spot" | 35.6–38.8 | −1.4 s | dead air; the pause there is set to 0.45 s so "sweet spot" lands before the closer |

Kept on purpose:
- "Now ROC is for picking thresholds." "Now" runs into "ROC" with no dip,
  so it can't be cut cleanly; it's 0.15 s.
- The closer keeps the decision ("you decide…"): it's the viewer's next
  move, which the runbook wants as the last line.
- "most of our users": the ledger's 0.20 stop blocks 51%. The visual
  shows 5,055 of 9,950, so the screen is exact even where the VO rounds.

After the first full cut Chris removed edit 1 (10/17): the context line is out,
so the Short is 40.66 s. The frame-0 tag still names the detector on screen.

If the "false" splice sounds wrong to Chris: end on "…for picking
thresholds." (−6 s, 36.1 s total), losing the closer.

## Not in this Short (on purpose)

AUC (ep 4). Precision on the curve (ep 4). "Specificity": the axis is
FPR = 1 − specificity, so the VO only says "false positive rate"; the
relationship goes in the description. The diagonal as "coin flip" (not
said; the dashed diagonal stays, unlabelled).
