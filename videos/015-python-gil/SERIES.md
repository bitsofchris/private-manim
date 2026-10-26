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
**How it works:** one recurring image (the interpreter box with its one
lock) carries both episodes; ep 2 adds the process boundary. One engine,
HyperFrames, for every beat.

## Who it is for, the promise

A Python engineer who added `threading` to a slow loop, saw no speedup,
and doesn't know why. Knows what a thread is; has never read about the
interpreter. **Promise:** the GIL is one lock per interpreter, so threads
only help when the work is waiting; for Python work, use processes, and
mind what crosses the boundary.

## The episodes

| # | Title | Their question | The answer | What they do after |
|---|---|---|---|---|
| 1 | `Every Python dev needs this (Python GIL explained)` (hook) / `Python GIL Explained (Beginner Friendly)` (search) | What is the Python GIL and why don't my threads run in parallel? | One lock per interpreter: only the thread holding it runs Python; threads overlap waiting, never Python work. | When threads don't help, ask: is the work waiting, or running Python? |
| 2 | `Most Python devs get this wrong (multithreading vs multiprocessing python)` (hook) / `Multithreading vs Multiprocessing Python (Made Simple)` (search) | Threads or processes: which one do I use? | Threads for waiting, processes for Python work; everything crossing between processes is copied, so big data goes in shared memory. | Pick by the kind of work, then watch what crosses the boundary. |

## Search phrases (checked 2026-10-25, YouTube autocomplete)

- ep 1: **python gil explained** (offered; "python gil" too). Results are
  the Tech With Tim and ArjanCodes explainers, Beazley's talk: on topic.
- ep 2: **multithreading vs multiprocessing python** (offered first; also
  "…vs asyncio python" and "…interview questions", so say "asyncio" once
  in the description).

## The two images (same in both episodes)

- **The interpreter box:** one rounded box, label "one interpreter", with
  thread lanes inside it (ep 1: four; ep 2: four) and **one lock token**
  (magenta, the hero) that sits in exactly one lane at a time. A lane
  without the lock is dim and waits. Native/IO lanes show a small
  "waiting" glyph (a clock) while the lock is elsewhere.
- **The process row:** several interpreter boxes side by side, each with
  its own lock; between them a thick boundary line with a copy arrow
  (ep 2 only). Shared memory is a slab under the boxes that the arrow
  points into instead of across.

## Evidence (one beat at most)

The Zephon post (DatologyAI, 2026): its process runner moves CPU-bound
Python off the GIL onto separate processes and keeps large tensors in
shared memory so the IPC pipe carries only small metadata; its thread
runner suits I/O and native code that releases the GIL. Used in ep 2
beat 7 only. Not the spine.

## Checklist

- [ ] ep 1 VO edited by Chris, recorded
- [ ] ep 2 VO edited by Chris, recorded
- [ ] ep 1 built, assembled, published
- [ ] ep 2 built, assembled, published
