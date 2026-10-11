ENGINE: hyperframes

# Ep 5. The `nn.Linear` shape gotcha — storyboard

**Series:** Linear Algebra for AI Engineers, episode 5 (`../SERIES.md`).
**Title:** PyTorch nn.Linear Explained | Linear Algebra for AI Engineers

Engine: HyperFrames (the default, `AGENTS.md` "Which engine"). Every beat is
code, number grids, a small network diagram and the flat 2D plane; nothing
needs Manim's axes or 3D camera.

## Preflight

- **THE QUESTION:** I asked for 3 in, 2 out. Why is the weight 2 by 3?
- **WHO IS ASKING:** an engineer who writes `nn.Linear` and `x @ W`, has
  watched 3Blue1Brown and episodes 3–4, and gets tripped up the first time
  they print `lin.weight.shape`.
- **THE ANSWER IN ONE SENTENCE:** PyTorch stores one row per output neuron
  and flips it on the forward pass. It is the same map, stored sideways.

## The look

Two halves of one Short, rendered in `00_layout/` (snapshots
`media/hf/00_layout_A.png`, `_B.png`). The code is
`../../../_shared/web/vec/vec.js` (the shared plane kit, linked as `vec/`)
plus this episode's `_ep/ep05.js` (linked as `ep/`): the ledger, where
things sit, and the four rest states. Notation is the series default
(`agents/style.md` "Vectors and matrices as numbers").

- **Colour is the input direction.** Input i, column i of `weight`, row i of
  `weight.T` and that row's landing arrow are one colour: 1 teal, 2 blue,
  3 gold (`VEC.SLOT`). A transpose moves each number and keeps its colour,
  so the viewer sees the columns become rows. Neurons have no colour; the
  active one gets the magenta box (its row) and a magenta ring.
- **Top (y 236–732):** the one-line code card at y 236; matrix names
  (monospace, code) at y 372 and shapes (Inter, as PyTorch prints `.shape`)
  at y 440, both `--dim`; matrices from y 516, 110 px cells, 60 px digits.
  First half: `weight` centred (left edge 375). Second half: `weight` at the
  left (120), `.T →` between, `weight.T` at the right (650).
- **Bottom (y 770–1100):** first half, the network: inputs at x 280 (y 818,
  930, 1042), two neurons at x 640 (y 874, 986), outputs to the right at
  x 740. Second half, the plane: 92 px a step, origin (600, 980), clipped
  above y 770, `weight.T`'s rows as arrows from the origin.
- **Magenta, one at a time:** the active neuron's row and ring; the shape
  `(2, 3)`; the `.T`; a lit row or column. At rest in CANON the `.T` (in the
  code card and between the matrices) is the hero.

## Ledger (identical in every beat; constants in `_ep/ep05.js`)

