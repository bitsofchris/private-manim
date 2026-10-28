ENGINE: hyperframes

# Why 6 FLOPs per parameter per token: storyboard (v1, VO draft for Chris)

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
endpoint and results page, not a browser: "flops llm" autocompletes
(typing "llm flops" offers it), and its results are LLM-compute
explainers ("FLOPs vs FLOPS Explained: LLM Compute Made Simple", "FLOPS
Demystified: AI and the math behind DeepSeek training costs"). "scaling
laws llm" autocompletes and is on topic (one result has a chapter "The
Compute Budget Equation (C ≈ 6ND)") but its viewers want the loss curves,
not the count; second choice. No autocomplete for "training compute"
(computer courses), "flops per token", "how much compute to train llm",
"llm training cost", "flops to train", "training flops" (soccer). Overlap
note: ep 2's phrase is "flops explained", whose results share some videos
with this one; ep 3's title adds "LLM" and "train" to split them.)

**Titles (runbook step 9, Chris picks):** search `How Many FLOPs to Train an LLM? (6 per Parameter, Explained)` · hook `Backprop costs twice the forward pass. Here's why.`

**One idea:** every weight is touched three times per token (once forward,
twice back), two FLOPs each time. That's the 6.

**Source note:** Chris asked "Why is it 6 flops per parameter per token?
Work that out for me" in the 10/27 storyboard session and liked the
worked answer (the tiny layer, dx = Wᵀ·dy, dW = dy·xᵀ). He has no written
sentences on this, so the VO is a draft in his voice for him to rewrite.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the tiny 3 → 2
layer drawn as six weight lines, a FLOP counter, the series chip in the
payoff beat, and a code card. Nothing needs Manim.

Series context: ep 3 of `../SERIES.md` (Understanding the GPU). Home of
"6 × params × tokens, forward 2 + backward 4". What a FLOP is belongs to
ep 2 (one clause here: "one multiply and one add"); MFU belongs to ep 8
(one clause at most: the closer's "what one GPU actually delivers").

## Ledger (every beat copies these, nothing invented per beat)

- A FLOP: one floating-point multiply or one add (ep 2's home; not
  re-defined here).
- **The tiny layer:** 3 inputs (x1, x2, x3), 2 outputs (y1, y2), **6
  weights** (w11 … w23). Forward **12 FLOPs** = 2 × 6. Backward 24 = 4 × 6.
  Total **36** = 6 × 6.
- FLOPs per token, training: **6 × params** (forward 2, backward 4).
- Model: **8B parameters**, dense transformer (Llama-3-8B sized), bf16.
- Throughput: **20,000 tokens/s** on one **B200**.
- Achieved: 6 × 8e9 × 20,000 = **960 TFLOPS** (9.6e14 FLOP/s).
- *(if time)* Llama 3 8B pretraining data: **15 trillion tokens** (Meta's
  model card says "over 15T"). At 20,000 tokens/s: 15e12 ÷ 2e4 = 7.5e8 s
  = **about 24 years** on one B200 (23.8).
- Code on screen: `flops = 6 * n_params * n_tokens`.

## VO (draft: 143 words without the if-time beat, 161 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Training an LLM costs six FLOPs per parameter, per token: two forward, four back. | Frame 0 already working: the tiny layer mid-stage (3 teal input dots left, 2 output dots right, 6 weight lines between) with a token chip passing through; a counter above it reads `6 × params` in magenta, split under it into `2 →` and `← 4`. ~6 rows of stage. |
| 02_layer | Almost every parameter sits in a weight matrix. Here's a tiny one: three inputs, two outputs, six weights. | The counter clears. The layer settles: inputs labeled `x1 x2 x3`, outputs `y1 y2`, each of the 6 lines labeled `w11 … w23`. On "six weights" the lines flash once in order. Beside it, small, the matrix form `y = W x` with `W` as a 2 × 3 grid of the same six cells. |
| 03_forward | Going forward, each weight does one multiply and one add. Two FLOPs per weight, twelve for the layer. | Left to right, each weight line ticks `×` then `+` as a value flows along it; a counter top-right climbs 0 → 12, two per line. Under the counter: `forward = 2 × 6`. Magenta hero: the counter. |
| 04_back_input | Coming back, the error has to reach the layer before: the same weights in reverse, another multiply and add each. | Error dots (`dy1 dy2`) appear on the outputs and flow right to left along the same six lines to `dx1 dx2 dx3`; each line ticks `×`, `+` again; counter 12 → 24. Small label: `dx = Wᵀ · dy`. Magenta hero passes to the backward flow. |
| 05_back_weight | Then each weight needs its own gradient, for the optimizer. Error times input, added to a running total. Two more. | Each weight line lights a third time: a small gradient tag `dw` hangs off each line, filled by `dy × x` and then `+` into a running-total bar under the tag; counter 24 → 36. Label: `dW = dy · xᵀ`. |
| 06_total | That's six per weight, per token. Backward costs twice the forward. | The three passes stack as bars beside the layer: forward 12 (teal), back-to-input 12, back-to-weights 12 (backward bracket = 24). Counter reads `36 = 6 × 6` in magenta. |
| 07_code | So training compute is six, times parameters, times tokens. An 8-billion-parameter model at 20,000 tokens a second is doing 960 teraflops. | The tiny layer shrinks into one core cell of the series chip (12 × 12 grid, mid-stage, cells lighting teal). The code card bottom-middle (the payoff, real lines): `flops = 6 * n_params * n_tokens` / `6 * 8e9 * 20_000  # 9.6e14 per second`. Each line lands on its number; a label by the chip: `960 TFLOPS`. Magenta hero: the `6` in the code. |
| 08_scale *(if time)* | At that pace, Llama 3 8B's 15 trillion tokens would keep one B200 busy for about 24 years. | A token counter under the chip races to `15T`; a calendar strip beside it flips to `~24 years`. |
| 09_close | Before your next run, multiply six by parameters by tokens. Divide by what one GPU actually delivers, and that's your GPU-hours. | Final visual: the code card alone, three lines: `flops = 6 * n_params * n_tokens` / `seconds = flops / flops_per_sec_per_gpu` / `gpu_hours = seconds / 3600`, `gpu_hours` in magenta. Takeaway only, no outro. |

Line 1 is the answer and says "FLOPs" and "LLM", the search phrase, in
its first clause; the 2 + 4 split is on screen from frame 0. Beats 03–05
are the working Chris asked for, one pass per beat, so each beat adds one
new step and the counter (12 → 24 → 36) carries the thread. Beat 06 is
short on purpose: it is the "backward = 2 × forward" takeaway, said once.
Beat 08 is the *(if time)* cut: a vivid scale, but the closer stands
without it. The closer is the viewer's next move (estimate a run), not
line 1 again; "what one GPU actually delivers" is the one-clause nod to
MFU (ep 8) and keeps the closer true (dividing by peak would undercount
the hours by about 2×).

## Facts to keep straight (notes, not VO)

- **Source of 6N:** Kaplan et al. 2020, *Scaling Laws for Neural Language
  Models*, §2.1: C_forward ≈ 2N + 2·n_layer·n_ctx·d_model; "accounting
  for the backwards pass (approximately twice the compute as the forwards
  pass)", C ≈ 6N FLOPs per training token; total C = 6NBS (§3.3).
  Chinchilla (Hoffmann et al. 2022) uses the same rule. Kaplan's N is
  **non-embedding** parameters.
- **Embeddings:** Llama-3-8B's 8.0B includes ~0.5B input embedding
  (128,256 × 4,096), a table lookup with no matmul, so 6 × 8e9 overcounts
  by ~7 %. The output head (also ~0.5B, untied) is a real matmul and does
  count. The ledger keeps 8e9 for series consistency; companion note.
- **"One multiply and one add per weight"** is the multiply-accumulate
  count. Strictly, y1 = w11·x1 + w12·x2 + w13·x3 is 3 multiplies + 2 adds
  (5, not 6) without a bias; the ledger's "12" counts each weight's
  multiply-add pair, which is the convention (a matmul of m×k by k×n is
  2mkn FLOPs). Don't say "exactly" anywhere.
- **dW per token is a multiply; the add is the accumulate.** dw_ij =
  dy_i · x_j for one token is one multiply; the add comes from summing
  that product into the weight's gradient across the tokens in the batch.
  That's why the VO says "added to a running total", not "multiply and
  add". Per token, per weight, it is still 2 FLOPs.
- **dx for the first layer** isn't needed (nothing before it to send the
  error to); negligible over 32 layers.
- **Left out of 6N:** (1) attention scores (QKᵀ and softmax·V use no
  weights and grow with sequence length): Kaplan's context term is
  2·n_layer·n_ctx·d_model per token forward; for Llama-3-8B (32 layers,
  d_model 4,096) at n_ctx 8,192 that is ~2.1e9 vs 2N = 1.6e10, ~13 %
  before the causal mask halves it; Kaplan drops it when d_model >
  n_ctx/12. Grows past that at long context. (2) The optimizer step: per
  step, not per token, a few FLOPs per weight, negligible. (3) Activation
  recompute: an extra forward, 8N per token; counting it gives HFU, not
  MFU (ep 8's companion).
- **960 TFLOPS is a rate** (FLOP/s), from tokens/s. The total for a run
  is 6 × N × D in FLOPs. Beat 07 keeps the "per second" on the code card.
- **24 years** (beat 08) is tokens ÷ tokens/s at the ledger's throughput,
  a hypothetical: Meta trained Llama 3 8B on many H100s (model card: 1.3M
  H100-80GB GPU-hours, pretraining). Say "would", never "took".
- To verify before publish: nothing new beyond the above; Meta's "over
  15T tokens" is from the Llama 3 model card (github.com/meta-llama/llama3
  MODEL_CARD.md), Kaplan §2.1 read on arXiv 2001.08361 (HTML).

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top-right: the FLOP counter (beats 01, 03–06), ~1 row.
- Stage middle: the tiny 3 → 2 layer, ~4 rows, inputs left, outputs right;
  `y = W x` / `dx = Wᵀ·dy` / `dW = dy·xᵀ` labels under it, one at a time.
  From beat 07 the layer shrinks into one cell of the series chip
  (12 × 12 grid, the same drawing as every episode).
- Stage bottom-middle: the code card (beats 07, 09).
- One magenta hero at a time: `6 × params` → the counter → the backward
  flow → `36 = 6 × 6` → the `6` in the code → `gpu_hours`.
