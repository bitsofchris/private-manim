ENGINE: hyperframes

# Floating point and precision (ep 4): storyboard v2, from the take

v1 (written before recording) is in git history; this version is built from
`script.md`, what Chris said. Working name only: titles at runbook step 9.

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
endpoint; "fp32 vs fp16" second; "mixed precision training" for the
description). The take says bf16, fp16 and fp32 in its first 18 s.

**One idea:** a number's bit width sets how fast the chip can do math on
it; bf16 wins because it halves the bits without shrinking the range.

## Ledger (from `../SERIES.md`; every beat copies these, nothing invented)

- GPU: one **B200**. Dense tensor-core peaks: **TF32 1,125 / bf16 2,250 /
  fp8 4,500 TFLOPS** (labelled TF32, never fp32). GPU memory **180 GB**.
- Bit layouts (sign | exponent | mantissa), one box per bit, to scale:
  **fp32** 1|8|23, **fp16** 1|5|10 (max **65,504**), **bf16** 1|8|7,
  **fp8 (E4M3)** 1|4|3.
- Half the bits → 2× the numbers per memory read → 2× peak dense FLOPS.
- Code (real, runs; `GPU_DATA.code.autocast`):
  `with torch.autocast("cuda",` / `    dtype=torch.bfloat16):` /
  `  loss = model(x)` / `loss.backward()`.
- Spelling: "FLOPs" is a count, "FLOPS" a rate (the ladder is a rate).
- The chip: the series 12 × 12 grid; each cell holds 1, 2 or 4 numbers
  (`split` 0, 1, 2) for fp32, bf16, fp8.

## What the take changed (from `script.md`)

- Not recorded: "Half the bits, twice the peak math", the three-parts line
  (sign, exponent, mantissa), the sparse spec-sheet trap. Their visuals
  are dropped (v1 beats 02_parts and 06_sparse). "Exponent" and
  "precision" now arrive undefined, so the bits view writes each row's
  field counts on screen ("8 exponent · 23 mantissa").
- The fp8 line says "three bits"; fp8 is 8 bits, 3 of them mantissa. The
  fp8 row's spec reads "4 exponent · 3 mantissa" and the mantissa field is
  the hero on "three bits", so the frame states the right number.
- The 4.7 s pause before "In PyTorch" is cut.
- v3 (after the first cut, Chris: "we mention fp8 early but dont show it",
  "not clear the difference ... what a number looks like"): fp8 is a fourth
  row from frame 0, and the bits view is a table of what two real numbers
  become in each format: 1/3 (precision; the digits still right in teal)
  and 70,000 (range; fp16 → inf). The range bars and marker are gone.

## VO and visual (built from what was said)

