ENGINE: hyperframes

# CUDA out of memory: storyboard (v1, VO draft for Chris)

THE QUESTION: "Why do I get CUDA out of memory, and what's filling my GPU?"
WHO IS ASKING: a research engineer whose PyTorch training run just died
with `torch.OutOfMemoryError`, who can see the model is smaller than the
GPU and doesn't know what else is using the memory or which knob to turn.
THE ANSWER IN ONE SENTENCE: training memory is weights + gradients +
optimizer state + activations; the first three are fixed by the model
(16 bytes per parameter with Adam in mixed precision), activations grow
with batch × sequence length, so the overflow is usually the batch and
the fix is a smaller micro-batch, then activation checkpointing.
THE SEARCH PHRASE: cuda out of memory pytorch (checked 10/27 via YouTube's
autocomplete endpoint and the results page, not a browser: "cuda out of
memory" autocompletes to "cuda out of memory pytorch", "… error" and
"… stable diffusion"; "pytorch out of memory" autocompletes to "cuda out
of memory pytorch". The pytorch variant's results are on topic: "Fix CUDA
Out of Memory (OOM) in PyTorch!", chapters "Where GPU Memory Goes (4
Consumers)", "Fix 1 — Batch Size & Gradient Accumulation". The stable
diffusion variant is image-gen users, a different audience. "gpu memory
training" and "what uses gpu memory" get no useful autocomplete.)

**Titles (runbook step 9, Chris picks):** search `CUDA Out of Memory in PyTorch: What's Filling Your GPU` · hook `Your 8B model needs 128 GB before it sees a single token`

**One idea:** the model's share of memory is fixed at 16 bytes a
parameter; the part that overflows is activations, and that's the batch.

**Source note:** *(adjacent)*: Chris didn't ask this one. The VO is a
draft in Chris's voice (plain, short sentences) for him to rewrite; no
vault sentences to keep.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip and
its HBM slab, stacked bars, a slider, two code cards. Nothing needs Manim.

Series context: ep 12 of `../SERIES.md` (Understanding the GPU). Owns
"what fills GPU memory; 16 bytes per param; OOM". Precision (ep 4) gets
one word ("bf16", "fp32"); multi-GPU sharding (ep 13) gets one clause in
the *(if time)* beat. HFU / recompute cost is ep 8's companion note.

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one **B200**, HBM **180 GB** (the slab label `HBM 180 GB`).
- Model: **8B parameters**, dense transformer, trained in **bf16** mixed
  precision with **Adam**.
- Bytes per parameter: **16** = bf16 weights **2** + bf16 grads **2** +
  fp32 master weights **4** + Adam m **4** + Adam v **4** (ZeRO paper,
  Rajbhandari et al. 2019, §3.1: "2Ψ+2Ψ+KΨ=16Ψ bytes", K = 12).
- Per component, 8B model: weights **16 GB**, grads **16 GB**, master
  **32 GB**, m **32 GB**, v **32 GB** = **128 GB** (decimal GB, 1e9).
- Left for activations: **52 GB** (on screen only, not spoken).
- Activations scale with **batch × sequence length** (no per-token GB
  figure is claimed anywhere).
- The error, real format (PyTorch `c10/cuda/CUDACachingAllocator.cpp`,
  main): `torch.OutOfMemoryError: CUDA out of memory. Tried to allocate
  4.00 GiB. GPU 0 has a total capacity of … of which … is free.` The
  `4.00 GiB` is illustrative; the capacity and free figures are elided
  with `…` (see Facts to verify).
- Code is real PyTorch: `torch.cuda.max_memory_allocated()`,
  `torch.cuda.memory_summary()`, `torch.cuda.reset_peak_memory_stats()`,
  `torch.utils.checkpoint.checkpoint(..., use_reentrant=False)`.

## VO (draft: 145 words without the if-time beat, 156 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | CUDA out of memory means four things filled your GPU: weights, gradients, optimizer state, and activations. Only activations grow with your batch. | Frame 0 already working: the series chip mid-left, the HBM slab to its right drawn tall (the hero of this episode), already full to the brim with five stacked teal bars plus an activations bar spilling over the top in magenta. Above, a terminal card with the real error line: `torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 4.00 GiB.` On "four things" the four labels tick on beside the slab. |
| 02_model | Train an 8-billion-parameter model in mixed precision with Adam. Each parameter costs 16 bytes. | Slab empties. One weight cell zooms out of the chip as a single parameter; a byte ruler of 16 boxes draws beside it. Magenta hero: the `16 bytes` label. |
| 03_breakdown | Two for the bf16 weight, two for its gradient, four for an fp32 master copy, eight for Adam's two running averages. | The 16 boxes color into five groups as each is said: `weight 2`, `grad 2`, `master 4`, `Adam m 4`, `Adam v 4`. Magenta hero moves group to group. |
| 04_total | That's 128 gigabytes on a 180 gigabyte B200, before a single activation. | Each group becomes a bar stacked into the slab, sized to scale: 16 / 16 / 32 / 32 / 32 GB, summing to a `128 GB` bracket. The empty top of the slab is labeled `52 GB left`. Magenta hero: `128 GB`. |
| 05_activations | Activations are what the forward pass keeps for the backward pass. They grow with batch size times sequence length, and fill the rest. That's what overflows. | A slider under the slab, `batch × seq len`. As it moves right a magenta activations bar rises from the 128 GB line, fills the 52 GB, and spills over the slab top; the terminal error card flashes back on at the overflow. |
| 06_fixes | So shrink the micro-batch and use gradient accumulation to keep the same effective batch. Still over? Turn on activation checkpointing: recompute most of them in the backward pass instead of storing them. | The code card, bottom-middle (real lines): `for mb in batch.chunk(4):` / `    loss = model(mb).loss / 4` / `    loss.backward()` / `opt.step(); opt.zero_grad()`. Slider snaps left to a quarter; the activations bar drops under the line. Then a second line highlights: `h = checkpoint(block, h, use_reentrant=False)`, and the activations bar shrinks again. Magenta hero: the activations bar. |
| 07_shard *(if time)* | Past that, FSDP splits weights, gradients and optimizer state across GPUs. | A second slab ghosts in beside the first; the m and v bars split between them. One label: `FSDP (more in ep 13)`. |
| 08_close | Next time it crashes, print the peak with max memory allocated, then cut the micro-batch until it fits. | Final visual: the code card with `torch.cuda.reset_peak_memory_stats()` / `train_step()` / `print(torch.cuda.max_memory_allocated() / 1e9)  # GB` and a `memory_summary()` line under it; the slab beside it with a magenta peak tick sitting just under the top. Takeaway only, no outro. |

Line 1 says the search phrase and the answer (the four things) in its
first clause; "out of memory" is said and the error is on screen at
frame 0. Beat 07 is the *(if time)* cut: sharding is ep 13's home, and a
one-GPU viewer won't miss it. Beat 05 stays: it is the contrast that stops
the wrong takeaway ("my model is too big"). Beat 06 is the only "how" beat
and carries the code. The closer is the viewer's next move (measure, then
cut the micro-batch), not line 1 again.

