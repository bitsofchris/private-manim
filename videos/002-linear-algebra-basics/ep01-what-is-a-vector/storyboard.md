ENGINE: hyperframes

# Ep 1. What Is a Vector? — storyboard

**Series:** Linear Algebra for Engineers, episode 1 (`../SERIES.md`).
**Title:** What Is a Vector? Linear Algebra for AI

## Preflight

- **THE QUESTION:** What is a vector, actually?
- **WHO IS ASKING:** an engineer who writes PyTorch and has seen "vector"
  a thousand times, but couldn't say what one *is* beyond "a list".
- **THE ANSWER IN ONE SENTENCE:** A vector is a move; its numbers are the
  recipe for building that move from agreed directions.

## The look

A flat 2D number plane (after Chris's first watches: the isometric floor didn't
read for linear algebra). East right, north up. **Space is the plane**:
one grid square is one step, directions are flat arrows lying on it (see a
thing). **Numbers stand on a flat upright card** (read a value). Parts:
`_vec/vec.js` (linked into each beat as `vec/`), on top of the house kit
`videos/_shared/web/iso/iso.js` (`iso/`). `00_layout/` is the canonical
frame; `media/hf/00_layout.png` shows it.

## Ledger (identical in every beat; constants in `_vec/vec.js`)

| What | Value |
|---|---|
| The vector | `VEC.V = [-2, 2]` shown as `[ −2, 2 ]` (true minus sign): 2 opposite east, 2 north = northwest |
| Agreed directions | east `[1, 0]`, north `[0, 1]`; compass letters E N W S at `VEC.COMPASS` |
| Steps | west step `[0,0]→[-2,0]`, north step `[-2,0]→[-2,2]`, both teal; the NW vector `[0,0]→[-2,2]` |
| Origin | the white dot at grid `[0, 0]`, screen (507, 780); one step = 165 px; axes ±2 in every direction |
| Vector card | `VEC.vecCard`, top edge `VEC.CARD_TOP` = 250, centred (`VEC.centreLeft`) |
| The house | `VEC.HOUSE`: `[ 1,800, 450,000 ]` with "sq ft" / "price" under the slots |
| The embedding | `VEC.EMBED` (ten values) and `VEC.DIMS` = "4,096" |

Colours: teal = the steps, data, the card at rest; magenta = the one hero
per beat (below); muted = construction (compass unit arrows); dim = labels.

## Final beats (the contract)

`vo_final.wav` is 48.708 s. Cuts sit in pauses. Beat-local t = master − start.

| # | Folder | Master start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.00 | 5.30 | A vector is just a list of numbers, and it's the key to understanding the math behind AI. |
| 2 | `02_northwest` | 5.30 | 5.55 | My son asked me, what does northwest mean? Now, northwest isn't a new direction. It's some west plus some north. |
| 3 | `03_move` | 10.85 | 7.75 | That's just a vector, a move through space. Its numbers are the recipe for building that move out of directions we already agreed upon. |
| 4 | `04_coords` | 18.60 | 6.89 | If the agreed directions are east and north, then minus two, two means two steps opposite east and two steps north. |
| 5 | `05_list` | 25.49 | 9.79 | In code, a vector is just a list where order matters. Each position means something. If we're describing a house, one dimension might be square feet, the other one price. |
| 6 | `06_views` | 35.28 | 6.52 | Linear algebra is moving between those two views. The arrow lets you see it. The list lets you compute with it. |
| 7 | `07_embed` | 41.80 | 6.908 | Every embedding in AI is one of these, a list of numbers we treat as directions in space with thousands of dimensions. |

Segment times (master) from `transcript_final.txt`: 0.55 "A vector…", 2.63
"and it's the key…", 5.38 "My son…", 7.56 "Now, northwest…", 9.30 "it's some
west…", 10.93 "That's just a vector…", 13.87 "Its numbers…", 16.47 "out of
directions…", 18.73 "If the agreed…", 20.94 "then minus two two…", 24.22
"and two steps north", 25.64 "In code…", 28.84 "Each position…", 30.54 "If
we're describing…", 32.27 "one dimension…", 35.40 "Linear algebra…", 37.90
"The arrow…", 39.59 "The list…", 41.89 "Every embedding…", 44.13 "a list of
numbers…", 46.73 "with thousands of dimensions". Place exact cues from the
audio (50 ms RMS envelope of your window), not from these.

