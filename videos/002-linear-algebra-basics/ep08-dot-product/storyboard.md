ENGINE: hyperframes

# Ep 8. The dot product measures alignment — storyboard

**Series:** Linear Algebra for AI Engineers, episode 8 (`../SERIES.md`).
**Title:** Dot Product Explained Visually | Linear Algebra for AI Engineers

**Why HyperFrames** (`AGENTS.md`, "Which engine"): the default. A flat 2D
plane, two arrows, a ticking number, a few rows of numbers and a code card;
no plotted data, no 3D camera, no Manim part cheaper to reuse than to redraw.

## Preflight

- **THE QUESTION:** What does a dot product tell you?
- **WHO IS ASKING:** an engineer who writes `x @ W` and `torch.dot`, has
  watched 3Blue1Brown and episodes 1–7, and knows the formula but not why
  every similarity score in AI is one.
- **THE ANSWER IN ONE SENTENCE:** Multiply pairwise and sum: positive means
  aligned, zero means perpendicular, negative means opposed.
- **THE SEARCH PHRASE:** `dot product explained visually` (autocomplete
  offers it word for word, SERIES.md). The title promises "visually", so
  frame 0 is the arrow already turning with the number ticking, under line 1.
- **Code beat:** `torch.dot(a, b)` / `# 1·2 + 1·2 = 4` in the lower stage (y 900),
  landing on "The way the math works" (beat 2) over the aligned pair whose
  numbers it computes.

