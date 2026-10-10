# Linear Algebra for AI Engineers: the series

**Name:** linear-algebra-series
**Description:** Home base for the "Linear Algebra for Engineers" Shorts.
The arc, one row per episode, and a checklist of where each episode is.
This folder keeps the source material (draft scenes, recap narration)
and one `epNN-slug/` subfolder per episode, laid out like any other
Short's folder.
**When to use:** start of any session on this series. Pick the next
episode from the checklist, then run `agents/runbook.md` from step 0 in
that episode's folder. Update the checklist in the same pass as the work.
**How it works:** audio first, one episode per session. This file fixes
each episode's title, question, one-sentence answer, opening frame, and
what to reuse. Beats and VO live in the episode's own `storyboard.md`.

## The arc

**Promise:** enough linear algebra to read a forward pass, from one vector
to an attention score, in the notation PyTorch actually uses.

**Who it is for:** an engineer who writes `nn.Linear` and `x @ W` and has
watched 3Blue1Brown, but still loses the thread at shapes, rows vs
columns, and "why a dot product?".

| Act | Episodes | The viewer leaves able to say |
|---|---|---|
| 1. Vectors | 1–2 | A vector is a move; its numbers are an address in a chosen basis. |
| 2. Matrices are layers | 3–7 | A matrix says where directions land; `x @ W` is a weighted sum of rows; a layer is that map plus a nonlinearity. |
| 3. Comparing vectors | 8–10 | A dot product measures alignment; attention scores are dot products. |
| 4. Structure (not started) | 11–14 | Rank, change of basis, SVD, QK/OV: what a learned matrix is really doing. |

Acts 1–3 are a complete season: they follow one vector through a layer
and into attention. They are not all of linear algebra for engineers.
Act 4 is the half that makes LoRA, PCA, and interpretability readable,
and it waits on Units 6–9, which were never studied.

Why the draft animations stop at episode 6: scenes were built alongside
Units 1–3 (May 24–30). Units 4–5 were finished in notebooks only
(June 5–6), then the sprint paused. Episodes 7–10 have notes and worked
examples but no visuals; nothing is wrong with them.

## Checklist

Stages, in runbook order. Every episode is **ready for VO**: the scripts
and final titles are in [`SCRIPTS.md`](SCRIPTS.md). All 11 were recorded
in one take (2026-10-09) and cut into one subfolder per episode here, each
with `vo_raw.m4a` and `script.md` (what was actually said). Tick Storyboard
when the take is cut into beats in that subfolder. Episode headings below
keep the short working names; the table has the publish titles.

| # | YouTube title | Folder | Draft visuals | Script | VO | Storyboard | Beats | Assembled | Shipped |
|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | What Is a Vector? \| Linear Algebra for AI Engineers | `ep01-what-is-a-vector` | x | x | x | x | x | x | |
| 2 | Change of Basis \| Linear Algebra for AI Engineers | `ep02-change-of-basis` | x | x | x | x | x | x | |
| 3 | What a Matrix Really Does \| Linear Algebra for AI Engineers | `ep03-what-a-matrix-does` | x | x | x | | | | |
| 4 | Matrix Multiplication (x @ W) \| Linear Algebra for AI Engineers | `ep04-matrix-multiplication` | x | x | x | | | | |
| 5 | PyTorch nn.Linear Explained \| Linear Algebra for AI Engineers | `ep05-nn-linear-shape` | x | x | x | | | | |
| 6 | Batch Matrix Multiplication \| Linear Algebra for AI Engineers | `ep06-batch-matmul` | x | x | x | | | | |
| 7 | Why Neural Nets Need Activations \| Linear Algebra for AI Engineers | `ep07-activation-functions` | | x | x | | | | |
| 8 | Dot Product Explained Visually \| Linear Algebra for AI Engineers | `ep08-dot-product` | | x | x | | | | |
| 9 | Cosine Similarity vs Dot Product \| Linear Algebra for AI Engineers | `ep09-cosine-vs-dot` | | x | x | | | | |
| 10 | Query, Key and Attention Scores \| Linear Algebra for AI Engineers | `ep10-attention-scores` | | x | x | | | | |
| T | How Much Linear Algebra for AI? \| Linear Algebra for AI Engineers | `epT-four-ideas` | x | x | x | | | | |

Draft visuals = a 16:9 `BocScene` draft exists in this folder with
narration in `UNIT_1_3_RECAP.md`. It is reference only: every beat is
rebuilt as a Short. Folder numbers are assigned when an episode is built
(the next free number at the time; 009–011 are taken).

