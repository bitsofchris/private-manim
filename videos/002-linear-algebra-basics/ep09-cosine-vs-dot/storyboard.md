ENGINE: hyperframes

# Ep 9. Dot, cosine, projection: storyboard

**Series:** Linear Algebra for AI Engineers, episode 9 (`../SERIES.md`).
**Title:** Cosine Similarity vs Dot Product | Linear Algebra for AI Engineers

Engine: HyperFrames (the default, `AGENTS.md` "Which engine"). Two arrows on
the flat plane, a shadow, three readouts and one code card; nothing needs
Manim's axes or 3D camera.

## Preflight

- **THE QUESTION:** Dot product, cosine similarity, projection: which one do I want?
- **WHO IS ASKING:** an engineer who calls `F.cosine_similarity` on
  embeddings and `q @ k` in attention, has watched episode 8 (the dot
  product measures alignment), and can't say when the lengths should count.
- **THE ANSWER IN ONE SENTENCE:** Same alignment, different normalization:
  divide by neither length, by both, or by only the target's.
- **THE SEARCH PHRASE:** `cosine similarity vs dot product` (offered word
  for word by autocomplete, `../SERIES.md`). VO line 1 says both halves of
  it in its first four seconds.
- **Code beat:** `F.cosine_similarity(u, v, dim=0)  # 0.6` lands on "that's
  what you use to compare embeddings" (beat 3, "that's" at 22.48 master).

## The look

The flat 2D plane (`agents/style.md` "Linear algebra"), rendered in
`00_layout/` (`media/hf/00_layout.png` is CANON; `media/hf/00_states.png`
shows all five states). Code: `../../../_shared/web/vec/vec.js` (linked as
`vec/`) plus this episode's `_ep/ep09.js` (linked as `ep/`): the ledger,
where things sit, the drawing of the picture, and the five rest states.

- **Top (y 244–476):** three readouts, one per row: `dot = 3`, `cos = 0.6`,
  `proj = 1.5`. Names `--dim`, right-aligned at x 290; values from x 380.
  A value is replaced in place by its derivation in its beat
  (`EP.DERIV`), then collapses back to the number.
- **Plane (y 482–1100):** 260 px a step, origin (250, 1010), grid clipped
  above y 482. v (blue) along the east axis to (2, 0); u (teal) to
  (1.5, 2); the angle arc between them, muted; the drop line, dashed, from
  u's tip straight down to (1.5, 0); the shadow, a magenta bar lying on v
  from the origin to (1.5, 0).
- **Band (y 1100–1536):** captions, anchored to the band bottom for the
  whole Short (`--captions-anchor bottom`, as ep03). A card at the band
  top (y 1115) twice: the code card (beat 3) and `u = [ 1.5, 2 ]` (beat 6).
- **Magenta, one at a time:** the shadow and the proj value are one tight
  group (the shadow is the proj number drawn). When the shadow is not on
  screen, the readout row being spoken is the hero. In a beat where the
  shadow is on and another row is called out, the row gets an off-white
  highlight box (`P.hl`, `COL.text`), not magenta.

## Ledger (identical in every beat; constants in `_ep/ep09.js`)

| What | Value |
|---|---|
| u | `EP.U = (1.5, 2)`, teal (`COL.data`), label "u". Length 2.5, label `|u| = 2.5` |
| v (the target) | `EP.V = (2, 0)`, blue (`VEC.SLOT[1]`), label "v". Length 2, label `|v| = 2`. Lies along e1, so its shadow is u's first coordinate (beat 6) |
| Dot product | `u · v = 1.5 × 2 + 2 × 0 = 3`. Readout `dot = 3`, derivation `1.5 × 2 + 2 × 0` |
| Cosine | `3 ÷ (2.5 × 2) = 0.6`. Readout `cos = 0.6`, derivation `3 ÷ (2.5 × 2)`. Unit arrows `EP.UHAT = (0.6, 0.8)`, `EP.VHAT = (1, 0)` |
| Projection | `3 ÷ 2 = 1.5`. Readout `proj = 1.5`, derivation `3 ÷ 2`. The shadow ends at (1.5, 0); the leftover is (1.5, 0) → (1.5, 2), i.e. (0, 2) |
| Length test (beat 5) | `EP.USMALL = (0.75, 1)`: half of u, same direction; shadow 0.75, proj reads `0.75`, cos stays 0.6 |
| Coordinates (beat 6) | u's shadow on e1 is 1.5 and on e2 is 2: card `u = [ 1.5, 2 ]` |
| Code | `F.cosine_similarity(` / `  u, v, dim=0)  # 0.6` (`EP.CODE`) |
| Numbers on screen | only these. True minus signs; no `2.0` |

## States (`EP.state(P, g, name)`)

