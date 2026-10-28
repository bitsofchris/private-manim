ENGINE: hyperframes

# bf16 vs fp16 vs fp32: storyboard (v1, B200 numbers; VO draft for Chris)

THE QUESTION: "Why does bf16 / fp8 make training faster, and what do fp32,
fp16, bf16 even mean?"
WHO IS ASKING: a research engineer who sees `bf16=True` or
`torch.autocast` in every training script, knows it makes things faster,
and can't say why, or why bf16 and not fp16.
THE ANSWER IN ONE SENTENCE: fewer bits per number means more numbers per
memory read and more multiply-adds per tensor-core cycle, so peak FLOPS
doubles each time the bits halve; bf16 keeps fp32's 8 exponent bits, so it
has fp32's range and trains without fp16's overflow.
THE SEARCH PHRASE: bf16 vs fp16 (checked 10/27 via YouTube's autocomplete
endpoint and results page, not a browser: "bf16 vs fp16" autocompletes
verbatim and "bf16" offers it second; results are ML data-type explainers,
"Data Types Explained: FP32 vs FP16 vs BF16 in Deep Learning" first.
"fp32 vs fp16" also autocompletes with the same results, so it goes in the
title as the second phrase. "fp8 training" autocompletes but its results
are conference talks for practitioners already doing it. "mixed precision
training" autocompletes, results on topic; kept for the description.
"floating point explained" autocompletes but returns general CS
(Computerphile), not ML.)

**One idea:** a number's bit width sets how fast the chip can do math on
it; bf16 wins because it halves the bits without shrinking the range.

**Source note:** Chris's input is questions in the 10/27 chat ("what is
floating point", "why does bf16 / fp8 make it faster"), with no answer
sentences, so this VO is a draft in his voice for him to rewrite (same as
ep 7 and 015).

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): bit-box rows, the
series chip, a spec-sheet card and a code card. Nothing needs Manim.

Series context: ep 4 of `../SERIES.md` (Understanding the GPU). Home of
"floating point, precision, bf16/fp8, dense vs sparse spec". What a FLOP
is belongs to ep 2 (no clause needed here: "math" carries it); tensor
cores get one clause ("tensor-core cycle"), their home is ep 5; bf16 as
an MFU lever is cut ep 11.

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one **B200**. Dense tensor-core peaks (NVIDIA HGX B200 spec,
  8-GPU figures ÷ 8, sparse ÷ 2): **TF32 1,125 TFLOPS**, **bf16/fp16
  2,250 TFLOPS** (series ledger), **fp8 4,500 TFLOPS**. Sparse is 2× each;
  the only sparse number shown is **4,500 bf16 "sparse"** on the spec card
  in beat 06, crossed out.
- Bit layouts (sign | exponent | mantissa), boxes drawn to scale, one box
  per bit:
  - **fp32** 1 | 8 | 23 (32 bits)
  - **fp16** 1 | 5 | 10 (16 bits), max **65,504**
  - **bf16** 1 | 8 | 7 (16 bits), max ≈ fp32's (≈ 3.4 × 10³⁸)
  - **fp8 (E4M3)** 1 | 4 | 3 (8 bits)
- Doubling: half the bits → 2× the numbers per memory read → 2× peak
  dense FLOPS (TF32 → bf16 → fp8: 1,125 → 2,250 → 4,500).
- Sparse = NVIDIA's **2:4 structured sparsity**: two of every four values
  zero, in a fixed pattern.
- Code (real, runs):
  ```python
  with torch.autocast("cuda", dtype=torch.bfloat16):
      loss = model(x)
  loss.backward()
  ```
- The chip: the series 12 × 12 grid; in beat 03 each cell holds 1 number
  (fp32 row), then 2 (bf16), then 4 (fp8), drawn as tick marks inside the
  cell.

