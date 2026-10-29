ENGINE: hyperframes

# FLOPs explained: storyboard (v3, built from the take)

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
THE SEARCH PHRASE: flops explained (checked 10/27 against YouTube's
autocomplete endpoint: it autocompletes and its top results are AI
explainers, but the other suggestions are flip-flops and movie flops, so
the title must say AI or GPU; "teraflops explained" is the second phrase).
The take says "A FLOP is…" in its first two words.

**One idea:** a FLOP is one multiply or one add, and AI is nearly nothing
else, so FLOPs are the unit of AI work. **The closer** (as recorded): divide
a run's FLOPs by the FLOPS you get and you have GPU-hours, the bill.

The VO is `script.md` ("As recorded"); the planned script (v2 of this file,
`../SCRIPTS.md`) is reference only. Where the take left it: "FLOP stands for
floating-point operation" and "This is a rate" were added; the *(if time)*
GPU-hours line is the closer; the spec-sheet closer (dense FLOPS at your
precision) was not recorded, so its spec-sheet card is dropped.

## Ledger (every beat copies these, nothing invented per beat)

From `../SERIES.md` and `../_kit/data.js`; ep 2's own strings are in
`_kit/flops.js`.

- A FLOP: one floating-point multiply or one add. `a × b + c` is 2 FLOPs.
- **FLOPs** (small s) is a count; **FLOPS** (capital S) is per second.
  Spelled so everywhere, on screen and in captions.
- No GPU model or peak is named (the B200 line was cut after the first
  cut, Chris: "irrelevant here").
- The count: the series run, an **8B-parameter** model on **15,000
  tokens**: 6 × 8e9 × 15,000 = **7.2e14**, said "about 720 trillion FLOPs".
  Code card line (data.js `code.flops[0]`): `flops = 6 * 8e9 * 15_000  # 7.2e14`.
  The `6 *` is not explained (ep 3). data.js's second line (`seconds = flops
  / 2250e12  # 0.32`) is not shown: the VO never says seconds or peak, and
  its closer divides by "the FLOPS you get", not the peak.
- Floating-point examples: **0.0000001** (a ten-millionth) = `+1.0 × 10⁻⁷`
  and **3000000** (three million) = `+3.0 × 10⁶`; the anatomy boxes
  `+ | 1.0 | −7` then `+ | 3.0 | 6`, labelled sign, digits, exponent. No
  format named, no bit counts (ep 4).
- The arithmetic in one core (illustration values, approved by Chris):
  `1.5 × 2.0 = 3.0`, `3.0 + 0.5 = 3.5`: 2 FLOPs.
- The matmul: `y = x @ W`; one output of the series' tiny layer (3 inputs)
  as three multiply-adds, x = [1.0, 2.0, 0.5], w = [0.5, 1.5, 2.0]:
  y = 0.5, 3.5, 4.5; 6 FLOPs (2 per pair; the ledger's tiny layer is 12 for
  2 outputs).
