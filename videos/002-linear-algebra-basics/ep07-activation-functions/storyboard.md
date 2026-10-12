ENGINE: hyperframes

# Ep 7. Why layers need activations — storyboard

**Series:** Linear Algebra for AI Engineers, episode 7 (`../SERIES.md`).
**Title:** Activation Functions: Why You Need Them | Linear Algebra for AI Engineers

Engine: HyperFrames (the default, `AGENTS.md` "Which engine"). Every beat is
code cards, 2 × 2 matrices and the flat 2D plane with its grid pushed through
a map; nothing needs Manim's axes or 3D camera.

## Preflight

- **THE QUESTION:** Why does a neural net need activation functions?
- **WHO IS ASKING:** an engineer who writes `nn.Linear` and `x @ W`, has
  watched episodes 3–6, and has typed `nn.ReLU()` between layers without
  knowing what breaks if it is left out.
- **THE ANSWER IN ONE SENTENCE:** Two linear layers multiply into one
  matrix, so without a nonlinearity between them depth buys nothing.
- **THE SEARCH PHRASE:** `activation functions` (SERIES.md; autocomplete
  offers "activation functions explained", "why do we need activation
  function in neural network"). Said in VO line 1: "Without activation
  functions, a 100-layer neural network is just one matrix."
- **Code beat:** `(x @ W1) @ W2` / `== x @ (W1 @ W2)` on "So that's the same
  as x at W1 times W2" (beat 4); then the `nn.Sequential` card with
  `nn.ReLU()` between the two `nn.Linear(2, 2)` lines on "Put a ReLU or a
  GELU between the layers" (beat 8).

## The look

Rendered in `00_layout/` (`media/hf/00_layout_sheet.png`: CHAIN, MERGED,
BENT). The code is `../../../_shared/web/vec/vec.js` (the shared plane kit,
linked as `vec/`) plus this episode's `_ep/ep07.js` (linked as `ep/`): the
ledger, where things sit, the maps, and the rest states.

- **Top (y 236–600):** the code card at y 236, centred; matrix names (`W1`,
  `W2`, `W`; Inter 60 px `--dim`) at y 372; 2 × 2 matrices from y 450, 110 px
  cells, 60 px digits, white, one tall bracket pair each. `W1 @ W2` side by
  side (left edges 195 and 600, `@` centred at x 507); the merged `W`
  centred (left 397). The five-line `nn.Sequential` card (beats 8–9) takes
  the whole top; the matrices are gone while it is up. A two-line card
  (beat 4) hides the names.
- **Bottom (y 620–1100): the plane.** 120 px a step, origin (447, 1016),
  clipped above y 620. The old square grid stays as a ghost (alpha 0.12);
  the grid the current map makes is drawn over it (`EP.warp`: every input
  grid line pushed through the map as a sampled polyline, so a linear map
  gives straight lines and relu gives bent ones, with one drawing call).
  `x` is the teal arrow from the origin to wherever the map sends (1, 2).
  x's trail: dashed hops with a small dot at each start.
- **The map is one function of five dials** (`EP.stage({w1, relu, w2,
  post})`): `p @ W1`, then relu, then `@ W2`, then any extra 2 × 2. Every
  beat moves the plane by tweening a dial, never by swapping drawings.
- **Magenta, one at a time:** a lit matrix (box); the merged `W` (its digits
  and the `W` in `x @ W`) at rest in MERGED; the hero line (the input grid
  line x1 = 1) from beat 7, which stays straight under any linear map and
  bends under relu; in beats 8–9 `nn.ReLU()` and the bent line are one
  hero pair (the line of code and what it does).

## Ledger (identical in every beat; constants in `_ep/ep07.js`)

Row-vector (PyTorch) convention: `x @ W`, row i of `W` is where input
direction i lands. New numbers (episodes 3–6 share `(5, 3) @ (3, 2)`, but
composition needs two square maps on one plane).

| What | Value | In `ep07.js` |
|---|---|---|
| x | `[ 1, 2 ]` (teal) | `EP.X` |
| W1, layer 1 | `[[ 1, 1 ], [ −1, 1 ]]`: rotate 45°, stretch √2 | `EP.W1` |
| W2, layer 2 | `[[ 1, 0 ], [ 0, 0.5 ]]`: squish north–south by half | `EP.W2` |
| W = W1 @ W2, the one matrix | `[[ 1, 0.5 ], [ −1, 0.5 ]]` | `EP.W` |
| x @ W1 | `(−1, 3)` | `EP.XW1` |
| x @ W1 @ W2 = x @ W | `(−1, 1.5)` | `EP.XW` |
| relu(x @ W1) | `(0, 3)` | `EP.RXW1` |
| relu(x @ W1) @ W2 | `(0, 1.5)` | `EP.RXW` |
| hero line | input line x1 = 1 (through x); under relu(· @ W1) @ W2 it bends at (2, 0) and (0, 1) | `EP.LINE_X` |
| Code | `x @ W1 @ W2`; `(x @ W1) @ W2`; `== x @ (W1 @ W2)`; `x @ W`; `nn.Sequential(` / `nn.Linear(2, 2),` / `nn.ReLU(),` / `nn.Linear(2, 2),` / `)` | `EP.CODE` |
| Many layers | 100 in the hook ("100-layer"), 200 in beat 6 ("or 200"), as the VO says | — |

## States (what each beat opens and ends on)

`P = EP.parts(root)` once; `EP.state(P, g, NAME)` at the top of `render(t)`;
a beat then draws only what differs (call `EP.plane(g, {...})` again with its
own dials; `EP.bg(g)` first if redrawing the whole canvas).

- **STACK:** card `x @ W1 @ W2`; `W1 @ W2` with names; plane: the plain
  grid, x at (1, 2).
- **CHAIN:** STACK with the grid through W1 then W2, x at (−1, 1.5), its two
  hops dashed (1, 2) → (−1, 3) → (−1, 1.5).
- **ASSOC:** CHAIN with the card `(x @ W1) @ W2`.
- **SAME:** two-line card `(x @ W1) @ W2` / `== x @ (W1 @ W2)`, names hidden;
  CHAIN's plane plus the shortcut hop (1, 2) → (−1, 1.5).
- **MERGED:** card `x @ W` (`W` magenta); `W` centred, digits magenta, name
  `W`; plane through W, x at (−1, 1.5), only the shortcut hop.
- **LINEAR:** MERGED with `W`'s digits white and no hop; the hero line magenta
  (straight).
- **FOLDED:** the `nn.Sequential` card (`nn.ReLU()` magenta), no matrices;
  plane relu(p @ W1), hero line bent, x at (0, 3).
- **BENT:** FOLDED with the plane relu(p @ W1) @ W2, x at (0, 1.5).
- **END:** MERGED without the hop: the last frame, one matrix.

## Final beats (the contract)

`vo_final.wav` is 53.34 s. Every cut sits in the middle of a pause. Beat-local
t = master − start. Word times: `words.json` (a first guess; ep05 found it
0.2–0.6 s late inside phrases): check every cue on a 10–50 ms RMS envelope of
your window.

| # | Folder | Master start | Length | Opens on | Ends on | VO |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 5.91 | (frame 0: already moving) | STACK | Without activation functions, a 100-layer neural network is just one matrix. Here's why. |
| 2 | `02_functions` | 5.91 | 4.64 | STACK | CHAIN | Matrices are functions, and multiplying matrices combines those functions. |
| 3 | `03_stack` | 10.55 | 6.29 | CHAIN | ASSOC | So if you stack two layers, x @ W1, then @ W2, the order matters, but it's associative. |
| 4 | `04_same` | 16.84 | 3.47 | ASSOC | SAME | So that's the same as x @ W1 times W2. |
| 5 | `05_one` | 20.31 | 2.74 | SAME | MERGED | And W1 times W2 is just one matrix. |
| 6 | `06_depth` | 23.05 | 6.73 | MERGED | MERGED | So two linear layers, or 200, collapse into a single linear transformation. The depth here doesn't buy you anything. |
| 7 | `07_straight` | 29.78 | 6.57 | MERGED | LINEAR | Now a linear map keeps the origin fixed and the grid line straight. It can stretch, rotate, and squish, but it can't bend. |
| 8 | `08_relu` | 36.35 | 4.18 | LINEAR | FOLDED | Put a ReLU or a GELU between the layers, and the collapse stops. |
| 9 | `09_bend` | 40.53 | 4.38 | FOLDED | BENT | Now each layer can bend the path, and stacking actually adds something. |
| 10 | `10_close` | 44.91 | 8.43 | BENT | END | That's why every layer in a model is a matrix multiply followed by some nonlinearity. Without activations, a deep network is just one matrix. |

Mid-Short beats end on ≥ 5 still frames; only beat 10 holds ≥ 0.8 s still.

## Beats (the visual brief)

| # | Folder | Hero | Visual |
|---|---|---|---|
| 1 | `01_hook` | the one matrix `W` | Frame 0: a deck of layer cards already sliding together in the top stage: five panels stacked down the stage (`W1`, `W2`, `W3`, `⋮`, `W100`; Inter 60 px names on `--panel` cards, ~96 px pitch), the plane under them in STACK with x at (1, 2). "100-layer": the `W100` card's name brightens. "just one matrix" (~4.1): the deck collapses into one card, which becomes the matrix `W` at its MERGED place (digits magenta, ≥ 0.6 s, one move). "Here's why" (~5.4): `W` splits into `W1 @ W2` (each half slides to its STACK place, the `@` fades in) and the card `x @ W1 @ W2` fades in; digits go white. Last 5 frames STACK. |
| 2 | `02_functions` | W1, then W2 | Opens STACK. "Matrices are functions": W1 gets the magenta box and the plane's grid turns by W1 (dial w1 0 → 1, ≥ 1 s) while x rides from (1, 2) to (−1, 3), leaving a dot at (1, 2) and the dashed hop behind it. "multiplying matrices combines those functions": the box passes to W2 and the grid squishes by W2 (w2 0 → 1, ≥ 1 s), x rides on to (−1, 1.5), the second hop dashed behind it. Box gone before the hold. Ends CHAIN. |
| 3 | `03_stack` | the two hops, in order | Opens CHAIN. "stack two layers": the card's `W1` and `W2` brighten together. "x @ W1": the card's `x @ W1` lights (magenta) with W1's box and the first hop pulses. "then @ W2": the light passes to `@ W2`, W2's box, the second hop. "the order matters": the hops pulse 1 then 2 (quick). "but it's associative": the card becomes `(x @ W1) @ W2` (the parentheses fade in around `x @ W1`; the rest does not move or retype). All lights back to rest. Ends ASSOC. |
| 4 | `04_same` | the shortcut hop | Code beat. Opens ASSOC. "So that's the same as": the card grows to two lines (names fade), line 2 `== x @ (W1 @ W2)` types on (≤ 0.5 s). "x @ W1 times W2": `(W1 @ W2)` lights magenta, and on the plane the shortcut hop draws from (1, 2) straight to (−1, 1.5) (≥ 0.6 s), landing on x's tip. Light back to rest. Ends SAME. |
| 5 | `05_one` | the merged W | Opens SAME. "W1 times W2": W1 and W2 slide together, their digits fading as W's digits fade in at the centre (one move, ≥ 0.6 s, the `@` going with it). "just one matrix": `W` lands magenta with its name; the card's line 2 `(W1 @ W2)` collapses into `W` and the card shrinks to one line `x @ W`; the two-hop trail fades, the shortcut stays. Ends MERGED. |
| 6 | `06_depth` | `W` | Opens MERGED. "two linear layers": the card becomes `x @ W1 @ W2` (W's digits dim to white). "or 200": it becomes `x @ W1 @ ⋯ @ W200`. "collapse into a single linear transformation": the card collapses back to `x @ W` (≥ 0.6 s) and W's digits go magenta again, W pulses once. "The depth here doesn't buy you anything": nothing moves but the shortcut hop and x pulse once. Ends MERGED. |
| 7 | `07_straight` | the origin, then the hero line | Opens MERGED. The shortcut hop fades and W's digits go white as the hero passes to the plane. "keeps the origin fixed": a magenta ring on the origin (`VEC.spot`) pulses, then goes. "and the grid line straight": the hero line (x1 = 1) turns magenta and the grid brightens once. "stretch, rotate, and squish": the plane runs through three extra maps on top of W, each on its word (`post`: a stretch east–west ×1.4, a ~30° turn, a squish north–south ×0.6, then back to none); the hero line stays straight throughout. "but it can't bend": the hero line tries to kink at its middle (a few px) and springs straight (≤ 0.5 s). Ends LINEAR. |
| 8 | `08_relu` | `nn.ReLU()`, then the bent line | Code beat. Opens LINEAR. "Put a ReLU": `W` and its name fade; the card cross-fades to the `nn.Sequential` card with the two `nn.Linear(2, 2),` lines only, then `nn.ReLU(),` opens a gap between them and types in, magenta. "or a GELU": that line reads `nn.GELU(),` for the word, back to `nn.ReLU(),` on "between". "between the layers": the plane goes back to between the layers (w2 1 → 0: the grid un-squishes to W1's, x back to (−1, 3)). "and the collapse stops": relu folds the grid (dial relu 0 → 1, ≥ 0.8 s): everything west of the north axis slides onto it, everything south onto the east axis; the hero line bends; x slides to (0, 3). Ends FOLDED. |
| 9 | `09_bend` | the bent line | Opens FOLDED. "each layer can bend the path": magenta rings (`VEC.spot`) pulse on the hero line's two corners. "stacking actually adds something": the second `nn.Linear(2, 2),` line brightens and W2 acts on the bent grid (w2 0 → 1, ≥ 1 s): the corners move to (2, 0) and (0, 1), the line stays bent, x rides to (0, 1.5). Ends BENT. |
| 10 | `10_close` | `nn.ReLU()`, then `W` | Opens BENT. "every layer in a model is a matrix multiply": both `nn.Linear(2, 2),` lines brighten; "followed by some nonlinearity": `nn.ReLU(),` pulses. "Without activations": the `nn.ReLU(),` line fades out and the gap closes; the plane un-bends (relu 1 → 0, ≥ 0.8 s), the hero line straight and back to grid colour. "a deep network is just one matrix": the card becomes `x @ W` and `W` fades in at its centre, digits magenta. Last ≥ 0.8 s still on END. |

## Cut list (runbook step 5)

`vo_raw.m4a` (58.8 s; same session as ep04–06, already clean) →
`vo_clean.wav` (loudnorm only) → `vo_final.wav` (53.34 s):
`tools/tighten_vo.py --max-gap 0.25` (no `--remove`).

- **No phrase removed.** The take has no flub and no repeated phrase; every
  sentence of `script.md` is in, including the "if time" line ("That's why
  every layer in a model…").
- Pauses capped at 0.25 s; the longest were 1.6 s before "Now a linear map",
  1.3 s before "Now each layer" and 1.1 s mid-sentence after "Put a ReLU or a
  GELU".
- Said slightly off the planned script, kept as spoken: "the grid line
  straight" (singular), "followed by *some* nonlinearity".
- Verified by re-transcribing `vo_final.wav` (Parakeet,
  `transcript_final_text.txt`): every word intact. `words.json` spellings fixed
  (`W1`, `W2`, `@` for "at", `GELU`, `100-layer`, `nonlinearity`).

## Revision 1: open on "can't bend" (Chris, 2026-10-12)

Chris, after the first cut: open on the strongest part, "a linear map … can
stretch, rotate, and squish, but it can't bend", then explain the collapse,
then the ReLU payoff. Beat 6 ("So two linear layers, or 200, … doesn't buy you
anything") is dropped, and so is the "Now" before "a linear map". The previous
cut's files are kept as `vo_final_v1.wav`, `words_v1.json`, `captions_v1.json`
and `beats_v1.json`. `06_depth/` stays on disk but is out of `beats.json`.

**VO re-splice** (from the v1 `vo_final.wav`, 8 ms fades at each join):
0.25 s silence + [30.12, 36.35] + [0, 23.05] + [36.35, 53.34] = **46.52 s**.
The cut at 30.12 drops "Now" (30.06 still transcribes as "Our linear map").
The join after "can't bend" leaves a 0.80 s pause before "Without activation
functions", kept on purpose as the turn into "Here's why". Re-transcribed clean
(`transcript_final_text.txt`). `words.json` is remapped by the same offsets and
`captions.json` rebuilt from it.

Line 1 is no longer the answer, and the search phrase "activation functions"
is now at 7.1 s. That breaks runbook step 1 on purpose: Chris chose the visual
hook. Check it at the day-10 read.

| # | Folder | Master start | Length | Opens on | Ends on | VO |
|---|---|---:|---:|---|---|---|
| 1 | `07_straight` | 0.00 | 6.48 | (frame 0: the grid easing into W) | LINEAR | A linear map keeps the origin fixed and the grid line straight. It can stretch, rotate, and squish, but it can't bend. |
| 2 | `01_hook` | 6.48 | 5.91 | LINEAR (then into the deck) | STACK | Without activation functions, a 100-layer neural network is just one matrix. Here's why. |
| 3 | `02_functions` | 12.39 | 4.64 | STACK | CHAIN | Matrices are functions, and multiplying matrices combines those functions. |
| 4 | `03_stack` | 17.03 | 6.29 | CHAIN | ASSOC | So if you stack two layers, x @ W1, then @ W2, the order matters, but it's associative. |
| 5 | `04_same` | 23.32 | 3.47 | ASSOC | SAME | So that's the same as x @ W1 times W2. |
| 6 | `05_one` | 26.79 | 2.74 | SAME | MERGED | And W1 times W2 is just one matrix. |
| 7 | `08_relu` | 29.53 | 4.18 | MERGED | FOLDED | Put a ReLU or a GELU between the layers, and the collapse stops. |
| 8 | `09_bend` | 33.71 | 4.38 | FOLDED | BENT | Now each layer can bend the path, and stacking actually adds something. |
| 9 | `10_close` | 38.09 | 8.43 | BENT | END | That's why every layer in a model is a matrix multiply followed by some nonlinearity. Without activations, a deep network is just one matrix. |

**Beats reworked:**
- `07_straight` opens cold: there is no hand-off from MERGED, the W grid eases in from the plain grid, and W is white from frame 0.
- `01_hook` opens on LINEAR and leaves it (plane back to the plain grid, hero line out) as the deck comes in.
- `08_relu` opens on MERGED: the shortcut hop fades and the hero line fades in before relu bends it.

The other six beats are unchanged.
