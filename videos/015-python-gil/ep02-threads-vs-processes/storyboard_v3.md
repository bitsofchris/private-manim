ENGINE: hyperframes

# Multithreading vs multiprocessing in Python (series ep 2 of 2): storyboard (v3, the cost of a process, VO draft for Chris)

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

**Engine:** HyperFrames, the same kitchen, cooks and knife as ep 1 plus the
row of kitchens, the wall with the pipe, and the fridge (`../SERIES.md`).

Split with ep 1: ep 1 owns the one kitchen and the waiting-vs-running
diagnostic. This episode recaps that in one line and spends its words on
processes, the pickling cost, and shared memory.

## VO (draft: 152 words without the if-time beat, 166 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Threads for waiting, processes for Python work. That's the rule for multithreading versus multiprocessing in Python. The part people get wrong is what a process costs. | Frame 0: left, one kitchen with four cooks and the magenta knife ("waiting → threads"); right, a row of four kitchens ("Python work → processes"); a price tag hangs on the row. |
| 02_recap | A process is a kitchen, threads are its cooks, the GIL is the one knife. Threads overlap only while a cook waits on the oven: I/O. | The single kitchen enlarged with the ep 1 labels ("kitchen / process", "cooks / threads", "knife / GIL", "oven / I/O"); cook 2 sets the knife down at the oven, the token jumps to cook 3. One beat, fast. |
| 03_processes | Multiprocessing builds more kitchens. Each process has its own interpreter and its own GIL, so Python really runs in parallel. PyTorch's DataLoader workers are processes. | The row of kitchens, eight small ones, each with a cook and its own knife, all chopping; label "kitchens / processes, one GIL each"; a code card bottom-middle: `DataLoader(ds, num_workers=8)`. Hero passes to the row of knives as one group. |
| 04_cost | The price: kitchens don't share counters, processes don't share memory. Every result crossing between them is pickled, pushed through a pipe, unpickled. For a big array, that copy can cost more than the compute. | A thick wall between two kitchens, label "wall / separate memory"; a large bowl is boxed ("pickle"), squeezed through a pipe, unboxed; the timer bar under the row stalls while it travels. |
| 05_fridge | The fix is a shared fridge: shared memory. Put the big tensor in once, and pass a note that says shelf 3. The pipe carries the note, not the food. | A fridge slab under the row, label "fridge / shared memory"; the bowl goes in once; across the wall goes only a small note ("shelf 3"); the timer bar resumes. Hero: the note. (Evidence beat: Zephon's process runner, `../SERIES.md`.) |
| 06_asyncio *(if time)* | All waiting and nothing else? asyncio: one cook, one event loop, no knife fights. | One kitchen, one cook, a loop arrow over the oven, label "one cook / event loop"; the other cooks gone. |
| 07_close | Waiting, threads. Python work, processes. Big data between processes, shared memory. | Final visual: kitchen, row of kitchens, fridge, each with its pair of labels. Takeaway only, no outro. |
Line 1 lands the rule in its first clause and says the search phrase; its
third sentence names the stake (the cost) that ep 1 did not cover.
Beat 06 is the *(if time)* cut; 04 and 05 are the "how", they stay.

## Layout

- Stage top-middle: the kitchen (beat 2) / the row of kitchens (3–5),
  ~5 rows. Every label is `kitchen thing / real thing`.
- Stage bottom-middle: the fridge, the timer bar, the code card in beat 3.
- One magenta hero at a time: the knife, then the row of knives as one
  group, then the note ("shelf 3") in beat 5.

## Final beats (the contract; `vo_final.wav` 58.54 s, master seconds; from `tools/beat_cuts.py`)

Captions are anchored bottom (`assemble.py --captions-anchor bottom`), so the stage runs to y 1330. Cut list: `script.md` (two phrase cuts + atempo 1.03, for Chris to approve).

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.000 | 6.160 | In Python, you use threads when you're stuck waiting for I/O, or processes when you have more CPU work in Python to do. |
| 2 | `02_recap` | 6.160 | 7.890 | The part people often miss is what an additional process actually costs. Think of a process as a full kitchen. Threads are its cooks, the GIL is one knife. |
| 3 | `03_processes` | 14.050 | 10.470 | Multiprocessing builds more kitchens. Each process has its own interpreter and its own GIL, so Python actually runs in parallel. PyTorch's data loader workers are new processes. |
| 4 | `04_cost` | 24.520 | 13.840 | But the cost is that kitchens don't actually share counter space. Similarly, processes don't share memory. Every result crossing between processes needs to be pickled, pushed through a pipe, and then unpickled again. For a big array, that copy can cost more than the compute. |
| 5 | `05_fridge` | 38.360 | 9.490 | The fix here is a shared fridge or shared memory. You put the big tensor in once and pass a note that says shelf 3. The pipe carries the note, not the actual food. |
| 6 | `06_close` | 47.850 | 10.694 | Think if you're waiting on I/O, use threads. If you're blocked by Python or CPU intensive work, use more processes. And if you have big data between processes, be sure to use shared memory. |

## Seam states (`SC.SEAM2[n]` in `../_kit/kitchen.js`; `00_layout/layout.png` shows them, state n at n–n+1 s)

| cut | what is on screen (both sides draw `SC.SEAM2[n]`, chop 0) |
|---|---|
| 0 (frame 0) | ep 1's close with the row real: kitchen with every label, cook 2 at the oven, cook 4 at the appliance, knife (hero) with cook 3; "waiting → threads"; below, the small row of four kitchens with "running Python → processes" above it |
| 1→2 | same |
| 2→3 | + the price tag on the row (lands on "costs") |
| 3→4 | the kitchen gone; the row big with "kitchens / processes", four knives magenta (one group), all chopping at the cut's hold; code card `DataLoader(ds, num_workers=4)` |
| 4→5 | row still (chop 0, knives ink); the wall and the pipe between kitchens 2 and 3, "wall / separate memory"; the bowl unboxed on kitchen 3's counter; timer bar at 0.55 |
| 5→6 | wall label gone; the fridge with "fridge / shared memory", the bowl on shelf 3 (magenta "3"); the note "shelf 3" (hero) at kitchen 3's counter |
| end | same, note dim, knives magenta again, cooks chopping to the hold; the three label pairs are the takeaway |
