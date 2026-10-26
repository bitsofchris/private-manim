ENGINE: hyperframes

# Multithreading vs multiprocessing in Python (series ep 2 of 2): storyboard (v2, kitchen image, VO draft for Chris)

THE QUESTION: "Multithreading vs multiprocessing in Python: which one do I use?"
WHO IS ASKING: a Python engineer who now knows the GIL exists (ep 1) and
has a real job to speed up.
THE ANSWER IN ONE SENTENCE: threads for work that waits, processes for
work that is Python; everything that crosses between processes is copied,
so big data goes in shared memory.
THE SEARCH PHRASE: multithreading vs multiprocessing python (checked
10/25; first autocomplete; "…vs asyncio python" and "…interview questions"
also offered, so name asyncio in the description).

**Titles (runbook step 9, Chris picks):** search `Multithreading vs Multiprocessing Python (Made Simple)` · hook `Most Python devs get this wrong (multithreading vs multiprocessing python)` (Chris's preference, 10/26).

**One idea:** pick by the kind of work (waiting or chopping), then watch what crosses between kitchens.

**Engine:** HyperFrames, the same kitchen, cooks and knife as ep 1 plus the
row of kitchens, the wall with the pipe, and the fridge (`../SERIES.md`).

## VO (draft: 154 words without the if-time beat, 166 with; the kitchen-and-knife image from Chris's chat, 10/26)

| beat | VO | visual |
|---|---|---|
| 01_hook | Threads for waiting, processes for chopping. That's the rule for multithreading versus multiprocessing in Python. | Frame 0: left, one kitchen with four cooks and the magenta knife; right, a row of four kitchens. Labels "waiting" and "chopping" under each. |
| 02_kitchen | Threads are cooks in one kitchen. They share every counter, so handing off data is free. But there's one knife. | The single kitchen enlarged; a shared counter (slab) under the cooks that a bowl slides along for free. The token in cook 1's hand. |
| 03_waiting | When the work is waiting, a request, a file, the oven, the cook puts the knife down and another picks it up. Threads win. | An oven and a "network" cloud; cook 2 sets the knife down at the oven, the token jumps to cook 3; a timer bar under the kitchen fills fast. |
| 04_chopping | When the work is Python, the cooks take turns on the knife. Ten threads, one core's worth of chopping. | All four cooks at the counter with bowls; the token hops in turn; the timer bar fills at the one-cook rate; a "1 core" tag. |
| 05_processes | Processes are separate kitchens, each with its own knife, so Python really runs in parallel. PyTorch's DataLoader workers are processes. | The row of kitchens, eight small ones, each with a cook and its own knife, all chopping; a code card bottom-middle: `DataLoader(ds, num_workers=8)`. Hero passes to the row of knives. |
| 06_containers | The cost: kitchens don't share counters. Every result gets boxed, piped, unboxed. For a big array, the boxing can cost more than the cooking. | A thick wall between two kitchens; a large bowl is boxed ("pickle"), squeezed through a pipe, unboxed; the timer bar stalls while it travels. |
| 07_fridge | The fix is a shared fridge: big tensors go in shared memory, and you pass a note that says shelf 3. | A fridge slab under the row of kitchens; the bowl goes into the fridge once; across the wall goes only a small note ("shelf 3"); the timer bar resumes. (Evidence beat: Zephon's process runner, `../SERIES.md`.) |
| 08_asyncio *(if time)* | All waiting and nothing else? Use asyncio: one cook, no knife fights. | One kitchen, one cook, a loop arrow over the oven and the cloud; the other cooks gone. |
| 09_close | Waiting, threads. Chopping, processes. Big food between kitchens, the shared fridge. | Final visual: kitchen, row of kitchens, fridge, each with its label. Takeaway only, no outro. |
Line 1 lands the rule in its first clause and says the search phrase.
Beat 08 is the *(if time)* cut; 06 and 07 are the "how", they stay.

## Layout

- Stage top-middle: the kitchen (beats 2–4) / the row of kitchens (5–7),
  ~5 rows.
- Stage bottom-middle: the shared counter, the fridge, the timer bar, the
  code card in beat 5.
- One magenta hero at a time: the knife, then the row of knives as one
  group, then the note ("shelf 3") in beat 7.
