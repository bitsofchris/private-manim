ENGINE: hyperframes

# Why your GPU sits idle: the data loader: storyboard (v1, VO draft for Chris)

THE QUESTION: "Why is my GPU utilization low during training?"
WHO IS ASKING: a research engineer whose PyTorch run shows GPU-Util
bouncing well under 100 % in nvidia-smi (or the Ray dashboard), who
suspects the model or the GPU and hasn't looked at the DataLoader
arguments since they copied them from a tutorial.
THE ANSWER IN ONE SENTENCE: the GPU finishes each step before one Python
process can load the next batch, so it sits idle between steps; give the
DataLoader worker processes (`num_workers`), pinned memory
(`pin_memory=True` plus `non_blocking=True`), and check it by timing the
loader alone.
THE SEARCH PHRASE: pytorch dataloader num_workers (checked 10/27 via
YouTube's autocomplete endpoint and results page, not a browser: it
autocompletes verbatim, and "pytorch num workers", "pytorch dataloader
slow", "pytorch dataloader speed" and "pytorch dataloader performance"
all autocomplete to it. Results are ML, including deeplizard's "PyTorch
DataLoader num_workers - Deep Learning Speed Limit Increase", the same
angle as this Short. "gpu utilization low" and "why is my gpu utilization
so low" autocomplete but every result is a gaming fix. "gpu utilization
pytorch" gets no autocomplete but its results are on topic (Technion's
"Maximizing CPU and GPU Utilization in PyTorch"), so it goes in the title
as the second phrase. **Collision:** 014 ep 5 (duplicate batches) also
claims this phrase; see the notes under the VO.)

**Titles (runbook step 9, Chris picks):** search `PyTorch DataLoader num_workers: Why GPU Utilization Is Low` · hook `Your GPU isn't slow. It's waiting on your data loader.`

**One idea:** low utilization is a waiting problem, not a speed problem;
the GPU waits on the loader, and the fix is in the DataLoader call.

**Source note:** Chris's dataloading take (`../../014-pytorch-dataloading/TRANSCRIPT.md`)
explains what the loader is, never why the GPU waits on it, so this VO is
a draft in Chris's voice for him to rewrite (same as ep 8). One fragment
is his, cut not reworded: beat 04's "workers that you can spin out in
parallel" (08:01.7, "So it has these workers that you can span out in
parallel"; "span" is Parakeet mishearing "spin", check the audio). His
title phrase from the series note: "GPU saturation".

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip,
a loader box, the time strip and a code card. Nothing needs Manim.

Series context: ep 10 of `../SERIES.md` (Understanding the GPU). Kernel
queue (ep 6), GPU-Util (ep 7) and the profiler (ep 9) get one clause each
at most. The dataloader machinery itself (Dataset vs DataLoader, the four
stations, workers as dataset copies) is 014's; this Short starts where 014
stops: what the loader's speed does to the GPU.

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one **B200** (the series chip). No B200 number is spoken or shown
  in this Short; the gaps are a picture, not a measurement.