## Beats (the visual brief)

Stage y 230–1100, band y 1100–1536 stays empty (captions are burned in).

| # | Hero (the one magenta thing) | Visual |
|---|---|---|
| 1 | the two numbers (card and axes) | Frame 0: the floor with its reference frame already on (`VEC.axes`: the east-west and north grid lines through the origin with a tick per step, the E and N unit arrows labelled), the NW vector already drawing up from the origin (teal here, not the hero), the card `[ −2, 2 ]` at the top. "list of numbers": dashed guides drop from the tip to −2 and 2 on the axes (`VEC.guides`); the card's numbers and the axis labels "−2" / "2" turn magenta, the card's swell once. (Added after Chris's first watch: the arrow alone didn't read as −2, 2.) "the math behind AI": a quiet fan of ~12 thin teal arrows grows out of the origin in many directions (low alpha, under the NW arrow), a hint of every vector a model holds; they fade by the end so the frame settles on the NW arrow + card. |
| 2 | the NW arrow | Card gone (fades out at the start). The compass: four muted unit arrows with E N W S, then the letters "NW" (magenta) above where NW will point, on "northwest". "isn't a new direction": the NW arrow draws from the origin, magenta. "some west": the west step draws (teal, 2 squares). "plus some north": the north step draws tip-to-tail and lands exactly on the NW tip. Ends on the 00_layout picture without the card. |
| 3 | the NW arrow | "a move through space": a white puck travels from the origin up the NW arrow to its tip (the move) and stops. "Its numbers are the recipe": the card `[ −2, 2 ]` drops in at the top (teal border). "directions we already agreed upon": the east and north unit arrows brighten from muted to teal with their letters, while the NW arrow stays magenta. |
| 4 | the card slot being read | "agreed directions are east and north": east and north unit arrows teal and labelled. "minus two": slot 0 (`−2`) magenta; the west step re-walks as two hops of one square each, a tick at each square; "two" (the second number): slot 0 back to text, slot 1 (`2`) magenta; the north step walks two hops. End: both steps drawn, NW arrow (teal now) between them, card with slot 1 lit. |
| 5 | the slot labels | The floor dims (grid alpha down, arrows fade to 25 %). The card moves to the stage centre and becomes code: `v = [ −2, 2 ]` in monospace ("In code"). "order matters": the two numbers swap places and swap back (a quick shuffle). "Each position means something": labels "east" / "north" appear under the slots, magenta. "describing a house": the card retypes to `house = [ 1,800, 450,000 ]`, labels "sq ft" / "price" (magenta), slot by slot on "square feet" and "price". |
| 6 | first the arrow, then the card | Two views at once: the floor and NW arrow come back (upper stage), the card `[ −2, 2 ]` (plain, not code) sits below the figure at stage bottom (above y 1100). "moving between those two views": a thin double-headed connector pulses between arrow and card. "The arrow lets you see it": the arrow magenta, card teal. "The list lets you compute with it": the card magenta, the arrow back to teal. |
| 7 | the "4,096 numbers" count | The card grows: after `−2, 2` the slots fill with `VEC.EMBED` values wrapping onto more rows (keep ≥ 60 px), ending in "…". "directions in space": the fan of thin arrows from beat 1 returns on the floor, many directions. "thousands of dimensions": a label "4,096 numbers" (magenta) under the card. Last 0.5 s still. |

## Render and assemble

```
cd videos/002-linear-algebra-basics/ep01-what-is-a-vector
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 02_northwest 03_move 04_coords 05_list 06_views 07_embed; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../../tools/captions_from_transcript.py transcript_final.txt captions.json
uv run --no-sync python ../../../tools/assemble.py beats.json --vo vo_final.wav \
    --captions captions.json -o media/short.mp4
```

## Cut list (runbook step 5)

`vo_raw.m4a` (57.3 s) → `vo_clean.wav` (loudnorm only: the take was already
Studio Sound clean, −67 dB floor) → `vo_final.wav` (48.7 s):
`tools/tighten_vo.py --max-gap 0.25 --remove 48.90-50.65`. The one removed
range is a false start ("Every--") and a throat clear before "Every
embedding". No content cut. Not recorded: the planned last line "A vector
is a move. Its numbers are the recipe."; the take ends on the embedding line.
