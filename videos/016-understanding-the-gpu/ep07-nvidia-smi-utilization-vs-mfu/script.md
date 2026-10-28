# Episode 7: GPU utilization vs MFU

- **Duration:** 75.6 s raw (`vo_raw.m4a`); ~62.3 s with pauses capped at 0.4 s (an estimate, before step 5).
- **Source:** cut from `~/Creating/016-gpu-understanding.m4a` at 363.06–438.71 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, `ep07-nvidia-smi-utilization-vs-mfu`. Reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").
- **Working name only.** Titles are proposed at runbook step 9.

## As recorded

GPU saturation can stay at 100 percent, but that only means your GPU is busy. MFU tells you if it's doing useful work.

~~GPU utilization measures the share of time any kernel was running.~~ A kernel is a single operation the GPU could be doing. GPU utilization is the share of time any kernel was running, not how much of the chip it used. One tiny kernel function can count as 100 percent.

If saturation drops, though, your data loader is likely starving the GPU. But model FLOPs utilization, or MFU, is the FLOPs your model does each second. This is the number of floating-point operations divided by what the chip could actually do. An 8-billion-parameter model at 15,000 tokens a second per GPU does 720 teraflops. A B200 peaks near 2,250, so that's about 32 percent utilization.

Dashboards like on Ray will show you the busy number, GPU utilization, not MFU. You need to log this yourself.

Utilization tells you if the GPU is waiting. MFU tells you if the busy time is useful. So log the tokens per second and watch the MFU.

## Where the take leaves the script

- **nvidia-smi is never said.** Line 1 became "GPU saturation can stay at 100 percent…" and the nvidia-smi beat (what the tool is) is not recorded. The search phrase `nvidia smi` is now not in the VO, so step 0 needs a new phrase or a re-recorded line 1. Rechecked 10/28: "gpu utilization" autocompletes (results lean gaming: "gpu utilization 100", "…low in games"); "gpu saturation", "mfu gpu", "model flops utilization" get nothing useful.
- Kernel is defined inline ("A kernel is a single operation the GPU could be doing"), which settles the open decision about viewers arriving from search.
- **Repeat:** "GPU utilization measures the share of time any kernel was running." then the same sentence again after the kernel definition. Cut the first (take 375.4–380.0 s, here 12.3–16.9 s).
- Not recorded: the *(if time)* PaLM 46 % line.
- Raw 75.6 s, ~62.3 s with pauses capped (a 4.8 s pause after "useful work"), ~57.7 s with the repeat cut. Tight against 60.
