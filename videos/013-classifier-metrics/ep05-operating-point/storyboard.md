ENGINE: hyperframes

# F1 score explained, and picking the threshold (series ep 5 of 5): storyboard (v2, recorded VO)

THE QUESTION: "What is the F1 score, and should I maximize it?"
WHO IS ASKING: someone with a decent curve who now has to ship one number
and was told to "use F1."
THE ANSWER IN ONE SENTENCE: F1 is the harmonic mean of precision and
recall, so it treats a blocked user and a missed attack as equally bad.
Usually they aren't, so write down what each mistake costs and set the
threshold there.
THE SEARCH PHRASE: f1 score explained (checked 10/16; "f1 score vs
accuracy" and "precision recall tradeoff" also autocomplete; "how to
choose threshold" and "optimal threshold" are dead, keep them out of the
title).

**One idea:** you don't ship a score, you ship a threshold, so set it by
what a mistake costs.

**Engine:** HyperFrames for every beat (`AGENTS.md` "Which engine"). v1 was
`mixed` for the two PR curves of its "best AUC can lose" beat; the take
doesn't say that beat (nor the code beat), so nothing here needs plotted
axes. Bars, cards and the score line are a canvas and DOM text.

Series context: `../SERIES.md` (ledger, images, Chris's words). The VO is
`script.md` (what Chris said), not the planned script in `../SCRIPTS.md`.
No spoken context line (Chris, 10/17): the frame-0 tag carries it.

## Ledger (copied from SERIES.md and `../_data/ledger.json`; every beat uses exactly these)

- A **prompt-injection detector** in front of an AI agent. **10,000
  requests: 50 attacks, 9,950 real users.** Dots from `../_data/scores.npz`
  (seed 13), model `a`.
- Frame-0 tag (SERIES.md "Context in every episode"): **prompt-injection
  detector · 10,000 requests · 50 attacks**, on from frame 0 to the end.
- F1 example: **precision 0.9, recall 0.1 → mean 0.5, F1 0.18.**
- **Model A** at threshold **0.70**: **precision 40%, recall 80%, F1
  0.53** (TP 40 · FP 60 · FN 10 · TN 9,890; flags 100).
- The two mistakes: **false positive = a real user blocked (they can try
  again). False negative = an attack gets through (the agent is hijacked,
  the data leaked).**
- The target: **2 blocked users for every attack stopped → at least 1 flag
  in 3 is a real attack.**
- The line, moved down as far as the target allows: **threshold 0.66
  (exactly: scores ≥ 0.656), 41 of 50 caught, 123 flags, 41 of them real
  (1 in 3).** On the way the counts tick from the dots themselves (they
  are the data), never typed.
- Not in this Short: Model B, the PR curves, the code, F-beta.

## The look

The **score line** from ep 1 (`../ep01-accuracy-trap/_kit/`, copied to
`_kit/` here as a snapshot so another session's edits can't move it):
tag at the top, users as a teal pile above a 0 → 1 axis, the 50 attacks in
gold below it. **The threshold** is the vertical line; it comes in with
Model A at 0.70 (dim, the F1 line is the hero then) and becomes the
magenta hero when it moves.

**The middle** (y 790–1320; captions are anchored bottom, so the stage
runs to 1330) holds one thing at a time:

1. **Bars** (beats 1–3): two vertical teal bars, "precision" and
   "recall", on a 0 → 1 scale, their values under their names. A dashed
   dim "mean" line and the magenta **F1 line** run across both bars, with
   their labels on the right ("mean 0.5", "F1 0.18").
2. **Cost cards** (beat 4): two full-width cards stacked. "false
   positive" (teal) → "real user blocked" / "can try again"; "false
   negative" (gold) → "agent hijacked" / "data leaked". The card being
   named gets the magenta frame; its dots on the score line ring.
3. **Target + readout** (beats 5–7): three tokens, two teal and one gold,
   "2 blocked : 1 stopped", then "at least 1 in 3 flags real". Under it the
   readout: "caught 40 / 50" and "100 flags, 40 real", which tick as the
   line moves to "41 / 50" and "123 flags, 41 real".

**Hero handoff:** the F1 line (1–3) → the card being named (4) → "1 in 3"
(5) → the threshold (6–7).

## Beats (VO from script.md + the context splice)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook | The F1 score is precision and recall in one number, and it punishes whichever is worse. | Frame 0, already working: the score line with its tag (no threshold), the bars at 0.9 and 0.1, the magenta F1 line at 0.18 labelled "F1 0.18". "one number": the F1 line pulses. "whichever is worse": the recall bar (0.1) pulses. | the F1 line |
| 2 | Why harmonic | Average 0.9 and 0.1 and you get 0.5. F1 will give you 0.18. It's a harmonic mean. | "you get 0.5": the dashed mean line draws in at 0.5, "mean 0.5". "F1 … 0.18": the F1 line pulses at 0.18 under it. "harmonic mean": the recall bar pulses again, the F1 line hugging it. | the F1 line |
| 3 | Model A | Our model, 40 percent precision, 80 percent recall, scores 0.53. | "Our model": the threshold drops in at 0.70 (dim, not magenta) and the 100 flagged dots ring; the mean line fades. "40 percent": the precision bar falls to 0.40 ("40%"). "80 percent": the recall bar rises to 0.80 ("80%"). "0.53": the F1 line rises to 0.53, "F1 0.53". | the F1 line |
| 4 | Costs | But F1 treats both mistakes the same, and here they aren't. A false positive blocks a real user who can try again. A false negative would let an attack hijack your agent and leak your data. | "But F1": the bars fade out, the two cost cards fade in, same size. "false positive": its card lit, the 60 flagged teal dots ring. "false negative": its card lit, the 10 gold dots left of the line ring. | the card being named |
| 5 | The target | So say we'll accept two blocked users for every attack we stop. That means at least one flag in three has to be a real attack. | "So say": the cards fade out; two teal tokens and one gold token come in, "2 blocked : 1 stopped". "one flag in three": a bracket closes over the three, "at least 1 in 3 flags real" in magenta. The readout fades in under it at Model A's numbers: "caught 40 / 50 · 100 flags, 40 real". | "1 in 3" |
| 6 | Move the line | Now move the line down as far as that allows, 41 of 50 attacks caught. | "move the line": the threshold turns magenta and slides left from 0.70 to 0.656 (≥ 1.5 s); dots it passes light up; the readout ticks from the dots ("123 flags, 41 real"). "41 of 50": "caught 41 / 50" pulses. | the threshold |
| 7 | Takeaway | You don't ship an F1 score, you ship a threshold. Decide what a mistake costs and then put the line there. | "ship a threshold": the threshold pulses. "what a mistake costs": the "1 in 3" line pulses (dim, not magenta). "put the line there": hold. Still for the last ~1 s. | the threshold |

## Final beats (the contract; `vo_final.wav` 42.91 s, master seconds)

Beat brief for the agents: `BRIEF.md` (seam states `SC.SEAM` in `_kit/score.js`;
its cue numbers are from the first cut, the beats' `CUE` blocks hold the current ones).
Captions are anchored bottom (`assemble.py --captions-anchor bottom`), so
the stage runs to y 1330, and every caption is one line (≤ 15 characters).

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.00 | 5.30 | The F1 score is precision and recall in one number, and it punishes whichever is worse. |
| 2 | `02_harmonic` | 5.30 | 7.45 | Average 0.9 and 0.1 and you get 0.5. F1 will give you 0.18. It's a harmonic mean. |
| 3 | `03_model_a` | 12.75 | 4.30 | Our model, 40 percent precision, 80 percent recall, scores 0.53. |
| 4 | `04_costs` | 17.05 | 9.75 | But F1 treats both mistakes the same, and here they aren't. A false positive blocks a real user who can try again. A false negative would let an attack hijack your agent and leak your data. |
| 5 | `05_target` | 26.80 | 6.35 | So say we'll accept two blocked users for every attack we stop. That means at least one flag in three has to be a real attack. |
| 6 | `06_move_line` | 33.15 | 3.95 | Now move the line down as far as that allows, 41 of 50 attacks caught. |
| 7 | `07_takeaway` | 37.10 | 5.81 | You don't ship an F1 score, you ship a threshold. Decide what a mistake costs and then put the line there. |

## Cut list (approved by Chris, 10/17; revised after his first watch)

Raw take 44.85 s, clean (no flubs; the F-beta line was never said).
Pauses capped at 0.25 s (`--noise=-45dB`), no phrase cuts: **42.9 s.**

After the first watch (Chris, 10/17):
- **The context line is out** ("It's a prompt injection detector"). The
  frame-0 tag still says it for every viewer.
  (A departure from SERIES.md "Context in every episode": noted for the
  update pass.)
- **Loudness normalization only, no `enhance_vo.sh`.** The take's noise
  floor is −67 dB (already processed); the denoise + de-ess + 3:1
  compressor chain on top made it sound bad (runbook step 3, the
  Studio Sound case).

## Not in this Short (on purpose)

In the description, not the VO: the trap (test at the real attack rate: on
a 50/50 test set, Model A's precision at its threshold goes from 40% to
about 99%), F-beta (β = 2 counts recall double), and the series list.
Model B and "the best AUC can lose" (v1 beat 4) and the code beat were not
recorded.
