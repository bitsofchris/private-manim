# Understanding the GPU: the series (8 Shorts)

**Name:** understanding-the-gpu-series
**Description:** Shorts for a research engineer who trains models on GPUs
but has never been taught what the GPU is doing: what a FLOP is, what a
kernel is, where the data goes, and how to tell whether training is using
the chip well. Grew out of Chris's 2026-10-27 note ("MFU vs GPU
saturation, what's the difference?") and his follow-up questions in the
storyboard session the same night. **Status (10/27, v2): 8 Shorts. Chris cut 10–13 (loader, raising MFU,
OOM, multi-GPU: storyboards kept in `_archive/`) and the nvidia-smi Short
merged into utilization vs MFU (ep 7). Numbers moved to realistic values
(15,000 tokens/s per GPU, 32 % MFU). No YouTube titles yet: proposed at
runbook step 9, Chris picks then. VO is
a draft in Chris's voice.**
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
- **Throughput:** **15,000 tokens/s per GPU**, one B200 in an 8-GPU run
  (an 8B model with Adam needs 128 GB before activations, so nobody trains
  it on one GPU; always say "per GPU"). Chosen, not measured: in the range
  real 8B runs report (torchtitan's H100 table, 5,762 tokens/s/GPU plain
  bf16 ≈ 28 % MFU; NVIDIA's tuned recipes ~39–40 %).
- **FLOPs:** a FLOP is one floating-point multiply or one add. Training
  costs **6 × params per token** (forward 2, backward 4). The run does
  6 × 8e9 × 15,000 = **720 TFLOPS** → **MFU 32 %**: a typical run with
  room to improve (big tuned runs: PaLM 46 %, Llama 3 405B 38–43 %). nvidia-smi on the same
  run: **GPU-Util 100 %**.
- **The tiny layer** (for counting FLOPs): 3 inputs, 2 outputs, **6
  weights**; forward 12 FLOPs = 2 × 6.
- **Memory for the 8B model with Adam, mixed precision:** 16 bytes per
  parameter = **128 GB** before activations (bf16 weights 2 + bf16 grads
  2 + fp32 master weights 4 + Adam m 4 + Adam v 4). Activations on top
  scale with batch × sequence length.
- **Reference:** PaLM 540B trained at **46 % MFU** (Chowdhery et al. 2022,
  the paper that named MFU).
- **Derived and shared (added after the storyboards, 10/27):**
  - B200 dense ladder: TF32 **1,125** / bf16 **2,250** / fp8 **4,500**
    TFLOPS (HGX B200 page, sparse ÷ 2 ÷ 8). An "fp32" matmul on tensor
    cores is TF32; the ladder is labeled TF32, never fp32.
  - Needed arithmetic intensity: 2,250e12 ÷ 8e12 ≈ **280 FLOPs per byte**
    (ep 5). Bandwidth 8 TB/s; one source says 7.7 (→ ~290).
  - Units: ledger memory is decimal **GB**; PyTorch errors print **GiB**
    (128 GB ≈ 119 GiB). Say GB in the VO.
  - GPU-Util's sample window is **1/6 s to 1 s** depending on the GPU:
    say "recent time", never "the last second". Ray's dashboard reads the
    same NVML number (verified in Ray's source, ep 7).
  - 6 × 8e9 includes Llama-3-8B's ~0.5B input-embedding lookup (no
    matmul), an overcount of ~7 %; notes only.
  - Whole-run example: Llama 3 8B trained on 15T+ tokens (Meta model
    card); at 15,000 tokens/s that's ~32 years on one B200 (ep 3).
  - The series training step, one code card for eps 6, 7, 8:
    `loss = loss_fn(model(x), y)` / `loss.backward()` / `opt.step()` /
    `print(loss.item())`.
  - Kernel-tile labels in the queue, everywhere: `matmul`, `add`, `relu`,
    `softmax`, `∇` (backward), `adam`.
  - On-screen nvidia-smi values (ep 7) are illustrative and
    must match: 100 % GPU-Util, ~143 GB used. The B200's reported total
    (MiB) is unverified: take it from a real readout before building.
- **Code on screen** is real PyTorch that runs: `torch.profiler`,
  `torch.compile`, `torch.cuda.utilization()`, `loss.item()`,
  `DataLoader(num_workers=..., pin_memory=True)`.

## The series image (one chip, drawn the same way every episode)

**Built 10/29 on take A (core grid), Chris's pick** from
`00_layout/takes/takes.png`. The kit is `_kit/` (`chip.js`: the chip and
its slots, state object `S`; `code.js`: a link to the shared code card
`videos/_shared/web/code/code.js`, mounted `CODE.DOCK` under the chip; `data.js`: every string and number). `00_layout/layout.png` shows it
in six states (rest, ep 5, ep 6, ep 7 ×3). The bottom slot holds the time
strip or the code card, one at a time; the side slot holds HBM or the MFU
meter, one at a time.

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
  kernel ran, grey when idle (ep 7 on; unrolls into the trace in ep 8).
- **The MFU meter:** a gauge right of the chip (ep 7 on).
- **The loader:** a box feeding batches in from the left (ep 7, beat 04).
- One magenta hero at a time (`AGENTS.md` rule 2); everything else teal
  or grey.

## One home per fact (say it fully once; elsewhere one clause at most)

| Fact | Home |
|---|---|
| GPU vs CPU: many simple cores vs few big ones | ep 1 |
| What a FLOP is; FLOPs vs FLOPS; floating point as the picture (scientific notation in binary) | ep 2 |
| 6 × params × tokens, forward 2 + backward 4 | ep 3 |
| Bit widths, bf16/fp16/fp8, dense vs sparse spec | ep 4 |
| Tensor cores vs memory; compute-bound vs memory-bound | ep 5 |
| What a kernel is; the CPU queue; async; `.item()` syncs | ep 6 |
| What nvidia-smi shows; GPU-Util = share of time any kernel ran; MFU from tokens/s | ep 7 |
| Reading a profiler trace; idle gaps | ep 8 |

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
| 1 | Why GPUs for AI | Why does AI run on GPUs and not CPUs? | A neural net is almost all multiply-adds, and they don't depend on each other; a GPU is thousands of simple cores built to do them at once, a CPU a few big cores built to run one thread fast (no CPU core count: 2026 server CPUs reach 192–288 cores). | `why gpu for ai` (offered; also `gpu vs cpu explained`) | *(adjacent)*, the ep 0 the rest stand on |
| 2 | FLOPs explained | What is a FLOP, and why are GPUs rated in them? | One floating-point multiply or add. FLOPs is a count, FLOPS a rate; a B200 does ~2,250 trillion bf16 FLOPS. AI compute and cost are counted in FLOPs. | `flops explained` (offered; results are AI explainers, suggestions are mostly flip-flops); `teraflops explained` | Chris |
| 3 | Why 6 FLOPs per parameter per token | How much compute does training a model take? | Forward: each weight is one multiply and one add, 2. Backward: two matmuls the same size (gradient for the input, gradient for the weight), 4. Total 6 × params × tokens; that turns into GPU-hours and dollars. | not checked; may fold into #2 | Chris's question |
| 4 | Floating point and precision | Why does bf16 / fp8 make training faster? | Fewer bits per number: more numbers per memory read and more multiply-adds per tensor-core cycle, so peak FLOPS roughly doubles each step down. Spec sheets also quote "sparse" at 2×; compare against dense in your training dtype. | `bf16 vs fp16`, `fp32 vs fp16`, `fp8 training` | Chris's "what is floating point" |
| 5 | Tensor cores vs memory | Where does the time go inside the GPU? | Data flows from GPU memory (HBM) through cache to the tensor cores. Matmuls reuse each number many times, so the tensor cores stay fed (compute-bound); elementwise ops do one FLOP per number moved, so the cores wait on memory (memory-bound). Drawn as data flowing through the chip. | `tensor cores explained`, `tensor cores vs cuda cores`, `how tensor cores work`; `roofline model explained` for a later cut | Chris |
| 6 | What is a CUDA kernel (one training step, walked through) | What is a GPU kernel, and what happens when my training step runs? | A kernel is one function the CPU launches onto the GPU, run as thousands of threads at once. `loss = model(x)` becomes a queue of kernel launches; the CPU runs ahead, the GPU drains the queue; `loss.item()` makes the CPU wait; a late batch leaves the queue empty and the GPU idle. | `what is a cuda kernel` (offered verbatim); `cuda kernel` (strong); alt `how gpu works for deep learning`. Competitive: Fireship, Computerphile | Chris |
| 7 | nvidia-smi: GPU-Util vs MFU | Is my training actually using the GPU fully? | nvidia-smi's GPU-Util says some kernel ran (busy); MFU says how much of the chip's peak math the model used (6 × params × tokens/s ÷ peak). You log it yourself. | `gpu utilization` (10/28: the take drops nvidia-smi on purpose; autocompletes, results lean gaming) | Chris, the original note; merged with the old nvidia-smi idea 10/27 |
| 8 | Reading a PyTorch profiler trace | Where are the idle gaps in my training step? | `torch.profiler` draws every kernel on a timeline; the gaps are the GPU waiting (data, CPU, a sync). Find the biggest gap first. | `pytorch profiler` (offered; also `pytorch profiler tutorial`) | Chris's "how does PyTorch show this" |

**Cut 10/27 (Chris: "we don't need 10–13"), storyboards in `_archive/`:**
the data loader (overlapped 014), raising MFU, CUDA out of memory,
multi-GPU communication. The standalone nvidia-smi Short is in
`_archive/ep07-nvidia-smi/` too; its fact checks back ep 7.

## Folded in, not their own Short

- **The word "kernel":** Linux kernel (OS core), CUDA kernel (a GPU
  function), convolution kernel (CNN weights), kernel methods (SVMs).
  One line in #6 at most; the rest is companion material.
- **HFU vs MFU** (activation recompute counts as 8N, not 6N): a note in
  #7's companion.
- **CPU-GPU sync points** (`.item()`, `print(loss)`): a beat inside #6.
- **DCGM counters** (`SM_ACTIVE`, `PIPE_TENSOR_ACTIVE`): companion
  material for #7.

## How it was recorded

One file, `~/Creating/016-gpu-understanding.m4a` (497.6 s, AAC mono
44.1 kHz), 2026-10-28, series order, "Episode N: working name" before
episodes 2–8. Exported with a title tag, like 014's, so likely Descript;
**whether Studio Sound was on is not known: ask Chris before step 3**
(loudnorm only unless he says otherwise; never denoise a Studio Sound
take). Split 2026-10-28: cut times in `TRANSCRIPT.md` and each
`script.md`, with where each take leaves the planned script.

From the split, for the episode sessions:
- Ep 7 never says "nvidia-smi", on purpose (Chris, 10/28). Its search
  phrase moves to `gpu utilization` (see its `script.md`).
- Repeats to cut: ep 6 ("Forward queues…"), ep 7 ("GPU utilization
  measures…").
- No recorded closer (next move) in ep 1 or ep 3.
- Ear checks settled by the written VO (Chris, 10/28): "Divide a run's
  FLOPs", "training step", "doing right then".

## Checklist

| # | Folder | Storyboard | VO (Chris edited) | Recorded (raw) | Beats | Assembled | Shipped |
|---|---|---|---|---|---|---|---|
| 1 | `ep01-why-gpus-for-ai/` | v5 | in the take | 49.5 s | 6 | 44.0 s | |
| 2 | `ep02-flops-explained/` | v2 | in the take | 61.9 s | | | |
| 3 | `ep03-six-flops-per-parameter/` | v2 | in the take | 48.2 s | | | |
| 4 | `ep04-floating-point-precision/` | v2 | in the take | 51.9 s | | | |
| 5 | `ep05-tensor-cores-vs-memory/` | v2 | in the take | 54.3 s | | | |
| 6 | `ep06-cuda-kernel-training-step/` | v2 | in the take | 59.6 s | | | |
| 7 | `ep07-nvidia-smi-utilization-vs-mfu/` | v3 | in the take | 75.6 s | | | |
| 8 | `ep08-pytorch-profiler/` | v2 | in the take | 47.5 s | | | |

## Open decisions (Chris's)

- ~~Recording order~~: recorded 1–8 (10/28).
- ~~Ep 7's search phrase~~: `gpu utilization` (10/28). It autocompletes
  but its results lean gaming, so the titles and description line 1 must
  say training or AI.
- ~~Ep 7's "kernel"~~: settled in the take; ep 7 defines it inline.
- Ep 7 keeps one clause on the data loader (beat 04) now that the loader
  Short is cut.
