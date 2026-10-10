ENGINE: hyperframes

# Ep 3. What a Matrix Really Does — storyboard

**Series:** Linear Algebra for AI Engineers, episode 3 (`../SERIES.md`).
**Title:** What a Matrix Really Does | Linear Algebra for AI Engineers

**Why HyperFrames** (`AGENTS.md`, "Which engine"): the default. A flat 2D
plane, arrows and two small cards; no plotted data, no 3D camera, no Manim
part cheaper to reuse than to redraw. ep01 and ep02 built the same look in
HyperFrames; this kit is a copy of ep01's.

## Preflight

- **THE QUESTION:** What does a matrix actually do to a vector?
- **WHO IS ASKING:** an engineer who writes `nn.Linear` and `x @ W` and has
  watched 3Blue1Brown, but sees a weight matrix as a table of numbers with
  no picture behind it.
- **THE ANSWER IN ONE SENTENCE:** A matrix records where each input
  direction lands; every vector follows its recipe to the new place.

VO line 1 is the answer ("A matrix just records where each direction
lands."), and the last line is the takeaway over the canonical frame.

## The look

The flat 2D number plane of ep01/ep02 (`agents/style.md` "Linear algebra"):
x right, y up, one square per step, brighter axes with a tick per step,
thin arrows, the hero marked by colour alone. Kit: `_vec/vec.js` (copied
from ep01's, linked into each beat as `vec/`, on top of
`videos/_shared/web/iso/iso.js` as `iso/`). `00_layout/` is the canonical
frame; `media/hf/00_layout.png` shows it.

**Three camera views** (`VEC.view(A, B, u)`; `VEC.setView(k)` is NEAR → FAR):

| View | Step | Origin (screen) | Used for |
|---|---:|---|---|
| `VEC.NEAR` | 300 px | (432, 1030) | e1, e2 and where they land, under the matrix card. The canonical frame. |
| `VEC.FAR` | 160 px | (240, 1060) | the recipe: x = (3, 2) and x @ W = (2, 4) fit; the card slot (top right) is free only while x @ W is not drawn |
| `VEC.MID` | 280 px | (507, 720) | beat 7's ring of vectors, centred on the stage |

The camera moves only inside a beat, on the words named below, and every
beat starts in the view the previous beat ended in.

## Ledger (identical in every beat; constants in `_vec/vec.js`)

Row-vector (PyTorch) convention throughout: `x @ W`, row i of W is where
input direction i lands.

| What | Value |
|---|---|
| Input directions | `e1 = (1, 0)`, `e2 = (0, 1)`, labelled "e1", "e2" (the VO says "e1", "e2") |
| The matrix | `VEC.W`: row 1 `[ 1, 0.5 ]` = where e1 lands, row 2 `[ −0.5, 1.25 ]` = where e2 lands (the draft's numbers, `../matrix_moves_basis_directions.py`). Card `VEC.matCard`: `W =` then the two rows, each tagged `e1` / `e2` on its right |
| The vector | `VEC.X = (3, 2)`: 3 of e1 plus 2 of e2. Card `VEC.vecCard([3, 2], { name: "x =" })` with slot colours teal, blue |
| The result | `VEC.XW = (2, 4)` = 3·(1, 0.5) + 2·(−0.5, 1.25) = (3, 1.5) + (−1, 2.5). The recipe's corner is (3, 1.5) |
| Identity colours | e1, its landed arrow, row 1, its card slot and its legs: teal `VEC.SLOT[0]`. e2, its landed arrow, row 2, slot and legs: blue `VEC.SLOT[1]` (`#60A5FA`). Old positions of e1, e2 after they move: muted ghosts |
| The hero (magenta) | per beat, named below. The landing spots `VEC.spot` (magenta rings on the landed tips) are the hero of the canonical frame |
| The moved grid | `VEC.lattice(g, VEC.basis(s))`, muted, alpha ≤ 0.35; the standard grid dims to ~0.14 under it (ep02: two grids at 0.3 read as a mesh) |
| Beat 7's matrix | `VEC.M = [[1.6, 0.8], [0.2, 0.1]]`, never shown as numbers: both rows lie on the (2, 1) line, so it stretches (2, 1) and flattens (1, −2) to zero. The ring: 16 teal dots at radius 0.8 around the origin |
| Numbers on screen | only W, x = [ 3, 2 ], and the axis ticks. No (2, 4) readout; the arrow lands on the grid point |

## Final beats (the contract)

`vo_final.wav` is 47.487 s. Cuts sit in pauses. Beat-local t = master − start.

| # | Folder | Master start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.00 | 6.33 | A matrix just records where each direction lands. Every weight matrix in a neural network is doing exactly this. |
| 2 | `02_sends` | 6.33 | 4.04 | Here's e1 and e2. This matrix sends e1 here and e2 here. |
| 3 | `03_recipe` | 10.37 | 4.86 | Now take a vector, three of e1 plus two of e2. The vector is a recipe. |
| 4 | `04_rebuild` | 15.23 | 7.88 | After the matrix, keep the same recipe and use the moved directions. Three of where e1 landed, plus two of where e2 landed. |
| 5 | `05_amounts` | 23.11 | 4.50 | The vector supplies the amounts, the matrix supplies the new directions. |
| 6 | `06_table` | 27.61 | 8.59 | That's why the table of numbers isn't random. Each row is one landing spot. In PyTorch, row i of W is where the input direction i lands. |
| 7 | `07_network` | 36.20 | 7.14 | In a network, that map moves vectors from one space to another, amplifying some directions and collapsing others. |
| 8 | `08_stored` | 43.34 | 4.147 | A matrix is just this stored map where every input direction lands. |

Segment times (master) from `transcript_final.txt`: 0.58 "A matrix just
records…", 3.40 "Every weight matrix…", 5.00 "is doing exactly this", 6.47
"Here's e1 and e2", 7.91 "This matrix sends…", 10.55 "Now take a vector…",
13.83 "The vector is a recipe", 15.43 "After the matrix…", 17.45 "and use
the moved directions", 19.11 "Three of where e1 landed…", 23.30 "The vector
supplies…", 25.23 "the matrix supplies…", 27.80 "That's why the table…",
29.50 "Each row is one landing spot", 31.33 "In PyTorch, row i of W…", 36.35
"In a network…", 39.37 "from one space to another", 41.02 "amplifying…",
43.55 "A matrix is just this stored map", 45.27 "where every input direction
lands". Pauses (master): 3.01–3.42, 6.13–6.53, 7.52–7.93, 10.17–10.58,
11.45–11.86, 13.50–13.87, 15.02–15.43, 18.77–19.18, 21.77–21.97,
22.91–23.32, 24.89–25.25, 27.41–27.82, 30.97–31.38, 33.46–33.81,
34.15–34.39, 35.99–36.40, 37.05–37.41, 40.62–41.02, 43.14–43.55. Place
exact cues from the audio (50 ms RMS envelope of your window), not from
these.

## Beats (the visual brief)

Stage y 230–1100; the band y 1100–1536 stays empty (captions are burned
in). Grid lines may bleed into it; arrows, dots and text may not.

| # | View | Hero (the one magenta thing) | Visual |
|---|---|---|---|
| 1 | FAR | the landing spots | **Frame 0 is the finished visual working:** FAR view, e1 and e2 already ~30 % of the way through their swing to (1, 0.5) and (−0.5, 1.25) (muted ghosts stay at the old positions), the moved lattice shearing with them, the standard grid dimming to 0.14, and the vector x riding along: an off-white (`--text`) arrow from the origin whose tip is `VEC.map(X, s)`, travelling from (3, 2) to (2, 4); a faint muted copy stays at (3, 2). Landed by ~1.3 s. On "lands": magenta spots ring onto both landed tips (a pop, k 1 → 0). "Every weight matrix… doing exactly this": the move replays once (everything eases back to s = 0 and lands again, ≥ 1.2 s each way, spots fading during the trip and ringing again on landing). Ends landed, spots on, x at (2, 4), no card. |
| 2 | FAR → NEAR | the landing spots | "Here's e1 and e2": x and its ghost, the lattice and the spots fade; the camera pushes in to NEAR (≥ 1 s) while e1 and e2 ease back home (s 1 → 0); the ghosts merge into them; the standard grid back to full; labels "e1" (teal) and "e2" (blue) beside the tips. "sends e1 here": a muted ghost stays at (1, 0), e1 swings to (1, 0.5) (≥ 0.8 s), its spot rings on landing. "and e2 here": the same for e2 to (−0.5, 1.25). Labels ride with the tips. Ends on the canonical frame without the card. |
| 3 | NEAR → FAR | the vector x | "Now take a vector": the spots fade, e1 and e2 ease back home (the landed arrows go back to s = 0; keep the ghosts muted so the viewer knows where they went), and the camera pulls out to FAR (≥ 1 s). "three of e1": three teal hops along x, one step each (tick per hop), to (3, 0). "plus two of e2": two blue hops up to (3, 2). Then the x arrow draws from the origin to (3, 2), magenta. "The vector is a recipe": the card `x = [ 3, 2 ]` drops in at the top right (slots teal, blue), right edge 950, top 250. Ends: FAR, standard grid, e1 e2 at home, legs, magenta x, card. |
| 4 | FAR | the output x @ W | "After the matrix": e1 and e2 swing to their landed spots (≥ 1 s, the same swing as beat 1), the moved lattice fades in (≤ 0.35) and the standard grid dims to 0.14; the old legs and x go muted (they stay as the ghost of the old recipe). "keep the same recipe": the card swells once. "use the moved directions": the two landed arrows brighten (alpha 0.7 → 1). "Three of where e1 landed": slot "3" lights teal-bright and three teal hops of (1, 0.5) walk from the origin to (3, 1.5). "plus two of where e2 landed": slot "2" lights, two blue hops of (−0.5, 1.25) to (2, 4). Then the output arrow draws from the origin to (2, 4), magenta. The card must not touch the output tip (card bottom ≈ 360, tip at (560, 420)). |
| 5 | FAR | first the amounts (card slots), then the landing spots | "The vector supplies the amounts": the output arrow goes off-white; the card's "3" and "2" turn magenta and swell; the hop ticks along the legs pulse once. "the matrix supplies the new directions": the slots back to teal / blue; magenta spots ring onto the landed tips of e1 and e2; the landed arrows brighten. Ends: the beat 4 picture with the output off-white and the spots on. |
| 6 | FAR → NEAR | the row being read, with its landing spot | "That's why the table of numbers": the recipe (legs, x, output, card x, lattice, ghost recipe) fades; the camera pushes in to NEAR (≥ 1 s); the W card drops in where x's card was (right edge 950, top 250), rows in teal / blue. Ends the push on the canonical frame (00_layout). "Each row is one landing spot": row 1 magenta + spot 1 pulses, then row 2 magenta + spot 2 pulses, ~0.7 s each. "In PyTorch, row i of W": row 1 magenta again; dashed guides (`VEC.guides`) from e1's landed tip to 1 and 0.5 on the axes. "is where the input direction i lands": the e1 ghost at (1, 0) brightens and a thin teal arc traces from (1, 0) to the landed tip, the tag "e1" on the card row lights. Ends: canonical frame, row 1 back to teal, guides faded. |
| 7 | NEAR → MID | the stretched direction (a magenta line through the origin along (2, 1)) | "In a network": the card fades, the arrows and ghosts fade; the camera moves to MID (≥ 1 s); 16 teal dots appear on a circle of radius 0.8 around the origin (they are vectors; dots, not arrows: a fan of arrows reads as clutter). "that map moves vectors": every dot rides W (`VEC.map`, s 0 → 1, ≥ 1.2 s): the circle becomes a slightly larger tilted ellipse. "from one space to another": a faint copy of the original circle stays (muted). "amplifying some directions": the map morphs on to `VEC.M` (`VEC.basisTo(W, M, u)`); a magenta line through the origin along (2, 1) draws as the dots stretch along it. "collapsing others": the dots flatten onto that line (the ellipse's other axis goes to zero). Ends still: dots on the magenta line, the muted circle behind. |
| 8 | MID → NEAR | the landing spots | "A matrix is just this stored map": the dots and the line fade; the camera returns to NEAR (≥ 1 s); e1, e2 ghosts and the landed arrows return, the W card fades in top right. "where every input direction lands": the spots ring onto both landed tips, row 1 and row 2 flash their colours toward white and back, in turn. Last ~0.6 s still: **the canonical frame exactly** (00_layout at its end). |

Last line is the take's last line; no outro. The final still is the frame
episode 4 can open on: W on its card, its rows drawn as landing arrows.

## Render and assemble

```
cd videos/002-linear-algebra-basics/ep03-what-a-matrix-does
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 02_sends 03_recipe 04_rebuild 05_amounts 06_table 07_network 08_stored; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../../tools/captions_from_transcript.py transcript_final.txt captions.json
uv run --no-sync python ../../../tools/assemble.py beats.json --vo vo_final.wav \
    --captions captions.json -o media/short.mp4
```

## Cut list (runbook step 5)

`vo_raw.m4a` (50.6 s) → `vo_clean.wav` (loudnorm only: the same Studio
Sound take as ep01 and ep02) → `vo_final.wav` (47.5 s):
`tools/tighten_vo.py --max-gap 0.25`, no `--remove`. No phrase cut; 14
pauses capped at 0.25 s. The re-transcription reads clean, word for word.

Flagged in the take, kept:
- "use the move directions": Whisper hears "move" in both the full take
  and a sub-clip; the script says "moved". The final d is soft or missing.
  The caption will read "moved".
- "row i of W is where **the** input direction i lands": one extra "the"
  against the script. Harmless.
- No repeated or restarted phrase.
