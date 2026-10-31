ENGINE: hyperframes

# Why GPUs for AI: storyboard (v5: network over the formula in beats 1–2)

THE QUESTION: "Why does AI run on GPUs and not CPUs?"
WHO IS ASKING: a research engineer or ML learner who types `.to("cuda")`
every day and never learned what the GPU does differently, or why the same
`x @ W` is so much faster there.
THE ANSWER IN ONE SENTENCE: a neural network is almost all multiply-adds
whose outputs don't depend on each other; a GPU is thousands of small cores
built to do them all at once, while a CPU is a few big cores built to run
one stream of branching instructions fast.
THE SEARCH PHRASE: why gpu for ai (checked 10/27 against YouTube's
autocomplete endpoint and results page; "gpu vs cpu explained" also
autocompletes, general hardware results, the second phrase for the title).
The take's line 1 says "neural network" and "GPUs", not "AI": the phrase
lives in the title and description line 1 (step 9).

**One idea:** the work is a pile of independent multiply-adds; the GPU is
the chip with enough hands to do the pile at once.

**Source:** the VO is the take (`script.md`, "As recorded"), not the
planned script in `../SCRIPTS.md`. v1 of this storyboard (the plan written
before recording) is in git history.

**Engine:** HyperFrames on the series kit (`../_kit/`, `../00_layout/`).
Ep 1's own parts are in `_kit/ep.js` (the 4-core CPU, `y = x @ W`, the
grid wave) and its seam states in `_kit/seam.js`; frame 0 and every seam
state are rendered in `00_layout/layout.png`.

## Ledger (every beat copies these, nothing invented per beat)

- **GPU:** one NVIDIA **B200**, drawn as the series chip: the 12 × 12 grid
  of core cells (dark at rest, teal when working), "GPU" under it, the
  memory slab beside it (`GPU memory (VRAM) 180 GB`, at rest, never named
  in ep 1). Core count only as "thousands" (VO); never on screen ("the
  grid is a picture, not a count").
- **The network:** a tiny neural network, 4-4-4-2 nodes left to right, in
  the top slot in beats 1–2 only (`_kit/ep.js`). Its first layer is `W`:
  the 16 edges from column 0 to column 1, the edges into node j are W's
  column j, node j's output is y's column j. No labels.
- **Beats 1–2 layout (`focus: 1`, Chris, second watch):** the network on
  top, `y = x @ W` stacked right under it at 1.3× (centre y 540), the
  series chip (grid, memory, title) at 0.8× below them (centre y 925).
  Beat 3 brings it back to the series layout (`focus: 0`): the matrices
  travel down to the bottom slot as the CPU grows.
- **The CPU:** one box of **4 big cores** (`_kit/ep.js`), a picture of "a
  few", no number on screen. Not on screen in beats 1–2 (Chris, first
  watch); fades in on "CPU" in beat 3, big in the chip's place, then
  small in the top slot from beat 4, each core with a cache block and a branch fork (icons,
  no labels; the captions name them). The series' "CPU / Python" box and
  kernel queue (ep 6's) are hidden all episode; so is the time strip (ep 7's).
- **The layer:** `y = x @ W`, three 4 × 4 matrices in the bottom slot, in
  the code's order (y, x, W). x and W grey; a y cell teal when done. No
  FLOP counts (ep 2), no timings (no CPU-vs-GPU number was sourced).
- **Tensor cores:** the kit's corner sub-block in each cell (`tc: 1`),
  title "tensor cores". One sentence; ep 5 owns the fact.
- **Code card:** `GPU_DATA.code.matmul`, fully shown, docked at `cy: 1246`
  (bottom edge 1330):
  `x, W = x.to("cuda"), W.to("cuda")` / `y = x @ W`.
- **Not used** (not recorded): the BERT "> 99 % of the arithmetic" bar and
  the timing closer (`torch.cuda.synchronize()`).

## Beats (from what was said)

