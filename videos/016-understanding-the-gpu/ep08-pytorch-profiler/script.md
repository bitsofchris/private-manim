# Episode 8: PyTorch profiler

- **Duration:** 47.5 s raw (`vo_raw.m4a`); ~43.1 s with pauses capped at 0.4 s (an estimate, before step 5).
- **Source:** cut from `~/Creating/016-gpu-understanding.m4a` at 444.40–491.86 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, `ep08-pytorch-profiler`. Reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").
- **Working name only.** Titles are proposed at runbook step 9.

## As recorded

The PyTorch profiler draws your training step as a timeline, and the gaps are where your GPU sits idle.

Wrap a few steps in torch.profiler. Skip the first couple, so you record real training, not startup. It writes a trace file. The top rows are the CPU; below them, the GPU stream, one block per kernel.

A gap in that row is the GPU doing nothing: waiting on the next batch, on Python launching small kernels, or a sync like loss.item().

Find the biggest gap first. Look at what the CPU is doing right then: what was the GPU waiting for?

Once the gaps are closed, sort the summary table by CUDA time. That's your list of kernels worth making faster.

On Ray Train, the same block goes inside your training function on each worker. Profile a few steps, open the trace, and close the biggest gap before you touch the model.

## Where the take leaves the script

- Not recorded: "open it in Perfetto". The VO says "it writes a trace file" and goes straight to the rows; name Perfetto on screen.
- The *(if time)* Ray Train line is recorded.
- Ear check: "Look at what the CPU is doing right then: what was the GPU waiting for?" Parakeet heard "doing right. Then, what was…" (clip `check_right_then.m4a`).
