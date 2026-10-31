ENGINE: hyperframes

# Multithreading vs multiprocessing in Python (series ep 2 of 2): storyboard (v4, on kit v2: the same two views as ep 1)

THE QUESTION: "Multithreading vs multiprocessing in Python: which one do I use, and what does a process cost me?"
WHO IS ASKING: a Python engineer who now knows the GIL exists (ep 1) and
has a real job to speed up.
THE ANSWER IN ONE SENTENCE: threads for work that waits, processes for
work that runs Python; everything that crosses between processes is
copied, so big data goes in shared memory.
THE SEARCH PHRASE: multithreading vs multiprocessing python (checked
10/25; first autocomplete; "…vs asyncio python" and "…interview questions"
also offered, so name asyncio in the description).

**Titles (runbook step 9, Chris picks):** search `Multithreading vs Multiprocessing Python (Made Simple)` · hook `Most Python devs get this wrong (multithreading vs multiprocessing python)` (Chris's preference, 10/26).

**One idea:** a process gives you a second knife, but everything that crosses between processes gets copied. That copy is what people get wrong.

**Rule for this script (Chris, 10/27):** same as ep 1, every kitchen beat
lands on the real term in the same breath; labels show both names.

**Engine:** HyperFrames on kit v2 (`../_kit/kitchen.js`): ep 1's kitchen
and Python panel, plus a 2×2 grid of half-size kitchens, a wall with a
pipe, a bowl that gets boxed through it, a fridge slab, and the panel as
processes. v3 (the kit v1 build) is `storyboard_v3.md`.

Split with ep 1: ep 1 owns the one kitchen and the waiting-vs-running
diagnostic. This episode recaps that in one line and spends its words on
processes, the pickling cost, and shared memory.

## What changed (v4, 2026-10-31)

- **Same grammar as ep 1.** Kitchen above, Python panel below, a thing
  lands on its word, every label shows both names, one magenta hero.
- **Frame 0 is ep 1's last frame.** Two kitchens, the panel split into
  `process 1` / `process 2`; the two lines land on "threads" and
  "processes". The recap grows the first kitchen back to full size.
- **Processes are a grid.** On "builds more kitchens" the kitchen shrinks
  and three more draw in (one cook each); on "its own GIL" a knife lands
  in each; on "in parallel" four magenta bars grow together under
  `multiprocessing.Pool(4)`; `num_workers=4` on "workers".
- **The cost is a wall, a pipe, a bowl and a grey bar.** The bowl from
  kitchen 1 is boxed, pushed through the pipe, unboxed in kitchen 2; the
  panel title names `pickle.dumps` / `pickle.loads`; Process 1's row grows
  a grey copy bar longer than its magenta compute bar.
- **The fridge is the bottom row.** Kitchens 3–4 give way to a fridge
  slab; the bowl goes in once on shelf 3 (its number lights magenta); only
  the note "shelf 3" crosses the pipe; the copy bar shrinks to a sliver
  under `SharedMemory(name)`.
- **The close replaces the panel** with three lines: waiting → threads,
  running Python → processes, big data → shared memory.

## Beats (`vo_final.wav` 58.54 s, cuts unchanged from v3; cues from `captions.json`)

| # | Folder | Start | Length | VO | Visual, on its word |
|---|---|---:|---:|---|---|
| 1 | `01_hook` | 0.000 | 6.160 | In Python, you use threads when you're stuck waiting for I/O, or processes when you have more CPU work in Python to do. | Frame 0 = ep 1's end (SEAM2[0]): kitchen 1 half size with its four cooks (cook 2 chopping), kitchen 2 with its cook chopping, panel split `process 1` / `process 2`. "threads" 1.04: "waiting → threads" lands in the gap, the dashed bar pulses; "processes" 3.36: "running Python → processes" lands, both magenta bars pulse. Chop throughout, still from 5.8. |
| 2 | `02_recap` | 6.160 | 7.890 | The part people often miss is what an additional process actually costs. Think of a process as a full kitchen. Threads are its cooks, the GIL is one knife. | "costs" 8.58: a magenta price tag hangs on kitchen 2's corner (hero); the close lines fade. "full kitchen" 10.66: the tag and kitchen 2 fade, the panel unsplits to `$ python main.py` with Thread lanes, kitchen 1 grows back to full size (0.6 s). "cooks" 12.14: cooks 2–4 walk to the counter and fold (one holder), slot "cooks / threads"; "one knife" 13.02: the knife lands with cook 1 (hero), slot "knife / GIL", Thread 1 bar 0–0.3. Still from 13.75. |
| 3 | `03_processes` | 14.050 | 10.470 | Multiprocessing builds more kitchens. Each process has its own interpreter and its own GIL, so Python actually runs in parallel. PyTorch's data loader workers are new processes. | "Multiprocessing" 14.46: title → `multiprocessing.Pool(4)`, lanes → `Process 1–4`. "more kitchens" 15.22: kitchen 1 shrinks to the grid's top-left (0.5 s); kitchens 2, 3, 4 draw in at 15.6 / 15.95 / 16.3 (0.3 s each), each with one cook walking in and a carrot; slot "kitchens / processes". "its own GIL" 18.44: a knife lands in each kitchen (four magenta knives, the hero group), slot "own knife / own GIL". "in parallel" 20.74: all four cooks chop, four magenta bars grow 0 → 0.5 together to the hold. "workers" 22.48: title → `num_workers=4`; slot back to "kitchens / processes". Still from 24.2. |
| 4 | `04_cost` | 24.520 | 13.840 | But the cost is that kitchens don't actually share counter space. Similarly, processes don't share memory. Every result crossing between processes needs to be pickled, pushed through a pipe, and then unpickled again. For a big array, that copy can cost more than the compute. | "cost" 24.78: chopping stops, knives go ink, kitchens 3–4 dim to 0.3, bars stop at 0.3, title back to `multiprocessing.Pool(4)`. "counter space" 27.32: the wall draws down between kitchens 1 and 2; "memory" 29.98: slot "wall / separate memory". "Every result" 31.18: a bowl appears on kitchen 1's counter. "pickled" 33.16: the bowl becomes a crate (0.3 s), title `pickle.dumps(arr)`, slot "through the pipe / pickled"; "pipe" 34.14: the pipe appears and the crate moves through it (34.14 → 34.6); "unpickled" 34.6: the crate becomes a bowl on kitchen 2's counter, title `pickle.loads(buf)`. Process 1's grey copy bar grows 0.3 → 0.9 from "pickled" to "compute" 37.68, past the magenta bar's length. Still from 38.0. |
| 5 | `05_fridge` | 38.360 | 9.490 | The fix here is a shared fridge or shared memory. You put the big tensor in once and pass a note that says shelf 3. The pipe carries the note, not the actual food. | "fridge" 39.78: kitchens 3–4 fade, the fridge slab draws across the bottom row with shelves 1–3; "shared memory" 40.36: slot "fridge / shared memory". "once" 42.52: the bowl drops from kitchen 2 (back at kitchen 1 first, 41.43 "put") into the fridge onto shelf 3, the "3" lights magenta; the copy bar shrinks to 0.3–0.36 and the title → `SharedMemory(name)`. "shelf 3" 43.67: the note "shelf 3" (hero) appears on kitchen 1's counter; "pipe" 44.82: the note goes through the pipe (0.45 s) to kitchen 2; "not the actual food" 45.76: slot "a note / not the data", the bowl in the fridge pulses. Still from 47.5. |
| 6 | `06_close` | 47.850 | 10.694 | Think if you're waiting on I/O, use threads. If you're blocked by Python or CPU intensive work, use more processes. And if you have big data between processes, be sure to use shared memory. | "Think" 48.14: the panel fades, the slot fades, the note dims to 0.5, knives magenta again and both cooks chop. "threads" 49.74: "waiting → threads" lands where the panel was; "processes" 53.16: "running Python → processes"; "shared memory" 57.4: "big data → shared memory". Chop stops at 57.4; still to the end. |

## Seam states (`SC.SEAM2[n]` in `../_kit/kitchen.js`; `00_layout/proto.png` tiles 1, 2, 5, 8, 11, 13, 14)

| cut | on screen (both sides draw `SC.SEAM2[n]`, chop 0) |
|---|---|
| 0 (frame 0) | ep 1's last frame without its lines and slot: kitchen 1 half size (cook 2 holds the knife, carrot done), kitchen 2 (cook 1 holds the knife), panel split `process 1` / `process 2` with ep 1's close rows |
| 1→2 | + "waiting → threads", "running Python → processes" in the gap |
| 2→3 | kitchen 1 full size, four cooks at the counter, cook 1 holds the knife (hero), oven and appliance in place; slot "knife / GIL"; `$ python main.py`, Thread lanes, Thread 1 bar 0–0.3 |
| 3→4 | the 2×2 grid, one cook with a magenta knife in each kitchen (kitchen 1 keeps its four, three folded), every carrot half cut; slot "kitchens / processes"; `num_workers=4`, Process 1–4 bars 0–0.5 |
| 4→5 | knives ink; kitchens 3–4 at 0.3; wall and pipe between kitchens 1 and 2; the bowl on kitchen 2's counter; slot "through the pipe / pickled"; `pickle.loads(buf)`, Process 1 magenta 0–0.3 + grey 0.3–0.9, Processes 2–4 magenta 0–0.3 |
| 5→6 | kitchens 3–4 gone, the fridge with the bowl on shelf 3 ("3" magenta); the note "shelf 3" (hero) on kitchen 2's counter; slot "fridge / shared memory"; `SharedMemory(name)`, Process 1 grey bar 0.3–0.36 |
| end | panel gone; the three close lines in its place; knives magenta, note at 0.5; the grid, wall, pipe and fridge stay |
