ENGINE: hyperframes

# FLOPs explained: storyboard (v1, VO draft for Chris)

THE QUESTION: "FLOP is a floating point operation? What does that mean
exactly? Why are FLOPs a thing with GPUs?"
WHO IS ASKING: a research engineer who reads "2,250 teraflops" on a GPU
spec sheet and "10^24 FLOPs" in a training report, knows it's a measure of
compute, and can't say what one FLOP is, why FLOPs vs FLOPS, or why AI
counts work this way.
THE ANSWER IN ONE SENTENCE: a FLOP is one multiply or one add on two
floating-point numbers (decimals stored like scientific notation in
binary); FLOPs counts them, FLOPS counts them per second, and because a
transformer is nearly all matmuls, which are only multiplies and adds,
counting FLOPs counts the work.
THE SEARCH PHRASE: flops explained (checked 10/27 via YouTube's
autocomplete endpoint, not a browser: "flops explained" autocompletes and
its top results are AI explainers ("FLOPS: The New Benchmark For AI
Performance", "FLOPS Demystified: AI and the math behind DeepSeek training
costs"), but the other suggestions are flip-flops (circuits, sandals) and
movie flops, so the title must say AI or GPU. "teraflops explained" also
autocompletes; its top result is PS5/Xbox, so it is the second phrase, not
the first. "what is a flop" autocompletes to floppy disks; "flops ai"
results are on topic ("FLOPs vs FLOPS Explained: LLM Compute Made Simple")
but the phrase is not offered.)

**Titles (runbook step 9, Chris picks; both carry the search phrase):** search `FLOPs Explained Made Simple (Beginner Friendly)` (47 chars) · hook `Every AI engineer needs this number (FLOPs explained)`

**One idea:** a FLOP is one multiply or one add, and AI is nearly nothing
else, so FLOPs are the unit of AI work.

**Source note:** Chris's input is questions in a chat ("FLOP is a floating
point operation? What does that mean exactly? Why are FLOPs a thing with
GPUs?") plus an explanation he read and liked, so this VO is a draft in
his voice for him to rewrite. His own words kept: "what does that mean
exactly" became the floating-point beat; "why are FLOPs a thing with GPUs"
became the matmul beat.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip, one
cell zoomed to an expression, a counter, a number card and a code card.
Nothing needs Manim.

Series context: ep 2 of `../SERIES.md` (Understanding the GPU). Home of
"what a FLOP is; FLOPs vs FLOPS; why chips are rated in them". Floating
point gets the one-sentence picture here (it is what the F means); bit
widths, bf16 vs fp8 and dense vs sparse are ep 4 (one clause each here:
"in bf16", "dense ... at the precision you train in"). 6 × params × tokens
is ep 3: the 720 trillion is shown as code, never derived in the VO.
Comes before ep 7, whose MFU fraction is FLOPS ÷ FLOPS.

## Ledger (every beat copies these, nothing invented per beat)

- A FLOP: one floating-point multiply or one add (series ledger).
- GPU: one **B200**, bf16 dense peak **2,250 TFLOPS** ("about 2,250
  teraflops"); the sparse figure (4,500) is never shown here.
- tera = 10^12 (a trillion).
- The count example: the series run, an **8B-parameter** model on
  **15,000 tokens** (one second of the ep 7 run): 6 × 8e9 × 15,000 =
  **7.2 × 10^14 FLOPs**, said "about 720 trillion FLOPs".
- That count at peak: 7.2e14 / 2.25e15 = **0.32 s** (shown on the code
  card only; it is why the run is 32 % MFU in ep 7, not said here).
- Floating-point examples: **0.0000001** (a ten-millionth) and
  **3,000,000** (three million), on screen as `1 × 10⁻⁷` and `3 × 10⁶`.
- The chip: the series 12 × 12 grid of core cells, dark at rest, teal
  when working; no label claims a core count.

## VO (draft: 136 words without the if-time beat, 153 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | A FLOP is one multiply or one add, and it's the unit all AI compute is measured in. | Frame 0 already working: the series chip mid-stage, the 12 × 12 grid flickering teal. One cell (row 6, col 6) zooms out to a card above the chip: `a × b + c`; on "multiply" the `×` lights, on "add" the `+` lights, and a counter under the card ticks `FLOPs: 1 → 2`. Magenta hero: the counter. ~5 rows of stage. |
| 02_float | Computers store decimals as floating point: scientific notation in binary, a sign, digits and an exponent. The point floats, so one format holds a ten-millionth and three million. | The `a` in the card expands into a number strip: `+ 1.0 × 10⁻⁷` over `+ 3.0 × 10⁶`, each split into three labeled boxes `sign · digits · exponent` (no bit counts; widths are ep 4). On "the point floats" the decimal point slides along `0.0000001` → `3000000.`. Magenta hero: the exponent box. |
| 03_everything | Every weight, activation and gradient is one. | The strip folds back into `a`; the zoom pulls out to the whole grid, every cell now showing a tiny `×+` glyph for a beat. Labels fade in left of the chip: `weights`, `activations`, `gradients`, each with an arrow into the grid. |
| 04_count | FLOPs, small s, is a count. Training an 8-billion-parameter model on 15,000 tokens costs about 720 trillion FLOPs. | Code card bottom-middle, line 1 types: `flops = 6 * 8e9 * 15_000  # 7.2e14`. The counter above runs up to `9.6 × 10¹⁴ FLOPs` as the line lands. The lowercase `s` in `FLOPs` on the counter is the magenta hero. |
| 05_rate | FLOPS, capital S, is per second. A B200 peaks near 2,250 teraflops in bf16. Tera is a trillion. | A spec chip label appears on the chip's top edge: `B200 · bf16 dense · 2,250 TFLOPS`; under it a small gloss `tera = 10¹²`. Code card line 2 types: `seconds = flops / 2250e12  # 0.32 at peak`. The whole grid lights teal for 0.32 s on a small timer, then rests. Magenta hero: the capital `S`. |
| 06_why | A transformer's compute is nearly all matrix multiplies, and a matmul is only multiplies and adds. GPUs are built to do exactly that, thousands at once. | Above the chip, a small matmul: a 3 × 2 weight block times a column; one output cell expands to `w₁x₁ + w₂x₂ + w₃x₃` and each `×` and `+` drops into a cell of the grid, which lights teal, many cells at once. Magenta hero: the one expanded output cell. |
| 07_bill *(if time)* | Divide a run's FLOPs by the FLOPS you get and you have GPU-hours. GPU-hours are the bill. | A one-line fraction over the code card: `FLOPs ÷ FLOPS = GPU-hours → $`. No numbers. |
| 08_close | Next time you read a GPU spec, find dense FLOPS at the precision you train in. That's your run's real ceiling. | Final visual: a spec-sheet card with three rows (`FP8 sparse`, `BF16 sparse`, `BF16 dense`); the `BF16 dense · 2,250 TFLOPS` row in magenta, the others greyed. The chip under it, all cells lit. Takeaway only, no outro. |

Line 1 is the answer and lands "FLOP" (the search phrase) in its first two
words; the `a × b + c` card and counter are on screen from frame 0. Beat 07
is the *(if time)* cut: the viewer keeps "the unit AI compute is measured
in" without the billing chain. Beat 02 stays: it is Chris's "what does that
mean exactly", the F in FLOP. Beat 04 is the code beat (real Python that
runs); the `6 *` on screen is not explained here (ep 3). The closer is the
viewer's next move (read a spec sheet correctly), not line 1 again.

## Facts to keep straight (notes, not VO)

- **One FMA counts as two FLOPs.** GPUs do a fused multiply-add in one
  instruction, but NVIDIA's peak figures count it as two operations (the
  Nsight docs define peak as cores × clock × 2 for this reason). That is
  why the VO says "one multiply or one add" and the card shows `a × b + c`
  ticking twice. Some papers count a MAC as one op; companion material.
