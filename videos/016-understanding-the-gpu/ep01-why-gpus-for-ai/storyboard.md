ENGINE: hyperframes

# Why GPUs for AI: storyboard (v1, VO draft for Chris)

THE QUESTION: "Why does AI run on GPUs and not CPUs?"
WHO IS ASKING: a research engineer or ML learner who types `.to("cuda")`
every day and never learned what the GPU does differently, or why the same
`x @ W` is so much faster there.
THE ANSWER IN ONE SENTENCE: a neural network is almost all multiply-adds
whose outputs don't depend on each other; a GPU is thousands of small cores
built to do them all at once, while a CPU is a few big cores built to run
one stream of branching instructions fast.
THE SEARCH PHRASE: why gpu for ai (checked 10/27 via YouTube's autocomplete
endpoint and the results page, not a browser: "why gpu for ai" autocompletes
verbatim, with "why gpu is used for ai", "why is gpu important for ai" and
"why nvidia chips for ai" beside it; its results are on topic: "How a GPU
Actually Works (and Powers AI)", "Why AI Runs on GPUs, Not CPUs".
"gpu vs cpu explained" also autocompletes and its results are general
hardware explainers ("CPU vs GPU | Simply Explained", "CPUs vs GPUs As Fast
As Possible"), so it goes in the title as the second phrase. "gpu vs cpu for
ai" autocompletes only itself, on-topic results.)

**One idea:** the work is a pile of independent multiply-adds; the GPU is
the chip with enough hands to do the pile at once.

**Source note:** there are no written sentences from Chris on this; the
source is his questions in the 10/27 chat. This VO is a draft in his voice
(plain, short sentences, no hype) for him to rewrite.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip (a
12 × 12 core grid), a CPU drawn as a few big cores, a matmul, a bar, and a
code card. Nothing needs Manim.

Series context: ep 1 of `../SERIES.md` (Understanding the GPU). It
introduces the chip picture every later episode reuses: the 12 × 12 grid
of core cells, dark at rest, teal when working. FLOPs (ep 2) and tensor
cores (ep 5) get one clause at most here.

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one **B200** (the series chip). Its core count is said only as
  "thousands" (it has 148 SMs × 128 FP32 cores = 18,944; never on screen,
  per the ledger's "the grid is a picture, not a count").
- The grid: 12 × 12 cells, a picture of "many small cores", no label claims
  a number.
- The CPU: drawn as **4 big cores**, a picture of "a few", no label claims
  a number (a laptop CPU has around 8–16 cores; the largest 2026 server
  CPUs reach 192–256).
- The layer on screen: `y = x @ W`. No FLOP counts (ep 2), no timings.
- Evidence number: in BERT training, matrix multiplies are **over 99 %** of
  the arithmetic (Ivanov et al., "Data Movement Is All You Need", MLSys
  2021).

## VO (draft: 145 words without the if-time beat, 159 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | AI runs on GPUs because a neural network is mostly multiply-adds, and they can all happen at the same time. | Frame 0 already working: the series chip mid-stage, the 12 × 12 grid every cell lit teal at once; to its left, smaller, the CPU box with 4 big cores, one lit. Multiply-add tiles (`×` `+`) pour into both from the top: the grid swallows its stream in one pulse, the CPU queue piles up. Labels `GPU` and `CPU` under each. Magenta hero: the lit grid. ~6 rows of stage. |
| 02_layer | Take one layer: y equals x times W. Each output is its own row times column. None of them waits on another. | The pour pauses; above the chip, `y = x @ W` as three small matrices (x 4 × 4, W 4 × 4, y 4 × 4). On "its own row times column" one row of x and one column of W light and fill one cell of y (magenta hero passes to that cell). On "none of them waits" every y cell fills at the same moment. |
| 03_share | In BERT, matrix multiplies like this are over 99 percent of the arithmetic. | A single horizontal bar under the matrices, label "BERT training, arithmetic": a magenta segment `matmul > 99 %` and a sliver `everything else`. Small source tag: "Ivanov et al. 2021". |
| 04_cpu | A CPU is built to run one thread as fast as possible: a few big cores, big caches, smart branching. It works through that pile a few at a time. | The CPU box grows to stage-middle (the GPU dims to grey): 4 big cores, each with a fat cache block and a branch icon (a fork). The y cells from beat 2 fill in groups of four, one group per tick, the rest waiting grey. Magenta hero: the CPU queue of unfilled cells. |
| 05_gpu | A GPU trades per-core speed for count. This grid is the chip: thousands of small cores, all working at once. | The CPU slides back small to the left; the chip returns to stage-middle. Each grid cell takes one y cell; on "all working at once" the whole grid lights teal in one pulse and every y cell fills together. Magenta hero: the grid. This is the drawing the next 12 episodes reuse. |
| 06_tensor *(if time)* | Newer GPUs add tensor cores, which do a small matrix multiply in one step. | Inside each grid cell a smaller highlighted sub-block appears (the series' tensor-core drawing, ep 5 on) and briefly glows. No label beyond `tensor cores`. |
| 07_code | In PyTorch, that's one line. Move x and W to cuda, and the same at sign runs across the whole grid. | Code card, bottom-middle (real lines that run): `x, W = x.to("cuda"), W.to("cuda")` / `y = x @ W`. On "one line" the `.to("cuda")` line lights; on "the same at sign" the `@` lights magenta and the grid pulses once. |
| 08_close | Try it: time one big matmul on the CPU, then on cuda. Call synchronize before you stop the clock. | The code card grows to the timing snippet: `t = time.perf_counter()` / `y = x @ W` / `torch.cuda.synchronize()` / `print(time.perf_counter() - t)`. `torch.cuda.synchronize()` is the magenta hero. No numbers on screen. Takeaway only, no outro. |

Line 1 is the answer and says "AI runs on GPUs" (the search phrase's words)
in its first clause; the grid and the CPU are both on screen at frame 0.
Beat 06 is the *(if time)* cut: tensor cores are ep 5's fact, and the
answer stands without them. Beat 03 stays: it is the proof that "mostly
multiply-adds" is not a figure of speech. Beat 04 stays: it is the contrast
that stops the wrong takeaway ("CPUs are just slow"); they are built for a
different kind of work. The closer is the viewer's next move, and the
synchronize clause is one clause of ep 6's fact (the GPU runs async) so the
viewer's first timing isn't a fake near-zero.

## Facts to keep straight (notes, not VO)

- CPU vs GPU design, NVIDIA's own words (CUDA Programming Guide,
  Introduction): "a CPU is designed to excel at executing a serial sequence
  of operations (called a thread) as fast as possible"; "a GPU is designed
  to excel at executing thousands of threads in parallel", "trading off
  lower single-thread performance to achieve much greater total
  throughput"; GPUs "devote more transistors to data processing units"
  while CPUs "dedicate more transistors to data caching and flow control".
  Beats 04–05 are this sentence, drawn.
- "Thousands of small cores": B200 is 148 SMs (74 enabled of 80 per die,
  two dies) × 128 FP32 CUDA cores = 18,944 (Chips and Cheese; Cornell
  Virtual Workshop B200 SM page). Some sites list 18,432 (the 144-SM
  figure); "thousands" is true either way. Never on screen.
- "A few big cores" is the picture, not a spec: a laptop has ~8–16 cores;
  server CPUs in 2026 reach 192 (EPYC Turin) and 256 (EPYC Venice, Zen 6),
  and Intel's E-core Xeon 6 reaches 288. Still two orders of magnitude
  below a GPU's lanes, which is why the VO says "a few" only about the
  drawing and never gives a CPU number.
- CPUs also do parallel math per core (SIMD: AVX-512, AMX). "A few at a
  time" is relative to the GPU, and the drawing shows groups of four, not
  one. Companion material, not VO.
- "None of them waits on another": true of the outputs of `x @ W`; inside
  one output the adds accumulate in order (a reduction). The VO says
  "each output", which is the true version.
- "Over 99 %" is of BERT's arithmetic (FLOPs), not its runtime: the same
  paper finds matmuls are 61 % of runtime, the rest memory-bound ops.
  That gap is ep 5's story (memory) and cut ep 11's (fusion); not here.
- Timing on the GPU without `torch.cuda.synchronize()` measures only the
  launch, because CUDA calls return before the kernel finishes (ep 6's
  home). The first CUDA call also pays for context setup; a warm-up run
  before timing belongs in the companion.
- No CPU vs GPU timing number is shown anywhere: none was sourced for a
  B200 against a named CPU on a named matrix size.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top: the `y = x @ W` matrices (beats 2–5), ~1.5 rows; the BERT bar
  directly under them (beat 3 only).
- Stage middle: the chip (12 × 12 grid, rounded box), with the CPU box
  (4 big cores) to its left at about a third of its size. Beat 4 swaps
  their sizes; beat 5 swaps them back. The chip is drawn exactly as
  `../SERIES.md` "The series image" says; later episodes copy it.
- Stage bottom-middle: the code card (beats 7–8).
- One magenta hero at a time: the lit grid → one y cell → the matmul
  segment of the bar → the CPU's waiting queue → the grid → the `@` →
  `torch.cuda.synchronize()`.
