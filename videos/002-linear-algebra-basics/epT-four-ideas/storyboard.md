ENGINE: hyperframes

# Ep T. The four ideas (trailer) — storyboard

**Series:** Linear Algebra for AI Engineers, the trailer (`../SERIES.md`).
**Title:** Linear Algebra for AI Engineers: The 4 Ideas
**Search phrase:** linear algebra for ai engineer (`../SERIES.md`, trailer)

Engine: HyperFrames (the default, `AGENTS.md` "Which engine"). Every beat is
the flat 2D plane, arrows, dots and small matrices; nothing needs Manim's
plotted axes or 3D camera.

## Preflight

- **THE QUESTION:** How much linear algebra do I need for AI?
- **WHO IS ASKING:** an engineer who writes `nn.Linear` and `x @ W`, has
  watched 3Blue1Brown, and wonders how much of a linear algebra course they
  actually need before a forward pass makes sense.
- **THE ANSWER IN ONE SENTENCE:** Four ideas: vectors hold information,
  and matrices are learned moves that reshape it.
- **THE SEARCH PHRASE:** linear algebra for ai engineer (offered by YouTube
  autocomplete; `../SERIES.md`). VO line 1 says "linear algebra" and "AI"
  ("You only need four ideas from linear algebra to understand what AI
  models are doing."). It answers the question, so no recut.
- **Code beat:** `y = x @ W` on "In PyTorch, x at W is just that" (beat 5),
  then the weights `3 ×`, `2 ×` and the sum `[ 2, 4 ]` on "Each number in x
  weights a row of W and adds them up".

## The look

Rendered in `00_layout/` (`media/hf/00_layout_sheet.png`, one rest state
per second; `00_layout_TILES.png`, `00_layout_CANON.png`). The code is
`../../../_shared/web/vec/vec.js` (the shared plane kit, linked as `vec/`)
plus this episode's `_ep/epT.js` (linked as `ep/`): the ledger, where things
sit, the views and the rest states.

- **The hook is a montage of four tiles** (SERIES.md: hero frames from
  1, 3, 4 and 10). A 2 × 2 grid of panels fills the stage (430 × 400 px
  each, y 240–1065), each a small plane with its own camera, labelled
  `vector`, `matrix`, `x @ W` (monospace) and `dot product` (60 px):
  1. x = (3, 2) as its recipe legs, then the arrow;
  2. e1 and e2 swinging to W's rows;
  3. the new recipe walking to x @ W = (2, 4);
  4. b turning against a.
  At rest no tile has magenta. The lit tile (its frame, label and hero
  element) is the one magenta hero.
- **One running example for ideas 1–3**, ep03's numbers: x = [ 3, 2 ],
  W = [[1, 0.5], [−0.5, 1.25]], x @ W = [ 2, 4 ]. Tile 1 grows into the MAIN
  plane in beat 2 (`VEC.view` from the tile's camera to MAIN, and the clip
  from the tile to the plane rectangle), and beats 2–5 keep that plane.
- **The strip (top, y 236–556):** names at y 236 (`--dim`), numbers from
  y 312 in the series notation (bare numbers, one tall bracket pair, row
  colours teal and blue). `x` is at the top left (x 110–310) and `W  (2, 2)`
  at the top right (cells 160 px, x 600–920). In beat 5 the weights `3 ×`
  and `2 ×` sit left of W's rows, and the sum `[ 2, 4 ]` (magenta) sits
  under W with `x @ W` (monospace) to its left.
- **MAIN plane:** 120 px a step, origin (320, 1070), clipped above y 566.
  It holds e1, e2, x (3, 2) and x @ W (2, 4). ep04 used 100 px and ep03
  160 px. 120 is the most that fits under the strip.
- **CENTER plane (beats 6–10):** 140 px a step, origin (507, 800), clipped
  above y 470. The strip above holds the readout `a · b = −5`, the token
  scores, or W1 W2 W3.
- **The code card** `y = x @ W` (monospace, `x` teal) sits at the band top
  (y 1115) in beat 5 only, as in ep03 and ep06. Captions are anchored to the
  band bottom for the whole Short (`assemble.py --captions-anchor bottom`).
- **Colour:** x and its legs: e1 / row 1 teal, e2 / row 2 blue; x itself is
  off-white (`--text`), as in ep03. Keys and token words are gold. Magenta
  is the one hero per beat (below). Retired things go `--muted`.

## Ledger (identical in every beat; constants in `_ep/epT.js`)

Row-vector (PyTorch) convention: `x @ W`, row i of W is where input
direction i lands.

| What | Value | In `epT.js` |
|---|---|---|
| The vector | x = `[ 3, 2 ]`: 3 of e1 plus 2 of e2 | `EP.X` |
| Old recipe | 3 teal hops of (1, 0), then 2 blue hops of (0, 1) | `EP.LEGS_OLD` |
| The matrix | W `(2, 2)`: row 1 `[ 1, 0.5 ]` (where e1 lands), row 2 `[ −0.5, 1.25 ]` (where e2 lands); ep03's draft numbers | `EP.W` |
| New recipe | 3 teal hops of (1, 0.5), then 2 blue hops of (−0.5, 1.25) | `EP.LEGS_NEW` |
| x @ W | `[ 2, 4 ]` = 3 × `[ 1, 0.5 ]` + 2 × `[ −0.5, 1.25 ]` = `[ 3, 1.5 ]` + `[ −1, 2.5 ]` | `EP.XW`, `EP.ROWS_W` |
| Code | `y = x @ W` (monospace) | `P.card` |
| Dot product | a = (2, 1) fixed (teal); b the same length, turning from aligned to opposed (blue); `a · b` reads 5 → 0 → −5 (whole numbers) | `EP.A`, `EP.bAt(u)` |
| Attention | one token's query q = (2, 1) (= a, teal, tip "q"); keys of the tokens `the` (−1, 2), `cat` (1, 2), `sat` (1, −1) (gold); scores q · k = `0`, `4`, `1`; `cat` (4) is the hero. Strip: `q · k` with the tokens over their scores | `EP.Q`, `EP.TOKENS`, `EP.KEYS`, `EP.SCORES` |
| Layers | `W1`, `W2`, `W3`, each (2, 2), untrained = `[[1, 0], [0, 1]]` (white digits) | `P.layers` |
| Training W1 | amplify e1 `[[2, 0], [0, 1]]` → ignore e2 `[[2, 0], [0, 0.2]]` → mix `[[2, 1], [0, 0.2]]` = W1 trained (`AMP @ IGN @ MIX`). The ring of 16 teal dots (unit circle) follows | `EP.AMP`, `EP.IGN`, `EP.MIX`, `EP.W1T`, `EP.ring` |
| The easier task | 14 dots, 7 teal and 7 gold, split by a thin diagonal gap; the learned move `EP.EASY` widens the gap and stands it upright; the boundary is a magenta dashed line | `EP.CLASSES`, `EP.EASY`, `EP.classes` |

## States (what each beat opens and ends on)

`P = EP.parts(root)` once, then `EP.state(P, g, NAME)` at the top of
`render(t)`. A beat then draws only what differs (`EP.plane(g, o)` takes
the MAIN knobs; `EP.centre(g)` draws the CENTER grid and returns a `done()`
that closes the clip).

- **TILES:** the four tiles at rest, no magenta.
- **VECTOR:** MAIN; strip `x`; plane with e1 and e2 at home (labelled), the
  old recipe legs, and x (off-white).
- **LANDED:** strip `x`, `W`. e1 and e2 landed (muted ghosts at home), the
  moved lattice at 0.35, magenta landing spots; old recipe and x at 0.35,
  x muted.
- **REBUILT:** LANDED without spots; the new recipe legs and x @ W (magenta).
- **CODE:** REBUILT plus the weights, the sum `[ 2, 4 ]` (magenta), `x @ W`
  and the card `y = x @ W`.
- **DOT:** CENTER; `a · b = −5` (magenta number); a and b opposed, tips "a",
  "b".
- **ATTN:** CENTER; q and three keys with their token tips; `cat`'s arrow,
  tip and score magenta.
- **LAYERS:** CENTER; strip W1 W2 W3 (identity); the ring of dots; a magenta
  box on W1.
- **TRAINED:** LAYERS with W1 = `[[2, 1], [0, 0.2]]` (magenta digits); W2 and
  W3 digits `--dim`; the ring through W1 (a thin tilted ellipse); e1 and e2
  at W1's rows (teal, blue).
- **EASY:** CENTER; the classes moved by EASY, the magenta dashed line
  upright. The strip is empty.
- **CANON:** the last frame. MAIN; strip `x`, `W`; plane with the lattice,
  e1 and e2 landed with their ghosts, x's ghost (muted), and x @ W (magenta).
  It is REBUILT without the legs.

## Final beats (the contract)

`vo_final.wav` is 45.831 s. Every cut sits in a pause of at least 0.39 s.
Beat-local t = master − start. Cue times come from `words.json` (master).

| # | Folder | Master start | Length | Opens on | Ends on | VO |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.000 | 4.225 | (frame 0: the tiles already moving) | TILES | You only need four ideas from linear algebra to understand what AI models are doing. |
| 2 | `02_vector` | 4.225 | 5.125 | TILES | VECTOR | A vector is a move. Its numbers are the recipe, amounts along directions that we all agreed on. |
| 3 | `03_matrix` | 9.350 | 2.690 | VECTOR | LANDED | A matrix says where those directions land. |
| 4 | `04_rebuild` | 12.040 | 3.210 | LANDED | REBUILT | Multiplying rebuilds that recipe in the new directions. |
| 5 | `05_code` | 15.250 | 5.790 | REBUILT | CODE | In PyTorch, x at W is just that. Each number in x weights a row of W and adds them up. |
| 6 | `06_dot` | 21.040 | 2.450 | CODE | DOT | A dot product measures alignment. |
| 7 | `07_attention` | 23.490 | 4.210 | DOT | ATTN | Attention scores are dot products between queries and keys of your tokens. |
| 8 | `08_layers` | 27.700 | 3.910 | ATTN | LAYERS | In a neural network, those matrices are learned, layer by layer. |
| 9 | `09_train` | 31.610 | 4.270 | LAYERS | TRAINED | Training finds which directions to amplify, which to ignore, and which ones to mix. |
| 10 | `10_easier` | 35.880 | 4.460 | TRAINED | EASY | The model doesn't understand in a human way, it learns moves that make the task easier. |
| 11 | `11_close` | 40.340 | 5.491 | EASY | CANON | Vectors hold information, matrices reshape it into the forms the model can use. |

## Beats (the visual brief)

| # | Hero | Visual |
|---|---|---|
| 1 | each tile in turn | Frame 0: all four tiles on screen, each already mid-motion, staggered so something is always moving (tile i's progress u runs 0 → 1 over about 1.2 s, starting at −0.3, 0.1, 0.5 and 0.9 s, so tile 1 is already in motion at frame 0). "four ideas" (1.12–1.74): the tiles light magenta in turn, 1 → 4, about 0.15 s apart, each back to rest as the next lights (frame, label, hero element). Then "linear algebra" … "AI models are doing": every tile at rest by 3.6. Ends TILES, still. |
| 2 | x (the move), then the legs | Opens TILES. "A vector" (4.44–4.56): tiles 2–4 fade and tile 1 grows into the MAIN plane (camera and clip together, ≥ 0.8 s, done by ~5.4); its frame and label fade. "is a move" (4.94–5.10): x turns magenta. "Its numbers" (5.58–6.12): `x  [ 3, 2 ]` fades in at the top left; x back to off-white. "are the recipe" (6.12–6.50): the 3 and the 2 swell once. "amounts along directions" (7.10–7.72): the old recipe legs redraw hop by hop (`EP.recipe` u 0 → 1, ≥ 0.8 s), the 3 lighting with the teal hops and the 2 with the blue. "we all agreed on" (8.40–8.98): e1 and e2 at home light (alpha pulse), with their labels `e1`, `e2`. Ends VECTOR. |
| 3 | the landing spots (with W's row while its arrow moves) | Opens VECTOR. "A matrix" (9.58–9.66): `W  (2, 2)` fades in at the top right. "says where those directions" (10.12–10.97): the e1/e2 labels fade; e1 swings to (1, 0.5) while W's row 1 lights magenta, then e2 to (−0.5, 1.25) while row 2 lights (≥ 0.6 s each; muted ghosts stay home); the lattice fades in to 0.35; the old recipe and x go to 0.35, x muted. "land" (11.38): magenta spots ring onto both tips (pop). Ends LANDED. |
| 4 | the output x @ W | Opens LANDED. "Multiplying" (12.36): the spots fade. "rebuilds that recipe" (12.88–13.46): the new legs walk hop by hop (3 teal, then 2 blue, `EP.recipe` u 0 → 1, ≥ 1.2 s), the 3 in `x` lighting with the teal hops and the 2 with the blue. "in the new directions" (13.82–14.36): x @ W draws from the origin to (2, 4), magenta. Ends REBUILT. |
| 5 | the code line, then the weighted rows, then the sum | Opens REBUILT. "In PyTorch" (15.46–15.56): the card `y = x @ W` rises into the band top (y 1115), its `x @ W` magenta on "x at W" (16.47–16.67), back to white by "just that" (17.34). "Each number in x" (18.07–18.76): a magenta box round `x`. "weights" (19.06): copies of the 3 and the 2 fly from `x` to `3 ×` and `2 ×` beside W's rows (≥ 0.6 s), each row lighting as its weight lands; the box goes. "a row of W" (19.56–19.96): the two rows swell. "and adds them up" (20.10–20.62): the sum `[ 2, 4 ]` and `x @ W` appear under W (each number pops from 1.3 to 1), and the plane's x @ W arrow pulses with it. Ends CODE. |
| 6 | the number | Opens CODE. First 0.6 s: the strip, card and MAIN plane fade; the CENTER plane fades in (one cross-fade, ≥ 0.6 s). "A dot product" (21.50–21.78): a (teal) and b (blue, aligned with a) draw from the origin, and `a · b = 5` appears at the top. "measures alignment" (22.16–23.2): b turns from aligned to opposed (≥ 1 s) and the number ticks 5 → 0 → −5 (whole numbers, magenta). Ends DOT. |
| 7 | the brightest score (`cat`: its key and its 4) | Opens DOT. "Attention scores" (23.70–24.42): b and the readout fade; a's tip relabels `q`; `q · k` and the three token words fade in at the top. "dot products between queries" (24.64–25.64): q pulses. "and keys" (26.04–26.24): the three keys draw from the origin in gold, their tips labelled `the`, `cat`, `sat`. "of your tokens" (26.62–27.4): each key lights in turn as its score pops in under its token (`0`, `4`, `1`); `cat`'s arrow, tip and 4 stay magenta. Ends ATTN. |
| 8 | the layer being learned | Opens ATTN. "In a neural network" (27.88–28.6): the arrows, tips and scores fade; W1, W2 and W3 (identity, white) fade into the strip; the ring of 16 teal dots appears on the unit circle. "those matrices are learned" (28.92–29.66): all twelve numbers flicker once (a quick tick through nearby values and back, ≤ 0.6 s). "layer by layer" (30.55–31.02): a magenta box steps W1 → W2 → W3 and back to W1. Ends LAYERS. |
| 9 | W1 (box and digits) | Opens LAYERS. W2 and W3 dim (digits `--dim`); e1 and e2 appear as W1's rows (teal, blue) on the plane. "amplify" (33.28): W1 ticks to AMP; the ring stretches along e1 (≥ 0.6 s); row 1 lights. "ignore" (34.12): W1 ticks to AMP @ IGN; the ring flattens and e2 shrinks to (0, 0.2); row 2 lights. "mix" (35.20): W1 ticks to W1T `[[2, 1], [0, 0.2]]`; the ring shears into a tilted thin ellipse; e1 swings to (2, 1). W1's digits end magenta. Ends TRAINED. |
| 10 | the gap (the boundary) | Opens TRAINED. "The model doesn't understand" (36.14–37.2): the strip and ring fade; the two classes appear (teal and gold dots, thin diagonal gap, `EP.classes(g, I)`). "in a human way" (37.34–37.9): still. "it learns moves" (38.34–38.68): every dot rides the map I → EASY together (`EP.mlerp`, ≥ 1 s). "that make the task easier" (39.01–39.77): the magenta dashed boundary draws through the now-wide gap. Ends EASY. |
| 11 | x (vectors), then W with x @ W (matrices) | Opens EASY. First 0.5 s: the dots and line fade; the camera goes CENTER → MAIN. "Vectors" (40.54): x (3, 2) draws off-white with `x  [ 3, 2 ]` in the strip; "hold information" (40.84–41.6): x and its numbers pulse teal. "matrices" (42.28): `W  (2, 2)` fades in. "reshape it" (42.66–43.42): e1 and e2 swing to W's rows with the lattice, x rides `VEC.map(X, s)` to (2, 4) and turns magenta, leaving a muted ghost at (3, 2) (≥ 1 s). "into the forms the model can use": still. The last ~1.4 s is still on CANON: the frame ep01 can open on in the stitched long-form. |

Beat boundaries sit in the pauses (silencedetect −35 dB on `vo_final.wav`).
Place exact cues from `words.json` and check the ones that matter on a 50 ms
RMS envelope of your window.

## Cut list (runbook step 5)

`vo_raw.m4a` (49.6 s; recorded clean in the 2026-10-09 session) →
`vo_clean.wav` (loudnorm only) → `vo_final.wav` (45.8 s):
`tools/tighten_vo.py --max-gap 0.25 --remove 38.10-39.70`.

- **One flub, removed:** "The model doesn't, the model doesn't understand"
  becomes "The model doesn't understand". 38.10–39.70 s of `vo_clean.wav`
  (the first "The model doesn't," and a breath) is cut. The second take of
  the phrase starts at 39.80.
- Pauses capped at 0.25 s.
- Nothing else cut. The take matches the planned script except "that we all
  agreed on", "which ones to mix" and "of your tokens", which stay.
- Both code-beat lines survive the cut: "In PyTorch, x at W is just that"
  at 15.46–17.6 and "Each number in x weights a row of W and adds them up" at
  18.07–20.8 (master, `vo_final.wav`).
- Re-transcribed `vo_final.wav` (Parakeet, `transcript_final_text.txt`): no
  fragments at the join.
- Spellings fixed in `words.json`: "MOV." → "move.", "w" → "W" (twice). "In"
  (27.34 → 27.88) was pinned before the pause; it is moved to where the
  speech starts.

Approval: pending (cut list and 00_layout look).