- The count rolls up as `720,000,000,000,000` and lands as `720 trillion
  = 7.2 × 10¹⁴` (the ledger's 7.2e14).
- The bill: `FLOPs ÷ FLOPS` / `= GPU-hours = $`. No numbers.
- The chip: the series 12 × 12 grid, dark at rest, teal when working; no
  label claims a core count. Chip title `GPU` throughout.

## The picture

The series chip (`../_kit/chip.js`) with the CPU, its queue and the time
strip off all episode (ep 2 never names them; the strip's "GPU-Util" is
ep 7's word). GPU memory stays at rest on the right. Ep 2's own parts
(`_kit/flops.js`):

- **The top card** (y 245–435, in the CPU and queue's place): one or two
  lines of text that change with the VO: the operation and its counter,
  the acronym, the word, the count, the rate, the matmul, the bill.
- **The float panel** (over the chip and memory, y 450–1078), grown out of
  one cell: a decimal row and its scientific form, and the anatomy boxes.
- **The code card** (`../_kit/code.js`) in the bottom slot, centred at y
  1245 so its bottom edge is 1329 (≤ 1330), beats 06–07. Captions anchored
  bottom all through (`assemble.py --captions-anchor bottom`), every caption
  one line.

Scene changes: op card (0–5.6) → acronym (5.6–8.3) → float panel (8.3–20.2)
in two states → memory (20.2–23.2) → count + code (23.2–32.3) → rate (32.3–42)
→ matmul (42–51.7) → bill (51.7–58.4). The 12 s on the float panel moves
through four states (grow, anatomy, point glide, second number).

## Beats (visual brief)

v2, after the first cut (Chris: "watching the GPU cores dance around gets
kind of boring and repetitive"): the Short alternates between **inside one
core** (the panel grown out of cell row 5, col 5: the arithmetic, the
number) and **the whole chip** (the scale). Example operands (`1.5 × 2.0 +
0.5`, the dot product's x and w) are illustration values Chris approved,
not ledger numbers.

| beat | VO | visual |
|---|---|---|
| 01_hook | A FLOP is one multiply or one add, and it's the unit that all AI compute is measured in. | Frame 0 is inside one core: `1.5 × 2.0`, `0 FLOPs` (the counter the hero), `FLOP` big on the card. "multiply" (1.32): the × goes teal, `= 3.0` slides out of it, counter 1. The 3.0 is carried down to row 2. "add" (2.24): `3.0 + 0.5 = 3.5`, the + teal, counter 2. "all AI compute" (3.84): the panel shrinks back into its cell and the hero passes to the chip: every core is doing this. |
| 02_name | FLOP stands for floating-point operation. | "FLOP" (5.92): F L O P go magenta (hero "acronym"). "floating" (6.62): the letters glide apart and FLOATING-POINT / OPERATION types in around them. |
| 03_float | Computers store decimals as floating point: scientific notation in binary, a sign, digits, and an exponent. | Unchanged: the float panel grows on "floating point", sign → digits → exponent. |
| 04_range | The point floats, so one format holds a ten-millionth and three million. | Unchanged: the point glides; row 2 on "three million". |
| 05_memory | Every weight, activation, and gradient is one of these numbers. | The panel shrinks back; memory is the hero, and numbers stream out of it along the pipe into the chip (`stream`) while the card shows `weights` → `activations` → `gradients`. The stream fades out before the cut. |
| 06_count | FLOPs with a small s is a count. Training an 8-billion-parameter model on 15,000 tokens costs about 720 trillion FLOPs. | `FLOPs`, small s the hero. "Training": the code line types (lit "count") and under `FLOPs` the count rolls up (mono digits) as it types, landing on "720": `720 trillion = 7.2 × 10¹⁴`. |
| 07_rate | FLOPS with a capital S is per second. This is a rate. | `FLOPS` / `per second`, capital S the hero; the code line unlit. "per second" (34.06): the 1 s clock appears at the card's right and sweeps once, the hero. |
| 08_matmul | A transformer's compute is nearly all matrix multiplies, and a matmul is only multiplies and adds. GPUs are built to do exactly that, thousands at once. | The code card and clock fade. "matrix" (37.62): `y = x @ W`. "matmul" (39.02): back inside one core for one output: x and w tiles; from "only" (39.54) each pair runs `y += x·w` (× teal, then +), y going 0.5, 3.5, 4.5 and the counter to 6 FLOPs; the running line the hero. "thousands" (44.00): the panel shrinks back, every cell lights, the chip the hero. |
| 09_bill | Divide a run's FLOPs by the FLOPS you get, and you have GPU-hours. This is the bill. | "Divide" (45.51): `FLOPs ÷ FLOPS`, hero none. "GPU-hours" (49.12): `= GPU-hours`, the hero. "bill" (50.88): ` = $`, the hero. Still to the end; every cell lit. |

## Final beats (the contract; `beats.json`)

VO 51.885 s (`vo_final.wav`). Chris, after the first cut: "A B200 peaks near 2,250 teraFLOPS in bf16. Tera is a trillion." cut (`tools/cut_vo.py --cut 35.50-41.98`, both edges in digital silence; 58.365 → 51.885 s). From 61.9 s raw: no line cut; pauses (which
in this take are breaths at about −50 dB, so the threshold is −45 dB, not
`auto`'s −53.8) capped at 0.3 s.

| beat | start | length | folder | VO |
|---|---|---|---|---|
| 1 | 0.000 | 5.640 | `01_hook` | A FLOP is one multiply or one add, and it's the unit that all AI compute is measured in. |
| 2 | 5.640 | 2.680 | `02_name` | FLOP stands for floating point operation. |
| 3 | 8.320 | 6.205 | `03_float` | Computers store decimals as a floating point, scientific notation in binary, a sign, digits, and an exponent. |
| 4 | 14.525 | 5.635 | `04_range` | The point floats, so one format holds a ten-millionth and three million. |
| 5 | 20.160 | 3.030 | `05_memory` | Every weight, activation, and gradient is one of these numbers. |
| 6 | 23.190 | 9.130 | `06_count` | FLOPs with a small s is a count. Training an 8 billion parameter model on 15,000 tokens costs about 720 trillion FLOPs. |
| 7 | 32.320 | 3.180 | `07_rate` | FLOPS with a capital S is per second. This is a rate. |
| 8 | 35.500 | 9.705 | `08_matmul` | A transformer's compute is nearly all matrix multiplies and a matmul is only multiplies and adds. GPUs are built to do exactly that, thousands at once. |
| 9 | 45.205 | 6.680 | `09_bill` | Divide a run's FLOPs by the FLOPS you get, and you have GPU-hours. This is the bill. |

## Seam states (code: `_kit/seam.js`, `SC.SEAM[0..9]`)

Every state: `cpu 0, queueO 0, strip 0, shimmer 1`, memory at rest, title
`GPU`, the card bg at `o 1`, `B null, mix 0`.

| cut | at | hero | card | acro | panel | chip | code card |
|---|---|---|---|---|---|---|---|
| 0 (frame 0) | 0.000 | count | — | `FLOP` (u 0) | core op: `1.5 × 2.0`, n 0 | (covered) | off |
| 1 (01→02) | 5.640 | chip | — | `FLOP` | off | lit 0.32 | off |
| 2 (02→03) | 8.320 | acronym | — | FLOATING-POINT / OPERATION (u 1) | off | lit 0.32 | off |
| 3 (03→04) | 14.525 | exp | — | u 1 | float: row 1, anatomy 1, labels | (covered) | off |
| 4 (04→05) | 20.160 | exp | — | u 1 | float: rows 1–2 glided, anatomy 2 | (covered) | off |
| 5 (05→06) | 23.190 | hbm | word `gradients` | off | off (stream off) | lit 0.32 | off |
| 6 (06→07) | 32.320 | null | count, `720 trillion = 7.2 × 10¹⁴` | off | off | lit 0.32 | line 1, lit `count`, cy 1245 |
| 7 (07→08) | 35.500 | clock | rate, clock swept (1), on | off | off | lit 0.32 | line 1, unlit |
| 8 (08→09) | 45.205 | chip | matmul `y = x @ W` | off | off | lit 1 | off |
| 9 (end) | 51.885 | bill | frac, `$` on | off | off | lit 1 | off |

## Facts to keep straight (notes, not VO)

- **One FMA counts as two FLOPs.** NVIDIA's peak figures count a fused
  multiply-add as two operations (Nsight: peak = cores × clock × 2), hence
  `a × b + c` ticking twice. Some papers count a MAC as one op.
- **A matmul of (m × k) by (k × n) costs 2·m·k·n FLOPs** (Narayanan et al.
  2021). "Nearly all" of a transformer's compute is matmuls (well over 90 %
  for Llama-style models at typical lengths); the VO says "nearly all".
- **The floating-point examples:** "holds" means "is in range of": true for
  fp32 and bf16, false for fp16 (3 × 10⁶ is past its max of 65,504). 10⁻⁷ is
  approximate in any binary format. The panel shows decimal scientific
  notation and names no format; ep 4 owns bit widths.
- **Where the numbers live:** weights, activations and gradients sit in GPU
  memory (HBM/VRAM) during training, hence memory as beat 05's hero.
- **"Divide a run's FLOPs by the FLOPS you get"** gives seconds; GPU-hours
  is that over 3,600 per GPU. The VO's "GPU-hours" is the unit you pay for;
  the card shows no numbers. "The FLOPS you get" is below peak (ep 7's MFU).
- **720 trillion FLOPs for 15,000 tokens** uses 6 × params per token (ep
  3), which ignores attention FLOPs and activation recompute.
