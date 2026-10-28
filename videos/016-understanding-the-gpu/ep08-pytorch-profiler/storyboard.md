ENGINE: hyperframes

# Reading a PyTorch profiler trace: storyboard (v1; VO draft for Chris)

THE QUESTION: "How does PyTorch show me where my training step wastes GPU
time?"
WHO IS ASKING: a research engineer whose run looks slow (or whose
GPU-Util isn't pinned), who has heard of `torch.profiler` but has never
opened a trace and doesn't know which row to look at or what a gap means.
THE ANSWER IN ONE SENTENCE: `torch.profiler` records every CPU op and GPU
kernel of a few real steps on one timeline; open the trace in Perfetto,
look at the GPU stream row, and the gaps are the GPU idle (waiting on
data, on Python, or on a sync), so fix the biggest gap first.
THE SEARCH PHRASE: pytorch profiler (checked 10/27 via YouTube's
autocomplete endpoint and results page, not a browser: "pytorch profiler"
autocompletes to itself and to "pytorch profiler tutorial"; both return
on-topic results, "Five Ways To Increase Your Model Performance Using
PyTorch Profiler" and the PyTorch conference talk on the profiler, with
chapter titles "GPU Utilization", "Trace View". "torch profiler" also
autocompletes; "pytorch profiler trace" falls back to the first two.)

**Titles (runbook step 9, Chris picks; both carry the search phrase):** search `PyTorch Profiler Made Simple (Beginner Friendly)` (48 chars) · hook `Your GPU sits idle. Find where (PyTorch profiler)`

**One idea:** the trace is a picture of idle time. Read the gaps, not the
blocks; the biggest gap is the first fix.

**Source note:** Chris's question in the 10/27 session ("How does PyTorch
or Ray show you this properly?") has no answer sentences of his, so this
VO is a draft in his voice for him to rewrite (same as ep 7). Every claim
was checked against the PyTorch docs (2.14 profiler page, the profiler
recipe, the TensorBoard profiler tutorial's deprecation note) and the
PyTorch `main` source; see "Facts to keep straight".

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip, its
time strip unrolled into a two-row trace, and a code card. Nothing needs
Manim.

Series context: ep 8 of `../SERIES.md` (Understanding the GPU). Home of
"reading a profiler trace; idle gaps". Leans on ep 6 (what a kernel is,
one clause here), ep 7 (GPU-Util, not said here), and hands the data-loader
gap to cut ep 10 (named once, not fixed here).

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one **B200** (the series chip, 12 × 12 core grid; no SM count).
- Model: the **8B** dense transformer, bf16, Adam (named nowhere in the
  VO; on screen only as the `train_step(batch)` the loop calls).
- The profile: `schedule(wait=1, warmup=1, active=3, repeat=1)`: step 1
  skipped, step 2 warm-up (traced, discarded), steps 3–5 recorded. The
  trace shows **3 steps**.
- The trace file: `trace.json`, opened in **Perfetto** (`ui.perfetto.dev`);
  `chrome://tracing` reads the same file.
- Rows, top to bottom: `CPU (Python)` (the series CPU box's label), then
  `GPU stream` (one block per kernel).
- The three gap causes, in this order and these words: `waiting on data`,
  `Python launching small kernels`, `sync: loss.item()`.
- The biggest gap is the **data** gap (it is cut ep 10's hand-off); its CPU
  row above shows a `DataLoader __next__` block. No gap carries a
  millisecond figure: the trace is a picture, not a measurement.
- The summary line: `prof.key_averages().table(sort_by="cuda_time_total", row_limit=10)`.
- Code card (≤ 6 lines, real and runnable given `loader` and `train_step`):

```python
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
             schedule=schedule(wait=1, warmup=1, active=3, repeat=1),
             on_trace_ready=lambda p: p.export_chrome_trace("trace.json")) as prof:
    for batch in loader:
        train_step(batch)
        prof.step()
```

  (the import, `from torch.profiler import profile, schedule,
  ProfilerActivity`, goes in the companion, not on the card.)

## VO (draft: 146 words without the if-time beat, 160 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | The PyTorch profiler draws your training step as a timeline, and the gaps are where your GPU sits idle. | Frame 0 already working: the series chip mid-stage, its time strip below it unrolling sideways into a wide trace: CPU row on top (small teal op blocks), GPU stream row below (teal kernel blocks with grey gaps between). On "gaps" every grey gap pulses once. ~7 rows of stage. |
| 02_record | Wrap a few steps in torch dot profiler. Skip the first couple, so you record real training, not startup. | The code card slides up bottom-middle with the ledger's six lines. Highlight walks: `profile(activities=[…CPU, …CUDA]` → `schedule(wait=1, warmup=1, active=3…)`. Above the card, five step tiles: tile 1 grey "skip", tile 2 grey "warm-up", tiles 3–5 teal "record". Magenta hero: `schedule(...)`. |
| 03_open | It writes a trace file; open it in Perfetto. The top rows are the CPU. Below them, the GPU stream: one block per kernel. | The card's `on_trace_ready` line highlights, a `trace.json` tile drops out of it and opens into the full-width trace (3 steps). Row labels draw on: `CPU (Python)`, `GPU stream`. Small gloss under the trace: "Perfetto: ui.perfetto.dev". On "one block per kernel" a thin flow line joins one CPU launch to its GPU block (ep 6's queue, one clause). |
| 04_gaps | A gap in that row is the GPU doing nothing, waiting on the next batch, on Python launching small kernels, or on a sync like loss dot item. | Camera stays on the trace. Three gaps get labels in turn, each label under its gap in grey: `waiting on data`, `Python launching small kernels` (a run of thin slivers with hairline gaps), `sync: loss.item()` (the CPU row above shows a `cudaStreamSynchronize` bar). |
| 05_biggest | Find the biggest gap first. Look at what the CPU was doing right then; that's what the GPU was waiting for. | The widest gap (the data gap) takes the magenta hero; the other labels dim. A vertical guide rises from the gap to the CPU row, landing on a `DataLoader __next__` block. Small tag at the gap's edge: "→ cut ep 10". |
| 06_table | Once the gaps are closed, sort the summary table by CUDA time. That's your list of kernels worth making faster. | The gaps close (blocks slide together). The code card swaps to one line, `prof.key_averages().table(sort_by="cuda_time_total")`, and a 4-row table prints under it: kernel name / CUDA total, top row a matmul (`…gemm…`), then `aten::copy_`, an elementwise op, a softmax. Names only, times shown as bars, no figures. Magenta hero: the top row. |
| 07_ray *(if time)* | On Ray Train, the same block goes inside your training function, on each worker. | A box labeled `train_func (each Ray worker)` wraps the code card; two small copies of the trace stack under it, one per worker. |
| 08_close | Profile a few steps, open the trace, and close the biggest gap before you touch the model. | Final visual: the trace, gaps closed, GPU row solid teal, with the magenta marker on where the biggest gap was. Takeaway only, no outro. |

Line 1 says the search phrase and the answer ("the gaps are where your
GPU sits idle") in one clause; the trace is on screen from frame 0.
Beat 07 is the *(if time)* cut: it answers the Ray half of Chris's
question, which the viewer from search won't miss. Beat 04 stays: the
three causes are what makes a gap readable. Beat 06 stays: it is the
contrast that stops the wrong takeaway ("the profiler is only for gaps")
and the second code line. Beat 05 is the only "how to read it" beat and
stays. The data loader gets one clause (beat 04) and a tag (beat 05);
the fixes are cut ep 10's. GPU-Util is not said (ep 7); "kernel" gets one
clause (beat 03, ep 6).

## Facts to keep straight (notes, not VO)

- **Sort key.** The docs' examples use `sort_by="cuda_time_total"` /
  `"self_cuda_time_total"` (2.14 profiler page, the profiler recipe). In
  current PyTorch `main`, `_build_table` rewrites `cuda` → `device` in the
  sort key, so `"cuda_time_total"` sorts by `device_time_total`; the
  *attribute* `evt.cuda_time_total` is `@deprecated` in favor of
  `device_time_total`, the *string* is not. On screen: `"cuda_time_total"`
  (the documented spelling; works on old and new versions). `"device_time_total"` also works on current versions but not older ones.
- **`cuda_time_total` vs `self_cuda_time_total`:** total includes child
  ops; "self" excludes them. For "which kernels take the time" the self
  column avoids double counting nested ops; the VO says "sort by CUDA
  time" and doesn't pick. Companion: show both.
- **schedule:** signature `schedule(*, wait, warmup, active, repeat=0,
  skip_first=0, skip_first_wait=0)`. Warm-up steps are traced but
  discarded. `repeat=0` means cycles repeat until profiling ends (and
  `on_trace_ready` fires every cycle, overwriting `trace.json`), so the card
  sets `repeat=1`. `prof.step()` must be called each step or the schedule
  never advances.
- **export_chrome_trace:** "Exports the collected trace in Chrome JSON
  format. If kineto is enabled, only last cycle in schedule is exported."
- **Viewers in 2026:** the PyTorch TensorBoard profiler tutorial now opens
  with "The TensorBoard integration with the PyTorch profiler is now
  deprecated. Instead, use Perfetto or the Chrome trace to view
  `trace.json` files"; it names HTA (Holistic Trace Analysis) as the
  analysis replacement. `tensorboard_trace_handler` itself is not
  deprecated in the API, but the card avoids it so the viewer isn't sent
  to TensorBoard. HTA's idle-time breakdown is companion material.
- **"Top rows are the CPU":** true of a PyTorch trace in Perfetto/Chrome
  (the Python process's threads, then the GPU process's stream rows);
  exact ordering can vary by viewer. Our drawing fixes the order.
- **"Look at what the CPU was doing right then":** the narrow, true version
  is: the CPU row during a GPU gap shows what the host was doing instead of
  enqueueing work (a `DataLoader __next__`, a run of tiny ops and
  `cudaLaunchKernel` calls, or a `cudaStreamSynchronize` from `.item()`).
  Kernel launches are async (ep 6), so the CPU row sits *ahead* of the GPU
  row; the guide in beat 05 points at the CPU just before the gap's end,
  where the next launch came from.
- **`loss.item()`** copies a scalar to the host and blocks until the GPU
  finishes; in the trace it appears as `aten::item` / `aten::_local_scalar_dense`
  with a sync under it. Its full story is ep 6.
- **Ray:** Ray's docs say the PyTorch profiler "is supported out of box"
  with Ray Train and have a tutorial ("Profiling a Ray Train Workload with
  PyTorch Profiler"): the same `with profile(...)` block goes in the
  per-worker training function, one trace per worker. The open-source Ray
  Dashboard's own profiling is CPU-side (flame graphs, stacks) and off by
  default; the on-demand GPU trace button is Anyscale's (managed) Train
  dashboard, not open-source Ray. The VO claims only the first.
- **Fix the gap before the model:** fixing kernels speeds up the busy
  blocks; an idle gap costs the same whatever the kernels do. Kept as the
  closer's ordering, not stated as a number.
- Gap causes not in the VO: CPU-side work (logging, Python bookkeeping),
  host-to-device copies without `pin_memory`, NCCL waits on multi-GPU
  (cut ep 13). Companion.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top: the chip, small (beat 01 only), shrinking up and out as its
  time strip becomes the trace.
- Stage middle: the trace, full stage width, 2 rows (`CPU (Python)` over
  `GPU stream`), ~3 rows of stage including labels and gap tags; 3 steps
  wide, step boundaries as faint ticks.
- Stage bottom-middle: the code card (beats 02, 03, 06), monospace at the
  code-card token size; the 6-line block's longest line is ~80 characters,
  so the card spans the safe width and the beat highlights one line at a
  time. If it won't read at phone size, the beat agent reports it rather
  than shortening the code (the orchestrator decides).
- Step tiles (beat 02) sit between trace and card, one row.
- One magenta hero at a time: `schedule(...)` → the biggest gap → the top
  table row → the closed-gap marker.
