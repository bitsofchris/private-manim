ENGINE: hyperframes

# Why 6 FLOPs per parameter per token: storyboard (v3, built from the take)

THE QUESTION: "Why is it 6 FLOPs per parameter per token? How much
compute does training a model actually take?"
WHO IS ASKING: a research engineer who has seen "6 × params × tokens" in
a paper or an MFU formula, uses it, and can't say where the 6 comes from,
or whether to trust it when estimating a run's GPU-hours.
THE ANSWER IN ONE SENTENCE: each weight does one multiply and one add per
token going forward (2), and twice that coming back, once to pass the
error to the layer before and once to build its own gradient (4), so
training costs 6 × params × tokens.
THE SEARCH PHRASE: flops llm (checked 10/27 via YouTube's autocomplete
endpoint and results page; second choice "scaling laws llm". The take
keeps it: line 1 says "LLM" and "FLOPs" in its first clause.)

**One idea:** every weight is touched three times per token (once forward,
twice back), two FLOPs each time. That's the 6.

**Source:** the VO is `script.md` ("As recorded"), not the planned script
in `../SCRIPTS.md`. v1 of this file (the draft before recording) is in
git history.

Series context: ep 3 of `../SERIES.md`. Home of "6 × params × tokens,
forward 2 + backward 4". What a FLOP is belongs to ep 2 (here only "one
multiply and one add"); MFU belongs to ep 7 (not mentioned: the take
dropped the closer).

## Ledger (every beat copies these, nothing invented per beat)

From `../SERIES.md` (series ledger), used identically in every beat:

- A FLOP: one floating-point multiply or one add. **FLOPs** is a count,
  **FLOPS** a rate (`TFLOPS`).
- FLOPs per token, training: **6 × params** (forward 2, backward 4).
- **The tiny layer:** 3 inputs (`x1 x2 x3`), 2 outputs (`y1 y2`), **6
  weights** (the 2 × 3 matrix `W`). Forward **12 FLOPs** = 2 × 6.
  Backward 24 = 4 × 6. Total **36** = 6 × 6.
- Model: **8B parameters**, dense transformer (Llama-3-8B sized), bf16.
- Throughput: **15,000 tokens/s per GPU** (one B200 in an 8-GPU run;
  always "per GPU").
- Achieved: 6 × 8e9 × 15,000 = **720 TFLOPS** (7.2e14 FLOP/s), a rate.
- Code on screen (`../_kit/data.js`, `code.sixN`):
  `flops = 6 * n_params * n_tokens` / `6 * 8e9 * 15_000  # 7.2e14 /s`.
- Every on-screen string of this episode is in `_kit/ep.js` (`EP`), the
  rest in `../_kit/data.js`.

## Beats (from what was said)

The take's changes from v1 (`script.md`, "Where the take leaves the
script"): line 1 says "about six" and the 2 / 4 split is its own
sentence; "Backward costs twice the forward", the *(if time)* Llama 3
line and the closer were not recorded. So v1's beat 06 keeps only "That's
six per weight per token", beat 08 (32 years) and beat 09 (the GPU-hours
card) are dropped, and v1's beat 07 splits in two at the sentence. The
Short ends on "720 teraflops" over the chip and the card.

