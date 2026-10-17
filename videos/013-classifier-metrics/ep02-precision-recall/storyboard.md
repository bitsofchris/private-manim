ENGINE: hyperframes

# Precision vs recall (series ep 2 of 5): storyboard (v2, recorded VO)

THE QUESTION: "What's the difference between precision and recall?"
WHO IS ASKING: someone who has seen both numbers on a report and mixes
them up.
THE ANSWER IN ONE SENTENCE: precision asks, of the ones I flagged, how
many were attacks; recall asks, of all the attacks, how many I caught.
Same numerator, different denominators.
THE SEARCH PHRASE: precision vs recall (checked 10/16, the top
suggestion; "precision and recall explained" also autocompletes).

**One idea:** the same 40 catches, divided by two different things.

**Engine:** HyperFrames for every beat (`AGENTS.md` "Which engine"). The
score line is dots on a 0 → 1 axis and the box is a grid, as in ep 1;
nothing here needs real plotted axes.

Series context: `../SERIES.md` (ledger, images, Chris's words). The VO is
`script.md` (what Chris said), not the planned script in `../SCRIPTS.md`.

## Ledger (copied from SERIES.md; every beat uses exactly these)

- A **prompt-injection detector** in front of an AI agent. **10,000
  requests: 50 attacks, 9,950 real users.**
- **Model A** flags **100** requests, and **40** are attacks.
- Box: **TP 40 · FP 60 · FN 10 · TN 9,890.** Rows "flagged / not
  flagged", columns "attack / real user": TP top-left, FP top-right, FN
  bottom-left, TN bottom-right. The same layout in all five episodes.
- **Recall** = TP / (TP + FN) = 40 / 50 = **80%**: the attack *column*.
- **Precision** = TP / (TP + FP) = 40 / 100 = **40%**: the flagged *row*.
- FP = a real user blocked (**60**). FN = an attack that got through
  (**10**).
- TN = **9,890**. The VO says "almost 10,000"; the screen shows 9,890.
- Model A's threshold is **0.70** (`_data/ledger.json`, `model_a_box`).
  Dots come from `_data/scores.npz` (seed 13), model `a`, through the
  kit's `dots.js`.
- Frame-0 tag (SERIES.md "Context in every episode"): **prompt-injection
  detector · 10,000 requests · 50 attacks**.
- Attacks are gold (`CONTENT_GOLD`, `#E0B040`), users teal, the hero
  magenta: ep 1's colours.

## The look

Frame 0 is ep 1's last frame, so the series reads as one picture: the tag
and score line on top (magenta threshold at 0.70, dimmed), the box below
with all four cells counted. Ep 2 adds **two fraction bars** under the
box: recall on the left, precision on the right, each the numerator over
the denominator with its percentage beside it.

The denominators come out of the box, so the viewer sees where each one
comes from: recall's is the **attack column** (TP + FN = 50), lifted out
of the left side of the box; precision's is the **flagged row** (TP + FP
= 100), lifted out of the top. The left bar sits under the left column
and the right bar under the right column, and that geometry holds to the
end: it's the memory aid.

To fit the bars, the box is shorter than in ep 1 (it runs to ~y 1110,
cells without dots), and the bars take y ~1140–1330. Captions are
anchored bottom (`assemble.py --captions-anchor bottom`), so the stage
runs to y 1330 as in ep 1. `00_layout/` settles this before any beat is
built.

Shared kit: `_kit/` is copied from ep 1's (`score.js`, `dots.js`,
`make_dots.py`, as of `bc1b4b3`) and extended here with the fraction
bars and ep 2's seam states. Ep 1's kit is not touched.

**Code: none.** The take has no code line, and the fraction bars already
are the two formulas. A silent code card would compete with the bars for
the same 200 px. Promote-later note in the hand-off.

## Beats (VO as recorded; vo_final seconds from the trial cut)

