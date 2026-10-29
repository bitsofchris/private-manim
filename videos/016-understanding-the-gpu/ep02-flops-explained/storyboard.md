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
- GPU: one **B200**, bf16 dense peak **2,250 TFLOPS** (said "2,250
  teraFLOPS in bf16"); the sparse figure is never shown here. tera = a
  trillion (10^12).
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
- The matmul: `y = x @ W`, one output expanded as `x1*w1 + x2*w2 + x3*w3`.
- The bill: `FLOPs ÷ FLOPS` / `= GPU-hours = $`. No numbers.
- The chip: the series 12 × 12 grid, dark at rest, teal when working; no
  label claims a core count. Chip title `GPU`, then `B200` from beat 07 on.

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

| beat | VO | visual |
|---|---|---|
| 01_hook | A FLOP is one multiply or one add, and it's the unit that all AI compute is measured in. | Frame 0 already working: the chip with ~32 % of cells shimmering teal, memory at rest, the top card `a × b + c` with the counter `0 FLOPs` (counter the magenta hero). "multiply" → the `×` lights teal and the counter ticks 1; "add" → the `+` lights, the counter ticks 2 (and the `×` returns). Both signs back to ink by "unit"; still from ~5.2. |
| 02_name | FLOP stands for floating-point operation. | The card crossfades to `floating-point` / `operation`, the **fl** and **op** letters magenta (hero "acronym") on "floating". |
| 03_float | Computers store decimals as floating point: scientific notation in binary, a sign, digits, and an exponent. | "floating point" (10.06): the float panel grows out of cell (row 5, col 5) over the chip and memory (0.6 s). "scientific notation": the decimal row `0.0000001 → +1.0 × 10⁻⁷` and the anatomy boxes fade in. Hero passes sign → digits → exponent on each word, each label appearing on its word. The acronym letters return to ink on "floating point". |
| 04_range | The point floats, so one format holds a ten-millionth and three million. | "floats" (15.31): hero → the point; row 1's point glides right to sit after the 1 (`00000001.`, the passed zeros dim). "ten-millionth" (17.96): hero → exponent (`−7`). "three million" (19.32): row 2 `3000000. → +3.0 × 10⁶` fades in and its point glides left to after the 3 (trailing zeros dim); the anatomy boxes switch to `+ 3.0 6` with the exponent the hero. |
| 05_memory | Every weight, activation, and gradient is one of these numbers. | The float panel shrinks back into its cell (0.5 s, the reverse of 03's grow); memory (VRAM) is the hero: it is where these numbers live. The card shows one word per word said: `weights` → `activations` → `gradients`. |
| 06_count | FLOPs with a small s is a count. Training an 8-billion-parameter model on 15,000 tokens costs about 720 trillion FLOPs. | "FLOPs" (23.52): the card crossfades to `FLOPs`; hero memory → the small `s` on "small s". "Training" (25.94): the code card grows in (0.2 s) and line 1 types (`SC_typedAt`), the hero passing to the code line (`lit: "count"`) as it types; it lands by "720". "720 trillion" (30.10): `720 trillion` fades in teal under `FLOPs`. |
| 07_rate | FLOPS with a capital S is per second. This is a rate. A B200 peaks near 2,250 teraFLOPS in bf16. Tera is a trillion. | "FLOPS" (32.62): the card crossfades to `FLOPS` / `per second`, the capital `S` the hero; the code line goes ink. "B200" (35.94): the chip title `GPU` → `B200`. "2,250" (37.26): the card crossfades to `2,250 TFLOPS` / `bf16`, the whole number the hero. "Tera" (40.84): the second line becomes `tera = a trillion` and the hero narrows to the `T`. |
| 08_matmul | A transformer's compute is nearly all matrix multiplies, and a matmul is only multiplies and adds. GPUs are built to do exactly that, thousands at once. | The code card fades out (0.4 s) at the start. "matrix multiplies" (44.10): the card crossfades to `y = x @ W`. "only multiplies and adds" (46.02): `x1*w1 + x2*w2 + x3*w3` fades in under it, the hero. "thousands at once" (50.48): every cell lights teal at once (lit 0.32 → 1 over ~0.3 s) and the hero passes to the chip (box and `B200` title). |
| 09_bill | Divide a run's FLOPs by the FLOPS you get, and you have GPU-hours. This is the bill. | "Divide" (52.00): the card crossfades to `FLOPs ÷ FLOPS`; hero chip → none. "GPU-hours" (55.60): `= GPU-hours` fades in, the hero. "bill" (57.36): ` = $` fades in and takes the hero. Still from ~57.8 to the end; every cell stays lit. |

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

Every state: `cpu 0, queueO 0, strip 0, shimmer 1`, memory at rest, the top
card at `o 1`, `B null, mix 0`.

| cut | at | hero | top card | float panel | chip | code card |
|---|---|---|---|---|---|---|
| 0 (frame 0) | 0.000 | count | op, n 0 | off | lit 0.32, `GPU` | off |
| 1 (01→02) | 5.640 | count | op, n 2, no sign lit | off | lit 0.32, `GPU` | off |
| 2 (02→03) | 8.320 | acronym | name | off | lit 0.32, `GPU` | off |
| 3 (03→04) | 14.525 | exp | name | grown, row 1, anatomy 1 (`+ 1.0 −7`), all three labels | (covered) | off |
| 4 (04→05) | 20.160 | exp | name | grown, rows 1–2 glided, anatomy 2 (`+ 3.0 6`), labels | (covered) | off |
| 5 (05→06) | 23.190 | hbm | word `gradients` | off | lit 0.32, `GPU` | off |
| 6 (06→07) | 32.320 | null | count, `720 trillion` on | off | lit 0.32, `GPU` | line 1 typed, lit `count`, cy 1245 |
| 7 (07→08) | 41.955 | tera | rate step 2 | off | lit 0.32, `B200` | line 1 typed, unlit |
| 8 (08→09) | 51.685 | chip | matmul step 1 | off | lit 1, `B200` | off |
| 9 (end) | 58.365 | bill | frac, `$` on | off | lit 1, `B200` | off |

## Facts to keep straight (notes, not VO)

- **One FMA counts as two FLOPs.** NVIDIA's peak figures count a fused
  multiply-add as two operations (Nsight: peak = cores × clock × 2), hence
  `a × b + c` ticking twice. Some papers count a MAC as one op.
- **A matmul of (m × k) by (k × n) costs 2·m·k·n FLOPs** (Narayanan et al.
  2021). "Nearly all" of a transformer's compute is matmuls (well over 90 %
  for Llama-style models at typical lengths); the VO says "nearly all".
- **B200 bf16 dense 2,250 TFLOPS** (series ledger).
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
