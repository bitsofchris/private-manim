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
- [x] ep 1 built 2026-10-29 (6 beats, every cut 0–4/255), assembled 46.1 s; Chris: "the animations are awful" (20 s of one cook wagging a fat knife). Rebuilt the same day on kit v2 (`_kit/kitchen.js`: the scene builds up, a Python panel turns code into a thread timeline, a chef's knife slices carrots; `ep01-the-gil/storyboard.md` v4, frames approved from `00_layout/proto.png`), every cut 0–4/255, assembled `ep01-the-gil/media/short.mp4` 46.1 s. Chris: "much better"; same day added the round trip (the oven dings, cook 2 gets the knife back, Thread 2 magenta again; beat 4/5 cut moved to 32.30) and a running second kitchen with its own four threads at the close (panel splits into process 1 / process 2); cuts 0–4/255 except 5→6 at 45/255 on 245 knife-edge pixels (antialiasing, state identical); 10/31: shrink moved to just before "second kitchen", panel box taller; Chris: "episode 1 is good". `ep01-the-gil/publish.md` written (titles, description, Substack note), hand-off pack sent 2026-10-31; [x] published (handed off; [ ] day-10 read)
- [x] ep 2 built 2026-10-29 (6 beats, every cut 1–4/255) on kit v1 (`_kit/kitchen_v1.js`); [x] redone on kit v2 2026-10-31 (`storyboard.md` v4, frames approved from `00_layout/proto.png`: a 2×2 grid of kitchens, wall and pipe, the bowl crated through it, the fridge with shelf 3 and the note, the panel as processes; six beats, every cut 0–7/255), assembled `ep02-threads-vs-processes/media/short.mp4` 58.5 s; Chris: "Publish ep 2"; `publish.md` written, hand-off pack sent 2026-10-31; [x] published (handed off; [ ] day-10 read)

## Update pass (step 11), collected from the beat agents of both episodes

- Kit helpers every beat rewrote: `swap(t, land, from, to)` for slot and title (out 0.15 s, in 0.2 s landing on the word); `hopKnife(t, from, to, t0)`; `pathAlong(points, u)` for the bowl and note over `SC.BOWL` waypoints; a `pulse` whose width clamps to a hold; `cooksPatch`; a cook walk as one field (`walkTo`) instead of the `at`/`u` flip.
- Kit drawing: `pulse.py` is nearly invisible (fill-opacity 0.9 → 1), give it a scale or tint; per-bar alpha in `panel.rows` so a split → unsplit can fade bars; the fridge's shelves pop at `draw` 1, fade them over the last 10 %; a small-kitchen "arriving" builder (draw in, then the cook walks in) since `ONE` is the arrived state only; `holds` should need an integer holder (mid-hop the middle cook brightens); `ghost.draw`-style draw-in for every box; a note that `rotation_pivot_drift` is expected.
- Kit states: give `SEAM2[5]` `close.panel: 1` (no visual effect while a/b/c are 0) so 06_close needs no `t > 0` guard.
- Tools: `hf_state_check` should treat `b <= a` bars as absent; `seam_check.py` crashes when two agents run it at once (one run after all renders); float cue sums miss a hold boundary by 1e-15 (write the constant).
- Docs: storyboard cue tables should quote `words.json` times, not the caption's first word (ep 2 row 1 listed 1.04 / 3.36 where the words are 1.20 / 3.42); the brief should say that "unpickled" lands on the word "again." (10.54); `tighten_vo --noise auto` lesson for the runbook (from ep 1 v1).
