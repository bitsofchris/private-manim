# The Python GIL: the series (two Shorts)

**Name:** python-gil-series
**Description:** Two Shorts for anyone writing Python: what the GIL is, in
one picture you can keep, and the rule for threads vs processes that
follows from it. Dispatched from Chris's 2026-10-24 note (`zzz short:`),
storyboarded 2026-10-25. **Status: VO is a draft in Chris's voice, for
him to edit before recording** (the source block had one sentence of his;
the runbook says Chris edits the VO in his words).
**When to use:** one session per episode, `agents/runbook.md` from step 2
(record) in the episode folder. Step 0–1 are done here.
**How it works:** one recurring image (one kitchen, one knife) carries
both episodes, and every kitchen beat lands on the real term in the same
breath (knife → GIL, oven → I/O). Ep 1 stops at the diagnostic (is the
thread waiting or running Python?); ep 2 owns processes, the pickling
cost, and shared memory. One engine, HyperFrames, for every beat.
Free-threaded Python is cut from both (opt-in build, not usable yet).

## Who it is for, the promise

A Python engineer who added `threading` to a slow loop, saw no speedup,
and doesn't know why. Knows what a thread is; has never read about the
interpreter. **Promise:** the GIL is one knife in one kitchen, so threads
only help when the cook is waiting; for chopping, use processes, and
mind what passes between kitchens.

## The episodes

| # | Title | Their question | The answer | What they do after |
|---|---|---|---|---|
| 1 | `Every Python dev needs this (Python GIL explained)` (hook) / `Python GIL Explained (Beginner Friendly)` (search) | What is the Python GIL and why don't my threads run in parallel? | One lock per interpreter: only the thread holding it runs Python; threads overlap while waiting (I/O, native code), never while running Python. | When threads don't help, ask: is the thread waiting, or running Python? Running Python → ep 2. |
| 2 | `Most Python devs get this wrong (multithreading vs multiprocessing python)` (hook) / `Multithreading vs Multiprocessing Python (Made Simple)` (search) | Threads or processes, and what does a process cost me? | Threads for waiting, processes for Python work; everything crossing between processes is pickled and copied, so big data goes in shared memory. | Pick by the kind of work, then keep big data out of the pipe. |

## Search phrases (checked 2026-10-25, YouTube autocomplete)

- ep 1: **python gil explained** (offered; "python gil" too). Results are
  the Tech With Tim and ArjanCodes explainers, Beazley's talk: on topic.
- ep 2: **multithreading vs multiprocessing python** (offered first; also
  "…vs asyncio python" and "…interview questions", so say "asyncio" once
  in the description).

## The image (Chris's chat, 2026-10-26: one kitchen, one knife; code: `_kit/kitchen.js`, seam states `SC.SEAM1` / `SC.SEAM2`)

- **The kitchen** is a process: a rounded box with a counter, four
  line-drawn cooks (`videos/_shared/web/cast/cast.js` humans), an oven on
  the right (waiting: disk, network) and a small appliance on the left
  (native code that releases the lock: numpy, a tokenizer).
- **The knife** is the GIL, the one magenta hero: one token, in exactly
  one cook's hand at a time. The holder chops; the others are dim, with a
  clock glyph when they are waiting at the oven.
- **The row of kitchens** is processes: several boxes, each with its own
  cook and its own knife; a thick wall between them with a pipe, through
  which a bowl travels boxed ("pickle").
- **The fridge** is shared memory: a slab under the row that the bowl goes
  into once; across the wall travels only a note ("shelf 3").
- **Every label shows both names** (`knife / GIL`, `oven / I/O`), so the
  analogy never floats free of the real thing (Chris, 10/27).

## Evidence (one beat at most)

The Zephon post (DatologyAI, 2026): its process runner moves CPU-bound
Python off the GIL onto separate processes and keeps large tensors in
shared memory so the IPC pipe carries only small metadata; its thread
runner suits I/O and native code that releases the GIL. Used in ep 2
beat 7 only. Not the spine.

## Checklist

- [x] ep 1 VO recorded 2026-10-28 (`ep01-the-gil/script.md`), cut, 46.1 s
- [x] ep 2 VO recorded 2026-10-28 (`ep02-threads-vs-processes/script.md`), cut, 58.5 s (cut list for Chris)
- [x] kit `_kit/kitchen.js` (both episodes' seam states) and `00_layout/` per episode (canonical frame for Chris)
- [ ] ep 1 built, assembled, published
- [ ] ep 2 built, assembled, published