| beat | VO | visual |
|---|---|---|
| 01_hook | bf16 makes training faster because each number is half the bits of fp32. | Frame 0 already working: chip view. fp32 / fp16 / bf16 / fp8 small in the top slot, the grid shimmering, bf16's row magenta. On "half the bits" a dashed ghost of the missing 16 boxes trails bf16's row to fp32's width, and fades by the cut. |
| 02_bits | Fewer bits means more numbers per memory read, and more multiply-adds per tensor core cycle. | "memory read": the pipe is the hero, number tiles stream from GPU memory into the grid (beat-only prop, gone by the cut); "more numbers": each cell splits in two (`split` 0 → 1). "tensor core": tensor cores grow and are the hero, title "tensor cores". |
| 03_peak | A B200 peaks near 2,250 teraflops in bf16. fp8 doubles that. | Title back to "GPU", tc back to rest. The ladder grows in the bottom slot: TF32 1,125 and bf16 2,250 on "2,250" (bf16 rung the hero); "fp8 doubles": the fp8 rung grows to 4,500 and is the hero (with fp8's row label), cells split to four. |
| 04_fp16 | fp16 is also 16 bits, but it spends them on precision. So anything past 65,504 will overflow. | "fp16": the chip fades and the four rows grow into the bits view (fp16's row the hero). "precision": the 1/3 column writes in (0.33333334 / 0.33325195 / 0.33398438 / 0.34375, right digits teal); fp16's mantissa and its 1/3 cell the hero. "65,504": the 70,000 column header and fp32's 70,000; "overflow": fp16's cell lands "inf", the hero. |
| 05_bf16 | bf16 keeps fp32's 8 exponent bits. Same range, less precision, and training stays stable. | "8 exponent bits": outlines on fp32's and bf16's exponent fields, bf16's exponent the hero (with fp32's, one group). "same range": bf16's 70,000 cell writes in, 70,144 (part of the hero group). "less precision": bf16's mantissa and its 0.33398438 the hero. "stable": back to bf16's exponent. |
| 06_fp8 | fp8 keeps just 3 bits, so training in it needs a scaling library like NVIDIA's Transformer Engine. | Outlines off; fp8's row the hero. "three bits": fp8's mantissa and its 0.34375 the hero. "scaling": fp8's 70,000 cell "max 448", then the "× scale" tag clips on, the hero; "Transformer Engine" under it on "Transformer". |
| 07_close | In PyTorch, wrap your forward pass in autocast with bf16. You get faster math without the overflow. | "PyTorch": back to chip view, lifted; fp32 / fp16 / fp8 fade, bf16 slides into the top slot; the autocast card types in under the chip. "bf16": `dtype=torch.bfloat16` lit (the hero). Still from ~0.5 s before the end. |

## Final beats (`beats.json`; `words.json` has every word's master time)

VO 44.684 s (`vo_final.wav`, take 51.9 s; cut: the 41.2–45.9 s pause,
other pauses capped at 0.25 s).

| beat | start | length | folder | VO |
|---|---|---|---|---|
| 1 | 0.000 | 6.010 | `01_hook` | bf16 makes training faster because each number is half the bits of fp32. |
| 2 | 6.010 | 5.200 | `02_bits` | Fewer bits means more numbers per memory read, and more multiply-adds per tensor core cycle. |
| 3 | 11.210 | 5.580 | `03_peak` | A B200 peaks near 2,250 teraflops in bf16. fp8 doubles that. |
| 4 | 16.790 | 8.200 | `04_fp16` | fp16 is also 16 bits, but it spends them on precision. So anything past 65,504 will overflow. |
| 5 | 24.990 | 6.520 | `05_bf16` | bf16 keeps fp32's 8 exponent bits. Same range, less precision, and training stays stable. |
| 6 | 31.510 | 6.730 | `06_fp8` | fp8 keeps just 3 bits, so training in it needs a scaling library like NVIDIA's Transformer Engine. |
| 7 | 38.240 | 6.444 | `07_close` | In PyTorch, wrap your forward pass in autocast with bf16. You get faster math without the overflow. |

## Seam states (`SC.SEAM[n]` in `_kit/seam.js`; `00_layout/layout.png` shows 0–7)

Every state: CPU, queue and time strip hidden; `lit` 0.32 with the
shimmer on (`SC.clock` = master seconds). Fields named as in `_kit/ep.js`.

| cut | on screen |
|---|---|
| 0 (frame 0) | chip view: fp32 / fp16 / bf16 / fp8 small in the top slot, chip + GPU memory, title "GPU"; hero `row:bf16` |
| 1→2 | same as 0 |
| 2→3 | `split` 1 (2 numbers a cell), `tc` 1, title "tensor cores"; hero `tc` |
| 3→4 | `split` 2, title "GPU", tc 0; ladder full (`rungs` 3); hero `rung:fp8` |
| 4→5 | bits view (`view` 1, chip hidden; `split` 1 under it); `colA` 1 (1/3 column), `big` 1 (70,000 header + fp32), `inf` 1; hero `inf` |
| 5→6 | + `bigb` 1 (70,144), `same` 1 (exponent outlines); hero `exp:bf16` |
| 6→7 | + `big8` 1 ("max 448"), `scale` 1, `same` 0; hero `scale` |
| end | chip view lifted 120 px (`close` 1), o32 / o16 / o8 0, bf16 alone in the top slot, `split` 1, autocast card full at cy 1310 (layer coords; 1190 on screen), `lit` "bf16"; hero `code` |

Captions: `assemble.py --captions-anchor bottom` for the whole Short (the
card ends at y 1330), every caption one line.

## Layout

- Chip view: four rows y 240–436 (labels x 65, boxes x 215–950); chip y
  450–1078 with GPU memory right; title y 1090; ladder y 1170–1325.
- Bits view: rows full width (x 65–940); label line above each row holds
  the name and its two value cells (1/3 at x 440, 70,000 at x 760,
  monospace 44 px, headers at y 240); field counts under the boxes; boxes
  at fp32 360, fp16 550, bf16 740, fp8 930; scale tag beside fp8's boxes,
  "Transformer Engine" at y 1056.
- End: the chip layer lifted 120 px (chip 330–958, title 970), bf16's row
  at y 250, the code card y 1050–1330.
- One magenta hero at a time, in order: bf16 row → pipe → tensor cores →
  bf16 rung → fp8 rung → fp16 row → fp16 mantissa (+ 1/3 cell) → inf →
  bf16 row → bf16 exponent (+ fp32's, + 70,144) → bf16 mantissa (+ 1/3
  cell) → bf16 exponent → fp8 row → fp8 mantissa (+ 1/3 cell) → scale tag →
  `dtype=torch.bfloat16`.

## Facts to keep straight (notes, not VO)

- Example values, computed with numpy (fp32, fp16) and round-to-nearest-
  even by hand (bf16, OCP E4M3): 1/3 → 0.33333334 / 0.33325195 /
  0.33398438 / 0.34375; 70,000 → 70,000 / inf / 70,144 / out of range
  (E4M3's max is 448; it has no inf). Script: the session scratchpad
  `fmt.py`, rerun before changing a value.
- fp8 here is E4M3 (4 exponent, 3 mantissa). The other fp8, E5M2, keeps
  2 mantissa bits; Transformer Engine's default recipe uses E4M3 forward
  and E5M2 for gradients.

- B200 numbers: NVIDIA HGX B200 page (sparse ÷ 2 ÷ 8). TF32 is how fp32
  matmuls run on tensor cores; plain fp32 is slower still.
- fp16 max finite value 65,504; above it, `inf`. fp16 also underflows
  small gradients (why it needs `GradScaler`); the VO names overflow only.
- "Training stays stable" is the range claim; mixed precision still keeps
  fp32 master weights and autocast keeps some ops in fp32.
- autocast does not do fp8; Transformer Engine (`te.fp8_autocast`) or
  torchao does, with per-tensor or block scaling.