The `(5, 3) @ (3, 2)` example from `nn_linear_weight_structure.py`, row 1,
the same numbers as ep04 (`weight.T` is ep04's `W`). Row-vector (PyTorch)
convention: `x @ weight.T`, rows of `weight.T` are where input directions
land. The math (column) convention appears only in beat 8.

| What | Value | In `ep05.js` |
|---|---|---|
| Code | `nn.Linear(3, 2)`; forward `x @ weight.T + bias` | `parts().cardA`, `.cardB` |
| x | `[ 1, 2, −1 ]` (true minus sign) | `EP.X` |
| weight `(2, 3)`, one row per neuron | `[[ 2, 0.5, −1 ], [ −1, 1, 2 ]]` | `EP.WEIGHT` |
| weight.T `(3, 2)` = ep04's W | rows `(2, −1)`, `(0.5, 1)`, `(−1, 2)` | `EP.WT` |
| Products x[i] · weight[n][i] | neuron 1: 2, 1, 1; neuron 2: −1, 2, −2 | `EP.PROD` |
| Sums | neuron 1: **4**; neuron 2: **−1** | `EP.DOT` |
| bias | `[ 0.1, −0.2 ]` | `EP.B` |
| Outputs | neuron 1 **4.1**, neuron 2 **−1.2**: `[ 4.1, −1.2 ]` (ep04's result) | `EP.Y` |
| Labels | `weight`, `weight.T` monospace; `(2, 3)`, `(3, 2)` Inter; all 60 px `--dim` | `parts().names` |

## States (what each beat opens and ends on)

`P = EP.parts(root)` once; `EP.state(P, g, NAME)` at the top of `render(t)`;
a beat then draws only what differs.

- **STORED:** card `nn.Linear(3, 2)`; `weight (2, 3)` centred; the network
  with empty input rings, both neurons dim, no outputs.
- **OUTPUTS:** STORED + inputs `1, 2, −1` in their rings + outputs `4.1`,
  `−1.2` beside the neurons (white). No highlight.
- **FLIPPED:** card `x @ weight.T + bias` (`.T` magenta); `weight` at the
  left, `.T →`, `weight.T (3, 2)` at the right; lower stage empty.
- **CANON:** FLIPPED + the plane with the three landing arrows (00_layout B).

## Final beats (the contract)

`vo_final.wav` is 51.341 s. Every cut sits in a pause. Beat-local t = master − start.

| # | Folder | Master start | Length | Opens on | Ends on | VO |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 3.60 | (frame 0: already moving) | STORED | PyTorch stores one output neuron per row. |
| 2 | `02_shape` | 3.60 | 5.24 | STORED | STORED | So when you give nn.Linear three in and two out, the weight will come back two by three. |
| 3 | `03_neuron` | 8.84 | 6.47 | STORED | OUTPUTS minus output 2 | A neuron takes all three inputs, multiplies each by its own weight, sums them, adds a bias, and outputs one number. |
| 4 | `04_two` | 15.31 | 3.09 | OUTPUTS minus output 2 | OUTPUTS | Two outputs, two neurons, two rows of three. |
| 5 | `05_flip` | 18.40 | 5.18 | OUTPUTS | FLIPPED | In the forward pass, PyTorch flips it. x @ weight.T plus a bias. |
| 6 | `06_landing` | 23.58 | 7.30 | FLIPPED | CANON | The flipped weight is three by two, exactly the W from the last video, where each row is where an input direction lands. |
| 7 | `07_ask` | 30.88 | 6.16 | CANON | CANON | So don't ask which is in and which is out, ask where are the landing vectors stored, in the rows or the columns? |
| 8 | `08_conventions` | 37.04 | 7.72 | CANON | CANON | In math, vectors are columns, and W times v uses the columns. In PyTorch, vectors are rows, and x @ W uses the rows. |
| 9 | `09_close` | 44.76 | 6.581 | CANON | CANON | It's the same idea, just transposed. nn.Linear stores neurons as rows and transposes on the way through. |

## Beats (the visual brief)

| # | Folder | Hero | Visual |
|---|---|---|---|
| 1 | `01_hook` | each neuron's row, in turn | Frame 0: STORED already drawing: the wires grow from the inputs to the neurons (0–0.6 s). "one output neuron": neuron 1's ring turns magenta and its three wires brighten; "per row": the magenta box draws round `weight`'s row 1, then box and ring pass to neuron 2 / row 2, then both return to rest by ~3.2 s. Ends STORED, still. |
| 2 | `02_shape` | the shape `(2, 3)` | Opens STORED. "three in": the three input rings pulse in turn (teal, blue, gold) and the `3` in the card brightens; "two out": the two neurons pulse and the `2` in the card brightens. "the weight will come back": `weight`'s brackets brighten once. "two by three": the shape `(2, 3)` turns magenta with a box round it, "two" on the `2` (the two rows pulse), "three" on the `3` (the three columns pulse). Box goes, shape back to `--dim` by the hold. Ends STORED. |
| 3 | `03_neuron` | neuron 1 (its row box + ring) | Opens STORED. "A neuron": neuron 1's ring magenta, row 1 boxed. "all three inputs": `1`, `2`, `−1` fade into the input rings in turn and neuron 1's three wires brighten. "multiplies each by its own weight": each of row 1's numbers pulses with its wire, in turn (2, 0.5, −1). "sums them": `4` appears beside neuron 1 at the output spot. "adds a bias": it reads `4 + 0.1` (the `+ 0.1` in `--dim`). "outputs one number": it becomes `4.1` (white). Ring and box back to rest before the hold. Ends OUTPUTS without `−1.2`. |
| 4 | `04_two` | neuron 2, then both rows | "Two outputs": `−1.2` appears beside neuron 2 (its three wires flick bright and back). "two neurons": both neuron rings pulse. "two rows of three": the box draws round both rows of `weight` together (one box, whole matrix), then goes. Ends OUTPUTS. |
| 5 | `05_flip` | the `.T` | Opens OUTPUTS. "In the forward pass": the network, inputs and outputs fade out (0.6 s) and the card `nn.Linear(3, 2)` cross-fades to `x @ weight.T + bias`; `weight` slides from centre to the left (≥ 0.8 s). "flips it": a copy of each of `weight`'s six numbers flies from (r, c) to `weight.T`'s (c, r), keeping its colour (≥ 1 s, gentle stagger by column so column 1 becomes row 1, and so on); the right brackets, the name `weight.T` and the `.T →` appear with it; the `.T`s are magenta. "x @ weight.T": the card's `.T` pulses. "plus a bias": `+ bias` in the card brightens once. Ends FLIPPED. |
| 6 | `06_landing` | `weight.T`'s rows, in turn | Opens FLIPPED. "three by two": `(3, 2)` turns magenta with a box, then back. "exactly the W from the last video": a `= W` tag fades in beside the name `weight.T` (Inter, `--dim`) and goes by the end of the clause. "where each row is where an input direction lands": the plane fades in under the matrices (0.5 s), then each row of `weight.T` gets the box in its turn while its arrow draws from the origin to (2, −1), (0.5, 1), (−1, 2) (teal, blue, gold; ≥ 0.6 s each). Ends CANON. |
| 7 | `07_ask` | the landing vectors, in both matrices | Opens CANON. "which is in and which is out": the two shapes `(2, 3)` and `(3, 2)` pulse, left then right. "where are the landing vectors stored": the three arrows pulse together. "in the rows": `weight.T`'s three rows get boxes in their colours, one after another (fast). "or the columns": `weight`'s three columns get boxes in the same colours, and the matching row/column pairs stay boxed together a moment so teal column ↔ teal row reads. All boxes go before the hold. Ends CANON. |
| 8 | `08_conventions` | first `weight`'s columns, then `weight.T`'s rows | Opens CANON. "In math": the plane fades out (0.4 s) and the lower stage becomes two labelled panels: left `math` (Inter, `--dim`), right `PyTorch`. "vectors are columns": under `math`, `v` as a column `[1; 2; −1]` (teal, blue, gold, one tall bracket pair). "W times v": `W v` (Inter) beside it; the name `weight` gets a `W` tag; "uses the columns": `weight`'s three columns box in turn. "In PyTorch, vectors are rows": under `PyTorch`, `x = [ 1, 2, −1 ]` as a row. "x @ W": `x @ W` (monospace); "uses the rows": `weight.T`'s three rows box in turn. At ~7.0 s the panels fade and the plane fades back. Ends CANON. |
| 9 | `09_close` | the `.T` | Opens CANON. "same idea": the three arrows pulse once. "just transposed": the `.T →` swells and a ghost of each column of `weight` slides to its row of `weight.T` and fades (≤ 1 s). "stores neurons as rows": `weight`'s two rows box in turn (magenta). "transposes on the way through": the card's `.T` and the `.T →` pulse magenta. Last 0.8 s still on CANON: the frame episode 6 opens beside `X`. |

Segment times (master, `transcript_final.txt`): 0.67 "PyTorch stores…",
3.81 "So when you give…", 7.00 "the weight will come back…", 9.10 "A neuron
takes…", 11.10 "multiplies each…", 12.82 "sums them…", 15.55 "Two outputs…",
18.62 "In the forward pass…", 23.78 "The flipped weight…", 25.54 "exactly
the W…", 28.02 "where each row…", 31.10 "So don't ask…", 32.54 "ask where
are…", 35.18 "in the rows or the columns", 37.23 "In math…", 40.84 "In
PyTorch…", 44.94 "It's the same idea…", 46.89 "nn.Linear stores…", 49.05
"and transposes…". Beat boundaries sit in the pauses. Place exact cues
from the audio (50 ms RMS envelope of your window), not from these.

## Cut list (runbook step 5)

`vo_raw.m4a` (58.5 s; already clean, same session as ep04) →
`vo_clean.wav` (loudnorm only) → `vo_final.wav` (51.3 s):
`tools/tighten_vo.py --max-gap 0.25 --remove 17.40-20.30`.

- **Removed, 17.40–20.30 (raw):** the flub "Two outputs, two neu-". The
  retake "Two outputs, two neurons, two rows of three" is kept.
- Pauses capped at 0.25 s. No other phrase removed; the "if time" line
  (math vs PyTorch) fits.

Approval: pending.
