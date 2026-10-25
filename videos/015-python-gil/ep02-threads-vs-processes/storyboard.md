ENGINE: hyperframes

# Multithreading vs multiprocessing in Python (series ep 2 of 2): storyboard (v1, VO draft for Chris)

THE QUESTION: "Multithreading vs multiprocessing in Python: which one do I use?"
WHO IS ASKING: a Python engineer who now knows the GIL exists (ep 1) and
has a real job to speed up.
THE ANSWER IN ONE SENTENCE: threads for work that waits, processes for
work that is Python; everything that crosses between processes is copied,
so big data goes in shared memory.
THE SEARCH PHRASE: multithreading vs multiprocessing python (checked
10/25; first autocomplete; "…vs asyncio python" and "…interview questions"
also offered, so name asyncio in the description).

**One idea:** pick by the kind of work, then watch what crosses the boundary.

**Engine:** HyperFrames, same box and token as ep 1 plus the process row
and the shared-memory slab (`../SERIES.md`).

## VO (draft: 145 words without the *(if time)* beats, 162 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Threads for waiting, processes for Python work. That's the whole rule for multithreading versus multiprocessing in Python. | Frame 0: left, the interpreter box with four lanes and its one magenta lock; right, the process row of four boxes. Labels "waiting" and "Python work" under each. |
| 02_threads | Threads share one interpreter and one lock, and they all see the same memory. | The box alone, enlarged; a small shared-memory slab under it that all four lanes point into. The token in lane 1. |
| 03_waits | When the work is waiting, a request, a file, a database, threads overlap the waits and you get the speedup. | Lanes 2–4 become request / file / database lanes with clock glyphs; the token hops to whichever lane has Python to run; a timer bar fills fast. |
| 04_python | When the work is Python, threads just take turns on the lock. You get one core's worth, with extra bookkeeping. | All four lanes become Python lanes; the token hops in turn; the timer bar fills at the one-lane rate. A "1 core" tag. |
| 05_processes | Processes each get their own interpreter and their own lock. Eight processes, eight cores, really in parallel. | The process row, eight small boxes, each with its own token, all bright; the timer bar fills eight times faster. Hero passes to the row of tokens. |
| 06_boundary | The price is the boundary. Every result is pickled and copied across. Send a big array and the copy can cost more than the work. | Thick boundary line between two boxes; a large array slides across and a full copy appears; the timer bar stalls while it copies. |
| 07_shared | That's why data loaders run workers as processes and keep big tensors in shared memory: the pipe only carries a pointer. | The shared-memory slab appears under the process row; the array drops into the slab once; across the boundary goes only a tiny tag (a pointer). Timer bar resumes. (Evidence beat; Zephon's process runner, `../SERIES.md`.) |
| 08_asyncio *(if time)* | If the work is all waiting, asyncio does it on one thread, no lock fights at all. | The box with a single lane and a loop arrow; the other lanes gone. |
| 09_close | So: waiting, threads. Python work, processes. Big data crossing, shared memory. | Final visual: the three labels under the three images (box / row / slab). Takeaway only, no outro. |

Line 1 lands the rule in its first clause and says the search phrase.
Beat 08 is the *(if time)* cut; 06 and 07 are the "how", they stay.

## Layout

- Stage top-middle: the interpreter box (beats 2–4) / the process row
  (5–7), ~5 rows.
- Stage bottom-middle: the shared-memory slab and the timer bar.
- One magenta hero at a time: the lock token, then the row of tokens as one
  group, then the pointer tag in beat 7.