- The chip: 12 × 12 grid of core cells, teal when working, dark at rest.
- The time strip: a row of slots under the chip, teal when any kernel
  ran, grey when idle (ep 7's strip, same drawing).
- The loader box: left of the chip, label `DataLoader`, batches as small
  teal tiles riding a conveyor into the chip (the series image, ep 10's
  added part).
- The CPU box top-left, label `CPU (Python)`, with its kernel queue (ep 6's
  drawing), shown, not explained.
- DataLoader defaults (PyTorch 2.14 docs, `torch.utils.data`):
  `num_workers=0` ("the data will be loaded in the main process"),
  `pin_memory=False`, `prefetch_factor` 2 when `num_workers > 0`,
  `persistent_workers=False`.
- Code-card values are examples, not recommendations: `batch_size=32`
  (014's notebook), `num_workers=8`, `prefetch_factor=4`. No beat claims
  "8 is right"; the right count is whatever closes the gaps.

## VO (draft: 145 words without the if-time beat, 160 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | If your GPU utilization is low, your GPU isn't slow. It's waiting on your data loader. | Frame 0 already working: the chip mid-stage, the time strip under it with grey gaps between teal runs, the loader box at left with one batch tile crawling along its conveyor. The grey gaps are the magenta hero (outlined magenta). ~7 rows of stage. |
| 02_gap | It can finish a training step before one Python process has read, decoded and batched the next. Then it sits idle until the batch shows up. | A step plays: the batch enters, the grid lights teal, the strip fills one teal run. The grid goes dark; inside the loader box a single worker tile works through three labeled stages (`read` → `decode` → `batch`) while the strip ticks grey slots. Batch arrives, grid lights. Magenta hero: the growing grey run. |
| 03_main | By default, num_workers is zero: batches load in your main process, the same one that queues the GPU's work. | The loader box slides up into the `CPU (Python)` box (same process, one box now). The kernel queue running into the chip is empty while the box shows `loading…`. Small code chip under the box: `num_workers=0  # default`. Magenta hero: `0`. |
| 04_workers | The data loader has workers that you can spin out in parallel. Set num_workers, and that many processes prepare batches while the GPU trains. | The code card types in, bottom-middle (the code beat, real lines): `loader = DataLoader(ds, batch_size=32, shuffle=True,` / `num_workers=8, pin_memory=True,` / `prefetch_factor=4, persistent_workers=True)`. On "num_workers" that argument lights and the loader box splits back out of the CPU box into 8 stacked worker tiles, each preparing a batch. Magenta hero: `num_workers=8`, then the worker stack. |
| 05_pinned | Turn on pin_memory, and the copy to the GPU gets faster. Add non_blocking, and Python keeps queueing work while it copies. | `pin_memory=True` lights on the card; a slab labeled `pinned RAM` appears between loader and chip, the batch tile hops loader → slab → chip faster than before. Second card line types: `for x, y in loader:` / `x = x.to("cuda", non_blocking=True)`. On "keeps queueing" the CPU box's kernel queue keeps filling while the tile crosses. Magenta hero: `non_blocking=True`. |
| 06_closed | Now the next batch is waiting when the step ends, and the gaps close. | The time strip: grey slots turn teal one by one as batches arrive on time; batches queue at the chip's edge. The magenta outline leaves the (now gone) gaps and rests; the strip is solid teal. |
| 07_prefetch *(if time)* | prefetch_factor sets how many batches each worker keeps ready. persistent_workers keeps them alive between epochs. | `prefetch_factor=4` lights: each worker tile shows a stack of 4 ready batches. `persistent_workers=True` lights: an `epoch 2` marker passes on the strip and the workers stay (with it off, ghosted, they'd blink out and restart). |
| 08_close | Before you touch the model, loop over the loader alone and time it. If a batch takes longer than a step, fix the loader first. | The chip dims to rest; the code card swaps to the timing loop: `t = time.perf_counter()` / `for i, (x, y) in enumerate(loader):` / `    if i == 100: break` / `print((time.perf_counter() - t) / 100)  # s per batch`. Beside it two bars: `loader: s/batch` vs `step: s/step`, loader bar in magenta. Takeaway only, no outro. |

Line 1 answers in its first clause and carries the search idea ("GPU
utilization low"); "data loader" is said and on screen by ~4 s, and
`num_workers` is said by ~14 s. Beat 07 is the *(if time)* cut: both
arguments stay on the code card either way, so a viewer who pauses still
sees them. Beat 03 stays: it is the "why", and without it beat 04's fix is
a magic number. Beat 05 stays: `non_blocking=True` is the code line the
brief asked for and the one most tutorials leave out.

The VO never says what a kernel or the queue is (ep 6), what GPU-Util
measures (ep 7), or how to see the gaps in a trace (ep 9). The closer
tells the viewer to time the loader, not to profile; a profiler mention
would be the one clause allowed, and it was cut for length.

**Search-phrase collision with 014 ep 5.** 014 ep 5 ("why you get duplicate
batches") also uses `pytorch dataloader num_workers`. The two answer
different questions under the same phrase (speed here, correctness there).
Options for Chris: keep both (two Shorts for one phrase, each title
says its own question), or retitle this one around `gpu utilization
pytorch` (on-topic results, no autocomplete). Recommendation: keep both;
the titles split cleanly ("Why GPU Utilization Is Low" vs "Why You Get
Duplicate Batches") and each can link the other.

## Facts to keep straight (notes, not VO)

- `num_workers=0` (the default): "the data will be loaded in the main
  process" (PyTorch 2.14 `torch.utils.data` docs), which is also the
  process issuing the CUDA launches, so while `next(loader)` runs nothing
  new is queued. With `num_workers > 0`, loading runs in that many
  subprocesses.
- More workers only help when the loader is the bottleneck, and each
  worker is a process with its own copy of the dataset object (014 ep 5)
  and its own RAM. Past the point where the gaps close, more workers do
  nothing or hurt (RAM, CPU contention, shared-memory limits in
  containers). Hence "set num_workers", never a number in the VO.
- `pin_memory=True`: "the data loader will copy Tensors into device/CUDA
  pinned memory before returning them" (docs). CUDA semantics notes: "Host
  to GPU copies are much faster when they originate from pinned
  (page-locked) memory." The pinning itself runs in the loader's pin-memory
  thread, off the training loop's path. Pinning too much RAM can starve
  the host (same notes, "Use pinned memory buffers").
- `non_blocking=True`: the copy returns to Python immediately when the
  source is pinned, so the CPU keeps launching work. The VO claims only
  that ("Python keeps queueing work"), not that the copy overlaps the
  GPU's compute: on the default stream the copy still runs in order after
  the kernels before it. True copy/compute overlap needs a second CUDA
  stream (companion material). From pageable (unpinned) memory,
  `non_blocking` gives little; that is why the two go together.
- `prefetch_factor`: "Number of batches loaded in advance by each
  worker"; default 2 when `num_workers > 0`, must be unset (None) when
  `num_workers=0`. So in-flight batches = `num_workers × prefetch_factor`.
- `persistent_workers=True`: "the data loader will not shut down the
  worker processes after a dataset has been consumed once" (docs). Without
  it, workers are torn down and respawned every epoch.
- Timing the loader alone: the first batch includes worker startup, so
  for a clean number skip it (or time batches 10–110). Compare against a
  step timed on a batch already on the GPU, with `torch.cuda.synchronize()`
  before reading the clock (ep 6's async point). The on-screen loop is
  the short version; the companion gives the careful one.
- Other causes of low utilization exist (CPU-bound Python between steps,
  `.item()` syncs, small kernels, multi-GPU communication). The VO says
  "If your GPU utilization is low ... it's waiting on your data loader",
  which is the common case in the asker's situation, not the only one; the
  closer's test is what tells them whether it's their case. If Chris wants
  it narrower, "the first place to look is your data loader".
- Verified against docs.pytorch.org/docs/2.14/data.html (DataLoader
  signature and parameters) and docs/2.14/notes/cuda.html ("Use pinned
  memory buffers"), 10/27.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top-left: the `CPU (Python)` box with its kernel queue (small).
- Stage middle: the loader box at left, the chip (12 × 12 grid) center,
  conveyor from loader to chip; the pinned-RAM slab appears between them
  in beat 05. The time strip directly under the chip, full stage width.
- Stage bottom-middle: the code card (beat 03's chip, beats 04–08), up to
  4 lines, monospaced, the argument being said lit.
- One magenta hero at a time: the grey gaps → `num_workers=0` → `num_workers=8`
  / the worker stack → `non_blocking=True` → (rest, solid strip) → the
  loader timing bar.
