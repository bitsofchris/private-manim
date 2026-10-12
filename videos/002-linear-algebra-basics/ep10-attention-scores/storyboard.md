ENGINE: hyperframes

# Ep 10. Attention scores are dot products — storyboard

**Series:** Linear Algebra for AI Engineers, episode 10 (`../SERIES.md`).
**Title:** Attention Score Calculation | Linear Algebra for AI Engineers

Engine: HyperFrames (the default, `AGENTS.md` "Which engine"). Every beat is
code cards, small matrices in the series notation and 2D vectors on the flat
plane; nothing needs Manim's axes or 3D camera.

## Preflight

- **THE QUESTION:** What is an attention score?
- **WHO IS ASKING:** an engineer who writes `nn.Linear` and `x @ W`, has
  watched episodes 8–9 (the dot product measures alignment), and has seen
  `Q @ K.T` in a transformer without knowing what one number in it means.
- **THE ANSWER IN ONE SENTENCE:** A dot product between one token's query and
  another token's key; `Q @ K.T` is every pair at once.
- **THE SEARCH PHRASE:** `attention score calculation` (SERIES.md; offered by
  autocomplete). Not "query key": it completes to "query key value…", and
  this episode never covers Value. VO line 1 says "attention score".
- **Code beat:** `scores = Q @ K.T` on "Q @ K transpose does every pair at
  once" (beat 7); then `scores /= d**0.5` on "divide by the square root of
  the head size" and `w = scores.softmax(-1)` on "softmax turns each row into
  weights" (beat 8). `Q = X @ W_Q` and `K = X @ W_K` carry the code into
  beats 3–4. One line at a time: `scores = Q @ K.T / d**0.5` (25 characters,
  ~950 px at 60 px monospace) does not fit the safe width, so the card swaps
  lines rather than growing.

## The look

Rendered in `00_layout/`. The code is `../../../_shared/web/vec/vec.js` (the
shared plane kit, linked as `vec/`) plus this episode's `_ep/ep10.js` (linked
as `ep/`): the ledger, where things sit, the token arrows and the rest states.

- **Top (y 236–700): the numbers.** The code card at y 236, centred, one
  line. Below it a block whose rows are the three tokens: a word column
  (`my`, `name`, `is`, right-aligned at x 236, each in its token colour),
  then either two 3 × 2 matrices side by side (`X`/`Q` at left 286, `W_Q`/
  `W_K`/`K` at left 626; names above in `--dim` at y 372) or the 3 × 3 score
  grid (left 286, 160 px cells; key words across the top at y 372 in their
  token colours, so rows are queries and columns are keys). Digits from y
  450, 72 px rows, 60 px, one tall bracket pair per matrix.
- **Bottom (y 700–1100): the plane.** 165 px a step, origin (215, 1075),
  first quadrant (every vector here is in it), clipped above y 700. Right of
  it (x 640–950, from y 850) is the readout zone: the dot product `1·2 + 2·2 = 6` in
  beats 5–6.
- **Tokens are rows, coloured** (`VEC.SLOT`: `my` teal, `name` blue, `is`
  gold): the word, its matrix row, its arrow. A query is a **solid** arrow, a
  key an **outline** arrow (`EP.keyArrow`), so one colour can be both. X's
  arrows are solid too: W_Q moves them into the queries; they leave muted
  ghosts for W_K.
- **Magenta, one at a time:** `W_Q` then `W_K` while each acts; then the
  dot product's result `6`, which becomes the hero cell (query `name`, key
  `is`) and stays the hero to the end (4.2 scaled, 0.8 as a weight).
- Row-vector convention throughout: tokens are rows of `X`; `Q = X @ W_Q`.
  SERIES.md's frame 0 says "token columns"; here they are rows (the series
  rule wins), and the transpose is shown as the key words turning from the
  column into the header row.

## Ledger (identical in every beat; constants in `_ep/ep10.js`)

