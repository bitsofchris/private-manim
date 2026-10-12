ENGINE: hyperframes

# Ep 6. One matmul, whole batch — storyboard

**Series:** Linear Algebra for AI Engineers, episode 6 (`../SERIES.md`).
**Title:** PyTorch Matrix Multiplication | Linear Algebra for AI Engineers
**Search phrase:** pytorch matrix multiplication (`../SERIES.md`, episode 6)

Engine: HyperFrames (the default, `AGENTS.md` "Which engine"). Every beat is
three matrices and a code card; nothing needs Manim's axes or
3D camera.

## Preflight

- **THE QUESTION:** How does a whole batch go through a layer in one line?
- **WHO IS ASKING:** an engineer who writes `x @ W` and `nn.Linear`, has
  watched episodes 3–5, and sees `X` with a batch dimension in real code and
  loses track of which matrix is which and why the shapes work.
- **THE ANSWER IN ONE SENTENCE:** `X` is data and `W` is the map:
  `(batch, in) @ (in, out)` applies the same map to every row.
- **THE SEARCH PHRASE:** pytorch matrix multiplication (offered by YouTube
  autocomplete; `../SERIES.md`). Not "batch matrix multiplication", which
  autocomplete pairs with "dsa" / "using dp". VO line 1 ("One line of
  PyTorch pushes a whole batch through a layer…") is a reframe and says
  "PyTorch"; no recut.

## The look

One stage, rendered in `00_layout/` (snapshots `media/hf/00_layout_A.png`
CANON, `_B.png` the beat-5 sweep, `_C.png` BIG). The
code is `../../../_shared/web/vec/vec.js` (the shared plane kit, linked as
`vec/`) plus this episode's `_ep/ep06.js` (linked as `ep/`): the ledger,
where things sit, and the rest states. Notation is the series default
(`agents/style.md` "Vectors and matrices as numbers").

- **No plane in this episode (a deviation, for Chris to OK on 00_layout).**
  The five outputs run from −5.2 to 5.8 on both axes; a plane that holds
  them beside fifteen input numbers would be about 35 px a step, too small
  to read. The episode is about the batch and the shapes, so the stage
  is all notation. The plane kit still supplies the cells, brackets, code
  card and highlight boxes.
- **Colour is the input direction**, as in ep04–05: column i of `X` (the
  i-th feature) and row i of `W` (where input direction i lands) are one
  colour: 1 teal, 2 blue, 3 gold (`VEC.SLOT`). `Y`'s digits are white.
  Magenta is the one hero.
- **Top (y 236–516):** `W  (3, 2)` labelled at y 236, its rows from
  y 312, centred at x 440, over the gap between `X` and `Y`. In beats 7–9
  the bias `b` sits at the top right, directly above `Y`'s two columns
  (cells at x 620–920, y 312, label `b  (2,)` at y 236), so broadcasting
  is a straight slide down.
- **Middle (y 556–972):** labels `X  (5, 3)` and `Y  (5, 2)` at y 556;
  `X` (cells 100 px, x 100–400) at the left, `Y` (cells 150 px, x 620–920)
  at the right, rows at y 632 + 68 px each, so row i of `X` and row i of
  `Y` share a line. A dim `→` per row in the gap between them (x 510).
- **The code card (the code beat, runbook step 1 "Show the code"):** one
  card for the whole Short, centred, top at y 1012, sharing the band top
  as ep03's code cards did (bottom ≤ 1330; `assemble.py --captions-anchor
  bottom`, every caption one line). Line 1 is `Y = X @ W`, and gains
  `+ b` on "the bias" (beat 7). In beat 6 the card grows a comment line,
  `# (5,3) @ (3,2) → (5,2)`, on "five by three at three by two gives five
  by two"; in beat 8 the comment becomes `# (batch,seq,3) @ (3,2)`. The
  tuples have no space after the comma because 60 px monospace holds ~24
  columns in the safe width (the comment is 23). The output is `Y`, not
  the `y` in SERIES.md's code-beat line, so the card and the matrix label
  agree.
- **`Y` is never pre-filled (Chris, 00_layout review).** Its brackets wait
  empty, and a row of `Y` appears only when that row's computation runs,
  one row at a time. Whenever the batch goes through `W` (beats 1 and 5),
  `Y` is built row by row.
- **The sweep:** a row "goes through W" as: a magenta box round row i of
  `X`; its three numbers flash in turn with `W`'s matching rows (the
  weighting; in beat 5 the weights also sit at `W` as `1 ×`, `2 ×`,
  `−1 ×`); its `→` turns magenta; row i of `Y` fills, first number then
  second (the two column sums, each popping in over 0.15 s from scale 1.3,
  magenta, settling to white); box and `→` return to rest. The row being
  computed is the hero.