Ship order: **3 → 4 → 5**, then 1, 2, 6, then 7–10, trailer last.
3–5 are the most PyTorch-specific, have the strongest drafts, and share
one running example and one `_parts.py`.

## Episodes

### 1. A vector is a recipe
- **Question:** What is a vector, actually?
- **Answer:** A vector is a move; its numbers are the recipe for building
  that move from agreed directions.
- **Frame 0 / hero:** compass with NW lit; west and north arrows build it.
  Hero: the NW arrow.
- **Reuse:** `northwest_linear_combination.py`; recap segment 1; the post's
  NW-on-the-mirror opening; Unit 0 notes.

### 2. Same vector, different numbers
- **Question:** How can the same vector have two different sets of numbers?
- **Answer:** The numbers are an address in a chosen basis. Change the
  basis: same arrow, new address.
- **Frame 0 / hero (as built):** the point on its stalk, the floor grid
  shearing, the route re-routing, the address ticking `(3, 5, 2)` ⇄
  `(−2, 3, 2)`. Hero: the point that does not move.
- **Reuse:** `plane_many_bases.py`; recap 2–3; Unit 1's note that `(1, 1)`
  becomes `(1, 0)` in a diagonal basis. The basis differs from
  `basis_transformation_3d.py`: v1 = (0, −1, 0), v2 = (1, 1, 0), v3 = z, so
  the change is a floor shear (same spoken numbers).
- **Ends on:** the 2D still, u = (1, 1) lying on d1 with the address
  (1, 0). Episode 3 can open on two basis arrows.

### 3. What a matrix actually does
- **Question:** What does a matrix actually do to a vector?
- **Answer:** A matrix records where each input direction lands; every
  vector follows its recipe to the new place.
- **Frame 0 / hero:** two basis arrows swing to new positions and a vector
  rides along. Hero: the landed arrows.
- **Reuse:** `matrix_moves_basis_directions.py`, `matrix_as_stored_map.py`;
  recap 4–5; Unit 2 notes.

### 4. What `x @ W` really computes
- **Question:** What is `x @ W` actually computing?
- **Answer:** Each number in `x` weights one row of `W`; add the weighted
  rows and you have the output.
- **Frame 0 / hero:** `x` turns sideways beside `W`, rows scale, columns
  sum. Hero: the output row.
- **Reuse:** `one_row_weighted_sum.py`, `rows_land_columns_add.py`; recap
  7 and 10; Unit 3 "sum down the columns".

### 5. The `nn.Linear` shape gotcha
- **Question:** I asked for 3 in, 2 out. Why is the weight 2 by 3?
- **Answer:** PyTorch stores one row per output neuron and flips it on the
  forward pass. It is the same map, stored sideways.
- **Frame 0 / hero:** `nn.Linear(3, 2)` with `weight.shape` printing
  `(2, 3)` under it. Hero: the `.T`.
- **Reuse:** `nn_linear_weight_structure.py`; recap 8; Unit 3 "where are
  the landing vectors stored, rows or columns?"; `code_block`.
- **Note:** the only episode where the math (column) convention appears.

### 6. One matmul, whole batch
- **Question:** How does a whole batch go through a layer in one line?
- **Answer:** `X` is data and `W` is the map: `(batch, in) @ (in, out)`
  applies the same map to every row.
- **Frame 0 / hero:** five rows of `X` sweeping through one `W`. Hero: the
  shape line `(5, 3) @ (3, 2) → (5, 2)`.
- **Reuse:** `batched_linear_map_tensors.py`, `ml_layer_5d_to_3d.py`; recap
  6 and 9; Unit 2 "data matrix vs weight matrix".

### 7. Why layers need activations
- **Question:** Why does a neural net need activation functions?
- **Answer:** Two linear layers multiply into one matrix, so without a
  nonlinearity between them depth buys nothing.
- **Frame 0 / hero:** two stacked `W` boxes collapse into one. Hero: the
  collapsed matrix.
- **Reuse:** Unit 3 notes and notebook; the post's "Stack the Moves"
  section; landing arrows from episode 3. No draft scene.

### 8. The dot product measures alignment
- **Question:** What does a dot product tell you?
- **Answer:** Multiply pairwise and sum: positive means aligned, zero means
  perpendicular, negative means opposed.
- **Frame 0 / hero:** two arrows, one rotating, a number tracking from
  positive through zero to negative. Hero: the number.
- **Reuse:** Unit 4 notes and notebook; `hero_arrow`;
  `pickle-pirate-gemma/blog02_king_queen.py` for the embedding payoff. No
  draft scene.