Chris's own worked example, `unit_05_attention_scores.ipynb` (T = 3,
d_model = d_head = 2). Token words are the channel's transformer example
(`ISO.TOKENS`, 005 and 009).

| What | Value | In `ep10.js` |
|---|---|---|
| tokens | `my`, `name`, `is` (teal, blue, gold) | `EP.TOK` |
| X, the token vectors | `[[1, 0], [1, 1], [0, 2]]`, shape `(3, 2)` | `EP.X` |
| W_Q | `[[1, 1], [0, 1]]` | `EP.WQ` |
| W_K | `[[1, 0], [1, 1]]` | `EP.WK` |
| Q = X @ W_Q | `[[1, 1], [1, 2], [0, 2]]` | `EP.Q` |
| K = X @ W_K | `[[1, 0], [2, 1], [2, 2]]` | `EP.K` |
| scores = Q @ K.T | `[[1, 3, 4], [1, 4, 6], [0, 2, 4]]`, shape `(3, 3)` | `EP.S` |
| the hero pair | query `name` (1, 2) · key `is` (2, 2) = `1·2 + 2·2 = 6`; row 1, column 2 | `EP.HERO` |
| head size d | 2, so ÷ √2 | `EP.D` |
| scaled, one decimal | `0.7 2.1 2.8` / `0.7 2.8 4.2` / `0 1.4 2.8` | `EP.SS` |
| softmax weights, one decimal | `0.1 0.3 0.6` / `0.0 0.2 0.8` / `0.0 0.2 0.8` (each row sums to 1.0; two decimals would not: row 3 rounds to 1.01) | `EP.WT` |
| Code | `Q = X @ W_Q`; `K = X @ W_K`; `scores = Q @ K.T`; `scores /= d**0.5`; `w = scores.softmax(-1)` | `EP.CODE` |

## States (what each beat opens and ends on)

`P = EP.parts(root)` once; `EP.state(P, g, NAME)` at the top of `render(t)`;
a beat then draws only what differs.

- **GRID:** card `scores = Q @ K.T`; word column, key headers, the raw score
  grid, `6` magenta, shape `(3, 3)` above the word column. Plane: query `name`
  (solid) and key `is` (outline) at full alpha with tip labels, the other
  queries and keys at 0.22.
- **TOKENS:** no card; word column, `X` at the left slot (name `X`). Plane:
  the three X arrows (solid, token colours).
- **QUERIES:** card `Q = X @ W_Q`; `Q` at the left slot. Plane: X's ghosts
  (muted, 0.5) and the three queries.
- **QK:** card `K = X @ W_K`; `Q` and `K` side by side. Plane: queries solid,
  keys outline, all full.
- **PAIR:** QK with the `name` row of Q and the `is` row of K boxed (`--dim`
  hbox); the other arrows at 0.22, tip labels on the pair; readout
  `1·2 + 2·2` (q digits blue, k digits gold) over `= 6` (magenta).
- **WEIGHTS:** GRID with card `w = scores.softmax(-1)`, the weights in the
  grid (`0.8` magenta) and `= 1` (`--dim`) right of each row.
- **PULL:** WEIGHTS with the `name` row boxed and the plane's keys at alpha
  0.15 + 0.85 × `name`'s weight (`is` near full, `my` faint).

## Final beats (the contract)

`vo_final.wav` is 51.01 s. Every cut sits in the middle of a 0.25 s pause.
Beat-local t = master − start. Word times: `words.json` (WhisperKit, master
seconds): check every cue that matters on a 10–50 ms RMS envelope of your
window.