| beat | VO | visual |
|---|---|---|
| 01_hook | A neural network is mostly multiplication and addition. GPUs allow these to all happen at the same time. | Frame 0 already working, in the beats 1–2 layout: the tiny network on top, its layers firing in turn (hero `net`); `y = x @ W` right under it, y empty; the chip smaller below, ~32 % of cells shimmering teal. On "GPUs" the hero passes to the chip and the network goes still. On "the same time" the whole grid lights at once and every y cell fills together. |
| 02_layer | So if you take one layer, y equals x times W, each output is its own row times column. None of them waits on the other. | On "one layer" the network's first layer goes magenta (hero `layer`) and y empties: the equation is that layer. On "its own row times column" one row of x, one column of W and their y cell go magenta (hero `ycell`) and that cell fills; the output node for that column and its 4 incoming edges light with W's column. On "none of them waits" every other y cell fills at the same moment, and the whole y matrix (with the layer's 4 output nodes) is the hero. |
| 03_cpu | Now a CPU is built to run one thread as fast as possible. A few big cores, some big caches, some smart branching. It works through that pile a few at a time. | On "CPU" the network, the chip and memory fade, the matrices travel down to the bottom slot, and the CPU fades in and grows into the chip's place (hero `cpu`); y empties as it grows. "one thread": one core lit. "A few big cores": the 4 cores. "big caches": the cache blocks. "smart branching": the forks. "a few at a time": all 4 cores lit, y fills one row of four per tick, three rows by the end, the last row waiting. |
| 04_gpu | A GPU trades per-core speed for count. This grid is the chip. Thousands of small cores all working at once. | On "A GPU" the CPU shrinks back to the top slot, the chip and memory return dark, y empties; hero `chip`. "This grid is the chip": the grid border pulses. On "all working at once" every cell lights in one pulse and every y cell fills together. |
| 05_tensor | Newer GPUs add tensor cores, which do a small matrix multiply in one step. | On "tensor cores" the corner sub-blocks grow (`tc: 1`), title "tensor cores", hero `tc`. On "in one step" the sub-blocks pulse once. |
| 06_code | In PyTorch, that's one line. Move x and W to CUDA, and the same at sign runs the whole grid. | On "In PyTorch" the matrices give way to the code card (the bottom slot), tensor cores and title back to rest ("GPU"). "that's one line": `y = x @ W` lit. "Move x and W to CUDA": the `.to("cuda")` line lit. "the same at sign": `y = x @ W` lit again; "runs the whole grid": a bright wave sweeps the lit grid once. Ends still. |

What changed from v1 (the plan): the BERT bar (03_share) and the timing
closer (08_close) were not recorded, so their visuals are gone; the take
ends on the code card, which is the viewer's next move on screen. The
take's "GPUs allow this to run in parallel" repeated line 1 and is cut.
The *(if time)* tensor-core line was recorded and stays (5.2 s).

## Final beats (the contract; `vo_final.wav` 44.036 s, master seconds)

Beat brief: `agents/beat-brief-hyperframes.md` plus this table; seam
states `SC.SEAM` in `_kit/seam.js`; links per beat: `vendor`
(`../../../_shared/web/vendor`), `kit` (`../../_kit`), `ep` (`../_kit`).
Scripts: `kit/data.js`, `kit/chip.js`, `kit/code.js`, `ep/ep.js`,
`ep/seam.js`; mount with `EP.mount(root)`. Captions: `assemble.py
--captions-anchor bottom` (the bottom slot holds the matrices, then the
code card, down to y 1330).

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.000 | 6.185 | A neural network is mostly multiplication and addition. GPUs allow these to all happen at the same time. |
| 2 | `02_layer` | 6.185 | 8.065 | So if you take one layer, y equals x times W, each output is its own row times column. None of them waits on the other. |
| 3 | `03_cpu` | 14.250 | 8.970 | Now a CPU is built to run one thread as fast as possible. A few big cores, some big caches, some smart branching. It works through that pile a few at a time. |
| 4 | `04_gpu` | 23.220 | 8.580 | A GPU trades per-core speed for count. This grid is the chip. Thousands of small cores all working at once. |
| 5 | `05_tensor` | 31.800 | 5.225 | Newer GPUs add tensor cores, which do a small matrix multiply in one step. |
| 6 | `06_code` | 37.025 | 7.011 | In PyTorch, that's one line. Move x and W to CUDA, and the same at sign runs the whole grid. |

## Seam states (`_kit/seam.js`; fields as `SC.REST` + ep 1's defaults unless named)

Ep 1's defaults (all cuts): series CPU, queue and time strip hidden; the
4-core CPU shown, cores `1111`; network hidden; matrices shown; chip and
memory shown. Cuts 0–2: **network 1, CPU 0, focus 1**.

| Cut | After beat | State |
|---|---|---|
| 0 | frame 0 | network 1 **flow 1**, CPU 0, lit 0.32, **shimmer 1**, hero net, y empty |
| 1 | hook | network 1 (still), CPU 0, **lit 1**, hero chip, y all done |
| 2 | layer | network 1, CPU 0, lit 1, **hero y** (every y cell and the layer's 4 output nodes magenta), y all done |
| 3 | cpu | **network 0, CPU 1, big 1, chip 0, memory 0**, cache 1, branch 1, hero cpu, y rows 1–3 done (`1111 1111 1111 0000`), lit 0 (hidden) |
| 4 | gpu | big 0, chip and memory back, lit 1, hero chip, y all done |
| 5 | tensor | as 4, **tc 1, hero tc, title "tensor cores"** |
| 6 | code (end) | as 4 but tc 0, title "GPU", hero null, **matrices 0, code card** (`matmul`, all typed, lit `at`, cy 1246) |

Cache and branch stay 1 after cut 3; they are drawn only while the CPU is
big, so they are invisible from beat 4 on.

## Cut list

Raw take 49.5 s, loudnorm only (`enhance_vo.sh` default; SERIES.md:
Studio Sound unknown, so no denoise), floor −72.7 dB.
`tighten_vo.py --max-gap 0.25 --noise=-45dB --remove 14.95-18.00 --level -14`
→ **44.0 s, 13 pieces, one phrase cut.** (`--noise auto`, −52.6 dB, left
every pause uncapped: the breaths sit above it.)

| Cut | Raw | Seconds | Why |
|---|---|---:|---|
| "GPUs allow this to run in parallel." | 14.95–18.00 | 3.05 | repeats line 1 (script.md's cut candidate) |
| pauses capped at 0.25 s | | 2.4 | |

Flagged, not cut:
- **05_tensor** (5.2 s): the plan's *(if time)* line; ep 5 owns tensor
  cores. Cutting it gives 38.8 s and drops the only beat that changes the
  chip drawing. Keep unless you want it shorter.
- **"GPUs allow these to all happen at the same time"** and **"all working
  at once"** say the same thing, but one is the answer and the other the
  payoff over the grid; kept.
- No closer: the take ends on "runs the whole grid" over the code card.

Ear checks: none named for ep 1 in `script.md` or SERIES.md (the three
settled ones are other episodes). Re-transcribed `vo_final.wav` reads
clean word for word.