## Ledger (identical in every beat; constants in `_ep/ep06.js`)

The `(5, 3) @ (3, 2)` example from `batched_linear_map_tensors.py`, shared
by episodes 3–6: row 1 of `X` is ep04's `x`, `W` is ep04's `W` (and ep05's
`weight.T`), row 1 of `Y` is ep04's `[ 4.1, −1.2 ]`. Row-vector (PyTorch)
convention: `X @ W`, rows of `W` are where input directions land.

| What | Value | In `ep06.js` |
|---|---|---|
| X `(5, 3)`, a batch of five input rows | `[ 1, 2, −1 ]`, `[ 0, −1, 3 ]`, `[ 2, 0.5, 1 ]`, `[ −1, 1, 2 ]`, `[ 3, −2, 0 ]` | `EP.X` |
| W `(3, 2)`, the map | rows `(2, −1)`, `(0.5, 1)`, `(−1, 2)` | `EP.W` |
| X @ W `(5, 2)` | `[ 4, −1 ]`, `[ −3.5, 5 ]`, `[ 3.25, 0.5 ]`, `[ −3.5, 6 ]`, `[ 5, −5 ]` | `EP.XW` |
| b `(2,)` | `[ 0.1, −0.2 ]` | `EP.B` |
| Y = X @ W + b `(5, 2)` | `[ 4.1, −1.2 ]`, `[ −3.4, 4.8 ]`, `[ 3.35, 0.3 ]`, `[ −3.4, 5.8 ]`, `[ 5.1, −5.2 ]` | `EP.Y` |
| Row 1, worked (beat 5) | 1 × `(2, −1)` + 2 × `(0.5, 1)` + −1 × `(−1, 2)` = `[ 4, −1 ]` | |
| Row 2, worked (beat 5) | 0 × `(2, −1)` + −1 × `(0.5, 1)` + 3 × `(−1, 2)` = `[ −3.5, 5 ]` | |
| Code, line 1 | `Y = X @ W`; from beat 7, `Y = X @ W + b` (monospace) | `parts().card.line1` |
| Code, comment | `# (5,3) @ (3,2) → (5,2)` (beats 6–7, 9) | `parts().card.shapes` |
| Code, real data | `# (batch,seq,3) @ (3,2)` (beat 8) | `parts().card.big` |
| Labels | `X`, `W`, `Y`, `b` (Inter 800) with shapes `(5, 3)`, `(3, 2)`, `(5, 2)`, `(2,)` in `--dim`; tags `data` (teal) and `map` (magenta) | `parts().names` |

## States (what each beat opens and ends on)

`P = EP.parts(root)` once; `EP.state(P, g, NAME)` at the top of `render(t)`;
a beat then draws only what differs.

- **INPUTS:** card `Y = X @ W`; `W`, `X`, the `→`s, and `Y`'s label and
  empty brackets (no digits). No `b`. No highlight.