| State | What is on screen | Beats that end here |
|---|---|---|
| `CANON` | u, v, arc, drop line, magenta shadow; readouts with proj value magenta; u, v labels | 1, 4, 7 (00_layout at t < 1) |
| `DOT` | CANON without drop line and shadow; `|u| = 2.5`, `|v| = 2` on; dot value magenta | 2 |
| `UNIT` | u, v at unit length; no shadow, no length labels; cos value magenta; code card at the band top | 3 |
| `SPLIT` | CANON + the leftover arrow (1.5, 0) → (1.5, 2), off-white | 5 |
| `COORDS` | v gone, no arc; u with two magenta shadows (1.5 on e1, 2 on e2) and dashed guides; readouts at 0.35; card `u = [ 1.5, 2 ]` | 6 |

## Final beats (the contract)

`vo_final.wav` is 52.329 s. Cuts sit in pauses. Beat-local t = master − start.

| # | Folder | Master start | Length | Opens on → ends on | VO |
|---|---|---:|---:|---|---|
| 1 | `01_hook` | 0.00 | 9.02 | CANON (in motion) → CANON | Cosine similarity is just a dot product with both lengths divided out. Projection divides out only one. Here's when you want each. |
| 2 | `02_dot` | 9.02 | 4.80 | CANON → DOT | Now, all three start from the same thing: the dot product, alignment with the length still in it. |
| 3 | `03_cosine` | 13.82 | 10.38 | DOT → UNIT | Cosine similarity divides by both lengths. Both magnitudes go away, and you're left with pure direction, a number between −1 and 1. And that's what you use to compare embeddings. |
| 4 | `04_shadow` | 24.20 | 8.80 | UNIT → CANON | Now projection divides by only the target's length. Picture casting a shadow from one vector onto another, and projection asks: how much of u points along this direction? |
| 5 | `05_split` | 33.00 | 7.05 | CANON → SPLIT | The shadow keeps the original's length in the answer, and it splits the vector in two: the part along the direction and the part left over. |
| 6 | `06_coords` | 40.05 | 3.75 | SPLIT → COORDS | Even coordinates are projections, one onto each basis direction. |
| 7 | `07_close` | 43.80 | 8.529 | COORDS → CANON | The dot product is alignment with the length. Cosine is alignment without them. Projection is how much of you lies along that line. |

Word starts (master, `words.json`): Cosine 0.59, dot 2.34, both 3.55,
lengths 3.85, divided 4.12, Projection 5.78, only 7.03, Here's 8.00,
each 8.52 | Now 9.24, three 9.52, dot 11.04, alignment 12.12, length 12.84 |
Cosine 14.04, divides 14.94, both 15.86, magnitudes 17.17, away 17.82,
pure 18.78, direction 19.20, number 20.30, −1 20.84, 1 21.60, that's 22.48,
compare 23.20, embeddings 23.50 | projection 24.60, only 25.46, target's
26.12, Picture 27.10, shadow 27.90, another 28.90, asks 30.02, how 30.66,
u 31.18, points 31.36, along 31.90, direction 32.30 | shadow 33.34, keeps
33.60, original's 34.24, length 34.68, splits 35.78, two 36.88, along
37.92, left 39.32, over 39.55 | Even 40.26, coordinates 40.46, projections
41.14, one 42.10, each 42.46, basis 42.79 | dot 44.10, alignment 44.76,
length 45.64, cosine 46.42, without 47.48, Projection 48.70, how 49.34,
you 50.02, lies 50.18, along 50.86, line 51.40.

## Beats (the visual brief)