VO line 1 is the answer ("A dot product tells you how much two vectors
point the same way."). The take ends on "It's also the core of attention";
the planned "if time" line and closing takeaway were not recorded.

## Revision 2 (Chris, after the first cut)

"I don't like the part when I am reading out the numbers. Does the dot
product 4 and then −4 make sense in the problem we show?" It did not: the
read-out example was 3-D ([1, 2, 3] · [4, −1, 0] = 2) and the turning arrows
were a different, unnumbered pair, so their 4 and −4 came from nowhere. Cut
"One, two, three, dot four, minus one, zero. That's four, minus two, zero,
sum two." (6.9 s) and put the math on the arrows: a = [ 1, 1 ], b's numbers at
its tip at each landmark, and the pairwise sum `1 × 2 + 1 × 2` live under the
readout from beat 2 on. 37.0 s → 30.08 s, 7 beats → 6.

## The look

The flat 2D plane (`agents/style.md` "Linear algebra"), from the shared kit
`../../../_shared/web/vec/vec.js` (linked as `vec/`), plus this episode's
`_ep/ep08.js` (linked as `ep/`): the ledger, where things sit, the drawing
helpers (`pair`, `nums`, `arc`, `rightMark`, `words`) and the rest states.
`00_layout/` renders MATH, th 90 and OPPOSITE_N (`media/hf/00_layout_sheet.png`).

- **One view, no camera move.** `EP.PLANE`: 145 px a step, origin (507, 805).
  b's whole sweep (45° to 225°) stays between y 395 and 1095, under the two
  readout rows and above the band.
- **The readout is the hero.** Row 1 (y 250): `dot product = ` in `--dim`
  right-aligned at x 700, the number left-aligned at x 724, magenta, tabular.
  Row 2 (y 326): the pairwise sum in seven fixed slots, `1 × bx + 1 × by`, a's
  1s teal, b's numbers blue (one decimal while moving), operators dim.
- **Tip labels:** `[ 1, 1 ]` teal beside a's tip; b's label (`[ 2, 2 ]`,
  `[ −2, 2 ]`, `[ −2, −2 ]`) only near a landmark (full within 3°, gone by 12°).
- **Code card** in the empty lower stage (y 900) under the aligned pair, beats 2–3 only; at the band top it collided with two-line captions. Captions sit at the
  band bottom (`--captions-anchor bottom`).

## Ledger (identical in every beat; constants in `_ep/ep08.js`)

| What | Value | In `ep08.js` |
|---|---|---|
| The turning pair | a = [ 1, 1 ] teal, fixed; b blue, length 2√2, at angle th from a (CCW) | `EP.A2`, `EP.bAt(th)` |
| Its dot product | 1·bx + 1·by: th 0 → b [ 2, 2 ], **4**; th 90 → b [ −2, 2 ], **0**; th 180 → b [ −2, −2 ], **−4**; th 60 → **2** (CANON) | `EP.dotAt`, `EP.TH` |
| Readout | `dot product = ` + the value; one decimal while moving, exact at landmarks (never "4.0" or "−0") | `EP.fmtd`, `P.ro[0].set` |
| Pairwise sum | `1 × 2 + 1 × 2` (live with b) | `P.form.set(th)`, `EP.nums` |
| Code | `torch.dot(a, b)` / `# 1·2 + 1·2 = 4` (comment `--dim`) | `EP.CODE`, `P.code`, `EP.placeCode` |
| Words (toy 2-D embeddings) | king (2, 1) teal, queen (1.5, 2) blue, banana (−1, 2) gold | `EP.WORDS` |
| Word scores | `king · queen = 5` (5 magenta), `king · banana = 0` (off-white) | `EP.KQ`, `EP.KB` |
| Attention | king → `query` (20 px further left: `EP.QUERY_DX`), queen → `key`, banana gone; `query · key = 5`, `attention score` under it | state `ATTN` |
| Marks | the angle arc a → b, muted, radius 0.7; the right-angle mark at th 90, off-white; the king–queen arc, radius 0.9 | `EP.arc`, `EP.rightMark` |

Row-vector (PyTorch) convention: vectors are rows `[ … ]`.

## States (what each beat opens and ends on)

`P = EP.parts(root)` once; `EP.state(P, g, NAME)` at the top of `render(t)`;
a beat then draws only what differs (see `00_layout/index.html`).

| State | Picture | Ends beat |
|---|---|---|
| `CANON` | plane, a, b at th 60, arc, `dot product = 2` | (the look) |
| `ALIGNED` | plane, b [ 2, 2 ] under a [ 1, 1 ], `dot product = 4`, no numbers | 1 |
| `MATH` | ALIGNED + tip labels + `1 × 2 + 1 × 2` + the code card | 2 |
| `ALIGNED_N` | MATH without the code card | 3 |
| `OPPOSITE_N` | th 180, b [ −2, −2 ], `1 × −2 + 1 × −2`, `dot product = −4`, arc a half turn | 4 |
| `WORDS` | king, queen, banana, muted king–queen arc; both word readouts | 5 |
| `ATTN` | query, key; `query · key = 5`, `attention score` | 6 (the last frame) |

## Final beats (the contract)

`vo_final.wav` is 30.080 s (29.39 s of take + 0.69 s of silence so the last
still holds). Cuts sit in pauses. Beat-local t = master − start. Word times:
`words.json` (master seconds). Beats 3–6 kept their audio exactly (shifted
−6.918 s), so their beat-local cues are unchanged from the first build.

| # | Folder | Master start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.00 | 6.07 | A dot product tells you how much two vectors point the same way. It's a way to measure similarity in AI models. |
| 2 | `02_math` | 6.07 | 2.92 | The way the math works is you multiply pairwise and then sum. |
| 3 | `03_turn` | 8.99 | 4.17 | Watch the number as this arrow turns. Pointing the same direction is positive. |
| 4 | `04_zero` | 13.16 | 7.44 | At ninety degrees, they're perpendicular, orthogonal, exactly zero. No overlap at all. Pointing opposite is negative. |
| 5 | `05_embed` | 20.60 | 6.69 | That's why it's everywhere in AI. Embeddings that mean similar things point in similar directions, and the dot product is how you check. |
| 6 | `06_attention` | 27.29 | 2.79 | It's also the core of attention. |

Key word times (master): "same way" 3.02–3.40, "similarity" 4.50, "math
works" 6.54–6.90, "multiply" 7.12, "pairwise" 7.56, "and then" 8.12–8.40,
"sum" 8.54, "Watch" 9.19, "number" 9.52, "arrow turns" 10.28–10.70, "same
direction" 11.88–12.40, "positive" 12.50, "90 degrees" 13.48–14.05,
"perpendicular" 14.70, "orthogonal" 15.48, "exactly zero" 16.32–16.98, "No
overlap at all" 17.78–18.60, "opposite" 19.44, "negative" 20.02, "everywhere"
21.30, "similar directions" 24.04–24.95, "dot product" 25.63, "check" 26.68,
"core" 28.00, "attention" 28.36–28.81.

## Beats (the visual brief)

Stage y 230–1100; the band y 1100–1536 holds only captions.
Grid lines may bleed into it; arrows
may not.

| # | Hero (the one magenta thing) | Visual |
|---|---|---|
| 1 | the readout number | **Frame 0 is the finished visual working:** b turning toward a with the number ticking up through 0, landing at th 0 on "same way": `4`, a lying on b. "measure similarity": b leans out to th 25 and back. Ends exactly `ALIGNED`. (Built; unchanged except the plane's new step and origin.) |
| 2 | `dot` in the code card on "multiply pairwise", then the readout `4` on "sum" | From ALIGNED. "The way the math works": the code card drops in under the pair (y 900), line 1 only; `[ 1, 1 ]` and `[ 2, 2 ]` fade in at the tips. "multiply pairwise": `dot` in the card goes magenta; the pairwise sum builds in under the readout: `1 × 2` on "multiply" (7.12), `+ 1 × 2` on "pairwise" (7.56), each pair of slots popping in. "and then sum": `dot` back to white; the comment `# 1·2 + 1·2` types in; on "sum" (8.54) ` = 4` appears in the comment and the readout `4` swells. Ends exactly `MATH`, still from ~8.8. |
| 3 | the readout number | From MATH: the code card fades out (0–0.4). "Watch the number": the number swells. "as this arrow turns": b swings out from th 0 to th 70 (≥ 1 s), the readout and the pairwise sum ticking down (b's tip label fades as it leaves); "Pointing the same direction": b turns back, landing at th 0 / `4` on "direction"; "positive": the number swells. Ends exactly `ALIGNED_N`. |
| 4 | the readout number | From ALIGNED_N (as built, plus `EP.nums` every frame): b turns 0 → 90 landing on "degrees", the sum reads `1 × −2 + 1 × 2`; right-angle mark on "perpendicular"; `0` swells on "zero"; mark pulses on "overlap"; b turns 90 → 180 landing on "negative" with a swell, the sum `1 × −2 + 1 × −2`. Ends exactly `OPPOSITE_N`. |
| 5 | the king–queen arc on "similar directions", then `5` | From OPPOSITE_N: a, b, the arc, the readout, the pairwise sum and the tip labels fade out (≤ 0.5 s). Then as built: the words grow, the magenta arc, `king · queen = 5`, `king · banana = 0`. Ends exactly `WORDS`. |
| 6 | `5` (as `query · key = 5`) | As built. Ends exactly `ATTN`. |

Last line is the take's last line; no outro. The final still is two arrows
from the origin and their score: episode 9 (cosine vs dot) can open on two
arrows.

## Render and assemble

```
cd videos/002-linear-algebra-basics/ep08-dot-product
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 02_math 03_turn 04_zero 05_embed 06_attention; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../../tools/captions_from_transcript.py words.json captions.json
uv run --no-sync python ../../../tools/assemble.py beats.json --vo vo_final.wav \
    --captions captions.json --captions-anchor bottom -o media/short.mp4
```

## Cut list (runbook step 5)

`vo_raw.m4a` (40.8 s) → `vo_clean.wav` (loudnorm only: the same Studio Sound
take as ep01–ep07) → `vo_final.wav`: `tools/tighten_vo.py --max-gap 0.25
--remove 11.30-19.45` (revision 2: the read-out numbers), 10 pieces, 29.39 s;
then 0.69 s of silence appended so the last beat holds a still after
"attention". The re-transcription (`transcript_final_text.txt`) reads word
for word. `words.json` is the first build's WhisperKit word times with the
cut range dropped and later words shifted −6.918 s (the cut is the only
change; `transcript_final.json` is the first build's timing transcript).

Flagged in the take, kept:
- "It's **a way to measure similarity in AI models**" (planned: "It's how AI
  measures similarity"). Reworded, clean, no restart.
- `words.json`: WhisperKit dropped "That's" before "why it's everywhere";
  inserted from the envelope. "exactly 0" spelled "zero". Caption phrase
  breaks are set by `seg` numbers in `words.json`.
- No flubbed or repeated phrase anywhere in the take.