| beat | VO | visual |
|---|---|---|
| 01_hook | Training an LLM costs about six FLOPs per parameter per token. | Frame 0 already working: the tiny layer mid-stage (3 input dots left, 2 output dots right, 6 weight lines, teal), a value pulse running along the lines; above it the FLOP bar, full, in three equal segments, labelled `→ 2` under the first and `← 4` under the other two; the readout `6 × params` (magenta hero). On "six FLOPs" the whole bar swells once. |
| 02_layer | Almost every parameter sits in a weight matrix. Here's a tiny one: three inputs, two outputs, six weights. | The bar and readout clear. On "weight matrix" the matrix `W` (2 × 3 cells) grows in under the layer with `y = W x` beside it (hero: the matrix). On "three inputs" the input dots pulse, "two outputs" the output dots, "six weights" the six lines flash once in order, each with its matrix cell (hero: the lines). |
| 03_forward | Going forward, each weight does one multiply and one add. So you have two FLOPs per weight, twelve for this entire layer. | The bar returns empty. Left to right, a value runs along each line, the line ticks `×` then `+`; the first segment fills one sixth per line; the readout counts `0 FLOPs` → `12 FLOPs`, two per line; on "twelve" it lands (magenta hero: the readout). |
| 04_back_input | Coming backwards now, the error has to reach the layer before. So the same weights in reverse, another multiply and add each. | Output labels become `dy1 dy2`, inputs `dx1 dx2 dx3`; `dx = Wᵀ dy` replaces `y = W x`. The error runs right to left along the same six lines, each ticking `×`, `+`; the second segment fills; readout 12 → 24. Hero: the backward flow (lines and the filling segment). |
| 05_back_weight | Then each weight needs its own gradient for the optimizer. Error times input, added to a running total, is two more. | Inputs back to `x1 x2 x3` (outputs stay `dy`); the matrix label becomes `dW`, `dW = dy xᵀ` beside it. Each weight's cell fills as its gradient lands (`×` on "error times input", `+` on "running total"); the third segment fills; readout 24 → 36. Hero: the `dW` matrix. |
| 06_total | That's six per weight per token. | The bar's labels go back to the hook's `→ 2` / `← 4`, the readout becomes `36 = 6 × 6` (magenta hero). |
| 07_code | So training compute is six times parameters times tokens. | The layer shrinks into one core cell of the series chip as the chip fades in (CPU and queue, cells lit teal, GPU memory: the rest image); the bar and readout clear. The code card in the bottom slot types `flops = 6 * n_params * n_tokens` (magenta hero: the line). |
| 08_run | An 8-billion-parameter model at 15,000 tokens per second per GPU is doing 720 teraflops. | The card types `6 * 8e9 * 15_000  # 7.2e14 /s` as it is said; on "720 teraflops" the label under the chip turns from `GPU` to `720 TFLOPS` (magenta hero: the chip and its label). Still from there to the end. |

Layout (px, 1080 × 1920; safe x 65–950, y 230–1536):