| # | Hero | Visual |
|---|---|---|
| 1 | the shadow (with the proj value) | **Frame 0 is the finished visual working:** CANON with the drop line already falling from u's tip (~30 % down) and the shadow growing along v behind it; the three values ticking up from 0 to 3, 0.6, 1.5 (done by ~1.2 s). "Cosine similarity": an off-white box rings the cos row. "dot product": the box moves to the dot row. "both lengths divided out": `|u| = 2.5` and `|v| = 2` pop on beside their arrows (both at once), the box back on cos. "Projection divides out only one": `|u|` fades, `|v|` stays and pulses once, box on the proj row. "Here's when you want each": box and `|v|` fade; settle on CANON by ~8.7 s and hold. |
| 2 | the dot value | "Now, all three": the three values pulse once in turn (dot, cos, proj, ~0.25 s apart). "start from the same thing": the drop line and shadow fade out; the proj value goes back to off-white. "the dot product": the dot value turns magenta and is replaced in place by `1.5 × 2 + 2 × 0`, then collapses back to `3`. "alignment": the angle arc brightens to off-white and back. "with the length still in it": `|u| = 2.5` and `|v| = 2` fade on. Ends DOT. |
| 3 | the cos value, then the code card | "Cosine similarity divides by both lengths": dot back to off-white, cos value magenta and replaced by `3 ÷ (2.5 × 2)`; `|u|` and `|v|` pulse on "both lengths". "Both magnitudes go away": the length labels fade and both arrows shrink to unit length (≥ 1 s, u to (0.6, 0.8), v to (1, 0)); the formula collapses to `0.6`. "pure direction": the arc brightens and back. "a number between −1 and 1": u swings round the origin from its angle to 0° (cos reads `1`), through 180° (`−1`) and back to its angle (`0.6`), ≥ 2 s; the cos value tracks it live (one decimal, true minus). "that's what you use to compare embeddings": the code card rises into the band top (y 1115); its `# 0.6` lights magenta, the cos value goes off-white (hero passes to the card). Ends UNIT (cos magenta, card on; set card comment back to dim before the end). |
| 4 | the shadow (with the proj value) | "Now projection": the code card fades; cos value to off-white; u and v grow back to full length (≥ 1 s). "divides by only the target's length": the proj value is replaced by `3 ÷ 2`; `|v| = 2` pops beside v and pulses on "target's length"; then the formula collapses to `1.5` and `|v|` fades. "Picture casting a shadow": the drop line falls from u's tip to v's line (≥ 0.6 s), and on "shadow" the magenta shadow grows along v from the origin to (1.5, 0); the proj value turns magenta with it. "how much of u points along this direction": u pulses (brighter, once) on "u", the shadow pulses on "along". Ends CANON. |
| 5 | the shadow | "The shadow keeps the original's length": u shrinks to (0.75, 1) (≥ 0.8 s); the drop line and shadow follow (shadow to 0.75), the proj value tracks to `0.75`; the cos value pulses and stays `0.6`. "in the answer": u grows back to (1.5, 2), shadow 1.5, proj `1.5`. "splits the vector in two": the shadow becomes the first part; on "the part along the direction" the shadow pulses; on "the part left over" the leftover arrow draws off-white from (1.5, 0) up to (1.5, 2) over the drop line (≥ 0.6 s). Ends SPLIT. |
| 6 | both coordinate shadows (one group) | "Even coordinates": the leftover arrow and v fade, the arc fades, the readouts dim to 0.35. "are projections": dashed guides from u's tip to both axes. "one onto each": the e1 shadow is already there (it is the same 1.5 on the x axis); on "basis direction" a second magenta shadow grows up the y axis to 2. The card `u = [ 1.5, 2 ]` rises into the band top; its 1.5 lights on "one", its 2 on "each". Ends COORDS. |
| 7 | each row in turn, then the shadow | "The dot product": the card and guides fade, v and the arc return, the y-axis shadow fades, the readouts back to full; the x-axis shadow stays (it is v's shadow again) but goes off-white while the dot value is magenta. "is alignment with the length": `|u|`, `|v|` flash on and off. "Cosine": cos value magenta (dot back). "without them": u and v dip to unit length and back (≥ 0.6 s each way). "Projection": proj value and shadow magenta together. "how much of you lies along that line": the drop line pulses. Last ~0.8 s still: **CANON exactly** (00_layout at t < 1, its end). |

The last line is the take's last line; no outro. The final still is the
frame episode 10 can open on: two arrows, one number for how aligned they are.

## Render and assemble

```
cd videos/002-linear-algebra-basics/ep09-cosine-vs-dot
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 02_dot 03_cosine 04_shadow 05_split 06_coords 07_close; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../../tools/captions_from_transcript.py words.json captions.json
uv run --no-sync python ../../../tools/assemble.py beats.json --vo vo_final.wav \
    --captions captions.json --captions-anchor bottom -o media/short.mp4
```

## Cut list (runbook step 5)

`vo_raw.m4a` (58.1 s; Studio Sound take, same session as the rest of the
series) → `vo_clean.wav` (loudnorm only) → `vo_final.wav` (52.3 s):
`tools/tighten_vo.py --max-gap 0.25`, no `--remove`. No phrase cut; 16
pauses capped at 0.25 s (the longest, 2.3 s before the closing line).
The "if time" line ("Even coordinates are projections…") stays: it fits.

Flagged in the take, kept:
- "Here's **when** you want each": Parakeet hears "one"; WhisperKit on a
  sub-clip hears "when". The caption reads "when".
- "alignment with the **length** still in it" and "the dot product is
  alignment with the **length**. Cosine is alignment without **them**":
  singular "length" both times against the plural "them". Captioned as said.
- "how much of **u** points along this direction" vs the last line "how
  much of **you** lies along that line": the same sound. Captioned "u" in
  beat 4 (the vector on screen is labelled u) and "you" at the end, as in
  `script.md`.
- "just **a** dot product": WhisperKit writes "the"; Parakeet and the
  script say "a". `words.json` fixed.
- No repeated or restarted phrase.