| # | Folder | Master start | Length | Opens on | Ends on | VO |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 5.50 | (frame 0: already moving) | GRID | An attention score is just a dot product between one token's query and another token's key. |
| 2 | `02_tokens` | 5.50 | 1.93 | GRID | TOKENS | Every token starts as a vector. |
| 3 | `03_query` | 7.43 | 6.22 | TOKENS | QUERIES | A learned matrix, W_Q, moves each one into a query, which is the question this token asks. |
| 4 | `04_key` | 13.65 | 6.77 | QUERIES | QK | Another matrix, W_K, moves each one into a key. What question can this token help answer? |
| 5 | `05_pair` | 20.42 | 4.86 | QK | PAIR | To score one pair, you take one token's query and another token's key and do the dot product. |
| 6 | `06_aligned` | 25.28 | 3.69 | PAIR | PAIR | High value here means they're aligned. This token has what the other one is looking for. |
| 7 | `07_grid` | 28.97 | 5.52 | PAIR | GRID | Q @ K transpose does every pair at once. 3 tokens, a 3-by-3 grid of scores. |
| 8 | `08_softmax` | 34.49 | 5.80 | GRID | WEIGHTS | Then divide by the square root of the head size, and softmax turns each row into weights that add up to one. |
| 9 | `09_parallel` | 40.29 | 6.12 | WEIGHTS | PULL | Transformers process every position in parallel. Attention is how tokens decide who to pull information from. |
| 10 | `10_close` | 46.41 | 4.60 | PULL | GRID | And attention scores measure which tokens are aligned under these learned projections. |

Mid-Short beats end on ≥ 5 still frames; only beat 10 holds ≥ 0.8 s still.

## Beats (the visual brief)

