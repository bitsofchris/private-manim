ENGINE: hyperframes

# Raising MFU: storyboard (v1, B200 numbers; VO draft for Chris)

THE QUESTION: "My GPU is busy but MFU is low. What do I change?"
WHO IS ASKING: a research engineer whose run shows GPU-Util near 100 % and
an MFU they've now computed (ep 8) that sits well under half, who has heard
of `torch.compile` and bf16 but doesn't know which knob to turn first or
why any of them would raise the number.
THE ANSWER IN ONE SENTENCE: try four changes in order, re-measuring MFU
after each: bf16 autocast (matmuls on the tensor cores), a bigger batch
(each kernel fills the chip), `torch.compile` (small memory-bound kernels
fused into one), and CUDA graphs (less launch overhead when the step is many
tiny kernels).
THE SEARCH PHRASE: torch compile (checked 10/27 via YouTube's autocomplete
endpoint and results page, not a browser: "torch compile" autocompletes,
and its results are all on topic ("torch.compile: The Missing Manual",
"Introduction to torch.compile"); the ComfyUI audience shows up only as a
second suggestion, "torch compile comfyui", not in the results. "how does
torch compile work" also autocompletes with on-topic results, but this Short
explains four levers, not compile's internals. "speed up pytorch training"
and "make pytorch faster" get no autocomplete; "pytorch training faster"
completes only to "pytorch training loop". "mixed precision training"
autocompletes, on topic, but precision is ep 4's home. "increase gpu
utilization" autocompletes but is the wrong problem: this viewer's GPU is
already busy.)

**Titles (runbook step 9, Chris picks):** search `torch compile and 3 more ways to raise MFU` · hook `Your training is wasting the GPU (torch compile)`

**One idea:** busy is not useful; four changes, in order, make the busy
time do more math, and MFU tells you which one worked.

**Source note:** the source is Chris's questions in the 10/27 chat ("how do
I actually raise it?"-shaped, following ep 8), with no answer sentences of
his, so this VO is a draft in Chris's voice for him to rewrite (same as
ep 8 and 015). The order of the levers and the one-clause links to eps 4,
5, 6 and 8 come from `../SERIES.md`.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip
(12 × 12 core grid, HBM slab, CPU queue, MFU meter) and a code card.
Nothing needs Manim.

Series context: ep 11 of `../SERIES.md` (Understanding the GPU). Builds on
ep 4 (precision), ep 5 (tensor cores vs memory), ep 6 (kernels and the CPU
queue) and ep 8 (MFU); each gets one clause here, no more. Batch size's
memory cost is ep 12's; here it is "as far as memory allows".

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one **B200**, bf16 dense peak **2,250 TFLOPS**, HBM **180 GB** at
  about **8 TB/s**. No other B200 figure appears.