## VO (draft: 144 words without the if-time beat, 162 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | bf16 makes training faster because each number is half the bits of fp32. Half the bits, twice the peak math. | Frame 0 already working: three bit-box rows stacked top-middle, widths to scale: `fp32` (32 boxes), `fp16` (16), `bf16` (16), labels left. Below, the series chip (12 × 12 grid) with cells lit teal. On "half the bits" the bf16 row is magenta (hero) and the chip's cells each split into two ticks. ~4 rows of stage. |
| 02_parts | A floating-point number has three parts: a sign, an exponent for how big it gets, and a mantissa for how precise. | The fp32 row grows to full width; its boxes color by field as each is named: sign (1 box), exponent (8), mantissa (23), each field labeled under the row. Magenta hero passes to the field being named. The other rows dim to grey. |
| 03_faster | Fewer bits means more numbers per memory read and more multiply-adds per tensor-core cycle. A B200 peaks near 2,250 teraflops in bf16. fp8 doubles that. | The HBM slab right of the chip, a pipe into the grid: a stream of number tiles flows in; at fp32 one tile per cell, at bf16 two, at fp8 four (tiles shrink as bits halve, the pipe stays the same width). A small ladder top-right fills as each row lands: `TF32 1,125` / `bf16 2,250` / `fp8 4,500` TFLOPS (dense). Magenta hero: the `bf16 2,250` rung, then `fp8 4,500`. |
| 04_range | fp16 is also 16 bits, but it spends them on precision, so anything past 65,504 overflows. bf16 keeps fp32's 8 exponent bits: same range, less precision, and training stays stable. | fp16 and bf16 rows side by side under the fp32 row, exponent fields aligned: fp16 `1 | 5 | 10`, bf16 `1 | 8 | 7`; bf16's 8 exponent boxes line up with fp32's 8 (a bracket joins them, label "same range"). A number line under them: a value climbs past `65,504`, the fp16 row flashes `inf`; the bf16 row holds it. Magenta hero: bf16's exponent field. |
| 05_fp8 *(if time)* | fp8 keeps just three mantissa bits, so training in it needs a scaling library like NVIDIA's Transformer Engine. | The fp8 row `1 | 4 | 3` (8 boxes) slides in under bf16; a small `× scale` tag clips onto it, label `Transformer Engine`. |
| 06_sparse | One spec-sheet trap: the biggest number is sparse. It's twice dense, and only counts if two of every four weights are zero. Compare dense, in the precision you train in. | A spec card top-middle: `bf16  4,500 TFLOPS*` with footnote `*with sparsity` (magenta hero). A weight row below it shows the 2:4 pattern: in every group of four, two boxes grey out (zero). The 4,500 crosses out; `2,250 dense` replaces it and goes teal. |
| 07_close | In PyTorch, wrap your forward pass in autocast with bf16. You get the faster math without the overflow. | The code card, bottom-middle (the payoff beat, real lines from the ledger); `dtype=torch.bfloat16` is the magenta hero. Above it, the chip with every cell holding two ticks and the bf16 row on top. Takeaway only, no outro. |

Line 1 lands the answer in its first clause ("makes training faster
because ... half the bits") and frame 0 shows fp32, fp16 and bf16, so the
title's terms are on screen at 0 s and fp16 is said by ~20 s. Beat 05 is
the *(if time)* cut: the viewer trains in bf16, and fp8 already got its
number in beat 03. Beat 04 stays: it is the contrast that stops the wrong
takeaway ("any 16-bit format is fine"). Beat 06 stays: it is the
spec-sheet trap this episode owns. The closer is the code beat, the
viewer's next move.

## Facts to keep straight (notes, not VO)

- B200 numbers come from NVIDIA's HGX page (checked 10/27): HGX B200
  (8 GPUs) lists FP8/FP6 72 PFLOPS, FP16/BF16 36 PFLOPS, TF32 18 PFLOPS,
  all "Specification in Sparse. Dense is ½ sparse spec shown." Per GPU,
  dense: fp8 4.5 PF, bf16 2.25 PF, TF32 1.125 PF. FP64 is 37 TF (296 ÷ 8),
  not used. Third-party sheets round TF32 to 1.1 PF; use 1,125.
- "Twice the peak math" vs fp32 is against **TF32**, which is how fp32
  matmuls run on tensor cores. Plain fp32 (no tensor cores, PyTorch's
  default for matmul since 1.12 unless `torch.backends.cuda.matmul.allow_tf32`
  or `set_float32_matmul_precision("high")`) is slower still, so "twice"
  is the floor, not an overstatement. The ladder shows TF32, not "fp32".
- fp16 max finite value 65,504; values above overflow to `inf`. Small
  gradients also underflow to zero in fp16; that's why fp16 training
  needs loss scaling (`torch.amp.GradScaler`). bf16 usually doesn't. VO
  names overflow only.
- "Training stays stable" is narrowed to the range problem: bf16 has
  fewer mantissa bits than fp16 (7 vs 10), so mixed-precision training
  keeps fp32 master weights and autocast keeps some ops (reductions,
  softmax, loss) in fp32. Memory cost of that is cut ep 12's.
- autocast does not do fp8. fp8 training uses Transformer Engine
  (`te.fp8_autocast`) or torchao's float8; formats E4M3 (forward) and E5M2
  (gradients) with per-tensor scaling (Hopper), block scaling (MXFP8) on
  Blackwell. Beat 05 draws E4M3 only.
- 2:4 structured sparsity: NVIDIA's sparse tensor cores skip two of every
  four values in a fixed pattern (Ampere onward). Dense training doesn't
  produce that pattern, so the sparse figure doesn't apply to it.
- "More numbers per memory read": bytes per number halve, so a fixed
  bandwidth (8 TB/s, ep 5's) moves twice the numbers. One clause only;
  memory-bound vs compute-bound is ep 5's.
- To verify before publish: NVIDIA's B200 datasheet PDF (the HGX page was
  the source; the per-GPU datasheet was not opened).

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top-middle: the bit-box rows (up to 4 rows: fp32, fp16, bf16,
  fp8), one box per bit, fp32 full stage width so the rest scale to it;
  the spec card takes this slot in beat 06.
- Stage top-right: the TFLOPS ladder (beat 03 only), 3 rungs.
- Stage middle: the series chip (12 × 12 grid) with the HBM slab and pipe
  to its right.
- Stage bottom-middle: the number line (beat 04), the 2:4 weight row
  (beat 06), the code card (beat 07); one at a time.
- One magenta hero at a time: bf16 row → the field being named → the
  `bf16 2,250` / `fp8 4,500` rung → bf16's exponent field → the sparse
  `4,500*` → `dtype=torch.bfloat16`.
