# Episode 5: tensor cores vs memory

- **Duration:** 54.3 s raw (`vo_raw.m4a`); ~47.0 s with pauses capped at 0.4 s (an estimate, before step 5).
- **Source:** cut from `~/Creating/016-gpu-understanding.m4a` at 236.07–290.40 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, `ep05-tensor-cores-vs-memory`. Reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").
- **Working name only.** Titles are proposed at runbook step 9.

## As recorded

Tensor cores are the part of a GPU that does matrix math. They're only as fast as memory can feed them.

Your data lives in GPU memory. Before any math happens, it flows through cache into the cores.

A B200's tensor cores do about 2,250 teraflops. Memory delivers about 8 terabytes a second. So each byte you load needs about 280 FLOPs done on it, or the cores will sit waiting.

A matrix multiply can clear that easily. Each number it loads gets used in thousands of multiply-adds. It's compute-bound.

ReLU does one operation per number, four bytes moved, and never touches the tensor cores. That's over a thousand times short. It's memory-bound.

Add, dropout, layer norm, and it's a similar story. A few operations per number.

When a step is slow, look at the small operations between the matmuls. That's your GPU waiting on memory.

## Where the take leaves the script

- Not recorded: "HBM", "That's arithmetic intensity", and "fusing them is the fix" at the close. The closer still gives a next move (look at the small ops between the matmuls).
- The *(if time)* "Add, dropout, layer norm" line is recorded.
- Tight boundary: "Episode six" follows "memory." with ~70 ms of gap; the cut is at take 290.40 s and the re-transcription ends cleanly on "memory." Listen to the last word once.
