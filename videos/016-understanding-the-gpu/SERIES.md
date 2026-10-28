# Understanding the GPU: the series (13 Shorts)

**Name:** understanding-the-gpu-series
**Description:** Shorts for a research engineer who trains models on GPUs
but has never been taught what the GPU is doing: what a FLOP is, what a
kernel is, where the data goes, and how to tell whether training is using
the chip well. Grew out of Chris's 2026-10-27 note ("MFU vs GPU
saturation, what's the difference?") and his follow-up questions in the
storyboard session the same night. **Status (10/27): Chris asked for all 13
ready to record; one storyboard per episode folder `epNN-slug/`, VO
drafted in his voice for him to edit.** Ep 8 (MFU) was storyboarded first.
**When to use:** the series home (`agents/series.md` step 1): the ledger
every episode copies, the recurring image, which episode owns which
fact, the checklist. Each episode then runs `agents/runbook.md` from
step 2 in its folder.
**How it works:** each idea is one Short with one question. Every
episode must stand alone (viewers arrive from search), but the order
below builds each one on the last. Search phrases were checked 2026-10-27
against YouTube's autocomplete endpoint, not a browser.

## Who it is for, the promise

A research engineer who writes PyTorch training loops, watches
nvidia-smi or the Ray dashboard, and can't say whether the run is
efficient, or why. Knows Python and neural nets; has never written CUDA.
**Promise:** by the end you can picture one training step moving through
the chip, and you know which number says the GPU is busy and which says
it is doing useful work.

## Ledger (every episode copies these; nothing invented per episode)

- **GPU:** one NVIDIA **B200**. bf16 dense peak **2,250 TFLOPS** (say
  "about 2,250 teraflops" or "2.25 petaflops"); the 2× "sparse" figure is
  only ever shown as the spec-sheet trap (ep 4). GPU memory (HBM):
  **180 GB**, bandwidth about **8 TB/s**. Verify any other B200 figure
  before using it; the exact SM count is never stated (the grid is a
  picture, not a count).
- **Model:** an **8B-parameter** dense transformer (Llama-3-8B sized),
  trained in **bf16** with Adam.
- **Throughput:** **20,000 tokens/s** on one B200.
- **FLOPs:** a FLOP is one floating-point multiply or one add. Training
  costs **6 × params per token** (forward 2, backward 4). The run does
  6 × 8e9 × 20,000 = **960 TFLOPS** → **MFU 43 %**. nvidia-smi on the same
  run: **GPU-Util 100 %**.
- **The tiny layer** (for counting FLOPs): 3 inputs, 2 outputs, **6
  weights**; forward 12 FLOPs = 2 × 6.
- **Memory for the 8B model with Adam, mixed precision:** 16 bytes per
  parameter = **128 GB** before activations (bf16 weights 2 + bf16 grads
  2 + fp32 master weights 4 + Adam m 4 + Adam v 4). Activations on top
  scale with batch × sequence length.
- **Reference:** PaLM 540B trained at **46 % MFU** (Chowdhery et al. 2022,
  the paper that named MFU).
- **Code on screen** is real PyTorch that runs: `torch.profiler`,
  `torch.compile`, `torch.cuda.utilization()`, `loss.item()`,
  `DataLoader(num_workers=..., pin_memory=True)`.

## The series image (one chip, drawn the same way every episode)

HyperFrames, house style (`AGENTS.md`). Each episode adds one part to a
picture the viewer has seen before:

- **The chip:** a rounded box mid-stage holding a **12 × 12 grid of core
  cells** (dark at rest, teal when working). Tensor cores (ep 5 on) are a
  highlighted sub-block inside each cell, not a new drawing.
- **Memory (HBM):** a slab to the right of the chip, label `HBM 180 GB`,
  joined to the grid by a pipe whose width shows bandwidth (ep 5).
- **The CPU and its queue:** a small box top-left, label `CPU (Python)`,
  with a queue of kernel tiles running into the chip (ep 6 on).
- **The time strip:** a row of slots under the chip, filled when any
  kernel ran, grey when idle (ep 7 on).
- **The MFU meter:** a gauge right of the chip (ep 8 on).
- **The loader:** a box feeding batches in from the left (ep 10).
- One magenta hero at a time (`AGENTS.md` rule 2); everything else teal
  or grey.