| # | Folder | Hero | Visual |
|---|---|---|---|
| 1 | `01_hook` | the `6` cell | Frame 0: GRID with the `name` row's three cells empty and the plane showing query `name` and all three keys (keys at 0.6), something already moving. Query `name` fans to the keys in turn: a dim connector from its tip to each key's tip, that key brightens, and its dot product fills the cell: `my` → `1` (~0.3), `name` → `4` (~1.6). "query" (3.58): query `name` pulses. "key" (5.03): key `is` brightens and `6` lands in its cell, magenta (pop ≤ 0.3 s). Keys `my` and `name` settle to 0.22 (and the other queries are at 0.22 throughout). Last 5 frames GRID. |
| 2 | `02_tokens` | none | Opens GRID. One cross-fade (≤ 0.6 s): card, grid, headers and shape out; `X` in at the left slot with its name; the plane's arrows out. "vector" (~1.36 local): the three X arrows grow from the origin together (≥ 0.5 s). Ends TOKENS. |
| 3 | `03_query` | `W_Q` | Opens TOKENS. "A learned matrix, W_Q" (8.62): `W_Q` fades in at the right slot, digits magenta, name `W_Q`; the card types on `Q = X @ W_Q`. "moves each one into a query" (9.28–11.24): the arrows ride from X to Q (`EP.lerp2`, ≥ 1.2 s) leaving muted ghosts at X; on the same move X's digits tick to Q's and the name `X` becomes `Q` (`my` and `is` rows: row `is` does not move, (0, 2) @ W_Q = (0, 2)). "the question this token asks" (12.3–13.06): the three query heads pulse once. W_Q fades out before the hold. Ends QUERIES. |
| 4 | `04_key` | `W_K` | Opens QUERIES. "Another matrix, W_K" (14.94): `W_K` fades in at the right slot, digits magenta, name `W_K`; card → `K = X @ W_K`. "moves each one into a key" (15.88–17.20): outline arrows ride from the X ghosts to K (≥ 1.2 s; key `my` stays at (1, 0)); the ghosts fade; `W_K` cross-fades into `K` (digits white, name `K`). "What question can this token help answer?" (17.92–19.84): the three keys pulse in turn, `my`, `name`, `is`. Ends QK. |
| 5 | `05_pair` | the readout's `6` | Opens QK. "To score one pair" (20.78): every arrow but query `name` and key `is` fades to 0.22. "one token's query" (22.45): Q's `name` row boxed, tip label `name` beside the query. "another token's key" (23.57): K's `is` row boxed, tip label `is`. "do the dot product" (24.54): the readout builds right of the plane, `1·2 + 2·2` (each digit flies from its matrix row), then `= 6` lands magenta. Ends PAIR. |
| 6 | `06_aligned` | `6` | Opens PAIR. "High value" (25.50): `6` pulses. "they're aligned" (26.44): a `--dim` wedge (arc) opens between query `name` and key `is` at the origin, about 18°. "This token has" (26.82–27.24): key `is` and its label pulse; "looking for" (28.32): query `name` and its label pulse. The wedge fades before the hold. Ends PAIR. |
| 7 | `07_grid` | the `6` cell | Code beat. Opens PAIR. "Q @ K transpose" (29.30–29.66): the card → `scores = Q @ K.T`; the matrices fade; the word column stays (rows = queries) while a copy of it turns into the header row above the grid columns (the transpose, ≥ 0.6 s). "every pair at once" (30.66–31.08): all nine cells pop in together, and the readout's `6` flies into row `name`, column `is` (magenta); the readout's rest fades; row boxes go. "3 tokens" (32.26): the row words pulse. "3-by-3 grid of scores" (33.07–33.84): `(3, 3)` fades in. Ends GRID. |
| 8 | `08_softmax` | the `6` cell, now `4.2`, then `0.8` | Code beat. Opens GRID. "divide by the square root of the head size" (34.92–36.58): card → `scores /= d**0.5`; `÷ √2` (`--dim`) beside the grid; all cells tick to the scaled values (≥ 0.6 s). "softmax" (37.20): card → `w = scores.softmax(-1)`; `÷ √2` goes. "turns each row into weights" (37.81–38.83): the rows tick to weights one after another (0.2 s stagger). "add up to one" (39.42–39.84): `= 1` fades in right of each row. Ends WEIGHTS. |
| 9 | `09_parallel` | `0.8` | Opens WEIGHTS. "every position in parallel" (41.58–42.24): the three rows box together (`--dim`) and their row words pulse at once. "Attention is how tokens decide" (42.80–43.94): the boxes on `my` and `is` go; `name` stays boxed. "who to pull information from" (44.36–45.76): on the plane the keys' alphas move to `name`'s weights (key `is` near full, `name` 0.32, `my` 0.15) and a short dim pull mark runs from key `is`'s tip toward query `name`'s. Ends PULL. |
| 10 | `10_close` | `6` | Opens PULL. "And attention scores" (46.70–46.98): card → `scores = Q @ K.T`, the grid ticks back to the raw scores, `= 1` labels go, the row box goes. "which tokens are aligned" (48.64): keys back to GRID alphas; `6` pulses once. "under these learned projections" (49.02–49.82): the tip labels brighten once. Last ≥ 0.8 s still on GRID. |

## Cut list (runbook step 5)

`vo_raw.m4a` (55.2 s; same Studio Sound session as ep01–09, so loudnorm only)
→ `vo_clean.wav` → `vo_final.wav` (51.01 s):
`tools/tighten_vo.py --max-gap 0.25`, no `--remove`.

- **No phrase removed.** No flub and no repeated phrase in the take; every
  sentence of `script.md` is in, including the "if time" line
  ("Transformers process every position in parallel…").
- 15 pauses capped at 0.25 s; the longest were 1.3 s before "3 tokens",
  1.2 s before "Q at K transpose" and 1.2 s before "Transformers".
- Said off the planned script, kept as spoken: "you take one token's
  query…and do the dot product", "High value here means", "What question can
  this token help answer?", "under these learned projections".
- Verified by re-transcribing `vo_final.wav` (Parakeet,
  `transcript_final_text.txt`): every word intact. Both recognizers hear the
  last phrase as "these alert / Lerch projections"; `script.md` has "learned"
  and the captions use it. `words.json` spellings fixed (`W_Q`, `W_K`, `@` for
  "at", `K`, `3`, `3-by-3`, `learned`, `one`).
