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
- **Code beat:** `torch.dot(a, b)` / `# 4 − 2 + 0 = 2`: line 1 lands on "The
  way the math works" (beat 2), line 2 fills term by term on "That's four,
  minus two, zero, sum two" (beat 3).

VO line 1 is the answer ("A dot product tells you how much two vectors
point the same way."). The take ends on "It's also the core of attention";
the planned "if time" line and closing takeaway were not recorded.

## The look

The flat 2D plane (`agents/style.md` "Linear algebra"), from the shared kit
`../../../_shared/web/vec/vec.js` (linked as `vec/`), plus this episode's
`_ep/ep08.js` (linked as `ep/`): the ledger, where things sit, the drawing
helpers (`pair`, `arc`, `rightMark`, `words`, `rule`) and the rest states.
`00_layout/` renders three of them (`media/hf/00_layout_sheet.png`).

- **One view, no camera move.** `EP.PLANE`: 150 px a step, origin (507, 775),
  axes ±2.6 east-west, −2.2 to 2.6 south-north. b's whole sweep (45° to 225°)
  stays between y 351 and 1075, under the readout and above the band.
- **The readout is the hero.** Top of the stage, two rows (y 250, 330), lead
  text right-aligned at x 700 in `--dim`, the number left-aligned at x 724,
  magenta, tabular, so it ticks without moving the words.
- **Numbers beats (2–3)** replace the plane: rows a and b, the rule, the
  products row, "sum = 2", the code card centred at y 850. Numbers are
  right-aligned on their columns (x 470, 640, 810), as PyTorch prints a tensor.

## Ledger (identical in every beat; constants in `_ep/ep08.js`)

| What | Value | In `ep08.js` |
|---|---|---|
| Pairwise example (Unit 4 notebook, problem 1) | `a = [ 1, 2, 3 ]` (teal), `b = [ 4, −1, 0 ]` (blue) | `EP.A3`, `EP.B3` |
| Products, sum | `[ 4, −2, 0 ]` (off-white), **sum = 2** (magenta) | `EP.PROD`, `EP.SUM` |
| Code | `torch.dot(a, b)` / `# 4 − 2 + 0 = 2` (comment `--dim`) | `EP.CODE`, `P.code` |
| The turning pair (2-D) | a = (1, 1) teal, fixed; b blue, length 2√2, at angle th from a (CCW) | `EP.A2`, `EP.bAt(th)` |
| Its dot product | a · b = 4 cos th: th 0 → b (2, 2), **4**; th 90 → b (−2, 2), **0**; th 180 → b (−2, −2), **−4**; th 60 → **2** (CANON) | `EP.dotAt`, `EP.TH` |
| Readout text | `dot product = ` + the value; one decimal while moving, exact at landmarks (2.8, 4, 0, −4; never "4.0" or "−0") | `EP.fmtd`, `P.ro[0].set` |
| Words (toy 2-D embeddings) | king (2, 1) teal, queen (1.5, 2) blue, banana (−1, 2) gold | `EP.WORDS` |
| Word scores | `king · queen = 5` (5 magenta), `king · banana = 0` (off-white) | `EP.KQ`, `EP.KB` |
| Attention | king → `query`, queen → `key`, banana gone; `query · key = 5`, `attention score` under it | state `ATTN` |
| Marks | the angle arc a → b, muted, radius 0.7; the right-angle mark at th 90, off-white | `EP.arc`, `EP.rightMark` |

Row-vector (PyTorch) convention: vectors are rows `[ … ]`. The 3-D pairwise
a, b and the 2-D plane pair are different vectors; the plane's arrows carry
no letters (the readout says "dot product") so the names never collide.

## States (what each beat opens and ends on)

`P = EP.parts(root)` once; `EP.state(P, g, NAME)` at the top of `render(t)`;
a beat then draws only what differs (see `00_layout/index.html`).

| State | Picture | Ends beat |
|---|---|---|
| `CANON` | plane, a, b at th 60, arc, `dot product = 2` | (00_layout; the look) |
| `ALIGNED` | plane, b (2, 2) under a (1, 1), `dot product = 4` | 1, 4 |
| `NUMS` | rows a, b; code card line 1 only | 2 |
| `SUM` | NUMS + rule, `[ 4, −2, 0 ]`, `sum = 2`, code line 2 full | 3 |
| `OPPOSITE` | plane, b (−2, −2), arc a half turn, `dot product = −4` | 5 |
| `WORDS` | plane, king, queen, banana; both word readouts | 6 |
| `ATTN` | query, key; `query · key = 5`, `attention score` | 7 (the last frame) |

## Final beats (the contract)

`vo_final.wav` is 37.000 s (36.31 s of take + 0.69 s of silence so the last
still holds; pending Chris's OK on the cut list). Cuts sit in pauses.
Beat-local t = master − start. Word times: `words.json` (master seconds).

| # | Folder | Master start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.00 | 6.07 | A dot product tells you how much two vectors point the same way. It's a way to measure similarity in AI models. |
| 2 | `02_pairwise` | 6.07 | 6.51 | The way the math works is you multiply pairwise and then sum. One, two, three, dot four, minus one, zero. |
| 3 | `03_sum` | 12.58 | 3.33 | That's four, minus two, zero, sum two. |
| 4 | `04_turn` | 15.91 | 4.17 | Watch the number as this arrow turns. Pointing the same direction is positive. |
| 5 | `05_zero` | 20.08 | 7.44 | At ninety degrees, they're perpendicular, orthogonal, exactly zero. No overlap at all. Pointing opposite is negative. |
| 6 | `06_embed` | 27.52 | 6.69 | That's why it's everywhere in AI. Embeddings that mean similar things point in similar directions, and the dot product is how you check. |
| 7 | `07_attention` | 34.21 | 2.79 | It's also the core of attention. |

Key word times (master, from `words.json`): "same way" 3.02–3.40,
"similarity" 4.50, "math works" 6.54–6.90, "multiply" 7.12, "pairwise" 7.56,
"sum" 8.54, "1" 9.26, "2" 9.50, "3" 10.09, "dot" 10.64, "4" 10.88, "minus"
11.47, "1" 11.58, "0" 12.12, "That's" 12.80, "4" 13.00, "minus" 13.35, "2"
13.46, "0" 14.18, "sum" 15.02, "2" 15.52, "Watch" 16.11, "number" 16.44,
"arrow turns" 17.20–17.60, "same direction" 18.80–19.30, "positive" 19.42,
"90 degrees" 20.40–21.00, "perpendicular" 21.62, "orthogonal" 22.40, "exactly
zero" 23.24–23.90, "No overlap at all" 24.70–25.50, "opposite" 26.36,
"negative" 26.94, "That's why" 27.70, "everywhere in AI" 28.22–28.90,
"Embeddings" 29.10, "similar things" 29.66–30.30, "point" 30.40, "similar
directions" 30.96–31.90, "dot product" 32.55–33.10, "check" 33.60, "core"
34.92, "attention" 35.28–35.73. Pauses (master): 3.48–3.89, 5.87–6.28,
8.79–9.20, 12.38–12.79, 14.54–14.96, 15.71–16.12, 17.91–18.32, 19.88–20.29,
21.23–21.53, 24.22–24.63, 25.60–26.01, 27.31–27.72, 32.06–32.30,
34.01–34.42, 35.73–end. Check a cue that matters on the envelope of your
window.

## Beats (the visual brief)

Stage y 230–1100; the band y 1100–1536 stays empty (captions are burned in).
Grid lines may bleed into it; arrows, numbers and text may not.

| # | Hero (the one magenta thing) | Visual |
|---|---|---|
| 1 | the readout number | **Frame 0 is the finished visual working:** CANON layout, b already turning: at t 0 th ≈ 140 (readout ≈ −3.1) and moving toward a, ticking up through 0 (no pause there), landing at th 0 on "same way" (master 3.02–3.40): readout `4`, a lying on b. A gentle swell of the number on landing (scale 1 → 1.15 → 1, ≤ 0.4 s). "measure similarity": b eases back out a little and settles (th 0 → 25 → 0, or hold); ends exactly `ALIGNED`, still from ~5.6 s. |
| 2 | first `dot` in the code card, then the slot being read | From ALIGNED: the plane, arrows and readout fade out (≤ 0.5 s) while the names `a =`, `b =` and both rows' brackets fade in (empty). "The way the math works": the code card line 1 `torch.dot(a, b)` drops in at y 850. "multiply pairwise and then sum": `dot` in the card turns magenta and back (hero), ~1 s. "One, two, three": a's digits pop in, one per word (9.26, 9.50, 10.09). "dot": nothing new (the card's `dot` may pulse once). "four, minus one, zero": b's digits pop in on their words (10.88, 11.47–11.58, 12.12). Ends `NUMS`, still from ~12.3. |
| 3 | each product as it lands, then the sum 2 | From NUMS: the rule draws (≤ 0.3 s) and the products row's brackets fade in. "four" (13.00): the magenta box (`EP.colRect(0)`) around column 1; `4` flies from between 1 and 4 into the products row; the comment's `4` appears. "minus two" (13.35–13.46): box to column 2, `−2` lands, comment ` − 2`. "zero" (14.18): column 3, `0`, ` + 0`. Box fades. "sum" (15.02): the three products pulse; `sum =` fades in. "two" (15.52): `2` pops in magenta (the hero), comment ` = 2`. Ends `SUM`. |
| 4 | the readout number | From SUM: the numbers and code card fade out (≤ 0.5 s) while the plane fades in with b at th 70 (`dot product = 1.4`). "Watch the number": the number swells once. "as this arrow turns": b turns toward a (≥ 1 s), the number ticking up, landing at th 0 / `4` on "same direction" (≈ 18.9). "positive": the number swells. Ends `ALIGNED` (still from ~19.7). |
| 5 | the readout number | From ALIGNED. "At ninety degrees": b turns 0 → 90 (≥ 0.8 s, landing ≈ 20.9) and the readout ticks 4 → 0. "perpendicular": the right-angle mark draws in at the origin (off-white). "exactly zero": the `0` swells. "No overlap at all": hold (the mark may pulse once). "Pointing opposite" (26.10): the mark fades, b turns 90 → 180 (≥ 0.8 s), ticking 0 → −4, landing on "negative" (26.94) with a swell. Ends `OPPOSITE`. |
| 6 | the king–queen arc on "similar directions", then `5` | From OPPOSITE: a, b, the arc and the readout fade out (≤ 0.5 s). "everywhere in AI": king, queen, banana grow from the origin (`EP.words` with u 0 → 1, staggered 0.15 s, labels riding the tips). "similar things" / "point in similar directions": a magenta arc between king and queen (`EP.arc(g, 26.57, 53.13, { r: 0.9, col: hero })`) draws. "the dot product": the arc goes muted; `king · queen = 5` fades in, its 5 magenta and swelling. "check": `king · banana = 0` fades in under it (off-white number). Ends `WORDS` (+ the muted arc is fine to keep; say so in the report). |
| 7 | `5` (as `query · key = 5`) | From WORDS: banana, its readout and the arc fade; the labels king → `query` and queen → `key` cross-fade on "core" (34.92); the readout lead cross-fades to `query · key = ` with the 5 staying put; on "attention" (35.28) `attention score` fades in under it. Still from ~36.0 to the end: `ATTN` exactly. |

Last line is the take's last line; no outro. The final still is two arrows
from the origin and their score: episode 9 (cosine vs dot) can open on two
arrows.

## Render and assemble

```
cd videos/002-linear-algebra-basics/ep08-dot-product
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 02_pairwise 03_sum 04_turn 05_zero 06_embed 07_attention; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../../tools/captions_from_transcript.py words.json captions.json
uv run --no-sync python ../../../tools/assemble.py beats.json --vo vo_final.wav \
    --captions captions.json --captions-anchor bottom -o media/short.mp4
```

## Cut list (runbook step 5)

`vo_raw.m4a` (40.8 s) → `vo_clean.wav` (loudnorm only: the same Studio Sound
take as ep01–ep07) → `vo_final.wav`: `tools/tighten_vo.py --max-gap 0.25`,
no `--remove`, 13 pieces, 36.31 s; then 0.69 s of silence appended so the
last beat holds a still after "attention". No phrase cut: the take is under
60 s with every line in. The re-transcription (`transcript_final_text.txt`)
reads word for word.

Flagged in the take, kept:
- "It's **a way to measure similarity in AI models**" (planned: "It's how AI
  measures similarity"). Reworded, clean, no restart.
- "one, two, three **dot** four, minus one, zero": WhisperKit hears "dot,"
  as its own word; it is a true "dot", read as the operator. Captions keep it.
- "That's four minus two, zero, sum two": "sum" is clear; no repeated phrase.
- `words.json`: WhisperKit dropped "That's" before "why it's everywhere";
  inserted at 27.70 from the envelope. "exactly 0" spelled "zero".
- No flubbed or repeated phrase anywhere in the take.
