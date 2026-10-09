ENGINE: hyperframes

# Ep 2. Same vector, different numbers — storyboard

**Title:** Change of Basis Made Simple (Beginner Friendly)

- **THE QUESTION:** How can the same vector have two different sets of numbers?
- **WHO IS ASKING:** an engineer who writes `x @ W` and has watched 3Blue1Brown, and has seen "coordinates" and "basis" used as if they were the vector itself.
- **THE ANSWER IN ONE SENTENCE:** The numbers are an address in a chosen basis. Change the basis: same arrow, new address.

**Why HyperFrames** (`AGENTS.md`, "Which engine"): the default. The one 3D
need is a fixed point inside a lattice that shears; that is a 3×3 projection
drawn on a canvas, with a slow yaw drift as a function of `t` for depth. No
plotted data, no Manim part that would cost less to reuse than to redraw.
The 16:9 drafts (`../basis_transformation_3d.py`, `../plane_many_bases.py`)
are reference for numbers and motion only.

## Ledger (identical in every beat)

| Thing | Value |
|---|---|
| Standard basis | `e1 = (1, 0, 0)`, `e2 = (0, 1, 0)`, `e3 = (0, 0, 1)`; on-screen names `x`, `y`, `z` (the VO says "the usual x, y, z") |
| New basis | `v1 = (1, 0, 0)`, `v2 = (1, 1, 0)`, `v3 = (1, 1, 1)`; on-screen names `v1`, `v2`, `v3` |
| The point | `P = (3, 5, 2)` in x, y, z = `(−2, 3, 2)` in v1, v2, v3. Check: −2·(1,0,0) + 3·(1,1,0) + 2·(1,1,1) = (3, 5, 2) |
| The 2D example | `u = (1, 1)` in x, y. Diagonal basis `d1 = (1, 1)`, `d2 = (−1, 1)`, so `u = (1, 0)` in d1, d2 |
| Basis colours | slot 1 teal `#2DD4BF` (`HERO_TEAL`), slot 2 blue `#60A5FA` (the iso kit's second token colour), slot 3 gold `#E0B040` (`CONTENT_GOLD`). e1 becomes v1, so slot colour is identity: the x arrow, v1, the first number of each address and its tip-to-tail leg are all teal. Same for 2 and 3. In the 2D beat d1 is teal, d2 blue |
| The hero (magenta `#C084FC`) | the vector: the arrow from the origin to P, and P's dot. It never moves in beats 1–6. In beat 7 the hero is `u` |
| Address readout | top of the stage, `(3, 5, 2)` style: parentheses and commas in `--text`, each number in its slot colour, minus sign U+2212. A readout ticks (number morph), never fade-swaps |
| Grid | lattice lines in `GRID` `#1F2440` lifted to read on the navy (≈ `MUTED` `#4A5070` at 0.5); the old grid ghosts at `OP_GHOST` 0.25 when the new one is up |
| Numbers on screen | only the two addresses, the coefficients `3·x 5·y 2·z` / `−2·v1 3·v2 2·v3`, and the 2D `(1, 1)` / `(1, 0)`. Nothing else |

Convention note: the series uses row vectors (`x @ W`). This episode has no
matrix on screen; addresses are written as rows `(a, b, c)`, which matches.

## Layout (every 3D beat)

- Stage y 230–1100, safe x 65–950, band y 1100–1536 empty (captions burned
  by `assemble.py`).
- **Readout slot:** y 250–400, centred on x 507, ~110 px Inter ExtraBold.
  One address at a time, except beat 6, which stacks old (dim, 0.4) above
  new.
- **World:** a canvas over y 420–1090; origin projected near (380, 900);
  the lattice spans `i ∈ [−2, 4]`, `j ∈ [−1, 6]`, `k ∈ [0, 3]` of the current
  basis, clipped to the stage. A slow yaw drift (≈ ±6° over a beat) keeps it
  reading as 3D; the drift is a function of master time so beats cut
  cleanly.
- Arrow labels (`x y z`, `v1 v2 v3`) are DOM text ≥ 60 px next to the
  arrow tips, positioned by the projection each frame.
- Local kit `_kit/basis.js` (written before the beats, linked into each beat
  as `basis/`) owns the projection, lattice, arrows, readout and the
  canonical frame; beats only drive it.

## Beats (from `script.md`, the take)

Times are master seconds in the tightened VO (provisional until step 5's
re-transcription; the "Final beats" table below is the contract).

| # | Beat | VO | Visual |
|---|---|---|---|
| 1 | Hook | The same vector can have completely different numbers. The numbers are just an address, and that address depends on the directions you pick. | **Frame 0 is the finished visual working:** the magenta arrow to P sits still while the lattice is mid-way between standard and new basis and swinging; the readout ticks `(3, 5, 2)` ⇄ `(−2, 3, 2)` in step with the grid. On "address" the readout swells once. On "directions you pick" the three basis arrows brighten (slot colours) while the grid settles on the standard basis. Ends on the canonical frame: standard lattice, x y z arrows, P and its arrow, readout `(3, 5, 2)` dim. |
| 2 | Basis | Those directions are the basis. A basis is a set of independent vectors that span the whole space. It's the coordinate system that you choose. | Starts from the canonical frame with the lattice and P dimmed out (P ghosted, readout empty). "the basis": x y z arrows full strength, labels in. "independent": each arrow in turn shows it leaves the plane of the other two (a faint plane through two, the third pierces it), one quick pulse each. "span the whole space": the lattice grows out from the three arrows to fill the world. "coordinate system you choose": hold, still. Ends on the canonical frame without P. |
| 3 | The point | Here's the point three, five, two in the usual x, y, z. | On "point": P's dot and magenta arrow draw from the origin (≥ 1 s). On "three, five, two": readout `(3, 5, 2)` types in, numbers in teal, blue, gold. Hold. Ends on the canonical frame. |
| 4 | Swap | Now swap the basis, but keep the point exactly where it is, and let the grid change around it. | "swap the basis": x y z arrows morph into v1 v2 v3 (same colours; e1 = v1 stays put, e2 swings to (1,1,0), e3 to (1,1,1)), labels retext. "keep the point exactly where it is": P gets a still pin ring (one pulse, no motion). "let the grid change around it": the lattice shears from standard to new over ≥ 2 s, old lattice left as a ghost. The readout stays `(3, 5, 2)`, dimmed to 0.4: the old address, now stale. |
| 5 | New address | In this new basis, the same point is minus two, three, two. | On "minus two, three, two": readout ticks from `(3, 5, 2)` to `(−2, 3, 2)`, number by number on each spoken number (teal −2, blue 3, gold 2), full strength. P's ring pulses once on "same point". Hold. |
| 6 | Why | The arrow didn't move, but its address changed, because coordinates are how much of each basis vector you need to get there. | "didn't move": hold still, magenta arrow brightens. "address changed": `(3, 5, 2)` reappears dim above `(−2, 3, 2)` (old over new). "how much of each basis vector": tip-to-tail path, −2·v1 (teal, backwards), then 3·v2 (blue), then 2·v3 (gold), each leg ≥ 0.8 s, each lighting its number in the readout as it draws. "get there": the last leg lands on P. Still, final frame clean. |
| 7 | Interpretability (if time) | This matters for interpretability work. One, one is a little x and a little y. Pick a diagonal basis, and it's just one, zero. One clean feature instead of a mix of two. | Cut to 2D, top-down: square grid, magenta arrow u = (1, 1), readout `(1, 1)`. "a little x and a little y": two legs, teal along x, blue up y, each pulses its number. "diagonal basis": the grid rotates 45° and stretches to the d1, d2 lattice (≥ 1.2 s), axes arrows retext to d1, d2; u does not move. "just one, zero": readout ticks to `(1, 0)`; u now lies on d1 exactly, a single teal leg. "one clean feature": the 0 dims, the 1 and u hold. Last frame still: u on d1, readout `(1, 0)`. |

Last line is the take's last line ("One clean feature instead of a mix of
two"); there is no outro. The planned closer "Same arrow, new basis, new
address" was not recorded, so the Short ends on beat 7's still.

## Final beats

Filled in after step 5.
