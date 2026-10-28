# Episode 6: CUDA kernel, one training step

- **Duration:** 59.6 s raw (`vo_raw.m4a`); ~46.5 s with pauses capped at 0.4 s (an estimate, before step 5).
- **Source:** cut from `~/Creating/016-gpu-understanding.m4a` at 294.47–354.12 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, `ep06-cuda-kernel-training-step`. Reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").
- **Working name only.** Titles are proposed at runbook step 9.

## As recorded

Every op in your PyTorch training step becomes CUDA kernels: functions your CPU hands the GPU to run.

Now, we call these kernels because they don't run just once. They run thousands of threads, each on its own slice of the data, in blocks across the GPU chip.

It returns nothing. It writes to GPU memory, and the CPU doesn't wait. It drops the launch in a queue and moves on.

Watch one step. ~~Forward queues a kernel or more per op.~~ Forward queues up a kernel or more per op: matmul, add, ReLU. Backward then queues more. So does the optimizer. The CPU runs ahead while the GPU drains the queue.

Then loss.item(). The CPU needs a number, so it waits until the queue is empty. And if the next batch isn't ready, the queue runs dry and the GPU sits idle.

Call item only on the steps you log. The CPU stays ahead and the queue stays full.

## Where the take leaves the script

- "Why not just say function?" became "Now, we call these kernels because they don't run just once." That states why they're called kernels, a claim this series could not source (SERIES.md: the name's origin is unsourced). Keep the visual to what a kernel does (many threads, one function), not the etymology.
- **Repeat:** "Forward queues a kernel or more per op." then the full "Forward queues up a kernel or more per op: matmul, add, ReLU." Cut the first (take 321.0–324.6 s, here 26.5–30.1 s).
- The *(if time)* "Not the Linux kernel" line is not recorded.
- Ear check: "training step" — both recognizers heard "training set" (clip `check_step.m4a`). If it was "set", Chris decides whether the caption says "step".
