ENGINE: hyperframes

# What is a CUDA kernel (one training step, walked through): storyboard (v1, VO draft for Chris)

THE QUESTION: "What is a kernel? Why not just say function? And what
happens on the GPU when my training step runs?"
WHO IS ASKING: a research engineer who writes PyTorch training loops,
keeps hearing "kernel" (in profiler traces, in `torch.compile` talk, in
"write a custom kernel") and can't say what one is or how a line of
Python turns into work on the GPU.
THE ANSWER IN ONE SENTENCE: a CUDA kernel is a function the CPU queues
for the GPU, run as thousands of threads at once; every op in your
training step becomes one or more, the CPU runs ahead filling the queue,
and `loss.item()` makes it stop and wait.
THE SEARCH PHRASE: what is a cuda kernel (checked 10/27 via YouTube's
autocomplete endpoint, not a browser: offered verbatim; "cuda kernel"
also strong, with "cuda kernel tutorial" and "writing cuda kernels".
Results are on topic but competitive: Fireship "Nvidia CUDA in 100
Seconds", Computerphile "What is CUDA?", "CUDA: Kernels, Blocks, Grids,
Threads and Warps". "what is a gpu kernel" autocompletes too, same
results. "pytorch cuda kernel" gets no autocomplete. Our angle is a
kernel seen through one PyTorch training step, not a CUDA C tutorial.)

**Titles (runbook step 9, Chris picks; both carry the search phrase):** search `What is a CUDA Kernel? Your code, on the GPU` (44 chars) · hook `Your CPU just fills a queue (what is a CUDA kernel)`

**One idea:** your training loop doesn't do the math; it queues kernels,
and the GPU drains the queue.

**Source note:** the source is Chris's questions in the 10/27 chat ("What
is a kernel? Why not just say function? Does kernel mean different things
in Linux, CPU, GPU?" and "what happens inside the kernel, how the CPU
queues commands in a typical training step"). He has no written sentences
on this, so the VO is a draft in his voice for him to rewrite. His own
question kept as beat 2's opener: "Why not just say function?"

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip, the
CPU box and its queue of kernel tiles, a block grid over the cells, and a
code card. Nothing needs Manim.

Series context: ep 6 of `../SERIES.md` (Understanding the GPU). This
episode adds the CPU box and its kernel queue to the series image; every
later episode keeps them. Owns: what a kernel is, the CPU queue, async
launch, `.item()` syncs. Mentions in one clause only: the idle GPU (the
time strip and what utilization measures are ep 7; the loader fix is
cut ep 10); GPU vs CPU cores (ep 1).

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one **B200** (the series chip). No number from the ledger is
  needed in the VO; none is invented.
- The chip: the 12 × 12 grid of core cells, a picture of "many cores",
  not the real SM count; no label claims a number.
- The CPU box: top-left, label `CPU (Python)`.
- Kernel tiles in the queue, labels in this order (forward): `matmul`,
  `add`, `relu`, `matmul`, `softmax`; backward tiles carry a `∇` prefix
  (`∇matmul`, `∇relu`, …); optimizer tiles `adam`.
- The code card (real PyTorch that runs, four lines):
  ```python
  loss = loss_fn(model(x), y)   # forward: queue kernels
  loss.backward()               # backward: queue more
  opt.step()                    # update: queue more
  print(loss.item())            # CPU waits here
  ```
- "Thousands of threads" is the only count said; the block grid on screen
  is a picture (e.g. 4 × 4 blocks), not a real launch config.

## VO (draft: 150 words without the if-time beat, 163 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Every op in your PyTorch training step becomes CUDA kernels: functions your CPU hands the GPU to run. | Frame 0 already working: the series chip mid-stage (12 × 12 cells, a few lit teal), the `CPU (Python)` box top-left, and a queue of kernel tiles (`matmul`, `add`, `relu`, …) sliding from the CPU into the chip. Each tile that enters lights a patch of cells. Magenta hero: the tile at the head of the queue. ~7 rows of stage. |
| 02_threads | Why not just say function? It doesn't run once. It runs as thousands of threads, each on its own slice of the data, in blocks across the chip. | The head tile (`matmul`) stops at the chip edge and opens into a grid of blocks; the blocks spread across the cells, each block lighting its own patch; a few tiny thread ticks inside one block. A small label under the CPU box: `one call` → over the chip: `thousands of threads`. Magenta hero: the opened tile's block grid. |
| 03_async | It returns nothing; it writes to GPU memory. And the CPU doesn't wait: it drops the launch in a queue and moves on. | The finished block writes back: a short arrow from the cells to the HBM slab (`HBM 180 GB`, right of the chip, as drawn in ep 5). Then the CPU box: a new tile pops out, joins the tail of the queue, and the CPU box is already lit on the next one. Label on the queue: `CUDA stream (a queue)`. Magenta hero: the CPU box moving on. |
| 04_step | Watch one step. Forward queues a kernel or more per op: matmul, add, ReLU. Backward queues more. So does the optimizer. The CPU runs ahead while the GPU drains the queue. | The code card, bottom-middle (the payoff beat, the four ledger lines). Line 1 lights and forward tiles stream into the queue; line 2 lights, `∇` tiles join; line 3 lights, `adam` tiles join. The CPU box is several tiles ahead of the chip, which is still eating the forward tiles. Magenta hero: the lit code line. |
| 05_sync | Then loss dot item. The CPU needs a number, so it waits until the queue is empty. | Line 4 (`print(loss.item())`) lights. The CPU box greys and shows a small wait mark; the queue shortens tile by tile into the chip; when the last tile goes, one number (`loss 2.31`) travels from HBM back to the CPU box. Magenta hero: `loss.item()` on the code card. |
| 06_idle | And if the next batch isn't ready, the queue runs dry and the GPU sits idle. | The queue is empty; the CPU box waits on a late batch (a small grey box at its left, label `next batch`); every cell in the chip goes dark. Hold the dark chip for a beat. Magenta hero: the empty queue slot. |
| 07_word *(if time)* | Not the Linux kernel, and not a convolution's weights. Same word, different thing. | Two small crossed-out cards pass by the CPU box: `Linux kernel: the OS core`, `conv kernel: a 3 × 3 of weights`. The chip stays. |
| 08_close | Call item only on the steps you log. The CPU stays ahead, and the queue stays full. | The code card's line 4 becomes `if step % 100 == 0: print(loss.item())`; the queue refills and stays long, the chip lights teal and stays lit. Final visual: CPU box, full queue, busy chip. Magenta hero: the edited line. Takeaway only, no outro. |