## One home per fact (say it fully once; elsewhere one clause at most)

| Fact | Home |
|---|---|
| GPU vs CPU: many simple cores vs few big ones | ep 1 |
| What a FLOP is; FLOPs vs FLOPS; why chips are rated in them | ep 2 |
| 6 × params × tokens, forward 2 + backward 4 | ep 3 |
| Floating point, precision, bf16/fp8, dense vs sparse spec | ep 4 |
| Tensor cores vs memory; compute-bound vs memory-bound | ep 5 |
| What a kernel is; the CPU queue; async; `.item()` syncs | ep 6 |
| What nvidia-smi shows; GPU-Util = share of time any kernel ran | ep 7 |
| MFU; computing it from tokens/s | ep 8 |
| Reading a profiler trace; idle gaps | ep 9 |
| Data loader starving the GPU; workers, pinned memory, prefetch | ep 10 |
| Raising MFU: batch, `torch.compile` fusion, bf16, CUDA graphs | ep 11 |
| What fills GPU memory; 16 bytes per param; OOM | ep 12 |
| Multi-GPU all-reduce; communication vs compute overlap | ep 13 |

## Where the ideas came from

- **Chris called out:** MFU vs utilization (the original note), FLOPs
  ("maybe another video is just explain FLOPs"), GPU kernels and how the
  CPU queues a training step, tensor cores vs memory as data flowing
  through the chip.
- **From Chris's questions in the session:** why 6 FLOPs per parameter
  per token; what nvidia-smi is; what "kernel" means and why not just
  "function"; what "any kernel ran" means and why a tiny kernel isn't
  useful; what floating point means; how PyTorch and Ray show this.
- **Adjacent, not asked:** marked *(adjacent)* below. On-topic and
  searched, but Chris hasn't asked for them.

## Ideas, in a build order

| # | Working title | Their question | The answer, roughly | Search phrase (autocomplete 10/27) | Source |
|---|---|---|---|---|---|
| 1 | Why GPUs for AI | Why does AI run on GPUs and not CPUs? | A neural net is almost all multiply-adds, and they don't depend on each other; a GPU is thousands of simple cores built to do them at once, a CPU a few dozen built for branching code. | `why gpu for ai` (offered; also `gpu vs cpu explained`) | *(adjacent)*, the ep 0 the rest stand on |
| 2 | FLOPs explained | What is a FLOP, and why are GPUs rated in them? | One floating-point multiply or add. FLOPs is a count, FLOPS a rate; a B200 does ~2,250 trillion bf16 FLOPS. AI compute and cost are counted in FLOPs. | `flops explained` (offered; results are AI explainers, suggestions are mostly flip-flops); `teraflops explained` | Chris |
| 3 | Why 6 FLOPs per parameter per token | How much compute does training a model take? | Forward: each weight is one multiply and one add, 2. Backward: two matmuls the same size (gradient for the input, gradient for the weight), 4. Total 6 × params × tokens; that turns into GPU-hours and dollars. | not checked; may fold into #2 | Chris's question |
| 4 | Floating point and precision | Why does bf16 / fp8 make training faster? | Fewer bits per number: more numbers per memory read and more multiply-adds per tensor-core cycle, so peak FLOPS roughly doubles each step down. Spec sheets also quote "sparse" at 2×; compare against dense in your training dtype. | `bf16 vs fp16`, `fp32 vs fp16`, `fp8 training` | Chris's "what is floating point" |
| 5 | Tensor cores vs memory | Where does the time go inside the GPU? | Data flows from GPU memory (HBM) through cache to the tensor cores. Matmuls reuse each number many times, so the tensor cores stay fed (compute-bound); elementwise ops do one FLOP per number moved, so the cores wait on memory (memory-bound). Drawn as data flowing through the chip. | `tensor cores explained`, `tensor cores vs cuda cores`, `how tensor cores work`; `roofline model explained` for a later cut | Chris |
| 6 | What is a CUDA kernel (one training step, walked through) | What is a GPU kernel, and what happens when my training step runs? | A kernel is one function the CPU launches onto the GPU, run as thousands of threads at once. `loss = model(x)` becomes a queue of kernel launches; the CPU runs ahead, the GPU drains the queue; `loss.item()` makes the CPU wait; a late batch leaves the queue empty and the GPU idle. | `what is a cuda kernel` (offered verbatim); `cuda kernel` (strong); alt `how gpu works for deep learning`. Competitive: Fireship, Computerphile | Chris |
| 7 | What nvidia-smi tells you | What do the numbers in nvidia-smi mean? | It's NVIDIA's monitor that ships with the driver: memory used, power, temperature, and GPU-Util, the share of time *any* kernel ran. Read it for "is it alive and is memory full", not "is it efficient". | `nvidia smi` (offered; results are ML/Linux monitoring) | Chris's "what is nvidia-smi" |
| 8 | GPU utilization vs MFU | Is my training actually using the GPU fully? | Utilization says the GPU is busy; MFU says how much of the chip's peak math your model used (6 × params × tokens/s ÷ peak). You log it yourself. | `nvidia smi gpu utilization`; `model flops utilization` (no autocomplete, on-topic results) | Chris, the original note. **Storyboarded: `storyboard.md` v2** |
| 9 | Reading a PyTorch profiler trace | Where are the idle gaps in my training step? | `torch.profiler` draws every kernel on a timeline; the gaps are the GPU waiting (data, CPU, a sync). Find the biggest gap first. | `pytorch profiler tutorial` (offered) | Chris's "how does PyTorch show this" |
| 10 | Why your GPU sits idle: the data loader | Why is my GPU utilization low? | The GPU drains its queue faster than the loader fills it. Workers, pinned memory, prefetch. | ties to `../014-pytorch-dataloading/` (Bytes to Tensor) | the original note ("GPU saturation") |
| 11 | Raising MFU | My GPU is busy but MFU is low; what do I change? | Bigger batches (fuller kernels), `torch.compile` (fuses small memory-bound kernels), bf16, CUDA graphs (less launch overhead). | `torch compile`, `how does torch compile work` | follows from #5, #6, #8 |
| 12 | CUDA out of memory | What fills GPU memory during training? | Weights, gradients, optimizer state (Adam keeps two more numbers per weight) and activations; activations grow with batch and sequence length. | `cuda out of memory pytorch` (offered, high-volume) | *(adjacent)* |
| 13 | Multi-GPU: when communication eats MFU | Why doesn't 8 GPUs give me 8× speed? | Gradients are synced every step (all-reduce); if that isn't overlapped with compute, the GPUs wait on each other. | not checked | *(adjacent)*, later |