- **A matmul of (m × k) by (k × n) costs 2·m·k·n FLOPs** (Megatron-LM,
  Narayanan et al. 2021). "Nearly all of a transformer's compute is
  matmuls": ELECTRA's appendix says matrix multiplies account for most of
  the compute; per-layer estimates for Llama-style models put it well over
  90 % at typical sequence lengths. Attention's score computation is also
  a matmul but grows with sequence length; softmax, norms and activations
  are the small non-matmul remainder. The VO says "nearly all", not a
  percentage.
- **B200 bf16 dense 2,250 TFLOPS, sparse 4,500** (Lenovo HGX B200 guide,
  SemiAnalysis InferenceX; NVIDIA's own datasheet not retrieved). Series
  ledger number.
- **The floating-point examples:** fp32 holds 3,000,000 exactly; bf16 only
  approximately (8 significant bits), and 10⁻⁷ is approximate in any
  binary format. "Holds" means "is in range of": true for fp32 and bf16,
  false for fp16 (3 × 10⁶ is past its max of 65,504, and 10⁻⁷ is below its
  smallest normal number). The card shows the values in decimal scientific
  notation and does not name a format; ep 4 owns the bit widths.
- **720 trillion FLOPs for 15,000 tokens** uses 6 × params per token (ep
  3), which ignores attention FLOPs and activation recompute.
- **"GPUs are built to do exactly that, thousands at once"**: one clause of
  ep 1's GPU-vs-CPU fact; tensor cores (ep 5) are what make the bf16
  matmul peak, CUDA cores do the rest. Not said here.
- **The closer:** dense FLOPS at your training precision is the right
  peak for MFU and for comparing chips' compute; whether a run gets near
  it is ep 5 (memory-bound ops) and ep 7 (MFU). Spec sheets often lead
  with the sparse or fp8/fp4 number.
- `torch.utils.flop_counter.FlopCounterMode` counts a step's real FLOPs;
  companion material, not this Short.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top: the zoom card (`a × b + c`, the number strip in beat 02, the
  matmul in beat 06, the spec-sheet card in beat 08), ~1.5 rows.
- Stage middle: the series chip, 12 × 12 grid, with its spec label on the
  top edge from beat 05; the FLOPs counter directly under the zoom card,
  between it and the chip.
- Stage bottom-middle: the code card (beats 04, 05; the if-time fraction
  in 07).
- One magenta hero at a time: the counter → the exponent box → (none,
  labels teal) → the small `s` → the capital `S` → the expanded matmul
  output cell → the `BF16 dense` row.
