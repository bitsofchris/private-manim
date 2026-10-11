ENGINE: hyperframes

# Ep 4. What `x @ W` Really Computes — storyboard

**Series:** Linear Algebra for AI Engineers, episode 4 (`../SERIES.md`).
**Title:** Matrix Multiplication (x @ W) | Linear Algebra for AI Engineers

Engine: HyperFrames (the default, `AGENTS.md` "Which engine"). Every beat is
number grids plus a flat 2D plane; nothing needs Manim's axes or 3D camera.

## Preflight

- **THE QUESTION:** What is `x @ W` actually computing?
- **WHO IS ASKING:** an engineer who writes `nn.Linear` and `x @ W` every
  day and has watched 3Blue1Brown, but can't say what the multiply does
  beyond "rows times columns".
- **THE ANSWER IN ONE SENTENCE:** Each number in `x` weights one row of `W`;
  add the weighted rows and you have the output.

## The look

One stage, two halves, both always on (`00_layout/`, rendered to
`media/hf/00_layout.png`):

- **Notation:** the series default, `agents/style.md` "Vectors and
  matrices as numbers" (Chris, ep04). Matrices are bare numbers in square
  brackets, with no box per number. The result is a vector, `[ 4, −1 ]`,
  so it has its comma. `W` carries its shape `(3, 2)`, and `x @ W` is
  monospace because it is code. A highlight is a box that appears around
  an entry or a column and then goes.
- **Top, the numbers (y 236–632).** The header line (y 236) holds the
  labels `x` and `W`, or `x = [ 1, 2, −1 ]` written flat before it turns.
  Under it, left to right: `x` turned sideways as a column, `W` (3 × 2),
  a `→` per row, the weighted rows (3 × 2). Under the weighted rows, the
  sum row `[ 4, −1 ]` with `x @ W` to its left.
- **Bottom, the plane (y 650–1100).** One square = one step (100 px; the
  plane is smaller than ep01's 165 because it shares the stage with the
  numbers). East right, north up, origin at screen (352, 880), axes with a
  tick per step, x −1…4, y −2…2.

Each row of `W` keeps one colour everywhere (digits, its `x` weight, its
weighted row, its arrow): row 1 teal, row 2 blue, row 3 gold
(`COL.tokens`, `CONTENT_BLUE` / `CONTENT_GOLD`). Magenta is free for the one
hero per beat. Parts: `_vec/vec.js` (linked into each beat as `vec/`), on
top of `videos/_shared/web/iso/iso.js` (`iso/`). Started from ep01's
`_vec/vec.js`; adds the ledger, the grids and a plane clipped to the bottom
half.

## Ledger (identical in every beat; constants in `_vec/vec.js`)

From `one_row_weighted_sum.py` and `batched_linear_map_tensors.py` (the
first row of the `(5, 3) @ (3, 2)` example shared by episodes 3–6).
Row-vector (PyTorch) convention: `x @ W`, `W` is `(in, out)` = 3 × 2, rows
of `W` are where input directions land.

| What | Value | In `vec.js` |
|---|---|---|
| x | `[ 1, 2, −1 ]` (true minus sign) | `VEC.X` |
| W rows (landing spots) | row 1 `(2, −1)`, row 2 `(0.5, 1)`, row 3 `(−1, 2)` | `VEC.W` |
| Weighted rows | 1 × row 1 = `(2, −1)`; 2 × row 2 = `(1, 2)`; −1 × row 3 = `(1, −2)` | `VEC.XW` |
| Column sums | 2 + 1 + 1 = **4**; −1 + 2 − 2 = **−1** | |
| x @ W | `[ 4, −1 ]` | `VEC.SUM` |
| Tip to tail | (0, 0) → (2, −1) → (3, 1) → (4, −1) | `VEC.CHAIN` |
| Bias b | `[ 0.1, −0.2 ]` | `VEC.B` |
| x @ W + b | `[ 4.1, −1.2 ]` (row 1 of `Y`) | `VEC.Y` |
| Labels | `x`, `W (3, 2)` in Inter 800; `x @ W`, `x @ W + b` in monospace (code); all 64 px | `VEC.headers` |

## States (what each beat opens and ends on)

All states are built with `VEC.parts(root)` once and `VEC.canon(P, g)` at
the top of `render(t)`; a beat then hides or moves only what differs.

- **CANON** = `00_layout`: `x` column, `W`, `→`s, weighted rows, sum row
  `[ 4, −1 ]` (magenta border and digits), `x @ W` label; plane with axes,
  the chain teal → blue → gold tip to tail, the magenta output arrow
  (0, 0) → (4, −1) drawn under the chain.