- Model: **8B parameters**, dense transformer, Adam.
- The starting run: **20,000 tokens/s**, **MFU 43 %**, **GPU-Util 100 %**
  (ep 8's numbers). The meter starts at 43 %.
- **No after-numbers.** The meter nudges up after each lever with no
  label and no percentage: no speedup or MFU gain is claimed for any
  lever (each depends on the model, batch and kernel mix; see "Facts to
  keep straight").
- The four levers, in this order, with the exact code on screen:
  1. `with torch.autocast("cuda", dtype=torch.bfloat16):`
  2. `batch_size = 64` → `128` (a picture of "bigger", not a recommended
     value; the label says only "batch ↑")
  3. `model = torch.compile(model)`
  4. `model = torch.compile(model, mode="reduce-overhead")`
- The grid: 12 × 12 cells, a picture of "many cores", not the SM count.
- Tensor cores: the highlighted sub-block inside each cell (series image,
  ep 5 on).

## VO (draft: 143 words without the if-time beat, 157 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Four changes raise MFU on a busy GPU, tried in this order: bf16, bigger batches, torch compile, CUDA graphs. | Frame 0 already working: the series chip mid-stage, ~40 % of cells lit teal, the rest dark; HBM slab right of the grid; the CPU (Python) box top-left with its queue of kernel tiles; the MFU meter at right reading `43%`, needle in magenta. A four-slot checklist card at the top of the stage fills as the VO names them: `bf16 · batch ↑ · torch.compile · CUDA graphs`, all grey. |
| 02_bf16 | First, autocast to bf16. By default, PyTorch runs fp32 matmuls without the tensor cores. In bf16, they run on them. | Checklist slot 1 turns teal. Code card bottom-middle, line 1 types in: `with torch.autocast("cuda", dtype=torch.bfloat16):` / `    loss = model(x)`. In the grid, each cell's tensor-core sub-block (dark until now) lights; magenta hero passes to the sub-blocks. The meter needle nudges up (no number). |
| 03_batch | Second, a bigger batch or longer sequences, as far as memory allows. Each kernel gets more work, so it fills more of the chip. | Slot 2 teal. A kernel tile leaves the queue: small, it lights a corner patch of the grid; the next tile is twice as wide and lights most of the grid. Code card adds `batch_size = 64` with `64` struck and `128` written over it. Magenta hero: the wide tile. Meter nudges up. |
| 04_compile | Third, torch compile. Small elementwise ops, like adds and activations, wait on memory: each one reads its data and writes it back. Compile fuses a chain of them into one kernel, so the data goes through memory once. | Slot 3 teal. In the queue, three small tiles labeled `add`, `mul`, `gelu`: each one, as it runs, sends a round trip down the pipe to HBM and back (three round trips). Then the three tiles slide together and merge into one tile `fused` (magenta hero); it makes one round trip. Code card adds `model = torch.compile(model)` (the payoff line, magenta for the beat). Meter nudges up. |
| 05_graphs | Fourth, CUDA graphs, for steps made of many tiny kernels the CPU can't launch fast enough. Reduce-overhead mode records the step once and replays it in one launch. | Slot 4 teal. The queue is a long row of tiny tiles; the CPU box ticks them out one by one and gaps open between them in the grid (cells go dark between tiles). The row snaps into one bracketed block labeled `graph` (magenta hero) that enters in one move; the gaps close. Code card's compile line gains `, mode="reduce-overhead"`. Meter nudges up. |
| 06_warmup *(if time)* | Your first compiled step is slow; that's the compile. Time the steps after it. | A small step-time strip under the chip: the first bar tall and grey, labeled `compile`, the rest short and teal. |
| 07_close | Make one change, re-measure MFU, and keep it only if the number goes up. | Final visual: the checklist card, each slot now followed by a small meter tick; the full code card below it; the MFU meter in magenta. Takeaway only, no outro. |

Line 1 is the answer (the four levers, in order) and says the search phrase;
"torch compile" is spoken by ~4 s and on screen in the checklist from frame
0. Beat 06 is the *(if time)* cut: a practical detour the viewer would not
miss. Beat 05 stays even though it is the least common fix: it is the
lever for the "busy but tiny kernels" case, and the code card would be
incomplete without it. The why-clauses link back once each: tensor cores
(ep 5), "wait on memory" (ep 5), "the CPU can't launch fast enough" (ep 6),
bf16 (ep 4). None is explained here.

The closer is the viewer's next move, not line 1 again: one change at a
time, measured.

## Facts to keep straight (notes, not VO)

- **Beat 02, "by default, PyTorch runs fp32 matmuls without the tensor
  cores":** `torch.backends.cuda.matmul.allow_tf32` "defaults to False in
  PyTorch 1.12 and later" (PyTorch CUDA semantics notes, 2.14 docs), so
  plain fp32 matmuls use full-fp32 (non-tensor-core) math unless you opt
  into TF32 (`torch.set_float32_matmul_precision("high")`). TF32 is a
  middle step, cut for length. Under `torch.autocast(..., dtype=bfloat16)`,
  matmuls and convolutions run in bf16, which the tensor cores run at the
  bf16 peak (2,250 TFLOPS dense on B200). The ledger's run is already
  bf16; for that run lever 1 is the check, not the fix. Note: newer cuBLAS
  can emulate fp32 GEMMs on Blackwell tensor cores, opt-in only; the
  "by default" in the VO keeps the claim true.
- **Autocast and Adam:** autocast keeps fp32 weights and casts per op;
  bf16 needs no loss scaling (fp16 does). Ep 12 owns the 16-bytes-per-param
  memory math.
- **Beat 03, bigger batch:** larger matmuls give more tiles to spread
  across the SMs and reuse each weight read across more tokens. Gains
  flatten once the matmuls are already big; for an 8B model at a
  reasonable batch they may already be. Bigger batch can change
  convergence (learning-rate scaling); companion material.
- **Beat 04, `torch.compile`:** the tutorial: "Speedup mainly comes from
  reducing Python overhead and GPU read/writes"
  (docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html).
  TorchInductor fuses pointwise and reduction ops into single Triton
  kernels, keeping intermediates in registers; matmuls use templates with
  limited epilogue fusion (PyTorch blog, "Why is PyTorch compile so fast:
  kernel fusion", 2026). The blog's multiply-add-sigmoid example cuts memory
  operations from 8 to 4; a simplified example, not cited in the VO.
  Graph breaks (Python the compiler can't trace) split the model into
  several compiled pieces and reduce the gain.
- **Beat 05, CUDA graphs:** `mode="reduce-overhead"` "reduces the overhead
  of python with CUDA graphs, useful for small batches", "can come at the
  cost of more memory usage", and "is not guaranteed to work" (torch.compile
  docs, 2.14). CUDA graphs need static shapes and no CPU-GPU sync (e.g.
  `.item()`) inside the captured region (CUDA semantics notes). With graph
  breaks there is one graph per compiled piece, so "replays it in one
  launch" is the simple case; narrow to "replays it as a graph" if Chris
  wants it exact. `mode="max-autotune"` also enables CUDA graphs on GPU;
  not mentioned.
- **The order** is the practical one (cheapest and most common first),
  not a ranking by gain; for a large model at a good batch, lever 4 often
  does nothing because kernels are already big.
- **No speedup number is in the VO** and the meter shows none: published
  `torch.compile` speedups (the PyTorch 2.0 launch benchmarks on A100
  across HF/TIMM/TorchBench models; figure not re-checked here) are not a
  comparable setup to an 8B LLM on a B200.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top: the four-slot checklist card, ~1 row.
- Stage upper-left: the CPU (Python) box and its queue of kernel tiles
  running right into the chip.
- Stage middle: the core grid (12 × 12) with tensor-core sub-blocks; HBM
  slab and pipe to its right; the MFU meter at the far right (shrink the
  slab if both don't fit at 9:16; meter wins).
- Under the grid: the step-time strip (beat 06 only).
- Stage bottom-middle: the code card, growing one line per lever, ~3 rows.
- One magenta hero at a time: the MFU needle → the tensor-core sub-blocks
  → the wide kernel tile → the `fused` tile and its code line → the
  `graph` block → the MFU meter.
