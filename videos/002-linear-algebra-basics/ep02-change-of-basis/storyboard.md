ENGINE: hyperframes

# Ep 2. Same vector, different numbers — storyboard

**Title:** Change of Basis Made Simple (Beginner Friendly)

- **THE QUESTION:** How can the same vector have two different sets of numbers?
- **WHO IS ASKING:** an engineer who writes `x @ W` and has watched 3Blue1Brown, and has seen "coordinates" and "basis" used as if they were the vector itself.
- **THE ANSWER IN ONE SENTENCE:** The numbers are an address in a chosen basis. Change the basis: same arrow, new address.

**Why HyperFrames** (`AGENTS.md`, "Which engine"): the default. No plotted
data, no Manim part that would cost less to reuse than to redraw.

**Rework (2026-10-09, after Chris's first watch):** the first build drew a
full 3D lattice (three families of lines through the volume). On a phone it
read as a confusing mesh and the fixed point got lost. The rebuild draws **a
floor, a stalk and a route**: one 2D grid on a solid floor (the plane of the
first two basis vectors), the point on a dashed stalk above it, and the
address drawn as legs tip to tail. The new basis was changed (Chris chose
option B) so its third vector stays `z`: the whole change of basis is a
shear of the floor grid, the stalk never moves, and the third number stays
2 because the height didn't change. Camera is fixed (no drift). Beat 7 was
unaffected. The 16:9 drafts (`../basis_transformation_3d.py`,
`../plane_many_bases.py`) remain reference for motion only; this episode's
new basis differs from theirs.

## Ledger (identical in every beat)

| Thing | Value |
|---|---|
| Standard basis | `e1 = (1, 0, 0)`, `e2 = (0, 1, 0)`, `e3 = (0, 0, 1)`; on-screen names `x`, `y`, `z` (the VO says "the usual x, y, z") |
| New basis | `v1 = (0, −1, 0)`, `v2 = (1, 1, 0)`, `v3 = (0, 0, 1)`; on-screen names `v1`, `v2`, `v3`. (Differs from the 16:9 draft's basis on purpose: v3 = z keeps the change on the floor.) |
| The point | `P = (3, 5, 2)` in x, y, z = `(−2, 3, 2)` in v1, v2, v3. Check: −2·(0,−1,0) + 3·(1,1,0) + 2·(0,0,1) = (0,2,0) + (3,3,0) + (0,0,2) = (3, 5, 2) |
| The routes | old: 3·x to (3,0,0), 5·y to (3,5,0), 2·z up to P. New: −2·v1 to (0,2,0) (backwards along v1), 3·v2 to (3,5,0), 2·v3 up to P. Both routes reach the same foot (3, 5, 0) and climb the same stalk |
| The 2D example | `u = (1, 1)` in x, y. Diagonal basis `d1 = (1, 1)`, `d2 = (−1, 1)`, so `u = (1, 0)` in d1, d2 |
| Basis colours | slot 1 teal `#2DD4BF` (`HERO_TEAL`), slot 2 blue `#60A5FA` (the iso kit's second token colour), slot 3 gold `#E0B040` (`CONTENT_GOLD`). e1 becomes v1, so slot colour is identity: the x arrow, v1, the first number of each address and its tip-to-tail leg are all teal. Same for 2 and 3. In the 2D beat d1 is teal, d2 blue |
| The hero (magenta `#C084FC`) | the vector: the arrow from the origin to P, and P's dot. It never moves in beats 1–6. In beat 7 the hero is `u` |
| Address readout | top of the stage, `(3, 5, 2)` style: parentheses and commas in `--text`, each number in its slot colour, minus sign U+2212. A readout ticks (number morph), never fade-swaps |
| Floor and grid | a solid floor (`BG_PANEL` at 0.9) with one 2D grid of the first two basis vectors (`MUTED` at 0.9, 3 px); the old standard grid ghosts at 0.3 when the new one is up. No lines through the volume |
| Stalk | dashed `FG_DIM` line from the foot (3, 5, 0) up to P, with a small dot at the foot; it is the depth cue and never moves |
| Numbers on screen | only the two addresses and the 2D `(1, 1)` / `(1, 0)`; the route legs carry the coefficients visually. Nothing else |

Convention note: the series uses row vectors (`x @ W`). This episode has no
matrix on screen; addresses are written as rows `(a, b, c)`, which matches.

## Layout (every 3D beat)

- Stage y 230–1100, safe x 65–950, band y 1100–1536 empty (captions burned
  by `assemble.py`).
- **Readout slot:** y 262–400, centred on x 507, 110 px Inter ExtraBold.
  One address at a time, except beat 6, which stacks old (dim) above new.
- **World:** the floor spans y ≈ 540–1070 (it may bleed off the right
  edge); P sits at about (900, 570); the origin and basis arrows at about
  (250, 960). Fixed camera.
- Arrow labels (`x y z`, `v1 v2 v3`) are DOM text ≥ 60 px next to the
  arrow tips, positioned by the projection each frame.
- Local kit `_kit/basis.js` (linked into each beat as `kit/`) owns the
  projection, floor, grid, stalk, route, arrows, readout and the canonical
  frame (`BK.world`); `00_layout/` renders it. Beats only drive it.

## Beats (from `script.md`, the take)

Times are master seconds in the tightened VO (provisional until step 5's
re-transcription; the "Final beats" table below is the contract).

| # | Beat | VO | Visual |
|---|---|---|---|
| 1 | Hook | The same vector can have completely different numbers. The numbers are just an address, and that address depends on the directions you pick. | **Frame 0 is the finished visual working:** P, its magenta arrow and the stalk sit still; the floor grid is mid-shear between standard and new basis and swinging; the route (three legs) re-routes with it, always landing on the foot (`BK.coordsAt(u)`), and the readout shows those coordinates ticking. On "address" the readout swells once. On "directions you pick" the three basis arrows brighten while the grid settles on the standard basis. Ends on row 1. |
| 2 | Basis | Those directions are the basis. A basis is a set of independent vectors that span the whole space. It's the coordinate system that you choose. | P, arrow, stalk, route and readout fade out; the camera pushes in on the origin (the three arrows ~250 px). "the basis": the arrows pulse. "independent": each arrow in turn leaves a faint plane through the other two. "span the whole space": the floor grid grows out from the origin while the camera pulls back to the canonical view. "coordinate system you choose": hold. Ends on row 2. |
| 3 | The point | Here's the point three, five, two in the usual x, y, z. | On "point": the magenta arrow draws to P, then the stalk appears. On "three, five, two": the route walks out leg by leg, each leg landing with its spoken number (3·x teal, 5·y blue, 2·z gold up the stalk), the readout typing the number as its leg lands. On "x, y, z": the basis arrows ripple. Ends on row 3. |
| 4 | Swap | Now swap the basis, but keep the point exactly where it is, and let the grid change around it. | "swap the basis": the old route fades; the basis arrows swing to v1 v2 v3 (labels retext; v3 = z stays). "keep the point exactly where it is": a still pin ring on P, one pulse; the readout dims to 0.4 (the stale address). "let the grid change around it": the floor grid shears from standard to new (≥ 1.8 s), the old grid left as a ghost. Ends on row 4. |
| 5 | New address | In this new basis, the same point is minus two, three, two. | On "same point": P's ring pulses and fades. On "minus two, three, two": the readout ticks number by number on each spoken number (3→−2 teal, 5→3 blue, 2 stays and pulses gold), back to full strength. Ends on row 5. |
| 6 | Why | The arrow didn't move, but its address changed, because coordinates are how much of each basis vector you need to get there. | "didn't move": the magenta arrow glows; nothing moves. "address changed": the readout slides down and the old `(3, 5, 2)` appears dim above it. "how much of each basis vector": the new route walks out, ≥ 0.8 s a leg: −2·v1 (teal, backwards along v1), 3·v2 (blue) to the foot, 2·v3 (gold) up the stalk, each lighting its number. "get there": the last leg lands on P, P pulses. Still. Ends on row 6. |
| 7 | Interpretability (if time) | This matters for interpretability work. One, one is a little x and a little y. Pick a diagonal basis, and it's just one, zero. One clean feature instead of a mix of two. | Cut to 2D, top-down: square grid, magenta arrow u = (1, 1), readout `(1, 1)`. "a little x and a little y": two legs, teal along x, blue up y, each pulses its number. "diagonal basis": the grid rotates 45° and stretches to the d1, d2 lattice (≥ 1.2 s), axes arrows retext to d1, d2; u does not move. "just one, zero": readout ticks to `(1, 0)`; u now lies on d1 exactly, a single teal leg. "one clean feature": the 0 dims, the 1 and u hold. Last frame still: u on d1, readout `(1, 0)`. |

Last line is the take's last line ("One clean feature instead of a mix of
two"); there is no outro. The planned closer "Same arrow, new basis, new
address" was not recorded, so the Short ends on beat 7's still.

## Final beats

Cut approved 2026-10-09: no phrase removals, pauses capped at 0.25 s
(`tighten_vo.py --max-gap 0.25`), 48.9 s → **45.41 s**. Re-transcription
(`transcript_final.txt`) is clean and confirms "can have". Boundaries sit at
the middle of the pause between beats. `beats.json` lists the same lengths.

| # | Beat | Master start | Length | Folder | VO (as said) |
|---|------|-------------:|-------:|--------|--------------|
| 1 | Hook | 0.00 | 6.66 | `01_hook` | The same vector can have completely different numbers. The numbers are just an address, and that address depends on the directions you pick. |
| 2 | Basis | 6.66 | 9.17 | `02_basis` | Those directions are the basis. A basis is a set of independent vectors that span the whole space. It's the coordinate system that you choose. |
| 3 | The point | 15.83 | 3.69 | `03_point` | Here's the point three, five, two in the usual x, y, z. |
| 4 | Swap | 19.52 | 4.87 | `04_swap` | Now swap the basis, but keep the point exactly where it is, and let the grid change around it. |
| 5 | New address | 24.39 | 3.90 | `05_address` | In this new basis, the same point is minus two, three, two. |
| 6 | Why | 28.29 | 6.74 | `06_why` | The arrow didn't move, but its address changed, because coordinates are how much of each basis vector you need to get there. |
| 7 | Interpretability | 35.03 | 10.38 | `07_feature` | This matters for interpretability work. One, one is a little x and a little y. Pick a diagonal basis, and it's just one, zero. One clean feature instead of a mix of two. |

Total 45.41 s.

### Hand-over frames (what each beat ends on = what the next opens on)

All 3D beats draw through `BK.world(g, t, u, opts)` after `BK.setMaster(start)`.

| After beat | u | floor + grid | ghost | basis arrows + labels | hero + stalk | route | readout |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 1, `x y z` | 1 | old route (3, 5, 2), alpha 1 | `(3, 5, 2)`, alpha 1 |
| 2 | 0 | 1 | 0 | 1, `x y z` | 0 | none | none (alpha 0) |
| 3 | 0 | 1 | 0 | 1, `x y z` | 1 | old route, alpha 1 | `(3, 5, 2)`, alpha 1 |
| 4 | 1 | 1 | 1 | 1, `v1 v2 v3` | 1 (+ pin ring) | none | `(3, 5, 2)`, alpha 0.4 |
| 5 | 1 | 1 | 1 | 1, `v1 v2 v3` | 1 | none | `(−2, 3, 2)`, alpha 1 |
| 6 | 1 | 1 | 1 | 1, `v1 v2 v3` | 1 | new route (−2, 3, 2), alpha 1 | `(3, 5, 2)` dim above `(−2, 3, 2)` |
| 7 | 2D, its own world | | | `d1 d2` | `u` on d1 | | `(1, 0)` |

## Render and assemble

```
cd videos/002-linear-algebra-basics/ep02-change-of-basis
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 02_basis 03_point 04_swap 05_address 06_why 07_feature; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../../tools/assemble.py beats.json --vo vo_final.wav \
    --captions captions.json -o media/short.mp4
```