- **CANON+b** = CANON with the sum row reading `[ 4.1, −1.2 ]`, its label
  `x @ W + b`, and the output arrow's tip at (4.1, −1.2); the chain is
  unchanged (`VEC.canon(P, g, { bias: true })`).
- **SIDEWAYS** = START with `x` turned into the column left of `W` (the
  `x` header, `x`'s brackets), `x = [ … ]` gone, the three `→`s shown, the
  landing arrows still from the origin. No highlight.
- **SCALED** = SIDEWAYS plus the weighted rows (with their brackets) and,
  on the plane, the three *weighted* arrows from the origin: (2, −1),
  (1, 2), (1, −2). No landing arrows. No highlight.
- **CHAINED** = SCALED with the arrows laid tip to tail as the chain, the
  sum row's brackets in place (dim) and empty. No output arrow, no
  `x @ W` label. No highlight.
- **START** = what beat 2 builds toward: `x = [ 1, 2, −1 ]` flat on the
  header line, `W` with its three landing arrows from the origin; no `x`
  column, no weighted rows, no sum, no chain.

## Final beats (the contract)

`vo_final.wav` is 53.321 s. Every cut sits in a pause. Beat-local t = master − start.

| # | Folder | Master start | Length | Opens on | Ends on | VO |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 7.35 | (frame 0: the computation already running) | CANON | x at W is just a weighted sum of W's rows. It's the one operation inside every linear layer. |
| 2 | `02_setup` | 7.35 | 9.37 | CANON | START | Take x equals one, two, minus one, and W, a three by two matrix. Three rows, one for each input direction, each a 2D landing spot. |
| 3 | `03_sideways` | 16.72 | 5.54 | START | SIDEWAYS | Now turn x sideways so it sits beside W. Now each number in x is a weight for one row. |
| 4 | `04_scale` | 22.26 | 3.58 | SIDEWAYS | SCALED | One times the first row, two times the second row, minus one times the third row. |
| 5 | `05_add` | 25.84 | 8.88 | SCALED | CHAINED | Now we have three weighted 2D vectors. To add vectors, you add first coordinates together and second coordinates together. That's summing down the columns. |
| 6 | `06_result` | 34.72 | 2.28 | CHAINED | CANON | Four minus one, that's x at W. |
| 7 | `07_meaning` | 37.00 | 6.03 | CANON | CANON | Rows are where input directions land. Columns are the totals in each output direction. |
| 8 | `08_bias` | 43.03 | 5.80 | CANON | CANON+b | Add the bias and you have one row of a linear layer's output, 4.1 minus 1.2. |
| 9 | `09_close` | 48.83 | 4.491 | CANON+b | CANON+b | Each number in x weights a row of W. Add the rows and you're done. |

## Beats (the visual brief)

| # | Folder | Start | Length | VO | Hero | Visual |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 7.35 | x at W is just a weighted sum of W's rows. It's the one operation inside every linear layer. | the sum row + output arrow | Frame 0: `x` column beside `W`, the rows already weighting (weighted cells popping in row by row, the three arrows on the plane growing from the origin). "weighted sum": the arrows slide tip to tail into the chain. "W's rows": the sum row lands `[ 4, −1 ]` and the magenta output arrow draws. By "every linear layer" it is CANON; the `x @ W` label brightens once. Ends CANON, still. |
| 2 | `02_setup` | 7.35 | 9.37 | Take x equals one, two, minus one, and W, a three by two matrix. Three rows, one for each input direction, each a 2D landing spot. | `W`'s outline | Opens CANON. First 0.6 s: weighted rows, `→`s, sum row, label, chain and output arrow fade out; the `x` column lifts to the header line as `x = [ 1, 2, −1 ]` ("one, two, minus one" lands each number). "three by two matrix": a magenta outline draws around `W`. "Three rows": each row of `W` pulses in turn. "one for each input direction": row k's `x` number pulses with its row. "2D landing spot": the three arrows draw from the origin to (2, −1), (0.5, 1), (−1, 2), each in its row's colour, the row pulsing as its arrow lands. Ends START. |
| 3 | `03_sideways` | 16.72 | 5.54 | Now turn x sideways so it sits beside W. Now each number in x is a weight for one row. | the `x` column | Opens START. "turn x sideways": the three numbers of `x` swing from the flat line down into the column left of `W` (≥ 0.8 s, one path each, the `x =` text becomes the `x` header). Outline moves from `W` to the `x` column (magenta). "a weight for one row": each `x` cell links to its row: a thin line of the row colour under the row from the `x` cell to the row's right end, one by one, then the `→`s appear. Plane: landing arrows stay. |
| 4 | `04_scale` | 22.26 | 3.58 | One times the first row, two times the second row, minus one times the third row. | the `x` weight being applied | On each "times": the `x` cell's border magenta, the weighted row appears at the right (`2, −1`; `1, 2`; `1, −2`), and on the plane that row's arrow scales: row 1 holds (×1, a pulse), row 2 doubles (0.5, 1) → (1, 2), row 3 flips through the origin (−1, 2) → (1, −2). Ends: three weighted arrows from the origin, weighted rows filled, `x` borders back to muted. |
| 5 | `05_add` | 25.84 | 8.88 | Now we have three weighted 2D vectors. To add vectors, you add first coordinates together and second coordinates together. That's summing down the columns. | the column being summed | "three weighted 2D vectors": the weighted rows and their arrows pulse together. "To add vectors": the blue arrow slides so its tail sits on the teal tip, then the gold onto the blue tip (the chain, ≥ 0.8 s each). "first coordinates": a magenta box around the weighted rows' first column, and on the plane the east steps light (guides along the axis). "second coordinates": box moves to column 2. "summing down the columns": the sum row's empty brackets appear (dim) under the weighted rows. No sum digits yet. Ends CHAINED. |
| 6 | `06_result` | 34.72 | 2.28 | Four minus one, that's x at W. | the sum row + output arrow | "Four": `4,` drops into the sum row; "minus one": `−1`; the brackets turn magenta and the magenta output arrow draws (0, 0) → (4, −1) under the chain; "x at W": the `x @ W` label. Ends CANON. |
| 7 | `07_meaning` | 37.00 | 6.03 | Rows are where input directions land. Columns are the totals in each output direction. | first `W`'s rows, then the sum row's columns | "Rows … land": `W`'s three rows outline in their colours and faint ghosts of the three landing arrows appear from the origin (alpha ~0.35). "Columns are the totals": ghosts fade; the sum cells' columns light one at a time with dashed guides from (4, −1) to 4 on the east axis and −1 on the north axis ("each output direction"). Guides fade before the hold. Ends CANON. |
| 8 | `08_bias` | 43.03 | 5.80 | Add the bias and you have one row of a linear layer's output, 4.1 minus 1.2. | the output row | "Add the bias": a row `b  [ 0.1, −0.2 ]` (dim label, white digits) appears just under the sum row, over the empty top edge of the plane. "one row of a linear layer's output": it slides up into the sum row and is gone; the label becomes `x @ W + b`. "4.1": the first cell retypes to `4.1`; "minus 1.2": the second to `−1.2`; the output arrow's tip nudges to (4.1, −1.2). Ends CANON+b. |
| 9 | `09_close` | 48.83 | 4.491 | Each number in x weights a row of W. Add the rows and you're done. | the output row | Opens CANON+b. "Each number in x weights a row of W": the three rows (x cell, W row, weighted row, arrow) pulse in turn, row colours. "Add the rows": the chain pulses tip to tail and the output row brightens. Last 0.6 s still on CANON+b: the frame episode 5 can open beside `nn.Linear`. |

Segment times (master, `transcript_final.txt`): 0.58 "x at W…", 4.61 "It's
the one operation…", 7.54 "Take x equals…", 10.37 "and W, a three by
two…", 12.95 "Three rows…", 15.27 "each a 2D landing spot", 16.92 "Now turn
x sideways…", 19.58 "Now each number…", 22.45 "One times…", 24.47 "minus
one times…", 26.03 "Now we have three…", 28.59 "To add vectors…", 31.60
"and second coordinates…", 33.16 "That's summing…", 34.90 "Four minus
one…", 37.20 "Rows are…", 39.47 "Columns are…", 43.23 "Add the bias…",
44.83 "of a linear layer's output…", 49.03 "Each number in x…", 51.70 "Add
the rows…". Beat boundaries sit in the pauses. Place exact cues from the
audio (50 ms RMS envelope of your window), not from these.

## Cut list (runbook step 5)

`vo_raw.m4a` (62.5 s; −67 dB floor, already clean) → `vo_clean.wav`
(loudnorm only) → `vo_final.wav` (53.3 s):
`tools/tighten_vo.py --max-gap 0.25` (pauses capped, no phrase removed).
Approved by Chris (2026-10-10). The repeated "Now" kept.