Line 1 says "CUDA kernels" (the search phrase's noun) and the reframe in
its first clause; the queue is on screen from frame 0. Beat 02 answers
Chris's "why not just say function?" with the two differences that matter
(many copies at once; beat 03: no return, no wait). Beat 07 is the
*(if time)* cut: it answers "does kernel mean different things", but a
viewer who skips it loses nothing about the GPU. Beat 06 stays: it is
the cost of an empty queue, the reason beat 08 matters; it names the
idle GPU in one clause and leaves "utilization" to ep 7 and the loader
fix to cut ep 10. The closer is the viewer's next move, not line 1 again.
`__global__` and the `<<<blocks, threads>>>` launch are not said; if
Chris wants CUDA C on screen, a one-line inset under the opened tile in
beat 02 (`__global__ void relu(float* x)`) is the place, as a label.

## Facts to keep straight (notes, not VO)

- **Kernel = function run N times by N threads.** CUDA C++ marks it
  `__global__`; it is called from the host and runs on the device, and its
  return type must be `void`, so results are written to device memory
  (CUDA C++ Programming Guide, "Kernels"). Threads are grouped into blocks;
  each block runs on one SM, and blocks are spread over the SMs.
- **Async launch.** "A kernel launch returns immediately" and calls "may
  return before the asynchronous operation has started" (CUDA Programming
  Guide, "Asynchronous Execution",
  docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html).
  PyTorch: "By default, GPU operations are asynchronous… enqueued to the
  particular device, but not necessarily executed until later… each device
  executes operations in the order they are queued" (PyTorch CUDA
  semantics notes, docs.pytorch.org/docs/2.14/notes/cuda.html). The queue
  on screen is the current CUDA stream.
- **"Runs ahead" has a limit.** The launch queue has a finite depth; if
  the CPU gets far enough ahead it blocks on launch. Not said; true in
  the regime the Short shows.
- **`.item()` waits for the queue in this code.** PyTorch "automatically
  performs necessary synchronization when copying data between CPU and
  GPU"; `.item()` copies one number to the CPU. In the 4-line step it
  comes after `opt.step()`, and the stream runs in order, so it waits for
  every kernel queued before it ("until the queue is empty" is true here;
  called right after the forward, it would wait only for the forward).
  `print(loss)` on a CUDA tensor syncs too.
- **"Thousands of threads"**: true for training-sized tensors (an 8B
  model's matmuls launch far more); a tiny tensor's kernel may use fewer.
  Not said.
- **"A kernel or more per op"**: matmul goes to cuBLAS (one or a few
  kernels); add, ReLU, softmax, layernorm are each one or more; a fused
  op (`torch.compile`, cut ep 11) is one kernel for several ops. The exact
  kernel count per step is not said (no verified number for the 8B model;
  "thousands" per step is plausible but unverified, so cut).
- **Where the word comes from** (Chris asked): unverified. Commonly
  explained as HPC's "compute kernel", the hot inner loop applied to every
  element; no primary source found on 10/27. Not in the VO; check before
  using it in the companion. The other meanings are verified and are beat
  07: Linux/OS kernel (the core of the operating system), convolution
  kernel (the CNN filter's weights); also kernel methods (SVMs), companion
  only.
- **The closer.** Calling `.item()` every step forces a sync every step;
  logging every N steps removes all but one in N. How much it costs
  depends on the model (ep 8 shows how to see it in a trace).
- Verify before publish: that the Fireship and Computerphile titles in
  the search note are still the top results (only for the description;
  nothing in the video depends on them).

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top-left: the `CPU (Python)` box; the queue of kernel tiles runs
  from it diagonally down-right into the chip's top-left corner (~1.5
  rows).
- Stage middle: the chip (12 × 12 grid), with the HBM slab to its right
  (beat 3 only draws its write-back arrow).
- Stage bottom-middle: the code card (beat 4 on), four lines, ~2 rows.
- One magenta hero at a time: head tile → opened block grid → CPU box →
  lit code line → `loss.item()` → empty queue slot → the edited line.
- No time strip (ep 7's part) and no MFU meter (ep 7's part).
