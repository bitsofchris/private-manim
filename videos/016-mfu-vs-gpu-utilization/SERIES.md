# Understanding the GPU: the series (idea backlog)

**Name:** understanding-the-gpu-series
**Description:** Shorts for a research engineer who trains models on GPUs
but has never been taught what the GPU is doing: what a FLOP is, what a
kernel is, where the data goes, and how to tell whether training is using
the chip well. Grew out of Chris's 2026-10-27 note ("MFU vs GPU
saturation, what's the difference?") and his follow-up questions in the
storyboard session the same night. **Status: idea backlog. The arc and
episode order are not agreed yet; only the MFU Short has a storyboard
(`storyboard.md`, v2).**
**When to use:** pick the next episode from here; when an arc is agreed,
this file becomes the series file `agents/series.md` step 1 describes
(ledger, per-episode preflight, checklist).
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

## Open decisions (Chris's)

- The arc: all 13, or a first season (a suggestion: 2, 6, 5, 8, the four
  Chris called out, in that order, then 7, 9, 11).
- Whether #3 folds into #2 and #7 folds into #8.
- The series image: one chip drawn the same way in every episode (a grid
  of cores, the memory beside it, a queue from the CPU), so each Short adds
  one part to a picture the viewer already knows.
- Folder layout: this folder becomes `016-understanding-the-gpu/` with one
  `epNN-slug/` per episode (`agents/series.md`), the MFU storyboard moving
  to its episode folder.