- Top, y 250–470 (the chip's top slot, free until beat 07): the readout
  (72 px, centred) and the FLOP bar under it (three segments, x 65–950),
  segment labels under the bar.
- Middle, y 520–940: the tiny layer. Input dots x 240, output dots x 760;
  labels outside the dots (`x1` left, `y1` right).
- Below, y 980–1100: the matrix `W` (2 × 3 cells) right, its formula left.
- Beats 07–08: the series chip (`../_kit/chip.js`, y 450–1078) and the
  code card docked at the band top (cy 1345). Captions anchored bottom
  for the whole Short (`assemble.py --captions-anchor bottom`), every
  caption one line.
- One magenta hero at a time: `6 × params` → the matrix → the lines →
  the readout → the backward flow → `dW` → `36 = 6 × 6` → the code line
  → `720 TFLOPS`.

## Final beats (the contract; `vo_final.wav` 41.140 s, master seconds)

Beat brief: `agents/beat-brief-hyperframes.md` plus this table; seam
states `SC.SEAM` in `_kit/seam.js`; links per beat: `vendor`
(`../../../_shared/web/vendor`), `kit` (`../../_kit`), `ep` (`../_kit`).

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.000 | 4.400 | Training an LLM costs about 6 FLOPs per parameter per token. |
| 2 | `02_layer` | 4.400 | 5.500 | Almost every parameter sits in a weight matrix. Here's a tiny one, 3 inputs, 2 outputs, 6 weights. |
| 3 | `03_forward` | 9.900 | 6.325 | Going forward, each weight does one multiply and one add. So you have 2 FLOPs per weight, 12 for this entire layer. |
| 4 | `04_back_input` | 16.225 | 6.255 | Coming backwards now, the error has to reach the layer before. So the same weights in reverse, another multiply and add each. |
| 5 | `05_back_weight` | 22.480 | 6.300 | Then each weight needs its own gradient for the optimizer. Error times input added to a running total is 2 more. |
| 6 | `06_total` | 28.780 | 1.850 | That's 6 per weight per token. |
| 7 | `07_code` | 30.630 | 4.070 | So training compute is 6 times parameters times tokens. |
| 8 | `08_run` | 34.700 | 6.440 | An 8 billion parameter model at 15,000 tokens per second per GPU is doing 720 teraflops. |

## Seam states (`_kit/seam.js`; layer fields as `SC.LAYER.LREST`, chip fields as `SC.REST`, unless named)

Beats 01–06 show no chip part (cpu, queue, chip, GPU memory, strip and
card all at 0). Beats 07–08 show the chip at rest (CPU, queue, GPU
memory, cells lit 32 %, shimmering), no strip, the code card at cy 1246
(bottom edge 1330), the layer gone.

| Cut | After beat | Hero | State |
|---|---|---|---|
| 0 | frame 0 | readout | layer, labels `x` / `y`, value pulses running (`run` 1); bar full, split 0 (`→ 2` / `← 4`); readout `6 × params`; no matrix, no formula |
| 1 | hook | readout | the same, pulses stopped (`run` 0) |
| 2 | layer | none | bar and readout gone; matrix `W` full (teal); formula `y = W x` |
| 3 | forward | readout | pass fwd done (lines teal); bar `[1, 0, 0]` split 1 (`→ 2` / `← 2` / `← 2`); readout `12 FLOPs`; `W`, `y = W x` |
| 4 | back to input | back | pass back done (lines magenta, segment 2 magenta); labels `dx` / `dy`; bar `[1, 1, 0]`; readout `24 FLOPs`; `W`, `dx = Wᵀ dy` |
| 5 | back to weights | grad | pass grad done (lines, segment 3 and the `dW` cells magenta); labels `x` / `dy`; matrix `dW` fill 6; bar `[1, 1, 1]`; readout `36 FLOPs`; `dW = dy xᵀ` |
| 6 | total | readout | as 5 with lines and cells teal; bar split 0 (`→ 2` / `← 4`); readout `36 = 6 × 6` |
| 7 | code | none (the card's line 1 is lit) | chip at rest, shimmer on; card `code.sixN`, line 1 typed (31 characters), lit `sixN`, no cursor |
| 8 | end | chip | shimmer off (still); title `720 TFLOPS`; card fully typed, nothing lit |

## Cut list

Raw take 48.2 s. Loudnorm-only chain (`enhance_vo.sh` default; Studio
Sound unknown, so no denoise), floor −73 dB. `tighten_vo.py --max-gap
0.25 --noise=-40dB --level -14` → **45.4 s, 10 pieces, no phrase cuts.**

- `--noise auto` (−54 dB) found only 4 pauses (breaths sit above it) and
  left 48.6 s; −40 dB caps them all, as 014 ep02 needed.
- `script.md` lists no repeats and no ear checks for this episode; a
  read of the Parakeet transcript finds no flub or repeated phrase.
- Kept as said: "about six", "Coming backwards now", "So the same
  weights", "for this entire layer".
- The Short ends on "teraflops." (the take's end).
- Parakeet on `vo_final.wav` reads clean, every sentence whole.
- After the first cut (Chris, 10/31): "You spend 2 FLOPs on the forward
  pass and about 4 on the backward pass" cut as redundant; it dragged out
  the opening. `cut_vo.py --cut 4.26-8.52` (both edges in digital
  silence) → **41.14 s**. Beat 01 is 4.40 s; beats 02–08 are untouched,
  shifted −4.26 s. Re-transcribed: "…per token. Almost every
  parameter…" reads clean.

Caption fixes in `words.json`: "in" → "an" (Training an LLM), "flops" →
"FLOPs", "1" → "one" (one multiply, one add), "15 ,000" → "15,000",
"multiply," → "multiply".

## Facts to keep straight (notes, not VO)

- **Source of 6N:** Kaplan et al. 2020, *Scaling Laws for Neural Language
  Models*, §2.1: C_forward ≈ 2N + 2·n_layer·n_ctx·d_model; "accounting
  for the backwards pass (approximately twice the compute as the forwards
  pass)", C ≈ 6N FLOPs per training token. Chinchilla uses the same rule.
  Kaplan's N is non-embedding parameters.
- **Embeddings:** Llama-3-8B's 8.0B includes ~0.5B input embedding (a
  lookup, no matmul), so 6 × 8e9 overcounts by ~7 %. Companion note.
- **"One multiply and one add per weight"** is the multiply-accumulate
  count (a matmul of m×k by k×n is 2mkn FLOPs). Don't say "exactly".
- **dW per token is a multiply; the add is the accumulate** across the
  batch's tokens, which is why the VO says "added to a running total".
- **Left out of 6N:** attention scores (~13 % for Llama-3-8B at 8K
  context, before the causal mask), the optimizer step (per step, not per
  token), activation recompute (8N: HFU, not MFU, ep 7's companion).
- **720 TFLOPS is a rate**, from tokens/s; the card keeps the "/s".