| # | Beat | ~s | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---:|---|---|---|
| 1 | Recall, the question | 4.3 | Recall is asking, of all the positives, how many did I actually catch? | Frame 0, already working: ep 1's end state (tag, score line, box with TP 40 / FP 60 / FN 10 / TN 9,890), the box already shortened, the two empty bars faint under it. "Recall": the left bar's label "recall" lights. "all the positives": the attack column (TP + FN) lights magenta and the 50 gold dots ring on the score line, both sides of the threshold. "catch": TP 40 brightens. | the attack column |
| 2 | Context | 4.4 | It's a prompt injection detector. 10,000 requests come in, but only 50 are attacks. | The column dims to rest. "prompt injection detector": the tag brightens. "10,000 requests": the teal pile pulses. "only 50": the 50 gold dots ring once (and the tag's "50 attacks"). | the tag (white, no magenta) |
| 3 | Recall = 80% | 4.0 | If there were 50 attacks and we only caught 40, recall is about 80%. | "50 attacks": the attack column lifts out of the box and drops into the left bar as the denominator **50** (40 + 10). "caught 40": TP's 40 flies up as the numerator **40**. "80%": **80%** lands beside the fraction. | the left bar |
| 4 | Precision, the question | 6.1 | Now precision is saying of the ones that I did predict were positive, how many actually were positive? | The left bar returns to rest (teal). "precision": the right bar's label lights. "predict were positive": the flagged row (TP + FP) lights magenta and the 100 dots right of the threshold ring (40 gold, 60 teal). "actually were": TP 40 brightens inside the row. | the flagged row |
| 5 | Precision = 40% | 3.8 | We flagged 100, 40 were attacks, precision is 40%. | "flagged 100": the row lifts out and drops into the right bar as the denominator **100** (40 + 60). "40 were attacks": TP's 40 flies up as the numerator **40**. "40%": **40%** lands. Both bars now filled. | the right bar |
| 6 | Neither uses TN | 6.2 | Neither one uses the true negatives. In this case, there's almost 10,000 of them. That's why they still work when the attacks are rare. | The right bar to rest. "true negatives": the TN cell lights, then ghosts to muted with a thin strike; neither bar holds any of it. "10,000": the TN count 9,890 pulses (the screen shows the ledger value). "rare": the 50 gold dots pulse on the score line. | the TN cell, then none |
| 7 | What you missed | 3.2 | Recall is all about what you missed. These are the attacks that got through, | "missed": the FN cell (10) lights and the recall bar's 50 shows its 10 part; "got through": the 10 gold dots left of the threshold ring on the score line, and "10 got through" appears under the recall bar. | the FN cell |
| 8 | What you wasted | 4.3 | and precision is about what you wasted. These are real users that you ended up blocking. | "wasted": FN to rest, the FP cell (60) lights; "real users": the 60 teal dots right of the threshold ring, and "60 users blocked" appears under the precision bar. Settles still: both bars, both notes, nothing lit. | the FP cell, then none |

## Final beats (the contract; `vo_final.wav` 37.12 s, master seconds)

Beat brief for the agents: `BRIEF.md` (seam states `SC.SEAM` in `_kit/score.js`).

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_recall_q` | 0.00 | 4.30 | Recall is asking, of all the positives, how many did I actually catch? |
| 2 | `02_context` | 4.30 | 4.25 | It's a prompt injection detector. 10,000 requests come in, but only 50 are attacks. |
| 3 | `03_recall_80` | 8.55 | 4.35 | If there were 50 attacks and we only caught 40, recall is about 80%. |
| 4 | `04_precision_q` | 12.90 | 6.40 | Now precision is saying, of the ones that I did predict were positive, how many actually were positive? |
| 5 | `05_precision_40` | 19.30 | 3.65 | We flagged 100, 40 were attacks, precision is 40%. |
| 6 | `06_no_tn` | 22.95 | 6.20 | Neither one uses the true negatives. In this case, there's almost 10,000 of them. That's why they still work when the attacks are rare. |
| 7 | `07_missed` | 29.15 | 3.05 | Recall is all about what you missed. These are the attacks that got through, |
| 8 | `08_wasted` | 32.20 | 4.922 | and precision is about what you wasted. These are real users that you ended up blocking. |

## Cut list (approved by Chris, 10/17; applied)

Raw take 45.0 s. The long context clip (`../vo_context_long.m4a`, 4.15 s,
"It's a prompt injection detector. 10,000 requests come in, but only 50
are attacks.") is spliced into the raw take in the silence after VO line
1 (raw 12.45 s), and the joined take goes through `enhance_vo.sh` once,
so the two match in level. Pauses capped at 0.25 s (`--noise=-45dB`).

```
ffmpeg -i vo_raw.m4a -i ../vo_context_long.m4a -filter_complex "[0:a]atrim=0:12.45,…[a];[1:a]…[b];[0:a]atrim=start=12.45,…[c];[a][b][c]concat=n=3:v=0:a=1" vo_joined.wav
tools/enhance_vo.sh vo_joined.wav vo_clean.wav
tools/tighten_vo.py vo_clean.wav --out vo_final.wav --map timemap.json --max-gap 0.25 --noise=-45dB --remove 0-8.40 --remove 20.75-23.10
```

| # | Cut | vo_clean range | Saves | Why |
|---|---|---|---:|---|
| 1 | "Recall is asking of all the positives my model classified, how… Sorry. Redo." | 0–8.40 | 8.4 s | the flub and restart; script.md flags it |
| 2 | "We caught 40 out of the 50 that are possible." | 20.75–23.10 | 2.4 s | repeats the line before it; script.md flags it |
| — | (splice) the context line after VO line 1 | — | +4.15 s | SERIES.md "Context in every episode" |

Result **37.1 s**, re-transcribed with Parakeet (`transcript_final_text.txt`):
every join reads clean. Words in `words.json` (WhisperKit, spellings
fixed: "10" + ",000" merged to "10,000"; "through." → "through,").

Kept on purpose:
- VO line 1 is the recall definition, not "precision versus recall", so
  the search phrase is never spoken. The title and frame 0 carry it.
- "recall is **about** 80%" (Chris's words); the screen shows 80%.
- "almost 10,000" true negatives; the screen shows 9,890.
- "If there were 50 attacks" right after "only 50 are attacks": the
  repeat sets up the fraction, and the Short is already short.

## Not in this Short (on purpose)

Moving the threshold (ep 3). F1 (ep 5). "Sensitivity" / "true positive
rate" as other names for recall go in the description, not the VO.