## Folded in, not their own Short

- **The word "kernel":** Linux kernel (OS core), CUDA kernel (a GPU
  function), convolution kernel (CNN weights), kernel methods (SVMs).
  One line in #6 at most; the rest is companion material.
- **HFU vs MFU** (activation recompute counts as 8N, not 6N): a note in
  #8's companion.
- **CPU-GPU sync points** (`.item()`, `print(loss)`): a beat inside #6.
- **DCGM counters** (`SM_ACTIVE`, `PIPE_TENSOR_ACTIVE`): companion
  material for #7 / #8.

## Checklist

| # | Folder | Storyboard | VO (Chris edited) | Recorded | Beats | Assembled | Shipped |
|---|---|---|---|---|---|---|---|
| 1 | `ep01-why-gpus-for-ai/` |  | | | | | |
| 2 | `ep02-flops-explained/` |  | | | | | |
| 3 | `ep03-six-flops-per-parameter/` |  | | | | | |
| 4 | `ep04-floating-point-precision/` |  | | | | | |
| 5 | `ep05-tensor-cores-vs-memory/` |  | | | | | |
| 6 | `ep06-cuda-kernel-training-step/` |  | | | | | |
| 7 | `ep07-nvidia-smi/` |  | | | | | |
| 8 | `ep08-gpu-utilization-vs-mfu/` | v2 | | | | | |
| 9 | `ep09-pytorch-profiler/` |  | | | | | |
| 10 | `ep10-gpu-idle-dataloader/` |  | | | | | |
| 11 | `ep11-raising-mfu/` |  | | | | | |
| 12 | `ep12-cuda-out-of-memory/` |  | | | | | |
| 13 | `ep13-multi-gpu-communication/` |  | | | | | |

## Open decisions (Chris's)

- Release order: build order above, or the four Chris called out first
  (2, 6, 5, 8).
- Whether #3 folds into #2 and #7 folds into #8 after reading the drafts.