### 9. Dot, cosine, projection
- **Question:** Dot product, cosine similarity, projection: which one do I
  want?
- **Answer:** Same alignment, different normalization: divide by neither
  length, by both, or by only the target's.
- **Frame 0 / hero:** one arrow casting a shadow on another, three
  readouts. Hero: the shadow.
- **Reuse:** Unit 4 notes; `residual` mobject;
  `001-pca-best-shadow/shadow_3d.py`. No draft scene.

### 10. Attention scores are dot products
- **Question:** What is an attention score?
- **Answer:** A dot product between one token's query and another token's
  key. `Q @ K.T` is every pair at once.
- **Frame 0 / hero:** token columns, one query arrow fanning to the keys, a
  score grid filling. Hero: the brightest cell.
- **Reuse:** Unit 5 notes and notebook;
  `005-transformer-short/_tokens.py`. No draft scene.

### T. Trailer: the four ideas
- **Question:** How much linear algebra do I need for AI?
- **Answer:** Four ideas: vectors hold information, and matrices are
  learned moves that reshape it.
- **Frame 0 / hero:** montage of the hero frames from 1, 3, 4, 10.
- **Reuse:** `ai_vectors_to_representations.py`; recap "Bottom Line Up
  Front" and closing VO. Built last; doubles as the stitched intro.

## Series rules

- **Publish copy (Chris, 2026-10-10):** the series is called *Linear Algebra
  for AI Engineers*, and every episode says so the same way. This replaces
  runbook step 9's title pattern and its 50-character cap for this series
  only; the rest of step 9 stands.
  - **Title:** `<Concept> | Linear Algebra for AI Engineers`. The concept
    comes first, in the words a beginner would search, and should be at
    most ~35 characters, because the feed may cut off the series suffix.
    No "Made Simple (Beginner Friendly)": the suffix does that job. The
    checklist above holds each episode's title (the `|` is escaped there as `\|` for the table).
  - **Description:** the line after the what's-shown lines and before the
    sign-off is, with the episode's number:
    `Episode N of Linear Algebra for AI Engineers. The write-up it comes from, How Vectors Move Through Neural Networks: https://bitsofchris.com/p/how-vectors-move-through-neural-networks`
    The trailer uses `The trailer for Linear Algebra for AI Engineers.`
    followed by the same write-up sentence.

- One question per episode, in the viewer's words. One sentence answers it.
- **Flat 2D grid, not the isometric floor** (Chris, 2026-10-09, after ep01): east right, north up, one square per step, brighter axes. Copy `ep01-what-is-a-vector/_vec/vec.js` for the plane, arrows, dots and the vector card; the look's rules are in `agents/style.md` "Linear algebra".
- **Episode folders are one level deeper** than `videos/NNN-slug/`, so every repo-relative path gains a level: HyperFrames symlinks `../../../_shared/web/vendor` (and `iso`), tools at `../../../tools/`, the Manim shim `parents[3]`.
- Row-vector (PyTorch) convention everywhere: `x @ W`, `W` is `(in, out)`,
  rows of `W` are where input directions land.
- Episodes 3–6 share the `(5, 3) @ (3, 2)` numbers already in the draft
  scenes, so stitched chapters share a frame.
- Shared visuals start in the first episode's `_parts.py` and are promoted
  to `videos/_shared/` on second use (`agents/parts.md`).
- Each episode ends on a still the next one can open on.

## Sources

| Source | What it gives |
|---|---|
| Vault `Projects/Foundations/Unit 0–5`, `# Notes` sections | Chris's own sentences and where he got stuck. VO starts here. |
| `deep-learning/code/22_ai-foundations-linear-algebra/notebooks/` units 0–5 | Worked PyTorch examples and on-screen numbers. |
| This folder | 11 draft scenes and `UNIT_1_3_RECAP.md` (see `README.md`). |
| Post: *How Vectors Move Through Neural Networks* (2026-05-31) | The hook and the through-line. |

## Stitching later

Episode order 1 → 10 is the long-form, with the trailer VO as its intro.
A 16:9 stitch needs re-renders on `BocScene`, so layout logic goes in
`_parts.py` functions that take a stage rather than assuming 9:16.

## Act 4, parked

Rank and low-rank (the LoRA episode), change of basis as the
interpretability punchline, SVD, QK/OV circuits. An episode is downstream
of a note, so these are added only after Units 6–9 are studied. "PCA is
the best shadow" (`videos/001-pca-best-shadow/`, one of three scenes
coded) fits after episode 9.