## Facts to keep straight (notes, not VO)

- 16 bytes per parameter is the ZeRO paper's figure for fp16 mixed
  precision with Adam (§3.1, "2Ψ+2Ψ+KΨ=16Ψ bytes"; their example: GPT-2
  1.5B needs at least 24 GB). bf16 is the same 2 bytes. Plain PyTorch
  AMP (`torch.autocast`) keeps fp32 weights and fp32 grads instead (4 +
  4 + 8) and also lands on 16 bytes; the split on screen is the ZeRO one.
- 128 GB is decimal (8e9 × 16 = 1.28e11 bytes) = about 119 GiB. PyTorch's
  error message prints GiB; `max_memory_allocated() / 1e9` prints GB, so
  the code card divides by 1e9 to match the slab.
- "Only activations grow with your batch": true of the four; temporary
  buffers, the CUDA context and allocator fragmentation also take some
  memory (the error's "reserved by PyTorch but unallocated" line is
  fragmentation). Companion material, with
  `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.
- Adam's m and v are allocated lazily at the first `opt.step()`, so an
  8B run that fits the forward and backward can still OOM on step 1.
- Activation checkpointing costs about one extra forward pass per step
  (the 8N vs 6N of ep 8's HFU note); it saves activation memory, not
  model-state memory.
- Gradient accumulation keeps the effective batch, not the step time:
  four micro-batches take about four times as long per optimizer step.
- FSDP (and ZeRO stages 1–3) shards optimizer state, then gradients, then
  weights; ep 13 owns the communication cost.
- `torch.OutOfMemoryError` is the current name (`torch/__init__.py` on
  main: `OutOfMemoryError = torch._C.OutOfMemoryError`);
  `torch.cuda.OutOfMemoryError` is the older alias and still catches it.

### Facts to verify before publish

- The B200's total capacity as PyTorch reports it, in GiB (180 GB is
  about 167.6 GiB; the driver may report a slightly different figure). Until
  checked on a real B200, the error card elides it with `…`.
- That the full error line still reads "GPU 0 has a total capacity of …
  of which … is free" in the PyTorch release viewers will have (read from
  main, 10/27).

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top: the terminal error card (beats 1 and 5), ~1.5 rows.
- Stage middle: the chip at left, smaller than in other episodes; the HBM
  slab at right, drawn tall (~5 rows), with the 0 / 128 / 180 GB ticks.
  The slider sits directly under the slab.
- Stage bottom-middle: the code card (beats 6 and 8).
- One magenta hero at a time: the overflowing activations bar → `16
  bytes` → each byte group → `128 GB` → the activations bar → the peak
  tick.