- **PRODUCT:** INPUTS + `Y`'s digits = `X @ W` (white).
- **SHAPES:** PRODUCT; the card has its comment `# (5,3) @ (3,2) → (5,2)`
  (`#` and the two inner `3`s `--dim`, "they disappear"; `--muted` fails
  `check`'s 3:1 contrast).
- **CANON** (`00_layout` A): SHAPES with line 1 `Y = X @ W + b`; `b` above
  `Y`; `Y`'s digits = the biased outputs.
- **BIG:** CANON with the comment `# (batch,seq,3) @ (3,2)`, its `3`
  magenta.

## Final beats (the contract)

`vo_final.wav` is 49.837 s. Every cut sits in a pause of at least 0.4 s.
Beat-local t = master − start. Cue times from `words.json` (master).

| # | Folder | Master start | Length | Opens on | Ends on | VO |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 6.35 | (frame 0: the sweep already running) | PRODUCT | One line of PyTorch pushes a whole batch through a layer because X is data and W is the map. |
| 2 | `02_rows` | 6.35 | 3.75 | PRODUCT | INPUTS | X is five rows. Each row is one input vector with three features. |
| 3 | `03_map` | 10.10 | 2.95 | INPUTS | INPUTS | W is the map from three dimensions to two. |
| 4 | `04_roles` | 13.05 | 7.90 | INPUTS | INPUTS | X and W are both matrices, but they play different roles. X is data, which is a stack of vectors here. W is a transformation. |
| 5 | `05_sweep` | 20.95 | 9.80 | INPUTS | PRODUCT | So X at W does the same thing to every row. Row one of X weights the rows of W and sums. Then row two, then all five in parallel. |
| 6 | `06_shapes` | 30.75 | 6.60 | PRODUCT | SHAPES | This five by three at three by two gives five by two. The inner dimensions have to match, and then they disappear. |
| 7 | `07_bias` | 37.35 | 2.40 | SHAPES | CANON | Then the bias broadcasts across every row. |
| 8 | `08_bigger` | 39.75 | 5.45 | CANON | BIG | Real data just makes this bigger. There's a batch, there's a sequence, there's features. The last dimension is always the vector. |
| 9 | `09_close` | 45.20 | 4.637 | BIG | CANON | It's the same learned map in that matrix, applied to many vectors. |

## Beats (the visual brief)

| # | Folder | Hero | Visual |
|---|---|---|---|
| 1 | `01_hook` | the code line, then the row going through `W`, then `W` | Built part by part (Chris, first watch). Frame 0: only the code card `Y = X @ W`, alone in the middle of the stage at about 1.6× size, typing in from frame 0 and complete by "PyTorch" (1.19). "pushes" (1.60): the card shrinks and slides down to its slot (y 1012, scale 1; ≥ 0.6 s). "whole batch" (2.08–2.42): `X` builds in, label then rows dropping in top to bottom. "through a layer" (2.63–3.04): `W` builds in (label, brackets, rows), then `Y`'s label, empty brackets and the `→`s. Then the sweep: rows 1–5 go through `W` one at a time, faster each time, `Y` filling row by row (first number then second), all done before "W is the map". "X is data" (~3.65): `X`'s brackets teal and the tag `data`. "W is the map" (~4.5–5.7): `W`'s brackets magenta and the tag `map`. Tags and brackets back to rest before the still. Ends PRODUCT, still. |
| 2 | `02_rows` | the row being counted, then row 1 | Opens PRODUCT. First 0.4 s: `Y`'s digits fade (empty brackets stay). "five rows" (6.92–7.13): `X`'s five rows pulse top to bottom (fast). "each row is one input vector" (7.45–8.55): a magenta box round row 1. "three features" (9.21–9.52): row 1's three numbers swell in turn (teal, blue, gold), and the `3` in `(5, 3)` brightens. Box and swell gone by 3.5. Ends INPUTS. |
| 3 | `03_map` | `W` | Opens INPUTS. "W is the map" (10.24–10.97): a magenta box round `W`. "three dimensions" (11.45): `W`'s three rows pulse in turn in their colours and the `3` in `(3, 2)` brightens. "to two" (12.50): `W`'s two columns pulse and the `2` brightens. Box gone by 2.7. Ends INPUTS. |
| 4 | `04_roles` | first both brackets (white), then `X`'s stack, then `W` | Opens INPUTS. "both matrices" (13.97–14.17): `X`'s and `W`'s brackets brighten together (white, not magenta). "different roles" (15.22–15.68): they drift apart in colour: `X`'s brackets teal, `W`'s `--dim`. "X is data" (16.40–16.62): tag `data` (teal) after `X  (5, 3)`. "a stack of vectors" (17.64–18.08): a thin teal box draws round each of `X`'s five rows in turn, top to bottom (one stack). "W is a transformation" (19.08–19.90): `X`'s boxes go; tag `map` (magenta) after `W  (3, 2)` and `W`'s brackets magenta. All tags and colours back to rest in the last 0.6 s. Ends INPUTS. |
| 5 | `05_sweep` | the active row (its box, the weights at `W`, its `Y` row) | Opens INPUTS. "the same thing to every row" (22.31–23.39): every `→` pulses once, top to bottom. "Row one of X" (23.99–25.00): magenta box round row 1 of `X`. "weights the rows of W" (25.33–26.67): copies of `1`, `2`, `−1` fly from row 1 to just left of `W`'s three rows, as `1 ×`, `2 ×`, `−1 ×` in their row colours, each `W` row pulsing as its weight lands (≥ 0.6 s). "and sums" (27.34): row 1's `→` magenta and `Y` row 1 fills `[ 4, −1 ]`. "Then row two" (28.12–28.71): the box moves to row 2; the weights retype `0 ×`, `−1 ×`, `3 ×`; `Y` row 2 fills `[ −3.5, 5 ]`. "all five in parallel" (29.30–30.19): the weights fade, boxes on rows 3–5 at once (magenta on all three), their `→`s light, and `Y` rows 3, 4, 5 fill in a quick cascade (0.12 s apart, each first number then second) so every row is still seen being computed. Boxes back to rest by 9.4. Ends PRODUCT. |
| 6 | `06_shapes` | the code card's comment (the code beat) | Opens PRODUCT. "This five by three" (30.88–31.62): the card grows its comment line (0.3 s) and `# (5,3)` types in, magenta, as `(5, 3)` in `X`'s label brightens. "at three by two" (31.87–32.62): ` @ (3,2)` types in, magenta, with `W`'s label. "gives five by two" (32.86–33.77): ` → (5,2)` types in, magenta, with `Y`'s label; the whole comment is magenta on "two". "The inner dimensions" (34.65–34.98): the comment goes back to `--text` and the two inner `3`s get a magenta box each. "have to match" (35.83): a magenta line joins the two boxes under the comment. "and then they disappear" (36.62): boxes and line go, the two `3`s fade to `--dim`, the outer `(5,` and `2)` pulse. Ends SHAPES. |
| 7 | `07_bias` | `b` (with the card's `+ b`) | Opens SHAPES. "Then the bias" (37.57–38.04): ` + b` types into the card's line 1, magenta (the card widens and re-centres), and `b` with `[ 0.1, −0.2 ]` fades in above `Y`. "broadcasts across every row" (38.28–39.07): five copies of `b`'s two numbers slide down `Y`'s columns, one per row (≥ 0.6 s, slight stagger), and as each lands that row's digits retype to the biased output. `+ b` to `--text` and `b` to rest by 2.2. Ends CANON. |
| 8 | `08_bigger` | the last dimension (`3`, with one row of `X`) | Opens CANON. "makes this bigger" (40.47–40.91): the comment becomes `# (5,3) @ (3,2)` (the ` → (5,2)` goes). "a batch" (41.63): it retypes as `# (batch,5,3) @ (3,2)` (`card.big`, with "seq" reading `5`). "a sequence" (42.26): `5` retypes as `seq`. "features" (42.82): the `3` turns magenta. "The last dimension is always the vector" (43.40–44.62): a magenta box round row 1 of `X` (three numbers = one vector), and the `3` in `W`'s `(3, 2)` pulses. Box gone by 5.0; the `3` in the comment stays magenta. Ends BIG. |
| 9 | `09_close` | `W`, then all five rows | Opens BIG. First 0.5 s: the comment cross-fades back to `# (5,3) @ (3,2) → (5,2)`. "the same learned map in that matrix" (45.94–47.70): a magenta box round `W`. "applied to many vectors" (48.02–48.90): the box goes and all five `→`s light at once, with a teal box round each of `X`'s rows. Back to rest by 4.0; last 0.6 s still on CANON: the frame episode 7 can open on (`W` then splits into two stacked layers). |

Beat boundaries sit in the pauses (silencedetect −35 dB on `vo_final.wav`).
Place exact cues from `words.json` and check the ones that matter on a 50 ms
RMS envelope of your window.

## Cut list (runbook step 5)

`vo_raw.m4a` (55.1 s; recorded clean in the 2026-10-09 session, as ep04–05)
→ `vo_clean.wav` (loudnorm only) → `vo_final.wav` (49.8 s):
`tools/tighten_vo.py --max-gap 0.25` with no `--remove`.

- **No flubbed or repeated phrase in the take.** Nothing removed.
- Pauses capped at 0.25 s (the longest, 2.2 s after "all five in parallel",
  and 1.4 s after "they disappear").
- The "if time" line ("Real data just makes this bigger…") fits and stays.
- Both code-beat lines survive the cut: "This five by three at three by two
  gives five by two" at 30.88–33.77 and "Then the bias broadcasts across
  every row" at 37.57–39.47 (master, `vo_final.wav`).
- Re-transcribed `vo_final.wav`: no fragments at the joins.
- Whisper's spellings fixed in `words.json`: "waits" → "weights", "add" →
  "at". "X's data" is how Whisper hears "X is data"; captions will say
  "X is data".

Approval: Chris, 2026-10-11 (cut list and 00_layout look, no plane; `Y` fills row by row).
