# Episode 1: why GPUs for AI

- **Duration:** 49.5 s raw (`vo_raw.m4a`); ~44.4 s with pauses capped at 0.4 s (an estimate, before step 5).
- **Source:** cut from `~/Creating/016-gpu-understanding.m4a` at 0.00–49.45 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, `ep01-why-gpus-for-ai`. Reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").
- **Working name only.** Titles are proposed at runbook step 9.

## As recorded

A neural network is mostly multiplication and addition. GPUs allow these to all happen at the same time.

So if you take one layer, y equals x times W, each output is its own row times column. None of them waits on the other. GPUs allow this to run in parallel.

Now, a CPU is built to run one thread as fast as possible. A few big cores, some big caches, some smart branching. It works through that pile a few at a time.

A GPU trades per-core speed for count. This grid is the chip: thousands of small cores, all working at once.

Newer GPUs add tensor cores, which do a small matrix multiply in one step.

In PyTorch, that's one line. Move x and W to CUDA, and the same at sign runs the whole grid.

## Where the take leaves the script

- Line 1 is new: "A neural network is mostly multiplication and addition. GPUs allow these to all happen at the same time." Still the answer, not a question.
- Added "GPUs allow this to run in parallel." after the row-times-column line. It repeats line 1's point: cut candidate (say each thing once).
- Not recorded: the BERT "over 99 percent of the arithmetic" line, and the closer ("Try it: time one big matmul on the CPU, then on cuda..."). The take ends on "runs the whole grid", so there is no next move for the viewer. Put it on screen (the code card) or accept it.
- The *(if time)* tensor-core line is recorded (take 37.1–42.0 s).
